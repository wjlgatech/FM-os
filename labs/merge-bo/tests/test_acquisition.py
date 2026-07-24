"""Acquisition functions must obey their defining properties."""
import numpy as np

from merge_bo.acquisition import (
    _hypervolume_2d,
    _pareto_front,
    constrained_ei,
    ei,
    ucb,
)


def test_ei_nonnegative():
    mu = np.array([0.0, 1.0, 2.0])
    var = np.array([0.1, 0.1, 0.1])
    assert np.all(ei(mu, var, best_f=1.0) >= 0)


def test_ei_prefers_higher_mean_at_equal_variance():
    mu = np.array([0.5, 2.0])
    var = np.array([0.05, 0.05])
    a = ei(mu, var, best_f=1.0)
    assert a[1] > a[0]


def test_ucb_rewards_uncertainty():
    mu = np.array([1.0, 1.0])
    var = np.array([0.01, 1.0])
    a = ucb(mu, var, beta=2.0)
    assert a[1] > a[0]


def test_constrained_ei_penalizes_infeasible():
    mu = np.array([2.0, 2.0])
    var = np.array([0.1, 0.1])
    # candidate 0 predicted feasible (constraint far below threshold),
    # candidate 1 predicted infeasible (constraint far above threshold)
    c_mu = np.array([-1.0, 3.0])
    c_var = np.array([0.05, 0.05])
    a = constrained_ei(mu, var, best_f=1.0, c_mu=c_mu, c_var=c_var, c_threshold=0.0)
    assert a[0] > a[1]


def test_pareto_front_and_hypervolume():
    ys = np.array([[1.0, 0.0], [0.0, 1.0], [0.5, 0.5], [0.2, 0.2]])
    front = _pareto_front(ys)
    # the dominated point (0.2,0.2) must be excluded
    assert not any(np.allclose(p, [0.2, 0.2]) for p in front)
    hv = _hypervolume_2d(front, ref=np.array([-0.1, -0.1]))
    assert hv > 0
    # adding a dominating point never shrinks hypervolume
    hv2 = _hypervolume_2d(_pareto_front(np.vstack([ys, [1.0, 1.0]])), np.array([-0.1, -0.1]))
    assert hv2 >= hv
