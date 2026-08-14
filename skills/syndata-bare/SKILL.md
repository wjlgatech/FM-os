---
name: syndata-bare
description: >-
  Run BARE (Base-Refine) synthetic data generation for vision-language models
  as a measurable closed loop: a base VLM drafts diverse candidates, an
  instruction-tuned VLM refines them for grounding, and twin gates (CLIP-style
  alignment floor + diversity floor) prove the pipeline beats either model
  alone — catching both hallucination and mode collapse before training.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# syndata-bare

A cross-runtime skill that turns the **BARE-VLM recipe into a gated pipeline**. The
diversity–correctness trade-off is the whole game in synthetic data: instruction-tuned models
mode-collapse (safe, samey captions), base models hallucinate (objects that aren't there).
BARE's answer — base drafts, instruct refines — is only trustworthy if **both failure modes are
measured**, so this skill ships twin gates and demands the two-stage pipeline beat each
single-stage baseline under the same budget and seed.

## When to use (trigger)

Invoke when the user says "generate synthetic data for a VLM", "BARE", "base-refine",
"synthetic captions / VQA pairs", "diversity vs quality trade-off", "mode collapse in
generated data", or "filter image-text pairs with CLIP".

## What it does

1. **Define the target** — task (captioning / VQA), domain, and the quality criteria that
   become gates (alignment floor, diversity floor, per-sample keep threshold).
2. **Draft with the base model** — high-temperature sampling, varied prompts/templates for
   entropy; expect (and measure) misalignment.
3. **Refine with the instruct model** — image-conditioned repair of each draft: fix ungrounded
   objects/attributes, keep the phrasing variety. Repair beats filtering: full yield instead
   of discarding hallucinated drafts.
4. **Gate on both axes** — mean CLIP-style alignment ≥ floor AND mean pairwise diversity ≥
   floor; the pipeline ships only if it passes both while each single-stage baseline fails
   its characteristic gate. Exits non-zero otherwise.
5. **Scale up** — swap the toy seams for BLIP-2 (base) / InstructBLIP or Qwen2.5-VL
   (refiner) / real CLIP; the loop, metrics, and gates are unchanged.

## Example

```bash
# self-contained proof (stdlib only): base fails alignment, instruct fails
# diversity, BARE passes both at full yield — exits non-zero otherwise
python reference/bare_loop.py
# against REAL vision models, over deterministic synthetic scenes.
# --per-scene 11 gives n=66 >= the 65 needed to resolve a 4.62% rate; fewer and
# the runner will (correctly) return INCONCLUSIVE rather than a verdict.
ANTHROPIC_API_KEY=… python reference/run_real.py --per-scene 11 --interference-n 12
# exit 0 = substantiated · 1 = refuted · 2 = inconclusive/underpowered
# offline gate (no network, no keys):
python -m pytest reference/test_bare_loop.py reference/test_run_real.py -q
```

```python
from reference.bare_loop import run_pipeline
assert not run_pipeline("base_only")["gate_pass"]      # hallucinates
assert not run_pipeline("instruct_only")["gate_pass"]  # mode-collapses
assert run_pipeline("bare")["gate_pass"]               # the thesis, measured
```

## Measured against real models — and the honest null

`reference/run_real.py` runs the three pipelines over six deterministic synthetic scenes
(`bare_stimuli.py`) whose ground truth is known by construction, so grounding is checkable
without CLIP, an LLM judge, or a human. **Two claims are scored separately and never conflated:**

| claim | what it needs | status |
|---|---|---|
| *pipeline* — draft-then-refine beats either single stage at matched budget | any two models | **NOT SUBSTANTIATED** at this difficulty |
| *paper* — a BASE checkpoint supplies diversity an instruct model cannot | a real base checkpoint in the base role | **UNMEASURABLE** with an instruction-tuned proxy |

First live run (2026-08-14, base role `claude-haiku-4-5` @ T=1.0, instruct `claude-sonnet-5`,
18 captions per pipeline):

| pipeline | alignment | diversity | yield | gate |
|---|---|---|---|---|
| base_only | 1.00 | 0.62 | 1.00 | PASS |
| instruct_only | 1.00 | 0.23 | 1.00 | **FAIL** (mode collapse) |
| bare | 1.00 | 0.56 | 1.00 | PASS |

**Half the thesis reproduced, half had no headroom.** Mode collapse is real and large — the
instruct role's diversity is a third of the base role's, and it fails the floor. The base role
did not hallucinate *once*.

> ⚠️ **That first verdict was retracted the same day.** The runner reported the pipeline claim
> **NOT SUBSTANTIATED**. Wrong — not the arithmetic, the logic. By the **rule of three**
> (Hanley & Lippman-Hand, *JAMA* 1983) 0 events in 18 trials puts the 95% CI for the true rate at
> **[0, 16.7%]**, which cannot exclude the **4.62%** rate independently published for the very
> model used; under that rate P(zero in 18) ≈ **0.43**. A claim is only refuted by a run that
> could have detected it. The honest verdict was **UNDERPOWERED**.

**The runner now returns three outcomes, not two** — `SUBSTANTIATED` / `NOT SUBSTANTIATED` /
**`INCONCLUSIVE`** — with exit codes `0` / `1` / **`2`**, because *we could not tell* must never
share a code with *we tested it and it failed*. Every negative ships with its *n* and the
smallest effect that *n* could resolve.

**A second condition, added as a control — not a retuned first one.** Text interference in colour
perception, after *What Color Is It?* (arXiv:2511.13400): a conflicting colour word is printed on
the shape and the model is asked the shape's colour. Naming the printed word is unambiguous
hallucination — no caption parsing, no synonym trap. Both conditions are always reported.

**Result at adequate power (n = 72 ⇒ CI upper bound 4.17% < 4.62%): 0 hallucinations.** The
published interference mechanism does not fool a 2026 frontier model on this construction. That
is a *well-powered negative* — and a far more useful result than the underpowered one it
replaces, because it says the precondition BARE needs (a base role that produces repairable
errors) does not hold **for this proxy**, which is a statement about the proxy, not about BARE.

The plain stimuli were **not** made harder until the thesis passed. Tuning a benchmark until it
agrees with you is how the 0.92 in the draft paper happened.

**Role fidelity is enforced, not assumed.** Every model reachable through the Anthropic API is
instruction-tuned, so it can fill the base *role* but is not a base *model*. A run stamps
`proxy` unless the base model is a checkpoint listed in `vlm_roles.BASE_CHECKPOINTS`, and a proxy
run can never mark the paper's claim substantiated — the emitted LaTeX caption says so in the
table itself. Point `--base-model` at a real base checkpoint over an OpenAI-compatible endpoint
(vLLM / NIM / TGI, via `BARE_OPENAI_BASE_URL`) to make that claim measurable at all.

**Known limits, restated in every artifact:** alignment is an upper bound (only closed-vocabulary
decoys can be scored wrong); high-entropy captions route around that vocabulary entirely
("crimson", "cobalt", "orbs" — observed live), which weakens the bound *in the direction that
flatters the base role*; and primitive colour/shape grounding is a weaker proxy than
natural-image captioning.

## Discipline (why this is trustworthy)

- **The thesis is falsifiable** — BARE must beat BOTH baselines under identical budget and
  seed; if refinement homogenizes (diversity drops) or misses hallucinations, the gate fails.
- **Repair over discard** — yield is reported: a CLIP filter alone throws away ~40% of base
  drafts here; refinement keeps 100% while reaching full grounding.
- **The refiner never invents** — property-tested: every refined token is grounded in the
  image's facts (the hallucination-snowballing guard).
- **Not measured is never a failure** — no key, an API error, an empty response or a truncated
  one all mean the caption is EXCLUDED from every aggregate. Scoring an empty string as a
  hallucination would publish a failure the model never committed; that exact fake failure was
  found live in the sibling skill `vlm-failure-probe`.
- **A rejected sampling parameter is disclosed** — `claude-sonnet-5` refuses `temperature`
  outright. The runner retries without it and stamps the artifact, because "matched budget" is a
  claim it makes and an unapplied temperature quietly voids it.
- **A negative carries its power or it is an opinion** — every zero-event result reports *n* and
  the rule-of-three CI, and an underpowered zero returns `INCONCLUSIVE`, never `FALSE`. This
  skill's own first published verdict violated that rule; the test that would have caught it
  (`test_the_first_live_run_was_underpowered_not_a_refutation`) is now pinned in CI.

## Deeper reference (FM-os knowledge base)

Zhu et al., *BARE: Base-Refine* (arXiv:2502.01697) · case study: *Adapting the BARE Framework
for Synthetic Data Generation in VLMs* (research-anything/case-studies) · sibling skills
[`vlm-quickstart`](../vlm-quickstart/) (train on the generated data), [`curation-loop`](../curation-loop/)
(dataset curation), [`vlm-failure-probe`](../vlm-failure-probe/) (probe the trained model). Gap
audit: [`docs/research/CASE-STUDIES-research-anything.md`](../../docs/research/CASE-STUDIES-research-anything.md).
