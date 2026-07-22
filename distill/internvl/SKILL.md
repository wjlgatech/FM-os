---
name: internvl-quickstart
description: >-
  Get productive with InternVL (multimodal): Scaled open VLM series with large vision encoders and full training code, competitive on high-resolution perception and video benchmarks. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# internvl-quickstart

A cross-runtime skill for **[InternVL](https://github.com/OpenGVLab/InternVL)** — the multimodal tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Scaled open VLM series with large vision encoders and full training code, competitive on high-resolution perception and video benchmarks.

## When to use (trigger)

Invoke when the user mentions "InternVL", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Training / fine-tuning foundation models", "Agentic evaluation / benchmarking", or asks to get started with InternVL.

## What it does

1. **Point at it** — clone / install InternVL from https://github.com/OpenGVLab/InternVL (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for multimodal.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/OpenGVLab/InternVL for the authoritative quickstart
git clone https://github.com/OpenGVLab/InternVL
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
