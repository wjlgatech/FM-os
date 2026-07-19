---
name: transformers-quickstart
description: >-
  Get productive with Hugging Face Transformers (frameworks): De facto model hub and API with first-class VLM/video-LLM support, the integration surface most training and serving stacks build on. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# transformers-quickstart

A cross-runtime skill for **[Hugging Face Transformers](https://github.com/huggingface/transformers)** — the frameworks tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): De facto model hub and API with first-class VLM/video-LLM support, the integration surface most training and serving stacks build on.

## When to use (trigger)

Invoke when the user mentions "Hugging Face Transformers", "Python / PyTorch / large-scale ML workflows", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Training / fine-tuning foundation models", or asks to get started with Hugging Face Transformers.

## What it does

1. **Point at it** — clone / install Hugging Face Transformers from https://github.com/huggingface/transformers (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for frameworks.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/huggingface/transformers for the authoritative quickstart
git clone https://github.com/huggingface/transformers
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
