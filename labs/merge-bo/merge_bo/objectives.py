"""Benchmark objectives — stand-ins for a wet-lab assay in a DBTL loop.

Real campaigns optimize an expensive, noisy assay readout over a discrete library
of candidate molecules described by featurized vectors. We cannot run a wet lab
offline, so we provide:

  - MolecularLibrary: a fixed pool of N candidates, each a d-dim descriptor vector
    (think RDKit fingerprints / learned embeddings), with a hidden ground-truth
    objective the loop must discover by "testing" candidates. Observation noise
    models assay variability. This is the standard way BO methods are validated
    (a known function stands in for the assay so regret is measurable).

  - Single-objective (potency-like), constrained (potency subject to a synthetic-
    accessibility budget), and multi-objective (potency vs. selectivity) variants.

The point is not chemical realism — it is a *measurable* closed loop where we can
prove the optimizer finds good candidates in fewer experiments than random search.
"""
from __future__ import annotations

import numpy as np


class MolecularLibrary:
    """A discrete pool of featurized candidates with a hidden objective landscape."""

    def __init__(self, n: int = 400, d: int = 6, noise: float = 0.05, seed: int = 0) -> None:
        self.rng = np.random.default_rng(seed)
        self.n, self.d, self.noise = n, d, noise
        # Descriptor vectors in [0,1]^d — a stand-in for normalized fingerprints.
        self.X = self.rng.uniform(0.0, 1.0, size=(n, d))
        # Hidden landscape: a smooth potency surface with a few local optima.
        centers = self.rng.uniform(0.1, 0.9, size=(4, d))
        widths = self.rng.uniform(0.10, 0.30, size=4)
        peaks = np.array([1.0, 0.85, 0.7, 0.6])
        self._potency = self._mixture(self.X, centers, widths, peaks)
        # A cheaper "synthetic accessibility" cost (lower is easier to make).
        self._sa_cost = 0.3 + 0.7 * self.X[:, 0] + 0.2 * np.sin(6 * self.X[:, 1])
        # A second objective: selectivity, anti-correlated with potency at the peak.
        self._selectivity = self._mixture(
            self.X, self.rng.uniform(0.1, 0.9, size=(3, d)),
            self.rng.uniform(0.12, 0.30, size=3), np.array([1.0, 0.8, 0.7]),
        )

    def _mixture(self, X, centers, widths, peaks):
        out = np.zeros(len(X))
        for c, w, p in zip(centers, widths, peaks):
            out += p * np.exp(-((X - c) ** 2).sum(1) / (2 * w**2))
        return out

    # ── ground truth (for regret bookkeeping; NOT visible to the optimizer) ────
    def best_potency(self) -> float:
        return float(self._potency.max())

    def feasible_best_potency(self, sa_budget: float) -> float:
        mask = self._sa_cost <= sa_budget
        return float(self._potency[mask].max()) if mask.any() else float("-inf")

    # ── "assay": test a candidate index, get a noisy readout ───────────────────
    def assay_potency(self, idx: int) -> float:
        return float(self._potency[idx] + self.rng.normal(0, self.noise))

    def assay_sa(self, idx: int) -> float:
        return float(self._sa_cost[idx] + self.rng.normal(0, self.noise * 0.5))

    def assay_selectivity(self, idx: int) -> float:
        return float(self._selectivity[idx] + self.rng.normal(0, self.noise))

    def features(self, idx) -> np.ndarray:
        return self.X[idx]
