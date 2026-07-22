---
name: lancedb-quickstart
description: >-
  Get productive with LanceDB (retrieval): Embedded columnar vector store on the Lance format, well suited to versioned multimodal datasets and fast on-disk embedding queries. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# lancedb-quickstart

A cross-runtime skill for **[LanceDB](https://github.com/lancedb/lancedb)** — the retrieval tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): Embedded columnar vector store on the Lance format, well suited to versioned multimodal datasets and fast on-disk embedding queries.

## When to use (trigger)

Invoke when the user mentions "LanceDB", "Vision-Language / multi-modal models", "Retrieval, embeddings & vector databases", or asks to get started with LanceDB.

## What it does

1. **Point at it** — clone / install LanceDB from https://github.com/lancedb/lancedb (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for retrieval.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see https://github.com/lancedb/lancedb for the authoritative quickstart
git clone https://github.com/lancedb/lancedb
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
