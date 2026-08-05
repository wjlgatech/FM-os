"""Every verdict path, plus the arithmetic, pinned.

A transfer gate that only ever says TRANSFERS is a rubber stamp. So each of the four
verdicts is tested with a case that must produce it, and the two that look like
successes (source-side gains) are tested to make sure they do NOT.
"""

import pytest

from transfer import (LOCAL_ONLY, NEGATIVE, NOT_MEASURED, TRANSFERS, Lesson, evaluate,
                      report)

BASE = {"eng-a": 0.60, "eng-b": 0.55, "eng-c": 0.58, "eng-d": 0.62}


def L(**kw):
    d = dict(name="l", source="eng-a", metric="task_success", direction="up",
             min_effect=0.05, predicted_before=True)
    d.update(kw)
    return Lesson(**d)


class TestVerdicts:
    def test_a_real_transfer_is_promoted(self):
        t = {"eng-a": 0.72, "eng-b": 0.64, "eng-c": 0.66, "eng-d": 0.70}
        r = evaluate(L(), BASE, t)
        assert r["verdict"] == TRANSFERS and r["promote"] is True

    def test_a_source_only_win_is_local_not_a_default(self):
        """The dangerous case: a big source gain and nothing elsewhere."""
        t = {"eng-a": 0.78, "eng-b": 0.555, "eng-c": 0.585, "eng-d": 0.625}
        r = evaluate(L(), BASE, t)
        assert r["verdict"] == LOCAL_ONLY and r["promote"] is False
        assert "fitted to where it was found" in r["reasons"][0]

    def test_negative_transfer_is_named_not_rounded_to_no_effect(self):
        t = {"eng-a": 0.70, "eng-b": 0.48, "eng-c": 0.50, "eng-d": 0.54}
        r = evaluate(L(), BASE, t)
        assert r["verdict"] == NEGATIVE and r["promote"] is False
        assert "hurt 3/3" in r["reasons"][0]

    def test_negative_transfer_outranks_a_strong_source_gain(self):
        """Source +0.30 must not rescue a default that hurts everywhere else."""
        t = {"eng-a": 0.90, "eng-b": 0.40, "eng-c": 0.42, "eng-d": 0.45}
        assert evaluate(L(), BASE, t)["verdict"] == NEGATIVE


class TestRefusals:
    def test_a_post_hoc_prediction_can_never_pass(self):
        t = {"eng-a": 0.90, "eng-b": 0.85, "eng-c": 0.88, "eng-d": 0.90}
        r = evaluate(L(predicted_before=False), BASE, t)
        assert r["verdict"] == NOT_MEASURED, "spectacular numbers must not buy a pass"
        assert "cannot fail" in r["reasons"][0]

    def test_one_held_out_engagement_is_not_enough(self):
        base, t = {"eng-a": 0.6, "eng-b": 0.5}, {"eng-a": 0.9, "eng-b": 0.9}
        r = evaluate(L(), base, t)
        assert r["verdict"] == NOT_MEASURED and "held-out engagement" in r["reasons"][0]

    def test_zero_held_out_engagements_is_not_measured(self):
        r = evaluate(L(), {"eng-a": 0.6}, {"eng-a": 0.99})
        assert r["verdict"] == NOT_MEASURED


class TestArithmetic:
    def test_held_out_mean_excludes_the_source(self):
        t = {"eng-a": 1.00, "eng-b": 0.60, "eng-c": 0.63, "eng-d": 0.67}
        r = evaluate(L(), BASE, t)
        # b +0.05, c +0.05, d +0.05 -> 0.05 exactly; the source's +0.40 is excluded
        assert r["held_out_mean"] == pytest.approx(0.05)
        assert r["source_lift"] == pytest.approx(0.40)

    def test_direction_down_treats_a_decrease_as_improvement(self):
        """Hallucination rate: lower is better."""
        base = {"eng-a": 0.40, "eng-b": 0.42, "eng-c": 0.38}
        t = {"eng-a": 0.30, "eng-b": 0.30, "eng-c": 0.28}
        r = evaluate(L(metric="halluc_rate", direction="down", min_effect=0.05), base, t)
        assert r["verdict"] == TRANSFERS
        assert r["held_out_mean"] == pytest.approx(0.11, abs=1e-9)

    def test_a_bad_direction_is_rejected_not_guessed(self):
        with pytest.raises(ValueError, match="direction"):
            evaluate(L(direction="sideways"), BASE, {k: v + 0.1 for k, v in BASE.items()})

    def test_exactly_meeting_the_predicted_effect_passes(self):
        t = {"eng-a": 0.60, "eng-b": 0.60, "eng-c": 0.63, "eng-d": 0.67}
        assert evaluate(L(), BASE, t)["verdict"] == TRANSFERS

    def test_just_under_the_predicted_effect_does_not(self):
        t = {"eng-a": 0.60, "eng-b": 0.599, "eng-c": 0.629, "eng-d": 0.669}
        assert evaluate(L(), BASE, t)["verdict"] == LOCAL_ONLY


class TestReport:
    def test_report_marks_the_source_as_never_decisive(self):
        t = {"eng-a": 0.72, "eng-b": 0.64, "eng-c": 0.66, "eng-d": 0.70}
        out = report(evaluate(L(), BASE, t))
        assert "never decisive" in out and "held-out mean" in out
        assert "VERDICT: TRANSFERS" in out
