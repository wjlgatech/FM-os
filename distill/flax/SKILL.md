---
name: flax-quickstart
description: >-
  Get productive with Flax (jax): Neural-network library for JAX (the NNX API) used across DeepMind/Google research models, including many multimodal architectures. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# flax-quickstart

A cross-runtime skill for **[Flax](https://github.com/google/flax)** — the jax tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Neural-network library for JAX (the NNX API) used across DeepMind/Google research models, including many multimodal architectures.

## When to use (trigger)

Invoke when the user mentions "Flax", "Vision-Language / multi-modal models", "Framework breadth (JAX / TensorFlow / Flax)", "Publishing research (NeurIPS / CVPR)", or asks to get started with Flax.

## What it does

1. **Point at it** — clone / install Flax from https://github.com/google/flax (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for jax.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/google/flax for the authoritative quickstart
git clone https://github.com/google/flax
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
