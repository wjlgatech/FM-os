"""Live rehearsal for the interview — runs the full pipeline on the real interview video.

Requires GEMINI_API_KEY (your own; the notebook's embedded key will be revoked).
Free-tier keys have no gemini-2.5-pro quota — override with GEMINI_MODEL=gemini-2.5-flash.

    GEMINI_API_KEY=... python3 run_live.py [--chunk 20] [--overlap 5] [--votes 3]

Prints the three-stage scoreboard: naive -> chunked -> validated.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from lane_change_solution import (
    CHUNK_PROMPT,
    GROUND_TRUTH,
    LaneChanges,
    detect_chunked,
    mmss_to_seconds,
    report,
    score_predictions,
    seconds_to_mmss,
    to_output_json,
    validate_all,
)

RESULTS_JSON = Path(__file__).parent / "live_results.json"

VIDEO_URL = "https://storage.googleapis.com/videolm-bc319.firebasestorage.app/videos/b16cef459d954371a92e4c4bb1cc9071.mp4"
VIDEO_PATH = Path(__file__).parent / "video.mp4"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")


def download_video() -> Path:
    if VIDEO_PATH.exists():
        return VIDEO_PATH
    import httpx

    print(f"downloading interview video -> {VIDEO_PATH}")
    with httpx.stream("GET", VIDEO_URL, timeout=120) as r:
        r.raise_for_status()
        with open(VIDEO_PATH, "wb") as f:
            for chunk in r.iter_bytes(8192):
                f.write(chunk)
    return VIDEO_PATH


def upload_gemini(client, video_path: Path):
    myfile = client.files.upload(file=str(video_path))
    while myfile.state and myfile.state.name == "PROCESSING":
        time.sleep(3)
        myfile = client.files.get(name=myfile.name)
    if myfile.state and myfile.state.name == "FAILED":
        raise RuntimeError("Gemini file processing failed")
    return myfile


def _generate_with_retry(client, max_attempts: int = 8, **kwargs):
    """Back off and retry on transient errors: 429 (free tier is ~5 req/min) and 5xx
    (flash regularly throws 503 UNAVAILABLE under load)."""
    from google.genai import errors as gerrors

    for attempt in range(max_attempts):
        try:
            return client.models.generate_content(**kwargs)
        except gerrors.APIError as e:
            if e.code not in (429, 500, 503, 504) or attempt == max_attempts - 1:
                raise
            wait = 20 * (attempt + 1)
            print(f"  {e.code} from API, retrying in {wait}s ({attempt + 1}/{max_attempts})")
            time.sleep(wait)


def make_gemini_inference(client):
    """Byte-for-byte mirror of the notebook's gemini_inference signature."""
    from google.genai import types as gtypes

    def gemini_inference(query: str, video=None, enable_thinking: bool = True,
                         time_interval: Optional[tuple] = None, fps: Optional[int] = None,
                         schema: Optional[type[BaseModel]] = None):
        contents = []
        cfg = {"thinkingConfig": gtypes.ThinkingConfig(thinking_budget=-1 if enable_thinking else 0)}
        if schema:
            cfg["responseMimeType"] = "application/json"
            cfg["responseSchema"] = schema
        if video is not None:
            meta = {}
            if fps:
                meta["fps"] = fps
            if time_interval and time_interval[0] < time_interval[1]:
                meta["startOffset"] = f"{time_interval[0]}s"
                meta["endOffset"] = f"{time_interval[1]}s"
            contents.append(gtypes.Part(
                file_data=gtypes.FileData(file_uri=video.uri, mime_type=video.mime_type),
                video_metadata=gtypes.VideoMetadata(**meta),
            ))
        contents.append(query)
        res = _generate_with_retry(
            client, model=MODEL, contents=contents,
            config=gtypes.GenerateContentConfig(**cfg))
        return res.text

    return gemini_inference


def _extract_window_frames(video_path: Path, t0: float, t1: float, fps: float,
                           max_frames: int = 20, height: int = 360) -> list[tuple[float, str]]:
    """Sample (clip_relative_seconds, jpeg_b64) frames from [t0, t1] via ffmpeg."""
    import base64
    import subprocess
    import tempfile

    span = max(t1 - t0, 1e-6)
    eff_fps = min(fps, max_frames / span)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(span), "-i", str(video_path),
             "-vf", f"fps={eff_fps},scale=-2:{height}", "-frames:v", str(max_frames),
             "-q:v", "4", f"{td}/f_%05d.jpg"],
            check=True,
        )
        return [(round(i / eff_fps, 1), base64.b64encode(p.read_bytes()).decode())
                for i, p in enumerate(sorted(Path(td).glob("f_*.jpg")))]


