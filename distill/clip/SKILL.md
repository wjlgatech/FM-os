---
name: clip-quickstart
description: >-
  Get productive with CLIP (multimodal): Original contrastive image-text model; the reference whose embeddings still anchor most multimodal retrieval and probing. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# clip-quickstart

A cross-runtime skill for **[CLIP](https://github.com/openai/CLIP)** — the multimodal tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Original contrastive image-text model; the reference whose embeddings still anchor most multimodal retrieval and probing.

## When to use (trigger)

Invoke when the user mentions "CLIP", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Agentic evaluation / benchmarking", "Retrieval, embeddings & vector databases", or asks to get started with CLIP.

## What it does

1. **Point at it** — clone / install CLIP from https://github.com/openai/CLIP (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for multimodal.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/openai/CLIP for the authoritative quickstart
git clone https://github.com/openai/CLIP
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
