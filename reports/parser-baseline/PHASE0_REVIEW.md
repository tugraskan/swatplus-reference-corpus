# Phase 0 baseline review

Review of `codex/fparser2-migration-plan-v2` at `be75bcf` (Phase 0 completion),
covering `75de609` and `be75bcf`. Recorded before Phase 1 so the gaps between
what Phase 0 *claims* and what Phase 0 *enforces* stay visible.

## Verified against the tracked artifacts

- The rich snapshot is 46,286,609 LF-normalized bytes with SHA-256
  `32c1b51c15251fb4c868fb2260472842bdf415f118c01c542bb9883fb1279114`, matching
  the `artifacts` entry inside `main-cb442f7c05fc.json` exactly.
- The report carries 31 fact categories and `baseline.schema.json` requires the
  same 31, with `additionalProperties: false` at the top level and under
  `facts`. Adding or removing a category forces a reviewed schema edit.
- The three README counts gated by `swatref docs baseline` (1,095 filled pages,
  0 grounding errors, 3,869 warnings) match the report's `documentation`
  section, and 1,092 hashed pages matches the plan's exit gate.
- Call totals reconcile end to end: 56,507 in-memory observations, 2,312
  exported call sites, 2,291 resolved, 21 unresolved explicit subroutine calls.
- `swatref.toml` pins the `main` profile by commit, so the baseline filename and
  recorded provenance are deterministic.

## Confirmed fixes from the previous review

- `RichStore.resolve_calls()` moved onto the store and now runs from both
  `build()` and `save()`, so the portable export no longer depends on a caller
  having run the documentation projection first.
- `_INTENTIONALLY_INTERNAL_EXPORT_FIELDS` plus `_export_field_names()` makes the
  export whitelist a two-sided gate, with parity test coverage.
- Replacing the bare-name `rich_index` lookup in `docs facts-diff` with
  `get_of_kind(name, kind, file=...)` showed that two of the three "known
  thin/rich disagreements" were comparing same-named derived types across
  different files. Pinning them as positive regression expectations (33/33 and
  23/23) rather than deleting them is the right correction.

## Findings

### 1. `fparser` is unpinned but its output is inside byte-compared artifacts

`contracts.fparser_version` is part of the byte-compared baseline report, and
fparser's `FortranSyntaxError` message text is embedded in the tracked rich
snapshot's `swatplus_reference_fparser_diagnostics` metadata. `pyproject.toml`
declares `fparser>=0.2` and CI installs with no lock or constraints file, so the
next fparser release fails `swatref docs baseline` with `stale baseline
artifact` for a reason unrelated to the parser under test.

### 2. The call-observation gate is vacuous

`build_parser_baseline()` sets `observations_before_resolution` from
`sum(len(item.calls))`, calls `rich.resolve_calls()`, then sets
`observations_after_resolution` from the same lists. Resolution only writes
`CallRef.name` and `CallRef.resolved` and cannot change list lengths, and since
`75de609` it self-asserts that internally. The `baseline_failures()` check
`"call observations changed during resolution"` therefore cannot fire. The store
also arrives already resolved, because both `parse_documentation()` and
`RichStore.save()` resolve first, so the "before" reading is post-resolution.
This is the headline Phase 0 guarantee (plan section 7) and it needs a check
with teeth.

### 3. The GitHub source-link audit is not in the repository

`VALIDATION.md` lists a 44,442-link audit in the exit-gate table beside the
automated gates, but no link-checking code exists in `src/`, `tests/`, or
`.github/workflows/validate.yml`. Those URLs are built from `source_link_base`
plus line numbers in `docs/render.py`, exactly what Phase 1 line-numbering work
will disturb, and nothing re-checks them.

### 4. Two named regression cases assert nothing

`type-procedure-name-collision` and `declared-dependency-hub` carry no
`comparison` and no `expected_fparser_fallback`, so `_regression_summary()` only
verifies that the file and the symbol exist. Their stated concerns are covered
elsewhere, but the entries themselves would not fail if the behavior regressed
while still counting toward `"count": 7`.

### 5. Schema validation bypasses the failure path

Reading `baseline.schema.json` and running `Draft202012Validator.validate()` sit
outside the `failures` collection in `cmd_baseline()`, so a contract breach
exits with a Python traceback instead of a `Phase 0 gate failed:` line.

### 6. CI parses the pinned source four times

`swatref docs parse` runs fparser2 plus the rich scanner, and `swatref docs
baseline` runs both again. The baseline must reparse from source to mean
anything, so the redundant step is `docs parse`: `docs status` populates the
same cache lazily.

