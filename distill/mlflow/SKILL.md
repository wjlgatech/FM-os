---
name: mlflow-quickstart
description: >-
  Get productive with MLflow (distributed): Experiment tracking, model registry, and artifact logging for reproducible large-scale training and eval runs. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# mlflow-quickstart

A cross-runtime skill for **[MLflow](https://github.com/mlflow/mlflow)** — the distributed tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Experiment tracking, model registry, and artifact logging for reproducible large-scale training and eval runs.

## When to use (trigger)

Invoke when the user mentions "MLflow", "Training / fine-tuning foundation models", "Agentic evaluation / benchmarking", "Distributed training & ML orchestration", "Research judgment & empirical rigor (experiment loop)", or asks to get started with MLflow.

## What it does

1. **Point at it** — clone / install MLflow from https://github.com/mlflow/mlflow (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for distributed.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/mlflow/mlflow for the authoritative quickstart
git clone https://github.com/mlflow/mlflow
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
