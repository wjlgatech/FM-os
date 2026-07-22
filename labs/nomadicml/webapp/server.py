"""Demo webapp for the NomadicML reverse-engineering lab.

- Serves the visual-first demo page (static/) and the two driving clips (data/).
- /api/results   — aggregated real analysis results (out/*.json), for the timelines.
- /api/chat      — the lab copilot: Anthropic, SSE-streamed plain text, system prompt
                   assembled LIVE from the lab's own artifacts (no second copy of truth).

Run: python3 webapp/server.py   (http://127.0.0.1:8787)
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

LAB = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"

# Every artifact the copilot must know, in reading order. Assembled at startup
# straight from disk so the agent's knowledge can never drift from the lab.
KNOWLEDGE_FILES = [
    "README.md",
    "GOAL-CONTRACT.md",
    "ARCHITECTURE.md",          # system design, spec, strengths/weaknesses, future plan
    "COMPARISON.md",            # term-by-term matrix + measured live findings
    "EVIDENCE-PACK.md",         # JD mapping, demo script, likely questions
    "recon/SDK-SURFACE.md",
    "recon/DOCS-KB.md",
    "recon/EXAMPLES.md",
    "out/RESULTS.md",
]
SOURCE_FILES = [
    "nomadic_mini/nomadic_mini/events.py",
    "nomadic_mini/nomadic_mini/analyze.py",
    "nomadic_mini/nomadic_mini/search.py",
    "nomadic_mini/nomadic_mini/frames.py",
    "nomadic_mini/nomadic_mini/client.py",
    "nomadic_mini/tests/test_parity_live.py",
    "Makefile",
]


def build_system_prompt() -> str:
    parts = [
        "You are the lab copilot for `labs/nomadicml` — a clean-room, small-scale "
        "reverse-engineering of NomadicML's video-analysis product, built as interview "
        "proof-of-capability for the Member of Technical Staff (ML) role. You know every "
        "detail below: architecture, detailed spec, term-by-term parity results, measured "
        "live-API findings, strengths, weaknesses, and the future plan.\n"
        "Answer visually-minded and concise: short paragraphs, concrete file/field names, "
        "timestamps, and numbers. When asked about something not in the knowledge, say so "
        "plainly — never invent. Attribute every claim (file or measured response).",
        "\n\n===== LAB ARTIFACTS =====",
    ]
    for rel in KNOWLEDGE_FILES:
        p = LAB / rel
        if p.exists():
            parts.append(f"\n\n----- {rel} -----\n{p.read_text()}")
    parts.append("\n\n===== ENGINE SOURCE (the actual implementation) =====")
    for rel in SOURCE_FILES:
        p = LAB / rel
        if p.exists():
            parts.append(f"\n\n----- {rel} -----\n{p.read_text()}")
    return "".join(parts)


SYSTEM_PROMPT = build_system_prompt()
app = FastAPI(title="nomadic_mini lab demo")


class ChatMsg(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMsg]


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/results")
def results():
    docs = []
    for f in sorted((LAB / "out").glob("*.json")):
        d = json.loads(f.read_text())
        clip, _, example = f.stem.partition("__")
        d["_clip"], d["_example"] = f"{clip}.mp4", example
        docs.append(d)
    return JSONResponse({"documents": docs})


@app.post("/api/chat")
def chat(req: ChatRequest):
    import anthropic

    client = anthropic.Anthropic()
    model = os.environ.get("COPILOT_MODEL", "claude-sonnet-5")

    def stream():
        try:
            with client.messages.stream(
                model=model,
                max_tokens=1500,
                system=[{"type": "text", "text": SYSTEM_PROMPT,
                         "cache_control": {"type": "ephemeral"}}],
                messages=[m.model_dump() for m in req.messages[-12:]],
            ) as s:
                for text in s.text_stream:  # plain content only (playbook rule)
                    yield f"data: {json.dumps({'delta': text})}\n\n"
            yield "data: {\"done\": true}\n\n"
        except Exception as e:  # surface the real error to the UI, don't fail silent
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


app.mount("/data", StaticFiles(directory=LAB / "data"), name="data")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


if __name__ == "__main__":
    import uvicorn

    print(f"knowledge pack: {len(SYSTEM_PROMPT):,} chars from "
          f"{len(KNOWLEDGE_FILES) + len(SOURCE_FILES)} files")
    uvicorn.run(app, host="127.0.0.1", port=8787)
