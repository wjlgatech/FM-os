---
name: av2-api-quickstart
description: >-
  Get productive with Argoverse 2 (dataset): Next-gen self-driving datasets (sensor, lidar, motion forecasting) with a maintained Python API and HD maps for multimodal AD research. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# av2-api-quickstart

A cross-runtime skill for **[Argoverse 2](https://github.com/argoverse/av2-api)** — the dataset tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Next-gen self-driving datasets (sensor, lidar, motion forecasting) with a maintained Python API and HD maps for multimodal AD research.

## When to use (trigger)

Invoke when the user mentions "Argoverse 2", "Python / PyTorch / large-scale ML workflows", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Building datasets & benchmarks", or asks to get started with Argoverse 2.

## What it does

1. **Point at it** — clone / install Argoverse 2 from https://github.com/argoverse/av2-api (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for dataset.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/argoverse/av2-api for the authoritative quickstart
git clone https://github.com/argoverse/av2-api
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
