"""Schema-contract tests — always run, no network. These pin our models to the
verbatim NomadicML field vocabulary recovered from SDK source + docs."""

import pytest
from pydantic import ValidationError

from nomadic_mini.events import (
    CATEGORIES, AnalysisDocument, MotionEvent, SearchResult, seconds_to_mmss,
)

GOOD = dict(
    label="Left lane change",
    t_start="00:02", t_end="00:04",
    category="Lane Change Detection",
    severity="medium",
    aiAnalysis="Red Prius merged into ego lane from the left.",
    confidence=0.91,
)


def test_event_verbatim_sdk_fields():
    e = MotionEvent(**GOOD)
    dumped = e.model_dump()
    # exact SDK RapidReviewEvent vocabulary (nomadicml 0.1.53 video.py)
    for field in ("label", "t_start", "t_end", "category", "severity",
                  "aiAnalysis", "confidence", "approval", "overlay"):
        assert field in dumped
    assert dumped["approval"] == "pending"


def test_event_docs_variant_aliases():
    e = MotionEvent(**GOOD)
    # docs/REST surface names (type, description) map onto SDK names
    assert e.type == e.category
    assert e.description == e.aiAnalysis


def test_mmss_enforced():
    with pytest.raises(ValidationError):
        MotionEvent(**{**GOOD, "t_start": "2.0"})
    with pytest.raises(ValidationError):
        MotionEvent(**{**GOOD, "t_end": "00:71"})


def test_severity_and_confidence_bounds():
    with pytest.raises(ValidationError):
        MotionEvent(**{**GOOD, "severity": "critical"})
    with pytest.raises(ValidationError):
        MotionEvent(**{**GOOD, "confidence": 1.4})


def test_t_start_seconds():
    assert MotionEvent(**GOOD).t_start_seconds() == 2
    assert seconds_to_mmss(125) == "02:05"


def test_analysis_document_shape():
    doc = AnalysisDocument(video_id="v1", analysis_id="a1", analysis="ok",
                           events=[MotionEvent(**GOOD)])
    d = doc.model_dump()
    for field in ("video_id", "analysis_id", "analysis", "metadata", "events"):
        assert field in d


def test_search_result_shape():
    r = SearchResult(summary="s")
    d = r.model_dump()
    for field in ("summary", "thoughts", "matches"):
        assert field in d


def test_category_vocabulary_is_verbatim():
    assert "Lane Change Detection" in CATEGORIES
    assert "Vehicle Turns" in CATEGORIES
    assert "Relative Motion Analysis" in CATEGORIES
    assert "Driving Violations" in CATEGORIES
