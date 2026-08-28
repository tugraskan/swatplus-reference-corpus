# SWAT+ Reference Corpus — Technical Specification

**Version:** 2.0  
**Package:** `swatplus_reference`  
**CLI:** `swatref`  
**Python:** 3.10 or newer

## 1. Purpose

The repository is the canonical home for both the reviewed SWAT+ documentation
corpus and release-oriented input schemas. The documentation builder is a
module inside this repository, not a second repository.

The system does not edit or vendor SWAT+ source. It consumes a configured local
Git checkout, verifies its exact commit, and generates reproducible reference
artifacts.

## 2. Pipeline boundaries

```text
swatref.toml
    |
    +-- source profile: main ------------------+
    |                                          |
    |                                  documentation parser
    |                                          |
    |                         .swatref/docs/facts.json (temporary)
    |                                          |
    |                    docs_src/ reviewed prose + generated facts
    |                                          |
    |                              docs/ -> MkDocs -> _site/
    |
    +-- source profile: release_62_0_0 --------+
                                               |
                                      schema scanner
                                               |
                           schema_artifacts/releases/*.json
                                                |
                   Editor report + range CSV --+-- range and field reports
```

The two consumers may select different profiles. This is intentional: readable
documentation can follow a pinned `main` commit while schemas follow a release
tag. Either can be pointed at another branch, tag, commit, or local checkout.

## 3. Source profiles and provenance

Each `[sources.NAME]` table supports:

| Key | Meaning |
|---|---|
| `repository` | Git remote URL |
| `ref` | Requested branch, tag, or commit |
| `commit` | Optional exact SHA lock |
| `checkout` | Ignored local checkout directory |
| `subdir` | Fortran source directory inside the checkout |
| `label` | Human-readable version label |
| `depth` | Fetch depth; `0` means full history |

Before parsing, `resolve_profile` reads `git rev-parse HEAD`. A configured
`commit` must match or the build stops. Branch/tag builds without a lock record
the resolved SHA. Documentation writes a derived source record under
`.swatref/sources/`; release schemas write a tracked provenance sidecar.

Provenance records contain only portable identifiers:

- profile name;
- repository URL;
- requested ref;
- configured commit lock;
- resolved commit; and
- artifact/version fields supplied by the consumer.

Local absolute paths and timestamps are excluded from tracked artifacts.

## 4. Package architecture

| Package | Responsibility |
|---|---|
| `source` | configuration, named profiles, fetch, exact-SHA verification |
| `parser` | documentation fact extraction and schema-oriented Fortran scan |
| `docs` | tracked page model, grounding, staleness, fact injection, rendering |
| `schema` | base schema, ranges, field maps, and Editor comparison |
| `comparison` | locked source builds, symbol/schema diffs, page impact, preview |
| `generation` | optional prose fill, batch fill, and source-diff refill |
| `provenance` | deterministic source/artifact records |
| `cli.py` | `source`, `docs`, `schema`, and `compare` command groups |

The two Fortran parsers have different contracts and are deliberately separate:

- the documentation parser uses fparser2 and produces a compact symbol fact
  store for pages and grounding; and
- the schema scanner preserves the richer legacy I/O/control model required by
  the reviewed schema resolver.

Sharing source selection and provenance prevents those parsers from silently
using different commits.

## 5. Documentation contract

### 5.1 Tracked input

`docs_src/` contains Markdown pages with YAML frontmatter. Pages own reviewed
prose. They do not own facts that can be derived from source.

### 5.2 Derived fact store

`.swatref/docs/facts.json` stores:

- symbols and kinds;
- source files and spans;
- arguments, locals, module variables, and derived-type components;
- calls, uses, and file I/O;
- module-state reads and writes;
- per-symbol source hashes;
- exact source commit; and
- parser fallback records.

The fact store is ignored and may be deleted at any time.

### 5.3 Rendering

`swatref docs render` copies tracked pages into ignored `docs/`, replaces
`<!-- facts:* -->` blocks, and resolves `[sym:name]` links. MkDocs writes the
ignored `_site/` directory.

### 5.4 Staleness

For each symbol page, the stored source hash is compared with the current fact
store:

| Condition | Result |
|---|---|
| no prose/hash | `todo` |
| symbol missing | `orphaned` |
| symbol hash changed | `stale` |
| nearby call/data-flow symbol changed | `affected` |
| hash matches | `filled` |

Affected is a review signal; it does not rewrite the page.

### 5.5 Grounding

