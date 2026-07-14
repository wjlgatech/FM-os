"""Shared helpers for the FM-os build/validate/certify scripts.

One place for the data-directory paths, the YAML loader, markdown escaping, and
the stars-merge — so the five scripts stop each redefining their own copy.
"""
from __future__ import annotations

import pathlib
import re

import yaml

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent.parent
DATA: pathlib.Path = ROOT / "data"


def load(name: str) -> list | dict:
    """Parse ``data/<name>.yml`` → list/dict, or ``[]`` when the file is absent."""
    path = DATA / f"{name}.yml"
    if not path.exists():
        return []
    return yaml.safe_load(path.read_text()) or []


def esc(text: object) -> str:
    """Normalize whitespace for Markdown output (collapse runs to single spaces).

    Deliberately does NOT HTML-escape: the README renders raw ``&`` (e.g.
    "Jobs & Careers"); browser-side escaping lives in the webapp's own helper.
    """
    return " ".join(str("" if text is None else text).split())


def repos_with_stars() -> list:
    """Load ``repos`` with live ``stars`` merged in from the generated ``_stars.yml``."""
    repos = load("repos")
    stars = load("_stars") if (DATA / "_stars.yml").exists() else {}
    if isinstance(stars, dict):
        for entry in repos:
            stat = stars.get(entry.get("repo"))
            if stat and stat.get("stars") is not None:
                entry["stars"] = stat["stars"]
    return repos


def frontmatter(text: str) -> dict:
    """Extract the leading ``---``-delimited YAML frontmatter block as a dict."""
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
