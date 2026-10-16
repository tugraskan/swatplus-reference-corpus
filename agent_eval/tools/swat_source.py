"""Which SWAT+ source the agent_eval tools read: a source named in swatref.toml (default release_62_0_1).

Every tool takes `--source NAME`, the same names `swatref --source` uses. Without it they read SWAT+ 62.0.1, the
version the user-docs fix targets. A source's Tamandua facts are built once with the command `build_command`
prints; until then the tools refuse that source instead of answering from another version's facts.
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[2]
TAM = CORPUS / ".swatref" / "tamandua-0.5"
DEFAULT_SOURCE = "release_62_0_1"


@dataclass(frozen=True)
class Source:
    name: str      # swatref.toml name, e.g. release_62_0_1
    label: str     # e.g. "SWAT+ 62.0.1"
    version: str   # the git ref, e.g. "62.0.1"
    commit: str
    src: Path      # Fortran source folder
    refdata: Path  # example input files
    facts: Path    # Tamandua facts for this source


def facts_path(name: str) -> Path:
    """The 62.0.1 facts were built first, in the Tamandua folder itself; every other source gets a folder of its
    own, because Tamandua keeps a source's sidecar (swatplus-rhs.json) beside its facts file under a fixed name."""
    if name == DEFAULT_SOURCE:
        return TAM / "swatplus-62.0.1-facts.json"
    return TAM / "facts" / name / "swatplus-facts.json"


def resolve(name: str | None = None) -> Source:
    name = name or DEFAULT_SOURCE
    sources = tomllib.loads((CORPUS / "swatref.toml").read_text(encoding="utf-8")).get("sources", {})
    if name not in sources:
        raise SystemExit(f"Unknown --source {name!r}. swatref.toml defines: {', '.join(sources)}")
    s = sources[name]
    checkout = CORPUS / s["checkout"]
    return Source(name=name, label=s.get("label", name), version=str(s.get("ref", name)),
                  commit=s.get("commit", ""), src=checkout / s.get("subdir", "src"),
                  refdata=checkout / "refdata", facts=facts_path(name))


def rel(path: Path) -> str:
    return path.relative_to(CORPUS).as_posix()


def build_command(source: Source) -> str:
    return (f".swatref/tamandua-0.5/venv/Scripts/swatplus-build.exe --source {rel(source.src)} "
            f"--corpus . --facts {rel(source.facts)}")


def require_facts(source: Source) -> None:
    """Stop with the build command when the source has no Tamandua facts yet."""
    if not source.src.is_dir():
        raise SystemExit(f"No {source.label} source at {rel(source.src)} (the checkout swatref.toml names for "
                         f"{source.name}): check it out first.")
    if not source.facts.is_file():
        raise SystemExit(f"No Tamandua facts for {source.label} yet. Build them once (from the corpus root):\n"
                         f"  {build_command(source)}\n"
                         f"or read {rel(source.src)} directly instead.")
