---
name: lmms-eval-quickstart
description: >-
  Get productive with lmms-eval (eval): One-command multimodal eval harness across image/video/audio benchmarks, the standard for consistent VLM regression testing. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# lmms-eval-quickstart

A cross-runtime skill for **[lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): One-command multimodal eval harness across image/video/audio benchmarks, the standard for consistent VLM regression testing.

## When to use (trigger)

Invoke when the user mentions "lmms-eval", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", or asks to get started with lmms-eval.

## What it does

1. **Point at it** — clone / install lmms-eval from https://github.com/EvolvingLMMs-Lab/lmms-eval (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/EvolvingLMMs-Lab/lmms-eval for the authoritative quickstart
git clone https://github.com/EvolvingLMMs-Lab/lmms-eval
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
