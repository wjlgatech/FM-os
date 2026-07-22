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
| Webapp | `webapp/server.py` + `webapp/static/` | FastAPI: serves the visual demo, `/api/results` (real out/*.json), `/api/chat` (copilot: Anthropic SSE, system prompt assembled **live from these very files** so knowledge never drifts) |

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
- **Search is cosine-only**: their production search shows agentic multi-step reasoning
  (`thoughts[]` traces); ours fills that field with a one-liner.

## Future plan

- **P0 (pre-interview)**: full live roundtrip on one clip (web-UI upload); read their two eval
  blog posts; rehearse the 5-minute demo on the webapp.
- **P1**: batch mode (`create-batch`/bulk-fetch mirror) on 20–50 BDD100K clips; temporal-IoU
  eval of our events vs their approved events — the agentic-eval story made quantitative.
- **P2**: curation loop demo — disagreements between our clone and their API become the mined
  edge-case dataset; fine-tune a small open VLM (per FM-os `vlm-quickstart`) on it.
- **P3**: agentic search — replace one-shot cosine with a plan→retrieve→validate loop that
  emits real `thoughts[]`, closing the last schema-fidelity gap.
