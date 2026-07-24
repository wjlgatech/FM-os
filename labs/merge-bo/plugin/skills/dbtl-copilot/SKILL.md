---
name: dbtl-copilot
description: >-
  Run a wet-lab optimization campaign as a closed loop without an ML PhD. Describe
  the goal in plain language ("optimize a peptide for binding affinity, keep cost
  low, 8 assays a week"); the copilot compiles it to a typed spec, proposes the next
  batch of experiments with uncertainty and a rationale, ingests assay results, and
  reports experiments saved vs. random. Use for design-build-test-learn (DBTL),
  Bayesian optimization, active learning, or "which experiment should I run next".
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# dbtl-copilot

The human-facing front of the Helix closed-loop optimization backbone. It turns a
scientist's intent into an optimization campaign and drives it one DBTL cycle at a time,
speaking experiments — not acquisition functions.

## When to use (trigger)

"optimize my experiment / assay", "which candidate should I test next", "design-build-test-learn",
"active learning loop", "Bayesian optimization of a molecule/peptide/protein/reaction",
"I have a limited experiment budget", "multi-objective / constrained optimization of a wet-lab
readout", "encode a constraint / prior into the search".

## How it works (each DBTL cycle)

1. **Compile the brief.** Restate the goal as a typed spec — objectives (max/min), constraints
   (with thresholds), per-cycle batch size, total budget — and surface any *open questions* rather
   than guessing. Confirm with the scientist before running.
2. **Propose.** Call `propose_experiments` → the next batch, each candidate with a predicted value,
   an uncertainty band, and a plain rationale ("highest expected improvement; model uncertain here,
   so it explores"). Feasibility-weighted when constraints exist.
3. **Test.** The scientist runs those experiments in the lab (or a simulator).
4. **Ingest & learn.** Call `ingest_results` with the assay readouts; the surrogate refits and the
   next proposal accounts for them.
5. **Report.** Call `campaign_status` → best-so-far, budget remaining, Pareto front (multi-objective),
   and how many experiments the loop saved versus random search.

## Tools (via the Helix MCP server)

`define_campaign` · `propose_experiments` · `ingest_results` · `campaign_status` — see the plugin's
`.mcp.json`. Campaign state persists, so a campaign survives the days/weeks between proposing a
batch and getting results back.

## Discipline

- **Never invent an objective.** If the brief is ambiguous, ask — the spec's `open_questions` drive
  the clarifying questions.
- **Uncertainty is shown, not hidden.** Every proposal carries its error bar; that is what makes the
  loop explore, not just exploit.
- **Prove the benefit.** Report experiments-saved vs. random, measured — never assert it.

## Example

> "I'm optimizing a fluorescent protein for brightness and photostability. I can run 6 variants a
> week, 36 total, and I need aggregation under 0.3."

→ spec: maximize {brightness, photostability}; aggregation ≤ 0.3; batch 6; budget 36 → propose 6 →
ingest → repeat. Full engine + a runnable simulation: [`labs/merge-bo`](../../../README.md).
