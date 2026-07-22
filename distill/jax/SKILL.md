---
name: jax-quickstart
description: >-
  Get productive with JAX (jax): Composable NumPy with autodiff, XLA compilation, and pmap/shard_map, the base for large-scale research training on TPUs/GPUs. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# jax-quickstart

A cross-runtime skill for **[JAX](https://github.com/jax-ml/jax)** — the jax tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Composable NumPy with autodiff, XLA compilation, and pmap/shard_map, the base for large-scale research training on TPUs/GPUs.

## When to use (trigger)

Invoke when the user mentions "JAX", "Training / fine-tuning foundation models", "Framework breadth (JAX / TensorFlow / Flax)", "Publishing research (NeurIPS / CVPR)", or asks to get started with JAX.

## What it does

1. **Point at it** — clone / install JAX from https://github.com/jax-ml/jax (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for jax.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/jax-ml/jax for the authoritative quickstart
git clone https://github.com/jax-ml/jax
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
