# NomadicML Docs — Knowledge Base

Synthesized 2026-07-21 from https://docs.nomadicml.com (Mintlify; every page fetchable as `<slug>.md`; index at `/llms.txt`). Raw pages cached in `/tmp/nomadic/docs/`.

---

## 1. Product Concepts & Analysis Modes

### What Nomadic is
Video-intelligence platform ("motion analysis platform") for analyzing video with natural-language prompts. Verticals shown in docs: autonomous driving / fleet dashcams (dominant — lane straddling, jaywalking, pedestrians, MUTCD road signs, potholes), robotics (manipulation sub-task segmentation, GR00T/LeRobot), construction ("workers near active machinery"), security. Web app at `app.nomadicml.com`; Python SDK `pip install nomadic` (`from nomadic import NomadicAI`). Source: `overview`, `getting-started/quickstart`, `sdk/sdk-examples`.

### Analysis modes (source: `sdk/analyzing-videos/overview`, `sdk/analyzing-videos/prompt-analysis`, `getting-started/quickstart`)
The public surface exposes **prompt-based analysis** with two processing modes:

| Mode | SDK value | Behavior |
|---|---|---|
| **Thinking** (default) | `mode="thinking"` | "For accurate results, can take a few mins." Matches the router behavior in the web app. |
| **Fast** | `mode="fast"` | "For quicker results, takes seconds." Speed-preferring router behavior. |

- `client.analyze(id(s) or folder=..., prompt=...)` — detect custom events via natural language. Defaults: `mode="thinking"`, `timeout=2400` s, `wait=True`. `scope` = `'user' | 'org' | 'sample'` for folder-based batches.
- There is an internal **router** that selects the extraction path (e.g., overlay/telemetry extraction when the prompt asks for speed/GPS/timestamps). Docs explicitly say: "Prompt analysis does not expose router overrides, model selection, overlay flags, reasoning traces, or Wizarding Trace artifacts. Put analysis requirements directly in the prompt." (`sdk/analyzing-videos/prompt-analysis`)
- **Rapid Review** appears as the *livestream* continuous-detection mode: a live session "runs the rapid-review query on each chunk" (`rapid_review_query` param). Source: `sdk/livestreams`, API `livestreams/start-live-session` ("Start a live-stream ingestion and optional rapid-review analysis session").
- **Action Segmentation** is a distinct analysis type for robotics: `client.analyze(videos, analysis_type=AnalysisType.ACTION_SEGMENTATION, segmenter_id=...)` (`from nomadic.video import AnalysisType`). Source: `sdk/robotics-lerobot-export`.
- **"Agent" language**: quickstart says "Reasoning Trace shows how our agents process in the data to provide the results to the user's query" — agentic reasoning traces are visible per event in the web UI; batch results include "Batch reasoning" summaries. No separately named "Agent Analysis" mode exists in current docs.
- **Semantic search** (`client.search`) over already-analyzed events — see §5.
- **Structured ODD export** (`client.generate_structured_odd`) — ASAM OpenODD-compliant CSV of the vehicle's operating domain, column-schema driven (name/prompt/type/literals). Returns `csv`, `columns`, `reasoning_trace_path`, `share_id`/`share_url`, `processing_time`, `raw`. Source: `sdk/structured-exports`.
- Legacy naming: prompt-analysis batches "may currently appear as legacy `\"ask\"`" in `batch_type`. Source: `sdk/batch-results-metadata/get-batch-analysis`.

### When to use which
- Custom one-off / batch event detection → prompt analysis, Thinking (accuracy) vs Fast (latency).
- Continuous monitoring of a live HLS stream → livestream session + `rapid_review_query`.
- Finding specific already-detected events across a folder → `search()`.
- Robot demonstration data → action segmentation + LeRobot export.
- Compliance/ODD documentation → structured ODD export.

---

## 2. REST API Surface (source: `api-reference/*` pages; all embed the same OpenAPI 3.0.3 "Nomadic API v1.0.0" spec, "Curated public REST API for Nomadic video operations. Administrative and internal orchestration endpoints are intentionally excluded.")

### Base URL & Auth
- Production server: `https://api-prod.nomadicml.com` (local dev: `http://localhost:8099`).
- Two accepted auth schemes on every endpoint:
  - `bearerAuth`: `Authorization: Bearer <NOMADIC_API_KEY>`
  - `apiKeyAuth`: header `X-API-Key: <key>` ("alternative API-key header accepted by parts of the API")
