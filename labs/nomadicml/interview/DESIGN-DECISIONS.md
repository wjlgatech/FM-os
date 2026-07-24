# Design decisions — ego lane-change detection with a black-box VLM

The prose companion to the [animated architecture](../nomadic-mini-demo/public/interview-design.html)
(live at `/interview-design.html` on the demo). Each decision states the alternative we rejected
and the evidence behind the choice. Constraint that shapes everything: **Gemini is a black box** —
the only levers are what video it sees and what we do with its answers.

## 1. Chunking = windowed calls, not re-encoded clips

**Decision:** one upload + N calls with `time_interval=(start, end)` through the notebook's own
`gemini_inference` (it already maps to `startOffset`/`endOffset`).
**Rejected:** ffmpeg-splitting the video into N files and uploading each.
**Why:** zero re-encoding time, zero extra uploads, N× fewer moving parts — and it exercises the
exact API surface the interview provides. (The Claude fallback backend does sample frames with
ffmpeg, because that model has no native video input — the seam absorbs the difference.)

## 2. Chunk 20s / overlap 5s — derived from the data, not guessed

**Decision:** windows must comfortably contain a whole maneuver, and consecutive windows must
overlap by at least a maneuver's length.
**Evidence:** longest ground-truth event is 7s (1:14–1:21). 20s ≫ 7s keeps per-window temporal
attention sharp; 5s overlap means any event cut by one boundary sits whole inside the neighbor.
**Their worked example** (10s chunks, no overlap) is one parameter setting of the same function:
`make_windows(60, chunk=10, overlap=0)`.

## 3. Timestamp remap is defensive, with a fallback

**Decision:** interpret predictions as window-relative (the requirement), but if adding the window
offset overflows the window while the raw values already fit inside it, treat them as global; clamp
anything else.
**Why:** VLMs are inconsistent about clip-relative vs absolute time — we observed both. A hard
assumption either way silently corrupts every downstream stage. All three branches unit-tested.
**Observed bonus:** claude-sonnet-5 emitted `"00:08.5"` (decimal seconds) live; the parser
tolerates it, with a regression test citing the observation.

## 4. Merging is deterministic code, not another model call

**Decision:** same-direction events that overlap or sit within 2s union into one; different
directions never merge.
**Why:** dedupes the same maneuver seen by two overlapping windows AND folds a double lane change
reported as two singles into one event — matching how the ground truth windows them. Free,
instant, testable offline. An LLM "merge" call would add cost and a new failure mode to the exact
place we're trying to remove failure modes.

## 5. Recall at detection, precision at validation

**Decision:** Stage 1's job is candidates (high recall): sample each window k times and union the
results (`samples=3` on the flakier frames backend). Stage 2's job is killing false positives.
**Evidence:** live, the same window flickered between 1 and 0 candidates across identical calls
(temperature is fixed at 1 — `temperature` is deprecated on claude-sonnet-5). Self-consistency at
detection is the only lever left, and a spurious extra candidate costs one judge call while a
missed event is unrecoverable.

## 6. The judge is adversarial, votes, and owns direction

**Decision:** per candidate, re-infer on the ±3s snippet at fps=5 with a prompt that enumerates
the reject reasons (curvature, straddling, other vehicles); 3 votes, majority; the judge's
direction overrides the detector's.
**Why:** the notebook names all three false-positive sources — putting them verbatim in the judge's
job description attacks them directly. The judge sees ~5× the frame density of the detector on a
~10s span, so when they disagree on direction the judge has strictly more evidence. The Part 2
contract (`is_valid_lane_change() -> bool`) is a thin wrapper that keeps the vote evidence.

## 7. A zero-API confirmer, shipped at its measured strength

**Decision:** a pixels-only second opinion — collapse a lane-marking scanline band to a 1-D
brightness profile, cross-correlate consecutive frames, integrate the sweep.
**Evidence trail (honest):** v1 (2-D phase correlation on the road strip) measured NOT separable —
rebuilt. v2 (marking-band 1-D) calibrated on the interview video: at threshold 0.18, **0/7 false
positives, 3/4 recall, 3/3 direction agreement** (`motion_eval.json`).
**Shipped role:** high-precision *confirmer* — boosts confidence and settles direction ties; never
a veto (it misses gentle changes). Exists because quota is real: the free Gemini tier allows 20
requests/DAY, and this validator costs zero.

## 8. Quota is a design input, not a surprise

**Decision:** `estimate_calls()` computes window calls + judge calls against RPM/RPD budgets
before any run.
**Evidence:** two live runs died learning this (5/min and 20/day caps, both hit). The function's
test reproduces the real failure: a full pass needs ~25 calls > 20/day. At NomadicML's fleet scale
this same math is the difference between a plan and a surprise bill.

## 9. Everything scored, every claim traceable

**Decision:** greedy IoU≥0.3 matching against the 4 ground-truth windows prints precision/recall/F1
at every stage; `REQUIREMENTS-TRACE.md` maps every requirement sentence → code → test/measurement;
30 offline tests (no key, no network) gate `make check`.
**Why:** "chunking helped" is a vibe; "recall 0.25 → 1.0 with 1 FP, then FP removed by the judge"
is an engineering result. The interview is a conversation about evidence.

## 10. Model-agnostic by a one-argument seam

**Decision:** every pipeline function takes `infer_fn` as a parameter (the notebook's
`gemini_inference` signature is the interface).
**Evidence:** the identical pipeline ran live on Gemini (native video) and Claude (frame sampling),
and runs on deterministic fakes in tests. Swapping models is writing one adapter function —
which is also why the free-tier quota death didn't end the live demo.
