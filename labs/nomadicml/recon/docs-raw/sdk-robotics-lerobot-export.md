> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# LeRobot / GR00T Export

> Turn Raw Robot Footage into a Subtask-Annotated, Training-Ready `LeRobot` Dataset for GR00T Finetuning.

# Nomadic → LeRobot: Sub-Task Annotation for GR00T Fine-Tuning

Consider the steps required for a robot to complete a long-horizon task like "make me
a cup of coffee": grab the pod, insert it, place the cup, press the button, wait, pick
up the finished cup. If your training data labels the whole demonstration with that
single sentence, the policy never sees where one sub-skill ends and the next begins.
"Insert the pod" and "pick up the cup" get the exact same language conditioning as
everything in between. That flat labeling throws away the sub-task structure that makes
long-horizon tasks learnable, and it makes failures hard to diagnose since you can't
tell which sub-skill broke.

Nomadic's action segmentation finds where each sub-task starts and ends in raw footage
and gives each one its own language label, turning a flat "make me a cup of coffee"
trajectory into a structured, multi-phase episode a policy can actually learn from.
This guide walks through that pipeline end to end:

1. **Fit a segmentation model on your fleet data** to adapt sub-task boundaries to
   your specific robot and task.
2. **Run automated sub-task annotation** on your videos to find sub-task boundaries
   and language-label each one.
3. **Export to a LeRobot dataset** ready for GR00T fine-tuning, with each source
   video as one episode and sub-tasks written as a per-frame `task_index` timeline
   inside it.
4. **Finetune GR00T** on the exported dataset.

The exported format is LeRobot v2.1 (`meta/info.json`, `meta/tasks.jsonl`,
`meta/modality.json`, per-episode parquet + mp4), the format GR00T fine-tuning
expects.

