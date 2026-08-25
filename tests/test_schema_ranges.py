from swatplus_reference.schema.input import (
    extract_range,
    parse_range_token,
    split_units_doc,
)
from swatplus_reference.schema.ranges import (
    RangeRow,
    build_editor_inventory,
    build_editor_to_official,
    clean_cell,
    crosswalk,
    iter_field_lists,
    parse_bound,
    quarantine_reason,
)


def make_row(**overrides) -> RangeRow:
    base = {
        "swat_file": "parameters.bsn",
        "db_field": "surq_lag",
        "header_name": "",
        "code_variable": "",
        "position": 3,
        "units": "",
        "description": "surface runoff lag time",
        "minimum": 0.5,
        "maximum": 2.0,
    }
    base.update(overrides)
    return RangeRow(**base)


def test_clean_cell_treats_na_as_empty() -> None:
    # 'na' appears 324 times in the export and must not be read as a bound.
    assert clean_cell("na") == ""
    assert clean_cell("Na") == ""
    assert clean_cell(" * ") == ""
    assert clean_cell(" 0.5 ") == "0.5"


def test_parse_bound_rejects_non_numeric_text() -> None:
    assert parse_bound("0.0001") == 0.0001
    assert parse_bound("na") is None
    assert parse_bound("") is None


def test_build_editor_to_official_uses_label_differences() -> None:
    report = {
        "parameters.bsn": {
            "field_diff": {
                "blocks": [
                    {
                        "count_matches": True,
                        "label_differences": [
                            {"editor_name": "surq_lag", "official_name": "surlag"},
                            {"editor_name": "lai_noevap", "official_name": "evlai"},
                        ],
                    }
                ]
            }
        }
    }
    assert build_editor_to_official(report)["parameters.bsn"] == {
        "surq_lag": "surlag",
        "lai_noevap": "evlai",
    }


def test_build_editor_to_official_skips_blocks_whose_counts_disagree() -> None:
    # sed_nut.cha gained two upstream fields, so position is not a safe key.
    report = {
        "sed_nut.cha": {
            "field_diff": {"blocks": [{"count_matches": False, "label_differences": [
                {"editor_name": "n_sol_part", "official_name": "n_setl"}
            ]}]},
            "editor_schema": {"blocks": [{"fields": [{"name": "n_sol_part"}]}]},
            "official_schema": {"blocks": [{"fields": [{"name": "n_setl"}, {"name": "p_setl"}]}]},
        }
    }
    assert build_editor_to_official(report) == {}


def test_build_editor_inventory_lists_columns_regardless_of_official_pairing() -> None:
    # sed_nut.cha's block counts disagree, so build_editor_to_official skips it -
    # build_editor_inventory still reports the real column, independent of that.
    report = {
        "sed_nut.cha": {
            "editor_schema": {"blocks": [{"fields": [{"name": "n_sol_part"}]}]},
            "official_schema": {"blocks": [{"fields": [{"name": "n_setl"}, {"name": "p_setl"}]}]},
        }
    }
    assert build_editor_inventory(report) == {"sed_nut.cha": {"n_sol_part": "n_sol_part"}}


def test_build_editor_inventory_preserves_original_case_and_is_absent_without_data() -> None:
    report = {
        "parameters.bsn": {"editor_schema": {"blocks": [{"fields": [{"name": "LAI_Noevap"}]}]}},
        "no_editor_data.ops": {"official_schema": {"blocks": [{"fields": [{"name": "x"}]}]}},
    }
    inventory = build_editor_inventory(report)
    assert inventory["parameters.bsn"] == {"lai_noevap": "LAI_Noevap"}
    assert "no_editor_data.ops" not in inventory


def test_iter_field_lists_walks_nested_schema_shapes() -> None:
    spec = {
        "fields": [{"fortran_name": "name"}],
        "repeat": {"fields": [{"fortran_name": "elem_cnt"}]},
        "sections": [{"fields": [{"fortran_name": "pcp"}]}],
    }
    found = {entry["fortran_name"] for fields in iter_field_lists(spec) for entry in fields}
    assert found == {"name", "elem_cnt", "pcp"}


