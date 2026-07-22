# NomadicML Python SDK (v0.1.53) — Exhaustive API-Surface Map

Source: unpacked wheel at `/tmp/nomadic/sdk/nomadicml/`. All line references are to that tree.
The SDK targets the **DriveMonitor** backend (module docstring, `__init__.py:2-5`).

---

## 1. Public entry points

`from nomadicml import ...` exposes (`__init__.py:32-50`):

| Name | Kind | Defined at |
|---|---|---|
| `NomadicML` | main client class | `client.py:28` |
| `VideoClient` | video ops helper | `video.py:149` |
| `AnalysisType` | enum | `video.py:99` |
| `OverlayMode` | enum | `video.py:131` |
| `CloudIntegrationsClient` | cloud storage integrations | `cloud_integrations.py:37` |
| `LiveStreamClient` | livestream helper | `livestream.py:47` |
| `LiveSessionStatus` | enum | `livestream.py:32` |
| `NomadicMLError`, `AuthenticationError`, `APIError`, `VideoUploadError`, `AnalysisError` | exceptions | `exceptions.py` |
| `VideoSource`, `ProcessingStatus` | enums | `types.py:14,22` |
| `DEFAULT_BASE_URL` | `"https://api-prod.nomadicml.com/"` | `client.py:20` |
| `DEFAULT_COLLECTION_NAME` | `"videos"` | `client.py:21` |
| `DEFAULT_STRUCTURED_ODD_COLUMNS` | list of ODD column dicts | `video.py:6566` |

`__version__ = "0.1.53"`, `__build__ = "5e0b70a"` (`__init__.py:8-9`).
`__init__.py:24-30` monkey-patches `NomadicML.__init__` so every instance eagerly gets `client.video = VideoClient(client)` (also available lazily via `cached_property`, `client.py:94-104`; alias `client.videos`, `client.py:106-109`).

Note: `nomadicml/test.py` is a leftover scratch module defining alternative `VideoClient` sketches; it is **not imported** by `__init__.py` and is dead code.

### Constructor (`client.py:42-49`)

```python
NomadicML(
    api_key: str,                                   # required, non-empty string (utils.py:15-29)
    base_url: str = "https://api-prod.nomadicml.com/",   # trailing "/" stripped (client.py:54)
    timeout: int = 900,                             # DEFAULT_TIMEOUT, client.py:23
    collection_name: str = "videos",                # Firestore collection for videos
    folder_collection_name: str = "videoFolders",   # DEFAULT_FOLDER_COLLECTION_NAME, client.py:22
)
```

(A stale test at `tests/test_client.py:19` still asserts the old default `https://fdixgrmuam.us-west-2.awsapprunner.com` — the shipped code uses `api-prod.nomadicml.com`.)

Dashboard base URL for batch-viewer links (`video.py:1047-1060`): env `NOMADICML_DASHBOARD_BASE_URL`, else `https://app.nomadicml.com` when `collection_name == "videos"`, else `https://main.app.nomadicml.com`. Path pattern: `/use-cases/rapid-review/batch-view/{batch_id}`.

### Flat proxies on `NomadicML` (`client.py:130-260`)
`upload`, `create_or_get_folder`, `create_folder`, `get_folder`, `analyze`, `analyze_multiview`, `my_videos`, `delete_video`, `search`, `get_visuals`, `get_visual`, `get_batch_analysis`, `get_import_job`, `get_mcap_ingest`, `wait_for_mcap_ingest`, `get_mcap_import_job`, `wait_for_mcap_import_job`, `stitch_mcap`, `get_import_job_videos`, `get_import_job_uploaded_video_ids` (deprecated alias), `add_batch_metadata`, `geovisualizer`, `visualize`, `create_agent`, `update_agent`, `list_agents`, `generate_structured_odd` — all delegate to `client.video.*`.

`NomadicML.verify_auth()` → `POST /api/keys/verify` → JSON incl. `user_id` (`client.py:384-395`, `video.py:755-776`).

---

## 2. Public methods by concern

### 2a. Upload

**`VideoClient.upload(videos, /, *, name=None, folder=None, metadata_file=None, scope="user", upload_timeout=1_200, wait_for_uploaded=True, gcs_integration_id=None, integration_id=None, chunk_size=None, front_channel=None, channel_roles=None, channel_labels=None, **_)`** (`video.py:1512-1879`)

Accepted `videos` shapes:
- single local path/URL (`str | Path`) — extensions: `.mp4 .webm .mov .avi` for video, `.mcap` for MCAP (`utils.py:34-35`)
- `(video, metadata)` tuple; dict `{"video":..., "name":..., "metadata":...}`; list mixing all of these (parallel upload, max 4 workers, `video.py:2101`)
- cloud URIs: `gs://`, `s3://`, `hf://buckets/...` (provider detection `video.py:81-97`); cloud allows only `.mp4` and `.mcap` (`video.py:52`)
- multi-view mapping `{"front": ..., "rear": ...}` or list of view dicts (view keys `front/rear/back/left/right/top/bottom`, `video.py:1578`; `front` required)

