"""
Persistent warehouse environment for continual-RL evaluation — the runnable core of the
continual-rl-eval skill, reproducing MORPHEUS's load-bearing ideas in pure stdlib Python.

What makes it a *continual* env (not an episodic toy):
  - Persistence:   world state (inventory, backlog, ledger) carries across steps; there is
                   NO reset that clears it. Actions compound.
  - Non-stationarity via a Failure-Injection Engine: typed failures at preset rates
                   (light 5% / realistic 8% / moderate 15% / aggressive 30%).
  - Config shifts are applied by the *harness* on fixed timesteps (see harness.ConfigShift),
                   independent of the policy, so an agent can't game update periodicity.
  - Composite verifier reward: failure-severity + cost-vs-plan ledger + throughput, weighted,
                   clipped, upper bound 0.5 per config — evidence-checked, not vibes.

Deterministic: pass a seed. No third-party deps.
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field

# preset failure name -> probability a failure fires on a given step
PRESETS = {"light": 0.05, "realistic": 0.08, "moderate": 0.15, "aggressive": 0.30}

# typed failures (subset of MORPHEUS's taxonomy) -> (severity, effect)
FAILURE_TYPES = ("missing_data", "dependency_failure", "rate_limit", "stock_out", "mislabel")

REWARD_WEIGHTS = {"failure": 0.5, "ledger": 0.25, "throughput": 0.25}
UPPER_BOUND = 0.5  # theoretical max composite reward per config (zero failures, on-plan, full throughput)


def _clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


@dataclass
class WarehouseEnv:
    """A persistent order-fulfillment world. capacity = units processable per step."""
    capacity: int = 10
    seed: int = 0
    # regime (mutated by configure(); never by a reset)
    failure_preset: str = "realistic"
    demand: float = 8.0
    # persistent state
    inventory: int = 50
    backlog: int = 0
    planned_cost: float = 0.0
    actual_cost: float = 0.0
    t: int = 0
    _rng: random.Random = field(default=None, repr=False)

    def __post_init__(self):
        self._rng = random.Random(self.seed)

    def configure(self, preset: str | None = None, demand: float | None = None) -> None:
        """Shift the regime. Does NOT reset state — that is the whole point."""
        if preset is not None:
            if preset not in PRESETS:
                raise ValueError(f"unknown failure preset {preset!r}")
            self.failure_preset = preset
        if demand is not None:
            self.demand = demand

    def _inject_failure(self) -> tuple[str | None, float]:
        """Return (failure_type, severity) — severity in [0,1]; (None,0.0) if none fired."""
        if self._rng.random() >= PRESETS[self.failure_preset]:
            return None, 0.0
        ftype = self._rng.choice(FAILURE_TYPES)
        severity = round(self._rng.uniform(0.3, 1.0), 3)
        return ftype, severity

    def step(self, action: int) -> tuple[dict, float, dict]:
        """
        action = units the policy commits to process this step (clamped to [0, capacity]).
        Returns (observation, reward, info). No `done` — the world does not end.
        """
        self.t += 1
        action = int(_clip(action, 0, self.capacity))

        # new demand arrives (Poisson-ish), joins the persistent backlog
        arrivals = max(0, int(self._rng.gauss(self.demand, self.demand * 0.25)))
        self.backlog += arrivals

        # a typed failure may degrade this step's effective throughput
        ftype, severity = self._inject_failure()
        effective = action
        if ftype in ("dependency_failure", "rate_limit"):
            effective = int(action * (1.0 - severity))       # can't process what's degraded
        elif ftype == "stock_out":
            effective = min(effective, self.inventory)
        elif ftype == "missing_data":
            self.backlog += int(severity * 3)                # rework piles up
        # (mislabel degrades quality but not throughput in this reference)

        processed = min(effective, self.backlog, self.inventory)
        self.backlog -= processed
        self.inventory -= processed
        if self.inventory < self.capacity * 2:               # naive replenishment
            self.inventory += self.capacity * 2

        # bookkeeping (reported; reward uses the per-step verifiers below)
        self.planned_cost += action
        self.actual_cost += action + severity * 4 + self.backlog * 0.1

        # ── composite verifier reward ────────────────────────────────────────
        # The regime's optimal staffing is target = min(demand, capacity). Over-staffing wastes
        # committed capacity (ledger efficiency < 1); under-staffing misses demand (throughput < 1).
        # So the reward PEAK shifts with the regime — tracking it requires continual adaptation.
        target = min(self.demand, self.capacity)
        r_fail = 1.0 - severity                              # 1.0 when no failure, lower when severe
        r_ledger = _clip(processed / max(action, 1), 0.0, 1.0)   # efficiency: don't pay for idle staff
        r_tput = _clip(processed / max(target, 1.0), 0.0, 1.0)   # did we meet the regime's demand?
        reward = (
            REWARD_WEIGHTS["failure"] * r_fail
            + REWARD_WEIGHTS["ledger"] * r_ledger
            + REWARD_WEIGHTS["throughput"] * r_tput
        ) * UPPER_BOUND

        obs = {"backlog": self.backlog, "inventory": self.inventory, "arrivals": arrivals, "t": self.t}
        info = {"failure": ftype, "severity": severity, "processed": processed,
                "r_fail": r_fail, "r_ledger": r_ledger, "r_tput": r_tput}
        return obs, reward, info
