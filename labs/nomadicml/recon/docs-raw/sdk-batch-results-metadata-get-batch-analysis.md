> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# get_batch_analysis()

> Retrieve analysis results for a completed batch

Retrieve analysis results for a completed batch. Optionally filter events by approval status (approved, rejected, pending, or invalid), or return event-level CSV.

```python theme={null}
# Get all results from a batch
batch_results = client.get_batch_analysis("batch_id")

# Filter for only approved events
approved_only = client.get_batch_analysis(
    "batch_id",
    filter="approved"
)

# Filter for multiple statuses
pending_and_rejected = client.get_batch_analysis(
    "batch_id",
    filter=["pending", "rejected"]
)

# Return event-level CSV instead of JSON
csv_text = client.get_batch_analysis("batch_id", as_csv=True)

# Filter + CSV (only approved events are included)
approved_csv = client.get_batch_analysis(
    "batch_id",
    filter="approved",
    as_csv=True
)

# Save CSV to disk
with open("batch-results-approved.csv", "w", encoding="utf-8", newline="") as f:
    f.write(approved_csv)

# Access batch metadata
print(batch_results["batch_metadata"]["batch_type"])
print(batch_results["batch_metadata"]["batch_viewer_url"])

# Iterate through video results
for result in batch_results["results"]:
    print(f"Video: {result['video_id']}")
    print(f"Events: {len(result['events'])}")
    for event in result["events"]:
        print(f"  - {event.get('label', '')} at {event.get('t_start', '')}-{event.get('t_end', '')}")
```

**Required Parameters:**

| Parameter  | Type  | Description                            |
| ---------- | ----- | -------------------------------------- |
| `batch_id` | `str` | ID of the batch to retrieve (required) |

**Optional Parameters:**

| Parameter | Type               | Default | Description                                                                                                                                                                                                                                                                                |
| --------- | ------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `filter`  | `str \| List[str]` | `None`  | Filter events by approval status. Valid values: `'approved'`, `'rejected'`, `'pending'`, `'invalid'`. If omitted, returns all events for all videos (including videos with zero events). If provided, only matching events are returned and videos with zero matching events are excluded. |
| `as_csv`  | `bool`             | `False` | If `True`, returns CSV text instead of JSON. CSV is event-level (one row per event) and does not emit placeholder rows for videos with zero events.                                                                                                                                        |

**Returns (`as_csv=False`, default):** Dict with two keys:

* `batch_metadata`: Contains batch information
  * `batch_id`: The batch identifier
  * `batch_viewer_url`: URL to view batch results in the web UI
  * `batch_type`: Internal batch category. Prompt-analysis batches may currently appear as legacy `"ask"`.
  * `analysis_type`: Internal analysis label used by the backend
  * `review_status`: Whether the batch analysis have been fully reviewed by someone
  * `review_status_updated_at`: Time the batch analysis review status was updated, N/A if not reviewed yet.
  * `metadata`: Dictionary of custom metadata key-value pairs (empty dict if no metadata exists)
  * Configuration details (for prompt batches: `prompt`, `category`, etc.)

* `results`: List of per-video analysis dictionaries
  * `video_id`: ID of the video
  * `analysis_id`: ID of the analysis
  * `mode`: Analysis mode used
  * `status`: Analysis status
  * `events`: List of detected events (filtered by approval status if specified)
  * Additional fields depending on analysis type

**Returns (`as_csv=True`):** `str` (CSV text)

* Header row is always included.
* Rows are event-level (one row per event).
* Current CSV columns:
  * `Query`
  * `Video`
  * `Approval Status`
  * `Timestamp`
  * `Category`
  * `Label`
  * `AI Analysis`
  * `Severity`
  * `Video ID`
  * `Analysis ID`
  * `Batch ID`
  * `Batch Viewer URL`
  * `Status`
  * `Confidence`
  * `Import Source URI`
  * `Summary`

**Raises:**

* `NomadicMLError`: If batch is not completed or other API errors occur
* `ValidationError`: If filter contains invalid values

<Note>
  The batch must be completed before you can retrieve its results. If you need to check batch status first, use the batch viewer URL.
</Note>
