# fparser2 Migration Plan

Status: **proposal for review only**. Do not begin the parser migration until
this plan has been reviewed and approved.

Revision 3 incorporates the valid findings from both passes of Claude's review
at `claude/plan-review-gksznb`, plus the repository verification performed on
this branch. The original review used GitHub `main` at `db6423d`, which
predates the current rich-parser documentation pipeline. The current branch,
not that older commit, is authoritative for the baseline below.

## 1. Goal

Make fparser2 the main SWAT+ Fortran parser without losing anything currently
needed by:

- the Markdown documentation pages;
- commit-pinned GitHub line links;
- Mermaid call and control-flow graphs;
- schema and comparison tools; or
- the versioned `ProjectIndex` snapshot consumed by Tamandua.

The current rich `FortranScanner` remains in place until the fparser2 path has
proved equal or better on the same pinned SWAT+ source tree.

This is not just a parser replacement. It is a controlled migration of the
shared source-fact model and every consumer of that model.

### Current baseline

- `get_store()` calls `parse_documentation()`, which calls `RichStore.build()`
  and therefore the rich `FortranScanner`. The fparser2 path is currently a
  comparison tool, not the main documentation parser.
- The Markdown renderer currently generates clickable Mermaid call graphs and
  control-flow outlines, and MkDocs is configured to render Mermaid. These are
  existing capabilities that must be preserved.
- The documentation projection currently resolves `CallRef.resolved` and
  populates `called_by`. `call_paths` and the `ReviewFlag` collections are not
  meaningfully populated and must be treated as new or redesigned features.
- The present documentation projection destructively rewrites shared rich call
  data during `_resolve_calls()`: unresolved function candidates and repeated
  call sites can be lost. Phase 0 must correct this before freezing the call
  baseline.
- The fparser2 comparison path currently loses `parse_errors` and
  `fallback_files` when it projects rich documentation into `FactStore`.
- The comparison preview currently renders without its already-built rich
  store, so it validates degraded pages rather than the real published page
  shape. Phase 0 must make preview and normal rendering use the same inputs.
- Dependency-derived `affected` pages are described as a soft review signal,
  but `docs status --require-current` currently treats them as release-blocking.
  Revision 3 makes the soft behavior explicit and provides a separate strict
  gate for workflows that intentionally require all affected pages to be
  reviewed.
- The pinned source currently exposes two known fparser2 failures:
  `gwflow_floodplain.f90` and `gwflow_heat.f90`, both involving the accepted
  `expr*-1` spelling.

## 2. Decisions to approve before implementation

1. **Use one rich shared model.** A revised `ProjectIndex` becomes the canonical
   parser result. The fparser2 parser must produce this model directly.
2. **Keep `FactStore` as a projection.** Markdown grounding, hashes, page status,
   and generated fact blocks may continue using the smaller `FactStore`, but it
   must be derived from the canonical `ProjectIndex`, never from a second parse.
3. **Use a hybrid extraction method.** fparser2 supplies structure and AST
   relationships. A shared raw-source layer supplies comments, exact statement
   text, formatting, and reliable physical line spans.
4. **Version the external contract.** New model fields require a new snapshot
   format version. Snapshot readers must reject unsupported versions instead
   of silently dropping fields. Existing fields must remain readable during
   the transition.
5. **Make uncertainty visible.** Parse failures, fallback use, ambiguous calls,
   unresolved types, and incomplete facts must produce structured diagnostics.
6. **Keep the old scanner as the reference implementation.** It is removed only
   after all cutover gates in this plan pass.
7. **Never destroy observations during resolution.** Every parsed call site,
   including repeated, unresolved, and ambiguous calls, remains in the
   canonical model with its source location. Resolved relationships and
   `called_by` are derived indexes, not replacements for the observed calls.
8. **Preserve diagnostics through every projection.** `parse_errors`, fallback
   files, ambiguity, and provenance must survive the `ProjectIndex` to
   `FactStore` path and appear in CLI and comparison reports.
9. **Keep declared dependency edges uncapped.** A `use` or type dependency is
   explicit source evidence and must not be hidden by a fanout cap. Heuristic
   data-flow edges retain their separately documented cap. Baselines and
   reports must identify the edge kind.
