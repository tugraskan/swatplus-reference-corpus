"""Per-file map from modular database columns to SWAT+ source variables.

Answers one question for each SWAT+ input file: which spreadsheet column is which
Fortran variable, and what does each side say about it. This starts from the
spreadsheet's own filename for each file, corrected first against
``FILE_NAME_ALIASES`` where the spreadsheet's name for the file itself, not
just a column within it, disagrees with the schema (e.g. ``res.dtl`` for what
the schema and the model's own reader call ``res_rel.dtl``) - otherwise every
row for that file is silently absent from this report rather than reported
as unmatched.

Three vocabularies describe the same parameter and none of them agree on names.
The modular database calls it ``lai_noevap`` (the SWAT+ Editor's database column),
the Fortran source calls it ``evlai``, and the schema records the type the reader
expects.  :mod:`swatplus_reference.schema.ranges` already resolves that
pairing in order to carry ranges across; this module reports the pairing itself,
for every row rather than only the rows that happen to carry a range.

The spreadsheet's own ``DATABASE_FIELD_NAME`` column is a hand-typed guess at
what the Editor calls a parameter - it can drift from the Editor's actual ORM
column name without anyone noticing, and a spreadsheet-to-source match that
routes through a stale guess is not verified, only coincidental. Each row is
therefore also checked directly against the Editor's real column inventory
(``editor_schema`` in the editor-schema report, independent of whether that
column resolved to a source field): ``editor_check`` says whether the name was
found there (``verified``), was not (``mismatch``), or the file carries no
Editor schema data to check against (``unavailable``). A row can be
``editor_check=verified`` and still ``status=spreadsheet_only`` - the Editor
database confirms the spreadsheet's name, but the source-side pairing did not
resolve (e.g. the file's block layout does not line up positionally).

Unmatched rows are listed too, but not every unmatched row is a real mismatch.
Two things short-circuit a real dropped-or-renamed-parameter reading:

* A compound code-variable cell like ``hru/props`` names two things at once -
  the Editor's word for it and the source's. Matched whole, it matches
  nothing; split on ``/``, either half may resolve. ``route`` gets a
  ``_split`` suffix (e.g. ``direct_name_split``) when a split half, not the
  whole cell, is what matched.
* A code-variable cell of ``*`` (or blank) is the spreadsheet's own marker
  for a row that was never a single named field - a repeat-block header or
  file-level note copied into every file's section. These are flagged
  ``structural`` and are not counted as drift. A row the Editor database
  confirms as a real column is never structural, whatever its code-variable
  cell says: a genuine Editor field can simply have no Fortran counterpart
  recorded.
* A handful of names are wrong on both sides of the spreadsheet row at once -
  not a translatable compound cell, just a stale name neither the Editor nor
  the source actually uses (``KNOWN_NAME_ALIASES``, e.g. decision-table
  ``act_name``/``act_option`` for the Editor and source's bare
  ``name``/``option``). ``route`` gets an ``_alias`` suffix when one of these
  is what matched.

A spreadsheet row with no counterpart, and not structural, is a parameter the
code renamed or dropped; a source field with no row is one the spreadsheet
never documented.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .ranges import (
    COL_CODE_VAR,
    COL_DB_FIELD,
    COL_DESCRIPTION,
    COL_FILE,
    COL_HEADER,
    COL_MAX,
    COL_MIN,
    COL_UNITS,
    SCHEMA_SECTIONS,
    build_editor_inventory,
    build_editor_to_official,
    clean_cell,
    iter_field_lists,
    parse_bound,
)

COL_DATA_TYPE = "Data_Type"

# Known spreadsheet name -> real name corrections, for rows where the
# spreadsheet's own DATABASE_FIELD_NAME *and* its own code-variable cell both
# give a name that neither the Editor nor the source actually uses - not a
# translatable compound cell (see _expand_candidates), just a wrong name on
# both sides at once. Decision-table action rows prefix "act_" for
# readability in the sheet; the Editor (D_table_dtl_act.name/.option in
# decision_table.py) and the official schema (action_block.row.fields) both
# use the bare name.
KNOWN_NAME_ALIASES = {
    "act_name": "name",
    "act_option": "option",
}


@dataclass(slots=True)
class MappedField:
    """One parameter, as the spreadsheet and the source each describe it."""

    editor_name: str = ""
    editor_type: str = ""
    editor_units: str = ""
    editor_description: str = ""
    minimum: float | None = None
    maximum: float | None = None
    code_name: str = ""
    code_type: str = ""
    code_units: str = ""
    code_description: str = ""
    status: str = "matched"
    route: str = ""
    editor_db_name: str = ""
    editor_check: str = ""
    structural: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "route": self.route,
            "structural": self.structural,
            "spreadsheet": {
                "name": self.editor_name or None,
                "type": self.editor_type or None,
                "units": self.editor_units or None,
                "description": self.editor_description or None,
                "minimum": self.minimum,
                "maximum": self.maximum,
            },
            "source": {
                "name": self.code_name or None,
                "type": self.code_type or None,
                "units": self.code_units or None,
                "description": self.code_description or None,
            },
            "editor_database": {
                "name": self.editor_db_name or None,
                "check": self.editor_check or None,
            },
        }


@dataclass(slots=True)
class FileMap:
    """Every parameter of one SWAT+ input file, from both sides."""

    swat_file: str
    fields: list[MappedField] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        tally: dict[str, int] = {}
        for item in self.fields:
            tally[item.status] = tally.get(item.status, 0) + 1
        return tally


# Known spreadsheet SWAT_File value -> the schema's real name for that file,
# where the two disagree on the filename itself rather than on a field within
# it. Confirmed by finding each real file's actual reader in the Fortran
# source, not guessed from similarity: e.g. lum.dtl/scen_lu.dtl/flo_con.dtl's
# sibling decision-table file is spelled "res.dtl" in the spreadsheet but the
# schema (and the file the model actually reads) calls it "res_rel.dtl".
# A spreadsheet file with no entry here and no schema counterpart either
# isn't necessarily a gap - most turn out to name a file SWAT+ 62.0.0 never
# actually reads (a declared-but-unused default filename, or an output file,
# both out of scope for an input schema), checked in the source per case
# rather than assumed.
FILE_NAME_ALIASES = {
    "res.dtl": "res_rel.dtl",
    "atmo.cli": "atmodep.cli",
    "cons_prac.lum": "cons_practice.lum",
    "path_hru_ini": "path_hru.ini",
    "salt_hru_ini": "salt_hru.ini",
}


def load_spreadsheet_rows(path: Path) -> dict[str, list[dict[str, str]]]:
    """Read every spreadsheet row, grouped by SWAT+ file and kept in sheet order."""
    grouped: dict[str, list[dict[str, str]]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for record in csv.DictReader(handle):
            swat_file = clean_cell(record.get(COL_FILE))
            swat_file = FILE_NAME_ALIASES.get(swat_file, swat_file)
            if swat_file:
                grouped.setdefault(swat_file, []).append(record)
    return grouped


def source_fields(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index a file's schema fields by Fortran name, preserving declared order."""
    fields: dict[str, dict[str, Any]] = {}
    for group in iter_field_lists(spec):
        for entry in group:
            name = str(entry.get("fortran_name") or entry.get("name") or "")
            if name and name.lower() not in fields:
                fields[name.lower()] = entry
    return fields


