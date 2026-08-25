"""Small scanner configuration kept separate from public pipeline config."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class BuildConfig:
    """Inputs used by the schema-oriented Fortran scanner."""

    project_name: str = "SWAT+"
    source_dir: Path = Path(".")
    output_dir: Path = Path("site")
    extensions: list[str] = field(
        default_factory=lambda: ["f90", "F90", "for", "f", "f95", "F95"]
    )
    exclude: list[str] = field(
        default_factory=lambda: ["**/.git/**", "**/site/**"]
    )