10. **Keep `affected` advisory by default.** `docs status --require-current`
    reports affected pages but does not fail solely because of them. Add an
    explicit strict option, such as `--fail-on-affected`, for a release workflow
    that intentionally requires review of every affected page. Update SPEC
    section 7.1 to match this policy.
11. **Preview the real page shape.** Comparison preview rendering receives the
    same candidate rich store as normal rendering. A regression test compares
    the generated rich block set so a degraded preview cannot pass cutover.

## 3. What the unified model must contain

The parity matrix will track each category below for the old rich scanner and
the new fparser2 path.

| Category | Required facts |
|---|---|
| Source files | Complete deterministic inventory across all configured extensions and file relationships |
| Symbols | Modules, programs, procedures, functions, subroutines, and derived types |
| Locations | Exact file, start line, and end line for every supported fact |
| Page identity and staleness | `source_hash`, composite hashes, physical line-slice rules, and affected-page propagation |
| Documentation | Preceding comments, inline comments, units, and descriptions |
| Variables | Full declaration, type, attributes, initial value, scope, and location |
| Arguments and locals | Argument order, intent, declarations, defaults, and scope |
| Derived types | Components, declarations, defaults, documentation, and ownership |
| `use` statements | Module, `only` names, renames, intrinsic status, raw text, and location |
| Calls | Subroutine and function-style calls, raw text, kind, location, and resolution status |
| Call relationships | Existing `called_by` behavior plus new, explicitly tested call paths |
| Assignments | Full left side, full right side, raw text, derived-field path, and location |
| Control flow | Conditions, loops, loop index/header, block spans, nesting, and select cases |
| Select cases | Subject expressions, literal case vocabularies, nested blocks, and exact locations |
| I/O | Operation, unit, file expression, resolved file, fields, raw text, condition, and location |
| Project summaries | Input/output files, output families, modules, procedures, and type relationships |
| Data flow | Shared-state reads/writes, affected-page edges, and outside-state references without collapsing derived-field paths |
| Identity and lookup | Current bare-name/type collision policy and fail-closed kind-plus-file lookup |
| Diagnostics | Existing fparser2 errors/fallback files plus new ambiguity, provenance, and review diagnostics |
| Provenance | Parser/model/export versions, fparser version, repository, source commit, and deterministic metadata |

Some requirements exceed the present model. In particular, assignments need
separate left- and right-hand-side fields, loops need first-class spans and
nesting, call paths need an implemented definition, and review diagnostics need
an implemented producer. These are new capabilities, not parity fields.

## 4. Proposed pipeline

```text
Pinned SWAT+ source
        |
        v
Raw source and location map
        |
        +------------------------+
        |                        |
        v                        v
fparser2 AST extraction     comments/exact text overlay
        |                        |
        +-----------+------------+
                    v
          semantic resolution
     (calls, types, fields, I/O files)
                    |
                    v
             ProjectIndex v2
          /         |          \
         v          v           v
   FactStore     schemas      snapshot
   and docs    comparisons   for Tamandua
```

All source extraction remains inside `swatplus-reference-corpus`. Tamandua
consumes a versioned snapshot and does not become responsible for parsing
Fortran.

## 5. Implementation phases

### Phase 0: Freeze the reference baseline

Deliverables:

- Correct `_resolve_calls()` so resolution does not mutate or delete the
  canonical call observations. Preserve each call-site identity and source
  location, and derive resolved edges and `called_by` separately.
- Preserve fparser2 `parse_errors` and `fallback_files` when building the
  documentation `FactStore`; verify they appear in the CLI and comparison
  reports.
- Pass the candidate rich store into comparison preview rendering. Add a
  regression test proving preview and normal rendering generate the same rich
  block set, including assignments, control flow, select cases, outside-state
  references, and enriched variable/use/I/O tables.
- Save a deterministic rich-parser snapshot for the configured SWAT+ commit.
- Build the machine-readable parity-harness schema before parser work begins.
- Record counts and stable identities for every fact category in the matrix,
  including source hashes, data-flow/affected edges, outside-state references,
  select-case vocabularies, and name-collision behavior.
- Record current documentation, graph, schema, snapshot-size, parse-time, and
  peak-memory baselines.
- Add difficult real-source examples to a named regression fixture list.
- Include the three known thin/rich disagreements and the two known fparser2
  rejection files in that list.
