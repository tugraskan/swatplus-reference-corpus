"""Semantic input-schema comparison policy and path-level evidence.

The full schema diff intentionally compares the original payloads. This module
adds a second view that classifies every changed path without discarding source
provenance or secondary changes in the same input file.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any


SCHEMA_SECTIONS = (
    "files",
    "decision_tables",
    "multi_record",
    "multi_section",
    "runtime_arity",
)
UNRESOLVED_SECTIONS = (
    "unresolved",
    "decision_tables_unresolved",
    "multi_record_unresolved",
    "multi_section_unresolved",
    "runtime_arity_unresolved",
)

STRUCTURAL = "structural"
DOCUMENTATION = "documentation"
SOURCE_LOCATION = "source_location"
SOURCE_ORGANIZATION = "source_organization"
UNCERTAIN = "uncertain"
CATEGORIES = (
    STRUCTURAL,
    DOCUMENTATION,
    SOURCE_LOCATION,
    SOURCE_ORGANIZATION,
    UNCERTAIN,
)

# Explicit policy: a future extractor key must be reviewed rather than being
# silently treated as an input-contract change or as disposable metadata.
_STRUCTURAL_KEYS = frozenset({
    "action_block", "action_typ", "action_vocabulary", "applies_when",
    "blocks", "cases", "condition_block", "condition_var",
    "condition_vocabulary", "count", "count_expr", "count_field",
    "count_literal", "count_source", "derived_type", "fields",
    "fortran_name", "fortran_type", "header", "header_fields", "name",
    "nested_file_field", "numeric", "other", "other_vocabularies",
    "position", "read_pattern", "repeat", "repeat_expr", "repeat_fields",
    "repeat_source", "row", "row_count_field", "row_fields", "row_repeat",
    "row_suffix_fields", "sections", "subject", "suffix_fields", "tag", "tag_field",
    "units", "variable_arity", "variable_width", "variants", "vocabulary",
})
_DYNAMIC_STRUCTURAL_MAPS = frozenset({
    "variants", "vocabulary", "condition_vocabulary",
    "action_vocabulary", "other_vocabularies",
})
_TYPE_SOURCE_RE = re.compile(r"^(.*?)(?::(\d+(?:-\d+)?))?$")
_MISSING = object()
MAX_COMPARISON_DEPTH = 64


def _unresolved_map(payload: dict[str, Any], section: str) -> dict[str, str]:
    return {
        str(item.get("file")): str(item.get("reason", ""))
        for item in payload.get(section, [])
    }


def _split_type_source(value: str | None) -> tuple[str | None, str | None]:
    """Return the source path and optional line range."""
    if not value:
        return None, None
    match = _TYPE_SOURCE_RE.fullmatch(str(value))
    if match is None:
        return str(value), None
    return match.group(1) or None, match.group(2)


def _strip_and_normalize(obj: Any) -> Any:
    """Legacy helper for inspecting payloads without source line positions.

    Classification does not use this lossy representation: it would erase a
    nested reader move and conflate it with a line-number change.
    """
    if isinstance(obj, dict):
        result: dict[str, Any] = {}
        for key, value in obj.items():
            if key in ("reader_line", "reader"):
                continue
            if key == "type_source":
                result[key] = _split_type_source(value)[0]
            else:
                result[key] = _strip_and_normalize(value)
        return result
    if isinstance(obj, list):
        return [_strip_and_normalize(item) for item in obj]
    return obj


def _pointer(path: str, part: str | int) -> str:
    escaped = str(part).replace("~", "~0").replace("/", "~1")
    return path + "/" + escaped


def _event(
    path: str, category: str, before: Any = _MISSING, after: Any = _MISSING
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": path or "/",
        "category": category,
        "base_present": before is not _MISSING,
        "candidate_present": after is not _MISSING,
    }
    if before is not _MISSING:
        result["base"] = before
    if after is not _MISSING:
        result["candidate"] = after
    return result


def _shape(value: Any) -> str:
    if isinstance(value, dict):
        return "dict"
    if isinstance(value, list):
        return "list"
    return "scalar"


def _bounded_event(
    path: str, category: str, reason: str, before: Any, after: Any
) -> dict[str, Any]:
    """Keep evidence serializable even if either value is deeply nested."""
    result = {
        "path": path or "/",
        "category": category,
        "reason": reason,
        "base_present": True,
        "candidate_present": True,
        "base_type": type(before).__name__,
        "candidate_type": type(after).__name__,
    }
    if _shape(before) == "scalar":
        result["base"] = before
    if _shape(after) == "scalar":
        result["candidate"] = after
    return result


def _scalar_order_key(value: Any) -> tuple[str, str]:
    return type(value).__name__, repr(value)


def _field_identities(values: list[Any]) -> list[str] | None:
    if not values or not all(isinstance(item, dict) for item in values):
        return None
    identities = [
        str(item.get("name") or item.get("fortran_name") or "")
        for item in values
    ]
    if any(not identity for identity in identities) or len(set(identities)) != len(values):
        return None
    return identities


def _category_for_key(key: str, parent_key: str | None) -> str:
    if key == "doc":
        return DOCUMENTATION
    if key == "reader_line":
        return SOURCE_LOCATION
    if key == "reader":
        return SOURCE_ORGANIZATION
    if key in _STRUCTURAL_KEYS or parent_key in _DYNAMIC_STRUCTURAL_MAPS:
        return STRUCTURAL
    return UNCERTAIN


def _compare(
    before: Any,
    after: Any,
    path: str = "",
    *,
    key: str | None = None,
    parent_key: str | None = None,
    depth: int = 0,
) -> list[dict[str, Any]]:
    """Classify every leaf difference; paths use JSON Pointer escaping."""
    if before is after:
        return []
    if before is _MISSING or after is _MISSING:
        category = _category_for_key(key or "", parent_key)
        if key == "type_source":
            category = SOURCE_ORGANIZATION
        present = after if before is _MISSING else before
        if _shape(present) != "scalar":
            return [{
                "path": path or "/",
                "category": category,
                "reason": "key_added" if before is _MISSING else "key_removed",
                "base_present": before is not _MISSING,
                "candidate_present": after is not _MISSING,
                "value_type": type(present).__name__,
            }]
        return [_event(path, category, before, after)]

    if _shape(before) != _shape(after):
        return [_bounded_event(
            path, STRUCTURAL, "schema_shape_change", before, after
        )]

    if _shape(before) == "scalar":
        if type(before) is not type(after):
            category = (
                UNCERTAIN if key == "type_source"
                else _category_for_key(key or "", parent_key)
            )
            return [_bounded_event(
                path, category, "value_type_change", before, after
            )]
        if before == after:
            return []

    if depth >= MAX_COMPARISON_DEPTH:
        return [{
            "path": path or "/",
            "category": UNCERTAIN,
            "reason": "comparison_depth_limit_exceeded",
            "base_present": True,
            "candidate_present": True,
            "base_type": type(before).__name__,
            "candidate_type": type(after).__name__,
            "depth": depth,
            "limit": MAX_COMPARISON_DEPTH,
        }]

    if key == "type_source":
        before_file, before_range = _split_type_source(before)
        after_file, after_range = _split_type_source(after)
        changes = []
        if before_file != after_file:
            changes.append(_event(path, SOURCE_ORGANIZATION, before, after))
        if before_range != after_range:
            changes.append(_event(path, SOURCE_LOCATION, before, after))
        return changes or [_event(path, UNCERTAIN, before, after)]

    if isinstance(before, dict) and isinstance(after, dict):
        changes: list[dict[str, Any]] = []
        for child in sorted(before.keys() | after.keys()):
            changes.extend(_compare(
                before.get(child, _MISSING),
                after.get(child, _MISSING),
                _pointer(path, child),
                key=child,
                parent_key=key,
                depth=depth + 1,
            ))
        return changes

    if isinstance(before, list) and isinstance(after, list):
        changes = []
        if (
            len(before) == len(after)
            and all(_shape(value) == "scalar" for value in before + after)
        ):
            base_order = [_scalar_order_key(value) for value in before]
            candidate_order = [_scalar_order_key(value) for value in after]
            if base_order != candidate_order and Counter(base_order) == Counter(
                candidate_order
            ):
                return [_event(
                    _pointer(path, "@order"), STRUCTURAL, before, after
                )]

        base_ids = _field_identities(before)
        candidate_ids = _field_identities(after)
        if base_ids is not None and candidate_ids is not None:
            base_map = dict(zip(base_ids, before))
            candidate_map = dict(zip(candidate_ids, after))
            common = base_map.keys() & candidate_map.keys()
            base_order = [identity for identity in base_ids if identity in common]
            candidate_order = [
                identity for identity in candidate_ids if identity in common
            ]
            if base_order != candidate_order:
                changes.append(_event(
                    _pointer(path, "@order"), STRUCTURAL, base_order, candidate_order
                ))
            # A same-length rename at a stable position is compared by index:
            # this retains its simultaneous documentation change.
            if len(before) != len(after) or set(base_ids) == set(candidate_ids):
                for identity in sorted(base_map.keys() | candidate_map.keys()):
                    changes.extend(_compare(
                        base_map.get(identity, _MISSING),
                        candidate_map.get(identity, _MISSING),
                        _pointer(path, identity),
                        key=key,
                        depth=depth + 1,
                    ))
                return changes

        if len(before) != len(after):
            changes.append(_event(
                _pointer(path, "@length"), STRUCTURAL, len(before), len(after)
            ))
        for index in range(max(len(before), len(after))):
            changes.extend(_compare(
                before[index] if index < len(before) else _MISSING,
                after[index] if index < len(after) else _MISSING,
                _pointer(path, index),
                key=key,
                depth=depth + 1,
            ))
        return changes

    return [_event(path, _category_for_key(key or "", parent_key), before, after)]


def _semantic_field_diff(
    before: dict[str, Any], after: dict[str, Any]
) -> dict[str, Any]:
    """Field-level view retained for callers inspecting one entry."""
    base_fields = before.get("fields", [])
    candidate_fields = after.get("fields", [])
    changes = _compare(base_fields, candidate_fields, "/fields", key="fields")
    structural = [change for change in changes if change["category"] == STRUCTURAL]
    documentation = [
        change for change in changes if change["category"] == DOCUMENTATION
    ]
    base_ids = _field_identities(base_fields)
    candidate_ids = _field_identities(candidate_fields)
    if base_ids is not None and candidate_ids is not None:
        base_map = dict(zip(base_ids, base_fields))
        candidate_map = dict(zip(candidate_ids, candidate_fields))
        unchanged_count = sum(
            not _compare(base_map[identity], candidate_map[identity])
            for identity in base_map.keys() & candidate_map.keys()
        )
    else:
        unchanged_count = sum(
            not _compare(base_field, candidate_field)
            for base_field, candidate_field in zip(base_fields, candidate_fields)
        )
    return {
        "added": [
            change["path"] for change in structural
            if not change["base_present"]
        ],
        "removed": [
            change["path"] for change in structural
            if not change["candidate_present"]
        ],
        "structural_changed": [change["path"] for change in structural],
        "documentation_changed": [change["path"] for change in documentation],
        "structural_changed_details": structural,
        "documentation_changed_details": documentation,
        "unchanged_count": unchanged_count,
    }


def _semantic_section_diff(
    base: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    base_names = set(base)
    candidate_names = set(candidate)
    added = sorted(candidate_names - base_names)
    removed = sorted(base_names - candidate_names)
    changed: list[str] = []
    unchanged_count = 0

    membership: dict[str, list[str]] = {category: [] for category in CATEGORIES}
    documentation_only: list[str] = []
    location_only: list[str] = []
    entry_details: dict[str, Any] = {}
    for name in sorted(base_names & candidate_names):
        changes = _compare(base[name], candidate[name])
        if not changes:
            unchanged_count += 1
            continue
        changed.append(name)
        categories = {change["category"] for change in changes}
        for category in CATEGORIES:
            if category in categories:
                membership[category].append(name)
        # Source line shifts do not disqualify a documentation-only headline.
        if DOCUMENTATION in categories and categories <= {
            DOCUMENTATION, SOURCE_LOCATION
        }:
            documentation_only.append(name)
        if categories == {SOURCE_LOCATION}:
            location_only.append(name)
        entry_details[name] = {
            "categories": [category for category in CATEGORIES if category in categories],
            "changes": changes,
        }

    def details_for(category: str, names: list[str]) -> dict[str, Any]:
        return {
            name: {
                "changed_paths": [
                    change["path"] for change in entry_details[name]["changes"]
                    if change["category"] == category
                ]
            }
            for name in names
        }

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged_count": unchanged_count,
        "structural_changes": membership[STRUCTURAL],
        "documentation_changes": membership[DOCUMENTATION],
        "documentation_only_changes": documentation_only,
        "source_location_changes": membership[SOURCE_LOCATION],
        "source_location_only_changes": location_only,
        "source_organization_changes": membership[SOURCE_ORGANIZATION],
        "uncertain_changes": membership[UNCERTAIN],
        "structural_details": details_for(STRUCTURAL, membership[STRUCTURAL]),
        "documentation_details": details_for(
            DOCUMENTATION, membership[DOCUMENTATION]
        ),
        "source_location_only_details": details_for(
            SOURCE_LOCATION, location_only
        ),
        "source_organization_details": details_for(
            SOURCE_ORGANIZATION, membership[SOURCE_ORGANIZATION]
        ),
        "uncertain_details": details_for(UNCERTAIN, membership[UNCERTAIN]),
        "entry_details": entry_details,
    }


def _semantic_schema_diff(
    base: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    """Compare schema entries and count both entries and unique filenames."""
    semantic_sections: dict[str, Any] = {}
    changed_names: set[str] = set()
    names_by_category: dict[str, set[str]] = {
        category: set() for category in CATEGORIES
    }
    counts = {category: 0 for category in CATEGORIES}
    documentation_only = 0
    location_only = 0
    changed_entries = 0

    for section in SCHEMA_SECTIONS:
        diff = _semantic_section_diff(
            base.get(section, {}), candidate.get(section, {})
        )
        semantic_sections[section] = diff
        all_names = set(diff["added"] + diff["removed"] + diff["changed"])
        changed_names.update(all_names)
        changed_entries += len(all_names)
        structural_names = set(
            diff["added"] + diff["removed"] + diff["structural_changes"]
        )
        for category, names in (
            (STRUCTURAL, structural_names),
            (DOCUMENTATION, set(diff["documentation_changes"])),
            (SOURCE_LOCATION, set(diff["source_location_changes"])),
            (SOURCE_ORGANIZATION, set(diff["source_organization_changes"])),
            (UNCERTAIN, set(diff["uncertain_changes"])),
        ):
            counts[category] += len(names)
            names_by_category[category].update(names)
        documentation_only += len(diff["documentation_only_changes"])
        location_only += len(diff["source_location_only_changes"])

    unresolved: dict[str, Any] = {}
    new_unresolved_total = 0
    changed_unresolved_reasons = 0
    base_unresolved_files: set[str] = set()
    candidate_unresolved_files: set[str] = set()
    for section in UNRESOLVED_SECTIONS:
        before = _unresolved_map(base, section)
        after = _unresolved_map(candidate, section)
        new = sorted(set(after) - set(before))
        resolved = sorted(set(before) - set(after))
        changed = {
            name: {"base": before[name], "candidate": after[name]}
            for name in sorted(set(before) & set(after))
            if before[name] != after[name]
        }
        new_unresolved_total += len(new)
        changed_unresolved_reasons += len(changed)
        base_unresolved_files.update(before.keys())
        candidate_unresolved_files.update(after.keys())
        unresolved[section] = {
            "base_count": len(before),
            "candidate_count": len(after),
            "new": new,
            "resolved": resolved,
            "changed_reasons": changed,
        }

    # Cross-reference: which newly-added schema entries were previously
    # unresolved in the base?  These are "unresolved → resolved" transitions
    # rather than genuinely new input files.
    added_names = set()
    for section in SCHEMA_SECTIONS:
        diff = semantic_sections[section]
        added_names.update(diff["added"])

    previously_unresolved_now_added = sorted(
        name for name in added_names if name in base_unresolved_files
    )
    genuinely_new_files = sorted(
        name for name in added_names if name not in base_unresolved_files
    )

    return {
        "summary": {
            "base_flat_files": len(base.get("files", {})),
            "candidate_flat_files": len(candidate.get("files", {})),
            "changed_schema_entries": changed_entries,
            "unique_changed_input_files": len(changed_names),
            "structural_changes": counts[STRUCTURAL],
            "documentation_changes": counts[DOCUMENTATION],
            "documentation_only_changes": documentation_only,
            "source_location_changes": counts[SOURCE_LOCATION],
            "source_location_only_changes": location_only,
            "source_organization_changes": counts[SOURCE_ORGANIZATION],
            "uncertain_changes": counts[UNCERTAIN],
            "unique_input_files_by_category": {
                category: len(names_by_category[category])
                for category in CATEGORIES
            },
            "new_unresolved": new_unresolved_total,
            "changed_unresolved_reasons": changed_unresolved_reasons,
            "previously_unresolved_now_resolved": len(
                previously_unresolved_now_added
            ),
            "genuinely_new_files": len(genuinely_new_files),
        },
        "counting": {
            "changed_schema_entries": "Sum of added, removed, and changed entries across schema sections.",
            "unique_changed_input_files": "Distinct entry names across schema sections.",
            "category_counts": "Entry memberships; mixed entries appear in multiple categories.",
        },
        "semantic_sections": semantic_sections,
        "unresolved_sections": unresolved,
        "resolved_unresolved_transitions": {
            "previously_unresolved_now_resolved": previously_unresolved_now_added,
            "genuinely_new_files": genuinely_new_files,
        },
        "metadata": {
            "base_commit": base.get("source_ref"),
            "candidate_commit": candidate.get("source_ref"),
            "base_version": base.get("swatplus_version"),
            "candidate_version": candidate.get("swatplus_version"),
        },
    }
