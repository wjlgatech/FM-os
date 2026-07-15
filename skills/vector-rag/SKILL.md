---
name: vector-rag
description: >-
  Build retrieval-augmented generation over VIDEO: embed clips/frames with a
  CLIP/SigLIP-style encoder, index them in a vector database (FAISS / Milvus /
  Qdrant / LanceDB), retrieve the relevant moments for a query, and ground a
  Vision-Language Model's answer in what it actually retrieved.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# vector-rag

A cross-runtime skill for **retrieval over video embeddings + grounded generation** — the
"understanding of retrieval systems, embeddings, and vector databases" a multi-modal ML role
needs. Grounded in vetted open tooling from [FM-os](https://github.com/wjlgatech/FM-os).

## When to use (trigger)

Invoke when the user says "video RAG", "retrieval over embeddings", "search my video corpus",
"build a vector index", "find the clip where…", "embed and retrieve frames", or "ground a VLM
answer in retrieved moments".

## What it does

1. **Embed** — encode frames/clips with a CLIP / SigLIP / open_clip encoder (and optionally text
   captions) into a shared embedding space.
2. **Index** — store vectors in a vector database: FAISS for a single node, Milvus / Qdrant /
   LanceDB when the corpus outgrows memory or needs payload filtering (timestamp, camera, scene).
3. **Retrieve** — approximate-nearest-neighbor search for a text or image query returns the top-k
   moments, with metadata filters (e.g. only night driving, only lane-change clips).
4. **Ground** — feed the retrieved clips to a VLM (see `vlm-quickstart`) so its answer cites the
   moments it actually saw — no ungrounded hallucination.
5. **Evaluate** — measure retrieval quality (Recall@k, mAP) and answer groundedness; gate on it.

## Example

```bash
pip install open_clip_torch faiss-cpu qdrant-client
# 1) embed frames -> vectors, 2) index, 3) query
python embed_frames.py --video ./clips/ --encoder ViT-B-32 --out emb.npy
python -c "import faiss,numpy as np; x=np.load('emb.npy'); idx=faiss.IndexFlatIP(x.shape[1]); idx.add(x); faiss.write_index(idx,'clips.faiss')"
python retrieve.py --index clips.faiss --query 'a car changing lanes at night' --k 5
# -> hand the 5 retrieved clips to vlm-quickstart for a grounded description
```

## Verification (eval-with-teeth)

Ships a tiny fixture so `pytest` can assert Recall@k on a known query, and gates real runs on a
minimum Recall@k so a regression in the embedding/index pipeline fails rather than silently
degrading retrieval.

## Safety

Operates on the user's own corpus; HTTPS downloads only for encoder weights; no secrets; no shell
beyond the documented commands.

## Cross-runtime

One `SKILL.md`; thin manifests wrap it for Claude Code, Codex, and Hermes.