- Record the current grounding baseline separately from comparison-candidate
  results. At the present pinned source it is zero errors and 3,867 warnings;
  Phase 0 must recompute and confirm those values.
- Document every known rich-parser limitation so an existing bug is not
  accidentally treated as required behavior.
- Record call-observation counts before resolution, resolved-edge counts after
  resolution, unresolved/ambiguous counts, and repeated call-site counts. The
  resolver must never reduce the observation count.
- Record affected-page fanout separately for declared module/type dependencies
  and heuristic data-flow dependencies. Do not apply the heuristic fanout cap
  to declared dependencies.
- Implement and document the advisory `affected` status policy and the separate
  strict affected-page gate before measuring release behavior.

Exit gate:

- Running the baseline twice produces identical normalized results.
- The source commit and parser version are recorded with the baseline.
- Call resolution preserves every observed call site and its location.
- Known fparser2 failures remain visible after every model projection.
- Comparison preview and normal rendering contain the same rich block set.
- `--require-current` and the strict affected-page option follow the documented
  policy, including a high-fanout dependency fixture.
- All 1,092 currently hashed pages retain their current hash at the pinned
  commit unless a separately reviewed one-time re-baseline is approved.

### Phase 1: Define `ProjectIndex v2`

Deliverables:

- Before adding v2 fields, make snapshot loading enforce an explicit set of
  supported format versions.
- Separate the internal model version from a dedicated, allowlisted export
  schema and its snapshot format version; do not serialize `asdict(index)` as
  the permanent Tamandua wire contract.
- Add a checked-in v1 contract fixture in this phase.
- Add structured records for assignments, control blocks/loops, raw
  statements, source spans, and parser diagnostics.
- Preserve existing `ProjectIndex` fields where practical.
- Add explicit parser, model, export, and snapshot versions.
- Pin fparser2 to an exact reviewed version and include it in provenance and
  cache invalidation.
- Add v1-to-v2 loading compatibility or a clearly documented conversion path.
- Define stable record identities so same-named symbols in different files or
  scopes cannot collide while preserving `FactStore.add()`'s existing
  procedure/module/type key behavior and `RichStore.get_of_kind()`'s
  fail-closed kind-plus-file lookup.
- Set the snapshot-size budget and decide in this phase whether the export is
  trimmed, compressed, or stored with Git LFS. The current snapshot is about
  48.3 MB, so storage is a model-shape constraint rather than a late check.
- Set reviewed full-parse time, peak-memory, and no-change cache budgets from
  the Phase 0 measurements.

Exit gate:

- Current rich-parser output can be represented in v2 without losing facts.
- Existing documentation and schema tests still pass through the compatibility
  layer.
- A current reader rejects a deliberately unsupported snapshot version.
- Tamandua's v1 contract fixture passes before any v2 export is produced.
- The proposed v2 export fits the approved storage and performance budgets.

### Phase 2: Build one source/location layer

Deliverables:

- Map fparser2 nodes and logical statements back to physical source lines.
- Freeze the current logical-source contract: comment handling, continuation
  joining, whitespace, case, and physical start/end spans.
- Preserve exact contract-defined raw text for multiline and continuation
  statements. Never use `str(node)` for consumer-visible source text.
- Attach preceding and inline comments deterministically.
- Centralize string/comment splitting so the AST and fallback paths do not
  duplicate it.
- Treat `IOOperation.raw`, `IOOperation.fields`, `IOOperation.condition`,
  `ControlStep.raw`, and `ControlStep.summary` as byte-sensitive compatibility
  fields. The schema resolver currently depends on the formatting of conditions
  and fields.
- Preserve the physical source-slice convention used by `hash_slice()` and
  `composite_source_hash()`.

Exit gate:

- Tests cover continuation lines, comments containing punctuation, semicolons,
  mixed case, closed-up `end` forms, and exact GitHub line spans.
- All existing page source hashes remain stable at the pinned commit, apart
  from any separately approved corrections.
- Byte-exact raw/field/condition fixtures match the current rich output.

### Phase 3: Populate structural facts from the AST

Implement in this order:

