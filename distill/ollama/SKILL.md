---
name: ollama-quickstart
description: >-
  Get productive with Ollama (serving): One-command local runner for small open models, the easiest path to running SLMs on a personal machine. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# ollama-quickstart

A cross-runtime skill for **[Ollama](https://github.com/ollama/ollama)** — the serving tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): One-command local runner for small open models, the easiest path to running SLMs on a personal machine.

## When to use (trigger)

Invoke when the user mentions "Ollama", "GPU optimization / efficient inference", or asks to get started with Ollama.

## What it does

1. **Point at it** — clone / install Ollama from https://github.com/ollama/ollama (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for serving.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/ollama/ollama for the authoritative quickstart
git clone https://github.com/ollama/ollama
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
