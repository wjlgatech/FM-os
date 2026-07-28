#!/usr/bin/env python3
"""The Tinker mental model, keyless (numpy only).

Thinking Machines' Tinker exposes FOUR primitives — forward_backward, optim_step,
sample, save_state — and trains LoRA adapters on frozen open-weights models while
the service owns distributed infrastructure. Every post-training algorithm in the
tinker-cookbook (SFT, DPO, RLHF) is a composition of those four calls.

This file is that mental model at 1:1 API shape but laptop scale: a char-bigram
"base model" stands in for the frozen open-weights LLM, a rank-r LoRA delta is the
ONLY thing training touches, and the same client surface composes into both an SFT
loop and a DPO loop. Swap the toy model for the real service client and the loops,
gates, and rollback are unchanged — which is the point: recipes you can run in CI
with zero keys are recipes users can trust before they spend GPU credit.

The FM-os addition is gates with teeth (no evidence => No):
  G1 domain-gain      held-out domain NLL must improve >= 15% over the base model
  G2 no-forgetting    held-out GENERIC NLL may regress <= 10% (catastrophic-forgetting gate)
  G3 dpo-margin       held-out preference margin must flip in favor of chosen vs. base
SHIP only if all gates pass; otherwise ROLLBACK and exit non-zero.

Run:  python tinker_local.py        (deterministic, < 2 s, numpy only)
Test: pytest test_tinker_local.py -q
"""
from __future__ import annotations

import sys

import numpy as np

SEED = 7
RANK = 4  # LoRA rank r
ALPHA = 8.0  # LoRA scaling alpha; delta = (alpha/r) * A @ B
BETA_DPO = 1.0  # DPO temperature

GATES = {"min_domain_gain": 0.15, "max_generic_regress": 0.10, "min_dpo_margin_flip": 0.0}

# ── corpora (pretrain = generic; domain = the fine-tune target style) ─────────
PRETRAIN = [
    "the quick brown fox jumps over the lazy dog",
    "a journey of a thousand miles begins with a single step",
    "all that glitters is not gold and all who wander are not lost",
    "to be or not to be that is the question",
    "the early bird catches the worm but the second mouse gets the cheese",
    "actions speak louder than words in every language",
]
DOMAIN_TRAIN = [
    "verify then ship: the gate must be green",
    "no evidence means no: the gate must be green",
    "measure the loss then ship or roll back",
    "the held out gate must be green before we ship",
    "ship only what the gate can verify",
]
DOMAIN_HELDOUT = [
    "the gate must verify before we ship",
    "roll back when the held out gate is not green",
]
GENERIC_HELDOUT = [
    "the lazy dog jumps over the quick brown fox",
    "a single step begins the journey of a thousand miles",
]
# preference pairs: chosen = gated-loop style, rejected = generic style
PREF_TRAIN = list(zip(DOMAIN_TRAIN, PRETRAIN[: len(DOMAIN_TRAIN)]))
PREF_HELDOUT = list(zip(DOMAIN_HELDOUT, GENERIC_HELDOUT))

VOCAB = sorted(set("".join(PRETRAIN + DOMAIN_TRAIN + DOMAIN_HELDOUT + GENERIC_HELDOUT)))
C2I = {c: i for i, c in enumerate(VOCAB)}
V = len(VOCAB)


def _pretrain_base() -> np.ndarray:
    """The frozen 'open-weights base model': log of add-1-smoothed bigram counts."""
    counts = np.ones((V, V))
    for s in PRETRAIN:
        for a, b in zip(s, s[1:]):
            counts[C2I[a], C2I[b]] += 1.0
    return np.log(counts / counts.sum(axis=1, keepdims=True))


def _log_softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - logits.max(axis=-1, keepdims=True)
    return z - np.log(np.exp(z).sum(axis=-1, keepdims=True))


