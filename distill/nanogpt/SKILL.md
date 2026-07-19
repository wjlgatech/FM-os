---
name: nanogpt-quickstart
description: >-
  Get productive with nanoGPT (frameworks): Minimal ~300-line GPT training/finetuning loop; the standard starting point for training small GPTs from scratch. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# nanogpt-quickstart

A cross-runtime skill for **[nanoGPT](https://github.com/karpathy/nanoGPT)** — the frameworks tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Minimal ~300-line GPT training/finetuning loop; the standard starting point for training small GPTs from scratch.

## When to use (trigger)

Invoke when the user mentions "nanoGPT", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", "Distributed training & ML orchestration", or asks to get started with nanoGPT.

## What it does

1. **Point at it** — clone / install nanoGPT from https://github.com/karpathy/nanoGPT (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for frameworks.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/karpathy/nanoGPT for the authoritative quickstart
git clone https://github.com/karpathy/nanoGPT
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
