"""`swatref docs maintain`: propose writes only the proposal, apply writes only it."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import anthropic
import pytest

from swatplus_reference import cli, maintain
from swatplus_reference.cli import main
from swatplus_reference.docs.pages import Page, load_all, parse_page
from swatplus_reference.docs.staleness import compute_status
from swatplus_reference.parser.facts import FactStore, Symbol
from swatplus_reference.provenance.records import SourceProvenance
from swatplus_reference.source.config import Config

BODY = """\
<!-- facts:header -->

{name} does a thing.

## Bottom Line

Original bottom line for {name}.

## Algorithm

| Step | What happens |
| --- | --- |
| 1 | It does the thing. |
"""

REPO = "https://example.test/swatplus"
BASE = SourceProvenance("base", REPO, "v1", "", "a" * 40)
CANDIDATE = SourceProvenance("main", REPO, "v2", "", "b" * 40)
DELTAS = {
    "demo": {"bottom_line": "Revised bottom line for demo."},
    "other": {"bottom_line": "Revised bottom line for other."},
}
DEMO, OTHER = "docs/procedures/demo.md", "docs/procedures/other.md"


@dataclass
class Case:
    cfg: Config
    store: FactStore
    old_store: FactStore
    old_dir: Path
    new_dir: Path

    @property
    def root(self) -> Path:
        return self.cfg.root

    def snapshot(self) -> dict[str, bytes]:
        docs = self.cfg.abs_docs_dir
        return {p.relative_to(docs).as_posix(): p.read_bytes()
                for p in sorted(docs.rglob("*")) if p.is_file()}


def make_case(tmp_path: Path) -> Case:
    """Two stale pages (demo, other), one affected (caller), one stale io page.

    ``demo`` and ``other`` changed between base and candidate; ``caller`` did
    not, but it calls ``demo``.
    """
    docs, old_dir, new_dir = tmp_path / "docs", tmp_path / "old", tmp_path / "new"
    old_dir.mkdir()
    new_dir.mkdir()
    store, old_store = FactStore(source_ref="b" * 40), FactStore(source_ref="a" * 40)
    for name, changed in (("demo", True), ("other", True), ("caller", False)):
        (old_dir / f"{name}.f90").write_text(f"subroutine {name}\n  x = 1\nend subroutine {name}\n")
        new_x = 2 if changed else 1
        (new_dir / f"{name}.f90").write_text(
            f"subroutine {name}\n  x = {new_x}\nend subroutine {name}\n")
        old_hash = f"{name}-old" if changed else f"{name}-same"
        new_hash = f"{name}-new" if changed else f"{name}-same"
        calls = ["demo"] if name == "caller" else []
        for s, h in ((old_store, old_hash), (store, new_hash)):
            s.add(Symbol(kind="subroutine", name=name, file=f"{name}.f90",
                         start_line=1, end_line=3, source_hash=h, calls=calls))
        Page(path=docs / "procedures" / f"{name}.md", kind="procedure", symbol=name,
             title=name, status="filled", source_hash=old_hash,
             version_label="SWAT+ OLD", body=BODY.format(name=name)).save()
    Page(path=docs / "io" / "demo_input.md", kind="io", source_symbols=["demo"],
         title="demo_input", status="filled", source_hash="composite-old",
         body="Read by demo.").save()
    cfg = Config(root=tmp_path, docs_dir=docs, source_dir=new_dir, version_label="SWAT+ NEW")
    return Case(cfg, store, old_store, old_dir, new_dir)


class Generate:
    """A delta generator that records each request."""

    def __init__(self, deltas: dict):
        self.deltas = deltas
        self.calls: list[str] = []

    def __call__(self, req) -> dict:
        self.calls.append(req.page.symbol)
        return self.deltas[req.page.symbol]


GENERATOR = {"kind": "deltas_file", "path": "deltas.json", "sha256": "0" * 64}


def propose(case: Case, deltas=DELTAS, generate=None, **kwargs):
    generate = generate or Generate(deltas)
    proposal = maintain.propose(case.cfg, case.store, case.old_store, case.old_dir,
                                BASE, CANDIDATE, generate, GENERATOR, **kwargs)
    return generate, proposal


def entry(proposal: dict, path: str) -> dict:
    return next(p for p in proposal["pages"] if p["path"] == path)


def apply(case: Case, proposal: dict, candidate=CANDIDATE):
    return maintain.apply(case.cfg, case.store, candidate, proposal)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------
# propose
# --------------------------------------------------------------------------

def test_propose_leaves_the_docs_tree_byte_for_byte_unchanged(tmp_path):
    case = make_case(tmp_path)
    before = case.snapshot()
    propose(case)
    assert case.snapshot() == before


def test_propose_generates_once_per_stale_page_and_records_why(tmp_path):
    case = make_case(tmp_path)
    generate, proposal = propose(case)

    assert sorted(generate.calls) == ["demo", "other"]
    assert proposal["format"] == maintain.FORMAT
    assert proposal["base"]["resolved_commit"] == "a" * 40
    assert proposal["candidate"]["resolved_commit"] == "b" * 40

    demo = entry(proposal, DEMO)
    original = (tmp_path / DEMO).read_bytes()
    assert demo["status"] == "ready"
    assert demo["symbol"] == "demo"
    assert demo["page_sha256"] == sha256(original)
    assert (demo["old_source_hash"], demo["new_source_hash"]) == ("demo-old", "demo-new")
    diff = demo["evidence"][0]["diff"]
    assert "-  x = 1" in diff and "+  x = 2" in diff
    assert demo["delta"] == DELTAS["demo"]
    assert demo["changed_fields"] == ["bottom_line"]
    assert demo["grounding"] == {"errors": [], "warnings": []}
    assert "+Revised bottom line for demo." in demo["patch"]
    assert demo["proposed_sha256"] == sha256(demo["proposed"].encode("utf-8"))

    proposed = parse_page(tmp_path / DEMO, demo["proposed"])
    assert (proposed.status, proposed.source_hash, proposed.version_label) == (
        "filled", "demo-new", "SWAT+ NEW")
    assert "## Algorithm" in proposed.body  # untouched sections carried over


def test_affected_and_unsupported_pages_are_listed_but_never_proposed(tmp_path):
    case = make_case(tmp_path)
    _, proposal = propose(case)

    assert {p["path"] for p in proposal["pages"]} == {DEMO, OTHER}
    assert proposal["review_only"] == [
        {"path": "docs/procedures/caller.md", "symbol": "caller", "changed": ["demo"]}]
    assert [m["path"] for m in proposal["manual"]] == ["docs/io/demo_input.md"]

    before = case.snapshot()
    ok, _ = apply(case, proposal)
    after = case.snapshot()
    assert ok
    assert after["procedures/caller.md"] == before["procedures/caller.md"]
    assert after["io/demo_input.md"] == before["io/demo_input.md"]


def test_wrong_baseline_is_refused_without_generating(tmp_path):
    case = make_case(tmp_path)
    case.old_store.add(Symbol(kind="subroutine", name="demo", file="demo.f90",
                              start_line=1, end_line=3, source_hash="unrelated"))
    generate, proposal = propose(case)

    demo = entry(proposal, DEMO)
    assert demo["status"] == "refused"
    assert "baseline" in demo["reason"]
    assert generate.calls == ["other"]
    assert maintain.has_failures(proposal)


def test_declined_and_failing_generation_is_recorded_per_page(tmp_path):
    case = make_case(tmp_path)

    def generate(req):
        if req.page.symbol == "demo":
            raise maintain.Declined("the model declined")
        raise RuntimeError("boom")

    _, proposal = propose(case, generate=generate)
    assert (entry(proposal, DEMO)["status"], entry(proposal, DEMO)["reason"]) == (
        "refused", "the model declined")
    assert (entry(proposal, OTHER)["status"], entry(proposal, OTHER)["reason"]) == (
        "error", "RuntimeError: boom")


def test_deltas_file_generator_records_its_source(tmp_path):
    case = make_case(tmp_path)
    path = tmp_path / "deltas.json"
    path.write_text(json.dumps({"other": DELTAS["other"]}))
    generate, info = maintain.deltas_generator(path, tmp_path)
    _, proposal = propose(case, generate=generate)

    assert info == {"kind": "deltas_file", "path": "deltas.json",
                    "sha256": sha256(path.read_bytes())}
    assert entry(proposal, OTHER)["status"] == "ready"
    assert entry(proposal, DEMO)["reason"] == "no delta for `demo` in deltas.json"


# --------------------------------------------------------------------------
# grounding: errors block, warnings stay visible
# --------------------------------------------------------------------------

def test_grounding_errors_block_the_page_and_warnings_stay_visible(tmp_path):
    case = make_case(tmp_path)
    _, proposal = propose(case, deltas={
        "demo": {"bottom_line": "Calls [sym:no_such_routine] daily."},
        "other": {"bottom_line": "Reads `mystery_var` daily."},
    })
    demo, other = entry(proposal, DEMO), entry(proposal, OTHER)
    assert demo["status"] == "rejected"
    assert [e["code"] for e in demo["grounding"]["errors"]] == ["broken-sym-ref"]
    assert other["status"] == "ready"
    assert [w["code"] for w in other["grounding"]["warnings"]] == ["unknown-backtick"]
    assert maintain.has_failures(proposal)

    preview = maintain.render(proposal)
    assert f"REJECTED {DEMO}" in preview and "broken-sym-ref" in preview
    assert "unknown-backtick" in preview

    demo_before = (tmp_path / DEMO).read_bytes()
    ok, lines = apply(case, proposal)
    assert ok
    assert (tmp_path / DEMO).read_bytes() == demo_before
    assert (tmp_path / OTHER).read_bytes() == other["proposed"].encode("utf-8")
    assert f"NOT APPLIED {DEMO}: rejected in the proposal" in lines
    assert any(line.startswith(f"APPLIED {OTHER}") and "unknown-backtick" in line
               for line in lines)


# --------------------------------------------------------------------------
# apply
# --------------------------------------------------------------------------

def test_apply_writes_exactly_the_previewed_bytes_without_generating(tmp_path, monkeypatch):
    case = make_case(tmp_path)
    generate, proposal = propose(case)
    stored = tmp_path / "proposal.json"
    maintain.write_proposal(stored, proposal)

    def no_model(*args, **kwargs):
        raise AssertionError("apply must not call the model")

    monkeypatch.setattr(anthropic, "Anthropic", no_model)
    before = case.snapshot()

    ok, lines = apply(case, maintain.load_proposal(stored))

    assert ok, lines
    after = case.snapshot()
    assert {k for k in after if after[k] != before[k]} == {
        "procedures/demo.md", "procedures/other.md"}
    for page in proposal["pages"]:
        assert (tmp_path / page["path"]).read_bytes() == page["proposed"].encode("utf-8")
    assert len(generate.calls) == 2  # nothing generated after propose
    stale = compute_status(case.store, load_all(case.cfg.abs_docs_dir)).stale
    assert [p.name for p in stale if p.symbol] == []


def test_applying_twice_is_a_no_op(tmp_path):
    case = make_case(tmp_path)
    _, proposal = propose(case)
    assert apply(case, proposal)[0]
    once = case.snapshot()

    ok, lines = apply(case, proposal)

    assert ok
    assert f"ALREADY APPLIED {DEMO}" in lines
    assert case.snapshot() == once


def test_apply_refuses_a_proposal_made_for_another_candidate_commit(tmp_path):
    case = make_case(tmp_path)
    _, proposal = propose(case)
    before = case.snapshot()

    moved = SourceProvenance("main", REPO, "v2", "", "c" * 40)
    ok, lines = apply(case, proposal, candidate=moved)

    assert not ok
    assert lines[0].startswith("REFUSED: the proposal was made for main @ bbbbbbbbbbbb")
    assert case.snapshot() == before


def test_apply_writes_nothing_when_any_page_changed_after_preview(tmp_path):
    case = make_case(tmp_path)
    _, proposal = propose(case)
    edited = tmp_path / OTHER
    edited.write_bytes(edited.read_bytes() + b"\nA reviewer's edit.\n")
    before = case.snapshot()

    ok, lines = apply(case, proposal)

    assert not ok
    assert any(f"REFUSED {OTHER}: page changed since the proposal" in line for line in lines)
    assert case.snapshot() == before  # demo was fine, but it is not written either


def test_apply_refuses_when_a_symbol_changed_after_preview(tmp_path):
    case = make_case(tmp_path)
    _, proposal = propose(case)
    case.store.add(Symbol(kind="subroutine", name="demo", file="demo.f90",
                          start_line=1, end_line=3, source_hash="demo-newer"))
    before = case.snapshot()

    ok, lines = apply(case, proposal)

    assert not ok
    assert any("the source of `demo` changed since the proposal" in line for line in lines)
    assert case.snapshot() == before


def _tamper_text(page):
    page["proposed"] += "\nSlipped in after review.\n"


def _escape_docs(page):
    page["path"] = "notes.md"


def _ungrounded_but_rehashed(page):
    page["proposed"] = page["proposed"].replace("Revised", "[sym:nope] Revised")
    page["proposed_sha256"] = sha256(page["proposed"].encode("utf-8"))


def _incomplete(page):
    del page["new_source_hash"]


@pytest.mark.parametrize("tamper, message", [
    (_tamper_text, "proposed content does not match its recorded hash"),
    (_escape_docs, "is not under the docs directory"),
    (_ungrounded_but_rehashed, "broken-sym-ref"),
    (_incomplete, "proposal entry is incomplete"),
])
def test_apply_rejects_tampered_or_invalid_entries(tmp_path, tamper, message):
    case = make_case(tmp_path)
    _, proposal = propose(case)
    tamper(entry(proposal, DEMO))
    before = case.snapshot()

    ok, lines = apply(case, proposal)

    assert not ok
    assert any(message in line for line in lines)
    assert case.snapshot() == before
    assert not (tmp_path / "notes.md").exists()


def test_load_proposal_rejects_missing_and_foreign_files(tmp_path):
    with pytest.raises(FileNotFoundError, match="maintain propose"):
        maintain.load_proposal(tmp_path / "missing.json")
    foreign = tmp_path / "foreign.json"
    foreign.write_text(json.dumps({"format": "something-else"}))
    with pytest.raises(ValueError, match="swatref-maintain-proposal/1"):
        maintain.load_proposal(foreign)


# --------------------------------------------------------------------------
# CLI: `swatref docs maintain`
# --------------------------------------------------------------------------

@pytest.fixture
def cli_case(tmp_path, monkeypatch):
    """`main()` against make_case, with profile resolution and parsing stubbed."""
    case = make_case(tmp_path)
    config = tmp_path / "swatref.toml"
    config.write_text('[docs]\npages = "docs"\n')
    profiles = {"main": (case.new_dir, CANDIDATE), "base": (case.old_dir, BASE)}

    def get_store(cfg, refresh=False):
        cfg.source_dir, cfg.version_label = case.new_dir, "SWAT+ NEW"
        return case.store

    monkeypatch.setattr(cli, "get_store", get_store)
    monkeypatch.setattr(cli, "resolve_profile", lambda cfg, name: profiles[name])
    monkeypatch.setattr(cli, "parse_documentation",
                        lambda *args, **kwargs: (case.old_store, None))
    deltas = tmp_path / "deltas.json"
    deltas.write_text(json.dumps(DELTAS))

    def run(*args):
        return main(["--config", str(config), "docs", "maintain", *args])

    return case, run, deltas


def test_docs_maintain_is_a_real_subcommand(tmp_path, capsys):
    config = tmp_path / "swatref.toml"
    config.write_text("")
    with pytest.raises(SystemExit) as exit_info:
        main(["--config", str(config), "docs", "maintain", "--help"])
    assert exit_info.value.code == 0
    assert "{propose,show,apply}" in capsys.readouterr().out


def test_cli_propose_show_apply_round_trip(cli_case, capsys):
    case, run, deltas = cli_case
    before = case.snapshot()

    assert run("propose", "--base", "base", "--deltas", str(deltas)) == 0
    proposed = capsys.readouterr().out
    assert f"READY {DEMO}" in proposed
    assert "wrote reports/maintain/proposal.json" in proposed
    assert case.snapshot() == before

    assert run("show") == 0
    assert f"READY {DEMO}" in capsys.readouterr().out

    assert run("apply") == 0
    stored = maintain.load_proposal(case.root / "reports" / "maintain" / "proposal.json")
    assert (case.root / DEMO).read_bytes() == entry(stored, DEMO)["proposed"].encode("utf-8")


def test_cli_propose_requires_a_distinct_base(cli_case):
    _, run, deltas = cli_case
    with pytest.raises(SystemExit, match="--base PROFILE is required"):
        run("propose", "--deltas", str(deltas))
    with pytest.raises(SystemExit, match="is the docs source itself"):
        run("propose", "--base", "main", "--deltas", str(deltas))


def test_cli_apply_fails_when_verification_fails(cli_case, capsys):
    case, run, deltas = cli_case
    run("propose", "--base", "base", "--deltas", str(deltas))
    (case.root / DEMO).write_text("edited after preview\n")
    capsys.readouterr()

    assert run("apply") == 1
    assert "page changed since the proposal" in capsys.readouterr().out
