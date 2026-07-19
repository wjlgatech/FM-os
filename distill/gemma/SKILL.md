---
name: gemma-quickstart
description: >-
  Get productive with Gemma (DeepMind) (models): Official JAX library for Gemma open weights including the 1B/2B and 3n on-device small variants. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# gemma-quickstart

A cross-runtime skill for **[Gemma (DeepMind)](https://github.com/google-deepmind/gemma)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Official JAX library for Gemma open weights including the 1B/2B and 3n on-device small variants.

## When to use (trigger)

Invoke when the user mentions "Gemma (DeepMind)", "Framework breadth (JAX / TensorFlow / Flax)", or asks to get started with Gemma (DeepMind).

## What it does

1. **Point at it** — clone / install Gemma (DeepMind) from https://github.com/google-deepmind/gemma (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/google-deepmind/gemma for the authoritative quickstart
git clone https://github.com/google-deepmind/gemma
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
