from swatplus_reference.schema.editor_report import (
    PASSTHROUGH_OFFICIAL_CONTRACTS,
    diff_fields,
    handled_editor_file_status,
    passthrough_contract_changed,
)


def test_diff_fields_reports_add_remove_type_and_order() -> None:
    official = [
        {"name": "name", "field_type": "character", "numeric": False, "position": 0},
        {"name": "area", "field_type": "real", "numeric": True, "position": 1},
        {"name": "flag", "field_type": "integer", "numeric": True, "position": 2},
    ]
    editor = [
        {"name": "name", "field_type": "character", "numeric": False, "position": 0},
        {"name": "flag", "field_type": "real", "numeric": True, "position": 1},
        {"name": "legacy", "field_type": "integer", "numeric": True, "position": 2},
    ]

    diff = diff_fields(official, editor)

    assert [f["name"] for f in diff["added_upstream_fields"]] == ["area"]
    assert [f["name"] for f in diff["removed_upstream_fields"]] == ["legacy"]
    assert diff["retyped_fields"] == [
        {"name": "flag", "official_type": "integer", "editor_type": "real"}
    ]
    assert diff["reordered_fields"] == [
        {"name": "flag", "official_position": 2, "editor_position": 1}
    ]


def test_handled_editor_file_statuses_are_not_extraction_failures() -> None:
    assert handled_editor_file_status("pcp.cli")[0] == "editor_passthrough"
    assert handled_editor_file_status("recall.con")[0] == "editor_inventory_not_written"
    assert handled_editor_file_status("gwflow.con")[0] == "editor_special_writer_unmapped"
    assert handled_editor_file_status("time.sim") is None


def test_passthrough_contract_detects_future_official_shape_change() -> None:
    official = PASSTHROUGH_OFFICIAL_CONTRACTS["pcp.cli"]

    assert passthrough_contract_changed("pcp.cli", official) is False
    assert handled_editor_file_status("pcp.cli", official)[0] == "editor_passthrough"

    changed = [dict(block) for block in official]
    changed[0] = {**changed[0], "fields": [*changed[0]["fields"], {"name": "extra", "field_type": "real"}]}

    assert passthrough_contract_changed("pcp.cli", changed) is True
    assert handled_editor_file_status("pcp.cli", changed)[0] == "passthrough_upstream_changed"
