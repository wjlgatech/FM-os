#!/usr/bin/env python3
"""BARE-VLM as a measurable closed loop (pure stdlib, deterministic).

The BARE thesis (Base-Refine, adapted to VLMs by the syndata case study in
research-anything): a base model gives DIVERSITY, an instruction-tuned model
gives CORRECTNESS, and only the two-stage pipeline delivers both. This module
makes that thesis falsifiable at toy scale with two gates:

  alignment gate  — mean caption↔image grounding (mock-CLIP) ≥ floor
  diversity gate  — mean pairwise Jaccard distance between captions ≥ floor

Three pipelines run under identical budgets and seeds:
  base_only      diverse but hallucinates  → fails the alignment gate
  instruct_only  grounded but mode-collapses → fails the diversity gate
  bare           base drafts + instruct refinement → passes BOTH

Swap the toy generators for real models (BLIP-2 base / InstructBLIP, CLIP for
alignment) and the loop, metrics, and gates are unchanged — that is the seam.
"""
from __future__ import annotations

import itertools
import random
import sys

# ── toy "images": ground-truth facts the mock-CLIP can check against ─────────
IMAGES = [
    {"id": "cat_sill", "main": "cat", "attr": "tabby", "objects": {"cat", "windowsill", "sunlight"}},
    {"id": "fridge", "main": "refrigerator", "attr": "silver", "objects": {"refrigerator", "kitchen", "counter"}},
    {"id": "forklift", "main": "forklift", "attr": "yellow", "objects": {"forklift", "warehouse", "pallet"}},
    {"id": "snowboard", "main": "snowboarder", "attr": "orange", "objects": {"snowboarder", "slope", "jacket"}},
    {"id": "tennis", "main": "player", "attr": "white", "objects": {"player", "racket", "court"}},
    {"id": "beach_kid", "main": "child", "attr": "small", "objects": {"child", "beach", "bucket"}},
]

DECOYS = ["dog", "umbrella", "bicycle", "guitar", "pizza", "lamp"]  # never in any image

TEMPLATES = [
    "a {attr} {main} with {o1} and {o2}",
    "the {main} near the {o1} beside a {o2}",
    "{o1} scene showing a {attr} {main} by the {o2}",
    "close view of the {main} and the {o1} under {o2}",
]


def _tokens(caption: str) -> frozenset:
    return frozenset(caption.split())


# ── generators (the swappable seam: replace with real VLM calls) ─────────────
def base_model(image: dict, rng: random.Random) -> str:
    """High-entropy drafts: varied templates/objects, hallucinates ~35%."""
    o1, o2 = rng.sample(sorted(image["objects"] - {image["main"]}), 2)
    if rng.random() < 0.35:  # the paper's misalignment failure, reproduced
        o1 = rng.choice(DECOYS)
    tpl = rng.choice(TEMPLATES)
    return tpl.format(attr=image["attr"], main=image["main"], o1=o1, o2=o2)


def instruct_model(image: dict) -> str:
    """Mode collapse: always the same safe, generic (but correct) sentence."""
    return f"a photo of a {image['attr']} {image['main']}"


def refine(image: dict, draft: str) -> str:
    """Instruction-tuned refinement: replace any token not grounded in the
    image's facts with a true fact — never invents, never homogenizes."""
    grounded = image["objects"] | {image["attr"], image["main"]}
    glue = {"a", "the", "with", "and", "near", "beside", "by", "under", "scene",
            "showing", "close", "view", "of", "photo"}
    out = []
    for tok in draft.split():
        if tok in grounded or tok in glue:
            out.append(tok)
        else:  # hallucinated content word → swap for a real, still-varied fact
            replacement = sorted(image["objects"] - set(out) - {image["main"]})
            out.append(replacement[0] if replacement else image["main"])
    return " ".join(out)


# ── metrics ──────────────────────────────────────────────────────────────────
def alignment(image: dict, caption: str) -> float:
    """Mock-CLIP: fraction of content words grounded in the image's facts."""
    glue = {"a", "the", "with", "and", "near", "beside", "by", "under", "scene",
            "showing", "close", "view", "of", "photo"}
    content = [t for t in caption.split() if t not in glue]
    grounded = image["objects"] | {image["attr"], image["main"]}
    return sum(1 for t in content if t in grounded) / max(len(content), 1)


def diversity(captions: list[str]) -> float:
    """Mean pairwise Jaccard DISTANCE between caption token sets (0 = collapse)."""
    if len(captions) < 2:
        return 0.0
    dists = []
    for a, b in itertools.combinations(captions, 2):
        ta, tb = _tokens(a), _tokens(b)
        dists.append(1.0 - len(ta & tb) / len(ta | tb))
    return sum(dists) / len(dists)


GATES = {"alignment_floor": 0.95, "diversity_floor": 0.25}
PER_SAMPLE_ALIGNMENT = 0.80  # the CLIP-filter analog: below this, a pair is dropped


# ── the closed loop ──────────────────────────────────────────────────────────
def run_pipeline(mode: str, n_per_image: int = 4, seed: int = 0) -> dict:
    rng = random.Random(seed)
    per_image_captions, alignments, kept = [], [], 0
    total = 0
    for image in IMAGES:
        captions = []
        for _ in range(n_per_image):
            if mode == "base_only":
                cap = base_model(image, rng)
            elif mode == "instruct_only":
                cap = instruct_model(image)
            elif mode == "bare":
                cap = refine(image, base_model(image, rng))
            else:
                raise ValueError(f"unknown mode: {mode}")
            captions.append(cap)
            a = alignment(image, cap)
            alignments.append(a)
            total += 1
            if a >= PER_SAMPLE_ALIGNMENT:
                kept += 1
        per_image_captions.append(captions)
    mean_align = sum(alignments) / len(alignments)
    mean_div = sum(diversity(c) for c in per_image_captions) / len(per_image_captions)
    gate_reasons = []
    if mean_align < GATES["alignment_floor"]:
        gate_reasons.append(f"alignment {mean_align:.2f} < {GATES['alignment_floor']}")
    if mean_div < GATES["diversity_floor"]:
        gate_reasons.append(f"diversity {mean_div:.2f} < {GATES['diversity_floor']}")
    return {
        "mode": mode,
        "alignment": mean_align,
        "diversity": mean_div,
        "yield": kept / total,
        "gate_pass": not gate_reasons,
        "gate_reasons": gate_reasons,
    }


if __name__ == "__main__":
    rows = [run_pipeline(m) for m in ("base_only", "instruct_only", "bare")]
    print(f"{'pipeline':<14}{'alignment':>10}{'diversity':>10}{'yield':>8}  gate")
    for r in rows:
        verdict = "PASS" if r["gate_pass"] else "FAIL (" + "; ".join(r["gate_reasons"]) + ")"
        print(f"{r['mode']:<14}{r['alignment']:>10.2f}{r['diversity']:>10.2f}{r['yield']:>8.2f}  {verdict}")
    # honest exit: BARE must pass while both single-stage baselines fail
    bare, base, instr = rows[2], rows[0], rows[1]
    sys.exit(0 if (bare["gate_pass"] and not base["gate_pass"] and not instr["gate_pass"]) else 1)
