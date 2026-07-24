"""Acquisition functions — how the closed loop decides what to test next.

Each takes a GP posterior (mean mu, variance var) over a pool of candidate points
and returns a score per candidate; the loop picks the argmax. This is where the
explore/exploit trade-off lives, and where domain constraints enter.

Implemented:
  - ei   : Expected Improvement (Jones et al. 1998) — the BO workhorse.
  - ucb  : Upper Confidence Bound (Srinivas et al. 2010, GP-UCB) — tunable via beta.
  - constrained_ei : feasibility-weighted EI (Gardner et al. 2014) — EI times the
           GP-predicted probability that a separate constraint is satisfied.
  - ehvi_2d : a cheap 2-objective Expected Hypervolume Improvement proxy for
           multi-objective campaigns (the direction BoTorch's qNEHVI formalizes).

All noise-free-posterior formulas; observation noise is folded into the GP.
"""
from __future__ import annotations

import math

import numpy as np

SQRT2 = math.sqrt(2.0)


def _norm_pdf(z: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * z**2) / math.sqrt(2 * math.pi)


def _norm_cdf(z: np.ndarray) -> np.ndarray:
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / SQRT2))


def ei(mu: np.ndarray, var: np.ndarray, best_f: float, xi: float = 0.01) -> np.ndarray:
    """Expected Improvement over the current best (maximization)."""
    sigma = np.sqrt(np.clip(var, 1e-12, None))
    imp = mu - best_f - xi
    z = imp / sigma
    return imp * _norm_cdf(z) + sigma * _norm_pdf(z)


def ucb(mu: np.ndarray, var: np.ndarray, beta: float = 2.0) -> np.ndarray:
    """Upper Confidence Bound (GP-UCB). Higher beta => more exploration."""
    return mu + beta * np.sqrt(np.clip(var, 1e-12, None))


def constrained_ei(
    mu: np.ndarray,
    var: np.ndarray,
    best_f: float,
    c_mu: np.ndarray,
    c_var: np.ndarray,
    c_threshold: float = 0.0,
    xi: float = 0.01,
) -> np.ndarray:
    """EI weighted by P(constraint <= threshold), a separate GP over the constraint.

    Encodes 'only propose molecules the GP believes are feasible' — the JD's
    'encode domain-specific priors and constraints'.
    """
    base = ei(mu, var, best_f, xi)
    c_sigma = np.sqrt(np.clip(c_var, 1e-12, None))
    p_feasible = _norm_cdf((c_threshold - c_mu) / c_sigma)
    return base * p_feasible


def ehvi_2d(mu: np.ndarray, pareto_ys: np.ndarray, ref_point: np.ndarray) -> np.ndarray:
    """Cheap 2-objective hypervolume-improvement proxy (both objectives maximized).

    For each candidate's predicted (y1, y2), score = dominated-area added over the
    current Pareto front relative to ref_point. A transparent stand-in for
    BoTorch qEHVI, enough to drive a 2-objective loop offline.
    """
    front = _pareto_front(pareto_ys)
    base_hv = _hypervolume_2d(front, ref_point)
    scores = np.zeros(mu.shape[0])
    for i, cand in enumerate(mu):
        aug = np.vstack([front, cand[None, :]])
        f2 = _pareto_front(aug)
        scores[i] = max(0.0, _hypervolume_2d(f2, ref_point) - base_hv)
    return scores


def _pareto_front(ys: np.ndarray) -> np.ndarray:
    """Return the non-dominated rows (maximization on all columns).

    Point i is dominated if some other point is >= it in every objective and
    strictly greater in at least one.
    """
    ys = np.atleast_2d(ys)
    keep = np.ones(len(ys), dtype=bool)
    for i in range(len(ys)):
        others = np.delete(ys, i, axis=0)
        if len(others) and np.any(
            np.all(others >= ys[i], axis=1) & np.any(others > ys[i], axis=1)
        ):
            keep[i] = False
    return ys[keep]


def _hypervolume_2d(front: np.ndarray, ref: np.ndarray) -> float:
    """2-D hypervolume dominated by `front`, above/right of `ref` (maximization).

    Sweep in ascending x; each vertical strip's height is the max y among points
    at or to the right of the strip (the staircase upper envelope).
    """
    pts = np.atleast_2d(front)
    pts = pts[np.all(pts > ref, axis=1)]
    if len(pts) == 0:
        return 0.0
    pts = pts[np.argsort(pts[:, 0])]                       # ascending x
    right_max_y = np.maximum.accumulate(pts[::-1, 1])[::-1]  # max y from here rightward
    xs = pts[:, 0]
    prev_x, total = ref[0], 0.0
    for i in range(len(xs)):
        total += max(0.0, xs[i] - prev_x) * max(0.0, right_max_y[i] - ref[1])
        prev_x = xs[i]
    return total
