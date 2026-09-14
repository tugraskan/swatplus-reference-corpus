# fparser2 Migration Plan

Status: **Phases 0 through 8 complete, except the legacy-scanner removal**.
The reference baseline and safety gates are implemented and verified; see
`reports/parser-baseline/VALIDATION.md`. Phase 1 has frozen the wire contract
and set the storage and size budgets (`reports/parser-baseline/BUDGETS.md`).
Phase 2 has frozen the shared source-text and physical-line contract. Phase 3
has built the AST extraction layer across all seven fact categories. Phase 4
has derived calls, call paths and shared state from the canonical index rather
than from a second parse. Phase 5 has closed the last unparseable file, so the
AST path now covers the whole pinned tree. Phase 6's field-level harness
reports **0 unexpected differences and 19 approved corrections** between the
two parsers, with no record missing in either direction.

Phase 7 has run every documentation consumer against the fparser2-produced
index: all 7 gates pass, and rendering from it changes 2 pages out of 1,095 --
both approved corrections reaching the docs.

Phase 8 has made fparser2 the default engine. The legacy scanner stays
selectable through `engine` under `[docs]` for one compatibility period and is
removed only after it -- deleting it now would drop the fallback in the same
change as the cutover.

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
  and therefore the rich `FortranScanner`. The fparser2 path supplies migration
  diagnostics and comparisons, not the main documentation facts.
- The Markdown renderer currently generates clickable Mermaid call graphs and
  control-flow outlines, and MkDocs is configured to render Mermaid. These are
  existing capabilities that must be preserved.
- Rich-store call resolution sets `CallRef.resolved`, exact internal target or
  candidate identities, `called_by`, maximal identity-based `call_paths`, and
  ambiguity review flags before the documentation projection.
- `RichStore.resolve_calls()` now preserves call observations and locations;
  both `build()` and `save()` resolve calls without relying on a docs projection.
- fparser2 `parse_errors` and `fallback_files` survive in rich metadata,
  `FactStore`, the CLI, comparison reports, and the Phase 0 baseline.
- Comparison preview rendering now receives the same rich store as normal
  rendering, with regression coverage for all rich page-block families.
- Dependency-derived `affected` pages are advisory under `--require-current`;
  `--fail-on-affected` provides the separate strict review gate.
- The pinned source currently exposes two known fparser2 failures:
  `gwflow_floodplain.f90` and `gwflow_heat.f90`, both involving the accepted
  `expr*-1` spelling.
- The reproducible v2 rich snapshot contains 2,312 exported call sites: 1,825
  explicit subroutine calls and 487 semantically proven function calls. Of
  these, 2,291 resolve to an internal procedure and 21 are unresolved explicit
  subroutine calls. The normalized LF byte size and SHA-256 are recorded in
  `reports/parser-baseline/main-cb442f7c05fc.json`.
- `ProjectIndex` keeps repeated source call sites and unresolved explicit
  subroutine calls. The compact `FactStore.Symbol.calls` list intentionally
  contains resolved internal graph edges only; intrinsic and external names do
  not become broken Markdown graph links or false affected-page dependencies.
- The three historically reported thin/rich disagreements are named in the
  regression list. Two were same-name/different-file type comparisons, not
  span errors; file-aware comparisons now agree. The floodplain argument-count
  disagreement remains real and visible.

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
   Broad regex `name(...)` candidates are not call observations until semantic
   resolution proves they are functions; unresolved candidates remain
   available during analysis but are excluded from the portable call export.
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

- Correct call resolution (now `RichStore.resolve_calls()`) so it does not delete the
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
  results. At the present pinned source it is zero errors and 3,869 warnings;
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
- Record the migration-only extra parse cost in `docs facts-diff`: a stale
  cache currently causes one rich scan and two fparser2 walks. Remove the
  redundant diagnostic walk when fparser2 becomes the canonical parser.
- Add a CI regeneration-freshness check so tracked snapshots, schema artifacts,
  and documented counts cannot silently remain one implementation commit behind.

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

Completion evidence (2026-09-02):

- The committed JSON baseline covers 31 fact categories and seven named
  real-source regression cases. Two independent full-source runs produced
  identical normalized facts, snapshot bytes, and provenance.
- All 1,092 reviewed hashes are unchanged. Corpus status is 1,095 filled pages
  with no drift; grounding reports zero errors and 3,869 existing warnings.
- The full test suite passed 310 tests. After the final diagnostic cache and
  snapshot-reprojection safeguards, all 71 relevant focused tests passed,
  including the three new cache cases.
- Normal rendering and strict MkDocs passed. The 1,100 rendered Markdown pages
  contain 44,442 GitHub line links with valid pinned-source file/range targets
  and 1,240 Mermaid blocks. Preview/normal rich-block equality is tested.
- Schema, range, and field-map regeneration leaves no tracked content diff.
- The snapshot retains both known fparser2 failures. Cached rich/compact
  diagnostics must agree; missing or inconsistent metadata triggers a rebuild.
- CI now verifies baseline/snapshot freshness. These gates passed locally;
  hosted CI has not been run for this change.

Post-review hardening (see `reports/parser-baseline/PHASE0_REVIEW.md`):

- `fparser` is pinned exactly, because its version string and syntax-error text
  are inside byte-compared artifacts. An unpinned resolve already selects 0.2.5.
- The call-observation gate compares SHA-256 identities of the ordered call
  sites at the raw scan, before resolution, and after, rather than comparing a
  count against itself.
