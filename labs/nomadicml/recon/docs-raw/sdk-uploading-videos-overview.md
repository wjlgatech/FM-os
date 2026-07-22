> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Uploading Videos

> Overview of the upload() method and supported sources

The `upload()` method handles all video ingestion. The return type differs depending on the source:

* **Local video files & URLs** return a `video_id`.
* **Local `.mcap` files** return an `mcap_ingest_id` — use `client.wait_for_mcap_ingest()` or `client.get_mcap_ingest()` to retrieve derived `video_ids`.
* **Cloud video imports (`gs://`, `s3://`, `hf://buckets/...`)** return an `import_job_id` — use `client.get_import_job()` and `client.get_import_job_videos()` to retrieve video IDs.
* **S3 `.mcap` cloud imports** return an `mcap_import_job_id` — use `client.wait_for_mcap_import_job()` or `client.get_mcap_import_job()` to retrieve child ingests and derived `video_ids`.
