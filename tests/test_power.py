"""Arithmetic for the power tool, pinned against published reference values.

A statistics helper that is wrong is worse than none: it launders a guess into a
number with a decimal point. So every formula here is checked against a value
that exists outside this repo.
"""
from __future__ import annotations

import pytest

from power import (mde_two_proportions, n_for_mde, describe_rate, rule_of_three,
                   wilson)


# ── Wilson, against textbook values ──────────────────────────────────────────


def test_wilson_matches_the_published_worked_example():
    """50/100 → [0.404, 0.596] is the standard worked example."""
    lo, hi = wilson(50, 100)
    assert lo == pytest.approx(0.404, abs=0.001)
    assert hi == pytest.approx(0.596, abs=0.001)


def test_wilson_has_width_at_the_boundary_where_the_normal_interval_collapses():
    """THE REASON WILSON IS USED. The normal interval gives +/-0 at k=0, i.e.
    perfect certainty exactly where the evidence is thinnest."""
    lo, hi = wilson(0, 30)
    assert lo == 0.0
    assert hi > 0.10, "a zero count must still carry a real upper bound"


def test_wilson_is_symmetric_under_swapping_successes_and_failures():
    lo_a, hi_a = wilson(7, 40)
    lo_b, hi_b = wilson(33, 40)
    assert lo_a == pytest.approx(1 - hi_b)
    assert hi_a == pytest.approx(1 - lo_b)


def test_wilson_narrows_as_n_grows():
    wide = wilson(5, 10)
    narrow = wilson(500, 1000)
    assert (narrow[1] - narrow[0]) < (wide[1] - wide[0])


def test_wilson_rejects_an_empty_sample():
    with pytest.raises(ValueError):
        wilson(0, 0)


# ── rule of three ────────────────────────────────────────────────────────────


def test_rule_of_three_matches_the_canonical_example():
    """Hanley & Lippman-Hand's own example: 0 adverse events in 1500 subjects
    ⇒ fewer than 1 in 500."""
    assert rule_of_three(1500) == pytest.approx(1 / 500)


def test_rule_of_three_undefined_without_trials():
    assert rule_of_three(0) is None


def test_wilson_and_rule_of_three_broadly_agree_at_zero():
    """Two independent routes to the same bound should not disagree wildly."""
    _, hi = wilson(0, 100)
    assert hi == pytest.approx(rule_of_three(100), rel=0.35)


# ── minimum detectable difference ────────────────────────────────────────────


def test_mde_and_n_for_mde_are_inverses():
    n = n_for_mde(0.10)
    assert mde_two_proportions(n) == pytest.approx(0.10, abs=0.002)


def test_detecting_ten_points_needs_the_textbook_sample_size():
    """(1.96+0.8416)^2 * 2 * 0.25 / 0.01 ≈ 392 per arm — the standard answer."""
    assert n_for_mde(0.10) == 393


def test_a_difference_needs_far_more_n_than_a_rate():
    """The point of the whole tool: 288 runs pins a RATE to a few points, but
    only resolves a DIFFERENCE of ~12 points."""
    lo, hi = wilson(144, 288)
    assert (hi - lo) < 0.12
    assert mde_two_proportions(288) > 0.11


def test_mde_shrinks_with_sample_size():
    assert mde_two_proportions(1000) < mde_two_proportions(100)


def test_mde_rejects_an_empty_arm():
    with pytest.raises(ValueError):
        mde_two_proportions(0)


@pytest.mark.parametrize("bad", [0.0, 1.0, -0.1, 1.5])
def test_n_for_mde_rejects_impossible_differences(bad):
    with pytest.raises(ValueError):
        n_for_mde(bad)


# ── the human-readable line ──────────────────────────────────────────────────


def test_zero_events_are_described_as_a_bound_not_as_zero():
    line = describe_rate(0, 18, "base hallucination")
    assert "rule of three" in line
    assert "not a zero rate" in line
    assert "16.7%" in line


def test_a_normal_rate_reports_its_interval_and_width():
    line = describe_rate(196, 1152)
    assert "17.0%" in line and "95% CI" in line and "width" in line
