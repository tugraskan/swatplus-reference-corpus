import csv

from swatplus_reference.schema.field_map import (
    _expand_candidates,
    build_file_map,
    load_spreadsheet_rows,
    render_markdown,
    source_fields,
)

SPEC = {
    "fields": [
        {"fortran_name": "evlai", "fortran_type": "real", "doc": "leaf area index", "units": "none"},
        {"fortran_name": "surlag", "fortran_type": "real", "doc": "runoff lag", "units": "days"},
        {"fortran_name": "spcon", "fortran_type": "real", "doc": "not used", "units": None},
    ]
}


def row(**overrides) -> dict[str, str]:
    base = {
        "SWAT_File": "parameters.bsn",
        "DATABASE_FIELD_NAME": "lai_noevap",
        "SWAT_Header_Name": "",
        "SWAT_Code_Variable_Name": "",
        "Data_Type": "numeric",
        "Units": "none",
        "Description": "leaf area index at which no evap occurs",
        "Minimum_Range": "0",
        "Maximum_Range": "1",
    }
    base.update(overrides)
    return base


def test_source_fields_indexes_by_lowercased_name() -> None:
    assert set(source_fields(SPEC)) == {"evlai", "surlag", "spcon"}


def test_build_file_map_pairs_through_the_editor_translation() -> None:
    result = build_file_map("parameters.bsn", [row()], SPEC, {"lai_noevap": "evlai"})
    matched = [f for f in result.fields if f.status == "matched"]
    assert len(matched) == 1
    assert (matched[0].editor_name, matched[0].code_name) == ("lai_noevap", "evlai")
    assert matched[0].route == "editor_map"
    assert (matched[0].minimum, matched[0].maximum) == (0.0, 1.0)


def test_build_file_map_pairs_on_an_identical_name_without_translation() -> None:
    result = build_file_map("parameters.bsn", [row(DATABASE_FIELD_NAME="surlag")], SPEC, {})
    matched = [f for f in result.fields if f.status == "matched"]
    assert matched[0].route == "direct_name"


def test_build_file_map_reports_both_unmatched_directions() -> None:
    result = build_file_map("parameters.bsn", [row(DATABASE_FIELD_NAME="gone")], SPEC, {})
    assert result.counts() == {"spreadsheet_only": 1, "source_only": 3}
    orphan = next(f for f in result.fields if f.status == "spreadsheet_only")
    assert orphan.editor_name == "gone"
    assert orphan.code_name == ""


def test_build_file_map_does_not_reuse_one_source_field_twice() -> None:
    rows = [row(), row(DATABASE_FIELD_NAME="lai_noevap")]
    result = build_file_map("parameters.bsn", rows, SPEC, {"lai_noevap": "evlai"})
    # Both rows name the same field; it is not reported as source_only as well.
    assert "evlai" not in {f.code_name for f in result.fields if f.status == "source_only"}


def test_render_markdown_escapes_pipes_in_descriptions() -> None:
    result = build_file_map(
        "parameters.bsn", [row(Description="a |b")], SPEC, {"lai_noevap": "evlai"}
    )
    out = render_markdown([result], "62.0.0")
    assert "a \\|b" in out
    assert "## parameters.bsn" in out


def test_editor_check_is_unavailable_without_an_inventory() -> None:
    result = build_file_map("parameters.bsn", [row()], SPEC, {"lai_noevap": "evlai"})
    assert result.fields[0].editor_check == "unavailable"
    assert result.fields[0].editor_db_name == ""


def test_editor_check_verifies_the_spreadsheet_name_against_the_real_editor_column() -> None:
    result = build_file_map(
        "parameters.bsn",
        [row()],
        SPEC,
        {"lai_noevap": "evlai"},
        editor_inventory={"lai_noevap": "LAI_NOEVAP"},
    )
    matched = result.fields[0]
    assert matched.status == "matched"
    assert matched.editor_check == "verified"
    assert matched.editor_db_name == "LAI_NOEVAP"


