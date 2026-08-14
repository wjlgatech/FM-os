# Case study — reverse-engineering the Thomson-1 stack

**What triggered this:** a LinkedIn post by **Andrew M. Bean** (Lead Research Scientist,
Thomson Reuters; DPhil, Oxford Internet Institute), ~2026-07-30:

> After countless experiments, benchmarks, training runs, RL environments, expert
> consultations etc… we're almost ready to launch our new LLM! We've built a pipeline which
> can take an open source base model and specialize it for professional work — in this case
> boosting Qwen 3.5 397B to performance competitive with Opus 4.8. Along the way, we perform
> a substantial re-alignment of model values towards factuality and pluralism, and perform
> targeted training for agentic capabilities and professional domains with minimal impact on
> other aspects of model performance.

…tagging eleven colleagues.

**The method in one line:** *the coauthor list is the bill of materials.* This team publishes.
Almost every stage of the pipeline that post describes has a paper behind it, written by
someone tagged in it. So this is not speculation about what a lab might do — it is their own
literature, reassembled into the pipeline they just announced.

**Live status of the reconstruction** (regenerate with `make thomson`):

```
Thomson-1 stack reconstruction — 18 stages
  published  14  (78%)
  stated      4  (22%)
  inferred    0  (0%)
  → 18/18 stages rest on a primary source, not on our reading.

Prediction ledger — 12 registered claims
  Brier: UNSCORED — 0 resolved, 12 awaiting the technical report.
```

---

## 1. The request, evaluated

The ask was: *track Bean and his coauthors, reverse-engineer the technical stack, do the same
for everyone mentioned, then build a case study with knowledge base, tooling and community.*
Good instincts, four real problems:

**① "Reverse-engineer their stack" is unfalsifiable as an essay.** Anyone can write a
plausible pipeline; nobody can check it. A confident, wrong reconstruction and a confident,
right one read identically. → **Fixed by** [`data/predictions.yml`](../../data/predictions.yml):
12 numbered claims with explicit probabilities and resolution criteria, registered
**2026-08-13, before the technical report exists**. The report is the answer key. `make thomson`
computes a Brier score when it lands. That converts an essay into a scored forecast.

**② "Track 11 people's publications" is a breadth trap.** FM-os's own
[research program](RESEARCH-PROGRAM.md) says *one mile deep, not one mile wide* — new work must
deepen a probe or sharpen the thesis. Eleven bios does neither. → **Fixed by** listing people
against **the mechanism they own** in the stack, and by *omitting* tagged names with no public
technical trace. Two of the eleven (Kirsty Fielding, and the tagged "Bradley B.") have no
findable technical publications in this line of work; under *no evidence ⇒ no entry* they are
absent. Alexander Kardos-Nyheim is present in this document as Safe Sign's founding CEO — a
company fact, not a mechanism — and so is not in `people.yml` either.

**③ "Community" is the ask most likely to produce a dead artifact.** A new forum nobody joins.
→ **Fixed by** joining one that already exists and is load-bearing here: **Every Eval Ever**
(arXiv:2606.14516), a community schema for evaluation results with Bean among its 49 authors —
22,235 models, 2,273 benchmarks, 31 formats, open to contribution. See §6.

**④ The premise is partly stale — and that is the most valuable finding.** The post says "not
a secret much longer." It is already substantially not a secret. On **2026-07-31** Thomson
Reuters published benchmark numbers, and the Q2 2026 earnings call named the model and its
cost. So a chunk of what was to be "reverse-engineered" is simply *reported*, and the honest
job is to separate the three tiers below. Anyone who wrote this up as pure inference would have
been re-deriving public facts and presenting them as insight.

**What the request did not ask for, and should have:** the "so what". Thomson Reuters Labs is
currently hiring a **Research Scientist, LLM Agents (Foundational Research)** in London — the
exact team, the exact stack. FM-os already has `make jdfit` for precisely this. Noted here as
an open thread, not actioned.

---

## 2. Evidence tiers — what is known vs. what we are betting on

Every stage in [`data/thomson_stack.yml`](../../data/thomson_stack.yml) carries one:

| tier | meaning | count |
|---|---|---|
| `published` | a paper by a **named team member** describes this mechanism | 14 |
| `stated` | the company or an author says it publicly, without the mechanism | 4 |
| `inferred` | our reconstruction — **must** carry a registered prediction id | 0 |

