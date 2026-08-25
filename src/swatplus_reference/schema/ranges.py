"""Carry parameter min/max ranges from the modular database spreadsheet onto the
official SWAT+ input schema.

The modular database workbook (``Modular Database_..._nbs.xlsb``, sheet
``Rev_61_0_nbs``, exported as ``data/modular_database_rev_61_0_nbs.csv``) is the
only place that records a ``Minimum_Range``/``Maximum_Range`` per parameter.
Nothing in the builder has ever read those two columns.  The export is tracked
because it is a hand-maintained input, not a regenerable artifact.

The spreadsheet names parameters the way the SWAT+ Editor database does
(``lai_noevap``, ``sw_init``, ``surq_lag``), while
``schemas/swatplus-<version>.json`` names them the way the Fortran source does
(``evlai``, ``ffcb``, ``surlag``).  Matching the two by name directly therefore
fails on most rows.  The translation between the two vocabularies already
exists: ``reports/swatplus-<version>-editor-schema-report.json`` pairs the Editor
and official field lists per file.  This module routes ranges along that pairing:

    spreadsheet row -> Editor field name -> official Fortran field name

Ranges are only written where that path resolves.  Everything else is reported,
never guessed: a wrong range in a validation artifact is worse than a missing
one, so positional near-misses are surfaced for review rather than applied.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

# Cells the spreadsheet uses to mean "no value".  ``na`` appears 324 times and
# must not be mistaken for a bound.
EMPTY_CELLS = {"", "*", "na", "n/a", "-"}

# Spreadsheet columns this module reads.
COL_FILE = "SWAT_File"
COL_DB_FIELD = "DATABASE_FIELD_NAME"
COL_HEADER = "SWAT_Header_Name"
COL_CODE_VAR = "SWAT_Code_Variable_Name"
COL_POSITION = "Position_in_File"
COL_UNITS = "Units"
COL_DESCRIPTION = "Description"
COL_MIN = "Minimum_Range"
COL_MAX = "Maximum_Range"

# Schema sections that hold per-file layouts.
SCHEMA_SECTIONS = (
    "files",
    "decision_tables",
    "multi_record",
    "multi_section",
    "runtime_arity",
)

FRACTION_UNITS = {"frac", "fraction"}


def clean_cell(value: str | None) -> str:
    """Normalise a spreadsheet cell, mapping the sheet's null spellings to ``""``."""
    text = (value or "").strip()
    return "" if text.lower() in EMPTY_CELLS else text


def parse_bound(value: str | None) -> float | None:
    """Parse a range bound, returning ``None`` when the cell carries no number."""
    text = clean_cell(value)
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


@dataclass(frozen=True, slots=True)
class RangeRow:
    """One spreadsheet row that carries at least one range bound."""

    swat_file: str
    db_field: str
    header_name: str
    code_variable: str
    position: int | None
    units: str
    description: str
    minimum: float | None
    maximum: float | None

    @property
    def names(self) -> tuple[str, ...]:
        """Candidate names for this row, most authoritative first."""
        seen: list[str] = []
        for name in (self.db_field, self.header_name, self.code_variable):
            lowered = name.lower()
            if lowered and lowered not in seen:
                seen.append(lowered)
        return tuple(seen)


@dataclass(slots=True)
class Finding:
    """A row that did not produce a written range."""

    swat_file: str
    name: str
    code: str
    message: str
    minimum: float | None = None
    maximum: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "file": self.swat_file,
            "name": self.name,
            "code": self.code,
            "message": self.message,
            "minimum": self.minimum,
            "maximum": self.maximum,
        }


@dataclass(slots=True)
class CrosswalkResult:
    """Outcome of routing spreadsheet ranges onto the official schema."""

    applied: list[dict[str, Any]] = field(default_factory=list)
    drift: list[Finding] = field(default_factory=list)
    needs_review: list[Finding] = field(default_factory=list)
    quarantined: list[Finding] = field(default_factory=list)
    not_applicable: list[Finding] = field(default_factory=list)

    def summary(self) -> dict[str, int]:
        return {
            "applied": len(self.applied),
            "drift": len(self.drift),
            "needs_review": len(self.needs_review),
            "quarantined": len(self.quarantined),
            "not_applicable": len(self.not_applicable),
        }


