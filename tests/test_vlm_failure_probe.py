"""CI runs the vlm-failure-probe reference for real (executed, not just present).

Why this file exists: the skill shipped 17 probe tests and 10 TGS gate-math tests
that `make check` never ran — the root suite collects only `tests/`. A grader whose
own tests are not gated can silently regress, which is precisely the failure the
probe-spec audit log (probe_spec.yml) was written to prevent. Same subprocess
pattern as test_continual_rl_eval.py.
"""
import pathlib
import subprocess
import sys

REF = pathlib.Path(__file__).resolve().parent.parent / "skills" / "vlm-failure-probe" / "reference"


def _run(*args):
    return subprocess.run([sys.executable, *args], cwd=REF, capture_output=True, text=True)


def test_probe_suite_offline_tests_pass():
    r = _run("-m", "pytest", "test_probe_runner.py", "-q")
    assert r.returncode == 0, r.stdout + r.stderr


def test_tgs_gate_math_tests_pass():
    r = _run("-m", "pytest", "test_tgs.py", "-q")
    assert r.returncode == 0, r.stdout + r.stderr


def test_probe_gate_discriminates_the_paper_baseline_from_a_grounded_model():
    """The suite's teeth: the VSS paper's observed failures must fail, a grounded
    model must pass. If both pass, the benchmark measures nothing."""
    r = _run("probe_runner.py")
    assert r.returncode == 0, r.stdout + r.stderr
    out = r.stdout
    assert "gate: FAIL" in out and "gate: PASS" in out, out


def test_temporal_grounding_score_discriminates_and_states_its_floor():
    r = _run("tgs.py")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "TGS = 0.000" in r.stdout, "the paper's observed baseline must score 0"
    assert "TGS = 1.000" in r.stdout, "a grounded model must score 1"
    assert "floor 0.75" in r.stdout


def test_spec_audit_log_and_predictions_are_committed_with_the_spec():
    """spec-as-data: a version bump only counts if its rationale ships beside it."""
    raw = (REF / "probe_spec.yml").read_text()
    assert 'version: "0.3"' in raw
    assert raw.count("AUDIT LOG") == 2  # v0.1→v0.2 and v0.2→v0.3, both retained
    assert "PRE-REGISTERED PREDICTION" in raw
    assert "ANTI-GOALPOST RULE" in raw
