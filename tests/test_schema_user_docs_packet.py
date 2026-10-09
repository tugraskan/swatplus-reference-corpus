"""Evidence packet and pass/fail check for one user-docs input table."""

from __future__ import annotations

import json
from pathlib import Path

from swatplus_reference import cli
from swatplus_reference.cli import main
from swatplus_reference.provenance.records import SourceProvenance
from swatplus_reference.schema.user_docs_packet import build_packet, check_tables, render_packet

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


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------

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
    assert "ALL PASS" in capsys.readouterr().out
    assert not list(reports.glob("*user-docs-report*"))  # neither command writes a report
