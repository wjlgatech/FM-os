#!/usr/bin/env python3
"""FM-os JD-fit — score how well FM-os equips someone for a job description.

Scans a JD for each capability in data/jd_taxonomy.yml, then for the ones the JD
requires, checks FM-os coverage:
  knowledge = FM-os curates a repo (by category) or course/paper (by topic)
  tooling   = an FM-os registry skill carries the capability's tag
Coverage: covered (knowledge + tooling) · partial (knowledge only) · gap (neither).
No evidence ⇒ gap — never a fake pass. This is the compounding artifact: every new
JD reuses the taxonomy + data, and the gaps it prints are the next things to build.

  jdfit.py --jd path/to/jd.txt [--json] [--gate N]
"""
from __future__ import annotations

import argparse
import json
import sys

from fmos import load


class JDFit:
    """Match a JD against the taxonomy and FM-os's curated knowledge + tooling."""

    def __init__(self, jd_text: str) -> None:
        self.jd = jd_text.lower()
        self.taxonomy = load("jd_taxonomy")
        self.repos = load("repos")
        self.courses = load("courses")
        self.papers = load("papers")
        self.registry = load("registry")
        self.certs = load("_certifications") if load("_certifications") else {}

    def _knowledge(self, cap: dict) -> list[str]:
        """Example FM-os resources (≤3) that teach this capability."""
        cats, topics = set(cap.get("repo_categories") or []), set(cap.get("topics") or [])
        hits = [r["name"] for r in self.repos if r.get("category") in cats]
        hits += [c["title"] for c in self.courses if c.get("topic") in topics]
        hits += [p["title"] for p in self.papers if p.get("topic") in topics]
        return hits[:3]

    def _tooling(self, cap: dict) -> list[str]:
        """Registry skills whose tags carry this capability (certified marked)."""
        tag = cap.get("skill_tag")
        if not tag:
            return []
        out = []
        for e in self.registry:
            if tag in (e.get("tags") or []):
                c = self.certs.get(e["name"], {})
                mark = f" ({c['tier']} {c['score']})" if c.get("tier") in ("certified", "provisional") else ""
                out.append(e["name"] + mark)
        return out

    def analyze(self) -> dict:
        """Return per-capability coverage for every capability the JD requires."""
        results = []
        for cap in self.taxonomy:
            if not any(k in self.jd for k in cap["keywords"]):
                continue  # not required by this JD
            knowledge = self._knowledge(cap)
            tooling = self._tooling(cap)
            wants_tool = cap.get("kind") != "knowledge"
            if knowledge and (tooling or not wants_tool):
                coverage = "covered"
            elif knowledge:
                coverage = "partial"
            else:
                coverage = "gap"
            results.append({
                "id": cap["id"], "label": cap["label"], "coverage": coverage,
                "wants_tool": wants_tool, "knowledge": knowledge, "tooling": tooling,
            })
        n = len(results)
        pts = sum(1.0 if r["coverage"] == "covered" else 0.5 if r["coverage"] == "partial" else 0 for r in results)
        return {"score": round(100 * pts / n) if n else 0, "required": n, "capabilities": results}


ICON = {"covered": "✅", "partial": "🟡", "gap": "❌"}


def to_markdown(result: dict) -> str:
    """Render a JD-fit result as a readiness report."""
    lines = [f"# FM-os JD-fit report — **{result['score']}/100** ({result['required']} capabilities required)", ""]
    lines += ["| Capability | Coverage | FM-os knowledge | FM-os tooling |", "|---|:--:|---|---|"]
    for r in result["capabilities"]:
        know = ", ".join(r["knowledge"]) or "—"
        tool = ", ".join(r["tooling"]) or ("—" if r["wants_tool"] else "n/a")
        lines.append(f"| {r['label']} | {ICON[r['coverage']]} {r['coverage']} | {know} | {tool} |")
    gaps = [r for r in result["capabilities"] if r["coverage"] != "covered"]
    if gaps:
        lines += ["", "## Gaps to close (the next things to build)"]
        for r in gaps:
            need = "add curated resources" if not r["knowledge"] else "build/certify a skill"
            lines.append(f"- **{r['label']}** ({r['coverage']}) → {need}")
    return "\n".join(lines)


def main() -> int:
    """CLI: score a --jd file against FM-os; --gate N fails under a fit threshold."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--jd", required=True, help="path to a job-description text file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--gate", type=int)
    args = ap.parse_args()

    result = JDFit(open(args.jd, encoding="utf-8", errors="ignore").read()).analyze()
    print(json.dumps(result, indent=2) if args.json else to_markdown(result))
    if args.gate is not None and result["score"] < args.gate:
        print(f"\n::gate:: FAILED — fit {result['score']} < {args.gate}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