### 7. The test reorder in CI buys nothing

Unit tests moved behind both `source fetch` steps, but every test reads
`tests/fixtures`; none reads the fetched checkout. A source-fetch outage now
costs all test feedback.

## Assessment

None of these block Phase 1. Findings 1, 2, and 3 matter most: one will fail CI
on an unrelated upstream release, and two are places where the recorded Phase 0
evidence claims more than the committed code enforces.

## Resolution

All seven findings are addressed on this branch. The fixes are summarized here
so the review and its outcome stay together.

1. `fparser` is pinned to `==0.2.4` in `pyproject.toml`. This was not
   hypothetical: an unpinned resolve during this review already selected
   fparser 0.2.5. `swatref docs baseline` now also names the moved contract
   when a byte comparison fails for a toolchain reason
   (`contract changed: fparser_version: '0.2.4' -> '0.2.5'`).
2. `RichStore.call_observations()` and `call_observation_identity()` give the
   call sites a resolution-independent identity, deliberately excluding `name`
   and `resolved`. `RichStore.build()` pins the scanner's own identity before
   anything resolves, and the baseline records it at the scan, before
   resolution, and after. `baseline_failures()` gates on those hashes, so a
   reordered or dropped observation fails even when the count is unchanged.
3. `swatref docs check-links` audits the rendered corpus against the pinned
   checkout by commit segment, file existence, and physical line bounds, and CI
   runs it after rendering. Against the current corpus it reproduces the
   recorded figure exactly: 44,442 links, zero invalid targets, in 13 seconds.
4. Regression cases accept `expected_symbol_keys` and
   `expected_min_dependents`. The collision case now requires both
   `salt_balance` and `type::salt_balance`; the hub case requires at least 390
   dependents. A case that asserts nothing is reported as unverified rather
   than passing, which is what the `asserts_behavior` check records.
5. Schema reading and validation are inside the failure path, so a contract
   breach prints `Phase 0 gate failed: ...` and returns 1.
6. The redundant `swatref docs parse` step is removed from CI; `docs status`
   populates the same cache lazily.
7. Unit tests run before the source fetch again.

Fixes 2 and 4 change the baseline payload, so `baseline.schema.json` gained
three call-identity fields and three regression-check fields, and the tracked
baseline was regenerated with `swatref docs baseline --write`.

## Codex follow-up on `a044ae4`

A second review reproduced four remaining gaps. These corrections preserve the
parser output and strengthen the checks; no re-baseline is intended.

1. **Restore the source-fetch/test order.** Finding 7 above was incorrect:
   `tests/test_schema_input.py::PinnedSourceSmokeTest` contains 23 tests using
   `external/swatplus-62.0.0/src`. All 23 skip if that checkout is absent. The
   workflow now fetches and verifies both sources before `pytest`, with a test
   enforcing that ordering. Removing the explicit `docs parse` command remains
   harmless, but does not save a parser pass on clean CI: `docs status` still
   builds the same cache.
2. **Fix physical line bounds.** Counting newlines plus one admitted a phantom
   final line in LF/CRLF-terminated files and a line in empty files. The audit
   now counts a final unterminated line only when present. Tests cover empty
   files, LF, CRLF, trailing blank lines, unterminated lines, and invalid single
   and range links alongside valid links.
3. **Capture scanner identity before enrichment.** The checkpoint previously
   ran after `extract_outside_state_refs`, so it could not detect changes made
   there. It now runs immediately after scanning and constructing the store,
   before outside-state extraction. Fault-injection tests drop a call or change
   its location during extraction and prove that the pinned raw identity no
   longer matches the corrupted result. Resolution-owned fields and the
   snapshot-loaded `None` identity policy are unchanged.
4. **Stop on an invalid schema/payload.** Schema failures now return 1 before
   invariant or README checks can inspect malformed fields. Tests cover missing
   sections and wrong root/nested types in both check and `--write` modes,
   verifying that tracked snapshots, provenance, reports, and performance
   measurements remain untouched.

The exact fparser pin, contract-drift diagnostics, strengthened named cases,
and recorded performance measurements from `a044ae4` are retained.

Verification: 348 tests passed with zero skips (52 focused tests also passed);
the real-corpus audit reports 44,442 links with zero invalid targets; a fresh
baseline check reproduces the tracked artifacts without `--write`. Full results
are recorded in `VALIDATION.md`.
