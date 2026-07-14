#!/usr/bin/env python3
"""Render README.md from data/*.yml — the single source of truth.

The README is a build artifact. Never hand-edit it; edit data/*.yml and run
`make build` (CI drift-gates the two against each other). See CONTRIBUTING.md.
"""
from __future__ import annotations

import re
import sys

from fmos import DATA, esc, load, repos_with_stars

README = DATA.parent / "README.md"
BADGE = "https://img.shields.io/github"


# ── per-source line formatters ───────────────────────────────────────────────
def fmt_repo(e: dict) -> str:
    """One repo → a Markdown bullet with the SLM marker + live star count."""
    star = f" `★ {e['stars']:,}`" if e.get("stars") else ""
    slm = " 🤏" if e.get("slm") else ""
    return f"- **[{esc(e['name'])}]({e['url']})**{slm}{star} — {esc(e.get('blurb',''))}"


def fmt_course(e: dict) -> str:
    """One course → a Markdown bullet with org/instructor/year and a free tag."""
    who = " · ".join(x for x in (e.get("org"), e.get("instructor")) if x)
    yr = f" ({e['year']})" if e.get("year") else ""
    free = " · _free_" if e.get("free") else ""
    meta = f" — {who}{yr}{free}" if who or yr else free
    return f"- **[{esc(e['title'])}]({e['url']})**{meta} — {esc(e.get('blurb',''))}"


def fmt_paper(e: dict) -> str:
    """One paper → a Markdown bullet with authors/org/year and venue."""
    bits = [b for b in (e.get("authors"), e.get("org")) if b]
    yr = f", {e['year']}" if e.get("year") else ""
    venue = f" · {e['venue']}" if e.get("venue") else ""
    meta = f" ({', '.join(bits)}{yr})" if bits or yr else ""
    return f"- **[{esc(e['title'])}]({e['url']})**{meta}{venue} — {esc(e.get('blurb',''))}"


def fmt_job(e: dict) -> str:
    """One job source → a Markdown bullet with its focus."""
    return f"- **[{esc(e['name'])}]({e['url']})** — {esc(e.get('focus',''))}"


FMT = {"repos": fmt_repo, "courses": fmt_course, "papers": fmt_paper, "jobs": fmt_job}


def render_section(sec: dict, entries: list) -> str:
    """Render one config-driven section, grouping entries by sub-heading."""
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


def render_model_table(models: list) -> str:
    """Render the SLM model zoo as a comparison table, smallest params first."""
    out = [
        '<h2 id="model-zoo">🤖 SLM Model Zoo</h2>',
        "",
        "The small open models worth knowing, smallest first. `⚠️` = non-commercial / restricted license — check before shipping.",
        "",
        "| Model | Org | Params | License | Context | On-device |",
        "|---|---|--:|---|--:|:--:|",
    ]
    def pb(p: str) -> float:
        m = re.search(r"([\d.]+)\s*B", p or "")
        return float(m.group(1)) if m else 999.0
    for m in sorted(models, key=lambda e: pb(e.get("params", ""))):
        lic = esc(m.get("license", "—"))
        if m.get("nc"):
            lic = "⚠️ " + lic
        od = "✅" if m.get("ondevice") else "—"
        out.append(
            f"| [{esc(m['name'])}]({m['url']}) | {esc(m.get('org','—'))} | {esc(m.get('params','—'))} "
            f"| {lic} | {esc(m.get('context','—'))} | {od} |"
        )
    out += ["", "<sub>[↑ back to top](#-table-of-contents)</sub>", ""]
    return "\n".join(out)