- Keys generated in web app: Profile → API Keys → Generate New Key; default expiry 90 days; shown once. Source: `advanced/authentication`.
- SDK client config: `NomadicAI(api_key, base_url="https://api-prod.nomadicml.com/", timeout=900, collection_name=...)` — `collection_name` is a **Firestore collection name** used only for self-hosted VPC instances. Source: `advanced/authentication`, `sdk/sdk_installation`.
- Standard error envelope `ErrorResponse`: `{detail: string|object, message: string, error: string}`; statuses 400/401/403/404/429/500 on all endpoints (429 = rate limited).

### Endpoints (tag → verb path — schema highlights, verbatim field names)

**Authentication**
- `POST /api/keys/verify` — verify key. 200 → `AuthVerification {valid: bool, user_id, uid, email, org_id}`.

**Uploads**
- `POST /api/upload-video` — multipart/form-data: `source` (required, enum `file|video_url`), `scope` (`user|org`, default `user`), `folder_id`, `chunk_size` (int ≥1), `video_url` (uri), `custom_name`, `file` (binary), `metadata_file` (binary, "Optional overlay metadata JSON"). 200 → `UploadResponse {video_id, status, visual_analysis: object}`.

**Analysis** (prompt-based; the "router v2 query" API)
- `POST /api/router/v2/query/start` — body `AnalyzeRequest {query: string (required), video_id: string, video_ids: [string]}`. 200 → `AnalyzeStartResponse {stream_id, status, batch_id}`. Start analysis, get an SSE stream id.
- `GET /api/router/v2/query/events/{stream_id}?last_id=0` — SSE (`text/event-stream`) progress events for a started analysis; `last_id` = last received SSE event id (default `'0'`) for resumability.
- `POST /api/router/v2/query/stream` — same `AnalyzeRequest`, but streams SSE progress in the same response. Docs: "Prefer the start/events flow for resumable clients."
- `GET /api/videos/{video_id}/analyses/{analysis_id}` — 200 → `AnalysisResponse {video_id, analysis_id, analysis: object, metadata: object, events: [object]}` (events are free-form objects; see §3).
- `GET /api/videos/{video_id}/analyses/{analysis_id}/status` — 200 → `AnalysisStatus {status: string, analysis_id, progress: number}`.

**Batches**
- `GET /api/batch/{batch_id}/status?include_videos=true` — 200 → `BatchStatus {batch_id, status, aggregated_progress: object, videos: [object]}`.
- `POST /api/batch/{batch_id}/analyses/bulk?include_source_uri=` — body `BulkAnalysesRequest {video_ids: [string], maxItems 500}`. 200 → `BulkAnalysesResponse {analyses: [object], unresolved_video_ids: [string], not_found_analysis_ids: [string]}`.

**Videos**
- `GET /api/my-videos?folder=&scope=user|org|sample` — 200 → `VideoListResponse {videos: [VideoSummary]}`; `VideoSummary {video_id, filename, status, folder_id, folder_name, created_at}`.
- `GET /api/video/{video_id}/status` — 200 → `VideoStatus {video_id, status, metadata: object}`.
- `POST /api/video/{video_id}/signed-url` — body `SignedUrlRequest {path, expires_in: int default 900 min 60, method: GET|HEAD default GET, share_token, allow_sample: bool default false, batch_id}`. 200 → `SignedUrlResponse {url, expires_at, method}`.
- `POST /api/video/signed-urls` — bulk: `BulkSignedUrlRequest {requests: [BulkSignedUrlRequestItem], maxItems 50}`; item adds required `request_id`, `video_id`, and `expires_in` max 3600. 200 → `results` map of request_id → `{ok:true, url, expires_at, method}` or `{ok:false, error, status}`.
- `DELETE /api/video/{video_id}` — 200 → `DeleteVideoResponse {status: "deleted", video_id}`.

**Other tags in the spec** (fetched via llms.txt listing; not pulled in full): Folders (`create-folder`, `create-or-get-folder`, `get-folder-by-name`), Cloud Imports (`import-gcs-objects`, `import-s3-objects`, `import-hugging-face-bucket-objects`, `get-import-job`, `list-import-job-videos`), Cloud Integrations (create GCS / S3 / HF-bucket / S3-Storage-Transfer integration, list/get/delete, `get-role-based-s3-import-setup`), MCAP (`create-mcap-ingest`, `process-mcap-ingest`, `get-mcap-ingest`, `start-s3-mcap-cloud-ingest`, `get-mcap-import-job`, `stitch-mcap-views`), Multi-view (`stitch-uploaded-views`), Livestreams (`start-live-session`, `attach-stream`, `end-live-session`, `get-live-session`, `list-live-sessions`, `create-signed-live-manifest-url`). Full OpenAPI at `https://docs.nomadicml.com/openapi.json`.

