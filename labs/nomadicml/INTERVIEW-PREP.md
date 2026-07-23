# 1-Hour Cofounder Interview — NomadicML (MTS, ML)

Companion to `EVIDENCE-PACK.md` (JD→artifact map) and the live artifacts:
- Demo: **https://nomadic-mini-demo.vercel.app** (password gated — keep the password in your own notes, not here)
- Animated system design: **https://nomadic-mini-demo.vercel.app/system.html**

## Who you're talking to (tailor on the fly)

- **Mustafa Bal** — ONNX Runtime + DeepSpeed contributor; distributed systems, large-scale model
  training infra. If it's him, lean **system-integration + training/serving infra**; be precise,
  don't hand-wave GPUs. He will probe depth.
- **Varun Krishnan** — INFORMS Wagner Prize (large-scale driver-navigation AI), top US chess. If
  it's him, lean **ML modeling, optimization, eval rigor, product intuition**.
- Either way the company thesis: **VLMs as "hydraulic mining" for video** — turn petabytes of
  AV/robotics footage into structured, searchable, trainable intelligence. Their moat is the
  *understanding + curation loop*, not just detection.

## The 60-minute arc (how to run the hour)

| Min | Segment | Your move |
|---|---|---|
| 0–5 | Rapport / "tell me about yourself" | 90-sec story → physical-AI engineer who ships; land: "so I reverse-engineered your product to make this conversation concrete." |
| 5–12 | **Live demo** (screen-share) | Diagram → demo → parity. Script below. Stop talking, let it run. |
| 12–35 | Deep technical dive | They'll pull a thread. Use the "key decisions" bank. Show reasoning, not recall. |
| 35–48 | Their problems / systems design | They pose a real NomadicML problem (eval at fleet scale, curation, training). Think out loud, name tradeoffs. |
| 48–57 | **Your questions** (see list) | Signal you want to build *their* hard thing. |
| 57–60 | Close | "What would week 1 look like?" + one crisp reason you'd take it. |

## The 5-minute demo script (screen-share)

1. **Open `/system.html`** (15s): "One pipeline shape, two implementations, held equal by a parity
   harness. Data flows left→right; the seam is where my clone is checked against your production."
2. **Open the demo, run "Analyze your own clip"** (2m): drop a dashcam clip → real progress bar →
   events on a timeline. "Real backend — Gemini native video in a serverless function, streaming
   the actual stages. Same event schema as yours."
3. **Ask the copilot "what did we measure against production?"** (1m): it answers, grounded, citing
   the verify-key schema drift + the undocumented 402. "I tested your live API with my own key."
4. **Land the parity point** (1m): "`make parity` uploads the same clip to api-prod and mine, diffs
   the surfaces field-by-field. That's an *agentic evaluation framework* — literally bullet 3 of
   this role — pointed at my own clone."
5. **Close** (30s): "Built from your public SDK + docs only. Week 1, I'd point the curation loop at
   the events where my clone and your API *disagree* — those disagreements are the edge cases worth
   mining."

## KEY TECHNICAL DECISIONS (the core ask) — by layer

### Data layer
1. **Mirror the event schema verbatim, not "equivalent."** Ours uses their exact SDK
   `RapidReviewEvent` field names (`label, t_start "MM:SS", t_end, category, severity, aiAnalysis,
   confidence, approval, overlay`) — even camelCase `aiAnalysis`. *Why:* the field names ARE the
   comparison; renaming would reduce "term-by-term parity" to vibes. Pydantic enforces MM:SS regex,
   the severity literal, and 0–1 confidence, so an arbitrary clip can't emit a malformed event.
2. **Model the docs↔SDK schema split.** Their public docs say `type`/`description`; their SDK
   dataclass says `category`/`aiAnalysis`; the SDK silently converts. I made `type`/`description`
   computed aliases so a document diffs against *either* surface. *(This detail signals I read the
   wheel, not just the docs.)*
3. **Gemini native video over frame-sampling.** Their models see full temporal context; sampling
   frames throws away motion — the whole point. Also decisive on infra: no ffmpeg in the Vercel
   runtime, so native-video ingest is the only path that even runs there.

### System-integration layer
4. **Backend seam, not backend lock-in.** `analyze()` picks Gemini (native video) → Claude (frames)
   by env; their thinking/fast modes map to a thinking-budget toggle. Swappable the day a
   Nomadic-VL-XLarge-class open model is comparable.
