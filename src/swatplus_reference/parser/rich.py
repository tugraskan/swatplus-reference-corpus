"""Rich parser: scans Fortran source into a structured ProjectIndex."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.parser.schema_model import ProjectIndex, ModuleDoc, ProcedureDoc, DerivedTypeDoc


@dataclass
class RichStore:
    """Holds the richly-parsed ProjectIndex with a name lookup cache."""
    index: ProjectIndex
    by_name: dict[str, Any] = field(init=False)

    def __post_init__(self) -> None:
        self.by_name = {}
        for mod in self.index.modules:
            self.by_name[mod.name.lower()] = mod
        for proc in self.index.procedures:
            self.by_name[proc.name.lower()] = proc
        for typ in self.index.types:
            key = typ.name.lower()
            if key in self.by_name:
                self.by_name[f"type::{key}"] = typ
            else:
                self.by_name[key] = typ

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
        candidates = [self.by_name.get(key), self.by_name.get(f"type::{key}")]
        matches = []
        for candidate in candidates:
            if candidate is None:
                continue
            if isinstance(candidate, ModuleDoc):
                rich_kind = "module"
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
        return matches[0]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self.index), indent=2), encoding="utf-8")

    @classmethod
    def build(cls, source_dir: Path) -> "RichStore":
        scanner = FortranScanner(BuildConfig(source_dir=source_dir))
        index = scanner.scan()
        return cls(index=index)
