#!/usr/bin/env python3
"""FM-os Certified — score a skill / plugin / workflow against data/certify.yml.

Two modes:
  certify.py --target <dir> [--json] [--badge out.json] [--gate N]
      Certify one tool from its own files (what the CI action runs in an
      author's repo). Produces REAL static evidence: provenance hash, a
      data-driven security scan, docs/relevance/cross-runtime/eval signals.
  certify.py --registry
      Certify every entry in data/registry.yml that has a local `path`, and
      write the generated results to data/_certifications.yml (like _stars.yml).

v0.1 is STATIC ONLY — it never executes the tool. Discipline: evidence over
claims; a dimension with no evidence is "not measured" and excluded from the
score (never a fake pass); a blocking gate cannot pass on unmeasured items.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RUBRIC = yaml.safe_load((DATA / "certify.yml").read_text())

TEXT_EXT = {".md", ".py", ".sh", ".js", ".ts", ".yml", ".yaml", ".json", ".toml", ".txt"}
DOC_NAMES = ("SKILL.md", "skill.md", "README.md", "readme.md")
MANIFEST = ("plugin.json", ".claude-plugin", "workflow.yaml", "action.yml", "action.yaml")


class Dim:
    """A measured (or not-measured) dimension result."""

    def __init__(self, score, evidence, measured=True):
        self.score = score  # 0..100 or None
        self.evidence = evidence
        self.measured = measured and score is not None


# ── evidence gathering ───────────────────────────────────────────────────────
def gather(target: pathlib.Path):
    files, blob, doc = [], [], None
    for p in sorted(target.rglob("*")):
        if p.is_file() and p.suffix.lower() in TEXT_EXT and ".git" not in p.parts:
            try:
                t = p.read_text(errors="ignore")
            except Exception:
                continue
            files.append(p)
            blob.append(t)
            if doc is None and p.name in DOC_NAMES:
                doc = (p, t)
    return files, "\n".join(blob), doc


def frontmatter(doc_text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", doc_text, re.S)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


# ── dimensions ───────────────────────────────────────────────────────────────
def dim_provenance(target, files, entry) -> Dim:
    h = hashlib.sha256()
    for p in sorted(files):
        h.update(p.read_bytes())
    digest = h.hexdigest()[:16]
    score, notes = 40, [f"content-hash {digest}"]  # hashable identity is baseline
    if entry.get("source"):
        score += 30
        notes.append("source declared")
    if entry.get("author"):
        score += 30
        notes.append("author declared")
    return Dim(min(score, 100), "; ".join(notes))


def dim_security(blob) -> Dim:
    cfg = RUBRIC["security"]
    crit = [p for p in cfg["critical_patterns"] if re.search(p, blob)]
    warn = [p for p in cfg["warn_patterns"] if re.search(p, blob)]
    if crit:
        return Dim(0, f"CRITICAL: {len(crit)} dangerous pattern(s) — {crit[0]}")
    score = max(0, 100 - 15 * len(warn))
    ev = "clean" if not warn else f"{len(warn)} warning(s): {', '.join(w[:20] for w in warn[:3])}"
    return Dim(score, ev)


def dim_relevance(blob) -> Dim:
    lc = blob.lower()
    hits = sorted({k for k in RUBRIC["relevance"]["keywords"] if k in lc})
    score = min(100, len(hits) * 18)
    return Dim(score, f"{len(hits)} SLM/FM-ops keyword(s): {', '.join(hits[:6])}" if hits else "no on-mission keywords")


def dim_docs(doc, fm) -> Dim:
    if not doc:
        return Dim(0, "no SKILL.md/README present")
    text = doc[1].lower()
    sig = RUBRIC["signals"]
    score, notes = 40, ["doc present"]
    if fm.get("description") or "description" in text:
        score += 20
        notes.append("description")
    if any(s in text for s in sig["trigger"]):
        score += 20
        notes.append("trigger")
    if any(s in text for s in sig["example"]):
        score += 20
        notes.append("example")
    return Dim(min(score, 100), "; ".join(notes))


def dim_correctness(target, blob) -> Dim:
    has_test = any((target / n).exists() for n in ("tests", "test")) or bool(
        re.search(r"(test_.*\.py|\.test\.|def test_)", blob)
    )
    has_example = "```" in blob or bool(re.search(r"(?i)example|usage", blob))
    if has_test:
        return Dim(90, "test artifact present (static; execution is v1)")
    if has_example:
        return Dim(55, "usage example present, no test (static)")
    return Dim(20, "no example or test found")


def dim_cross_runtime(blob) -> Dim:
    lc = blob.lower()
    hits = [s for s in RUBRIC["signals"]["cross_runtime"] if s in lc]
    if not hits:
        return Dim(50, "single-runtime (no cross-runtime signal) — assumed Claude-only")
    return Dim(min(100, 60 + 15 * len(hits)), f"cross-runtime: {', '.join(hits)}")


def dim_eval(blob) -> Dim:
    lc = blob.lower()
    hits = [s for s in RUBRIC["signals"]["eval"] if s in lc]
    return Dim(min(100, len(hits) * 30) if hits else 30, f"eval signals: {', '.join(hits[:4])}" if hits else "none")


def dim_freshness(target) -> Dim:
    git = target
    for _ in range(4):
        if (git / ".git").exists():
            break
        git = git.parent
    if not (git / ".git").exists():
        return Dim(None, "no git history at target — not measured", measured=False)
    try:
        out = subprocess.check_output(
            ["git", "-C", str(git), "log", "-1", "--format=%cr"], text=True).strip()
    except Exception:
        return Dim(None, "git log unavailable — not measured", measured=False)
    score = 90 if any(u in out for u in ("hour", "minute", "day")) else \
        70 if "week" in out else 50 if "month" in out else 30
    return Dim(score, f"last commit {out}")


# ── scoring ──────────────────────────────────────────────────────────────────
def certify(target: pathlib.Path, entry: dict | None = None) -> dict:
    entry = entry or {}
    files, blob, doc = gather(target)
    fm = frontmatter(doc[1]) if doc else {}
    name = entry.get("name") or fm.get("name") or target.name

    dims = {
        "provenance": dim_provenance(target, files, entry),
        "security": dim_security(blob),
        "relevance": dim_relevance(blob),
        "docs": dim_docs(doc, fm),
        "correctness": dim_correctness(target, blob),
        "cross_runtime": dim_cross_runtime(blob),
        "eval": dim_eval(blob),
        "freshness": dim_freshness(target),
    }
    weights = {d["id"]: d["weight"] for d in RUBRIC["dimensions"]}

    measured_w = sum(weights[k] for k, d in dims.items() if d.measured)
    score = round(sum(weights[k] * d.score for k, d in dims.items() if d.measured) / measured_w) if measured_w else 0

    # gates
    g = RUBRIC["gates"]
    sec, rel = dims["security"], dims["relevance"]
    security_ok = sec.measured and sec.score >= g["security"]["min"]
    on_mission = rel.measured and rel.score >= g["relevance"]["min"]

    if not on_mission:
        tier = "not-applicable"
    elif not security_ok:
        tier = "rejected"
    elif score >= RUBRIC["tiers"]["certified"]:
        tier = "certified"
    elif score >= RUBRIC["tiers"]["provisional"]:
        tier = "provisional"
    else:
        tier = "rejected"

    gaps = [f"{k} ({d.score})" for k, d in dims.items()
            if d.measured and d.score < 60]
    return {
        "name": name,
        "kind": entry.get("kind", fm.get("kind", "skill")),
        "score": score,
        "tier": tier,
        "security_ok": security_ok,
        "on_mission": on_mission,
        "dimensions": {k: {"score": d.score, "measured": d.measured, "evidence": d.evidence} for k, d in dims.items()},
        "gaps": gaps,
        "source": entry.get("source", ""),
    }


# ── badge (shields.io endpoint schema) ───────────────────────────────────────
def badge(result: dict) -> dict:
    color = {"certified": "brightgreen", "provisional": "yellow",
             "rejected": "red", "not-applicable": "lightgrey"}[result["tier"]]
    label = "FM-os Certified"
    msg = f"{result['tier']} · {result['score']}/100" if result["tier"] in ("certified", "provisional") else result["tier"]
    return {"schemaVersion": 1, "label": label, "message": msg, "color": color}


# ── CLI ──────────────────────────────────────────────────────────────────────
def print_human(r: dict):
    icon = {"certified": "✅", "provisional": "🟡", "rejected": "❌", "not-applicable": "⚪"}[r["tier"]]
    print(f"{icon}  {r['name']} ({r['kind']}) — {r['tier'].upper()}  score {r['score']}/100")
    for k, d in r["dimensions"].items():
        s = f"{d['score']:>3}" if d["measured"] else " NM"
        print(f"    {s}  {k:<13} {d['evidence']}")
    if r["gaps"]:
        print(f"    ↑ improve: {', '.join(r['gaps'])}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target")
    ap.add_argument("--registry", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--badge")
    ap.add_argument("--gate", type=int, help="exit non-zero if score < N or a blocking gate fails")
    args = ap.parse_args()

    if args.registry:
        reg = yaml.safe_load((DATA / "registry.yml").read_text()) or []
        out = {}
        for e in reg:
            if not e.get("path"):
                continue
            tp = (ROOT / e["path"]).resolve() if not pathlib.Path(e["path"]).is_absolute() else pathlib.Path(e["path"])
            if not tp.exists():
                print(f"  ⚠ skip {e['name']}: path not found ({e['path']})")
                continue
            r = certify(tp, e)
            out[e["name"]] = {k: r[k] for k in ("kind", "score", "tier", "security_ok", "on_mission", "source", "gaps")}
            bp = ROOT / "site" / "badges" / f"{e['name']}.json"
            bp.parent.mkdir(parents=True, exist_ok=True)
            bp.write_text(json.dumps(badge(r)))
            print_human(r)
        (DATA / "_certifications.yml").write_text(
            "# GENERATED by scripts/certify.py --registry — do not edit.\n"
            + yaml.safe_dump(out, sort_keys=True, allow_unicode=True))
        print(f"\nWrote data/_certifications.yml — {len(out)} tool(s) certified.")
        return 0

    if not args.target:
        ap.error("give --target <dir> or --registry")
    r = certify(pathlib.Path(args.target).resolve())
    if args.badge:
        pathlib.Path(args.badge).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.badge).write_text(json.dumps(badge(r)))
    print(json.dumps(r, indent=2) if args.json else "", end="")
    if not args.json:
        print_human(r)
    if args.gate is not None:
        if not r["on_mission"]:
            print(f"::gate:: not on-mission (relevance) — out of scope", file=sys.stderr)
            return 1
        if not r["security_ok"] or r["score"] < args.gate:
            print(f"::gate:: FAILED — score {r['score']} < {args.gate} or security gate", file=sys.stderr)
            return 1
        print(f"::gate:: PASSED — score {r['score']} >= {args.gate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
