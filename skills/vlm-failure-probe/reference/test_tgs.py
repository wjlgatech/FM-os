"""Gate math for the Temporal Grounding Score, checked against HAND computation.

A custom metric earns trust by having its arithmetic pinned to numbers a reviewer
can verify with a pencil — not by having code that runs. Every expected value
below is written as the explicit fraction it comes from.
"""

import pytest

from probe_runner import MockVSS, PatchedVSS, load_spec, run_probes
from tgs import compute_tgs, gate_tgs, load_tgs_spec, tgs_report

SPEC = load_spec()
TSPEC = load_tgs_spec()

# the probes each component averages, per tgs_spec.yml
ORDER = ("squares_race", "forklift_fork_direction")
ANCHOR = ("sport_stays_tennis", "end_of_video")
PERSIST = ("warehouse_no_fall", "shirt_stays_white")
ALL_TGS_PROBES = ORDER + ANCHOR + PERSIST


def _results_from(scores: dict[str, float | None]) -> dict:
    """A minimal run_probes()-shaped payload for exact-arithmetic fixtures."""
    return {
        "synthetic": {
            "measured": True,
            "score": None,
            "threshold": 0.0,
            "probes": [{"id": pid, "answer": "x", "score": s} for pid, s in scores.items()],
        }
    }


def test_perfect_and_zero_are_the_endpoints():
    perfect = compute_tgs(_results_from({p: 1.0 for p in ALL_TGS_PROBES}), TSPEC)
    assert perfect["tgs"] == 1.0 and perfect["measured"]
    zero = compute_tgs(_results_from({p: 0.0 for p in ALL_TGS_PROBES}), TSPEC)
    assert zero["tgs"] == 0.0 and zero["measured"]


def test_hand_computed_mixed_case():
    """order = (1.0 + 0.0)/2 = 0.5 · anchor = (1.0 + 1.0)/2 = 1.0
    persistence = (1.0 + 0.0)/2 = 0.5
    TGS = (1·0.5 + 1·1.0 + 1·0.5) / 3 = 2.0/3 = 0.6667"""
    r = compute_tgs(
        _results_from(
            {
                "squares_race": 1.0,
                "forklift_fork_direction": 0.0,
                "sport_stays_tennis": 1.0,
                "end_of_video": 1.0,
                "warehouse_no_fall": 1.0,
                "shirt_stays_white": 0.0,
            }
        ),
        TSPEC,
    )
    assert r["components"]["order"]["score"] == pytest.approx(0.5)
    assert r["components"]["anchor"]["score"] == pytest.approx(1.0)
    assert r["components"]["persistence"]["score"] == pytest.approx(0.5)
    assert r["tgs"] == pytest.approx(2.0 / 3.0)
    ok, reasons = gate_tgs(r, TSPEC)
    assert not ok and "0.667" in reasons[0]  # 0.667 < floor 0.75


def test_weights_renormalize_and_are_honoured():
    """A weight change must move the number — otherwise the weights are decoration.
    With order weighted 3 and the others 1: (3·0.0 + 1·1.0 + 1·1.0)/5 = 0.4"""
    spec = {
        **TSPEC,
        "require_all_components": False,
        "components": [
            {**c, "weight": 3.0 if c["id"] == "order" else 1.0} for c in TSPEC["components"]
        ],
    }
    r = compute_tgs(
        _results_from(
            {
                "squares_race": 0.0,
                "forklift_fork_direction": 0.0,
                "sport_stays_tennis": 1.0,
                "end_of_video": 1.0,
                "warehouse_no_fall": 1.0,
                "shirt_stays_white": 1.0,
            }
        ),
        spec,
    )
    assert r["weight_total"] == pytest.approx(5.0)
    assert r["tgs"] == pytest.approx(0.4)


