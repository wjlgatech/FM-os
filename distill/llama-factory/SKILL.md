---
name: llama-factory-quickstart
description: >-
  Get productive with LLaMA-Factory (finetuning): Unified zero-code fine-tuning of 100+ LLMs/VLMs with LoRA/QLoRA/DPO and a web UI, common for SLM tuning. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# llama-factory-quickstart

A cross-runtime skill for **[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)** — the finetuning tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Unified zero-code fine-tuning of 100+ LLMs/VLMs with LoRA/QLoRA/DPO and a web UI, common for SLM tuning.

## When to use (trigger)

Invoke when the user mentions "LLaMA-Factory", "Python / PyTorch / large-scale ML workflows", "Vision-Language / multi-modal models", "Training / fine-tuning foundation models", "Post-training / RL / alignment", or asks to get started with LLaMA-Factory.

## What it does

1. **Point at it** — clone / install LLaMA-Factory from https://github.com/hiyouga/LLaMA-Factory (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for finetuning.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/hiyouga/LLaMA-Factory for the authoritative quickstart
git clone https://github.com/hiyouga/LLaMA-Factory
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