`make thomson` fails if an `inferred` stage has no bet attached. The reconstruction turned out
to need none: everything traces to a primary source. What is genuinely *inferred* is not any
single stage but **the assembly** — which of these published mechanisms actually made it into
Thomson-1, and in what order. That is exactly what the 12 predictions bet on.

---

## 3. The stack

### Training

| # | Stage | Mechanism | Evidence |
|---|---|---|---|
| 0 | Base model | Open-weight frontier base (post says Qwen 3.5 397B); TR says only "open source LLMs" | stated |
| 1 | Data construction | [Knowledge graphs for training-data construction](https://arxiv.org/abs/2601.13806) over Westlaw · Practical Law · Checkpoint · Reuters | published |
| 2 | Targeted selection | [CoLoR-Filter](https://arxiv.org/abs/2406.10670) — pick documents by loss reduction on the target domain | published |
| 3 | **Data mixture** | [ADMIRE-BayesOpt](https://arxiv.org/abs/2508.11551) — mixture weights via **multi-fidelity Bayesian optimization**, learned on proxy models and transferred up. **>500% speed-up**; 460 runs / 13,000 GPU-hours released | published |
| 4 | **Specialization** | [SIMoE](https://arxiv.org/abs/2506.12597) — upcycle dense → MoE where each expert is a **structurally sparse subset of the seed model's own parameters**, discovered automatically, merged by a learned router | published |
| 5 | **Forgetting control** | [CapTrack](https://arxiv.org/abs/2603.06610) — forgetting as capability-decomposed drift. **Instruction tuning drifts harder; preference optimization is conservative and can partially recover** | published |
| 6 | Value re-alignment | [PRISM](https://arxiv.org/abs/2404.16019) (1,500 people / 75 countries) + [Principal Hierarchies](https://arxiv.org/abs/2605.12120) | published |
| 7 | Factuality | [HalluLens](https://arxiv.org/abs/2504.17550) — hallucination and factuality as **separate** problems needing separate benchmarks | published |
| 8 | Agentic training | RL in tool-use environments over Westlaw/Practical Law; Deep Research harness | stated |
| 9 | Composition | [Composable Interventions](https://arxiv.org/abs/2407.06483) — stacking edit/unlearn/compress changes outcomes; order matters | published |
| 10 | Staying current | [Memory of Amortized Contexts](https://arxiv.org/abs/2403.04317) — absorb new documents without retraining | published |

### Evaluation — where this team is unusually strong

| # | Stage | Mechanism | Evidence |
|---|---|---|---|
| E1 | **Eval cost** | [Scales++](https://arxiv.org/abs/2510.26384) — item-centric subsetting, **18× cheaper**; 0.25% of Open LLM Leaderboard → 3.2% MAE | published · **[runnable in FM-os](../../skills/eval-subset/)** |
| E2 | Judging | [DeCE](https://arxiv.org/abs/2509.16093) — decomposed criteria, not one pointwise judge score; 224 attorney-curated legal QA pairs | published |
| E3 | Validity | [Measuring What Matters](https://arxiv.org/abs/2511.04703) — **445 benchmarks, 29 reviewers, most fail construct validity** | published |
| E4 | Contamination | [LingOly](https://arxiv.org/abs/2406.06196) / LingOly-TOO — reasoning that cannot be memorised | published |
| E5 | Long context | LOFT + NovelQA at 1M tokens; 20,000+ test samples; attorney-authored "minimum viable answer" standards | stated |
| E6 | Shared substrate | [Every Eval Ever](https://arxiv.org/abs/2606.14516) — one schema, 22,235 models | published |
| H | Human loop | Hundreds of SMEs; bar-admitted attorney editors; human + automated red-teaming | stated |

### The three findings that actually matter

**① The org chart is the architecture.** Bean's title is *Evaluations Lead **for LLM
post-training***. Not "eval team". The people who decide what counts as good and the people who
train the model are one group. FM-os's own research thesis — *eval gates are training-signal
factories* — is this, and here it is running at industrial scale in a public company. That is a
sharpening of our thesis by an existence proof, which is worth more than another probe.

**② "Minimal impact on other aspects" is a mechanism claim, not a reassurance.** It rests on
two published results: SIMoE puts domain knowledge into *separable sparse parameter subsets*
instead of smearing it across all weights, and CapTrack shows *preference optimization is more
conservative than instruction tuning and can partially recover lost capability*. Schwarz's whole
pre-Thomson career — Progress & Compress, Powerpropagation, functional regularisation for
continual learning — is the continual-learning problem. He was hired to solve exactly this, and
it is the specific thing the post is bragging about.

**③ The moat is the corpus and the editors, not the recipe.** Every mechanism above is
published and reproducible. What is not reproducible: Westlaw, Practical Law, Checkpoint and
Reuters, **less than 10% of which has been used so far**, plus 174 years of bar-admitted
attorney editors. The reported numbers back this — best-in-class on instruction following
(0.914) and long context (0.753), strong on legal (LegalBench 0.823, Harvey Legal Agent 0.857),
but **coding 0.399**. This is not a frontier model that also does law. It is a professional-work
model, and the headline "competitive with Opus 4.8" is domain-scoped. Prediction **P12** bets
the technical report will show exactly that shape.

---

## 4. The people, mapped to mechanisms

Added to [`data/people.yml`](../../data/people.yml) under `eval-science`:

| Person | Owns |
|---|---|
| **Jonathan Richard Schwarz** — Head of AI Research, TR · ex-DeepMind | The stack's architecture: mixtures, selection, sparse experts, forgetting. Co-founded Safe Sign Technologies (acquired Aug 2024) — the acquisition **is** the pipeline's origin. |
| **Andrew M. Bean** — Evaluations Lead, LLM post-training · OII | Evaluation science: construct validity, contamination resistance, cheap eval subsets, shared schemas. |
| **Nabeel Seedat** — Cambridge (van der Schaar) · TR | Data-centric AI; agent verification (GLEAN: AUROC > 0.94, Brier < 0.10, 55.6% → 77.5% Best-of-N). |
| **Shengzhuang Chen** — TR | First author of **both** SIMoE and ADMIRE-BayesOpt — the two levers that make a general model professional. |
| **Yejin Bang** — TR · ex-HKUST CAiRE | Factuality/hallucination as distinct, separately-benchmarked problems. |
| **Fangyi Yu** — TR Labs | DeCE judging; principal hierarchies in legal reasoning. |
| **Stefan Winzeck** — TR | CapTrack coauthor — the forgetting measurement. |
| **Dietrich Trautmann** — TR Labs Zug | Groundedness measurement for legal QA. |
| **Daniele Giofré** — TR Labs Zug | BudgetLongformer: a SOTA long-context legal LM in **under 12 GPU-days**. The efficiency instinct that reappears as a $20M frontier-competitive model. |
| **Hannah Rose Kirk** — UK AISI · OII | PRISM lead author — pluralism as a measured distribution. |
| **Mihaela van der Schaar** — Cambridge | Lab lineage behind the verification methods. |

**Deliberately absent:** Kirsty Fielding and the tagged "Bradley B." — no findable technical
publications in this line. *No evidence ⇒ no entry.* **Alexander Kardos-Nyheim** — Safe Sign's
founding CEO (Cambridge law, ex-A&O Shearman trainee solicitor); a company fact, not a
mechanism, so he appears here and not in the knowledge base.

---

## 5. What FM-os built, not just described

[**`skills/eval-subset`**](../../skills/eval-subset/) — stage **E1** made runnable. Item-centric
evaluation-subset selection: pick benchmark items by their own difficulty signature, so **zero
seed-model runs** are needed, then predict full-benchmark scores with a stratified estimator.

Measured, 2,000-item benchmark · 100-item subset (5.0%) · 36 runs:

| selector | mean MAE | p90 MAE | selection cost |
|---|---|---|---|
| random | 0.0375 | 0.0452 | 0 model runs |
| **item-centric** | **0.0316** | **0.0363** | **0 model runs** |
| model-centric | 0.0326 | 0.0356 | **40 model runs** |

It matches the expensive selector for free. Three things make this an FM-os artifact rather
than a demo:

- **It gates on p90, not the mean.** You pick one subset and live with it; averaging over draws
  is a luxury you never get in production.
- **It shipped two honest failures.** The first two versions failed their own gate — one medoid
  per cluster (Bernoulli variance swamped the gain), then equal allocation across unequal
  clusters (destroyed effective sample size). Both are documented in the source. A gate that
  never fails is not a gate.
- **It carries a falsifier.** `test_uninformative_features_destroy_the_edge` drowns the item
  features in noise and asserts the advantage vanishes. A harness that wins on noise is
  measuring itself.

It is **not** a reproduction of Scales++ — that method embeds real item text with cognitive-scales
features. This tests the *claim structure* on a synthetic 2PL IRT benchmark where ground truth
is known. Stated in the skill, not buried.

Stage 3 (ADMIRE-BayesOpt) needs no new tooling: FM-os already ships
[`bayesopt-loop`](../../skills/bayesopt-loop/) and [`labs/merge-bo`](../../labs/merge-bo/). Same
machinery, pointed at data mixtures instead of molecules — depth, not width.

---

## 6. Community — join one, don't found one

The research theme already has a community artifact, and Bean is inside it: **Every Eval Ever**
([arXiv:2606.14516](https://arxiv.org/abs/2606.14516) · [GitHub](https://github.com/evaleval/every_eval_ever)
· [HF](https://huggingface.co/evaleval)) — a community-governed schema for evaluation results,
converters from popular harnesses, and a crowdsourced database spanning 22,235 models, 2,273
benchmarks, 31 formats.

FM-os produces exactly the artifact that schema exists to hold: certified skills with measured
eval results (`vlm-failure-probe`'s multi-model probe runs, `eval-subset`'s selector comparison,
RewardForge's DPO deltas). Emitting those in EEE format is a real contribution to a real
community with a named front door — and it is the *reciprocal* of this case study, which took
from their work. **Open, not done:** nothing has been submitted yet.

The distinction worth keeping: a Discord is an audience; a shared schema is a community. Only
one of them compounds.

---

## 7. The prediction ledger

12 claims registered **2026-08-13**, resolving by 2026-12-31 against the technical report.
Full text and resolution criteria: [`data/predictions.yml`](../../data/predictions.yml).

| id | claim (abbreviated) | P |
|---|---|---|
| P4 | Preference optimization applied after SFT | 0.90 |
| P1 | Base model is Qwen-family | 0.85 |
| P12 | Opus-4.8 parity holds on professional axes, **not** on coding | 0.80 |
| P11 | Data mixture is optimized/searched, not hand-set | 0.75 |
| P3 | Forgetting reported with a capability-decomposed metric | 0.70 |
| P9 | Agentic RL with programmatic rewards over TR corpora | 0.70 |
| P8 | Report contains a contamination analysis | 0.65 |
| P6 | Decomposed criteria-based judge, not only pointwise | 0.60 |
| P2 | Specialization uses sparse/MoE expert subsets (SIMoE) | 0.55 |
| P5 | Pluralism = explicit principal hierarchy, not just representative preferences | 0.50 |
| P7 | Cheap eval-subset method used inside the training loop | 0.45 |
| P10 | A no-retrain content-update mechanism is described | 0.40 |

The ledger is deliberately mixed. **P4 at 0.90 and P12 at 0.80 are nearly free** — they are
recorded precisely so the easy/hard mix stays visible, because a ledger of only bold calls is
one someone curated. **P5 sits at exactly 0.50** because the evidence genuinely does not decide
it: this team owns both readings of "pluralism", and we have no basis to prefer one. A ledger
with no coin-flips is a ledger that was tuned after the fact.

Rules the gate enforces: probabilities strictly between 0 and 1 (certainty is not a forecast);
an outcome may only be set with a `resolved_by` citation; and an unresolved prediction is
**excluded** from the Brier score, never counted as a win.

---

## 8. Honest flags

- **The Qwen 3.5 397B detail is single-sourced** to Bean's post. Thomson Reuters' own materials
  say only "open source LLMs". P1 carries that uncertainty at 0.85.
- **Stage ordering is our reconstruction.** Each mechanism is published; the sequence is
  inferred from what the mechanisms require of each other. The report may reveal a different order.
- **No stage is confirmed to be *in* Thomson-1.** These are the team's published methods. A team
  publishing a method does not prove they shipped it. That gap is what the ledger measures.
- **"Competitive with Opus 4.8" is a vendor claim on vendor-selected benchmarks.** Independent
  replication does not exist. Bean's own NeurIPS 2025 paper — 445 benchmarks, most failing
  construct validity — is the reason to hold even a well-intentioned number loosely.
- **The `eval-subset` numbers are synthetic-benchmark numbers.** They show the mechanism is
  sound. They are not evidence about real benchmarks.
- **Nothing has been contributed to Every Eval Ever yet.** §6 describes an intent, and is marked
  as such.

---

## 9. How this stays alive

```bash
make thomson          # validate the stack + score the ledger
make check            # the above, inside CI's finish line
python3 skills/eval-subset/reference/subset.py    # reproduce the E1 result
```

When the technical report lands: set `outcome` and `resolved_by` on each prediction in
`data/predictions.yml`, run `make thomson --score`, and the Brier score says whether reading a
research team through its publications actually works. That number — not this document — is the
deliverable.
