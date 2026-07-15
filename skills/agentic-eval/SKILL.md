---
name: agentic-eval
description: >-
  Build an agentic evaluation framework for Vision-Language Models on video:
  benchmark spatiotemporal reasoning, localization accuracy, and narrative
  consistency, with an LLM-as-judge harness and regression gates. Turns eval
  from a one-off script into a repeatable, gated pipeline.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# agentic-eval

A cross-runtime skill that stands up a **repeatable, gated evaluation** pipeline for VLMs on
video — the "agentic evaluation frameworks" a motion-understanding team needs. Uses vetted open
eval tooling from [FM-os](https://github.com/wjlgatech/FM-os).

## When to use (trigger)

Invoke when the user says "build an eval framework", "benchmark spatiotemporal reasoning",
"measure localization accuracy", "narrative consistency", or "gate model quality in CI".

## What it does

1. **Assemble benchmarks** — wires `lmms-eval` / `VLMEvalKit` tasks (Video-MME, MMBench-Video,
   grounding/localization sets) into one runner.
2. **Score three axes** — spatiotemporal reasoning, localization accuracy (IoU / temporal IoU),
   and narrative consistency (LLM-as-judge with chain-of-thought, majority-vote to reduce bias).
3. **Gate** — asserts each axis stays above a threshold; exits non-zero so a regression blocks CI
   (the same no-evidence-⇒-No discipline as FM-os Certified).
4. **Report** — emits a per-axis scorecard + a diff against the previous run.

## Example

```bash
pip install lmms-eval
python -m lmms_eval --model qwen2_5_vl --tasks videomme,mmbench_video --output ./eval.json
python eval_gate.py --results ./eval.json --min-spatiotemporal 0.55 --min-localization 0.45
# non-zero exit if any axis regresses -> CI fails
```

## Verification (eval-with-teeth)

The gate itself is the test: it runs against a fixed held-out set and fails the build on
regression. Ships a tiny fixture so `pytest` can assert the gate math.

## Safety

Read-only over model outputs; no shell beyond documented eval commands; no secrets.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
