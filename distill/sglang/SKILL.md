---
name: sglang-quickstart
description: >-
  Get productive with SGLang (serving): Fast serving runtime with RadixAttention and structured decoding plus VLM support, strong for high-concurrency multimodal endpoints. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# sglang-quickstart

A cross-runtime skill for **[SGLang](https://github.com/sgl-project/sglang)** — the serving tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Fast serving runtime with RadixAttention and structured decoding plus VLM support, strong for high-concurrency multimodal endpoints.

## When to use (trigger)

Invoke when the user mentions "SGLang", "Vision-Language / multi-modal models", "Post-training / RL / alignment", "GPU optimization / efficient inference", or asks to get started with SGLang.

## What it does

1. **Point at it** — clone / install SGLang from https://github.com/sgl-project/sglang (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for serving.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/sgl-project/sglang for the authoritative quickstart
git clone https://github.com/sgl-project/sglang
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
