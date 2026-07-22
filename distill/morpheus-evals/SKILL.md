---
name: morpheus-evals-quickstart
description: >-
  Get productive with MORPHEUS evals (Skyfall) (eval): Open eval code for MORPHEUS, a persistent enterprise simulation for CONTINUAL RL: no episode resets, structured non-stationarity (failure-injection + config shifts), composite verifier reward. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# morpheus-evals-quickstart

A cross-runtime skill for **[MORPHEUS evals (Skyfall)](https://github.com/Skyfall-Research/morpheus-evals)** — the eval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Open eval code for MORPHEUS, a persistent enterprise simulation for CONTINUAL RL: no episode resets, structured non-stationarity (failure-injection + config shifts), composite verifier reward.

## When to use (trigger)

Invoke when the user mentions "MORPHEUS evals (Skyfall)", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", or asks to get started with MORPHEUS evals (Skyfall).

## What it does

1. **Point at it** — clone / install MORPHEUS evals (Skyfall) from https://github.com/Skyfall-Research/morpheus-evals (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for eval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/Skyfall-Research/morpheus-evals for the authoritative quickstart
git clone https://github.com/Skyfall-Research/morpheus-evals
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
