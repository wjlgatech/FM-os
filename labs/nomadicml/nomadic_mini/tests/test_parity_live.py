"""Term-by-term parity vs the REAL NomadicML production API.

Marked `live`: auto-run when NOMADICML_API_KEY is set, honest `skip` otherwise
(never a fake pass). Run via `make parity`.

This harness IS the JD's "agentic evaluation framework" bullet: it benchmarks
our clean-room clone against their production surface, field by field.
"""

import os
from pathlib import Path

import pytest

from nomadic_mini.client import MiniClient, NomadicLive

DATA = Path(__file__).resolve().parents[2] / "data"
CLIP = DATA / "drive_city_34s.mp4"
QUERY = "Find driving violations and cite their relevant DMV code."  # verbatim public example

pytestmark = pytest.mark.live

needs_key = pytest.mark.skipif(
    not os.environ.get("NOMADICML_API_KEY"),
    reason="NOMADICML_API_KEY not set — sign up at app.nomadicml.com (Profile > API Key)",
)

# SDK RapidReviewEvent contract (nomadicml 0.1.53); confidence/overlay are optional upstream
EVENT_CORE_FIELDS = {"label", "t_start", "t_end", "severity"}
DOC_FIELDS = {"video_id", "analysis_id", "analysis", "events"}


@pytest.fixture(scope="module")
def live():
    return NomadicLive()


@needs_key
def test_key_verifies(live):
    info = live.verify_key()
    assert info.get("valid") is True
    assert "user_id" in info or "uid" in info


@needs_key
def test_full_parity_roundtrip(live, tmp_path):
    # --- their side ---
    # Free-trial keys can't upload (402 "Video upload is not available on the
    # free trial", measured 2026-07-21). Fall back to any video already in the
    # account (e.g. added via the app.nomadicml.com web UI); skip honestly if
    # there is nothing to analyze.
    import httpx as _httpx
    try:
        their_vid = live.upload(CLIP)
        live.wait_uploaded(their_vid)
    except _httpx.HTTPStatusError as err:
        if err.response.status_code != 402:
            raise
        existing = live.my_videos()
        if not existing:
            pytest.skip(
                "free-trial key: API upload paywalled (402) and account has no "
                "videos — upload one clip via the app.nomadicml.com web UI "
                "(or upgrade the plan), then re-run `make parity`")
        their_vid = existing[0]["video_id"]
    start = live.analyze_start(their_vid, QUERY)
    assert "stream_id" in start
    progress = live.analyze_events(start["stream_id"])
    assert progress and progress[-1].get("event") in ("done", "error")
    assert progress[-1].get("event") == "done", f"their analysis errored: {progress[-1]}"

    analysis_id = (progress[-1].get("analysis_id")
                   or progress[-1].get("data", {}).get("analysis_id"))
    assert analysis_id, f"no analysis_id in terminal event: {progress[-1]}"
    theirs = live.get_analysis(their_vid, analysis_id)

    # --- our side, same clip, same verbatim query ---
    mini = MiniClient()
    ours = mini.analyze(mini.upload(CLIP), QUERY)

    # --- term-by-term: document envelope ---
    missing_doc = DOC_FIELDS - set(theirs.keys())
    assert not missing_doc, f"their document lacks documented fields: {missing_doc}"
    assert DOC_FIELDS <= set(ours.model_dump().keys())

    # --- term-by-term: event fields ---
    for ev in theirs.get("events", []):
        assert EVENT_CORE_FIELDS <= set(ev.keys()), (
            f"their event diverges from documented schema: {sorted(ev.keys())}")
    for ev in ours.events:
        assert EVENT_CORE_FIELDS <= set(ev.model_dump().keys())

    # --- semantic overlap report (informative, printed not asserted) ---
    print(f"\nTHEIRS: {len(theirs.get('events', []))} events; "
          f"OURS: {len(ours.events)} events on {CLIP.name} for query {QUERY!r}")
    for ev in theirs.get("events", []):
        print(f"  their: [{ev.get('t_start')}–{ev.get('t_end')}] {ev.get('label')}")
    for ev in ours.events:
        print(f"  ours : [{ev.t_start}–{ev.t_end}] {ev.label}")
