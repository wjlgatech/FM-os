"""Offline tests for the interview solution — no API key, no network.

The Gemini call is a seam (`infer_fn`), so Part 1 and Part 2 orchestration are exercised
end-to-end with fakes that speak the notebook's gemini_inference signature."""

from __future__ import annotations

import json

import pytest

from lane_change_solution import (
    GROUND_TRUTH,
    detect_chunked,
    interval_iou,
    make_windows,
    merge_events,
    mmss_to_seconds,
    remap_to_global,
    report,
    score_predictions,
    seconds_to_mmss,
    to_output_json,
    validate_all,
    validate_event,
)


# ---------------------------------------------------------------- time helpers

def test_mmss_roundtrip():
    assert mmss_to_seconds("01:24") == 84
    assert seconds_to_mmss(84) == "01:24"
    assert seconds_to_mmss(0) == "00:00"
    assert mmss_to_seconds(seconds_to_mmss(101)) == 101


def test_mmss_tolerates_decimal_seconds():
    assert mmss_to_seconds("00:08.5") == 8.5  # observed live from claude-sonnet-5


# ---------------------------------------------------------------- windows

def test_windows_cover_duration_with_overlap():
    windows = make_windows(105, chunk=20, overlap=5)
    assert windows[0] == (0.0, 20.0)
    assert windows[-1][1] == 105
    for (s1, e1), (s2, e2) in zip(windows, windows[1:]):
        assert s2 < e1, "consecutive windows must overlap"
        assert e1 - s2 == pytest.approx(5.0)


def test_windows_short_video_single_window():
    assert make_windows(12, chunk=20, overlap=5) == [(0.0, 12.0)]


def test_windows_rejects_bad_overlap():
    with pytest.raises(ValueError):
        make_windows(60, chunk=5, overlap=5)


# ---------------------------------------------------------------- remap

def test_remap_window_relative():
    assert remap_to_global(0, 5, 40, 60) == (40, 45)


def test_remap_falls_back_to_global_when_model_answered_absolute():
    assert remap_to_global(45, 50, 40, 60) == (45, 50)


def test_remap_clamps_nonsense_to_window():
    s, e = remap_to_global(15, 25, 40, 60)
    assert s == 55 and e == 60


# ---------------------------------------------------------------- merge

def _ev(s, e, d, desc="x"):
    return {"t_start_s": s, "t_end_s": e, "direction": d, "description": desc}


def test_merge_dedupes_overlapping_windows_same_event():
    merged = merge_events([_ev(48, 50, "right", "a"), _ev(48, 52, "right", "b")])
    assert len(merged) == 1
    assert (merged[0]["t_start_s"], merged[0]["t_end_s"]) == (48, 52)


def test_merge_folds_double_lane_change_within_gap():
    merged = merge_events([_ev(84, 87, "right"), _ev(88, 91, "right")], max_gap=2.0)
    assert len(merged) == 1
    assert (merged[0]["t_start_s"], merged[0]["t_end_s"]) == (84, 91)


def test_merge_keeps_opposite_directions_apart():
    merged = merge_events([_ev(48, 52, "right"), _ev(50, 54, "left")])
    assert len(merged) == 2


def test_merge_respects_gap():
    merged = merge_events([_ev(10, 12, "left"), _ev(20, 22, "left")], max_gap=2.0)
    assert len(merged) == 2


# ---------------------------------------------------------------- scoring

def test_iou():
    assert interval_iou((0, 10), (0, 10)) == 1.0
    assert interval_iou((0, 10), (5, 15)) == pytest.approx(1 / 3)
    assert interval_iou((0, 10), (20, 30)) == 0.0


def test_score_perfect_predictions():
    preds = [_ev(s, e, d) for s, e, d, _ in GROUND_TRUTH]
    s = score_predictions(preds)
    assert (s["precision"], s["recall"], s["f1"]) == (1.0, 1.0, 1.0)
    assert all(m["direction_ok"] for m in s["matches"])


def test_score_false_positive_lowers_precision():
    preds = [_ev(s, e, d) for s, e, d, _ in GROUND_TRUTH] + [_ev(10, 14, "left", "curvature FP")]
    s = score_predictions(preds)
    assert s["fp"] == 1 and s["recall"] == 1.0 and s["precision"] == 0.8


def test_score_missed_event_lowers_recall():
    preds = [_ev(48, 52, "right")]
    s = score_predictions(preds)
    assert s["fn"] == 3 and s["precision"] == 1.0 and s["recall"] == 0.25


def test_report_and_output_json_shapes():
    preds = [_ev(48, 52, "right", "right lane change")]
    assert "precision" in report(preds)
    out = to_output_json(preds)
    assert out["lane_changes"][0] == {"t_start": "00:48", "t_end": "00:52",
                                      "direction": "right", "description": "right lane change"}


