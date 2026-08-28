from pathlib import Path
from types import SimpleNamespace

from swatplus_reference.cli import _rel, _report_is_current, _rich_report_index
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


def test_require_current_rejects_every_drift_bucket():
    clean = SimpleNamespace(stale=[], affected=[], todo=[], orphaned=[], missing=[])
    assert _report_is_current(clean)

    for field in ("stale", "affected", "todo", "orphaned", "missing"):
        drifted = SimpleNamespace(stale=[], affected=[], todo=[], orphaned=[], missing=[])
        setattr(drifted, field, ["item"])
        assert not _report_is_current(drifted)


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
