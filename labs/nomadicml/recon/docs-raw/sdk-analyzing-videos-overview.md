> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Analyzing Videos

> Overview of prompt-based analyze()

Run prompt-based analysis on one or more uploaded videos. Prompt analysis detects custom events using natural language prompts and defaults to **Thinking** mode.

```python theme={null}
analysis = client.analyze(
    "video_id_1",
    prompt="detect vehicles parked on the sidewalk",
)
```

Use prompt analysis for custom natural-language requirements.
