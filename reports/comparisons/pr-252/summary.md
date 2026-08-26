# SWAT+ pull request 252 impact report

Comparison: [SWAT+ pull request 252](https://github.com/swat-model/swatplus/pull/252)

- Exact base: `e05177f4cb837613cf465802159eb723401668bb` (`dev`)
- Exact candidate: `795d2d92ef11bfb3c30a6b38fd987463f025ef93` (`refs/pull/252/head`)
- Existing reviewed corpus pages were read only; no AI filling was run.

## Result

Overall: **requires corpus and schema updates before adoption**.

- Same-toolchain compile: base=skipped, candidate=skipped
- Candidate facts deterministic: pass
- Candidate schema deterministic: pass
- Candidate input contracts repeat with zero changes: pass
- Strict isolated preview: skipped
- Parser fallback coverage: base=2 files, candidate=2 files
- Symbols: 29 added, 18 removed, 309 changed
- Schema entries: 44 added, removed, or changed; 6 newly unresolved
- Input contracts: 7 added, 4 removed, 8 changed; 1 newly unresolved filename expressions (27 candidate total)
- Corpus impact attributable to the PR: 100 newly stale, 184 newly affected, 9 newly orphaned, 8 new pages needed
- Grounding attributable to the PR: 139 new errors, 50 new warnings

## Human review focus

Start with `input-contract-changes.md` for added, removed, and changed SWAT+ inputs and their source read order. Use `schema-read-evidence.md` and `schema-diff.json` for extractor certification details. Generated candidate facts, schemas, rendered pages, site, and full logs stay in the ignored comparison workspace.

This run proves repeatable generation for the locked candidate commit. Differences between base and candidate are expected and are reported as review targets; only a repeat run of the same candidate is required to have zero byte difference.
