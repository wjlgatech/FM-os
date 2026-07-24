# Merge Labs — ML Research Scientist, Bayesian Optimization · FM-os dossier

**Role:** Senior / Principal ML Scientist — Bayesian Optimization (Bioengineering) ·
[job posting](https://jobs.ashbyhq.com/Merge%20Labs/a8440ed8-9e11-4861-8413-fc23e2213790) ·
San Francisco Bay Area (on-site).

**The company & the job in one line:** Merge Labs is a frontier brain-computer-interface
lab bridging biological and artificial intelligence. This role architects the company's
**closed-loop optimization backbone** — Bayesian optimization + RL frameworks that steer
molecular-engineering campaigns through iterative **design–build–test–learn (DBTL)** cycles,
starting from a blank slate and scaling prototypes into production pipelines.

This dossier records how FM-os equips a candidate for it: what the hub curates, what runs,
and where the honest edges are. Regenerate the score with
`make jdfit JD=docs/jd-fit/_merge-bayesopt.jd.txt`.

---

## Coverage scorecard (generated, not hand-written)

> The taxonomy (`data/jd_taxonomy.yml`) was extended with the eight capabilities this
> role actually turns on — Bayesian optimization, active learning / closed-loop DBTL,
> uncertainty quantification, representation learning, molecular/bio ML, multi-objective &
> constrained optimization, neuroscience/BCI, and state-space models. Before that, the
> scorer reported a **false 100/100 over 6 capabilities** — it simply had no keywords for
> the role's specialty, so it could not see the gap. This is the honest score.

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (14 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Python / PyTorch / large-scale ML workflows | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94) |
| Agentic evaluation / benchmarking | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98) |
| Research judgment & empirical rigor (experiment loop) | ✅ covered | AI-Scientist, AI-Scientist-v2, Agent Laboratory | research-loop (certified 92), bayesopt-loop (certified 98) |
| Bayesian optimization & Gaussian-process surrogates | ✅ covered | BoTorch, Ax, GPyTorch | bayesopt-loop (certified 98) |
| Active learning & closed-loop optimization (DBTL cycles) | ✅ covered | BoTorch, Ax, GPyTorch | bayesopt-loop (certified 98) |
| Probabilistic modeling & uncertainty quantification | ✅ covered | Pyro, NumPyro, GPyTorch | bayesopt-loop (certified 98) |
| Representation learning (molecular / sequence embeddings) | ✅ covered | GAUCHE, Chemprop, Laplace | n/a |
| ML for molecular / biomolecular design & discovery | ✅ covered | GAUCHE, RDKit, REINVENT 4 | bayesopt-loop (certified 98) |
| Multi-objective & constrained optimization | ✅ covered | BoTorch, Ax, GPyTorch | bayesopt-loop (certified 98) |
| Neuroscience / brain-computer interfaces | ✅ covered | MNE-Python, Braindecode, Neural Latents Benchmark | n/a |
| State-space / sequence models (Mamba / S4) | ✅ covered | Mamba, S4 | n/a |
| GPU optimization / efficient inference | ✅ covered | llama.cpp, vLLM, Ollama | n/a |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336, GPSS, Bayesian Optimization (Garnett) | n/a |
<!-- END jdfit -->

---

## The proof, not the promise — `labs/merge-bo`

Curated links are necessary but not sufficient; the interview asks *can you build the loop*.
[`labs/merge-bo/`](../../labs/merge-bo/) is a from-scratch, runnable **closed-loop Bayesian
optimizer** — the exact "closed-loop optimization backbone" the JD describes:

- **GP surrogate** (`merge_bo/gp.py`) — exact Gaussian process, isotropic RBF, hyperparameters
  fit by marginal likelihood; returns calibrated mean **and** variance.
- **Acquisition** (`merge_bo/acquisition.py`) — Expected Improvement, UCB, feasibility-weighted
  EI (constraints), and an EHVI proxy (multi-objective).
- **DBTL loop** (`merge_bo/loop.py`) — design → build → test → learn over a molecular library,
  with constrained and multi-objective variants.
- **Production path** (`merge_bo/botorch_adapter.py`) — the same loop on BoTorch's
  `SingleTaskGP` + `qLogExpectedImprovement`.

