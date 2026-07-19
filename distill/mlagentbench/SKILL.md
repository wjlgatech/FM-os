---
name: mlagentbench-quickstart
description: >-
  Get productive with MLAgentBench (eval): Benchmark of end-to-end ML experimentation tasks for measuring how well agents can improve models from a starting codebase. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# mlagentbench-quickstart

A cross-runtime skill for **[MLAgentBench](https://github.com/snap-stanford/MLAgentBench)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Benchmark of end-to-end ML experimentation tasks for measuring how well agents can improve models from a starting codebase.

## When to use (trigger)

Invoke when the user mentions "MLAgentBench", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", "Research judgment & empirical rigor (experiment loop)", or asks to get started with MLAgentBench.

## What it does

1. **Point at it** — clone / install MLAgentBench from https://github.com/snap-stanford/MLAgentBench (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/snap-stanford/MLAgentBench for the authoritative quickstart
git clone https://github.com/snap-stanford/MLAgentBench
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
