---
name: vlmevalkit-quickstart
description: >-
  Get productive with VLMEvalKit (eval): Broad LMM evaluation toolkit (220+ models, 80+ benchmarks) with unified data prep, complementary to lmms-eval for coverage. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# vlmevalkit-quickstart

A cross-runtime skill for **[VLMEvalKit](https://github.com/open-compass/VLMEvalKit)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Broad LMM evaluation toolkit (220+ models, 80+ benchmarks) with unified data prep, complementary to lmms-eval for coverage.

## When to use (trigger)

Invoke when the user mentions "VLMEvalKit", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", "Retrieval, embeddings & vector databases", or asks to get started with VLMEvalKit.

## What it does

1. **Point at it** — clone / install VLMEvalKit from https://github.com/open-compass/VLMEvalKit (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/open-compass/VLMEvalKit for the authoritative quickstart
git clone https://github.com/open-compass/VLMEvalKit
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