HTTP flows:
- **Local file / HTTP URL** → `POST /api/upload-video` multipart form: `source` (`file`|`video_url`), `firebase_collection_name`, `scope`, optional `folder_id`, `chunk_size`, `video_url`, `custom_name`; file part `file`, optional part `metadata_file` (`video.py:4813-4851`). Returns backend JSON incl. `video_id`.
- Then, if `wait_for_uploaded`, polls `GET /api/video/{video_id}/status` (`get_video_status`, `video.py:4925-4948`) until metadata `visual_analysis.status.status == "UPLOADED"` or `chunks_uploaded >= chunks_total` (`_wait_for_uploaded`, `video.py:6220-6260`; exp backoff 15s→30s ±1s jitter). Final return: `{"video_id": ..., "status": "<lowercased status>"}` (`_parse_upload_response`, `video.py:542-548`).
- **GCS** → `POST /api/gcs/upload` `{integration_id, files:[object_names], collection, folder_id, scope}` → `{"import_job_id": ...}`; SDK returns `{"import_job_id": ..., "status": "importing"}` (async; `wait_for_uploaded` ignored) (`video.py:3953-4002, 4554-4565`).
- **S3** → `POST /api/s3/upload` `{keys, collection, folder_id, scope, bucket[, integration_id]}` → same import-job shape (`video.py:4004-4071`).
- **HF bucket** → `POST /api/hf-buckets/upload` `{files, collection, folder_id, scope, bucket[, integration_id]}` (`video.py:4141-4206`).
- **Local MCAP** → 3 steps (`_upload_mcap_source`, `video.py:4661-4741`): `POST /api/mcap/create-ingest` `{filename, size_bytes, sha256, content_type, folder_id, scope, chunk_size}` → `{mcap_ingest_id, upload_url, upload_headers, source_uri}`; raw `PUT` of file bytes to `upload_url`; `POST /api/mcap/{ingest_id}/process` `{front_channel, channel_roles, channel_labels}`. If waiting, polls `GET /api/mcap/{ingest_id}` until status in `{"completed","partial","failed"}` (`MCAP_TERMINAL_STATUSES`, `video.py:53`). Normalized payload adds `videos`, `video_ids`, `videos_by_channel`, `videos_by_role`, `primary_video_id`, `video_id` (`video.py:4602-4646`).
- **MCAP from S3** → `POST /api/mcap/cloud-ingest/s3` `{integration_id, files:[{key,filename}], folder_id, scope, chunk_size}` → `{mcap_import_job_id, ...}` (`video.py:4073-4139`); requires an `s3_storage_transfer` integration.
- **Multi-view local** → per-view uploads then `POST /api/multi-view/stitch` `{primary_view_id, views: {role: video_id}}` (`video.py:4534-4541`); returns front-view `{video_id, status}`.
- **Multi-view cloud** → `POST /api/gcs/upload` or `/api/s3/upload` with `sets: [{"views": {role: uri}}]` (`video.py:4208-4322`).

**Folders**:
- `create_or_get_folder(name, *, scope="user", org_id=None, description=None)` → `POST /api/folders/create-or-get` (`video.py:1881-1917`)
- `create_folder(name, *, scope="user", description=None)` → `POST /api/folders` (`video.py:1919-1952`)
- `get_folder(name, *, scope="user")` → `GET /api/folders/get?name=&scope=` (`video.py:1954-1979`)

**Import-job status**:
- `get_import_job(import_job_id)` → `GET /api/import-jobs/{id}` (`video.py:5023-5035`)
- `get_import_job_videos(id, *, limit=500, cursor=None, offset=None)` → `GET /api/import-jobs/{id}/videos` → `{videos:[{video_id,status,import_source_uri}], total, video_count, has_more, next_cursor}` (`video.py:5037-5068`)
- MCAP: `get_mcap_ingest(id)` → `GET /api/mcap/{id}`; `wait_for_mcap_ingest(id, *, timeout=1200)`; `get_mcap_import_job(id)` → `GET /api/mcap/import-jobs/{id}`; `wait_for_mcap_import_job(id, *, timeout=1200, poll_interval=10)`; `stitch_mcap(ingest_id, *, front_channel, channel_roles=None, channel_labels=None)` → `POST /api/mcap/{ingest_id}/stitch` (`video.py:4950-5021`)

**Listing / deletion**:
- `my_videos(folder=None, *, scope=None)` → `GET /api/my-videos?firebase_collection_name=&folder_collection=[&folder=][&scope=]` → list of `{video_id, video_name, duration_s, folder_id, status[, folder_name, org_id]}` (`video.py:6186-6211`)
- `delete_video(video_id)` → `DELETE /api/video/{video_id}?firebase_collection_name=` (`video.py:6213-6216`)

### 2b. Analyze

