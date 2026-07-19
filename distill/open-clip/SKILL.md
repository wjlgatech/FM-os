---
name: open-clip-quickstart
description: >-
  Get productive with open_clip (multimodal): Open training/eval for CLIP-style models at scale, the go-to for reproducible contrastive image-text encoders and domain pretraining. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# open-clip-quickstart

A cross-runtime skill for **[open_clip](https://github.com/mlfoundations/open_clip)** — the multimodal tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Open training/eval for CLIP-style models at scale, the go-to for reproducible contrastive image-text encoders and domain pretraining.

## When to use (trigger)

Invoke when the user mentions "open_clip", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Training / fine-tuning foundation models", "Agentic evaluation / benchmarking", or asks to get started with open_clip.

## What it does

1. **Point at it** — clone / install open_clip from https://github.com/mlfoundations/open_clip (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for multimodal.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/mlfoundations/open_clip for the authoritative quickstart
git clone https://github.com/mlfoundations/open_clip
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
