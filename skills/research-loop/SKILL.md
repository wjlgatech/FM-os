---
name: research-loop
description: >-
  Run a rigorous, closed research loop on a foundation-model question: frame a
  falsifiable hypothesis, design a minimal experiment with a control, run it,
  measure honestly (report the metric AND the failure), adversarially critique
  the result, and write it up so it reproduces. Turns "read the field" into
  "practice the craft" with empirical rigor.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# research-loop

A cross-runtime skill for **doing research, not just reading it** — the "research judgment and
empirical rigor" a frontier-lab role is hired for. It enforces a closed loop so a claim is never
shipped without evidence. Grounded in the autonomous-research methods FM-os curates
([FM-os](https://github.com/wjlgatech/FM-os)).

## When to use (trigger)

Invoke when the user says "run an experiment", "test this hypothesis", "ablation", "is this real",
"design a study", "reproduce this paper", "research loop", or "write this up for a paper".

## The loop (each stage gates the next)

1. **Frame** — state one *falsifiable* hypothesis and the metric that would confirm/refute it, plus
   the null result you'd accept. Vague questions are rejected here.
2. **Design** — the *minimal* experiment: one variable, a control/baseline, fixed seeds, a
   pre-registered success threshold. Estimate cost before running.
3. **Run** — execute end to end; log config + environment + seed for reproducibility.
4. **Measure honestly** — report the metric with variance across seeds, AND where it failed. No
   cherry-picking; a regression or null result is a valid, reportable outcome (no evidence ⇒ no claim).
5. **Ablate** — remove/vary each component to show *what actually caused* the effect, guarding
   against a confound.
6. **Critique (adversarial)** — a skeptic pass tries to refute the finding: leakage, unfair
   baseline, tuning-on-test, too few seeds. The claim survives only if it withstands this.
7. **Write up** — a short report (claim, method, results-incl-negative, threats-to-validity, repro
   command) ready for a lab notebook or a NeurIPS/CVPR-style submission.

## Example

```bash
# hypothesis: LoRA rank 16 beats rank 8 on our eval, holding all else fixed
for r in 8 16; do
  for seed in 0 1 2; do
    swift sft --model Qwen/Qwen2.5-1.5B --lora_rank $r --seed $seed --output out_r${r}_s${seed}
    lm_eval --model hf --model_args pretrained=out_r${r}_s${seed} --tasks arc_easy > res_r${r}_s${seed}.json
  done
done
python analyze.py --glob 'res_*.json'   # mean±std per rank; refute if CIs overlap
```

## Verification (eval-with-teeth)

The write-up is rejected if it lacks: a control, ≥3 seeds with variance, an ablation, and a
reproduce command. A finding with overlapping confidence intervals is reported as "no effect",
never inflated — the same no-evidence-⇒-No discipline as FM-os Certified.

## Safety

Runs the user's own experiments; HTTPS downloads only; no secrets; flags any eval that touches the
test set during development (leakage guard).

## Cross-runtime

One `SKILL.md`; thin manifests wrap it for Claude Code, Codex, and Hermes.
