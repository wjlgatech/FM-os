#!/usr/bin/env python3
"""
Tests for the continual-rl-eval reference env + harness. Pure stdlib; deterministic.
Run:  python3 test_env.py   (exit 0 = all pass, non-zero = failure — gates CI)

These assert the properties that make it a *continual* benchmark, and — the point of the
skill — that the eval-with-teeth gate actually discriminates a learner from a coaster.
"""
from __future__ import annotations
import sys, statistics
from env import WarehouseEnv, PRESETS, UPPER_BOUND
import run_demo

ok = True
def check(name, cond):
    global ok
    print(f"{'PASS' if cond else 'FAIL'}  {name}")
    ok = ok and cond


# 1. Persistence: state carries across steps; configure() shifts the regime WITHOUT resetting.
env = WarehouseEnv(capacity=10, seed=1)
for _ in range(20):
    env.step(6)
t_before, backlog_before = env.t, env.backlog
check("step advances persistent clock", t_before == 20)
env.configure(preset="aggressive", demand=15.0)
check("configure() does NOT reset the world (no episodic reset)",
      env.t == t_before and env.backlog == backlog_before and env.failure_preset == "aggressive")

# 2. Failure-injection rate tracks the preset (within tolerance) over many steps.
for preset, rate in PRESETS.items():
    e = WarehouseEnv(capacity=10, seed=7)
    e.configure(preset=preset, demand=8.0)
    fires = sum(1 for _ in range(4000) if e.step(8)[2]["failure"] is not None)
    observed = fires / 4000
    check(f"failure rate ~ {rate:.0%} for '{preset}' (observed {observed:.0%})", abs(observed - rate) < 0.03)

# 3. Reward is bounded to [0, UPPER_BOUND] every step (verifier reward can't be gamed out of range).
e = WarehouseEnv(capacity=10, seed=3); e.configure(preset="moderate", demand=9.0)
rs = [e.step(a % 11)[1] for a in range(1000)]
check("reward within [0, UPPER_BOUND]", all(0.0 <= r <= UPPER_BOUND + 1e-9 for r in rs))

# 4. The regime's optimum shifts: staffing==demand beats under/over-staffing in a busy regime.
def mean_reward(level, demand, preset="light", n=400, seed=5):
    e = WarehouseEnv(capacity=10, seed=seed); e.configure(preset=preset, demand=demand)
    return statistics.fmean(e.step(level)[1] for _ in range(n))
busy = 10.0
check("in a busy regime, matching demand beats under-staffing",
      mean_reward(10, busy) > mean_reward(4, busy))
calm = 4.0
check("in a calm regime, matching demand beats over-staffing (idle-capacity penalty)",
      mean_reward(4, calm) > mean_reward(10, calm))

# 5. THE POINT: the gate discriminates a continual learner from a coaster.
adaptive_ok, _ = run_demo.gate(run_demo.metrics(run_demo.run("adaptive", seed=0)))
static_ok, static_reasons = run_demo.gate(run_demo.metrics(run_demo.run("static", seed=0)))
check("adaptive policy PASSES the eval-with-teeth gate", adaptive_ok is True)
check("static policy FAILS the gate (coasts on the hard regime)", static_ok is False and len(static_reasons) > 0)

# 6. Determinism: same seed => identical metrics (reproducible eval).
m1 = run_demo.metrics(run_demo.run("adaptive", seed=0))
m2 = run_demo.metrics(run_demo.run("adaptive", seed=0))
check("same seed => identical metrics (reproducible)", m1 == m2)

print("\nALL PASS" if ok else "\nSOME FAILED")
sys.exit(0 if ok else 1)
