from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest

from swatplus_reference.docs.pages import Page, load_page
from swatplus_reference.generation import refill
from swatplus_reference.parser.facts import FactStore, Symbol
from swatplus_reference.source.config import Config

# A curated page: fill-managed sections plus additional sections
# (Theory Equations, Lineage) that the fill template never emits.
MIGRATED_BODY = """\
<!-- facts:header -->

Short description here.

## Bottom Line

Bottom line paragraph one.

Bottom line paragraph two.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs in the daily loop after setup.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. do a thing | It does the thing. |

## Modules Used

<!-- facts:uses -->

## Local Variables

<!-- facts:locals -->

## State Changes

*Not documented.*

## File I/O

<!-- facts:io -->

## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:2.3 | A law | $x=y$ | matches. |

## Lineage

Introduced in abc123; changed twice since.

## Review Notes

- a review note
"""


def make_page(tmp: Path) -> Page:
    p = Path(tmp) / "procedures" / "demo.md"
    return Page(
        path=p,
        kind="procedure",
        symbol="demo",
        title="demo",
        status="filled",
        source_hash="oldhash0000000",
        body=MIGRATED_BODY,
        extra={
            "locals": {"j": "counter note", "wrk": "accumulator note"},
            "uses": {"demo_module": "provides state"},
        },
    )


def sym(hash="newhash1111111") -> Symbol:
    return Symbol(kind="subroutine", name="demo", file="demo.f90",
                  start_line=1, end_line=9, source_hash=hash)


def section(body: str, anchor: str) -> str:
    lines = body.splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip() == anchor)
    out = []
    for l in lines[i + 1:]:
        if l.strip().startswith("## ") or l.strip().startswith("<!-- facts:"):
            break
        out.append(l)
    return "\n".join(out).strip()


class RoundTrip:
    pass


def test_page_to_data_extracts_clean_prose(tmp_path):
    data = refill.page_to_data(make_page(tmp_path))
    assert data["short_description"] == "Short description here."
    assert data["bottom_line"].startswith("Bottom line paragraph one.")
    # bottom_line must NOT swallow the following ## Arguments section
    assert "## Arguments" not in data["bottom_line"]
    assert data["where_it_fits"] == "Runs in the daily loop after setup."
    assert data["algorithm"] == [{"step": "1. do a thing", "behavior": "It does the thing."}]
    assert data["state_changes"] == []
    assert {"name": "j", "note": "counter note"} in data["local_notes"]


def test_splice_changes_only_named_section(tmp_path):
    page = make_page(tmp_path)
    sym_new = sym()
    orig = page.body
    refill.splice_delta(page, sym_new, {"bottom_line": "REVISED bottom line."})
    assert "REVISED bottom line." in page.body
    # every other section byte-identical
    for anchor in ("## Where It Fits", "## Algorithm", "## Theory Equations",
                   "## Lineage", "## Review Notes"):
        assert section(orig, anchor) == section(page.body, anchor)
    # source_hash advanced to the new symbol
    assert page.source_hash == "newhash1111111"


def test_splice_preserves_additional_curated_sections(tmp_path):
    page = make_page(tmp_path)
    refill.splice_delta(page, sym(), {"short_description": "New desc.",
                                      "where_it_fits": "New fit."})
    for marker in ("## Theory Equations", "$x=y$", "## Lineage", "abc123",
                   "## Review Notes", "a review note"):
        assert marker in page.body


def test_note_delta_updates_named_entry_only(tmp_path):
    page = make_page(tmp_path)
    refill.splice_delta(page, sym(), {"local_notes": [{"name": "j", "note": "NEW j note"}]})
    assert page.extra["locals"]["j"] == "NEW j note"
    assert page.extra["locals"]["wrk"] == "accumulator note"  # untouched


def test_absent_section_is_not_invented(tmp_path):
    page = make_page(tmp_path)
    # module-only field with no section on this page -> no-op, no crash
    before = page.body
    refill.splice_delta(page, sym(), {"variable_notes": [{"name": "x", "note": "n"}]})
    assert page.body == before  # body untouched; variables map added to extra is fine
    assert page.source_hash == "newhash1111111"


def test_omitted_fields_are_untouched(tmp_path):
    page = make_page(tmp_path)
    orig = page.body
    refill.splice_delta(page, sym(), {})  # empty delta
    assert page.body == orig  # nothing changed except source_hash


