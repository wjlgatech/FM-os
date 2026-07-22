> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cloud Imports (GCS / S3 / Cloudflare R2 / Hugging Face Buckets)

> Import videos directly from cloud storage

#### upload() for cloud URIs

Provide full `gs://`, `s3://`, or `hf://buckets/...` URIs to import videos from cloud storage.

```python title="Cloud import examples" theme={null}
# Import from GCS
batch = client.upload([
  "gs://drive-monitor/uploads/trip-042/front.mp4",
  "gs://drive-monitor/uploads/trip-042/rear.mp4",
])
# Returns: {"import_job_id": "ij_xxx", "status": "importing"}

# Import from S3 with a specific integration
client.upload(
    "s3://drive-monitor-archive/2024-09-01/front.mp4",
    integration_id="aws-prod",
)

# Import from Cloudflare R2 after saving it as an S3-compatible integration
client.upload(
    "s3://customer-r2/incoming/front.mp4",
    integration_id="r2-prod",
)

# Import into a folder
client.upload(
    ["s3://my-bucket/videos/clip_001.mp4", "s3://my-bucket/videos/clip_002.mp4"],
    folder="fleet_uploads",
    scope="org",
)

# Import from a Hugging Face bucket
client.upload(
    "hf://buckets/JohnnyMnenonic/test/incoming/front.mp4",
    integration_id="hf-bucket-prod",
)
```

**Cloud-specific parameter:**

| Parameter        | Type  | Default | Description                                                                                                                                     |
| ---------------- | ----- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `integration_id` | `str` | `None`  | Saved cloud integration identifier to use for imports. When omitted, the backend resolves access from the bucket when the provider supports it. |

All other parameters (`folder`, `scope`, etc.) are shared with local uploads — see the [full parameter table](/sdk/uploading-videos/local-files-urls).

**Returns:** `{"import_job_id": "ij_xxx", "status": "importing"}`

<Note>
  Cloud imports accept `.mp4` objects referenced by full `gs://bucket/object.mp4`, `s3://bucket/object.mp4`, or `hf://buckets/namespace/name/object.mp4` URIs. Wildcard patterns are not supported—list each object explicitly. For Hugging Face buckets, when no `integration_id` is provided the backend first checks for a saved `hf_bucket` integration matching the bucket and otherwise falls back to public bucket access automatically.
</Note>

<Note>
  For S3-compatible providers such as Cloudflare R2, keep using `s3://bucket/object.mp4` URIs. The provider-specific endpoint belongs on the saved cloud integration, not in the import URI itself.
</Note>

<Note>
  Cloud import requests are acknowledged asynchronously. Even when a request later fails validation or authorization in background processing, the API still returns an `import_job_id`; those failures surface as `UPLOADING_FAILED` rows in `get_import_job_videos()`.
</Note>

#### Managing Cloud Integrations

Use this helper to manage reusable GCS/S3 credentials for cloud imports. See [Cloud Storage Uploads](/sdk/cloud-storage) for instructions on creating service-account keys and web UI setup.

```python title="Cloud integrations helper" theme={null}
# List every integration visible to your user/org
client.cloud_integrations.list()

# Filter by provider
client.cloud_integrations.list(type="gcs")

# Add a new GCS integration using a service account JSON file
client.cloud_integrations.add(
    type="gcs",
    name="Fleet bucket",
    bucket="drive-monitor",
    prefix="uploads/",
    credentials="service-account.json",  # path or dict/bytes
)

# Add a new S3 integration
client.cloud_integrations.add(
    type="s3",
    name="AWS archive",
    bucket="drive-archive",
    prefix="raw/",
    region="us-east-1",
    credentials={
        "accessKeyId": "...",
        "secretAccessKey": "...",
        "sessionToken": "...",  # optional
    },
)

# Add a Cloudflare R2 integration using the same S3 helper
client.cloud_integrations.add(
    type="s3",
    name="Customer R2",
    bucket="customer-r2",
    prefix="incoming/",
    endpoint_url="https://<account>.r2.cloudflarestorage.com",
    region="auto",
    credentials={
        "accessKeyId": "...",
        "secretAccessKey": "...",
    },
)

# Import from R2 using a normal s3:// URI and the saved integration id
client.upload(
    "s3://customer-r2/incoming/front.mp4",
    integration_id="r2-prod",
)
```

