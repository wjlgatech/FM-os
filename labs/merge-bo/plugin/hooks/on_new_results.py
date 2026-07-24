#!/usr/bin/env python3
"""PostToolUse hook — advance a DBTL campaign the instant assay results are written.

Claude Code passes the tool event as JSON on stdin. If the just-written file is an
assay-results CSV in a campaign inbox (helix/campaigns/<name>.inbox.csv), this hook
auto-ingests the readouts into that campaign, refits, and emits the refreshed status +
the next proposed batch — closing the human-in-the-loop gap so no cycle stalls waiting
for someone to remember to run "ingest".

CSV format (header row):  candidate_id,<objective_or_constraint>,...
Exit 0 always (a hook must never block the session); it just prints an advisory.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def _load_helix():
    """Import the Helix engine relative to the plugin root (labs/merge-bo)."""
    here = Path(__file__).resolve()
    # plugin/hooks/on_new_results.py -> labs/merge-bo is two parents up from plugin/
    root = here.parent.parent.parent  # labs/merge-bo
    sys.path.insert(0, str(root))
    from helix.campaign import Campaign  # noqa: E402
    return Campaign


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    path_str = (event.get("tool_input", {}) or {}).get("file_path", "")
    if not path_str or not path_str.endswith(".inbox.csv"):
        return 0  # not an assay inbox write — nothing to do

    inbox = Path(path_str)
    campaign_file = inbox.with_name(inbox.name.replace(".inbox.csv", ".json"))
    if not campaign_file.exists():
        return 0

    try:
        Campaign = _load_helix()
        camp = Campaign.load(campaign_file)
        with inbox.open() as fh:
            rows = list(csv.DictReader(fh))
        results = [{k: (int(v) if k == "candidate_id" else float(v)) for k, v in row.items() if v != ""}
                   for row in rows]
        n = camp.ingest(results)
        camp.save(campaign_file)
        status = camp.status()
        nxt = camp.propose()
        camp.save(campaign_file)
        msg = (f"🧬 Helix: ingested {n} assay result(s) into '{status['title']}'. "
               f"Best {status.get('objective','')} so far: {status.get('best','n/a')}. "
               f"Budget left: {status['budget_remaining']}. "
               f"Next batch of {len(nxt)} experiment(s) is ready — ask me to show it.")
        # additionalContext is surfaced to the model; stderr is shown to the user.
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": msg}}))
    except Exception as exc:
        print(f"Helix hook: skipped ({exc})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
