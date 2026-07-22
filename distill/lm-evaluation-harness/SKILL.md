---
name: lm-evaluation-harness-quickstart
description: >-
  Get productive with lm-evaluation-harness (eval): De-facto standard few-shot eval harness (60+ benchmarks) backing the Open LLM Leaderboard, ideal for SLM benchmarking. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# lm-evaluation-harness-quickstart

A cross-runtime skill for **[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): De-facto standard few-shot eval harness (60+ benchmarks) backing the Open LLM Leaderboard, ideal for SLM benchmarking.

## When to use (trigger)

Invoke when the user mentions "lm-evaluation-harness", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", or asks to get started with lm-evaluation-harness.

## What it does

1. **Point at it** — clone / install lm-evaluation-harness from https://github.com/EleutherAI/lm-evaluation-harness (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/EleutherAI/lm-evaluation-harness for the authoritative quickstart
git clone https://github.com/EleutherAI/lm-evaluation-harness
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