def test_editor_check_flags_a_spreadsheet_name_absent_from_the_real_editor_columns() -> None:
    result = build_file_map(
        "parameters.bsn",
        [row(DATABASE_FIELD_NAME="surlag")],
        SPEC,
        {},
        editor_inventory={"other_col": "OTHER_COL"},
    )
    matched = result.fields[0]
    assert matched.status == "matched"
    assert matched.route == "direct_name"
    assert matched.editor_check == "mismatch"
    assert matched.editor_db_name == ""


def test_editor_check_can_verify_a_name_the_source_pairing_never_resolved() -> None:
    """A row can be a confirmed real Editor column and still be spreadsheet_only.

    ``editor_pairs`` only carries names that resolved to a source field (e.g.
    block field counts lined up); ``editor_inventory`` is the Editor's full
    real column list regardless. A name can be genuinely correct on the
    Editor side while the source-side pairing above never resolved it.
    """
    result = build_file_map(
        "parameters.bsn",
        [row()],
        SPEC,
        {},
        editor_inventory={"lai_noevap": "lai_noevap"},
    )
    matched = result.fields[0]
    assert matched.status == "spreadsheet_only"
    assert matched.editor_check == "verified"
    assert matched.editor_db_name == "lai_noevap"


def test_expand_candidates_returns_the_whole_cell_when_there_is_no_slash() -> None:
    assert _expand_candidates("lai_noevap") == ["lai_noevap"]
    assert _expand_candidates("") == []


def test_expand_candidates_splits_a_compound_cell_whole_value_first() -> None:
    # "hru/props" - a real spreadsheet cell: the Editor's word for it, then the source's.
    assert _expand_candidates("hru/props") == ["hru/props", "hru", "props"]


def test_build_file_map_matches_a_compound_code_variable_by_splitting_it() -> None:
    # "hru/props" itself matches nothing; "props" (a real source field here) does.
    spec = {"fields": SPEC["fields"] + [{"fortran_name": "props", "fortran_type": "integer"}]}
    result = build_file_map(
        "channel.con",
        [row(DATABASE_FIELD_NAME="hru", SWAT_Code_Variable_Name="hru/props")],
        spec,
        {},
    )
    matched = result.fields[0]
    assert matched.status == "matched"
    assert matched.code_name == "props"
    assert matched.route == "direct_name_split"


def test_build_file_map_tries_the_whole_compound_cell_before_its_split_halves() -> None:
    # A field literally named "gone/spcon" must win over the split candidate "spcon".
    spec = {"fields": SPEC["fields"] + [{"fortran_name": "gone/spcon", "fortran_type": "real"}]}
    result = build_file_map(
        "parameters.bsn", [row(DATABASE_FIELD_NAME="gone/spcon")], spec, {}
    )
    matched = result.fields[0]
    assert matched.code_name == "gone/spcon"
    assert matched.route == "direct_name"


def test_structural_flags_a_wildcard_code_variable_as_not_real_drift() -> None:
    result = build_file_map(
        "hru.con", [row(DATABASE_FIELD_NAME="hru_id", SWAT_Code_Variable_Name="*")], SPEC, {}
    )
    orphan = result.fields[0]
    assert orphan.status == "spreadsheet_only"
    assert orphan.structural is True


def test_structural_flags_a_blank_code_variable_too() -> None:
    result = build_file_map(
        "hru.con", [row(DATABASE_FIELD_NAME="description", SWAT_Code_Variable_Name="")], SPEC, {}
    )
    orphan = result.fields[0]
    assert orphan.structural is True


def test_structural_is_false_once_a_row_actually_matches() -> None:
    # A wildcard code-var must not suppress a real match found through another column.
    result = build_file_map(
        "parameters.bsn", [row(DATABASE_FIELD_NAME="surlag", SWAT_Code_Variable_Name="*")], SPEC, {}
    )
    matched = result.fields[0]
    assert matched.status == "matched"
    assert matched.structural is False


