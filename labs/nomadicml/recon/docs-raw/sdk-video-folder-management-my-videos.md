> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# my_videos()

> Retrieve uploaded videos, optionally filtered by folder

```python theme={null}
# Get all videos
videos = client.my_videos()

# Get videos in specific folder
videos = client.my_videos(folder="my_folder")

# Get videos from a personal folder (when org folder has same name)
videos = client.my_videos(folder="shared_folder", scope="user")

# Get videos from an organization folder
videos = client.my_videos(folder="shared_folder", scope="org")

# Get videos from a read-only demo/sample folder
videos = client.my_videos(folder="Construction Samples", scope="sample")
```

**Optional Parameters:**

| Parameter | Type                          | Default | Description                                                                                                                                                                                                                                                         |
| --------- | ----------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `folder`  | `str`                         | `None`  | Filter videos by folder name                                                                                                                                                                                                                                        |
| `scope`   | `'user' \| 'org' \| 'sample'` | `None`  | Disambiguate folder lookup when personal and org folders share the same name. `'user'` matches only personal folders, `'org'` matches only organization folders, and `'sample'` matches read-only demo/sample folders. When `None`, personal folders are preferred. |

**Returns:** `List[Dict]` - Each dict contains:

| Field         | Type    | Description                            |
| ------------- | ------- | -------------------------------------- |
| `video_id`    | `str`   | Unique video identifier                |
| `video_name`  | `str`   | Original filename                      |
| `duration_s`  | `float` | Video duration in seconds              |
| `folder_id`   | `str`   | Folder identifier                      |
| `status`      | `str`   | Upload status (see below)              |
| `folder_name` | `str`   | Folder name (when filtering by folder) |
| `org_id`      | `str`   | Organization ID (if org-scoped)        |

**Upload status values:**

| Status             | Meaning            |
| ------------------ | ------------------ |
| `processing`       | Upload in progress |
| `uploading_failed` | Upload failed      |
| `uploaded`         | Ready for analysis |
