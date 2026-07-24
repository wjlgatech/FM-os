# Interview solution — ego lane-change detection (Paul_Problem_Notebook)

Solves the NomadicML live-coding notebook: find every ego-vehicle lane change in the
highway video, treating Gemini 2.5 Pro as a black box. Ground truth (from the notebook):
right 0:48–0:52 · left 1:14–1:21 · double-right 1:24–1:31 · double-left 1:35–1:41.

## Files

| File | What it is |
|---|---|
| `lane_change_solution.py` | The whole solution — paste as ONE Colab cell. Pure logic + prompts + Part 1/Part 2 orchestration with the Gemini call injected (`infer_fn`), the literal `is_valid_lane_change() -> bool` contract, and `estimate_calls()` quota math. |
| `REQUIREMENTS-TRACE.md` | Term-by-term traceability: every notebook requirement → where addressed → the test or measured run that proves it. |
| `test_lane_change_solution.py` | 22 offline tests (no key, no network) covering remap, merge, scoring, and both pipelines against fakes. Runs in `make check`. |
| `test_beyond_ask.py` | 6 more offline tests: quota math (reproduces the real free-tier failure), motion-validator sign/threshold logic, the bare-boolean contract. |
| `run_live.py` | Rehearsal runner: real video, prints + banks the naive → chunked → validated scoreboard. `--backend gemini` (your `GEMINI_API_KEY`) or `--backend claude` — the SAME pipeline over frame sampling, proving the `infer_fn` seam is model-agnostic. |
| `motion_check.py` / `eval_motion.py` | Zero-API lane-change confirmer from pixels (1-D marking-sweep cross-correlation) + its calibration eval vs ground truth. Measured role (banked in `motion_eval.json`): high-precision confirmer — 0/7 FP, 3/4 recall, 3/3 direction — never a veto. |

## How to use it in the interview (Colab)

1. Run the notebook's setup cells (download, `upload_gemini`, `gemini_inference`).
2. Paste the contents of `lane_change_solution.py` as one cell.
3. Then:

```python
duration = video_duration_seconds(VIDEO_PATH)

# Part 1 — chunked inference (structured JSON out)
candidates = detect_chunked(gemini_inference, video_file, duration)
print(report(candidates, GROUND_TRUTH, title="After chunking"))

# Part 2 — validation pipeline (boolean per event)
validated = validate_all(gemini_inference, video_file, candidates, duration)
print(report(validated, GROUND_TRUTH, title="After validation"))

print(json.dumps(to_output_json(validated), indent=2))
```

## Design (the 30-second pitch)

- **Chunking without re-encoding.** `gemini_inference` already takes `time_interval`
  (startOffset/endOffset), so chunking = one upload + N windowed calls. 20 s windows,
  5 s overlap — the longest GT maneuver is 7 s, so every event fits whole in ≥1 window
  and nothing is cut at a boundary.
- **Timestamp remap is defensive.** Primary reading: clip-relative (+window start), per the
  requirement. If the model answered in global time anyway, keep it; nonsense clamps to the
  window. Unit-tested.
- **Merging is deterministic code, not another LLM call.** Same-direction events overlapping
  or within 2 s union together — dedupes events seen by two overlapping windows AND folds a
  double lane change reported as two singles into one event (matching how GT windows them).
- **Validation = adversarial judge + self-consistency.** Each candidate re-inferred on its
  ±3 s snippet at fps=5 with a prompt that names the false-positive causes (curvature,
  straddling, other vehicles) and demands a strict boolean. 3 votes, majority wins. The
  judge saw more frames, so on direction disagreement the judge's direction wins (fixes the
  flipped-direction failure mode).
- **Every stage is scored, not vibed.** Greedy IoU≥0.3 matching against the 4 GT windows →
  precision/recall/F1 printed naive → chunked → validated (the FM-os parity-harness
  discipline from `../nomadic_mini`).

## Rehearse before the interview

```bash
cd labs/nomadicml/interview
GEMINI_API_KEY=... python3 run_live.py                 # gemini-2.5-pro
GEMINI_API_KEY=... GEMINI_MODEL=gemini-2.5-flash python3 run_live.py   # free tier
```

Offline gate (also part of `make check` one level up):

```bash
python3 -m pytest -q
```

## Reused from FM-os

`nomadic_mini/events.py` (MM:SS contract + `seconds_to_mmss`), `analyze.py` (prompt/JSON
pattern, upload-poll loop), the KNOWLEDGE-BASE insight that lane-change signal lives in
cross-frame temporal attention (→ chunk ≫ maneuver length, overlap ≥ boundary risk), and
the parity-harness scoring discipline. Kept copy-inline rather than imported so the Colab
cell is self-contained.
