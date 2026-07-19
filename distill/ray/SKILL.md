---
name: ray-quickstart
description: >-
  Get productive with Ray (distributed): Distributed compute for data loading, training, and batch multimodal inference, the orchestration layer for scaling VLM pipelines across a cluster. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# ray-quickstart

A cross-runtime skill for **[Ray](https://github.com/ray-project/ray)** — the distributed tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Distributed compute for data loading, training, and batch multimodal inference, the orchestration layer for scaling VLM pipelines across a cluster.

## When to use (trigger)

Invoke when the user mentions "Ray", "Vision-Language / multi-modal models", "Training / fine-tuning foundation models", "GPU optimization / efficient inference", "Distributed training & ML orchestration", or asks to get started with Ray.

## What it does

1. **Point at it** — clone / install Ray from https://github.com/ray-project/ray (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for distributed.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/ray-project/ray for the authoritative quickstart
git clone https://github.com/ray-project/ray
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
