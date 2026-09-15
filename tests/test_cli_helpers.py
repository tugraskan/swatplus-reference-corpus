import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from swatplus_reference.cli import (
    _parse_docs_with_diagnostics,
    _rel,
    _report_is_current,
    _rich_report_index,
    cmd_status,
    cmd_parse,
)
from swatplus_reference.parser.facts import FactStore
from swatplus_reference.parser.fortran import fparser_version
from swatplus_reference.parser.rich import RichStore
from swatplus_reference.parser.schema_model import (
    DerivedTypeDoc,
    ProcedureDoc,
    ProjectIndex,
    SourceLocation,
)
from swatplus_reference.source.config import Config, SourceProfile, load_config
from swatplus_reference.source.fetch import fetch_profile


def test_rel_under_root():
    root = Path("/a/b")
    assert _rel(Path("/a/b/docs_src/x.md"), root) == "docs_src/x.md"


def test_rel_outside_root_returns_absolute():
    # A version-bump run can point one ref's config (root) at another ref's
    # absolute docs_dir; _rel must not raise ValueError there.
    root = Path("/tmp/scratch")
    p = Path("/home/user/repo/docs_src/x.md")
    assert _rel(p, root) == str(p)


def test_fetch_supports_an_exact_commit_ref(tmp_path, monkeypatch):
    ref = "cb442f7c05fc3bfc34349c446010f452d2737ca0"
    checkout = tmp_path / "external" / "swatplus-pinned"
    cfg = Config(root=tmp_path, docs_source="pinned")
    cfg.sources["pinned"] = SourceProfile(
        name="pinned", ref="main", commit=ref, checkout=checkout
    )
    calls = []

    def fake_git(*args, cwd=None):
        calls.append(args)
        if args == ("init",):
            (cwd / ".git").mkdir(parents=True)
            (cwd / "src").mkdir()
        if args == ("rev-parse", "FETCH_HEAD") or args == ("rev-parse", "HEAD"):
            return ref
        if args == ("remote", "get-url", "origin"):
            return cfg.source_profile("pinned").repository
        return ""

    monkeypatch.setattr("swatplus_reference.source.fetch._git", fake_git)

    provenance = fetch_profile(cfg, "pinned")
    assert provenance.resolved_commit == ref
    assert ("fetch", "--depth", "1", "origin", "main") in calls
    assert ("checkout", "--detach", ref) in calls


def test_config_selects_independent_docs_and_schema_profiles(tmp_path):
    config_path = tmp_path / "swatref.toml"
    config_path.write_text(
        """
[sources.branch]
ref = "main"
checkout = "external/main"

[sources.release]
ref = "62.0.0"
commit = "de210d64db4f1d75e110bd6af33ea9c333d27b8a"
checkout = "external/release"

[docs]
source = "branch"

[schema]
source = "release"
version = "62.0.0"
""".strip(),
        encoding="utf-8",
    )

    cfg = load_config(config_path)
    assert cfg.source_profile().ref == "main"
    assert cfg.source_profile(cfg.schema.source).ref == "62.0.0"
    assert cfg.source_profile(cfg.schema.source).pinned_ref == (
        "de210d64db4f1d75e110bd6af33ea9c333d27b8a"
    )


def test_require_current_treats_affected_as_advisory():
    clean = SimpleNamespace(stale=[], affected=[], todo=[], orphaned=[], missing=[])
    assert _report_is_current(clean)

    affected = SimpleNamespace(
        stale=[], affected=["item"], todo=[], orphaned=[], missing=[]
    )
    assert _report_is_current(affected)

    for field in ("stale", "todo", "orphaned", "missing"):
        drifted = SimpleNamespace(stale=[], affected=[], todo=[], orphaned=[], missing=[])
        setattr(drifted, field, ["item"])
        assert not _report_is_current(drifted)


def test_status_only_blocks_affected_when_strict_option_is_selected(
    tmp_path, monkeypatch
):
    affected_page = SimpleNamespace(path=tmp_path / "affected.md")
    report = SimpleNamespace(
        stale=[],
        affected=[affected_page],
        affected_by={"affected.md": ["hub_module (dependency)"]},
        todo=[],
        orphaned=[],
        missing=[],
        summary=lambda: "affected=1",
    )
    monkeypatch.setattr("swatplus_reference.cli.get_store", lambda cfg: object())
    monkeypatch.setattr("swatplus_reference.cli.load_all", lambda path: [])
    monkeypatch.setattr(
        "swatplus_reference.docs.staleness.compute_status",
        lambda store, pages: report,
    )
    cfg = Config(root=tmp_path)

    advisory = SimpleNamespace(
        verbose=False, require_current=True, fail_on_affected=False
    )
    strict = SimpleNamespace(
        verbose=False, require_current=True, fail_on_affected=True
    )

    assert cmd_status(cfg, advisory) == 0
    assert cmd_status(cfg, strict) == 1


