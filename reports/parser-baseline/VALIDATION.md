# Phase 0 completion evidence

Locally verified on 2026-09-02. Phase 0 freezes the existing rich parser as the
reference; it does not switch documentation facts to fparser2.

## Sources and reproducibility

- Documentation source: `cb442f7c05fc3bfc34349c446010f452d2737ca0`.
- Schema source: `de210d64db4f1d75e110bd6af33ea9c333d27b8a` (SWAT+ 62.0.0).
- `swatref docs baseline --write` passed, followed by an independent fresh
  `swatref docs baseline` run that matched the report, rich snapshot, and
  provenance exactly after LF normalization.
- The machine-readable report covers 31 fact categories and seven named
  source regression cases, and validates against `baseline.schema.json`.
- The rich snapshot contains 46,286,609 LF-normalized bytes; SHA-256:
  `32c1b51c15251fb4c868fb2260472842bdf415f118c01c542bb9883fb1279114`.
- Both runs used real fparser2 and rich parsing, not a saved fact cache. Parse
  observations were 304.60 seconds / 449.46 MiB and 448.35 seconds / 449.93 MiB.
  Concurrent work affected wall time; performance is not an equality gate.
- The post-review re-baseline reran on a different machine and Python, so
  `PERFORMANCE.md` now records 107.73 seconds / 499.86 MiB. The figures above
  remain the Phase 0 reference measurement; neither is an equality gate, and
  Phase 1 should set its budgets from a controlled run rather than either.

## Exit-gate results

| Check | Result |
| --- | --- |
| Full test suite | 310 passed before final diagnostic cache/reprojection safeguards |
| Final focused suite | 71 passed, including all three new cache cases, snapshot reprojection, baseline, render, preview, and affected-page tests |
| Post-review suite | 328 passed, adding call-observation identity, link-audit, regression-expectation, contract-drift, and schema-breach cases |
| Codex follow-up suite | 348 passed, zero skipped; includes all 23 pinned-source tests and 20 new regression cases for the four follow-up fixes |
| Reviewed source hashes | All 1,092 unchanged; no reviewed prose re-filled |
| Corpus status | 1,095 filled; zero stale, affected, todo, orphaned, or missing pages |
| Grounding | Zero errors; 3,869 warnings |
| Normal render and strict MkDocs | Passed; 1,100 rendered Markdown/HTML pages including generated indexes |
| GitHub source-link audit | `swatref docs check-links`: 44,442 links; zero wrong-commit, missing-file, or out-of-range targets |
| Graph output | 1,240 Mermaid blocks; rich preview/normal block equality covered by tests |
| Schema regeneration | 145 resolved input files, zero unresolved; no content diff after schema/range/field-map regeneration |
| Diagnostic retention | Both known fallback files survive rich metadata, FactStore, snapshot save/load, and reprojection |
| Cache upgrade | Missing or inconsistent rich/compact diagnostics force a rebuild; matching caches remain reusable |
| Declared dependency hub | Uncapped; `hydrograph_module` has 390 dependents; separate high-fanout fixture passes |
| Affected-page policy | Advisory by default; explicit strict option tested |

The source-link audit is now a committed gate rather than a one-time script:
`swatref docs check-links` resolves every emitted URL against the pinned local
source, checking the commit segment, the file, and physical line bounds, and CI
runs it after rendering. It does not request each URL over the network or
execute every Mermaid diagram in a browser.

## Calls and known discrepancies

The fresh internal model retains all 56,507 regex observations/candidates before
and after resolution. The baseline records this as a SHA-256 over the ordered
call-site tuples at three points — the raw scan, before resolution, and after —
so a resolution step that reordered or dropped a site would fail the gate even
while the count stayed equal. These are not all proven calls: 54,195 are unresolved
function-shaped candidates such as arrays or intrinsic expressions. The portable
snapshot exports 2,312 call sites: 2,291 resolved internal calls and 21 unresolved
explicit subroutine calls. Raw repeated-site and graph-edge counts are recorded
separately in the JSON baseline; unsupported ambiguity remains `null`.

The two known fparser2 fallback files are `gwflow_floodplain.f90` and
`gwflow_heat.f90`. The floodplain argument-count disagreement remains visible.
The two historical salt-type span disagreements were name-only comparisons
across different files; kind-plus-file matching agrees at 33 and 23 lines.
The named regressions retain these cases so that the correction remains tested.

## Handoff

The follow-up to `a044ae4` was verified locally on 2026-09-02:

- Focused workflow/link/rich-store/baseline tests: 52 passed.
- Full suite: 348 passed in 169.23 seconds, with the pinned release source
  present and no skipped tests.
- `swatref docs check-links`: 44,442 links, zero invalid targets, using the
  corrected physical line count.
- A fresh `swatref docs baseline` check reproduced the tracked report,
  snapshot, and provenance exactly. Parsing took 106.10 seconds with 449.46 MiB
  peak process memory; this observation did not replace `PERFORMANCE.md`.
- No `--write` re-baseline was used. The portable snapshot, deterministic JSON
  baseline, reviewed pages, schema artifacts, and performance reference have
  no content changes relative to `a044ae4`.
- The review's four follow-up corrections and their rationale are recorded
  in `PHASE0_REVIEW.md`. Hosted CI has not run for these local changes.

CI now checks baseline/snapshot freshness and fetches pinned sources before
source-backed tests. Hosted CI and publishing have not been verified for this
change. The next implementation step is Phase 1: define the richer shared model
and compatibility contract before changing parser extraction.