- The source-link audit is committed as `swatref docs check-links` and runs in
  CI after rendering, instead of existing only as recorded evidence.
- Every named regression case must assert something; a case with no expectation
  is reported unverified.

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
  46.3 MB with normalized LF endings, so storage is a model-shape constraint
  rather than a late check.
- Set reviewed full-parse time, peak-memory, and no-change cache budgets from
  the Phase 0 measurements.

Exit gate:

- Current rich-parser output can be represented in v2 without losing facts.
- Existing documentation and schema tests still pass through the compatibility
  layer.
- A current reader rejects a deliberately unsupported snapshot version.
- Tamandua's v1 contract fixture passes before any v2 export is produced.
- The proposed v2 export fits the approved storage and performance budgets.

Progress (Phase 1):

- Snapshot loading already enforced an allowlist of envelope formats; loading
  now also allowlists the field-level export schema and requires one from
  format 2 onward, so an unknown contract is refused rather than half-read.
- `tests/contracts/` holds checked-in v1, v2, and v3 fixtures. V2 remains the
  original allowlisted export; the structured Phase 1 fields moved to v3 rather
  than changing that contract in place. The current v3 export is frozen byte
  for byte against a rebuild from the demo sources, so any wire change is a
  reviewed diff. The v1 fixture reproduces the pre-v2 producer, including the
  unresolved function candidates later contracts filter.
- The v1-to-v3 path is compatibility *and* a documented limit: a v1 snapshot
  loads and re-saves as a valid v3 envelope, but fields v1 never recorded stay
  null. A complete v3 requires re-scanning the pinned source, not converting.
- Assignments are the first structured record: `target`, `target_root` and
  `expression` sit alongside the existing `kind`, `summary`, `raw` and
  `location`, so existing consumers are unaffected. This removed three separate
  re-parses of `raw`, including the renderer recovering a target by stripping
  the `Sets ` prefix off a human-readable summary.
- Storage decided and budgets set in `BUDGETS.md`: the snapshot stays plain
  JSON because git already absorbs it (three versions cost under 6 MiB of
  pack). The 64 MiB size budget is enforced by `baseline_failures()`, not just
  documented. The snapshot is 46.7 MiB after the assignment fields.

- Every named record (module, program, procedure, derived type) carries a
  stable `identity` of `kind:name:file[:scope]`. Bare names collide in SWAT+ --
  a type and a procedure share `salt_balance`, and same-named types live in
  different modules, while contained declarations can repeat within one file --
  so a name and file alone cannot address every record. `FactStore.add()` keys and
  `RichStore.get_of_kind()`'s fail-closed lookup are untouched, and the baseline
  reuses the same formula so its owner strings and a record's identity join.
  Identity is derived from scope data when the source contract carries it.
  Converted historical snapshots get the most specific identity their recorded
  module/parent fields allow; a complete scope-aware identity requires a v3 scan.
- The pinned fparser version travels with the diagnostics it produced and is
  part of the cache identity, so a cache built by a different fparser is
  rebuilt instead of silently reused.

- Control steps carry their block nesting, so the flat source-order outline is
  now a walkable tree: `block_id` identifies a construct, `parent_id` the
  construct enclosing a statement, `branch_of` ties an `else`/`else if`/`case`
  arm to its construct, and an opener records the `end_line` that closes it.
  The convention that was previously undecided is settled and tested: a
  construct sits at the depth it opens at, its body one deeper, and its arms at
  the construct's own depth rather than inside it. Only `if ... then`, `do` and
  `select case` are tracked, which a survey of the pinned source shows are the
  only block constructs it contains.
- Both valid spellings of an else-if arm, `else if` and `elseif`, are included
  in that tree. Pointer association (`=>`) is also distinguished from ordinary
  assignment (`=`), so the exported right-hand expression no longer begins
  with a spurious `>`.

Phase 1 deliverables are complete. The remaining plan items belong to Phase 2
and later.

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

Progress (Phase 2):

- `parser/source_text.py` is the one source/location layer. The quote-aware
  comment scanner, the continuation joiner, the statement splitter and the
  doc-comment helpers live there, and `schema_fortran` re-exports them so
  existing importers are unaffected.
- Seven bare `!` splits across `fortran.py`, `documentation.py` and `refs.py`
  are gone. Each truncated any line whose string literal contained a `!`; the
  pinned source has two such lines, both in `output_path_module.f90`.
- A blank or comment-only line inside a continuation used to terminate the
  join and emit a truncated statement. Five statements in the pinned source
  were affected; `regres.f90`'s `bcod` declaration, for instance, ended at
  `real , dimension(5,3) :: bcod =` and now carries its full `reshape(...)`
  initializer.
- Statements separated by `;` are now split. 255 lines carried 680 statements
  that the model never saw, including `case ('ncell'); read(code_val,*) ncell`,
  where the read was invisible to the I/O layer entirely. This recovered 263
  assignments, 244 control steps and 22 I/O operations.
- `tests/test_source_layer.py` freezes the contract case by case: comments
  containing punctuation and quotes, statement separators inside literals,
  every continuation form, whitespace and case handling, closed-up `end`
  spellings, physical spans against `hash_slice`, and byte-exact
  `IOOperation.raw`/`fields`/`condition` and `ControlStep.raw`/`summary`.
- The parser identity initially advanced to `fortran-scanner-v3`. That forced
  existing caches to rebuild instead of silently reusing pre-Phase-2 results
  that lacked the recovered statements.
