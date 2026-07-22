---
name: llm-awq-quickstart
description: >-
  Get productive with LLM-AWQ (compression): Activation-aware INT3/4 weight quantization (MLSys 2024) plus TinyChat for on-device/edge SLM inference. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# llm-awq-quickstart

A cross-runtime skill for **[LLM-AWQ](https://github.com/mit-han-lab/llm-awq)** — the compression tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Activation-aware INT3/4 weight quantization (MLSys 2024) plus TinyChat for on-device/edge SLM inference.

## When to use (trigger)

Invoke when the user mentions "LLM-AWQ", "GPU optimization / efficient inference", or asks to get started with LLM-AWQ.

## What it does

1. **Point at it** — clone / install LLM-AWQ from https://github.com/mit-han-lab/llm-awq (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for compression.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/mit-han-lab/llm-awq for the authoritative quickstart
git clone https://github.com/mit-han-lab/llm-awq
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