def _expand_candidates(raw: str) -> list[str]:
    """Try a compound cell like "hru/props" as itself, then as each half.

    The modular database sometimes names a pointer field with two words
    joined by a slash - one side echoing the Editor's name for it, the other
    the source's. Whole, it matches nothing; split, either half may resolve.
    """
    if not raw:
        return []
    if "/" not in raw:
        return [raw]
    seen: list[str] = []
    for part in [raw, *(p.strip() for p in raw.split("/"))]:
        if part and part not in seen:
            seen.append(part)
    return seen


def build_file_map(
    swat_file: str,
    rows: list[dict[str, str]],
    spec: dict[str, Any],
    editor_pairs: dict[str, str],
    editor_inventory: dict[str, str] | None = None,
) -> FileMap:
    """Pair one file's spreadsheet rows with its source fields.

    ``editor_pairs`` resolves an Editor column to a source field name (used to
    find ``code_key``/``route`` below, unchanged from before). ``editor_inventory``
    is a separate, independent check: the full set of real Editor database
    column names for this file, regardless of whether they resolved to a
    source field. It verifies the spreadsheet's own name claim rather than
    relying on it having produced a usable pairing.
    """
    available = source_fields(spec)
    result = FileMap(swat_file=swat_file)
    claimed: set[str] = set()

    for record in rows:
        raw_cells = [
            clean_cell(record.get(column)).lower()
            for column in (COL_DB_FIELD, COL_HEADER, COL_CODE_VAR)
        ]
        candidates: list[str] = []
        origins: dict[str, str] = {}
        for raw in raw_cells:
            for candidate in _expand_candidates(raw):
                if candidate not in candidates:
                    candidates.append(candidate)
                    origins[candidate] = "raw" if candidate == raw else "split"
                alias = KNOWN_NAME_ALIASES.get(candidate)
                if alias and alias not in candidates:
                    candidates.append(alias)
                    origins[alias] = "alias"

        code_key = ""
        route = ""
        for candidate in candidates:
            if not candidate:
                continue
            origin = origins.get(candidate, "raw")
            suffix = "" if origin == "raw" else f"_{origin}"
            translated = editor_pairs.get(candidate)
            if translated and translated in available:
                code_key = translated
                route = f"editor_map{suffix}"
                break
            if candidate in available:
                code_key = candidate
                route = f"direct_name{suffix}"
                break

        editor_db_name = ""
        editor_check = "unavailable"
        if editor_inventory is not None:
            editor_check = "mismatch"
            for candidate in candidates:
                if candidate and candidate in editor_inventory:
                    editor_db_name = editor_inventory[candidate]
                    editor_check = "verified"
                    break

        # The spreadsheet's own marker for "not a real field": a repeat-block
        # header or file-level note, not a dropped/renamed parameter. A row the
        # Editor database confirms as a real column is never structural, however
        # the code-variable cell reads - cntable.lum's `treat` and `cond_cov`
        # carry no Fortran name but are genuine Editor columns.
        structural = (
            not code_key
            and clean_cell(record.get(COL_CODE_VAR)) == ""
            and editor_check != "verified"
        )

        entry = available.get(code_key, {}) if code_key else {}
        if code_key:
            claimed.add(code_key)
        result.fields.append(
            MappedField(
                editor_name=clean_cell(record.get(COL_DB_FIELD)),
                editor_type=clean_cell(record.get(COL_DATA_TYPE)),
                editor_units=clean_cell(record.get(COL_UNITS)),
                editor_description=clean_cell(record.get(COL_DESCRIPTION)),
                minimum=parse_bound(record.get(COL_MIN)),
                maximum=parse_bound(record.get(COL_MAX)),
                code_name=str(entry.get("fortran_name") or entry.get("name") or ""),
                code_type=str(entry.get("fortran_type") or ""),
                code_units=str(entry.get("units") or ""),
                code_description=str(entry.get("doc") or ""),
                status="matched" if code_key else "spreadsheet_only",
                route=route,
                editor_db_name=editor_db_name,
                editor_check=editor_check,
                structural=structural,
            )
        )

    for name, entry in available.items():
        if name in claimed:
            continue
        result.fields.append(
            MappedField(
                code_name=str(entry.get("fortran_name") or entry.get("name") or ""),
                code_type=str(entry.get("fortran_type") or ""),
                code_units=str(entry.get("units") or ""),
                code_description=str(entry.get("doc") or ""),
                status="source_only",
            )
        )
    return result