---

## 3. Events / Output Schema

### Prompt analysis result (SDK) — source: `sdk/analyzing-videos/prompt-analysis`, `sdk/batch-results-metadata/get-batch-analysis`
Single video: dict with `video_id`, `analysis_id`, `mode`, `status`, `summary`, `events`.
Batch: `batch_metadata` {`batch_id`, `batch_viewer_url`, `batch_type` (legacy `"ask"` for prompt batches), `analysis_type`, `review_status`, `review_status_updated_at`, `metadata` (custom KV), plus config like `prompt`, `category`} + `results` (per-video dicts as above).

### Event object fields (seen verbatim across docs)
- `label` — natural-language event label (`event.get('label')`)
- `t_start` / `t_end` — human-readable event window (`MM:SS`)
- `type` — event category (e.g., `"Security"`, `"Motion Anomaly"`)
- `description` — scene description
- `severity` — `low` / `medium` / `high` guidance in `advanced/best-practices`: Low = improvement opportunity, Medium = notable, High = critical safety concern
- `confidence` — float 0–1 (e.g., `0.95`)
- `overlay` — map of telemetry field → `{start, end}` values extracted from on-screen overlays (e.g., `event["overlay"]["frame_speed"]["start"]`) — only when metadata sidecar was uploaded / overlays visible and prompt requests it (`sdk/sdk-examples` §10)
- Older/alternate example fields (Supabase example, `sdk/sdk-examples` §11): `time`, `dmvRule`, `aiAnalysis`
- Approval workflow: every event carries an approval status — `approved | rejected | pending | invalid` — set via web UI Approve/Reject buttons; filterable in `get_batch_analysis(filter=...)`. Reviewed state rolls up to batch `review_status`.
- REST `AnalysisResponse.events` is intentionally loose: `array of object, additionalProperties: true`.

### Batch CSV columns (`get_batch_analysis(as_csv=True)`) — verbatim
`Query, Video, Approval Status, Timestamp, Category, Label, AI Analysis, Severity, Video ID, Analysis ID, Batch ID, Batch Viewer URL, Status, Confidence, Import Source URI, Summary` (one row per event; header always included).

### Reasoning / chain-of-thought
- Web UI: per-event **Reasoning Trace** ("how our agents process the data") + **Batch reasoning** summary; filter by approved/rejected/pending. (`getting-started/quickstart`)
- Search returns `thoughts` (list of reasoning steps) — see §5.
- Structured ODD export returns `reasoning_trace_path` ("Final Firestore path used for reasoning logs") — confirms Firestore as the metadata/results store. (`sdk/structured-exports`)
- SDK prompt analysis explicitly does NOT expose reasoning traces or "Wizarding Trace artifacts" (an internal artifact name that leaks into the docs). (`sdk/analyzing-videos/prompt-analysis`)

### Livestream event schema (source: `sdk/livestreams`) — example verbatim
```python
{"type": "Security", "label": "robot picking up an apple", "description": "...",
 "severity": "low", "confidence": 0.95, "stream_time": 9.0, "chunk_relative_time": 9.0,
 "t_start": "00:09", "t_end": "00:16", "created_at": "2026-03-07T22:51:55.312121+00:00",
 "chunk_index": 0, "chunk_id": "session_000", "analysis_id": "session_analysis_000"}
```
Timing fields: `stream_time` (main display field, seconds from session start), `capture_time`, `chunk_index`, `chunk_relative_time`, `hls_cumulative_offset`, `t_start`/`t_end`, `created_at`, `analysis_id`, `chunk_id`. Session fields: `stream_id`, `session_id`, `name`, `source_url`, `status` (`INITIALIZING | ACTIVE | FINISHED | FAILED`), `chunk_count`, `events`, `chunks`.

---

## 4. Video / Upload Lifecycle (source: `sdk/uploading-videos/*`, `sdk/cloud-storage`, `sdk/video-folder-management/*`)

