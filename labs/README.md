# labs/ — applied proof-of-capability builds

Hands-on labs that put the FM-os skills to work on a concrete target.

> These labs are probes of ONE research program — *eval gates as training-signal
> factories* — with homes chosen for depth over width: see
> [docs/research/RESEARCH-PROGRAM.md](../docs/research/RESEARCH-PROGRAM.md)
> (P2 lives at [mcp-arena](https://github.com/wjlgatech/mcp-arena), P3 in super-u). Each is self-contained,
test-gated, and built from public surfaces only.

| Lab | What it proves | Gates |
|---|---|---|
| [`nomadicml/`](nomadicml/) | Clean-room, small-scale reverse-engineering of NomadicML's VLM video-analysis product (driving events → structured schema → semantic search), compared term-by-term against their production API. Interview proof-of-capability for a Member-of-Technical-Staff (ML) role. **Live demo (password-gated):** https://nomadic-mini-demo.vercel.app | `make check` (offline) · `make e2e` (real VLM) · `make parity` (live API) · `make webapp` (visual demo + lab copilot) |
| [`rewardforge/`](rewardforge/) | **Eval failures → preference data → a real gated fine-tune**: chosen/rejected pairs labeled by FM-os's own certified gates (syndata-bare alignment, vlm-failure-probe), a from-scratch DPO loss (torch+peft, unit-tested math), LoRA on SmolLM2-135M, and a held-out grounding gate (zero word overlap with training — leakage is a tested property) that SHIPS or ROLLS BACK the tune. The "evals → training data → reward signals" bridge the OpenAI Personal AGI JDs name. **M2 (multi-seed + shuffled-pair ablation): complete arm separation (all treatment +0.048..+0.110, all controls ≤0) but one seed missed the pre-registered floor by 0.002 — verdict honestly NO-EFFECT per pre-registration ([out/M2-RESULTS.md](rewardforge/out/M2-RESULTS.md)).** | `make check` (offline, 8 tests) · `make e2e` (real fine-tune) · `python -m rewardforge.sweep` (M2) |
| [`merge-bo/`](merge-bo/) | A from-scratch **closed-loop Bayesian optimization** backbone (GP surrogate + EI/UCB/constrained-EI/EHVI acquisition + DBTL loop over a molecular library), with constrained and multi-objective variants and an optional BoTorch adapter. Proves the [Merge Labs](https://jobs.ashbyhq.com/Merge%20Labs/a8440ed8-9e11-4861-8413-fc23e2213790) *ML Research Scientist — Bayesian Optimization* tasks: **BO finds ~51% better candidates and cuts regret ~71%** vs random search at equal experimental budget. | `make check` (offline pytest) · `make e2e` (regenerate RESULTS.md) · `make botorch` (real BoTorch stack) |