**`VideoClient.analyze(ids=None, /, *prompt_args, prompt=None, analysis_type=None, model_id="Nomadic-VL-XLarge", timeout=2_400, wait_for_completion=True, wait=None, folder=None, scope=None, search_query=None, custom_event=None, custom_category=None, concept_ids=None, mode=None, return_subset=False, is_thumbnail=False, use_enhanced_motion_analysis=False, haystack_search=False, confidence="low", custom_agent_id=None, custom_edge_case_agent_id=None, overlay_mode=None, **legacy_kwargs)`** (`video.py:2263-2459`)

Three dispatch paths:

1. **Modern prompt path** — `client.analyze(video_id, "detect hard braking events")`, optional `mode="thinking"|"fast"` (`PROMPT_ANALYSIS_MODES`, `video.py:54`). Rejects all legacy knobs (`_validate_prompt_analysis_options`, `video.py:2810-2866`: only `mode`, `wait`, `timeout` allowed).
   - fast: `POST /api/router/query` `{query, prefer_fast: true, quick_analysis: true, use_thinking: false, video_id|video_ids}` (`video.py:2961-2989`)
   - thinking: `POST /api/router/v2/query/start` `{query, client_info: "sdk-analyze-thinking", video_id|video_ids}` → `{stream_id}`, then SSE `GET /api/router/v2/query/events/{stream_id}?last_id=` until event `batch_created`/`done` yields `data.batch_id`; SSE `error` event raises (`video.py:2991-3195`). Fallback on 5xx: streaming `POST /api/router/v2/query/stream`. Reconnects: max 10, 1.0s delay (`video.py:57-58`).
   - Then polls `GET /api/batch/{batch_id}/status` and fetches results (below). Single-video return: `{video_id, analysis_id, mode, status, summary, events}`.
2. **Fixed edge-agents** (`analysis_type` in `_AGENT_DEFAULTS`) — `analyze_video_edge` → `POST /api/analyze-video-edge/{video_id}` form `{firebase_collection_name, model_id, edge_case_category, concepts_json, mode, assistant_edge_cases_json, config[, custom_edge_case_agent_id]}` (`video.py:248-277, 4893-4923`) → `{analysis_id}`; then `wait_for_analysis` + `get_video_analysis`; returns `{video_id, mode: "agent", status: "completed", events, analysis_id}`.
3. **Legacy ASK / CUSTOM_AGENT / ACTION_SEGMENTATION** — `_custom_event_detection` → `POST /api/ask` form `{question, video_id, is_thumbnail, use_enhanced_motion_analysis, config, confidence, custom_agent_id[, custom_workflow_name][, extract_frame_timestamps][, extract_frame_gps][, overlay_mode]}` (`video.py:1002-1028`). `question = f"{category}-----------EVENT_DESCRIPTION-----------{event_description}"` (`_BACKEND_SPLIT_SYMBOL`, `video.py:172,1000`). HTTP 202 → chunked; poll `GET /api/videos/{video_id}/analyses/{analysis_id}/status` (`_wait_for_rapid_review`, `video.py:6114-6183`) until `COMPLETED`; result `{answer, suggested_events, video_id, analysis_id, status}`. SDK return: `{video_id, analysis_id, mode: "rapid_review", status: "completed", summary, events}`.
   - Legacy `AnalysisType.ASK`+`custom_event` emits `FutureWarning`; hard removal date `"May 19, 2026"` (`LEGACY_ASK_DEPRECATION_DATE`, `video.py:55`; `LEGACY_ASK_HARD_ERROR = False`, `video.py:56`).

**Batch (multiple ids or `folder=`)** — `_analyze_many` (`video.py:3575-3762`):
- `POST /api/create-batch` form entries (`_prepare_batch_form`, `video.py:1097-1235`): repeated `video_ids`; `analysis_kind` = `"rapid_review"` (ask/custom_agent/action_segmentation) or `"edge_agent"` (agents); ask adds `prompt`, `category`, `concepts_json`, `config`, `confidence`, `is_thumbnail`, `use_enhanced_motion_analysis`, `use_embedding_search` (from `haystack_search`), overlay flags; agents add `model_id`, `edge_case_category`, `agent_mode`, `assistant_edge_cases_json`; always `("start","true")` and `client_batch_id` (uuid hex). Response must contain `batch_id`.
- Poll `GET /api/batch/{batch_id}/status` (interval 5s) — payload fields: `status` (`completed|failed|cancelled` terminal), `aggregated_progress: {total, completed}`, `videos: [{video_id, status, analysis_id, last_error, ...}]`, `config`, `created_at` (`video.py:1253-1304`).
- Bulk fetch: `POST /api/batch/{batch_id}/analyses/bulk` json `{video_ids: [...]}` (chunks of 100, ≤10 threads; backend limit 500) `?include_source_uri=true` → `{analyses:[{video_id, analysis_id, analysis, pointer, import_source_uri, filename}], unresolved_video_ids, not_found_analysis_ids}` (`video.py:1306-1417`).
- Return: `{"batch_metadata": {batch_id, batch_viewer_url, batch_type ("ask"|"agent")}, "results": [{video_id, analysis_id, mode, status, events[, summary][, import_source_uri][, error]}]}`.

