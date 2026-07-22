> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Livestreams

> Start livestream analysis sessions, listen for events, and inspect stream timing fields.

Use `client.livestream` to run continuous analysis on a live video source such as an HLS `.m3u8` stream. A session pulls the stream, chunks it, runs the rapid-review query on each chunk, and appends detected events to the session.

[![Open the livestream demo in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zPgjWq3A_I_0JGLEMIkmr9mEOZ-n2f7F?usp=sharing)

## Start a Session

```python theme={null}
from getpass import getpass
import os

from nomadic import NomadicAI

api_key = os.environ.get("NOMADICAI_API_KEY") or getpass("Nomadic API key: ")
client = NomadicAI(api_key=api_key)

stream_url = "https://stream.nomadicml.com/stream2.m3u8"

result = client.livestream.start_session(
    source_url=stream_url,
    name="Robot pick demo",
    rapid_review_query="detect robot picking up an apple",
)

stream_id = result["stream_id"]
session_id = result["session_id"]

print(stream_id, session_id)
print(f"https://app.nomadicml.com/events/{stream_id}/{session_id}")
```

`source_url` should point to a reachable live stream. HLS `.m3u8` URLs are the common path for browser-viewable livestreams.

**Parameters:**

| Parameter            | Type          | Default | Description                                                       |
| -------------------- | ------------- | ------- | ----------------------------------------------------------------- |
| `source_url`         | `str`         | —       | Reachable live-stream URL.                                        |
| `name`               | `str`         | —       | Friendly session name shown in the web UI.                        |
| `rapid_review_query` | `str \| None` | `None`  | Natural-language query for continuous event detection.            |
| `stream_id`          | `str \| None` | `None`  | Existing parent stream ID. Omit it to let the backend create one. |

## Listen for Events

`iter_events()` polls the session and yields each new event once. Use `poll_interval` to control how often the SDK checks for new events and `timeout` to stop listening after a fixed number of seconds.

```python theme={null}
for event in client.livestream.iter_events(
    stream_id,
    session_id,
    poll_interval=10,
    timeout=180,
):
    severity = event.get("severity", "info").upper()
    event_type = event.get("type", "unknown")
    stream_time = event.get("stream_time", "?")
    description = event.get("description", "")

    print(f"[{severity}] {event_type} @ {stream_time}s - {description}")
```

**Parameters:**

| Parameter       | Type            | Default | Description                                          |
| --------------- | --------------- | ------- | ---------------------------------------------------- |
| `stream_id`     | `str`           | —       | Parent stream ID returned by `start_session()`.      |
| `session_id`    | `str`           | —       | Session ID returned by `start_session()`.            |
| `poll_interval` | `float`         | `5.0`   | Seconds between polling attempts.                    |
| `timeout`       | `float \| None` | `None`  | Maximum seconds to listen before stopping iteration. |

## End and Fetch the Final Session

```python theme={null}
client.livestream.end_session(stream_id=stream_id, session_id=session_id)

final = client.livestream.get_session(stream_id, session_id)

print(final["status"])
print(final["chunk_count"])
print(len(final.get("events", [])))
```

Completed sessions include the final chunk count and the accumulated event list.

`end_session(stream_id, session_id)` stops an active session. `get_session(stream_id, session_id)` returns the current or final session payload.

## Session Fields

| Field         | Description                                                                                               |
| ------------- | --------------------------------------------------------------------------------------------------------- |
| `stream_id`   | Stable stream identifier. The backend can create one when omitted from `start_session()`.                 |
| `session_id`  | Identifier for this run of the stream. Use it with `get_session()`, `iter_events()`, and `end_session()`. |
| `name`        | Friendly session name shown in the web UI.                                                                |
| `source_url`  | Original livestream URL supplied to `start_session()`.                                                    |
| `status`      | Session lifecycle status such as `INITIALIZING`, `ACTIVE`, `FINISHED`, or `FAILED`.                       |
| `chunk_count` | Number of stream chunks processed so far.                                                                 |
| `events`      | Detected rapid-review events when `rapid_review_query` is supplied.                                       |
| `chunks`      | Chunk metadata for the session.                                                                           |

## Event Timing Fields

Livestream event timestamps are relative to the session timeline.

| Field                   | Description                                                                                                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `stream_time`           | Event start time in seconds from the beginning of the livestream session. This is the main field to display in user-facing logs. |
| `capture_time`          | Capture time in seconds on the stream timeline. Often matches `stream_time`.                                                     |
| `chunk_index`           | Zero-based index of the processed livestream chunk where the event was detected.                                                 |
| `chunk_relative_time`   | Event time in seconds relative to the start of the chunk.                                                                        |
| `hls_cumulative_offset` | Offset in seconds contributed by prior HLS chunks.                                                                               |
| `t_start` / `t_end`     | Human-readable event window inside the session, usually formatted as `MM:SS`.                                                    |
| `created_at`            | ISO timestamp for when the event record was created by the backend.                                                              |
| `analysis_id`           | Analysis run that produced the event.                                                                                            |
| `chunk_id`              | Backend chunk identifier associated with the event.                                                                              |

Example event shape:

```python theme={null}
{
    "type": "Security",
    "label": "robot picking up an apple",
    "description": "robot picking up an apple",
    "severity": "low",
    "confidence": 0.95,
    "stream_time": 9.0,
    "chunk_relative_time": 9.0,
    "t_start": "00:09",
    "t_end": "00:16",
    "created_at": "2026-03-07T22:51:55.312121+00:00",
    "chunk_index": 0,
    "chunk_id": "session_000",
    "analysis_id": "session_analysis_000",
}
```

## Signed Playback Manifest

After chunks are available, `get_signed_manifest()` returns a short-lived signed HLS manifest URL for playback.

```python theme={null}
manifest = client.livestream.get_signed_manifest(session_id)
print(manifest["url"])
print(manifest["expires_at"])
```

Use the returned `url` with an HLS-capable player.
