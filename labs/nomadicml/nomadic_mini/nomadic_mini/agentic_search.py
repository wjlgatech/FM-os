"""P3 — agentic search with real `thoughts[]` traces.

NomadicML's production search returns a chain-of-thought (`thoughts[]`) and per-match
`reason` — a plan → retrieve → validate funnel, not one-shot similarity. This mirrors that:

  1. PLAN     — expand the query into sub-intents + an acceptance criterion (a real step)
  2. RETRIEVE — embed each sub-intent, union the candidate events (dedup, keep best score)
  3. VALIDATE — judge each candidate against the original intent; keep/drop with a reason

Each step appends a real line to `thoughts`. LLM-backed (Claude) when ANTHROPIC_API_KEY is set;
otherwise a deterministic heuristic fallback so `make check` runs offline. Closes the last
schema-fidelity gap vs their `{summary, thoughts, matches}` contract.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Callable

from .events import SearchMatch, SearchResult
from .search import EventIndex

PlanFn = Callable[[str], dict]              # query -> {"subqueries": [...], "criteria": str}
ValidateFn = Callable[[str, dict, float], tuple[bool, str]]  # (query, event, score) -> (keep, reason)

_CONNECTORS = re.compile(r"\bor\b|\band\b|,|;|/", re.IGNORECASE)
_KEEP_THRESHOLD = 0.12  # offline cosine floor for the heuristic validator


# ---------- heuristic (offline, deterministic) ----------

def heuristic_plan(query: str) -> dict:
    parts = [p.strip() for p in _CONNECTORS.split(query) if len(p.strip()) > 2]
    return {"subqueries": parts or [query.strip()],
            "criteria": f"event is genuinely about: {query.strip()}"}


def heuristic_validate(query: str, event: dict, score: float) -> tuple[bool, str]:
    keep = score >= _KEEP_THRESHOLD
    verb = "matches" if keep else "too weak for"
    return keep, f"cosine {score:.2f} {verb} “{query}”"


# ---------- LLM-backed (real reasoning when a key is present) ----------

def _anthropic():
    import anthropic
    return anthropic.Anthropic()


def llm_plan(query: str) -> dict:
    client = _anthropic()
    r = client.messages.create(
        model=os.environ.get("COPILOT_MODEL", "claude-sonnet-5"), max_tokens=400,
        messages=[{"role": "user", "content": (
            "Break this driving-video search query into 2-4 concrete sub-intents to retrieve on, "
            "and one acceptance criterion. Return ONLY JSON "
            '{"subqueries":[...],"criteria":"..."}.\n\nQuery: ' + query)}],
    )
    txt = "".join(b.text for b in r.content if b.type == "text")
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    return json.loads(m.group(0)) if m else heuristic_plan(query)


def llm_validate_batch(query: str, criteria: str, candidates: list[dict]) -> list[tuple[bool, str]]:
    """One batched judgement call — returns (keep, reason) per candidate, in order."""
    client = _anthropic()
    listing = "\n".join(
        f"{i}. [{e.get('category')}] {e.get('label')} — {e.get('aiAnalysis','')}"
        for i, e in enumerate(candidates))
    r = client.messages.create(
        model=os.environ.get("COPILOT_MODEL", "claude-sonnet-5"), max_tokens=900,
        messages=[{"role": "user", "content": (
            f"Query: {query}\nAcceptance criterion: {criteria}\n\nEvents:\n{listing}\n\n"
            "For EACH event decide if it satisfies the query. Return ONLY a JSON list "
            '[{"i":0,"keep":true,"reason":"<=10 words"}, ...] covering every index.')}],
    )
    txt = "".join(b.text for b in r.content if b.type == "text")
    m = re.search(r"\[.*\]", txt, re.DOTALL)
    verdicts = json.loads(m.group(0)) if m else []
    by_i = {v["i"]: (bool(v.get("keep")), str(v.get("reason", ""))) for v in verdicts}
    return [by_i.get(i, (True, "kept (no verdict)")) for i in range(len(candidates))]


# ---------- the loop ----------

def agentic_search(index: EventIndex, query: str, *, top_k: int = 5,
                   plan_fn: PlanFn | None = None,
                   validate_fn: ValidateFn | None = None,
                   use_llm: bool | None = None) -> SearchResult:
    if use_llm is None:
        use_llm = bool(os.environ.get("ANTHROPIC_API_KEY")) and plan_fn is None and validate_fn is None
    thoughts: list[str] = []

    # 1. PLAN
    plan = (plan_fn or (llm_plan if use_llm else heuristic_plan))(query)
    subs = plan.get("subqueries") or [query]
    criteria = plan.get("criteria", f"about: {query}")
    thoughts.append(f"Planned {len(subs)} sub-quer{'y' if len(subs)==1 else 'ies'}: " + "; ".join(subs))

    # 2. RETRIEVE (union, keep best score per event)
    pool: dict[tuple, tuple[float, dict]] = {}
    for sq in subs:
        for score, e in index.query(sq, top_k=max(top_k * 2, 8)):
            key = (e.get("video_id"), e.get("analysis_id"), e.get("event_index"))
            if key not in pool or score > pool[key][0]:
                pool[key] = (score, e)
    ranked = sorted(pool.values(), key=lambda p: -p[0])
    thoughts.append(f"Retrieved {len(ranked)} unique candidate events across sub-queries.")
    if not ranked:
        thoughts.append("No candidates cleared retrieval.")
        return SearchResult(summary=f"0 events matched {query!r}", thoughts=thoughts, matches=[])

    # 3. VALIDATE
    cand_events = [e for _, e in ranked]
    if validate_fn is not None:
        verdicts = [validate_fn(query, e, s) for s, e in ranked]
    elif use_llm:
        verdicts = llm_validate_batch(query, criteria, cand_events)
    else:
        verdicts = [heuristic_validate(query, e, s) for s, e in ranked]

    kept = [(s, e, r) for (s, e), (keep, r) in zip(ranked, verdicts) if keep]
    thoughts.append(f"Validated against criterion — kept {len(kept)}, dropped {len(ranked) - len(kept)}.")

    matches = [
        SearchMatch(video_id=e.get("video_id", ""), analysis_id=e.get("analysis_id", ""),
                    event_index=e.get("event_index", -1), similarity=round(s, 4), reason=r)
        for s, e, r in kept[:top_k]
    ]
    return SearchResult(
        summary=f"{len(matches)} event(s) satisfied {query!r} (plan→retrieve→validate)",
        thoughts=thoughts, matches=matches)
