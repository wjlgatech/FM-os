"""Frame extraction via ffmpeg — the frames-as-images path for VLMs without native video input."""

from __future__ import annotations

import base64
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Frame:
    t_seconds: float
    jpeg_b64: str


def video_duration(path: str | Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def extract_frames(path: str | Path, fps: float = 1.0, max_frames: int = 60,
                   height: int = 480) -> list[Frame]:
    """Sample frames at `fps`, capped at `max_frames`, downscaled to `height`."""
    duration = video_duration(path)
    effective_fps = min(fps, max_frames / max(duration, 1e-6))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(path),
             "-vf", f"fps={effective_fps},scale=-2:{height}",
             "-frames:v", str(max_frames), "-q:v", "4",
             f"{td}/f_%05d.jpg"],
            check=True,
        )
        frames = []
        for i, f in enumerate(sorted(Path(td).glob("f_*.jpg"))):
            frames.append(Frame(
                t_seconds=round(i / effective_fps, 2),
                jpeg_b64=base64.b64encode(f.read_bytes()).decode(),
            ))
    return frames
