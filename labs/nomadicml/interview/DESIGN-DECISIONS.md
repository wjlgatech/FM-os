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
**Measured live (gemini-2.5-pro):** under `startOffset/endOffset` the model reports **GLOBAL**
timestamps (probed directly: clip (45,55) described with "00:46…00:54"), despite the prompt asking
for clip-relative — the global fallback is what kept the run correct. A single-interpretation
remap would have silently shifted every event by its window offset.
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

## 6. The judge is marking-anchored, votes, and refines boundaries

**Decision:** per candidate, re-infer on the ±5s snippet at fps=5 with a prompt that (a) forces the
decision onto the PAINTED LANE MARKINGS ("markings sweep left ⇒ ego moved right"), explicitly
disqualifying other-vehicle motion as evidence, (b) enumerates the reject reasons (curvature,
straddling, other vehicles), and (c) returns a refined t_start/t_end; 3 votes, majority.
**Why marking-anchoring (measured live):** gemini-2.5-pro rejected a REAL lane change (0:48–0:52)
claiming "the white SUV ahead changed lanes; the ego continued straight" — it attributed the ego's
motion to the lead vehicle. Ego-vs-other relative motion is genuinely ambiguous unless anchored on
the markings, which move only when the ego moves.
**Why boundary refinement (measured live):** the detector times onsets 2–4s early (e.g. 1:22–1:24
for the true 1:24–1:31), which scores IoU=0 against ground truth despite being a real detection.
The judge sees the padded snippet at 5× frame density — it's the right place to fix timing.

## 7. Pixel evidence arbitrates the VLM — rescue and direction

**Decision:** a pixels-only second opinion — collapse a lane-marking scanline band to a 1-D
brightness profile, cross-correlate consecutive frames, integrate the sweep. Wired into
validation as an arbiter: judge-KEEP takes motion's direction when it fires; judge-REJECT with
strong motion evidence is RESCUED (kept, motion's direction).
**Evidence trail (honest):** v1 (2-D phase correlation on the road strip) measured NOT separable —
rebuilt. v2 (marking-band 1-D) calibrated on the interview video: at threshold 0.18, **0/7 false
positives, 3/4 recall, 3/3 direction agreement** (`motion_eval.json`). The rescue rule exists
because the judge's live false-negative (0:48–0:52, §6) is exactly the ambiguity class the motion
check is immune to — and at its threshold it has measured zero false positives, so a rescue
cannot inject curvature FPs on this calibration set.
**Also why it exists at all:** quota is real — the free Gemini tier allows 20 requests/DAY, and
this validator costs zero.

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

## 10. Recall-first funnel: pixels nominate, models judge

**Decision:** detection = union of VLM window candidates AND motion-scan nominations
(`nominate_candidates`: one 3-second decode pass, threshold deliberately LOW at 0.10). Precision
is restored downstream by the judge + calibrated sweep arbitration (rescue at 0.25, measured
0-FP on calibration windows).
**Why:** a candidate missed at Stage 1 is unrecoverable; a spurious one costs one judge call.
Measured standalone: the scan alone hits 3 of 4 ground-truth regions (including both doubles)
with zero model calls — including regions the VLM detector missed outright. Loose nomination
bounds don't matter because the judge refines boundaries and the sweep's own span times the
crossing (it recovered 48.0–53.1 for the true 48–52 event).

## 11. This is feature engineering — and the combiner's scaling path is learned

**Decision:** treat the VLM and the pixels as feature extractors over candidate windows, and the
validation logic as a combiner. Today the combiner is hand-tuned rules over calibrated thresholds
(0.10 nominate / 0.18 direction / 0.25 rescue); `to_feature_vector()` freezes the schema a
LEARNED combiner would consume: sweep magnitude/span/agreement, judge vote fraction,
detector-judge direction agreement, refinement offset.
**Why the pixel feature earns its place:** it was chosen for an *invariance* — the marking sweep
cannot confuse ego motion with a lead vehicle's maneuver, which is precisely the VLM's measured
failure mode. Classic feature engineering: encode the domain knowledge the model lacks.
**Scaling path (other data):** labels from public sets (BDD100K lane annotations, comma2k19 CAN,
NGSIM/highD trajectories) or pseudo-labels distilled from the expensive pro pipeline over
unlabeled fleet video — the same curation flywheel NomadicML productizes. Where CAN/IMU exists,
lateral-acceleration S-curves become the strongest feature of all and the VLM's job shrinks to
description. AutoML/tsfresh over the shift series or a small temporal CNN on the profile
sequence are the hands-free variants.

## 12. Model-agnostic by a one-argument seam

**Decision:** every pipeline function takes `infer_fn` as a parameter (the notebook's
`gemini_inference` signature is the interface).
**Evidence:** the identical pipeline ran live on Gemini (native video) and Claude (frame sampling),
and runs on deterministic fakes in tests. Swapping models is writing one adapter function —
which is also why the free-tier quota death didn't end the live demo.
