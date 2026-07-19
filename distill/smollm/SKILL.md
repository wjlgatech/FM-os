---
name: smollm-quickstart
description: >-
  Get productive with SmolLM / SmolLM2 / SmolLM3 (models): Fully open recipes, data, and weights for the 135M-3B SmolLM family, the reference open SLM line. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# smollm-quickstart

A cross-runtime skill for **[SmolLM / SmolLM2 / SmolLM3](https://github.com/huggingface/smollm)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Fully open recipes, data, and weights for the 135M-3B SmolLM family, the reference open SLM line.

## When to use (trigger)

Invoke when the user mentions "SmolLM / SmolLM2 / SmolLM3", or asks to get started with SmolLM / SmolLM2 / SmolLM3.

## What it does

1. **Point at it** — clone / install SmolLM / SmolLM2 / SmolLM3 from https://github.com/huggingface/smollm (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/huggingface/smollm for the authoritative quickstart
git clone https://github.com/huggingface/smollm
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
