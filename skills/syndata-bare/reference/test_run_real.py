"""Offline gate for the real-model BARE runner — no network, no keys.

What must hold whatever the models say: unmeasured captions never become
failures, an unrecognised word is never a hallucination, a proxy base role can
never substantiate the paper's claim, and the emitted LaTeX says which of those
two worlds the numbers came from.
"""
from __future__ import annotations

import pytest

import bare_stimuli as st
import run_real as rr
from vlm_roles import is_true_base

S1 = st.by_id("s1_red_circle_blue_square")
F1 = st.facts(S1)


# ── stimuli: ground truth is known by construction ───────────────────────────


def test_every_scene_renders_identically_every_time():
    a, b = st.render(S1), st.render(S1)
    assert a.tobytes() == b.tobytes()


def test_facts_and_decoys_partition_the_closed_vocabulary():
    for scene in st.SCENES:
        f = st.facts(scene)
        assert f["colors"] & f["decoy_colors"] == set()
        assert f["shapes"] & f["decoy_shapes"] == set()
        assert f["colors"] | f["decoy_colors"] == st.ALL_COLORS
        assert f["shapes"] | f["decoy_shapes"] == st.ALL_SHAPES


# ── the metric: precision, not coverage ──────────────────────────────────────


def test_absent_colour_is_a_hallucination():
    assert rr.hallucinations("a green circle beside a blue square", F1) == {"green"}


def test_absent_shape_is_a_hallucination():
    assert rr.hallucinations("a red triangle and a blue square", F1) == {"triangle"}


def test_plural_forms_are_caught():
    assert "triangle" in rr.hallucinations("two red triangles", F1)


def test_correct_caption_scores_clean():
    assert rr.hallucinations("a red circle on the left, a blue square right", F1) == set()


def test_unknown_words_are_never_scored_as_hallucination():
    """THE SYNONYM GUARD. 'box', 'disc', 'vibrant' are outside the closed
    vocabulary — scoring them would publish failures the model never made."""
    assert rr.hallucinations("a vibrant crimson disc beside a navy box", F1) == set()


def test_diversity_is_zero_under_mode_collapse():
    assert rr.diversity(["a red circle", "a red circle", "a red circle"]) == 0.0


def test_diversity_is_positive_when_phrasing_varies():
    assert rr.diversity(["a red circle left of a blue square",
                         "on the right sits a navy cube, crimson orb opposite"]) > 0.5


def test_single_caption_has_no_defined_diversity():
    assert rr.diversity(["only one"]) == 0.0


# ── unmeasured is excluded, never a failure ──────────────────────────────────


def test_unmeasured_captions_are_excluded_not_scored_zero():
    """A None caption must not drag alignment down; it is absent, not wrong."""
    clean = "a red circle and a blue square"
    both = rr.score({S1["id"]: [clean, None, clean]})
    only = rr.score({S1["id"]: [clean, clean]})
    assert both["measured"] == 2
    assert both["alignment"] == only["alignment"] == 1.0


def test_all_unmeasured_yields_none_not_a_pass():
    s = rr.score({S1["id"]: [None, None]})
    assert s["measured"] == 0
    assert s["alignment"] is None and s["gate_pass"] is None


def test_hallucinated_caption_lowers_alignment():
    s = rr.score({S1["id"]: ["a red circle", "a green triangle"]})
    assert s["alignment"] == 0.5
    assert s["gate_pass"] is False


# ── role fidelity: a proxy can never earn the paper's claim ──────────────────


def _thesis_shaped() -> dict:
    """Scores in exactly the shape the BARE thesis predicts."""
    return {
        "base_only": {"measured": 9, "alignment": 0.6, "diversity": 0.7,
                      "yield": 0.6, "gate_pass": False, "gate_reasons": ["alignment"]},
        "instruct_only": {"measured": 9, "alignment": 1.0, "diversity": 0.05,
                          "yield": 1.0, "gate_pass": False, "gate_reasons": ["diversity"]},
        "bare": {"measured": 9, "alignment": 1.0, "diversity": 0.6,
                 "yield": 1.0, "gate_pass": True, "gate_reasons": []},
    }


def test_proxy_base_cannot_substantiate_the_paper_claim():
    """THE CORE RULE. Even with textbook-perfect numbers, an instruction-tuned
    model in the base role does not test BARE's base-vs-instruct claim."""
    v = rr.verdicts(_thesis_shaped(), "proxy")
    assert v["pipeline_claim"] is True
    assert v["paper_claim"] is False
    assert v["paper_claim_blocked_by_proxy"] is True


def test_true_base_can_substantiate_both_claims():
    v = rr.verdicts(_thesis_shaped(), "true_base")
    assert v["pipeline_claim"] is True and v["paper_claim"] is True


def test_pipeline_claim_fails_when_a_baseline_does_not_fail():
    s = _thesis_shaped()
    s["base_only"]["gate_pass"] = True  # nothing for refinement to fix
    v = rr.verdicts(s, "true_base")
    assert v["pipeline_claim"] is False and v["paper_claim"] is False
    assert "no hallucination" in v["why"]


def test_unmeasured_pipeline_gives_an_unmeasured_verdict_not_a_false_one():
    s = _thesis_shaped()
    s["bare"]["gate_pass"] = None
    v = rr.verdicts(s, "true_base")
    assert v["pipeline_claim"] is None and v["paper_claim"] is None


def test_anthropic_models_are_never_true_base():
    assert not is_true_base("claude-sonnet-5")
    assert not is_true_base("gpt-4o")
    assert is_true_base("Salesforce/blip2-opt-2.7b")


def test_unknown_model_defaults_to_proxy_not_base():
    """Unknown resolves to the weaker claim — the safe direction."""
    assert not is_true_base("some-lab/unreleased-vlm")


# ── the artifact must disclose which world it came from ──────────────────────


def _meta(fidelity: str) -> dict:
    return {"base_model": "m-b", "instruct_model": "m-i", "role_fidelity": fidelity,
            "n_scenes": 6, "date": "2026-08-14"}


def test_latex_caption_discloses_a_proxy_run():
    tex = rr.latex_table(_thesis_shaped(), _meta("proxy"))
    assert "not a base checkpoint" in tex
    assert "do not substantiate" in tex


def test_latex_caption_does_not_hedge_a_true_base_run():
    tex = rr.latex_table(_thesis_shaped(), _meta("true_base"))
    assert "genuine base checkpoint" in tex
    assert "do not substantiate" not in tex


def test_latex_marks_unmeasured_cells_rather_than_zero():
    s = _thesis_shaped()
    s["bare"] = {"measured": 0, "alignment": None, "diversity": None, "yield": None,
                 "gate_pass": None, "gate_reasons": ["nothing measured"]}
    tex = rr.latex_table(s, _meta("proxy"))
    assert "n.m." in tex
    assert "0.00" not in tex.split("bare")[-1]


def test_single_run_reports_variance_as_unmeasured():
    assert "UNMEASURED" in rr.variance_report([_thesis_shaped()], 1)


def test_repeats_report_a_spread():
    a, b = _thesis_shaped(), _thesis_shaped()
    b["bare"]["diversity"] = 0.4
    out = rr.variance_report([a, b], 2)
    assert "UNMEASURED" not in out and "sd" in out


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
