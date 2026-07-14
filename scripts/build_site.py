#!/usr/bin/env python3
"""Compile data/*.yml -> site/data.json for the FM-os agentic webapp.

The webapp is grounded in the SAME single source of truth as the README, so its
actions operate on real, verified data and cannot hallucinate resources.
"""
from __future__ import annotations

import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "site" / "data.json"


def load(name: str):
    path = DATA / f"{name}.yml"
    return (yaml.safe_load(path.read_text()) if path.exists() else []) or []


def main() -> int:
    repos = load("repos")
    stars = load("_stars") if (DATA / "_stars.yml").exists() else {}
    if isinstance(stars, dict):
        for e in repos:
            stat = stars.get(e.get("repo"))
            if stat and stat.get("stars") is not None:
                e["stars"] = stat["stars"]

    bundle = {
        "generated": True,
        "repos": repos,
        "courses": load("courses"),
        "papers": load("papers"),
        "jobs": load("jobs"),
        "models": load("models"),
        "registry": load("registry"),
        "certifications": load("_certifications") if (DATA / "_certifications.yml").exists() else {},
    }
    bundle["counts"] = {k: len(v) for k, v in bundle.items() if isinstance(v, list)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(bundle, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT.relative_to(ROOT)} — {bundle['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
