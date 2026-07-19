---
name: aviary-quickstart
description: >-
  Get productive with Aviary (eval): Gym-style environment framework for training and evaluating language agents on challenging scientific tasks. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# aviary-quickstart

A cross-runtime skill for **[Aviary](https://github.com/Future-House/aviary)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Gym-style environment framework for training and evaluating language agents on challenging scientific tasks.

## When to use (trigger)

Invoke when the user mentions "Aviary", "Training / fine-tuning foundation models", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", or asks to get started with Aviary.

## What it does

1. **Point at it** — clone / install Aviary from https://github.com/Future-House/aviary (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/Future-House/aviary for the authoritative quickstart
git clone https://github.com/Future-House/aviary
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
