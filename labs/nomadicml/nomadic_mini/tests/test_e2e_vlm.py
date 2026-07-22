"""End-to-end VLM tests on the bundled real driving clips.
Marked `vlm`: they call Gemini/Claude and are run via `make e2e`."""

import os
from pathlib import Path

import pytest

from nomadic_mini.client import MiniClient
from nomadic_mini.events import CATEGORIES
from nomadic_mini.frames import video_duration

DATA = Path(__file__).resolve().parents[2] / "data"
CLIP = DATA / "drive_city_34s.mp4"

pytestmark = pytest.mark.vlm

needs_vlm = pytest.mark.skipif(
    not (os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")),
    reason="no VLM backend key set",
)


@needs_vlm
def test_upload_analyze_search_roundtrip():
    client = MiniClient()
    vid = client.upload(CLIP)
    # verbatim query from NomadicML's public "Behavior Recognition" example
    doc = client.analyze(vid, "Find lane merge instances.", mode="fast")

    assert doc.video_id == vid
    assert doc.analysis  # non-empty summary
    duration = video_duration(CLIP)
    for e in doc.events:
        assert e.t_start_seconds() <= duration + 1
        assert e.category in CATEGORIES
        assert 0.0 <= e.confidence <= 1.0

    res = client.search("vehicle merging or changing lanes")
    assert res.summary
    if doc.events:
        assert res.matches, "events were detected but search returned nothing"
