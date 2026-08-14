#!/usr/bin/env python3
"""Turn N job descriptions into a DEPENDENCY GRAPH of campaign work.

WHY: applying to N roles one-at-a-time redoes shared work N times; applying to all
of them with one generic package is the false-100 trap at campaign scale. The middle
path is to compute what is actually shared.

The graph has two node kinds:
  ROLE       one distinct posting (after dedupe)
  CAPABILITY one entry in data/jd_taxonomy.yml that ≥1 role's JD turns on

An edge ROLE→CAPABILITY is weighted by that capability's coverage for us today
(covered / partial / gap). Then:

  SHARED CORE   caps required by ≥ SHARED_MIN roles. Closing one of these pays off
                across the whole campaign — build FIRST.
  ROLE-SPECIFIC caps required by exactly one role. These are the only legitimate
                reason to build something per-role, and they are also what makes a
                resume genuinely custom rather than reworded.
  LEVERAGE      per-cap: (#roles needing it) × (1 if gap, 0.5 if partial, 0 if covered).
                Sort descending = the honest build order.

Usage:
    python3 scripts/campaign_graph.py --jds /tmp/jds --roles data/campaign_roles.yml
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SHARED_MIN = 3
WEIGHT = {"gap": 1.0, "partial": 0.5, "covered": 0.0}


def scorecard(jd_path: Path) -> tuple[int, dict[str, str]]:
    """Run jdfit and parse (score, {capability_label: coverage})."""
    out = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "jdfit.py"), "--jd", str(jd_path)],
        capture_output=True, text=True, cwd=ROOT,
    ).stdout
    m = re.search(r"\*\*(\d+)/100\*\*", out)
    score = int(m.group(1)) if m else -1
    caps: dict[str, str] = {}
    for line in out.splitlines():
        if not line.startswith("| ") or "Capability" in line or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        cov = ("covered" if "covered" in cells[1] else
               "partial" if "partial" in cells[1] else
               "gap" if "gap" in cells[1] else None)
        if cov:
            caps[cells[0]] = cov
    return score, caps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jds", default="/tmp/jds", help="dir of <jobid>.txt JD files")
    ap.add_argument("--roles", default="data/campaign_roles.yml")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    roles = yaml.safe_load((ROOT / args.roles).read_text())
    jd_dir = Path(args.jds)

    graph = {}
    for r in roles:
        jd = jd_dir / f"{r['job_id']}.txt"
        if not jd.exists():
            print(f"⚠ missing JD text for {r['job_id']} — skipped (never invented)")
            continue
        score, caps = scorecard(jd)
        graph[r["slug"]] = {"role": r, "score": score, "caps": caps}

    # capability → roles that need it
    cap_roles: dict[str, list[str]] = {}
    cap_cov: dict[str, str] = {}
    for slug, d in graph.items():
        for cap, cov in d["caps"].items():
            cap_roles.setdefault(cap, []).append(slug)
            # worst coverage seen wins — a cap that is a gap anywhere is not "done"
            prev = cap_cov.get(cap)
            if prev is None or WEIGHT[cov] > WEIGHT[prev]:
                cap_cov[cap] = cov

    if args.json:
        print(json.dumps({"roles": {k: {"score": v["score"], "caps": v["caps"]}
                                    for k, v in graph.items()},
                          "cap_roles": cap_roles, "cap_cov": cap_cov}, indent=1))
        return 0

    print(f"\n=== {len(graph)} distinct roles · {len(cap_roles)} capabilities turned on ===\n")
    for slug, d in sorted(graph.items(), key=lambda kv: -kv[1]["score"]):
        r = d["role"]
        n_gap = sum(1 for c in d["caps"].values() if c != "covered")
        print(f"  {d['score']:3d}/100  {len(d['caps']):2d} caps  {n_gap} open  "
              f"{slug:<28} {r['company']} · {r['location']}")

    print(f"\n=== SHARED CORE (needed by ≥{SHARED_MIN} roles — build once, pays N times) ===\n")
    shared = sorted(((c, rs) for c, rs in cap_roles.items() if len(rs) >= SHARED_MIN),
                    key=lambda kv: (-len(kv[1]), kv[0]))
    for cap, rs in shared:
        mark = {"covered": "✅", "partial": "🟡", "gap": "❌"}[cap_cov[cap]]
        print(f"  {mark} {len(rs)} roles  {cap[:74]}")

    print("\n=== ROLE-SPECIFIC (exactly one role — the real custom-resume material) ===\n")
    for cap, rs in sorted(cap_roles.items(), key=lambda kv: kv[0]):
        if len(rs) == 1:
            mark = {"covered": "✅", "partial": "🟡", "gap": "❌"}[cap_cov[cap]]
            print(f"  {mark} {rs[0]:<28} {cap[:60]}")

    print("\n=== BUILD ORDER by leverage = roles × openness (0 ⇒ nothing to build) ===\n")
    lev = [(len(rs) * WEIGHT[cap_cov[c]], c, len(rs), cap_cov[c])
           for c, rs in cap_roles.items()]
    for score_, cap, n, cov in sorted(lev, reverse=True):
        if score_ <= 0:
            continue
        print(f"  leverage {score_:4.1f}  ({n} roles × {cov:<7})  {cap[:60]}")
    if not any(s > 0 for s, *_ in lev):
        print("  (nothing open — every capability these roles need is already covered)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
