"""Live analysis backend — run the REAL pipeline on a user's clip.

Input: {url: <blob or direct video URL>, prompt?: str, password: str}. Streams SSE
stage events (received → downloading → uploading-to-model → processing → generating →
parsing → done) so the client drives a real progress bar, then returns events in the
verbatim NomadicML schema (label, t_start, t_end, category, severity, aiAnalysis, confidence).

Gemini native video (no ffmpeg needed in the serverless runtime). Fast mode (flash,
thinking_budget=0) to fit the function time budget; honest timeout, never a fake result.
"""

import json
import os
import re
import time
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler

APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
CATEGORIES = ["Lane Change Detection", "Vehicle Turns", "Relative Motion Analysis",
              "Driving Violations", "Edge Case", "Other"]
DEFAULT_PROMPT = "Find driving events: turns, lane changes, merges, hard brakes, and anomalies."

SYSTEM_PROMPT = """You are a driving-video analyst for autonomous-vehicle data curation.
Detect discrete MOTION EVENTS relevant to the user's query. Return ONLY JSON:
{"analysis":"<2-4 sentence summary>","events":[{"label":"<short>","t_start":"MM:SS","t_end":"MM:SS",
"category":"<one of: Lane Change Detection | Vehicle Turns | Relative Motion Analysis | Driving Violations | Edge Case | Other>",
"severity":"low|medium|high","aiAnalysis":"<1-3 sentence reasoning>","confidence":<0.0-1.0>}]}
Timestamps within the clip. Report only events you can actually see."""

_MMSS = re.compile(r"^\d{1,3}:[0-5]\d$")


def _sanitize(raw: dict, backend: str) -> dict:
    events = []
    for e in raw.get("events", []):
        try:
            ts, te = str(e["t_start"]), str(e["t_end"])
            if not (_MMSS.match(ts) and _MMSS.match(te)):
                continue
            cat = e.get("category", "Other")
            events.append({
                "label": str(e.get("label", "Event"))[:120],
                "t_start": ts, "t_end": te,
                "category": cat if cat in CATEGORIES else "Other",
                "severity": e.get("severity") if e.get("severity") in ("low", "medium", "high") else "medium",
                "aiAnalysis": str(e.get("aiAnalysis", ""))[:600],
                "confidence": max(0.0, min(1.0, float(e.get("confidence", 0.8)))),
                "approval": "pending",
            })
        except Exception:
            continue
    events.sort(key=lambda x: (int(x["t_start"].split(":")[0]) * 60 + int(x["t_start"].split(":")[1])))
    return {"video_id": f"vid-{uuid.uuid4().hex[:10]}", "analysis_id": f"mini-{uuid.uuid4().hex[:12]}",
            "analysis": str(raw.get("analysis", ""))[:800], "metadata": {"backend": backend},
            "events": events}


class handler(BaseHTTPRequestHandler):
    def _sse(self, obj):
        try:
            self.wfile.write(f"data: {json.dumps(obj)}\n\n".encode()); self.wfile.flush()
        except Exception:
            pass

    def _stage(self, name, pct, note=""):
        self._sse({"stage": name, "pct": pct, "note": note})

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            n = int(self.headers.get("content-length", 0))
            body = json.loads(self.rfile.read(n) or "{}")
            if not APP_PASSWORD or body.get("password") != APP_PASSWORD:
                self._sse({"error": "unauthorized — enter the demo password"}); return
            url = (body.get("url") or "").strip()
            if not re.match(r"^https?://", url):
                self._sse({"error": "provide a video URL (upload a file or paste a direct link)"}); return
            prompt = (body.get("prompt") or DEFAULT_PROMPT).strip()

            from google import genai
            from google.genai import types as gt
            client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

            self._stage("downloading", 45, "fetching your clip")
            path = f"/tmp/{uuid.uuid4().hex}.mp4"
            req = urllib.request.Request(url, headers={  # some CDNs 403 the default UA
                "User-Agent": "Mozilla/5.0 (compatible; nomadic-mini/1.0)"})
            cap = 150 * 1024 * 1024
            with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as out:  # noqa: S310
                got = 0
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    got += len(chunk)
                    if got > cap:
                        self._sse({"error": "clip too large (>150 MB)"}); return
                    out.write(chunk)

            self._stage("uploading", 60, "handing the video to the model")
            f = client.files.upload(file=path)
            self._stage("processing", 70, "model is decoding frames")
            waited = 0
            while f.state and f.state.name == "PROCESSING" and waited < 40:
                time.sleep(2); waited += 2
                self._stage("processing", min(70 + waited, 85), f"decoding… {waited}s")
                f = client.files.get(name=f.name)
            if f.state and f.state.name == "FAILED":
                self._sse({"error": "the model could not decode this video"}); return

            self._stage("generating", 90, "reasoning over the clip")
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[f, f"{SYSTEM_PROMPT}\n\nUser query: {prompt}"],
                config=gt.GenerateContentConfig(thinking_config=gt.ThinkingConfig(thinking_budget=0)),
            )
            self._stage("parsing", 97, "structuring events")
            m = re.search(r"\{.*\}", res.text or "", re.DOTALL)
            if not m:
                self._sse({"error": "model returned no structured events"}); return
            doc = _sanitize(json.loads(m.group(0)), "gemini/2.5-flash/fast")
            try:
                client.files.delete(name=f.name)
            except Exception:
                pass
            self._sse({"stage": "done", "pct": 100, "document": doc})
        except Exception as e:
            self._sse({"error": f"{type(e).__name__}: {e}"})
