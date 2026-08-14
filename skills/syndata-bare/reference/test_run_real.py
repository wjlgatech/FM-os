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
        "base_only": {"measured": 9, "alignment": 0.6, "diversity": 0.7, "yield": 0.6,
                      "hallucinated": 4, "gate_pass": False, "gate_reasons": ["alignment"]},
        "instruct_only": {"measured": 9, "alignment": 1.0, "diversity": 0.05, "yield": 1.0,
                          "hallucinated": 0, "gate_pass": False, "gate_reasons": ["diversity"]},
        "bare": {"measured": 9, "alignment": 1.0, "diversity": 0.6, "yield": 1.0,
                 "hallucinated": 0, "gate_pass": True, "gate_reasons": []},
    }


# ── statistical power: a zero is not a refutation ────────────────────────────


def test_rule_of_three_matches_the_published_formula():
    """Hanley & Lippman-Hand 1983: 0 events in n ⇒ 95% CI [0, 3/n]."""
    assert rr.rule_of_three(18) == pytest.approx(3 / 18)
    assert rr.rule_of_three(1500) == pytest.approx(0.002)
    assert rr.rule_of_three(0) is None


def test_the_first_live_run_was_underpowered_not_a_refutation():
    """THE CORRECTION, pinned. 0 hallucinations in 18 captions puts the true rate
    anywhere in [0, 16.7%] — it cannot exclude the ~4.6% rate independently
    published for the very model used. Yesterday's run called this FALSE."""
    p = rr.power_check(hallucinated=0, measured=18)
    assert p["powered"] is False
    assert p["upper95"] == pytest.approx(3 / 18)
    assert p["n_required"] == 65
    assert "CANNOT exclude" in p["why"]


def test_enough_samples_makes_a_zero_informative():
    p = rr.power_check(hallucinated=0, measured=100)
    assert p["powered"] is True and p["upper95"] == pytest.approx(0.03)


def test_observed_events_need_no_power_argument():
    """With events observed the rate is estimated directly; the zero-numerator
    problem does not arise."""
    p = rr.power_check(hallucinated=3, measured=18)
    assert p["powered"] is True and p["upper95"] is None


def test_underpowered_zero_yields_inconclusive_never_false():
    """A base role that showed no hallucination in too few samples must make the
    pipeline claim INCONCLUSIVE — not refuted, not supported."""
    s = _thesis_shaped()
    s["base_only"].update(gate_pass=True, gate_reasons=[], alignment=1.0,
                          hallucinated=0, measured=18)
    v = rr.verdicts(s, "true_base")
    assert v["pipeline_claim"] is None
    assert v["paper_claim"] is None
    assert v["underpowered"] is True
    assert "lacked the power" in v["why"]


def test_a_powered_clean_base_role_does_refute_the_pipeline_claim():
    """The same shape WITH enough samples is a real negative, not an unknown."""
    s = _thesis_shaped()
    s["base_only"].update(gate_pass=True, gate_reasons=[], alignment=1.0,
                          hallucinated=0, measured=200)
    v = rr.verdicts(s, "true_base")
    assert v["pipeline_claim"] is False
    assert v["underpowered"] is False
    assert "genuinely" in v["why"]


# ── the precondition probe ───────────────────────────────────────────────────


def test_interference_scenes_print_a_conflicting_colour():
    for s in st.INTERFERENCE_SCENES:
        true_color = s["objects"][0][0]
        assert s["label"].lower() != true_color, "the label must CONFLICT"
        assert s["label"].lower() in st.ALL_COLORS


def test_interference_render_differs_from_the_plain_render():
    s = st.INTERFERENCE_SCENES[0]
    assert st.render(s).tobytes() != st.render_interference(s).tobytes()


def test_naming_the_printed_word_is_scored_as_hallucination():
    s = st.INTERFERENCE_SCENES[0]  # red circle labelled BLUE
    res = rr.score_interference({s["id"]: ["Blue."]})
    assert res["hallucinated"] == 1 and res["rate"] == 1.0


def test_naming_the_true_colour_is_clean_even_if_the_word_is_mentioned():
    """A model that says 'red, though the word BLUE is printed on it' is CORRECT.
    Scoring that as a hallucination would invent a failure."""
    s = st.INTERFERENCE_SCENES[0]
    res = rr.score_interference({s["id"]: ["Red, although the word BLUE is printed on it."]})
    assert res["hallucinated"] == 0


def test_interference_excludes_unmeasured_answers():
    s = st.INTERFERENCE_SCENES[0]
    res = rr.score_interference({s["id"]: ["Red.", None, None]})
    assert res["measured"] == 1 and res["hallucinated"] == 0


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
    assert "nothing for refinement to fix" in v["why"]


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
