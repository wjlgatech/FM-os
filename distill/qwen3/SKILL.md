---
name: qwen3-quickstart
description: >-
  Get productive with Qwen3 (models): Alibaba's Qwen series spanning 0.6B/1.7B/4B dense SLMs with strong multilingual and reasoning quality. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# qwen3-quickstart

A cross-runtime skill for **[Qwen3](https://github.com/QwenLM/Qwen3)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Alibaba's Qwen series spanning 0.6B/1.7B/4B dense SLMs with strong multilingual and reasoning quality.

## When to use (trigger)

Invoke when the user mentions "Qwen3", or asks to get started with Qwen3.

## What it does

1. **Point at it** — clone / install Qwen3 from https://github.com/QwenLM/Qwen3 (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/QwenLM/Qwen3 for the authoritative quickstart
git clone https://github.com/QwenLM/Qwen3
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
