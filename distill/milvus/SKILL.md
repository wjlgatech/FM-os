---
name: milvus-quickstart
description: >-
  Get productive with Milvus (retrieval): Distributed vector database for large multimodal embedding corpora, used when single-node indices no longer fit. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# milvus-quickstart

A cross-runtime skill for **[Milvus](https://github.com/milvus-io/milvus)** — the retrieval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Distributed vector database for large multimodal embedding corpora, used when single-node indices no longer fit.

## When to use (trigger)

Invoke when the user mentions "Milvus", "Vision-Language / multi-modal models", "Retrieval, embeddings & vector databases", "Distributed training & ML orchestration", or asks to get started with Milvus.

## What it does

1. **Point at it** — clone / install Milvus from https://github.com/milvus-io/milvus (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for retrieval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/milvus-io/milvus for the authoritative quickstart
git clone https://github.com/milvus-io/milvus
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
