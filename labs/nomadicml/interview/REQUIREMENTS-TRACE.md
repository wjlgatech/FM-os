# Requirements traceability — Paul_Problem_Notebook.ipynb, term by term

Every requirement sentence in the notebook, mapped to where it is addressed and how it is
verified. Rule: **no evidence ⇒ not claimed** (a requirement without a test or a measured
run is marked accordingly).

## Task statement

| # | Requirement (verbatim/condensed) | Where addressed | Verified by |
|---|---|---|---|
| T1 | "identify all the moments the ego-vehicle … performs a **lane change**" | `detect_chunked()` + `validate_all()` end-to-end | `test_detect_chunked_recovers_all_ground_truth_globally` (fake VLM); live runs banked in `live_results.json` |
| T2 | "treating Gemini as a **black-box** that can't be changed … focus on improving the visual input" | No fine-tuning anywhere; all levers are input-side: windowing (`time_interval`), sampling (`fps`), snippet padding | By construction — the model is only reached through the notebook's own `gemini_inference` signature |
| T3 | Use the provided `display_video` / `upload_gemini` / `gemini_inference` | Solution functions take the notebook's `gemini_inference` verbatim as `infer_fn` (dependency injection) | `run_live.py::make_gemini_inference` mirrors the signature byte-for-byte; fakes in tests speak the same signature |
| T4 | "Feel free to use any other VLMs or embedding models" | The `infer_fn` seam makes the pipeline VLM-agnostic | `run_live.py --backend claude` runs the identical pipeline on Claude over sampled frames |

## Part 1 — Enhancing Visual Inputs

| # | Requirement | Where addressed | Verified by |
|---|---|---|---|
| P1.1 | "full video will be **split into separate sections** … analyzed separately" | `make_windows(duration, chunk, overlap)`; one upload, N windowed calls via `time_interval` (no re-encoding) | `test_windows_cover_duration_with_overlap`, `test_windows_short_video_single_window` |
| P1.2 | Worked example: 1-min video, 10s chunks → (0,10),(10,20)…(50,60), "merge the results" | `make_windows(60, chunk=10, overlap=0)` reproduces their exact windows; default `overlap=5` is a deliberate improvement (no maneuver cut at a boundary — longest GT event is 7s) | `make_windows` parameterization + overlap test; improvement rationale in README |
| P1.3 | "predictions for each window are **respect to the full video**" (their example: [40,50] window, 0–5 prediction → [40,45]) | `remap_to_global()` — window-relative primary, global-time fallback, clamp for nonsense | `test_remap_window_relative` (their exact example shape), `test_remap_falls_back_to_global_when_model_answered_absolute`, `test_remap_clamps_nonsense_to_window` |
| P1.4 | "output must be a **structured JSON** format that includes the start, end, and description" (their `LaneChangePredictions` cell) | `LaneChanges` Pydantic schema (`t_start`/`t_end` MM:SS + `description`, superset: `direction`) passed to `responseSchema`; `to_output_json()` emits the final JSON | `test_report_and_output_json_shapes`; schema field names match their reference cell |
| P1.5 | (implied by example) "merge the results from each of these windows" | `merge_events()` — same-direction interval union, ≤2s gap; dedupes double-seen events, folds double lane changes | `test_merge_dedupes_overlapping_windows_same_event`, `test_merge_folds_double_lane_change_within_gap`, `test_merge_keeps_opposite_directions_apart`, `test_merge_respects_gap` |

## Part 2 — Eliminating False Positive Predictions

| # | Requirement | Where addressed | Verified by |
|---|---|---|---|
| P2.1 | "implement a separate **validation pipeline**" | `validate_event()` / `validate_all()` — separate pass, padded snippet, higher fps, adversarial judge prompt, majority vote | `test_validate_event_majority_yes/no`, `test_validate_all_filters_fp_and_fixes_direction`, `test_validate_snippet_padding_clamped_to_video` |
| P2.2 | "for each predicted lane change event, validate whether its correct or not" | Per-event loop in `validate_all` | same as above |
| P2.3 | "For each lane change event snippet, **return a boolean** which is True when the predicted event is a valid lane change and False otherwise" | `is_valid_lane_change(...) -> bool` — the contract verbatim (thin wrapper keeping evidence in `validate_event`) | `test_is_valid_lane_change_returns_bare_bool` |
| P2.4 | "open ended problem! Feel free to be creative and use any approach … any tool" | Judge + self-consistency voting + direction override + zero-API motion confirmer (`motion_check.py`) | `eval_motion.py` measured on the real video (banked in `motion_eval.json`) |

## The notebook's three named failure modes

| Failure mode (their words) | Countermeasure | Evidence |
|---|---|---|
| "Lose information towards the end of the video" | Chunking — every window is short enough to keep temporal attention | Live Gemini run: naive found 0 events after 0:50; chunked windows cover to 2:07 |
| "Directions of the lane changes are often predicted incorrectly" | Judge (more frames on snippet) overrides detector direction; motion confirmer's direction was 3/3 correct where confident | `test_validate_all_filters_fp_and_fixes_direction`; `motion_eval.json` |
| "False positives … road curvature and lane straddling" | Both named explicitly as NOT-report rules in `CHUNK_PROMPT` and as reject rules in `JUDGE_PROMPT`; motion confirmer measured 0/7 FP on curvature windows | prompts in `lane_change_solution.py`; `motion_eval.json` |

## Known honest gaps

- Live full-pipeline numbers on **gemini-2.5-pro** (the interview's actual model) are not
  measurable from this machine: the free key allows 20 requests/day on flash and 0 on pro
  (`estimate_calls()` shows a full run needs ~25). The pipeline is exercised live via the
  Claude backend instead; the Gemini path is verified to the point the quota allows
  (naive + 7 of 9 windows, banked in `live_results_gemini_partial.json`).
- Motion confirmer is calibrated on ONE video (n=4 positives / 7 negatives) — a confirmer,
  not a gate, and says so in its docstring.