`client.upload()` handles everything; return type keys on source:
- Local files & URLs → `{"video_id": ..., "status": "processing" | "uploaded" | ...}`. Multi-file → list. Video statuses: `processing`, `uploading_failed`, `uploaded` (ready for analysis).
- Local `.mcap` → `mcap_ingest_id` → `wait_for_mcap_ingest()` → `video_ids`, `videos_by_channel`.
- Cloud imports (`gs://`, `s3://`, `hf://buckets/...`) → `{"import_job_id": "ij_xxx", "status": "importing"}` → poll `get_import_job()` (`job_id`, `source` = `s3|gcs|hf_bucket`, `bucket`, `prefix`, `folder_id`, `folder_name`, `total`, timestamps) + `get_import_job_videos()` (cursor-paginated: `videos: [{video_id, status, import_source_uri}]`, `has_more`, `next_cursor`; terminal statuses `UPLOADED` / `UPLOADING_FAILED`). No wildcards; list objects explicitly. R2 = S3-compatible via `endpoint_url` on the saved integration.
- S3 `.mcap` cloud ingest → role-based `s3_storage_transfer` integration (AWS IAM role trusted by Google Storage Transfer via `accounts.google.com:sub` = `google_service_account_subject_id`) → `mcap_import_job_id` → `wait_for_mcap_import_job()`.
- Multi-view: dict of view→file/URI, `front` required; returns stitched front `video_id` (local) or import job (cloud).
- Metadata sidecars: JSON with same base filename as video; describes overlay fields (`fields: [{name, type, unit, position, format}]`) per the external "Metadata Ingestion Spec" Google Doc.
- Upload params: `name`, `folder` (auto-created), `scope` (`user|org`), `upload_timeout=1200`, `wait_for_uploaded=True`, `integration_id`, MCAP-specific `chunk_size`, `front_channel`, `channel_roles`, `channel_labels`.
- Video quality guidance: ≥720p (1080p rec.), ≥24 fps (30 rec.), ≥4 Mbps (8 rec.), MP4/H.264 best; optimal duration 5–20 min, split >30 min. (`advanced/best-practices`)
- Folders: `create_folder(name, scope, description)`, `get_folder(name, scope)` → `{id, name, org_id, scope, created_at, created_by, description, video_count}`. `my_videos(folder, scope)` → `[{video_id, video_name, duration_s, folder_id, status, folder_name, org_id}]`.
- `cloud_integrations` helper: `.list(type=...)`, `.add(type="gcs"|"s3", name, bucket, prefix, region, endpoint_url, credentials)`, `.add_hf_bucket(name, bucket, token, prefix)`, `.add_s3_storage_transfer(name, bucket, prefix, role_arn)`, `.get_s3_storage_transfer_setup()`.

---

## 5. Semantic / Embedding Search (source: `sdk/search`, `sdk/sdk-examples` §4)

`client.search(query, folder_name, scope='user'|'org'|'sample')` — semantic search **across analyzed events inside a folder** (i.e., over analysis results, not raw video). Open-ended natural-language queries ("red pickup truck overtaking", "Find near-misses with pedestrians on crosswalks"). "Nomadic will reason about what fits best."

**Returns** (verbatim):
- `summary`: string overview of the findings
- `thoughts`: list of reasoning steps (chain-of-thought) shown in the UI
- `matches`: list of `{video_id, analysis_id, event_index, similarity, reason}` — similarity score + per-match natural-language reason
- `session_id`: identifier for the search session (re-fetching / sharing)

Canonical composite workflow (`sdk/sdk-examples` §6): broad `analyze()` over a folder → `search()` to narrow to matching videos → targeted re-`analyze()` on the matched subset → this is the documented funnel/edge-case-mining pattern. Videos never need re-upload for new analyses (§7).

---

## 6. The ML Story (models, VLMs, fine-tuning, curation, edge-case mining)

