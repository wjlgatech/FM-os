---
name: verl-quickstart
description: >-
  Get productive with verl (rl): ByteDance HybridFlow RL post-training (PPO/GRPO/DAPO) with vLLM/SGLang; popular for GRPO on small models. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# verl-quickstart

A cross-runtime skill for **[verl](https://github.com/verl-project/verl)** — the rl tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): ByteDance HybridFlow RL post-training (PPO/GRPO/DAPO) with vLLM/SGLang; popular for GRPO on small models.

## When to use (trigger)

Invoke when the user mentions "verl", "Training / fine-tuning foundation models", "Post-training / RL / alignment", or asks to get started with verl.

## What it does

1. **Point at it** — clone / install verl from https://github.com/verl-project/verl (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for rl.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/verl-project/verl for the authoritative quickstart
git clone https://github.com/verl-project/verl
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
