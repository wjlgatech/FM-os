---
name: peft-quickstart
description: >-
  Get productive with PEFT (finetuning): Reference library for LoRA/QLoRA and other parameter-efficient methods, enabling SLM tuning on consumer GPUs. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# peft-quickstart

A cross-runtime skill for **[PEFT](https://github.com/huggingface/peft)** — the finetuning tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Reference library for LoRA/QLoRA and other parameter-efficient methods, enabling SLM tuning on consumer GPUs.

## When to use (trigger)

Invoke when the user mentions "PEFT", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", or asks to get started with PEFT.

## What it does

1. **Point at it** — clone / install PEFT from https://github.com/huggingface/peft (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for finetuning.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/huggingface/peft for the authoritative quickstart
git clone https://github.com/huggingface/peft
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