- **Named model**: `"Nomadic-VL-XLarge"` appears as a `model` metadata value in `add_batch_metadata` example — implies a family of in-house VL (vision-language) models. (`sdk/batch-results-metadata/add-batch-metadata`)
- **Model stack (VPC page)**: self-hosted deployments provision "model-specific SageMaker endpoints… This is the pattern we use for **large VLM endpoints, OCR, segmentation**, and related GPU workloads" — i.e., the platform composes a large VLM + OCR (overlay/telemetry reading) + segmentation models, each independently deployable/resizable. (`getting-started/vpc-setup`)
- **Router**: internal analysis router chooses extraction paths per prompt (Thinking vs Fast are router behaviors; overlay-aware queries "the router selects the appropriate extraction path"). Router overrides / model selection are deliberately not exposed. (`sdk/analyzing-videos/prompt-analysis`, `sdk/sdk-examples` §10)
- **Reasoning agents**: results include per-event agentic reasoning traces; search is chain-of-thought based. (`getting-started/quickstart`, `sdk/search`)
- **Trainable segmentation models (customer-side fine-tuning)**: `client.train_segmenter(name, external_data=<trajectory .npz>, domain="manipulation"|"construction", epochs=...)` trains a sub-task segmentation model on fleet trajectory data (NPZ schema: `signal (n_channels,T)`, `t_sec (T,)`, `sample_rate_hz`); poll `get_segmenter_status()` → `segmenter_id`; then `analyze(..., analysis_type=AnalysisType.ACTION_SEGMENTATION, segmenter_id=...)`. (`sdk/robotics-lerobot-export`)
- **Data curation for robot foundation models**: `export_lerobot_dataset(batch_id|results, output_dir, trajectory_tool="manipulator_trajectory", camera_key, robot_type)` → LeRobot v2.1 dataset (`meta/info.json`, `meta/tasks.jsonl`, `meta/modality.json`, per-episode parquet+mp4, per-frame `task_index` sub-task timeline) ready for NVIDIA **GR00T fine-tuning**. Rationale: flat single-sentence labels throw away sub-task structure; Nomadic's action segmentation restores language conditioning per sub-skill. Requires `pip install 'nomadic[lerobot]'` + ffmpeg. Videos need a completed `manipulator_trajectory` artifact for proprioception (else `skipped_segments`; `trajectory_tool=None` → video-only export). (`sdk/robotics-lerobot-export`)
- **Human-in-the-loop eval/curation**: approve/reject/pending/invalid per event in the web UI; batch-level `review_status`; `get_batch_analysis(filter="approved")` to harvest only human-approved detections — the documented curation loop. Batch `metadata` KV (`experiment_id`, `version`, `model`, `notes`) supports experiment tracking. (`sdk/batch-results-metadata/*`)
- **Edge-case mining pattern**: broad analyze → semantic search → targeted re-analyze (§5); "Find outlier events" is the canonical demo prompt. (`sdk/sdk-examples`)
- **Firestore** backs analysis/metadata storage (`collection_name` client param; `reasoning_trace_path` is a Firestore path); GCS/S3 for video objects.

---

## 7. Rate Limits, Plans, Best Practices (source: `advanced/best-practices`, `advanced/authentication`, `getting-started/vpc-setup`)

- **Rate limits**: 60 requests/minute, 10,000/day (published); 429 responses on all endpoints; implement exponential backoff; batch operations to reduce calls.
- **Pricing/plan hints**: free account signup ("Sign up for a free account"); read-only demo/sample folders (`scope="sample"`) for trying without data; enterprise = self-hosted VPC deployments (AWS or GCP, Terraform-managed, SageMaker or private inference endpoints; contact support@nomadicml.com). No public price list in docs.
- **API keys**: default 90-day expiry, rotate every 90 days, shown once, minimum permissions, store in env vars/credential stores.
- **SDK exceptions** (note module inconsistency in docs: `from nomadic import NomadicAI` but `from nomadicml.exceptions import ...`): `AuthenticationError`, `VideoUploadError`, `AnalysisError`, `NomadicError` (also `NomadicMLError`, `ValidationError` referenced in SDK reference pages). PyPI package page is `pypi.org/project/nomadicml/` though install command is `pip install nomadic`; Python 3.8–3.11.
- **Best practices highlights**: 5–20 min videos; consistent naming `YYYY-MM-DD_Operator_Location.mp4`; metadata/tags at upload; pagination + server-side filters + field selection + gzip; TTL caching; retention tiers 30/90-day/1+ year; audit logging of uploads/deletions/key events; process batches off-peak; compress before upload.
- **Timeouts**: client default 900 s; `analyze` timeout default 2400 s; upload timeout 1200 s; MCAP import waits up to 7200 s in examples.

---

## 8. Page Index Consulted
Non-API: `overview`, `getting-started/quickstart`, `getting-started/vpc-setup`, `advanced/authentication`, `advanced/best-practices`, `sdk/sdk_installation`, `sdk/sdk-examples`, `sdk/analyzing-videos/{overview,prompt-analysis}`, `sdk/search`, `sdk/structured-exports`, `sdk/uploading-videos/{overview,local-files-urls,cloud-imports}`, `sdk/cloud-storage`, `sdk/livestreams`, `sdk/robotics-lerobot-export`, `sdk/batch-results-metadata/{add-batch-metadata,get-batch-analysis}`, `sdk/video-folder-management/{folders,my-videos,delete-video}`, `more/{main-services-agreement,privacy-policy}` (not fetched — legal).
API reference fetched: `analysis/{start-analysis,stream-analysis,read-analysis-events,get-analysis-document,get-analysis-status}`, `authentication/verify-api-key`, `uploads/upload-a-video`, `videos/{list-videos,get-video-status,create-signed-video-url,create-signed-urls-in-bulk,delete-video}`, `batches/{get-batch-status,get-batch-analyses-in-bulk}`. Remaining API pages (folders, cloud-imports, cloud-integrations, mcap, multi-view, livestreams) enumerated in §2 and covered functionally via the SDK pages; full spec at `/openapi.json`.
