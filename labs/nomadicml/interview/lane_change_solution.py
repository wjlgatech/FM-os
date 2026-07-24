"""NomadicML interview — ego-vehicle lane-change detection with Gemini as a black box.

Solves the two parts of Paul_Problem_Notebook.ipynb:

  Part 1 (Enhancing Visual Inputs)  -> detect_chunked(): overlapping-window inference over
      one uploaded video (the notebook's gemini_inference already supports startOffset/
      endOffset via time_interval, so chunking needs NO re-encoding), window-relative ->
      global timestamp remap, then deterministic cross-window merging.
  Part 2 (Eliminating False Positives) -> validate_all(): per-event judge pass on a padded
      snippet at higher fps, with an adversarial prompt targeting the notebook's named
      failure modes (road curvature, lane straddling), majority-voted for stability.

All pure logic (windows, remap, merge, IoU scoring) is API-free and unit-tested offline
(test_lane_change_solution.py). The Gemini call is injected as `infer_fn` — in Colab pass
the notebook's own `gemini_inference`; in tests pass a fake.

COLAB USAGE (paste this file's contents as one cell, then):

    duration = video_duration_seconds(VIDEO_PATH)          # via cv2
    candidates = detect_chunked(gemini_inference, video_file, duration)
    print(report(candidates, GROUND_TRUTH, title="After chunking"))
    validated = validate_all(gemini_inference, video_file, candidates, duration)
    print(report(validated, GROUND_TRUTH, title="After validation"))
    print(json.dumps(to_output_json(validated), indent=2))
"""

from __future__ import annotations

import json
from typing import Callable, List, Literal, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Ground truth from the notebook (seconds, direction) — used only for scoring.
# ---------------------------------------------------------------------------
GROUND_TRUTH = [
    (48, 52, "right", "right lane change"),
    (74, 81, "left", "left lane change"),
    (84, 91, "right", "double right lane change"),
    (95, 101, "left", "double left lane change"),
]

# ---------------------------------------------------------------------------
# Structured-output schemas (passed straight to gemini_inference's `schema=`).
# ---------------------------------------------------------------------------


class LaneChange(BaseModel):
    t_start: str = Field(description="Start of the lane change in MM:SS, relative to the clip shown")
    t_end: str = Field(description="End of the lane change in MM:SS, relative to the clip shown")
    direction: Literal["left", "right"] = Field(description="Direction the ego-vehicle moves")
    description: str = Field(description="One sentence: what visibly happens")


class LaneChanges(BaseModel):
    lane_changes: List[LaneChange] = Field(description="All ego lane changes in the clip")


class Verdict(BaseModel):
    is_lane_change: bool = Field(description="True only for a fully completed ego lane change")
    direction: Literal["left", "right", "none"] = Field(description="'none' when is_lane_change is false")
    reason: str = Field(description="One sentence of visual evidence for the verdict")


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

CHUNK_PROMPT = """You are analyzing a SHORT CLIP cut from a longer highway drive, filmed from the \
ego-vehicle's forward-facing camera.

Find every moment the EGO-VEHICLE (the camera car) performs a lane change.

A lane change means: the ego-vehicle's camera centerline FULLY crosses one painted lane divider \
and settles into the adjacent lane. Direction is "left" if the ego moves into the lane to its \
left, "right" if into the lane to its right. If two dividers are crossed back-to-back (a double \
lane change), report it and say "double" in the description.

Do NOT report:
- Road curvature: the whole road bends but the ego stays centered between the same lane markings.
- Lane straddling: the ego drifts onto a divider but returns without completing the crossing.
- Lane changes performed by OTHER vehicles.

All timestamps must be relative to THE CLIP YOU ARE SHOWN, starting at 00:00.
If there are no ego lane changes in this clip, return an empty list."""

JUDGE_PROMPT = """You are a strict validator. This short clip was flagged as containing exactly one \
ego-vehicle lane change (the ego-vehicle is the camera car). Your job is to REJECT false positives.

Answer is_lane_change=true ONLY if you can visibly see the ego camera position fully cross a \
painted lane divider and settle into the adjacent lane within this clip.

Answer is_lane_change=false if what you see is any of:
- Road curvature (the road bends; the ego keeps the same position between its lane markings).
- Lane straddling or an aborted change (touches/rides the divider, returns to the original lane).
- Another vehicle changing lanes, not the ego.
- No visible crossing inside this clip.

If true, report the direction the ego moves ("left" or "right"); otherwise direction="none"."""


# ---------------------------------------------------------------------------
# Pure logic — no API, fully unit-testable.
# ---------------------------------------------------------------------------


def mmss_to_seconds(t: str) -> float:
    """MM:SS -> seconds. Tolerates decimal seconds ('00:08.5') — VLMs emit them."""
    m, s = t.strip().split(":")
    return int(m) * 60 + float(s)


def seconds_to_mmss(t: float) -> str:
    t = max(0, int(round(t)))
    return f"{t // 60:02d}:{t % 60:02d}"


