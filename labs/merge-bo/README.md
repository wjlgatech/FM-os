# merge-bo — a closed-loop Bayesian optimization lab

**Proof-of-capability for the Merge Labs role _"Senior/Principal ML Research Scientist — Bayesian Optimization"_** ([JD](https://jobs.ashbyhq.com/Merge%20Labs/a8440ed8-9e11-4861-8413-fc23e2213790)).

The role: *"design and scale Bayesian optimization and reinforcement-learning
frameworks that guide molecular engineering campaigns through iterative
design–build–test–learn (DBTL) cycles … architect the company's closed-loop
optimization backbone."*

This lab is exactly that backbone, in miniature and fully runnable: a Gaussian-process
surrogate, standard acquisition functions, and a Design→Build→Test→Learn loop over a
molecular library — with **constrained** and **multi-objective** variants — implemented
from scratch in numpy so it runs anywhere, plus an optional adapter that runs the *same
loop* on the production **BoTorch** stack.

## The claim it proves (measured, not asserted)

Run `make e2e` and read [`out/RESULTS.md`](out/RESULTS.md). Averaged over 8 seeds at a
fixed budget of 30 experiments:

| | Best candidate found | Simple regret |
|---|---|---|
| **BO (GP + Expected Improvement)** | **0.485** | **0.066** |
| Random search | 0.322 | 0.230 |

**Bayesian optimization finds ~51% better candidates and cuts regret ~71% at the same
experimental budget** — the entire economic argument for a closed-loop optimizer in a
wet lab where each DBTL cycle is slow and expensive. The constrained loop optimizes
potency while respecting a synthesizability budget; the multi-objective loop grows the
potency-vs-selectivity Pareto hypervolume over the campaign.

## Map to the JD

| JD requirement | Where it lives here |
|---|---|
| Bayesian optimization / acquisition strategy | `merge_bo/acquisition.py` (EI, UCB, constrained EI, EHVI) |
| Gaussian-process surrogate / probabilistic modeling | `merge_bo/gp.py` (exact GP, marginal-likelihood fit) |
| Uncertainty quantification | GP posterior variance drives every acquisition; UQ test in `tests/test_gp.py` |
| Closed-loop / active learning / DBTL | `merge_bo/loop.py` (`bo_loop` = the DBTL cycle) |
| Constrained optimization + domain priors | `constrained_bo_loop` (feasibility-weighted EI) |
| Multi-objective optimization | `multiobjective_bo_loop` (hypervolume improvement) |
| Sparse, noisy, high-cost data | isotropic GP + noisy `assay_*` readouts, budgets of ~30 |
| Production-grade code (PyTorch/BoTorch) | `merge_bo/botorch_adapter.py` (SingleTaskGP + qLogEI) |
| "Serve to non-domain experts" | one function call per loop; `run_demo.py` is the demo |

## Run it

```bash
make check     # offline gate: pytest — GP correctness, acquisition properties,
               #                        and BO-beats-random-search on the benchmark
make e2e       # run the closed loop, regenerate out/RESULTS.md (numpy only)
make botorch   # run the SAME loop on the real BoTorch stack (pip install botorch)
```

No heavy dependencies for the core (numpy only) — `torch`/`gpytorch`/`botorch` are
needed **only** for `make botorch`, which is import-guarded and skips cleanly if absent.

## What's deliberately a model, not the real thing

The "assay" is a known synthetic landscape so that **regret is measurable** — the standard
way BO methods are validated. Swap `merge_bo/objectives.py` for a real assay readout (or a
`chemprop`/GAUCHE property model over RDKit features) and the loop is unchanged. That
substitution is the whole point of the seam. See [`ARCHITECTURE.md`](ARCHITECTURE.md).

## The product built on this engine — Helix

`labs/merge-bo` is the *engine*. [`helix/`](helix/) is the **product** Merge Labs could ship on
top of it: the **Design·Build·Test·Learn Copilot**. A wet-lab scientist describes a campaign in
plain language → Helix compiles a typed spec → proposes the next experiments with uncertainty and
a rationale → ingests results → shows experiments saved vs. random. It's packaged as **agent
tooling** (a Claude Code plugin): a skill (`dbtl-copilot`), a command (`/dbtl-cycle`), an
auto-ingest **hook**, an **MCP server** (`define_campaign · propose_experiments · ingest_results ·
campaign_status`), and a **workflow**.

- Product pitch: [`helix/PRODUCT-BRIEF.md`](helix/PRODUCT-BRIEF.md)
- Live dashboard (wow surface): `make helix` → [`out/helix-dashboard.html`](out/helix-dashboard.html) ([screenshot](out/helix-dashboard.png))
- Plugin package: [`plugin/`](plugin/) · MCP server: `make mcp`

Measured on the demo: **108 experiments saved (median), +79% better candidate at equal budget,
7 Pareto-optimal designs** — all computed live.

## Further reading (from the FM-os knowledge base)

Frazier, *A Tutorial on Bayesian Optimization* (arXiv:1807.02811) · Balandat et al.,
*BoTorch* (arXiv:1910.06403) · Daulton et al., *qNEHVI* (arXiv:2105.08195) · Griffiths et
al., *GAUCHE* (arXiv:2212.04450) · Rasmussen & Williams, *GPML*. All curated in
[`data/papers.yml`](../../data/papers.yml) and the [Merge dossier](../../docs/jd-fit/merge-bayesopt.md).
