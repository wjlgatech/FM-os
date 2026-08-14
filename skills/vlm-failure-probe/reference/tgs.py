#!/usr/bin/env python3
"""Temporal Grounding Score — the VSS paper's named-but-undefined metric, defined.

The paper (§X) names a "Temporal Grounding Score" and reports results against it
in a §XI that is still TODO. A metric with no formula cannot be reproduced or
checked, so this module supplies one: the formula, its weights, its degenerate
cases, and its gate — with the definition living in `tgs_spec.yml` (data) and the
arithmetic unit-tested against hand computation in `test_tgs.py`.

    TGS = ( Σ_c w_c · s_c ) / ( Σ_c w_c )   over MEASURED components c

Discipline (FM-os Certified / BRACE), identical to the probe gate:
  · an unmeasured component is EXCLUDED and the weights renormalize — never
    zeroed (a fake failure) and never assumed (a fake pass);
  · if the spec requires all components and one is unmeasured, TGS is None and
    the gate cannot pass on it;
  · a component whose items are all unmeasured is itself unmeasured.

Usage:
    from tgs import load_tgs_spec, compute_tgs, gate_tgs
    tgs = compute_tgs(probe_results, load_tgs_spec())   # probe_results from run_probes
"""
from __future__ import annotations

from pathlib import Path

import yaml

TGS_SPEC_PATH = Path(__file__).parent / "tgs_spec.yml"


def load_tgs_spec(path: Path = TGS_SPEC_PATH) -> dict:
    return yaml.safe_load(path.read_text())


def _probe_scores(probe_results: dict) -> dict[str, float | None]:
    """Flatten run_probes() output to {probe_id: score|None}."""
    return {
        p["id"]: p["score"]
        for mode in probe_results.values()
        for p in mode["probes"]
    }


def compute_tgs(probe_results: dict, spec: dict) -> dict:
    """Return the full derivation, not just a number — a bare score is unauditable.

    {"tgs": float|None, "measured": bool, "components": {id: {...}},
     "unmeasured": [component ids], "weight_total": float}
    """
    scores = _probe_scores(probe_results)
    components: dict[str, dict] = {}
    unmeasured: list[str] = []

    for comp in spec["components"]:
        item_scores, missing = [], []
        for item in comp["items"]:
            pid = item["probe"]
            if pid not in scores:
                # spec drift: a component references a probe that no longer exists.
                # Loud, not silent — a metric quietly averaging fewer items than it
                # claims is exactly the failure this whole file exists to prevent.
                raise KeyError(f"tgs_spec references unknown probe: {pid}")
            if scores[pid] is None:
                missing.append(pid)
            else:
                item_scores.append(scores[pid])
        measured = bool(item_scores)
        components[comp["id"]] = {
            "measured": measured,
            "score": (sum(item_scores) / len(item_scores)) if measured else None,
            "weight": comp["weight"],
            "n_items": len(comp["items"]),
            "n_measured": len(item_scores),
            "unmeasured_items": missing,
        }
        if not measured:
            unmeasured.append(comp["id"])

    if spec.get("require_all_components") and unmeasured:
        return {
            "tgs": None,
            "measured": False,
            "components": components,
            "unmeasured": unmeasured,
            "weight_total": 0.0,
        }

    live = [(c["weight"], c["score"]) for c in components.values() if c["measured"]]
    w_total = sum(w for w, _ in live)
    if not live or w_total <= 0:
        return {
            "tgs": None,
            "measured": False,
            "components": components,
            "unmeasured": unmeasured,
            "weight_total": 0.0,
        }
    return {
        "tgs": sum(w * s for w, s in live) / w_total,  # renormalized: no fake pass/fail
        "measured": True,
        "components": components,
        "unmeasured": unmeasured,
        "weight_total": w_total,
    }


def gate_tgs(tgs_result: dict, spec: dict) -> tuple[bool, list[str]]:
    """Blocking gate. Cannot pass on an unmeasured TGS (no evidence ⇒ No)."""
    floor = spec["floor"]
    if not tgs_result["measured"]:
        missing = ", ".join(tgs_result["unmeasured"]) or "all components"
        return False, [f"TGS NOT MEASURED ({missing}) — cannot pass"]
    if tgs_result["tgs"] < floor:
        return False, [f"TGS {tgs_result['tgs']:.3f} < floor {floor:.2f}"]
    return True, []


def tgs_report(name: str, tgs_result: dict, spec: dict) -> str:
    """Human-readable derivation: every component, weight, and the arithmetic."""
    ok, reasons = gate_tgs(tgs_result, spec)
    lines = [f"── Temporal Grounding Score · {name} (tgs_spec v{spec['version']}) ──"]
    for comp in spec["components"]:
        c = tgs_result["components"][comp["id"]]
        shown = "not measured" if not c["measured"] else f"{c['score']:.3f}"
        lines.append(
            f"  {comp['id']:<12} w={c['weight']:<4} {shown:>12}"
            f"   ({c['n_measured']}/{c['n_items']} items)  [{comp['paper_clause']}]"
        )
    total = "undefined" if tgs_result["tgs"] is None else f"{tgs_result['tgs']:.3f}"
    lines.append(f"  TGS = {total}   (floor {spec['floor']:.2f})")
    lines.append(f"  gate: {'PASS' if ok else 'FAIL — ' + '; '.join(reasons)}")
    return "\n".join(lines)


if __name__ == "__main__":
    from probe_runner import MockVSS, PatchedVSS, load_spec, run_probes

    spec, tspec = load_spec(), load_tgs_spec()
    for name, model in (("VSS baseline (paper's observed failures)", MockVSS()), ("patched", PatchedVSS())):
        print(tgs_report(name, compute_tgs(run_probes(model, spec), tspec), tspec))
