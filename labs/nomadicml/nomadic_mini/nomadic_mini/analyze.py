"""Prompt-based video analysis — the VLM core.

Mirrors NomadicML's `client.analyze(video_id, prompt=..., mode=Thinking|Fast)`:
  - "thinking" mode -> gemini-2.5-pro (native video input, slower, more accurate)
  - "fast" mode     -> gemini-2.5-flash
  - fallback        -> Anthropic Claude over sampled frames (no native video input)

Output is coerced into the verbatim NomadicML event schema (events.py).
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from pathlib import Path

from .events import AnalysisDocument, MotionEvent
from .frames import extract_frames

SYSTEM_PROMPT = """You are a driving-video analyst for autonomous-vehicle data curation.
Watch the video and detect discrete MOTION EVENTS relevant to the user's query:
turns, lane changes, merges, hard brakes, near-misses, pedestrian/cyclist interactions,
traffic-signal events, and anomalies (unusual or unsafe situations).

Return ONLY a JSON object:
{
  "analysis": "<2-4 sentence overall summary>",
  "events": [
    {
      "label": "<short human label, e.g. 'Left lane change'>",
      "t_start": "MM:SS",
      "t_end": "MM:SS",
      "category": "<exactly one of: Lane Change Detection | Vehicle Turns | Relative Motion Analysis | Driving Violations | Edge Case | Other>",
      "severity": "low" | "medium" | "high",
      "aiAnalysis": "<1-3 sentences of reasoning: what happens, who is involved, why it matters>",
      "confidence": <0.0-1.0>
    }
  ]
}
Timestamps must be within the video duration. Report only events you can actually see."""


def _parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in model output: {text[:200]!r}")
    return json.loads(m.group(0))


def _to_document(raw: dict, video_id: str, backend: str, prompt: str) -> AnalysisDocument:
    events = [MotionEvent(**e) for e in raw.get("events", [])]
    return AnalysisDocument(
        video_id=video_id,
        analysis_id=f"mini-{uuid.uuid4().hex[:12]}",
        analysis=raw.get("analysis", ""),
        metadata={"backend": backend, "prompt": prompt},
        events=sorted(events, key=lambda e: e.t_start_seconds()),
    )


def analyze_gemini(video_path: str | Path, prompt: str, mode: str = "thinking") -> AnalysisDocument:
    from google import genai

    from google.genai import types as gtypes

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    # Mirror NomadicML's thinking/fast split. gemini-2.5-pro is the natural
    # "thinking" tier but is unavailable on free-tier keys (quota 0), so both
    # modes run on flash: thinking = dynamic reasoning budget, fast = budget 0.
    model = "gemini-2.5-flash"
    config = gtypes.GenerateContentConfig(
        thinking_config=gtypes.ThinkingConfig(
            thinking_budget=-1 if mode == "thinking" else 0)
    )

    uploaded = client.files.upload(file=str(video_path))
    while uploaded.state and uploaded.state.name == "PROCESSING":
        time.sleep(2)
        uploaded = client.files.get(name=uploaded.name)
    if uploaded.state and uploaded.state.name == "FAILED":
        raise RuntimeError(f"Gemini file processing failed for {video_path}")

    res = client.models.generate_content(
        model=model,
        contents=[uploaded, f"{SYSTEM_PROMPT}\n\nUser query: {prompt}"],
        config=config,
    )
    return _to_document(_parse_json(res.text), Path(video_path).stem,
                        f"gemini/{model}/{mode}", prompt)


def analyze_claude_frames(video_path: str | Path, prompt: str, fps: float = 0.5) -> AnalysisDocument:
    import anthropic

    frames = extract_frames(video_path, fps=fps, max_frames=20)
    content: list[dict] = []
    for fr in frames:
        content.append({"type": "text", "text": f"[frame at {fr.t_seconds:.0f}s]"})
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": "image/jpeg", "data": fr.jpeg_b64}})
    content.append({"type": "text", "text": f"{SYSTEM_PROMPT}\n\nUser query: {prompt}"})

    client = anthropic.Anthropic()
    res = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": content}],
    )
    text = "".join(b.text for b in res.content if b.type == "text")
    return _to_document(_parse_json(text), Path(video_path).stem, "anthropic/frames", prompt)


def analyze(video_path: str | Path, prompt: str, mode: str = "thinking") -> AnalysisDocument:
    """Backend-picking seam: Gemini native video first, Claude frames fallback."""
    if os.environ.get("GEMINI_API_KEY"):
        return analyze_gemini(video_path, prompt, mode)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return analyze_claude_frames(video_path, prompt)
    raise RuntimeError("no VLM backend: set GEMINI_API_KEY or ANTHROPIC_API_KEY")
