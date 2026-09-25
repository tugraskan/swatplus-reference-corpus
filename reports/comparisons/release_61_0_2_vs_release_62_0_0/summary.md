# release_61_0_2 vs release_62_0_0 impact report

Comparison: release_61_0_2 vs release_62_0_0

- Exact base: `5f932baf276792c28db0e0d8faa6e8ed30003522` (`61.0.2`)
- Exact candidate: `de210d64db4f1d75e110bd6af33ea9c333d27b8a` (`62.0.0`)
- Existing reviewed corpus pages were read only; no AI filling was run.

## Result

Overall: **requires corpus and schema updates before adoption**.

- Same-toolchain compile: base=skipped, candidate=skipped
- Candidate facts deterministic: pass
- Candidate schema deterministic: pass
- Candidate input contracts repeat with zero changes: pass
- Candidate output contracts repeat with zero changes: pass
- Strict isolated preview: skipped
- Parser fallback coverage: base=1 files, candidate=0 files
- Symbols: 161 added, 88 removed, 807 changed
- Schema entries: 126 added, removed, or changed; 0 newly unresolved
- Semantic schema: 126 changed section entries across 126 unique input filenames; 55 structural, 6 documentation-only, 64 source-location-only, 2 source-organization, 0 uncertain; 36 previously unresolved now resolved, 0 genuinely new files
- Input contracts: 46 added, 21 removed, 15 changed; 2 newly unresolved filename expressions (27 candidate total)
- Output contracts: 93 added, 91 removed, 113 changed; 0 newly unresolved filename expressions (56 candidate total)
- Corpus impact attributable to the PR: 0 newly stale, 72 newly affected, 0 newly orphaned, 0 new pages needed
- Grounding attributable to the PR: 0 new errors, 222 new warnings

## Human review focus

Start with `input-contract-changes.md` for added, removed, and changed SWAT+ inputs and their source read order, then `output-contract-changes.md` for the same view of files SWAT+ writes. Use `schema-read-evidence.md` and `schema-diff.json` for extractor certification details. Generated candidate facts, schemas, rendered pages, site, and full logs stay in the ignored comparison workspace.

This run proves repeatable generation for the locked candidate commit. Differences between base and candidate are expected and are reported as review targets; only a repeat run of the same candidate is required to have zero byte difference.
