"""User-documentation input tables vs a release schema (read-only report)."""

from __future__ import annotations

import json
from pathlib import Path

from swatplus_reference.cli import main
from swatplus_reference.schema import user_docs


def field(name: str, ftype: str = "real", position: int = 0) -> dict:
    return {"doc": None, "fortran_name": name, "fortran_type": ftype,
            "numeric": ftype != "character", "position": position, "units": None}


HTML_TABLE = """\
---
description: Aquifer properties.
---

# aquifer.aqu

<table><thead><tr><th>Field</th><th>Description</th><th>Type</th></tr></thead><tbody>
<tr><td><a href="id.md">id</a></td><td>ID</td><td>integer</td></tr>
<tr><td><a href="name.md">name</a></td><td>Name</td><td>string</td></tr>
<tr><td><a href="gone.md">gw_flo</a></td><td>Flow</td><td>real</td></tr>
</tbody></table>
"""

PIPE_TABLE = """\
# codes.bsn

| Field | Description | Type |
| ----- | ----------- | :--: |
| [pet\\_file](pet_file.md) | PET file | string |
| [event](event.md) | Event flag | integer |
"""


def make_docs(root: Path) -> Path:
    """A miniature SWATPlus-user-documentation checkout."""
    io = root / user_docs.IO_DOCS
    pages = {
        "aquifers/aquifer.aqu/README.md": HTML_TABLE,
        "aquifers/aquifer.aqu/id.md": "# id\n\nRefers to aquifer.con.\n",
        "aquifers/aquifer.aqu/name.md": "# name\n",
        "basin/codes.bsn/README.md": PIPE_TABLE,
        "routing-units/untitled/README.md":
            "# rout\\_unit.rtu\n\n| Field | Description |\n| --- | --- |\n| id | ID |\n| name | Name |\n",
        "climate/pcp.cli-and-precipitation-data-files.md": "# pcp.cli\n\nWeather.\n",
        "connectivity/chan_surf.lin.md": "# chan\\_surf.lin\n\nLinks.\n",
        "calibration/wb_parms.sft.md": "# wb\\_parms.sft\n",
        # One table documents every connect file, as in the real docs.
        "connectivity/README.md": (
            "# Connectivity\n\n| Object | Connect file |\n| --- | --- |\n"
            "| HRU | hru.con |\n| Aquifer | aquifer.con |\n\n"
            "All connect files have the same structure (see [**'object'.con**](hru.con/)).\n"
        ),
        "connectivity/hru.con/README.md": (
            "# hru.con\n\n| Field | Description | Type |\n| --- | --- | --- |\n"
            "| id | ID | integer |\n| name | Name | string |\n| rule | Rule | integer |\n"
        ),
        "master-file-file.cio.md": "# Master File (file.cio)\n\n1. channel.con (currently not used)\n",
    }
    for rel, text in pages.items():
        (io / rel).parent.mkdir(parents=True, exist_ok=True)
        (io / rel).write_text(text, encoding="utf-8")
    return root


SCHEMA = {
    "swatplus_version": "62.0.1",
    "files": {
        "aquifer.aqu": {"fields": [field("k", "integer", 0), field("aqunm", "character", 1),
                                   field("flo", "real", 2)]},
        "codes.bsn": {"fields": [field("event", "integer", 0), field("pet_file", "character", 1),
                                 field("idc_till", "integer", 2)]},
        "rout_unit.rtu": {"fields": [field("id", "integer", 0), field("nm", "character", 1)]},
        "wb_parms.sft": {"fields": [field("name", "character", 0)]},
        "chan-surf.lin": {"fields": [field("id", "integer", 0)]},
        **{con: {"fields": [field("id", "integer", 0), field("name", "character", 1),
                            field("rule", "character", 2)]}
           for con in ("hru.con", "aquifer.con", "channel.con")},
    },
    "runtime_arity": {"pcp.cli": {}},
    "unresolved": [{"file": "manure.frt", "reason": "reader not found"}],
}
PROVENANCE = {"profile": "release_62_0_1", "repository": "https://example.test/swatplus",
              "resolved_commit": "c" * 40}
FIELD_MAP = {"files": {"aquifer.aqu": [
    {"source": {"name": "k"}, "editor_database": {"name": "id"}},
    {"source": {"name": "aqunm"}, "editor_database": {"name": "name"}},
    {"source": {"name": "flo"}, "editor_database": {"name": "gw_flo"}},
]}}


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


# --------------------------------------------------------------------------
# docs parsing
# --------------------------------------------------------------------------

def test_field_table_reads_html_and_pipe_tables():
    assert user_docs.field_table(HTML_TABLE) == [
        {"field": "id", "link": "id.md", "type": "integer"},
        {"field": "name", "link": "name.md", "type": "string"},
        {"field": "gw_flo", "link": "gone.md", "type": "real"},
    ]
    assert user_docs.field_table(PIPE_TABLE) == [
        {"field": "pet_file", "link": "pet_file.md", "type": "string"},
        {"field": "event", "link": "event.md", "type": "integer"},
    ]


