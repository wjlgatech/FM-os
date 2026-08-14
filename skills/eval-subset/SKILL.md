---
name: eval-subset
description: >-
  Cut the cost of an evaluation loop without lying about the score. Selects a
  small, representative subset of a benchmark using ITEM-CENTRIC properties —
  the items' own difficulty signature — so no seed-model runs are needed, then
  predicts full-benchmark scores from the subset with a stratified estimator and
  gates on tail risk, not just average error. Grounded in Scales++ (Bean, Seedat,
  Chen & Schwarz, arXiv:2510.26384) and the FM-os curated knowledge base.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# eval-subset

An evaluation loop you cannot afford to run is an evaluation loop you do not run.
That is the real reason post-training teams ship on vibes: full-benchmark
evaluation after every candidate run is unaffordable, so it happens at the end,
where it can no longer change any decision.

This skill makes the eval gate cheap enough to run *every time*, and is explicit
about what that costs you in fidelity.

## When to use (trigger)

Invoke when the user says "our evals are too expensive", "benchmark subset",
"tiny benchmarks", "anchor points", "which eval items should I run", "predict
full benchmark score from a sample", "eval is the bottleneck in our training
loop", "cheap proxy benchmark", or "we only run evals at the end because they
cost too much". Also activates on "Scales++", "item response theory for evals",
"IRT benchmark", or "cold-start benchmark selection".

## The distinction that matters

| | **Model-centric** (anchor points, tinyBenchmarks) | **Item-centric** (Scales++, this skill) |
|---|---|---|
| Picks items by | how seed models performed on them | the items' own intrinsic properties |
| Upfront cost | N full benchmark runs before you can select anything | **zero model runs** |
| Works on a brand-new benchmark | ✗ needs a score matrix first | ✓ cold start |
| Re-selection when the model family changes | rerun the seeds | free |

The upfront cost is the entire argument. A selector that must burn 40 full
benchmark evaluations to tell you which 100 items to run has not saved you
anything on the first model you care about.

## What it does

1. **Featurize items** — turn each benchmark item into a vector describing its
   demands (in production: embeddings of the item text plus structural features;
   in the shipped probe: a controlled noisy image of latent difficulty).
2. **Stratify** — k-means over item features to build strata of similar demand.
3. **Allocate proportionally** — items per stratum proportional to stratum size,
   sampled uniformly *within* the stratum. Both details are load-bearing; see
   "Two ways this went wrong" below.
4. **Estimate** — predict full-benchmark accuracy as the stratified weighted
   mean of subset scores.
5. **Gate on tail risk** — the blocking assertion is on the **p90** error, not
   the mean. You pick one subset and live with it; the mean over draws is a
   luxury you never get. A selector that is fine on average and occasionally
   catastrophic is not fine.
6. **Falsify** — the suite includes a test that destroys the feature signal and
   asserts the advantage disappears. A harness that wins on noise is measuring
   itself.

## Example

```bash
python3 reference/subset.py                       # comparison table + gate
python3 -m pytest reference/test_subset.py -q      # 17 offline tests
```

```python
from reference.subset import compare, gate, select_item_centric, make_benchmark

bench = make_benchmark(n_items=2000, seed=0)
idx, weights, cost = select_item_centric(bench["features"], k=100)
assert cost == 0                     # no seed-model runs were needed

passed, reasons = gate()
assert passed, reasons               # p90 beats random · cost is 0 · MAE within budget
```

## Measured result

2,000-item benchmark · 100-item subset (5.0%) · 36 runs (3 benchmark draws × 12
subset draws) · MAE against held-out models the selectors never saw:

| selector | mean MAE | **p90 MAE** | std | selection cost |
|---|---|---|---|---|
| random | 0.0375 | 0.0452 | 0.0084 | 0 model runs |
| **item-centric** | **0.0316** | **0.0363** | 0.0034 | **0 model runs** |
| model-centric | 0.0326 | 0.0356 | 0.0030 | **40 model runs** |

Item-centric selection **matches the expensive model-centric selector** — mean
MAE marginally better, p90 marginally worse — while spending **zero** seed-model
runs against its 40. Against random it cuts p90 error by 20% and the spread
across draws by 2.5×. Reproduce with `python3 reference/subset.py`.

## Two ways this went wrong (kept, because the gate caught both)

The first two versions of this probe **failed their own gate**, and the failures
were informative enough to keep in the file:

1. **One medoid per cluster.** With binary item scores a lone representative is a
   single Bernoulli draw; its variance swamped everything stratification bought,
   and item-centric lost to random (0.0648 vs 0.0642).
2. **Equal allocation across unequal clusters.** Giving every stratum the same
   item count and then weighting by stratum size destroys effective sample size.
   Item-centric drew level with random (0.0315 vs 0.0310) but never beat it.

Proportional allocation with within-stratum random sampling fixed it. Both dead
ends are documented in `reference/subset.py` at the function that now does it
right — a gate that never fails is not a gate.

## Honest limits

- **This is not a reproduction of Scales++.** That method embeds real benchmark
  items with cognitive-scales features. This probe tests the *claim structure*
  on a synthetic 2PL IRT benchmark where ground truth is known and every number
  is checkable by hand. It shows the mechanism is sound; it does not confirm the
  paper's numbers on real benchmarks.
- **The advantage is bounded by feature quality.** With uninformative features
  the method degrades to random — asserted, not assumed, by
  `test_uninformative_features_destroy_the_edge`.
- **Subset estimates are for triage, not for publication.** Use them to rank
  candidate runs inside a loop; run the full benchmark before you claim a number.
- **Binary-scored items only.** Graded or free-text rubrics need the estimator
  extended to continuous scores.

## Where this sits in FM-os

The eval-cost stage (`E1`) of the Thomson-1 stack reconstruction —
see [`data/thomson_stack.yml`](../../data/thomson_stack.yml) and
[`docs/research/CASE-STUDY-thomson-stack.md`](../../docs/research/CASE-STUDY-thomson-stack.md).
It is the one stage of that pipeline FM-os can run rather than merely describe,
and it directly serves FM-os's own thesis — *eval gates are training-signal
factories* — by making the gate cheap enough to run on every candidate.

Pairs with [`agentic-eval`](../agentic-eval/) (what to measure),
[`research-loop`](../research-loop/) (how to report it honestly), and
[`bayesopt-loop`](../bayesopt-loop/) (the sibling mechanism at stage 3, where
Bayesian optimization picks data mixtures instead of eval items).
