# The zero that wasn't evidence — a four-window audit of our own null

**Date:** 2026-08-14 · **Trigger:** rc0039 reported `pipeline_claim: FALSE` after the base
role hallucinated 0 times in 18 captions. That verdict was wrong, and the four research
windows say so from four independent directions.

---

## The mistake, stated plainly

On 2026-08-14 `skills/syndata-bare/reference/run_real.py` ran the BARE pipeline against real
vision models. The base role produced **0 hallucinations in 18 captions**, so the runner
concluded there was nothing for refinement to repair and marked the pipeline claim **not
substantiated**.

The arithmetic was right. The inference was not. *Observing zero events does not make the
underlying rate zero* — and the correction is older than machine learning by a century.

---

## 🏺 last300years — the binomial, and the rule of three

The load-bearing survivor is the binomial distribution itself (Jacob Bernoulli, *Ars
Conjectandi*, 1713): the probability of observing zero events in *n* trials when the true rate
is *p* is (1−p)ⁿ, which is large for small *n* however non-zero *p* is.

Its practical form is the **rule of three** — Hanley & Lippman-Hand, *"If nothing goes wrong,
is everything all right? Interpreting zero numerators"* (JAMA, 1983). With 0 events in *n*
trials, the 95% confidence interval for the true rate is **[0, 3/n]**. It falls straight out of
(1−p)ⁿ = 0.05. Three centuries on, it is still the first thing to reach for when a count comes
back zero, and it is still routinely forgotten.

Applied to our run: **0/18 ⇒ 95% CI [0, 16.7%]**. Our experiment could not distinguish a base
role that never hallucinates from one that hallucinates on one caption in six.

## 🕰 last30years — power analysis reached NLP, and was ignored anyway

The survival-tested finding in this window is that **NLP experiments are routinely
underpowered**, and that this is known, published, and still not practised. Card et al. (EMNLP
2020) is the canonical statement: a typical 2,000-sentence machine-translation test set has
only about **75% power** to detect a one-BLEU difference. The 2026 restatement is blunter — most
teams size eval sets by "feels like enough" rather than by any power calculation, and the
majority of experiments that report a sample size are underpowered for the effect they claim.

The window's verdict: this correction has survived thirty years of being right and being
skipped. Our run was a textbook instance.

## 🌗 last30months — half the thesis is independently confirmed; half is not

**Mode collapse in instruction-tuned models is 🌗 adopted.** Independently confirmed outside the
BARE paper: Schaffelder & Gatt, *"Synthetic Eggs in Many Baskets: The Impact of Synthetic Data
Diversity on LLM Fine-Tuning"* (Findings of ACL 2026) reproduces distribution collapse and shows
multi-source synthetic data mitigates it, with code released. Mixing teachers, seeding with real
data, and running an explicit diversity check are described as standard 2026 practice.

**BARE itself is ⚪ unproven in this window.** The paper (Zhu et al., arXiv:2502.01697, Feb 2025)
is well cited and has a public repo, but this run found **no independent replication and no
evidence of production adoption**. That is a finding, not a gap in our searching — and it is
worth stating precisely because our own measurement reproduced the confirmed half (mode
collapse, large and repeatable) and could not test the unconfirmed half.

**The number that decided it:** independent 2026 frontier benchmarking puts **Claude Haiku 4.5 —
our default base role — at a 4.62% hallucination rate**. With p = 0.0462 and n = 18, the chance
of observing exactly zero is (1−0.0462)¹⁸ ≈ **0.43**. A coin-flip's worth of luck produced our
"result".

## 📰 last30days — benchmark saturation is the live conversation

The current discussion is that evaluations built to last years are saturating in months, so the
gaps that remain are smaller than the benchmarks can resolve. That is our failure mode viewed
from the other end: our stimuli were not merely easy, they were **below the resolution of the
thing we were trying to measure**.

---

## What was changed, in code

1. **`rule_of_three(n)` and `power_check(...)`** — the 1983 correction, executable, with the
   minimum detectable rate anchored to the published 4.62% figure rather than to taste.
2. **A third verdict.** `pipeline_claim` is now `True` / `False` / **`None` (inconclusive)**. A
   clean base role with too few samples yields `None` and the artifact says why. Exit codes
   separate the three: `0` substantiated, `1` refuted, **`2` inconclusive** — because "we could
   not tell" must never be filed under the same code as "we tested it and it failed".
3. **A second declared condition, not a retuned first one.** Text interference in colour
   perception, after *What Color Is It?* (arXiv:2511.13400): a conflicting colour word is
   printed on the shape and the model is asked the shape's colour. Both conditions are always
   reported. The plain condition was **not** made harder until something broke — that is the
   distinction between adding a control and p-hacking, and it is why the null survived rather
   than being tuned out of existence.

## What the powered runs found

Both conditions were re-run at adequate power:

| condition | n | hallucinations | 95% CI | resolves 4.62%? |
|---|---|---|---|---|
| plain captioning | 66 | 0 | [0, 4.5%] | yes |
| text interference | 72 | 0 | [0, 4.2%] | yes |

**0 hallucinations in both.** The published text-interference mechanism — built specifically to
induce colour hallucination — does not fool a 2026 frontier model on this construction. The
verdict is now `pipeline_claim: NOT SUBSTANTIATED` with `underpowered: False`: a genuine
negative, carried by its *n*.

That sharpens the open question rather than closing it. BARE's pipeline claim presupposes a base
role producing repairable errors. With an instruction-tuned proxy, that presupposition **does not
hold** — a statement about the proxy, not about BARE. The paper's own claim stays untested until
a genuine base checkpoint fills the role.

**The half that did replicate:** mode collapse, and it got *clearer* with sample size — instruct
diversity 0.23 (n=18) → 0.19 (n=36) → 0.18 (n=66) against a base role steady at ~0.60. A real
effect sharpens as n grows; that is what the underpowered zero could never have shown us.

## Sources

- Hanley & Lippman-Hand, *If nothing goes wrong, is everything all right?* (JAMA 1983) —
  https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf ·
  https://en.wikipedia.org/wiki/Rule_of_three_(statistics)
- Schaffelder & Gatt, *Synthetic Eggs in Many Baskets* (Findings of ACL 2026) —
  https://aclanthology.org/2026.findings-acl.360/ · code
  https://github.com/maxschaffelder/synthetic_data_diversity
- Zhu et al., *BARE* (arXiv:2502.01697) — https://arxiv.org/abs/2502.01697 · repo
  https://github.com/pgasawa/BARE
- *What Color Is It? A Text-Interference Multimodal Hallucination Benchmark* —
  https://arxiv.org/abs/2511.13400
- 2026 frontier hallucination-rate benchmarking (Claude Haiku 4.5 at 4.62%) —
  https://www.digitalapplied.com/blog/ai-model-hallucination-rate-benchmarks-2026-study
- Statistical power in NLP evaluation —
  https://www.tmls.nyc/research/eval-sample-complexity

**Caveat on the tiers:** the 4.62% figure comes from a vendor-independent blog benchmark, not a
peer-reviewed source; it is used as a *reference rate for sizing*, which is the use it can bear.
Swap in a better-sourced rate and `MIN_DETECTABLE_RATE` is the one line to change.
