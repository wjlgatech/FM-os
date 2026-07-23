# Architecture — nomadic_mini + demo webapp

## System design (bird's eye)

```
                      ┌─────────────────────────────────────────────────┐
                      │                    THEIRS (production)          │
                      │  app.nomadicml.com ── api-prod.nomadicml.com    │
                      │  Nomadic-VL-XLarge + OCR + segmentation (VPC)   │
                      └───────────────▲─────────────────────────────────┘
                                      │ term-by-term parity (tests/test_parity_live.py)
                                      │
 video file ──► MiniClient.upload() ──► analyze(prompt, mode) ──► AnalysisDocument
                (registry, vid-*)      │                          {video_id, analysis_id,
                                       │                           analysis, metadata, events[]}
                              backend seam (analyze.py)                    │
                              ├─ Gemini 2.5 Flash (native video)           ▼
                              │   thinking = dynamic budget        EventIndex.add()
                              │   fast     = budget 0              (search.py)
                              └─ Claude frames fallback                    │
                                 (ffmpeg 0.5fps → images)                  ▼
                                                              search(query) → {summary,
                                                               thoughts, matches[]}
```

## Component spec

| Component | File | Contract |
|---|---|---|
| Event model | `nomadic_mini/events.py` | Verbatim SDK `RapidReviewEvent` fields (`label, t_start MM:SS, t_end, category, severity, aiAnalysis, confidence, approval, overlay`) + computed docs-variant aliases (`type`, `description`). Pydantic-enforced: MM:SS regex, severity literal, confidence 0–1 |
| VLM analyzer | `nomadic_mini/analyze.py` | `analyze(path, prompt, mode)` → `AnalysisDocument`. Prompt pins their verbatim category vocabulary; JSON-only output parsed + validated. Backend seam picks Gemini (native video) else Claude (frames) |
| Frame extraction | `nomadic_mini/frames.py` | ffmpeg → JPEG b64 at capped fps/height — only used by the Claude fallback |
| Search | `nomadic_mini/search.py` | `EventIndex`: embed event text (gemini-embedding-001 live / hashed BoW offline) → cosine → matches in their verbatim `{summary, thoughts, matches}` shape |
| Clients | `nomadic_mini/client.py` | `MiniClient` (local, same customer verbs) and `NomadicLive` (real REST: verbatim endpoints, both auth headers, upload→402 fallback to `my_videos()`) |
| Gates | `Makefile` | `check` (offline contracts) · `e2e` (real VLM) · `parity` (live API, honest skip) |
| Webapp (local) | `webapp/server.py` + `webapp/static/` | FastAPI: serves the visual demo, `/api/results` (real out/*.json), `/api/chat` (copilot: Anthropic SSE, system prompt assembled **live from these very files** so knowledge never drifts) |
| Webapp (public deploy) | `nomadic-mini-demo/` | Vercel: static CDN + `api/chat.py` (copilot) + **`api/analyze.py`** (live pipeline: user clip → Gemini native video → events, SSE stage progress) + **`api/blob-upload.js`** (Vercel Blob client-upload handshake, so the browser uploads big clips direct to storage past the 4.5 MB function-body limit). Password-gated; **https://nomadic-mini-demo.vercel.app** |

## Key design decisions (and why)

1. **Verbatim schema mirroring** — field names are the comparison; renaming anything would
   reduce the parity harness to vibes. Even `aiAnalysis` camelCase is preserved.
2. **Two-schema duality mirrored** — their docs (`type/description`) and SDK (`category/aiAnalysis`)
   disagree; we model SDK-primary with computed aliases, so we can diff against either surface.
3. **Backend seam, not backend lock-in** — `analyze()` picks Gemini/Claude by env; their
   thinking/fast split maps to thinking-budget on/off. Swappable when Nomadic-VL-XLarge-class
   models become comparable.
4. **Offline-first gates** — `make check` needs zero keys/network (hashed-BoW embedder, schema
   contracts), so CI can always run; live tests skip honestly, never fake-pass.
5. **Knowledge-from-artifacts copilot** — the webapp's agent reads the actual lab files at
   startup; there is no second copy of the truth to go stale.

## Strengths

- **Term-by-term verifiable**: every claim traces to file:line (SDK) or a measured HTTP response.
- **Honest by construction**: zero-event results reported; paywalled paths skip with instructions;
  probing stopped at authorization boundaries.
- **Real signal found**: docs-vs-production drift (verify-key schema, Bearer-on-GET failure,
  undocumented 402) — findings their own team would care about.
- **Small and legible**: ~600 lines of engine code, fully test-gated, one afternoon of work.

## Weaknesses (named, not hidden)

- **No trained model**: we orchestrate frontier VLMs; they trained Nomadic-VL-XLarge. The clone
  proves pipeline/product understanding, not model-training capability (FM-os `vlm-quickstart`
  covers that story).
- **Two clips ≠ fleet scale**: no batching, no 500-video runs, no cost model at scale.
- **No sensor fusion**: overlay/GPS/joint-telemetry fields exist in the schema but are never
  populated; ms-precision action segmentation is out of reach for pure-vision sampling.
- **Full live parity still gated**: free trial blocks API upload; roundtrip comparison awaits a
  web-UI upload or plan upgrade.
- ~~**Search is cosine-only**~~ → **RESOLVED (P3, 2026-07-23)**: `agentic_search.py` runs a real
  plan → retrieve → validate loop emitting genuine `thoughts[]` + per-match reasons (LLM-backed,
  offline-deterministic fallback). Live proof: query "stopped vehicle forcing a lane shift" → 4
  planned sub-queries → 4 retrieved → 1 validated (the U-Haul), each with a reason.

## Future plan — status (2026-07-23)

- **P0 — blocked on a 5-min human step.** Full live roundtrip needs a clip uploaded via
  app.nomadicml.com's web UI (API upload is 402-gated on the free trial; I can't log into the
  account). Everything else is prepped: `make parity` auto-runs the roundtrip once one video
  exists (falls back to `my_videos()`). *Unblock:* Paul uploads `data/drive_city_34s.mp4` in the
  web UI, then `make parity`.
- **P1 — partially blocked.** Buildable now: the batch-mirror harness (our clone over N clips) +
  the temporal-IoU eval function (ready-on-arrival, unit-tested). Blocked: the comparison
  *denominator* — "their approved events" needs their API to analyze the clips (upload paywalled),
  and BDD100K needs a license/download. *Unblock:* paid NomadicML plan (or bulk web-UI upload) +
  BDD100K access.
- **P2 — blocked (depends on P1 + GPU).** The disagreement-miner (clone↔API mismatches → edge-case
  set) can be scaffolded, but a real small-VLM fine-tune is GPU-hours, not a session task. Gated on
  P1's disagreements existing first.
- **P3 — ✅ DONE.** `agentic_search.py` + `tests/test_agentic_search.py` (4 tests); wired into
  `MiniClient.search`. Mirrors their `{summary, thoughts, matches}` funnel with real reasoning.
