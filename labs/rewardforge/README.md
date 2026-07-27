# RewardForge — eval failures → preference data → a REAL gated fine-tune

**The bridge the OpenAI Personal AGI JDs ask for** ("translate insights into robust evals,
training data, reward signals"): FM-os's certified eval gates already *label* good vs bad
behavior — RewardForge turns those labels into DPO preference pairs and closes the loop with
an actual LoRA fine-tune, judged on held-out worlds, shipped or rolled back by a gate.

## The pipeline (M1)

```
certified eval gates                preference pairs                  real fine-tune
─────────────────────    ──────>   ──────────────────    ──────>    ─────────────────────
syndata-bare alignment              chosen  = grounded               SmolLM2-135M-Instruct
gate (cert 98) ·                    rejected = hallucinated /        + LoRA r=16, from-
vlm-failure-probe                   observed-failure answer          scratch DPO loss
(cert 98)                           provenance on every pair         (torch+peft, no trl)
                                                                          │
                                                              held-out grounding gate
                                                              (8 fact worlds, ZERO word
                                                              overlap with training —
                                                              leakage is a tested property)
                                                              → SHIP or ROLLBACK
```

- **No human labels anywhere:** chosen/rejected come from gates that were themselves
  certified (the alignment gate, the paper-observed VSS failures).
- **DPO from scratch** (`rewardforge/dpo.py`): the Rafailov et al. loss in ~30 lines on
  torch + peft — reference log-probs precomputed before LoRA attaches, one model in memory,
  MPS/CUDA/CPU. Loss math is unit-tested against hand computation.
- **The gate is the deliverable** (`rewardforge/gates.py`): hallucination rate on held-out
  fact worlds must DROP by a real margin without degeneration, else exit non-zero.

## Run it

```bash
make check   # offline: pair provenance + no-leakage + DPO math + gate math (8 tests)
make e2e     # REAL fine-tune (~300 MB model download; minutes on Apple Silicon MPS)
```

Results land in [`out/RESULTS.md`](out/RESULTS.md) — metrics table, sample held-out
generations (evidence), training telemetry.

## Scale seams (M2+)

Swap the pair source for cli-judge verdicts / MCP-Arena failures (same JSONL shape), the
model for Qwen2.5-0.5B/1.5B, the gate for a task benchmark — pipeline unchanged. Multi-seed
+ ablation (auto-pairs vs shuffled pairs) per `skills/research-loop` before any public claim.
Roadmap: `~/Downloads/OpenAI Personal AGI — … — 10X.md` §4 (P1).
