# labs/ — applied proof-of-capability builds

Hands-on labs that put the FM-os skills to work on a concrete target. Each is self-contained,
test-gated, and built from public surfaces only.

| Lab | What it proves | Gates |
|---|---|---|
| [`nomadicml/`](nomadicml/) | Clean-room, small-scale reverse-engineering of NomadicML's VLM video-analysis product (driving events → structured schema → semantic search), compared term-by-term against their production API. Interview proof-of-capability for a Member-of-Technical-Staff (ML) role. **Live demo (password-gated):** https://nomadic-mini-demo.vercel.app | `make check` (offline) · `make e2e` (real VLM) · `make parity` (live API) · `make webapp` (visual demo + lab copilot) |
| [`merge-bo/`](merge-bo/) | A from-scratch **closed-loop Bayesian optimization** backbone (GP surrogate + EI/UCB/constrained-EI/EHVI acquisition + DBTL loop over a molecular library), with constrained and multi-objective variants and an optional BoTorch adapter. Proves the [Merge Labs](https://jobs.ashbyhq.com/Merge%20Labs/a8440ed8-9e11-4861-8413-fc23e2213790) *ML Research Scientist — Bayesian Optimization* tasks: **BO finds ~51% better candidates and cuts regret ~71%** vs random search at equal experimental budget. | `make check` (offline pytest) · `make e2e` (regenerate RESULTS.md) · `make botorch` (real BoTorch stack) |
