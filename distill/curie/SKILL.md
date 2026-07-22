---
name: curie-quickstart
description: >-
  Get productive with Curie (research): Experimentation agent that enforces methodological rigor (controlled setup, reproducibility) when running and analyzing experiments. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# curie-quickstart

A cross-runtime skill for **[Curie](https://github.com/Just-Curieous/Curie)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Experimentation agent that enforces methodological rigor (controlled setup, reproducibility) when running and analyzing experiments.

## When to use (trigger)

Invoke when the user mentions "Curie", "Research judgment & empirical rigor (experiment loop)", or asks to get started with Curie.

## What it does

1. **Point at it** — clone / install Curie from https://github.com/Just-Curieous/Curie (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/Just-Curieous/Curie for the authoritative quickstart
git clone https://github.com/Just-Curieous/Curie
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
