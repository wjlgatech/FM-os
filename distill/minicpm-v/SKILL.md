---
name: minicpm-v-quickstart
description: >-
  Get productive with MiniCPM-V (multimodal): Efficient end-side VLM series with strong image/video/OCR performance, relevant where on-vehicle or edge inference budgets are tight. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# minicpm-v-quickstart

A cross-runtime skill for **[MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V)** — the multimodal tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Efficient end-side VLM series with strong image/video/OCR performance, relevant where on-vehicle or edge inference budgets are tight.

## When to use (trigger)

Invoke when the user mentions "MiniCPM-V", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "GPU optimization / efficient inference", or asks to get started with MiniCPM-V.

## What it does

1. **Point at it** — clone / install MiniCPM-V from https://github.com/OpenBMB/MiniCPM-V (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for multimodal.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/OpenBMB/MiniCPM-V for the authoritative quickstart
git clone https://github.com/OpenBMB/MiniCPM-V
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
