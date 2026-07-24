"""The GP surrogate must interpolate training data and give calibrated uncertainty."""
import numpy as np

from merge_bo.gp import GaussianProcess


def _f(x):
    return np.sin(3 * x[:, 0]) + 0.5 * x[:, 0]


def test_interpolates_training_points():
    rng = np.random.default_rng(0)
    X = rng.uniform(0, 1, size=(12, 1))
    y = _f(X)
    gp = GaussianProcess(seed=1).fit(X, y, restarts=12)
    mu, var = gp.predict(X)
    # near-zero-noise fit reproduces training targets closely
    assert np.mean(np.abs(mu - y)) < 0.15
    assert np.all(var >= 0)


def test_uncertainty_grows_away_from_data():
    X = np.linspace(0.2, 0.4, 8)[:, None]
    y = _f(X)
    gp = GaussianProcess(seed=2).fit(X, y, restarts=12)
    _, var_near = gp.predict(np.array([[0.3]]))
    _, var_far = gp.predict(np.array([[0.95]]))
    # posterior variance is larger in the unexplored region
    assert var_far[0] > var_near[0]


def test_predict_shapes():
    X = np.random.default_rng(3).uniform(0, 1, size=(10, 3))
    y = X.sum(1)
    gp = GaussianProcess(seed=3).fit(X, y)
    mu, var = gp.predict(np.random.default_rng(4).uniform(0, 1, size=(5, 3)))
    assert mu.shape == (5,) and var.shape == (5,)
