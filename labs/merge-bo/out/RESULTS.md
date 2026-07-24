# merge-bo — closed-loop optimization RESULTS

Averaged over 8 seeds · budget = 30 experiments (5 seed + 25 loop) ·
GP surrogate (from-scratch, numpy) · EI acquisition. Every number below is produced
live by `python run_demo.py` — no hand-entered values.

## 1. Bayesian optimization vs. random search (single objective)

| Method | Best potency found (mean ± sd) | Simple regret vs. true optimum |
|---|---|---|
| **BO (GP + EI)** | 0.485 ± 0.264 | 0.066 |
| Random search | 0.322 ± 0.194 | 0.230 |

**BO finds +50.8% better candidates and cuts regret by 71%
at the same experimental budget.** That gap *is* the value proposition of a
closed-loop optimizer to a wet lab: fewer expensive DBTL cycles to reach a target.

## 2. Constrained BO (potency subject to a synthetic-accessibility budget)

Feasibility-weighted EI keeps proposals inside the SA budget (≤ 0.8).
Best *feasible* potency found: **0.387** (mean over seeds) — the loop optimizes
the objective while respecting a domain constraint, never rewarding infeasible picks.

## 3. Multi-objective BO (potency vs. selectivity)

EHVI-proxy acquisition grows the Pareto-front hypervolume from
**0.057 → 0.149** over the campaign — the loop discovers trade-off-optimal
candidates, not just a single-objective winner.

---

_Reproduce: `make e2e` (this script) · offline gate: `make check` (pytest)._
