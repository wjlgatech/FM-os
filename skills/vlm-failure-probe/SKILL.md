---
name: vlm-failure-probe
description: >-
  Turn a VLM failure taxonomy into a gated probe suite: encode failure modes
  (spatial/directional, temporal cross-chunk, multi-part prompts, retrieval
  reranking, grounding hallucination) as data, score any video-VLM pipeline
  against them, and gate with no-evidence⇒No discipline. Seeded from the VSS
  failure-benchmarking case study — every probe is an observed real failure.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# vlm-failure-probe

A cross-runtime skill that converts a **failure taxonomy into a regression gate**. Failure
analyses of video VLM pipelines (like NVIDIA VSS) usually end as prose in a paper; this skill
makes them **spec-as-data**: each failure mode lives in `probe_spec.yml` with its probes, ground
truth, matcher, and threshold — so the benchmark can gate CI, and a mitigation claim (prompt
engineering, reranking fix, vDPO) must move a measured score, not an anecdote.

## When to use (trigger)

Invoke when the user says "benchmark VLM failures", "failure taxonomy", "probe spatial
reasoning", "test cross-chunk consistency", "audit a video summarization pipeline", "did the
mitigation actually work", or names a system like NVIDIA VSS / a video-RAG pipeline.

## What it does

1. **Encode the taxonomy as data** — failure modes → probes (question, ground truth, matcher:
   `contains` / `order` / graded `all_parts`, threshold) in one YAML. The spec is the single
   source of truth; the paper's tables can be generated from it, so prose never drifts.
2. **Adapt any model** — the runner scores anything exposed as `answer(probe) -> str | None`:
   the VSS REST API, a local VLM, or a post-mitigation checkpoint.
3. **Score per failure mode** — mean probe score per mode, side-by-side scorecards for
   baseline vs. mitigated runs.
4. **Gate honestly** — a mode with no answers is **"not measured", never a pass**, and the
   blocking gate cannot pass while a required mode is unmeasured (FM-os Certified / BRACE
   discipline). Exits non-zero on failure so it gates CI.
5. **Define the paper's undefined metric** — the VSS paper names a *Temporal Grounding Score*
   (§X) and reports against it in a §XI that is still `TODO`. [`tgs_spec.yml`](reference/tgs_spec.yml)
   supplies the missing formula — `TGS = Σ wᶜ·sᶜ / Σ wᶜ` over three components mapped 1:1 to the
   paper's own prose (**order** = "sequencing of events", **anchor** = "time-based references",
   **persistence** = cross-chunk drift) — with weights as data, unmeasured components excluded
   and renormalized (never zeroed, never assumed), and the arithmetic pinned to hand computation
   in [`test_tgs.py`](reference/test_tgs.py).
6. **Report the grader's own variance** — `--repeat N` scores each model N times over the
   identical deterministic stimulus and flags any probe with `sd > 0` as **GRADER-UNSTABLE**.
   This exists because it caught us: see *Grader stability* below.

## Example

```bash
# self-contained proof: the paper's observed VSS failures are all caught,
# and a grounded model passes — exits non-zero if either side breaks
python reference/probe_runner.py
# offline gate (probe suite + the TGS gate math):
python -m pytest reference/test_probe_runner.py reference/test_tgs.py -q
# the Temporal Grounding Score derivation, baseline vs grounded:
python reference/tgs.py
# regenerate the deterministic synthetic stimuli (the paper's own methodology, as code):
python reference/stimuli.py
# LIVE: probe real vision models; writes out/RESULTS.md, the LaTeX table, raw_answers.json
ANTHROPIC_API_KEY=… python reference/run_real.py [--models claude-sonnet-5]
# LIVE + variance: score each model 3x and flag grader-unstable probes
ANTHROPIC_API_KEY=… python reference/run_real.py --repeat 3
```

```python
from reference.probe_runner import load_spec, run_probes, gate
spec = load_spec()                      # the taxonomy, as data
results = run_probes(my_vlm_adapter, spec)
ok, reasons = gate(results, spec)       # unmeasured mode -> cannot pass
```

## Live proof (measured 2026-07-25)

Run against **claude-sonnet-5** over the bundled synthetic stimuli: **5/5 failure modes PASS
at 1.00** — the same probes the observed VSS baseline fails 5/5 (spatial 0.25, temporal 0.00,
multipart 0.42, reranking 0.00, grounding 0.00). Raw answers + the generated LaTeX results
table live in [`reference/out/`](reference/out/). Every stimulus is deterministic
(`stimuli.manifest()` is hash-pinned by the tests), and a missing API key yields
"not measured" — never a fake pass.

## Discipline (why this is trustworthy)

- **Every probe is an observed failure** — seeded verbatim from the VSS failure-benchmarking
  study (colored-square ordering, snowboarder left/right, circled letter, fabricated falls,
  padel hallucination, last-line-only prompt handling, forklift reranking miss).
- **No evidence ⇒ No** — an unreachable endpoint yields "not measured", excluded from the
  score and fatal to the gate; a fake pass is impossible by construction.
- **Mitigations are measured** — the bundled `MockVSS` (reproduces the paper's failures) and
  `PatchedVSS` (the bar a fix must reach) keep the harness itself regression-tested.
- **The grader is audited like a model, and every audit is pre-registered** — spec changes carry
  a classified, justified audit log *in the spec* (`probe_spec.yml`), committed with falsifiable
  per-probe predictions **before** the run that tests them. Relaxing an expectation must be paid
  for by a tightening: the `reject:` field zeroes a probe whose answer credits the **wrong**
  entity, and `CheaterVSS` (fluent, confident, visually wrong prose) must still score 0 on every
  touched probe — so a grader fix can never make the gate vacuous.
- **A metric is not a name** — `tgs_spec.yml` states the formula, the weights, the tie-breaks and
  the degenerate cases; `test_tgs.py` pins the arithmetic to numbers a reviewer can check with a
  pencil. The paper's observed baseline scores **TGS 0.000** and a grounded model **1.000**, so
  the metric demonstrably discriminates.

## Deeper reference (FM-os knowledge base)

Case study: *Failure Benchmarking of NVIDIA's VSS Tool* (research-anything/case-studies).
Related: Zhong et al., *Multimodal Hallucination Snowballing*; Kosmos-2 (grounded VLM);
sibling skills [`agentic-eval`](../agentic-eval/) (benchmark axes + CI gates) and
[`research-loop`](../research-loop/) (pre-registered mitigation experiments). Gap audit:
[`docs/research/CASE-STUDIES-research-anything.md`](../../docs/research/CASE-STUDIES-research-anything.md).
