---
name: olmo-quickstart
description: >-
  Get productive with OLMo (models): AI2's fully open model+data+training stack including small 1B variants for reproducible SLM research. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# olmo-quickstart

A cross-runtime skill for **[OLMo](https://github.com/allenai/OLMo)** — the models tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): AI2's fully open model+data+training stack including small 1B variants for reproducible SLM research.

## When to use (trigger)

Invoke when the user mentions "OLMo", "Training / fine-tuning foundation models", "Research judgment & empirical rigor (experiment loop)", "Publishing research (NeurIPS / CVPR)", or asks to get started with OLMo.

## What it does

1. **Point at it** — clone / install OLMo from https://github.com/allenai/OLMo (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for models.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/allenai/OLMo for the authoritative quickstart
git clone https://github.com/allenai/OLMo
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