def render_certified(registry: list, certs: dict, owner: str, repo: str) -> str:
    """Render the FM-os Certified table: scored tools first, then submitted ones."""
    slug = f"{owner}/{repo}"
    icon = {"certified": "✅", "provisional": "🟡", "rejected": "❌", "not-applicable": "⚪"}
    out = [
        '<h2 id="fm-os-certified">🏅 FM-os Certified</h2>',
        "",
        "Trust, not just a list. Every tool below is scored by an **automated, "
        "evidence-based rubric** ([`data/certify.yml`](data/certify.yml)) — provenance, a "
        "security scan, docs, SLM/FM-ops relevance, and more. Security is a blocking gate; "
        "no evidence ⇒ no pass. Authors self-certify in CI — see [docs/CERTIFY.md](docs/CERTIFY.md).",
        "",
        "| Tool | Kind | Score | Status |",
        "|---|---|--:|:--|",
    ]
    scored = [e for e in registry if e["name"] in certs]
    for e in sorted(scored, key=lambda e: -certs[e["name"]]["score"]):
        c = certs[e["name"]]
        name = f"[{esc(e['name'])}]({e['source']})" if e.get("source") else esc(e["name"])
        out.append(f"| {name} | {esc(c['kind'])} | {c['score']}/100 | {icon.get(c['tier'],'')} {esc(c['tier'])} |")
    submitted = [e for e in registry if e["name"] not in certs]
    for e in submitted:
        name = f"[{esc(e['name'])}]({e['source']})" if e.get("source") else esc(e["name"])
        out.append(f"| {name} | {esc(e.get('kind','—'))} | — | ⏳ submitted |")
    out += [
        "",
        "> **Earn the badge for your tool:** add the FM-os Certify action to your CI "
        "(see [docs/CERTIFY.md](docs/CERTIFY.md)) and embed:",
        "> ```md",
        f"> ![FM-os Certified](https://img.shields.io/endpoint?url=https://{owner}.github.io/{repo}/badges/YOUR-TOOL.json)",
        "> ```",
        "",
        "<sub>[↑ back to top](#-table-of-contents)</sub>",
        "",
    ]
    return "\n".join(out)


def render_header(meta: dict, slug: str) -> list[str]:
    """Title, badge row, tagline, nav, and the 'why different' hook."""
    out = [
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
    out += [f"> {i}. {esc(w)}" for i, w in enumerate(meta["why_different"], 1)]
    return out + ["", "---", ""]


def render_start_here() -> list[str]:
    """The ordered onboarding path for a newcomer."""
    return [
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


def render_toc(meta: dict, data: dict, models: list, registry: list) -> list[str]:
    """Table of contents with per-section entry counts."""
    out = ['<h2 id="-table-of-contents">📚 Table of Contents</h2>', "", "- [🚀 Start Here](#start-here)"]
    if models:
        out.append(f"- [🤖 SLM Model Zoo](#model-zoo) `{len(models)}`")
    if registry:
        out.append(f"- [🏅 FM-os Certified](#fm-os-certified) `{len(registry)}`")
    for sec in meta["sections"]:
        out.append(f"- [{sec['icon']} {sec['title']}](#{sec['id']}) `{len(data[sec['source']])}`")
    return out + ["- [🗺️ Learning Roadmap](#learning-roadmap)", "- [🤝 Contribute](#contribute)", "", "---", ""]


def render_roadmap() -> list[str]:
    """The beginner→practitioner SLM learning track."""
    return [
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


def render_footer(meta: dict, slug: str) -> list[str]:
    """Contribute section, star-history chart, and contributor wall."""
    return [
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


def build() -> str:
    """Assemble the full README from data/*.yml. Sections are emitted in order."""
    meta = load("meta")
    data = {"repos": repos_with_stars()}
    data.update({name: load(name) for name in ("courses", "papers", "jobs")})
    models, registry = load("models"), load("registry")
    certs = load("_certifications") if (DATA / "_certifications.yml").exists() else {}
    owner, repo = meta["repo_owner"], meta["repo_name"]
    slug = f"{owner}/{repo}"

    parts: list[str] = render_header(meta, slug) + render_start_here() + render_toc(meta, data, models, registry)
    if models:
        parts += [render_model_table(models), "---", ""]
    if registry:
        parts += [render_certified(registry, certs, owner, repo), "---", ""]
    for sec in meta["sections"]:
        parts += [render_section(sec, data[sec["source"]]), "---", ""]
    parts += render_roadmap() + render_footer(meta, slug)
    return "\n".join(parts)


def main() -> int:
    """Write README.md, or with --check verify it matches (drift gate)."""
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
