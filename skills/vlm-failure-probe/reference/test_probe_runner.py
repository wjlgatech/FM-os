"""The probe suite must catch every paper-reported failure mode AND pass a
grounded model — plus honor no-evidence ⇒ No. This is the skill's teeth."""

from probe_runner import MockVSS, PatchedVSS, gate, load_spec, run_probes, score_probe

SPEC = load_spec()


def test_baseline_vss_fails_gate_on_every_mode():
    results = run_probes(MockVSS(), SPEC)
    ok, reasons = gate(results, SPEC)
    assert not ok
    failing = {r.split(":")[0] for r in reasons}
    assert failing == {m["id"] for m in SPEC["failure_modes"]}


def test_patched_model_passes_gate():
    ok, reasons = gate(run_probes(PatchedVSS(), SPEC), SPEC)
    assert ok, reasons


def test_order_matcher_catches_bottom_up_reversal():
    probe = next(
        p for m in SPEC["failure_modes"] for p in m["probes"] if p["id"] == "squares_stack"
    )
    assert score_probe("red, blue, green, yellow", probe) == 0.0  # reversed
    assert score_probe("yellow, green, blue, red", probe) == 1.0


def test_multipart_matcher_grades_partial_credit():
    probe = next(
        p
        for m in SPEC["failure_modes"]
        for p in m["probes"]
        if p["id"] == "summary_count_clothing"
    )
    only_last = MockVSS.ANSWERS["summary_count_clothing"]
    assert 0.0 < score_probe(only_last, probe) < 1.0


def test_unmeasured_mode_cannot_pass_the_gate():
    patched = PatchedVSS()

    def silent_on_temporal(probe):
        if probe["id"] in ("warehouse_no_fall", "sport_stays_tennis", "shirt_stays_white"):
            return None  # e.g. the endpoint refused — no evidence
        return patched(probe)

    results = run_probes(silent_on_temporal, SPEC)
    assert results["temporal_cross_chunk"]["measured"] is False
    assert results["temporal_cross_chunk"]["score"] is None  # excluded, not zeroed
    ok, reasons = gate(results, SPEC)
    assert not ok and any("NOT MEASURED" in r for r in reasons)


def test_stimuli_exist_and_are_deterministic():
    import stimuli

    probe_ids = {p["id"] for m in SPEC["failure_modes"] for p in m["probes"]}
    assert probe_ids == set(stimuli.GENERATORS)  # every probe ships its stimulus
    assert stimuli.manifest() == stimuli.manifest()  # pixel-identical re-runs


def test_word_boundary_matching_no_substring_accidents():
    probe = {"expect": ["no|never"], "match": "contains"}
    assert score_probe("The snowboarder is on the slope", probe) == 0.0  # 'no' ⊄ 'snowboarder'
    assert score_probe("No, the person never falls.", probe) == 1.0


# ── spec v0.2: the grader audit must not have made the gate vacuous ───────────
#
# v0.2 relaxed two probes after an audit found the GRADER at fault (see the audit
# log in probe_spec.yml). A relaxation is only legitimate if a wrong answer still
# fails — so the relaxation is paid for by `reject:` and policed by these tests.
# CheaterVSS is the adversary: fluent, confident, visually WRONG prose that a
# bag-of-words matcher is most likely to over-credit.

AUDITED_PROBES = ("describe_and_closer", "end_of_video", "sport_stays_tennis")


def _probe(pid: str) -> dict:
    return next(p for m in SPEC["failure_modes"] for p in m["probes"] if p["id"] == pid)


class CheaterVSS:
    """Plausible-but-wrong answers aimed squarely at the v0.2 relaxations."""

    ANSWERS = {
        # credits the FAR player — the exact thing `reject` exists to catch
        "describe_and_closer": (
            "Two players exchange shots in a long rally. The player in red is closer "
            "to the camera, standing at the bottom of the frame near the net."
        ),
        # 'disappears' without leaving the frame — why the bare word was NOT added
        "end_of_video": "At the very end the truck disappears behind the loading dock and parks.",
        "sport_stays_tennis": "The players are having a tennis-style warm-up before the soccer match.",
    }

    def __call__(self, probe: dict) -> str:
        return self.ANSWERS[probe["id"]]


