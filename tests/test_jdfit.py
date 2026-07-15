import pathlib
import sys

import build_readme
import certify
import jdfit
from fmos import ROOT

JD = ROOT / "examples" / "jd" / "nomadicml-mts-ml.txt"


def test_jdfit_scores_the_nomadicml_jd_well():
    result = jdfit.JDFit(JD.read_text()).analyze()
    assert result["score"] >= 80, f"fit dropped to {result['score']}"
    assert result["required"] >= 8
    caps = {c["id"]: c for c in result["capabilities"]}
    # The VLM/video capabilities must now be covered (knowledge + tooling).
    assert caps["vlm_multimodal"]["coverage"] == "covered"
    assert caps["video_understanding"]["coverage"] == "covered"
    assert "vlm-quickstart" in " ".join(caps["vlm_multimodal"]["tooling"])


def test_jdfit_marks_unrequired_capabilities_absent():
    # A JD with none of the keywords should require nothing.
    result = jdfit.JDFit("we are hiring a barista to make espresso").analyze()
    assert result["required"] == 0


def test_build_readme_path_is_under_root():
    # Guards the ROOT import that main()'s "Wrote ..." line depends on.
    assert str(build_readme.README).startswith(str(ROOT))
    assert build_readme.README.relative_to(ROOT)


def test_certify_registry_smoke(monkeypatch):
    # Exercises the --registry write path (yaml.safe_dump) end to end.
    monkeypatch.setattr(sys, "argv", ["certify", "--registry"])
    assert certify.main() == 0
    out = pathlib.Path(ROOT / "data" / "_certifications.yml")
    assert out.exists() and "slm-quickstart" in out.read_text()