**Measured result** (`make e2e`, 8 seeds, budget 30): Bayesian optimization finds **~51%
better candidates and cuts simple regret ~71%** versus random search at the same experimental
budget — the economic case for a closed loop in a wet lab where each cycle is expensive. The
constrained loop respects a synthesizability budget; the multi-objective loop grows the
potency-vs-selectivity Pareto hypervolume over the campaign. All gated by `make check`.

---

## JD requirement → where it's answered

| "In this role, you will…" | FM-os answer |
|---|---|
| Build scaffolding for active-learning / closed-loop optimization | `labs/merge-bo` (loop) + `bayesopt-loop` skill (certified 98) |
| Encode domain-specific priors and constraints | `constrained_bo_loop` (feasibility-weighted EI); GP priors in `gp.py` |
| Prototype representation-learning + acquisition strategies; benchmark | acquisition zoo + BO-beats-random benchmark; GAUCHE/Chemprop for molecular reps |
| Integrate ML with experimental data streams; serve to non-experts | one-call loop API; `run_demo.py` demo; Ax service API (curated) |
| Multi-objective / constrained optimization | `multiobjective_bo_loop` (EHVI); qEHVI/qNEHVI papers curated |
| Stay current; prototype novel algorithms | Papers section: TuRBO, SAASBO, qNEHVI, MES, PES, GAUCHE |
| "You might thrive if…" probabilistic modeling / UQ | Pyro, NumPyro, GPyTorch, Uncertainty Toolbox; GP UQ test in the lab |
| Preference optimization & transfer learning | REINVENT (RL), MolSkill (preference), deep-kernel transfer (curated) |
| Python / PyTorch / BoTorch / Pyro | all curated + the BoTorch adapter runs the loop |
| Bridge ML & experimental science (sparse, noisy, costly data) | low-data isotropic GP + noisy assays + ~30-experiment budgets |
| Nice: neuroscience | MNE-Python, Braindecode, Neural Latents Benchmark, Neuromatch, LFADS |
| Nice: language / state-space models | Mamba, S4 curated (+ FM-os's whole SLM core) |

---

## Interview prep — the five things to be able to say cold

1. **Why a GP, and what breaks it.** GPs give calibrated uncertainty from a handful of
   points, which is what makes acquisition *active*. At n≈5 in high-d, a per-dimension
   (ARD) lengthscale is unidentifiable — start isotropic, graduate to ARD/SAASBO as data
   accumulates. Cubic cost in n caps exact GPs around a few thousand points; past that use
   sparse/variational GPs or TuRBO's local models. (See `labs/merge-bo/ARCHITECTURE.md`.)
2. **Which acquisition, when.** EI as the default; UCB when you want a knob on exploration;
   Thompson sampling / qEI for batches; **qNEHVI for noisy multi-objective** (the realistic
   DBTL case); feasibility-weighted EI for constraints. Be able to derive EI's closed form.
3. **DBTL is noisy and multi-objective.** Real assays are noisy and you optimize potency
   *and* selectivity *and* synthesizability at once — so noisy multi-objective + constrained
   BO (Letham qNEI, Daulton qNEHVI) is the center of gravity, not vanilla single-objective EI.
4. **Representation is half the battle.** The surrogate is only as good as the features:
   RDKit fingerprints vs. learned embeddings (Chemprop, chemical VAE, GAUCHE's molecular
   kernels). Deep kernel learning keeps GP uncertainty over learned features.
5. **Prove it beats random.** Always benchmark the loop against random search on a known
   objective and report simple regret — the discipline that catches a broken surrogate. This
   is the honest gate in `labs/merge-bo` and the `bayesopt-loop` skill.

**People to read first:** Frazier (BO tutorial), Garnett (the book), Balandat/Bakshy/Daulton
(BoTorch, qNEHVI), Eriksson (TuRBO/SAASBO), Aspuru-Guzik & Coley (self-driving labs), Yang &
Arnold (ML-guided directed evolution). All in the hub's [People](../../README.md#people--researchers)
section.

**Papers to have at your fingertips:** Frazier 1807.02811 · Snoek 1206.2944 · BoTorch
1910.06403 · qNEHVI 2105.08195 · TuRBO 1910.01739 · GAUCHE 2212.04450 · GPML (R&W).
