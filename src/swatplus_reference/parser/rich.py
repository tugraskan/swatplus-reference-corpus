"""Rich parser: scans Fortran source into a structured ProjectIndex."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.parser.schema_model import ProjectIndex


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
            self.by_name[typ.name.lower()] = typ

    def get(self, name: str) -> Any | None:
        return self.by_name.get(name.lower())

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self.index), indent=2), encoding="utf-8")

    @classmethod
    def build(cls, source_dir: Path) -> "RichStore":
        scanner = FortranScanner(BuildConfig(source_dir=source_dir))
        index = scanner.scan()
        return cls(index=index)
