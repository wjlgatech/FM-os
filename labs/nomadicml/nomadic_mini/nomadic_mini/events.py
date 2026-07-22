"""Event + analysis document models.

Field names mirror NomadicML's schemas VERBATIM so outputs diff term-by-term
against their production API. Two schemas coexist upstream:

  SDK RapidReviewEvent (nomadicml 0.1.53, video.py — the customer contract):
      t_start "MM:SS", t_end, category, label, severity, aiAnalysis,
      confidence, approval, overlay
  Docs/REST event (docs.nomadicml.com api-reference/analysis):
      label, t_start, t_end, type, description, severity, confidence

We mirror the SDK contract (what a customer's code actually touches) and keep
`type`/`description` as computed aliases for the docs variant, so the parity
harness can compare against either surface.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

_MMSS = re.compile(r"^\d{1,3}:[0-5]\d$")

# Verbatim agent categories from nomadicml SDK (video.py) — used as the
# canonical `category` vocabulary so parity diffs are string-equal.
CATEGORIES = [
    "Lane Change Detection",
    "Vehicle Turns",
    "Relative Motion Analysis",
    "Driving Violations",
    "Edge Case",
    "Other",
]


class MotionEvent(BaseModel):
    label: str
    t_start: str = Field(description="MM:SS")
    t_end: str = Field(description="MM:SS")
    category: str = Field(description="one of CATEGORIES (verbatim SDK vocabulary)")
    severity: Literal["low", "medium", "high"]
    aiAnalysis: str = Field(description="model reasoning / event description")
    confidence: float = Field(ge=0.0, le=1.0)
    approval: Literal["approved", "rejected", "pending", "invalid"] = "pending"
    overlay: dict = Field(default_factory=dict)

    @field_validator("t_start", "t_end")
    @classmethod
    def _mmss(cls, v: str) -> str:
        if not _MMSS.match(v):
            raise ValueError(f"timestamp must be MM:SS, got {v!r}")
        return v

    def t_start_seconds(self) -> float:
        m, s = self.t_start.split(":")
        return int(m) * 60 + int(s)

    # ---- docs/REST-variant aliases (for parity vs the raw API) ----
    @property
    def type(self) -> str:
        return self.category

    @property
    def description(self) -> str:
        return self.aiAnalysis


class AnalysisDocument(BaseModel):
    """Mirrors GET /api/videos/{video_id}/analyses/{analysis_id}."""
    video_id: str
    analysis_id: str
    analysis: str = Field(description="natural-language summary of the run")
    metadata: dict = Field(default_factory=dict)
    events: list[MotionEvent] = Field(default_factory=list)


class SearchMatch(BaseModel):
    video_id: str
    analysis_id: str
    event_index: int
    similarity: float
    reason: str


class SearchResult(BaseModel):
    """Mirrors the /api/search session result: {summary, thoughts, matches}."""
    summary: str
    thoughts: list[str] = Field(default_factory=list)
    matches: list[SearchMatch] = Field(default_factory=list)


def seconds_to_mmss(t: float) -> str:
    t = max(0, int(round(t)))
    return f"{t // 60:02d}:{t % 60:02d}"