def test_symbol_source_diff(tmp_path):
    old_dir = tmp_path / "old" / ""
    new_dir = tmp_path / "new"
    (old_dir).mkdir(parents=True)
    new_dir.mkdir(parents=True)
    (old_dir / "demo.f90").write_text("line1\nold body\nline3\n")
    (new_dir / "demo.f90").write_text("line1\nnew body\nline3\n")
    s = Symbol(kind="subroutine", name="demo", file="demo.f90", start_line=1, end_line=3)
    diff = refill.symbol_source_diff(s, s, old_dir, new_dir)
    assert "-old body" in diff and "+new body" in diff


def test_apply_delta_file_key_free(tmp_path):
    # a page on disk + a fact store + a hand-authored delta json
    docs = tmp_path / "docs"
    (docs / "procedures").mkdir(parents=True)
    page = make_page(docs)
    page.save()
    store = FactStore(source_ref="t")
    store.add(sym())
    from swatplus_reference.source.config import Config
    cfg = Config(root=tmp_path, docs_dir=docs)
    deltas = tmp_path / "d.json"
    deltas.write_text(json.dumps({"demo": {"bottom_line": "FROM DELTA FILE."}}))
    results = refill.apply_delta_file(cfg, store, deltas)
    assert any("REFILLED demo" in r for r in results)
    assert "FROM DELTA FILE." in page.path.read_text()
    # Additional curated sections still present after a key-free apply.
    assert "## Theory Equations" in page.path.read_text()


# --------------------------------------------------------------------------
# Refill gates: stale only, verified baseline, grounded writes, per-page errors
# --------------------------------------------------------------------------

def refill_case(tmp_path, names=("demo",), old_hash="oldhash0000000"):
    """Stale pages on disk plus old/new source trees and their fact stores.

    Every page records ``oldhash0000000``. The new store has moved on to
    ``newhash1111111``; the old store hashes to ``old_hash``, which is the
    page's baseline unless a test overrides it.
    """
    docs, old_dir, new_dir = tmp_path / "docs", tmp_path / "old", tmp_path / "new"
    old_dir.mkdir()
    new_dir.mkdir()
    store, old_store, paths = FactStore(source_ref="new"), FactStore(source_ref="old"), []
    for name in names:
        page = make_page(docs)
        page.path, page.symbol, page.title = docs / "procedures" / f"{name}.md", name, name
        page.status = "stale"
        page.save()
        paths.append(page.path)
        (old_dir / f"{name}.f90").write_text(f"subroutine {name}\n  x = 1\nend subroutine {name}\n")
        (new_dir / f"{name}.f90").write_text(f"subroutine {name}\n  x = 2\nend subroutine {name}\n")
        for s, h in ((store, "newhash1111111"), (old_store, old_hash)):
            s.add(Symbol(kind="subroutine", name=name, file=f"{name}.f90",
                         start_line=1, end_line=3, source_hash=h))
    cfg = Config(root=tmp_path, docs_dir=docs, source_dir=new_dir, version_label="SWAT+ NEW")
    return cfg, store, old_store, old_dir, paths


class FakeClient:
    """Stands in for anthropic.Anthropic(): canned reply text per symbol."""

    def __init__(self, replies: dict[str, str]):
        self.replies = replies
        self.prompts: list[str] = []
        self.messages = self

    def create(self, **kwargs):
        prompt = kwargs["messages"][0]["content"]
        self.prompts.append(prompt)
        text = next(t for name, t in self.replies.items() if f"# Symbol: {name} " in prompt)
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text=text)])


def run_refill_with(monkeypatch, replies, cfg, store, old_store, old_dir, paths):
    client = FakeClient(replies)
    monkeypatch.setattr(anthropic, "Anthropic", lambda: client)
    return client, refill.run_refill(cfg, store, old_store, old_dir, paths)


def apply_deltas(tmp_path, cfg, store, deltas):
    path = tmp_path / "deltas.json"
    path.write_text(json.dumps(deltas))
    return refill.apply_delta_file(cfg, store, path)