**`analyze_multiview(view_dict, *, analysis_type, model_id="Nomadic-VL-XLarge", timeout=2_400, wait_for_completion=True, custom_event=None, custom_category=None, concept_ids=None, mode="assistant", return_subset=False, is_thumbnail=False, use_enhanced_motion_analysis=False, haystack_search=False, confidence="low", custom_agent_id=None, custom_edge_case_agent_id=None, overlay_mode=None, filter_results=False, top_k=None)`** (`video.py:2461-2611`): runs `analyze` per view (e.g. `{"FRONT":[ids], "REAR":[ids]}`), optionally `POST /api/batch/{batch_id}/sort_edge_cases` (uniqueness sort, `video.py:2640-2668`), then fuses via `POST /api/fuse_multiview_results` `{batch_ids, view_keys}` (`video.py:2613-2638`). Fused return has `view_types`, `fusion_method: "source_uri_matching"`, `results`, `unmatched_results`, `batch_ids_by_view`; fallback: `{batch_ids_by_view, batch_results}`.

**Low-level singles**:
- `analyze_video(video_id, model_id="Nomadic-VL-XLarge")` → `POST /api/analyze-video/{video_id}` form `{firebase_collection_name, model_id}` (`video.py:4860-4891`)
- `analyze_video_edge(video_id, agent_type, *, model_id="Nomadic-VL-XLarge", concept_ids=None, _config="default", custom_edge_case_agent_id=None)` (`video.py:4893-4923`)

### 2c. Status / results / events

- `get_video_status(video_id)` → `GET /api/video/{video_id}/status?firebase_collection_name=` (`video.py:4925-4948`)
- `wait_for_analysis(video_id, timeout=2_400, poll_interval=5, analysis_id=None)` (`video.py:5088-5155`): with `analysis_id` polls `get_video_analysis` and reads `payload["analysis"]["status"]`; terminal `{"COMPLETED","FAILED"}`. Without, polls `get_video_status` `payload["status"]`.
- `wait_for_analyses(video_ids, timeout=4800, poll_interval=5)` — parallel (`video.py:5157-5176`)
- `get_video_analysis(video_id, analysis_id=None)`: with id → `GET /api/videos/{video_id}/analyses/{analysis_id}?firebase_collection_name=`; without → legacy `GET /api/video/{video_id}/analysis?firebase_collection_name=` (`video.py:5178-5217`)
- `get_video_analyses(video_ids)` — sequential loop (`video.py:5219-5237`)
- `get_detected_events(video_id)` → parses events out of `get_video_analysis` (`video.py:5239-5253`)
- `get_batch_analysis(batch_id, filter=None, as_csv=False)` (`video.py:5255-5427`): status + bulk fetch; `filter` ∈ `{'approved','rejected','pending','invalid'}` (approval filter, client-side). `batch_metadata` includes `batch_id, batch_viewer_url, batch_type, analysis_type, created_at`, and for ask: `prompt, category, is_thumbnail, use_enhanced_motion_analysis`. CSV columns (`video.py:5523-5543`): `Query, Video Name, Approval Status, Timestamp, unix_timestamp_start, unix_timestamp_end, Category, Label, AI Analysis, Severity, Video ID, Analysis ID, Batch ID, Batch Viewer URL, Status, Confidence, Annotated Thumbnail URL, Import Source URI, Summary`.
- `add_batch_metadata(batch_id, metadata)` → `POST /api/batch/{batch_id}/metadata` json `{"metadata": "<json string>"}`; flat str/int values only (`video.py:5908-5958`)
- `get_visuals(video_id, analysis_id)` → `POST /api/videos/{video_id}/analyses/{analysis_id}/generate-thumbnails` form `{firebase_collection_name}`; returns list of `annotated_thumbnail_url` strings (`video.py:6301-6339`)
- `get_visual(video_id, analysis_id, event_idx)` — indexes into `get_visuals` (`video.py:6341-6368`)
- `visualize(result_or_batch=None, *, batch_id=None, width=860, display=True, output_path=None, expires_in=900, only_with_events=False)` — self-contained HTML viewer; uses `POST /api/video/{video_id}/signed-url` json `{"expires_in": 900}` → `{"url"}` (`video.py:5552-5792`)
- `geovisualizer(batch_id, *, filter=None)` — GeoJSON FeatureCollection from events having `overlay.frame_gps_lat/frame_gps_lon`; properties: `id, video_id, analysis_id, label, category, severity, approval, t_start, t_end, start_seconds, end_seconds, video_offset, annotated_thumbnail_url, type ("point"|"path")` (`video.py:5794-5906`)
- `generate_structured_odd(video_id, *, columns=None, reasoning_trace_path=None, timeout=None)` → `POST /api/ask-question` form `{question: "odd_export", prompt_type: "odd_export", video_id, reasoning_trace_path, custom_columns}` → `StructuredOddResult {csv, share_id, share_url, processing_time, reasoning_trace_path, columns, raw}` (`video.py:869-956`). Reasoning path default: `user-status/{pro|dev}/users/{user_id}/reasoning-traces/structured-output` (`video.py:902-911`); env override `DRIVEMONITOR_IS_PROD` (`video.py:778-790`).