For Cloudflare R2 and other S3-compatible providers, keep using `s3://bucket/key.mp4`
URIs in `client.upload(...)`. The custom endpoint stays on the saved integration
via `endpoint_url`; it does not go into the import URI.

#### Multi-view (cloud)

Cloud multi-view uploads use dict mappings with `gs://` or `s3://` URIs. `front` is required in every set.

```python theme={null}
# Single cloud multi-view set
multi = client.upload(
  {
    "front": "s3://drive-monitor/uploads/trip-042/front.mp4",
    "left": "s3://drive-monitor/uploads/trip-042/left.mp4",
    "right": "s3://drive-monitor/uploads/trip-042/right.mp4",
  },
  folder="fleet_uploads",
  scope="org",
)
# Returns: {"import_job_id": "ij_xxx", "status": "importing"}
```

* Multiple cloud multi-view sets submitted in one `upload([...])` call produce one import job.
* `wait_for_uploaded=True` is ignored for cloud multi-view uploads.
* For multi-view import jobs, `client.get_import_job_videos()` returns front rows only and `total` is the requested set count.

#### get\_import\_job()

Fetch metadata for a cloud import job.

```python theme={null}
upload = client.upload(
    [
        "s3://drive-monitor-archive/2024-09-01/front.mp4",
        "s3://drive-monitor-archive/2024-09-01/rear.mp4",
    ],
    wait_for_uploaded=False,
)

job = client.get_import_job(upload["import_job_id"])
print(job["job_id"], job["total"])
```

**Required Parameters:**

| Parameter       | Type  | Description                                |
| --------------- | ----- | ------------------------------------------ |
| `import_job_id` | `str` | Cloud import job ID returned by `upload()` |

**Returns:** Dict with job metadata fields such as:

* `job_id`
* `source` (`"s3"`, `"gcs"`, or `"hf_bucket"`)
* `bucket`
* `prefix`
* `folder_id`
* `folder_name`
* `total`
* timestamps (`created_at`, `completed_at`, `updated_at` when available)

#### Hugging Face integrations via the SDK

If you want to create and reuse a saved Hugging Face integration from the SDK,
create it with the cloud integrations helper and then pass its
`integration_id` into `upload()`:

```python theme={null}
integration = client.cloud_integrations.add_hf_bucket(
    name="HF footage",
    bucket="JohnnyMnenonic/test",
    token="hf_xxx",
    prefix="incoming/",
)

result = client.upload(
    "hf://buckets/JohnnyMnenonic/test/incoming/front.mp4",
    integration_id=integration["id"],
    wait_for_uploaded=False,
)
```

Prefer a fine-grained token if Hugging Face supports the required bucket
access. If bucket-specific scoping is unavailable, use a dedicated token or
account reserved for storage imports.

Outside of integration creation, the SDK does not accept Hugging Face tokens.
Use `client.upload("hf://buckets/...")` with an `integration_id`, or omit
`integration_id` and let the backend resolve a saved integration or public
access for that bucket.

<Note>
  For high-volume imports, treat `total` + `client.get_import_job_videos()` as the readiness contract.
</Note>

#### get\_import\_job\_videos()

Fetch paginated per-video upload statuses for a cloud import job.

This endpoint is designed for large import jobs where returning all rows in one
response would be expensive (for example, thousands to hundreds of thousands of
videos). For jobs with more than \~1,000 videos, prefer cursor-based pagination
(`limit` + `cursor`) instead of requesting everything at once.

