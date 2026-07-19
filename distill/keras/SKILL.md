---
name: keras-quickstart
description: >-
  Get productive with Keras (jax): Multi-backend (JAX / TensorFlow / PyTorch) high-level API, handy for portable model code across the three frameworks this role expects. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# keras-quickstart

A cross-runtime skill for **[Keras](https://github.com/keras-team/keras)** — the jax tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Multi-backend (JAX / TensorFlow / PyTorch) high-level API, handy for portable model code across the three frameworks this role expects.

## When to use (trigger)

Invoke when the user mentions "Keras", "Python / PyTorch / large-scale ML workflows", "Framework breadth (JAX / TensorFlow / Flax)", or asks to get started with Keras.

## What it does

1. **Point at it** — clone / install Keras from https://github.com/keras-team/keras (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for jax.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/keras-team/keras for the authoritative quickstart
git clone https://github.com/keras-team/keras
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