def test_reject_zeroes_a_probe_that_credits_the_wrong_entity():
    probe = _probe("describe_and_closer")
    # right entity by POSITION (the v0.2 intent fix) — full credit
    assert score_probe(
        "Two players rally; the player at the bottom, in the lower court, is closer to the camera.",
        probe,
    ) == 1.0
    # right entity by SHIRT — still full credit, unchanged from v0.1
    assert score_probe("A tennis rally between two players; the player in white is closer.", probe) == 1.0
    # WRONG entity — zeroed outright, not given partial credit for the description
    assert score_probe(CheaterVSS.ANSWERS["describe_and_closer"], probe) == 0.0


def test_audited_probes_still_score_zero_for_a_confident_cheater():
    cheater = CheaterVSS()
    for pid in AUDITED_PROBES:
        probe = _probe(pid)
        assert score_probe(cheater(probe), probe) == 0.0, pid


def test_end_of_video_accepts_frame_exit_phrasing_but_not_bare_disappearance():
    probe = _probe("end_of_video")
    assert score_probe("The truck completely disappears off the right side of the screen.", probe) == 1.0
    assert score_probe("The truck drives out of frame.", probe) == 1.0
    assert score_probe("The truck disappears behind the dock.", probe) == 0.0  # not an exit
    assert score_probe("A worker stacks pallets near the entrance.", probe) == 0.0  # no truck


def test_audit_relaxations_did_not_let_the_paper_baseline_pass():
    """The whole point: MockVSS encodes the VSS paper's OBSERVED failures. If a
    grader fix lets those pass, the fix broke the benchmark."""
    results = run_probes(MockVSS(), SPEC)
    for pid in AUDITED_PROBES:
        scored = next(
            p for r in results.values() for p in r["probes"] if p["id"] == pid
        )
        assert scored["score"] == 0.0 or scored["score"] < 1.0, pid
    ok, _ = gate(results, SPEC)
    assert not ok


def test_sport_reject_does_not_punish_a_correct_contrastive_answer():
    """The guard on my own fix: rejects are claim-shaped, so a model that names
    tennis AND rules out the look-alike sport must still score 1.0. Bare sport
    words in the reject list would have zeroed this correct answer."""
    probe = _probe("sport_stays_tennis")
    assert score_probe("Tennis. The green court is not soccer — there is a net and rackets.", probe) == 1.0
    assert score_probe("They are playing tennis throughout; no soccer at any point.", probe) == 1.0
    # but a claimed transition is still caught, wherever it appears
    assert score_probe("Tennis at first, but it switches to soccer.", probe) == 0.0
    assert score_probe("They are playing table tennis.", probe) == 0.0  # ⊄ 'tennis' credit


def test_multiword_aliases_survive_punctuation_collapse():
    """Answers are markdown; 'drives, away' must still match 'drives away'."""
    probe = {"expect": ["drives away"], "match": "contains"}
    assert score_probe("The truck **drives**, away from the dock.", probe) == 1.0


def test_spec_records_its_own_audit():
    """spec-as-data: v0.2 exists only with the audit rationale committed beside it."""
    from pathlib import Path

    raw = Path(__file__).parent.joinpath("probe_spec.yml").read_text()
    assert SPEC["version"] == "0.3"
    assert raw.count("AUDIT LOG") == 2  # v0.1→v0.2 and v0.2→v0.3, both retained
    assert "PRE-REGISTERED PREDICTION" in raw


def test_phrasing_invariance_v03_markdown_and_prose_score_alike():
    """The v0.3 fix, stated as a property: two answers with IDENTICAL content must
    score identically regardless of phrasing. This is the exact pair that flipped
    claude-opus-5's gate between the v0.1 and v0.2 runs."""
    probe = _probe("summary_count_clothing")
    prose = (
        "There is one person — a figure standing on a gray floor with brown boxes "
        "behind them. They're wearing a yellow short-sleeved top and blue pants."
    )
    markdown = (
        "**Summary:** A figure stands between brown boxes on a gray floor.\n\n"
        "**People present:** One.\n\n**Clothing:** A yellow short-sleeved top and blue pants."
    )
    assert score_probe(prose, probe) == score_probe(markdown, probe) == 1.0
    # part 1 is NOT relaxed: an answer that skips the summary still loses a third
    no_summary = "One person is present. The person is wearing a yellow shirt and blue pants."
    assert round(score_probe(no_summary, probe), 2) == 0.67


