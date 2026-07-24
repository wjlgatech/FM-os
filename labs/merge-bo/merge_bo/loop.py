"""The closed-loop optimizer — one DBTL cycle per iteration.

Design → Build → Test → Learn, as an executable loop:
  Design : fit the GP surrogate on everything tested so far, score the untested
           pool with an acquisition function, pick the top batch.
  Build  : (a wet lab would synthesize; here it's a no-op — candidates preexist).
  Test   : query the assay for the chosen candidates (noisy readouts).
  Learn  : add the new (x, y) to the training set; repeat.

Returns a trajectory of best-found value per experiment, so we can compute simple
regret and compare against a random-search baseline — the honest measure that the
optimizer is actually saving experiments.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .acquisition import constrained_ei, ehvi_2d, ei, ucb
from .gp import GaussianProcess
from .objectives import MolecularLibrary


@dataclass
class Result:
    best_trajectory: list[float] = field(default_factory=list)  # best-so-far per experiment
    tested_idx: list[int] = field(default_factory=list)
    final_best: float = float("-inf")


def _init_design(lib: MolecularLibrary, n_init: int, rng) -> list[int]:
    """Space-filling-ish random seed set (a real loop might use a Sobol/maximin set)."""
    return list(rng.choice(lib.n, size=n_init, replace=False))


def bo_loop(
    lib: MolecularLibrary,
    acqf: str = "ei",
    n_init: int = 5,
    n_iters: int = 25,
    batch: int = 1,
    beta: float = 2.0,
    seed: int = 0,
) -> Result:
    """Single-objective Bayesian optimization over the library pool."""
    rng = np.random.default_rng(seed)
    tested = _init_design(lib, n_init, rng)
    ys = [lib.assay_potency(i) for i in tested]

    res = Result()
    best = max(ys)
    for y in ys:
        best = max(best, y)
        res.best_trajectory.append(best)

    for _ in range(n_iters):
        untested = np.array([i for i in range(lib.n) if i not in set(tested)])
        if len(untested) == 0:
            break
        gp = GaussianProcess(seed=seed).fit(lib.X[tested], np.array(ys))
        mu, var = gp.predict(lib.X[untested])
        if acqf == "ucb":
            score = ucb(mu, var, beta=beta)
        else:
            score = ei(mu, var, best_f=best)
        pick = untested[np.argsort(-score)[:batch]]
        for idx in pick:
            y = lib.assay_potency(int(idx))
            tested.append(int(idx))
            ys.append(y)
            best = max(best, y)
            res.best_trajectory.append(best)
    res.tested_idx = tested
    res.final_best = best
    return res


def random_loop(lib: MolecularLibrary, n_total: int, seed: int = 0) -> Result:
    """Random-search baseline over the same budget — the honest control."""
    rng = np.random.default_rng(seed)
    order = list(rng.permutation(lib.n))[:n_total]
    res, best = Result(), float("-inf")
    for idx in order:
        best = max(best, lib.assay_potency(int(idx)))
        res.best_trajectory.append(best)
    res.tested_idx = order
    res.final_best = best
    return res


def constrained_bo_loop(
    lib: MolecularLibrary,
    sa_budget: float = 0.8,
    n_init: int = 5,
    n_iters: int = 25,
    seed: int = 0,
) -> Result:
    """BO that only rewards feasible (synthesizable) candidates via feasibility-weighted EI."""
    rng = np.random.default_rng(seed)
    tested = _init_design(lib, n_init, rng)
    ys = [lib.assay_potency(i) for i in tested]
    cs = [lib.assay_sa(i) for i in tested]

    res = Result()
    feasible_best = max((y for y, c in zip(ys, cs) if c <= sa_budget), default=float("-inf"))
    res.best_trajectory.append(feasible_best)

    for _ in range(n_iters):
        untested = np.array([i for i in range(lib.n) if i not in set(tested)])
        if len(untested) == 0:
            break
        gp = GaussianProcess(seed=seed).fit(lib.X[tested], np.array(ys))
        cgp = GaussianProcess(seed=seed + 1).fit(lib.X[tested], np.array(cs))
        mu, var = gp.predict(lib.X[untested])
        cmu, cvar = cgp.predict(lib.X[untested])
        best_ref = feasible_best if feasible_best > float("-inf") else float(np.max(ys))
        score = constrained_ei(mu, var, best_ref, cmu, cvar, c_threshold=sa_budget)
        idx = int(untested[int(np.argmax(score))])
        y, c = lib.assay_potency(idx), lib.assay_sa(idx)
        tested.append(idx)
        ys.append(y)
        cs.append(c)
        if c <= sa_budget:
            feasible_best = max(feasible_best, y)
        res.best_trajectory.append(feasible_best)
    res.tested_idx = tested
    res.final_best = feasible_best
    return res


def multiobjective_bo_loop(
    lib: MolecularLibrary,
    n_init: int = 6,
    n_iters: int = 25,
    ref_point=(-0.1, -0.1),
    seed: int = 0,
) -> list[float]:
    """2-objective BO (potency vs. selectivity) driven by an EHVI proxy.

    Returns the hypervolume trajectory — the standard multi-objective progress metric.
    """
    from .acquisition import _hypervolume_2d, _pareto_front

    rng = np.random.default_rng(seed)
    tested = _init_design(lib, n_init, rng)
    Y = np.array([[lib.assay_potency(i), lib.assay_selectivity(i)] for i in tested])
    ref = np.array(ref_point, float)
    hv_traj = [_hypervolume_2d(_pareto_front(Y), ref)]

    for _ in range(n_iters):
        untested = np.array([i for i in range(lib.n) if i not in set(tested)])
        if len(untested) == 0:
            break
        gp1 = GaussianProcess(seed=seed).fit(lib.X[tested], Y[:, 0])
        gp2 = GaussianProcess(seed=seed + 1).fit(lib.X[tested], Y[:, 1])
        m1, _ = gp1.predict(lib.X[untested])
        m2, _ = gp2.predict(lib.X[untested])
        pred = np.column_stack([m1, m2])
        score = ehvi_2d(pred, _pareto_front(Y), ref)
        idx = int(untested[int(np.argmax(score))])
        y = np.array([lib.assay_potency(idx), lib.assay_selectivity(idx)])
        tested.append(idx)
        Y = np.vstack([Y, y])
        hv_traj.append(_hypervolume_2d(_pareto_front(Y), ref))
    return hv_traj
