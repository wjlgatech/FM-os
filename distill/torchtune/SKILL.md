---
name: torchtune-quickstart
description: >-
  Get productive with torchtune (finetuning): PyTorch-native post-training recipes (SFT, distillation, DPO/PPO/GRPO, QAT) tuned for memory-limited hardware. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# torchtune-quickstart

A cross-runtime skill for **[torchtune](https://github.com/meta-pytorch/torchtune)** — the finetuning tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): PyTorch-native post-training recipes (SFT, distillation, DPO/PPO/GRPO, QAT) tuned for memory-limited hardware.

## When to use (trigger)

Invoke when the user mentions "torchtune", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", "Post-training / RL / alignment", or asks to get started with torchtune.

## What it does

1. **Point at it** — clone / install torchtune from https://github.com/meta-pytorch/torchtune (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for finetuning.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/meta-pytorch/torchtune for the authoritative quickstart
git clone https://github.com/meta-pytorch/torchtune
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
