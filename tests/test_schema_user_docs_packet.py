"""Evidence packet and pass/fail check for one user-docs input table."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from swatplus_reference import cli
from swatplus_reference.cli import main
from swatplus_reference.provenance.records import SourceProvenance
from swatplus_reference.schema.user_docs_packet import (
    ApplyError,
    apply_packet,
    build_packet,
    check_tables,
    comment_lines,
    render_packet,
)

COMMIT = "c" * 40
PROVENANCE = {"profile": "release_62_0_1", "repository": "https://example.test/swatplus",
              "resolved_commit": COMMIT}

MODULE = """\
module basin_module
  type basin_codes
    character(len=16) :: petfile = ""  !! potential et filename
    integer :: event = 0   !! extra columns switch
    integer :: idc_till = 3  !! 1 = dssat tillage method
                             !! 2 = epic tillage method
  end type basin_codes
end module basin_module
"""
READER = """\
subroutine basin_read_cc
  use basin_module
  open (107,file="codes.bsn")
  read (107,*) titldum
  read (107,*) header
  read (107,*) bsn_cc
end subroutine basin_read_cc
"""
DEAD_READER = """\
subroutine dead_read
  open (108,file="dead.dat")
  read (108,*) titldum
  read (108,*) dead_db
end subroutine dead_read
"""
CALLER = """\
subroutine proc_bsn
  external :: dead_read
  ! call dead_read   (commented out, does not count)
  call basin_read_cc
end subroutine proc_bsn
"""
TABLE = """\
---
description: Control codes.
---

# codes.bsn