def test_structural_yields_to_a_confirmed_real_editor_column() -> None:
    """A blank code-variable does not make a confirmed Editor column structural.

    cntable.lum's ``treat`` and ``cond_cov`` carry ``*`` as their code
    variable yet are genuine Editor columns - a real field with no recorded
    Fortran counterpart, not a template placeholder.
    """
    result = build_file_map(
        "cntable.lum",
        [row(DATABASE_FIELD_NAME="treat", SWAT_Code_Variable_Name="*")],
        SPEC,
        {},
        editor_inventory={"treat": "treat"},
    )
    orphan = result.fields[0]
    assert orphan.status == "spreadsheet_only"
    assert orphan.editor_check == "verified"
    assert orphan.structural is False


def test_structural_is_false_for_a_named_code_variable() -> None:
    result = build_file_map(
        "parameters.bsn", [row(DATABASE_FIELD_NAME="gone", SWAT_Code_Variable_Name="something")], SPEC, {}
    )
    orphan = result.fields[0]
    assert orphan.status == "spreadsheet_only"
    assert orphan.structural is False


def test_known_name_alias_matches_a_stale_name_wrong_on_both_sides() -> None:
    # act_name/act_option: the sheet's own DATABASE_FIELD_NAME and code
    # variable both say "act_name", but the Editor and source both use the
    # bare "name" - not a compound cell, a stale name on both sides at once.
    spec = {"fields": [{"fortran_name": "name", "fortran_type": "character"}]}
    result = build_file_map(
        "lum.dtl",
        [row(DATABASE_FIELD_NAME="act_name", SWAT_Code_Variable_Name="act_name")],
        spec,
        {},
    )
    matched = result.fields[0]
    assert matched.status == "matched"
    assert matched.code_name == "name"
    assert matched.route == "direct_name_alias"


def test_known_name_alias_also_feeds_the_editor_check() -> None:
    spec = {"fields": [{"fortran_name": "option", "fortran_type": "character"}]}
    result = build_file_map(
        "lum.dtl",
        [row(DATABASE_FIELD_NAME="act_option", SWAT_Code_Variable_Name="act_option")],
        spec,
        {},
        editor_inventory={"option": "option"},
    )
    matched = result.fields[0]
    assert matched.status == "matched"
    assert matched.editor_check == "verified"
    assert matched.editor_db_name == "option"


def test_known_name_alias_does_not_override_a_working_direct_match() -> None:
    # If the raw name already resolves, the alias must never be preferred.
    spec = {
        "fields": [
            {"fortran_name": "act_name", "fortran_type": "character"},
            {"fortran_name": "name", "fortran_type": "character"},
        ]
    }
    result = build_file_map(
        "lum.dtl",
        [row(DATABASE_FIELD_NAME="act_name", SWAT_Code_Variable_Name="act_name")],
        spec,
        {},
    )
    matched = result.fields[0]
    assert matched.code_name == "act_name"
    assert matched.route == "direct_name"


def test_load_spreadsheet_rows_remaps_a_known_stale_filename(tmp_path) -> None:
    # The spreadsheet spells this file "res.dtl"; the schema and the model's
    # own reader call it "res_rel.dtl" - without the remap, every row for it
    # groups under a key nothing ever looks up and silently disappears.
    csv_path = tmp_path / "sheet.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["SWAT_File", "DATABASE_FIELD_NAME"])
        writer.writeheader()
        writer.writerow({"SWAT_File": "res.dtl", "DATABASE_FIELD_NAME": "mdtbl"})
        writer.writerow({"SWAT_File": "lum.dtl", "DATABASE_FIELD_NAME": "mdtbl"})

    grouped = load_spreadsheet_rows(csv_path)
    assert "res.dtl" not in grouped
    assert [r["DATABASE_FIELD_NAME"] for r in grouped["res_rel.dtl"]] == ["mdtbl"]
    # A file with no alias passes through unchanged.
    assert [r["DATABASE_FIELD_NAME"] for r in grouped["lum.dtl"]] == ["mdtbl"]
