---
name: curation-loop
description: >-
  Stand up an "AI training AI" data curation loop: use your own model to label,
  generate, and refine a video/multi-modal dataset, filter with quality + safety
  gates, and feed the result back into fine-tuning. Closes the data flywheel.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# curation-loop

A cross-runtime skill that builds a **self-improving dataset loop** — the "develop and
productionize curation loops that use our own models to generate and refine datasets" work.
Grounded in vetted open tooling from [FM-os](https://github.com/wjlgatech/FM-os).

## When to use (trigger)

Invoke when the user says "curation loop", "AI training AI", "generate and refine a dataset",
"auto-label video", "synthetic data pipeline", or "bootstrap training data from our model".

## What it does

1. **Mine** — sample candidate clips/frames from raw footage (video + sensor metadata).
2. **Label with the model** — run the current VLM to auto-caption / localize motion events,
   producing weak labels at scale.
3. **Refine + filter** — dedupe, score label confidence, and drop low-quality/unsafe samples
   (no-evidence-⇒-drop; keep only clips with agreement across passes).
4. **Human-in-the-loop gate** — surface a review queue for a sample; never auto-promote unlabeled
   or low-agreement data.
5. **Feed back** — emit a fine-tune-ready dataset and hand off to `vlm-quickstart`, then measure
   the delta with `agentic-eval`. Repeat.

## Example

```bash
python mine_clips.py --video ./raw/ --out candidates.jsonl
python label_with_vlm.py --model ./my-vlm --in candidates.jsonl --out labeled.jsonl
python refine.py --in labeled.jsonl --min-agreement 2 --out train.jsonl   # drop low-agreement
# -> feed train.jsonl to vlm-quickstart, then re-run agentic-eval to confirm a gain
```

## Verification (eval-with-teeth)

The loop only "succeeds" if the next `agentic-eval` run improves (or holds) on the held-out set;
a curation round that regresses eval is rejected, not shipped.

## Safety

Operates on the user's own data; HTTPS downloads only; no secrets; human gate before any
auto-generated data enters training.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