- `call_observations` is the one baseline count that went *down*, 56,507 to
  56,506. The lost record is `reshape` at `regres.f90:49`. Before the
  continuation fix, the truncated tail of the `bcod` declaration stood as its
  own statement and `_collect_function_calls` recorded a `reshape` candidate
  from it; now that tail is part of a declaration, and declarations are not
  scanned for calls. The decrease is a removed false positive, not a lost
  observation. `unresolved_function_candidates` moves by the same one.

Phase 2 review follow-ups (post-`9db720c`):

- `inline_doc_from_raw` was the one helper in the layer still splitting each
  physical line independently, so a `!` inside a continued character literal
  became documentation and a real comment after that literal closed was
  dropped. It now carries the quote state the way `logical_lines` does, and
  skips whole-line comments explicitly so the two agree on what a comment is.
  Both directions are pinned in `tests/test_source_layer.py`. No record in the
  pinned source is affected: a scan of all 648 files found zero statements
  where the stateful and stateless readings differ, and the tracked baseline
  and snapshot still verify byte for byte. The parser identity advances to
  `fortran-scanner-v4` because behavior changes for source trees containing the
  pattern; this prevents a pre-fix `v3` cache from being silently reused even
  though the pinned corpus is byte-neutral.
- The `if continuing and not stripped.strip()` branch was unreachable -- the
  skip above it already consumes every blank and comment-only physical line
  while continuing -- and has been removed, with its explanation folded into
  the live skip.
- `!$` is deliberately *not* special-cased in the continuation skip. fparser2,
  the migration target, treats `!$` as a comment and resumes the continuation
  at the next code line; the source layer produces the identical statement for
  the same input. `schema_fortran`'s `!$` exclusion answers a different
  question -- whether the line is documentation prose -- and the two are
  consistent, not in conflict. A regression test pins the valid form with a
  following code line so a dangling continuation is not mistaken for sentinel
  behavior.

Exit gate results: all 1,092 reviewed page hashes unchanged and the page
identity hash stable; grounding unchanged at zero errors and 3,869 warnings
with a stable identity hash; the released schema artifact rebuilds byte for
byte, verified against both the current and the statement-split parse before
the change was adopted.

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

Progress (Phase 3, categories 1-3):

- `parser/ast_index.py` is the AST extraction layer. It inverts the split the
  Phase 4 pipeline calls for: fparser2 answers *what owns this statement and
  where does this scope end*, and the Phase 2 source layer answers *what does
  it say*. Every consumer-visible string still comes from the physical source.
  `str(node)` is used nowhere -- fparser2 re-prints `real :: mv = 1.` as
  `REAL :: mv = 1.`, and the schema resolver matches on those bytes, so
  printing the node would silently rewrite the frozen Phase 2 contract.
- Categories 1-3 are complete and at byte-exact parity with the rich scanner on
  the pinned tree: 66 of 66 modules, 514 of 514 derived types and 732 of 732
  reachable procedures agree on every compared field -- `args`, `variables`,
  `components`, `uses`, `module`, `parent` and `doc` -- comparing full
  `VariableRef` and `UseRef` tuples including declaration text, initial value,
  documentation and location, not just counts.
- The only inventory difference is the two procedures in `gwflow_floodplain.f90`
  and `gwflow_heat.f90`. fparser2 rejects both files over the `expr*-1`
  spelling; they are the pinned tree's two documented fallback cases, and the
  AST path now records an `ast_parse_failed` diagnostic for each and keeps the
  file in the inventory rather than dropping it. Wiring the fallback back in is
  Phase 5's deliverable, not a Phase 3 gap.
- Structure now comes from the parse tree rather than from regex plus stacks,
  which closes several classes of misreading by construction: a derived type's
  components arrive as `Data_Component_Def_Stmt` and a scope's variables as
  `Type_Declaration_Stmt`, so the `type_stack` that kept them apart is gone;
  procedure-local derived types and contained procedures get their true scope;
  and an `end` statement supplies a scope's real end line.
- Two readings that only an AST can distinguish are pinned by regression tests
  even though the pinned corpus does not exercise them. `type(box) function
  make(x)` declares `make`: taking the first `Name` in the statement -- what a
  walk over the node returns -- yields `box`, the result type, and names the
  procedure after it (`parser/fortran.py`'s thin path still reads it that way;
  the pinned tree contains no typed function, so the defect is latent there).
  And an interface body's dummy-argument declarations belong to the procedure
  it describes, not to the enclosing module: fparser2 models the body as a
  `Subroutine_Body`, which is not a subprogram, so ownership stops at the
  `Interface_Block` instead of walking on. The pinned tree's 89 interface
  blocks are all `interface operator (...)` wrapping only `module procedure`
  statements, so nothing leaks there today.
- `_collect_doc_blocks` moved to a module-level `collect_doc_blocks` in
  `schema_fortran` so both paths share one definition of a documentation
  comment. The move is behavior-neutral; the scanner method now delegates.
- One unreviewed declaration was reported rather than guessed, and has since
  been corrected. At `utils.f90:222`, `character(len=len(str)) :: lower` was
  dropped by *both* parsers, because the shared `DECL_RE` matched a character
  length with `[^)]*`, which cannot span the nested parentheses of
  `len=len(str)`. The rich scanner had always lost this variable silently; the
  AST path knew a declaration was there and emitted
  `ast_declaration_unreadable`, which is what surfaced it. The approved fix is
  recorded under "Approved correction: nested character length" below.
