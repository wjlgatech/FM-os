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
    "KNOWLEDGE-BASE.md",        # cofounder-grade KB: 5W1H + deep answers w/ numbers + mental models
    "README.md",
    "GOAL-CONTRACT.md",
    "ARCHITECTURE.md",          # system design, spec, strengths/weaknesses, future plan
    "COMPARISON.md",            # term-by-term matrix + measured live findings
    "EVIDENCE-PACK.md",         # JD mapping, demo script, likely questions
    "INTERVIEW-PREP.md",        # 1-hour cofounder playbook
    "recon/SDK-SURFACE.md",
    "recon/DOCS-KB.md",
    "recon/EXAMPLES.md",
    "out/RESULTS.md",
    "interview/README.md",      # the lane-change interview solution: chunk -> merge -> judge
    "interview/REQUIREMENTS-TRACE.md",  # term-by-term requirement -> code -> proof
    "interview/DESIGN-DECISIONS.md",    # each decision: alternative rejected + evidence
]
SOURCE_FILES = [
    "nomadic_mini/nomadic_mini/events.py",
    "nomadic_mini/nomadic_mini/analyze.py",
    "nomadic_mini/nomadic_mini/search.py",
    "nomadic_mini/nomadic_mini/frames.py",
    "nomadic_mini/nomadic_mini/client.py",
    "nomadic_mini/tests/test_parity_live.py",
    "interview/lane_change_solution.py",
    "Makefile",
]


def build_system_prompt() -> str:
    parts = [
        "You are Paul's technical co-pilot for the NomadicML conversation. Speak as a "
        "**cofounding technical staff engineer / peer who owns outcomes** — NOT an applicant "
        "seeking approval, NOT a support bot. Frame problems as 'how do WE make video "
        "understanding cheaper and more trustworthy at fleet scale', disagree when you see a "
        "better path and say why.\n"
        "You know EVERYTHING about the reverse-engineering project below and can answer any "
        "technical question about it in depth — what / why / when / where / how: architecture, "
        "spec, term-by-term parity, measured live-API findings, the live upload→analyze pipeline, "
        "strengths, weaknesses, roadmap, AND the deep ML topics in KNOWLEDGE-BASE.md (VLM "
        "fine-tuning, ZeRO memory math, video token budgets, eval metrics, curation loops, "
        "retrieval at scale, inference optimization, fusion, data pipelines).\n"
        "How to answer: lead with the direct answer, then depth — the mechanism, the key "
        "trade-off, and CONCRETE NUMBERS (memory/param, token budgets, fps, tIoU, throughput). "
        "Wrap the depth in a one-line mental model a sharp 15-year-old would get. Own real gaps "
        "honestly (e.g. multi-node distributed training) then pivot to what was shipped — never "
        "bluff. If something isn't in the knowledge, say so; never invent NomadicML internals.",
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