def video_duration_seconds(video_path: str) -> float:
    import cv2

    cap = cv2.VideoCapture(video_path)
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        return frames / fps if fps else 0.0
    finally:
        cap.release()


def make_windows(duration: float, chunk: float = 20.0, overlap: float = 5.0) -> list[tuple[float, float]]:
    """Overlapping windows covering [0, duration]. Overlap > longest maneuver (~7s here is the
    max ground-truth event, 5s overlap + 20s chunk means every event fits whole in >=1 window)."""
    if chunk <= overlap:
        raise ValueError(f"chunk ({chunk}) must exceed overlap ({overlap})")
    step = chunk - overlap
    windows, start = [], 0.0
    while True:
        end = min(start + chunk, duration)
        windows.append((start, end))
        if end >= duration:
            return windows
        start += step


def remap_to_global(t_start: float, t_end: float, win_start: float, win_end: float,
                    tol: float = 2.0) -> tuple[float, float]:
    """Window-relative -> global seconds (the Part 1 requirement).

    Primary interpretation: timestamps are relative to the clip start (add win_start).
    Fallback: if that lands past the window end but the raw values already fit inside the
    window, the model answered in global time — keep them. Otherwise clamp to the window."""
    rel_s, rel_e = win_start + t_start, win_start + t_end
    if rel_e <= win_end + tol:
        return rel_s, rel_e
    if win_start - tol <= t_start and t_end <= win_end + tol:
        return t_start, t_end
    return min(rel_s, win_end), min(rel_e, win_end)


def merge_events(events: list[dict], max_gap: float = 2.0) -> list[dict]:
    """Merge same-direction events that overlap or sit within max_gap seconds — dedupes the
    same maneuver seen by two overlapping windows, and folds double lane changes reported as
    two back-to-back singles into one event (matching how the ground truth windows them)."""
    merged: list[dict] = []
    for direction in sorted({e["direction"] for e in events}):
        group = sorted((e for e in events if e["direction"] == direction),
                       key=lambda e: (e["t_start_s"], e["t_end_s"]))
        run: Optional[dict] = None
        for ev in group:
            if run and ev["t_start_s"] - run["t_end_s"] <= max_gap:
                run["t_end_s"] = max(run["t_end_s"], ev["t_end_s"])
                if ev["description"] not in run["description"]:
                    run["description"] += " / " + ev["description"]
            else:
                if run:
                    merged.append(run)
                run = dict(ev)
        if run:
            merged.append(run)
    return sorted(merged, key=lambda e: e["t_start_s"])


def interval_iou(a: tuple[float, float], b: tuple[float, float]) -> float:
    inter = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    union = max(a[1], b[1]) - min(a[0], b[0])
    return inter / union if union > 0 else 0.0


def score_predictions(preds: list[dict], gt: list[tuple] = GROUND_TRUTH,
                      iou_thresh: float = 0.3) -> dict:
    """Greedy IoU matching, each prediction/GT window used at most once -> precision/recall/F1."""
    pairs = sorted(
        ((interval_iou((p["t_start_s"], p["t_end_s"]), (g[0], g[1])), i, j)
         for i, p in enumerate(preds) for j, g in enumerate(gt)),
        reverse=True,
    )
    matched_p, matched_g, matches = set(), set(), []
    for iou, i, j in pairs:
        if iou < iou_thresh or i in matched_p or j in matched_g:
            continue
        matched_p.add(i)
        matched_g.add(j)
        matches.append({"pred": i, "gt": j, "iou": round(iou, 3),
                        "direction_ok": preds[i]["direction"] == gt[j][2]})
    tp, fp, fn = len(matches), len(preds) - len(matches), len(gt) - len(matches)
    precision = tp / len(preds) if preds else 0.0
    recall = tp / len(gt) if gt else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": round(precision, 3),
            "recall": round(recall, 3), "f1": round(f1, 3), "matches": matches}


def report(preds: list[dict], gt: list[tuple] = GROUND_TRUTH, title: str = "Score") -> str:
    s = score_predictions(preds, gt)
    lines = [f"== {title} ==",
             f"predictions={len(preds)}  TP={s['tp']}  FP={s['fp']}  FN={s['fn']}",
             f"precision={s['precision']}  recall={s['recall']}  f1={s['f1']}"]
    for ev in preds:
        lines.append(f"  {seconds_to_mmss(ev['t_start_s'])}-{seconds_to_mmss(ev['t_end_s'])} "
                     f"{ev['direction']:>5}  {ev['description'][:80]}")
    return "\n".join(lines)


def to_output_json(events: list[dict]) -> dict:
    """The required structured JSON output: start, end, description (plus direction)."""
    return {"lane_changes": [
        {"t_start": seconds_to_mmss(e["t_start_s"]), "t_end": seconds_to_mmss(e["t_end_s"]),
         "direction": e["direction"], "description": e["description"]}
        for e in events
    ]}


