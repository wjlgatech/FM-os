#!/usr/bin/env python3
"""Generate one interview dossier per campaign role, from the SAME fact base as the resumes.

Stage 5 of docs/PLAYBOOK-jobapp-flywheel.md wants, per role: the pasted scorecard, the
honest edges, and five stories. Hand-writing nine of those guarantees nine slightly
different accounts of the same work — the exact drift the resume builder exists to
prevent — so this reuses `data/resume_facts.yml` and `data/campaign_roles.yml` and
regenerates the scorecard by RUNNING jdfit rather than pasting a remembered number.

Each story is rendered in the Situation / What I did / Result / What it cost shape,
because the last field is the one interviewers actually probe and the one a generated
story usually omits.

Usage:
    python3 scripts/build_dossier.py                      # all roles
    python3 scripts/build_dossier.py --slug gdm-humanoids
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "jd-fit"
JD_DIR = Path("/tmp/jds")


def scorecard(job_id: str) -> tuple[str, int, list[str]]:
    """Run jdfit live. Returns (markdown, score, open_caps)."""
    jd = JD_DIR / f"{job_id}.txt"
    if not jd.exists():
        return ("_JD text not present locally — regenerate with the campaign fetcher "
                "before quoting a score._", -1, [])
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "jdfit.py"), "--jd", str(jd)],
                         capture_output=True, text=True, cwd=ROOT).stdout
    m = re.search(r"\*\*(\d+)/100\*\*", out)
    score = int(m.group(1)) if m else -1
    open_caps = [l.strip("- ").split("**")[1] for l in out.splitlines()
                 if l.startswith("- **") and "**" in l[4:]]
    return out.strip(), score, open_caps


def stories(facts: dict, role: dict) -> list[dict]:
    """Five stories, drawn from the proof blocks this role actually leads with."""
    proof = {p["id"]: p for p in facts["proof"]}
    ids = (role["resume"].get("lead", []) + role["resume"].get("also", []))[:5]
    return [proof[i] for i in ids if i in proof]


def build(facts: dict, role: dict) -> str:
    r = role["resume"]
    card, score, open_caps = scorecard(role["job_id"])
    apply_url = role.get("apply_url")
    L = [f"# {role['title']} — {role['company']}", "",
         f"**Fit:** {score}/100 · **Location:** {role.get('location','(per posting)')}",
         f"**Apply:** {apply_url or '⚠ UNRESOLVED — do not guess a job id; resolve it first'}",
         f"**Resume:** [`resumes/{role['slug']}.pdf`](resumes/{role['slug']}.pdf)", ""]

    if role.get("comp"):
        L += [f"**Comp:** {role['comp']}", ""]
    if role.get("search_keyword_mismatch"):
        L += ["> **Keyword mismatch, recorded at intake:** "
              + " ".join(role["search_keyword_mismatch"].split()), ""]
    if role.get("note"):
        L += ["> **Note:** " + " ".join(role["note"].split()), ""]

    L += ["## The angle", "", " ".join(r["thesis"].split()), "",
          "## Scorecard", "", "<!-- BEGIN jdfit -->", card, "<!-- END jdfit -->", ""]

    L += ["## The honest edge — say it before they find it", "",
          " ".join(r["honest_edge"].split()), ""]
    if open_caps:
        L += ["Still open on the capability map (name these rather than hoping they do not come up):", ""]
        L += [f"- {c}" for c in open_caps] + [""]

    L += ["## Five stories", "",
          "_Situation → what I did → result → **what it cost**. The last line is the one "
          "that gets probed; a story without it sounds rehearsed._", ""]
    for i, s in enumerate(stories(facts, role), 1):
        L += [f"### {i}. {s['headline']}", "", " ".join(s["body"].split()), "",
              f"- **Evidence:** {s['evidence']}", ""]

    L += ["## Outreach — DRAFTED, NEVER SENT", "",
          "| Who | Why them | The give | The ask |", "|---|---|---|---|",
          "| _(fill from the team's published work)_ | a specific paper/repo of theirs this "
          "role touches | the artifact above that is closest to their problem | one "
          "20-minute question, not \"can I pick your brain\" |", "",
          "## Submission gate", "",
          "Not submitted until ALL hold:", "",
          "1. This dossier's scorecard regenerated (never a remembered number).",
          "2. The resume is the one tailored to THIS role, not a generic copy.",
          "3. Every resume claim traces to a shipped artifact.",
          "4. The honest edge above is stated in the application, not hidden.",
          f"5. The apply URL is verified{' ✓' if apply_url else ' — ⚠ NOT YET'}.", "",
          "## Outcome log", "", "| Date | Event | Artifact that carried it |", "|---|---|---|",
          "| — | not yet submitted | — |", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default=None)
    args = ap.parse_args()
    facts = yaml.safe_load((ROOT / "data" / "resume_facts.yml").read_text())
    roles = yaml.safe_load((ROOT / "data" / "campaign_roles.yml").read_text())
    n = 0
    for role in roles:
        if args.slug and role["slug"] != args.slug:
            continue
        if "resume" not in role:
            continue
        md = build(facts, role)
        (OUT / f"{role['slug']}.md").write_text(md)
        n_stories = md.count("\n### ")
        flag = "" if role.get("apply_url") else "  ⚠ apply_url unresolved"
        print(f"  ✓ {role['slug']:<38} {n_stories} stories{flag}")
        n += 1
    print(f"\n{n} dossier(s) generated from one verified fact base.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
