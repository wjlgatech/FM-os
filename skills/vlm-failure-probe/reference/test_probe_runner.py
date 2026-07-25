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
