---
name: penzai-quickstart
description: >-
  Get productive with Penzai (jax): DeepMind JAX toolkit for building and visualizing/interpreting models as legible pytrees, useful for research-grade experimentation. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# penzai-quickstart

A cross-runtime skill for **[Penzai](https://github.com/google-deepmind/penzai)** — the jax tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): DeepMind JAX toolkit for building and visualizing/interpreting models as legible pytrees, useful for research-grade experimentation.

## When to use (trigger)

Invoke when the user mentions "Penzai", "Framework breadth (JAX / TensorFlow / Flax)", "Research judgment & empirical rigor (experiment loop)", "Publishing research (NeurIPS / CVPR)", or asks to get started with Penzai.

## What it does

1. **Point at it** — clone / install Penzai from https://github.com/google-deepmind/penzai (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for jax.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/google-deepmind/penzai for the authoritative quickstart
git clone https://github.com/google-deepmind/penzai
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
