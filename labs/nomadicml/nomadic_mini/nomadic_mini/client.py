"""Two clients, one method vocabulary.

MiniClient      — our local clean-room pipeline, exposing the same verbs a
                  NomadicML customer uses: upload() -> analyze() -> search().
NomadicLive     — a thin REST client for the REAL production API
                  (api-prod.nomadicml.com), built from the documented surface,
                  used by the parity harness. Requires NOMADICML_API_KEY.

Endpoint paths and headers are verbatim from nomadicml 0.1.53 source and
docs.nomadicml.com (see ../COMPARISON.md for the full term-by-term map).
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path

import httpx

from .analyze import analyze as _vlm_analyze
from .events import AnalysisDocument, SearchMatch, SearchResult
from .search import EventIndex


class MiniClient:
    """Local reconstruction: same customer-facing verbs, our own engine."""

    def __init__(self):
        self._videos: dict[str, Path] = {}
        self._analyses: dict[str, AnalysisDocument] = {}
        self._index = EventIndex()

    def upload(self, path: str | Path) -> str:
        video_id = f"vid-{uuid.uuid4().hex[:10]}"
        self._videos[video_id] = Path(path)
        return video_id

    def analyze(self, video_id: str, prompt: str, mode: str = "thinking") -> AnalysisDocument:
        doc = _vlm_analyze(self._videos[video_id], prompt, mode=mode)
        doc = doc.model_copy(update={"video_id": video_id})
        self._analyses[doc.analysis_id] = doc
        self._index.add([
            {**e.model_dump(), "video_id": video_id,
             "analysis_id": doc.analysis_id, "event_index": i}
            for i, e in enumerate(doc.events)
        ])
        return doc

    def get_analysis(self, analysis_id: str) -> AnalysisDocument:
        return self._analyses[analysis_id]

    def search(self, query: str, top_k: int = 5) -> SearchResult:
        hits = self._index.query(query, top_k=top_k)
        matches = [
            SearchMatch(
                video_id=e["video_id"], analysis_id=e["analysis_id"],
                event_index=e["event_index"], similarity=round(score, 4),
                reason=e.get("aiAnalysis", ""),
            )
            for score, e in hits
        ]
        return SearchResult(
            summary=f"{len(matches)} event(s) matched {query!r}",
            thoughts=[f"embedded query and ranked {len(self._index._events)} indexed events by cosine similarity"],
            matches=matches,
        )


class NomadicLive:
    """Minimal real-API client (documented surface only). Parity-harness use."""

    BASE_URL = "https://api-prod.nomadicml.com"

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.environ.get("NOMADICML_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("NOMADICML_API_KEY not set")
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self._http = httpx.Client(
            timeout=900,
            headers={
                # verbatim: nomadicml/client.py sends both header forms
                "X-API-Key": self.api_key,
                "Authorization": f"Bearer {self.api_key}",
                "X-Client-Type": "SDK",
            },
        )

    def verify_key(self) -> dict:
        r = self._http.post(f"{self.base_url}/api/keys/verify")
        r.raise_for_status()
        return r.json()

    def my_videos(self, scope: str | None = None) -> list[dict]:
        params = {"firebase_collection_name": "videos",
                  "folder_collection": "videoFolders"}
        if scope:
            params["scope"] = scope
        r = self._http.get(f"{self.base_url}/api/my-videos", params=params)
        r.raise_for_status()
        return r.json().get("videos", [])

    def upload(self, path: str | Path) -> str:
        with open(path, "rb") as f:
            r = self._http.post(
                f"{self.base_url}/api/upload-video",
                data={"source": "file"},
                files={"file": (Path(path).name, f, "video/mp4")},
            )
        r.raise_for_status()
        return r.json()["video_id"]

    def wait_uploaded(self, video_id: str, timeout: float = 600) -> dict:
        t0 = time.time()
        while time.time() - t0 < timeout:
            r = self._http.get(f"{self.base_url}/api/video/{video_id}/status")
            r.raise_for_status()
            status = r.json()
            state = (status.get("visual_analysis", {}).get("status", {}) or {}).get("status")
            if state == "UPLOADED":
                return status
            time.sleep(5)
        raise TimeoutError(f"video {video_id} not UPLOADED after {timeout}s")

    def analyze_start(self, video_id: str, prompt: str) -> dict:
        r = self._http.post(
            f"{self.base_url}/api/router/v2/query/start",
            json={"query": prompt, "video_id": video_id},
        )
        r.raise_for_status()
        return r.json()  # {stream_id, status, batch_id}

    def analyze_events(self, stream_id: str, last_id: str = "") -> list[dict]:
        """Read the SSE progress feed once (parity harness polls)."""
        events = []
        with self._http.stream(
            "GET",
            f"{self.base_url}/api/router/v2/query/events/{stream_id}",
            params={"last_id": last_id} if last_id else None,
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line.startswith("data:"):
                    try:
                        events.append(json.loads(line[5:].strip()))
                    except json.JSONDecodeError:
                        pass
                    if events and events[-1].get("event") in ("done", "error"):
                        break
        return events

    def get_analysis(self, video_id: str, analysis_id: str) -> dict:
        r = self._http.get(f"{self.base_url}/api/videos/{video_id}/analyses/{analysis_id}")
        r.raise_for_status()
        return r.json()  # {video_id, analysis_id, analysis, metadata, events[]}
