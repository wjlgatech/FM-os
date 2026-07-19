---
name: tinyllama-quickstart
description: >-
  Get productive with TinyLlama (models): Compact 1.1B Llama pretrained on 3T tokens; a canonical, reproducible sub-2B pretraining reference. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# tinyllama-quickstart

A cross-runtime skill for **[TinyLlama](https://github.com/jzhang38/TinyLlama)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Compact 1.1B Llama pretrained on 3T tokens; a canonical, reproducible sub-2B pretraining reference.

## When to use (trigger)

Invoke when the user mentions "TinyLlama", "Training / fine-tuning foundation models", "Research judgment & empirical rigor (experiment loop)", or asks to get started with TinyLlama.

## What it does

1. **Point at it** — clone / install TinyLlama from https://github.com/jzhang38/TinyLlama (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/jzhang38/TinyLlama for the authoritative quickstart
git clone https://github.com/jzhang38/TinyLlama
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
