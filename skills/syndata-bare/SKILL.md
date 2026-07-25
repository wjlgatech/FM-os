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
# offline gate:
python -m pytest reference/test_bare_loop.py -q
```

```python
from reference.bare_loop import run_pipeline
assert not run_pipeline("base_only")["gate_pass"]      # hallucinates
assert not run_pipeline("instruct_only")["gate_pass"]  # mode-collapses
assert run_pipeline("bare")["gate_pass"]               # the thesis, measured
```

## Discipline (why this is trustworthy)

- **The thesis is falsifiable** — BARE must beat BOTH baselines under identical budget and
  seed; if refinement homogenizes (diversity drops) or misses hallucinations, the gate fails.
- **Repair over discard** — yield is reported: a CLIP filter alone throws away ~40% of base
  drafts here; refinement keeps 100% while reaching full grounding.
- **The refiner never invents** — property-tested: every refined token is grounded in the
  image's facts (the hallucination-snowballing guard).

## Deeper reference (FM-os knowledge base)

Zhu et al., *BARE: Base-Refine* (arXiv:2502.01697) · case study: *Adapting the BARE Framework
for Synthetic Data Generation in VLMs* (research-anything/case-studies) · sibling skills
[`vlm-quickstart`](../vlm-quickstart/) (train on the generated data), [`curation-loop`](../curation-loop/)
(dataset curation), [`vlm-failure-probe`](../vlm-failure-probe/) (probe the trained model). Gap
audit: [`docs/research/CASE-STUDIES-research-anything.md`](../../docs/research/CASE-STUDIES-research-anything.md).
