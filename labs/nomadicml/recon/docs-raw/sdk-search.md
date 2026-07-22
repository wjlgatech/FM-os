> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Search

> Semantic search across analysed events in a folder

### search()

Run semantic search across all analysed events inside a folder. You can use open-ended natural language queries.

```python theme={null}
results = client.search(
    query="red pickup truck overtaking",
    folder_name="my_fleet_uploads",
    scope="org",                 # optional, defaults to "user"
)

print(results["summary"])
for thought in results["thoughts"]:
    print("•", thought)
```

**Required Parameters:**

| Parameter     | Type  | Description                                 |
| ------------- | ----- | ------------------------------------------- |
| `query`       | `str` | Natural-language search query               |
| `folder_name` | `str` | Human-friendly folder name to search within |

**Optional Parameters:**

| Parameter | Type                          | Default  | Description                                                                                                    |
| --------- | ----------------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| `scope`   | `'user' \| 'org' \| 'sample'` | `'user'` | Scope hint for folder resolution. Use `'org'` for organization folders and `'sample'` for demo/sample folders. |

**Returns:** Dict with:

* `summary`: string overview of the findings
* `thoughts`: list of reasoning steps (chain-of-thought) shown in the UI
* `matches`: list of `{video_id, analysis_id, event_index, similarity, reason}`
* `session_id`: identifier for the associated search session (useful for re-fetching or sharing)