1. files, modules, programs, procedures, and derived types;
2. arguments, locals, module variables, and type components;
3. `use` statements, imports, `only` lists, and renames;
4. assignments and full component paths such as `aqu_d%rchrg`;
5. loops, conditionals, select blocks, nesting, and end locations;
6. calls and function-reference candidates; and
7. I/O statements and their source fields.

Array subscripts may be normalized for symbol resolution, but the stored source
path and raw expression must remain intact.

Exit gate:

- Unit and fixture tests pass for every category before the next category is
  considered complete.
- No AST fact has a missing location unless it carries a diagnostic explaining
  why.

### Phase 4: Add semantic and project-level resolution

Deliverables:

- Resolve calls against defined procedures using scope, imports, and symbol
  kinds. Keep every observed call site, including duplicates at different
  locations, and attach resolution results or diagnostics without rewriting
  the observation collection.
- Preserve the currently populated `resolved` and `called_by` behavior, and
  define call paths as a separately tested new capability.
- Resolve derived types and component paths without reducing them to root
  variable names.
- Resolve I/O units and filename expressions across procedures and modules.
- Reuse or port the current input/output-file and output-family aggregation.
- Compute shared-state reads/writes and dependency edges.
- Keep explicit module/type dependency propagation uncapped and label its edge
  kind. Keep any fanout limit confined to the documented heuristic data-flow
  edge kind.
- Preserve the `swatplus_reference_outside_state_refs` metadata family and its
  `kind:name:file` identity contract.

Exit gate:

- All derived relationships point back to source facts and locations.
- Ambiguity is reported instead of guessed or silently discarded.
- The number and identities of observed calls are unchanged by resolution.
- High-fanout declared dependencies propagate to every real dependent page.

### Phase 5: Make fallback behavior complete and visible

Deliverables:

- Catch parse failures per file, never for the complete project.
- Produce a `SourceFileDoc` and diagnostic for every rejected source file.
- Run a targeted raw-source fallback for supported facts.
- Mark every fallback-derived record and its confidence/provenance.
- Carry `parse_errors` and `fallback_files` through all model projections and
  show them in CLI status and comparison output.
- Keep fallback ordering and serialization deterministic.
- Add `gwflow_floodplain.f90`, `gwflow_heat.f90`, and the `expr*-1` construct
  as permanent regression cases.
- Evaluate a narrowly scoped lexical normalization for fparser2 when it is
  provably semantics-preserving. Even when normalized for AST input, all raw
  text, source hashes, and locations must come from the unchanged source.

During migration, selected logic from `FortranScanner` may be reused as the
fallback implementation. Migration is not complete while the full legacy
scanner is secretly required to produce normal fparser2 results.

Exit gate:

- No configured source file disappears from the index.
- Every fallback file produces the full required rich fact set, not only
  symbol/use/call names.
- Tests intentionally feed invalid and unsupported Fortran and verify visible
  degradation.

### Phase 6: Run and close the real parity harness

Use the field-level harness established in Phase 0 to replace the current
shallow symbol/count comparison.

For each fact category, report:

- exact matches;
- facts missing from fparser2;
- facts only found by fparser2;
- value or location disagreements;
- fallback-derived facts;
- unresolved or ambiguous facts; and
- explicitly reviewed AST corrections to old scanner behavior.

The comparison must run both parsers against the exact same pinned SWAT+
checkout. It may normalize collection order, identities, and explicitly
approved semantic equivalents. It must not normalize raw statements, I/O
fields, conditions, summaries, source spans, or source hashes; those are
byte-sensitive contracts. Deterministic serialization is checked separately.

Exit gate:

- No meaningful rich fact is missing.
- Every disagreement has a regression test and an explicit resolution.
- AST-proven corrections are recorded as intentional improvements rather than
  hidden by normalization.

### Phase 7: Verify every downstream consumer

Documentation gates:

- All Markdown pages render.
- Candidate comparison previews receive the candidate rich store and render
  the same rich fact-block set as normal site generation.
- Every generated GitHub URL uses the configured source commit.
- Every source link points to the correct current line or line span.
- Mermaid call and control-flow graphs render with clickable source nodes.
- Page hashes and direct/indirect staleness behave as before.
- Declared dependency fanout remains complete. Affected pages are reported but
  do not fail `--require-current`; the explicit strict option does fail while
  affected pages remain unreviewed.
