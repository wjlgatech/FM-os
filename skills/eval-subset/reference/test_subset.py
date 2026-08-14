"""Offline gate for the item-centric evaluation-subset probe.

The important test in this file is ``test_uninformative_features_destroy_the_edge``.
Everything else checks the plumbing; that one checks that the *result* is real —
if item features carry no information about item difficulty, the item-centric
selector must collapse toward random. A harness that "wins" even on noise is
measuring itself, not the method.
"""
from __future__ import annotations

import numpy as np
import pytest

from subset import (
    _apportion,
    compare,
    gate,
    make_benchmark,
    mean_absolute_error,
    predict_full,
    select_item_centric,
    select_model_centric,
    select_random,
)


# ── the generator ────────────────────────────────────────────────────────────


def test_benchmark_shapes_and_determinism():
    """Same seed → identical benchmark; shapes match the requested sizes."""
    a = make_benchmark(n_items=200, n_models=30, seed=3)
    b = make_benchmark(n_items=200, n_models=30, seed=3)
    assert a["scores"].shape == (30, 200)
    assert a["features"].shape[0] == 200
    assert np.array_equal(a["scores"], b["scores"])
    assert np.allclose(a["features"], b["features"])


def test_scores_are_binary():
    """The 2PL generator must emit 0/1 outcomes, not probabilities."""
    scores = make_benchmark(n_items=150, n_models=20, seed=1)["scores"]
    assert set(np.unique(scores)).issubset({0.0, 1.0})


def test_harder_items_are_answered_less_often():
    """Sanity-check the IRT direction: higher difficulty → lower accuracy."""
    bench = make_benchmark(n_items=800, n_models=200, seed=5)
    per_item = bench["scores"].mean(axis=0)
    hardest = np.argsort(-bench["difficulty"])[:200]
    easiest = np.argsort(bench["difficulty"])[:200]
    assert per_item[easiest].mean() > per_item[hardest].mean()


# ── apportionment ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("budget", [10, 37, 100])
def test_apportion_hits_the_budget(budget):
    """Allocation sums exactly to the budget."""
    sizes = np.array([50, 30, 20, 10, 5, 100])
    alloc = _apportion(sizes, budget)
    assert alloc.sum() == budget


def test_apportion_respects_bounds():
    """No stratum gets fewer than 1 item or more items than it contains."""
    sizes = np.array([3, 40, 200, 7])
    alloc = _apportion(sizes, 60)
    assert (alloc >= 1).all()
    assert (alloc <= sizes).all()


def test_apportion_is_proportional():
    """A stratum twice the size receives roughly twice the items."""
    sizes = np.array([100, 200, 400])
    alloc = _apportion(sizes, 70)
    assert alloc[2] > alloc[1] > alloc[0]


# ── the selectors ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("k", [20, 60, 100])
def test_all_selectors_return_normalized_weights(k):
    """Weights must sum to 1 or the estimator is not an average of anything."""
    bench = make_benchmark(n_items=500, n_models=40, seed=2)
    for idx, w, _ in (
        select_random(500, k, seed=0),
        select_item_centric(bench["features"], k, seed=0),
        select_model_centric(bench["scores"], k, 20, seed=0),
    ):
        assert len(idx) == len(w)
        assert w.sum() == pytest.approx(1.0)
        assert len(set(idx.tolist())) == len(idx), "an item was selected twice"


def test_selection_costs_are_reported_honestly():
    """Item-centric costs zero model runs; model-centric costs what it spends."""
    bench = make_benchmark(n_items=400, n_models=40, seed=0)
    _, _, item_cost = select_item_centric(bench["features"], 40, seed=0)
    _, _, model_cost = select_model_centric(bench["scores"], 40, 25, seed=0)
    assert item_cost == 0
    assert model_cost == 25


def test_full_benchmark_selection_is_exact():
    """Selecting every item must predict the true score with zero error."""
    bench = make_benchmark(n_items=120, n_models=15, seed=7)
    scores = bench["scores"]
    idx = np.arange(120)
    weights = np.full(120, 1.0 / 120)
    assert mean_absolute_error(scores, idx, weights) == pytest.approx(0.0, abs=1e-12)
    assert predict_full(scores, idx, weights) == pytest.approx(scores.mean(axis=1))


# ── the result ───────────────────────────────────────────────────────────────


def test_gate_passes_on_the_default_configuration():
    """The shipped configuration must pass its own gate."""
    passed, reasons = gate()
    assert passed, "\n".join(reasons)
    assert len(reasons) == 3


def test_item_centric_beats_random_on_tail_risk():
    """The headline claim: lower p90 error than random at the same subset size."""
    result = compare()
    assert result["item_centric"]["mae_p90"] < result["random"]["mae_p90"]
    assert result["item_centric"]["mae"] < result["random"]["mae"]


def test_item_centric_is_competitive_with_model_centric_for_free():
    """Matches the expensive selector while spending zero seed-model runs.

    This is the whole argument for item-centric selection, so it is asserted
    rather than admired: within 15% relative mean MAE, at 0 vs 40 model runs.
    """
    result = compare()
    ic, mc = result["item_centric"], result["model_centric"]
    assert ic["selection_cost_model_runs"] == 0
    assert mc["selection_cost_model_runs"] > 0
    assert ic["mae"] <= mc["mae"] * 1.15


def test_uninformative_features_destroy_the_edge():
    """THE FALSIFIER.

    Item-centric selection works only because item features carry information
    about item difficulty. Drown the features in noise and the advantage over
    random must disappear. If this test fails, the harness is manufacturing a
    win from its own structure and every other number here is worthless.
    """
    informative = compare(feature_noise=0.4, n_bench=2, n_trials=8)
    noise_only = compare(feature_noise=40.0, n_bench=2, n_trials=8)

    edge_informative = informative["random"]["mae_p90"] - informative["item_centric"]["mae_p90"]
    edge_noise = noise_only["random"]["mae_p90"] - noise_only["item_centric"]["mae_p90"]

    assert edge_informative > 0, "informative features should yield an edge"
    assert edge_noise < edge_informative * 0.5, (
        f"uninformative features still gave an edge of {edge_noise:.4f} vs "
        f"{edge_informative:.4f} — the harness is rigged"
    )