### 2d. Search

`search(*, query, folder_name, scope="user")` (`video.py:5964-6085`):
1. `POST /api/search-sessions/start` json `{query, folder_name, scope}` where scope maps `user→"my"`, `org→"org"`, `sample→"sample"` → `{session_id, owner_uid, session_doc_path, reasoning_trace_path}`
2. `POST /api/search?folder_collection={scope}` form `{query, folder, session_id, session_doc_path, reasoning_trace_path[, is_sample_videos]}`
3. Poll `GET /api/search-sessions/{owner_uid}/{session_id}` until `data.status == "completed"` (backoff 1s×1.5 → max 10s; overall timeout = `client.timeout`).
Return: `{"summary", "thoughts", "matches": [{video_id, analysis_id, event_index, similarity, reason}], "session_id"}`.
Deprecated: `apply_search(...)` raises (`video.py:6091-6100`); `AnalysisType.SEARCH`/`search_query` removed (`video.py:2743-2754`).

### 2e. Custom agents (fine-tuned)

- `create_agent(name, batch_ids=[], analysis_ids=[], wait_for_completion=False)` → `POST /api/create-agent` json `{batch_ids, analysis_ids, name, wait_for_completion, client_agent_id}` (idempotency uuid), timeout 10_800s; returns dict incl. `job_id` (`video.py:6370-6434`)
- `update_agent(agent_id, batch_ids=[], analysis_ids=[], wait_for_completion=False)` → `POST /api/update-agent`; returns incl. `update_type` (`"prompt_optimization"|"finetuning"`), `total_approved`, `total_rejected` (`video.py:6436-6507`). `analysis_ids` format: `"video_id:analysis_id"`.
- `list_agents(scope="user")` → `POST /api/list-agents` json `{scope}` → `result["agents"]`: `[{agent_id, name, status}]` (`video.py:6509-6565`)

### 2f. Livestream (`livestream.py`)

- `attach_stream(stream_id, stream_name, source_url)` → `POST /api/live/attach-stream` (form) → `{"ok": true}` (:64-97)
- `start_session(source_url, name, rapid_review_query=None, stream_id=None)` → `POST /api/live/start-session` (form) → `{"session_id": ...}` (:103-158)
- `end_session(stream_id, session_id)` → `POST /api/live/end-session` → `{"status": "ended"|"already_ended"}` (:160-194)
- `get_sessions(scope=None)` (`None`/`"personal"`/`"org"`) → `GET /api/live/live-sessions[?scope=]` → `sessions` list; each has `session_id, stream_id, name, source_url, status, created_by, created_at, chunk_count, chunks, events` (:200-244)
- `get_session(stream_id, session_id)` → `GET /api/live/live-sessions/{stream_id}/{session_id}` (:246-267)
- `get_signed_manifest(session_id)` → `POST /api/live/session/{session_id}/signed-manifest` → `{url, expires_at, method: "GET"}` (:273-299)
- `monitor_session(stream_id, session_id, *, poll_interval=5.0, timeout=None, on_update=None)` — poll until status ∈ `{FINISHED, FAILED}` (:305-378)
- `iter_events(stream_id, session_id, *, poll_interval=5.0, timeout=None)` — generator; de-dupes by `event_id`/`id` else `(chunk_index, chunk_relative_time, description)` (:380-443). Live events carry `type`, `description` fields (:404-406).
- `LiveSessionStatus`: `INITIALIZING, ACTIVE, ENDING, FINISHED, FAILED` (:32-39)

### 2g. Cloud integrations (`cloud_integrations.py`)

- `list(*, type=None)` → `GET /api/cloud-integrations` → list of `CloudIntegration` TypedDict: `{id, name, type ("gcs"|"s3"|"hf_bucket"|"s3_storage_transfer"), bucket, prefix, region, endpoint_url, role_arn, created_at, last_used, created_by, created_by_display_name, is_owner}` (:16-70)
- `add(*, type, name, bucket, credentials, prefix=None, region=None, endpoint_url=None)`:
  - gcs → `POST /api/cloud-integrations/gcs` `{name, type, service_account, bucket, prefix}`
  - s3 → `POST /api/cloud-integrations/s3` `{name, type, access_key_id, secret_access_key, session_token, region, endpoint_url, bucket, prefix}` (region required unless endpoint_url; then `"auto"`)
  - hf_bucket → `POST /api/cloud-integrations/hf-bucket` `{name, type, token, bucket, prefix}` (:72-170)
