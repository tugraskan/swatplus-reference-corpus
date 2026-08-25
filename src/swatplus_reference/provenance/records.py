"""Deterministic provenance records shared by generated artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceProvenance:
    profile: str
    repository: str
    requested_ref: str
    configured_commit: str
    resolved_commit: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def write_provenance(path: Path, provenance: SourceProvenance, **extra: object) -> None:
    payload: dict[str, object] = {**provenance.to_dict(), **extra}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
