---
name: bayesopt-loop
description: >-
  Stand up a closed-loop Bayesian optimizer for expensive experiments: fit a
  Gaussian-process surrogate, choose the next experiment with an acquisition
  function (EI / UCB / constrained / multi-objective), and run the
  design–build–test–learn (DBTL) loop until budget is spent. Grounded in the
  FM-os curated knowledge base; scales up to BoTorch/Ax for production.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# bayesopt-loop

A cross-runtime skill that helps you build a **closed-loop optimization backbone** —
the active-learning pattern behind molecular discovery, hyperparameter tuning, reaction
optimization, and any campaign where each experiment is slow, noisy, or expensive and
you want the *fewest* experiments to a target.

## When to use (trigger)

Invoke when the user says "Bayesian optimization", "optimize an expensive/black-box
function", "active learning loop", "design-build-test-learn / DBTL", "which experiment
should I run next", "tune with few evaluations", "multi-objective optimization",
"Gaussian process surrogate", or "self-driving lab / autonomous experimentation". Also
activates on "BoTorch", "Ax", "acquisition function", or "uncertainty-guided sampling".

## What it does

1. **Frame the loop** — identify the search space, the objective(s), the constraints,
   the per-experiment cost, and the budget. Pick single- vs. multi-objective.
2. **Featurize** — turn candidates into vectors (RDKit fingerprints / learned embeddings
   for molecules; raw parameters otherwise) — the representation the surrogate sees.
3. **Fit a surrogate** — a Gaussian process gives a calibrated posterior (mean **and**
   uncertainty); the uncertainty is what makes sampling active, not greedy.
4. **Choose an acquisition** — Expected Improvement (default), UCB (tunable
   exploration), feasibility-weighted EI (constraints), or Expected Hypervolume
   Improvement (multi-objective) — score the untested pool, pick the top batch.
5. **Test & learn** — evaluate the chosen candidates (the assay / experiment / eval),
   append the results, refit, repeat. Track simple regret vs. a **random-search
   baseline** so the benefit is measured, not assumed.
6. **Scale up** — graduate the same loop to BoTorch `SingleTaskGP` + `qLogEI` /
   `qNEHVI` and Ax's scheduler for noisy, batched, production DBTL campaigns.

## Example

```bash
# self-contained proof (numpy only): a GP + EI loop beats random search
python reference/bo_demo.py
# offline gate:
python -m pytest reference/test_bo_demo.py -q
```

```python
from reference.bo_demo import bo_loop, random_search, toy_objective
bo   = bo_loop(toy_objective, budget=20, seed=0)      # GP + Expected Improvement
rand = random_search(toy_objective, budget=20, seed=0) # honest baseline
assert bo["best"] > rand["best"]   # BO reaches a better optimum within the same budget
```

## Discipline (why this is trustworthy)

- **Measured, not asserted** — every run compares against random search; if the
  surrogate or acquisition regresses, the test fails loudly.
- **Uncertainty is first-class** — acquisition is driven by GP posterior variance, so
  the loop explores where it is ignorant, not just where it is optimistic.
- **No evidence ⇒ no claim** — regret is computed against a known optimum in the demo;
  swap in your real experiment and the loop is unchanged.

## Deeper reference (FM-os knowledge base)

Frazier, *A Tutorial on Bayesian Optimization* · Balandat et al., *BoTorch* · Daulton et
al., *qNEHVI* (multi-objective) · Griffiths et al., *GAUCHE* (BO over molecules) ·
Rasmussen & Williams, *GPML*. All in [`data/papers.yml`](../../data/papers.yml). A full
worked build with constrained + multi-objective variants lives in
[`labs/merge-bo/`](../../labs/merge-bo/).
