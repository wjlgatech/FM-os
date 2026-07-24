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


def strongest_sweep(shifts: np.ndarray, times: list[float], width: int,
                    max_span_s: float = 8.0) -> dict:
    """The maximal |sum| of per-step shifts over any contiguous run of duration <= max_span_s,
    both signs considered. Immune to opposite-sweep cancellation (a window straddling a right
    then a left lane change nets to ~0 but contains two strong runs). Pure — testable.

    Returns {frac, t0, t1, direction} for the strongest run ('none' if no steps)."""
    n = len(shifts)
    if n == 0 or len(times) != n:
        return {"frac": 0.0, "t0": 0.0, "t1": 0.0, "direction": "none"}
    best = {"frac": 0.0, "t0": times[0], "t1": times[0], "direction": "none"}
    cum = np.concatenate([[0.0], np.cumsum(shifts)])
    for i in range(n):
        for j in range(i, n):
            if times[j] - times[i] > max_span_s:
                break
            s = (cum[j + 1] - cum[i]) / width
            if abs(s) > abs(best["frac"]):
                best = {"frac": round(float(s), 4), "t0": times[i], "t1": times[j],
                        "direction": "right" if s < 0 else "left"}
    return best


def sweep_in_window(video_path: str | Path, t_start: float, t_end: float,
                    fps: float = 8.0, max_span_s: float = 8.0) -> dict:
    """Strongest bounded sweep inside [t_start, t_end] of the video (no model, no network)."""
    cap = cv2.VideoCapture(str(video_path))
    try:
        native = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1
        step = max(1, round(native / fps))
        f0, f1 = int(t_start * native), int(t_end * native)
        cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
        prev, times, shifts = None, [], []
        for f in range(f0, f1 + 1):
            ok, frame = cap.read()
            if not ok:
                break
            if (f - f0) % step:
                continue
            prof = _band_profile(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            if prev is not None:
                shift, conf = pattern_shift(prev, prof)
                shifts.append(shift if conf >= 0.55 and abs(shift) <= 50 else 0)
                times.append(f / native)
            prev = prof
        return strongest_sweep(np.asarray(shifts), times, width, max_span_s)
    finally:
        cap.release()


# ---------------------------------------------------------------------------
# Recall-first candidate NOMINATION — scan the whole video once, propose windows.
# Detection funnel: nominate low-threshold (recall) -> judge + calibrated motion
# arbitration downstream (precision). A missed candidate is unrecoverable; a
# spurious one costs one judge call.
# ---------------------------------------------------------------------------

NOMINATE_THRESHOLD = 0.10  # deliberately below NET_SHIFT_THRESHOLD: recall-first

# Rescue bar for judge-overrides, calibrated at judge-scale (±5s) windows via
# strongest_sweep: true sweeps measured 0.236-0.362, worst negative 0.218.
RESCUE_THRESHOLD = 0.25


def candidate_motion(video_path: str | Path, t_start: float, t_end: float,
                     pad: float = 5.0) -> dict:
    """Sweep evidence for one candidate, on the judge's padded window (detectors time onsets
    early, so the sweep often lies outside tight candidate bounds). Returns the validate_all
    arbitration dict: rescue-grade (>= RESCUE_THRESHOLD), direction-grade (>= NET_SHIFT
    threshold), plus the sweep's own time span (better bounds than the candidate's)."""
    sw = sweep_in_window(video_path, max(0.0, t_start - pad), t_end + pad)
    frac = abs(sw["frac"])
    return {"lateral_motion": frac >= RESCUE_THRESHOLD,
            "direction_confident": frac >= NET_SHIFT_THRESHOLD,
            "direction": sw["direction"] if frac >= NET_SHIFT_THRESHOLD else "none",
            "net_shift_frac": sw["frac"], "span": (sw["t0"], sw["t1"])}


def whole_video_shift_series(video_path: str | Path, fps: float = 8.0
                             ) -> tuple[list[float], np.ndarray, int]:
    """One decode pass -> (sample times, cumulative shift at each sample, frame width)."""
    cap = cv2.VideoCapture(str(video_path))
    try:
        native = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1
        step = max(1, round(native / fps))
        prev, times, shifts = None, [], []
        f = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if f % step == 0:
                prof = _band_profile(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
                if prev is not None:
                    shift, conf = pattern_shift(prev, prof)
                    shifts.append(shift if conf >= 0.55 and abs(shift) <= 50 else 0)
                    times.append(f / native)
                prev = prof
            f += 1
        return times, np.cumsum(shifts) if shifts else np.array([]), width
    finally:
        cap.release()


def nominate_from_series(times: list[float], cum: np.ndarray, width: int,
                         win: float = 8.0, stride: float = 2.0,
                         threshold: float = NOMINATE_THRESHOLD) -> list[dict]:
    """Slide a window over the cumulative-shift series; nominate spans whose net sweep
    exceeds threshold*width; merge overlapping same-sign nominations. Pure — testable."""
    if len(times) < 2:
        return []
    noms = []
    t, t_max = times[0], times[-1]
    idx = np.asarray(times)
    while t < t_max:
        t1 = min(t + win, t_max)
        i, j = int(np.searchsorted(idx, t)), min(int(np.searchsorted(idx, t1)), len(cum) - 1)
        net = (float(cum[j]) - float(cum[i])) / width
        if abs(net) >= threshold:
            noms.append({"t_start_s": round(t, 1), "t_end_s": round(t1, 1),
                         "direction": "right" if net < 0 else "left",
                         "description": f"motion-nominated (net sweep {net:+.3f} of width)"})
        if t1 >= t_max:
            break
        t += stride
    # merge overlapping same-direction nominations into single candidates
    merged: list[dict] = []
    for n in noms:
        if merged and merged[-1]["direction"] == n["direction"] \
                and n["t_start_s"] <= merged[-1]["t_end_s"]:
            merged[-1]["t_end_s"] = n["t_end_s"]
        else:
            merged.append(dict(n))
    return merged


def nominate_candidates(video_path: str | Path, win: float = 8.0, stride: float = 2.0,
                        threshold: float = NOMINATE_THRESHOLD) -> list[dict]:
    """Whole video in -> motion-nominated candidate events out. Zero model calls."""
    times, cum, width = whole_video_shift_series(video_path)
    return nominate_from_series(times, cum, width, win, stride, threshold)
