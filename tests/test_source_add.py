import json
import subprocess
import tomllib

import pytest

from swatplus_reference.cli import main
from swatplus_reference.source.add import add_profile, default_profile_name
from swatplus_reference.source.config import (
    load_config,
    with_docs_source,
    with_schema_source,
)
from swatplus_reference.source.fetch import fetch_profile

CONFIG = """
# kept comment
default_source = "main"

[sources.main]
ref = "main"
checkout = "external/main"

[docs]
source = "main"

[schema]
source = "main"
version = "62.0.0"
""".lstrip()


def _git(cwd, *args):
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout.strip()


@pytest.fixture
def upstream(tmp_path):
    """A tiny SWAT+-shaped repository with a branch and two kinds of tag."""
    repo = tmp_path / "upstream"
    (repo / "src").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    (repo / "src" / "main.f90").write_text("program main\nend program main\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "one")
    _git(repo, "tag", "-a", "63.0.0", "-m", "release")  # annotated
    _git(repo, "tag", "light")  # lightweight
    _git(repo, "checkout", "-q", "-b", "feature/foo")
    return repo, f"file://{repo}"


@pytest.fixture
def config_path(tmp_path):
    path = tmp_path / "corpus" / "swatref.toml"
    path.parent.mkdir()
    path.write_text(CONFIG, encoding="utf-8")
    return path


@pytest.mark.parametrize(
    "ref, name",
    [
        ("63.0.0", "release_63_0_0"),
        ("v63.0.1", "release_63_0_1"),
        ("refs/pull/252/head", "pr_252"),
        ("feature/Foo-bar", "feature_foo_bar"),
        ("refs/heads/dev", "dev"),
        ("DE210D64DB4F1D75E110BD6AF33EA9C333D27B8A", "commit_de210d64db4f"),
    ],
)
def test_default_profile_names(ref, name):
    assert default_profile_name(ref) == name


def test_add_locks_an_annotated_tag_to_its_commit(upstream, config_path):
    repo, url = upstream
    commit = _git(repo, "rev-parse", "63.0.0^{commit}")

    result = add_profile(config_path, "63.0.0", repository=url)

    assert result.created
    text = config_path.read_text()
    assert text.startswith("# kept comment")
    # Inserted with the other profiles, not after [docs]/[schema].
    assert text.index("[sources.release_63_0_0]") < text.index("[docs]")
    profile = load_config(config_path).sources["release_63_0_0"]
    assert profile.commit == commit  # the commit, not the tag object
    assert profile.ref == "63.0.0"
    assert profile.label == "SWAT+ 63.0.0"
    assert str(profile.checkout) == "external/swatplus-release_63_0_0"


def test_added_profile_fetches_and_verifies(upstream, config_path):
    _, url = upstream
    add_profile(config_path, "feature/foo", repository=url)
    cfg = load_config(config_path)

    provenance = fetch_profile(cfg, "feature_foo")

    assert provenance.resolved_commit == cfg.sources["feature_foo"].commit
    assert (cfg.root / "external/swatplus-feature_foo/src/main.f90").exists()


def test_readding_reports_a_moved_branch_without_relocking(upstream, config_path):
    repo, url = upstream
    first = add_profile(config_path, "feature/foo", repository=url)
    (repo / "src" / "main.f90").write_text("program main\n! moved\nend program main\n")
    _git(repo, "commit", "-q", "-am", "two")

    again = add_profile(config_path, "feature/foo", repository=url)

    assert not again.created
    assert again.profile.commit == first.profile.commit
    assert again.current_commit == _git(repo, "rev-parse", "HEAD")
    assert again.to_dict()["moved"] is True
    assert config_path.read_text().count("[sources.feature_foo]") == 1


def test_add_refuses_a_name_taken_by_another_ref(upstream, config_path):
    _, url = upstream
    with pytest.raises(ValueError, match="already exists"):
        add_profile(config_path, "light", name="main", repository=url)


def test_add_refuses_an_unknown_ref(upstream, config_path):
    _, url = upstream
    before = config_path.read_text()
    with pytest.raises(ValueError, match="not a branch, tag, or ref"):
        add_profile(config_path, "no-such-branch", repository=url)
    assert config_path.read_text() == before


def test_add_refuses_a_ref_that_is_both_branch_and_tag(upstream, config_path):
    repo, url = upstream
    _git(repo, "branch", "light")
    with pytest.raises(ValueError, match="both a branch and a tag"):
        add_profile(config_path, "light", repository=url)
    assert add_profile(config_path, "refs/tags/light", name="light_tag", repository=url).created


def test_cli_source_add_prints_the_lock(upstream, config_path, capsys):
    _, url = upstream
    code = main(["--config", str(config_path), "source", "add", "63.0.0", "--repository", url])
    assert code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["profile"] == "release_63_0_0" and out["created"] and not out["moved"]
    tomllib.loads(config_path.read_text())


def test_docs_source_override_repoints_every_docs_field(upstream, config_path):
    _, url = upstream
    add_profile(config_path, "63.0.0", repository=url)
    cfg = load_config(config_path)

    selected = with_docs_source(cfg, "release_63_0_0")

    profile = cfg.sources["release_63_0_0"]
    assert selected.docs_source == "release_63_0_0"
    assert selected.source_ref == profile.commit
    assert str(selected.source_dir) == "external/swatplus-release_63_0_0/src"
    assert profile.commit in selected.source_link_base
    assert selected.version_label == "SWAT+ 63.0.0"
    assert cfg.docs_source == "main"  # the loaded config is untouched


def test_schema_override_takes_its_version_from_the_release_tag(upstream, config_path):
    _, url = upstream
    add_profile(config_path, "63.0.0", repository=url)
    add_profile(config_path, "feature/foo", repository=url)
    cfg = load_config(config_path)

    release = with_schema_source(cfg, "release_63_0_0")
    assert (release.schema.source, release.schema.version) == ("release_63_0_0", "63.0.0")
    assert cfg.schema.version == "62.0.0"

    with pytest.raises(ValueError, match="pass --version"):
        with_schema_source(cfg, "feature_foo")
    assert with_schema_source(cfg, "feature_foo", "dev-foo").schema.version == "dev-foo"


def test_cli_docs_rejects_an_unknown_source(config_path):
    with pytest.raises(SystemExit, match="unknown source profile"):
        main(["--config", str(config_path), "docs", "status", "--source", "nope"])


@pytest.mark.parametrize(
    "args, message",
    [
        (["--base", "main"], "go together"),
        (["pr_252", "--base", "a", "--candidate", "b"], "not both"),
        ([], "not both"),
    ],
)
def test_cli_compare_argument_rules(config_path, capsys, args, message):
    with pytest.raises(SystemExit):
        main(["--config", str(config_path), "compare", *args])
    assert message in capsys.readouterr().err


def test_cli_compare_base_candidate_builds_an_unconfigured_comparison(
    config_path, monkeypatch
):
    from swatplus_reference.source.config import SourceProfile

    seen = {}

    def fake_run(cfg, name, **kwargs):
        seen["comparison"] = cfg.comparison(name)
        raise RuntimeError("stop here")

    monkeypatch.setattr("swatplus_reference.comparison.run.run_comparison", fake_run)
    cfg_text = config_path.read_text() + '\n[sources.other]\nref = "dev"\n'
    config_path.write_text(cfg_text)
    with pytest.raises(SystemExit):
        main(["--config", str(config_path), "compare", "--base", "main", "--candidate", "other"])

    comparison = seen["comparison"]
    assert (comparison.base_source, comparison.candidate_source) == ("main", "other")
    assert str(comparison.output_dir) == "reports/comparisons/main_vs_other"
    assert isinstance(load_config(config_path).sources["other"], SourceProfile)


def test_cli_source_list_reports_profiles_and_fetch_state(upstream, config_path, capsys):
    _, url = upstream
    add_profile(config_path, "63.0.0", repository=url)
    fetch_profile(load_config(config_path), "release_63_0_0")
    capsys.readouterr()

    assert main(["--config", str(config_path), "source", "list"]) == 0
    rows = {row["name"]: row for row in json.loads(capsys.readouterr().out)}

    assert rows["main"]["docs_default"] and not rows["main"]["fetched"]
    assert rows["release_63_0_0"]["fetched"]
    assert rows["release_63_0_0"]["label"] == "SWAT+ 63.0.0"


def test_cli_source_refs_lists_releases_newest_first(upstream, capsys):
    repo, url = upstream
    _git(repo, "tag", "-a", "62.0.0", "HEAD", "-m", "older")
    _git(repo, "tag", "-a", "63.10.0", "HEAD", "-m", "newer")

    assert main(["source", "refs", "--repository", url]) == 0
    out = json.loads(capsys.readouterr().out)

    tags = [t["ref"] for t in out["tags"]]
    assert tags[:3] == ["63.10.0", "63.0.0", "62.0.0"]  # numeric, not string, order
    assert tags[-1] == "light" and not out["tags"][-1]["release"]
    assert out["tags"][0]["commit"] == _git(repo, "rev-parse", "HEAD")  # peeled
    assert {b["ref"] for b in out["branches"]} == {"main", "feature/foo"}
