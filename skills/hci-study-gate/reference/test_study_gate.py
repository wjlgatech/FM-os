"""Gate math pinned to textbook values, plus every refusal path.

A power formula that silently drifts is worse than none: it would bless
underpowered studies with a number. So the arithmetic is checked against values a
reviewer can look up, not against whatever the code currently returns.
"""

import pytest

from study_gate import (CONFOUNDED, NOT_MEASURED, SUPPORTED, UNDERPOWERED, StudyDesign,
                        counterbalance_ok, gate, latin_square, report,
                        required_n_per_arm)


class TestPowerMath:
    def test_textbook_medium_effect_is_64_per_arm(self):
        """d=0.5, alpha=.05, power=.80 -> 64 per arm. The canonical value."""
        assert required_n_per_arm(0.5, 0.05, 0.80) == 64

    def test_conventional_large_and_small_effects(self):
        """G*Power values for the same alpha/power — not the normal approximation,
        which gives 25 and 393 (one short in each case)."""
        assert required_n_per_arm(0.8, 0.05, 0.80) == 26    # large effect
        assert required_n_per_arm(0.2, 0.05, 0.80) == 394   # small effect

    def test_more_power_costs_more_participants(self):
        assert (required_n_per_arm(0.5, 0.05, 0.90)
                > required_n_per_arm(0.5, 0.05, 0.80))

    def test_stricter_alpha_costs_more_participants(self):
        assert (required_n_per_arm(0.5, 0.01, 0.80)
                > required_n_per_arm(0.5, 0.05, 0.80))

    def test_n_scales_as_one_over_d_squared(self):
        """Halving the detectable effect should roughly quadruple N."""
        assert required_n_per_arm(0.25) == pytest.approx(
            4 * required_n_per_arm(0.5), rel=0.02)

    def test_vague_expectations_are_rejected_not_defaulted(self):
        with pytest.raises(ValueError, match="effect_size"):
            required_n_per_arm(0.0)
        with pytest.raises(ValueError):
            required_n_per_arm(0.5, alpha=0.42)


class TestCounterbalance:
    def test_latin_square_is_balanced(self):
        ok, note = counterbalance_ok(StudyDesign(
            name="x", within_subjects=True,
            condition_orders=latin_square(["a", "b", "c"])))
        assert ok, note

    def test_everyone_sees_the_ai_second_is_confounded(self):
        ok, note = counterbalance_ok(StudyDesign(
            name="x", within_subjects=True, condition_orders=[("baseline", "agent")]))
        assert not ok and "imbalanced" in note

    def test_within_subjects_without_declared_orders_is_refused(self):
        ok, note = counterbalance_ok(StudyDesign(name="x", within_subjects=True))
        assert not ok and "no condition_orders" in note

    def test_between_subjects_is_exempt(self):
        ok, note = counterbalance_ok(StudyDesign(name="x", within_subjects=False))
        assert ok and "not applicable" in note

    def test_inconsistent_order_sets_are_caught(self):
        ok, _ = counterbalance_ok(StudyDesign(
            name="x", within_subjects=True, condition_orders=[("a", "b"), ("a", "b", "c")]))
        assert not ok


class TestGate:
    def _sound(self, **kw):
        base = dict(name="s", primary_metric="task_success_rate", effect_size=0.5,
                    planned_n_per_arm=64)
        base.update(kw)
        return StudyDesign(**base)

    def test_sound_design_is_supported(self):
        r = gate(self._sound())
        assert r["verdict"] == SUPPORTED and r["required_n_per_arm"] == 64

    def test_n12_is_refused_with_the_number_it_needed(self):
        r = gate(self._sound(planned_n_per_arm=12))
        assert r["verdict"] == UNDERPOWERED
        assert "12/arm planned, 64/arm needed" in r["reasons"][0]

    def test_order_confound_beats_power_in_the_verdict(self):
        """Even a well-powered study is void if order confounds the condition."""
        r = gate(self._sound(within_subjects=True,
                             condition_orders=[("baseline", "agent")]))
        assert r["verdict"] == CONFOUNDED

    def test_missing_pre_registration_is_not_measured_not_a_guess(self):
        for missing in ({"primary_metric": None}, {"effect_size": None},
                        {"planned_n_per_arm": None}):
            r = gate(self._sound(**missing))
            assert r["verdict"] == NOT_MEASURED, missing
            assert "incomplete" in r["reasons"][0]

    def test_an_empty_design_never_passes(self):
        assert gate(StudyDesign(name="we'll see"))["verdict"] == NOT_MEASURED

    def test_secondary_metrics_are_labelled_exploratory(self):
        d = self._sound(secondary_metrics=["trust", "time", "nps"])
        r = gate(d)
        assert r["exploratory"] == ["trust", "time", "nps"]
        assert "cannot carry the headline" in report(d, r)

    def test_report_shows_the_arithmetic_not_just_a_verdict(self):
        d = self._sound(planned_n_per_arm=20)
        out = report(d, gate(d))
        assert "required 64" in out and "UNDERPOWERED" in out
