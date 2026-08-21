#!/usr/bin/env python3
"""Generate one tailored resume per campaign role from ONE verified fact base.

Seven hand-written "custom resumes" drift into seven different accounts of the same
work. So the facts live once in data/resume_facts.yml and each role in
data/campaign_roles.yml selects and orders them (`lead` / `also`) plus supplies its own
title, thesis, and — required — an `honest_edge`.

The honest_edge is not modesty theatre: every role here has a real weak spot, and naming
it is what makes the rest of the document trustworthy. A role without one does not build.

Usage:
    python3 scripts/build_resume.py                 # markdown + HTML for every role
    python3 scripts/build_resume.py --pdf           # also render PDFs via headless Chrome
    python3 scripts/build_resume.py --slug gdm-humanoids
"""
from __future__ import annotations

import argparse
import html as html_mod
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "jd-fit" / "resumes"
CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def md_inline(s: str) -> str:
    """Minimal inline markdown → HTML (bold + links), then escape the rest."""
    s = html_mod.escape(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def build_markdown(facts: dict, role: dict) -> str:
    r = role["resume"]
    proof = {p["id"]: p for p in facts["proof"]}
    missing = [i for i in (r.get("lead", []) + r.get("also", [])) if i not in proof]
    if missing:
        raise KeyError(f"{role['slug']}: unknown proof id(s) {missing}")
    if not r.get("honest_edge"):
        raise ValueError(f"{role['slug']}: honest_edge is required")

    i = facts["identity"]
    L = [f"# {i['name']}", "",
         f"**{r['title']}**", "",
         f"{i['email']} · {i['github']} · {i['linkedin']} · [live portfolio]({i['portfolio']})",
         "", "## SUMMARY", "", r["thesis"].strip(), "",
         f"## WHY {role['company'].upper()} — {role['title'].upper()}", ""]

    for pid in r.get("lead", []):
        p = proof[pid]
        L.append(f"- **{p['headline']}:** {p['body'].strip()} "
                 f"({p['evidence']})")
    L += ["", "## ALSO SHIPPED", ""]
    for pid in r.get("also", []):
        p = proof[pid]
        L.append(f"- **{p['headline']}** — {p['evidence']}")

    # A bullet may be a plain string (always shown) or {text, only_for: [tag]}, shown only
    # when the role declares a matching `experience_focus`. Same fact base, no per-role prose.
    focus = set(r.get("experience_focus") or [])
    L += ["", "## EXPERIENCE", ""]
    for e in facts["experience"]:
        L.append(f"**{e['role']} — {e['org']}** · {e['dates']}")
        for b in e["bullets"]:
            if isinstance(b, dict):
                if not focus.intersection(b.get("only_for") or []):
                    continue
                b = b["text"]
            L.append(f"- {b}")
        L.append("")

    L += ["## PUBLICATIONS", ""]
    for pid in ("scwm", "physical_ai_paper"):
        p = proof[pid]
        L.append(f"- **{p['headline']}** — {p['body'].strip()}")

    L += ["", "## TECHNICAL SKILLS", ""]
    groups = r.get("skill_groups") or facts.get("default_skill_groups") or list(facts["skills"])
    unknown = [g for g in groups if g not in facts["skills"]]
    if unknown:
        raise KeyError(f"{role['slug']}: unknown skill group(s) {unknown}")
    labels = facts.get("skill_labels") or {}
    for k in groups:
        L.append(f"**{labels.get(k, k.title())}:** {facts['skills'][k]}")
        L.append("")

    L += ["## EDUCATION", "", facts["education"].strip(), "",
          "## THE EDGE I'D BE LEARNING, NOT TEACHING", "",
          r["honest_edge"].strip(), ""]
    return "\n".join(L)


def build_html(md: str) -> str:
    """Print-ready HTML. ASCII-safe fonts only — no CJK here, but keep the stack
    conservative so headless-Chrome PDF never silently drops a glyph."""
    body: list[str] = []
    in_list = False
    for line in md.splitlines():
        if line.startswith("# "):
            if in_list: body.append("</ul>"); in_list = False
            body.append(f"<h1>{md_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list: body.append("</ul>"); in_list = False
            body.append(f"<h2>{md_inline(line[3:])}</h2>")
        elif line.startswith("- "):
            if not in_list: body.append("<ul>"); in_list = True
            body.append(f"<li>{md_inline(line[2:])}</li>")
        elif line.strip():
            if in_list: body.append("</ul>"); in_list = False
            body.append(f"<p>{md_inline(line)}</p>")
    if in_list:
        body.append("</ul>")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>
  @page {{ size: Letter; margin: 0.5in; }}
  body {{ font: 10.5pt/1.42 "Helvetica Neue", Helvetica, Arial, sans-serif;
          color: #141413; max-width: 7.5in; margin: 0 auto; }}
  h1 {{ font-size: 19pt; margin: 0 0 2pt; letter-spacing: -0.2pt; }}
  h2 {{ font-size: 10pt; text-transform: uppercase; letter-spacing: 0.9pt;
        border-bottom: 1.2pt solid #d97757; padding-bottom: 2pt;
        margin: 13pt 0 6pt; color: #141413; }}
  p {{ margin: 0 0 5pt; }}
  ul {{ margin: 0 0 7pt; padding-left: 15pt; }}
  li {{ margin-bottom: 4pt; }}
  a {{ color: #6a9bcc; text-decoration: none; }}
  strong {{ color: #141413; }}
</style></head><body>
{chr(10).join(body)}
</body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default=None)
    ap.add_argument("--pdf", action="store_true")
    args = ap.parse_args()

    facts = yaml.safe_load((ROOT / "data" / "resume_facts.yml").read_text())
    roles = yaml.safe_load((ROOT / "data" / "campaign_roles.yml").read_text())
    OUT.mkdir(parents=True, exist_ok=True)

    n = 0
    for role in roles:
        if args.slug and role["slug"] != args.slug:
            continue
        if "resume" not in role:
            print(f"  ○ {role['slug']}: no resume block — skipped")
            continue
        md = build_markdown(facts, role)
        (OUT / f"{role['slug']}.md").write_text(md)
        (OUT / f"{role['slug']}.html").write_text(build_html(md))
        words = len(md.split())
        print(f"  ✓ {role['slug']:<38} {words:4d} words  ({role['company']})")
        if args.pdf:
            pdf = OUT / f"{role['slug']}.pdf"
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", (OUT / f'{role["slug"]}.html').as_uri()],
                           capture_output=True, timeout=120)
            size = pdf.stat().st_size // 1024 if pdf.exists() else 0
            print(f"      → {pdf.name} ({size} KB)")
        n += 1
    print(f"\n{n} tailored resume(s) generated from one verified fact base.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
