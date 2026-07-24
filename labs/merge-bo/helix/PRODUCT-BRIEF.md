# Helix — the Design·Build·Test·Learn Copilot

*A product brief for Merge Labs, built from the FM-os / merge-bo case study.*

> "Starting from a blank slate, you'll first architect the company's closed-loop
> optimization backbone… translate these prototypes into production pipelines that
> measurably improve experimental throughput… integrate ML models with experimental data
> streams and **serve to non-domain experts for model democratization**."
> — Merge Labs, *ML Research Scientist, Bayesian Optimization*

Helix is that backbone, shipped as a product. It is the thing the JD asks the first hire to
build — so it doubles as the strongest possible interview artifact: not a slide about what
you'd build, but the working system.

---

## The problem it kills

A DBTL campaign at a bench looks like this today: a scientist picks the next variants to test
mostly by intuition and a spreadsheet; each cycle is a week and real money; nobody can say how
many experiments were *wasted*; and the one ML person who could run Bayesian optimization is a
bottleneck who has to be in every loop. The optimization backbone either doesn't exist yet or
lives in a notebook only its author can drive.

## What Helix does

A wet-lab scientist describes the campaign in plain language. Helix:

1. **Compiles intent to a contract.** "Optimize a peptide for binding affinity, keep cost
   under 0.7, also maximize stability, 6 assays a week, ~30 total" → a typed `OptimizationSpec`
   (objectives with direction, constraints with thresholds, batch size, budget). Anything
   ambiguous becomes an **open question** — it never invents an objective.
2. **Proposes the next batch** with a GP surrogate + acquisition function — each candidate
   carrying a predicted value, an **uncertainty band**, and a one-line rationale ("model unsure
   here, so it explores"). Feasibility-weighted when constraints exist; hypervolume-driven when
   multi-objective.
3. **Ingests assay results and refits** — and because campaign state persists, it survives the
   days or weeks between proposing a batch and the lab reporting back.
4. **Shows the value, measured:** best-so-far vs. random, experiments saved to hit target, and
   the Pareto front for trade-offs. See [`out/helix-dashboard.png`](../out/helix-dashboard.png).

## Why it's a wow (the demo numbers, computed live)

On a molecular optimization benchmark, averaged over 8 campaigns:

- **108 experiments saved** (median) to reach 90% of the optimum vs. random search.
- **+79% better** best candidate at an equal budget.
- **7 Pareto-optimal designs** mapped for a potency-vs-selectivity trade-off.

Every number regenerates with `python -m helix.build_dashboard` — nothing is hand-entered.

## Democratization is the point — it ships as agent tooling

The reason Helix "serves non-domain experts" is that it isn't a library you import; it's a set
of tools an agent (Claude) drives on the scientist's behalf:

| Tooling | What it is | Why it matters to Merge |
|---|---|---|
| **Skill** `dbtl-copilot` | The conversational front — turns intent into a campaign, speaks *experiments* not acquisition functions | A scientist runs BO without an ML PhD |
| **Command** `/dbtl-cycle` | One-shot "advance my campaign a cycle" | Zero-friction daily driver |
| **Hook** `on_new_results` | Auto-ingests + refits the moment an assay CSV lands | No cycle stalls waiting for a human to click "ingest" |
| **MCP server** | `define_campaign · propose_experiments · ingest_results · campaign_status` | Any client (Claude Desktop) becomes the campaign console — the backbone is a service, not a notebook |
| **Workflow** `dbtl-campaign` | Deterministic multi-cycle orchestration | Reproducible campaign runs, CI-gateable |

The whole thing installs as one Claude Code plugin (`plugin/`). That is the "model
democratization" line, executable.

## Architecture (production-shaped, not a toy)

```
scientist ─ plain language ─▶ dbtl-copilot skill ─▶ Helix MCP server
                                                       │
        spec.py (typed contract) ◀────────────────────┤
        campaign.py (persistent DBTL loop) ────────────┤ propose / ingest / status
                                                       │
        merge_bo engine: GP surrogate · EI/UCB/         │
        constrained-EI/EHVI · BoTorch adapter ◀─────────┘
```

Swap seams for production: the numpy GP → BoTorch `SingleTaskGP`/`qNEHVI`; the synthetic assay
→ real instrument data streams; the discrete pool → your enumerated/generated library or GAUCHE
molecular kernels. The interfaces don't change — that's the point of the seams (see
[`../ARCHITECTURE.md`](../ARCHITECTURE.md)).

## What would make it real at Merge (the roadmap conversation)

- **Noisy multi-objective + constraints as first-class** (qNEHVI) — DBTL is never single-objective.
- **Batch/async scheduling** via Ax's service API for parallel wet-lab throughput.
- **Transfer & priors** across campaigns (warm-start a new target from a related one).
- **Instrument integration** — the MCP `ingest_results` tool behind a LIMS/robotics adapter.
- **Neuro vertical** — the same loop over device/stimulation parameters, not just molecules.

## Try it

```bash
cd labs/merge-bo
make check              # 21 tests: engine + product
python -m helix.build_dashboard   # regenerate the live dashboard
python -m helix.mcp_server        # run the MCP server (wire via plugin/.mcp.json)
```
