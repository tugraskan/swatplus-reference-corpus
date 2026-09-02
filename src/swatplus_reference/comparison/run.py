"""Reproducible impact comparisons between two locked SWAT+ source profiles."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, replace
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import yaml

from .. import __version__
from ..docs.grounding import check_all
from ..docs.pages import Page, load_all
from ..docs.render import render_site
from ..docs.staleness import StatusReport, compute_status
from ..parser.facts import FactStore, enc_symbol
from ..parser.documentation import parse_documentation
from ..parser.fortran import parse_tree
from ..parser.rich import RichStore
from ..parser.schema_config import BuildConfig
from ..parser.schema_fortran import FortranScanner
from ..parser.schema_model import IOOperation, ProcedureDoc, ProjectIndex
from ..schema.input import SchemaResolver, build_schema, dumps as schema_dumps
from ..source.config import ComparisonConfig, Config
from ..source.fetch import fetch_profile, resolve_profile


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


@dataclass(frozen=True)
class ComparisonRunResult:
    report_dir: Path
    complete: bool
    one_line_summary: str


@dataclass(frozen=True)
class SchemaBuildResult:
    payload: dict[str, Any]
    project: ProjectIndex


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_text(value), encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _first_line(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except OSError as exc:
        return f"unavailable: {exc}"
    output = (result.stdout or result.stderr).strip()
    return output.splitlines()[0] if output else f"exit {result.returncode}"


def _run_logged(
    command: list[str], *, cwd: Path, log_path: Path, timeout: int = 1800
) -> dict[str, Any]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log_path.open("w", encoding="utf-8", errors="replace") as log:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=False,
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout,
            )
        return {
            "command": command,
            "exit_code": result.returncode,
            "success": result.returncode == 0,
            "log": log_path.as_posix(),
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        with log_path.open("a", encoding="utf-8") as log:
            log.write(f"\ncomparison runner stopped command: {exc}\n")
        return {
            "command": command,
            "exit_code": None,
            "success": False,
            "log": log_path.as_posix(),
            "error": str(exc),
        }


def _build_source(
    cfg: Config,
    comparison: ComparisonConfig,
    profile_name: str,
    role: str,
) -> dict[str, Any]:
    profile = cfg.source_profile(profile_name)
    checkout = profile.abs_checkout(cfg.root)
    build_dir = cfg.resolve(comparison.work_dir) / "build" / role
    build_dir.mkdir(parents=True, exist_ok=True)
    logs = cfg.resolve(comparison.work_dir) / "logs"
    build_tag = f"{comparison.name.replace('_', '-')}-comparison"
    configure = [
        "cmake",
        "--fresh",
        "-S",
        str(checkout),
        "-B",
        str(build_dir),
        "-G",
        "MinGW Makefiles",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_Fortran_COMPILER=gfortran",
        f"-DTAG={build_tag}",
    ]
    configured = _run_logged(
        configure, cwd=cfg.root, log_path=logs / f"{role}-configure.log"
    )
    built: dict[str, Any] = {
        "command": [
            "cmake",
            "--build",
            str(build_dir),
            "--config",
            "Release",
            "--parallel",
            "4",
        ],
        "exit_code": None,
        "success": False,
        "log": (logs / f"{role}-build.log").as_posix(),
        "skipped": True,
    }
    if configured["success"]:
        built = _run_logged(
            built["command"], cwd=cfg.root, log_path=logs / f"{role}-build.log"
        )
    source_dir, provenance = resolve_profile(cfg, profile_name)
    return {
        "profile": profile_name,
        "role": role,
        "source_dir": _relative(source_dir, cfg.root),
        "resolved_commit": provenance.resolved_commit,
        "configure": configured,
        "build": built,
        "success": bool(configured["success"] and built["success"]),
    }


def _symbol_diff(base: FactStore, candidate: FactStore) -> dict[str, Any]:
    base_names = set(base.symbols)
    candidate_names = set(candidate.symbols)
    added = sorted(candidate_names - base_names)
    removed = sorted(base_names - candidate_names)
    changed: list[dict[str, Any]] = []
    unchanged = 0
    for name in sorted(base_names & candidate_names):
        before = enc_symbol(base.symbols[name])
        after = enc_symbol(candidate.symbols[name])
        if before == after:
            unchanged += 1
            continue
        fields = {
            key: {"base": before.get(key), "candidate": after.get(key)}
            for key in sorted(set(before) | set(after))
            if before.get(key) != after.get(key)
        }
        changed.append({"symbol": name, "changed_fields": fields})
    return {
        "summary": {
            "base_symbols": len(base.symbols),
            "candidate_symbols": len(candidate.symbols),
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
            "unchanged": len(base_names & candidate_names) - len(changed),
            "unchanged": unchanged,
        },
        "parser": {
            "base": {
                "fallback_files": sorted(base.fallback_files),
                "parse_errors": base.parse_errors,
            },
            "candidate": {
                "fallback_files": sorted(candidate.fallback_files),
                "parse_errors": candidate.parse_errors,
            },
        },
        "added": added,
        "removed": removed,
        "changed": changed,
    }


def _unresolved_map(payload: dict[str, Any], section: str) -> dict[str, str]:
    return {
        str(item.get("file")): str(item.get("reason", ""))
        for item in payload.get(section, [])
    }


def _mapping_diff(base: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    base_names = set(base)
    candidate_names = set(candidate)
    changed = sorted(
        name
        for name in base_names & candidate_names
        if base[name] != candidate[name]
    )
    return {
        "added": sorted(candidate_names - base_names),
        "removed": sorted(base_names - candidate_names),
        "changed": changed,
        "unchanged_count": len(base_names & candidate_names) - len(changed),
    }


def _field_diff(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_fields = {
        str(field.get("name", index)): field
        for index, field in enumerate(before.get("fields", []))
    }
    after_fields = {
        str(field.get("name", index)): field
        for index, field in enumerate(after.get("fields", []))
    }
    result = _mapping_diff(before_fields, after_fields)
    result["changed_details"] = {
        name: {"base": before_fields[name], "candidate": after_fields[name]}
        for name in result["changed"]
    }
    return result


def _schema_diff(
    base: dict[str, Any],
    candidate: dict[str, Any],
    *,
    base_project: ProjectIndex | None = None,
    candidate_project: ProjectIndex | None = None,
) -> dict[str, Any]:
    sections: dict[str, Any] = {}
    for section in SCHEMA_SECTIONS:
        before = base.get(section, {})
        after = candidate.get(section, {})
        diff = _mapping_diff(before, after)
        details: dict[str, Any] = {}
        for name in diff["changed"]:
            item: dict[str, Any] = {
                "changed_keys": sorted(
                    key
                    for key in set(before[name]) | set(after[name])
                    if before[name].get(key) != after[name].get(key)
                )
            }
            if isinstance(before[name], dict) and isinstance(after[name], dict):
                if "fields" in before[name] or "fields" in after[name]:
                    item["fields"] = _field_diff(before[name], after[name])
            details[name] = item
        diff["changed_details"] = details
        sections[section] = diff

    unresolved: dict[str, Any] = {}
    new_unresolved_total = 0
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
        unresolved[section] = {
            "base_count": len(before),
            "candidate_count": len(after),
            "new": new,
            "resolved": resolved,
            "changed_reasons": changed,
            "candidate": after,
        }

    changed_entries = sum(
        len(value["added"]) + len(value["removed"]) + len(value["changed"])
        for value in sections.values()
    )
    result = {
        "summary": {
            "base_flat_files": len(base.get("files", {})),
            "candidate_flat_files": len(candidate.get("files", {})),
            "changed_entries": changed_entries,
            "new_unresolved": new_unresolved_total,
        },
        "sections": sections,
        "unresolved_sections": unresolved,
    }
    if base_project is not None and candidate_project is not None:
        result["source_read_evidence"] = _source_read_evidence(
            result, base, candidate, base_project, candidate_project
        )
    return result


def _file_token_key(value: str | None) -> str:
    if not value:
        return ""
    stripped = str(value).strip().strip("\"'")
    stripped = stripped.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return re.sub(r"[^a-z0-9]+", "", stripped)


def _file_tokens(value: str | None) -> set[str]:
    if not value:
        return set()
    return {
        token
        for token in re.split(r"[^a-z0-9]+", str(value).strip().strip("\"'").lower())
        if token and token not in {"in", "file", "read"}
    }


def _read_role(op: IOOperation) -> str:
    names = [_file_token_key(field) for field in op.fields]
    if len(names) == 1:
        if names[0] in {"titldum", "title", "title1", "title2"}:
            return "title"
        if names[0] == "header":
            return "header"
        if names[0] in {"imax", "mrec", "nbyr", "num"} or names[0].endswith("tot"):
            return "count"
    return "data"


def _io_blocks(proc: ProcedureDoc) -> list[tuple[IOOperation | None, list[IOOperation]]]:
    blocks: list[tuple[IOOperation | None, list[IOOperation]]] = []
    current_by_unit: dict[str, int] = {}
    current_index: int | None = None
    orphan_index: int | None = None
    for op in proc.io:
        if op.kind == "open":
            blocks.append((op, []))
            current_index = len(blocks) - 1
            if op.unit:
                current_by_unit[op.unit.lower()] = current_index
        elif op.kind == "read":
            if op.unit and "(" in op.unit:
                if current_index is not None:
                    blocks[current_index][1].append(op)
                continue
            index = current_by_unit.get(op.unit.lower()) if op.unit else None
            if index is None:
                if orphan_index is None:
                    blocks.append((None, []))
                    orphan_index = len(blocks) - 1
                index = orphan_index
            blocks[index][1].append(op)
    return blocks


def _block_file_names(
    open_op: IOOperation | None,
    reads: list[IOOperation],
    *,
    resolver: SchemaResolver | None = None,
    proc: ProcedureDoc | None = None,
) -> list[str]:
    names: list[str] = []
    for op in ([open_op] if open_op is not None else []) + reads:
        for value in (op.file_resolved, op.file_expr):
            if value and value not in names:
                names.append(value)
            if not value or resolver is None:
                continue
            resolved = resolver.resolve_filename(value)
            if resolved and resolved not in names:
                names.append(resolved)
            if proc is not None:
                for filename in resolver.resolve_dummy_arg_filenames(proc, value):
                    if filename not in names:
                        names.append(filename)
    return names


def _resolved_block_filenames(
    resolver: SchemaResolver,
    proc: ProcedureDoc,
    open_op: IOOperation | None,
    reads: list[IOOperation],
) -> tuple[list[str], list[str]]:
    """Return concrete defaults and unresolved source expressions for an input block."""
    resolved: list[str] = []
    expressions: list[str] = []
    for op in ([open_op] if open_op is not None else []) + reads:
        for value in (op.file_expr, op.file_resolved):
            if not value:
                continue
            text = value.strip().strip("`'\"")
            if text and text not in expressions:
                expressions.append(text)
            direct = resolver.resolve_filename(value)
            if direct and direct not in resolved:
                resolved.append(direct)
            for filename in resolver.resolve_dummy_arg_filenames(proc, value):
                if filename not in resolved:
                    resolved.append(filename)
    return resolved, expressions


def _read_payload(op: IOOperation) -> dict[str, Any]:
    return {
        "line": op.location.line,
        "role": _read_role(op),
        "fields": op.fields,
        "condition": op.condition,
        "raw": op.raw,
    }


def _block_payload(
    proc: ProcedureDoc,
    open_op: IOOperation | None,
    reads: list[IOOperation],
    *,
    match: str,
    resolver: SchemaResolver | None = None,
) -> dict[str, Any]:
    resolved_defaults: list[str] = []
    source_expressions: list[str] = []
    if resolver is not None:
        resolved_defaults, source_expressions = _resolved_block_filenames(
            resolver, proc, open_op, reads
        )
    return {
        "procedure": proc.name,
        "reader": proc.location.path,
        "match": match,
        "resolved_default_filenames": resolved_defaults,
        "source_expressions": source_expressions,
        "open": None
        if open_op is None
        else {
            "line": open_op.location.line,
            "file_expr": open_op.file_expr,
            "file_resolved": open_op.file_resolved,
            "condition": open_op.condition,
            "raw": open_op.raw,
        },
        "reads": [_read_payload(op) for op in reads],
    }


def _exact_read_evidence(
    project: ProjectIndex,
    filename: str,
    *,
    resolver: SchemaResolver | None = None,
) -> dict[str, Any]:
    resolver = resolver or SchemaResolver(project)
    target = _file_token_key(filename)
    blocks: list[dict[str, Any]] = []
    for proc in project.procedures:
        for open_op, reads in _io_blocks(proc):
            names = _block_file_names(open_op, reads, resolver=resolver, proc=proc)
            if any(_file_token_key(name) == target for name in names):
                blocks.append(
                    _block_payload(
                        proc,
                        open_op,
                        reads,
                        match="exact_filename",
                        resolver=resolver,
                    )
                )
    return {"status": "found" if blocks else "not_found", "blocks": blocks}


def _related_read_evidence(
    project: ProjectIndex,
    filename: str,
    *,
    resolver: SchemaResolver | None = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    resolver = resolver or SchemaResolver(project)
    target_key = _file_token_key(filename)
    target_stem = Path(filename).stem.lower()
    target_tokens = _file_tokens(Path(filename).stem)
    scored: list[tuple[float, int, dict[str, Any]]] = []
    order = 0
    for proc in project.procedures:
        proc_key = _file_token_key(proc.name)
        proc_tokens = _file_tokens(proc.name)
        proc_reasons: list[str] = []
        proc_score = 0.0
        if target_stem and target_stem in proc.name.lower():
            proc_reasons.append("same reader procedure stem")
            proc_score += 2.0
        proc_overlap = len(target_tokens & proc_tokens)
        if proc_overlap:
            proc_score += proc_overlap * 0.5
        if proc_overlap >= max(1, len(target_tokens)):
            proc_reasons.append("reader procedure tokens match target")
        for open_op, reads in _io_blocks(proc):
            names = _block_file_names(open_op, reads, resolver=resolver, proc=proc)
            if any(_file_token_key(name) == target_key for name in names):
                continue
            candidates = names or [proc.name]
            score = proc_score
            reasons: list[str] = list(proc_reasons)
            for candidate in candidates:
                candidate_key = _file_token_key(candidate)
                candidate_tokens = _file_tokens(candidate)
                ratio = SequenceMatcher(None, target_key, candidate_key).ratio()
                overlap = len(target_tokens & candidate_tokens)
                if ratio >= 0.62:
                    reasons.append("similar opened filename/expression")
                if overlap:
                    reasons.append("shared filename tokens")
                score = max(score, proc_score + ratio + overlap * 0.2)
            if reasons:
                payload = _block_payload(
                    proc,
                    open_op,
                    reads,
                    match=", ".join(sorted(set(reasons))),
                    resolver=resolver,
                )
                scored.append((score, order, payload))
                order += 1
    scored.sort(key=lambda item: (-item[0], item[1]))
    if not scored:
        return []
    best_score = scored[0][0]
    threshold = max(0.8, best_score - 0.75)
    return [
        payload
        for score, _order, payload in scored
        if score >= threshold
    ][:limit]


def _schema_presence(payload: dict[str, Any], filename: str) -> dict[str, list[str]]:
    resolved = [
        section
        for section in SCHEMA_SECTIONS
        if filename in (payload.get(section) or {})
    ]
    unresolved = [
        section
        for section in UNRESOLVED_SECTIONS
        if filename in _unresolved_map(payload, section)
    ]
    return {"resolved_sections": resolved, "unresolved_sections": unresolved}


def _review_target_files(schema_diff: dict[str, Any]) -> dict[str, list[str]]:
    files: dict[str, set[str]] = {}
    for section_name, section in schema_diff["sections"].items():
        for kind in ("added", "removed"):
            for filename in section[kind]:
                files.setdefault(filename, set()).add(f"{section_name}.{kind}")
        if section_name != "files":
            for filename in section["changed"]:
                files.setdefault(filename, set()).add(f"{section_name}.changed")
    for section in schema_diff["unresolved_sections"].values():
        for filename in section["new"]:
            files.setdefault(filename, set()).add("newly_unresolved")
    return {filename: sorted(statuses) for filename, statuses in sorted(files.items())}


def _source_read_evidence(
    schema_diff: dict[str, Any],
    base_schema: dict[str, Any],
    candidate_schema: dict[str, Any],
    base_project: ProjectIndex,
    candidate_project: ProjectIndex,
) -> dict[str, Any]:
    base_resolver = SchemaResolver(base_project)
    candidate_resolver = SchemaResolver(candidate_project)
    evidence: dict[str, Any] = {}
    for filename, statuses in _review_target_files(schema_diff).items():
        base = _exact_read_evidence(
            base_project, filename, resolver=base_resolver
        )
        candidate = _exact_read_evidence(
            candidate_project, filename, resolver=candidate_resolver
        )
        evidence[filename] = {
            "schema_diff_status": statuses,
            "review_needed": candidate["status"] != "found"
            or any(status.endswith(".removed") for status in statuses)
            or "newly_unresolved" in statuses,
            "base_schema_presence": _schema_presence(base_schema, filename),
            "candidate_schema_presence": _schema_presence(candidate_schema, filename),
            "base": base,
            "base_related": []
            if base["status"] == "found"
            else _related_read_evidence(
                base_project, filename, resolver=base_resolver
            ),
            "candidate": candidate,
            "candidate_related": []
            if candidate["status"] == "found"
            else _related_read_evidence(
                candidate_project, filename, resolver=candidate_resolver
            ),
        }
    return evidence


def _contract_block_signature(block: dict[str, Any]) -> dict[str, Any]:
    """Stable read contract: exclude source lines and raw formatting noise."""
    return {
        "procedure": block["procedure"],
        "open_condition": (block.get("open") or {}).get("condition"),
        "reads": [
            {
                "role": read["role"],
                "fields": read.get("fields") or [],
                "condition": read.get("condition"),
            }
            for read in block.get("reads") or []
        ],
    }


def _input_file_inventory(
    project: ProjectIndex, schema: dict[str, Any]
) -> dict[str, Any]:
    """Inventory source-opened input defaults and their actual read layouts."""
    resolver = SchemaResolver(project)
    files: dict[str, dict[str, Any]] = {}
    unresolved_blocks: list[dict[str, Any]] = []

    for proc in project.procedures:
        for open_op, reads in _io_blocks(proc):
            # A source input contract needs both a named open target and at least
            # one read. Orphan reads and write-only opens are outside this report.
            if open_op is None or not reads:
                continue
            filenames, expressions = _resolved_block_filenames(
                resolver, proc, open_op, reads
            )
            block = _block_payload(
                proc,
                open_op,
                reads,
                match="source_input",
                resolver=resolver,
            )
            if not filenames:
                unresolved_blocks.append(
                    {
                        "review_needed": True,
                        "reason": "opened input filename could not be resolved",
                        "source_expressions": expressions,
                        "block": block,
                    }
                )
                continue
            for filename in filenames:
                entry = files.setdefault(
                    filename,
                    {
                        "filename": filename,
                        "source_expressions": [],
                        "blocks": [],
                    },
                )
                for expression in expressions:
                    if expression not in entry["source_expressions"]:
                        entry["source_expressions"].append(expression)
                entry["blocks"].append(block)

    for filename, entry in files.items():
        presence = _schema_presence(schema, filename)
        if presence["resolved_sections"]:
            certification = "certified"
        elif presence["unresolved_sections"]:
            certification = "schema_unresolved_but_readable"
        else:
            certification = "readable_needs_schema_review"
        entry["schema_presence"] = presence
        entry["certification"] = certification
        entry["review_needed"] = certification != "certified"
        entry["contract"] = sorted(
            (_contract_block_signature(block) for block in entry["blocks"]),
            key=lambda item: _json_text(item),
        )

    return {
        "files": dict(sorted(files.items())),
        "unresolved_open_blocks": sorted(
            unresolved_blocks,
            key=lambda item: (
                item["block"]["reader"],
                (item["block"].get("open") or {}).get("line") or 0,
            ),
        ),
    }


def _flatten_contract_fields(entry: dict[str, Any]) -> list[str]:
    return [
        field
        for block in entry.get("contract") or []
        for read in block.get("reads") or []
        for field in read.get("fields") or []
    ]


def _possible_input_replacements(
    removed: dict[str, dict[str, Any]], added: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flag source-supported replacement candidates without claiming a rename."""
    candidates: list[dict[str, Any]] = []
    for old_name, old_entry in removed.items():
        old_procs = {block["procedure"] for block in old_entry.get("blocks") or []}
        old_fields = _flatten_contract_fields(old_entry)
        for new_name, new_entry in added.items():
            new_procs = {block["procedure"] for block in new_entry.get("blocks") or []}
            shared_procs = sorted(old_procs & new_procs)
            if not shared_procs:
                continue
            field_similarity = SequenceMatcher(
                None, old_fields, _flatten_contract_fields(new_entry)
            ).ratio()
            score = 2.0 + field_similarity
            reasons = [f"same reader procedure: {', '.join(shared_procs)}"]
            if Path(old_name).suffix.lower() == Path(new_name).suffix.lower():
                score += 0.25
                reasons.append("same file extension")
            if field_similarity >= 0.5:
                reasons.append("similar read-field order")
            candidates.append(
                {
                    "removed": old_name,
                    "added": new_name,
                    "classification": "possible_rename_or_replacement",
                    "review_needed": True,
                    "reasons": reasons,
                    "score": round(score, 3),
                }
            )
    return sorted(candidates, key=lambda item: (item["removed"], item["added"]))