def test_unmeasured_component_is_excluded_not_zeroed():
    """The no-evidence⇒No core. With `require_all_components: false`, an unmeasured
    ORDER component must be dropped and the rest renormalized:
        TGS = (1·1.0 + 1·1.0)/2 = 1.0  — NOT (0 + 1 + 1)/3 = 0.667 (fake failure)
    """
    spec = {**TSPEC, "require_all_components": False}
    r = compute_tgs(
        _results_from(
            {
                "squares_race": None,
                "forklift_fork_direction": None,
                "sport_stays_tennis": 1.0,
                "end_of_video": 1.0,
                "warehouse_no_fall": 1.0,
                "shirt_stays_white": 1.0,
            }
        ),
        spec,
    )
    assert r["components"]["order"]["measured"] is False
    assert r["components"]["order"]["score"] is None  # excluded, never zeroed
    assert r["unmeasured"] == ["order"]
    assert r["weight_total"] == pytest.approx(2.0)
    assert r["tgs"] == pytest.approx(1.0)


def test_required_component_unmeasured_makes_tgs_undefined_and_ungateable():
    """The shipped spec requires all three: a missing one CANNOT be papered over."""
    assert TSPEC["require_all_components"] is True
    r = compute_tgs(
        _results_from(
            {
                "squares_race": None,
                "forklift_fork_direction": None,
                "sport_stays_tennis": 1.0,
                "end_of_video": 1.0,
                "warehouse_no_fall": 1.0,
                "shirt_stays_white": 1.0,
            }
        ),
        TSPEC,
    )
    assert r["tgs"] is None and r["measured"] is False
    ok, reasons = gate_tgs(r, TSPEC)
    assert not ok and "NOT MEASURED" in reasons[0]
    # and a perfect score on everything else must NOT rescue it
    assert "order" in reasons[0]


def test_partially_measured_component_averages_only_what_exists():
    """order: one item measured at 1.0, one unmeasured ⇒ order = 1.0/1, not 0.5."""
    r = compute_tgs(
        _results_from(
            {
                "squares_race": 1.0,
                "forklift_fork_direction": None,
                "sport_stays_tennis": 1.0,
                "end_of_video": 1.0,
                "warehouse_no_fall": 1.0,
                "shirt_stays_white": 1.0,
            }
        ),
        TSPEC,
    )
    o = r["components"]["order"]
    assert o["measured"] and o["score"] == pytest.approx(1.0)
    assert o["n_measured"] == 1 and o["n_items"] == 2
    assert o["unmeasured_items"] == ["forklift_fork_direction"]
    assert r["tgs"] == pytest.approx(1.0)


def test_spec_drift_raises_instead_of_silently_averaging_fewer_items():
    bad = {**TSPEC, "components": [{**TSPEC["components"][0], "items": [{"probe": "ghost_probe"}]}]}
    with pytest.raises(KeyError, match="ghost_probe"):
        compute_tgs(_results_from({p: 1.0 for p in ALL_TGS_PROBES}), bad)


def test_every_referenced_probe_exists_in_the_probe_spec():
    """tgs_spec and probe_spec must not drift apart (spec-as-data, one source)."""
    known = {p["id"] for m in SPEC["failure_modes"] for p in m["probes"]}
    for comp in TSPEC["components"]:
        for item in comp["items"]:
            assert item["probe"] in known, f"{comp['id']} → {item['probe']}"


def test_paper_baseline_fails_tgs_and_a_grounded_model_passes():
    """End-to-end teeth: the VSS paper's OBSERVED failures must fail this metric,
    and a grounded model must clear it — otherwise the metric measures nothing."""
    base = compute_tgs(run_probes(MockVSS(), SPEC), TSPEC)
    ok, _ = gate_tgs(base, TSPEC)
    assert base["tgs"] == pytest.approx(0.0)  # every temporal probe wrong
    assert not ok

    good = compute_tgs(run_probes(PatchedVSS(), SPEC), TSPEC)
    ok, reasons = gate_tgs(good, TSPEC)
    assert good["tgs"] == pytest.approx(1.0)
    assert ok, reasons


def test_report_shows_the_derivation_not_just_a_number():
    r = compute_tgs(run_probes(PatchedVSS(), SPEC), TSPEC)
    out = tgs_report("patched", r, TSPEC)
    for comp in TSPEC["components"]:
        assert comp["id"] in out and comp["paper_clause"] in out
    assert "TGS = 1.000" in out and "floor 0.75" in out
