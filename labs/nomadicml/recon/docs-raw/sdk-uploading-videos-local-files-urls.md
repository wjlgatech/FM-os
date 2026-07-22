> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Local File & URL Uploads

> Upload local files, URLs, MCAPs, and multi-view sets

Upload local files or HTTP/HTTPS URLs. Returns a `video_id` per video.

```python title="Local file & URL upload examples" theme={null}
# Single local file
result = client.upload("video.mp4")

# Single video with custom display name
result = client.upload("video.mp4", name="Morning Commute.mp4")

# Single video with metadata
result = client.upload(("video.mp4", "video.json"))

# Multiple local files
batch = client.upload(["a.mp4", "b.mp4"])

# Multiple videos with mixed metadata
batch = client.upload([
    ("video1.mp4", "video1.json"),     # Video with metadata
    "video2.mp4",                       # Video without metadata
    ("video3.mp4", "video3.json")      # Another video with metadata
])

# Batch upload with per-video custom names (dict syntax)
batch = client.upload([
    {"video": "dashcam_001.mp4", "name": "Trip to Downtown"},
    {"video": "dashcam_002.mp4", "name": "Highway Merge"},
    {"video": "dashcam_003.mp4", "name": "Parking Lot Exit", "metadata": "trip3.json"}
])

# Public GCS URL (any accessible HTTPS URL)
remote = client.upload("https://storage.googleapis.com/my-bucket/videos/demo.mp4")

# URL with custom display name
remote = client.upload(
    "https://storage.googleapis.com/my-bucket/videos/scene-1.mp4",
    name="scene_1.mp4"
)

# With folder organization
result = client.upload("video.mp4", folder="my_folder")

# With metadata JSON file and folder
result = client.upload(("dashcam.mp4", "dashcam.json"), folder="fleet_videos")

# Organization scope
result = client.upload("launch.mp4", folder="robotics_org", scope="org")
```

#### Local MCAP Uploads

Upload local `.mcap` files through the same `upload()` helper. The initial response
contains an `mcap_ingest_id`; wait for completion to retrieve the derived videos.

```python title="Local MCAP upload" theme={null}
queued = client.upload("sample.mcap")

final = client.wait_for_mcap_ingest(queued["mcap_ingest_id"])
print("video_ids:", final["video_ids"])
print("videos_by_channel:", final.get("videos_by_channel", {}))
```

#### S3 MCAP Cloud Ingest

For large MCAPs already stored in S3, create a role-based S3 Storage Transfer
integration, then pass the `s3://...mcap` URI to `upload()`. This avoids routing
the source MCAP through your local machine or the Nomadic backend before storage
transfer starts.

```python title="S3 MCAP cloud ingest" theme={null}
BUCKET = "your-mcap-bucket"
PREFIX = "mcap/"
ROLE_ARN = "arn:aws:iam::123456789012:role/NomadicMcapTransferRole"

integration = client.cloud_integrations.add_s3_storage_transfer(
    name="MCAP archive",
    bucket=BUCKET,
    prefix=PREFIX,
    role_arn=ROLE_ARN,
)

job = client.upload(
    f"s3://{BUCKET}/{PREFIX}example-017-droid-ds.mcap",
    folder="mcap_cloud_test",
    integration_id=integration["id"],
    wait_for_uploaded=False,
)

final = client.wait_for_mcap_import_job(
    job["mcap_import_job_id"],
    timeout=7200,
)

print(final["status"])
print(final["video_ids"])
```

See [Cloud Storage Uploads](/sdk/cloud-storage) for the AWS IAM role
setup required before creating the S3 Storage Transfer integration.

#### Multi-view (local/URL)

Use a dict mapping view names to local files or URLs. `front` is required in every set.

```python theme={null}
# Single multi-view set
multi = client.upload(
  {
    "front": "https://example.com/trip-042/front.mp4",
    "left": "https://example.com/trip-042/left.mp4",
    "right": "https://example.com/trip-042/right.mp4",
  },
  folder="fleet_uploads",
  scope="org",
)

# Multiple multi-view sets in one call
multi_batch = client.upload([
  {
    "front": "https://example.com/set1/front.mp4",
    "left": "https://example.com/set1/left.mp4",
    "right": "https://example.com/set1/right.mp4",
  },
  {
    "front": "https://example.com/set2/front.mp4",
    "left": "https://example.com/set2/left.mp4",
    "right": "https://example.com/set2/right.mp4",
  },
])
```

Local/HTTP multi-view uploads return the stitched front `video_id`.

<Note>
  * **Metadata sidecars** must share the same base filename as the video (e.g., `launch.mp4` + `launch.json`). See the [Metadata Ingestion Spec](https://docs.google.com/document/d/1Stz24u2rZ6EsOU0qZEI8oVsZRlg-qMD9xMDymj2enKA/edit?usp=sharing) for the full schema.
  * **Custom names** (`name` param) are supported for single files, URLs, and batch dict syntax — not for cloud imports or multi-view.
  * **Folders** are auto-created if they don't exist. Defaults to personal scope; use `scope="org"` for shared org folders.
</Note>

**Required Parameters:**

| Parameter | Type                               | Description                                                           |
| --------- | ---------------------------------- | --------------------------------------------------------------------- |
| `videos`  | `str \| Path \| tuple \| Sequence` | Single video, (video, metadata) tuple, or list of mixed videos/tuples |

**Optional Parameters:**

| Parameter           | Type                | Default  | Description                                                                                                                                                                                                          |
| ------------------- | ------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | `str`               | `None`   | Custom display name for the uploaded video. Overrides the original filename. Only supported for single file uploads, URLs, or per-video in batch dict syntax. Not supported for cloud imports or multi-view uploads. |
| `folder`            | `str`               | `None`   | Folder name for organizing uploads (unique within each scope)                                                                                                                                                        |
| `metadata_file`     | `str \| Path`       | `None`   | Overlay metadata JSON file (must share the video's base filename) per [spec](https://docs.google.com/document/d/1Stz24u2rZ6EsOU0qZEI8oVsZRlg-qMD9xMDymj2enKA/edit?usp=sharing) (ignored when using tuples)           |
| `scope`             | `'user' \| 'org'`   | `'user'` | Scope hint for folder resolution. Use `'org'` for shared org folders and `'user'` for personal uploads.                                                                                                              |
| `upload_timeout`    | `int`               | `1200`   | Timeout in seconds for upload completion                                                                                                                                                                             |
| `wait_for_uploaded` | `bool`              | `True`   | Wait until upload is complete                                                                                                                                                                                        |
| `integration_id`    | `str`               | `None`   | Saved cloud integration identifier for `gs://`, `s3://`, `hf://buckets/...`, and S3 MCAP imports.                                                                                                                    |
| `chunk_size`        | `int`               | `None`   | Optional chunk size for MCAP ingest.                                                                                                                                                                                 |
| `front_channel`     | `str`               | `None`   | Front-camera channel name for local MCAP stitching.                                                                                                                                                                  |
| `channel_roles`     | `Mapping[str, str]` | `None`   | Optional channel-to-role mapping for local MCAP uploads.                                                                                                                                                             |
| `channel_labels`    | `Mapping[str, str]` | `None`   | Optional channel display labels for local MCAP uploads.                                                                                                                                                              |

**Returns:** Dict (single) or List\[Dict] (multiple) with `{"video_id": "...", "status": "processing" | "uploaded" | ...}`