class LocalTrainingClient:
    """Same surface as Tinker's TrainingClient: forward_backward / optim_step /
    save_state / save_weights_and_get_sampling_client. Base weights are FROZEN;
    only the LoRA pair (A, B) ever receives gradient — exactly Tinker's contract."""

    def __init__(self, base: np.ndarray, rng: np.random.Generator) -> None:
        self.base = base  # frozen
        self.A = rng.normal(scale=0.01, size=(V, RANK))
        self.B = np.zeros((RANK, V))  # delta starts at exactly 0 (LoRA convention)
        self._gA = np.zeros_like(self.A)
        self._gB = np.zeros_like(self.B)
        self._m: dict[str, np.ndarray] = {}
        self._v: dict[str, np.ndarray] = {}
        self._t = 0

    # ── model math ────────────────────────────────────────────────────────────
    def logits(self) -> np.ndarray:
        return self.base + (ALPHA / RANK) * (self.A @ self.B)

    def seq_logprob_and_grad(self, s: str, logp: np.ndarray) -> tuple[float, np.ndarray]:
        """log p(s) and its gradient w.r.t. the logits matrix (per-row softmax grads)."""
        g = np.zeros((V, V))
        total = 0.0
        p = np.exp(logp)
        for a, b in zip(s, s[1:]):
            i, j = C2I[a], C2I[b]
            total += logp[i, j]
            g[i] -= p[i]
            g[i, j] += 1.0
        return total, g

    def _accumulate(self, g_logits: np.ndarray) -> None:
        self._gA += (ALPHA / RANK) * g_logits @ self.B.T
        self._gB += (ALPHA / RANK) * self.A.T @ g_logits

    # ── primitive 1: forward_backward ────────────────────────────────────────
    def forward_backward(self, batch: list, loss_fn: str = "cross_entropy") -> dict:
        """Compute loss on a batch and ACCUMULATE adapter gradients (Tinker semantics:
        gradients accumulate across calls until optim_step applies and clears them)."""
        logp = _log_softmax(self.logits())
        if loss_fn == "cross_entropy":
            n_tok, nll_g = 0, np.zeros((V, V))
            total = 0.0
            for s in batch:
                lp, g = self.seq_logprob_and_grad(s, logp)
                total -= lp
                nll_g -= g
                n_tok += len(s) - 1
            self._accumulate(nll_g / n_tok)
            return {"loss": total / n_tok}
        if loss_fn == "dpo":  # batch = [(chosen, rejected)], vs. frozen base reference
            ref_logp = _log_softmax(self.base)
            g_total, total = np.zeros((V, V)), 0.0
            for chosen, rejected in batch:
                lc, gc = self.seq_logprob_and_grad(chosen, logp)
                lr, gr = self.seq_logprob_and_grad(rejected, logp)
                rc, _ = self.seq_logprob_and_grad(chosen, ref_logp)
                rr, _ = self.seq_logprob_and_grad(rejected, ref_logp)
                z = BETA_DPO * ((lc - lr) - (rc - rr))
                sig = 1.0 / (1.0 + np.exp(-z))
                total += -np.log(max(sig, 1e-12))
                g_total += (sig - 1.0) * BETA_DPO * (gc - gr)  # d(-log sigma(z))/dlogits
            self._accumulate(g_total / len(batch))
            return {"loss": total / len(batch)}
        raise ValueError(f"unknown loss_fn: {loss_fn}")

    # ── primitive 2: optim_step (Adam, adapters only) ─────────────────────────
    def optim_step(self, lr: float = 0.05, b1: float = 0.9, b2: float = 0.999) -> None:
        self._t += 1
        for name, param, grad in (("A", self.A, self._gA), ("B", self.B, self._gB)):
            m = self._m.setdefault(name, np.zeros_like(param))
            v = self._v.setdefault(name, np.zeros_like(param))
            m[:] = b1 * m + (1 - b1) * grad
            v[:] = b2 * v + (1 - b2) * grad**2
            mh = m / (1 - b1**self._t)
            vh = v / (1 - b2**self._t)
            param -= lr * mh / (np.sqrt(vh) + 1e-8)
        self._gA[:], self._gB[:] = 0.0, 0.0

    # ── primitive 3: save_state / load_state ─────────────────────────────────
    def save_state(self, path: str) -> None:
        np.savez(path, A=self.A, B=self.B, t=self._t)

    def load_state(self, path: str) -> None:
        st = np.load(path if path.endswith(".npz") else path + ".npz")
        self.A, self.B, self._t = st["A"], st["B"], int(st["t"])

    # ── primitive 4: sample (via a sampling client, as in the real API) ───────
    def save_weights_and_get_sampling_client(self) -> "LocalSamplingClient":
        return LocalSamplingClient(self.logits().copy())


class LocalSamplingClient:
    def __init__(self, logits: np.ndarray) -> None:
        self.logp = _log_softmax(logits)

    def sample(self, prompt: str, max_tokens: int = 40, temperature: float = 1.0,
               seed: int = SEED) -> str:
        rng = np.random.default_rng(seed)
        out = prompt
        for _ in range(max_tokens):
            row = self.logp[C2I[out[-1]]]
            if temperature == 0.0:
                nxt = int(row.argmax())
            else:
                p = np.exp(row / temperature)
                nxt = int(rng.choice(V, p=p / p.sum()))
            out += VOCAB[nxt]
        return out


def heldout_nll(logits: np.ndarray, corpus: list[str]) -> float:
    logp = _log_softmax(logits)
    total, n = 0.0, 0
    for s in corpus:
        for a, b in zip(s, s[1:]):
            total -= logp[C2I[a], C2I[b]]
            n += 1
    return total / n


