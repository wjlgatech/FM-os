---
name: nuscenes-devkit-quickstart
description: >-
  Get productive with nuScenes devkit (dataset): Official devkit for the multimodal nuScenes AD dataset (camera, lidar, radar), the standard toolkit for sensor+video data loading and eval. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# nuscenes-devkit-quickstart

A cross-runtime skill for **[nuScenes devkit](https://github.com/nutonomy/nuscenes-devkit)** — the dataset tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Official devkit for the multimodal nuScenes AD dataset (camera, lidar, radar), the standard toolkit for sensor+video data loading and eval.

## When to use (trigger)

Invoke when the user mentions "nuScenes devkit", "Vision-Language / multi-modal models", "Video / motion understanding, spatiotemporal", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", or asks to get started with nuScenes devkit.

## What it does

1. **Point at it** — clone / install nuScenes devkit from https://github.com/nutonomy/nuscenes-devkit (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for dataset.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/nutonomy/nuscenes-devkit for the authoritative quickstart
git clone https://github.com/nutonomy/nuscenes-devkit
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
