"""Zero-API lane-change validator — lateral-motion evidence straight from pixels.

The physics: a completed ego lane change slides the camera sideways ~one lane width, so
the LANE MARKINGS sweep horizontally across the image. Road curvature yaws the scene
slowly (small net sweep over a short snippet); lane straddling drifts then REVERSES
(low net displacement). So the cumulative horizontal shift of the marking pattern over
a snippet separates the cases — with zero model calls, zero quota, ~free latency.
(Motivated the hard way: the free Gemini tier is 20 requests/DAY; an LLM-judge-only
validation pipeline burns quota on every candidate.)

Method: collapse a scanline band (just below the horizon, where markings are widest)
into a 1-D brightness profile per sampled frame, then cross-correlate consecutive
profiles to measure how far the pattern slid sideways; integrate to a cumulative
profile and decide on |net displacement| / frame width.

NOTE: a first attempt used 2-D phase correlation on the whole road strip — measured
NOT separable on this video (flat asphalt + forward flow drown the lateral signal;
see git history). The threshold below is CALIBRATED by eval_motion.py on the interview
video's 4 ground-truth windows vs 7 matched negatives, and reported honestly.

Composes with the LLM judge as an independent CONFIRMING vote (measured role — see
threshold note below): boost confidence / settle direction when it fires; never veto.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

# Calibrated on the interview video by eval_motion.py (see motion_eval.json).
# MEASURED ROLE (honest): at 0.18 this is a HIGH-PRECISION CONFIRMER — 0/7 false
# positives, 3/4 recall, direction 3/3 correct on confident detections. Use it to
# CONFIRM a judge "yes" or break direction ties; never as a veto (it misses gentle
# lane changes, e.g. the 74-81s left change measured only 0.02).
NET_SHIFT_THRESHOLD = 0.18  # |net pattern shift| as fraction of frame width


def _band_profile(gray: np.ndarray, band: tuple[float, float] = (0.60, 0.72),
                  xmargin: float = 0.05) -> np.ndarray:
    """Collapse the lane-marking scanline band into a zero-mean 1-D brightness profile."""
    h, w = gray.shape
    strip = gray[int(h * band[0]):int(h * band[1]), int(w * xmargin):int(w * (1 - xmargin))]
    strip = cv2.GaussianBlur(strip, (9, 3), 0)
    prof = strip.mean(axis=0).astype(np.float64)
    return prof - prof.mean()


def pattern_shift(prev_prof: np.ndarray, cur_prof: np.ndarray,
                  max_lag: int = 120) -> tuple[int, float]:
    """(pixels the 1-D pattern moved RIGHT between prev and cur, correlation confidence)."""
    best_v, best_lag = -np.inf, 0
    n = prev_prof.size
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = prev_prof[lag:], cur_prof[:n - lag]
        else:
            x, y = prev_prof[:n + lag], cur_prof[-lag:]
        if x.size < 32:
            continue
        denom = (np.linalg.norm(x) * np.linalg.norm(y)) or 1.0
        v = float(np.dot(x, y)) / denom
        if v > best_v:
            best_v, best_lag = v, lag
    return -best_lag, best_v


def horizontal_shift_profile(video_path: str | Path, t_start: float, t_end: float,
                             fps: float = 8.0) -> np.ndarray:
    """Cumulative horizontal shift (pixels, + = markings sweep right) across [t_start, t_end]."""
    cap = cv2.VideoCapture(str(video_path))
    try:
        native = cap.get(cv2.CAP_PROP_FPS) or 30.0
        step = max(1, round(native / fps))
        f0, f1 = int(t_start * native), int(t_end * native)
        cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
        prev, shifts = None, []
        for f in range(f0, f1 + 1):
            ok, frame = cap.read()
            if not ok:
                break
            if (f - f0) % step:
                continue
            prof = _band_profile(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            if prev is not None:
                shift, conf = pattern_shift(prev, prof)
                # dashed markings streaming through the band alias as huge low-confidence
                # jumps — count a step only when the match is trustworthy and plausible
                shifts.append(shift if conf >= 0.55 and abs(shift) <= 50 else 0)
            prev = prof
        return np.cumsum(shifts) if shifts else np.array([])
    finally:
        cap.release()


def frame_width(video_path: str | Path) -> int:
    cap = cv2.VideoCapture(str(video_path))
    try:
        return int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1
    finally:
        cap.release()


def motion_evidence(profile: np.ndarray, width: int,
                    threshold: float = NET_SHIFT_THRESHOLD) -> dict:
    """Decision from a cumulative-shift profile. Pure — unit-testable without video."""
    if profile.size == 0:
        return {"lateral_motion": False, "net_shift_frac": 0.0, "direction": "none",
                "reason": "no frames"}
    net = float(profile[-1]) / width
    seen = abs(net) >= threshold
    # Ego moving RIGHT translates the camera right -> markings sweep LEFT in the image.
    direction = "none" if not seen else ("right" if net < 0 else "left")
    return {"lateral_motion": seen, "net_shift_frac": round(net, 4),
            "direction": direction,
            "reason": f"|net shift| {abs(net):.3f} of frame width vs threshold {threshold}"}


def is_lane_change_motion(video_path: str | Path, t_start: float, t_end: float,
                          pad: float = 1.0, fps: float = 8.0,
                          threshold: float = NET_SHIFT_THRESHOLD) -> dict:
    """One candidate window in -> motion verdict out (no model, no network)."""
    t0, t1 = max(0.0, t_start - pad), t_end + pad
    profile = horizontal_shift_profile(video_path, t0, t1, fps=fps)
    return motion_evidence(profile, frame_width(video_path), threshold)
