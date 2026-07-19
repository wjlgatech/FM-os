---
name: unsloth-quickstart
description: >-
  Get productive with Unsloth (finetuning): 2x-faster, ~70%-less-VRAM finetuning for small models, ideal for LoRA/QLoRA on single-GPU setups. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# unsloth-quickstart

A cross-runtime skill for **[Unsloth](https://github.com/unslothai/unsloth)** — the finetuning tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): 2x-faster, ~70%-less-VRAM finetuning for small models, ideal for LoRA/QLoRA on single-GPU setups.

## When to use (trigger)

Invoke when the user mentions "Unsloth", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", or asks to get started with Unsloth.

## What it does

1. **Point at it** — clone / install Unsloth from https://github.com/unslothai/unsloth (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for finetuning.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/unslothai/unsloth for the authoritative quickstart
git clone https://github.com/unslothai/unsloth
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
