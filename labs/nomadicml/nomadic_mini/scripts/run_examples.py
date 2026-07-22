"""Reproduce NomadicML's public examples (verbatim queries) on our own clips.

Their examples (recon/EXAMPLES.md):
  1. Driving Violations   — "Find driving violations and cite their relevant DMV code."
  2. Behavior Recognition — "Find lane merge instances."
  3. Multi-Query hazard   — roadside-vehicle hazard query (verbatim, abridged input set)

Writes out/<clip>__<example>.json (full AnalysisDocument) + out/RESULTS.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nomadic_mini.client import MiniClient  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

EXAMPLES = {
    "driving-violations": "Find driving violations and cite their relevant DMV code.",
    "lane-merges": "Find lane merge instances.",
    "roadside-hazard": (
        "Determine whether a stopped, disabled, or roadside vehicle creates a hazard "
        "for the ego vehicle — close enough to the travel lane to narrow the path, "
        "require a lane shift or move-over, or create a close-pass risk."
    ),
}

CLIPS = ["drive_city_34s.mp4", "drive_highway_51s.mp4"]


def main() -> None:
    client = MiniClient()
    lines = ["# nomadic_mini — reproduction of NomadicML public examples",
             "", "Verbatim queries from nomadicai.com/examples, run on our own",
             "CC-licensed clips (data/SOURCES.txt) through the clean-room pipeline.", ""]

    for clip in CLIPS:
        vid = client.upload(DATA / clip)
        lines.append(f"## {clip}")
        for name, query in EXAMPLES.items():
            doc = client.analyze(vid, query, mode="thinking")
            (OUT / f"{clip.removesuffix('.mp4')}__{name}.json").write_text(
                doc.model_dump_json(indent=2))
            lines.append(f"\n### {name} — query: {query!r}")
            lines.append(f"\n> {doc.analysis}\n")
            if not doc.events:
                lines.append("- (no events detected)")
            for e in doc.events:
                lines.append(
                    f"- [{e.t_start}–{e.t_end}] **{e.label}** ({e.category}, "
                    f"{e.severity}, conf {e.confidence:.2f}) — {e.aiAnalysis}")
            print(f"{clip} / {name}: {len(doc.events)} events")
        lines.append("")

    for query in ["vehicle merging into ego lane", "stop sign or traffic violation",
                  "hazard requiring a lane shift"]:
        res = client.search(query)
        lines.append(f"## search: {query!r}")
        lines.append(f"summary: {res.summary}")
        for m in res.matches[:3]:
            lines.append(f"- sim {m.similarity:.3f} · {m.video_id} · event {m.event_index} — {m.reason[:110]}")
        lines.append("")

    (OUT / "RESULTS.md").write_text("\n".join(lines))
    print(f"\nwrote {OUT}/RESULTS.md")


if __name__ == "__main__":
    main()