def test_pipe_cells_lose_gitbook_markup():
    text = (
        "| Field | Type |\n| --- | --- |\n"
        '| <p><a href="plt_n.md">plt_n</a></p><p></p> | real |\n'
        "| name&#xD; | string |\n"
        "| init​ | string  |\n"
    )
    assert user_docs.field_table(text) == [
        {"field": "plt_n", "link": "plt_n.md", "type": "real"},
        {"field": "name", "link": "", "type": "string"},
        {"field": "init", "link": "", "type": "string"},
    ]


def test_field_table_ignores_tables_that_are_not_field_tables():
    assert user_docs.field_table("| Code | Option |\n| --- | --- |\n| 0 | off |\n") is None
    assert user_docs.field_table("# just prose\n") is None


def test_pages_are_found_by_folder_slug_and_escaped_title(tmp_path):
    io = make_docs(tmp_path) / user_docs.IO_DOCS
    files = {"aquifer.aqu", "codes.bsn", "rout_unit.rtu", "pcp.cli", "chan-surf.lin", "aquifer.con"}
    by_file, unmatched = user_docs.index_pages(io, files)

    found = {f: [p.relative_to(io).as_posix() for p in ps] for f, ps in by_file.items()}
    assert found == {
        "aquifer.aqu": ["aquifers/aquifer.aqu/README.md"],
        "codes.bsn": ["basin/codes.bsn/README.md"],
        "rout_unit.rtu": ["routing-units/untitled/README.md"],
        "pcp.cli": ["climate/pcp.cli-and-precipitation-data-files.md"],
    }  # a field page that merely mentions aquifer.con does not document it
    by_page = {u["page"].relative_to(io).as_posix(): u for u in unmatched}
    assert by_page["connectivity/chan_surf.lin.md"]["closest"] == ["chan-surf.lin"]
    assert by_page["calibration/wb_parms.sft.md"]["closest"] == []


# --------------------------------------------------------------------------
# comparison
# --------------------------------------------------------------------------

def test_fields_match_on_fortran_or_editor_name():
    source = [field("k", "integer"), field("aqunm", "character"), field("flo")]
    rows = [{"field": "id", "type": "integer"}, {"field": "aqunm", "type": "string"},
            {"field": "gw_flo", "type": "real"}]
    assert user_docs.compare_table(source, rows, {"k": "id", "flo": "gw_flo"}) == {}


def test_missing_extra_renamed_reordered_and_retyped_fields_are_reported():
    source = [field("a", "integer"), field("b"), field("c"), field("d"), field("e")]
    rows = [{"field": "a", "type": "real"}, {"field": "c", "type": "real"},
            {"field": "b", "type": "real"}, {"field": "x", "type": "real"}]
    assert user_docs.compare_table(source, rows, {}) == {
        "missing_from_docs": ["e"],
        "name_differs": [{"position": 4, "docs": "x", "source": "d"}],
        "out_of_order": ["c"],
        "type_differs": [{"field": "a", "docs": "real", "source": "integer"}],
    }
    extra_row = [{"field": "a"}, {"field": "b"}, {"field": "c"}, {"field": "d"},
                 {"field": "e"}, {"field": "zz"}]
    assert user_docs.compare_table(source, extra_row, {}) == {"not_in_source": ["zz"]}


def test_unknown_doc_type_words_are_not_flagged():
    rows = [{"field": "a", "type": "numeric"}, {"field": "b", "type": ""}]
    assert user_docs.compare_table([field("a"), field("b")], rows, {}) == {}


def test_a_file_read_as_several_records_lists_every_block_in_read_order():
    entry = {  # print.prt: the first block is listed first, but read order decides
        "fields": [field("nyskip", "integer")], "reader_line": 28,
        "blocks": [
            {"reader_line": 28, "fields": [field("nyskip", "integer")]},
            {"reader_line": 44, "fields": [field("csvout", "character")]},
            {"reader_line": 32, "fields": [field("aa_numint", "integer")],
             "repeat": {"fields": [field("aa_yrs", "integer")]}},
        ],
    }
    assert [f["fortran_name"] for f in user_docs.expected_fields(entry)] == [
        "nyskip", "aa_numint", "aa_yrs", "csvout"]
    assert [(line, rep) for _, line, rep in user_docs.field_origins(entry)] == [
        (28, False), (32, False), (32, True), (44, False)]


def test_a_repeating_group_is_expected_once():
    entry = {"fields": [field("id", "integer")],
             "repeat": {"count_field": "out_tot", "fields": [field("obj_typ", "character")]}}
    assert [f["fortran_name"] for f in user_docs.expected_fields(entry)] == ["id", "obj_typ"]


