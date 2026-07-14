import build_readme as br


def test_build_contains_key_anchors():
    out = br.build()
    for anchor in ("start-here", "model-zoo", "fm-os-certified", "open-source-repos"):
        assert f'id="{anchor}"' in out, f"missing section {anchor}"


def test_readme_on_disk_matches_generator():
    # The drift gate as a unit test: committed README == freshly generated.
    assert br.README.read_text() == br.build()


def test_fmt_repo_marks_slm_and_stars():
    line = br.fmt_repo({"name": "X", "url": "u", "slm": True, "stars": 1234, "blurb": "b"})
    assert "🤏" in line and "1,234" in line and "[X](u)" in line


def test_render_model_table_flags_noncommercial():
    tbl = br.render_model_table([
        {"name": "M", "url": "u", "params": "1B", "license": "NC-thing", "nc": True, "ondevice": True},
    ])
    assert "⚠️" in tbl and "model-zoo" in tbl