def _contract_change_details(
    base_entry: dict[str, Any], candidate_entry: dict[str, Any]
) -> dict[str, Any]:
    base_contract = base_entry.get("contract") or []
    candidate_contract = candidate_entry.get("contract") or []
    base_fields = _flatten_contract_fields(base_entry)
    candidate_fields = _flatten_contract_fields(candidate_entry)
    field_edits: list[dict[str, Any]] = []
    matcher = SequenceMatcher(None, base_fields, candidate_fields, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        field_edits.append(
            {
                "operation": tag,
                "base_index": i1,
                "candidate_index": j1,
                "removed": base_fields[i1:i2],
                "added": candidate_fields[j1:j2],
            }
        )
    return {
        "reader_procedures_changed": sorted(
            {block["procedure"] for block in base_contract}
        )
        != sorted({block["procedure"] for block in candidate_contract}),
        "block_count_changed": len(base_contract) != len(candidate_contract),
        "conditions_changed": [
            (block.get("open_condition"), [read.get("condition") for read in block["reads"]])
            for block in base_contract
        ]
        != [
            (block.get("open_condition"), [read.get("condition") for read in block["reads"]])
            for block in candidate_contract
        ],
        "base_read_fields": base_fields,
        "candidate_read_fields": candidate_fields,
        "field_edits": field_edits,
    }


def _unresolved_block_key(item: dict[str, Any]) -> str:
    block = item["block"]
    return _json_text(
        {
            "procedure": block["procedure"],
            "reader": block["reader"],
            "source_expressions": item.get("source_expressions") or [],
        }
    )


def _input_contract_diff(
    base_project: ProjectIndex,
    base_schema: dict[str, Any],
    candidate_project: ProjectIndex,
    candidate_schema: dict[str, Any],
) -> dict[str, Any]:
    base_inventory = _input_file_inventory(base_project, base_schema)
    candidate_inventory = _input_file_inventory(candidate_project, candidate_schema)
    base_files = base_inventory["files"]
    candidate_files = candidate_inventory["files"]
    base_names = set(base_files)
    candidate_names = set(candidate_files)

    added = {
        name: candidate_files[name] for name in sorted(candidate_names - base_names)
    }
    removed = {name: base_files[name] for name in sorted(base_names - candidate_names)}
    changed: dict[str, Any] = {}
    for name in sorted(base_names & candidate_names):
        before = base_files[name]
        after = candidate_files[name]
        if before["contract"] != after["contract"]:
            changed[name] = {
                "filename": name,
                "review_needed": True,
                "changes": _contract_change_details(before, after),
                "base": before,
                "candidate": after,
            }

    base_unresolved = {
        _unresolved_block_key(item): item
        for item in base_inventory["unresolved_open_blocks"]
    }
    candidate_unresolved = {
        _unresolved_block_key(item): item
        for item in candidate_inventory["unresolved_open_blocks"]
    }
    introduced_unresolved = [
        candidate_unresolved[key]
        for key in sorted(candidate_unresolved.keys() - base_unresolved.keys())
    ]
    resolved_unresolved = [
        base_unresolved[key]
        for key in sorted(base_unresolved.keys() - candidate_unresolved.keys())
    ]

    return {
        "summary": {
            "base_input_files": len(base_files),
            "candidate_input_files": len(candidate_files),
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
            "possible_renames_or_replacements": len(
                _possible_input_replacements(removed, added)
            ),
            "base_unresolved_open_blocks": len(
                base_inventory["unresolved_open_blocks"]
            ),
            "candidate_unresolved_open_blocks": len(
                candidate_inventory["unresolved_open_blocks"]
            ),
            "new_unresolved_open_blocks": len(introduced_unresolved),
            "resolved_unresolved_open_blocks": len(resolved_unresolved),
        },
        "added": added,
        "removed": removed,
        "changed": changed,
        "possible_renames_or_replacements": _possible_input_replacements(
            removed, added
        ),
        "unresolved_open_blocks": {
            "introduced": introduced_unresolved,
            "resolved": resolved_unresolved,
        },
    }


def _field_list(fields: list[str]) -> str:
    if not fields:
        return "_no fields captured_"
    return ", ".join(f"`{field}`" for field in fields)


def _read_block_markdown(block: dict[str, Any]) -> list[str]:
    open_info = block.get("open") or {}
    lines = [
        f"- Procedure: `{block['procedure']}`",
        f"- Reader: `{block['reader']}`",
        f"- Match: {block['match']}",
    ]
    defaults = block.get("resolved_default_filenames") or []
    expressions = block.get("source_expressions") or []
    if defaults:
        lines.append(
            "- Resolved default filename(s): "
            + ", ".join(f"`{name}`" for name in defaults)
        )
    if expressions:
        lines.append(
            "- Source filename expression(s): "
            + ", ".join(f"`{expr}`" for expr in expressions)
        )
    if open_info:
        lines.append(
            "- Open: "
            f"line {open_info['line']}, "
            f"file expression `{open_info.get('file_expr')}`, "
            f"parser value `{open_info.get('file_resolved')}`, "
            f"condition `{open_info.get('condition')}`"
        )
    reads = block.get("reads") or []
    if not reads:
        lines.append("- Reads: _none captured_")
        return lines
    lines.extend(
        [
            "",
            "| Line | Role | Condition | Fields read |",
            "| --- | --- | --- | --- |",
        ]
    )
    for read in reads:
        lines.append(
            f"| {read['line']} | {read['role']} | `{read.get('condition')}` | "
            f"{_field_list(read.get('fields') or [])} |"
        )
    return lines


def _schema_read_evidence_markdown(schema_diff: dict[str, Any]) -> str:
    evidence = schema_diff.get("source_read_evidence") or {}
    lines = [
        "# Source Read Evidence for Schema Review",
        "",
        "This report is generated when a comparison has schema entries that changed, disappeared from resolved schemas, or became newly unresolved. It does not certify a final schema. It shows the Fortran read evidence that a human or extractor update should review.",
    ]
    if not evidence:
        lines.extend(["", "No schema read-review evidence was generated."])
        return "\n".join(lines) + "\n"

    for filename in sorted(evidence):
        item = evidence[filename]
        lines.extend(
            [
                "",
                f"## `{filename}`",
                "",
                f"- Schema diff status: `{item.get('schema_diff_status')}`",
                f"- Review needed: {'yes' if item.get('review_needed') else 'no'}",
                f"- Base schema presence: `{item.get('base_schema_presence')}`",
                f"- Candidate schema presence: `{item.get('candidate_schema_presence')}`",
                "",
                "### Base exact read evidence",
                "",
            ]
        )
        base = item.get("base") or {}
        if base.get("status") != "found":
            lines.append("_No exact base opened/read evidence found._")
        else:
            for block in base.get("blocks") or []:
                lines.extend(_read_block_markdown(block))
                lines.append("")

        base_related = item.get("base_related") or []
        if base_related:
            lines.extend(["", "### Base related read evidence", ""])
            for block in base_related:
                lines.extend(_read_block_markdown(block))
                lines.append("")

        lines.extend(["", "### Candidate exact read evidence", ""])
        candidate = item.get("candidate") or {}
        if candidate.get("status") != "found":
            lines.append("_No exact candidate opened/read evidence found._")
        else:
            for block in candidate.get("blocks") or []:
                lines.extend(_read_block_markdown(block))
                lines.append("")

        related = item.get("candidate_related") or []
        if related:
            lines.extend(["", "### Candidate related read evidence", ""])
            for block in related:
                lines.extend(_read_block_markdown(block))
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _contract_entry_markdown(entry: dict[str, Any]) -> list[str]:
    lines = [
        f"- Schema status: `{entry.get('certification')}`",
        f"- Review needed: {'yes' if entry.get('review_needed') else 'no'}",
        "- Source expression(s): "
        + (
            ", ".join(
                f"`{expr}`" for expr in entry.get("source_expressions") or []
            )
            or "_none captured_"
        ),
    ]
    for block in entry.get("blocks") or []:
        lines.extend(["", *_read_block_markdown(block), ""])
    return lines


def _input_contract_changes_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# SWAT+ Input Contract Changes",
        "",
        "This is the primary source-level input change report. Filenames are resolved from the same defaults used by the schema extractor. A resolved default can still be overridden by runtime configuration.",
        "",
        "## Summary",
        "",
        f"- Added input defaults: **{summary['added']}**",
        f"- Removed input defaults: **{summary['removed']}**",
        f"- Changed read contracts: **{summary['changed']}**",
        "- Possible renames or replacements: "
        f"**{summary['possible_renames_or_replacements']}**",
        "- Candidate open/read blocks with unresolved filenames: "
        f"**{summary['candidate_unresolved_open_blocks']}**",
        "- Newly unresolved filename expressions in the candidate: "
        f"**{summary['new_unresolved_open_blocks']}**",
    ]

    for heading, key in (
        ("Added inputs", "added"),
        ("Removed inputs", "removed"),
    ):
        lines.extend(["", f"## {heading}", ""])
        entries = result[key]
        if not entries:
            lines.append("_None._")
        for filename, entry in entries.items():
            lines.extend([f"### `{filename}`", "", *_contract_entry_markdown(entry)])

    lines.extend(["", "## Changed input read contracts", ""])
    if not result["changed"]:
        lines.append("_None._")
    for filename, item in result["changed"].items():
        details = item["changes"]
        lines.extend(
            [
                f"### `{filename}`",
                "",
                "- Review needed: yes",
                "- Reader procedures changed: "
                f"{'yes' if details['reader_procedures_changed'] else 'no'}",
                "- Read-block count changed: "
                f"{'yes' if details['block_count_changed'] else 'no'}",
                "- Read conditions changed: "
                f"{'yes' if details['conditions_changed'] else 'no'}",
                "- Base flattened read order: "
                + _field_list(details["base_read_fields"]),
                "- Candidate flattened read order: "
                + _field_list(details["candidate_read_fields"]),
                "",
                "#### Read-order edits",
                "",
            ]
        )
        if not details["field_edits"]:
            lines.append("_No field-order edits; the contract changed in structure or conditions._")
        for edit in details["field_edits"]:
            lines.append(
                f"- `{edit['operation']}` at base index {edit['base_index']} / "
                f"candidate index {edit['candidate_index']}: removed "
                f"{_field_list(edit['removed'])}; added {_field_list(edit['added'])}"
            )
        lines.extend(
            [
                "",
                "#### Base read structure",
                "",
                *_contract_entry_markdown(item["base"]),
                "",
                "#### Candidate read structure",
                "",
                *_contract_entry_markdown(item["candidate"]),
            ]
        )

    lines.extend(["", "## Possible renames or replacements", ""])
    replacements = result["possible_renames_or_replacements"]
    if not replacements:
        lines.append("_None._")
    for item in replacements:
        lines.append(
            f"- `{item['removed']}` -> `{item['added']}`: "
            + "; ".join(item["reasons"])
            + ". **Human review required; this is not asserted as a rename.**"
        )

    lines.extend(["", "## Unresolved opened input filenames", ""])
    introduced_unresolved = result["unresolved_open_blocks"]["introduced"]
    lines.append(
        f"The candidate contains {summary['candidate_unresolved_open_blocks']} unresolved runtime filename expression(s); "
        f"{len(introduced_unresolved)} were introduced by this comparison. Only newly introduced expressions are expanded below."
    )
    if not introduced_unresolved:
        lines.extend(["", "_No newly unresolved input filename expressions._"])
    for item in introduced_unresolved:
        block = item["block"]
        lines.extend(
            [
                f"### `{block['procedure']}` at `{block['reader']}`",
                "",
                f"- Reason: {item['reason']}",
                "- Expression(s): "
                + ", ".join(
                    f"`{expr}`" for expr in item.get("source_expressions") or []
                ),
                *_read_block_markdown(block),
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def _page_key(page: Page, root: Path) -> str:
    return _relative(page.path, root)


def _status_payload(report: StatusReport, root: Path) -> dict[str, Any]:
    def pages(items: list[Page]) -> list[str]:
        return sorted(_page_key(page, root) for page in items)

    return {
        "counts": {
            "filled": len(report.filled),
            "stale": len(report.stale),
            "affected": len(report.affected),
            "todo": len(report.todo),
            "orphaned": len(report.orphaned),
            "missing": len(report.missing),
        },
        "filled": pages(report.filled),
        "stale": pages(report.stale),
        "affected": pages(report.affected),
        "todo": pages(report.todo),
        "orphaned": pages(report.orphaned),
        "missing": sorted(report.missing),
        "affected_by": dict(sorted(report.affected_by.items())),
    }


def _page_status_diff(
    base_report: StatusReport, candidate_report: StatusReport, root: Path
) -> dict[str, Any]:
    base = _status_payload(base_report, root)
    candidate = _status_payload(candidate_report, root)
    return {
        "base": base,
        "candidate": candidate,
        "pr_delta": {
            "newly_stale": sorted(set(candidate["stale"]) - set(base["stale"])),
            "no_longer_stale": sorted(set(base["stale"]) - set(candidate["stale"])),
            "newly_affected": sorted(
                set(candidate["affected"]) - set(base["affected"])
            ),
            "newly_orphaned": sorted(
                set(candidate["orphaned"]) - set(base["orphaned"])
            ),
            "new_missing_pages": sorted(
                set(candidate["missing"]) - set(base["missing"])
            ),
        },
    }


def _finding_key(finding: Any) -> tuple[str, str, str, str]:
    return (finding.page, finding.level, finding.code, finding.message)


def _grounding_payload(base_findings: list[Any], candidate_findings: list[Any]) -> dict[str, Any]:
    base_map = {_finding_key(finding): finding for finding in base_findings}
    candidate_map = {_finding_key(finding): finding for finding in candidate_findings}
    introduced = [asdict(candidate_map[key]) for key in sorted(candidate_map.keys() - base_map.keys())]
    resolved = [asdict(base_map[key]) for key in sorted(base_map.keys() - candidate_map.keys())]

    def counts(findings: list[Any]) -> dict[str, int]:
        return {
            "total": len(findings),
            "errors": sum(f.level == "error" for f in findings),
            "warnings": sum(f.level == "warning" for f in findings),
        }

    return {
        "base_counts": counts(base_findings),
        "candidate_counts": counts(candidate_findings),
        "introduced_counts": counts([candidate_map[key] for key in candidate_map.keys() - base_map.keys()]),
        "resolved_counts": counts([base_map[key] for key in base_map.keys() - candidate_map.keys()]),
        "introduced": introduced,
        "resolved": resolved,
        "candidate_findings": [asdict(finding) for finding in candidate_findings],
    }


def _build_preview(
    cfg: Config,
    comparison: ComparisonConfig,
    candidate_store: FactStore,
    candidate_rich: RichStore,
    candidate_commit: str,
) -> dict[str, Any]:
    work_dir = cfg.resolve(comparison.work_dir)
    preview_docs = work_dir / "preview" / "docs"
    preview_site = work_dir / "preview" / "site"
    profile = cfg.source_profile(comparison.candidate_source)
    preview_cfg = replace(
        cfg,
        source_dir=profile.checkout / profile.subdir,
        source_ref=candidate_commit,
        source_repo_url=profile.repository,
        source_link_base=profile.source_link_base(candidate_commit),
        version_label=profile.version_label,
        facts_path=work_dir / "facts" / "candidate.json",
        render_dir=preview_docs,
    )
    render_site(preview_cfg, candidate_store, candidate_rich)

    mkdocs_path = cfg.root / "mkdocs.yml"
    mkdocs_data = yaml.safe_load(mkdocs_path.read_text(encoding="utf-8")) or {}
    mkdocs_data["site_name"] = f"{comparison.title or comparison.name} preview"
    mkdocs_data["site_description"] = (
        f"Isolated preview for candidate {candidate_commit}"
    )
    mkdocs_data["docs_dir"] = str(preview_docs.resolve())
    mkdocs_data["site_dir"] = str(preview_site.resolve())
    preview_config = work_dir / "preview" / "mkdocs.yml"
    preview_config.parent.mkdir(parents=True, exist_ok=True)
    preview_config.write_text(
        yaml.safe_dump(mkdocs_data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    command = [
        sys.executable,
        "-m",
        "mkdocs",
        "build",
        "--strict",
        "--config-file",
        str(preview_config),
    ]
    result = _run_logged(
        command,
        cwd=cfg.root,
        log_path=work_dir / "logs" / "preview-mkdocs.log",
    )
    result.update(
        {
            "rendered_docs": _relative(preview_docs, cfg.root),
            "site": _relative(preview_site, cfg.root),
            "config": _relative(preview_config, cfg.root),
        }
    )
    return result


def _build_schema_payload(source_dir: Path, source_ref: str, label: str) -> SchemaBuildResult:
    project = FortranScanner(BuildConfig(source_dir=source_dir)).scan()
    return SchemaBuildResult(
        payload=build_schema(
            project,
            swatplus_version=label,
            source_ref=source_ref,
            source_repository="swat-model/swatplus",
            generator=f"swatplus-reference-corpus {__version__}",
            generated_utc=None,
        ),
        project=project,
    )


def _source_build_markdown(data: dict[str, Any]) -> str:
    skipped = all(data[role].get("skipped") for role in ("base", "candidate"))
    description = (
        "Source compilation was skipped for this deterministic report reproduction. "
        "Run the comparison without `--skip-source-build` for the manual release gate."
        if skipped
        else "Both revisions were configured with the same Release settings, MinGW Makefiles generator, and GNU Fortran compiler."
    )
    lines = [
        "# Source build results",
        "",
        description,
        "",
        f"- CMake: `{data['toolchain']['cmake']}`",
        f"- Fortran compiler: `{data['toolchain']['fortran']}`",
        f"- Generator: `{data['toolchain']['generator']}`",
        f"- Build type: `{data['toolchain']['build_type']}`",
        f"- Shared tag override: `{data['toolchain']['tag']}`",
        "",
        "| Revision | Commit | Configure | Compile |",
        "| --- | --- | --- | --- |",
    ]
    for role in ("base", "candidate"):
        build = data[role]
        if build.get("skipped"):
            configure = compile_result = "skipped"
        else:
            configure = "pass" if build["configure"]["success"] else "FAIL"
            compile_result = "pass" if build["build"]["success"] else "FAIL"
        lines.append(
            f"| {role} | `{build['resolved_commit']}` | {configure} | {compile_result} |"
        )
    lines.extend(
        [
            "",
            f"Full configure and compiler logs are retained in the ignored comparison workspace under `{data['logs_dir']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def _summary_markdown(summary: dict[str, Any]) -> str:
    checks = summary["checks"]
    symbols = summary["symbols"]
    schemas = summary["schemas"]
    inputs = summary["inputs"]
    pages = summary["pages"]
    grounding = summary["grounding"]
    readiness = (
        "ready for corpus adoption"
        if summary["ready_for_adoption"]
        else "requires corpus and schema updates before adoption"
    )
    source = summary["source"]
    title = summary["title"]
    link = f"[{title}]({summary['url']})" if summary.get("url") else title

    def check_label(value: bool | None) -> str:
        if value is None:
            return "skipped"
        return "pass" if value else "FAIL"

    lines = [
        f"# {title} impact report",
        "",
        f"Comparison: {link}",
        "",
        f"- Exact base: `{source['base_commit']}` (`{source['base_ref']}`)",
        f"- Exact candidate: `{source['candidate_commit']}` (`{source['candidate_ref']}`)",
        "- Existing reviewed corpus pages were read only; no AI filling was run.",
        "",
        "## Result",
        "",
        f"Overall: **{readiness}**.",
        "",
        f"- Same-toolchain compile: base={check_label(checks['base_compile'])}, candidate={check_label(checks['candidate_compile'])}",
        f"- Candidate facts deterministic: {check_label(checks['facts_deterministic'])}",
        f"- Candidate schema deterministic: {check_label(checks['schema_deterministic'])}",
        f"- Candidate input contracts repeat with zero changes: {check_label(checks['input_contract_deterministic'])}",
        f"- Strict isolated preview: {check_label(checks['preview'])}",
        f"- Parser fallback coverage: base={summary['parser']['base_fallback_files']} files, candidate={summary['parser']['candidate_fallback_files']} files",
        f"- Symbols: {symbols['added']} added, {symbols['removed']} removed, {symbols['changed']} changed",
        f"- Schema entries: {schemas['changed_entries']} added, removed, or changed; {schemas['new_unresolved']} newly unresolved",
        f"- Input contracts: {inputs['added']} added, {inputs['removed']} removed, {inputs['changed']} changed; {inputs['new_unresolved_open_blocks']} newly unresolved filename expressions ({inputs['candidate_unresolved_open_blocks']} candidate total)",
        f"- Corpus impact attributable to the PR: {pages['newly_stale']} newly stale, {pages['newly_affected']} newly affected, {pages['newly_orphaned']} newly orphaned, {pages['new_missing_pages']} new pages needed",
        f"- Grounding attributable to the PR: {grounding['introduced_errors']} new errors, {grounding['introduced_warnings']} new warnings",
        "",
        "## Human review focus",
        "",
        "Start with `input-contract-changes.md` for added, removed, and changed SWAT+ inputs and their source read order. Use `schema-read-evidence.md` and `schema-diff.json` for extractor certification details. Generated candidate facts, schemas, rendered pages, site, and full logs stay in the ignored comparison workspace.",
        "",
        "This run proves repeatable generation for the locked candidate commit. Differences between base and candidate are expected and are reported as review targets; only a repeat run of the same candidate is required to have zero byte difference.",
        "",
    ]
    return "\n".join(lines)


def run_comparison(
    cfg: Config,
    name: str,
    *,
    fetch: bool = False,
    build_sources: bool = True,
    build_preview: bool = True,
) -> ComparisonRunResult:
    comparison = cfg.comparison(name)
    if comparison.base_source == comparison.candidate_source:
        raise ValueError("comparison base_source and candidate_source must be different")
    if fetch:
        fetch_profile(cfg, comparison.base_source)
        fetch_profile(cfg, comparison.candidate_source)

    base_dir, base_provenance = resolve_profile(cfg, comparison.base_source)
    candidate_dir, candidate_provenance = resolve_profile(cfg, comparison.candidate_source)
    work_dir = cfg.resolve(comparison.work_dir)
    report_dir = cfg.resolve(comparison.output_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    if build_sources:
        toolchain = {
            "cmake": _first_line(["cmake", "--version"]),
            "fortran": _first_line(["gfortran", "--version"]),
            "generator": "MinGW Makefiles",
            "build_type": "Release",
            "tag": f"{comparison.name.replace('_', '-')}-comparison",
        }
    else:
        toolchain = {
            "cmake": "not checked (source build skipped)",
            "fortran": "not checked (source build skipped)",
            "generator": "not checked (source build skipped)",
            "build_type": "Release",
            "tag": f"{comparison.name.replace('_', '-')}-comparison",
        }
    if build_sources:
        source_builds = {
            "toolchain": toolchain,
            "logs_dir": _relative(work_dir / "logs", cfg.root),
            "base": _build_source(
                cfg, comparison, comparison.base_source, "base"
            ),
            "candidate": _build_source(
                cfg, comparison, comparison.candidate_source, "candidate"
            ),
        }
    else:
        skipped = {
            "resolved_commit": "skipped",
            "configure": {"success": True},
            "build": {"success": True},
            "success": True,
            "skipped": True,
        }
        source_builds = {
            "toolchain": toolchain,
            "logs_dir": _relative(work_dir / "logs", cfg.root),
            "base": {**skipped, "resolved_commit": base_provenance.resolved_commit},
            "candidate": {**skipped, "resolved_commit": candidate_provenance.resolved_commit},
        }

    facts_dir = work_dir / "facts"
    base_diagnostics = parse_tree(base_dir, base_provenance.resolved_commit)
    candidate_diagnostics = parse_tree(
        candidate_dir, candidate_provenance.resolved_commit
    )
    candidate_repeat_diagnostics = parse_tree(
        candidate_dir, candidate_provenance.resolved_commit
    )
    base_store, _base_rich_docs = parse_documentation(
        base_dir,
        base_provenance.resolved_commit,
        diagnostics=base_diagnostics,
    )
    candidate_store, candidate_rich_docs = parse_documentation(
        candidate_dir,
        candidate_provenance.resolved_commit,
        diagnostics=candidate_diagnostics,
    )
    candidate_repeat, _candidate_repeat_rich_docs = parse_documentation(
        candidate_dir,
        candidate_provenance.resolved_commit,
        diagnostics=candidate_repeat_diagnostics,
    )
    base_facts = facts_dir / "base.json"
    candidate_facts = facts_dir / "candidate.json"
    candidate_repeat_facts = facts_dir / "candidate-repeat.json"
    base_store.save(base_facts)
    candidate_store.save(candidate_facts)
    candidate_repeat.save(candidate_repeat_facts)
    fact_hashes = {
        "base": _sha256(base_facts),
        "candidate": _sha256(candidate_facts),
        "candidate_repeat": _sha256(candidate_repeat_facts),
    }
    symbol_diff = _symbol_diff(base_store, candidate_store)
    symbol_diff["source"] = {
        "base_commit": base_provenance.resolved_commit,
        "candidate_commit": candidate_provenance.resolved_commit,
    }
    symbol_diff["determinism"] = {
        "candidate_sha256": fact_hashes["candidate"],
        "repeat_sha256": fact_hashes["candidate_repeat"],
        "zero_byte_diff": fact_hashes["candidate"] == fact_hashes["candidate_repeat"],
    }

    schemas_dir = work_dir / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    base_schema_result = _build_schema_payload(
        base_dir, base_provenance.resolved_commit, "pr-252-base"
    )
    candidate_schema_result = _build_schema_payload(
        candidate_dir, candidate_provenance.resolved_commit, "pr-252-candidate"
    )
    candidate_schema_repeat_result = _build_schema_payload(
        candidate_dir, candidate_provenance.resolved_commit, "pr-252-candidate"
    )
    base_schema = base_schema_result.payload
    candidate_schema = candidate_schema_result.payload
    candidate_schema_repeat = candidate_schema_repeat_result.payload
    base_schema_path = schemas_dir / "base.json"
    candidate_schema_path = schemas_dir / "candidate.json"
    candidate_schema_repeat_path = schemas_dir / "candidate-repeat.json"
    base_schema_path.write_bytes(schema_dumps(base_schema).encode("utf-8"))
    candidate_schema_path.write_bytes(schema_dumps(candidate_schema).encode("utf-8"))
    candidate_schema_repeat_path.write_bytes(
        schema_dumps(candidate_schema_repeat).encode("utf-8")
    )
    schema_hashes = {
        "base": _sha256(base_schema_path),
        "candidate": _sha256(candidate_schema_path),
        "candidate_repeat": _sha256(candidate_schema_repeat_path),
    }
    schema_diff = _schema_diff(
        base_schema,
        candidate_schema,
        base_project=base_schema_result.project,
        candidate_project=candidate_schema_result.project,
    )
    schema_diff["source"] = {
        "base_commit": base_provenance.resolved_commit,
        "candidate_commit": candidate_provenance.resolved_commit,
    }
    schema_diff["determinism"] = {
        "candidate_sha256": schema_hashes["candidate"],
        "repeat_sha256": schema_hashes["candidate_repeat"],
        "zero_byte_diff": schema_hashes["candidate"] == schema_hashes["candidate_repeat"],
    }
    input_contract_changes = _input_contract_diff(
        base_schema_result.project,
        base_schema,
        candidate_schema_result.project,
        candidate_schema,
    )
    repeat_input_contract_check = _input_contract_diff(
        candidate_schema_result.project,
        candidate_schema,
        candidate_schema_repeat_result.project,
        candidate_schema_repeat,
    )
    repeat_input_summary = repeat_input_contract_check["summary"]
    input_contract_changes["determinism"] = {
        "candidate_repeat_zero_change": all(
            repeat_input_summary[key] == 0
            for key in (
                "added",
                "removed",
                "changed",
                "new_unresolved_open_blocks",
                "resolved_unresolved_open_blocks",
            )
        ),
        "repeat_comparison_summary": repeat_input_summary,
    }
    input_contract_changes["source"] = {
        "base_commit": base_provenance.resolved_commit,
        "candidate_commit": candidate_provenance.resolved_commit,
    }

    pages = load_all(cfg.abs_docs_dir)
    base_status = compute_status(base_store, pages)
    candidate_status = compute_status(candidate_store, pages)
    page_status = _page_status_diff(base_status, candidate_status, cfg.root)
    base_findings = check_all(base_store, pages)
    candidate_findings = check_all(candidate_store, pages)
    grounding = _grounding_payload(base_findings, candidate_findings)

    if build_preview:
        preview = _build_preview(
            cfg,
            comparison,
            candidate_store,
            candidate_rich_docs,
            candidate_provenance.resolved_commit,
        )
    else:
        preview = {"success": True, "skipped": True}

    checks = {
        "base_compile": None
        if source_builds["base"].get("skipped")
        else bool(source_builds["base"]["success"]),
        "candidate_compile": None
        if source_builds["candidate"].get("skipped")
        else bool(source_builds["candidate"]["success"]),
        "facts_deterministic": bool(symbol_diff["determinism"]["zero_byte_diff"]),
        "schema_deterministic": bool(schema_diff["determinism"]["zero_byte_diff"]),
        "input_contract_deterministic": bool(
            input_contract_changes["determinism"]["candidate_repeat_zero_change"]
        ),
        "preview": None if preview.get("skipped") else bool(preview["success"]),
    }
    page_delta = page_status["pr_delta"]
    introduced_grounding = grounding["introduced_counts"]
    new_unresolved_files = sorted(
        {
            filename
            for section in schema_diff["unresolved_sections"].values()
            for filename in section["new"]
        }
    )
    summary = {
        "comparison": name,
        "title": comparison.title or name,
        "url": comparison.url,
        "source": {
            "base_profile": comparison.base_source,
            "base_ref": cfg.source_profile(comparison.base_source).ref,
            "base_commit": base_provenance.resolved_commit,
            "candidate_profile": comparison.candidate_source,
            "candidate_ref": cfg.source_profile(comparison.candidate_source).ref,
            "candidate_commit": candidate_provenance.resolved_commit,
        },
        "checks": checks,
        "parser": {
            "base_fallback_files": len(base_store.fallback_files),
            "candidate_fallback_files": len(candidate_store.fallback_files),
            "fallback_set_changed": sorted(base_store.fallback_files)
            != sorted(candidate_store.fallback_files),
        },
        "symbols": symbol_diff["summary"],
        "schemas": {
            **schema_diff["summary"],
            "new_unresolved_files": new_unresolved_files,
        },
        "inputs": input_contract_changes["summary"],
        "pages": {
            "newly_stale": len(page_delta["newly_stale"]),
            "newly_affected": len(page_delta["newly_affected"]),
            "newly_orphaned": len(page_delta["newly_orphaned"]),
            "new_missing_pages": len(page_delta["new_missing_pages"]),
            "candidate_counts": page_status["candidate"]["counts"],
        },
        "grounding": {
            "introduced_errors": introduced_grounding["errors"],
            "introduced_warnings": introduced_grounding["warnings"],
            "candidate_counts": grounding["candidate_counts"],
        },
        "ready_for_adoption": bool(
            all(value is True for value in checks.values())
            and schema_diff["summary"]["new_unresolved"] == 0
            and introduced_grounding["errors"] == 0
        ),
        "workspace": {
            "tracked_reports": _relative(report_dir, cfg.root),
            "ignored_artifacts": _relative(work_dir, cfg.root),
        },
    }

    _write_json(report_dir / "summary.json", summary)
    _write_json(report_dir / "symbol-diff.json", symbol_diff)
    _write_json(report_dir / "schema-diff.json", schema_diff)
    _write_json(report_dir / "input-contract-changes.json", input_contract_changes)
    _write_json(report_dir / "page-status.json", page_status)
    _write_json(report_dir / "grounding-findings.json", grounding)
    (report_dir / "schema-read-evidence.md").write_text(
        _schema_read_evidence_markdown(schema_diff), encoding="utf-8"
    )
    (report_dir / "input-contract-changes.md").write_text(
        _input_contract_changes_markdown(input_contract_changes), encoding="utf-8"
    )
    (report_dir / "source-build.md").write_text(
        _source_build_markdown(source_builds), encoding="utf-8"
    )
    (report_dir / "summary.md").write_text(
        _summary_markdown(summary), encoding="utf-8"
    )

    complete = all(value is not False for value in checks.values())

    def line_label(value: bool | None) -> str:
        return "skipped" if value is None else str(value)

    line = (
        "compile base/candidate="
        f"{line_label(checks['base_compile'])}/{line_label(checks['candidate_compile'])}; "
        f"facts zero-diff={checks['facts_deterministic']}; "
        f"schema zero-diff={checks['schema_deterministic']}; "
        f"input contracts zero-change={checks['input_contract_deterministic']}; "
        f"preview={line_label(checks['preview'])}"
    )
    return ComparisonRunResult(report_dir=report_dir, complete=complete, one_line_summary=line)
