---
name: lighteval-quickstart
description: >-
  Get productive with LightEval (eval): Hugging Face all-in-one evaluator across vLLM/Accelerate/TGI backends with 1000+ tasks for small-model eval. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# lighteval-quickstart

A cross-runtime skill for **[LightEval](https://github.com/huggingface/lighteval)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Hugging Face all-in-one evaluator across vLLM/Accelerate/TGI backends with 1000+ tasks for small-model eval.

## When to use (trigger)

Invoke when the user mentions "LightEval", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", or asks to get started with LightEval.

## What it does

1. **Point at it** — clone / install LightEval from https://github.com/huggingface/lighteval (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/huggingface/lighteval for the authoritative quickstart
git clone https://github.com/huggingface/lighteval
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