def load_range_rows(path: Path) -> list[RangeRow]:
    """Read the spreadsheet export, keeping only rows that carry a bound."""
    rows: list[RangeRow] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for record in csv.DictReader(handle):
            minimum = parse_bound(record.get(COL_MIN))
            maximum = parse_bound(record.get(COL_MAX))
            if minimum is None and maximum is None:
                continue
            swat_file = clean_cell(record.get(COL_FILE))
            if not swat_file:
                continue
            position_text = clean_cell(record.get(COL_POSITION))
            try:
                position = int(float(position_text)) if position_text else None
            except ValueError:
                position = None
            rows.append(
                RangeRow(
                    swat_file=swat_file,
                    db_field=clean_cell(record.get(COL_DB_FIELD)),
                    header_name=clean_cell(record.get(COL_HEADER)),
                    code_variable=clean_cell(record.get(COL_CODE_VAR)),
                    position=position,
                    units=clean_cell(record.get(COL_UNITS)),
                    description=clean_cell(record.get(COL_DESCRIPTION)),
                    minimum=minimum,
                    maximum=maximum,
                )
            )
    return rows


def _blocks(schema: dict[str, Any] | None) -> list[dict[str, Any]]:
    return list((schema or {}).get("blocks") or [])


def build_editor_to_official(report: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Map Editor field names to official field names, per file.

    Two sources are combined, both taken from the existing editor-schema report:

    * ``field_diff.label_differences`` states the pairing outright.
    * blocks whose field counts agree pair up positionally; identical names on
      both sides need no translation.

    Blocks whose counts disagree are skipped.  A field inserted upstream shifts
    every later column, so position is not a safe key there (``sed_nut.cha``
    gained ``n_setl``/``p_setl`` and drifts by two from column five onward).
    """
    mapping: dict[str, dict[str, str]] = {}
    for swat_file, spec in report.items():
        pairs: dict[str, str] = {}
        diff_blocks = _blocks(spec.get("field_diff"))
        editor_blocks = _blocks(spec.get("editor_schema"))
        official_blocks = _blocks(spec.get("official_schema"))

        for block in diff_blocks:
            if not block.get("count_matches"):
                continue
            for label in block.get("label_differences") or []:
                editor_name = str(label.get("editor_name") or "").lower()
                official_name = str(label.get("official_name") or "").lower()
                if editor_name and official_name:
                    pairs[editor_name] = official_name

        for index, editor_block in enumerate(editor_blocks):
            if index >= len(official_blocks):
                break
            editor_fields = editor_block.get("fields") or []
            official_fields = official_blocks[index].get("fields") or []
            if len(editor_fields) != len(official_fields):
                continue
            for editor_field, official_field in zip(editor_fields, official_fields):
                editor_name = str(editor_field.get("name") or "").lower()
                official_name = str(official_field.get("name") or "").lower()
                if editor_name and official_name:
                    pairs.setdefault(editor_name, official_name)

        if pairs:
            mapping[swat_file] = pairs
    return mapping


def build_editor_inventory(report: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Map every real Editor database column name to itself, per file.

    Unlike :func:`build_editor_to_official`, this does not require the column
    to resolve to an official field - it is the full ``editor_schema`` column
    list straight from the Editor's own ORM models, keyed by lowercased name
    so a spreadsheet cell can be checked against it directly. A name missing
    here was never in the Editor database, regardless of whether it also
    happens to match a source variable name.
    """
    inventory: dict[str, dict[str, str]] = {}
    for swat_file, spec in report.items():
        names: dict[str, str] = {}
        for block in _blocks(spec.get("editor_schema")):
            for entry in block.get("fields") or []:
                name = str(entry.get("name") or "")
                if name:
                    names.setdefault(name.lower(), name)
        if names:
            inventory[swat_file] = names
    return inventory


def iter_field_lists(node: Any) -> Iterator[list[dict[str, Any]]]:
    """Yield every ``fields`` list reachable in a schema file spec.

    Schema sections differ in shape (``blocks``/``sections``/``header``/
    ``repeat``/``condition_block``), so the walk is structural rather than a
    fixed set of keys.
    """
    if isinstance(node, dict):
        fields = node.get("fields")
        if isinstance(fields, list) and all(isinstance(item, dict) for item in fields):
            yield fields
        for key, value in node.items():
            if key == "fields":
                continue
            yield from iter_field_lists(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_field_lists(item)


def schema_file_specs(schema: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Collect the file specs the schema describes, keyed by file name."""
    specs: dict[str, list[dict[str, Any]]] = {}
    for section in SCHEMA_SECTIONS:
        for swat_file, spec in (schema.get(section) or {}).items():
            specs.setdefault(swat_file, []).append(spec)
    return specs


def schema_field_index(specs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Index a file's schema fields by lowercased Fortran name."""
    index: dict[str, list[dict[str, Any]]] = {}
    for spec in specs:
        for fields in iter_field_lists(spec):
            for entry in fields:
                name = str(entry.get("fortran_name") or entry.get("name") or "").lower()
                if name:
                    index.setdefault(name, []).append(entry)
    return index


def quarantine_reason(
    row: RangeRow, targets: list[dict[str, Any]]
) -> tuple[str, str] | None:
    """Return ``(code, message)`` when a resolved range must not be written."""
    low, high = row.minimum, row.maximum
    if low is not None and high is not None:
        if low == 0.0 and high == 0.0:
            return ("placeholder_zero_range", "Both bounds are 0; a placeholder, not a range.")
        if high < low:
            return ("inverted_range", f"Maximum {high} is below minimum {low}.")
    if high is not None and high > 1.0:
        units = row.units.lower()
        description = row.description.lower()
        if units in FRACTION_UNITS or "fraction" in description:
            return (
                "fraction_bound_conflict",
                f"Row is described as a fraction but the maximum is {high}.",
            )
    if any(entry.get("numeric") is False for entry in targets):
        return (
            "range_on_non_numeric_field",
            "The schema marks this field non-numeric, so a numeric range cannot apply.",
        )
    return None


def crosswalk(
    rows: list[RangeRow],
    editor_map: dict[str, dict[str, str]],
    schema: dict[str, Any],
) -> CrosswalkResult:
    """Route each spreadsheet range onto an official schema field."""
    result = CrosswalkResult()
    specs = schema_file_specs(schema)
    indexes = {name: schema_field_index(spec) for name, spec in specs.items()}

    for row in rows:
        if row.swat_file not in specs:
            result.not_applicable.append(
                Finding(
                    row.swat_file,
                    row.db_field,
                    "file_not_in_input_schema",
                    "The official input schema does not describe this file (output files are out of scope).",
                    row.minimum,
                    row.maximum,
                )
            )
            continue

        index = indexes[row.swat_file]
        pairs = editor_map.get(row.swat_file, {})
        official_name = ""
        route = ""
        for candidate in row.names:
            translated = pairs.get(candidate)
            if translated and translated in index:
                official_name, route = translated, "editor_map"
                break
            if candidate in index:
                official_name, route = candidate, "direct_name"
                break

        if not official_name:
            code, message = (
                ("no_editor_mapping", "This file has no Editor pairing, so the name could not be translated.")
                if not pairs
                else ("name_not_in_schema", "No official field matches this spreadsheet name.")
            )
            bucket = result.needs_review if not pairs else result.drift
            bucket.append(
                Finding(row.swat_file, row.db_field, code, message, row.minimum, row.maximum)
            )
            continue

        targets = index[official_name]
        reason = quarantine_reason(row, targets)
        if reason is not None:
            code, message = reason
            result.quarantined.append(
                Finding(row.swat_file, official_name, code, message, row.minimum, row.maximum)
            )
            continue

        for entry in targets:
            if row.minimum is not None:
                entry["minimum"] = row.minimum
            if row.maximum is not None:
                entry["maximum"] = row.maximum
            entry["range_source"] = "modular_database_rev_61_0_nbs"
        result.applied.append(
            {
                "file": row.swat_file,
                "spreadsheet_name": row.db_field,
                "official_name": official_name,
                "route": route,
                "minimum": row.minimum,
                "maximum": row.maximum,
                "units": row.units or None,
                "description": row.description or None,
            }
        )
    return result


def render_markdown(result: CrosswalkResult, source: str, schema_version: str) -> str:
    """Render the crosswalk outcome as a maintainer-facing Markdown report."""
    summary = result.summary()
    applicable = summary["applied"] + summary["drift"] + summary["needs_review"] + summary["quarantined"]
    lines = [
        f"# Parameter Range Crosswalk: SWAT+ {schema_version}",
        "",
        f"Ranges carried from `{source}` onto the official input schema by translating",
        "spreadsheet (Editor) names into official Fortran names through the existing",
        "editor-schema report.",
        "",
        "| Outcome | Count |",
        "|---|---:|",
        f"| Applied to schema | {summary['applied']} |",
        f"| Drift - name no longer in schema | {summary['drift']} |",
        f"| Needs review - no Editor pairing | {summary['needs_review']} |",
        f"| Quarantined - range contradicts the row | {summary['quarantined']} |",
        f"| Not applicable - file outside the input schema | {summary['not_applicable']} |",
        "",
        f"Applicable rows: {applicable}. Applied: {summary['applied']}.",
        "",
    ]

    def table(title: str, findings: list[Finding], note: str) -> None:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(note)
        lines.append("")
        if not findings:
            lines.append("None.")
            lines.append("")
            return
        lines.append("| File | Name | Min | Max | Code | Detail |")
        lines.append("|---|---|---:|---:|---|---|")
        for item in sorted(findings, key=lambda f: (f.swat_file, f.name)):
            low = "" if item.minimum is None else f"{item.minimum:g}"
            high = "" if item.maximum is None else f"{item.maximum:g}"
            lines.append(
                f"| `{item.swat_file}` | `{item.name}` | {low} | {high} | `{item.code}` | {item.message} |"
            )
        lines.append("")

    table(
        "Drift",
        result.drift,
        "The spreadsheet names a parameter the current schema no longer has. These are "
        "the genuine rename or removal candidates and need a human decision.",
    )
    table(
        "Needs review",
        result.needs_review,
        "These files have no Editor pairing to translate through. Column position lines "
        "the two sides up only when no field was inserted upstream, so nothing is "
        "applied automatically here.",
    )
    table(
        "Quarantined",
        result.quarantined,
        "A name resolved, but the range contradicts the row's own units, description, or "
        "field type. A wrong range is worse than a missing one, so these are withheld.",
    )
    return "\n".join(lines) + "\n"


def build_range_crosswalk(
    spreadsheet: Path,
    report_path: Path,
    schema_path: Path,
    output_dir: Path,
    reports_dir: Path | None = None,
) -> CrosswalkResult:
    """Run the crosswalk and write the enriched schema plus both report forms."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8")).get("files") or {}
    rows = load_range_rows(spreadsheet)
    editor_map = build_editor_to_official(report)
    result = crosswalk(rows, editor_map, schema)

    version = str(schema.get("swatplus_version") or "unknown")
    schema["range_source"] = spreadsheet.name
    schema["range_summary"] = result.summary()

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"swatplus-{version}-ranges.json").write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    reports_dir = reports_dir or output_dir.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / f"swatplus-{version}-range-crosswalk.json").write_text(
        json.dumps(
            {
                "summary": result.summary(),
                "source": spreadsheet.name,
                "swatplus_version": version,
                "applied": result.applied,
                "drift": [f.to_dict() for f in result.drift],
                "needs_review": [f.to_dict() for f in result.needs_review],
                "quarantined": [f.to_dict() for f in result.quarantined],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (reports_dir / f"swatplus-{version}-range-crosswalk.md").write_text(
        render_markdown(result, spreadsheet.name, version), encoding="utf-8"
    )
    return result


def main(argv: list[str] | None = None) -> int:
    """CLI: carry spreadsheet ranges onto the official input schema."""
    parser = argparse.ArgumentParser(
        prog="swatplus-doc-parameter-ranges",
        description="Carry modular-database ranges onto the official SWAT+ input schema.",
    )
    parser.add_argument(
        "--spreadsheet",
        default="data/modular_database_rev_61_0_nbs.csv",
        help="Modular database CSV export",
    )
    parser.add_argument(
        "--editor-report",
        default="reports/swatplus-62.0.0-editor-schema-report.json",
        help="Editor schema report that pairs Editor and official field names",
    )
    parser.add_argument(
        "--schema",
        default="schemas/swatplus-62.0.0.json",
        help="Official input schema to enrich",
    )
    parser.add_argument("--output", default="schemas", help="Directory for the enriched schema")
    args = parser.parse_args(argv)

    spreadsheet = Path(args.spreadsheet)
    if not spreadsheet.exists():
        parser.error(f"{spreadsheet} not found; pass --spreadsheet to point at the export.")
    result = build_range_crosswalk(
        spreadsheet, Path(args.editor_report), Path(args.schema), Path(args.output)
    )
    summary = result.summary()
    for key in ("applied", "drift", "needs_review", "quarantined", "not_applicable"):
        print(f"{key}: {summary[key]}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