def test_normal_docs_parse_retains_and_prints_fparser_diagnostics(
    tmp_path, monkeypatch, capsys
):
    (tmp_path / "broken.f90").write_text(
        "subroutine broken(\nthis is not valid fortran ???\n",
        encoding="utf-8",
    )

    store, _rich = _parse_docs_with_diagnostics(tmp_path, "source-sha")

    assert store.fallback_files == ["broken.f90"]
    assert "broken.f90" in store.parse_errors
    monkeypatch.setattr(
        "swatplus_reference.cli.get_store",
        lambda cfg, refresh=False: FactStore(
            parse_errors=store.parse_errors,
            fallback_files=store.fallback_files,
        ),
    )
    assert cmd_parse(Config(root=tmp_path), SimpleNamespace()) == 0
    assert "fallback: broken.f90:" in capsys.readouterr().out


def test_rich_report_index_preserves_type_procedure_collisions():
    loc = SourceLocation("fixture.f90", 1, 2)
    proc = ProcedureDoc("cs_balance", "subroutine", loc)
    dtype = DerivedTypeDoc("cs_balance", loc)
    plain_type = DerivedTypeDoc("standalone", loc)
    rich = RichStore(
        ProjectIndex(
            project_name="fixture",
            source_root=".",
            procedures=[proc],
            types=[dtype, plain_type],
        )
    )

    index = _rich_report_index(rich)
    assert index["cs_balance"] is proc
    assert index["type::cs_balance"] is dtype
    assert index["standalone"] is plain_type


@pytest.mark.parametrize(
    "cache_state",
    ["missing", "mismatch", "stale_fparser", "stale_contract", "current"],
)
def test_docs_cache_requires_matching_rich_diagnostics(tmp_path, monkeypatch, cache_state):
    from swatplus_reference import cli
    from swatplus_reference.parser.documentation import RICH_DOCUMENTATION_PRODUCER
    from swatplus_reference.parser.rich import FPARSER_DIAGNOSTICS_METADATA_KEY

    source_ref = "a" * 40
    cfg = Config(root=tmp_path, source_dir=tmp_path, source_ref=source_ref)
    store = FactStore(
        source_ref=source_ref, producer=RICH_DOCUMENTATION_PRODUCER,
        parse_errors={"broken.f90": "bad expression"}, fallback_files=["broken.f90"],
        normalized_files={"signs.f90": [4, 9]},
    )
    expected = {
        "parse_errors": store.parse_errors,
        "fallback_files": store.fallback_files,
        "normalized_files": store.normalized_files,
        "fparser_version": fparser_version(),
    }
    stale = {
        "missing": None,
        # Diagnostics that disagree with the compact store.
        "mismatch": {"parse_errors": {}, "fallback_files": []},
        # Same diagnostics, but produced by an fparser we are no longer running.
        "stale_fparser": {**expected, "fparser_version": "0.0.0-not-installed"},
        # Compatible for explicit loading, but not current enough for cache reuse.
        "stale_contract": expected,
        "current": expected,
    }[cache_state]
    rich = RichStore(ProjectIndex("fixture", "."))
    if stale is not None:
        rich.index.metadata[FPARSER_DIAGNOSTICS_METADATA_KEY] = stale
    rich_path = tmp_path / ".swatref/docs/rich.json"
    store.save(cfg.abs_facts_path)
    rich.save(rich_path, provenance={"resolved_commit": source_ref})
    if cache_state == "stale_contract":
        payload = json.loads(rich_path.read_text(encoding="utf-8"))
        contract = payload["metadata"]["swatplus_reference_rich_snapshot"]
        contract.update(
            format=2,
            export="swatplus-reference-rich-v2",
            model="project-index-v1",
            parser="fortran-scanner-v1",
        )
        rich_path.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(cli, "activate_docs_source", lambda _: SimpleNamespace(
        to_dict=lambda: {"resolved_commit": source_ref}
    ))
    rebuilds = []

    def rebuild(*args):
        rebuilds.append(True)
        rich.index.metadata[FPARSER_DIAGNOSTICS_METADATA_KEY] = expected
        return store, rich

    monkeypatch.setattr(cli, "_parse_docs_with_diagnostics", rebuild)
    loaded = cli.get_store(cfg)
    assert loaded.parse_errors == store.parse_errors
    assert len(rebuilds) == (0 if cache_state == "current" else 1)
    assert RichStore.load(rich_path).index.metadata[FPARSER_DIAGNOSTICS_METADATA_KEY] == expected
