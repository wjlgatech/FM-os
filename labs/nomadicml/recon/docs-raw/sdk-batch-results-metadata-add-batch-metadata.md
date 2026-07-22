> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# add_batch_metadata()

> Add or update custom metadata for a batch analysis

Add or update custom metadata for a batch analysis. Metadata is stored as key-value pairs and can be used to track experiments, versions, or any custom information about your batch runs.

```python theme={null}
# Add metadata to a batch
client.add_batch_metadata(
    "batch_id",
    {
        "experiment_id": "exp-001",
        "version": 2,
        "model": "Nomadic-VL-XLarge",
        "notes": "Test run with new parameters"
    }
)

# Update existing metadata (new keys will be merged, existing keys overwritten)
client.add_batch_metadata(
    "batch_id",
    {
        "version": 3,
        "status": "completed"
    }
)

# Retrieve metadata later
batch_results = client.get_batch_analysis("batch_id")
metadata = batch_results["batch_metadata"]["metadata"]
print(f"Experiment: {metadata.get('experiment_id')}")
print(f"Version: {metadata.get('version')}")
```

**Required Parameters:**

| Parameter  | Type                         | Description                                                    |
| ---------- | ---------------------------- | -------------------------------------------------------------- |
| `batch_id` | `str`                        | ID of the batch to update (required)                           |
| `metadata` | `Dict[str, Union[str, int]]` | Dictionary with string keys and string/int values (non-nested) |

**Returns:** Dict with success status and updated metadata:

* `success`: Boolean indicating if the operation succeeded
* `batch_id`: The batch identifier
* `metadata`: Complete metadata dictionary after merge

**Raises:**

* `ValidationError`: If metadata format is invalid (e.g., nested objects, non-string keys, invalid value types)
* `NomadicMLError`: If batch is not found or you don't have permission to modify it

<Note>
  Only the batch owner can add or update metadata. New metadata keys will be merged with existing metadata, with new values overwriting any existing keys with the same name.

  Metadata values must be strings or integers only - nested objects, arrays, booleans, or null values are not supported.
</Note>
