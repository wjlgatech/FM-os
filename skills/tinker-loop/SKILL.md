---
name: tinker-loop
description: >-
  Post-training through fine-tuning-service primitives, with gates: the Tinker
  API mental model (forward_backward / optim_step / sample / save_state + LoRA
  on a frozen base) implemented keylessly in pure numpy, composed into SFT and
  DPO recipes that are judged by held-out gates — domain gain, no catastrophic
  forgetting, preference-margin flip — with honest ship/rollback. Cookbook
  recipes you can run in CI before spending a dollar of GPU credit.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# tinker-loop

A cross-runtime skill that teaches (and lets an agent verify) how modern
fine-tuning-service APIs work — Thinking Machines'
[Tinker](https://thinkingmachines.ai/tinker/) being the reference design — by
running the whole loop locally with zero keys, zero GPUs, and numpy only.

The core insight of Tinker's design: every post-training algorithm (SFT, DPO,
RLHF, custom RL) is a composition of **four primitives** — `forward_backward`,
`optim_step`, `sample`, `save_state` — over **LoRA adapters on a frozen
open-weights base**. This skill ships that exact API surface at laptop scale,
plus the FM-os addition: **eval gates with teeth** on every recipe.

## When to use (trigger)

Invoke when the user says "fine-tune with Tinker", "how does a fine-tuning API
work", "forward_backward / optim_step / training primitives", "write a
post-training recipe", "test my fine-tuning pipeline without GPU credits",
"cookbook recipe with an eval gate", or asks how SFT/DPO compose from
low-level training-client calls. Also activates when designing or reviewing
the developer experience of a training API or SDK.

## What it does

1. **Teach the API shape** — a `LocalTrainingClient` with the same surface as
   Tinker's: `forward_backward(batch, loss_fn)` accumulates adapter gradients,
   `optim_step()` applies Adam and clears them, `save_state()`/`load_state()`
   checkpoint, `save_weights_and_get_sampling_client().sample(...)` generates.
   Base weights are frozen; only the rank-r LoRA pair (A, B) trains — verified
   by test, not asserted by prose.
2. **Compose recipe 1: SFT** — cross-entropy `forward_backward` + `optim_step`
   on a domain corpus.
3. **Compose recipe 2: DPO** — `loss_fn="dpo"` computes the DPO objective
   against the frozen base as reference policy, through the same two calls.
4. **Gate everything (held-out, no evidence ⇒ No)** —
   G1 domain NLL must improve ≥15%; G2 generic NLL may regress ≤10%
   (catastrophic-forgetting gate); G3 preference margin must flip positive.
   SHIP only if all gates pass, else ROLLBACK with exit 1.
5. **Show the gate has teeth both ways** — the demo runs the classic user
   mistake (domain-only SFT) and gets honestly ROLLED BACK (+208% forgetting),
   then the standard fix (replay mixing) and SHIPs. A gate that never fails
   anything is decoration.
6. **Graduate to the real service** — swap `LocalTrainingClient` for the real
   `tinker` client and the loops, gates, and rollback transfer unchanged; the
   [tinker-cookbook](https://github.com/thinking-machines-lab/tinker-cookbook)
   (Apache-2.0) provides the production recipes this mirrors.

## Example

```bash
cd reference/
python tinker_local.py       # both recipes + gates, deterministic, < 2 s, exit 0 iff honest
python test_tinker_local.py  # 7 gates: frozen base, LoRA-zero init, loss ↓, DPO margin ↑,
                             # checkpoint roundtrip, greedy determinism, teeth-both-ways
pytest test_tinker_local.py -q   # same suite under pytest / codex / hermes runners
```

## Measured proof (deterministic, seed 7)

| Recipe | held-out domain NLL | held-out generic NLL | DPO margin | Verdict |
|---|---|---|---|---|
| base | 2.722 | 2.575 | −0.148 | — |
| naive (domain-only SFT) | 1.980 (+27.2%) | 7.930 (**+208% — G2 ❌**) | +5.936 | **ROLLBACK** |
| replay (pretrain mixing) | 1.929 (+29.1%) | 2.270 (−11.9% ✅) | +0.355 ✅ | **SHIP** |

## Discipline (why this is trustworthy)

- **Keyless by construction** — no API keys, no network, no GPU; the recipe is
  verifiable in CI on every commit, which is the DX bar a cookbook example
  should meet before it asks a user for credit.
- **Gates are held-out and pre-registered** — thresholds live at the top of
  the file, judged on data the loop never trains on; an honest ❌ (the naive
  attempt) is part of the shipped artifact.
- **Same shape as production** — the primitives, the frozen-base/LoRA split,
  the gradient-accumulate-then-step semantics, and the sampling-client
  handoff all mirror the public Tinker API design, so the mental model
  transfers rather than expires.

## Deeper reference (FM-os knowledge base)

- [Tinker](https://thinkingmachines.ai/tinker/) · [Announcing Tinker](https://thinkingmachines.ai/news/announcing-tinker/) · [tinker-cookbook](https://github.com/thinking-machines-lab/tinker-cookbook) — the reference fine-tuning service + its Apache-2.0 recipe library
- `skills/slm-quickstart` — the same lifecycle with real models (LoRA/QLoRA → DPO/GRPO → GGUF → serve)
- `skills/product-rl-loop` — preference signal → DPO update → held-out judge → ship/rollback, at product scale
- `labs/rewardforge` — real LoRA-DPO on SmolLM2-135M with the same honest-rollback discipline (held-out hallucination 0.398 → 0.287, bad-lr attempt rolled back)
- TRL / OpenRLHF / verl / PEFT / Unsloth — curated in `data/repos.yml` for when the toy graduates
