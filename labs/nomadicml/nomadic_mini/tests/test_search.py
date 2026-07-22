"""Offline semantic-search tests using the deterministic local embedder."""

from nomadic_mini.search import EventIndex, local_embed

EVENTS = [
    {"label": "Left lane change", "category": "Lane Change Detection",
     "aiAnalysis": "Red Prius merged into ego lane from the left.",
     "video_id": "v1", "analysis_id": "a1", "event_index": 0},
    {"label": "Rolling stop", "category": "Driving Violations",
     "aiAnalysis": "Ego vehicle performed a rolling stop at a marked STOP intersection.",
     "video_id": "v1", "analysis_id": "a1", "event_index": 1},
    {"label": "Pothole cluster", "category": "Edge Case",
     "aiAnalysis": "Pothole cluster in the oncoming lane near the centerline.",
     "video_id": "v2", "analysis_id": "a2", "event_index": 0},
]


def _index():
    idx = EventIndex(embed_fn=local_embed)
    idx.add(EVENTS)
    return idx


def test_query_ranks_relevant_event_first():
    hits = _index().query("vehicle merging into my lane", top_k=3)
    assert hits[0][1]["label"] == "Left lane change"


def test_query_violations():
    hits = _index().query("stop sign violation rolling stop", top_k=1)
    assert hits[0][1]["category"] == "Driving Violations"


def test_empty_index():
    assert EventIndex(embed_fn=local_embed).query("anything") == []


def test_add_empty_is_noop():
    calls = []

    def spy(texts):
        calls.append(texts)
        return local_embed(texts)

    idx = EventIndex(embed_fn=spy)
    idx.add([])  # a zero-event analysis must not hit the embedder at all
    assert calls == []
