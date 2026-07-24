#!/usr/bin/env python3
"""Self-contained closed-loop Bayesian optimization demo (numpy only).

A compact, portable proof of the skill: a Gaussian-process surrogate + Expected
Improvement acquisition running a design-build-test-learn loop that beats random
search on a known objective within the same experiment budget. Runs anywhere numpy
runs — no torch/botorch needed. For the production stack and constrained/multi-
objective variants, see labs/merge-bo/.
"""
from __future__ import annotations

import math

import numpy as np


def toy_objective(x: np.ndarray) -> float:
    """A multi-modal test surface on [0,1]^2 (maximization). Stands in for an assay."""
    x = np.atleast_1d(x)
    return float(
        math.sin(3 * math.pi * x[0]) * (1 - abs(x[0] - 0.6))
        + 0.7 * math.exp(-((x[1] - 0.3) ** 2) / 0.05)
    )


# ── a tiny isotropic-RBF Gaussian process ────────────────────────────────────
def _rbf(A, B, ell, sf2):
    d2 = (A**2).sum(1)[:, None] + (B**2).sum(1)[None, :] - 2 * A @ B.T
    return sf2 * np.exp(-0.5 * np.clip(d2, 0, None) / ell**2)


def _gp_posterior(X, y, Xs, ell=0.2, sf2=1.0, noise=1e-3):
    """Return posterior (mean, var) at Xs — Rasmussen & Williams Alg. 2.1."""
    ymu, ysd = y.mean(), (y.std() or 1.0)
    yz = (y - ymu) / ysd
    K = _rbf(X, X, ell, sf2) + noise * np.eye(len(X))
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, yz))
    Ks = _rbf(X, Xs, ell, sf2)
    mean = Ks.T @ alpha
    v = np.linalg.solve(L, Ks)
    var = np.clip(sf2 - (v**2).sum(0), 1e-9, None)
    return mean * ysd + ymu, var * ysd**2


def _ei(mu, var, best, xi=0.01):
    """Expected Improvement (Jones et al. 1998)."""
    sigma = np.sqrt(var)
    z = (mu - best - xi) / sigma
    cdf = 0.5 * (1 + np.vectorize(math.erf)(z / math.sqrt(2)))
    pdf = np.exp(-0.5 * z**2) / math.sqrt(2 * math.pi)
    return (mu - best - xi) * cdf + sigma * pdf


def bo_loop(objective, budget=20, n_init=4, pool=400, dim=2, seed=0) -> dict:
    """GP + EI closed loop over a random candidate pool. Returns best-found value."""
    rng = np.random.default_rng(seed)
    cand = rng.uniform(0, 1, size=(pool, dim))
    tested = list(rng.choice(pool, size=n_init, replace=False))
    ys = [objective(cand[i]) for i in tested]
    best = max(ys)
    for _ in range(budget - n_init):
        untested = np.array([i for i in range(pool) if i not in set(tested)])
        mu, var = _gp_posterior(cand[tested], np.array(ys), cand[untested])
        idx = int(untested[int(np.argmax(_ei(mu, var, best)))])
        tested.append(idx)
        ys.append(objective(cand[idx]))
        best = max(best, ys[-1])
    return {"best": best, "n": len(tested)}


def random_search(objective, budget=20, pool=400, dim=2, seed=0) -> dict:
    """The honest baseline: sample the same budget at random."""
    rng = np.random.default_rng(seed)
    cand = rng.uniform(0, 1, size=(pool, dim))
    idx = rng.permutation(pool)[:budget]
    return {"best": max(objective(cand[i]) for i in idx), "n": budget}


if __name__ == "__main__":
    bos, rnds = [], []
    for s in range(6):
        bos.append(bo_loop(toy_objective, seed=s)["best"])
        rnds.append(random_search(toy_objective, seed=s + 99)["best"])
    print(f"BO mean best     : {np.mean(bos):.3f}")
    print(f"random mean best : {np.mean(rnds):.3f}")
    print(f"BO advantage     : {100*(np.mean(bos)-np.mean(rnds))/abs(np.mean(rnds)):+.1f}%")