def test_grounding_error_blocks_the_write(tmp_path):
    cfg, store, _old, _dir, (path,) = refill_case(tmp_path)
    before = path.read_bytes()
    results = apply_deltas(tmp_path, cfg, store,
                           {"demo": {"bottom_line": "Calls [sym:no_such_routine] daily."}})
    assert results[0].startswith("REJECTED demo")
    assert "broken-sym-ref" in results[0]
    assert path.read_bytes() == before
    assert refill.has_failures(results)


def test_grounding_warnings_are_reported_but_do_not_block(tmp_path):
    cfg, store, _old, _dir, (path,) = refill_case(tmp_path)
    results = apply_deltas(tmp_path, cfg, store,
                           {"demo": {"bottom_line": "Reads `mystery_var` daily."}})
    assert results[0].startswith("REFILLED demo")
    assert "grounding warnings: 1" in results[0]
    assert "`mystery_var`" in path.read_text()
    assert not refill.has_failures(results)


def test_empty_fields_leave_reviewed_sections_untouched(tmp_path):
    page = make_page(tmp_path)
    body, notes = page.body, dict(page.extra["locals"])
    refill.splice_delta(page, sym(), {"short_description": "", "algorithm": [],
                                      "state_changes": [], "local_notes": []})
    assert page.body == body  # the Algorithm table in particular survives
    assert page.extra["locals"] == notes


def test_refill_marks_the_page_filled_at_the_new_version(tmp_path):
    cfg, store, _old, _dir, (path,) = refill_case(tmp_path)
    apply_deltas(tmp_path, cfg, store, {"demo": {"bottom_line": "Revised."}})
    page = load_page(path)
    assert (page.status, page.version_label, page.source_hash) == (
        "filled", "SWAT+ NEW", "newhash1111111")


@pytest.mark.parametrize("status, source_hash", [
    ("filled", "newhash1111111"),  # current: its own source is unchanged
    ("todo", ""),                  # never filled: that is `fill`'s job
])
def test_pages_that_are_not_stale_are_never_rewritten(tmp_path, monkeypatch, status, source_hash):
    cfg, store, old_store, old_dir, (path,) = refill_case(tmp_path)
    page = load_page(path)
    page.status, page.source_hash = status, source_hash
    page.save()
    before = path.read_bytes()

    applied = apply_deltas(tmp_path, cfg, store, {"demo": {"bottom_line": "Rewritten."}})
    client, refilled = run_refill_with(monkeypatch, {"demo": "{}"},
                                       cfg, store, old_store, old_dir, [path])

    assert applied[0].startswith("SKIP demo: not stale")
    assert refilled[0].startswith("SKIP demo: not stale")
    assert client.prompts == []
    assert path.read_bytes() == before


def test_refill_refuses_an_old_source_that_is_not_the_page_baseline(tmp_path, monkeypatch):
    cfg, store, old_store, old_dir, (path,) = refill_case(tmp_path, old_hash="unrelated00000")
    before = path.read_bytes()

    client, refilled = run_refill_with(monkeypatch, {"demo": '{"bottom_line": "x"}'},
                                       cfg, store, old_store, old_dir, [path])
    prompts = refill.emit_delta_prompts(cfg, store, old_store, old_dir, [path],
                                        tmp_path / "prompts")

    for results in (refilled, prompts):
        assert results[0].startswith("REFUSED demo: the old source is not the baseline")
        assert "unrelated00000" in results[0]
        assert refill.has_failures(results)
    assert client.prompts == []
    assert not list((tmp_path / "prompts").iterdir())
    assert path.read_bytes() == before


def test_one_failing_page_does_not_stop_the_batch(tmp_path, monkeypatch):
    cfg, store, old_store, old_dir, paths = refill_case(tmp_path, names=("demo", "other"))
    other_before = paths[1].read_bytes()

    client, results = run_refill_with(
        monkeypatch, {"demo": '{"bottom_line": "Revised."}', "other": "not json"},
        cfg, store, old_store, old_dir, paths,
    )

    assert results[0].startswith("REFILLED demo [bottom_line]")
    assert results[1].startswith("ERROR other: JSONDecodeError")
    assert "Revised." in paths[0].read_text()
    assert paths[1].read_bytes() == other_before
    assert refill.has_failures(results)
    # the model saw this symbol's own old -> new diff
    assert any("-  x = 1" in p and "+  x = 2" in p for p in client.prompts)
