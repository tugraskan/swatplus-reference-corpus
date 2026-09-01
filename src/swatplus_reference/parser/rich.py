"""Rich parser: scans Fortran source into a structured ProjectIndex."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path
from types import UnionType
from typing import Any, Mapping, Union, get_args, get_origin, get_type_hints

from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.parser.schema_model import (
    DerivedTypeDoc,
    ModuleDoc,
    ProcedureDoc,
    ProgramDoc,
    ProjectIndex,
)
from swatplus_reference.parser.refs import (
    OutsideStateRef,
    extract_outside_state_refs,
    outside_state_ref_from_record,
    outside_state_ref_record,
)


SNAPSHOT_METADATA_KEY = "swatplus_reference_rich_snapshot"
SNAPSHOT_FORMAT = 1
OUTSIDE_STATE_METADATA_KEY = "swatplus_reference_outside_state_refs"


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

    def save(self, path: Path, *, provenance: Mapping[str, str] | None = None) -> None:
        """Write a portable, deterministic rich-parser snapshot.

        The payload remains a serialized ``ProjectIndex`` so existing consumers
        can keep reading its normal top-level collections. Provenance lives in
        ``metadata`` and is required before a renderer will use a cached file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(self.index)
        payload["source_root"] = "."
        metadata = dict(payload.get("metadata") or {})
        if provenance is not None:
            metadata[SNAPSHOT_METADATA_KEY] = {
                "format": SNAPSHOT_FORMAT,
                "source": dict(provenance),
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
        if expected_source_ref is not None:
            actual = (snapshot or {}).get("source", {}).get("resolved_commit")
            if actual != expected_source_ref:
                raise ValueError(
                    f"rich snapshot source is {actual or 'unrecorded'}, expected {expected_source_ref}"
                )
        return cls(index=_restore(raw, ProjectIndex))

    @classmethod
    def build(cls, source_dir: Path) -> "RichStore":
        scanner = FortranScanner(BuildConfig(source_dir=source_dir))
        index = scanner.scan()
        index.metadata[OUTSIDE_STATE_METADATA_KEY] = {
            cls._reference_key(proc.name, proc.kind, proc.location.path): [
                outside_state_ref_record(ref)
                for ref in extract_outside_state_refs(proc, index, source_dir)
            ]
            for proc in index.procedures
        }
        return cls(index=index)
