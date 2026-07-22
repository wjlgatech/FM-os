---
name: agentlaboratory-quickstart
description: >-
  Get productive with Agent Laboratory (research): Multi-agent pipeline that takes a human research idea through literature review, experimentation, and report writing. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# agentlaboratory-quickstart

A cross-runtime skill for **[Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)** — the research tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Multi-agent pipeline that takes a human research idea through literature review, experimentation, and report writing.

## When to use (trigger)

Invoke when the user mentions "Agent Laboratory", "Research judgment & empirical rigor (experiment loop)", "Publishing research (NeurIPS / CVPR)", or asks to get started with Agent Laboratory.

## What it does

1. **Point at it** — clone / install Agent Laboratory from https://github.com/SamuelSchmidgall/AgentLaboratory (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for research.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/SamuelSchmidgall/AgentLaboratory for the authoritative quickstart
git clone https://github.com/SamuelSchmidgall/AgentLaboratory
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