`swatref docs check` fails on a wrong page symbol, broken symbol reference, or
structured note naming an argument/local/use/variable absent from the parser.
Unresolved backticked identifiers are warnings unless strict mode is selected.

## 6. Schema contract

### 6.1 Base schema

`swatref schema build` deterministically scans the configured source profile.
The output has sorted keys, a trailing newline, and no timestamp. It contains:

- flat input files;
- unresolved inputs with reasons;
- decision tables;
- multi-record files;
- multi-section files; and
- runtime-arity files.

Unknown layouts are reported, never invented.

### 6.2 Range schema

`swatref schema ranges` joins three tracked inputs:

1. the base source schema;
2. the SWAT+ Editor effective-schema report; and
3. `schema_artifacts/inputs/modular_database_rev_61_0_nbs.csv`.

A range is applied only when the Editor-to-Fortran name translation resolves
and the value does not contradict the row's own type, units, or description.
All rejected and inapplicable rows remain visible in the crosswalk reports.

### 6.3 Field map

`swatref schema field-map` produces a per-file mapping across spreadsheet name,
Editor database column, and Fortran variable. Both unmatched sides are kept;
the report does not discard drift.

### 6.4 Editor report

`swatref schema editor-report --editor-root PATH` compares the official schema
with a read-only SWAT+ Editor checkout. Peewee is an optional dependency used
only for this path and its tests. The report records the Editor commit and a
portable checkout name, not a machine-specific absolute path.

## 7. Reproducibility

### 7.1 Release and corpus gates

The following are build gates:

1. source profile resolves and satisfies its optional commit lock;
2. unit tests pass;
3. documentation status has no drift buckets;
4. documentation grounding has no errors;
5. rendering followed by `mkdocs build --strict` succeeds;
6. base schema has no unexpected unresolved files; and
7. rebuilding tracked schema/range/field artifacts leaves no Git diff.

Verified migration results:

- documentation render: 1,100 files before and after, zero byte differences;
- base 62.0.0 schema: zero byte differences;
- range-enriched 62.0.0 schema: zero byte differences;
- range crosswalk JSON/Markdown: zero byte differences; and
- field-map JSON/Markdown: zero byte differences.

The Editor report has one intentional metadata cleanup: its old machine path
was replaced by the portable checkout name. Scientific comparison content is
unchanged.

### 7.2 Locked source comparisons

Each `[comparisons.NAME]` table selects a locked base profile, locked candidate
profile, tracked report directory, and ignored work directory. `swatref compare
NAME` performs these independent checks without editing reviewed pages:

1. verify both exact commits;
2. compile both with the same compiler, generator, flags, build type, and tag;
3. parse both source trees and parse the candidate a second time;
4. generate both schemas and generate the candidate schema a second time;
5. inventory source-opened inputs using the schema resolver's literal, derived-
   type-slot, and reader-argument filename resolution;
6. report added, removed, changed, replacement-candidate, unresolved, symbol,
   parser-fallback, schema, page-status, and grounding changes;
7. render the candidate into an isolated directory and run strict MkDocs; and
8. require zero byte difference between repeated candidate facts and schemas,
   plus zero semantic changes between repeated candidate input contracts.

A base-to-candidate difference is expected and does not itself fail the run.
New unresolved schemas and grounding errors block corpus adoption but remain
reported review work rather than being silently filled or guessed. A readable
source contract that is not yet certified is published as
`readable_needs_schema_review`, including the source expression, resolved default
filename, read roles, conditions, and field order.

## 8. Tracked versus derived files

Tracked:

- reviewed pages in `docs_src/`;
- release schemas and provenance sidecars;
- schema source data and review reports;
- source/parser/builder code;
- tests, configuration, license, and CI.

Ignored and reproducible:

- `external/` source checkouts;
- `.swatref/` fact/provenance cache;
- rendered `docs/`;
- built `_site/`;
- test caches and virtual environments.

Manual prototype reports, obsolete migration tools, generated package metadata,
legacy overlay machinery, duplicate schema copies, and the old flat config were
not carried into the public repository.

## 9. Release update procedure

1. Add or update a source profile and its exact commit lock.
2. Fetch it and run `swatref source show NAME`.
3. Point `[schema].source` at the profile and set the artifact version.
4. Run schema build, ranges, and field-map commands.
5. Review unresolved/drift/quarantine reports.
6. Run the full reproducibility gates in section 7.
7. Commit the schema, reports, provenance sidecar, and configuration together.

For a documentation bump, preserve the old checkout, change `[docs].source`,
parse and mark staleness, then use the delta refill path only for changed pages.
