---
name: open-agentrl-quickstart
description: >-
  Get productive with Open-AgentRL (RLAnything / AutoTool) (rl): Open RL for LLMs + agentic scenarios (ICML 2026); RLAnything closed-loop-optimizes each component of the training pipeline. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# open-agentrl-quickstart

A cross-runtime skill for **[Open-AgentRL (RLAnything / AutoTool)](https://github.com/Gen-Verse/Open-AgentRL)** — the rl tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Open RL for LLMs + agentic scenarios (ICML 2026); RLAnything closed-loop-optimizes each component of the training pipeline.

## When to use (trigger)

Invoke when the user mentions "Open-AgentRL (RLAnything / AutoTool)", "Training / fine-tuning foundation models", "Post-training / RL / alignment", or asks to get started with Open-AgentRL (RLAnything / AutoTool).

## What it does

1. **Point at it** — clone / install Open-AgentRL (RLAnything / AutoTool) from https://github.com/Gen-Verse/Open-AgentRL (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for rl.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/Gen-Verse/Open-AgentRL for the authoritative quickstart
git clone https://github.com/Gen-Verse/Open-AgentRL
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
