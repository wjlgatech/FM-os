"""Tests for the beyond-the-ask deliverables: quota math + zero-API motion validator.

Pure-logic tests only (no video decode, no network) — the video-level calibration
lives in eval_motion.py and banks its measured result in motion_eval.json."""

from __future__ import annotations

import numpy as np
import pytest

from lane_change_solution import estimate_calls, is_valid_lane_change
from motion_check import NET_SHIFT_THRESHOLD, motion_evidence, pattern_shift


# ---------------------------------------------------------------- quota math

def test_estimate_calls_reproduces_the_free_tier_failure():
    # The exact run that died on the 20/day cap: 127.5s video, naive + 9 windows + judges.
    est = estimate_calls(127.5, chunk=20, overlap=5, votes=1, candidates=4, include_naive=True)
    assert est["window_calls"] == 9
    assert est["total_calls"] == 14  # ...plus retries pushed the earlier partial day over 20
    est_full = estimate_calls(127.5, votes=3, candidates=5, include_naive=True)
    assert est_full["total_calls"] == 25
    assert not est_full["fits_free_day"]
    assert est_full["days_at_free_tier"] == 2


def test_estimate_calls_fits_when_trimmed():
    est = estimate_calls(127.5, votes=1, candidates=4, include_naive=False)
    assert est["total_calls"] == 13 and est["fits_free_day"]


# ---------------------------------------------------------------- motion validator (pure)

def _smooth_noise(n=1200, seed=7):
    rng = np.random.default_rng(seed)
    return np.convolve(rng.normal(size=n), np.ones(9) / 9, "same")


def test_pattern_shift_sign_convention():
    a = _smooth_noise()
    assert pattern_shift(a, np.roll(a, 37))[0] == 37     # pattern moved right
    assert pattern_shift(a, np.roll(a, -21))[0] == -21   # pattern moved left


def test_pattern_shift_confidence_high_on_true_shift():
    a = _smooth_noise()
    _, conf = pattern_shift(a, np.roll(a, 10))
    assert conf > 0.9


def test_motion_evidence_thresholds_and_directions():
    width = 1000
    strong_left_sweep = np.array([width * NET_SHIFT_THRESHOLD * 1.5])   # markings sweep right
    assert motion_evidence(strong_left_sweep, width)["direction"] == "left"
    strong_right = np.array([-width * NET_SHIFT_THRESHOLD * 1.5])       # markings sweep left
    assert motion_evidence(strong_right, width)["direction"] == "right"
    weak = np.array([width * NET_SHIFT_THRESHOLD * 0.5])
    ev = motion_evidence(weak, width)
    assert not ev["lateral_motion"] and ev["direction"] == "none"
    empty = motion_evidence(np.array([]), width)
    assert not empty["lateral_motion"]


# ---------------------------------------------------------------- Part 2 literal boolean

def test_is_valid_lane_change_returns_bare_bool():
    import json

    def judge(query, video=None, enable_thinking=True, time_interval=None, fps=None, schema=None):
        return json.dumps({"is_lane_change": True, "direction": "left", "reason": "ok"})

    out = is_valid_lane_change(judge, None,
                               {"t_start_s": 48, "t_end_s": 52, "direction": "left",
                                "description": "x"}, duration=127.5, votes=1)
    assert out is True
