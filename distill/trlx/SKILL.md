---
name: trlx-quickstart
description: >-
  Get productive with trlX (rl): Distributed RLHF framework (PPO, ILQL) via Accelerate/NeMo; an early, widely-cited RLHF reference. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# trlx-quickstart

A cross-runtime skill for **[trlX](https://github.com/CarperAI/trlx)** — the rl tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Distributed RLHF framework (PPO, ILQL) via Accelerate/NeMo; an early, widely-cited RLHF reference.

## When to use (trigger)

Invoke when the user mentions "trlX", "Post-training / RL / alignment", "Distributed training & ML orchestration", or asks to get started with trlX.

## What it does

1. **Point at it** — clone / install trlX from https://github.com/CarperAI/trlx (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for rl.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/CarperAI/trlx for the authoritative quickstart
git clone https://github.com/CarperAI/trlx
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