# ---------------------------------------------------------------- Part 1 e2e with fake VLM

def make_fake_detector(true_events):
    """Fake gemini_inference: reports the clip-relative intersection of each true event
    with the requested window — exactly what a well-behaved VLM would return."""

    def fake(query, video=None, enable_thinking=True, time_interval=None, fps=None, schema=None):
        win_s, win_e = time_interval
        found = []
        for s, e, d in true_events:
            lo, hi = max(s, win_s), min(e, win_e)
            if hi - lo >= 1:
                found.append({"t_start": seconds_to_mmss(lo - win_s), "t_end": seconds_to_mmss(hi - win_s),
                              "direction": d, "description": f"{d} lane change"})
        return json.dumps({"lane_changes": found})

    return fake


def test_detect_chunked_recovers_all_ground_truth_globally():
    fake = make_fake_detector([(s, e, d) for s, e, d, _ in GROUND_TRUTH])
    merged = detect_chunked(fake, video_file=None, duration=105, chunk=20, overlap=5)
    s = score_predictions(merged)
    assert s["recall"] == 1.0, report(merged)
    assert s["precision"] == 1.0, report(merged)


def test_detect_chunked_samples_rescue_flaky_detection():
    """A borderline event reported only on the 2nd sample of a window is still recovered."""
    calls = {"n": 0}

    def flaky(query, video=None, enable_thinking=True, time_interval=None, fps=None, schema=None):
        calls["n"] += 1
        win_s, win_e = time_interval
        if calls["n"] % 3 == 2 and win_s <= 48 and 52 <= win_e:  # only 2nd sample sees it
            return json.dumps({"lane_changes": [
                {"t_start": seconds_to_mmss(48 - win_s), "t_end": seconds_to_mmss(52 - win_s),
                 "direction": "right", "description": "right lane change"}]})
        return json.dumps({"lane_changes": []})

    assert detect_chunked(flaky, None, 105, samples=1) == []
    calls["n"] = 0
    merged = detect_chunked(flaky, None, 105, samples=3)
    assert len(merged) == 1 and merged[0]["direction"] == "right"


def test_detect_chunked_dedupes_event_seen_by_two_windows():
    fake = make_fake_detector([(48, 52, "right")])
    merged = detect_chunked(fake, video_file=None, duration=105, chunk=20, overlap=5)
    assert len(merged) == 1
    assert merged[0]["t_start_s"] == pytest.approx(48, abs=1)
    assert merged[0]["t_end_s"] == pytest.approx(52, abs=1)


# ---------------------------------------------------------------- Part 2 e2e with fake judge

def make_fake_judge(answers):
    """Fake gemini_inference for the judge: pops one scripted verdict per call."""
    queue = list(answers)

    def fake(query, video=None, enable_thinking=True, time_interval=None, fps=None, schema=None):
        ok, direction = queue.pop(0)
        return json.dumps({"is_lane_change": ok, "direction": direction,
                           "reason": "scripted verdict"})

    return fake


def test_validate_event_majority_yes():
    judge = make_fake_judge([(True, "right"), (True, "right"), (False, "none")])
    v = validate_event(judge, None, _ev(48, 52, "right"), duration=105, votes=3)
    assert v["valid"] and v["votes_yes"] == 2 and v["judge_direction"] == "right"


def test_validate_event_majority_no():
    judge = make_fake_judge([(False, "none"), (False, "none"), (True, "left")])
    v = validate_event(judge, None, _ev(10, 14, "left"), duration=105, votes=3)
    assert not v["valid"]


def test_validate_all_filters_fp_and_fixes_direction():
    # candidate 1: real but detector said "left" while judge sees "right" -> direction corrected
    # candidate 2: curvature FP -> dropped
    judge = make_fake_judge([
        (True, "right"), (True, "right"), (True, "right"),
        (False, "none"), (False, "none"), (False, "none"),
    ])
    events = [_ev(48, 52, "left", "real one"), _ev(10, 14, "left", "curvature FP")]
    kept = validate_all(judge, None, events, duration=105, votes=3)
    assert len(kept) == 1
    assert kept[0]["direction"] == "right"
    assert kept[0]["validation"]["valid"]


def test_validate_snippet_padding_clamped_to_video():
    seen = []

    def judge(query, video=None, enable_thinking=True, time_interval=None, fps=None, schema=None):
        seen.append((time_interval, fps))
        return json.dumps({"is_lane_change": True, "direction": "left", "reason": "ok"})

    validate_event(judge, None, _ev(1, 4, "left"), duration=105, pad=3.0, votes=1, fps=5)
    (interval, fps) = seen[0]
    assert interval == (0, 7) and fps == 5
