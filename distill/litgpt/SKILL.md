---
name: litgpt-quickstart
description: >-
  Get productive with LitGPT (frameworks): 20+ hackable LLM implementations with pretrain/finetune/deploy recipes, including small Phi/Qwen/Gemma models. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# litgpt-quickstart

A cross-runtime skill for **[LitGPT](https://github.com/Lightning-AI/litgpt)** — the frameworks tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): 20+ hackable LLM implementations with pretrain/finetune/deploy recipes, including small Phi/Qwen/Gemma models.

## When to use (trigger)

Invoke when the user mentions "LitGPT", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", "Distributed training & ML orchestration", or asks to get started with LitGPT.

## What it does

1. **Point at it** — clone / install LitGPT from https://github.com/Lightning-AI/litgpt (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for frameworks.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/Lightning-AI/litgpt for the authoritative quickstart
git clone https://github.com/Lightning-AI/litgpt
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
