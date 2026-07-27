"""The held-out grounding gate — the ship/rollback decision, measured.

A model writes captions for FACT WORLDS IT NEVER TRAINED ON. Every non-glue
word that isn't in the prompt's fact set is a hallucination. The gate ships
the fine-tune only if the hallucination rate drops by a real margin AND the
model still produces text (no degeneration) — otherwise ROLLBACK.
"""
from __future__ import annotations

import re

GLUE = {
    "a", "an", "the", "with", "and", "or", "on", "in", "at", "by", "of", "to",
    "is", "are", "was", "sits", "sitting", "stands", "standing", "rests",
    "resting", "lies", "lying", "near", "beside", "under", "over", "next",
    "scene", "showing", "view", "close", "photo", "picture", "image", "caption",
    "there", "this", "that", "it", "its", "one", "two", "small", "large",
}

GATES = {"min_halluc_drop": 0.05, "min_avg_words": 3.0}


def content_words(text: str) -> list[str]:
    words = re.findall(r"[a-z]+", text.lower())
    return [w for w in words if w not in GLUE]


def hallucination_rate(caption: str, image: dict) -> float:
    """Fraction of content words not grounded in the image's facts."""
    grounded = {w.lower() for w in image["objects"] | {image["attr"], image["main"]}}
    cw = content_words(caption)
    if not cw:
        return 1.0  # empty/degenerate output grounds nothing
    return sum(1 for w in cw if w not in grounded) / len(cw)


def evaluate(captions: list[str], images: list[dict]) -> dict:
    rates = [hallucination_rate(c, im) for c, im in zip(captions, images)]
    words = [len(content_words(c)) + sum(1 for w in re.findall(r"[a-z]+", c.lower()) if w in GLUE)
             for c in captions]
    return {
        "halluc_rate": sum(rates) / len(rates),
        "avg_words": sum(words) / len(words),
        "per_prompt": rates,
    }


def gate(before: dict, after: dict) -> tuple[bool, list[str]]:
    reasons = []
    drop = before["halluc_rate"] - after["halluc_rate"]
    if drop < GATES["min_halluc_drop"]:
        reasons.append(
            f"hallucination drop {drop:+.3f} < required {GATES['min_halluc_drop']} "
            f"(before {before['halluc_rate']:.3f} -> after {after['halluc_rate']:.3f})"
        )
    if after["avg_words"] < GATES["min_avg_words"]:
        reasons.append(f"degeneration: avg words {after['avg_words']:.1f} < {GATES['min_avg_words']}")
    return (not reasons), reasons