- Grounding checks and strict MkDocs builds pass.

Schema/comparison gates:

- Existing schema and comparison test suites pass.
- Locked comparison reports remain reproducible or have reviewed changes.
- Rebuilding all tracked schema, range, crosswalk, and field-map artifacts
  leaves no Git diff, matching SPEC section 7.1 gate 7.
- Grounding remains at zero errors. Warning-count changes are reported and
  reviewed against the Phase 0 main-source baseline, never a PR candidate's
  comparison totals.

Tamandua gates:

- Save both v1-compatible and v2 snapshots during the transition if needed.
- Reuse the checked-in snapshot contract fixture added in Phase 1.
- Run Tamandua's snapshot-loading and graph/output tests against the candidate
  v2 artifact before changing the default producer.
- Document every intentional consumer-visible schema change.

Exit gate:

- All consumers pass against the fparser2-produced index without invoking the
  legacy scanner.

### Phase 8: Cut over and remove duplication

Rollout:

1. Add an explicit parser-engine option for development and CI.
2. Keep the rich scanner as the default while parity work is incomplete.
3. Run both engines in CI and publish the parity report.
4. Make fparser2 the default only after all gates pass.
5. Keep one short compatibility period in which the old scanner can be selected
   manually.
6. Remove the legacy scanner, redundant parsing code, and obsolete comparison
   switches after the compatibility period.

The supported end state may retain a small, independently tested raw-source
fallback engine. It must not retain the full legacy `FortranScanner` under a
new name or run a hidden second project-wide scan.

Exit gate:

- There is one normal parsing path, one shared model, one raw-source utility
  layer, and one documented fallback path.

## 6. Proposed pull-request breakdown

Keep changes reviewable and do not combine the model rewrite with the cutover.

1. **PR 1:** non-destructive call resolution and call-observation regression
   tests.
2. **PR 2:** diagnostic propagation and rich comparison-preview parity tests.
3. **PR 3:** affected-status policy, dependency-edge-kind baselines, parity
   inventory, baseline artifacts, and the full comparison harness.
4. **PR 4:** format enforcement, explicit export contract, exact fparser pin,
   `ProjectIndex v2`, size/performance decisions, and compatibility tests.
5. **PR 5:** shared source mapping, raw statement, and comment attachment.
6. **PR 6:** AST symbols, scopes, declarations, uses, and derived types.
7. **PR 7:** assignments, component paths, loops, select cases, and nesting.
8. **PR 8:** calls, call resolution, I/O, file resolution, and output families.
9. **PR 9:** fallback diagnostics and full-tree parity closure.
10. **PR 10:** documentation, graph, schema, and Tamandua integration gates.
11. **PR 11:** default-engine cutover.
12. **PR 12:** legacy removal after the agreed compatibility period.

Each PR must add tests for the capabilities it introduces and must not weaken
existing assertions merely to make parity numbers look better.

## 7. Testing strategy

### Small unit tests

Cover individual Fortran forms, including:

- free-form continuation lines;
- old and unusual SWAT+ declarations;
- type-bound and nested component references;
- array components and array subscripts;
- typed, recursive, pure, elemental, and module procedures;
- function calls versus array references;
- nested loops and conditionals;
- nested `select case` blocks;
- positional and keyword I/O control lists;
- internal reads and writes;
- strings containing `!`, commas, and parentheses; and
- malformed or unsupported source that triggers fallback.

### Real-source regression tests

- Run against all configured SWAT+ source files.
- Keep a focused list of difficult real routines for fast CI diagnosis.
- Store machine-readable and human-readable parity reports.
- Fail CI when a previously matched fact becomes missing or ambiguous.

### Compatibility tests

- Load existing rich snapshots.
- Reject unknown snapshot formats rather than silently dropping fields.
- Serialize the same result twice and compare bytes.
- Verify source commit and parser/model/export/fparser versions.
- Verify Tamandua's minimum required fields with a contract fixture.

### Performance tests

Phase 0 establishes the real baseline and Phase 1 approves budgets for full
parse time, peak memory, snapshot size, and cached no-change updates before the
model shape is frozen. Correctness is required first, but an unexpectedly slow
parser must not silently become the default. Cache invalidation must include
source commit, parser version, model version, export version, and relevant
configuration.

## 8. Main risks and controls

