---
name: levanter-quickstart
description: >-
  Get productive with Levanter (jax): JAX/Equinox framework for legible, scalable, reproducible foundation-model training with bitwise determinism across hardware. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# levanter-quickstart

A cross-runtime skill for **[Levanter](https://github.com/marin-community/levanter)** — the jax tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): JAX/Equinox framework for legible, scalable, reproducible foundation-model training with bitwise determinism across hardware.

## When to use (trigger)

Invoke when the user mentions "Levanter", "Training / fine-tuning foundation models", "Framework breadth (JAX / TensorFlow / Flax)", "Research judgment & empirical rigor (experiment loop)", or asks to get started with Levanter.

## What it does

1. **Point at it** — clone / install Levanter from https://github.com/marin-community/levanter (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for jax.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/marin-community/levanter for the authoritative quickstart
git clone https://github.com/marin-community/levanter
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