- No consumer is wired to the AST path yet. `get_store()` still runs the rich
  scanner, and the layer is additive: all 1,095 pages, the grounding run (0
  errors, 3,869 warnings), the Phase 0 baseline, the rich snapshot and the
  released schema artifact all rebuild byte for byte, and the 44,596 rendered
  source links still resolve.

Progress (Phase 3, categories 4-7):

- The executable pass walks the file's statements in source order. A statement
  is any node fparser2 gives its own source item, which is exactly one node per
  statement and in source order, so the AST and the Phase 2 source layer
  enumerate the same statements and pair one for one -- including both halves of
  `case ('ncell'); read(code_val,*) ncell`. Source order is not cosmetic: string
  defaults picked up from declarations and earlier assignments are what a later
  `open (107, file=in_aqu%aqu)` resolves against.
- Select-case vocabularies match exactly: all 732 procedures agree on every
  subject and literal label. Assignments, calls, control steps and I/O match
  exactly except in the cases below, each of which is the AST reading a
  statement the scanner's anchored patterns cannot reach. **Nothing is lost in
  either direction that was not a false positive.**
- **63 assignments recovered.** 56 have a target whose own subscript contains
  parentheses -- `gw_chan_info(channel)%cells(gw_chan_info(channel)%ncon) =
  gw_chan_cell(i)` -- and `ASSIGN_RE`'s `\([^()]*\)` subscript group stops at
  the first inner `)`, so the statement failed to match at all and the
  assignment was dropped rather than mis-split. 6 more carry a leading statement
  label, and 1 combines both. These are exactly the "full component paths"
  category 4 asks for. `source_text.split_assignment` replaces the pattern: it
  splits at the first `=` or `=>` at paren depth zero outside any literal. It
  finds the split point and does not decide the grammar -- it is called only for
  a node fparser2 already parsed as an assignment -- which is what lets the
  split stay purely textual and therefore byte-exact.
- **2 false function-call candidates dropped**, both at `utils.f90:222`. Because
  `parse_declaration` cannot read `character(len=len(str)) :: lower`, the
  scanner falls through to its executable handling and records `character(` and
  `len(` as function references. The AST knows the statement is a declaration
  and never reaches that path. This is the same class of removal as Phase 2's
  `reshape` at `regres.f90:49`.
- **2 labelled statements read.** Fortran lets any statement carry a numeric
  label, and every scanner pattern that anchors on the statement keyword fails
  on the labelled spelling. `carbon_layers_read.f90:48` is `99 close (107)`,
  which the scanner does not see as I/O at all; the AST records it and resolves
  it to `carbon_layers.prt` through the unit its `open` bound.
  `gwflow_pond.f90:360` is `10  enddo`, which the scanner does not see as a
  block close, so the loop it ends stays open and swallows the enclosing
  construct's `end if`. The consequences were real: across the whole pinned tree
  the scanner leaves exactly one block opener unclosed -- the `if` at
  `gwflow_pond.f90:53`, reported with no end line at all -- and records every
  statement after line 363 in that procedure one level too deep, with the loop
  at line 65 ending at 418 instead of 360. The AST leaves nothing unclosed
  anywhere. `source_text.split_statement_label` peels the label off before a
  keyword-anchored helper sees it; `raw` keeps the statement exactly as written,
  label included, because the label is source text.
- Function-reference candidates deliberately remain a text pattern. Without
  semantic analysis fparser2 parses `a(i)` and `f(i)` into the same `Part_Ref`,
  so the AST cannot separate an array element from a function call either. Plan
  decision 7 settles the policy: these stay observations until semantic
  resolution proves which are functions, and none may be discarded meanwhile
  because their locations are evidence.
- Four more scanner internals became shared module-level functions so both paths
  produce identical bytes rather than re-deriving the rules: `summarize_step`,
  `resolve_file_expression`, `resolve_project_file_expressions`, and
  `string_literal`/`derived_type_name`. Each move is behavior-neutral and the
  scanner methods delegate. Cross-file filename resolution in particular is what
  turns a symbolic `in_aqu%aqu` into `aquifer.aqu`; running it closed 112 of the
  113 I/O differences that remained before it was wired in.
- One trap is worth recording because it is invisible until it bites. fparser2
  builds some node classes dynamically, so an `Open_Stmt` instance is a subclass
  carrying the same `__name__` as `f03.Open_Stmt` without being that class. A
  dict keyed on `type(node)` silently misses exactly those, while an `isinstance`
  check on the same node succeeds -- which showed up as I/O operations being
  recorded while their control steps went missing. All classification is
  `isinstance`-based for this reason.

Exit gate results (Phase 3): all seven categories implemented with unit and
fixture tests per category; every AST fact carries a location, and the three
diagnostics that remain on the pinned tree are accounted for exactly -- two
files fparser2 rejects and one declaration the shared pattern cannot read. No
consumer is wired to the AST path, and all 1,095 pages, the grounding run (0
errors, 3,869 warnings), the Phase 0 baseline, the rich snapshot and the
released schema artifact rebuild byte for byte, with all 44,596 rendered source
links still resolving.

Phase 3 review follow-ups (post-`05cde36`):

- AST statements now bind to source-layer statements once per file and reuse
  that map in every fact pass. Declarations and `use` statements after a
  semicolon therefore keep their own text instead of repeatedly binding to the
  first statement on the physical line; an unpaired AST statement produces an
  `ast_source_unmapped` diagnostic rather than disappearing.
