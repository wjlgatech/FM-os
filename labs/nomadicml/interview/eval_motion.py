"""Calibrate + evaluate the zero-API motion validator against the interview video.

Positives: the 4 ground-truth lane-change windows.
Negatives: 7 matched-length windows chosen away from any GT event (includes early-video
curvature stretches — exactly the false-positive source the notebook warns about).

Prints per-window measured net shift, the positive/negative separation, accuracy at the
shipped threshold, and direction agreement vs GT. Writes motion_eval.json. No API calls.

    python3 eval_motion.py   (needs interview/video.mp4 — run run_live.py once, or it downloads)
"""

from __future__ import annotations

import json
from pathlib import Path

from lane_change_solution import GROUND_TRUTH
from motion_check import (
    NET_SHIFT_THRESHOLD,
    frame_width,
    horizontal_shift_profile,
    motion_evidence,
)

VIDEO = Path(__file__).parent / "video.mp4"

# No-lane-change windows (checked against GT: nearest event edge >= 4s away).
NEGATIVES = [(5, 12), (14, 21), (25, 32), (33, 40), (56, 63), (64, 71), (110, 117)]


def main():
    if not VIDEO.exists():
        from run_live import download_video
        download_video()
    width = frame_width(VIDEO)
    rows = []
    for (s, e, d, label) in GROUND_TRUTH:
        ev = motion_evidence(horizontal_shift_profile(VIDEO, s - 1, e + 1), width)
        rows.append({"window": f"{s}-{e}", "kind": "positive", "gt_direction": d,
                     "label": label, **ev})
    for (s, e) in NEGATIVES:
        ev = motion_evidence(horizontal_shift_profile(VIDEO, s, e), width)
        rows.append({"window": f"{s}-{e}", "kind": "negative", "gt_direction": "none",
                     "label": "no lane change", **ev})

    pos = [r for r in rows if r["kind"] == "positive"]
    neg = [r for r in rows if r["kind"] == "negative"]
    tp = sum(r["lateral_motion"] for r in pos)
    fp = sum(r["lateral_motion"] for r in neg)
    dir_ok = sum(r["direction"] == r["gt_direction"] for r in pos if r["lateral_motion"])

    print(f"{'window':>9}  {'kind':>8}  {'net_shift':>9}  {'motion?':>7}  {'dir':>5}  {'gt':>5}")
    for r in rows:
        print(f"{r['window']:>9}  {r['kind']:>8}  {r['net_shift_frac']:>9}  "
              f"{str(r['lateral_motion']):>7}  {r['direction']:>5}  {r['gt_direction']:>5}")
    pos_min = min(abs(r["net_shift_frac"]) for r in pos)
    neg_max = max(abs(r["net_shift_frac"]) for r in neg)
    print(f"\npositives |net| min = {pos_min:.3f}   negatives |net| max = {neg_max:.3f}"
          f"   threshold = {NET_SHIFT_THRESHOLD}")
    print(f"recall {tp}/{len(pos)} · false positives {fp}/{len(neg)}"
          f" · direction correct {dir_ok}/{tp if tp else 0}")
    if pos_min > neg_max:
        verdict = "SEPARABLE — usable as a standalone gate"
    elif fp == 0 and tp >= len(pos) - 1:
        verdict = "HIGH-PRECISION CONFIRMER — confirms/directions only, never veto"
    else:
        verdict = "NOT usable as a gate at any single threshold"
    print(f"verdict: {verdict}")

    out = {"threshold": NET_SHIFT_THRESHOLD, "rows": rows,
           "summary": {"recall": f"{tp}/{len(pos)}", "false_positives": f"{fp}/{len(neg)}",
                       "direction_correct": f"{dir_ok}/{tp}", "pos_min_abs": round(pos_min, 4),
                       "neg_max_abs": round(neg_max, 4), "verdict": verdict}}
    Path(__file__).with_name("motion_eval.json").write_text(json.dumps(out, indent=2))
    print("wrote motion_eval.json")


if __name__ == "__main__":
    main()
