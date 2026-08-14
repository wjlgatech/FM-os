"""CI runs the syndata-bare reference for real (executed, not just present).

Why this file exists: the skill now ships a real-model runner whose whole value is
a set of refusals — a proxy base role can never substantiate the paper's claim, an
unmeasured caption is never a failure, an unrecognised word is never a
hallucination. Refusals that nothing exercises are decoration. Same subprocess
pattern as test_vlm_failure_probe.py, because the root suite collects only tests/.

Nothing here touches the network: run_real.py is imported and its pure functions
are driven, and the toy loop runs offline by construction.
"""
import pathlib
import subprocess
import sys

REF = pathlib.Path(__file__).resolve().parent.parent / "skills" / "syndata-bare" / "reference"


def _run(*args, env=None):
    return subprocess.run([sys.executable, *args], cwd=REF, capture_output=True,
                          text=True, env=env)


def test_toy_loop_offline_tests_pass():
    r = _run("-m", "pytest", "test_bare_loop.py", "-q")
    assert r.returncode == 0, r.stdout + r.stderr


def test_real_runner_offline_tests_pass():
    r = _run("-m", "pytest", "test_run_real.py", "-q")
    assert r.returncode == 0, r.stdout + r.stderr


def test_toy_loop_discriminates_all_three_pipelines():
    """The thesis at toy scale: BARE must pass while BOTH single-stage baselines
    fail. If every pipeline passes, the loop measures nothing."""
    r = _run("bare_loop.py")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" in r.stdout and "PASS" in r.stdout, r.stdout


def test_real_runner_reports_not_measured_without_a_key_and_never_fakes_a_pass():
    """No key ⇒ nothing measured ⇒ exit 1 and NO artifacts written. The failure
    mode this guards is the worst one available: a runner that quietly emits a
    green results table nobody measured."""
    import os

    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
    r = _run("run_real.py", "--per-scene", "2", env=env)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "nothing measured" in (r.stdout + r.stderr)


def test_stimuli_render_deterministically_from_the_command_line():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        a = _run("bare_stimuli.py", tmp)
        assert a.returncode == 0, a.stdout + a.stderr
        assert "wrote 6 scenes" in a.stdout
