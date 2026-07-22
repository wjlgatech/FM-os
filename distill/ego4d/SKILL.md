---
name: ego4d-quickstart
description: >-
  Get productive with Ego4D (dataset): Massive egocentric video dataset with download, feature-extraction, and API tooling, relevant for first-person video understanding and robotics. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# ego4d-quickstart

A cross-runtime skill for **[Ego4D](https://github.com/facebookresearch/Ego4d)** — the dataset tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Massive egocentric video dataset with download, feature-extraction, and API tooling, relevant for first-person video understanding and robotics.

## When to use (trigger)

Invoke when the user mentions "Ego4D", "Video / motion understanding, spatiotemporal", "Building datasets & benchmarks", "Dataset curation loops ("AI training AI")", "Autonomous-driving / robotics datasets", or asks to get started with Ego4D.

## What it does

1. **Point at it** — clone / install Ego4D from https://github.com/facebookresearch/Ego4d (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for dataset.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/facebookresearch/Ego4d for the authoritative quickstart
git clone https://github.com/facebookresearch/Ego4d
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
