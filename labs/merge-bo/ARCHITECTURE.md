# merge-bo — architecture

A closed-loop Bayesian optimizer is four replaceable seams. This lab keeps each one small,
tested, and swap-able — the same decomposition you'd scale into a production DBTL backbone.

```
                 ┌─────────────────────────────────────────────────────┐
                 │                  DBTL closed loop                     │
                 │                  (merge_bo/loop.py)                   │
                 │                                                       │
   design  ─────▶│  1. fit surrogate on all data so far  (gp.py)        │
                 │  2. score untested pool with acquisition (acq.py)    │
                 │  3. pick top-k candidates                            │
   build   ─────▶│  4. (synthesize — no-op; candidates preexist)        │
   test    ─────▶│  5. query the assay → noisy readout   (objectives)  │
   learn   ─────▶│  6. append (x, y); repeat                            │
                 └─────────────────────────────────────────────────────┘
```

## The four seams

| Seam | File | Reference impl | Production swap |
|---|---|---|---|
| **Surrogate** (x → posterior mean+var) | `gp.py` | exact GP, isotropic RBF, marginal-likelihood fit, numpy | BoTorch `SingleTaskGP` / GPyTorch; deep-kernel or GAUCHE molecular kernels |
| **Acquisition** (posterior → next pick) | `acquisition.py` | EI, UCB, constrained-EI, EHVI proxy | BoTorch `qLogEI` / `qNEHVI` / `qNEI` (Monte-Carlo, batch, noisy) |
| **Objective** (candidate → readout) | `objectives.py` | synthetic potency/SA/selectivity landscape | a real wet-lab assay, or a `chemprop`/DeepChem property model |
| **Loop policy** (budget, batch, init) | `loop.py` | random init, greedy top-k | Ax `Scheduler` service API for async DBTL orchestration |

Because the seams are typed by their signatures — surrogate returns `(mean, var)`,
acquisition returns a score per candidate — the numpy reference and the BoTorch adapter are
drop-in interchangeable. `botorch_adapter.py` demonstrates the swap on seams 1–2 without
touching the loop.

## Why isotropic GP + marginal-likelihood grid

DBTL loops start data-starved: the first cycles have ~5 observations. A per-dimension
(anisotropic) lengthscale has one free parameter per feature — unidentifiable and prone to
overfit at that sample size. One isotropic lengthscale, fit by a deterministic log-spaced
grid over the exact marginal likelihood (R&W Eq. 5.8), generalizes far better in the low-data
regime and makes the fit reproducible. As data accumulates you'd graduate to ARD kernels;
the seam makes that a one-line change.

## Why a known objective

You cannot compute regret against an unknown optimum, so validation uses a **known synthetic
landscape** — the discipline the BO literature uses (Branin, Ackley, Olympus surfaces). The
honest test (`tests/test_loop.py::test_bo_beats_random_on_average`) asserts BO beats random
search on average AND wins the majority of seeds — a claim that fails loudly if the surrogate
or acquisition regresses. This is the lab's `ready-is-a-gate`.

## Test gates

- `test_gp.py` — surrogate interpolates data; posterior variance grows away from data (UQ).
- `test_acquisition.py` — EI ≥ 0 and prefers higher mean; UCB rewards uncertainty;
  constrained-EI penalizes infeasible; Pareto/hypervolume are monotone under domination.
- `test_loop.py` — BO beats random; trajectory monotone; constraint respected; MO HV grows.
