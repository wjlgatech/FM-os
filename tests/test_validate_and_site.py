import json

import build_site
import validate


def test_check_entry_flags_problems():
    seen: set = set()
    errs = validate.check_entry({"name": "x"}, ["name", "url"], "t[0]", seen)
    assert any("url" in e for e in errs)  # missing required field
    errs = validate.check_entry({"name": "x", "url": "ftp://bad"}, ["name", "url"], "t[1]", seen)
    assert any("http" in e for e in errs)  # bad scheme


def test_check_entry_detects_duplicate_url():
    seen: set = set()
    validate.check_entry({"name": "a", "url": "https://x"}, ["name"], "t[0]", seen)
    errs = validate.check_entry({"name": "b", "url": "https://x"}, ["name"], "t[1]", seen)
    assert any("duplicate" in e for e in errs)


def test_real_data_passes_validation():
    assert validate.check_file("repos", ["name", "url", "category"]) == []
    assert validate.check_file("registry", ["name", "kind"]) == []


def test_build_site_emits_registry_and_certifications():
    build_site.main()
    bundle = json.loads(build_site.OUT.read_text())
    assert "registry" in bundle and "certifications" in bundle
    assert bundle["counts"]["repos"] > 0