Run this walkthrough end to end in [Google Colab](https://colab.research.google.com/drive/1SkHiteAQzESTtPtzgXKKteUZZhg-JvAO?usp=sharing).

## Setup

```python theme={null}
from nomadic import NomadicAI
from nomadic.video import AnalysisType

client = NomadicAI(api_key="your_api_key")
```

## 1. Fit a segmentation model on your fleet data

With Nomadic, you can easily train a sub-task segmentation model that uses your
robot's common motion patterns to learn its sub-tasks.

Train from a pre-computed trajectory NPZ (`external_data=`). Point this at your own
fleet's local `.npz` file — Nomadic uploads it to managed storage automatically.

**NPZ schema.** The file must contain these three arrays:

| Key              | Shape / type               | Description                      |
| ---------------- | -------------------------- | -------------------------------- |
| `signal`         | `(n_channels, T)`, `float` | Per-channel trajectory signal    |
| `t_sec`          | `(T,)`, `float`            | Timestamp per sample, in seconds |
| `sample_rate_hz` | `float` scalar             | Sampling rate, e.g. `50.0`       |

```python title="Train a segmentation model from your fleet trajectory NPZ" theme={null}
trajectory_npz = "./my_fleet_trajectories.npz"

# `domain="manipulation"` picks tuned defaults for arm-style motion.
# Use `domain="construction"` for heavy-machinery motion instead.
segmenter_job = client.train_segmenter(
    name="my-manipulator-segmenter",
    external_data=trajectory_npz,
    domain="manipulation",
    epochs=40,   # optional; server picks a sensible default when unset
)
```

Poll until training completes:

```python theme={null}
import time

segmenter_status = client.get_segmenter_status(segmenter_job["job_id"])
while segmenter_status["status"] not in {"completed", "failed"}:
    print("segmenter training:", segmenter_status["status"])
    time.sleep(15)
    segmenter_status = client.get_segmenter_status(segmenter_job["job_id"])
```

`get_segmenter_status` returns `status`, `segmenter_id` (populated once
`status == "completed"`), `created_at` / `completed_at`, and `error` on failure.

## 2. Run automated sub-task annotation

With the model trained, pass its ID into `analyze()` alongside
`AnalysisType.ACTION_SEGMENTATION`. Sub-task boundaries now come from the trajectory
phases the model learned.

```python title="Analyze videos with your trained segmentation model" theme={null}
if segmenter_status["status"] != "completed":
    raise RuntimeError(f"Segmenter training failed: {segmenter_status.get('error')}")

segmenter_id = segmenter_status["segmenter_id"]

folder_videos = client.my_videos(folder="YOUR_FOLDER_NAME", scope="org")
videos = [v["video_id"] for v in folder_videos[:10]]

segmentation_result = client.analyze(
    videos,
    analysis_type=AnalysisType.ACTION_SEGMENTATION,
    segmenter_id=segmenter_id,
)

batch_id = segmentation_result["batch_metadata"]["batch_id"]
```

`segmenter_id` is accepted by `client.analyze(...)` for single videos, lists of video
IDs, and folder/batch calls when `analysis_type=AnalysisType.ACTION_SEGMENTATION`.

### Review the segmented sub-tasks

Each event is a short manipulation sub-task with a natural-language label. Rather than
treating each span as its own clip, the export step below stitches these spans back
onto the full video as a per-frame sub-task timeline, giving VLAs like GR00T the
language conditioning signal they train on without breaking the continuous
demonstration apart.

```python theme={null}
client.visualize(segmentation_result, width=920)

batch_results = client.get_batch_analysis(batch_id)
for entry in batch_results["results"][:2]:
    print(entry["video_id"], "-", len(entry.get("events", [])), "segments")
    for event in entry.get("events", [])[:5]:
        print("   ", event.get("t_start"), "-", event.get("t_end"), ":", event.get("label"))
```

## 3. Export to a LeRobot dataset

By default, each source video becomes one LeRobot episode, and each Nomadic-annotated
sub-task is included as a separate `task_index` inside that episode. If you prefer
the sub-tasks to be their own episodes, pass `episode_mode="per_segment"`.

```python title="Export a LeRobot v2.1 dataset for GR00T fine-tuning" theme={null}
export_result = client.export_lerobot_dataset(
    batch_id=batch_id,
    output_dir="./lerobot_dataset",
    trajectory_tool="manipulator_trajectory",
    camera_key="exterior",
    robot_type="franka",
)
```

**Required parameters:**

| Parameter               | Type           | Description                                                                                                |
| ----------------------- | -------------- | ---------------------------------------------------------------------------------------------------------- |
| `batch_id` or `results` | `str` / `dict` | An action-segmentation batch ID, or an already-fetched `get_batch_analysis()` payload (mutually exclusive) |
| `output_dir`            | `str`          | Local directory to write the dataset into                                                                  |

**Returns:** `output_dir`, `num_episodes`, `num_frames`, `num_tasks`, `tasks`, `fps`,
`state_dim`, `state_names`, `skipped_segments`, `warnings`.

**Requires:** `pip install 'nomadic[lerobot]'` (numpy, pandas, pyarrow) and the
`ffmpeg` / `ffprobe` binaries on `PATH`. Re-running against the same `output_dir`
wipes and regenerates it.

If `skipped_segments` isn't empty, those source videos didn't have a completed
`manipulator_trajectory` artifact to draw proprioception from. Point the pipeline at
your own manipulator footage with trajectory imported, or pass `trajectory_tool=None`
to export a video-only dataset (no `observation.state` / `action` features).

### Inspect the exported dataset

The layout matches what GR00T's fine-tuning pipeline expects: `meta/modality.json`
maps the flattened trajectory channels to named state/action groups, and each episode
is a `(parquet, mp4)` pair. `meta/episodes.jsonl`'s `tasks` list and the parquet's
`task_index` column are where the sub-task annotation actually lives. Check that
`task_index` changes over the course of the episode where you'd expect a sub-task
transition.

```python theme={null}
import json
from pathlib import Path
import pandas as pd

dataset_root = Path(export_result["output_dir"])

info = json.loads((dataset_root / "meta" / "info.json").read_text())
modality = json.loads((dataset_root / "meta" / "modality.json").read_text())

episode_df = pd.read_parquet(dataset_root / "data" / "chunk-000" / "episode_000000.parquet")
episode_df.head()
```

## 4. Finetune GR00T

The exported directory is ready to hand to NVIDIA's fine-tuning workflow:

1. Copy/mount `./lerobot_dataset` where your GR00T fine-tuning environment can read it.
2. Follow the [real-robot fine-tuning guide](https://docs.nvidia.com/learning/physical-ai/gr00t-e2e-workflow/latest/real-robot-workflow/real-fine-tuning-and-leapp.html).
   The exported `meta/modality.json` is auto-generated in the same spirit as the
   config defaults GR00T generates for its own data-collection pipeline; review
   and adjust the per-group `absolute`/`rotation_type` settings for your robot
   before training.
3. Launch `launch_finetune.py` pointed at `./lerobot_dataset`.

Happy fine-tuning!
