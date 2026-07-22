---
name: video-llava-quickstart
description: >-
  Get productive with Video-LLaVA (multimodal): Unified image+video projection into one representation before the LLM, a compact reference for joint image/video instruction tuning. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# video-llava-quickstart

A cross-runtime skill for **[Video-LLaVA](https://github.com/PKU-YuanGroup/Video-LLaVA)** — the multimodal tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Unified image+video projection into one representation before the LLM, a compact reference for joint image/video instruction tuning.

## When to use (trigger)

Invoke when the user mentions "Video-LLaVA", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", or asks to get started with Video-LLaVA.

## What it does

1. **Point at it** — clone / install Video-LLaVA from https://github.com/PKU-YuanGroup/Video-LLaVA (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for multimodal.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/PKU-YuanGroup/Video-LLaVA for the authoritative quickstart
git clone https://github.com/PKU-YuanGroup/Video-LLaVA
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
