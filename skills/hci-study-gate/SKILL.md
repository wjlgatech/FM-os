---
name: hci-study-gate
description: >-
  Pre-register a human-AI interaction study and gate its claims on whether the design
  can actually support them: required N from a target effect size, counterbalancing
  against order effects, a single pre-registered primary metric, and a blocking gate
  that reports "not measured" instead of a p-value the study is too small to earn.
  Use when designing or reviewing a user study of an AI system, or when a claim about
  human trust / preference / task performance needs an honest sample-size check.
---

# hci-study-gate — an underpowered user study is not evidence

## When to use (trigger)

- "we ran a user study, n=12, people preferred our agent"
- designing an evaluation where **humans** are the measuring instrument
- reviewing a paper/PR claim about trust, preference, workload, or task success
- any AI system whose real metric is what a person does with it

## The problem it solves

A human-AI interaction result fails for reasons an ML benchmark never does. The three
that kill most studies:

1. **Underpowered N.** With n=12 per arm you can only detect enormous effects. A null
   result is then uninformative, and a positive one is probably noise — yet both get
   reported as findings.
2. **Order effects.** If everyone sees the AI condition second, you measured practice
   and fatigue, not the AI.
3. **Metric drift.** Twenty outcomes collected, the significant one reported. The
   garden of forking paths, wearing a lab coat.

This skill turns each into a **machine-checkable gate**, in the FM-os discipline:
*no evidence ⇒ No.* A design that cannot support a claim yields **not measured** —
never a fake pass, and never a fake failure either.

## What it does

1. **Power → required N.** Given a target effect size (Cohen's *d*), α and power,
   compute the N per arm. Compare against planned N and refuse the claim if short.
2. **Counterbalancing check.** Within-subjects designs must present conditions in a
   balanced order (Latin square / full counterbalance); the gate names the imbalance.
3. **One primary metric, pre-registered.** Secondary metrics are allowed but are
   labelled exploratory in the output — they cannot carry the headline.
4. **Honest verdict.** `SUPPORTED` / `UNDERPOWERED` / `CONFOUNDED` / `NOT-MEASURED`,
   with the arithmetic shown so a reviewer can check it by hand.

## Example

```bash
# self-contained proof: a well-powered design passes, an n=12 design is refused,
# and an uncounterbalanced within-subjects design is caught. Exits non-zero on failure.
python reference/study_gate.py

# offline gate (power math pinned to textbook values + the three refusal paths):
python -m pytest reference/test_study_gate.py -q
```

```python
from reference.study_gate import StudyDesign, gate
design = StudyDesign(name="agent-vs-baseline", primary_metric="task_success_rate",
                     effect_size=0.5, planned_n_per_arm=40, arms=2,
                     within_subjects=True, condition_orders=[("A","B"),("B","A")])
verdict = gate(design)   # -> SUPPORTED, with required_n=64 shown if it were short
```

## Discipline (why this is trustworthy)

- **The power math is pinned to known values** — d=0.5, α=0.05, power=0.80 must give
  64 per arm (the textbook answer); the test fails if the formula drifts.
- **Refusal is the default.** A design missing a primary metric, an effect size, or a
  counterbalance is `NOT-MEASURED`, not "probably fine".
- **It cannot be argued with after the fact** — the design is the input, so raising N
  or changing the metric is a visible edit to a pre-registered artifact.

## Deeper reference (FM-os knowledge base)

Human-centred AI: Shneiderman, *Human-Centered AI* (arXiv:2002.04087) · Gilpin et al.,
*Explaining Explanations* (arXiv:1806.00069). Study tooling: jsPsych, PsychoPy,
OpenFace, Lab Streaming Layer (`data/repos.yml`, category `hci`). Sibling skills:
[`agentic-eval`](../agentic-eval/) (machine-side axes), [`research-loop`](../research-loop/)
(pre-registration for the whole experiment).
