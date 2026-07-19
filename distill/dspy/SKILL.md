---
name: dspy-quickstart
description: >-
  Get productive with DSPy (research): Define LLM pipelines as modules and optimize their prompts/weights against a metric rather than hand-prompting — the rigor layer for agent pipelines. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# dspy-quickstart

A cross-runtime skill for **[DSPy](https://github.com/stanfordnlp/dspy)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Define LLM pipelines as modules and optimize their prompts/weights against a metric rather than hand-prompting — the rigor layer for agent pipelines.

## When to use (trigger)

Invoke when the user mentions "DSPy", "Research judgment & empirical rigor (experiment loop)", or asks to get started with DSPy.

## What it does

1. **Point at it** — clone / install DSPy from https://github.com/stanfordnlp/dspy (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/stanfordnlp/dspy for the authoritative quickstart
git clone https://github.com/stanfordnlp/dspy
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