- The AST reader and source layer select fixed form for `.f`, `.for`, `.ftn`
  and `.f77`. Fixed-form labels, continuation columns, comments, raw spans and
  the 72-column statement field have dedicated regression coverage.
- Legacy label-terminated `do` constructs close at their shared terminal
  statement, including nested loops sharing one label. Any block still open at
  scope exit now produces `ast_unclosed_block`.
- Non-`only` `use` renames are preserved separately from the unrestricted
  import set and participate in outside-state resolution. The new internal
  field is deliberately excluded from the frozen rich-v3 export until the
  planned snapshot-contract change.
- The full suite passes 454 tests with 23 expected skips, and all 14 pinned-tree
  AST/rich parity tests still pass unchanged.

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

Phase 4 slice 1 -- scope-aware call resolution:

- `resolve_project_calls()` now operates on the canonical `ProjectIndex`, so
  scanner- and AST-built indexes use one semantic implementation. Resolution
  proceeds through lexical internal procedures, same-module definitions,
  `use`-associated definitions, and external definitions; the first non-empty
  visibility tier wins, and procedure kind must match the call kind.
- `only` lists, local renames, non-`only` renames, module host association and
  procedure host association participate in lookup. Type-bound calls remain
  unresolved until the derived-type/component slice can resolve them safely.
- Every `CallRef` retains its observed spelling, raw statement, ordering and
  location. Exact target identity and all equally-visible candidate identities
  are attached as internal semantic fields while rich-v3 stays frozen. An
  ambiguity fails closed and emits an idempotent `ambiguous_call` review flag.
- On the pinned main source, all 56,506 ordered call observations retain the
  existing identity hash. The semantic result also retains 2,291 resolved call
  sites and 778 reverse edges, with no ambiguities on that tree. The focused
  suite passes 33 tests and the full available suite passes 450 tests with 37
  expected skips; pinned-source facts were additionally exercised directly
  from the canonical checkout because this worktree has no local `external/`
  fixture link.

Phase 4 slice 2 -- deterministic call paths:

- Every procedure now records all maximal paths through exact resolved target
  identities. A path includes its root and ends at a leaf or at one cycle-closing
  repeated identity; unresolved and ambiguous calls never create graph edges.
- Adjacency collapses repeated call sites only for path traversal. The ordered
  `CallRef` observations, including duplicate locations, remain unchanged and
  are still the source evidence behind every edge.
- Paths and adjacency are identity-sorted, rebuilt idempotently after call
  resolution, and exercised for branching, merge points, recursion, mutual
  recursion, repeated observations, unresolved calls, and ambiguity.
- The parser/cache identity advances to `fortran-scanner-v5`. The reviewed
  snapshot delta also preserves 116 call-name spellings exactly as written;
  those were previously lowercased as a side effect of resolution. Baseline
  observation grouping remains case-insensitive because Fortran names are.
- On pinned main, the result is 16,671 maximal paths across 198 procedures; the
  longest path contains 12 procedure identities and no cycle occurs in that
  source revision. Resolution takes about 1.4 seconds in the direct semantic
  measurement. The regenerated rich snapshot is 58,690,186 bytes, below the
  64 MiB raw-size gate.
- Enumerating every maximal simple path is worst-case exponential, and nothing
  caps path count, length or recursion depth, so the size gate is the only
  backstop and it fails the build rather than degrading. The cost is also highly
  concentrated: 536 of 734 procedures contribute no path at all, while
  `calsoft_control` and `calsoft_hyd_bfr` together produce 50.3% of them. **This
  risk is accepted for now and deliberately left uncapped**; the measurements,
  the revisit triggers, and the two fallback representations are recorded under
  "Accepted risk: call-path growth is not bounded by the model" in
  `reports/parser-baseline/BUDGETS.md`.
- The official write/read-back baseline gate passes. The complete unit and
  pinned-source suite passes 469 tests with 23 expected skips; documentation
  status remains 1,095 filled with no stale, affected or missing pages,
  grounding remains at 0 errors and 3,869 established warnings, and the strict
  MkDocs build passes.

Phase 4 slice 3 -- shared state derived from the index:

- `annotate_project_dataflow()` derives each procedure's `reads`/`writes` from
  the records the parser already produced -- assignment targets and expressions,
  and the statement text on control steps, calls and I/O operations. It reads
  nothing from disk. Both the thin `fortran.py` path and the rich projection
  previously re-opened every source file and re-classified its physical lines,
  which is the second parse decision 2 rules out; the documentation projection
  now copies the derived facts instead, and its private classifier is gone.
- `ProcedureDoc` and `ProgramDoc` carry `reads`/`writes`, listed as
  intentionally internal so the frozen rich-v3 wire shape does not grow. The
  regenerated snapshot is byte-identical, which confirms the guard.
- Deriving from statements rather than physical lines removes four classes of
  false positive that a line-by-line reading cannot avoid, and recovers reads
  that it lost:
  - a `use m, only: hru` import counted `hru` as a read, though an import reads
    nothing. This was the largest class;
  - a `format` statement counted the identifiers inside its quoted literals, so
    `100 format (1x,'   hru','   day')` read `hru` and `day`;
  - `a = 0; b = 0; c = 0` matched one assignment per physical line and counted
    the remainder as its right-hand side, so `b` and `c` were recorded as reads
    of the variables they actually write;
  - a host procedure's line span covers the procedures it contains, so it
    absorbed their state access; the contained procedure is its own documented
    symbol and the access belongs there; and
  - a continued statement was classified one fragment at a time, so the joined
    statement now contributes reads the fragments lost.
