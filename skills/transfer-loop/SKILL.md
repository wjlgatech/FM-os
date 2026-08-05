---
name: transfer-loop
description: >-
  Turn what one deployment learned into a measured improvement for all the others —
  and refuse the transfer when the evidence does not support it. Extracts a candidate
  lesson from one engagement's failures, tests it against held-out engagements, and
  ships it only if it helps ELSEWHERE, not merely where it was found. Use when a fix
  found at one customer/site/repo is about to be generalised into a default, or when a
  self-improving agent framework needs to know whether a lesson actually transfers.
---

# transfer-loop — a lesson that only helps where you found it is not a lesson

## When to use (trigger)

- "this worked for customer A, let's make it the default"
- a self-improving agent framework generalising across engagements
- any playbook/backbone entry about to be promoted from one incident
- post-mortem output about to become policy

## The problem it solves

Cross-engagement learning fails in a specific, predictable way: the lesson is extracted
from the same data that motivated it, so it always looks true. This is overfitting with
a project-management vocabulary. Three concrete failure modes:

1. **The n=1 promotion.** One incident becomes a rule. It cannot be wrong, because the
   only evidence for it is the case it was drawn from.
2. **The lesson that transfers negatively.** It helps at the source and *hurts*
   elsewhere — the most expensive kind, because the source keeps confirming it.
3. **The unfalsifiable lesson.** "Communicate more clearly." No engagement can fail it,
   so no engagement can test it.

## What it does

1. **Split by engagement, never by sample.** The held-out set is *other engagements*.
   Splitting rows within one engagement leaks the thing you are trying to measure.
2. **Require a directional prediction, pre-registered.** A lesson must say which metric
   moves, which way, and by at least how much — before it is tested.
3. **Score transfer, not fit.** `lift_elsewhere` = mean improvement on held-out
   engagements. Improvement at the source is reported but **cannot** carry the verdict.
4. **Four honest verdicts.** `TRANSFERS` · `LOCAL-ONLY` (helps only at the source —
   keep it as a note on that engagement, not a default) · `NEGATIVE-TRANSFER` (hurts
   elsewhere: a finding worth more than a pass) · `NOT-MEASURED` (too few engagements,
   or no prediction — never a pass).

## Example

```bash
# self-contained proof: a real transfer passes, a source-only win is caught as
# LOCAL-ONLY, a harmful default is caught as NEGATIVE-TRANSFER. Exits non-zero on failure.
python reference/transfer.py

# offline gate (the arithmetic + all four verdict paths):
python -m pytest reference/test_transfer.py -q
```

```python
from reference.transfer import Lesson, evaluate
lesson = Lesson(name="retry-on-429-with-jitter", source="engagement-a",
                metric="task_success", direction="up", min_effect=0.05,
                predicted_before=True)
verdict = evaluate(lesson, baselines, treatments)   # -> TRANSFERS / LOCAL-ONLY / ...
```

## Discipline (why this is trustworthy)

- **Held out by engagement.** The unit of generalisation is the engagement, so that is
  the unit of the split.
- **A prediction made after the fact is not a prediction.** `predicted_before=False`
  forces `NOT-MEASURED`, regardless of how good the numbers look.
- **Fewer than 2 held-out engagements ⇒ NOT-MEASURED.** No amount of source-side
  improvement substitutes for somewhere else to test it.
- **Negative transfer is reported, never rounded to "no effect"** — it is the signal
  that a default would have quietly cost you.

## Deeper reference (FM-os knowledge base)

Post-training and preference transfer: `data/papers.yml` (InstructGPT and the
post-training entries). Siblings: [`agentic-eval`](../agentic-eval/) (per-axis gates),
[`research-loop`](../research-loop/) (pre-registration for a whole experiment),
[`vlm-failure-probe`](../vlm-failure-probe/) (the grader-audit discipline this inherits).