- `add_hf_bucket(*, name, bucket, token, prefix=None)` (:172-187)
- `get_s3_storage_transfer_setup()` → `GET /api/cloud-integrations/s3-storage-transfer/setup` (:189-198)
- `add_s3_storage_transfer(*, name, bucket, role_arn, prefix=None)` → `POST /api/cloud-integrations/s3-storage-transfer` (:200-231)

---

## 3. The analysis model

### AnalysisType enum — verbatim values (`video.py:99-122`)

| Member | Value |
|---|---|
| `ASK` | `"rapid_review"` (legacy Ask; prompt path replaces it) |
| `GENERAL_AGENT` | `"edge_case_agent"` |
| `LANE_CHANGE` | `"lane_change_agent"` |
| `TURN` | `"turn_agent"` |
| `RELATIVE_MOTION` | `"relative_motion_agent"` |
| `DRIVING_VIOLATIONS` | `"violation_agent"` |
| `CUSTOM_AGENT` | `"custom_agent"` |
| `ACTION_SEGMENTATION` | `"action_segmentation"` |
| `SEARCH` | `"search"` (deprecated) |
| aliases | `AGENT_GENERAL`, `LANE_CHANGE_AGENT`, `TURN_AGENT`, `RELATIVE_MOTION_AGENT`, `VIOLATION_AGENT`, `EDGE_CASE_AGENT` |

String aliases accepted by `_coerce_analysis_type` (`video.py:2874-2893`): `ask`, `general`, `general_agent`, `general-edge-case`, `edge_case_agent`, `lane_change`, `lane-change`, `lane_change_agent`, `turn`, `turn_agent`, `relative_motion`, `relative-motion`, `relative_motion_agent`, `driving_violations`, `driving-violations`, `violation_agent`, `action_segmentation`, `action-segmentation`.

Other enums:
- `CustomCategory` (`video.py:124-129`): `driving`, `robotics`, `aerial`, `security`, `environment` (default category is `'driving'`, `video.py:999,1144`).
- `OverlayMode` (`video.py:131-135`): `timestamps` (→ form `extract_frame_timestamps=true`), `gps` (→ `extract_frame_timestamps` + `extract_frame_gps`), `custom` (→ `overlay_mode=true`).
- `ProcessingStatus` (`types.py:22-31`): `uploading, uploading_failed, uploaded, processing, analyzing, completed, failed`.
- `VideoSource` (`types.py:14-19`): `file, saved, video_url`.
- Internal status ranks (`video.py:158-170`): `NOT_STARTED, PREPARE_IN_PROGRESS, PREPARE_COMPLETED, UPLOADED, DETECTING_IN_PROGRESS, PROCESSING, DETECTING_COMPLETED, DETECTING_COMPLETED_NO_EVENTS, SUMMARIZING_IN_PROGRESS, SUMMARIZING_COMPLETED, COMPLETED`.
- Prompt modes: `{"thinking", "fast"}` (`video.py:54`); default model id everywhere: **`"Nomadic-VL-XLarge"`**.

### Polling & streaming

- Prompt "thinking" uses **SSE** (`GET /api/router/v2/query/events/{stream_id}`; events: `batch_created`, `done`, `error`, generic `message`; fields `id:`, `event:`, `data:` JSON; `data.batch_id`, `data.error`) (`video.py:3067-3264`). Everything else is **HTTP polling** (batch status every 5s; analysis every 5s; upload status exp backoff; search 1s→10s).
- Rapid-review chunked status payload fields: `status`, `progress`, `chunks_completed`, `chunks_total`, `events`, `answer` (str or list) (`video.py:6120-6156`).

### Analysis document / events payload shapes

Event array candidate keys, in frontend-parity order (`_get_api_events`, `video.py:352-424`): `analysis.events`, then for agent docs `analysis.detected_events`, `analysis.detectedEvents`, `analysis.edge_case_events`, `analysis.edgeCaseEvents`, `analysis.result.events`, then `analysis.visual_analysis.events`; legacy fallbacks `metadata.visual_analysis.events` and `events.visual_analysis.status.quick_summary.events`. Analysis doc summary keys: `analysis.answer` or `analysis.summary`; legacy `metadata.visual_analysis.status.quick_summary.answer` (`video.py:1441-1463`). Analysis id extraction keys: `analysis_id`, `analysis.analysis_id`, `metadata.analysis_id`, `metadata.visual_analysis.analysis_id|analysisId` (`video.py:1419-1439`).

**`RapidReviewEvent`** (SDK-facing, `types.py:34-46`):
```
t_start: str  ("MM:SS" or "HH:MM:SS")
t_end: str
category: str
label: str
severity: str
aiAnalysis: str
confidence: float          (default 0.85 when converting; coerced, fallback 0.0)
annotated_thumbnail_url: Optional[str]
approval: str              (default "pending")
overlay: Optional[Dict[str, {"start", "end"}]]
```

