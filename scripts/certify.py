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

from fmos import DATA, ROOT, frontmatter, load

RUBRIC = load("certify")

TEXT_EXT = {".md", ".py", ".sh", ".js", ".ts", ".yml", ".yaml", ".json", ".toml", ".txt"}
DOC_NAMES = ("SKILL.md", "skill.md", "README.md", "readme.md")
MANIFEST = ("plugin.json", ".claude-plugin", "workflow.yaml", "action.yml", "action.yaml")


class Dim:
    """A measured (or not-measured) dimension result."""

    def __init__(self, score: int | None, evidence: str, measured: bool = True) -> None:
        """Hold a dimension's 0-100 score (or None if not measured) + its evidence."""
        self.score = score  # 0..100 or None
        self.evidence = evidence
        self.measured = measured and score is not None


# ── evidence gathering ───────────────────────────────────────────────────────
def gather(target: pathlib.Path) -> tuple[list[pathlib.Path], str, tuple | None]:
    """Collect readable text files under ``target`` → (files, joined-blob, doc)."""
    files: list[pathlib.Path] = []
    blob: list[str] = []
    doc: tuple | None = None
    for p in sorted(target.rglob("*")):
        if not (p.is_file() and p.suffix.lower() in TEXT_EXT and ".git" not in p.parts):
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        files.append(p)
        blob.append(text)
        if doc is None and p.name in DOC_NAMES:
            doc = (p, text)
    return files, "\n".join(blob), doc


# ── the certifier ─────────────────────────────────────────────────────────────
class Certifier:
    """Scores one tool against the rubric. Evidence is gathered once in __init__;
    each ``_dimension`` method reads that shared state and returns a ``Dim``."""

    def __init__(self, target: pathlib.Path, entry: dict | None = None) -> None:
        """Gather the tool's files, joined text, doc, and frontmatter up front."""
        self.target = target
        self.entry = entry or {}
        self.files, self.blob, self.doc = gather(target)
        self.fm = frontmatter(self.doc[1]) if self.doc else {}

    @property
    def name(self) -> str:
        """Display name: explicit entry name, else frontmatter, else dir name."""
        return self.entry.get("name") or self.fm.get("name") or self.target.name

    def _provenance(self) -> Dim:
        """Verifiable identity: content-hash pin plus declared source/author."""
        h = hashlib.sha256()
        for p in sorted(self.files):
            h.update(p.read_bytes())
        score, notes = 40, [f"content-hash {h.hexdigest()[:16]}"]
        if self.entry.get("source"):
            score += 30
            notes.append("source declared")
        if self.entry.get("author"):
            score += 30
            notes.append("author declared")
        return Dim(min(score, 100), "; ".join(notes))

    def _security(self) -> Dim:
        """Scan for dangerous patterns; any critical hit is an automatic 0."""
        cfg = RUBRIC["security"]
        crit = [p for p in cfg["critical_patterns"] if re.search(p, self.blob)]
        warn = [p for p in cfg["warn_patterns"] if re.search(p, self.blob)]
        if crit:
            return Dim(0, f"CRITICAL: {len(crit)} dangerous pattern(s) — {crit[0]}")
        ev = "clean" if not warn else f"{len(warn)} warning(s): {', '.join(w[:20] for w in warn[:3])}"
        return Dim(max(0, 100 - 15 * len(warn)), ev)

    def _relevance(self) -> Dim:
        """Count SLM/FM-ops keyword hits — the on-mission gate."""
        lc = self.blob.lower()
        hits = sorted({k for k in RUBRIC["relevance"]["keywords"] if k in lc})
        ev = f"{len(hits)} SLM/FM-ops keyword(s): {', '.join(hits[:6])}" if hits else "no on-mission keywords"
        return Dim(min(100, len(hits) * 18), ev)

    def _docs(self) -> Dim:
        """Reward a doc that has a description, a trigger, and a usage example."""
        if not self.doc:
            return Dim(0, "no SKILL.md/README present")
        text, sig = self.doc[1].lower(), RUBRIC["signals"]
        score, notes = 40, ["doc present"]
        if self.fm.get("description") or "description" in text:
            score += 20
            notes.append("description")
        if any(s in text for s in sig["trigger"]):
            score += 20
            notes.append("trigger")
        if any(s in text for s in sig["example"]):
            score += 20
            notes.append("example")
        return Dim(min(score, 100), "; ".join(notes))

    def _correctness(self) -> Dim:
        """Static evidence of a test or usage example (execution is deferred to v1)."""
        has_test = any((self.target / n).exists() for n in ("tests", "test")) or bool(
            re.search(r"(test_.*\.py|\.test\.|def test_)", self.blob))
        if has_test:
            return Dim(90, "test artifact present (static; execution is v1)")
        if "```" in self.blob or re.search(r"(?i)example|usage", self.blob):
            return Dim(55, "usage example present, no test (static)")
        return Dim(20, "no example or test found")

    def _cross_runtime(self) -> Dim:
        """Credit tools that signal they run beyond a single agent host."""
        hits = [s for s in RUBRIC["signals"]["cross_runtime"] if s in self.blob.lower()]
        if not hits:
            return Dim(50, "single-runtime (no cross-runtime signal) — assumed Claude-only")
        return Dim(min(100, 60 + 15 * len(hits)), f"cross-runtime: {', '.join(hits)}")

    def _eval(self) -> Dim:
        """Credit tools that ship an eval / verification signal."""
        hits = [s for s in RUBRIC["signals"]["eval"] if s in self.blob.lower()]
        ev = f"eval signals: {', '.join(hits[:4])}" if hits else "none"
        return Dim(min(100, len(hits) * 30) if hits else 30, ev)

    def _freshness(self) -> Dim:
        """Recency of the last commit — measured only with reachable git history."""
        git = self.target
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

    def run(self) -> dict:
        """Compute every dimension, apply the blocking gates, assemble the result."""
        dims = {
            "provenance": self._provenance(),
            "security": self._security(),
            "relevance": self._relevance(),
            "docs": self._docs(),
            "correctness": self._correctness(),
            "cross_runtime": self._cross_runtime(),
            "eval": self._eval(),
            "freshness": self._freshness(),
        }
        weights = {d["id"]: d["weight"] for d in RUBRIC["dimensions"]}
        measured_w = sum(weights[k] for k, d in dims.items() if d.measured)
        score = round(sum(weights[k] * d.score for k, d in dims.items() if d.measured) / measured_w) if measured_w else 0

        sec, rel = dims["security"], dims["relevance"]
        security_ok = bool(sec.measured and sec.score >= RUBRIC["gates"]["security"]["min"])
        on_mission = bool(rel.measured and rel.score >= RUBRIC["gates"]["relevance"]["min"])
        return {
            "name": self.name,
            "kind": self.entry.get("kind", self.fm.get("kind", "skill")),
            "score": score,
            "tier": decide_tier(score, security_ok, on_mission),
            "security_ok": security_ok,
            "on_mission": on_mission,
            "dimensions": {k: {"score": d.score, "measured": d.measured, "evidence": d.evidence} for k, d in dims.items()},
            "gaps": [f"{k} ({d.score})" for k, d in dims.items() if d.measured and d.score < 60],
            "source": self.entry.get("source", ""),
        }