def estimate_calls(duration: float, chunk: float = 20.0, overlap: float = 5.0,
                   votes: int = 3, candidates: int = 4, include_naive: bool = False,
                   rpm: int = 5, rpd: int = 20) -> dict:
    """Quota math BEFORE running — the free Gemini tier (5 req/min, 20 req/DAY) killed
    two live rehearsals of this pipeline before this function existed. At fleet scale
    (NomadicML's world: 500+ videos/day) this is the difference between a plan and a bill."""
    import math

    window_calls = len(make_windows(duration, chunk, overlap))
    judge_calls = candidates * votes
    total = window_calls + judge_calls + (1 if include_naive else 0)
    return {"window_calls": window_calls, "judge_calls": judge_calls, "total_calls": total,
            "minutes_at_rpm": math.ceil(total / rpm),
            "days_at_free_tier": math.ceil(total / rpd),
            "fits_free_day": total <= rpd}


# ---------------------------------------------------------------------------
# Part 1 — chunked inference (infer_fn = the notebook's gemini_inference).
# ---------------------------------------------------------------------------


def detect_chunked(infer_fn: Callable, video_file, duration: float,
                   chunk: float = 20.0, overlap: float = 5.0,
                   fps: Optional[int] = None, samples: int = 1) -> list[dict]:
    """samples > 1 = self-consistency for RECALL: a borderline maneuver may be reported on
    only some detection samples, so union candidates across samples (merge dedupes); the
    judge stage restores precision downstream."""
    raw: list[dict] = []
    for win_start, win_end in make_windows(duration, chunk, overlap):
        found: list[dict] = []
        for _ in range(samples):
            text = infer_fn(query=CHUNK_PROMPT, video=video_file,
                            time_interval=(int(win_start), int(win_end)), fps=fps,
                            schema=LaneChanges)
            found.extend(json.loads(text)["lane_changes"])
        print(f"window {seconds_to_mmss(win_start)}-{seconds_to_mmss(win_end)}: "
              f"{len(found)} candidate(s) across {samples} sample(s)")
        for ev in found:
            g_start, g_end = remap_to_global(mmss_to_seconds(ev["t_start"]),
                                             mmss_to_seconds(ev["t_end"]), win_start, win_end)
            if g_end - g_start <= 0:
                continue
            raw.append({"t_start_s": g_start, "t_end_s": g_end,
                        "direction": ev["direction"], "description": ev["description"]})
    return merge_events(raw)


# ---------------------------------------------------------------------------
# Part 2 — per-event validation pipeline (returns the required boolean per event).
# ---------------------------------------------------------------------------


def validate_event(infer_fn: Callable, video_file, event: dict, duration: float,
                   pad: float = 3.0, votes: int = 3, fps: int = 5) -> dict:
    """Judge one candidate on its padded snippet at high fps; majority vote across `votes` runs."""
    win_start = max(0.0, event["t_start_s"] - pad)
    win_end = min(duration, event["t_end_s"] + pad)
    verdicts = []
    for _ in range(votes):
        text = infer_fn(query=JUDGE_PROMPT, video=video_file,
                        time_interval=(int(win_start), int(win_end)), fps=fps, schema=Verdict)
        verdicts.append(json.loads(text))
    yes = sum(bool(v["is_lane_change"]) for v in verdicts)
    valid = yes * 2 > len(verdicts)
    dirs = [v["direction"] for v in verdicts if v["is_lane_change"] and v["direction"] != "none"]
    judge_direction = max(set(dirs), key=dirs.count) if dirs else "none"
    return {"valid": valid, "votes_yes": yes, "votes": len(verdicts),
            "judge_direction": judge_direction, "reasons": [v["reason"] for v in verdicts]}


def is_valid_lane_change(infer_fn: Callable, video_file, event: dict, duration: float,
                         **judge_kwargs) -> bool:
    """The Part 2 contract, verbatim: one predicted event snippet in -> one boolean out
    (True = valid lane change). Thin wrapper over validate_event, which keeps the evidence."""
    return validate_event(infer_fn, video_file, event, duration, **judge_kwargs)["valid"]


def validate_all(infer_fn: Callable, video_file, events: list[dict], duration: float,
                 **judge_kwargs) -> list[dict]:
    """Filter candidates through the judge; the judge saw the snippet at higher fps, so when it
    confirms the event but disagrees on direction, its direction wins (fixes flipped directions)."""
    kept = []
    for ev in events:
        verdict = validate_event(infer_fn, video_file, ev, duration, **judge_kwargs)
        print(f"judge {seconds_to_mmss(ev['t_start_s'])}-{seconds_to_mmss(ev['t_end_s'])} "
              f"({ev['direction']}): {'KEEP' if verdict['valid'] else 'REJECT'} "
              f"[{verdict['votes_yes']}/{verdict['votes']} yes, dir={verdict['judge_direction']}]")
        ev = dict(ev, validation=verdict)
        if verdict["valid"]:
            if verdict["judge_direction"] in ("left", "right"):
                ev["direction"] = verdict["judge_direction"]
            kept.append(ev)
    return kept
