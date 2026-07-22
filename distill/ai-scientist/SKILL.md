---
name: ai-scientist-quickstart
description: >-
  Get productive with AI-Scientist (research): Runs a full loop that generates ideas, writes and executes experiment code, plots results, and drafts a paper with an automated reviewer. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# ai-scientist-quickstart

A cross-runtime skill for **[AI-Scientist](https://github.com/SakanaAI/AI-Scientist)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Runs a full loop that generates ideas, writes and executes experiment code, plots results, and drafts a paper with an automated reviewer.

## When to use (trigger)

Invoke when the user mentions "AI-Scientist", "Research judgment & empirical rigor (experiment loop)", or asks to get started with AI-Scientist.

## What it does

1. **Point at it** — clone / install AI-Scientist from https://github.com/SakanaAI/AI-Scientist (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/SakanaAI/AI-Scientist for the authoritative quickstart
git clone https://github.com/SakanaAI/AI-Scientist
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
