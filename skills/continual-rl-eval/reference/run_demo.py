#!/usr/bin/env python3
"""
Continual-RL evaluation harness + demo for the persistent WarehouseEnv.

Runs a policy across a SCHEDULE of regime shifts (demand + failure preset changed on fixed
timesteps, independent of the policy) and scores continual adaptation, then applies the
eval-with-teeth gate:

    PASS iff  (1) the policy ADAPTS within the shifted regime
                  (2nd-half mean reward > 1st-half mean reward in the final config), AND
              (2) overall gap-to-upper-bound <= MAX_GAP.

A static policy (fixed threshold, no feedback) fails (1): it fits the first regime and coasts.
An adaptive policy (hill-climbs its threshold on reward feedback) passes. That contrast is the
whole point — "no durable adaptation => no claim of learning."

Usage:
    python3 run_demo.py --policy adaptive     # -> PASS (exit 0)
    python3 run_demo.py --policy static        # -> FAIL, honestly (exit 1)
"""
from __future__ import annotations
import argparse, json, statistics, sys
from env import WarehouseEnv, UPPER_BOUND

MAX_WORST_GAP = 0.18 * UPPER_BOUND     # a durable learner keeps EVERY regime's gap low, not just the average
STEPS_PER_CONFIG = 300

# regime schedule: (label, failure_preset, demand). Applied by the harness, not the policy.
SCHEDULE = [
    ("calm",    "light",      5.0),
    ("surge",   "moderate",  12.0),
    ("storm",   "aggressive", 9.0),
    ("calm-2",  "light",      5.0),   # revisit calm-like regime to probe forgetting
]


class StaticPolicy:
    """Commits a FIXED staffing level tuned to the first regime, ignores feedback.
    Great in 'calm', then under-staffs every harder regime — fits regime 1 and coasts."""
    def __init__(self, capacity: int, level: int = 5):
        self.capacity, self.level = capacity, level
    def act(self, obs: dict) -> int:
        return self.level
    def update(self, reward: float) -> None:
        pass


class AdaptivePolicy:
    """Hill-climbs its staffing level on reward feedback — a minimal continual learner.
    Tracks the shifting optimum (target = min(demand, capacity)) across regimes."""
    def __init__(self, capacity: int, level: float = 5.0):
        self.capacity, self.level = capacity, float(level)
        self._last_r, self._dir = None, 1.0
    def act(self, obs: dict) -> int:
        return int(round(self.level))
    def update(self, reward: float) -> None:
        if self._last_r is not None and reward < self._last_r - 1e-9:
            self._dir *= -1                            # got worse -> reverse search direction
        self.level = max(0.0, min(float(self.capacity), self.level + self._dir * 0.4))
        self._last_r = reward


def run(policy_name: str, seed: int = 0) -> dict:
    env = WarehouseEnv(capacity=10, seed=seed)
    policy = (AdaptivePolicy if policy_name == "adaptive" else StaticPolicy)(env.capacity)
    per_config: dict[str, list[float]] = {}
    obs = {"backlog": 0, "inventory": env.inventory, "arrivals": 0, "t": 0}
    for label, preset, demand in SCHEDULE:
        env.configure(preset=preset, demand=demand)   # regime shift on a fixed boundary
        rewards: list[float] = []
        for _ in range(STEPS_PER_CONFIG):
            action = policy.act(obs)
            obs, reward, _ = env.step(action)
            policy.update(reward)
            rewards.append(reward)
        per_config[label] = rewards
    return per_config


def metrics(per_config: dict[str, list[float]]) -> dict:
    out = {"per_config": {}, "gaps": {}}
    for label, rs in per_config.items():
        mean = statistics.fmean(rs)
        out["per_config"][label] = round(mean, 4)
        out["gaps"][label] = round(UPPER_BOUND - mean, 4)
    # worst-config gap: the regime the policy handles WORST (averaging would hide it)
    worst_label = max(out["gaps"], key=out["gaps"].get)
    out["worst_config"], out["worst_gap"] = worst_label, out["gaps"][worst_label]
    out["overall_gap"] = round(UPPER_BOUND - statistics.fmean([x for rs in per_config.values() for x in rs]), 4)
    # recovery from the first HARD shift ('surge'): did reward climb within the regime? (reported)
    sr = per_config["surge"]; half = len(sr) // 2
    out["recovered_in_surge"] = round(statistics.fmean(sr[half:]) - statistics.fmean(sr[:half]), 4)
    # forgetting: calm-2 revisits a calm-like regime; how much worse than the original 'calm'?
    out["forgetting"] = round(out["per_config"]["calm"] - out["per_config"].get("calm-2", 0.0), 4)
    return out


def gate(m: dict) -> tuple[bool, list[str]]:
    """Eval-with-teeth: durable adaptation means EVERY regime's gap stays low — not a good average."""
    reasons = []
    if m["worst_gap"] > MAX_WORST_GAP:
        reasons.append(f"worst-regime gap {m['worst_gap']} (on '{m['worst_config']}') "
                       f"> {round(MAX_WORST_GAP, 4)} — coasts on that regime instead of adapting")
    if m["forgetting"] > 0.5 * MAX_WORST_GAP:
        reasons.append(f"forgetting {m['forgetting']} > {round(0.5 * MAX_WORST_GAP, 4)} "
                       f"(lost the original 'calm' regime after adapting)")
    return (len(reasons) == 0), reasons


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", choices=["adaptive", "static"], default="adaptive")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    m = metrics(run(args.policy, args.seed))
    ok, reasons = gate(m)
    if args.json:
        print(json.dumps({"policy": args.policy, "metrics": m, "pass": ok, "reasons": reasons}, indent=2))
    else:
        print(f"policy = {args.policy}  (upper bound {UPPER_BOUND}/config)")
        for label, mean in m["per_config"].items():
            print(f"  {label:8s} mean reward {mean:.3f}   gap {m['gaps'][label]:.3f}")
        print(f"  recovered in 'surge': {m['recovered_in_surge']:+.3f}"
              f"   forgetting: {m['forgetting']:+.3f}   overall gap: {m['overall_gap']:.3f}")
        print(("PASS — durable adaptation demonstrated" if ok
               else "FAIL — no durable adaptation:\n   - " + "\n   - ".join(reasons)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
