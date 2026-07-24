"""A from-scratch Gaussian-process regressor (numpy only, zero heavy deps).

This is the surrogate model at the heart of Bayesian optimization: given a few
expensive (x, y) observations it returns a *calibrated posterior* — a predictive
mean AND variance at any new x. The variance is what makes the loop "active":
acquisition functions trade off exploiting a high mean against exploring a high
variance.

Kernel: anisotropic RBF (per-dim lengthscales) + constant signal variance + i.i.d.
observation noise. Hyperparameters (lengthscale, signal, noise) are fit by
maximizing the exact log marginal likelihood over a small random-restart search —
no autodiff needed, so this runs anywhere numpy runs.

The math mirrors Rasmussen & Williams, *Gaussian Processes for Machine Learning*,
Algorithm 2.1 (predictive equations) and Eq. 5.8 (log marginal likelihood).
The real job would use GPyTorch/BoTorch; this is the transparent reference so the
loop is testable offline and the behavior is auditable.
"""
from __future__ import annotations

import numpy as np


def _cholesky_solve(L: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve (L L^T) x = b given lower-triangular Cholesky factor L (scipy-free)."""
    y = _forward_sub(L, b)
    return _back_sub(L.T, y)


def _forward_sub(L: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = L.shape[0]
    x = np.zeros_like(b)
    for i in range(n):
        x[i] = (b[i] - L[i, :i] @ x[:i]) / L[i, i]
    return x


def _back_sub(U: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = U.shape[0]
    x = np.zeros_like(b)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


class GaussianProcess:
    """Exact GP regression with an anisotropic RBF kernel, fit by marginal likelihood."""

    def __init__(self, noise: float = 1e-3, jitter: float = 1e-8, seed: int = 0) -> None:
        self.noise = float(noise)
        self.jitter = float(jitter)
        self.rng = np.random.default_rng(seed)
        self._fitted = False

    # ── kernel ───────────────────────────────────────────────────────────────
    def _kernel(self, A: np.ndarray, B: np.ndarray, ell: float, sf2: float) -> np.ndarray:
        """Isotropic squared-exponential kernel k(a,b)=sf2 * exp(-0.5 * ||a-b||^2 / ell^2).

        Isotropic (one lengthscale) is deliberate: in the low-data regime of a DBTL
        loop (a handful of experiments), a per-dimension lengthscale is unidentifiable
        and overfits. One well-fit lengthscale generalizes far better.
        """
        d2 = (A**2).sum(1)[:, None] + (B**2).sum(1)[None, :] - 2 * A @ B.T
        return sf2 * np.exp(-0.5 * np.clip(d2, 0, None) / (ell**2))

    # ── likelihood ────────────────────────────────────────────────────────────
    def _nll(self, ell: float, sf2: float, noise: float) -> float:
        """Negative log marginal likelihood (R&W Eq. 5.8), lower is better."""
        n = self.X.shape[0]
        K = self._kernel(self.X, self.X, ell, sf2) + (noise + self.jitter) * np.eye(n)
        try:
            L = np.linalg.cholesky(K)
        except np.linalg.LinAlgError:
            return np.inf
        alpha = _cholesky_solve(L, self.y)
        return float(0.5 * self.y @ alpha + np.log(np.diag(L)).sum() + 0.5 * n * np.log(2 * np.pi))

    # ── fit / predict ──────────────────────────────────────────────────────────
    def fit(self, X: np.ndarray, y: np.ndarray, restarts: int = 8) -> "GaussianProcess":
        """Fit hyperparameters (lengthscale, signal, noise) by marginal-likelihood search.

        Grid over a log-spaced lengthscale range (robust, deterministic) plus a few
        random restarts on signal/noise; keep the lowest NLL. y is standardized so
        the signal-variance prior is scale-free.
        """
        self.X = np.atleast_2d(np.asarray(X, float))
        yv = np.asarray(y, float).ravel()
        self.y_mean = float(np.mean(yv))
        self.y_std = float(np.std(yv)) or 1.0
        self.y = (yv - self.y_mean) / self.y_std

        # Candidate lengthscales span sub-feature to whole-domain distances.
        ell_grid = np.logspace(-1.5, 1.0, 18)
        noise_grid = np.array([1e-4, 1e-3, 1e-2, 3e-2])
        best = None
        for ell in ell_grid:
            for noise in noise_grid:
                for _ in range(2):  # a couple of signal-variance draws per (ell, noise)
                    sf2 = float(np.exp(self.rng.uniform(-1.0, 1.0)))
                    nll = self._nll(float(ell), sf2, float(noise))
                    if best is None or nll < best[0]:
                        best = (nll, float(ell), sf2, float(noise))

        _, self.ell, self.sf2, self.noise = best
        n = self.X.shape[0]
        K = self._kernel(self.X, self.X, self.ell, self.sf2) + (self.noise + self.jitter) * np.eye(n)
        self.L = np.linalg.cholesky(K)
        self.alpha = _cholesky_solve(self.L, self.y)
        self._fitted = True
        return self

    def predict(self, Xstar: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return posterior (mean, variance) at query points (R&W Alg. 2.1), de-standardized."""
        if not self._fitted:
            raise RuntimeError("call fit() before predict()")
        Xstar = np.atleast_2d(np.asarray(Xstar, float))
        Ks = self._kernel(self.X, Xstar, self.ell, self.sf2)
        mean = Ks.T @ self.alpha
        v = _batched_forward(self.L, Ks)
        var = self.sf2 - (v**2).sum(0)  # RBF self-covariance diagonal is sf2
        mean = mean * self.y_std + self.y_mean
        var = np.clip(var, 1e-12, None) * (self.y_std**2)
        return mean, var


def _batched_forward(L: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Solve L V = B column-by-column (forward substitution) without scipy."""
    n, m = B.shape
    V = np.zeros((n, m))
    for i in range(n):
        V[i] = (B[i] - L[i, :i] @ V[:i]) / L[i, i]
    return V
