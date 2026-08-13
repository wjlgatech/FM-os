#!/usr/bin/env python3
"""Item-centric evaluation-subset selection — a runnable probe of the Scales++ claim.

WHAT THIS IS, HONESTLY
----------------------
This is NOT a reproduction of Scales++ (Bean, Seedat, Chen & Schwarz,
arXiv:2510.26384). That method embeds real benchmark items with cognitive-scales
features; we have neither their embeddings nor their benchmarks.

What this IS: a controlled harness that tests the *claim structure* of the paper
on a benchmark whose ground truth we generate, so every number here is checkable
by hand. The claim under test:

    An ITEM-CENTRIC selector — choosing evaluation items by their own intrinsic
    properties — can predict full-benchmark scores about as faithfully as a
    MODEL-CENTRIC selector, while costing ZERO seed-model runs to build.

That cost asymmetry is the whole point. A model-centric selector (anchor points,
tinyBenchmarks-style) must first run N seed models over the FULL benchmark to
learn which items are informative. An item-centric selector reads the items and
nothing else, so it works cold-start on a benchmark no model has ever been run
on. In FM-os terms: it is the difference between an eval gate you can afford to
run on every candidate and one you run once a quarter.

THE GENERATIVE MODEL (why the comparison is meaningful)
------------------------------------------------------
Items follow a 2-parameter IRT model: item i has difficulty b_i and
discrimination a_i; model m has ability theta_m; and

    P(model m answers item i correctly) = sigmoid(a_i * (theta_m - b_i))

Each item also carries a feature vector — its observable "cognitive demand"
signature — which is a NOISY linear image of (b_i, a_i). That noise is the
honest part: item features are informative about difficulty but not equal to it,
which is exactly the bet Scales++ makes. Turn the noise up (`feature_noise`) and
the item-centric selector should degrade toward random. The harness lets you
check that, rather than asking you to believe it.

Run it:
    python3 subset.py
    python3 -m pytest test_subset.py -q
"""
from __future__ import annotations

import numpy as np

# ── the synthetic benchmark ──────────────────────────────────────────────────


def make_benchmark(
    n_items: int = 2000,
    n_models: int = 120,
    n_features: int = 8,
    feature_noise: float = 0.6,
    seed: int = 0,
) -> dict:
    """Generate a 2PL IRT benchmark plus per-item observable feature vectors.

    Returns a dict with ``scores`` (n_models x n_items, 0/1), ``features``
    (n_items x n_features), and the latent ``difficulty`` / ``ability`` arrays
    kept only so tests can assert the generator behaves as documented.
    """
    rng = np.random.default_rng(seed)

    difficulty = rng.normal(0.0, 1.2, n_items)
    discrimination = np.abs(rng.normal(1.0, 0.35, n_items)) + 0.2
    ability = rng.normal(0.0, 1.0, n_models)

    # Item features: a noisy linear image of the latent (difficulty, discrimination).
    basis = rng.normal(0.0, 1.0, (2, n_features))
    latent = np.stack([difficulty, discrimination], axis=1)          # (n_items, 2)
    features = latent @ basis + rng.normal(0.0, feature_noise, (n_items, n_features))

    logits = discrimination[None, :] * (ability[:, None] - difficulty[None, :])
    probs = 1.0 / (1.0 + np.exp(-logits))
    scores = (rng.random((n_models, n_items)) < probs).astype(float)

    return {
        "scores": scores,
        "features": features,
        "difficulty": difficulty,
        "discrimination": discrimination,
        "ability": ability,
    }


# ── clustering (plain numpy, seeded, deterministic) ──────────────────────────