**`UIEvent`** (Firestore storage format, `types.py:49-59`):
```
type: str        # maps to category
time: str        # "t=X.XX"
end_time: str    # "t=X.XX"
severity: str
description: str # maps to label
dmvRule: str
aiAnalysis: str
data: dict       # original event data
approval: str
```
Conversion UI→RapidReview at `video.py:646-752`: `type→category`, `description→label`, `time→t_start`, `end_time→t_end`; severity default `"medium"`; carries `frame_timestamp_start/_end`, `unix_timestamp_start/_end`, and all `frame_*_start|_end` keys (GPS lat/lon floated).

**Legacy agent event shape** (parsed output, `video.py:482-537`): `{label, start_time: float, end_time: float}`; sourced from `description`, `time` (`t=..` regex), `end_time`, and optional `refined_events` JSON list of `[start, end, text]`.

**Overlay map**: keys promoted from `frame_*` / `unix_timestamp` prefixed `*_start`/`*_end` pairs into `event["overlay"] = {base: {"start", "end"}}` (`_OVERLAY_PREFIXES = ("frame_", "unix_timestamp")`, `video.py:568-629`). GPS overlay keys used by geovisualizer: `frame_gps_lat`, `frame_gps_lon`.

**Normalized SDK result** (single analysis): `{video_id, analysis_id, mode, status, summary, events}`; mode values seen: `"rapid_review"`, `"agent"`, `"action_segmentation"`, `"ask"` (batch), `"thinking"|"fast"` (prompt path). Status values: `"started"`, `"completed"`, `"failed"`.

Raw `/api/ask` response fields: `answer`, `suggested_events`, `analysis_id` (`video.py:3507-3537`); batch pointer fields: `status`, `analysis_id`, `last_error` (`video.py:3690-3699`).

---

## 4. Domain vocabulary (verbatim strings)

**Agent categories** (`edge_case_category` form values, `video.py:174-195`): `"agent_mode_placeholder"` (general, mode `"agent"`), `"Lane Change Detection"`, `"Vehicle Turns"`, `"Relative Motion Analysis"`, `"Driving Violations"` (all mode `"assistant"`).

**Assistant edge-case presets** (`video.py:197-246`), `{title, description, importance}`:
- lane change: title `"lane change"` — "Detect instances where the ego vehicle crosses lane markings to change lanes (left or right)." (80)
- turn: `"vehicle turns"` — "Detect left or right turns at intersections or driveways." (80)
- relative motion: `"relative motion"` — "Detect significant relative motion patterns between ego and surrounding vehicles (approach, overtake, diverge)." (70)
- violations: `"speeding"` (90), `"running red light"` (95), `"failure to stop"` (85), `"improper lane usage"` (80), `"following too closely"` (75) — descriptions reference posted speed limits, traffic signal turning red, complete stops at stop signs / right turns on red, wrong lane / solid lines / emergency/HOV lanes, tailgating.

**Event fields**: `label`, `category`, `severity` (`low|medium|high` implied; default `"medium"`), `aiAnalysis`, `dmvRule` (UIEvent, `types.py:56` — DMV rule reference), `approval` ∈ `{approved, rejected, pending, invalid}` (`video.py:5288`), `confidence`, `t_start/t_end`, `time`/`end_time` (`"t=X.XX"`), `start_time`/`end_time` (float seconds), `frame_timestamp_start/_end`, `unix_timestamp_start/_end`, `frame_gps_lat`, `frame_gps_lon`, `annotated_thumbnail_url`, `refined_events`, `suggested_events`, `detected_events`/`edge_case_events`, `uniqueness_rating`, `uniqueness_reasoning` (sort_edge_cases, `video.py:2675-2687`).

**Canonical example prompt**: `"detect hard braking events"` (`video.py:63, 73`); livestream examples: `"detect hard braking or lane departures"`, `"detect pedestrians entering the road"` (`livestream.py:122,140`).

**Structured ODD vocabulary** (`DEFAULT_STRUCTURED_ODD_COLUMNS`, `video.py:6566-6711`, ASAM OpenODD-aligned): columns `timestamp`, `comment`, `scenery.road.type` (`motorway, rural, urban_street, parking_lot, unpaved, unknown`), `scenery.road.number_of_lanes`, `scenery.road.lane_marking_type` (`clear, blurred, temporary_yellow, none, unknown`), `scenery.road.surface_condition` (`dry, wet, icy, snow_covered, leaves_debris, potholes, uneven, unknown`), `scenery.road.grade_category` (`level, slight_incline, steep_incline, slight_decline, steep_decline, unknown`), `scenery.road.speed_limit` (km/h), `scenery.road.is_construction_zone`, `scenery.junction.type` (`none, t_junction, four_way, roundabout, merge_lane, exit_lane, unknown`), `scenery.junction.traffic_control` (`none, traffic_light, stop_sign, yield_sign, uncontrolled, unknown`), `scenery.junction.is_signalized`, `scenery.participants.{pedestrian,cyclist,car,truck}.count`, `scenery.participants.emergency_vehicle.is_present`, `environment.weather.precipitation_type` (`none, rain, snow, hail, sleet`), `environment.weather.precipitation_intensity` (`none, light, moderate, heavy, violent`), `environment.weather.fog_density` (`none, light, moderate, dense`), `environment.weather.is_sun_glare`, `environment.weather.lighting_condition` (`daylight, dusk_dawn, night_well_lit, night_unlit, tunnel`).

