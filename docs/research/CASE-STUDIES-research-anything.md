# FM-os × research-anything — what FM-os uniquely contributes to the two VLM case studies

Two draft papers live in `research-anything/case-studies/` (Overleaf: [VSS](https://www.overleaf.com/project/6851f17b4f1e4ca645ef4827) ·
[syndata](https://www.overleaf.com/project/6851f18fef84747e5315dd63); extracted text under
`case-studies/extracted/`):

1. **VSS** — *Failure Benchmarking of NVIDIA's VSS Tool: Insights from Vision-Language
   Evaluation* (Shah, Hosseini, Shahab — Accenture Center for Advanced AI). A failure taxonomy
   (spatial/directional, temporal cross-chunk, multi-part prompts, retrieval reranking,
   grounding hallucination) plus a proposed vDPO mitigation.
2. **syndata** — *Adapting the BARE Framework for Synthetic Data Generation in Vision-Language
   Models* (same authors). Base-VLM drafts for diversity, instruction-tuned refinement for
   correctness, CLIP-based validation.

FM-os's unique contribution is not another literature take — it is the **gate disciplines made
runnable**: spec-as-data, no-evidence⇒No, eval-with-teeth, mitigation-must-move-a-measured-score.
Both papers are strong on taxonomy/design and thin on executable evidence (most experimental
sections are still TODO); the tooling below closes exactly that gap.

## The tooling shipped for these papers

| Tool | What it gives each paper | Proof |
|---|---|---|
| [`skills/vlm-failure-probe`](../../skills/vlm-failure-probe/) | VSS §IV–XI: the failure taxonomy **as data** (`probe_spec.yml`, one probe per observed failure in the paper), deterministic synthetic stimuli for every probe (`stimuli.py` — the paper's own methodology, as code), a runner that scores any pipeline exposed as `answer(probe)`, and a blocking gate that cannot pass on unmeasured modes. The benchmark becomes a CI regression gate, and the Results section generates from a run: `run_real.py` emits `out/RESULTS.md` + a paste-ready `out/vss_results_table.tex`. | **Measured live (multi-model, 2026-07-31):** baseline VSS fails 5/5 modes; claude-opus-5 and claude-sonnet-5 pass 5/5; **claude-haiku-4.5 fails 3/5** (temporal 0.67, multipart 0.58, retrieval 0.00 — e.g. it reads the rising fork as 'moving down') — the failure profile is capability-dependent, not only architectural (raw answers in `reference/out/RESULTS.md`) |
| [`skills/syndata-bare`](../../skills/syndata-bare/) | syndata §III–IV: BARE-VLM as a **closed loop with twin gates** — alignment floor (mock-CLIP, swap in real CLIP) catches base-model hallucination; diversity floor (pairwise Jaccard) catches instruct-model mode collapse. The paper's central thesis becomes a falsifiable assertion: BARE must beat both single-stage baselines at equal budget and seed. | `python reference/bare_loop.py` — base fails alignment (0.88), instruct fails diversity (0.00), BARE passes both at 100% yield. **Live (2026-08-14):** `reference/run_real.py` over real vision models — mode collapse reproduced (0.23 vs 0.62), base-role hallucination did **not**, so the pipeline claim is NOT SUBSTANTIATED at this difficulty; see the headline below |
| [`skills/research-loop`](../../skills/research-loop/) (existing) | Both papers' experiment sections: pre-registered thresholds, ≥3 seeds with variance, ablations, adversarial critique, repro command — the write-up gate for every TODO results section. | rubric enforced by the skill itself |
| [`skills/agentic-eval`](../../skills/agentic-eval/) (existing) | VSS §X: wiring standard video benchmarks (Video-MME, MMBench-Video) alongside the custom probes, LLM-as-judge for narrative consistency, per-axis CI gates. | see skill |
| [`skills/vlm-quickstart`](../../skills/vlm-quickstart/) (existing) | syndata §IV: fine-tune an open VLM on the BARE-generated data and assert no regression vs. base on a held-out benchmark — the downstream-utility experiment the paper plans. | see skill |

**The pipeline the two papers form together** (each stage gated):

```
syndata-bare  →  vlm-quickstart  →  vlm-failure-probe + agentic-eval  →  research-loop
(generate gated data)  (train on it)   (probe the failure taxonomy)      (write it up honestly)
```

The syndata paper *generates* the diverse probe videos/pairs the VSS paper's benchmark needs
(warehouse, sports, synthetic geometric scenes); the VSS paper's taxonomy defines the failure
axes the syndata paper's downstream evaluation should probe. FM-os supplies the connective
tissue: one gate discipline across both.

## Honest flags (research-loop's adversarial-critique stage, applied)

These are the claims a reviewer will attack first; each maps to a concrete next experiment:

- **The 0.92 temporal-coherence / vDPO claims** (both abstracts) currently have no documented
  experimental setup in the drafts — no dataset partition spec, seed count, variance, or
  baseline-comparison protocol. Until the vDPO run is pre-registered and reproducible, treat
  0.92 as a placeholder, not a result. `research-loop` stages 2–6 are the recipe;
  `vlm-failure-probe`'s baseline-vs-patched scorecard is the reporting format.
- ~~**"Temporal Grounding Score" (VSS §X) is undefined**~~ — **CLOSED 2026-07-31.** The paper names
  the metric ("a custom metric that quantifies the model's ability to correctly interpret and
  respond to temporal cues … sequencing of events, time-based references") and then reports against
  it in a §XI that is still `TODO` — a name with no formula, so no number computed from it can be
  checked. Now defined in [`skills/vlm-failure-probe/reference/tgs_spec.yml`](../../skills/vlm-failure-probe/reference/tgs_spec.yml):
  `TGS = Σ wᶜ·sᶜ / Σ wᶜ` over three components mapped 1:1 to the paper's own prose — **order**
  ("sequencing of events"), **anchor** ("time-based references"), **persistence** (the §VII
  cross-chunk drift failures) — weights as data so a reviewer can disagree with the number by
  disagreeing with a line of YAML. Unmeasured components are excluded and the weights renormalize
  (never zeroed = a fake failure; never assumed = a fake pass), and a required-but-unmeasured
  component makes TGS **undefined** and the gate unpassable. Arithmetic pinned to hand computation
  in `test_tgs.py` (10 tests); it discriminates — the paper's observed baseline scores **TGS 0.000**,
  a grounded model **1.000**.
- **Prompt-sensitivity findings are anecdotal n=1 observations** ("MAKE SURE TO ANSWER ALL
  QUESTIONS" fixed one video) — the probe suite turns each anecdote into a repeated, scored
  probe across the dataset.
- **BARE-VLM refinement can homogenize** (the paper acknowledges this) — the diversity floor in
  `syndata-bare` is the guard; report diversity *after* refinement, not just before.
- ~~**Proxy stimuli can under-credit weaker models**~~ — **SETTLED 2026-07-31 by measurement, and
  the answer reversed a published claim.** The suspicion was correct and larger than suspected. A
  per-probe audit of haiku-4.5's raw answers (pre-registered in `probe_spec.yml`'s audit log and
  committed *before* the re-run) found **3 of its 5 apparent failures were OUR grader's fault**:
  the 2D tennis proxy genuinely read as a soccer pitch (green field, halfway band, orange-ish
  ball → fixed with service boxes, a posted mesh net, strung rackets, a yellow-green ball); the
  compound-prompt probe demanded the literal token "white" when the model had identified the near
  player *positionally*; and "the truck disappears off the right side of the screen" was not in the
  alias list for "leaves". Every pre-registered per-probe prediction held: **haiku went from
  FAIL(3 modes) to PASS on all 5**, leaving exactly **one** real, unambiguous failure — it reads the
  provably rising forklift fork as descending — plus one genuine compound-prompt miss (it never
  gave the summary). So the earlier "capability ladder" framing overstated a grader artifact as
  architecture: the honest claim is *one* capability-dependent failure mode, not three — and under
  3 repeats even that one turns out to be **stochastic** (haiku answers the fork direction
  down/up/up; ~2/3 correct), so it is a real but intermittent failure, not a deterministic one.
  Rule, upgraded: when tiers disagree, audit the stimulus AND the matcher per probe **before**
  publishing — and pre-register the fix so the correction cannot become goalpost-moving.
- **An absent answer is not a wrong answer** (found 2026-07-31 by the variance run, not by
  reasoning): the adapter joined a response's text blocks and returned `""` when there were none
  (all tokens spent on a non-text block, a bare refusal). `""` is not `None`, so it scored **0.0**
  and was reported as a model failure the model never committed — including one `claude-opus-5`
  gate FAIL. This is the exact mirror of the fake *pass* the no-evidence⇒No rule guards against,
  and it is invisible unless you read raw answers: a wrong answer and an absent one look identical
  in a score table. Any paper computing fuzzy-match metrics over API responses has this exposure.
  Empty now returns "not measured" and logs `stop_reason` + block types; regression-tested.
- **Graders fail before models do** (lesson from the live run): the first live pass scored
  claude-sonnet-5 at 0.58 on multi-part prompts — but the raw answers showed every sub-question
  answered; the misses were stimulus/matcher artifacts (a drawn vest read as a "yellow shirt",
  a 2D court read as ping-pong). Expectations must grade the failure mode's *intent*
  (compound-prompt completeness), not incidental scene naming. Always read raw answers before
  reporting a failure — the paper's fuzzy-matching metrics need the same audit.

**syndata-bare goes live — and returns an honest null (2026-08-14, 18 captions per pipeline,
base role `claude-haiku-4-5` @ T=1.0, instruct `claude-sonnet-5`, six deterministic scenes):**
the asymmetry that let the VSS paper carry measurements while the BARE paper carried a
hypothesis is closed — `skills/syndata-bare/reference/run_real.py` is the counterpart of
`vlm-failure-probe`'s runner, emitting `bare_results_table.tex` the same way.

| pipeline | alignment | diversity | yield | gate |
|---|---|---|---|---|
| base_only | 1.00 | 0.62 | 1.00 | PASS |
| instruct_only | 1.00 | 0.23 | 1.00 | **FAIL** — mode collapse |
| bare | 1.00 | 0.56 | 1.00 | PASS |

**Half the thesis reproduced; half had no headroom.** Mode collapse is real and large (0.23 vs
0.62, below the 0.25 floor). The base role did not hallucinate once across 18 captions. The
stimuli were **not** made harder until it passed — tuning a benchmark until it agrees with you is
exactly how the 0.92 in the draft paper happened.

> ⚠️ **Correction, same day — that verdict was wrong.** The runner reported the pipeline claim
> **NOT SUBSTANTIATED**. By the rule of three (Hanley & Lippman-Hand, JAMA 1983), 0 events in 18
> trials puts the 95% CI for the true rate at **[0, 16.7%]**, which cannot exclude the **4.62%**
> hallucination rate independently published for the very model used — where P(zero in 18) ≈
> **0.43**. The honest verdict was never "false"; it was **UNDERPOWERED**. The runner now
> computes this and returns a third outcome, `INCONCLUSIVE`, with its own exit code. Full
> four-window audit: [`POWER-AND-THE-ZERO-NUMERATOR.md`](POWER-AND-THE-ZERO-NUMERATOR.md).

Two refusals are enforced in code, not prose. **Role fidelity:** every Anthropic model is
instruction-tuned, so it fills the base *role* but is not a base *model*; a run stamps `proxy`
and the *paper claim* (base-vs-instruct) can never be marked substantiated — the emitted LaTeX
caption says so inside the table. **Metric asymmetry:** only closed-vocabulary decoys can be
scored wrong, and high-entropy captions route around that vocabulary entirely ("crimson",
"cobalt", "orbs" — observed live), so alignment is a weaker bound for the base role than for the
instruct role, *in the direction that flatters the base role*.

A third finding came from the API itself: `claude-sonnet-5` **rejects `temperature` outright**,
which silently zeroed the entire instruct role on the first run (18 captions, all "not
measured"). The runner now retries without it and stamps the artifact, because "matched budget"
is a claim it makes and an unapplied temperature quietly voids it.

**BARE/RewardForge headline (2026-07-31, 5 seeds):** preference pairs labeled by an
independent eval gate carry real training signal — treatment **+0.098 ± 0.028** held-out
hallucination reduction vs shuffled-label control **−0.046 ± 0.055**, complete arm separation,
under a median+separation criterion **committed to git before the run** (`91981e2`). The
stricter every-seed floor still reads NO-EFFECT on one seed; both verdicts ship together.
Evidence: [`labs/rewardforge/out/M2-RESULTS.md`](../../labs/rewardforge/out/M2-RESULTS.md).

**The measurement finding that supersedes every single-run number here (2026-07-31, 3 repeats ×
3 models × 12 probes = 108 live probes per run, four runs):** *a single-run score from this
benchmark — or from the papers' fuzzy-matching metrics — is not a measurement.* Repeating the
identical, deterministic stimulus moved scores enough to flip **gate verdicts**, and the set of
unstable probes differed between runs. Every instability traced to one of four causes, and only the
last is a property of the model:

| cause | what it looked like | fixed? |
|---|---|---|
| **empty response scored 0.0** | no text block (all 200 tokens spent on a `thinking` block) → `""` → graded as a wrong answer; caused one `claude-opus-5` gate FAIL | yes — now *not measured*, with `stop_reason` logged |
| **truncated response graded as complete** | answer cut off mid-word (`"…A yellow short"`), missing tail scored as a missing sub-answer | yes — truncation ⇒ *not measured*; budget 200 → 400 |
| **grader alias gaps** | "the truck **disappears off the right side**" not in the aliases for *leaves*; "**volleyball**… two **teams**" not matched by `rally\|ball\|players` | partly — the diagnosed remainder is pre-registered for v0.4, deliberately unpatched |
| **genuine model nondeterminism** | haiku answers the provably rising fork *down/up/up*; sonnet calls the same drawn vehicle a "truck" then a "car-like vehicle" | not fixable — this is the signal, and it is why variance must be reported |

Fixing the two harness bugs cut instability from **5 unstable probe/model pairs to 2**; applying the
pre-registered v0.4 fix then cut it to **1**. That v0.4 prediction was made in git BEFORE its run and
**CONFIRMED**: `end_of_video` went sd 0.471 → **0.000** on all three tiers once the expectation
accepted any vehicle noun (sonnet had described the exit correctly 3/3 while once calling the drawn
truck a "car-like vehicle"). The single survivor is model-side: haiku sometimes omits the summary
half of the compound prompt. **The pre-registered prediction was FALSIFIED** — `summary_count_clothing`
did *not* reach sd = 0.00 under the phrasing-invariance fix (opus 1.00/1.00/0.67). The
pre-registered fallback was "then keyword matching cannot grade compound-prompt completeness and it
needs an LLM judge"; the raw answers instead showed **truncation** as the cause, so that fallback is
recorded as *not adopted* — with the caveat stated plainly, since a reviewer may fairly hold the
stricter pre-registered reading. Evidence, including the two superseded buggy runs kept verbatim:
[`skills/vlm-failure-probe/reference/out/`](../../skills/vlm-failure-probe/reference/out/)
(`RESULTS.md`, `RESULTS-v0.1-spec.md`, `RESULTS-v0.3-run1-emptybug.md`,
`RESULTS-v0.3-run2-truncbug.md`, `raw_answers.json`).

**Consequence for the VSS paper (needs a human call):** TABLE I in the Overleaf currently reports
the single-run v0.1 numbers, where haiku-4.5 fails 3/5 modes. Under the audited spec all three
tiers **PASS 5/5** (headline column = repeat 1; 3-repeat means are in the stability table), and TGS
is opus **1.000** / sonnet **1.000** / haiku **0.833** vs the observed VSS baseline **0.000**. The
table and its "capability ladder" subsection need replacing — it is a co-authored paper, so that
edit is flagged here rather than made unilaterally.

**Headline live result (2026-07-25):** on the exact probes VSS fails 5/5, a frontier VLM
(claude-sonnet-5, 6 frames per stimulus) passes 5/5 at 1.00 — evidence that the paper's failure
modes are *architectural* (chunking, late fusion, retrieval) rather than intrinsic to current
VLMs, which strengthens its core argument. `reference/out/vss_results_table.tex` is paste-ready
for the empty Results section.

## Provenance

Papers: `research-anything/case-studies/extracted/{VSS_Benchmark,BARE_Video}.txt` ·
BARE original: Zhu et al., arXiv:2502.01697 · registry entries: `data/registry.yml`
(`vlm-failure-probe`, `syndata-bare`) — certified by `make certify`, gated by `make check`.
