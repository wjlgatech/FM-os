---
name: openrlhf-quickstart
description: >-
  Get productive with OpenRLHF (rl): Ray+vLLM RLHF framework (PPO/GRPO/RLOO) that scales from small models up to 70B+, agent-friendly. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# openrlhf-quickstart

A cross-runtime skill for **[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)** — the rl tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Ray+vLLM RLHF framework (PPO/GRPO/RLOO) that scales from small models up to 70B+, agent-friendly.

## When to use (trigger)

Invoke when the user mentions "OpenRLHF", "Post-training / RL / alignment", "Distributed training & ML orchestration", or asks to get started with OpenRLHF.

## What it does

1. **Point at it** — clone / install OpenRLHF from https://github.com/OpenRLHF/OpenRLHF (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for rl.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/OpenRLHF/OpenRLHF for the authoritative quickstart
git clone https://github.com/OpenRLHF/OpenRLHF
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
