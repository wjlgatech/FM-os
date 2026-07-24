#!/usr/bin/env python3
"""Run the closed-loop BO demo and write out/RESULTS.md — the evidence artifact.

Proves the core claim of the role in a measurable way: Bayesian optimization finds
high-potency candidates in far fewer 'experiments' than random search, handles a
synthesizability constraint, and improves a 2-objective Pareto front. Averaged over
several seeds so the numbers are not a lucky draw.
"""
from __future__ import annotations

import statistics as stats
from pathlib import Path

from merge_bo.loop import (
    bo_loop,
    constrained_bo_loop,
    multiobjective_bo_loop,
    random_loop,
)
from merge_bo.objectives import MolecularLibrary

OUT = Path(__file__).parent / "out"
N_INIT, N_ITERS, SEEDS = 5, 25, list(range(8))
BUDGET = N_INIT + N_ITERS


def _mean_sd(xs):
    return stats.mean(xs), (stats.pstdev(xs) if len(xs) > 1 else 0.0)


def main() -> int:
    bo_final, rand_final, gaps, con_final = [], [], [], []
    mo_start, mo_end = [], []
    for s in SEEDS:
        lib = MolecularLibrary(seed=s)
        opt = lib.best_potency()
        bo = bo_loop(lib, acqf="ei", n_init=N_INIT, n_iters=N_ITERS, seed=s)
        rnd = random_loop(MolecularLibrary(seed=s), n_total=BUDGET, seed=s + 100)
        con = constrained_bo_loop(MolecularLibrary(seed=s), sa_budget=0.8,
                                  n_init=N_INIT, n_iters=N_ITERS, seed=s)
        mo = multiobjective_bo_loop(MolecularLibrary(seed=s), n_init=6,
                                    n_iters=N_ITERS, seed=s)
        bo_final.append(bo.final_best)
        rand_final.append(rnd.final_best)
        gaps.append((opt - bo.final_best, opt - rnd.final_best))
        con_final.append(con.final_best)
        mo_start.append(mo[0])
        mo_end.append(mo[-1])

    bo_m, bo_s = _mean_sd(bo_final)
    rd_m, rd_s = _mean_sd(rand_final)
    bo_regret, _ = _mean_sd([g[0] for g in gaps])
    rd_regret, _ = _mean_sd([g[1] for g in gaps])
    con_m, _ = _mean_sd(con_final)
    mo0, _ = _mean_sd(mo_start)
    mo1, _ = _mean_sd(mo_end)

    improvement = 100 * (bo_m - rd_m) / abs(rd_m) if rd_m else 0.0
    regret_cut = 100 * (rd_regret - bo_regret) / rd_regret if rd_regret else 0.0

    OUT.mkdir(exist_ok=True)
    md = f"""# merge-bo — closed-loop optimization RESULTS

Averaged over {len(SEEDS)} seeds · budget = {BUDGET} experiments ({N_INIT} seed + {N_ITERS} loop) ·
GP surrogate (from-scratch, numpy) · EI acquisition. Every number below is produced
live by `python run_demo.py` — no hand-entered values.

## 1. Bayesian optimization vs. random search (single objective)

| Method | Best potency found (mean ± sd) | Simple regret vs. true optimum |
|---|---|---|
| **BO (GP + EI)** | {bo_m:.3f} ± {bo_s:.3f} | {bo_regret:.3f} |
| Random search | {rd_m:.3f} ± {rd_s:.3f} | {rd_regret:.3f} |

**BO finds {improvement:+.1f}% better candidates and cuts regret by {regret_cut:.0f}%
at the same experimental budget.** That gap *is* the value proposition of a
closed-loop optimizer to a wet lab: fewer expensive DBTL cycles to reach a target.

## 2. Constrained BO (potency subject to a synthetic-accessibility budget)

Feasibility-weighted EI keeps proposals inside the SA budget (≤ 0.8).
Best *feasible* potency found: **{con_m:.3f}** (mean over seeds) — the loop optimizes
the objective while respecting a domain constraint, never rewarding infeasible picks.

## 3. Multi-objective BO (potency vs. selectivity)

EHVI-proxy acquisition grows the Pareto-front hypervolume from
**{mo0:.3f} → {mo1:.3f}** over the campaign — the loop discovers trade-off-optimal
candidates, not just a single-objective winner.

---

_Reproduce: `make e2e` (this script) · offline gate: `make check` (pytest)._
"""
    (OUT / "RESULTS.md").write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
