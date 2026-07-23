"""P3 — agentic search: offline-deterministic tests of the plan→retrieve→validate loop."""

from nomadic_mini.agentic_search import agentic_search, heuristic_plan
from nomadic_mini.search import EventIndex, local_embed

EVENTS = [
    {"label": "Left lane change", "category": "Lane Change Detection",
     "aiAnalysis": "Red Prius merged into ego lane from the left.",
     "video_id": "v1", "analysis_id": "a1", "event_index": 0},
    {"label": "Rolling stop", "category": "Driving Violations",
     "aiAnalysis": "Ego performed a rolling stop at a marked STOP intersection.",
     "video_id": "v1", "analysis_id": "a1", "event_index": 1},
    {"label": "Pothole cluster", "category": "Edge Case",
     "aiAnalysis": "Pothole cluster in the oncoming lane near the centerline.",
     "video_id": "v2", "analysis_id": "a2", "event_index": 0},
]


def _index():
    idx = EventIndex(embed_fn=local_embed)
    idx.add(EVENTS)
    return idx


def test_plan_splits_compound_query():
    plan = heuristic_plan("lane merges or stopped vehicles")
    assert len(plan["subqueries"]) >= 2
    assert plan["criteria"]


def test_agentic_search_emits_real_thoughts():
    res = agentic_search(_index(), "vehicle merging into my lane", top_k=3, use_llm=False)
    # thoughts must reflect the three real steps, not a canned one-liner
    assert len(res.thoughts) >= 3
    assert any("Planned" in t for t in res.thoughts)
    assert any("Retrieved" in t for t in res.thoughts)
    assert any("Validated" in t for t in res.thoughts)


def test_matches_ranked_with_reasons():
    res = agentic_search(_index(), "vehicle merging into my lane", top_k=3, use_llm=False)
    assert res.matches, "expected at least one validated match"
    assert res.matches[0].event_index == 0  # the lane-change event ranks first
    assert all(m.reason for m in res.matches)  # every match carries a reason
    sims = [m.similarity for m in res.matches]
    assert sims == sorted(sims, reverse=True)  # ranked by similarity


def test_custom_validate_fn_can_drop_all():
    res = agentic_search(_index(), "anything", top_k=5,
                         validate_fn=lambda q, e, s: (False, "rejected by test"))
    assert res.matches == []
    assert any("dropped" in t for t in res.thoughts)
