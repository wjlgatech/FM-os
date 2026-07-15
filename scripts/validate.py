#!/usr/bin/env python3
"""Schema gate for data/*.yml — every entry needs its required fields + a URL.

This is the cheap, offline half of `make check`; the CI link-checker (lychee)
is the online half that confirms URLs actually resolve.
"""
from __future__ import annotations

import sys

import yaml

from fmos import DATA

REQUIRED = {
    "repos": ["name", "url", "category"],
    "courses": ["title", "url", "topic"],
    "papers": ["title", "url", "topic"],
    "jobs": ["name", "url", "type"],
    "labs": ["name", "url", "category"],
    "models": ["name", "url", "params", "license"],
    "registry": ["name", "kind"],
}


def check_entry(entry: object, fields: list[str], where: str, seen: set) -> list[str]:
    """Validate one data entry: required fields present, URL well-formed + unique."""
    if not isinstance(entry, dict):
        return [f"{where}: entry must be a mapping"]
    errs = [f"{where}: missing required field '{f}'" for f in fields if not entry.get(f)]
    url = str(entry.get("url", ""))
    if url and not url.startswith(("http://", "https://")):
        errs.append(f"{where}: url must start with http(s):// — got {url!r}")
    if url and url in seen:
        errs.append(f"{where}: duplicate url {url}")
    if url:
        seen.add(url)
    return errs


def check_file(name: str, fields: list[str]) -> list[str]:
    """Validate one data/*.yml file end to end."""
    path = DATA / f"{name}.yml"
    if not path.exists():
        return [f"{name}.yml: missing"]
    try:
        rows = yaml.safe_load(path.read_text()) or []
    except yaml.YAMLError as exc:
        return [f"{name}.yml: invalid YAML — {exc}"]
    if not isinstance(rows, list):
        return [f"{name}.yml: top level must be a list"]
    seen: set = set()
    errs: list[str] = []
    for i, entry in enumerate(rows):
        errs += check_entry(entry, fields, f"{name}.yml[{i}]", seen)
    return errs


def main() -> int:
    """Validate every data/*.yml file; exit non-zero if any entry is malformed."""
    errors: list[str] = []
    for name, fields in REQUIRED.items():
        errors += check_file(name, fields)

    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print("Validation passed — all data/*.yml entries have required fields + URLs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
