# SWAT+ Reference Corpus

This repository turns selected versions of the
[SWAT+](https://github.com/swat-model/swatplus) Fortran source into two kinds
of reference material:

1. readable documentation pages; and
2. machine-readable JSON input schemas and review reports.

The SWAT+ source itself is not copied into this repository. The build fetches
it into an ignored `external/` directory and verifies the exact Git commit
before producing anything.

This is an independent project, not the official SWAT+ documentation site.

## Current baselines

| Consumer | Requested source | Exact commit |
|---|---|---|
| Readable corpus | `main` | `cb442f7c05fc3bfc34349c446010f452d2737ca0` |
| Release schemas | tag `62.0.0` | `de210d64db4f1d75e110bd6af33ea9c333d27b8a` |

Both selections live in `swatref.toml`. A profile may use a branch, tag, or
commit. Adding `commit = "..."` locks it to an exact revision; omitting the
lock follows whatever the requested branch or tag resolves to and records the
actual SHA used.

## What is in this repository

```text
docs_src/                         1,095 reviewed Markdown corpus pages
  procedures/                     734 procedure pages
  modules/                         66 module pages
  io/                             192 input-file pages
  output_families/                103 output-family pages

schema_artifacts/
  inputs/
    modular_database_rev_61_0_nbs.csv
                                    tracked range and field reference input
  releases/
    swatplus-62.0.0.json          source-derived input schema
    swatplus-62.0.0-ranges.json   same schema with reviewed ranges
    swatplus-62.0.0.provenance.json
                                    exact source commit used
  reports/
    swatplus-62.0.0-editor-schema-report.json
    swatplus-62.0.0-field-map.{json,md}
    swatplus-62.0.0-range-crosswalk.{json,md}

reports/comparisons/
  pr-252/                         locked base-vs-candidate impact report

src/swatplus_reference/
  source/                          source profiles, fetching, SHA checks
  parser/                          documentation facts + schema scanner
  docs/                            pages, grounding, staleness, rendering
  schema/                          schema, range, field-map, Editor comparison
  comparison/                      locked builds, diffs, reproducibility checks
  generation/                      optional prose fill and delta refill
  provenance/                      deterministic provenance sidecars
  cli.py                           `swatref` command

tests/                             documentation and schema tests
swatref.toml                       all source and output configuration
mkdocs.yml                         readable-site build
```

Generated facts, rendered Markdown, the built website, test scratch space,
and fetched upstream repositories are ignored. They can all be recreated.

`swatref docs parse` builds one AST-backed `ProjectIndex` with fparser2 and
writes both the compact documentation facts and the local rich cache. The
legacy scanner remains selectable through `[docs].engine = "scanner"` for the
compatibility period. `swatref docs
rich-parse --snapshot` reuses that current parse to write a tracked-ready handoff
artifact at `snapshots/rich/<profile>-<resolved-commit>.rich.json` and an
adjacent provenance sidecar. This is the supported handoff for TAMANDUA or
another external consumer: it contains the selected engine's `ProjectIndex`, is
named by the exact SWAT+ commit, and records the selected profile, requested
ref/tag, configured lock, resolved commit, and explicit snapshot/export/model
versions. The current portable format is v3; metadata-bearing v1 and v2
snapshots remain readable, while unsupported or metadata-less files are
rejected or rebuilt by the normal CLI path. Both local documentation caches
must match that resolved commit and parser engine; stale caches are rebuilt
instead of being mixed with current facts.

## Quick start

```sh
python -m pip install -e ".[dev]"

# Fetch and verify both configured SWAT+ versions.
swatref source fetch main
swatref source fetch release_62_0_0
swatref source show main
swatref source show release_62_0_0

# Build and check the readable corpus.
swatref docs parse
swatref docs rich-parse --snapshot
swatref docs baseline
swatref docs status --require-current
swatref docs check
swatref docs render
swatref docs check-links
mkdocs build --strict

# Rebuild the release schema and its range/field reports.
swatref schema build
swatref schema ranges
swatref schema field-map

# Re-run the locked PR 252 comparison (fetch once, then compare).
swatref source fetch dev_pr252_base
swatref source fetch pr_252
swatref compare pr_252
```

## Comparing a branch or pull request

A `[comparisons.NAME]` entry selects two source profiles: an exact base and an
exact candidate. `swatref compare NAME` compiles both with the same settings,
parses the candidate twice, generates its schema twice, inventories source-opened
inputs, measures reviewed-page impact, runs grounding checks, and builds an
isolated strict documentation preview. Base-to-candidate differences are review
targets; repeated facts and schemas from the same candidate must have a zero-byte
difference, and repeated input contracts must have zero semantic changes.

Tracked comparison reports contain portable commits, counts, detailed diffs,
resolved default filenames, source read order, and explicit
`readable_needs_schema_review` flags. Source checkouts, compiler logs, fact
stores, candidate schemas, rendered Markdown, and the preview site remain
ignored under `.swatref/comparisons/`. The command never fills prose or edits
`docs_src/`.

The main validation workflow runs tests, source-backed documentation checks,
the Phase 0 parser/snapshot freshness gate, schema reproduction, and a strict
MkDocs build. A path-filtered comparison
workflow regenerates the locked PR reports whenever comparison inputs or code
change. Full source compilation remains a manual release gate. The rendered site
is always available as a workflow artifact; GitHub Pages deployment is gated by
the repository variable `PUBLISH_PAGES=true` and only runs from corpus `main`.

## How the readable corpus works

The fparser2 AST parser creates a structured `ProjectIndex` from the selected
source. Exact source bytes and comments come from the shared source-text layer,
while the AST supplies ownership and structure. The documentation fact store is
a compact projection of that same index and contains things the code can prove: symbols,
arguments, variables, calls, module/type dependencies, file I/O, source spans,
exact declaration lines, and source hashes. Parser diagnostics and any
normalization applied only to parser input remain visible in `docs parse`, the
rich snapshot, and comparison reports.

The tracked pages contain reviewed prose plus markers such as
`<!-- facts:calls -->`. Rendering replaces those markers with current facts and
resolves symbol links against the exact commit. This keeps generated facts out
of the reviewed prose. Procedure call relationships and parsed control-flow
outlines render as clickable Mermaid diagrams; every diagram node opens the
corresponding line in the commit-pinned GitHub source.

Each page records the hash of its source symbol. `swatref docs status` reports
which pages are current, changed, indirectly affected through calls, shared
state, imported modules, or derived types, unfinished, orphaned, or missing.
Affected pages are advisory under `--require-current`; use
`--fail-on-affected` when a workflow intentionally requires every indirectly
affected page to be reviewed before it can pass.
`swatref docs check` mechanically checks prose against parser facts.

The current corpus validates as:

- 1,095 filled pages;
- 0 stale, affected, unfinished, orphaned, or missing pages;
- 0 grounding errors; and
- 3,869 non-blocking identifier warnings.

The migration baseline is tracked under `reports/parser-baseline/`. It records
counts and stable identity hashes for every rich fact category, call-resolution
and graph fanout behavior, documentation and grounding totals, schema summaries,
artifact hashes, known parser failures, and named difficult source cases.
`swatref docs baseline` reparses the pinned source and fails if either that
normalized report or the portable rich snapshot has drifted. Use
`swatref docs baseline --write` only when intentionally reviewing a new
baseline.

`swatref docs check-links` audits the rendered corpus against the pinned
checkout: every emitted GitHub source link must sit on the pinned commit, name
a file that exists in that tree, and cite lines that exist in that file. It
resolves links locally rather than requesting them, so the gate does not depend
on GitHub availability. Run it after `swatref docs render`.

`fparser` is pinned to an exact version because its version string and its
syntax-error text both appear inside byte-compared baseline artifacts; upgrading
it is a reviewed baseline change, and `swatref docs baseline` names the moved
contract when that is what drifted.

## How schemas work

Schema inputs, release outputs, and review reports live together under
`schema_artifacts/`. The subdirectories keep their lifecycles explicit:
`inputs/` is checked-in reference material, `releases/` is generated release
schema JSON, and `reports/` is generated evidence for review.

`swatref schema build` scans the configured release source and writes a
deterministic JSON description of SWAT+ input files. Release 62.0.0 contains
145 resolved file schemas and 0 unresolved files, plus separate structures for
decision tables, multi-record files, multi-section files, and runtime-sized
records.

`swatref schema ranges` translates reviewed ranges from the CSV through the
Editor/source crosswalk. It never guesses. For release 62.0.0 it applies 444
ranges and reports 15 drift cases, 13 needing review, 14 quarantined
contradictions, and 526 rows that do not apply to the input schema.

`swatref schema field-map` writes the full spreadsheet-to-Editor-to-Fortran
mapping in JSON and readable Markdown.

For backward compatibility with the reviewed release artifact, the schema JSON
keeps its historical generator label. Exact modern provenance is stored in the
adjacent `.provenance.json` file, including requested ref and resolved commit.

## Changing a source version

Edit or add a profile in `swatref.toml`, then point `[docs].source` or
`[schema].source` at that profile. For example:

```toml
[sources.my_branch]
repository = "https://github.com/swat-model/swatplus"
ref = "feature-branch"
checkout = "external/swatplus-my-branch"
subdir = "src"
depth = 1

[schema]
source = "my_branch"
version = "my-branch-build"
```

Add a `commit` value when the result must be reproducible. Keep the previous
source checkout when updating documentation so `swatref docs refill` can make
small, source-diff-driven prose changes instead of rewriting whole pages.

## Optional prose generation

The corpus is usable without any AI service. Prose generation is only a
maintenance tool for unfinished or changed pages:

```sh
python -m pip install -e ".[fill]"
swatref docs fill --limit 10
swatref docs refill --old-source-dir external/swatplus-OLD/src
```

Generated prose still passes through the same symbol-grounding checks before it
is saved.

## License

Repository-owned code, corpus content, schemas, and reports are released under
the [MIT License](LICENSE). Fetched SWAT+ and SWAT+ Editor source trees are not
redistributed and retain their upstream licenses. See [NOTICE.md](NOTICE.md).