def pref_margin(logits: np.ndarray, pairs: list[tuple[str, str]]) -> float:
    """Mean length-normalized held-out margin log p(chosen) - log p(rejected)."""
    logp = _log_softmax(logits)
    margins = []
    for c, r in pairs:
        lc = sum(logp[C2I[a], C2I[b]] for a, b in zip(c, c[1:])) / (len(c) - 1)
        lr = sum(logp[C2I[a], C2I[b]] for a, b in zip(r, r[1:])) / (len(r) - 1)
        margins.append(lc - lr)
    return float(np.mean(margins))


def run_demo(recipe: str = "naive", sft_steps: int = 150, dpo_steps: int = 20) -> dict:
    """SFT recipe + DPO recipe, both as compositions of the four primitives,
    each judged by held-out gates. recipe='naive' trains on domain data only
    (the classic user mistake); recipe='replay' mixes pretrain data back into
    the SFT batch — the standard forgetting mitigation. Returns every number."""
    rng = np.random.default_rng(SEED)
    base = _pretrain_base()
    client = LocalTrainingClient(base, rng)

    base_domain = heldout_nll(base, DOMAIN_HELDOUT)
    base_generic = heldout_nll(base, GENERIC_HELDOUT)
    base_margin = pref_margin(base, PREF_HELDOUT)

    # recipe 1 — SFT: forward_backward(cross_entropy) + optim_step
    sft_batch = DOMAIN_TRAIN + (PRETRAIN if recipe == "replay" else [])
    for _ in range(sft_steps):
        client.forward_backward(sft_batch, loss_fn="cross_entropy")
        client.optim_step(lr=0.05)

    # recipe 2 — gentle DPO on top, against the frozen base as reference
    for _ in range(dpo_steps):
        client.forward_backward(PREF_TRAIN, loss_fn="dpo")
        client.optim_step(lr=0.005)

    tuned = client.logits()
    res = {
        "base_domain_nll": base_domain,
        "tuned_domain_nll": heldout_nll(tuned, DOMAIN_HELDOUT),
        "base_generic_nll": base_generic,
        "tuned_generic_nll": heldout_nll(tuned, GENERIC_HELDOUT),
        "base_pref_margin": base_margin,
        "tuned_pref_margin": pref_margin(tuned, PREF_HELDOUT),
        "base_frozen": True,
    }
    res["domain_gain"] = 1.0 - res["tuned_domain_nll"] / res["base_domain_nll"]
    res["generic_regress"] = res["tuned_generic_nll"] / res["base_generic_nll"] - 1.0
    res["margin_flip"] = res["tuned_pref_margin"] - res["base_pref_margin"]
    res["gates"] = {
        "G1_domain_gain": res["domain_gain"] >= GATES["min_domain_gain"],
        "G2_no_forgetting": res["generic_regress"] <= GATES["max_generic_regress"],
        "G3_dpo_margin": res["margin_flip"] > GATES["min_dpo_margin_flip"],
    }
    res["ship"] = all(res["gates"].values())
    res["client"] = client
    return res


def _report(name: str, res: dict) -> None:
    print(f"attempt: {name}")
    print(f"  SFT   held-out domain NLL  {res['base_domain_nll']:.3f} -> "
          f"{res['tuned_domain_nll']:.3f}  (gain {res['domain_gain']:+.1%})")
    print(f"  SFT   held-out generic NLL {res['base_generic_nll']:.3f} -> "
          f"{res['tuned_generic_nll']:.3f}  (regress {res['generic_regress']:+.1%})")
    print(f"  DPO   held-out pref margin {res['base_pref_margin']:+.3f} -> "
          f"{res['tuned_pref_margin']:+.3f}  (flip {res['margin_flip']:+.3f})")
    for gate, ok in res["gates"].items():
        print(f"  {'✅' if ok else '❌'} {gate}")
    print(f"  verdict: {'SHIP' if res['ship'] else 'ROLLBACK'}")


def main() -> int:
    print("tinker-loop — four primitives, two recipes, three gates (numpy, keyless)")
    naive = run_demo("naive")  # the classic user mistake: domain-only SFT
    _report("naive (domain-only SFT)", naive)
    replay = run_demo("replay")  # the standard fix: mix pretrain data back in
    _report("replay (SFT with pretrain mixing)", replay)
    sample = replay["client"].save_weights_and_get_sampling_client().sample("the g", 30, 0.0)
    print(f"  sample(greedy): {sample!r}")
    # the demo's promise: the gate catches the bad recipe AND passes the good one
    honest = (not naive["ship"]) and replay["ship"]
    print(f"gate-has-teeth check: naive ROLLBACK + replay SHIP -> {'✅' if honest else '❌'}")
    return 0 if honest else 1


if __name__ == "__main__":
    sys.exit(main())
