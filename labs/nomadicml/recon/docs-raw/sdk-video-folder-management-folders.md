> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Folders

> Create and look up folders

#### create\_folder()

Create a new folder in a specific scope. Raises an error if a folder with the
same name already exists in the target scope.

```python theme={null}
marketing = client.create_folder("marketing", description="Q1 campaign")
```

**Parameters:**

| Parameter     | Type              | Default  | Description                 |
| ------------- | ----------------- | -------- | --------------------------- |
| `name`        | `str`             | —        | Folder name to create       |
| `scope`       | `'user' \| 'org'` | `'user'` | Target scope for creation   |
| `description` | `str \| None`     | `None`   | Optional folder description |

**Returns:** Dict with folder `id`, `name`, `org_id`, `created_at`, and `description`

#### get\_folder()

Lookup a folder by name. Defaults to your personal scope; pass `scope="org"`
for organization folders.

```python theme={null}
folder = client.get_folder("fleet_uploads")
org_folder = client.get_folder("fleet_uploads", scope="org")
```

**Parameters:**

| Parameter | Type              | Default  | Description            |
| --------- | ----------------- | -------- | ---------------------- |
| `name`    | `str`             | —        | Folder name to look up |
| `scope`   | `'user' \| 'org'` | `'user'` | Scope to search within |

**Returns:** Dict with folder `id`, `name`, `org_id`, `scope`, `created_at`, `created_by`, `description`, and `video_count`
