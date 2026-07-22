# Term-by-Term: NomadicML (production) vs `nomadic_mini` (clean-room clone)

Every "theirs" cell is verbatim from the published SDK source (`nomadicml` 0.1.53 off PyPI,
cited as `video.py:line`) or their public docs (`docs.nomadicml.com`, raw markdown in
`recon/docs-raw/`). Every "ours" cell is a file in `nomadic_mini/`. Live-API cells are
verified by `make parity` when `NOMADICML_API_KEY` is set — never claimed otherwise.

## 1. Customer-facing verbs

| Concern | Theirs (SDK 0.1.53) | Ours (`nomadic_mini`) | Parity |
|---|---|---|---|
| Client | `NomadicML(api_key, base_url="https://api-prod.nomadicml.com/", timeout=900)` (client.py:42) | `MiniClient()` local; `NomadicLive(api_key)` for their API | same verb set |
| Upload | `client.upload(video)` → `POST /api/upload-video` (multipart `source=file`), poll `/api/video/{id}/status` until `UPLOADED` (video.py:1512, 4813) | `MiniClient.upload()` (local registry); `NomadicLive.upload()` + `wait_uploaded()` hit the same endpoint/poll verbatim | ✅ endpoint-for-endpoint |
| Analyze (prompt) | `client.analyze(id, "…", mode="thinking"\|"fast")`; fast → `POST /api/router/query`; thinking → `POST /api/router/v2/query/start` + SSE `/api/router/v2/query/events/{stream_id}` (video.py:2961–3195) | `MiniClient.analyze(id, prompt, mode="thinking"\|"fast")` → VLM; `NomadicLive.analyze_start()/analyze_events()` mirror the start+SSE flow | ✅ same modes, same flow shape |
| Results | `GET /api/videos/{vid}/analyses/{aid}` → `{video_id, analysis_id, analysis, metadata, events[]}` | `AnalysisDocument` with the same five fields (events.py) | ✅ field-for-field |
| Search | `client.search(query=…)`: session start → `/api/search` → poll; returns `{summary, thoughts, matches[{video_id, analysis_id, event_index, similarity, reason}], session_id}` (video.py:5964) | `MiniClient.search()` → `SearchResult` with identical field names; cosine over event embeddings | ✅ response-shape identical |
| Batches | `POST /api/create-batch`, poll `/api/batch/{id}/status`, bulk `POST /api/batch/{id}/analyses/bulk` (≤500) | not reproduced (out of small-scale scope — single-video path only) | ◻ scoped out, documented |
| Livestream ("Rapid Review" live) | `client.livestream.start_session(source_url=HLS, rapid_review_query=…)` (livestream.py:103) | not reproduced | ◻ scoped out |
| Custom agents / fine-tune | `create_agent/update_agent` (`prompt_optimization`\|`finetuning`) from approved/rejected events (video.py:6370–6507) | not reproduced; the **concept** is FM-os `curation-loop` + `agentic-eval` skills | ◻ concept covered elsewhere |

## 2. Event schema (the term-by-term core)

| Field | Theirs — SDK `RapidReviewEvent` (types.py:34) | Ours — `MotionEvent` (events.py) |
|---|---|---|
| `label` | str | ✅ same name, same meaning |
| `t_start` / `t_end` | `"MM:SS"` (or HH:MM:SS) | ✅ same name, MM:SS regex-enforced |
| `category` | str; agent vocabulary "Lane Change Detection", "Vehicle Turns", "Relative Motion Analysis", "Driving Violations" (video.py:174–195) | ✅ same name; `CATEGORIES` pins their verbatim strings |
| `severity` | str, default `"medium"` | ✅ `Literal["low","medium","high"]` |
| `aiAnalysis` | str (model reasoning) | ✅ same name (camelCase preserved deliberately) |
| `confidence` | float, default 0.85 on conversion | ✅ float, 0–1 bound enforced |
| `approval` | `approved\|rejected\|pending\|invalid`, default `"pending"` (video.py:5288) | ✅ same Literal, same default |
| `overlay` | `{base: {"start","end"}}` promoted from `frame_*`/`unix_timestamp` pairs; GPS keys `frame_gps_lat/lon` (video.py:568–629) | ✅ same-name dict; population scoped out (needs sensor telemetry) |
| `annotated_thumbnail_url` | Optional[str] | ✗ not mirrored (server-rendered artifact) |

