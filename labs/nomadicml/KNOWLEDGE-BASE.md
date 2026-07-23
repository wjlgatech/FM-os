# NomadicML — cofounder-grade knowledge base

The single knowledge base behind the interview: the reverse-engineering project (what/why/when/
where/how) + deep technical answers with **real numbers** and a **15-yo mental model** each. Written
for Paul to speak as a **cofounding technical staff / peer engineer who owns outcomes** — not an
applicant seeking approval. Feeds three surfaces: the demo copilot (`_knowledge.txt`), loop's RAG
(`knowledge.db`), and loop's live `playbook.md`.

---

## PART A — the reverse-engineering project, 5W1H

**WHAT.** A clean-room, small-scale reconstruction of NomadicML's video-understanding product:
`video → VLM → structured motion events (their verbatim schema) → semantic search`, plus a
**term-by-term parity harness** that diffs the clone against their production API, and a public,
password-gated demo (upload a clip → 1-click analyze → real progress → events on a timeline) with
an embedded copilot. Live: nomadic-mini-demo.vercel.app · /system.html (animated design).

**WHY.** To prove capability by construction, not by claim. A cofounder hires for judgment and
ownership; the fastest proof is to rebuild their loop and show where my version and theirs *agree
and disagree*. The parity harness is itself the JD's "agentic evaluation framework" — I didn't just
describe one, I pointed one at their product.

**WHEN.** Built in days (2026-07), single-person, every step test-gated. Deliberately time-boxed to
"small scale" to prove the *shape* is right before spending on fleet scale.

