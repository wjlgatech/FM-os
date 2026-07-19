---
name: deepspeed-quickstart
description: >-
  Get productive with DeepSpeed (frameworks): ZeRO sharding, offload, and pipeline/tensor parallelism that make large VLM training fit real GPU budgets; wired into most trainers. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# deepspeed-quickstart

A cross-runtime skill for **[DeepSpeed](https://github.com/deepspeedai/DeepSpeed)** — the frameworks tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): ZeRO sharding, offload, and pipeline/tensor parallelism that make large VLM training fit real GPU budgets; wired into most trainers.

## When to use (trigger)

Invoke when the user mentions "DeepSpeed", "Python / PyTorch / large-scale ML workflows", "Vision-Language / multi-modal models", "Training / fine-tuning foundation models", "Distributed training & ML orchestration", or asks to get started with DeepSpeed.

## What it does

1. **Point at it** — clone / install DeepSpeed from https://github.com/deepspeedai/DeepSpeed (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for frameworks.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/deepspeedai/DeepSpeed for the authoritative quickstart
git clone https://github.com/deepspeedai/DeepSpeed
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
