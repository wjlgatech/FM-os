"""The closed loop must actually beat random search — the honest capability claim."""
import numpy as np

from merge_bo.loop import (
    bo_loop,
    constrained_bo_loop,
    multiobjective_bo_loop,
    random_loop,
)
from merge_bo.objectives import MolecularLibrary


def test_bo_beats_random_on_average():
    n_init, n_iters, seeds = 5, 25, range(6)
    wins, bo_scores, rnd_scores = 0, [], []
    for s in seeds:
        bo = bo_loop(MolecularLibrary(seed=s), n_init=n_init, n_iters=n_iters, seed=s)
        rnd = random_loop(MolecularLibrary(seed=s), n_total=n_init + n_iters, seed=s + 50)
        bo_scores.append(bo.final_best)
        rnd_scores.append(rnd.final_best)
        wins += bo.final_best >= rnd.final_best
    # on average BO should find strictly better candidates within the same budget
    assert np.mean(bo_scores) > np.mean(rnd_scores)
    assert wins >= 4  # and win the majority of seeds


def test_trajectory_is_monotone_nondecreasing():
    bo = bo_loop(MolecularLibrary(seed=0), n_init=5, n_iters=10, seed=0)
    traj = bo.best_trajectory
    assert all(traj[i + 1] >= traj[i] - 1e-9 for i in range(len(traj) - 1))


def test_constrained_loop_respects_budget():
    lib = MolecularLibrary(seed=1)
    con = constrained_bo_loop(lib, sa_budget=0.8, n_init=5, n_iters=15, seed=1)
    # the reported best must be achievable by some feasible candidate
    assert con.final_best <= lib.feasible_best_potency(0.8) + 1e-6


def test_multiobjective_hypervolume_grows():
    hv = multiobjective_bo_loop(MolecularLibrary(seed=2), n_init=6, n_iters=15, seed=2)
    assert hv[-1] >= hv[0]  # Pareto front never regresses
    assert hv[-1] > hv[0]   # and actually improves over the campaign
