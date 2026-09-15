"""Rich parser: scans Fortran source into a structured ProjectIndex."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, fields, is_dataclass
from pathlib import Path
from types import UnionType
from typing import Any, Mapping, Union, get_args, get_origin, get_type_hints

from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.parser.schema_model import (
    AssignmentDoc,
    CallRef,
    ControlStep,
    DerivedTypeDoc,
    IOFileDoc,
    IOOperation,
    ModuleDoc,
    OutputFamilyDoc,
    OutputFile,
    ProcedureDoc,
    ProgramDoc,
    ProjectIndex,
    ReviewFlag,
    SelectCaseDoc,
    SourceFileDoc,
    SourceLocation,
    UseRef,
    VariableRef,
    record_identity,
    record_scope,
)
from swatplus_reference.parser.refs import (
    OutsideStateRef,
    extract_outside_state_refs,
    outside_state_ref_from_record,
    outside_state_ref_record,
)
from swatplus_reference.parser.semantic import (
    annotate_project_dataflow,
    resolve_project_calls,
)


SNAPSHOT_METADATA_KEY = "swatplus_reference_rich_snapshot"
SNAPSHOT_FORMAT = 3
RICH_EXPORT_SCHEMA = "swatplus-reference-rich-v3"
EXPORT_SCHEMAS_BY_FORMAT = {
    2: "swatplus-reference-rich-v2",
    SNAPSHOT_FORMAT: RICH_EXPORT_SCHEMA,
}
SUPPORTED_SNAPSHOT_FORMATS = frozenset({1, *EXPORT_SCHEMAS_BY_FORMAT})
# The export schema names the field-level wire contract; the snapshot format
# names the envelope around it. They move independently, so a reader has to
# check both. Format 1 predates the export identifier and carries none.
SUPPORTED_EXPORT_SCHEMAS = frozenset(EXPORT_SCHEMAS_BY_FORMAT.values())
EXPORT_SCHEMA_REQUIRED_FROM_FORMAT = 2
RICH_MODEL_VERSION = "project-index-v2"
# The parser identity recorded in a snapshot. It names the engine that produced
# the store, so a consumer can tell the two apart and a cache built by one is
# never reused for the other.
#
# `fortran-scanner-v6`: the legacy line-oriented scanner. v6 because the
# declaration pattern gained one level of nesting inside a character length,
# and a behaviour change has to advance the identity or a pre-fix cache is
# reused in silence.
SCANNER_PARSER_VERSION = "fortran-scanner-v6"
AST_PARSER_VERSION = "fparser-ast-v1"

# Which parser produces the raw index.
#
# Phase 8 made `fparser2` the default once every gate passed: the field-level
# parity harness reports no unexpected difference, and every documentation
# consumer passes on the AST-produced index. The legacy scanner stays
# selectable for one compatibility period -- set `engine` under `[docs]` in
# `swatref.toml` -- and is removed only after it.
SCANNER_ENGINE = "scanner"
AST_ENGINE = "fparser2"
ENGINES = frozenset({SCANNER_ENGINE, AST_ENGINE})
DEFAULT_ENGINE = AST_ENGINE

PARSER_VERSIONS = {
    SCANNER_ENGINE: SCANNER_PARSER_VERSION,
    AST_ENGINE: AST_PARSER_VERSION,
}


def parser_version(engine: str = DEFAULT_ENGINE) -> str:
    """The identity an *engine*-produced snapshot records."""

    return PARSER_VERSIONS[engine]
OUTSIDE_STATE_METADATA_KEY = "swatplus_reference_outside_state_refs"
FPARSER_DIAGNOSTICS_METADATA_KEY = "swatplus_reference_fparser_diagnostics"


# The portable snapshot is a public contract. Keep its fields explicit so a
# new internal dataclass attribute cannot silently become a Tamandua-facing
# wire change merely because it was added to ProjectIndex.
_EXPORT_FIELDS: dict[type, tuple[str, ...]] = {
    SourceLocation: ("path", "line", "end_line"),
    AssignmentDoc: (
        "kind",
        "summary",
        "raw",
        "location",
        "target",
        "target_root",
        "expression",
    ),
    ReviewFlag: ("code", "severity", "message", "location", "target"),
    VariableRef: ("name", "declaration", "location", "vartype", "initial", "doc"),
    UseRef: ("module", "only", "intrinsic", "location"),
    CallRef: ("name", "raw", "location", "resolved", "kind"),
    ControlStep: (
        "kind",
        "summary",
        "raw",
        "location",
        "depth",
        "block_id",
        "parent_id",
        "branch_of",
        "end_line",
    ),
    SelectCaseDoc: ("subject", "cases", "location"),
    IOOperation: (
        "kind",
        "unit",
        "file_expr",
        "file_resolved",
        "raw",
        "location",
        "fields",
        "condition",
    ),
    DerivedTypeDoc: (
        "name",
        "location",
        "module",
        "parent",
        "doc",
        "components",
        "review_flags",
        "identity",
    ),
    ProcedureDoc: (
        "name",
        "kind",
        "location",
        "module",
        "parent",
        "args",
        "doc",
        "uses",
        "variables",
        "calls",
        "called_by",
        "call_paths",
        "control_steps",
        "io",
        "assignments",
        "review_flags",
        "select_cases",
        "identity",
    ),
    ModuleDoc: (
        "name",
        "location",
        "doc",
        "uses",
        "variables",
        "procedures",
        "types",
        "review_flags",
        "identity",
    ),
    ProgramDoc: (
        "name",
        "location",
        "doc",
        "uses",
        "calls",
        "control_steps",
        "review_flags",
        "identity",
    ),
    SourceFileDoc: ("path", "modules", "programs", "procedures", "types"),
    IOFileDoc: ("key", "display_name", "operations", "procedures", "review_flags"),
    OutputFile: (
        "name",
        "frequency",
        "fmt",
        "unit",
        "open_location",
        "open_condition",
    ),
    OutputFamilyDoc: (
        "key",
        "display_name",
        "base",
        "opened_by",
        "written_by",
        "files",
        "review_flags",
    ),
    ProjectIndex: (
        "project_name",
        "source_root",
        "files",
        "modules",
        "programs",
        "procedures",
        "types",
        "io_files",
        "output_families",
        "review_flags",
        "stats",
        "metadata",
    ),
}
_INTENTIONALLY_INTERNAL_EXPORT_FIELDS: dict[type, frozenset[str]] = {
    # Phase 3 preserves non-ONLY rename lists in the canonical model. The v3
    # wire contract remains frozen until the planned snapshot-version change.
    UseRef: frozenset({"renames"}),
    # Phase 4 call resolution records exact and ambiguous definition identities
    # without changing the frozen rich-v3 wire shape.
    CallRef: frozenset({"resolved_target", "resolution_candidates"}),
    # Phase 4 shared-state derivation. `FactStore` already carries reads/writes
    # to its consumers; holding them on the canonical model too keeps the
    # projection from recomputing them, without widening the frozen v3 shape.
    ProcedureDoc: frozenset({"reads", "writes"}),
    ProgramDoc: frozenset({"reads", "writes"}),
}


def _export_field_names(record_type: type) -> tuple[str, ...]:
    """Return the reviewed wire fields and fail on an unclassified model field."""

    names = _EXPORT_FIELDS.get(record_type)
    if names is None:
        raise TypeError(f"{record_type.__name__} is not in the rich export schema")
    declared = {item.name for item in fields(record_type)}
    exported = set(names)
    internal = set(_INTENTIONALLY_INTERNAL_EXPORT_FIELDS.get(record_type, ()))
    if exported & internal or exported | internal != declared:
        missing = sorted(declared - exported - internal)
        unknown = sorted((exported | internal) - declared)
        raise TypeError(
            f"{record_type.__name__} export fields are out of sync; "
            f"unclassified={missing}, unknown={unknown}"
        )
    return names


def _export_value(value: Any) -> Any:
    """Convert the rich model to the explicit v2 portable contract."""

    if is_dataclass(value):
        names = _export_field_names(type(value))
        payload = {}
        for name in names:
            item = getattr(value, name)
            if name == "calls" and isinstance(value, (ProcedureDoc, ProgramDoc)):
                # Function-like tokens begin as broad regex candidates. Export
                # only those proven to be functions; explicit CALL statements
                # remain visible even when their target is unresolved.
                item = [
                    call
                    for call in item
                    if call.kind != "function" or call.resolved
                ]
            payload[name] = _export_value(item)
        return payload
    if isinstance(value, list):
        return [_export_value(item) for item in value]
    if isinstance(value, tuple):
        return [_export_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _export_value(item) for key, item in value.items()}
    return value


def _restore(value: Any, annotation: Any) -> Any:
    """Recreate schema dataclasses from the JSON written by :meth:`save`."""
    if value is None:
        return None
    origin = get_origin(annotation)
    if origin in (Union, UnionType):
        for candidate in get_args(annotation):
            if candidate is type(None):
                continue
            try:
                return _restore(value, candidate)
            except (KeyError, TypeError, ValueError):
                continue
        return value
    if origin is list:
        (item_type,) = get_args(annotation) or (Any,)
        return [_restore(item, item_type) for item in value]
    if origin is dict:
        key_type, value_type = get_args(annotation) or (Any, Any)
        return {
            _restore(key, key_type): _restore(item, value_type)
            for key, item in value.items()
        }
    if annotation is Any:
        return value
    if isinstance(annotation, type) and is_dataclass(annotation):
        annotations = get_type_hints(annotation)
        return annotation(
            **{
                item.name: _restore(value[item.name], annotations[item.name])
                for item in fields(annotation)
                if item.name in value
            }
        )
    return value


@dataclass
class RichStore:
    """Holds the richly-parsed ProjectIndex with a name lookup cache."""
    index: ProjectIndex
    by_name: dict[str, Any] = field(init=False)
    records_by_name: dict[str, list[Any]] = field(init=False)
    # Set by build() only; a store loaded from a snapshot has no scan to pin.
    scan_call_identity: str | None = field(init=False, default=None)
    # Which engine produced this index. A store loaded from a snapshot reports
    # the engine recorded in it, so the two are never confused.
    engine: str = field(init=False, default=DEFAULT_ENGINE)

    def has_current_contract(self, engine: str | None = None) -> bool:
        """Whether this store came from the contract *engine* emits now.

        A snapshot records which parser produced it, so a cache built by the
        other engine fails this check and is rebuilt rather than reused. The
        caller passes the configured engine; a store that knows its own uses
        that.
        """

        snapshot = (self.index.metadata or {}).get(SNAPSHOT_METADATA_KEY, {})
        expected = {
            "format": SNAPSHOT_FORMAT,
            "export": RICH_EXPORT_SCHEMA,
            "model": RICH_MODEL_VERSION,
            # Compared against the engine this store was built for, so a cache
            # produced by the other engine is rebuilt rather than reused.
            "parser": parser_version(engine or self.engine),
        }
        return isinstance(snapshot, dict) and all(
            snapshot.get(key) == value for key, value in expected.items()
        )

    def __post_init__(self) -> None:
        self.by_name = {}
        self.records_by_name = {}
        for record in [
            *self.index.modules,
            *self.index.programs,
            *self.index.procedures,
            *self.index.types,
        ]:
            key = record.name.lower()
            self.records_by_name.setdefault(key, []).append(record)
            # Keep the original simple lookup for callers that only have a
            # name. Kind-aware rendering uses records_by_name below instead.
            self.by_name.setdefault(key, record)

    def get(self, name: str) -> Any | None:
        return self.by_name.get(name.lower())

    def get_of_kind(self, name: str, kind: str, file: str | None = None) -> Any | None:
        """Return the symbol named `name` matching `kind`, optionally disambiguated by file.

        `kind` is one of the thin Symbol.kind values the caller already has:
        "module", "subroutine", "function", or "type". Guards Phase 2
        enrichment against a bare-name collision (e.g. a type and a
        subroutine sharing a name) ever letting the wrong kind's rich
        record enrich a page.

        `file` is the thin symbol's own `.file` value (a source-relative path).
        When multiple same-kind candidates share `name` (e.g. two derived types
        named `field` in different modules), passing `file` picks the one whose
        rich `.location.path` matches. If `file` is given but nothing matches it
        exactly, returns None (fails closed) rather than guessing.

        Note: does not disambiguate 3+ same-bare-name symbols where 2+ are types
        and 1 is a non-type (e.g., procedure + 2 types sharing a name); not
        observed in real data and out of scope for this minimal strategy.
        """
        key = name.lower()
        candidates = self.records_by_name.get(key, [])
        matches = []
        for candidate in candidates:
            if candidate is None:
                continue
            if isinstance(candidate, ModuleDoc):
                rich_kind = "module"
            elif isinstance(candidate, ProgramDoc):
                rich_kind = "program"
            elif isinstance(candidate, DerivedTypeDoc):
                rich_kind = "type"
            elif isinstance(candidate, ProcedureDoc):
                rich_kind = candidate.kind
            else:
                continue
            if rich_kind == kind:
                matches.append(candidate)
        if not matches:
            return None
        if file is not None:
            for candidate in matches:
                if getattr(candidate.location, "path", None) == file:
                    return candidate
            return None
        return matches[0] if len(matches) == 1 else None

    @staticmethod
    def _reference_key(name: str, kind: str, file: str) -> str:
        return f"{kind.lower()}:{name.lower()}:{file.lower()}"

    def outside_state_refs_for(self, name: str, kind: str, file: str) -> list[OutsideStateRef]:
        """Return declaration-backed external references captured at rich-parse time."""
        raw = (self.index.metadata or {}).get(OUTSIDE_STATE_METADATA_KEY, {})
        records = raw.get(self._reference_key(name, kind, file), [])
        return [outside_state_ref_from_record(record) for record in records]

    def stamp_identities(self) -> None:
        """Give every named record its stable identity.

        Derived from data a v1 snapshot also carries, so a converted snapshot
        gets real identities rather than nulls.
        """

        groups = (
            (self.index.modules, lambda record: "module", lambda record: None),
            (self.index.programs, lambda record: "program", lambda record: None),
            (
                self.index.procedures,
                lambda record: record.kind,
                lambda record: record_scope(record.module, record.parent),
            ),
            (
                self.index.types,
                lambda record: "type",
                lambda record: record_scope(record.module, record.parent),
            ),
        )
        for records, kind_of, scope_of in groups:
            for record in records:
                record.identity = record_identity(
                    kind_of(record),
                    record.name,
                    record.location.path,
                    scope_of(record),
                )

    def call_observations(self) -> list[tuple[str, str, str, str, int, int | None]]:
        """Return every call site as an ordered, resolution-independent identity.

        Deliberately excludes ``name`` and ``resolved`` because resolution owns
        those. Everything else is what the scanner observed in the source and
        must survive untouched.
        """

        return [
            (
                holder.name.lower(),
                call.kind,
                call.raw,
                call.location.path,
                call.location.line,
                call.location.end_line,
            )
            for holder in [*self.index.procedures, *self.index.programs]
            for call in holder.calls
        ]

    def call_observation_identity(self) -> str:
        """Hash the ordered call observations so drift is comparable and small."""

        body = json.dumps(self.call_observations(), separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(body).hexdigest()

    def resolve_calls(self) -> None:
        """Derive the index's semantic layer: calls, call paths, shared state.

        This is the one hook every consumer already runs before reading derived
        relationships -- build, save, the documentation projection and the
        baseline -- so the shared-state annotation belongs here rather than in
        any single one of them.
        """

        observations_before = self.call_observations()
        resolve_project_calls(self.index)
        if self.call_observations() != observations_before:
            raise RuntimeError("call resolution changed source observations")
        annotate_project_dataflow(self.index)

    def save(self, path: Path, *, provenance: Mapping[str, str] | None = None) -> None:
        """Write a portable, deterministic rich-parser snapshot.

        The payload remains a serialized ``ProjectIndex`` so existing consumers
        can keep reading its normal top-level collections. Provenance lives in
        ``metadata`` and is required before a renderer will use a cached file.
        """
        # Saving is a supported public entry point, so do not rely on a caller
        # having projected documentation facts first to resolve function calls.
        self.resolve_calls()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = _export_value(self.index)
        payload["source_root"] = "."
        metadata = dict(payload.get("metadata") or {})
        metadata[SNAPSHOT_METADATA_KEY] = {
            "format": SNAPSHOT_FORMAT,
            "export": RICH_EXPORT_SCHEMA,
            "model": RICH_MODEL_VERSION,
            "parser": parser_version(self.engine),
            "source": dict(provenance or {}),
        }
        payload["metadata"] = metadata
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    @classmethod
    def load(cls, path: Path, *, expected_source_ref: str | None = None) -> "RichStore":
        """Load a saved store, refusing a known snapshot for another source SHA."""
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"rich snapshot {path} is not a JSON object")
        metadata = raw.get("metadata") or {}
        snapshot = metadata.get(SNAPSHOT_METADATA_KEY)
        if not isinstance(snapshot, dict):
            raise ValueError(f"rich snapshot {path} has no format metadata")
        try:
            snapshot_format = int(snapshot.get("format"))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"rich snapshot {path} has an invalid format") from exc
        if snapshot_format not in SUPPORTED_SNAPSHOT_FORMATS:
            supported = ", ".join(str(item) for item in sorted(SUPPORTED_SNAPSHOT_FORMATS))
            raise ValueError(
                f"rich snapshot {path} uses format {snapshot_format}; "
                f"supported formats: {supported}"
            )
        export = snapshot.get("export")
        if export is None and snapshot_format >= EXPORT_SCHEMA_REQUIRED_FROM_FORMAT:
            raise ValueError(
                f"rich snapshot {path} uses format {snapshot_format} but names no export schema"
            )
        if export is not None and export not in SUPPORTED_EXPORT_SCHEMAS:
            supported = ", ".join(sorted(SUPPORTED_EXPORT_SCHEMAS))
            raise ValueError(
                f"rich snapshot {path} uses export schema {export!r}; "
                f"supported export schemas: {supported}"
            )
        expected_export = EXPORT_SCHEMAS_BY_FORMAT.get(snapshot_format)
        if expected_export is not None and export != expected_export:
            raise ValueError(
                f"rich snapshot {path} uses format {snapshot_format} with export "
                f"schema {export!r}; format {snapshot_format} requires {expected_export!r}"
            )
        if expected_source_ref is not None:
            actual = snapshot.get("source", {}).get("resolved_commit")
            if actual != expected_source_ref:
                raise ValueError(
                    f"rich snapshot source is {actual or 'unrecorded'}, expected {expected_source_ref}"
                )
        store = cls(index=_restore(raw, ProjectIndex))
        parser_identity = snapshot.get("parser")
        if isinstance(parser_identity, str):
            if parser_identity.startswith("fortran-scanner-"):
                store.engine = SCANNER_ENGINE
            elif parser_identity.startswith("fparser-ast-"):
                store.engine = AST_ENGINE
        store.stamp_identities()
        return store

    @classmethod
    def build(cls, source_dir: Path, *, engine: str = DEFAULT_ENGINE) -> "RichStore":
        """Scan *source_dir* with *engine* and enrich the result.

        The engine chooses who produces the raw `ProjectIndex`; everything after
        that is identical, which is the point. Phase 7 ran every consumer
        against the fparser2-produced index "without invoking the legacy
        scanner", and that was only a meaningful test because the two indexes
        travel the same path afterwards.
        """

        if engine not in ENGINES:
            raise ValueError(f"unknown parser engine {engine!r}; expected one of {sorted(ENGINES)}")
        config = BuildConfig(source_dir=source_dir)
        if engine == AST_ENGINE:
            from swatplus_reference.parser.ast_index import build_ast_index

            index = build_ast_index(config)
        else:
            index = FortranScanner(config).scan()
        return cls.from_index(index, source_dir, engine=engine)

    @classmethod
    def from_index(
        cls, index: ProjectIndex, source_dir: Path, *, engine: str = DEFAULT_ENGINE
    ) -> "RichStore":
        """Enrich an already-parsed index, whichever parser produced it."""

        store = cls(index=index)
        store.engine = engine
        store.stamp_identities()
        # Capture raw parser evidence before enrichment or resolution can
        # mutate it. The baseline compares this with the projected result.
        store.scan_call_identity = store.call_observation_identity()
        index.metadata[OUTSIDE_STATE_METADATA_KEY] = {
            cls._reference_key(proc.name, proc.kind, proc.location.path): [
                outside_state_ref_record(ref)
                for ref in extract_outside_state_refs(proc, index, source_dir)
            ]
            for proc in index.procedures
        }
        store.resolve_calls()
        return store
