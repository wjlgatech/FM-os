"""Semantic search over detected events — the retrieval half of the pipeline.

Two embedding backends behind one seam:
- gemini_embed: real dense embeddings (needs GEMINI_API_KEY)
- local_embed:  deterministic bag-of-words vectors, so unit tests run offline
"""

from __future__ import annotations

import math
import os
import re
from collections.abc import Callable, Sequence

EmbedFn = Callable[[Sequence[str]], list[list[float]]]

_TOKEN = re.compile(r"[a-z0-9]+")


def local_embed(texts: Sequence[str]) -> list[list[float]]:
    """Hashed bag-of-words embedding — offline, deterministic, test-grade only."""
    dim = 512
    out = []
    for t in texts:
        v = [0.0] * dim
        for tok in _TOKEN.findall(t.lower()):
            v[hash(tok) % dim] += 1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        out.append([x / norm for x in v])
    return out


def gemini_embed(texts: Sequence[str]) -> list[list[float]]:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    res = client.models.embed_content(model="gemini-embedding-001", contents=list(texts))
    return [e.values for e in res.embeddings]


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a)) or 1.0
    db = math.sqrt(sum(x * x for x in b)) or 1.0
    return num / (da * db)


class EventIndex:
    """Index event descriptions; query in natural language, get ranked events back."""

    def __init__(self, embed_fn: EmbedFn | None = None):
        self.embed_fn = embed_fn or (
            gemini_embed if os.environ.get("GEMINI_API_KEY") else local_embed
        )
        self._events: list[dict] = []
        self._vecs: list[list[float]] = []

    def add(self, events: Sequence[dict]) -> None:
        if not events:
            return
        texts = [self._event_text(e) for e in events]
        self._events.extend(events)
        self._vecs.extend(self.embed_fn(texts))

    def query(self, text: str, top_k: int = 5) -> list[tuple[float, dict]]:
        if not self._events:
            return []
        qv = self.embed_fn([text])[0]
        scored = sorted(
            ((_cosine(qv, v), e) for v, e in zip(self._vecs, self._events)),
            key=lambda p: -p[0],
        )
        return scored[:top_k]

    @staticmethod
    def _event_text(e: dict) -> str:
        parts = [str(e.get(k, "")) for k in ("category", "label", "aiAnalysis", "type", "description")]
        return " ".join(p for p in parts if p)
