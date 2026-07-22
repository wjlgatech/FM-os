---
name: phicookbook-quickstart
description: >-
  Get productive with Phi Cookbook (models): Microsoft's official hub for the Phi SLM family with inference, fine-tuning, quantization, and edge-deployment recipes. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# phicookbook-quickstart

A cross-runtime skill for **[Phi Cookbook](https://github.com/microsoft/PhiCookBook)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Microsoft's official hub for the Phi SLM family with inference, fine-tuning, quantization, and edge-deployment recipes.

## When to use (trigger)

Invoke when the user mentions "Phi Cookbook", "Training / fine-tuning foundation models", "GPU optimization / efficient inference", or asks to get started with Phi Cookbook.

## What it does

1. **Point at it** — clone / install Phi Cookbook from https://github.com/microsoft/PhiCookBook (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/microsoft/PhiCookBook for the authoritative quickstart
git clone https://github.com/microsoft/PhiCookBook
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
