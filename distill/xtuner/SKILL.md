---
name: xtuner-quickstart
description: >-
  Get productive with XTuner (finetuning): Memory-efficient LLM/VLM fine-tuning engine (LLaVA-style pipelines, large-MoE support) for constrained or very large setups. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# xtuner-quickstart

A cross-runtime skill for **[XTuner](https://github.com/InternLM/xtuner)** — the finetuning tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Memory-efficient LLM/VLM fine-tuning engine (LLaVA-style pipelines, large-MoE support) for constrained or very large setups.

## When to use (trigger)

Invoke when the user mentions "XTuner", "Python / PyTorch / large-scale ML workflows", "Vision-Language / multi-modal models", "Training / fine-tuning foundation models", or asks to get started with XTuner.

## What it does

1. **Point at it** — clone / install XTuner from https://github.com/InternLM/xtuner (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for finetuning.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/InternLM/xtuner for the authoritative quickstart
git clone https://github.com/InternLM/xtuner
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
