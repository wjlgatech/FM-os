"""Real lab-copilot backend, as a Vercel Python serverless function.

Calls Claude for real, grounded in the bundled knowledge pack (_knowledge.txt,
assembled at build time from every lab artifact). No mock, no canned replies.
Returns the answer over SSE so the existing front end renders it unchanged.
"""

import json
import os
from http.server import BaseHTTPRequestHandler
from pathlib import Path

import anthropic

KNOWLEDGE = (Path(__file__).parent / "_knowledge.txt").read_text()
MODEL = os.environ.get("COPILOT_MODEL", "claude-sonnet-5")
MAX_CHARS = 4000  # per-message input guard (public endpoint)
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")  # gate on the credit-spending endpoint


class handler(BaseHTTPRequestHandler):
    def _sse(self, obj):
        self.wfile.write(f"data: {json.dumps(obj)}\n\n".encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            if APP_PASSWORD and self.headers.get("x-app-password") != APP_PASSWORD:
                self._sse({"error": "unauthorized — enter the demo password"})
                return
            n = int(self.headers.get("content-length", 0))
            body = json.loads(self.rfile.read(n) or "{}")
            messages = [
                {"role": m["role"], "content": str(m["content"])[:MAX_CHARS]}
                for m in body.get("messages", [])[-12:]
                if m.get("role") in ("user", "assistant") and m.get("content")
            ]
            if not messages:
                self._sse({"error": "no message"})
                return
            client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
            resp = client.messages.create(
                model=MODEL,
                max_tokens=1500,
                system=[{"type": "text", "text": KNOWLEDGE,
                         "cache_control": {"type": "ephemeral"}}],
                messages=messages,
            )
            text = "".join(b.text for b in resp.content if b.type == "text")
            self._sse({"delta": text})
            self._sse({"done": True})
        except Exception as e:  # surface the real error to the UI, never fake success
            self._sse({"error": str(e)})
