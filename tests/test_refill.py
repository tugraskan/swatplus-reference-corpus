from __future__ import annotations

import json
from pathlib import Path

from swatplus_reference.docs.pages import Page
from swatplus_reference.generation import refill
from swatplus_reference.parser.facts import FactStore, Symbol

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
