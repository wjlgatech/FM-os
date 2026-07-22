---
name: nanotron-quickstart
description: >-
  Get productive with Nanotron (frameworks): Minimalistic 3D-parallelism pretraining library from Hugging Face, basis of the Ultrascale Playbook. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# nanotron-quickstart

A cross-runtime skill for **[Nanotron](https://github.com/huggingface/nanotron)** — the frameworks tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Minimalistic 3D-parallelism pretraining library from Hugging Face, basis of the Ultrascale Playbook.

## When to use (trigger)

Invoke when the user mentions "Nanotron", "Python / PyTorch / large-scale ML workflows", "Training / fine-tuning foundation models", "Distributed training & ML orchestration", or asks to get started with Nanotron.

## What it does

1. **Point at it** — clone / install Nanotron from https://github.com/huggingface/nanotron (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for frameworks.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/huggingface/nanotron for the authoritative quickstart
git clone https://github.com/huggingface/nanotron
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
