---
name: gymnasium-quickstart
description: >-
  Get productive with Gymnasium (Farama) (rl): The maintained successor to OpenAI Gym — the standard environment API most RL training stacks (incl. RLlib) build on. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# gymnasium-quickstart

A cross-runtime skill for **[Gymnasium (Farama)](https://github.com/Farama-Foundation/Gymnasium)** — the rl tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): The maintained successor to OpenAI Gym — the standard environment API most RL training stacks (incl. RLlib) build on.

## When to use (trigger)

Invoke when the user mentions "Gymnasium (Farama)", "Training / fine-tuning foundation models", "Post-training / RL / alignment", or asks to get started with Gymnasium (Farama).

## What it does

1. **Point at it** — clone / install Gymnasium (Farama) from https://github.com/Farama-Foundation/Gymnasium (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for rl.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/Farama-Foundation/Gymnasium for the authoritative quickstart
git clone https://github.com/Farama-Foundation/Gymnasium
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
