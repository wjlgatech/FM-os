---
name: axolotl-quickstart
description: >-
  Get productive with Axolotl (finetuning): Config-driven post-training framework covering SFT/LoRA/DPO across many small and large model families. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# axolotl-quickstart

A cross-runtime skill for **[Axolotl](https://github.com/axolotl-ai-cloud/axolotl)** — the finetuning tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Config-driven post-training framework covering SFT/LoRA/DPO across many small and large model families.

## When to use (trigger)

Invoke when the user mentions "Axolotl", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", "Post-training / RL / alignment", or asks to get started with Axolotl.

## What it does

1. **Point at it** — clone / install Axolotl from https://github.com/axolotl-ai-cloud/axolotl (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for finetuning.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/axolotl-ai-cloud/axolotl for the authoritative quickstart
git clone https://github.com/axolotl-ai-cloud/axolotl
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
