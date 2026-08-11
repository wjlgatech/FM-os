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


def test_render_demos_discloses_progressively_and_labels_access():
    out = br.render_demos([{
        "name": "d", "icon": "🎬", "tagline": "t", "path": "labs/d",
        "url": "https://demo.example", "url_note": "🔒 password-gated",
        "public": "https://demo.example/system.html", "public_label": "Architecture",
        "what": "w", "why": "y", "how": "h",
    }])
    # The link row is open by default; the reasoning is one click away.
    assert "▶ Open the live app](https://demo.example)" in out
    assert "🔒 password-gated" in out, "a gated demo must say so on the link itself"
    assert "[Architecture](https://demo.example/system.html)" in out
    assert "<details>" in out and out.count("</details>") == 1
    for label in ("**What** — w", "**Why** — y", "**How** — h"):
        assert label in out


def test_demos_data_is_wired_into_the_readme():
    out = br.build()
    assert 'id="labs--demos"' in out
    assert "https://nomadic-mini-demo.vercel.app" in out, "the hosted demo must be linked"


def test_render_model_table_flags_noncommercial():
    tbl = br.render_model_table([
        {"name": "M", "url": "u", "params": "1B", "license": "NC-thing", "nc": True, "ondevice": True},
    ])
    assert "⚠️" in tbl and "model-zoo" in tbl