- Net effect on pinned main: 38 false reads removed, 62 genuine reads recovered,
  4 writes recovered. `dataflow_reads` moves 5,440 -> 5,464 and `dataflow_writes`
  2,935 -> 2,939; the heuristic dataflow graph moves 1,273 -> 1,306 applied edges
  and 3,841 -> 3,860 candidates, with `wet_initial` appearing as a documented
  source for the first time and the big orchestrators (`time_control`,
  `time_read`, `proc_bsn`) shedding their `use`-import false positives. The
  Phase 0 baseline is regenerated for exactly these fields; no page hash, call
  observation, symbol count or schema fact changes, and `docs status` stays at
  1,095 filled with no stale or affected pages.
- Because the derivation consumes records rather than source text, the AST path
  gets it with no reimplementation. On pinned main the two parsers agree on
  shared state for 731 of 732 shared procedures. The one difference is
  `salt_chem_soil_single`, whose `10    upion1 = Sul_Conc(salt_c4)` carries a
  statement label: the scanner's assignment pattern cannot match past the label,
  so it never records the write and reports `upion1` as a read instead. That is
  the Phase 3 labelled-statement finding surfacing in a second fact family, and
  the AST reading is the correct one.
- `fortran.py`'s `annotate_dataflow` is deliberately left in place. It serves
  the thin `thin-v1` fparser2 diagnostic store, not the documentation
  projection, and it is removed with the rest of that path in Phase 8.

Phase 4 slice 4 -- I/O and output-family aggregation shared:

- `populate_io_summaries()` is module-level, so the AST path closes out a scan
  the way the scanner does. Until now it produced no `io_files` and no
  `output_families` at all, which meant its index could not stand in for the
  scanner's however well the per-procedure facts matched.
- On pinned main both paths now build 1,028 I/O files and 23 output families
  from the same keys, with 1,025 of the 1,028 identical operation-for-operation
  and all 23 families identical. The three that differ are the two labelled
  statements Phase 3 already documented: `carbon_layers_read.f90`'s
  `99 close (107)`, which the scanner does not recognise as I/O at all, and
  `gwflow_pond.f90`, whose condition trail drifts from the labelled `enddo` it
  never closes. No new class of difference appears.
- The function reads no source; it aggregates the completed index. Nothing in
  the tracked artifacts moves.

Phase 4 slice 5 -- outside-state references stop reading quoted text:

- `refs._code()` stripped comments and single-quoted literals before scanning a
  line for module-state references, but not double-quoted ones. A name inside a
  message or a `case ("res")` label was therefore reported as a reference to the
  module state of the same name: `write (2612,*) j, " FERT-WET"` referenced
  `fert` and `wet`, and `1234 format(..." Time",...)` referenced `time`.
- The fix is a quote-aware `source_text.strip_string_literals()`, not a second
  substitution. A literal ends only at its own kind of quote, so one
  left-to-right scan is what gets that right; running an `'...'` pattern over
  `x = "don't" // 'y'` pairs the apostrophe inside the double-quoted literal
  with the opening quote of `'y'` and eats the text between them, leaving
  `x = "dony'`. That misreading is present today and the fix removes it too.
- 78 candidate references disappear across 40 procedures and none appear.
  `outside_state_refs` moves 21,601 -> 21,523 and the snapshot shrinks by 31,049
  bytes. The removed entries are bare names harvested from quoted text --
  `FERT`, `WET`, `res`, `aqu`, `ru` -- while the genuine subscripted references
  on the same lines are separate entries and are kept, which is why nothing is
  added. The change is confined to the
  `swatplus_reference_outside_state_refs` metadata family; no page hash, call
  observation, dataflow fact or schema artifact moves, and `docs status` stays
  at 1,095 filled with nothing stale or affected.
- The second parse behind these candidates is untouched: `candidate_outside_refs`
  still re-reads the source and scans physical lines. Deriving them from the
  index instead would change roughly 1,050 entries -- overwhelmingly `use`-line
  and `format`-statement artifacts -- and is deferred rather than bundled with
  this defect fix.

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

Phase 5 slice 1 -- lexical normalization closes the corpus gap:

- `gwflow_floodplain.f90` and `gwflow_heat.f90` spell a negation as `expr*-1`.
  Two operators in a row is not valid Fortran; gfortran accepts it and fparser2
  rejected the whole file, which is why the AST path produced no facts for
  either. `source_text.normalize_nonstandard_signs()` parenthesises the signed
  operand in the text handed to fparser2 only. `a * -b` and `a * (-b)` denote
  the same value for `*` and `/`, so this is a rewrite of spelling, not meaning.
- The pinned tree now has **no unparseable file**. The AST index reports 734
  procedures against the scanner's 734, with no rich-only and no ast-only
  entries, and `ast_parse_failed` no longer occurs. The two files carry an
  `ast_input_normalized` diagnostic at `info` severity naming the exact lines
  rewritten: `gwflow_floodplain.f90:86` and `gwflow_heat.f90:61,62,104,105`.
- **The two newly parsed files introduce no new disagreement.** After the
  change, the categories that still differ are exactly the ones already
  documented -- 10 files of assignments, `utils.f90`'s two false call
  candidates, and the labelled statements in `carbon_layers_read.f90`,
  `gwflow_pond.f90` and `salt_chem_soil_single.f90`. Their spans, variables,
  uses and args match the scanner exactly.
