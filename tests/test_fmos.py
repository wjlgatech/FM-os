import fmos


def test_load_returns_list_for_real_file():
    repos = fmos.load("repos")
    assert isinstance(repos, list) and len(repos) > 0
    assert all("url" in r for r in repos)


def test_load_missing_file_is_empty():
    assert fmos.load("does-not-exist") == []


def test_esc_collapses_whitespace_but_keeps_ampersand():
    # The README renders raw '&' (e.g. "Jobs & Careers"); esc must NOT escape it.
    assert fmos.esc("a   b\n c") == "a b c"
    assert fmos.esc("Jobs & Careers") == "Jobs & Careers"
    assert fmos.esc(None) == ""


def test_repos_with_stars_merges_when_available():
    repos = fmos.repos_with_stars()
    # If the generated stars map exists, at least one repo should carry a count.
    if (fmos.DATA / "_stars.yml").exists():
        assert any("stars" in r for r in repos)