5. **Verification is the contract.** Three gates: `make check` (16 offline schema/search tests, no
   keys) · `make e2e` (real VLM) · `make parity` (live vs api-prod, **honest skip** without a key —
   never a fake pass). Offline-first so CI always runs.
6. **Beat the platform limits honestly.** Vercel rejects >4.5 MB request bodies → the browser
   uploads *direct* to Vercel Blob (client-upload handshake), the function only sees a URL. The
   ~60 s function cap → fast mode + a real SSE progress bar + an honest timeout for long clips
   (never a fabricated result). Provisioned the Blob store via the REST API when the CLI's link
   step was an interactive dead-end.
7. **Knowledge-from-artifacts copilot.** The demo's copilot system prompt is assembled at deploy
   from the lab's own files — there's no second copy of the truth to drift.

### People & operations layer
8. **Honest-by-construction, because the founders will probe.** Zero-event clips are reported as
   zeros; paywalled paths *skip with instructions*; probing stopped at authorization boundaries
   (their demo batches returned "Access denied" to my key — correct, and I stopped there).
9. **Clean-room + gated exposure.** Public surfaces only (PyPI wheel, docs `llms.txt`, site-bundle
   example data). The public demo spends real model credits, so credit-spending endpoints are
   password-gated; no secret is in the repo (env vars only).
10. **Named the gaps out loud** (see below) rather than hoping they don't ask.

## Likely questions → answers

- *"How would you evaluate a VLM's localization on video?"* → temporal-IoU of predicted event
  spans vs human-labeled spans + a narrative-consistency LLM-judge; gate it in CI so a regression
  can't merge. My parity harness is the API-level analog.
- *"MM:SS precision at fleet scale — how do you keep cost sane?"* → two-tier routing (your own
  fast/thinking split proves it): a cheap pass shortlists, a thinking pass localizes; embedding
  search (`haystack_search` in your SDK) avoids re-analyzing.
- *"How do you stop 'AI training AI' from collapsing?"* → approval gates (your
  approved/rejected/pending/invalid vocabulary), a held-out human-labeled eval that never enters
  training, and drift alarms on the label distribution.
- *"What did you find in our SDK you'd fix?"* (deliver as an engineer, not a critic): stale App
  Runner URL in a shipped test; dead `test.py` in the wheel; docs↔SDK field-name divergence;
  `pip install nomadic` vs `nomadicml`. And measured live: verify-key returns
  `{valid,key_id,user_id,scope,expires_at}` not the documented shape; Bearer-only fails on GETs
  (parsed as a Firebase token) which is why the SDK sends both headers; upload is 402 on trial.
- *"Design our eval framework for spatiotemporal reasoning."* → items-as-data (single source →
  generated contract, can't drift); an EvidenceCollector seam per source; no-evidence⇒No; blocking
  gate can't pass on unmeasured items; prefer observed traces over claimed. (This is how I'd build
  it; it's also how I built the parity harness.)

## Own these gaps proactively (before they ask)

- **Distributed training at scale** (DeepSpeed/ZeRO, multi-node) — Mustafa's home turf; do NOT
  bluff. Say: "I've run single-GPU LoRA fine-tunes; I haven't owned multi-node ZeRO-3. I know the
  stages and the sharding tradeoffs conceptually and I'd ramp fast." Then pivot to what you *have*
  shipped.
- **Petabyte-scale data ops** — I've done small-scale; I understand your funnel (analyze → search →
  re-analyze) and would learn your storage/ingest reality.
- **No trained model of my own** — I orchestrate frontier VLMs; the clone proves product/pipeline
  understanding, not model-training capability (yet).

## Questions to ask them (pick 3–4)

1. Where does Nomadic-VL-XLarge still fail hardest — long-horizon temporal reasoning, rare-object
   localization, or multi-view fusion?
2. How do you measure "understanding" quality today, and what's the eval you *wish* you had?
3. What's the human-in-the-loop ratio in the curation loop now, and where do you want it to go?
4. Build vs buy on the VLM base — are you fine-tuning open models or training from scratch, and why?
5. What breaks first as you scale from N customers' fleets to 10×?
6. For this role in the first 90 days — what's the single result that would make you glad you hired?

## One-liner to close
"I don't just use video-understanding tools — I reverse-engineered yours to prove I understand the
whole loop, and built the eval harness that would tell you when my version is wrong. That's the job."
