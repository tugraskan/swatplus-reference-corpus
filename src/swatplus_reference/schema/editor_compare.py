"""Compare official SWAT+ schemas with Editor effective serialized schemas."""

from __future__ import annotations

import re
from typing import Any

from .editor_effective import EffectiveFileSchema


def _field(field: dict[str, Any], *, repeated: bool = False) -> dict[str, Any]:
    return {
        "name": field["fortran_name"],
        "field_type": field.get("fortran_type"),
        "numeric": bool(field.get("numeric")),
        "position": int(field.get("position", 0)),
        "repeated": repeated or bool(field.get("variable_arity")),
    }


def _row_fields(row: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    if "fields" in row:
        fields = [_field(value) for value in row.get("fields", [])]
        repeat = row.get("repeat") or {}
        fields.extend(_field(value, repeated=True) for value in repeat.get("fields", []))
        fields.extend(_field(value) for value in row.get("suffix_fields", []))
        return fields, False

    variants = row.get("variants", [])
    if not variants:
        return [], False
    first = [_field(value) for value in variants[0].get("fields", [])]
    all_same_layout = all(
        [value["field_type"] for value in first]
        == [value.get("fortran_type") for value in variant.get("fields", [])]
        for variant in variants[1:]
    )
    return first, not all_same_layout


def official_blocks(
    schema: dict[str, Any],
    section: str,
    file_name: str,
) -> tuple[list[dict[str, Any]], str | None]:
    """Normalize the official flat and structured schemas into ordered blocks."""

    entry = schema[section][file_name]
    if section == "files":
        fields = [_field(value) for value in entry.get("fields", [])]
        repeat = entry.get("repeat") or {}
        fields.extend(_field(value, repeated=True) for value in repeat.get("fields", []))
        return [{"name": "rows", "fields": fields}], None

    if section == "decision_tables":
        blocks = [
            {
                "name": "header",
                "fields": [_field(value) for value in entry["header"].get("fields", [])],
            }
        ]
        for name, key in (("condition", "condition_block"), ("action", "action_block")):
            fields, uncertain = _row_fields(entry[key]["row"])
            if uncertain:
                return blocks, f"Official {name} block has incompatible row variants."
            blocks.append({"name": name, "fields": fields})
        return blocks, None

    if section == "multi_record":
        header_fields = [_field(value) for value in entry["header"].get("fields", [])]
        header_repeat = entry["header"].get("repeat") or {}
        header_fields.extend(
            _field(value, repeated=True) for value in header_repeat.get("fields", [])
        )
        blocks = [{"name": "header", "fields": header_fields}]
        for index, block in enumerate(entry.get("blocks", []), start=1):
            fields, uncertain = _row_fields(block.get("row", {}))
            if uncertain:
                return blocks, "Official multi-record file has incompatible tagged variants."
            blocks.append({"name": f"block_{index}", "fields": fields})
        return blocks, None

    if section in {"multi_section", "runtime_arity"}:
        return [
            {
                "name": value.get("name", f"section_{index}"),
                "fields": [_field(field) for field in value.get("fields", [])],
            }
            for index, value in enumerate(entry.get("sections", []), start=1)
            if value.get("fields")
        ], None

    return [], f"Unsupported official schema section: {section}"


def _normalized_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def compare_effective_schema(
    official: list[dict[str, Any]],
    editor: EffectiveFileSchema,
    *,
    structured: bool,
    official_uncertainty: str | None = None,
) -> dict[str, Any]:
    """Compare ordered token layouts while keeping label differences visible."""

    editor_blocks = [block.to_dict() for block in editor.blocks]
    selected_editor_block: int | None = None
    if structured:
        compared_editor = editor_blocks
    elif official and editor_blocks:
        target_fields = official[0]["fields"]

        def block_score(block: dict[str, Any]) -> tuple[int, int]:
            fields = block["fields"]
            count_gap = abs(len(target_fields) - len(fields))
            type_gap = sum(
                1
                for official_field, editor_field in zip(target_fields, fields)
                if editor_field["field_type"] not in {"unknown", official_field["field_type"]}
            )
            return count_gap, type_gap

        selected_editor_block = min(
            range(len(editor_blocks)),
            key=lambda index: block_score(editor_blocks[index]),
        )
        compared_editor = [editor_blocks[selected_editor_block]]
    else:
        compared_editor = []
    block_count_matches = len(official) == len(compared_editor)
    block_diffs: list[dict[str, Any]] = []
    layout_compatible = block_count_matches
    all_names_exact = True
    all_names_normalized = True
    has_unknown_types = False

    for index in range(max(len(official), len(compared_editor))):
        official_block = official[index] if index < len(official) else None
        editor_block = compared_editor[index] if index < len(compared_editor) else None
        if official_block is None or editor_block is None:
            layout_compatible = False
            block_diffs.append(
                {
                    "position": index,
                    "official_block": official_block and official_block["name"],
                    "editor_block": editor_block and editor_block["name"],
                    "missing_block": True,
                }
            )
            continue

        official_fields = official_block["fields"]
        editor_fields = editor_block["fields"]
        count_matches = len(official_fields) == len(editor_fields)
        type_differences: list[dict[str, Any]] = []
        label_differences: list[dict[str, Any]] = []
        if not count_matches:
            layout_compatible = False
        for position, (official_field, editor_field) in enumerate(
            zip(official_fields, editor_fields)
        ):
            editor_type = editor_field["field_type"]
            if editor_type == "unknown":
                has_unknown_types = True
            elif official_field["field_type"] != editor_type:
                layout_compatible = False
                type_differences.append(
                    {
                        "position": position,
                        "official_name": official_field["name"],
                        "editor_name": editor_field["name"],
                        "official_type": official_field["field_type"],
                        "editor_type": editor_type,
                    }
                )
            if official_field["name"] != editor_field["name"]:
                all_names_exact = False
                normalized_match = _normalized_name(official_field["name"]) == _normalized_name(
                    editor_field["name"]
                )
                all_names_normalized = all_names_normalized and normalized_match
                label_differences.append(
                    {
                        "position": position,
                        "official_name": official_field["name"],
                        "editor_name": editor_field["name"],
                        "normalized_match": normalized_match,
                    }
                )
        block_diffs.append(
            {
                "position": index,
                "official_block": official_block["name"],
                "editor_block": editor_block["name"],
                "official_field_count": len(official_fields),
                "editor_field_count": len(editor_fields),
                "count_matches": count_matches,
                "type_differences": type_differences,
                "label_differences": label_differences,
            }
        )

    incomplete_structured = (
        structured
        and editor.extraction != "manual_canonical"
        and len(editor_blocks) <= 1 < len(official)
    )

    if editor.confidence == "low":
        status = "extraction_needs_review"
        reason = "The Editor writer was not resolved; only its database model is available."
    elif official_uncertainty:
        status = "official_schema_variant"
        reason = official_uncertainty
    elif incomplete_structured:
        status = "extraction_needs_review"
        reason = "Only the first Editor block was extracted from this structured file."
    elif has_unknown_types:
        status = "extraction_needs_review"
        reason = "The writer layout was found, but one or more computed column types are unresolved."
    elif not layout_compatible:
        status = "real_layout_change"
        reason = "The emitted block, column-count, or column-type layout differs."
    elif all_names_exact:
        status = "compatible"
        reason = "The emitted layout and field labels match the official schema."
    else:
        status = "compatible_labels_differ"
        reason = "Column positions and types match; only field labels or implementation names differ."

    return {
        "status": status,
        "reason": reason,
        "layout_compatible": layout_compatible,
        "labels_exact": all_names_exact,
        "labels_normalized": all_names_normalized,
        "has_unknown_types": has_unknown_types,
        "official_block_count": len(official),
        "editor_block_count": len(compared_editor),
        "selected_editor_block": selected_editor_block,
        "editor_additional_blocks_unchecked": (
            len(editor_blocks) - len(compared_editor) if not structured else 0
        ),
        "blocks": block_diffs,
    }
