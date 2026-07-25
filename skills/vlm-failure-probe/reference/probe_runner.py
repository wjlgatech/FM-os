#!/usr/bin/env python3
"""Turn a VLM failure taxonomy (probe_spec.yml) into a gated probe suite.

The spec is the single source of truth: each failure mode carries its probes,
ground truth, matcher, and threshold. The runner scores ANY model exposed as
`answer(probe) -> str | None` and gates with the FM-os Certified discipline:
no evidence ⇒ No — an unanswered mode is "not measured", never a pass, and a
blocking gate cannot pass while a mode is unmeasured.

Seeded from the VSS failure-benchmarking case study (research-anything): the
bundled MockVSS reproduces the paper's observed failures verbatim, so the
suite demonstrably catches every category before you point it at a real
pipeline (VSS API, a fine-tuned VLM, or a post-vDPO checkpoint).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SPEC_PATH = Path(__file__).parent / "probe_spec.yml"


def load_spec(path: Path = SPEC_PATH) -> dict:
    return yaml.safe_load(path.read_text())


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


# ── matchers: probe score in [0, 1] ──────────────────────────────────────────
def score_probe(answer: str, probe: dict) -> float:
    ans = _norm(answer)
    expect = [_norm(e) for e in probe["expect"]]
    kind = probe["match"]
    if kind == "contains":
        return 1.0 if all(e in ans for e in expect) else 0.0
    if kind == "order":  # every item present AND in the stated order
        pos = [ans.find(e) for e in expect]
        return 1.0 if all(p >= 0 for p in pos) and pos == sorted(pos) else 0.0
    if kind == "all_parts":  # graded: fraction of sub-answers present
        return sum(1.0 for e in expect if e in ans) / len(expect)
    raise ValueError(f"unknown matcher: {kind}")


# ── runner ───────────────────────────────────────────────────────────────────
def run_probes(model, spec: dict) -> dict:
    """model: callable(probe: dict) -> str | None (None = could not measure)."""
    results = {}
    for mode in spec["failure_modes"]:
        probes = []
        for probe in mode["probes"]:
            answer = model(probe)
            probes.append(
                {
                    "id": probe["id"],
                    "answer": answer,
                    "score": None if answer is None else score_probe(answer, probe),
                }
            )
        scored = [p["score"] for p in probes if p["score"] is not None]
        results[mode["id"]] = {
            "measured": bool(scored),
            "score": (sum(scored) / len(scored)) if scored else None,
            "threshold": mode["threshold"],
            "probes": probes,
        }
    return results


def gate(results: dict, spec: dict) -> tuple[bool, list[str]]:
    """Blocking gate: fails on any measured mode below threshold, and cannot
    pass while a mode is unmeasured (when the spec requires measurement)."""
    reasons = []
    for mode_id, r in results.items():
        if not r["measured"]:
            if spec.get("require_measured", True):
                reasons.append(f"{mode_id}: NOT MEASURED (no evidence ⇒ no pass)")
            continue
        if r["score"] < r["threshold"]:
            reasons.append(f"{mode_id}: {r['score']:.2f} < threshold {r['threshold']:.2f}")
    return (not reasons), reasons


# ── model adapters: the paper's failures, reproduced ─────────────────────────
class MockVSS:
    """Answers exactly as the VSS paper reports the real system failing."""

    ANSWERS = {
        "squares_race": "The blue square crosses the finish line first.",
        "squares_stack": "From top to bottom: red, blue, green, yellow.",  # bottom-up reversal
        "snowboarders_left": "The snowboarder in the blue jacket is on the left.",
        "circled_letter": "The letter T is circled.",
        "warehouse_no_fall": "Yes — the person falls and then gets back up.",  # fabricated event
        "sport_stays_tennis": "Midway through, the game switches to padel.",
        "shirt_stays_white": "The person wears a blue shirt and has a beard.",  # attribute drift
        "summary_count_clothing": "The man is wearing a yellow vest.",  # last part only
        "describe_and_closer": "The player in white is closer to the camera.",
        "forklift_fork_direction": "The warehouse is busy with workers moving boxes.",  # generic
        "end_of_video": "A worker stacks pallets near the entrance.",  # earlier scene
        "floor_color": "The floor is blue and red.",  # hallucinated attribute
    }

    def __call__(self, probe: dict) -> str:
        return self.ANSWERS[probe["id"]]


class PatchedVSS:
    """A model that actually grounds its answers — what a mitigation must reach."""

    ANSWERS = {
        "squares_race": "The red square crosses the finish line first.",
        "squares_stack": "From top to bottom: yellow, green, blue, red.",
        "snowboarders_left": "The snowboarder in the orange jacket is on the left.",
        "circled_letter": "The letter H is circled.",
        "warehouse_no_fall": "No — the person bends down but never falls.",
        "sport_stays_tennis": "Tennis is played for the entire video.",
        "shirt_stays_white": "The person wears a white shirt throughout.",
        "summary_count_clothing": (
            "Summary: a single worker moves boxes in a warehouse. "
            "There is one person present. The person is wearing a yellow vest."
        ),
        "describe_and_closer": (
            "Two players exchange shots in a rally; the player in white is closer to the camera."
        ),
        "forklift_fork_direction": "The forklift's fork is moving up.",
        "end_of_video": "At the very end, the truck leaves the loading dock.",
        "floor_color": "The floor is plain concrete.",
    }

    def __call__(self, probe: dict) -> str:
        return self.ANSWERS[probe["id"]]


def scorecard(name: str, results: dict, spec: dict) -> str:
    ok, reasons = gate(results, spec)
    lines = [f"── {name} ──"]
    for mode_id, r in results.items():
        shown = "not measured" if not r["measured"] else f"{r['score']:.2f}"
        verdict = "—" if not r["measured"] else ("PASS" if r["score"] >= r["threshold"] else "FAIL")
        lines.append(f"  {mode_id:<24} {shown:>12}  (min {r['threshold']:.2f})  {verdict}")
    lines.append(f"  gate: {'PASS' if ok else 'FAIL — ' + '; '.join(reasons)}")
    return "\n".join(lines)


if __name__ == "__main__":
    spec = load_spec()
    baseline = run_probes(MockVSS(), spec)
    patched = run_probes(PatchedVSS(), spec)
    print(scorecard("baseline (paper's observed VSS failures)", baseline, spec))
    print(scorecard("patched (what a mitigation must reach)", patched, spec))
    ok, _ = gate(patched, spec)
    baseline_ok, _ = gate(baseline, spec)
    # honest exit: the harness must catch the baseline AND pass the patched model
    sys.exit(0 if (ok and not baseline_ok) else 1)
