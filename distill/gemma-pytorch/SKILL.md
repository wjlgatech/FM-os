---
name: gemma-pytorch-quickstart
description: >-
  Get productive with gemma_pytorch (models): Official PyTorch inference implementation of Gemma (incl. small text-only variants) for CPU/GPU/TPU. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# gemma-pytorch-quickstart

A cross-runtime skill for **[gemma_pytorch](https://github.com/google/gemma_pytorch)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Official PyTorch inference implementation of Gemma (incl. small text-only variants) for CPU/GPU/TPU.

## When to use (trigger)

Invoke when the user mentions "gemma_pytorch", "Python / PyTorch / large-scale ML workflows", "GPU optimization / efficient inference", or asks to get started with gemma_pytorch.

## What it does

1. **Point at it** — clone / install gemma_pytorch from https://github.com/google/gemma_pytorch (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/google/gemma_pytorch for the authoritative quickstart
git clone https://github.com/google/gemma_pytorch
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