- The plan's constraint holds and is tested: every raw string, span and hash
  still comes from the unchanged source. `raw` on the rewritten lines reads
  `if((Q*-1) >= gw_state(cell_id)%stor) then`, not the parenthesised form the
  parser saw. Line count is preserved, so physical spans stay valid.
- The rewrite is deliberately narrow, and each exclusion is a correctness
  requirement rather than caution:
  - `**` is excluded. Exponentiation is right-associative and unary minus binds
    looser than it, so `a ** -b ** c` means `a ** (-(b ** c))`; wrapping the
    operand would give `a ** ((-b) ** c)` and silently change the value.
  - `//` is excluded because it concatenates strings.
  - The operand must be a bare name or number: `a * -b(i)` is left alone
    because the parenthesis belongs around the whole reference, and wrapping
    the name alone would produce `a * (-b)(i)`.
  - Comments and character literals are untouched, including a literal that
    spans a continuation.
  Anything unmatched is left for the parser to reject, so a file it still
  cannot read degrades visibly instead of being quietly half-repaired. The
  degradation path is now tested with `q = q*-b(1)`, which is outside the
  scope by design.
- `fortran.py`'s thin diagnostic path is unchanged and still records both files
  as fparser fallbacks, so the regression cases in
  `reports/parser-baseline/regression-cases.json` continue to hold and no
  tracked artifact moves.

Still open in Phase 5: a raw-source fallback for files that cannot be parsed at
all. The pinned corpus no longer contains one, so such code would have nothing
in the corpus to exercise it; whether to build it on principle is a decision
rather than a gap.

Approved correction: nested character length
--------------------------------------------

`DECL_RE` matched a character length selector with `[^)]*`, which stops at the
first inner `)`. `character(len=len(str)) :: lower` therefore failed to match at
all and the variable was dropped outright rather than mis-read. The `character`
branch now spans one level of nesting; `type(...)` and `class(...)` take a bare
type name and are unchanged.

A sweep of both configured source trees finds exactly one declaration newly
parsed in each, and it is the same line -- `utils.f90:222` -- so the correction
is as narrow as the diagnostic said it was.

The effect on the tracked baseline reconciles exactly to "+1 variable, -2 false
calls":

| Fact | Before | After |
|---|---|---|
| `locals` | 6,341 | 6,342 |
| `variables_and_components` | 15,936 | 15,937 |
| `call_observations` | 56,506 | 56,504 |
| `unresolved_function_candidates` | 54,194 | 54,192 |
| `repeated_sites` | 48,810 | 48,809 |
| `locations` | 137,058 | 137,057 |

The two lost calls are `character(` and `len(`, which the scanner recorded as
function references only because it fell through to executable handling on a
declaration it could not read. Recovering the declaration removes them from
both paths, so the AST and scanner call lists now agree exactly and the
`CALL_CANDIDATES_DROPPED` parity exception is retired.

No page goes stale: `source_hash` covers the Fortran source slice, which is
unchanged. `docs status` stays at 1,095 filled with nothing stale or affected,
grounding stays at 0 errors and 3,869 warnings, the released schema artifact
rebuilds byte for byte, and all 44,596 rendered source links still resolve.

Two levels of nesting are still beyond the pattern --
`character(len=max(len(a),len(b)))` -- as are `complex` and `procedure(...)`
declarations, none of which occur in either configured tree. The
`ast_declaration_unreadable` diagnostic stays in place to surface them if a
future source tree introduces one, and is tested with the two-level form.

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

Progress (Phase 6):

- `parser/parity.py` compares the two completed indexes field by field and
  sorts every difference into one of three buckets: an **approved correction**
  the project has examined and accepted, an **unexpected difference** that fails
  the harness, or agreement. `swatref docs parity` runs it, writes the report to
  `reports/parser-baseline/parity-main-cb442f7c05fc.json`, and exits non-zero on
  anything unexpected; CI runs it next to the baseline verification.
- Result on pinned main: **0 unexpected differences, 19 approved corrections,
  and no record found by one parser and missed by the other in either
  direction.** Modules 66/66 identical, types 514/514, output families 23/23,
  procedures 722 of 734 fully identical, I/O files 1,025 of 1,028.
- The remaining differences are the ones this plan already documents, and they
  are *listed* rather than normalised away, which is what the exit gate asks
  for: assignments in 10 files (nested-paren targets and statement labels),
  control steps and I/O in `carbon_layers_read.f90` and `gwflow_pond.f90`
  (labelled statements), shared state in `salt_chem_soil_single.f90` (a labelled
  assignment), and the three I/O files downstream of those.
- Only two things are normalised, and both are properties of Fortran rather than
  of a parser: the **order** of a collection, and the **case** of a name. Every
  byte-sensitive contract the plan names -- raw statements, I/O fields,
  conditions, summaries, source spans and hashes -- is compared verbatim, and a
  test tampers with each of them in turn to prove a whitespace-only change still
  fails.
- Approval is scoped to a category, a field **and** an owning file, never a
  blanket exemption, so a new difference in a file that is not listed still
  fails. A further test asserts that no declared correction has gone stale: a
  correction whose files no longer differ would be an exemption nobody needs,
  quietly covering a future regression in that file.
- The harness is tested for going red, not only for passing. Tampering with a
  summary, deleting a record on either side, and mutating each byte-sensitive
  field all fail it. A parity harness that cannot fail is worse than none,
  because it reads as evidence.

