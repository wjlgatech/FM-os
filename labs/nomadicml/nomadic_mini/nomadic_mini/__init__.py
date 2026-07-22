"""nomadic_mini — clean-room, small-scale reconstruction of the NomadicML
video-analysis pipeline, built only from public docs and the published SDK
surface, as verifiable interview proof-of-capability."""

from .analyze import analyze
from .client import MiniClient, NomadicLive
from .events import CATEGORIES, AnalysisDocument, MotionEvent, SearchResult
from .search import EventIndex

__all__ = [
    "analyze", "MiniClient", "NomadicLive", "MotionEvent",
    "AnalysisDocument", "SearchResult", "EventIndex", "CATEGORIES",
]
