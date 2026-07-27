#!/usr/bin/env python3
"""Personalization with memory, as a gated closed loop (numpy only).

The Personal-AGI question in miniature: does per-user MEMORY actually pay
rent? A personalized policy keeps one small memory per user (an online
estimate of their preferences, updated only from that user's own feedback)
and must beat a stateless global policy — under four gates:

  lift        mean per-user reward must beat the stateless baseline
  cold-start  a brand-new user must never be served WORSE than the baseline
  isolation   user A's behavior must be bit-identical whether or not user B
              exists (no cross-user leakage, by construction and by test)
  rent        the memory CONTENT must drive the lift: serving user A with
              user B's memory must underperform the stateless baseline

Swap the linear toy for a real reranker/model-choice layer and the gates are
unchanged — this is the eval harness personalization ships through.
"""
from __future__ import annotations

import numpy as np

D = 4              # response style features (e.g. brevity, formality, depth, emoji)
N_USERS = 24
SESSIONS = 30      # feedback rounds per user
K = 8              # candidate responses per session
FEEDBACK_NOISE = 0.25

GATES = {"min_lift": 0.10, "max_cold_start_deficit": 0.0, "max_leakage": 0.0}


def population(seed=0):
    rng = np.random.default_rng(seed)
    prefs = rng.normal(0, 1, size=(N_USERS, D))          # hidden per-user taste
    prefs /= np.linalg.norm(prefs, axis=1, keepdims=True)
    global_mean = prefs.mean(axis=0)
    return prefs, global_mean, rng


def user_stream(rng_seed, sessions=SESSIONS, k=K):
    """Deterministic per-user candidate stream — seeded ONLY by the user's own
    id, so no other user's existence can perturb it (isolation by design)."""
    rng = np.random.default_rng(10_000 + rng_seed)
    return rng.uniform(-1, 1, size=(sessions, k, D)), rng


def run_user(pref, user_id, global_mean, personalized=True, memory_override=None):
    """One user's lifetime. Returns per-session TRUE reward of the served pick."""
    cands, rng = user_stream(user_id)
    memory = global_mean.copy() if memory_override is None else memory_override.copy()
    rewards = []
    for t in range(cands.shape[0]):
        scores = cands[t] @ (memory if personalized else global_mean)
        pick = int(np.argmax(scores))
        true_r = float(pref @ cands[t, pick])
        rewards.append(true_r)
        if personalized and memory_override is None:
            feedback = true_r + rng.normal(0, FEEDBACK_NOISE)  # user's own signal only
            memory += 0.15 * (feedback - memory @ cands[t, pick]) * cands[t, pick]
    return np.array(rewards)


def run_cohort(seed=0):
    prefs, global_mean, _ = population(seed)
    stateless = np.array([run_user(prefs[u], u, global_mean, personalized=False)
                          for u in range(N_USERS)])
    personal = np.array([run_user(prefs[u], u, global_mean, personalized=True)
                         for u in range(N_USERS)])
    # rent check: serve each user with their NEIGHBOR's converged taste estimate
    wrong = np.array([
        run_user(prefs[u], u, global_mean, personalized=True,
                 memory_override=prefs[(u + 1) % N_USERS])
        for u in range(N_USERS)
    ])
    lift = float(personal[:, SESSIONS // 2:].mean() - stateless[:, SESSIONS // 2:].mean())
    cold_start_deficit = float(stateless[:, 0].mean() - personal[:, 0].mean())
    wrong_memory_delta = float(wrong.mean() - stateless.mean())
    return {
        "lift": lift,
        "cold_start_deficit": cold_start_deficit,
        "wrong_memory_delta": wrong_memory_delta,
        "personal": personal,
        "stateless": stateless,
    }


def leakage(seed=0):
    """Bit-level isolation: user 0's trajectory served ALONE must be identical
    to their trajectory served amid the full cohort. Guards against anyone
    later introducing shared state (a global memory, cross-user cache, …)."""
    prefs, global_mean, _ = population(seed)
    alone = run_user(prefs[0], 0, global_mean, personalized=True)
    amid_cohort = [run_user(prefs[u], u, global_mean, personalized=True)
                   for u in range(N_USERS)][0]
    return float(np.max(np.abs(alone - amid_cohort)))


def gate_cohort(r, leak):
    reasons = []
    if r["lift"] < GATES["min_lift"]:
        reasons.append(f"lift {r['lift']:.3f} < {GATES['min_lift']}")
    if r["cold_start_deficit"] > GATES["max_cold_start_deficit"] + 1e-9:
        reasons.append(f"cold-start served worse than baseline by {r['cold_start_deficit']:.3f}")
    if leak > GATES["max_leakage"]:
        reasons.append(f"cross-user leakage detected: {leak}")
    if r["wrong_memory_delta"] >= 0:
        reasons.append("wrong-user memory did NOT hurt — the memory isn't paying rent")
    return (not reasons), reasons


if __name__ == "__main__":
    import sys

    r = run_cohort()
    leak = leakage()
    ok, reasons = gate_cohort(r, leak)
    print(f"personalization lift (late sessions): {r['lift']:+.3f}")
    print(f"cold-start deficit vs baseline:       {r['cold_start_deficit']:+.3f}")
    print(f"wrong-user-memory delta:              {r['wrong_memory_delta']:+.3f}  (must be < 0)")
    print(f"cross-user leakage:                   {leak}")
    print(f"gate: {'PASS' if ok else 'FAIL — ' + '; '.join(reasons)}")
    sys.exit(0 if ok else 1)
