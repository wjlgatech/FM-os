> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# SDK Usage Examples

> Practical examples of using the Nomadic Python SDK for common tasks.

## Quick Start Notebook

For programmatic access to Nomadic, you can use our Python SDK. Quick Start Notebook below.
[![Open this demo in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/18J_Q-5wTS2xLjryqA-b2OtBetfCC9zMv)

### 1. Install the SDK

```bash theme={null}
pip install nomadic
```

### 2. Initialize the Client

```python theme={null}
from nomadic import NomadicAI
import os

# Initialize with your API key
client = NomadicAI(
    api_key=os.environ.get("NOMADICAI_API_KEY")
)
```

<Note>
  To get your API key, log in to the web platform, go to Profile > API Key, and generate a new key.
  We recommend storing your API key in an environment variable for security.
</Note>

### 3. Upload and Analyze Videos

The standard workflow involves uploading your videos first, then running analysis on them.
Uploads accept local paths or remote URLs that end with a common video extension (`.mp4`, `.mov`, `.avi`, `.webm`):

```python theme={null}
response = client.upload('https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Mayhem-on-Road-Compilation.mp4')

# Extract video ID
video_id = response["video_id"]

# Add scope="org" when uploading to shared organization folders.

# Then analyze it
analysis = client.analyze(video_id, prompt="Find outlier events")
print(analysis)
```

You can also pass a list of paths/URLs to `upload` and a list of ids to `analyze` for batch operations.

```python theme={null}
paths = [
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Driving-a-bus-in-Switzerland-on-Snowy-Roads.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/LIDAR-RBG-Waymo-YouTube-Public-Sample.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Mayhem-on-Road-Compilation.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Oakland-to-SF-on-Bridge.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Zoox_San%20Francisco-Bike-To-Wherever-Day.mp4'
]
response = client.upload(paths)
video_ids = [v['video_id'] for v in response]

batch = client.analyze(video_ids, prompt="Find outlier events")
print(batch["batch_metadata"])  # Contains batch_id, batch_viewer_url, batch_type
for result in batch["results"]:
    print(result["video_id"], result["analysis_id"], len(result.get("events", [])))

```

### 4. Semantic Search with Chain-of-Thought

Search can be used are open in the natural language queries. Nomadic will reason about what fits best. Search response includes a chain-of-thought summary plus the reasoning behind each matched video. Supply
the natural language query, the folder name, and the scope (`"user"`, `"org"`,
or `"sample"`), and the call returns the complete set of results in one
payload.

```python theme={null}
results = client.search(
    query="Find near-misses with pedestrians on crosswalks",
    folder_name="fleet_uploads_march",
    scope="org",          # optional, defaults to "user"
)

print(results["summary"])       # overall overview
print(results["thoughts"])      # list of reasoning steps
for match in results["matches"]:
    print(match["video_id"], match["reason"], match["similarity"])

# Advanced: reuse the session ID if you want to reference the same results later
print(results["session_id"])  # Unique identifier for this search session
```

### 5. Analysis

Nomadic prompt analysis can be run on a single video, a list of videos, or a folder.

#### Prompt Analysis

Extracts custom events based on your specific requirements. The default analyzer uses Thinking mode. Use Fast mode when you want speed-preferring router behavior.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1-IXsag4dZhv4oT-6wy7mf4iRLD99AuhJ#scrollTo=Cofv1h7W1hur)

```python theme={null}
analysis = client.analyze("video_id_1", prompt="green crosswalk")
fast_analysis = client.analyze("video_id_1", prompt="green crosswalk", mode="fast")
print(analysis)
```

### 6. Project-Based File Management & Composite Workflows

For larger projects, you can organize videos into folders and run batch analysis on entire folders at once. This is especially useful for processing datasets or running systematic reviews.

#### Example: Deleting videos

```python theme={null}
client.delete_video(video_id)

# OR
for v in video_ids:
    client.delete_video(v)
```

#### Example: Creating and looking up folders

```python theme={null}
# Create a new personal folder
folder = client.create_folder("marketing", description="Q1 campaign")
print(folder["id"], folder["created_at"])

# Lookup by name (personal scope by default)
existing = client.get_folder("marketing")
print(existing["id"], existing["video_count"])

# Organization-scoped folders
org_folder = client.create_folder("fleet_uploads", scope="org")
org_existing = client.get_folder("fleet_uploads", scope="org")
```

#### Example: Analysis + Search Workflow

This example demonstrates a common workflow: first, run a broad analysis to cast a wide net, then use search across analysis results to hone in on specific events, and finally, run a detailed analysis on the resulting subset of videos.

```python theme={null}
paths = [
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Driving-a-bus-in-Switzerland-on-Snowy-Roads.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/LIDAR-RBG-Waymo-YouTube-Public-Sample.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Mayhem-on-Road-Compilation.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Oakland-to-SF-on-Bridge.mp4',
    'https://storage.googleapis.com/videolm-bc319.firebasestorage.app/example-videos/Zoox_San%20Francisco-Bike-To-Wherever-Day.mp4'
]

# Define a folder for the project
folder_name = "prompt-analysis-videos"
project_folder = client.create_folder(folder_name, scope="org")
# If you're reusing an existing folder, use:
# project_folder = client.get_folder(folder_name, scope="org")
print(f"Using folder '{project_folder['name']}' scoped to {project_folder['scope']} (id={project_folder['id']})")

print("📁 Step 1: Uploading videos to project folder...")
response = client.upload(paths, folder=folder_name, scope="org")
print(f"✅ Successfully uploaded {len(response)} videos to '{folder_name}' folder")

print("\n🔍 Step 2: Running broad prompt analysis on all videos...")
analyses = client.analyze(
    folder=folder_name,
    scope="org",
    prompt="Find risky road-user interactions and traffic safety events",
)
print(f"✅ Completed prompt analysis on {len(analyses)} videos")

print("\n🔎 Step 3: Searching for pedestrian-related incidents...")
# Use natural-language search over the analysis results
search_results = client.search(
    query="Find risky incidents involving pedestrians",
    folder_name=folder_name,
    scope="org",
)

matching_video_ids = list(set([match['video_id'] for match in search_results['matches']]))
print(f"✅ Found {len(matching_video_ids)} videos with pedestrian incidents")

print(f"\n🎯 Step 4: Re-analyzing {len(matching_video_ids)} videos for pedestrian fault analysis...")
analyses = client.analyze(
    matching_video_ids,
    prompt="Mark incidents involving pedestrians where pedestrians are at fault",
)
print(f"✅ Completed detailed analysis on {len(analyses)} videos")

for analysis in analyses:
    if analysis['events']:
        print(f"\n🎬 Events found in video {analysis['video_id']}:")
        for e in analysis['events']:
            print(f"  • {e}")
        print("-" * 80)

print("\n🧹 Step 5: Cleaning up - deleting project videos...")
for response in client.my_videos(folder_name):
    result = client.delete_video(response['video_id'])
```

### 7. Re-analyzing Videos

You don't need to re-upload videos to run new analyses. You can efficiently query already uploaded videos using either their specific `video_id`s or by organizing them into folders.

#### Re-analyzing Specific Videos by ID

This is the most direct way to re-run analysis on a few specific videos. After you upload a video, the API returns a `video_id`. Store this ID to reference the video in future calls.

```python theme={null}
# Replace these strings with the video IDs returned by upload
pedestrian_analysis = client.analyze(
    ["video_id_1", "video_id_2"],
    prompt="pedestrians close to vehicle",
)
print(f"Found {len(pedestrian_analysis)} videos with pedestrian interactions.")
```

#### Using Folders for Batch Re-analysis

For larger-scale projects, organizing videos into folders is the best practice. This allows you to run analysis on an entire dataset with a single command.

```python theme={null}
folder_name = "2024_urban_driving_set"

# Step 1: Upload and organize your videos into a folder (only needs to be done once)
client.upload(
    ['/path/to/city_drive_1.mp4', '/path/to/city_drive_2.mp4'],
    folder=folder_name
)

# Step 2: Run an initial analysis to find all road signs and their MUTCD codes
print(f"\nRunning initial analysis for 'road signs & MUTCD codes' in folder '{folder_name}'...")
pedestrian_analysis = client.analyze(
    folder=folder_name,
    prompt="Find all road signs and note their corresponding MUTCD codes?",
)
print(f"Found {len(pedestrian_analysis)} videos with road signs.")
# Step 3: Later, run a different analysis on the same set of videos
print(f"\nRunning second analysis for 'potholes' in folder '{folder_name}'...")
pothole_analysis = client.analyze(
    folder=folder_name,
    prompt="potholes or major road cracks",
)
print(f"Found {len(pothole_analysis)} videos with potholes.")

# Read-only demo/sample folders can be analyzed by opting into sample scope
sample_analysis = client.analyze(
    folder="Construction Samples",
    scope="sample",
    prompt="detect workers near active machinery",
)
```

### 8. Visualizing Results

Use the SDK visualizer to inspect detected events against the source video.

#### Creating a Video/Event Viewer

The visualizer returns standalone HTML and displays inline in notebooks when possible.

```python theme={null}
result = client.analyze(
    "video_id_1",
    prompt="green crosswalk",
)

html = client.visualize(result)
```

For batch analysis, pass either the batch result or a saved `batch_id`:

```python theme={null}
batch = client.analyze(
    ["video_id_1", "video_id_2"],
    prompt="green crosswalk",
)

html = client.visualize(batch)
html = client.visualize(batch, only_with_events=True)  # Hide videos with zero events

# Later, hydrate the batch and render it by ID.
html = client.visualize(batch["batch_metadata"]["batch_id"])
```

### 9. Livestream Analysis

Use `client.livestream` to start a live HLS session, run a continuous rapid-review query, and poll newly detected events.

[![Open the livestream demo in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zPgjWq3A_I_0JGLEMIkmr9mEOZ-n2f7F?usp=sharing)

```python theme={null}
from getpass import getpass
import os

from nomadic import NomadicAI

client = NomadicAI(
    api_key=os.environ.get("NOMADICAI_API_KEY") or getpass("Nomadic API key: ")
)

result = client.livestream.start_session(
    source_url="https://stream.nomadicml.com/stream2.m3u8",
    name="Robot pick demo",
    rapid_review_query="detect robot picking up an apple",
)

stream_id = result["stream_id"]
session_id = result["session_id"]

for event in client.livestream.iter_events(
    stream_id,
    session_id,
    poll_interval=10,
    timeout=180,
):
    print(event.get("stream_time"), event.get("description"))

client.livestream.end_session(stream_id=stream_id, session_id=session_id)
final = client.livestream.get_session(stream_id, session_id)

print(final["status"], final["chunk_count"], len(final.get("events", [])))
```

Livestream event timing fields include `stream_time`, `capture_time`, `chunk_relative_time`, `t_start`, `t_end`, and backend creation timestamp `created_at`. See [Livestreams](/sdk/livestreams) for the full event schema.

### 10. Working with Overlay Metadata

Nomadic can extract telemetry data from on-screen overlays in videos. This is useful for videos with embedded metadata like timestamps, GPS coordinates, speed, altitude, or custom telemetry values.

<Note>
  **Important:** Metadata describing overlay fields must be provided at upload time. During analysis, request the telemetry you need directly in the prompt.
</Note>

#### Uploading Videos with Metadata

You can provide metadata files that describe the overlay fields in your videos. Metadata must be a properly formatted JSON file according to the [Metadata Ingestion Spec](https://docs.google.com/document/d/1Stz24u2rZ6EsOU0qZEI8oVsZRlg-qMD9xMDymj2enKA/edit?usp=sharing), and the `.json` file must share the same base filename as the video (for example, `drone_footage.mp4` pairs with `drone_footage.json`).

```python theme={null}
# Single video with metadata file (names must match)
result = client.upload(("dashcam_video.mp4", "dashcam_video.json"))

# Multiple videos with mixed metadata
uploads = client.upload([
    ("video1.mp4", "video1.json"),           # Video with metadata
    "video2.mp4",                             # Video without metadata
    ("video3.mp4", "video3.json"),           # Another video with metadata
])

print(f"Uploaded {len(uploads)} videos")
for upload in uploads:
    print(f"Video ID: {upload['video_id']}, Status: {upload['status']}")
```

#### Overlay-Aware Queries

For videos uploaded with metadata or visible overlays, request the telemetry you need in the prompt. The router selects the appropriate extraction path.

```python theme={null}
analysis = client.analyze(
    video_id,
    prompt="Find speed limit violations and include available timestamp and GPS evidence",
)

# Access extracted overlay data in events
for event in analysis["events"]:
    print(f"Event: {event['label']} at {event['t_start']}-{event['t_end']}")

    overlay_values = event.get("overlay", {})
    for field, values in overlay_values.items():
        start = values.get("start")
        end = values.get("end")
        print(f"  {field}: {start} -> {end}")
```

#### Batch Analysis with Overlay Extraction

For batch processing of videos with overlays:

```python theme={null}
# Step 1: Upload batch of videos with metadata
videos_with_metadata = [
    ("fleet_cam_001.mp4", "fleet_cam_001.json"),
    ("fleet_cam_002.mp4", "fleet_cam_002.json"),
    ("fleet_cam_003.mp4", "fleet_cam_003.json"),
]

upload_results = client.upload(videos_with_metadata, folder="fleet_telemetry")
video_ids = [r['video_id'] for r in upload_results]

batch_analysis = client.analyze(
    video_ids,
    prompt="harsh braking events where speed drops rapidly; include available speed telemetry",
)

# Process results with overlay data
for result in batch_analysis["results"]:
    video_id = result["video_id"]
    for event in result["events"]:
        # Speed (and other custom telemetry) is exposed through the overlay map
        speed_overlay = event.get("overlay", {}).get("frame_speed")
        if speed_overlay:
            print(
                f"Video {video_id}: Speed changed from "
                f"{speed_overlay.get('start')} to {speed_overlay.get('end')}"
            )
```

#### Metadata File Format

The metadata JSON file should describe the fields that appear as overlays in your video. For the complete metadata ingestion specification and detailed schema documentation, see the [Metadata Ingestion Spec](https://docs.google.com/document/d/1Stz24u2rZ6EsOU0qZEI8oVsZRlg-qMD9xMDymj2enKA/edit?usp=sharing).

Example metadata file:

```json theme={null}
{
  "fields": [
    {
      "name": "speed",
      "type": "number",
      "unit": "mph",
      "position": "top-left"
    },
    {
      "name": "gps_lat",
      "type": "number",
      "unit": "degrees"
    },
    {
      "name": "gps_lon",
      "type": "number",
      "unit": "degrees"
    },
    {
      "name": "timestamp",
      "type": "timestamp",
      "format": "ISO8601"
    },
    {
      "name": "altitude",
      "type": "number",
      "unit": "meters"
    }
  ]
}
```

<Note>
  Metadata files must have the same base filename as their corresponding video file. For example, `dashcam_recording.mp4` should have metadata named `dashcam_recording.json`.
</Note>

### 11. Storing Results in a Document Database

All SDK methods return serializable Python dictionaries, which can be easily processed and stored in any document database.

#### Example: Storing in MongoDB

```python theme={null}
from pymongo import MongoClient

# Assume 'analysis_results' is the list of dicts from a client.analyze() call
results_to_store = []
for analysis in analysis_results:
    # ... (processing logic from previous examples) ...
    results_to_store.append(processed_event)

# Connect to MongoDB and insert the documents
try:
    db_client = MongoClient('mongodb://localhost:27017/')
    db = db_client['nomadicml_results']
    collection = db['driving_events']
    if results_to_store:
      collection.insert_many(results_to_store)
      print("Successfully saved results to MongoDB.")
except Exception as e:
    print(f"An error occurred with MongoDB: {e}")

```

#### Example: Storing in Supabase

Supabase provides a Postgres database with a Python client that's simple to use.

```python theme={null}
from supabase import create_client, Client
import os

# Assume 'analysis_results' is the list of dicts from a client.analyze() call
results_to_store = []
for analysis in analysis_results:
    # ... (processing logic from previous examples) ...
    # Ensure your dict keys match your Supabase table columns
    processed_event_for_supabase = {
        'source_video_id': video_id,
        'event_type': event.get('type'),
        'timestamp_sec': event.get('time'),
        'description': event.get('description'),
        'severity': event.get('severity'),
        'dmv_rule': event.get('dmvRule'),
        'raw_ai_analysis': event.get('aiAnalysis')
    }
    results_to_store.append(processed_event_for_supabase)

# Initialize Supabase client
try:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    # Insert data into your 'events' table
    if results_to_store:
        data, count = supabase.table('events').insert(results_to_store).execute()
        print(f"Successfully saved {len(data[1])} results to Supabase.")
except Exception as e:
    print(f"An error occurred with Supabase: {e}")
```

## Next Steps

<CardGroup cols={2}>
  <Card title="Uploading From Cloud Storage" icon="code-branch" href="/sdk/cloud-storage">
    A guide to integrate with common cloud storage providers.
  </Card>

  <Card title="SDK Documentation" icon="code-branch" href="/sdk/uploading-videos/overview">
    A concise listing of all video-related SDK functions
  </Card>
</CardGroup>
