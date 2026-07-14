#!/usr/bin/env python3
"""Schema gate for data/*.yml — every entry needs its required fields + a URL.

This is the cheap, offline half of `make check`; the CI link-checker (lychee)
is the online half that confirms URLs actually resolve.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

REQUIRED = {
    "repos": ["name", "url", "category"],
    "courses": ["title", "url", "topic"],
    "papers": ["title", "url", "topic"],
    "jobs": ["name", "url", "type"],
    "models": ["name", "url", "params", "license"],
}


def main() -> int:
    errors: list[str] = []
    for name, fields in REQUIRED.items():
        path = DATA / f"{name}.yml"
        if not path.exists():
            errors.append(f"{name}.yml: missing")
            continue
        try:
            rows = yaml.safe_load(path.read_text()) or []
        except yaml.YAMLError as exc:
            errors.append(f"{name}.yml: invalid YAML — {exc}")
            continue
        if not isinstance(rows, list):
            errors.append(f"{name}.yml: top level must be a list")
            continue
        seen_urls = set()
        for i, e in enumerate(rows):
            where = f"{name}.yml[{i}]"
            if not isinstance(e, dict):
                errors.append(f"{where}: entry must be a mapping")
                continue
            for f in fields:
                if not e.get(f):
                    errors.append(f"{where}: missing required field '{f}'")
            url = str(e.get("url", ""))
            if url and not url.startswith(("http://", "https://")):
                errors.append(f"{where}: url must start with http(s):// — got {url!r}")
            if url in seen_urls:
                errors.append(f"{where}: duplicate url {url}")
            seen_urls.add(url)

    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print("Validation passed — all data/*.yml entries have required fields + URLs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
