---
name: maxtext-quickstart
description: >-
  Get productive with MaxText (jax): High-performance, scalable JAX LLM reference (Google) for TPU/GPU pods, a clean example of large-scale distributed training in JAX. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# maxtext-quickstart

A cross-runtime skill for **[MaxText](https://github.com/AI-Hypercomputer/maxtext)** — the jax tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): High-performance, scalable JAX LLM reference (Google) for TPU/GPU pods, a clean example of large-scale distributed training in JAX.

## When to use (trigger)

Invoke when the user mentions "MaxText", "Training / fine-tuning foundation models", "Framework breadth (JAX / TensorFlow / Flax)", "Distributed training & ML orchestration", or asks to get started with MaxText.

## What it does

1. **Point at it** — clone / install MaxText from https://github.com/AI-Hypercomputer/maxtext (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for jax.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/AI-Hypercomputer/maxtext for the authoritative quickstart
git clone https://github.com/AI-Hypercomputer/maxtext
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