| Field | Description | Type |
| --- | --- | --- |
| [pet\\_file](pet_file.md) | PET file | string |
| event | Extra columns | integer |
"""


def field(name: str, ftype: str) -> dict:
    return {"doc": None, "fortran_name": name, "fortran_type": ftype,
            "numeric": ftype != "character", "position": 0, "units": None}


SCHEMA = {
    "swatplus_version": "62.0.1",
    "files": {
        "codes.bsn": {
            "derived_type": "basin_codes", "read_pattern": "derived_type",
            "reader": "basin_read_cc.f90", "reader_line": 6,
            "type_source": "basin_module.f90:2-7",
            "fields": [field("petfile", "character"), field("event", "integer"),
                       field("idc_till", "integer")],
        },
        "dead.dat": {
            "derived_type": "dead_db", "read_pattern": "derived_type",
            "reader": "dead_read.f90", "reader_line": 4,
            "fields": [field("name", "character")],
        },
    },
}
FIELD_MAP = {"files": {"codes.bsn": [
    {"source": {"name": "petfile"}, "editor_database": {"name": "pet_file"}}]}}


def make_tree(tmp_path: Path) -> tuple[Path, Path]:
    """A SWAT+ source tree and a docs checkout with one stale table."""
    src = tmp_path / "swatplus" / "src"
    src.mkdir(parents=True)
    for name, text in (("basin_module.f90", MODULE), ("basin_read_cc.f90", READER),
                       ("dead_read.f90", DEAD_READER), ("proc_bsn.f90", CALLER)):
        (src / name).write_text(text)
    docs = tmp_path / "SWATPlus-user-documentation"
    table = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn"
    table.mkdir(parents=True)
    (table / "README.md").write_text(TABLE)
    (table / "pet_file.md").write_text("---\ndescription: PET file\n---\n\n# pet\\_file\n")
    (docs / "io-docs" / "introduction-1" / "dead.dat.md").write_text("# dead.dat\n\nNo table.\n")
    (docs / "io-docs" / "SUMMARY.md").write_text(
        "* [codes.bsn](introduction-1/basin/codes.bsn/README.md)\n"
        "  * [pet\\_file](introduction-1/basin/codes.bsn/pet_file.md)\n")
    return src, docs


def add_idc_till(docs: Path, register: bool = True, front_matter: bool = True) -> Path:
    table = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn"
    readme = table / "README.md"
    readme.write_text(readme.read_text() + "| [idc\\_till](idc_till.md) | Tillage method | integer |\n")
    page = table / "idc_till.md"
    page.write_text(("---\ndescription: Tillage method\n---\n\n" if front_matter else "")
                    + "# idc\\_till\n")
    if register:
        summary = docs / "io-docs" / "SUMMARY.md"
        summary.write_text(summary.read_text()
                           + "  * [idc\\_till](introduction-1/basin/codes.bsn/idc_till.md)\n")
    return page.resolve()


# --------------------------------------------------------------------------
# packet
# --------------------------------------------------------------------------

def test_packet_places_the_missing_row_and_quotes_its_declaration(tmp_path):
    src, docs = make_tree(tmp_path)
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    idc = packet["fields"][2]
    assert idc["docs_row"] is None
    assert idc["insert"] == "after line 10 (the event row)"
    assert idc["declaration"] == {
        "at": "basin_module.f90:5-6",
        "text": ["integer :: idc_till = 3  !! 1 = dssat tillage method",
                 "!! 2 = epic tillage method"],
    }
    assert packet["fields"][0]["docs_row"] == {"line": 9, "field": "pet_file", "match": "same name"}
    assert packet["reader"]["called_from"] == ["proc_bsn.f90:4"]
    assert packet["reader"]["statement"] == [(6, "  read (107,*) bsn_cc")]
    assert [d["line"] for d in packet["docs_rows"]] == [9, 10]
    assert packet["differences"] == {"missing_from_docs": ["idc_till"]}

    text = render_packet(packet)
    assert "**MISSING**, insert after line 10 (the event row)" in text
    assert "!! 2 = epic tillage method" in text
    assert "probably" not in text  # nothing sits where idc_till goes


def test_packet_pairs_an_unread_row_with_the_missing_field_in_its_place(tmp_path):
    # pet_file is missing too, so positions no longer line up (as `order` does
    # in hyd-sed-lte.cha) and only the insertion point pairs till_meth.
    src, docs = make_tree(tmp_path)
    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    readme.write_text(TABLE.replace("| [pet\\_file](pet_file.md) | PET file | string |\n", "")
                      + "| [till\\_meth](till_meth.md) | Old name | integer |\n")
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    assert packet["fields"][0]["insert"] == "before line 9 (as the first row)"
    assert "probably_replaces" not in packet["fields"][0]  # event is read, not replaced
    assert packet["fields"][2]["probably_replaces"] == "till_meth"
    assert [(d["field"], d["read_by_source"], d["probably_replaced_by"])
            for d in packet["docs_rows"]] == [("event", True, None),
                                               ("till_meth", False, "idc_till")]
    text = render_packet(packet)
    assert "insert after line 9 (the event row); probably replaces `till_meth`" in text
    assert "NOT READ BY THE SOURCE (probably replaced by `idc_till`: rename its field page)" in text


def test_packet_says_when_a_reader_never_runs(tmp_path):
    src, docs = make_tree(tmp_path)
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "dead.dat", FIELD_MAP)
    # dead.dat has a page but no Field table, so there is nothing to place
    assert packet["status"] == "no_field_table"
    assert "no Field table" in render_packet(packet)

    src_only = build_packet(
        {**SCHEMA, "files": {**SCHEMA["files"], "codes.bsn": {**SCHEMA["files"]["codes.bsn"],
                                                            "reader": "dead_read.f90"}}},
        PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)
    assert src_only["reader"]["called_from"] == []  # `external ::` and comments do not count
    assert "nothing (the reader never runs" in render_packet(src_only)


def test_comment_lines_drop_the_bangs_and_the_units_column():
    decl = {"text": ["real :: pl_uptake = 0.  !! none   |fraction taken up by plant", "!! (0-1)"]}
    assert comment_lines(decl) == ["fraction taken up by plant", "(0-1)"]
    assert comment_lines(None) == []


def test_pasting_the_exact_text_passes_the_check(tmp_path):
    src, docs = make_tree(tmp_path)
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)
    assert packet["moves"] == [] and packet["row_edits"] == []
    [x] = packet["exact_text"]
    assert x["row"] == "| [idc\\_till](idc_till.md) | 1 = dssat tillage method; 2 = epic tillage method | integer |"
    assert x["table"] == "insert after line 10 (the event row)"
    assert x["named_after"] == "the Fortran variable"
    assert x["page_action"] == "create io-docs/introduction-1/basin/codes.bsn/idc_till.md with"
    # event has no page, so the new entry goes after pet_file's
    assert x["summary"] == "insert after line 2 (`* [pet\\_file](introduction-1/basin/codes.bsn/pet_file.md)`)"
    assert x["summary_line"] == "  * [idc\\_till](introduction-1/basin/codes.bsn/idc_till.md)"  # its siblings' indent
    assert "1 = dssat tillage method; 2 = epic" in render_packet(packet)

    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    lines = readme.read_text().splitlines()
    readme.write_text("\n".join(lines[:10] + [x["row"]] + lines[10:]) + "\n")
    page = docs / "io-docs" / x["page"]
    page.write_text(x["page_text"])
    summary = docs / "io-docs" / "SUMMARY.md"
    s = summary.read_text().splitlines()
    summary.write_text("\n".join(s[:2] + [x["summary_line"]] + s[2:]) + "\n")
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP,
                             new_pages={page.resolve()})
    assert ok, lines


def test_packet_gives_exact_moves_and_row_edits(tmp_path):
    src, docs = make_tree(tmp_path)
    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    readme.write_text(TABLE.replace(
        "| [pet\\_file](pet_file.md) | PET file | string |\n| event | Extra columns | integer |\n",
        "| event | Extra columns | real |\n| [pet\\_file](pet_file.md) | PET file | string |\n"
        "| [idc\\_till](idc_till.md) | Tillage | integer |\n| wnd_dir | Wind direction | real |\n"))
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    assert packet["moves"] == [{"field": "pet_file", "line": 10, "after": None, "after_line": None,
                                "before": "event", "before_line": 9}]
    retype, delete = packet["row_edits"]
    assert (retype["field"], retype["action"], retype["row"]) == (
        "event", "retype", "| event | Extra columns | integer |")
    assert (delete["field"], delete["action"]) == ("wnd_dir", "delete")
    assert packet["exact_text"] == []
    text = render_packet(packet)
    assert "Move the `pet_file` row (line 10) to directly before the `event` row (line 9)." in text
    assert "Delete the `wnd_dir` row (the source does not read it)" in text


def test_html_tables_anchor_on_row_starts_without_invisible_characters(tmp_path):
    src, docs = make_tree(tmp_path)
    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    readme.write_text(
        "# codes.bsn\n\n<table><thead><tr><th>Field</th><th>Description</th><th>Type</th></tr></thead>"
        "<tbody><tr><td><a href=\"pet_file.md\">pet_file</a></td><td>PET file</td><td>​string</td></tr>"
        "<tr><td>event</td><td>Extra</td><td>​real</td></tr></tbody></table>\n", encoding="utf-8")
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    [x] = packet["exact_text"]
    assert (x["table"], x["table_anchor"]) == (
        "insert directly before this exact text, the end of the table", "</tbody>")
    assert x["row"] == ('<tr><td><a href="idc_till.md">idc_till</a></td>'
                        "<td>1 = dssat tillage method; 2 = epic tillage method</td><td>integer</td></tr>")
    [e] = packet["row_edits"]
    assert e["anchor"] == "<tr><td>event</td>"
    assert e["row"] == "<tr><td>event</td><td>Extra</td><td>integer</td></tr>"


# --------------------------------------------------------------------------
# apply
# --------------------------------------------------------------------------

def _committed(docs: Path) -> list[str]:
    """Make the docs a git repository with everything committed; returns the git prefix."""
    import subprocess

    git = ["git", "-C", str(docs), "-c", "user.name=t", "-c", "user.email=t@example.test"]
    subprocess.run(git + ["init", "-q"], check=True)
    subprocess.run(git + ["config", "core.autocrlf", "false"], check=True)
    subprocess.run(git + ["add", "-A"], check=True)
    subprocess.run(git + ["commit", "-qm", "base"], check=True)
    return git


def test_apply_writes_the_missing_row_page_and_summary_entry(tmp_path):
    src, docs = make_tree(tmp_path)
    summary = docs / "io-docs" / "SUMMARY.md"
    summary.write_bytes(summary.read_text().replace("\n", "\r\n").encode())  # GitBook's CRLF
    _committed(docs)
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    done = apply_packet(packet, docs)
    assert done == ["added the idc_till row, its page io-docs/introduction-1/basin/codes.bsn/idc_till.md, "
                    "and its SUMMARY.md entry"]
    assert b"\r\n" in summary.read_bytes() and b"\n" not in summary.read_bytes().replace(b"\r\n", b"")
    page = (docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "idc_till.md").resolve()
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP,
                             new_pages={page}, source_root=src)
    assert ok, lines


def test_apply_moves_retypes_and_deletes_rows(tmp_path):
    src, docs = make_tree(tmp_path)
    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    # pet_file out of order, event wrongly typed, wnd_dir not read by the source
    readme.write_text(TABLE.replace(
        "| [pet\\_file](pet_file.md) | PET file | string |\n| event | Extra columns | integer |\n",
        "| event | Extra columns | real |\n| [pet\\_file](pet_file.md) | PET file | string |\n"
        "| idc_till | Tillage | integer |\n| wnd_dir | Wind direction | real |\n"))
    _committed(docs)
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    assert apply_packet(packet, docs) == ["moved the pet_file row before the event row",
                                          "set the event row's type to integer", "deleted the wnd_dir row"]
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP, source_root=src)
    assert ok, lines


def test_apply_renames_the_page_of_a_replaced_row(tmp_path):
    # pet_file is missing too, so positions shift and till_meth sits where idc_till goes
    src, docs = make_tree(tmp_path)
    table = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn"
    (table / "README.md").write_text(
        TABLE.replace("| [pet\\_file](pet_file.md) | PET file | string |\n", "")
        + "| [till\\_meth](till_meth.md) | Old name | integer |\n")
    (table / "till_meth.md").write_text("---\ndescription: old\n---\n\n# till\\_meth\n")
    (table / "pet_file.md").unlink()
    summary = docs / "io-docs" / "SUMMARY.md"
    summary.write_text("* [codes.bsn](introduction-1/basin/codes.bsn/README.md)\n"
                       "  * [till\\_meth](introduction-1/basin/codes.bsn/till_meth.md)\n")
    _committed(docs)
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)

    done = apply_packet(packet, docs)
    assert done[-1] == ("replaced the idc_till row, its page io-docs/introduction-1/basin/codes.bsn/"
                        "idc_till.md, and its SUMMARY.md entry")
    assert not (table / "till_meth.md").exists() and (table / "idc_till.md").exists()
    assert "till_meth" not in summary.read_text()
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP, source_root=src)
    assert ok, lines


def test_apply_writes_nothing_over_uncommitted_changes(tmp_path):
    src, docs = make_tree(tmp_path)
    _committed(docs)
    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    readme.write_text(readme.read_text() + "\nlocal edit\n")
    before = readme.read_text()
    packet = build_packet(SCHEMA, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)
    with pytest.raises(ApplyError, match="uncommitted changes under io-docs"):
        apply_packet(packet, docs)
    assert readme.read_text() == before
    assert not (readme.parent / "idc_till.md").exists()


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------

def test_check_names_a_row_split_across_lines(tmp_path):
    _, docs = make_tree(tmp_path)
    readme = docs / "io-docs" / "introduction-1" / "basin" / "codes.bsn" / "README.md"
    readme.write_text(readme.read_text() + "| idc_till | 1 = dssat\n!! 2 = epic | integer |\n")
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP)
    assert not ok
    assert lines[0].startswith("FAIL codes.bsn: table broken at line(s) 11, 12")


def test_check_skips_a_table_whose_reader_never_runs(tmp_path):
    src, docs = make_tree(tmp_path)
    dead = {**SCHEMA, "files": {**SCHEMA["files"], "codes.bsn": {**SCHEMA["files"]["codes.bsn"],
                                                                "reader": "dead_read.f90"}}}
    ok, lines = check_tables(dead, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP, source_root=src)
    assert ok and lines == ["SKIP codes.bsn: its reader dead_read never runs; leave the table alone"]
    assert build_packet(dead, PROVENANCE, docs, src, "codes.bsn", FIELD_MAP)["exact_text"] == []

def test_check_fails_until_the_table_is_fixed_and_registered(tmp_path):
    _, docs = make_tree(tmp_path)
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP)
    assert not ok and lines == ["FAIL codes.bsn: missing from docs: idc_till"]

    page = add_idc_till(docs)
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP,
                             new_pages={page})
    assert ok and lines == ["PASS codes.bsn"]


def test_check_requires_new_pages_in_summary_with_front_matter(tmp_path):
    _, docs = make_tree(tmp_path)
    page = add_idc_till(docs, register=False, front_matter=False)
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP,
                             new_pages={page})
    assert not ok
    assert "is not in SUMMARY.md" in lines[0]
    assert "needs front matter" in lines[0]


def test_check_catches_summary_entries_for_deleted_pages(tmp_path):
    _, docs = make_tree(tmp_path)
    add_idc_till(docs)
    summary = docs / "io-docs" / "SUMMARY.md"
    summary.write_text(summary.read_text() + "  * [old](introduction-1/basin/codes.bsn/bed_load.md)\n")
    ok, lines = check_tables(SCHEMA, PROVENANCE, docs.resolve(), ["codes.bsn"], FIELD_MAP)
    assert not ok
    assert lines[-1] == ("FAIL SUMMARY.md points at missing pages: "
                         "introduction-1/basin/codes.bsn/bed_load.md")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_cli_packet_and_check(tmp_path, monkeypatch, capsys):
    src, docs = make_tree(tmp_path)
    releases, reports = tmp_path / "releases", tmp_path / "reports"
    releases.mkdir()
    reports.mkdir()
    (releases / "swatplus-62.0.1.json").write_text(json.dumps(SCHEMA))
    (releases / "swatplus-62.0.1.provenance.json").write_text(json.dumps(PROVENANCE))
    (reports / "swatplus-62.0.0-field-map.json").write_text(json.dumps(FIELD_MAP))
    config = tmp_path / "swatref.toml"
    config.write_text('[sources.release_62_0_1]\nref = "62.0.1"\n\n'
                      '[docs]\nsource = "release_62_0_1"\n\n'
                      '[schema]\noutput_dir = "releases"\nreports_dir = "reports"\n')
    checkout = SourceProvenance("release_62_0_1", "https://example.test/swatplus", "62.0.1",
                                COMMIT, COMMIT)
    monkeypatch.setattr(cli, "resolve_profile", lambda cfg, name: (src, checkout))
    base = ["--config", str(config), "schema", "--source", "release_62_0_1"]

    assert main(base + ["user-docs-packet", "codes.bsn", "--docs-root", str(docs)]) == 0
    out = capsys.readouterr().out
    assert "**MISSING**, insert after line 10 (the event row)" in out
    assert "user-docs-check codes.bsn" in out

    assert main(base + ["user-docs-check", "codes.bsn", "--docs-root", str(docs)]) == 1
    assert "NOT DONE" in capsys.readouterr().out
    add_idc_till(docs)
    assert main(base + ["user-docs-check", "codes.bsn", "--docs-root", str(docs)]) == 0
    out = capsys.readouterr().out
    assert out.startswith(f"Checked against SWAT+ 62.0.1 @ {COMMIT[:12]}; docs @ ")
    assert "ALL PASS" in out
    assert not list(reports.glob("*user-docs-report*"))  # neither command writes a report


def test_cli_check_committed_fails_until_io_docs_is_committed(tmp_path, monkeypatch, capsys):
    # An agent once reported a commit it never made; --committed makes the
    # claim checkable from the output it pastes.
    import subprocess

    src, docs = make_tree(tmp_path)
    releases = tmp_path / "releases"
    releases.mkdir()
    (releases / "swatplus-62.0.1.json").write_text(json.dumps(SCHEMA))
    (releases / "swatplus-62.0.1.provenance.json").write_text(json.dumps(PROVENANCE))
    config = tmp_path / "swatref.toml"
    config.write_text('[sources.release_62_0_1]\nref = "62.0.1"\n\n'
                      '[docs]\nsource = "release_62_0_1"\n\n'
                      '[schema]\noutput_dir = "releases"\nreports_dir = "releases"\n')
    checkout = SourceProvenance("release_62_0_1", "https://example.test/swatplus", "62.0.1",
                                COMMIT, COMMIT)
    monkeypatch.setattr(cli, "resolve_profile", lambda cfg, name: (src, checkout))
    git = ["git", "-C", str(docs), "-c", "user.name=t", "-c", "user.email=t@example.test"]
    subprocess.run(git + ["init", "-q"], check=True)
    add_idc_till(docs)
    command = ["--config", str(config), "schema", "--source", "release_62_0_1",
               "user-docs-check", "codes.bsn", "--docs-root", str(docs), "--committed"]

    assert main(command) == 1
    assert "FAIL not committed: io-docs/" in capsys.readouterr().out
    subprocess.run(git + ["add", "-A"], check=True)
    subprocess.run(git + ["commit", "-qm", "fix"], check=True)
    assert main(command) == 0
    out = capsys.readouterr().out
    assert "COMMITTED: no uncommitted changes under io-docs" in out and "ALL PASS" in out


def test_cli_refuses_to_compare_without_a_config_file(tmp_path, capsys):
    # Built-in defaults name another SWAT+ commit; a check against them once
    # passed a table that was still wrong.
    _, docs = make_tree(tmp_path)
    with pytest.raises(SystemExit) as stop:
        main(["--config", str(tmp_path / "missing" / "swatref.toml"), "schema", "--source",
              "release_62_0_1", "user-docs-check", "codes.bsn", "--docs-root", str(docs)])
    assert stop.value.code == 2
    assert "no swatref.toml in" in capsys.readouterr().err
