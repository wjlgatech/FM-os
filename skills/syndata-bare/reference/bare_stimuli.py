#!/usr/bin/env python3
"""Deterministic synthetic scenes with ground truth known BY CONSTRUCTION.

`bare_loop.py` proves the BARE thesis on toy text with a mock-CLIP. To measure
real models you need real images — and the hard part is not the generation, it
is knowing what is true about them without a judge.

Two design rules make that possible:

1. **Primitive attributes only.** Every scene is coloured geometric shapes in
   stated spatial relations. Colour and shape are not matters of opinion, so
   grounding can be checked exactly — no CLIP, no LLM judge, no human. The cost
   is stated plainly in the SKILL: this measures grounding of *primitive visual
   attributes*, a weaker proxy than natural-image captioning.

2. **Closed decoy sets.** Each scene carries the colours and shapes that are
   definitionally ABSENT. A caption is only scored wrong when it names one of
   those. A word that is neither a known fact nor a known decoy ("vibrant",
   "geometric", "background") is left UNSCORED — because the alternative is the
   synonym trap: a model that says "box" for "square" would be recorded as
   hallucinating, and the run would publish a failure the model never committed.

That asymmetry is deliberate and it is a limit, not an oversight: the alignment
score is an UPPER bound on grounding. We detect the hallucinations we enumerated
and no others.
"""
from __future__ import annotations

from PIL import Image, ImageDraw

W, H = 320, 240
BG = (250, 250, 250)

PALETTE = {
    "red": (220, 40, 40),
    "blue": (40, 80, 220),
    "green": (40, 160, 60),
    "yellow": (235, 200, 30),
    "purple": (140, 60, 180),
    "orange": (240, 130, 30),
}
ALL_COLORS = set(PALETTE)
ALL_SHAPES = {"circle", "square", "triangle"}

# Scenes: (id, [(color, shape, position)]) where position ∈ {left, right, top, bottom, center}
SCENES: list[dict] = [
    {"id": "s1_red_circle_blue_square",
     "objects": [("red", "circle", "left"), ("blue", "square", "right")]},
    {"id": "s2_green_triangle_alone",
     "objects": [("green", "triangle", "center")]},
    {"id": "s3_yellow_square_over_purple_circle",
     "objects": [("yellow", "square", "top"), ("purple", "circle", "bottom")]},
    {"id": "s4_three_orange_circles",
     "objects": [("orange", "circle", "left"), ("orange", "circle", "center"),
                 ("orange", "circle", "right")]},
    {"id": "s5_blue_triangle_green_square",
     "objects": [("blue", "triangle", "left"), ("green", "square", "right")]},
    {"id": "s6_purple_square_red_triangle_yellow_circle",
     "objects": [("purple", "square", "left"), ("red", "triangle", "center"),
                 ("yellow", "circle", "right")]},
]

_POS = {"left": (65, 120), "center": (160, 120), "right": (255, 120),
        "top": (160, 70), "bottom": (160, 175)}
_R = 42


def facts(scene: dict) -> dict:
    """Everything true about a scene, and everything definitionally absent."""
    colors = {c for c, _, _ in scene["objects"]}
    shapes = {s for _, s, _ in scene["objects"]}
    return {
        "colors": colors,
        "shapes": shapes,
        "count": len(scene["objects"]),
        "decoy_colors": ALL_COLORS - colors,
        "decoy_shapes": ALL_SHAPES - shapes,
    }


def _draw(d: ImageDraw.ImageDraw, color: str, shape: str, pos: str) -> None:
    cx, cy = _POS[pos]
    fill = PALETTE[color]
    if shape == "circle":
        d.ellipse([cx - _R, cy - _R, cx + _R, cy + _R], fill=fill)
    elif shape == "square":
        d.rectangle([cx - _R, cy - _R, cx + _R, cy + _R], fill=fill)
    elif shape == "triangle":
        d.polygon([(cx, cy - _R), (cx - _R, cy + _R), (cx + _R, cy + _R)], fill=fill)
    else:  # pragma: no cover — unreachable while SCENES is the only caller
        raise ValueError(f"unknown shape: {shape}")


def render(scene: dict) -> Image.Image:
    """Pixel-identical on every run: no randomness, no system fonts."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for color, shape, pos in scene["objects"]:
        _draw(d, color, shape, pos)
    return img


def by_id(scene_id: str) -> dict:
    for s in SCENES:
        if s["id"] == scene_id:
            return s
    raise KeyError(scene_id)


if __name__ == "__main__":  # pragma: no cover — visual smoke check
    import sys
    from pathlib import Path

    out = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/bare_stimuli")
    out.mkdir(parents=True, exist_ok=True)
    for s in SCENES:
        render(s).save(out / f"{s['id']}.png")
        print(f"{s['id']}: {facts(s)}")
    print(f"wrote {len(SCENES)} scenes to {out}")
