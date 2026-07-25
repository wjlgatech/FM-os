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
| [`skills/vlm-failure-probe`](../../skills/vlm-failure-probe/) | VSS §IV–XI: the failure taxonomy **as data** (`probe_spec.yml`, one probe per observed failure in the paper), a runner that scores any pipeline exposed as `answer(probe)`, and a blocking gate that cannot pass on unmeasured modes. The benchmark becomes a CI regression gate, and Table/Results sections can be generated from the spec. | `python reference/probe_runner.py` — the paper's failures are all caught (baseline fails 5/5 modes), a grounded model passes |
| [`skills/syndata-bare`](../../skills/syndata-bare/) | syndata §III–IV: BARE-VLM as a **closed loop with twin gates** — alignment floor (mock-CLIP, swap in real CLIP) catches base-model hallucination; diversity floor (pairwise Jaccard) catches instruct-model mode collapse. The paper's central thesis becomes a falsifiable assertion: BARE must beat both single-stage baselines at equal budget and seed. | `python reference/bare_loop.py` — base fails alignment (0.88), instruct fails diversity (0.00), BARE passes both at 100% yield |
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
- **"Temporal Grounding Score" (VSS §X) is undefined** — a custom metric needs a formula and a
  fixture test before results are computed against it (the `agentic-eval` gate-math pattern).
- **Prompt-sensitivity findings are anecdotal n=1 observations** ("MAKE SURE TO ANSWER ALL
  QUESTIONS" fixed one video) — the probe suite turns each anecdote into a repeated, scored
  probe across the dataset.
- **BARE-VLM refinement can homogenize** (the paper acknowledges this) — the diversity floor in
  `syndata-bare` is the guard; report diversity *after* refinement, not just before.

## Provenance

Papers: `research-anything/case-studies/extracted/{VSS_Benchmark,BARE_Video}.txt` ·
BARE original: Zhu et al., arXiv:2502.01697 · registry entries: `data/registry.yml`
(`vlm-failure-probe`, `syndata-bare`) — certified by `make certify`, gated by `make check`.
