# Interview Evidence Pack — Member of Technical Staff, ML @ NomadicML

Every JD line mapped to an artifact you can open, run, or demo. Gaps are named, not hidden.
(JD source: Ashby posting, captured 2026-07-21. Company: VLMs as "hydraulic mining" for
driving/robotics video; founders Mustafa Bal — ONNX Runtime/DeepSpeed contributor — and
Varun Krishnan; $8.4M seed 2026-03.)

## 1. Responsibilities → evidence

| JD says | Your proof | Where |
|---|---|---|
| "Train and evaluate VLMs specialized for motion understanding" | `vlm-quickstart` skill: open-VLM fine-tuning (LoRA/QLoRA) on video + sensor metadata for motion understanding, with spatiotemporal eval | `FM-os/skills/vlm-quickstart` |
| "Design and scale GPU-accelerated pipelines … multi-modal data" | `slm-quickstart` (train→quantize→serve) + honest gap: no multi-node distributed-training war story — say so, then discuss DeepSpeed ZeRO stages concretely (founder is a DeepSpeed contributor; do NOT bluff here) | `FM-os/skills/slm-quickstart` + study plan §4 |
| "Build agentic evaluation frameworks that benchmark spatiotemporal reasoning, localization accuracy, narrative consistency" | **Two exhibits**: (a) `agentic-eval` skill — exactly this, verbatim; (b) the **parity harness built here**: benchmarks a clean-room clone against their production API term-by-term | `FM-os/skills/agentic-eval`; `labs/nomadicml/nomadic_mini/tests/test_parity_live.py` |
| "Develop and productionize curation loops … 'AI training AI'" | `curation-loop` skill: model labels/generates/refines its own video dataset behind quality+safety gates → feeds fine-tuning. Their product version: approve/reject events → `create_agent`/`update_agent` (`prompt_optimization`\|`finetuning`) — you can discuss their actual mechanism from SDK source | `FM-os/skills/curation-loop`; `recon/SDK-SURFACE.md` §2e |
| "Publish high-impact research … while shipping features" | `research-loop` skill (falsifiable-hypothesis discipline) + FM-os build-in-public flywheel | `FM-os/skills/research-loop` |

## 2. Qualifications → evidence

| JD says | Your proof |
|---|---|
| Python, PyTorch, large-scale ML workflows | FM-os certified skills (94→98 certification loop in repo history); `nomadic_mini` built and gated in a day |
| Research experience in foundation models / VLMs / multi-modal | FM-os knowledge base + skills are SLM/VLM-first by design |
| Iterate quickly and autonomously, end-to-end | **This lab**: JD → recon → working clone → parity harness in one session, every step gated (`make check` / `e2e` / `parity`) |
| Training/fine-tuning on video or sensor data | `vlm-quickstart` (video+sensor LoRA); honest gap: no petabyte-scale AV dataset experience — counter with their own funnel (analyze → search → re-analyze) which you've mapped |
| Retrieval systems, embeddings, GPU optimization | `vector-rag` skill (CLIP/SigLIP video RAG over FAISS/Milvus/Qdrant/LanceDB) + `nomadic_mini/search.py` mirroring their `{summary, thoughts, matches}` search contract |
| Nice-to-have: vector DBs, distributed training, Ray/Kubeflow/MLflow, AV/robotics datasets | vector DBs ✅ (`vector-rag`); AV datasets: their public showcases (BDD100K, nuReasoning, DROID, ArmBench, VIRAT) are now familiar ground via `recon/EXAMPLES.md`; distributed training = named gap |

## 3. The demo (5 minutes)

1. **Open `recon/EXAMPLES.md`** (30s): "I recovered all 20 of your public examples from your
   site bundle — here's your Driving Violations demo: CVC 21703 + CVC 22450(a)."
2. **Run `make check`** (30s): 12 offline tests pin my event model to your SDK's verbatim
   `RapidReviewEvent` fields — including the `type/description` ↔ `category/aiAnalysis`
   duality between your docs and your SDK.
