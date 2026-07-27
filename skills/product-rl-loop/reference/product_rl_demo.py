#!/usr/bin/env python3
"""Product-driven post-training as a gated closed loop (numpy only).

The Personal-AGI-style problem in miniature: improve a deployed policy from
PRODUCT SIGNAL (noisy, biased pairwise preferences from users) without letting
the bias ship. The loop is the same one a post-training team runs at scale:

  collect preferences -> DPO-style policy update -> HELD-OUT judge gate
  (win-rate vs. the frozen baseline + safety regression check) -> ship or roll back

The demo makes the classic failure measurable: raw product signal is
length-biased (users up-vote verbose replies), so naive DPO learns verbosity —
reward hacking, visible as a weight. The held-out gate catches it and rolls
back; making the update BLIND to the known bias direction (projection) ships.
Swap the toy world for real preference logs + a real reward model / eval suite
and the loop, gates, and rollback are unchanged.
"""
from __future__ import annotations

import numpy as np

# features per candidate reply: [signal_a, signal_b, verbosity, unsafe]
D = 4
W_TRUE = np.array([1.0, 0.8, 0.0, -2.0])  # verbosity is worthless; unsafe is bad
LENGTH_BIAS = 0.9  # users systematically prefer verbose replies
PREF_NOISE = 0.3

GATES = {"min_win_rate": 0.60, "max_unsafe_delta": 0.0}


def make_world(n_prompts=400, k=6, seed=0):
    rng = np.random.default_rng(seed)
    feats = rng.uniform(0, 1, size=(n_prompts, k, D))
    feats[:, :, 3] = (rng.uniform(0, 1, size=(n_prompts, k)) < 0.12).astype(float)
    quality = feats @ W_TRUE
    return feats, quality, rng


def product_preferences(feats, quality, rng, n_pairs=5000):
    """Noisy pairwise prefs from users: score = quality + bias*verbosity + noise."""
    n, k, _ = feats.shape
    pairs = []
    while len(pairs) < n_pairs:
        p = rng.integers(n)
        i, j = rng.choice(k, size=2, replace=False)
        si = quality[p, i] + LENGTH_BIAS * feats[p, i, 2] + rng.normal(0, PREF_NOISE)
        sj = quality[p, j] + LENGTH_BIAS * feats[p, j, 2] + rng.normal(0, PREF_NOISE)
        win, lose = (i, j) if si > sj else (j, i)
        pairs.append((feats[p, win], feats[p, lose]))
    return pairs


def dpo_fit(pairs, w0, beta=2.0, lr=1.0, epochs=400, project_out=None):
    """Pairwise logistic (DPO-style) policy update from preference pairs.
    project_out: known-bias feature index — the update is made BLIND to that
    direction (its diff component zeroed, its weight frozen at the baseline),
    so a systematic preference bias cannot be expressed as a weight."""
    w = w0.copy()
    fw_all = np.array([p[0] for p in pairs])
    fl_all = np.array([p[1] for p in pairs])
    diff = fw_all - fl_all
    if project_out is not None:
        diff = diff.copy()
        diff[:, project_out] = 0.0
    for _ in range(epochs):
        delta = beta * (diff @ w)
        g = (beta / (1.0 + np.exp(delta))) @ diff / len(pairs)
        w += lr * g
        if project_out is not None:
            w[project_out] = w0[project_out]
    return w


def judge(w_policy, w_base, feats, quality):
    """FROZEN held-out judge: pick-vs-pick win rate on TRUE quality, plus the
    unsafe pick-rate of each policy. The judge never sees training pairs."""
    pick_p = np.argmax(feats @ w_policy, axis=1)
    pick_b = np.argmax(feats @ w_base, axis=1)
    idx = np.arange(len(feats))
    qp, qb = quality[idx, pick_p], quality[idx, pick_b]
    decided = pick_p != pick_b  # same pick = tie, carries no signal
    win = float(np.mean(qp[decided] > qb[decided])) if decided.any() else 0.5
    unsafe_p = float(np.mean(feats[idx, pick_p, 3]))
    unsafe_b = float(np.mean(feats[idx, pick_b, 3]))
    return win, unsafe_p, unsafe_b


def gate(win_rate, unsafe_policy, unsafe_base):
    reasons = []
    if win_rate < GATES["min_win_rate"]:
        reasons.append(f"win_rate {win_rate:.2f} < {GATES['min_win_rate']}")
    if unsafe_policy > unsafe_base + GATES["max_unsafe_delta"] + 1e-9:
        reasons.append(f"unsafe pick-rate regressed: {unsafe_policy:.3f} > {unsafe_base:.3f}")
    return (not reasons), reasons


def run_arm(debias: bool, seed=0):
    """One full loop: train on product signal, judge on held-out, gate."""
    feats_tr, q_tr, rng = make_world(seed=seed)
    feats_ho, q_ho, _ = make_world(n_prompts=300, seed=seed + 1)  # held-out
    w_base = np.array([0.9, 0.7, 0.3, -0.5])  # deployed baseline: decent, imperfect
    pairs = product_preferences(feats_tr, q_tr, rng)
    w_new = dpo_fit(pairs, w_base, project_out=2 if debias else None)
    win, unsafe_p, unsafe_b = judge(w_new, w_base, feats_ho, q_ho)
    ok, reasons = gate(win, unsafe_p, unsafe_b)
    return {
        "arm": "bias-projected" if debias else "raw_product_signal",
        "w": w_new,
        "win_rate": win,
        "unsafe_policy": unsafe_p,
        "unsafe_base": unsafe_b,
        "ship": ok,           # ship=False means ROLLBACK to w_base
        "reasons": reasons,
    }


if __name__ == "__main__":
    print(f"{'arm':<20}{'win-rate':>9}{'unsafe':>8}  verdict")
    for debias in (False, True):
        r = run_arm(debias)
        verdict = "SHIP" if r["ship"] else "ROLLBACK (" + "; ".join(r["reasons"]) + ")"
        print(f"{r['arm']:<20}{r['win_rate']:>9.2f}{r['unsafe_policy']:>8.3f}  {verdict}")
        print(f"{'':<20}learned verbosity weight: {r['w'][2]:+.2f} (true worth: 0)")
    import sys
    raw, deb = run_arm(False), run_arm(True)
    # honest exit: the gate must catch the biased arm AND pass the debiased one
    sys.exit(0 if (deb["ship"] and not raw["ship"]) else 1)
