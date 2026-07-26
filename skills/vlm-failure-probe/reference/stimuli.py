#!/usr/bin/env python3
"""Deterministic synthetic stimuli for every probe in probe_spec.yml.

The VSS paper built its spatial tests synthetically (colored squares racing,
stacked squares, a circled letter); this module regenerates that methodology
as code so the benchmark SHIPS WITH its stimuli: `generate(probe_id)` returns
an ordered list of PIL frames, pixel-identical on every run (no randomness,
no fonts drawn from system state — letters are vector strokes). Real footage
probes (snowboarders, tennis, warehouse) get simple 2D proxies that preserve
the ground truth the probe grades on.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 320, 240
WHITE, BLACK, GRAY = (255, 255, 255), (20, 20, 20), (150, 150, 150)
RED, BLUE, GREEN, YELLOW = (220, 40, 40), (40, 80, 220), (40, 160, 60), (235, 200, 30)
ORANGE, SKIN, CONCRETE = (240, 130, 30), (230, 190, 160), (168, 168, 168)


def _canvas(bg=WHITE):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def _person(d, x, y, shirt, bend=0.0, vest=None, scale=1.0):
    """Stick figure: head + shirt torso + legs. bend tilts the torso forward."""
    s = scale
    head_r, torso = int(9 * s), int(34 * s)
    dx = int(bend * torso)  # forward lean of the shoulders
    hx, hy = x + dx, y - torso - int(bend * 6 * s)
    d.ellipse([hx - head_r, hy - 2 * head_r, hx + head_r, hy], fill=SKIN, outline=BLACK)
    d.line([x, y, hx, hy], fill=BLACK, width=int(10 * s))  # torso line
    color = vest or shirt
    d.rectangle([min(x, hx) - int(7 * s), hy, max(x, hx) + int(7 * s), y - int(10 * s)], fill=color, outline=BLACK)
    d.line([x, y, x - int(8 * s), y + int(26 * s)], fill=BLUE, width=int(6 * s))
    d.line([x, y, x + int(8 * s), y + int(26 * s)], fill=BLUE, width=int(6 * s))


# vector strokes for the letters of TECHNOLOGY (no system fonts → deterministic)
_STROKES = {
    "T": [(0, 0, 1, 0), (0.5, 0, 0.5, 1)],
    "E": [(0, 0, 0, 1), (0, 0, 1, 0), (0, 0.5, 0.8, 0.5), (0, 1, 1, 1)],
    "C": [(1, 0, 0, 0), (0, 0, 0, 1), (0, 1, 1, 1)],
    "H": [(0, 0, 0, 1), (1, 0, 1, 1), (0, 0.5, 1, 0.5)],
    "N": [(0, 1, 0, 0), (0, 0, 1, 1), (1, 1, 1, 0)],
    "O": [(0, 0, 1, 0), (1, 0, 1, 1), (1, 1, 0, 1), (0, 1, 0, 0)],
    "L": [(0, 0, 0, 1), (0, 1, 1, 1)],
    "G": [(1, 0, 0, 0), (0, 0, 0, 1), (0, 1, 1, 1), (1, 1, 1, 0.5), (0.55, 0.5, 1, 0.5)],
    "Y": [(0, 0, 0.5, 0.5), (1, 0, 0.5, 0.5), (0.5, 0.5, 0.5, 1)],
}


def _letter(d, ch, x, y, w=18, h=26):
    for x0, y0, x1, y1 in _STROKES[ch]:
        d.line([x + x0 * w, y + y0 * h, x + x1 * w, y + y1 * h], fill=BLACK, width=3)


def _tennis_scene(ball_t: float, near_shirt=WHITE, far_shirt=RED):
    img, d = _canvas((70, 130, 80))  # court green
    d.rectangle([30, 30, W - 30, H - 20], outline=WHITE, width=3)
    d.rectangle([10, H // 2 - 4, W - 10, H // 2 + 4], fill=(230, 230, 230))  # net
    _person(d, 110, 78, far_shirt, scale=0.7)  # far player: small, above the net
    _person(d, 200, 205, near_shirt, scale=1.3)  # near player: large, below the net
    d.line([90, 60, 100, 75], fill=BLACK, width=3)
    d.line([222, 165, 236, 150], fill=BLACK, width=4)  # rackets
    by = 75 + ball_t * 110
    d.ellipse([160 - 5, by - 5, 160 + 5, by + 5], fill=YELLOW, outline=BLACK)
    return img


def _warehouse(d):
    d.rectangle([0, 150, W, H], fill=CONCRETE)  # concrete floor
    d.rectangle([0, 0, W, 150], fill=(215, 215, 210))
    for bx in (20, 60, 250):
        d.rectangle([bx, 118, bx + 34, 152], fill=(160, 110, 60), outline=BLACK)


# ── one generator per probe id ───────────────────────────────────────────────
def squares_race(n=12):
    frames = []
    speeds = {RED: 23, BLUE: 14, GREEN: 11, YELLOW: 8}  # red wins, clearly
    for t in range(n):
        img, d = _canvas()
        for i in range(6):  # dashed finish line
            d.line([272, i * 40, 272, i * 40 + 22], fill=BLACK, width=3)
        for lane, color in enumerate((RED, BLUE, GREEN, YELLOW)):
            x = 8 + speeds[color] * t
            y = 22 + lane * 54
            d.rectangle([x, y, x + 30, y + 30], fill=color, outline=BLACK)
        frames.append(img)
    return frames


def squares_stack(n=4):
    img, d = _canvas()
    for i, color in enumerate((YELLOW, GREEN, BLUE, RED)):  # top → bottom
        y = 18 + i * 52
        d.rectangle([135, y, 185, y + 50], fill=color, outline=BLACK)
    return [img.copy() for _ in range(n)]


def snowboarders_left(n=4):
    frames = []
    for t in range(n):
        img, d = _canvas((170, 200, 235))  # sky
        d.polygon([(0, 90), (W, 200), (W, H), (0, H)], fill=WHITE)  # slope
        _person(d, 90 + t * 4, 150 + t * 3, ORANGE)   # LEFT: orange jacket
        _person(d, 230 + t * 4, 190 + t * 3, BLUE)    # right: blue jacket
        d.line([70, 180 + t * 3, 115, 172 + t * 3], fill=BLACK, width=5)
        d.line([210, 220 + t * 3, 255, 212 + t * 3], fill=BLACK, width=5)
        frames.append(img)
    return frames


def circled_letter(n=12):
    word = "TECHNOLOGY"
    frames = []
    x0, y0, step = 22, 105, 28
    for t in range(n):
        img, d = _canvas()
        shown = min(len(word), t + 1)
        for i in range(shown):
            _letter(d, word[i], x0 + i * step, y0)
        if t >= len(word):  # final frames: circle the H (index 3)
            cx = x0 + 3 * step + 9
            d.ellipse([cx - 17, y0 - 12, cx + 17, y0 + 38], outline=RED, width=3)
        frames.append(img)
    return frames


def warehouse_no_fall(n=10):
    # stand → bend to pick a box → stand again; the person is NEVER horizontal
    bends = [0.0, 0.15, 0.35, 0.55, 0.65, 0.65, 0.5, 0.3, 0.1, 0.0]
    frames = []
    for t in range(n):
        img, d = _canvas()
        _warehouse(d)
        _person(d, 160, 150, (90, 90, 200), bend=bends[t])
        frames.append(img)
    return frames


def sport_stays_tennis(n=10):
    return [_tennis_scene(abs((t % 8) - 4) / 4.0) for t in range(n)]


def shirt_stays_white(n=9):
    # three simulated "chunks" (wall tone shifts); the shirt is white in ALL of them
    frames = []
    for t in range(n):
        wall = [(225, 222, 214), (208, 214, 222), (218, 208, 220)][t // 3]
        img, d = _canvas(wall)
        d.rectangle([0, 190, W, H], fill=CONCRETE)
        _person(d, 150 + 6 * t, 190, WHITE)
        frames.append(img)
    return frames


def summary_count_clothing(n=6):
    frames = []
    for t in range(n):
        img, d = _canvas()
        _warehouse(d)
        _person(d, 120 + 10 * t, 150, WHITE, vest=YELLOW)  # ONE person, yellow vest
        frames.append(img)
    return frames


def describe_and_closer(n=8):
    return [_tennis_scene(abs((t % 6) - 3) / 3.0, near_shirt=WHITE, far_shirt=RED) for t in range(n)]


def forklift_fork_direction(n=8):
    frames = []
    for t in range(n):
        img, d = _canvas()
        _warehouse(d)
        d.rectangle([90, 105, 175, 150], fill=ORANGE, outline=BLACK)  # body
        d.ellipse([95, 140, 120, 165], fill=BLACK)
        d.ellipse([150, 140, 175, 165], fill=BLACK)  # wheels
        d.line([185, 40, 185, 150], fill=BLACK, width=5)  # mast
        fy = 140 - t * 12  # the fork RISES
        d.line([185, fy, 235, fy], fill=BLACK, width=6)
        d.rectangle([190, fy - 18, 228, fy - 2], fill=(160, 110, 60), outline=BLACK)
        frames.append(img)
    return frames


def end_of_video(n=10):
    frames = []
    for t in range(n):
        img, d = _canvas((200, 205, 210))
        d.rectangle([0, 160, W, H], fill=(90, 90, 95))  # road
        d.rectangle([0, 40, 70, 160], fill=(180, 170, 150), outline=BLACK)  # dock
        tx = 60 + t * 30  # the truck drives right and EXITS the frame
        d.rectangle([tx, 100, tx + 90, 155], fill=(60, 100, 160), outline=BLACK)
        d.rectangle([tx + 90, 118, tx + 120, 155], fill=(50, 60, 70), outline=BLACK)
        for wx in (tx + 15, tx + 65, tx + 100):
            d.ellipse([wx, 148, wx + 20, 168], fill=BLACK)
        frames.append(img)
    return frames


def floor_color(n=4):
    img, d = _canvas()
    _warehouse(d)  # concrete-gray floor, nothing blue or red on it
    return [img.copy() for _ in range(n)]


GENERATORS = {
    "squares_race": squares_race,
    "squares_stack": squares_stack,
    "snowboarders_left": snowboarders_left,
    "circled_letter": circled_letter,
    "warehouse_no_fall": warehouse_no_fall,
    "sport_stays_tennis": sport_stays_tennis,
    "shirt_stays_white": shirt_stays_white,
    "summary_count_clothing": summary_count_clothing,
    "describe_and_closer": describe_and_closer,
    "forklift_fork_direction": forklift_fork_direction,
    "end_of_video": end_of_video,
    "floor_color": floor_color,
}


def generate(probe_id: str) -> list:
    return GENERATORS[probe_id]()


def manifest() -> dict:
    """probe_id -> sha256 over all frame bytes (the determinism contract)."""
    out = {}
    for pid in sorted(GENERATORS):
        h = hashlib.sha256()
        for frame in generate(pid):
            h.update(frame.tobytes())
        out[pid] = h.hexdigest()[:16]
    return out


def save_all(outdir: Path) -> None:
    for pid in sorted(GENERATORS):
        d = outdir / pid
        d.mkdir(parents=True, exist_ok=True)
        for i, frame in enumerate(generate(pid)):
            frame.save(d / f"frame_{i:02d}.png")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "out" / "stimuli"
    save_all(out)
    for pid, sha in manifest().items():
        print(f"{sha}  {pid}")
    print(f"saved to {out}")