3. **Show `out/RESULTS.md`** (2m): your three automotive example queries, verbatim, run through
   my small-scale pipeline on my own CC-licensed clips — structured events in your schema, then
   semantic search over them mirroring your `{summary, thoughts, matches}` contract.
4. **Open `tests/test_parity_live.py`** (1.5m): "This is an agentic eval framework — JD bullet 3.
   It uploads the same clip to api-prod.nomadicml.com, runs the same query on your side and mine,
   and diffs the surfaces field by field. It skips honestly without a key; with one, it's live."
5. **Close** (30s): "Built from public docs and your published SDK only — clean-room. What I'd do
   in week 1: point the curation loop at the events my clone disagrees with yours on — those
   disagreements are exactly the edge cases worth mining."

## 4. Gaps + study plan (say these before they ask)

1. **Distributed training at scale** (DeepSpeed/ZeRO, multi-node) — founder's home turf.
   Prep: re-run `vlm-quickstart` fine-tune with DeepSpeed ZeRO-2/3 configs; be fluent in
   ZeRO stages, gradient checkpointing, sequence parallelism for video-token streams.
2. **Video tokenization economics** — frames/second vs token budget vs localization accuracy;
   why ms-precision action segmentation (their Franka demo: 37 events at ms precision) likely
   needs sensor fusion (joint telemetry), not pure vision. You can point at their own excavator
   example: "segmented from joint-angle trajectory."
3. **Their eval question, reversed**: how do THEY benchmark Nomadic-VL-XLarge? Blog posts
   `action-segmentation-benchmark` (2026-07-08) and `av-motion-eval` — read before interview.
4. **Publication story**: NeurIPS/CVPR ambition in JD — bring one concrete paper idea
   (e.g., agentic parity-testing of video-understanding APIs as an eval methodology).

## 5. Likely technical questions → grounded answers

- *"How would you evaluate localization accuracy of a VLM on video?"* → temporal IoU per event
  vs human-labeled spans + narrative-consistency LLM-judge; regression-gate in CI
  (`agentic-eval` skill implements this shape; parity harness demonstrates the API-level analog).
- *"Our events need MM:SS precision at fleet scale — how do you keep costs sane?"* → two-tier
  routing (their own fast/thinking split proves this): cheap pass to shortlist, thinking pass to
  localize; embedding search (`haystack_search` in their SDK) to avoid re-analyzing.
- *"How do you stop 'AI training AI' from collapsing?"* → approval gates (their
  approved/rejected/pending/invalid vocabulary), held-out human-labeled eval that never enters
  training, and drift alarms — `curation-loop` skill encodes exactly this.
- *"What did you find in our SDK you'd fix?"* → honest, specific: stale App Runner URL in a
  shipped test, dead `test.py` module in the wheel, docs/SDK field-name divergence
  (`type/description` vs `category/aiAnalysis`), `pip install nomadic` vs `nomadicml` naming
  quirk. (Deliver as an engineer, not a critic.)
- **Measured live** (free-trial key, 2026-07-21 — see COMPARISON.md §4b): docs say auth is
  Bearer *or* `X-API-Key`, but Bearer-only gets parsed as a Firebase ID token on GET endpoints
  and fails — which is exactly why their SDK sends both headers unconditionally; `/api/keys/verify`
  returns `{valid, key_id, user_id, scope, expires_at}`, not the documented
  `{valid, user_id, uid, email, org_id}`; API upload is 402-paywalled on trial (undocumented).
  These prove the comparison ran against production, not just against paper.

## 6. Provenance / ethics line (if asked how you did this)

"Public surfaces only: your PyPI wheel, your docs' llms.txt, and the example data your own site
ships in its JS bundle. No auth walls crossed, no scraping of gated content; the live-API tests
use my own key against my own uploads. Clean-room reconstruction — which is also why the parity
harness matters: it proves fidelity by test, not by copying."