Phase 6 exit gate: no meaningful rich fact is missing, every disagreement has a
regression test and a recorded resolution, and the AST-proven corrections are
recorded as intentional improvements rather than hidden by normalization.

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

Progress (Phase 7):

- `RichStore.build(source_dir, engine=...)` selects which parser produces the
  raw index; `RichStore.from_index()` holds the enrichment both share. That
  sharing is what makes the gate meaningful -- running the consumers on the
  fparser2 index only proves something if the index travels the same path the
  scanner's does. The scanner stays the default; Phase 8 flips it.
- `swatref docs verify-consumers` builds the facts with the AST engine and then
  drives the **real** consumer code -- projection, staleness, rendering,
  grounding and the source-link audit -- rather than re-implementing their
  checks. CI runs it beside the parity harness.
- **All 7 consumer gates pass on the fparser2 index**: 1,310 projected symbols
  (scanner: 1,310); grounding 0 errors and 3,869 warnings, matching the scanner
  baseline exactly; page status unchanged at 1,095 filled with nothing stale,
  affected, orphaned or missing; every page renders; 0 invalid targets across
  44,599 source links; and every rendered link carries the pinned commit
  `cb442f7c05fc`.
- Rendering from the AST facts and diffing against the scanner's render leaves
  **2 pages different out of 1,095**, and both are approved corrections
  reaching the documentation: `carbon_layers_read.md` gains the recovered
  `99 close (107)` as an `io` node in its control-flow graph, and
  `gwflow_pond.md`'s I/O table loses a phantom nesting level from every
  condition trail -- the scanner reported
  `... > do r=1,gw_npond > if(gwflag_flux == 1) then` because its stack never
  popped the labelled `enddo`.

Phase 7 found a real defect, which is what running the consumers is for:
the declaration correction changed scanner behaviour **without advancing
`RICH_PARSER_VERSION`**, so `get_store()` kept serving a pre-fix cache and the
rendered `to_lower` page still lacked `lower` even after the fix. The test
suite could not see it -- tests build stores directly and never consult the
cache. The identity now advances to `fortran-scanner-v6`, which forces the
rebuild, and the checked-in contract fixture and its version tripwire are
updated as the reviewed diff the contract tests demand. This is the rule Phase
2 established, applied late: a behaviour change has to advance the identity or
a stale cache is reused in silence.

Phase 7 exit gate: all consumers pass against the fparser2-produced index
without invoking the legacy scanner. The scanner is still built alongside it in
`verify-consumers`, but only to produce the comparison baseline; every gate
above is evaluated on the AST index.

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

Progress (Phase 8, steps 1-5 -- the cutover):

- **fparser2 is the default engine.** `DEFAULT_ENGINE` is the single place the
  switch happens, and `RichStore.build`, `RichStore.from_index` and
  `parse_documentation` all read it. A test asserts they agree, because two
  defaults out of sync is how a cutover looks finished while half the pipeline
  still runs the old parser -- which is exactly what happened here: the baseline
  kept reporting `fortran-scanner-v6` because `parse_documentation` still
  defaulted to the scanner, and the give-away was a baseline that came back
  byte-identical when it should have moved.
- **The parser identity now names the engine**: `fparser-ast-v1` or
  `fortran-scanner-v6`. `has_current_contract(engine)` compares against the
  engine asked about, so a cache built by one is rebuilt rather than reused when
  the other is configured.
- **The scanner stays selectable** for the compatibility period: `engine` under
  `[docs]` in `swatref.toml`, defaulting to `fparser2`.
- Every number the cutover moves reconciles to an approved correction:

  | Baseline fact | scanner | fparser2 | why |
  |---|---|---|---|
  | `assignments` | 21,770 | 21,833 | +63 nested-paren and labelled targets |
  | `control_steps` | 23,914 | 23,915 | +1 `99 close (107)` |
  | `io_operations` | 7,101 | 7,102 | the same labelled close |
  | `dataflow_reads` | 5,464 | 5,463 | `upion1` is a write, not a read |
  | `dataflow_writes` | 2,939 | 2,940 | the same labelled assignment |
  | `locations` | 137,057 | 137,125 | +68, one per recovered fact |
  | `review_flags` | 0 | 2 | the two `ast_input_normalized` notices |
  | heuristic dataflow edges | 1,306 | 1,304 | see below |

- The two lost dataflow edges are traced, not waved through.
  `salt_chem_soil_single` now writes `upion1` instead of reading it, and both
  `salt_chem_aqu` and `salt_chem_hru` write `upion1`, so each loses its
  heuristic writer -> reader edge to it. One approved correction, two edges.
- Gates under the cutover: 549 tests pass; grounding unchanged at 0 errors and
  3,869 warnings; `docs status` unchanged at 1,095 filled with nothing stale or
  affected; the released schema artifact rebuilds byte for byte; 0 invalid
  targets across 44,599 source links; the parity harness reports 0 unexpected
  differences; all 7 consumer gates pass.

**Step 6 is deliberately not done.** Removing the legacy scanner is gated on
the compatibility period elapsing, and doing it now would delete the fallback in
the same change as the cutover -- the one combination this plan warns against.
`FortranScanner` therefore remains, reachable only through the documented
`engine` setting, and Phase 8's exit gate ("one normal parsing path, one shared
model, one raw-source utility layer, one documented fallback path") is met for
the normal path while the legacy engine is retired on its own schedule.

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
