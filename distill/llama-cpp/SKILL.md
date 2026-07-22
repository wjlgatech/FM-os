---
name: llama-cpp-quickstart
description: >-
  Get productive with llama.cpp (serving): C/C++ GGUF inference engine that runs quantized SLMs efficiently on CPUs, laptops, and edge devices. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# llama-cpp-quickstart

A cross-runtime skill for **[llama.cpp](https://github.com/ggml-org/llama.cpp)** — the serving tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): C/C++ GGUF inference engine that runs quantized SLMs efficiently on CPUs, laptops, and edge devices.

## When to use (trigger)

Invoke when the user mentions "llama.cpp", "GPU optimization / efficient inference", or asks to get started with llama.cpp.

## What it does

1. **Point at it** — clone / install llama.cpp from https://github.com/ggml-org/llama.cpp (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for serving.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/ggml-org/llama.cpp for the authoritative quickstart
git clone https://github.com/ggml-org/llama.cpp
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
