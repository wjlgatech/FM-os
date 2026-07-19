---
name: bdd100k-models-quickstart
description: >-
  Get productive with BDD100K (dataset): Model zoo and tooling for the diverse BDD100K driving-video dataset, useful for detection/segmentation/tracking baselines and labels. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# bdd100k-models-quickstart

A cross-runtime skill for **[BDD100K](https://github.com/SysCV/bdd100k-models)** — the dataset tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Model zoo and tooling for the diverse BDD100K driving-video dataset, useful for detection/segmentation/tracking baselines and labels.

## When to use (trigger)

Invoke when the user mentions "BDD100K", "Video / motion understanding, spatiotemporal", "Building datasets & benchmarks", "Dataset curation loops ("AI training AI")", "Autonomous-driving / robotics datasets", or asks to get started with BDD100K.

## What it does

1. **Point at it** — clone / install BDD100K from https://github.com/SysCV/bdd100k-models (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for dataset.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/SysCV/bdd100k-models for the authoritative quickstart
git clone https://github.com/SysCV/bdd100k-models
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