def build_all(
    spreadsheet: Path, report_path: Path, schema: dict[str, Any]
) -> list[FileMap]:
    """Build a map for every file the schema describes."""
    grouped = load_spreadsheet_rows(spreadsheet)
    report_files = json.loads(report_path.read_text(encoding="utf-8")).get("files") or {}
    editor_map = build_editor_to_official(report_files)
    editor_inventory = build_editor_inventory(report_files)
    specs: dict[str, dict[str, Any]] = {}
    for section in SCHEMA_SECTIONS:
        for swat_file, spec in (schema.get(section) or {}).items():
            specs.setdefault(swat_file, spec)

    maps: list[FileMap] = []
    for swat_file in sorted(specs):
        maps.append(
            build_file_map(
                swat_file,
                grouped.get(swat_file, []),
                specs[swat_file],
                editor_map.get(swat_file, {}),
                editor_inventory.get(swat_file),
            )
        )
    return maps


def _cell(text: str) -> str:
    """Render a value for a Markdown table cell."""
    cleaned = " ".join((text or "").split()).replace("|", "\\|")
    return cleaned or "-"


def _range_cell(item: MappedField) -> str:
    if item.minimum is not None and item.maximum is not None:
        return f"{item.minimum:g}..{item.maximum:g}"
    if item.minimum is not None:
        return f">={item.minimum:g}"
    if item.maximum is not None:
        return f"<={item.maximum:g}"
    return "-"


