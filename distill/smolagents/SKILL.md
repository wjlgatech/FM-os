---
name: smolagents-quickstart
description: >-
  Get productive with smolagents (research): Barebones code-acting agent library; its examples include Hugging Face's open reproduction of Deep Research. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# smolagents-quickstart

A cross-runtime skill for **[smolagents](https://github.com/huggingface/smolagents)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Barebones code-acting agent library; its examples include Hugging Face's open reproduction of Deep Research.

## When to use (trigger)

Invoke when the user mentions "smolagents", "Research judgment & empirical rigor (experiment loop)", "Publishing research (NeurIPS / CVPR)", or asks to get started with smolagents.

## What it does

1. **Point at it** — clone / install smolagents from https://github.com/huggingface/smolagents (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/huggingface/smolagents for the authoritative quickstart
git clone https://github.com/huggingface/smolagents
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