def test_crosswalk_applies_range_through_editor_translation() -> None:
    schema = {
        "files": {
            "parameters.bsn": {
                "fields": [{"fortran_name": "surlag", "numeric": True, "position": 2}]
            }
        }
    }
    result = crosswalk([make_row()], {"parameters.bsn": {"surq_lag": "surlag"}}, schema)
    assert result.summary()["applied"] == 1
    field = schema["files"]["parameters.bsn"]["fields"][0]
    assert field["minimum"] == 0.5
    assert field["maximum"] == 2.0
    assert field["range_source"] == "modular_database_rev_61_0_nbs"


def test_crosswalk_reports_drift_when_name_is_gone() -> None:
    schema = {"files": {"codes.bsn": {"fields": [{"fortran_name": "pet", "numeric": True}]}}}
    row = make_row(swat_file="codes.bsn", db_field="rtu_wq", minimum=0.0, maximum=1.0)
    result = crosswalk([row], {"codes.bsn": {"pet": "pet"}}, schema)
    assert result.summary() == {
        "applied": 0,
        "drift": 1,
        "needs_review": 0,
        "quarantined": 0,
        "not_applicable": 0,
    }
    assert result.drift[0].code == "name_not_in_schema"


def test_crosswalk_marks_output_files_not_applicable() -> None:
    result = crosswalk([make_row(swat_file="channel.out")], {}, {"files": {}})
    assert result.summary()["not_applicable"] == 1
    assert result.not_applicable[0].code == "file_not_in_input_schema"


def test_crosswalk_holds_files_without_an_editor_pairing_for_review() -> None:
    schema = {"files": {"sed_nut.cha": {"fields": [{"fortran_name": "n_setl", "numeric": True}]}}}
    row = make_row(swat_file="sed_nut.cha", db_field="n_sol_part", minimum=1.1, maximum=1.9)
    result = crosswalk([row], {}, schema)
    assert result.summary()["needs_review"] == 1
    assert result.needs_review[0].code == "no_editor_mapping"
    # Nothing is written when the pairing is unknown.
    assert "minimum" not in schema["files"]["sed_nut.cha"]["fields"][0]


def test_quarantine_rejects_fraction_row_with_out_of_range_maximum() -> None:
    row = make_row(units="frac", description="fraction of fc", minimum=1.0, maximum=24.0)
    reason = quarantine_reason(row, [{"numeric": True}])
    assert reason is not None and reason[0] == "fraction_bound_conflict"


def test_quarantine_rejects_zero_placeholder_and_inverted_ranges() -> None:
    assert quarantine_reason(make_row(minimum=0.0, maximum=0.0), [])[0] == "placeholder_zero_range"
    assert quarantine_reason(make_row(minimum=5.0, maximum=1.0), [])[0] == "inverted_range"


def test_quarantine_rejects_range_on_non_numeric_field() -> None:
    reason = quarantine_reason(make_row(minimum=0.0, maximum=4.0), [{"numeric": False}])
    assert reason is not None and reason[0] == "range_on_non_numeric_field"


def test_quarantine_allows_a_sound_range() -> None:
    assert quarantine_reason(make_row(), [{"numeric": True}]) is None


# --- declaration-comment range token (input_schema parser side) -------------


def test_extract_range_strips_the_trailing_token() -> None:
    body, text = extract_range("none |leaf area index at which no evap occurs |range: 0-1")
    assert body == "none |leaf area index at which no evap occurs"
    assert text == "0-1"


def test_extract_range_leaves_untagged_comments_alone() -> None:
    assert extract_range("deg C |snowfall temp") == ("deg C |snowfall temp", None)
    assert extract_range("") == ("", None)


def test_split_units_doc_keeps_the_range_out_of_the_description() -> None:
    # Without the strip, "description is everything after the first pipe" would
    # fold the range token into the prose.
    units, desc = split_units_doc("none |leaf area index at which no evap occurs |range: 0-1")
    assert units == "none"
    assert desc == "leaf area index at which no evap occurs"


def test_split_units_doc_handles_a_range_only_comment() -> None:
    assert split_units_doc("|range: 0-1") == (None, None)


def test_parse_range_token_reads_pairs_bounds_and_disputes() -> None:
    assert parse_range_token("0-1") == (0.0, 1.0)
    assert parse_range_token("0.0001-0.01") == (0.0001, 0.01)
    assert parse_range_token(">=0") == (0.0, None)
    # A disputed range keeps the source value; the parenthetical is ignored.
    assert parse_range_token("0-1 * (modular db: 10-17.5)") == (0.0, 1.0)
    assert parse_range_token(None) == (None, None)