**WHERE.** Public surfaces only — their published PyPI SDK (`nomadicml` wheel), their docs
`llms.txt`, the example data shipped in their site's JS bundle, and live calls to `api-prod.
nomadicml.com` with my own key against my own uploads. No auth walls crossed; probing stopped at
their authorization boundaries.

**HOW.** Recon (read the wheel source + docs) → mirror the event schema verbatim → implement the
pipeline with a swappable VLM backend (Gemini native video; Claude-frames fallback) → gate with
`make check` (16 offline schema/search tests) / `make e2e` (real VLM) / `make parity` (live vs prod)
→ ship a deployed demo with a real serverless backend.

**Cofounder stance:** I treat this as *our* problem — "how do we make understanding cheaper and
more trustworthy at fleet scale," not "please evaluate me." I disagree where I see a better path and
say why.

---

## PART B — measured live findings (proof it hit production, not paper)
- `POST /api/keys/verify` returns `{valid, key_id, user_id, scope, expires_at}` — NOT the documented
  `{valid, user_id, uid, email, org_id}`.
- Bearer-only auth fails on GET endpoints (parsed as a Firebase ID token) — which is why their SDK
  sends BOTH `Authorization: Bearer` and `X-API-Key`.
- `POST /api/upload-video` returns HTTP **402** on the free trial (undocumented paywall).
- Their public demo batches return `Access denied` to an outside key (correct org-scoping).

---

## PART C — deep technical answers (numbers + mental model)

### C1. Fine-tuning a VLM for motion understanding
A video-VLM = **vision encoder** (ViT/SigLIP) → **connector/projector** → **LLM decoder**. For
motion (turns, lane changes) the signal lives in *cross-frame temporal attention*, not per-frame
appearance. So **freeze the vision encoder** (it already sees cars), **train the connector + LoRA
adapters on the LLM's attention** (rank 16–64, ~0.1–1% of params), and add **temporal position
encodings** (M-RoPE / absolute-time tokens). Full fine-tune only if you have the data + GPUs;
LoRA first for iteration speed. Trade-off: freezing the encoder saves memory/compute but caps you
if the encoder itself misses fine motion cues — then you unfreeze its top blocks.
🧠 *Mental model:* tutoring a kid who knows every car by sight but never watched a movie — don't
re-teach "what a car is," teach him to follow the plot across frames.

### C2. Spatiotemporal localization eval (design the metric)
Don't say "accuracy." Events are **time intervals**, so score **temporal IoU** =
(overlap of predicted vs ground-truth span) / (their union). Sweep thresholds (tIoU ≥ 0.3/0.5/0.7),
compute **mAP@tIoU** like ActivityNet/THUMOS action detection. Add a **start/end offset bias**
diagnostic (are we systematically early/late?) and handle **multi-event clips** with Hungarian
matching of predictions to GT, penalizing unmatched (false positives / missed). Narrative accuracy
is separate (see C8).
🧠 *Mental model:* grading a highlight reel — not "did you find the goal?" but "do your clip's
in/out points line up with the real goal, and how much do they overlap?"

### C3. DeepSpeed ZeRO stages (memory math)
Mixed-precision Adam costs ~**16 bytes/param**: fp16 weights (2) + fp16 grads (2) + fp32 optimizer
master+momentum+variance (12). A 7B model = ~112 GB — over one 80 GB A100.
- **ZeRO-1** shards the 12-byte optimizer state across N GPUs → ~4Ψ + 12Ψ/N.
- **ZeRO-2** also shards gradients → ~2Ψ + 14Ψ/N.
- **ZeRO-3** also shards parameters → ~16Ψ/N (7B across 8 GPUs ≈ **14 GB/GPU**), at the cost of
  extra all-gathers (params gathered on the fly in fwd+bwd → ~1.5× the communication of ZeRO-2).
Pick: **ZeRO-2** when the model fits but optimizer states don't; **ZeRO-3 (+CPU/NVMe offload)** when
even params don't fit. VLM caveat: keep the frozen vision encoder out of the sharded param group.
🧠 *Mental model:* moving house with friends — ZeRO-1: everyone stores a slice of the *paperwork*;
ZeRO-2: also a slice of the *boxes*; ZeRO-3: also a slice of the *furniture* — less to hold each,
but you phone each other constantly to fetch pieces.

### C4. Video token explosion
A frame ≈ **256–576 vision tokens** (a 336px ViT ≈ 24×24 = 576 patches). Naive 30 fps × 1 min ≈
**0.5–1M tokens** — impossible. Fix: **sample 1–2 fps** (motion-triggered — denser around detected
events), then **compress tokens** (pooling / Q-Former / dynamic resolution à la Qwen2-VL) to
~64–128/frame, plus **time-aware position encoding** so the model knows *when*. Budget example: 1 fps
× 60 frames × 128 tokens ≈ **7.7k tokens** — fits. Trade-off: under-sampling can *miss* a fast event
between sampled frames — irrecoverable, so you tune fps to the shortest event you care about.
🧠 *Mental model:* flipping a flipbook — you don't need every page to follow the action, but flip too
few and you miss the jump.

### C5. Curation loop ("AI training AI") without collapse
Model labels data → you fine-tune on it → repeat. Collapse/drift happens when the model reinforces
its own errors. Guards: (1) a **frozen, human-labeled eval set that NEVER enters training** — the
ground truth of record; (2) **agreement-gating** — only auto-labels above a confidence threshold AND
where independent models/passes agree get promoted; (3) **keep hard examples** (don't just drop
low-confidence — route them to human review; they're the edge cases worth mining); (4) **track the
label distribution** (KL vs the human set) to catch slow semantic drift the point-metric misses.
🧠 *Mental model:* a student grading their own homework — fine, as long as a teacher keeps a sealed
answer key and you flag every question you weren't sure about instead of guessing confidently.

### C6. Retrieval over millions of frames
Don't embed raw frames — embed **events** (the structured output): one vector per detected event
(text description + optionally a visual embedding), via CLIP/SigLIP or a text encoder. Index in an
**ANN** store (HNSW for recall/latency, or IVF-PQ when memory-bound) — FAISS/Qdrant/Milvus/LanceDB.
Query → embed → top-k → optional **rerank** by a cross-encoder. Keep **recall@k** as the gate; shard
by fleet/time to scale. Failure mode to own: event-boundary errors upstream propagate into search
misses — so retrieval quality is capped by detection quality.
🧠 *Mental model:* don't index every second of security footage — index the *incident reports* the
system already wrote, then search those.

### C7. VLM inference optimization
Decode is **memory-bandwidth-bound**, not FLOP-bound (A100 HBM ≈ 2 TB/s is the ceiling). Levers:
**quantize** weights (AWQ/GPTQ int4 → ~4× smaller, ~2–3× throughput), **KV-cache management**
(vLLM **PagedAttention** to pack more concurrent sequences; KV size = 2·layers·kv_heads·head_dim·
seq·bytes), **continuous batching** (don't wait for the slowest sequence), and export to
**ONNX/TensorRT** for kernel fusion on fixed shapes. Gate every speedup behind the eval so you don't
trade accuracy for latency silently.
🧠 *Mental model:* a kitchen bottlenecked by the pantry, not the chef — the fix is a bigger doorway
and cooking many orders at once, not a faster chef.

### C8. Narrative consistency / hallucination
Decompose the model's description into **atomic claims** ("a red car merged left at 0:12"), then
**ground each** against detected events + timestamps (an unsupported claim = a hallucination). Use
an **LLM-judge with the video-derived facts as context**, backstopped by deterministic checks
(does the cited timestamp have a matching event?). Trade-off: the judge itself can be gamed, so
calibrate it against human agreement on a sample.
🧠 *Mental model:* fact-checking a news story sentence by sentence against the security tape — every
sentence needs a timestamp that actually shows it.

### C9. Multi-modal fusion (video + language + sensor)
Sensors (GPS/IMU/lidar) run at different rates than video. Resample to a **common clock**, encode
each stream as **time-stamped tokens**, and fuse with **cross-attention** (language query attends
over video+sensor tokens) — richer than late fusion (concatenating final embeddings), cheaper to
train than fully early fusion. Own the hard part: **timestamp jitter/misalignment** — a 100 ms skew
between IMU and frames wrecks "hard brake" localization, so alignment + interpolation is load-bearing.
🧠 *Mental model:* dubbing a film — video, dialogue, and sound effects must snap to the same
timeline, or the punch lands before the fist.

### C10. Petabyte data pipeline (don't starve the GPUs)
Target **>90% GPU utilization**. Store as **sharded tars** (WebDataset) for sequential reads (random
reads kill throughput at PB scale); decode video on the **GPU (NVDEC/DALI)** so the CPU isn't the
bottleneck; **prefetch + overlap** IO with compute; shard-level shuffle for randomness without random
IO. Diagnose starvation by watching **SM utilization + data-loader wait time** (nvidia-smi dmon /
DCGM) — low SM% with high wait = starved. Honest gap: I've done this single-GPU; multi-node
coordination (sharding across workers, avoiding duplicate reads) is where I'd ramp.
🧠 *Mental model:* a car assembly line — if parts don't arrive just-in-time on the conveyor, the
robots stand idle; you widen the conveyor and stage parts trackside, you don't buy faster robots.

---

## PART D — founder-tailoring
- **Mustafa Bal** (ONNX Runtime, DeepSpeed; distributed systems): go deep on C3/C7/C10; give
  numbers; **never bluff** — own the multi-node gap and show I know the mechanism.
- **Varun Krishnan** (INFORMS Wagner Prize, optimization, chess): go deep on C2/C5/C8; eval rigor,
  metric design, avoiding reward-hacking in the curation loop.