def make_claude_inference(video_path: Path, duration: float):
    """Same infer_fn signature, but Claude over ffmpeg-sampled frames — proves the
    pipeline is VLM-agnostic (the whole solution swaps models by swapping this seam).
    Frames are captioned with CLIP-RELATIVE seconds, so the window-relative timestamp
    contract (and our remap) is exercised exactly as with Gemini's start/endOffset."""
    import re

    import anthropic

    client = anthropic.Anthropic()

    def infer(query: str, video=None, enable_thinking: bool = True,
              time_interval: Optional[tuple] = None, fps: Optional[int] = None,
              schema: Optional[type[BaseModel]] = None):
        t0, t1 = time_interval if time_interval else (0.0, duration)
        frames = _extract_window_frames(video_path, t0, t1, fps or 1.0, max_frames=40)
        content: list[dict] = []
        for t_rel, b64 in frames:
            content.append({"type": "text", "text": f"[frame at {t_rel:.1f}s into this clip]"})
            content.append({"type": "image", "source": {
                "type": "base64", "media_type": "image/jpeg", "data": b64}})
        prompt = ("These are consecutive frames from one continuous clip. Track the painted "
                  "lane markings' horizontal position across consecutive frames: during an ego "
                  "lane change the markings sweep sideways across the image until the car "
                  "settles between a new pair of markings.\n"
                  "Each image's caption is its timestamp within the clip. When you report an "
                  "event, take t_start/t_end from the captions of the frames where it begins "
                  "and ends — caption-based estimates are expected; do NOT abstain because "
                  "exact timing is uncertain. Failing to report a visible ego lane change is "
                  "a worse error than an imprecise timestamp.\n\n") + query
        if schema:
            prompt += ("\n\nReply with ONLY a JSON object matching this schema (no prose):\n"
                       + json.dumps(schema.model_json_schema()))
        content.append({"type": "text", "text": prompt})
        text = ""
        for attempt in range(3):  # occasionally returns a bare thinking block, empty text
            res = client.messages.create(model="claude-sonnet-5", max_tokens=2000,
                                         messages=[{"role": "user", "content": content}])
            text = "".join(b.text for b in res.content if b.type == "text")
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                return m.group(0)
            time.sleep(2)
        raise ValueError(f"no JSON in Claude output after 3 tries: {text[:200]!r}")

    return infer


def naive_baseline(infer_fn, video_file) -> list[dict]:
    text = infer_fn(query=CHUNK_PROMPT.replace("SHORT CLIP cut from a longer highway drive",
                                               "highway driving video"),
                    video=video_file, schema=LaneChanges)
    return [{"t_start_s": mmss_to_seconds(e["t_start"]), "t_end_s": mmss_to_seconds(e["t_end"]),
             "direction": e["direction"], "description": e["description"]}
            for e in json.loads(text)["lane_changes"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", type=float, default=20.0)
    ap.add_argument("--overlap", type=float, default=5.0)
    ap.add_argument("--votes", type=int, default=3)
    ap.add_argument("--skip-naive", action="store_true", help="skip the whole-video baseline call")
    ap.add_argument("--backend", choices=["gemini", "claude"], default="gemini",
                    help="claude = same pipeline over frame sampling (no Gemini quota needed)")
    ap.add_argument("--out", default=None, help="bank results to this JSON instead of live_results.json")
    args = ap.parse_args()
    if args.out:
        global RESULTS_JSON
        RESULTS_JSON = Path(args.out)

    video_path = download_video()

    from lane_change_solution import video_duration_seconds
    try:
        duration = video_duration_seconds(str(video_path))
    except ImportError:  # no cv2 -> ffprobe fallback
        import subprocess
        duration = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
             str(video_path)], capture_output=True, text=True, check=True).stdout.strip())
    global MODEL
    if args.backend == "claude":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("set ANTHROPIC_API_KEY for --backend claude")
        MODEL = "claude-sonnet-5/frames"
        print(f"video duration: {duration:.1f}s, model: {MODEL}")
        video_file = None
        infer_fn = make_claude_inference(video_path, duration)
    else:
        if not os.environ.get("GEMINI_API_KEY"):
            raise SystemExit("set GEMINI_API_KEY (use GEMINI_MODEL=gemini-2.5-flash on free tier)")
        from google import genai

        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        print(f"video duration: {duration:.1f}s, model: {MODEL}")
        t0 = time.time()
        video_file = upload_gemini(client, video_path)
        print(f"upload+processing took {time.time() - t0:.1f}s")
        infer_fn = make_gemini_inference(client)

    stages = []

    def bank(title: str, events: list[dict]):
        stages.append({"title": title, "score": score_predictions(events, GROUND_TRUTH),
                       "events": to_output_json(events)["lane_changes"]})
        RESULTS_JSON.write_text(json.dumps({
            "model": MODEL, "duration_s": duration,
            "ground_truth": [{"t_start": seconds_to_mmss(s), "t_end": seconds_to_mmss(e),
                              "direction": d, "label": lbl} for s, e, d, lbl in GROUND_TRUTH],
            "stages": stages,
        }, indent=2))

    if not args.skip_naive:
        naive = naive_baseline(infer_fn, video_file)
        print("\n" + report(naive, GROUND_TRUTH, title="Stage 0: naive whole-video"))
        bank("Stage 0: naive whole-video", naive)

    candidates = detect_chunked(infer_fn, video_file, duration,
                                chunk=args.chunk, overlap=args.overlap,
                                fps=2 if args.backend == "claude" else None,
                                samples=3 if args.backend == "claude" else 2)
    # recall-first union: pixel-level motion scan nominates candidates the VLM missed
    # (zero model calls); judge + boundary refinement restore precision downstream
    from motion_check import nominate_candidates

    from lane_change_solution import merge_events
    noms = nominate_candidates(str(video_path))
    print(f"motion scan nominated {len(noms)} candidate(s)")
    candidates = merge_events(candidates + noms)
    print("\n" + report(candidates, GROUND_TRUTH, title="Stage 1: VLM windows + motion scan"))
    bank("Stage 1: VLM windows + motion scan", candidates)

    validated = validate_all(infer_fn, video_file, candidates, duration,
                             video_path=str(video_path), votes=args.votes)
    validated = merge_events(validated)  # refined boundaries can make same-direction keeps overlap
    print("\n" + report(validated, GROUND_TRUTH, title="Stage 2: judge-validated"))
    bank("Stage 2: judge-validated", validated)

    print("\nFinal structured output:")
    print(json.dumps(to_output_json(validated), indent=2))
    print(f"\nresults banked -> {RESULTS_JSON}")


if __name__ == "__main__":
    main()
