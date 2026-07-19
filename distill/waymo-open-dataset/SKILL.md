---
name: waymo-open-dataset-quickstart
description: >-
  Get productive with Waymo Open Dataset (dataset): Large-scale AD perception/motion/end-to-end datasets with eval code, a primary source of camera+lidar video for driving models. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# waymo-open-dataset-quickstart

A cross-runtime skill for **[Waymo Open Dataset](https://github.com/waymo-research/waymo-open-dataset)** — the dataset tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Large-scale AD perception/motion/end-to-end datasets with eval code, a primary source of camera+lidar video for driving models.

## When to use (trigger)

Invoke when the user mentions "Waymo Open Dataset", "Video / motion understanding, spatiotemporal", "Agentic evaluation / benchmarking", "Building datasets & benchmarks", "Dataset curation loops ("AI training AI")", or asks to get started with Waymo Open Dataset.

## What it does

1. **Point at it** — clone / install Waymo Open Dataset from https://github.com/waymo-research/waymo-open-dataset (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for dataset.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/waymo-research/waymo-open-dataset for the authoritative quickstart
git clone https://github.com/waymo-research/waymo-open-dataset
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
