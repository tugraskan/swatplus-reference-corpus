# Phase 0 reference baseline

Phase 0 is complete locally. See `VALIDATION.md` for the measured exit-gate
results and the scope of verification.

Run `swatref docs baseline` to verify the pinned reference. It performs fresh
fparser2 and rich parses, validates the report against `baseline.schema.json`,
checks the Phase 0 invariants, and compares both the report and newly generated
portable snapshot with the tracked files. Candidate output stays under ignored
`.swatref/parser-baseline/`; a failed check never overwrites reviewed artifacts.

For an intentional update, use `swatref docs baseline --write` and review the
diff. Even `--write` refuses changed reviewed-page source hashes, hard page
drift, grounding errors, missing regression cases, or lost diagnostics.

## What is frozen

- `main-cb442f7c05fc.json` records counts and stable identity/value fingerprints
  for 31 fact categories: source inventory and relationships, symbols, physical
  locations, declarations and comments, arguments and locals, uses, calls and
  reverse edges, assignments, control flow, select vocabularies, I/O, project
  summaries, dependencies, data flow, external-state receipts, diagnostics, and
  collision behavior. Each category hashes sorted compact JSON records,
  including owner identity, source path/span, and the extracted values.
- The portable rich snapshot preserves the underlying rich records. The fresh
  in-memory baseline additionally counts broad unresolved function candidates;
  those candidates are deliberately absent from the portable call export.
- Every one of the 1,092 reviewed page hashes is recorded beside its freshly
  computed value. The 3 remaining filled pages have no source hash and are
  counted separately by the page inventory.
- Graph fanout is separated into resolved calls, uncapped declared dependencies,
  and capped heuristic data flow. Symbol-target and documented-target counts
  are distinct. Unknown call ambiguity is `null`, not an invented zero.
- Snapshot and schema artifact sizes/hashes use LF-normalized text, matching
  `.gitattributes` on both Windows and Linux. This is the only artifact-byte
  normalization; scientific values and JSON/Markdown formatting are preserved.
- `regression-cases.json` names the two real fparser rejection files, all three
  historical comparison findings, a name collision, and the dependency hub.
  Its argument/span expectations are checked against the fresh parsers.
- Diagnostic metadata survives saving, loading, and reprojection. Documentation
  caches with missing or inconsistent rich/compact diagnostics rebuild before
  use, so existing caches cannot bypass this requirement.
- `KNOWN_LIMITATIONS.md` records limitations and explains the two additional
  grounding warnings. `PERFORMANCE.md` records measured runtime and process
  peak memory separately because those numbers cannot reproduce byte-for-byte.

## CI and release checks

The validation workflow fetches the pinned sources before running tests, so
source-backed tests are not silently skipped. It checks the baseline and rich
snapshot, README corpus counts, corpus status and grounding, strict MkDocs, and
schema/range/field-map regeneration. Baseline verification does not replace
the full test suite or the strict site build.

Parser cutover is still a later phase. Completing this baseline does not enable
fparser2 as the documentation fact producer.