Other terms: "edge case" / "edge-agent" / `analysis_kind` ∈ `{"rapid_review", "edge_agent"}`; "rapid review"; "haystack search" → form key `use_embedding_search`; "enhanced motion analysis"; "concepts" (`concept_ids` → `concepts_json`); "ego vehicle"; robotic workflow `"Robotic Action Segmentation"` with `custom_workflow_name="action-segmentation"` (`video.py:1129-1133, 3465-3480`).

---

## 5. Auth + error model

**Headers** — session-level (`client.py:61-64`): `X-API-Key: <api_key>`, `User-Agent: NomadicML-Python-SDK/<version>`. Per-request (`client.py:307-317`): `Authorization: Bearer <api_key>` (so both header styles are sent), `X-Client-Type: SDK`, `X-Client-Version`, `User-Agent`, `X-Request-ID` (uuid4), and `Idempotency-Key` (same uuid) on POST/PUT/PATCH/DELETE.

**Exceptions** (`exceptions.py`): `NomadicMLError` (base) ← `AuthenticationError`, `APIError(status_code, message, details)` (str: `"API Error ({status_code}): {message}"`), `VideoUploadError`, `AnalysisError`, `ValidationError`. 401 → `AuthenticationError` (special-cased message when body mentions "hugging face"/"hf bucket", `client.py:361-366`); other ≥400 → `APIError`; network → `NomadicMLError("Request failed: ...")`. Error message extraction order: `detail` (incl. FastAPI validation list `loc`/`msg`), `message`, `error` (`utils.py:94-119`).

**Retries** — two layers (`client.py:66-88, 319-338`):
1. urllib3 `Retry`: status-only, 3 retries, `backoff_factor=0.5`, `status_forcelist=[408, 429, 500, 502, 503, 504, 520-527]`, all methods, respects `Retry-After`. Pool: 100 connections / 100 per host.
2. `backoff.expo` decorator: on `SSLError, ConnectionError, Timeout, ChunkedEncodingError, ReadTimeout`; `max_tries=4`, `max_time=300`, random jitter.

Extended timeouts: uploads and MCAP calls use `client.timeout * 20` (`video.py:4109, 4697, 4709, 4725, 4850`); agent creation 10_800s.

---

## 6. Minimal re-implementation: the 5-6 core calls

Base URL `https://api-prod.nomadicml.com`; send `Authorization: Bearer <API_KEY>` (or `X-API-Key`).

1. **Verify** (optional): `POST /api/keys/verify` → `{user_id, ...}`.
2. **Upload**: `POST /api/upload-video` — multipart form `source=file`, `firebase_collection_name=videos`, `scope=user`, file part `file=(name, bytes, mime)` → `{video_id, ...}`. Poll `GET /api/video/{video_id}/status?firebase_collection_name=videos` until `metadata.visual_analysis.status.status == "UPLOADED"`.
3. **Analyze (prompt, fast)**: `POST /api/router/query` json `{"query": "<prompt>", "video_id": "<id>", "prefer_fast": true, "quick_analysis": true, "use_thinking": false}` → `{batch_id}` or `{analysis_id}`/immediate `result`. (Thinking mode: `POST /api/router/v2/query/start` then SSE `GET /api/router/v2/query/events/{stream_id}` for `batch_created` → `batch_id`.)
4. **Poll**: `GET /api/batch/{batch_id}/status` until `status ∈ {completed, failed, cancelled}`; read `videos[].{video_id, analysis_id, status}`. (Single analysis: `GET /api/videos/{video_id}/analyses/{analysis_id}` until `analysis.status == "COMPLETED"`.)
5. **Get events**: `POST /api/batch/{batch_id}/analyses/bulk` json `{"video_ids": [...]}` → `analyses[].analysis.events` (UI format: `type/time/end_time/severity/description/aiAnalysis/approval/data`) — or `GET /api/videos/{video_id}/analyses/{analysis_id}` and read `analysis.events` (agent docs may use `detected_events`/`edge_case_events`). Convert `"t=X.XX"` → seconds; `description→label`, `type→category`.
6. **Search**: `POST /api/search-sessions/start` json `{query, folder_name, scope: "my"}` → session; `POST /api/search?folder_collection=my` form `{query, folder, session_id, session_doc_path, reasoning_trace_path}`; poll `GET /api/search-sessions/{owner_uid}/{session_id}` until `data.status == "completed"`; read `data.matches[].{video_id, analysis_id, event_index, similarity, reason}`, `data.summary`, `data.thoughts`.
