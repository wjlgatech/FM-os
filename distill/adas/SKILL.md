---
name: adas-quickstart
description: >-
  Get productive with ADAS (research): Meta-agent that iteratively programs and evaluates new agent designs in code, automating the search over agentic systems. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# adas-quickstart

A cross-runtime skill for **[ADAS](https://github.com/ShengranHu/ADAS)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Meta-agent that iteratively programs and evaluates new agent designs in code, automating the search over agentic systems.

## When to use (trigger)

Invoke when the user mentions "ADAS", "Agentic evaluation / benchmarking", "Research judgment & empirical rigor (experiment loop)", or asks to get started with ADAS.

## What it does

1. **Point at it** — clone / install ADAS from https://github.com/ShengranHu/ADAS (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/ShengranHu/ADAS for the authoritative quickstart
git clone https://github.com/ShengranHu/ADAS
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