def test_example_headers_confirm_names_only_at_the_same_position(tmp_path):
    dataset = tmp_path / "refdata" / "Osu_1hru"
    dataset.mkdir(parents=True)
    (dataset / "aquifer.aqu").write_text(
        "aquifer.aqu: written by SWAT+ editor\n  id  name  init  gw_flo\n  1 aqu1 ini1 0.05\n")
    headers = user_docs.example_headers(tmp_path / "refdata")
    assert headers == {"aquifer.aqu": [["id", "name", "init", "gw_flo"]]}

    entry = {
        "missing_from_docs": ["flo_min"],
        "name_differs": [
            {"position": 3, "docs": "init", "source": "aqu_ini"},     # header agrees
            {"position": 2, "docs": "gw_flo", "source": "aqunm"},     # header has it elsewhere
        ],
    }
    user_docs._confirm_names(entry, headers["aquifer.aqu"])
    assert entry == {
        "missing_from_docs": ["flo_min"],  # structural findings are never touched
        "name_differs": [{"position": 2, "docs": "gw_flo", "source": "aqunm"}],
        "names_confirmed_by_example_header": [
            {"position": 3, "docs": "init", "source": "aqu_ini"}],
    }


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def test_report_classifies_every_input_file_and_writes_nothing_to_the_docs(tmp_path):
    docs = make_docs(tmp_path / "SWATPlus-user-documentation")
    before = snapshot(docs)

    report = user_docs.build_report(SCHEMA, PROVENANCE, docs, FIELD_MAP, "fm.json")

    assert snapshot(docs) == before
    status = {f: e["status"] for f, e in report["files"].items()}
    assert status == {
        "aquifer.aqu": "match",
        "codes.bsn": "differs",
        "rout_unit.rtu": "names_to_check",
        "wb_parms.sft": "no_field_table",
        "chan-surf.lin": "no_page",
        "pcp.cli": "not_compared",
        "manure.frt": "no_page",
        "hru.con": "differs",       # own page: rule is integer in docs
        "aquifer.con": "differs",   # same shared table, though a field page also mentions it
        "channel.con": "named_only",
    }
    aquifer_con = report["files"]["aquifer.con"]
    assert aquifer_con["table_page"].endswith("connectivity/hru.con/README.md")
    assert aquifer_con["listed_on"].endswith("connectivity/README.md")
    assert aquifer_con["type_differs"] == [{"field": "rule", "docs": "integer", "source": "character"}]
    assert report["files"]["channel.con"]["docs_say_not_used"] is True
    assert report["files"]["channel.con"]["named_on"] == [
        "io-docs/introduction-1/master-file-file.cio.md"]
    codes = report["files"]["codes.bsn"]
    assert codes["missing_from_docs"] == ["idc_till"]
    assert codes["out_of_order"] == ["pet_file"]
    assert report["files"]["aquifer.aqu"]["broken_links"] == ["gw_flo -> gone.md"]
    assert report["files"]["rout_unit.rtu"]["name_differs"] == [
        {"position": 2, "docs": "name", "source": "nm"}]
    assert report["source"]["resolved_commit"] == "c" * 40
    assert report["summary"]["pages_not_in_schema"] == 2  # chan_surf.lin, file.cio


def test_report_files_are_deterministic(tmp_path):
    docs = make_docs(tmp_path / "SWATPlus-user-documentation")
    out = tmp_path / "out" / "report.json"
    user_docs.write_report(user_docs.build_report(SCHEMA, PROVENANCE, docs, FIELD_MAP), out)
    first = out.read_bytes(), out.with_suffix(".md").read_bytes()
    user_docs.write_report(user_docs.build_report(SCHEMA, PROVENANCE, docs, FIELD_MAP), out)
    assert (out.read_bytes(), out.with_suffix(".md").read_bytes()) == first
    markdown = first[1].decode("utf-8")
    assert "## Tables that differ from the source (3)" in markdown
    assert "(shared table, listed on `io-docs/introduction-1/connectivity/README.md`)" in markdown
    assert "## Named in the docs, but no page describes them (1)" in markdown
    assert "near-identical input file: `chan-surf.lin`" in markdown


def test_cli_writes_the_report_next_to_the_editor_report(tmp_path, capsys):
    docs = make_docs(tmp_path / "SWATPlus-user-documentation")
    releases, reports = tmp_path / "releases", tmp_path / "reports"
    releases.mkdir()
    reports.mkdir()
    (releases / "swatplus-62.0.1.json").write_text(json.dumps(SCHEMA))
    (releases / "swatplus-62.0.1.provenance.json").write_text(json.dumps(PROVENANCE))
    (reports / "swatplus-62.0.0-field-map.json").write_text(json.dumps(FIELD_MAP))
    config = tmp_path / "swatref.toml"
    config.write_text(
        '[sources.release_62_0_1]\nref = "62.0.1"\n\n'
        '[docs]\nsource = "release_62_0_1"\n\n'
        '[schema]\noutput_dir = "releases"\nreports_dir = "reports"\n'
    )

    assert main(["--config", str(config), "schema", "--source", "release_62_0_1",
                 "user-docs-report", "--docs-root", str(docs)]) == 0

    report = json.loads((reports / "swatplus-62.0.1-user-docs-report.json").read_text())
    assert report["field_map"] == "swatplus-62.0.0-field-map.json"
    assert report["files"]["aquifer.aqu"]["status"] == "match"
    assert (reports / "swatplus-62.0.1-user-docs-report.md").exists()
    assert '"differs": 3' in capsys.readouterr().out
