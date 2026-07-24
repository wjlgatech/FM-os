"""The closed loop must beat random search — the skill's honest capability gate."""
import numpy as np

from bo_demo import bo_loop, random_search, toy_objective


def test_bo_beats_random_on_average():
    bos = [bo_loop(toy_objective, budget=20, seed=s)["best"] for s in range(6)]
    rnds = [random_search(toy_objective, budget=20, seed=s + 99)["best"] for s in range(6)]
    assert np.mean(bos) > np.mean(rnds)


def test_respects_budget():
    r = bo_loop(toy_objective, budget=15, seed=1)
    assert r["n"] == 15
