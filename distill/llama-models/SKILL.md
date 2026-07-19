---
name: llama-models-quickstart
description: >-
  Get productive with Llama Models (models): Meta's official utilities and model cards for Llama, including the 1B/3B Llama 3.2 on-device SLMs. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# llama-models-quickstart

A cross-runtime skill for **[Llama Models](https://github.com/meta-llama/llama-models)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Meta's official utilities and model cards for Llama, including the 1B/3B Llama 3.2 on-device SLMs.

## When to use (trigger)

Invoke when the user mentions "Llama Models", or asks to get started with Llama Models.

## What it does

1. **Point at it** — clone / install Llama Models from https://github.com/meta-llama/llama-models (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/meta-llama/llama-models for the authoritative quickstart
git clone https://github.com/meta-llama/llama-models
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