def render_markdown(maps: list[FileMap], version: str) -> str:
    """Render one section per file, each a spreadsheet-to-source table."""
    totals: dict[str, int] = {}
    editor_totals: dict[str, int] = {}
    structural_total = 0
    for file_map in maps:
        for status, count in file_map.counts().items():
            totals[status] = totals.get(status, 0) + count
        for item in file_map.fields:
            if item.editor_check:
                editor_totals[item.editor_check] = editor_totals.get(item.editor_check, 0) + 1
            if item.structural:
                structural_total += 1

    lines = [
        f"# Modular Database to Source Field Map: SWAT+ {version}",
        "",
        "For each input file, which modular database column corresponds to which",
        "SWAT+ source variable. The two sides use different names for the same",
        "parameter -- the spreadsheet uses SWAT+ Editor database names, the source",
        "uses Fortran names -- so the pairing is resolved through the editor schema",
        "report rather than by matching names directly.",
        "",
        "| Status | Meaning | Count |",
        "|---|---|---:|",
        f"| `matched` | The spreadsheet row and a source field are the same parameter | {totals.get('matched', 0)} |",
        f"| `spreadsheet_only` | Documented in the spreadsheet, no such field in the source | {totals.get('spreadsheet_only', 0)} |",
        f"| `source_only` | Read by the source, never documented in the spreadsheet | {totals.get('source_only', 0)} |",
        "",
        f"Of the `spreadsheet_only` rows, {structural_total} are marked `(structural)` in the table",
        "below: the row's code-variable cell is blank or `*`, the spreadsheet's own marker for a",
        "repeat-block header or file-level note rather than a single named field. These are not",
        "counted as dropped or renamed parameters. The remaining `spreadsheet_only` rows are.",
        "",
        "The spreadsheet's name for a parameter is also checked directly against the",
        "Editor's real database columns (`editor_schema` in the editor-schema report),",
        "independent of whether the source-side pairing above resolved:",
        "",
        "| Editor check | Meaning | Count |",
        "|---|---|---:|",
        f"| `verified` | This name is a real Editor database column | {editor_totals.get('verified', 0)} |",
        f"| `mismatch` | This name is not in the Editor database for this file | {editor_totals.get('mismatch', 0)} |",
        f"| `unavailable` | This file has no Editor schema data to check against | {editor_totals.get('unavailable', 0)} |",
        "",
        "## Contents",
        "",
    ]
    for file_map in maps:
        counts = file_map.counts()
        anchor = file_map.swat_file.replace(".", "").replace("_", "")
        lines.append(
            f"- [`{file_map.swat_file}`](#{anchor}) - {counts.get('matched', 0)} matched, "
            f"{counts.get('spreadsheet_only', 0)} spreadsheet-only, "
            f"{counts.get('source_only', 0)} source-only"
        )
    lines.append("")

    for file_map in maps:
        lines += [
            f"## {file_map.swat_file}",
            "",
            "| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for item in file_map.fields:
            description = item.editor_description or item.code_description
            status_cell = f"`{item.status}`"
            if item.structural:
                status_cell += " (structural)"
            lines.append(
                f"| {_cell(item.editor_name)} | {_cell(item.editor_type)} "
                f"| {_cell(item.editor_units or item.code_units)} | {_range_cell(item)} "
                f"| {_cell(item.code_name)} | {_cell(item.code_type)} "
                f"| {_cell(description)} | {status_cell} "
                f"| {_cell(item.editor_db_name)} | {f'`{item.editor_check}`' if item.editor_check else '-'} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    """CLI: write the modular-database-to-source field map."""
    parser = argparse.ArgumentParser(
        prog="swatplus-doc-field-map",
        description="Map modular database columns to SWAT+ source variables, per file.",
    )
    parser.add_argument(
        "--spreadsheet",
        default="schema_artifacts/inputs/modular_database_rev_61_0_nbs.csv",
        help="Modular database CSV export",
    )
    parser.add_argument(
        "--editor-report",
        default="schema_artifacts/reports/swatplus-62.0.0-editor-schema-report.json",
        help="Editor schema report that pairs Editor and official field names",
    )
    parser.add_argument(
        "--schema",
        default="schema_artifacts/releases/swatplus-62.0.0.json",
        help="Official input schema",
    )
    parser.add_argument(
        "--output",
        default="schema_artifacts/reports",
        help="Directory for the report",
    )
    args = parser.parse_args(argv)

    spreadsheet = Path(args.spreadsheet)
    if not spreadsheet.exists():
        parser.error(f"{spreadsheet} not found; pass --spreadsheet to point at the export.")

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    version = str(schema.get("swatplus_version") or "unknown")
    maps = build_all(spreadsheet, Path(args.editor_report), schema)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"swatplus-{version}-field-map.md").write_text(
        render_markdown(maps, version), encoding="utf-8"
    )
    (output_dir / f"swatplus-{version}-field-map.json").write_text(
        json.dumps(
            {
                "swatplus_version": version,
                "source": spreadsheet.name,
                "files": {
                    file_map.swat_file: [item.to_dict() for item in file_map.fields]
                    for file_map in maps
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    totals: dict[str, int] = {}
    editor_totals: dict[str, int] = {}
    structural_total = 0
    split_total = 0
    for file_map in maps:
        for status, count in file_map.counts().items():
            totals[status] = totals.get(status, 0) + count
        for item in file_map.fields:
            if item.editor_check:
                editor_totals[item.editor_check] = editor_totals.get(item.editor_check, 0) + 1
            if item.structural:
                structural_total += 1
            if item.route.endswith("_split"):
                split_total += 1
    print(f"files: {len(maps)}")
    for status in ("matched", "spreadsheet_only", "source_only"):
        print(f"  {status}: {totals.get(status, 0)}")
    print(f"  of which spreadsheet_only, structural (not real drift): {structural_total}")
    print(f"  of which matched, via a split compound name: {split_total}")
    print("editor_check:")
    for check in ("verified", "mismatch", "unavailable"):
        print(f"  {check}: {editor_totals.get(check, 0)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