**Their second schema** — Firestore `UIEvent` `{type, time:"t=X.XX", end_time, severity, description, dmvRule, aiAnalysis, data, approval}` (types.py:49) with conversion `type→category`, `description→label`, `time→t_start` (video.py:646–752). We mirror this duality: `MotionEvent.type` / `.description` are computed aliases, so our documents diff against either surface. (An interview-grade detail: their docs' REST examples and their SDK dataclass disagree on field names; the SDK converts.)

## 3. Analysis modes & models

| Term | Theirs | Ours |
|---|---|---|
| `mode="thinking"` | v2 start + SSE, slower/accurate | Gemini flash, dynamic thinking budget |
| `mode="fast"` | `/api/router/query` `prefer_fast: true, quick_analysis: true` | Gemini flash, `thinking_budget=0` |
| Model name | `"Nomadic-VL-XLarge"` default everywhere (video.py) — in-house VLM family | `gemini-2.5-flash` / Claude frames fallback; backend recorded in `metadata.backend` |
| Legacy fixed agents | `AnalysisType`: `rapid_review`, `edge_case_agent`, `lane_change_agent`, `turn_agent`, `relative_motion_agent`, `violation_agent`, `custom_agent`, `action_segmentation` (video.py:99–122) | prompt-path only (their own modern direction; legacy ASK is deprecated for 2026-05-19) |
| Prompt wire format (legacy ASK) | `"{category}-----------EVENT_DESCRIPTION-----------{description}"` (video.py:172,1000) | n/a (modern path) |

## 4. Auth & transport

| Term | Theirs | Ours (`NomadicLive`) |
|---|---|---|
| Base URL | `https://api-prod.nomadicml.com` (client.py:20) | ✅ verbatim |
| Headers | BOTH `X-API-Key` and `Authorization: Bearer` + `X-Client-Type: SDK`, `X-Request-ID`, `Idempotency-Key` (client.py:61–64, 307–317) | ✅ both auth headers + `X-Client-Type` |
| Verify | `POST /api/keys/verify` → `{valid, user_id, uid, email, org_id}` | ✅ `verify_key()` |
| Retry | urllib3 status retry (408/429/5xx/520–527, 3×) + `backoff.expo` on conn errors (client.py:66–88) | ✗ simplified (httpx defaults) — noted, not needed at demo scale |
| Errors | 401→`AuthenticationError`, ≥400→`APIError(status_code, message, details)` | httpx `raise_for_status` (simplified) |

## 4b. Live-API findings (measured against api-prod, 2026-07-21)

| Surface | Docs claim | Production reality |
|---|---|---|
| `POST /api/keys/verify` | returns `{valid, user_id, uid, email, org_id}` | returns `{valid, key_id, user_id, scope, expires_at}` — `uid`/`email`/`org_id` absent, `scope: [read, write]` + 1-year `expires_at` undocumented (docs also say keys expire in 90 days) |
| Auth headers | docs: `Authorization: Bearer` **or** `X-API-Key` | on GET endpoints, Bearer-only is parsed as a **Firebase ID token** and fails ("Firebase auth: Invalid or expired token"); `X-API-Key` works everywhere. This explains why their SDK unconditionally sends BOTH headers (client.py:61–64, 307–317) — the docs' "or" is wrong in practice |
| `POST /api/upload-video` | documented plainly | free trial: HTTP **402** `{"detail": "Video upload is not available on the free trial. Upgrade to upload videos."}` — both `source=file` and `source=video_url`; not mentioned in docs |
| `GET /api/my-videos` | per docs | ✅ works with `X-API-Key`; fresh account returns `{"videos": []}` (sample scope too) |
| Sample scope | docs: free tier includes sample folders | `GET /api/folders/get?scope=sample` → `{"detail": "Sample scope is read-only"}`; samples not reachable via this API surface on trial |
| Batch endpoints on public demo batches | n/a | `GET /api/batch/{id}/status` on the demo batches their own site deep-links → `{"detail": "Access denied"}` — org-scoped authorization enforced (correct behavior; probing stopped there) |

## 5. What we deliberately did NOT reproduce (honesty ledger)

- **Their models**: `Nomadic-VL-XLarge` is in-house (VPC docs show large VLM + OCR + segmentation
  on per-model GPU endpoints). We substitute frontier VLMs — the pipeline shape is the claim, not
  the weights.
- **Fleet scale**: their public runs cover 85–500 videos per batch (BDD100K: 500 → 1,969 events);
  ours is 2 clips by design ("small scale" per the original ask).
- **Sensor fusion**: overlay telemetry (GPS, joint angles), multi-view stitching, MCAP ingest,
  3D trajectory viewers, ms-precision action segmentation.
- **Batch/livestream/custom-agent surfaces** (mapped above, not implemented).
- **Evidence artifacts**: segmentation overlays, annotated thumbnails, reasoning-trace UI.

## 6. Verification map

| Claim | How it's checked |
|---|---|
| Our schema == their SDK schema | `make check` (`tests/test_schema.py`) — offline, always runs |
| Pipeline works on real video | `make e2e` (`tests/test_e2e_vlm.py`) — real clip, verbatim example query |
| Their API behaves as documented AND matches our surface | `make parity` (`tests/test_parity_live.py`) — uploads the same clip to api-prod, runs the same verbatim query, diffs document + event fields, prints side-by-side events. Requires `NOMADICML_API_KEY`; skips honestly without it |
| Example reproduction | `nomadic_mini/scripts/run_examples.py` → `out/RESULTS.md` + JSON docs |
