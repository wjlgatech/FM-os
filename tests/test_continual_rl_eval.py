"""CI runs the continual-rl-eval reference for real (executed, not just present)."""
import subprocess, sys, pathlib

REF = pathlib.Path(__file__).resolve().parent.parent / "skills" / "continual-rl-eval" / "reference"


def _run(*args):
    return subprocess.run([sys.executable, *args], cwd=REF, capture_output=True, text=True)


def test_reference_property_suite_passes():
    r = _run("test_env.py")
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_discriminates_learner_from_coaster():
    adaptive = _run("run_demo.py", "--policy", "adaptive")
    static = _run("run_demo.py", "--policy", "static")
    assert adaptive.returncode == 0, "a continual learner should PASS: " + adaptive.stdout
    assert static.returncode == 1, "a coaster should FAIL the eval-with-teeth gate: " + static.stdout
