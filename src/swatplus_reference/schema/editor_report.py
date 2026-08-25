"""Compare official SWAT+ input schemas with SWAT+ Editor input coverage.

The model-side schema is produced by :mod:`swatplus_reference.schema.input`
from an official upstream SWAT+ release.  The Editor side is intentionally
read-only: this module inspects the cloned Editor source tree and its shipped
dataset database, then reports what can and cannot be compared safely.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .editor_effective import (
    EffectiveFileSchema,
    extract_editor_effective_schemas,
)

from .editor_compare import compare_effective_schema, official_blocks

SCHEMA_SECTIONS = (
    "files",
    "decision_tables",
    "multi_record",
    "multi_section",
    "runtime_arity",
)


EDITOR_TABLE_ALIASES = {
    "atmodep_cli": "atmo_cli",
    "cons_practice_lum": "cons_prac_lum",
    "dr_om_exc": "dr_om_del",
    "salt_hru_ini": "salt_hru_ini_cs",
}

PASSTHROUGH_EDITOR_FILES = frozenset(
    {
        "hmd.cli",
        "pcp.cli",
        "pet.cli",
        "slr.cli",
        "tmp.cli",
        "wnd.cli",
    }
)


def _passthrough_contract(station_field: str) -> list[dict[str, Any]]:
    return [
        {
            "name": "station_name_pass",
            "fields": [
                {
                    "name": station_field,
                    "field_type": "character",
                    "numeric": False,
                    "position": 0,
                    "repeated": False,
                }
            ],
        },
        {
            "name": "station_filename_pass",
            "fields": [
                {
                    "name": "filename",
                    "field_type": "character",
                    "numeric": False,
                    "position": 0,
                    "repeated": False,
                }
            ],
        },
    ]


PASSTHROUGH_OFFICIAL_CONTRACTS = {
    "hmd.cli": _passthrough_contract("hmd_n"),
    "pcp.cli": _passthrough_contract("pcp_n"),
    "pet.cli": _passthrough_contract("petm_n"),
    "slr.cli": _passthrough_contract("slr_n"),
    "tmp.cli": _passthrough_contract("tmp_n"),
    "wnd.cli": _passthrough_contract("wnd_n"),
}

EDITOR_INVENTORY_NOT_WRITTEN_FILES = frozenset(
    {
        "aqu_catunit.def",
        "aqu_reg.def",
        "ch_catunit.def",
        "ch_reg.def",
        "chan-surf.lin",
        "dr_hmet.del",
        "dr_path.del",
        "dr_pest.del",
        "dr_salt.del",
        "hmet_hru.ini",
        "ls_reg.def",
        "ls_reg.ele",
        "outlet.con",
        "rec_catunit.def",
        "rec_catunit.ele",
        "rec_reg.def",
        "recall.con",
        "res_catunit.def",
        "res_catunit.ele",
        "res_reg.def",
        "temperature.cha",
    }
)

EDITOR_SPECIAL_WRITER_UNMAPPED_FILES = frozenset({"gwflow.con", "rout_unit.def"})


def _contract_field_shape(blocks: list[dict[str, Any]]) -> list[tuple[str, tuple[tuple[str, str, bool], ...]]]:
    return [
        (
            block.get("name", ""),
            tuple(
                (
                    field.get("name", ""),
                    field.get("field_type", ""),
                    bool(field.get("repeated", False)),
                )
                for field in block.get("fields", [])
            ),
        )
        for block in blocks
    ]


def passthrough_contract_changed(file_name: str, official_schema_blocks: list[dict[str, Any]]) -> bool:
    contract = PASSTHROUGH_OFFICIAL_CONTRACTS[file_name]
    return _contract_field_shape(official_schema_blocks) != _contract_field_shape(contract)


def handled_editor_file_status(
    file_name: str,
    official_schema_blocks: list[dict[str, Any]] | None = None,
) -> tuple[str, str] | None:
    if file_name in PASSTHROUGH_EDITOR_FILES:
        if official_schema_blocks is not None and passthrough_contract_changed(file_name, official_schema_blocks):
            return (
                "passthrough_upstream_changed",
                "Editor copies this file, but the official SWAT+ layout differs from the stored passthrough contract.",
            )
        return (
            "editor_passthrough",
            "Editor copies this input file from the project/weather source directory instead of serializing it from ORM columns.",
        )
    if file_name in EDITOR_INVENTORY_NOT_WRITTEN_FILES:
        return (
            "editor_inventory_not_written",
            "Editor file_cio lists this file, but the current write workflow does not produce it as a normal SWAT+ input file.",
        )
    if file_name in EDITOR_SPECIAL_WRITER_UNMAPPED_FILES:
        return (
            "editor_special_writer_unmapped",
            "Editor writes this file through special code that is not tied to a file_cio database table schema.",
        )
    return None


@dataclass(frozen=True)
class EditorInventoryRow:
    classification: str
    order_in_class: int
    file_name: str
    database_table: str
    is_core_file: bool


def _run_git(args: list[str], cwd: Path | None = None) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def load_official_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def official_file_index(schema: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for section in SCHEMA_SECTIONS:
        for file_name in schema.get(section, {}):
            out[file_name] = section
    return out


def load_editor_inventory(editor_root: Path, sqlite_path: Path | None = None) -> list[EditorInventoryRow]:
    db_path = sqlite_path or editor_root / "release" / "build" / "swatplus_datasets.sqlite"
    if not db_path.exists():
        raise FileNotFoundError(f"Editor dataset database not found: {db_path}")

    query = """
        select c.name, f.order_in_class, f.default_file_name, f.database_table, f.is_core_file
        from file_cio f
        join file_cio_classification c on f.classification_id = c.id
        order by c.id, f.order_in_class
    """
    with sqlite3.connect(str(db_path)) as con:
        rows = con.execute(query).fetchall()
    return [
        EditorInventoryRow(
            classification=row[0],
            order_in_class=int(row[1]),
            file_name=row[2],
            database_table=row[3] or "",
            is_core_file=bool(row[4]),
        )
        for row in rows
    ]


def _import_editor_models(editor_root: Path) -> dict[str, type[Any]]:
    api_root = editor_root / "src" / "api"
    if not api_root.exists():
        raise FileNotFoundError(f"Editor API root not found: {api_root}")
    sys.path.insert(0, str(api_root.resolve()))
    try:
        from peewee import Model

        models: dict[str, type[Any]] = {}
        for package in ("database.project", "database.datasets"):
            package_path = api_root / Path(package.replace(".", "/"))
            for file_path in sorted(package_path.glob("*.py")):
                if file_path.name in {"__init__.py", "base.py", "setup.py"}:
                    continue
                module_name = f"{package}.{file_path.stem}"
                try:
                    module = importlib.import_module(module_name)
                except Exception:
                    continue
                for value in vars(module).values():
                    if not isinstance(value, type):
                        continue
                    if value is Model or not issubclass(value, Model):
                        continue
                    table_name = getattr(value._meta, "table_name", "")
                    if table_name:
                        models.setdefault(table_name, value)
        return models
    finally:
        try:
            sys.path.remove(str(api_root.resolve()))
        except ValueError:
            pass


def build_editor_table_schemas(
    editor_root: Path,
) -> tuple[dict[str, EffectiveFileSchema], dict[str, int]]:
    models = _import_editor_models(editor_root)
    return extract_editor_effective_schemas(editor_root, models)


def diff_fields(
    official_fields: list[dict[str, Any]],
    editor_fields: list[dict[str, Any]],
) -> dict[str, Any]:
    official_by_name = {f["name"]: f for f in official_fields}
    editor_by_name = {f["name"]: f for f in editor_fields}
    common = sorted(set(official_by_name) & set(editor_by_name))
    added = [
        official_by_name[name]
        for name in sorted(set(official_by_name) - set(editor_by_name))
    ]
    removed = [
        editor_by_name[name]
        for name in sorted(set(editor_by_name) - set(official_by_name))
    ]
    retyped = [
        {
            "name": name,
            "official_type": official_by_name[name]["field_type"],
            "editor_type": editor_by_name[name]["field_type"],
        }
        for name in common
        if official_by_name[name]["field_type"] != editor_by_name[name]["field_type"]
    ]
    reordered = [
        {
            "name": name,
            "official_position": official_by_name[name]["position"],
            "editor_position": editor_by_name[name]["position"],
        }
        for name in common
        if official_by_name[name]["position"] != editor_by_name[name]["position"]
    ]
    return {
        "added_upstream_fields": added,
        "removed_upstream_fields": removed,
        "retyped_fields": retyped,
        "reordered_fields": reordered,
        "official_field_count": len(official_fields),
        "editor_field_count": len(editor_fields),
    }


def build_report(
    official_schema: dict[str, Any],
    editor_root: Path,
    *,
    official_source_repo: Path | None = None,
    verify_upstream: bool = False,
    upstream_tag_commit_override: str | None = None,
) -> dict[str, Any]:
    official_index = official_file_index(official_schema)
    inventory = load_editor_inventory(editor_root)
    inventory_by_name = {row.file_name: row for row in inventory}
    table_schemas, extraction_stats = build_editor_table_schemas(editor_root)

    source_ref = official_schema.get("source_ref")
    source_repo_url = official_schema.get("source_repository")
    official_commit = None
    exact_tag = None
    upstream_tag_commit = upstream_tag_commit_override
    if official_source_repo:
        official_commit = _run_git(["rev-parse", "HEAD"], official_source_repo)
        exact_tag = _run_git(["describe", "--tags", "--exact-match", "HEAD"], official_source_repo)
    if verify_upstream and upstream_tag_commit is None and source_repo_url and source_ref:
        remote = source_repo_url
        if "/" in source_repo_url and not source_repo_url.startswith("http"):
            remote = f"https://github.com/{source_repo_url}.git"
        ref = f"refs/tags/{source_ref}"
        output = _run_git(["ls-remote", remote, ref])
        if output:
            upstream_tag_commit = output.split()[0]

    upstream_verified = bool(
        official_commit
        and upstream_tag_commit
        and official_commit == upstream_tag_commit
        and exact_tag == source_ref
    )
    if verify_upstream and not upstream_verified:
        raise ValueError(
            "Official schema source does not match the verified upstream tag and commit."
        )

    files: dict[str, Any] = {}
    all_names = sorted(set(official_index) | set(inventory_by_name))
    for file_name in all_names:
        official_section = official_index.get(file_name)
        editor_row = inventory_by_name.get(file_name)
        entry: dict[str, Any] = {
            "file": file_name,
            "official_section": official_section,
            "editor_inventory": None,
        }
        if editor_row:
            entry["editor_inventory"] = {
                "classification": editor_row.classification,
                "order_in_class": editor_row.order_in_class,
                "database_table": editor_row.database_table,
                "is_core_file": editor_row.is_core_file,
            }

        if official_section is None:
            entry["status"] = "editor_inventory_only"
            entry["reason"] = (
                "Editor file_cio inventory contains this file, but the official schema extractor does not."
            )
            files[file_name] = entry
            continue
        if editor_row is None:
            entry["status"] = "upstream_only"
            entry["reason"] = (
                "Official SWAT+ schema contains this file, but Editor file_cio inventory does not."
            )
            files[file_name] = entry
            continue

        editor_table_name = (
            "d_table_dtl"
            if editor_row.classification == "decision_table"
            else EDITOR_TABLE_ALIASES.get(editor_row.database_table, editor_row.database_table)
        )
        entry["editor_inventory"]["resolved_schema_table"] = editor_table_name

        official_entry = official_schema[official_section][file_name]
        official_schema_blocks, official_uncertainty = official_blocks(
            official_schema,
            official_section,
            file_name,
        )
        entry["official_schema"] = {
            "reader": official_entry.get("reader"),
            "read_pattern": official_entry.get("read_pattern"),
            "blocks": official_schema_blocks,
        }

        handled_status = handled_editor_file_status(file_name, official_schema_blocks)
        if handled_status is not None:
            entry["status"], entry["reason"] = handled_status
            if file_name in PASSTHROUGH_OFFICIAL_CONTRACTS:
                entry["passthrough_contract"] = {
                    "baseline": "SWAT+ 62.0.0 official schema",
                    "blocks": PASSTHROUGH_OFFICIAL_CONTRACTS[file_name],
                    "changed_from_baseline": passthrough_contract_changed(
                        file_name,
                        official_schema_blocks,
                    ),
                }
            files[file_name] = entry
            continue

        table_schema = table_schemas.get(editor_table_name)
        if table_schema is None:
            entry["status"] = "extraction_needs_review"
            entry["reason"] = "No importable Editor model was found for the file_cio database table."
            files[file_name] = entry
            continue

        comparison = compare_effective_schema(
            official_schema_blocks,
            table_schema,
            structured=official_section != "files",
            official_uncertainty=official_uncertainty,
        )
        entry["editor_schema"] = table_schema.to_dict()
        entry["field_diff"] = comparison
        entry["status"] = comparison["status"]
        entry["reason"] = comparison["reason"]
        files[file_name] = entry

    counts: dict[str, int] = {}
    for entry in files.values():
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1

    editor_commit = _run_git(["rev-parse", "HEAD"], editor_root)
    editor_branch = _run_git(["branch", "--show-current"], editor_root)
    return {
        "report_version": 2,
        "official_schema": {
            "schema_path_version": official_schema.get("swatplus_version"),
            "source_repository": source_repo_url,
            "source_ref": source_ref,
            "source_commit": official_commit,
            "source_exact_tag": exact_tag,
            "upstream_tag_commit": upstream_tag_commit,
            "upstream_verified": upstream_verified if verify_upstream else None,
            "generator": official_schema.get("generator"),
        },
        "editor": {
            # Local absolute paths are not provenance and make otherwise
            # identical reports differ across machines.
            "root": editor_root.name,
            "branch": editor_branch,
            "commit": editor_commit,
            "inventory_count": len(inventory),
            "imported_table_schema_count": len(table_schemas),
            "effective_schema_extractions": extraction_stats,
        },
        "summary": counts,
        "files": files,
    }


def dumps(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="swatplus-doc-editor-schema-report",
        description="Compare official SWAT+ input schema coverage with SWAT+ Editor inputs.",
    )
    parser.add_argument("--official-schema", required=True, help="Path to swatplus-<version>.json")
    parser.add_argument("--editor-root", required=True, help="Read-only SWAT+ Editor checkout")
    parser.add_argument(
        "--official-source-repo",
        help="Official SWAT+ checkout root used to generate the schema, for commit provenance",
    )
    parser.add_argument(
        "--verify-upstream",
        action="store_true",
        help="Verify source_ref against the upstream Git tag with git ls-remote",
    )
    parser.add_argument(
        "--upstream-tag-commit",
        help=(
            "Known git ls-remote commit for source_ref. Use when verification was "
            "performed outside this process."
        ),
    )
    parser.add_argument("--output", help="Write JSON report to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    official_schema_path = Path(args.official_schema)
    editor_root = Path(args.editor_root)
    official_source_repo = Path(args.official_source_repo) if args.official_source_repo else None
    report = build_report(
        load_official_schema(official_schema_path),
        editor_root,
        official_source_repo=official_source_repo,
        verify_upstream=args.verify_upstream,
        upstream_tag_commit_override=args.upstream_tag_commit,
    )
    text = dumps(report)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Wrote {out_path}")
    else:
        print(text, end="")
    print("Summary:")
    for status, count in sorted(report["summary"].items()):
        print(f"  {status}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
