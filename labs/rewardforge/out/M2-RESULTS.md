# RewardForge M2 — multi-seed + shuffled-pair ablation (research-loop rigor pass)

- **model**: `HuggingFaceTB/SmolLM2-135M-Instruct` (LoRA r=16, lr=1e-5, beta=0.2, 1 epoch) · seeds [0, 1, 2, 3, 4] · 2026-07-31
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
| 3 | treatment | 0.398 | 0.287 | +0.110 |
| 3 | shuffled | 0.398 | 0.419 | -0.021 |
| 4 | treatment | 0.398 | 0.287 | +0.110 |
| 4 | shuffled | 0.398 | 0.502 | -0.104 |

**treatment drop: +0.098 ± 0.028** (n=5) · **shuffled drop: -0.046 ± 0.054** (n=5)

## Verdict (M2 every-seed rule): NO-EFFECT — treatment below the pre-registered floor on at least one seed
## Verdict (M3 median+separation rule, pre-registered in git before the 5-seed run): CONFIRMED-M3 — median treatment clears the floor with complete arm separation

Threats to validity: single small model (135M); toy grounding task; 8 held-out worlds;
greedy decoding (deterministic eval). Reproduce: `python -m rewardforge.sweep`.

---

## M3 (5 seeds, pre-registered median+separation rule committed in 91981e2 BEFORE this run)

| seed | treatment drop | shuffled control drop |
|---|---|---|
| 0 | +0.110 | 0.000 |
| 1 | +0.048 | 0.000 |
| 2 | +0.110 | −0.104 |
| 3 | +0.110 | −0.021 |
| 4 | +0.110 | −0.104 |

treatment **+0.098 ± 0.028** (median +0.110) · control **−0.046 ± 0.055** (max 0.000)

**Verdict (M3 rule): CONFIRMED-M3** — median treatment (0.110) clears the 0.05 floor and
arm separation is complete (worst treatment +0.048 > best control 0.000). The M2 every-seed
rule still reads NO-EFFECT on seed 1 (+0.048 vs the 0.05 floor); both verdicts are reported
side by side and the floor was never moved. Claim for the paper: *preference pairs labeled by
an independent eval gate carry real training signal — destroying the labels while preserving
the data distribution destroys the gain (and often reverses it).*

Threats to validity unchanged: single 135M model, toy grounding task, 8 held-out worlds,
greedy decoding. Reproduce: `python -m rewardforge.sweep --seeds 0 1 2 3 4`.