# ── scoring ──────────────────────────────────────────────────────────────────
def decide_tier(score: int, security_ok: bool, on_mission: bool) -> str:
    """Map a score + the blocking gates to a tier. Gates dominate the score."""
    if not on_mission:
        return "not-applicable"
    if not security_ok:
        return "rejected"
    if score >= RUBRIC["tiers"]["certified"]:
        return "certified"
    if score >= RUBRIC["tiers"]["provisional"]:
        return "provisional"
    return "rejected"


def certify(target: pathlib.Path, entry: dict | None = None) -> dict:
    """Score one tool against the rubric → {score, tier, per-dimension evidence}."""
    return Certifier(target, entry).run()


# ── badge (shields.io endpoint schema) ───────────────────────────────────────
def badge(result: dict) -> dict:
    """Build a shields.io endpoint-schema badge JSON for a certification result."""
    color = {"certified": "brightgreen", "provisional": "yellow",
             "rejected": "red", "not-applicable": "lightgrey"}[result["tier"]]
    label = "FM-os Certified"
    msg = f"{result['tier']} · {result['score']}/100" if result["tier"] in ("certified", "provisional") else result["tier"]
    return {"schemaVersion": 1, "label": label, "message": msg, "color": color}


# ── CLI ──────────────────────────────────────────────────────────────────────
def print_human(r: dict) -> None:
    """Print a certification result as an aligned per-dimension scorecard."""
    icon = {"certified": "✅", "provisional": "🟡", "rejected": "❌", "not-applicable": "⚪"}[r["tier"]]
    print(f"{icon}  {r['name']} ({r['kind']}) — {r['tier'].upper()}  score {r['score']}/100")
    for k, d in r["dimensions"].items():
        s = f"{d['score']:>3}" if d["measured"] else " NM"
        print(f"    {s}  {k:<13} {d['evidence']}")
    if r["gaps"]:
        print(f"    ↑ improve: {', '.join(r['gaps'])}")


def main() -> int:
    """CLI: certify a --target dir or the whole --registry; gate CI with --gate."""
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
