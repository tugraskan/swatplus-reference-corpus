"""Shared configuration for source, documentation, and schema pipelines."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_REPOSITORY = "https://github.com/swat-model/swatplus"
DEFAULT_MAIN_COMMIT = "cb442f7c05fc3bfc34349c446010f452d2737ca0"


@dataclass
class FillConfig:
    model: str = "claude-opus-4-8"
    max_tokens: int = 8192
    concurrency: int = 4


@dataclass
class SourceProfile:
    """One selectable upstream source checkout.

    ``ref`` may be a branch, tag, or commit. ``commit`` is an optional lock;
    when present, every consumer verifies the checkout against that exact SHA.
    """

    name: str
    repository: str = DEFAULT_REPOSITORY
    ref: str = "main"
    commit: str = ""
    checkout: Path = Path("external/swatplus-main")
    subdir: str = "src"
    label: str = ""
    depth: int = 1

    def abs_checkout(self, root: Path) -> Path:
        return self.checkout if self.checkout.is_absolute() else root / self.checkout

    def abs_source_dir(self, root: Path) -> Path:
        return self.abs_checkout(root) / self.subdir

    @property
    def pinned_ref(self) -> str:
        return self.commit or self.ref

    @property
    def version_label(self) -> str:
        if self.label:
            return self.label
        suffix = self.commit[:12] if self.commit else self.ref
        return f"SWAT+ {self.ref} @ {suffix}"

    def source_link_base(self, resolved_commit: str | None = None) -> str:
        repo = self.repository.removesuffix(".git")
        revision = resolved_commit or self.commit or self.ref
        return f"{repo}/blob/{revision}/{self.subdir.strip('/')}"


@dataclass
class SchemaPipelineConfig:
    source: str = "release_62_0_0"
    version: str = "62.0.0"
    output_dir: Path = Path("schemas/releases")
    range_csv: Path = Path("schema_data/modular_database_rev_61_0_nbs.csv")
    editor_report: Path = Path("reports/schema/swatplus-62.0.0-editor-schema-report.json")
    reports_dir: Path = Path("reports/schema")


@dataclass
class ComparisonConfig:
    """One locked source-to-source impact comparison."""

    name: str
    base_source: str
    candidate_source: str
    output_dir: Path
    work_dir: Path
    title: str = ""
    url: str = ""


@dataclass
class Config:
    root: Path

    # Compatibility fields used by the documentation modules and fixture
    # configs. A loaded swatref.toml derives them from [docs] and [sources.*].
    source_repo_url: str = DEFAULT_REPOSITORY
    source_ref: str = DEFAULT_MAIN_COMMIT
    source_dir: Path = Path("external/swatplus-cb442f7c05fc/src")
    source_link_base: str = f"{DEFAULT_REPOSITORY}/blob/{DEFAULT_MAIN_COMMIT}/src"
    version_label: str = "SWAT+ main @ cb442f7c05fc"
    docs_dir: Path = Path("docs_src")
    facts_path: Path = Path(".swatref/docs/facts.json")
    render_dir: Path = Path("docs")
    fill: FillConfig = field(default_factory=FillConfig)

    sources: dict[str, SourceProfile] = field(default_factory=dict)
    docs_source: str = "main"
    schema: SchemaPipelineConfig = field(default_factory=SchemaPipelineConfig)
    comparisons: dict[str, ComparisonConfig] = field(default_factory=dict)

    def resolve(self, p: Path) -> Path:
        return p if p.is_absolute() else self.root / p

    @property
    def abs_source_dir(self) -> Path:
        return self.resolve(self.source_dir)

    @property
    def abs_docs_dir(self) -> Path:
        return self.resolve(self.docs_dir)

    @property
    def abs_facts_path(self) -> Path:
        return self.resolve(self.facts_path)

    @property
    def abs_render_dir(self) -> Path:
        return self.resolve(self.render_dir)

    def source_profile(self, name: str | None = None) -> SourceProfile:
        selected = name or self.docs_source
        if self.sources:
            try:
                return self.sources[selected]
            except KeyError as exc:
                choices = ", ".join(sorted(self.sources))
                raise ValueError(f"unknown source profile {selected!r}; choose: {choices}") from exc
        checkout = self.source_dir.parent if self.source_dir.name == "src" else self.source_dir
        return SourceProfile(
            name=selected,
            repository=self.source_repo_url,
            ref=self.source_ref,
            commit=self.source_ref if len(self.source_ref) == 40 else "",
            checkout=checkout,
            subdir=self.source_dir.name if self.source_dir.name == "src" else "src",
            label=self.version_label,
        )

    def comparison(self, name: str) -> ComparisonConfig:
        try:
            return self.comparisons[name]
        except KeyError as exc:
            choices = ", ".join(sorted(self.comparisons)) or "none configured"
            raise ValueError(f"unknown comparison {name!r}; choose: {choices}") from exc


def _path(value: object, default: Path) -> Path:
    return Path(str(value)) if value is not None else default


def load_config(path: str | Path = "swatref.toml") -> Config:
    path = Path(path)
    data = tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    root = path.resolve().parent

    fill = FillConfig(**data.get("fill", {}))
    sources: dict[str, SourceProfile] = {}
    for name, raw in data.get("sources", {}).items():
        sources[name] = SourceProfile(
            name=name,
            repository=str(raw.get("repository", DEFAULT_REPOSITORY)),
            ref=str(raw.get("ref", "main")),
            commit=str(raw.get("commit", "")),
            checkout=_path(raw.get("checkout"), Path(f"external/swatplus-{name}")),
            subdir=str(raw.get("subdir", "src")),
            label=str(raw.get("label", "")),
            depth=int(raw.get("depth", 1)),
        )

    docs = data.get("docs", {})
    docs_source = str(docs.get("source", data.get("default_source", "main")))
    schema_raw = data.get("schema", {})
    schema = SchemaPipelineConfig(
        source=str(schema_raw.get("source", "release_62_0_0")),
        version=str(schema_raw.get("version", "62.0.0")),
        output_dir=_path(schema_raw.get("output_dir"), Path("schemas/releases")),
        range_csv=_path(
            schema_raw.get("range_csv"), Path("schema_data/modular_database_rev_61_0_nbs.csv")
        ),
        editor_report=_path(
            schema_raw.get("editor_report"),
            Path("reports/schema/swatplus-62.0.0-editor-schema-report.json"),
        ),
        reports_dir=_path(schema_raw.get("reports_dir"), Path("reports/schema")),
    )
    comparisons: dict[str, ComparisonConfig] = {}
    for name, raw in data.get("comparisons", {}).items():
        comparisons[name] = ComparisonConfig(
            name=name,
            base_source=str(raw["base_source"]),
            candidate_source=str(raw["candidate_source"]),
            output_dir=_path(
                raw.get("output_dir"), Path("reports") / "comparisons" / name
            ),
            work_dir=_path(
                raw.get("work_dir"), Path(".swatref") / "comparisons" / name
            ),
            title=str(raw.get("title", name)),
            url=str(raw.get("url", "")),
        )

    cfg = Config(
        root=root,
        docs_dir=_path(docs.get("pages"), Path("docs_src")),
        facts_path=_path(docs.get("facts"), Path(".swatref/docs/facts.json")),
        render_dir=_path(docs.get("render"), Path("docs")),
        fill=fill,
        sources=sources,
        docs_source=docs_source,
        schema=schema,
        comparisons=comparisons,
    )

    if sources:
        profile = cfg.source_profile(docs_source)
        cfg.source_repo_url = profile.repository
        cfg.source_ref = profile.commit or profile.ref
        cfg.source_dir = profile.checkout / profile.subdir
        cfg.source_link_base = profile.source_link_base()
        cfg.version_label = str(docs.get("version_label", profile.version_label))
    return cfg
