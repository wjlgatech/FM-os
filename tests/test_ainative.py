import ainative


def test_repo_stays_ai_native():
    r = ainative.AINativeAudit().run()
    assert r["score"] >= r["pass_threshold"], f"AI-native score dropped to {r['score']}"


def test_every_principle_has_some_evidence():
    # No principle may be a pure claim: each must have real evidence in the repo.
    r = ainative.AINativeAudit().run()
    dead = [p["id"] for p in r["principles"] if p["status"] == "fail"]
    assert not dead, f"principles with no evidence (fake claims): {dead}"


def test_evidence_checker_detects_missing(tmp_path):
    assert ainative._has({"file": "Makefile"}) is True
    assert ainative._has({"file": "does/not/exist.xyz"}) is False
    assert ainative._has({"file": "Makefile", "grep": "check:"}) is True
    assert ainative._has({"file": "Makefile", "grep": "zzz_not_present_zzz"}) is False
