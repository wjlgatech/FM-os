#!/usr/bin/env python3
"""Compile data/*.yml -> site/data.json for the FM-os agentic webapp.

The webapp is grounded in the SAME single source of truth as the README, so its
actions operate on real, verified data and cannot hallucinate resources.
"""
from __future__ import annotations

import json

from fmos import DATA, ROOT, load, repos_with_stars

OUT = ROOT / "site" / "data.json"


def main() -> int:
    """Compile all data/*.yml (repos with live stars) into site/data.json."""
    bundle = {
        "generated": True,
        "meta": load("meta"),
        "repos": repos_with_stars(),
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
