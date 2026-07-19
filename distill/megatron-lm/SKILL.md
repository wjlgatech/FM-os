---
name: megatron-lm-quickstart
description: >-
  Get productive with Megatron-LM (frameworks): NVIDIA's GPU-optimized library and building blocks for large-scale transformer pretraining. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# megatron-lm-quickstart

A cross-runtime skill for **[Megatron-LM](https://github.com/NVIDIA/Megatron-LM)** — the frameworks tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): NVIDIA's GPU-optimized library and building blocks for large-scale transformer pretraining.

## When to use (trigger)

Invoke when the user mentions "Megatron-LM", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", "Distributed training & ML orchestration", or asks to get started with Megatron-LM.

## What it does

1. **Point at it** — clone / install Megatron-LM from https://github.com/NVIDIA/Megatron-LM (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for frameworks.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/NVIDIA/Megatron-LM for the authoritative quickstart
git clone https://github.com/NVIDIA/Megatron-LM
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
