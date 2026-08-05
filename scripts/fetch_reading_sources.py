#!/usr/bin/env python3
"""Download the primary sources behind each reading list, one folder per essay.

WHY A SCRIPT AND NOT A PILE OF CURLS: the reading lists are the spec. Entries get
added and links rot, so the download must be regenerable and must report an HONEST
status per source — a study folder that silently contains a paywall stub is worse
than an empty one, because you only discover it after committing to read.

Layout (one folder per list, one per essay — deep study is sequential):

    docs/reading-lists/sources/<list-slug>/
        INDEX.md                     digest order + status of every source
        NN-<essay-slug>/
            SOURCE.md                provenance, licence posture, what landed
            PRIOR.md                 the reading list's OWN claims about this work,
                                     extracted verbatim — the prior your deep pass
                                     is supposed to CONFIRM or REFUTE
            <fetched files>          .pdf / .html / .txt as served

Status vocabulary (never fudged):
    full          the primary text itself landed (open-access PDF or full article)
    landing-only  only the public abstract/landing page is served — the full text is
                  behind a paywall. NOT bypassed, NOT faked; read via institutional
                  access or an author copy.
    unresolved    the list names a work but gives no public URL, and this script does
                  not guess a link. Resolve by hand, then add it to LINK_OVERRIDES.
    failed        fetch attempted and errored — reason recorded.

Usage:
    python3 scripts/fetch_reading_sources.py            # fetch what is missing
    python3 scripts/fetch_reading_sources.py --force    # re-fetch everything
    python3 scripts/fetch_reading_sources.py --check    # report status, download nothing
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTS_DIR = ROOT / "docs" / "reading-lists"
OUT_DIR = LISTS_DIR / "sources"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PAUSE_S = 1.5  # be a polite guest on someone else's server

# Which list docs to process → the folder name they get.
LISTS = {
    "ai-reading-list-07-30-2026.md": "frontier-ai-reading-list",
    "ai-enabled-research-reading-list-07-30-2026.md": "ai-for-math-and-science",
}

# Hosts that serve only an abstract to the public. We fetch the landing page (which is
# public) and label it honestly rather than pretending we have the paper.
PAYWALLED_HOSTS = ("nature.com", "science.org", "sciencedirect.com", "springer.com",
                   "ieeexplore.ieee.org", "dl.acm.org", "jstor.org")

# Entries the markdown names without a URL. Left EMPTY on purpose: this script will not
# invent a citation. Add a verified link here and re-run.
#
# Searched and NOT found (2026-08-01), so deliberately still unresolved:
#   "Mathematical Exploration and Discovery at Scale" (AlphaEvolve) — no arXiv match
#   "AI-assisted proof of Nesterov's Accelerated Method" (Ryu)      — no arXiv match
#   "AlphaEvolve's Bruhat Interval Hypercube Discovery"             — no arXiv match
# All three are described inside the Quanta article (entry 01 of that list), which DID
# download — so the deep pass has a real source for the story, just not the primaries.
LINK_OVERRIDES: dict[str, str] = {}

# Landing pages that are NOT the paper. Each URL below was probed and confirmed to
# return a real PDF (%PDF magic bytes) before being added — none is a guessed path.
EXTRA_PDFS: dict[int | str, str] = {
    "Brook for GPUs": "https://graphics.stanford.edu/papers/brookgpu/brookgpu.pdf",
    "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control":
        "https://robotics-transformer2.github.io/assets/rt2.pdf",
}

# Sources whose full text we could not retrieve, with the honest reason. Recorded so a
# reader knows to open it by hand rather than assuming the folder holds the paper.
FETCH_NOTES: dict[str, str] = {
    "A Path Towards Autonomous Machine Intelligence (APTAMI)":
        "OpenReview serves a JavaScript shell to plain HTTP (42 words extracted) and "
        "returns 403 to its own /pdf endpoint for automated clients. NOT circumvented — "
        "open https://openreview.net/pdf?id=BZ5a1r-kVsf in a browser to read it.",
    "AlphaGo Zero":
        "Nature paywall. The landing page (abstract + figures) is what is public.",
}


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:60]


def parse_entries(md: str) -> list[dict]:
    """Pull `### N. Title (year)` blocks, with or without a markdown link."""
    entries, lines = [], md.splitlines()
    heads = [(i, l) for i, l in enumerate(lines) if re.match(r"^###\s+\d+\.", l)]
    for idx, (line_no, head) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        body = "\n".join(lines[line_no + 1:end]).strip()
        m = re.match(r"^###\s+(\d+)\.\s+(.*)$", head)
        num, rest = m.group(1), m.group(2)
        link = re.search(r'\[["“]?(.+?)["”]?\]\((https?://[^)]+)\)', rest)
        if link:
            title, url = link.group(1), link.group(2)
        else:  # named but unlinked — e.g. "AlphaEvolve / Mathematical Exploration…"
            title = re.sub(r"\s*\(.*?\)\s*$", "", rest).strip().strip('"“”')
            url = LINK_OVERRIDES.get(title, "")
        entries.append({"num": int(num), "title": title.strip('"“”'),
                        "url": url, "prior": body})
    return entries


def html_to_text(raw: bytes) -> str:
    s = raw.decode("utf-8", errors="replace")
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?is)<br\s*/?>|</p>|</div>|</h[1-6]>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", s).strip()


def fetch(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get("Content-Type", "")


def arxiv_pdf_url(url: str) -> str | None:
    m = re.search(r"arxiv\.org/abs/([\w.\-/]+)", url)
    return f"https://arxiv.org/pdf/{m.group(1)}" if m else None


def grab(entry: dict, folder: Path) -> dict:
    """Fetch one source. Returns {status, files, note} — honest on every path."""
    url = entry["url"]
    if not url:
        return {"status": "unresolved", "files": [],
                "note": "the list names this work but gives no public URL; "
                        "no link was guessed. Add a verified one to LINK_OVERRIDES."}
    files, notes = [], []
    paywalled = any(h in url for h in PAYWALLED_HOSTS)

    # Landing page ≠ paper: fetch the author-hosted PDF where we verified one exists.
    extra = EXTRA_PDFS.get(entry["title"])
    if extra:
        try:
            raw, _ = fetch(extra)
            if raw[:4] == b"%PDF":
                (folder / "paper.pdf").write_bytes(raw)
                files.append("paper.pdf")
                notes.append(f"author-hosted PDF from {extra}")
            else:
                notes.append(f"{extra} did not return a PDF — landing page only")
            time.sleep(PAUSE_S)
        except Exception as e:  # noqa: BLE001
            notes.append(f"extra PDF fetch failed: {e}")

    # arXiv: the PDF is the primary text and is open access.
    pdf = arxiv_pdf_url(url)
    if pdf:
        try:
            raw, _ = fetch(pdf)
            if raw[:4] == b"%PDF":
                p = folder / "paper.pdf"
                p.write_bytes(raw)
                files.append(p.name)
                notes.append(f"open-access PDF from {pdf}")
            time.sleep(PAUSE_S)
        except Exception as e:  # noqa: BLE001
            notes.append(f"arXiv PDF fetch failed: {e}")

    try:
        raw, ctype = fetch(url)
    except Exception as e:  # noqa: BLE001
        if files:
            return {"status": "full", "files": files,
                    "note": "; ".join(notes) + f"; landing page failed: {e}"}
        return {"status": "failed", "files": [], "note": f"{type(e).__name__}: {e}"}

    if raw[:4] == b"%PDF":
        p = folder / "paper.pdf"
        p.write_bytes(raw)
        files.append(p.name)
        notes.append("PDF served directly")
    else:
        (folder / "page.html").write_bytes(raw)
        text = html_to_text(raw)
        (folder / "page.txt").write_text(text)
        files += ["page.html", "page.txt"]
        notes.append(f"{len(text.split())} words of readable text extracted")

    known = FETCH_NOTES.get(entry["title"])
    if known:
        notes.append(known)
    has_pdf = any(f.endswith(".pdf") for f in files)
    word_count = len(html_to_text(raw).split()) if not raw[:4] == b"%PDF" else 0

    # A 200 is not a paper. A landing page or a JS shell reads as success in a status
    # column and wastes a study session — call it what it is.
    if not has_pdf and (paywalled or known or word_count < 400):
        reason = ("Publisher paywall — full text NOT retrieved, nothing circumvented."
                  if paywalled else
                  f"Only {word_count} words of text — this is a landing page or JS "
                  f"shell, not the primary text.")
        return {"status": "landing-only", "files": files,
                "note": "; ".join(notes + [reason])}
    return {"status": "full", "files": files, "note": "; ".join(notes)}


def write_entry_docs(folder: Path, entry: dict, res: dict, list_name: str) -> None:
    (folder / "PRIOR.md").write_text(
        f"# Prior claims — {entry['title']}\n\n"
        f"> Extracted verbatim from `docs/reading-lists/{list_name}`. This is what the\n"
        f"> reading list ALREADY asserts about this work. Your deep pass is not a summary —\n"
        f"> it is a test: confirm, sharpen, or refute each line against the primary text.\n\n"
        f"{entry['prior']}\n")
    files = "\n".join(f"- `{f}`" for f in res["files"]) or "- (nothing downloaded)"
    (folder / "SOURCE.md").write_text(
        f"# {entry['num']:02d}. {entry['title']}\n\n"
        f"- **primary URL:** {entry['url'] or '(none in the list)'}\n"
        f"- **status:** `{res['status']}`\n"
        f"- **note:** {res['note']}\n\n"
        f"## Files\n\n{files}\n\n"
        f"## Licence posture\n\n"
        f"Downloaded for personal study only. Copyright remains with the authors and\n"
        f"publishers; nothing here is redistributed. Paywalled works are never\n"
        f"circumvented — they are recorded as `landing-only` and read through legitimate\n"
        f"access.\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-fetch even if files exist")
    ap.add_argument("--check", action="store_true", help="report only, download nothing")
    args = ap.parse_args()

    grand = []
    for md_name, list_slug in LISTS.items():
        md_path = LISTS_DIR / md_name
        if not md_path.exists():
            print(f"⚠ missing list: {md_path}")
            continue
        entries = parse_entries(md_path.read_text())
        list_dir = OUT_DIR / list_slug
        list_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n── {list_slug} — {len(entries)} entries ──")
        rows = []
        for e in entries:
            folder = list_dir / f"{e['num']:02d}-{slugify(e['title'])}"
            folder.mkdir(parents=True, exist_ok=True)
            existing = [p.name for p in folder.iterdir()
                        if p.suffix in (".pdf", ".html", ".txt")]
            if args.check:
                res = {"status": "present" if existing else "absent",
                       "files": existing, "note": "check-only"}
            elif existing and not args.force:
                res = {"status": "full", "files": existing, "note": "already downloaded"}
            else:
                res = grab(e, folder)
                time.sleep(PAUSE_S)
            if not args.check:
                write_entry_docs(folder, e, res, md_name)
            icon = {"full": "✓", "landing-only": "◐", "unresolved": "○",
                    "failed": "✗", "present": "✓", "absent": "○"}.get(res["status"], "?")
            print(f"  {icon} {e['num']:02d} {e['title'][:52]:<52} {res['status']}")
            rows.append((e, res, folder))
        grand.append((list_slug, rows))

        if not args.check:
            lines = [f"# Sources — {list_slug}", "",
                     "One folder per essay. Digest them **in order, one at a time** —",
                     "depth over coverage. Each folder carries `SOURCE.md` (provenance +",
                     "honest status) and `PRIOR.md` (what the reading list already claims,",
                     "which your deep pass must confirm or refute).", "",
                     "| # | source | status | files |", "|---|---|---|---|"]
            for e, res, folder in rows:
                lines.append(f"| {e['num']:02d} | [{e['title']}]({folder.name}/) | "
                             f"`{res['status']}` | {len(res['files'])} |")
            n_full = sum(1 for _, r, _ in rows if r["status"] == "full")
            lines += ["", f"**{n_full}/{len(rows)} have their primary text locally.** "
                          "`landing-only` = publisher paywall, not circumvented. "
                          "`unresolved` = the list names the work without a public link; "
                          "no citation was invented.", ""]
            (list_dir / "INDEX.md").write_text("\n".join(lines))

    total = sum(len(r) for _, r in grand)
    full = sum(1 for _, rows in grand for _, res, _ in rows if res["status"] == "full")
    print(f"\n{full}/{total} sources have their primary text locally.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
