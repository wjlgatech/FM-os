---
description: Run one Design·Build·Test·Learn cycle for a Helix campaign — propose the next batch, help record results, and report progress.
argument-hint: "<campaign-name> [batch-size]"
---

# /dbtl-cycle

Advance the Helix campaign named **$1** by one closed-loop cycle.

1. Call the `propose_experiments` MCP tool for campaign `$1` (batch `$2` if given). Present each
   proposed experiment as a card: candidate id, key features, predicted value ± uncertainty, and the
   one-line rationale. Lead with the highest-expected-improvement pick.
2. Ask the scientist to run those experiments and paste back the readouts (or drop a
   `campaigns/$1.inbox.csv` — the Helix hook will auto-ingest).
3. When results arrive, call `ingest_results` for campaign `$1`.
4. Call `campaign_status` and report: best-so-far, budget remaining, and (if multi-objective) the
   Pareto-front size. If a known simulator is in play, also state experiments saved vs. random.

Never invent objectives or thresholds — if the campaign has open questions, resolve them first with
`define_campaign`. Keep the language about *experiments*, not acquisition functions.
