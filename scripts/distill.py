#!/usr/bin/env python3
"""
distill.py — turn each cited repo into (1) a grounded knowledge graph + (2) an agentic-tooling
scaffold. The hub's distillation factory: data/repos.yml (spec) -> distill/<slug>/{graph.json,SKILL.md}.

Design (matches the FM-os philosophy):
  - HONEST: the KG is built ONLY from data we actually have (repos.yml blurb/category, the
    jd_taxonomy concept vocabulary, labs.yml authorship, sibling repos). Every node + edge carries
    a `provenance` string. No LLM guesswork, nothing fabricated — no evidence ⇒ no node.
  - CHEAP + FAST: pure-stdlib, deterministic, no network, no model. Milliseconds per repo.
  - UP-TO-DATE: each graph pins a content hash of its source entry; `--check` flags drift so a
    weekly CI cron can regenerate only what changed.
  - FUTURE-PROOF: spec-as-data (repos.yml is the single trigger list); the semantic layer is a
    swappable seam (a richer LLM analyzer can replace concept-matching without changing consumers);
    standard JSON graph + SKILL.md that any harness can read.

The tooling scaffold is gated by the EXISTING certify.py (run separately) — a scaffold too thin to
clear the bar is simply not certified (no fake pass). Promotion distill/ -> the curated registry is
a human step.

Usage:
    python3 scripts/distill.py --slugs unsloth,vllm,verifiers   # a thin slice
    python3 scripts/distill.py --all                            # every cited repo
    python3 scripts/distill.py --check                          # validate graphs + flag drift (gates CI)
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, sys
from fmos import ROOT, load

OUT = ROOT / "distill"


def slug_of(repo: dict) -> str:
    r = repo.get("repo") or repo.get("url", "")
    tail = r.rstrip("/").split("/")[-1] if r else repo["name"]
    return re.sub(r"[^a-z0-9]+", "-", tail.lower()).strip("-")


def owner_of(repo: dict) -> str:
    r = repo.get("repo", "")
    if "/" in r:
        return r.split("/")[0].lower()
    m = re.search(r"github\.com/([^/]+)/", repo.get("url", ""))
    return m.group(1).lower() if m else ""


def entry_hash(repo: dict) -> str:
    return hashlib.sha256(json.dumps(repo, sort_keys=True).encode()).hexdigest()[:16]


def build_graph(repo: dict, taxonomy: list, labs: list, siblings: list) -> dict:
    """A grounded shallow KG for one repo. Every node/edge cites its provenance."""
    name, cat = repo["name"], repo.get("category", "uncategorized")
    blurb = (repo.get("blurb") or "").lower()
    sl = slug_of(repo)
    rid = f"repo:{sl}"
    nodes = {rid: {"id": rid, "type": "repo", "label": name, "provenance": "data/repos.yml"}}
    edges = []

    # category
    cid = f"category:{cat}"
    nodes[cid] = {"id": cid, "type": "category", "label": cat, "provenance": "data/repos.yml:category"}
    edges.append({"from": rid, "to": cid, "rel": "in_category", "provenance": "data/repos.yml:category"})

    # concepts — a taxonomy term is added ONLY if its keyword appears in the blurb, or the repo's
    # category is one the term covers. Provenance records exactly why.
    for t in taxonomy:
        hit = next((kw for kw in t.get("keywords", []) if kw.lower() in blurb), None)
        cat_hit = cat in t.get("repo_categories", [])
        if not hit and not cat_hit:
            continue
        nid = f"concept:{t['id']}"
        nodes[nid] = {"id": nid, "type": "concept", "label": t["label"],
                      "provenance": f"jd_taxonomy:{t['id']} via " + (f"keyword '{hit}'" if hit else f"category '{cat}'")}
        edges.append({"from": rid, "to": nid, "rel": "covers",
                      "provenance": f"blurb keyword '{hit}'" if hit else f"category '{cat}'"})

    # authorship (the EXPERTS pillar) — repo owner matched to a lab's GitHub org
    owner = owner_of(repo)
    for lab in labs:
        org = (lab.get("github", "").rstrip("/").split("/")[-1] or "").lower()
        if org and org == owner:
            lid = f"lab:{re.sub(r'[^a-z0-9]+', '-', lab['name'].lower()).strip('-')}"
            nodes[lid] = {"id": lid, "type": "lab", "label": lab["name"], "provenance": "data/labs.yml"}
            edges.append({"from": rid, "to": lid, "rel": "maintained_by",
                          "provenance": f"owner '{owner}' == labs github org"})
            break

    # related repos (same category, cap 5) — the graph's connective tissue
    for s in siblings[:5]:
        sid = f"repo:{slug_of(s)}"
        if sid == rid:
            continue
        nodes.setdefault(sid, {"id": sid, "type": "repo", "label": s["name"], "provenance": "data/repos.yml"})
        edges.append({"from": rid, "to": sid, "rel": "related", "provenance": f"same category '{cat}'"})

    return {"repo": repo.get("repo", name), "slug": sl, "category": cat,
            "source_hash": entry_hash(repo), "generator": "distill.py",
            "nodes": list(nodes.values()), "edges": edges}


def build_skill(repo: dict, graph: dict) -> str:
    """A grounded agentic-tooling scaffold (gated later by certify.py — thin ⇒ not certified)."""
    name, url, cat = repo["name"], repo.get("url", ""), repo.get("category", "tool")
    blurb = repo.get("blurb", "").strip().rstrip(".")
    sl = graph["slug"]
    concepts = [n["label"] for n in graph["nodes"] if n["type"] == "concept"]
    triggers = ", ".join(f'"{c}"' for c in ([name] + concepts)[:5]) or f'"{name}"'
    return f"""---
