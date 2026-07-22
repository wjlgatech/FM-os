---
name: bitnet-quickstart
description: >-
  Get productive with BitNet (compression): Official 1-bit (1.58-bit) LLM inference framework with optimized CPU/GPU kernels for extreme efficiency. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# bitnet-quickstart

A cross-runtime skill for **[BitNet](https://github.com/microsoft/BitNet)** — the compression tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Official 1-bit (1.58-bit) LLM inference framework with optimized CPU/GPU kernels for extreme efficiency.

## When to use (trigger)

Invoke when the user mentions "BitNet", "GPU optimization / efficient inference", or asks to get started with BitNet.

## What it does

1. **Point at it** — clone / install BitNet from https://github.com/microsoft/BitNet (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for compression.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/microsoft/BitNet for the authoritative quickstart
git clone https://github.com/microsoft/BitNet
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
