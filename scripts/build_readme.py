#!/usr/bin/env python3
"""Render README.md from data/*.yml — the single source of truth.

The README is a build artifact. Never hand-edit it; edit data/*.yml and run
`make build` (CI drift-gates the two against each other). See CONTRIBUTING.md.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
README = ROOT / "README.md"

BADGE = "https://img.shields.io/github"


def load(name: str):
    path = DATA / f"{name}.yml"
    if not path.exists():
        return []
    return yaml.safe_load(path.read_text()) or []


def esc(text: str) -> str:
    return " ".join(str(text).split())


# ── per-source line formatters ───────────────────────────────────────────────
def fmt_repo(e: dict) -> str:
    star = f" `★ {e['stars']:,}`" if e.get("stars") else ""
    slm = " 🤏" if e.get("slm") else ""
    return f"- **[{esc(e['name'])}]({e['url']})**{slm}{star} — {esc(e.get('blurb',''))}"


def fmt_course(e: dict) -> str:
    who = " · ".join(x for x in (e.get("org"), e.get("instructor")) if x)
    yr = f" ({e['year']})" if e.get("year") else ""
    free = " · _free_" if e.get("free") else ""
    meta = f" — {who}{yr}{free}" if who or yr else free
    return f"- **[{esc(e['title'])}]({e['url']})**{meta} — {esc(e.get('blurb',''))}"


def fmt_paper(e: dict) -> str:
    bits = [b for b in (e.get("authors"), e.get("org")) if b]
    yr = f", {e['year']}" if e.get("year") else ""
    venue = f" · {e['venue']}" if e.get("venue") else ""
    meta = f" ({', '.join(bits)}{yr})" if bits or yr else ""
    return f"- **[{esc(e['title'])}]({e['url']})**{meta}{venue} — {esc(e.get('blurb',''))}"


def fmt_job(e: dict) -> str:
    return f"- **[{esc(e['name'])}]({e['url']})** — {esc(e.get('focus',''))}"


FMT = {"repos": fmt_repo, "courses": fmt_course, "papers": fmt_paper, "jobs": fmt_job}


def render_section(sec: dict, entries: list) -> str:
    key = sec["key"]
    fmt = FMT[sec["source"]]
    out = [f'<h2 id="{sec["id"]}">{sec["icon"]} {sec["title"]}</h2>', ""]

    # Merge groups that share a title (e.g. distillation + compression).
    ordered_titles: list[str] = []
    title_keys: dict[str, list[str]] = {}
    for g in sec.get("groups", []):
        if g["title"] not in title_keys:
            title_keys[g["title"]] = []
            ordered_titles.append(g["title"])
        title_keys[g["title"]].append(g["key"])

    used = set()
    for title in ordered_titles:
        keys = title_keys[title]
        rows = [e for e in entries if e.get(key) in keys]
        for e in rows:
            used.add(id(e))
        if not rows:
            continue
        out.append(f"### {title}")
        out += [fmt(e) for e in rows]
        out += ["", "<sub>[↑ back to top](#-table-of-contents)</sub>", ""]

    # Never silently drop an entry whose category doesn't match a group.
    leftover = [e for e in entries if id(e) not in used]
    if leftover:
        out.append("### More")
        out += [fmt(e) for e in leftover]
        out += ["", "<sub>[↑ back to top](#-table-of-contents)</sub>", ""]
    return "\n".join(out)


def build() -> str:
    meta = load("meta")
    data = {name: load(name) for name in ("repos", "courses", "papers", "jobs")}

    # Merge live stats from the generated stars map (written by scripts/sync.py).
    stars = {}
    stars_path = DATA / "_stars.yml"
    if stars_path.exists():
        stars = yaml.safe_load(stars_path.read_text()) or {}
    for e in data["repos"]:
        stat = stars.get(e.get("repo"))
        if stat and stat.get("stars") is not None:
            e["stars"] = stat["stars"]

    owner, repo = meta["repo_owner"], meta["repo_name"]
    slug = f"{owner}/{repo}"
    L: list[str] = []

    # ── header ──────────────────────────────────────────────────────────────
    L += [
        f"# {meta['title']}",
        "",
        "<div align=\"center\">",
        "",
        "[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)",
        "[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)",
        f"[![Stars]({BADGE}/stars/{slug}?style=flat-square)](https://github.com/{slug}/stargazers)",
        f"[![Contributors]({BADGE}/contributors/{slug}?style=flat-square)](https://github.com/{slug}/graphs/contributors)",
        f"[![Last Updated]({BADGE}/last-commit/{slug}?style=flat-square&label=updated)](https://github.com/{slug}/commits/main)",
        f"[![Weekly Sync]({BADGE}/actions/workflow/status/{slug}/sync.yml?style=flat-square&label=weekly%20sync)](https://github.com/{slug}/actions/workflows/sync.yml)",
        f"[![License]({BADGE}/license/{slug}?style=flat-square)](LICENSE)",
        "",
        meta["tagline"],
        "",
        meta["subtitle"],
        "",
        " • ".join(f"[{n['label']}](#{n['anchor']})" for n in meta["nav"]),
        "",
        "</div>",
        "",
        "---",
        "",
        "> **⚡ Why FM-os and not the other lists?**",
        "",
    ]
    for i, w in enumerate(meta["why_different"], 1):
        L.append(f"> {i}. {esc(w)}")
    L += ["", "---", ""]

    # ── start here ────────────────────────────────────────────────────────────
    L += [
        '<h2 id="start-here">🚀 Start Here</h2>',
        "",
        "New to foundation-model ops? Read this in order:",
        "",
        "1. **Understand the lifecycle** → *pre-training → post-training → fine-tuning → RL → serving*. Every section below follows it.",
        "2. **Pick a small model you can actually run** → jump to [Small & Efficient Models](#open-source-repos).",
        "3. **Learn from scratch** → the [Courses](#courses) section starts with from-scratch, one-GPU-friendly material.",
        "4. **Go deep** → [Papers](#papers) are filed by lifecycle stage, SLM first.",
        "5. **Get hired** → [Jobs & Careers](#jobs--careers) points at the labs and boards that hire for this work.",
        "",
        "🤏 = directly Small-Language-Model relevant.",
        "",
        "---",
        "",
    ]

    # ── table of contents ───────────────────────────────────────────────────
    L += ['<h2 id="-table-of-contents">📚 Table of Contents</h2>', ""]
    L.append("- [🚀 Start Here](#start-here)")
    counts = {}
    for sec in meta["sections"]:
        entries = data[sec["source"]]
        counts[sec["id"]] = len(entries)
        L.append(f"- [{sec['icon']} {sec['title']}](#{sec['id']}) `{len(entries)}`")
    L += [
        "- [🗺️ Learning Roadmap](#learning-roadmap)",
        "- [🤝 Contribute](#contribute)",
        "",
        "---",
        "",
    ]

    # ── generated sections ────────────────────────────────────────────────────
    for sec in meta["sections"]:
        L.append(render_section(sec, data[sec["source"]]))
        L += ["---", ""]

    # ── roadmap ────────────────────────────────────────────────────────────────
    L += [
        '<h2 id="learning-roadmap">🗺️ Learning Roadmap</h2>',
        "",
        "**Beginner → practitioner (SLM track):**",
        "",
        "1. Watch a from-scratch course and train a tiny model (see Courses → Foundations).",
        "2. Fine-tune a small open model with LoRA/QLoRA on your own data (Repos → Fine-tuning).",
        "3. Align it with DPO, then try a GRPO-style RL loop (Repos → Post-training & RL).",
        "4. Evaluate honestly (Repos → Evaluation) and serve it on-device (Repos → Serving).",
        "5. Read the SLM surveys + the model tech reports to understand the design space (Papers).",
        "",
        "---",
        "",
    ]

    # ── contribute ─────────────────────────────────────────────────────────────
    L += [
        '<h2 id="contribute">🤝 Contribute</h2>',
        "",
        "This list is **data-driven** — every entry is a few lines of YAML in `data/`.",
        "Adding a resource is a two-line PR; you never touch the README (it's generated).",
        "",
        "```bash",
        "# 1. add your entry to the right file, e.g. data/repos.yml",
        "# 2. regenerate + check locally",
        "make check",
        "# 3. open a PR",
        "```",
        "",
        "See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the entry schema and the one rule",
        "(every entry needs a working `url`). A weekly Action re-verifies links and refreshes",
        "repo stats automatically.",
        "",
        "---",
        "",
        "<div align=\"center\">",
        "",
        "### ⭐ Star History",
        "",
        f'<a href="https://star-history.com/#{slug}&Date">',
        f'  <img src="https://api.star-history.com/svg?repos={slug}&type=Date" alt="Star history chart" width="600">',
        "</a>",
        "",
        "### 🙌 Contributors",
        "",
        f'<a href="https://github.com/{slug}/graphs/contributors">',
        f'  <img src="https://contrib.rocks/image?repo={slug}" alt="Contributors">',
        "</a>",
        "",
        esc(meta["footer_note"]),
        "",
        "<sub>README generated from <code>data/*.yml</code> by <code>scripts/build_readme.py</code> — do not edit by hand.</sub>",
        "",
        "</div>",
        "",
    ]
    return "\n".join(L)


def main() -> int:
    text = build()
    if "--check" in sys.argv:
        current = README.read_text() if README.exists() else ""
        if current != text:
            print("README.md is out of date. Run `make build` and commit.", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0
    README.write_text(text)
    print(f"Wrote {README.relative_to(ROOT)} ({len(text.splitlines())} lines).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