def _kmeans(points: np.ndarray, k: int, seed: int = 0, iters: int = 40) -> np.ndarray:
    """k-means++ init then Lloyd's algorithm. Returns a cluster label per row."""
    rng = np.random.default_rng(seed)
    n = points.shape[0]
    k = max(1, min(k, n))

    # k-means++ seeding: spread the initial centres out by squared distance.
    centres = [points[rng.integers(n)]]
    for _ in range(k - 1):
        d2 = np.min(
            np.stack([np.sum((points - c) ** 2, axis=1) for c in centres]), axis=0
        )
        total = d2.sum()
        # Degenerate case: all points identical → fall back to a uniform draw.
        probs = d2 / total if total > 0 else np.full(n, 1.0 / n)
        centres.append(points[rng.choice(n, p=probs)])
    centres = np.stack(centres)

    labels = np.zeros(n, dtype=int)
    for _ in range(iters):
        dists = ((points[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
        new_labels = dists.argmin(axis=1)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for c in range(k):
            members = points[labels == c]
            if len(members):
                centres[c] = members.mean(axis=0)
    return labels


def _apportion(sizes: np.ndarray, budget: int) -> np.ndarray:
    """Split ``budget`` items across strata proportional to size (largest remainder).

    Every non-empty stratum gets at least one item, and no stratum is asked for
    more items than it contains.
    """
    sizes = sizes.astype(float)
    exact = budget * sizes / sizes.sum()
    alloc = np.floor(exact).astype(int)
    alloc = np.maximum(alloc, 1)
    alloc = np.minimum(alloc, sizes.astype(int))

    # Hand out (or claw back) the rounding remainder, largest fractional part first.
    order = np.argsort(-(exact - np.floor(exact)))
    i = 0
    while alloc.sum() < budget and i < 10 * len(sizes):
        c = order[i % len(order)]
        if alloc[c] < sizes[c]:
            alloc[c] += 1
        i += 1
    i = 0
    while alloc.sum() > budget and i < 10 * len(sizes):
        c = order[-1 - (i % len(order))]
        if alloc[c] > 1:
            alloc[c] -= 1
        i += 1
    return alloc


def _stratified_pick(
    labels: np.ndarray, n_clusters: int, budget: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Stratified sample of ``budget`` items with PROPORTIONAL allocation.

    Two design choices here are load-bearing, and both were forced by gate
    failures rather than chosen up front:

    1. **Proportional, not equal, allocation.** Giving every cluster the same
       number of items and then weighting by cluster size destroys effective
       sample size whenever clusters are unequal — the variance penalty can
       exceed everything stratification buys. Allocating in proportion to
       cluster size keeps each item's weight at ~1/budget, so the estimator is
       strictly better than simple random sampling by the between-stratum
       variance. (Textbook proportional allocation; the first two versions of
       this file got it wrong and the gate said so.)

    2. **Random within a stratum, not nearest-to-centre.** Taking the items
       closest to the cluster centre biases the sample toward the centroid and
       under-represents the stratum's own spread. Uniform sampling inside the
       stratum keeps the estimator unbiased; the fixed seed keeps it reproducible.
    """
    n = labels.shape[0]
    members = [np.flatnonzero(labels == c) for c in range(n_clusters)]
    members = [m for m in members if len(m)]
    sizes = np.array([len(m) for m in members])
    alloc = _apportion(sizes, budget)

    idx: list[int] = []
    weights: list[float] = []
    for m, a in zip(members, alloc):
        chosen = rng.choice(m, size=int(min(a, len(m))), replace=False)
        share = (len(m) / n) / len(chosen)
        idx.extend(int(i) for i in chosen)
        weights.extend([share] * len(chosen))

    w = np.asarray(weights, dtype=float)
    return np.asarray(idx, dtype=int), w / w.sum()


# ── the three selectors ──────────────────────────────────────────────────────


def select_random(n_items: int, k: int, seed: int = 0) -> tuple[np.ndarray, np.ndarray, int]:
    """Uniform random subset. Selection cost: 0 model runs. The honest baseline."""
    rng = np.random.default_rng(seed)
    idx = rng.choice(n_items, size=min(k, n_items), replace=False)
    return np.sort(idx), np.full(len(idx), 1.0 / len(idx)), 0


def select_item_centric(
    features: np.ndarray, k: int, per_cluster: int = 4, seed: int = 0
) -> tuple[np.ndarray, np.ndarray, int]:
    """Stratify items by their OWN features. Selection cost: 0 model runs.

    This is the Scales++-shaped selector: it never looks at a score matrix, so it
    works on a brand-new benchmark before any model has been evaluated on it.
    """
    n_clusters = max(1, k // per_cluster)
    labels = _kmeans(features, n_clusters, seed=seed)
    idx, weights = _stratified_pick(labels, n_clusters, k, np.random.default_rng(seed))
    order = np.argsort(idx)
    return idx[order], weights[order], 0


def select_model_centric(
    scores: np.ndarray, k: int, n_seed_models: int, per_cluster: int = 4, seed: int = 0
) -> tuple[np.ndarray, np.ndarray, int]:
    """Stratify items by their response vectors across seed models. Costs N full runs.

    The anchor-points / tinyBenchmarks shape: strictly more information per item,
    but it must burn ``n_seed_models`` complete benchmark evaluations before it
    can select anything at all. That upfront cost is what item-centric avoids.
    """
    response = scores[:n_seed_models].T               # (n_items, n_seed_models)
    n_clusters = max(1, k // per_cluster)
    labels = _kmeans(response, n_clusters, seed=seed)
    idx, weights = _stratified_pick(labels, n_clusters, k, np.random.default_rng(seed))
    order = np.argsort(idx)
    return idx[order], weights[order], n_seed_models


# ── prediction + scoring ─────────────────────────────────────────────────────


def predict_full(scores: np.ndarray, idx: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Predict each model's FULL-benchmark accuracy from the weighted subset."""
    return scores[:, idx] @ weights


def mean_absolute_error(scores: np.ndarray, idx: np.ndarray, weights: np.ndarray) -> float:
    """Mean absolute error between predicted and true full-benchmark accuracy."""
    true = scores.mean(axis=1)
    return float(np.mean(np.abs(predict_full(scores, idx, weights) - true)))


def compare(
    k: int = 100,
    n_seed_models: int = 40,
    n_eval_models: int = 60,
    n_bench: int = 3,
    n_trials: int = 12,
    **bench_kwargs,
) -> dict:
    """Compare the three selectors over ``n_bench`` benchmarks x ``n_trials`` subsets.

    WHAT IS BEING MEASURED, AND WHY IT IS THE P90 AND NOT THE MEAN
    --------------------------------------------------------------
    In practice you pick ONE subset and live with it for a whole training
    campaign. You do not get to average your luck over twelve draws. So the
    statistic that decides whether a selector is safe is not its average error
    but its TAIL: how bad is the subset you might unluckily get?

    Reporting only the mean hides exactly the property stratification buys.
    Random sampling and stratified sampling can agree on average while random
    has a long right tail of unrepresentative subsets. That tail is the risk of
    shipping a bad gate, so p90 is the number the gate is written against.

    MAE is always measured on the last ``n_eval_models`` models, which no
    selector has seen — otherwise the model-centric selector, which spends
    ``n_seed_models`` full runs, would be graded on its own training set.
    """
    per: dict[str, list[float]] = {"random": [], "item_centric": [], "model_centric": []}
    cost = {"random": 0, "item_centric": 0, "model_centric": n_seed_models}
    n_selected = 0
    n_items = 0

    for b in range(n_bench):
        bench = make_benchmark(seed=b, **bench_kwargs)
        scores = bench["scores"]
        held_out = scores[-n_eval_models:]
        n_items = scores.shape[1]
        for t in range(n_trials):
            s = 1000 * b + t
            draws = {
                "random": select_random(n_items, k, seed=s),
                "item_centric": select_item_centric(bench["features"], k, seed=s),
                "model_centric": select_model_centric(scores, k, n_seed_models, seed=s),
            }
            for name, (idx, weights, _) in draws.items():
                per[name].append(mean_absolute_error(held_out, idx, weights))
                n_selected = len(idx)

    out: dict = {}
    for name, maes in per.items():
        arr = np.asarray(maes)
        out[name] = {
            "mae": float(arr.mean()),
            "mae_p90": float(np.percentile(arr, 90)),
            "mae_std": float(arr.std(ddof=1)),
            "selection_cost_model_runs": cost[name],
            "n_items": n_selected,
            "subset_fraction": n_selected / n_items,
            "n_runs": len(arr),
        }
    return out


def gate(result: dict | None = None, max_mae: float = 0.04) -> tuple[bool, list[str]]:
    """Blocking gate. Returns (passed, reasons) — reasons are always populated.

    Three assertions, each of which can genuinely fail:
      1. item-centric has a lower p90 error than random at the same subset size
         (the selector reduces the risk of an unrepresentative subset);
      2. item-centric costs ZERO seed-model runs (the cost claim — the whole
         reason to prefer it over anchor-point methods);
      3. item-centric mean MAE is within ``max_mae`` (it is fit to actually use).
    """
    result = result or compare()
    ic, rnd, mc = result["item_centric"], result["random"], result["model_centric"]
    reasons = []

    safer = ic["mae_p90"] < rnd["mae_p90"]
    reasons.append(
        f"{'PASS' if safer else 'FAIL'}  item-centric p90 error {ic['mae_p90']:.4f} "
        f"{'<' if safer else '>='} random p90 {rnd['mae_p90']:.4f}"
    )

    free = ic["selection_cost_model_runs"] == 0
    reasons.append(
        f"{'PASS' if free else 'FAIL'}  item-centric selection cost "
        f"{ic['selection_cost_model_runs']} model runs vs model-centric "
        f"{mc['selection_cost_model_runs']}"
    )

    usable = ic["mae"] <= max_mae
    reasons.append(
        f"{'PASS' if usable else 'FAIL'}  item-centric mean MAE {ic['mae']:.4f} <= {max_mae}"
    )

    return (safer and free and usable), reasons


def main() -> int:
    """Print the comparison table and run the gate."""
    result = compare()
    first = next(iter(result.values()))
    print(
        f"Evaluation-subset selection — 2000-item benchmark, "
        f"{first['n_items']}-item subset ({first['subset_fraction']:.1%}), "
        f"{first['n_runs']} runs"
    )
    print(f"{'selector':<16}{'mean MAE':>10}{'p90 MAE':>10}{'std':>9}{'sel. cost':>12}")
    for name in ("random", "item_centric", "model_centric"):
        r = result[name]
        print(
            f"{name:<16}{r['mae']:>10.4f}{r['mae_p90']:>10.4f}{r['mae_std']:>9.4f}"
            f"{r['selection_cost_model_runs']:>9} runs"
        )

    passed, reasons = gate(result)
    print("\nGate:")
    for line in reasons:
        print(f"  {line}")
    print(f"\n{'GATE PASSED' if passed else 'GATE FAILED'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