```python theme={null}
upload = client.upload(
    [
        "gs://drive-monitor/uploads/trip-042/front.mp4",
        "gs://drive-monitor/uploads/trip-042/rear.mp4",
    ],
    wait_for_uploaded=False,
)

cursor = None  # First page: no cursor
while True:
    result = client.get_import_job_videos(
        upload["import_job_id"],
        limit=500,
        cursor=cursor,  # Pass cursor from previous response
    )

    print(result["import_job_id"])
    print(result["video_count"], result["has_more"], result["next_cursor"])  # page_size, more pages?, next anchor
    print(result["videos"][:3])  # [{video_id, status, import_source_uri}, ...]

    if not result["has_more"]:
        break
    cursor = result["next_cursor"]  # Use this value for the next page
```

**Required Parameters:**

| Parameter       | Type  | Description                                |
| --------------- | ----- | ------------------------------------------ |
| `import_job_id` | `str` | Cloud import job ID returned by `upload()` |

**Optional Parameters:**

| Parameter | Type  | Default | Description                                                                                                |
| --------- | ----- | ------- | ---------------------------------------------------------------------------------------------------------- |
| `limit`   | `int` | `500`   | Max videos to return in one page                                                                           |
| `cursor`  | `str` | `None`  | Last `video_id` from previous page                                                                         |
| `offset`  | `int` | `None`  | Offset-based fallback pagination (do not combine with `cursor`). Not supported for multi-view import jobs. |

**Returns:** Dict with:

* `import_job_id`
* `total` (requested count for this job; for multi-view jobs this is the requested set count)
* `limit`
* `cursor`
* `has_more`
* `next_cursor`
* `videos` (list of `{video_id, status, import_source_uri}` entries for detailed polling; multi-view jobs return front rows only)
* `video_count`

**Cursor Notes:**

* `cursor` is the last `video_id` from the previous response's `next_cursor`.
* Start with `cursor=None` for the first page.
* Stop paging when `has_more` is `False`.
* Prefer `cursor` pagination for large jobs; `offset` is mainly a fallback/debug option.
* Do not pass both `cursor` and `offset` in the same request.
* For multi-view cloud imports, `videos` contains currently materialized IDs (best-effort); use `total` as the requested target count.

<Note>
  `client.get_import_job_uploaded_video_ids()` remains available as a deprecated alias of `client.get_import_job_videos()`.
</Note>

#### End-to-end cloud import example

```python theme={null}
import time

# 1. Start the cloud import — returns an import_job_id, NOT a video_id
result = client.upload([
    "s3://my-bucket/videos/clip_001.mp4",
    "s3://my-bucket/videos/clip_002.mp4",
    "s3://my-bucket/videos/clip_003.mp4",
])
print(result)
# {"import_job_id": "ij_a1b2c3d4e5f6", "status": "importing"}

job_id = result["import_job_id"]

# 2. Poll import-job videos until returned IDs reach the requested total
#    and each returned row is terminal.
TERMINAL = {"UPLOADED", "UPLOADING_FAILED"}
seen = {}
while True:
    job = client.get_import_job(job_id)
    target_total = int(job.get("total") or 0)
    cursor = None
    while True:
        page = client.get_import_job_videos(job_id, limit=500, cursor=cursor)
        for row in page["videos"]:
            seen[row["video_id"]] = row["status"]
        if not page["has_more"]:
            break
        cursor = page["next_cursor"]

    if target_total > 0:
        all_ids_materialized = len(seen) >= target_total
        all_terminal = all(status in TERMINAL for status in seen.values())
        print(f"Import progress: ids={len(seen)}/{target_total}")
        if all_ids_materialized and all_terminal:
            break
    time.sleep(10)

# 3. Use uploaded IDs for analysis
video_ids = [vid for vid, status in seen.items() if status == "UPLOADED"]

print(f"Imported {len(video_ids)} videos: {video_ids[:5]}...")

# 4. Now use the video IDs for analysis
client.analyze(
    video_ids,
    prompt="detect lane departure events",
)
```