name: {sl}-quickstart
description: >-
  Get productive with {name} ({cat}): {blurb}. A cross-runtime quickstart grounded in the
  vetted FM-os catalog — install it, run its core workflow, and verify the result.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# {sl}-quickstart

A cross-runtime skill for **[{name}]({url})** — the {cat} tool curated in
[FM-os](https://github.com/wjlgatech/FM-os): {blurb}.

## When to use (trigger)

Invoke when the user mentions {triggers}, or asks to get started with {name}.

## What it does

1. **Point at it** — clone / install {name} from {url} (read its README first; it is upstream code).
2. **Run the core workflow** — the smallest end-to-end path the repo documents for {cat}.
3. **Verify** — check the output against the repo's own example/benchmark before trusting it.

## Example

```bash
# see {url} for the authoritative quickstart
git clone {url}
# follow the repo's README to run its minimal example, then verify the result
```

## Verification (eval-with-teeth)

Only "works" if the repo's own smallest example reproduces; a run that doesn't reproduce is
reported, not shipped. No reproduction ⇒ no claim.

## Safety

HTTPS only; no secrets; upstream code is untrusted — read it before you run it.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes.
"""


def validate_graph(g: dict) -> list[str]:
    errs, ids = [], {n["id"] for n in g["nodes"]}
    if f"repo:{g['slug']}" not in ids:
        errs.append(f"{g['slug']}: missing the repo node")
    for n in g["nodes"]:
        if not n.get("provenance"):
            errs.append(f"{g['slug']}: node {n['id']} has no provenance")
    touched = set()
    for e in g["edges"]:
        touched |= {e["from"], e["to"]}
        if e["from"] not in ids or e["to"] not in ids:
            errs.append(f"{g['slug']}: edge {e['from']}->{e['to']} references a missing node")
        if not e.get("provenance"):
            errs.append(f"{g['slug']}: edge {e['from']}->{e['to']} has no provenance")
    for n in g["nodes"]:
        if n["id"] not in touched:
            errs.append(f"{g['slug']}: orphan node {n['id']} (no edge)")
    return errs


def select(repos: list, args) -> list:
    if args.all:
        return repos
    want = {s.strip() for s in (args.slugs or "").split(",") if s.strip()}
    return [r for r in repos if slug_of(r) in want]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--slugs", help="comma-separated repo slugs (thin slice)")
    ap.add_argument("--check", action="store_true", help="validate existing graphs + flag drift; gate CI")
    args = ap.parse_args()

    repos = load("repos")
    taxonomy, labs = load("jd_taxonomy"), load("labs")
    by_cat: dict[str, list] = {}
    for r in repos:
        by_cat.setdefault(r.get("category", "uncategorized"), []).append(r)

    if args.check:
        errs, drift = [], []
        for gp in sorted(OUT.glob("*/graph.json")):
            g = json.loads(gp.read_text())
            errs += validate_graph(g)
            match = next((r for r in repos if slug_of(r) == g["slug"]), None)
            if match and entry_hash(match) != g.get("source_hash"):
                drift.append(g["slug"])
        for e in errs:
            print("❌", e)
        if drift:
            print("⚠️  stale (source changed, re-run distill):", ", ".join(drift))
        if errs:
            print(f"\nFAIL — {len(errs)} graph error(s)."); return 1
        print(f"OK — {len(list(OUT.glob('*/graph.json')))} graph(s) valid" +
              (f", {len(drift)} stale" if drift else ", 0 stale") + ".")
        return 0

    chosen = select(repos, args)
    if not chosen:
        ap.error("give --all or --slugs a,b,c")
    manifest = []
    for r in chosen:
        sl = slug_of(r)
        g = build_graph(r, taxonomy, labs, by_cat.get(r.get("category", ""), []))
        errs = validate_graph(g)
        d = OUT / sl
        d.mkdir(parents=True, exist_ok=True)
        (d / "graph.json").write_text(json.dumps(g, indent=2) + "\n")
        (d / "SKILL.md").write_text(build_skill(r, g))
        manifest.append({"slug": sl, "repo": r.get("repo", r["name"]),
                         "nodes": len(g["nodes"]), "edges": len(g["edges"]),
                         "kg_valid": not errs, "source_hash": g["source_hash"],
                         "skill": f"distill/{sl}/SKILL.md", "certified": None})
        print(f"  ✓ {sl:22s} {len(g['nodes'])} nodes / {len(g['edges'])} edges"
              + ("" if not errs else f"  ❌ {len(errs)} KG errors"))
    OUT.mkdir(exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(
        {"generator": "distill.py", "count": len(manifest), "items": manifest}, indent=2) + "\n")
    print(f"\nWrote {len(manifest)} repo(s) to distill/ (+ manifest.json). "
          f"Certify tooling: python3 scripts/certify.py --target distill/<slug>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
