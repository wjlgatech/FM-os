> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Prompt Analysis

> Detect custom events using natural language prompts

Detect custom events in videos using natural language prompts. The default analyzer uses **Thinking** mode, which matches the router behavior in the web app. Use **Fast** mode when you want speed-preferring analysis.

```python title="Prompt examples" theme={null}
# Single-video prompt, defaults to Thinking
analysis = client.analyze(
    "video_id_1",
    prompt="detect vehicles parked on the sidewalk",
)

# Fast mode
analysis = client.analyze(
    "video_id_1",
    prompt="detect delivery vans double parked",
    mode="fast",
)

# Request available telemetry directly in the prompt
analysis = client.analyze(
    "video_id_1",
    prompt="detect speeding events and include available speed, GPS, and timestamp evidence",
)

# Batch prompt: analyze multiple IDs at once
batch = client.analyze(
    ["video_id_1", "video_id_2"],
    prompt="detect jaywalking near intersections",
)

# Batch prompt: analyze every video in a folder
batch = client.analyze(
    folder="fleet_uploads",
    prompt="detect jaywalking near intersections",
)

# Batch prompt: analyze an organization folder
org_batch = client.analyze(
    folder="fleet_uploads",
    scope="org",
    prompt="detect jaywalking near intersections",
)

# Batch prompt: analyze a read-only demo/sample folder
sample_batch = client.analyze(
    folder="Construction Samples",
    scope="sample",
    prompt="detect workers near active machinery",
)

# Open an SDK-native video/event viewer
client.visualize(analysis)

# Open a viewer from a batch result or an existing batch ID
client.visualize(batch)
client.visualize(batch, only_with_events=True)  # Hide videos with zero events
client.visualize(batch["batch_metadata"]["batch_id"])
```

**Required Parameters:**

| Parameter           | Type                   | Description                                                                |
| ------------------- | ---------------------- | -------------------------------------------------------------------------- |
| `id(s)` or `folder` | `str \| Sequence[str]` | Video ID(s) or folder name (use one, not both)                             |
| `prompt`            | `str`                  | Event description or question to analyze (e.g., "detect green crosswalks") |

**Optional Parameters:**

| Parameter | Type                          | Default      | Description                                                                                                                                                        |
| --------- | ----------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `mode`    | `str`                         | `"thinking"` | Either `"thinking"` or `"fast"`                                                                                                                                    |
| `scope`   | `'user' \| 'org' \| 'sample'` | `None`       | Folder lookup scope. Use the same scope used for folder creation/upload; use `'sample'` for read-only demo/sample folders. Only applies when `folder` is provided. |
| `timeout` | `int`                         | `2400`       | Analysis timeout in seconds                                                                                                                                        |
| `wait`    | `bool`                        | `True`       | Wait for analysis to complete                                                                                                                                      |

**Returns:** Dict with `video_id`, `analysis_id`, `mode`, `status`, `summary`, and `events`.

Batch prompt analysis returns `batch_metadata` with `batch_id`, `batch_viewer_url`, and `mode`, plus a `results` list of normalized per-video results.

Use `client.visualize(batch)` when you already have the SDK batch result. Add `only_with_events=True` to hide videos with zero detected events. Use `client.visualize(batch_id)` to hydrate and render a saved batch later.

<Note>
  Prompt analysis does not expose router overrides, model selection, overlay flags, reasoning traces, or Wizarding Trace artifacts. Put analysis requirements directly in the prompt.
</Note>