| Risk | Control |
|---|---|
| fparser2 rejects valid project source | Per-file visible fallback; never drop the file |
| AST loses comments or formatting | Raw-source overlay tied to exact node spans |
| Function calls are confused with arrays | Scope/type resolution plus explicit ambiguity diagnostics |
| Call resolution silently deletes observations | Keep immutable call-site observations and derive resolution indexes separately |
| Parser failures disappear during projection | Carry structured diagnostics through every model and report |
| Comparison preview validates degraded pages | Pass the rich store into preview and assert block-set parity with normal rendering |
| A hub-module edit creates an impractical release block | Keep explicit dependency fanout complete, report affected pages as advisory, and use a separate opt-in strict gate |
| Line links move or point to the wrong commit | Source-span tests and provenance-locked rendering tests |
| Tamandua breaks on model changes | Versioned snapshots and consumer contract tests before cutover |
| Parser output changes order between runs | Canonical identities, sorting, and byte-for-byte determinism tests |
| The old parser's bugs become required behavior | Record and review disagreements; prefer AST-proven behavior |
| Migration creates two permanent parsers | Defined cutover gates and a scheduled legacy-removal PR |
| Full parsing becomes too slow | Benchmarks, per-file caching, and no-change cache tests |
| Source spans invalidate reviewed pages | Freeze physical-slice hashing and compare all existing page hashes |
| Snapshot readers silently discard v2 fields | Enforce accepted formats and use an explicit export schema |

## 9. Definition of done

The migration is complete only when all statements below are true:

- fparser2 is the primary parsing engine.
- A single canonical rich model supports all consumers.
- No meaningful fact from the old rich parser is missing on the pinned source.
- Every accepted difference is documented and tested.
- All source files are represented, including fallback files.
- GitHub line links point to the correct lines at the correct commit.
- Call and control-flow graphs still work and remain clickable.
- Documentation status, grounding, and rendering checks pass.
- Schema and comparison outputs pass their release checks.
- Tamandua consumes the new snapshot successfully.
- Output is deterministic and provenance is complete.
- Performance is within the reviewed budget.
- The normal pipeline no longer depends on `FortranScanner`.
- Duplicate legacy project-wide parsing code has been removed; any supported
  fallback is narrow, visible, and independently tested.

## 10. Claude review request

Please review Revision 3 on branch `codex/fparser2-migration-plan-v2` before
implementation. Use the code on that branch as the baseline rather than GitHub
`main` at `db6423d`; the branch includes the current rich-primary documentation
pipeline and Mermaid graph support. Answer the following:

1. Is `ProjectIndex v2` the correct canonical boundary, or is another unified
   model cleaner?
2. Does the plan preserve the current Markdown, GitHub-link, Mermaid-graph,
   schema, comparison, and Tamandua capabilities?
3. Are any facts exposed by `FortranScanner`, `ProjectIndex`, `RichStore`, or
   `FactStore` missing from the parity matrix?
4. Is the AST-plus-raw-source-overlay design appropriate for comments, exact
   raw text, and line numbers?
5. Is fallback behavior visible and strong enough to guarantee that no file is
   silently lost?
6. Is the v1/v2 snapshot compatibility strategy safe for Tamandua?
7. Are the phase exit gates strong enough to prevent an early cutover?
8. Which phase or proposed data structure should change before coding begins?
9. Does the plan now preserve source-hash/staleness behavior, raw-text
   compatibility, collision lookup, outside-state references, and the schema
   reproducibility gate?
10. Are snapshot format enforcement, the explicit export schema, exact fparser
    pinning, and Phase 1 size/performance decisions sufficient for Tamandua?
11. Does Phase 0 now prevent `_resolve_calls()` from deleting call observations
    or call-site locations while still deriving resolved edges and `called_by`?
12. Do parse errors and fallback files now have complete model-to-CLI and
    comparison coverage?
13. Is the uncapped declared-dependency policy correctly separated from the
    capped heuristic data-flow policy, and is the advisory/strict `affected`
    gate split clear?
14. Does the comparison-preview requirement guarantee the same rich block set
    as normal rendering?

Return one of:

- **APPROVE**, with any non-blocking suggestions; or
- **REQUEST CHANGES**, listing the blocking changes required before Phase 0.
