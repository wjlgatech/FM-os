> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Structured Exports

> ASAM OpenODD-compliant CSV exports

### generate\_structured\_odd()

Produce an ASAM OpenODD-compliant CSV describing the vehicle's operating domain.

```python title="Structured ODD export" theme={null}
from nomadic import NomadicAI, DEFAULT_STRUCTURED_ODD_COLUMNS

client = NomadicAI(api_key="your_api_key")

# Use the default schema or customise it before calling the export.
columns = [
    {
        "name": "timestamp",
        "prompt": "Log the timestamp in ISO 8601 format (placeholder date 2024-01-01).",
        "type": "YYYY-MM-DDTHH:MM:SSZ",
    },
    {
        "name": "scenery.road.type",
        "prompt": "The type of road the vehicle is on.",
        "type": "categorical",
        "literals": ["motorway", "rural", "urban_street", "parking_lot", "unpaved", "unknown"],
    },
]

odd = client.generate_structured_odd(
    video_id="VIDEO_ID",
    columns=columns or DEFAULT_STRUCTURED_ODD_COLUMNS,
)

print(odd["csv"])
print(odd.get("share_url"))
```

**Required Parameters:**

| Parameter  | Type  | Description                                                        |
| ---------- | ----- | ------------------------------------------------------------------ |
| `video_id` | `str` | ID of the analysed video whose operating domain you want to export |

**Optional Parameters:**

| Parameter | Type                            | Default                          | Description                                                                       |
| --------- | ------------------------------- | -------------------------------- | --------------------------------------------------------------------------------- |
| `columns` | `Sequence[StructuredOddColumn]` | `DEFAULT_STRUCTURED_ODD_COLUMNS` | Column definitions matching the UI schema (name, prompt, type, optional literals) |
| `timeout` | `int`                           | client default                   | Request timeout override in seconds                                               |

**Returns:** Dict containing:

* `csv`: The generated CSV text.
* `columns`: The resolved column schema (after validation).
* `reasoning_trace_path`: Final Firestore path used for reasoning logs.
* `share_id` / `share_url`: Optional sharing metadata if the backend stored the export.
* `processing_time`: Time spent generating the export.
* `raw`: Full backend response payload for additional introspection.
