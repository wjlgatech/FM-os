---
name: qwen2-5-vl-quickstart
description: >-
  Get productive with Qwen2.5-VL (multimodal): Strong open VLM family with native dynamic-resolution and long-video/temporal grounding, a common backbone for fine-tuning on driving footage. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# qwen2-5-vl-quickstart

A cross-runtime skill for **[Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL)** — the multimodal tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Strong open VLM family with native dynamic-resolution and long-video/temporal grounding, a common backbone for fine-tuning on driving footage.

## When to use (trigger)

Invoke when the user mentions "Qwen2.5-VL", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Training / fine-tuning foundation models", "Autonomous-driving / robotics datasets", or asks to get started with Qwen2.5-VL.

## What it does

1. **Point at it** — clone / install Qwen2.5-VL from https://github.com/QwenLM/Qwen2.5-VL (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for multimodal.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/QwenLM/Qwen2.5-VL for the authoritative quickstart
git clone https://github.com/QwenLM/Qwen2.5-VL
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
