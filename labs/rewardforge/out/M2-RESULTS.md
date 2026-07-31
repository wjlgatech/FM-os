# RewardForge M2 — multi-seed + shuffled-pair ablation (research-loop rigor pass)

- **model**: `HuggingFaceTB/SmolLM2-135M-Instruct` (LoRA r=16, lr=1e-5, beta=0.2, 1 epoch) · seeds [0, 1, 2] · 2026-07-31
- **treatment**: eval-derived pairs (labels from FM-os certified gates)
- **ablation control**: identical pairs, chosen/rejected randomly swapped 50% per pair (seeded)
- **pre-registered**: treatment floor drop ≥ 0.05; verdict rules declared in `rewardforge/sweep.py` before running

| seed | arm | halluc before | after | drop |
|---|---|---|---|---|
| 0 | treatment | 0.398 | 0.287 | +0.110 |
| 0 | shuffled | 0.398 | 0.398 | +0.000 |
| 1 | treatment | 0.398 | 0.350 | +0.048 |
| 1 | shuffled | 0.398 | 0.398 | +0.000 |
| 2 | treatment | 0.398 | 0.287 | +0.110 |
| 2 | shuffled | 0.398 | 0.502 | -0.104 |

**treatment drop: +0.090 ± 0.036** (n=3) · **shuffled drop: -0.035 ± 0.060** (n=3)

## Verdict: NO-EFFECT — treatment below the pre-registered floor on at least one seed

Honest reading (the verdict above stands — pre-registration is not renegotiable post-hoc):
the arm separation is complete — every treatment seed improved (+0.048 to +0.110) and every
shuffled control was flat or worse (0.000, 0.000, −0.104); best control < worst treatment.
The CONFIRMED criterion was missed by 0.002 on one seed's floor. We report NO-EFFECT per the
pre-registered rule and note the full separation as the motivating result for the next run
(same criterion, more seeds — the floor does not move because the data wants it to).

Threats to validity: single small model (135M); toy grounding task; 8 held-out worlds;
greedy decoding (deterministic eval). Reproduce: `python -m rewardforge.sweep`.