def test_variance_report_flags_an_unstable_probe():
    """A grader that moves on rephrasing must be FLAGGED, not averaged away."""
    import run_real

    class Rephraser:
        """Semantically identical, differently worded on each call."""

        def __init__(self):
            self.n = 0

        def __call__(self, probe):
            if probe["id"] != "floor_color":
                return "no idea"
            self.n += 1
            # same meaning both times; only the SECOND uses a word the alias list
            # happens to know — precisely the grader defect this flag exists for
            return "The floor is a plain neutral surface." if self.n == 1 else "The floor is grey."

    spec = load_spec()
    m = Rephraser()
    runs = {"fake": [run_probes(m, spec) for _ in range(2)]}
    report = run_real.variance_report(runs, spec)
    assert "GRADER-UNSTABLE" in report and "floor_color" in report
    assert "1 unstable probe/model pair" in report

    stable = {"fake": [run_probes(PatchedVSS(), spec) for _ in range(3)]}
    ok_report = run_real.variance_report(stable, spec)
    assert "GRADER-UNSTABLE" not in ok_report
    assert "Every probe/model pair was stable" in ok_report


def test_empty_response_is_not_measured_never_a_zero():
    """Found in a live 3-repeat run: a response with no text block joined to "",
    which is not None, so it was SCORED 0.0 and reported as a model failure the
    model never committed. An absent answer must be excluded, never a fake FAIL."""
    import vlm_adapter

    class _Block:
        def __init__(self, type_):
            self.type = type_

    class _Msg:
        stop_reason = "max_tokens"
        content = [_Block("thinking")]  # zero text blocks

    class _Client:
        class messages:
            @staticmethod
            def create(**_):
                return _Msg()

    model = vlm_adapter.RealVLM.__new__(vlm_adapter.RealVLM)
    model.model = "test"
    model._client = _Client()
    assert model({"id": "floor_color", "question": "What color?"}) is None

    # and the runner must treat that as unmeasured, not as a wrong answer
    spec = load_spec()
    patched = PatchedVSS()
    results = run_probes(
        lambda p: None if p["id"] == "floor_color" else patched(p), spec
    )
    hallu = results["grounding_hallucination"]
    assert hallu["measured"] is False and hallu["score"] is None
    ok, reasons = gate(results, spec)
    assert not ok and any("NOT MEASURED" in r for r in reasons)


def test_truncated_response_is_not_measured_never_a_zero():
    """Found live: a compound answer cut off mid-word ("...A yellow short") had its
    missing tail graded as a missing sub-answer. A truncated answer carries no
    evidence about what it would have said — exclude it, never score it."""
    import vlm_adapter

    class _Text:
        type = "text"
        text = "The person is wearing a yellow short"  # cut off mid-phrase

    class _Msg:
        stop_reason = "max_tokens"
        content = [_Text()]

    class _Client:
        class messages:
            @staticmethod
            def create(**_):
                return _Msg()

    model = vlm_adapter.RealVLM.__new__(vlm_adapter.RealVLM)
    model.model, model._client = "test", _Client()
    assert model({"id": "summary_count_clothing", "question": "?"}) is None

    # a COMPLETE response with the same text is still graded normally
    class _Done(_Msg):
        stop_reason = "end_turn"

    _Client.messages.create = staticmethod(lambda **_: _Done())
    assert model({"id": "summary_count_clothing", "question": "?"}) == _Text.text


def test_real_adapter_returns_none_without_key(monkeypatch):
    import vlm_adapter

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    model = vlm_adapter.RealVLM()
    assert model({"id": "floor_color", "question": "?"}) is None  # not measured, never fake
