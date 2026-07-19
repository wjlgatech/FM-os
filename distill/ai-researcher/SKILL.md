---
name: ai-researcher-quickstart
description: >-
  Get productive with AI-Researcher (research): Automates the research pipeline from literature analysis through algorithm implementation to paper generation. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# ai-researcher-quickstart

A cross-runtime skill for **[AI-Researcher](https://github.com/HKUDS/AI-Researcher)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Automates the research pipeline from literature analysis through algorithm implementation to paper generation.

## When to use (trigger)

Invoke when the user mentions "AI-Researcher", "Research judgment & empirical rigor (experiment loop)", "Publishing research (NeurIPS / CVPR)", or asks to get started with AI-Researcher.

## What it does

1. **Point at it** — clone / install AI-Researcher from https://github.com/HKUDS/AI-Researcher (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/HKUDS/AI-Researcher for the authoritative quickstart
git clone https://github.com/HKUDS/AI-Researcher
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
