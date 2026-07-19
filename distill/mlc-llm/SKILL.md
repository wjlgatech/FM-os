---
name: mlc-llm-quickstart
description: >-
  Get productive with MLC-LLM (serving): ML-compilation deployment engine that compiles SLMs to iOS, Android, WebGPU, and diverse GPUs/CPUs. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# mlc-llm-quickstart

A cross-runtime skill for **[MLC-LLM](https://github.com/mlc-ai/mlc-llm)** — the serving tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): ML-compilation deployment engine that compiles SLMs to iOS, Android, WebGPU, and diverse GPUs/CPUs.

## When to use (trigger)

Invoke when the user mentions "MLC-LLM", "GPU optimization / efficient inference", or asks to get started with MLC-LLM.

## What it does

1. **Point at it** — clone / install MLC-LLM from https://github.com/mlc-ai/mlc-llm (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for serving.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/mlc-ai/mlc-llm for the authoritative quickstart
git clone https://github.com/mlc-ai/mlc-llm
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
