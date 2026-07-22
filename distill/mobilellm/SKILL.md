---
name: mobilellm-quickstart
description: >-
  Get productive with MobileLLM (models): Meta research on sub-billion-parameter, deep-thin architectures optimized for on-device use (ICML 2024). A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# mobilellm-quickstart

A cross-runtime skill for **[MobileLLM](https://github.com/facebookresearch/MobileLLM)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Meta research on sub-billion-parameter, deep-thin architectures optimized for on-device use (ICML 2024).

## When to use (trigger)

Invoke when the user mentions "MobileLLM", "Publishing research (NeurIPS / CVPR)", or asks to get started with MobileLLM.

## What it does

1. **Point at it** — clone / install MobileLLM from https://github.com/facebookresearch/MobileLLM (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/facebookresearch/MobileLLM for the authoritative quickstart
git clone https://github.com/facebookresearch/MobileLLM
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
