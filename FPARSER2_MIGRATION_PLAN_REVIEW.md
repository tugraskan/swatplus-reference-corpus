# Review — fparser2 Migration Plan, Revision 2

Reviewer: code review against `codex/fparser2-migration-plan-v2` @ `33b43ad`,
with the pinned SWAT+ tree (`cb442f7c05fc`, 648 files) checked out and the
pipeline actually run.

## Verdict

**REQUEST CHANGES** — narrowly. All eight blocking items from the Revision 1
review are resolved, and the plan document itself is now sound. What blocks
Phase 0 is not the plan's design: it is that the branch's new rich-primary
pipeline has already changed two published contracts without a version signal,
and the plan's "Current baseline" section does not record it. Phase 0's job is
to freeze a baseline; right now the tracked baseline artifact does not
reproduce.

Three items, all small and concrete. Everything else is approved.

## What I verified by running the branch

| Claim | Result |
|---|---|
| Test suite | 274 passed, 23 skipped |
| Page drift (`docs status`) | `filled=1095 stale=0 affected=0 todo=0 orphaned=0 missing-pages=0` |
| Grounding baseline | `0 errors, 3867 warnings across 1095 pages` — matches the plan exactly |
| Mermaid | 650 rendered pages carry diagrams; 15,765 clickable nodes; `mkdocs build --strict` succeeds; `mermaid.js` ships to `_site/assets/javascripts/` |
| Determinism | `facts.json` and the portable snapshot are byte-identical across repeated runs |
| `call_paths` / `ReviewFlag` | still 0 and 0 — the plan correctly calls these new work |

The zero-drift result is the important one. Revision 1 warned that moving the
`FactStore` to rich-scanner spans would re-hash all 1,092 pages and fail SPEC
§7.1 gate 3. It does not: every hash survives the producer switch unchanged,
with no re-baseline commit to `docs_src/`. Phase 0's new exit gate on page
hashes is therefore already satisfied at the pinned commit.

## Status of the Revision 1 blocking items

| # | Item | Status |
|---|---|---|
| B1 | `source_hash` / staleness missing from matrix | **Resolved** — own matrix row, Phase 0 and Phase 2 exit gates, verified zero drift |
| B2 | Dead fields presented as parity | **Resolved** — baseline section is accurate; `called_by`/`resolved` really are populated now, `call_paths`/ReviewFlags correctly marked new |
| B3 | Mermaid not a real capability | **Resolved** — it is now, and I confirmed it renders |
| B4 | Legacy removal unreachable | **Resolved** — Phase 8 permits a narrow fallback engine; the two rejection files and `expr*-1` are permanent regression cases |
| B5 | Raw text from `str(node)` | **Resolved** — Phase 2 forbids it, names the byte-sensitive fields, Phase 6 forbids normalizing them |
| B6 | Snapshot format fails open | **Resolved in the plan** — see C1 below for what the branch did in the meantime |
| B7 | fparser unpinned, no parser version | **Resolved** — Phase 1 |
| B8 | Snapshot size decided too late | **Resolved** — Phase 1 exit gate, with the 48.3 MB figure |

The Revision 1 grounding figures (141 errors / 3,904 warnings) were the pr-252
*candidate's* totals, not the main-source baseline. Revision 2's correction is
right, and its instruction to baseline against main rather than a comparison
candidate is the correct rule.

## Blocking changes before Phase 0

### C1. The `rich-v1` snapshot has already changed shape under the same version string

I regenerated the portable snapshot at the same pinned commit and diffed it
against the tracked `snapshots/rich/main-cb442f7c05fc.rich.json`:

| Field | Tracked artifact | Branch output |
|---|---|---|
| `metadata.format` | 1 | 1 |
| provenance `format` | `swatplus-reference-rich-v1` | `swatplus-reference-rich-v1` |
| total `calls` | 8,785 | **788** |
| — of kind `function` | 6,960 | 51 |
| — of kind `subroutine` | 1,825 | 737 |
| `called_by` entries | 0 | 778 |
| `resolved` calls | 0 | 778 |
| file size | 48.3 MB | 45.8 MB |

`_resolve_calls()` in `parser/documentation.py:105` mutates the `ProjectIndex`
in place before `RichStore.save()`, so the published Tamandua artifact now
carries a 91%-smaller call collection under an unchanged version string. Two
distinct losses are folded together:

- **Unresolved function candidates are deleted** (6,960 → 51). Defensible as a
  documentation view — it is exactly the filter `schema_fortran.py:719` says the
  analyzer should apply — but it is destructive on the shared model.
- **Duplicate call sites are collapsed** (1,825 → 737) by the `seen: set[(name,
  kind)]` dedupe. I checked: no unique `(procedure, target)` pair is lost, so
  the 1,088 removed records are repeat call sites with distinct `location`
  values. **The canonical model can no longer express that a procedure calls
  something from more than one line.** That contradicts the plan's own matrix
  row "Calls | ... raw text, kind, location".

This is precisely the failure Decision 4 exists to prevent, and it landed
before Phase 0. It also breaks Decision 1: `ProjectIndex.calls` now means
different things depending on which entry point produced the index —
`swatref schema build` still goes through `FortranScanner` directly
(`cli.py:472`) and sees all 8,785. A canonical model cannot have
producer-dependent semantics.

Required before Phase 0:
- Make the call resolution non-destructive — annotate `resolved` and populate
  `called_by` on the index, and apply the candidate filter and per-procedure
  dedupe in the `FactStore` projection where they belong, not in the shared
  model. Preserve per-call-site records and locations.
- Regenerate the tracked snapshot, or bump the export version, so the artifact
  in `snapshots/` reproduces from the code that claims to produce it.
- Record this change in the plan's "Current baseline" section, and have Phase 1's
  format-enforcement work explicitly cover the already-shipped divergence rather
  than assuming v1 is pristine.

### C2. Fallback and parse-error diagnostics are now permanently zero in tracked comparison reports

`comparison/run.py` switched from `parse_tree()` to `parse_documentation()`
(line 1474), but still reports:

```
"parser": {"base_fallback_files": len(base_store.fallback_files),
           "candidate_fallback_files": len(candidate_store.fallback_files),
           "fallback_set_changed": ...}
```

The rich projection never sets `parse_errors` or `fallback_files` — nothing in
`project_documentation_facts()` touches them — so these fields are now
structurally empty. `symbol-diff.json` emits the same always-empty
`parse_errors` blocks at line 211. The tracked
`reports/comparisons/pr-252/symbol-diff.json` still records two fallback files
with their fparser2 errors, so the artifact and the code that regenerates it now
disagree, and `fallback_set_changed` can never fire again.

`swatref docs parse` has the same hole: `cmd_parse` still iterates
`store.parse_errors`, which is now always empty, so the two known problem files
are no longer surfaced by any ordinary command.

This directly regresses Decision 5 ("make uncertainty visible") in the tree the
plan proposes to build on. Required: either feed those fields from a real
diagnostic source, or remove them and say in the plan that fparser2 rejection
tracking is reintroduced in Phase 5 — but do not leave a gate reporting a
hardcoded zero.

### C3. The new `depends_on` affected-edge is uncapped, and Phase 0 must baseline it per edge kind

`staleness.py` gained a third propagation kind (module/type dependency,
line 137). The older data-flow edge is deliberately capped
(`MAX_DATAFLOW_FANOUT = 12`, with a comment explaining that hub propagation "says
nothing"). The new edge has no cap, and dependency hubs are far larger than
variable hubs. Measured from the current fact store:

```
hydrograph_module 390   basin_module 251   constituent_mass_module 239
hru_module 233   maximum_data_module 215   time_module 197
53 symbols exceed the existing fanout cap of 12
```

So a release bump that touches `hydrograph_module` flags ~390 pages `affected`
in one hop. SPEC §7.1 gate 3 requires no drift buckets for a release, and the
pr-252 report's previous total was 235 affected pages overall.

The feature is defensible and SPEC §5.4 was updated for it, but Phase 7's gate
"Page hashes and direct/indirect staleness behave as before" is now ambiguous
about which "before". Required:
- Phase 0 must record affected-edge counts **per edge kind** (call graph,
  dependency, data flow), not one total.
- Decide now whether the dependency edge gets a fanout cap consistent with the
  data-flow one, and state the decision in the plan.

## Answers to the plan's questions

**1. Canonical boundary.** Yes, with the C1 correction: the boundary only holds
if the shared index is never mutated by one consumer's projection. Revision 2's
Phase 1 split of internal model version from an allowlisted export schema is the
right shape and directly addresses the `asdict(index)` problem.

**2. Capabilities preserved.** Yes for Markdown, GitHub links, Mermaid, schema
and comparison — verified by running them. Tamandua: not currently, per C1.

**3. Missing facts.** The matrix is now complete against what I can find. The
one thing it should sharpen is per-call-site call records (C1), which the matrix
already implies with "Calls | ... location" but the code no longer honours.

**4. AST plus raw-source overlay.** Appropriate, and Phase 2's ban on
`str(node)` for consumer-visible text is the correct hard rule.

**5. Fallback strength.** The plan's Phase 5 is now strong — "every fallback file
produces the full required rich fact set" is exactly the right gate. But the
*current* visibility is weaker than when Revision 1 was written (C2), so Phase 0
freezes a baseline in which the diagnostic reports zero.

**6. v1/v2 safety for Tamandua.** The strategy is right and the ordering
(enforce formats before adding fields, v1 fixture in Phase 1) is right. It is
unsafe today only because of C1.

**7. Exit gates.** Strong enough, and materially better than Revision 1 — the
hash gate, the byte-sensitive-field gate, the format-rejection gate, and the
SPEC §7.1 gate 7 reference all close real holes. Add the per-edge-kind
affected baseline from C3.

**8. What to change before coding.** C1, C2, C3, plus one line in "Current
baseline" recording that the snapshot contract has already moved.

**9. Source-hash, raw text, collision lookup, outside-state refs, schema
reproducibility.** Yes to all five in the plan, and I confirmed the hash and
schema-reproducibility claims hold in the tree (the branch does not touch
`schema/` or `schema_fortran.py` at all).

**10. Format enforcement, export schema, fparser pin, size/performance.**
Sufficient as written. They must additionally cover the already-shipped v1
divergence rather than treating v1 as a fixed point.

## Non-blocking suggestions

- `cmd_render` now calls `RichStore.load()` unguarded (`cli.py:440`), replacing
  the documented graceful degradation. It is safe because `get_store()` rebuilds
  first, but the failure mode on a manually deleted `rich.json` is a traceback,
  not a message. A one-line guard keeps the old behaviour.
- `mkdocs.yml` loads `https://unpkg.com/mermaid@11/dist/mermaid.min.js` — a
  floating major version from a third-party CDN, in a project that otherwise
  pins everything to exact commits. Consider vendoring it next to
  `assets/javascripts/mermaid.js`, or at least pinning the exact version.
- `comparison/run.py:204` has a duplicate `"unchanged"` key in one dict literal
  (pre-existing, from `2cf576f`, not this branch). Harmless — the second wins —
  but it is dead code in a gate-checked report builder.
- Phase 6 says the harness "may normalize collection order, identities, and
  explicitly approved semantic equivalents". Worth naming where the approved
  list lives, so "explicitly approved" cannot quietly grow during Phases 3–5.

---

# Appendix — Review of Revision 1

Reviewer: code review against `main` @ `db6423d` (pinned SWAT+ `cb442f7c05fc`).

## Verdict

**REQUEST CHANGES.** The strategy is sound and the phase discipline is good, but
the plan misstates the current baseline in ways that would send Phase 0 chasing
parity with things that do not exist, and it omits the one fact family that
gates the whole documentation pipeline. Eight blocking changes are listed in
§2; none require redesigning the approach.

## 1. The plan's framing is inverted

The plan is written as "make fparser2 the main parser, replacing
`FortranScanner`". In this repository fparser2 is *already* the main parser for
documentation:

- `parser/fortran.py:41` `parse_tree()` is AST-first (fparser2 F2008) and
  produces the `FactStore` that drives pages, staleness, grounding and
  rendering.
- `parser/schema_fortran.py:410` `FortranScanner` is the regex/logical-line
  scanner that produces `ProjectIndex`.

So the real migration is: **give the rich `ProjectIndex` an AST backend**. That
matters for scoping, because the consumer most at risk is not the Markdown
pipeline — it is `schema/input.py` (5,706 lines), which reads `ProcedureDoc.io`
(708 references), `IOOperation.fields` (580 references), `IOOperation.condition`
(19 references) and `.location` (123 references), and which produces the tracked
release schemas that SPEC §7.1 gate 7 requires to rebuild byte-identically.

Please restate the goal accordingly. Everything else in the plan survives the
restatement; only the risk ordering changes.

## 2. Blocking changes

### B1. The parity matrix omits `source_hash` — the staleness engine

`Symbol.source_hash` (`parser/facts.py:76`), `hash_slice()` (`facts.py:243`) and
`composite_source_hash()` (`facts.py:226`) are absent from §3. They are not a
minor field: **1,092 of 1,095 tracked pages in `docs_src/` carry a
`source_hash` in their reviewed frontmatter**, and `docs/staleness.py` compares
it to the fact store to assign `filled` / `stale` / `affected` / `orphaned`.
SPEC §7.1 gate 3 requires no drift buckets.

The hash is taken over a *physical line slice* (`lines[start_line-1:end_line]`).
Any change in how start/end lines are derived silently re-hashes every page and
fails the release gate with 1,092 false `stale` pages.

Required:
- Add "page identity and staleness" as its own matrix category: `source_hash`,
  `composite_source_hash`, and the `hash_slice` line-slice convention.
- Add a Phase 2 exit gate: all 1,092 tracked `source_hash` values are unchanged
  against the pinned commit — or the plan explicitly budgets a one-time
  re-baseline commit and says who reviews it.

This gate is achievable: `reports/docs/rich-vs-thin-cb442f7c05fc.md` shows the
two engines already agree on 0 thin-only / 0 rich-only symbols and disagree on
only 3 (`gwflow_floodplain` arg count, `output_saltbal_header` and
`type::salt_balance` spans). Keep the fparser2 span convention as the hash
input and the risk is bounded to those.

### B2. Four matrix rows describe fields that are never populated today

Presented as parity, these are new features:

| Field | Status in code |
|---|---|
| `ProcedureDoc.called_by` (`schema_model.py:113`) | declared, never written anywhere |
| `ProcedureDoc.call_paths` (`schema_model.py:114`) | declared, never written anywhere |
| `ReviewFlag` lists (7 declarations) | declared, never written anywhere |
| `CallRef.resolved` (`schema_model.py:53`) | always `False` |

Consequently §3's "Call relationships" and "Diagnostics" rows have no baseline
to freeze in Phase 0, and Phase 4's `called_by`/call-path work is greenfield,
not a port. Mark them as new capability with their own acceptance tests, and
decide in Phase 1 whether to populate or delete the dead fields rather than
carrying them into v2.

Note also that `FortranScanner` has *no* failure path at all — it is regex-based
and cannot raise on bad Fortran. "Diagnostics parity" is therefore vacuous; the
only diagnostics that exist today are `FactStore.parse_errors` /
`fallback_files` on the fparser2 side.

### B3. Mermaid graphs are not a current capability

§1, §7 and §9 gate on "Mermaid call and control-flow graphs render with
clickable source nodes". There is no graph generator in the repository. The only
mermaid in the tree is one hand-written block in reviewed prose
(`docs_src/output_families/hru_wb.md:161`), and `mkdocs.yml` does not register a
mermaid custom fence, so it renders as a code block, not a diagram.

Either drop these gates or move them to an explicitly-new deliverable with its
own PR. As written they will either block cutover forever or be quietly waived.

### B4. The two fparser2 failures are structural, so "remove the legacy scanner" is not reachable as stated

`reports/comparisons/pr-252/symbol-diff.json` records the real failures on the
pinned tree:

```
gwflow_floodplain.f90: FortranSyntaxError at line 86
  >>> if((Q*-1) >= gw_state(cell_id)%stor) then
gwflow_heat.f90:       FortranSyntaxError at line 61
  >>> if((cell_adv*-1) > heat_cell(i)) then
```

fparser2 0.2.5 rejects `expr*-1`, which gfortran accepts and SWAT+ uses. Today
those two files degrade to a symbols-only fallback — which is exactly why
`gwflow_floodplain` shows `arg_count: thin=0 rich=1` in the rich-vs-thin report.

For `ProjectIndex` parity those two files need the *full* rich fact set
(assignments, I/O, conditions, select cases), which only `FortranScanner` can
produce. So §9's "the normal pipeline no longer depends on `FortranScanner`" and
"duplicate legacy parsing code has been removed" are unachievable unless the
line-oriented scanner is *retained and renamed* as the supported per-file
fallback engine.

Required: reframe the definition of done as "one AST path plus one documented
fallback engine, both producing the same model", and add these two files (and
the `expr*-1` form) to the Phase 0 named fixture list.

### B5. Raw text must never come from `str(node)` — and the parity harness must compare it exactly

Verified against fparser 0.2.5. Source:

```fortran
read (107,*,iostat=eof) titldum, (vals(j),j=1,10)
```

`str(node)` returns:

```
READ(107, *, IOSTAT = eof) titldum, (vals(j), j = 1, 10)
```

fparser2 re-prints from the tree: keywords uppercased, spacing normalised,
`j=1,10` becomes `j = 1, 10`. §2 decision 3 already says the raw layer supplies
exact statement text, which is the right call — but two consequences are not
stated and need to be:

1. `IOOperation.raw`, `IOOperation.fields`, `IOOperation.condition`,
   `ControlStep.raw` and `ControlStep.summary` must be sliced from source, never
   rendered from the AST. `condition` in particular is matched as a literal
   substring in `schema/input.py:3340` (`f'timestep == "{branch}"' in
   op.condition`) and split on its `" > "` join convention in
   `input.py:5130-5229`. Its exact format is a load-bearing informal API.
2. Phase 6's "compare normalized facts rather than JSON list order" must
   **exclude** these fields: they require byte-exact comparison. Normalising
   them is precisely how a regression would hide.

Add a "raw-text normalisation contract" to Phase 2 with the current
`logical_lines()` behaviour (comment-stripped, continuations joined with a
single space, original case preserved) as the frozen specification.

### B6. `SNAPSHOT_FORMAT` is written but never checked on load — v2 will silently half-load in a v1 reader

`RichStore.save` writes `{"format": 1, "source": {...}}` (`parser/rich.py:141`),
but `RichStore.load` only validates `resolved_commit` (`rich.py:154-160`); the
`format` key is never read. `_restore()` (`rich.py:26`) drops unknown JSON keys
and defaults missing ones.

So a v2 snapshot handed to a current-generation reader does not fail — it loads
with new fields discarded and any renamed field silently defaulted. That is the
worst failure mode for Tamandua, and §7's v1/v2 compatibility answer does not
address it.

Required, and it must ship **before** any v2 field exists:
- Make `load()` read and enforce `format`, with an explicit accepted-version set.
- Publish the checked-in contract fixture (§7 already asks for one) in the same
  PR, not in PR 8.

Related: `RichStore.save` serialises `asdict(self.index)` wholesale, so *every*
in-memory model change is automatically a wire-format change. Phase 1 should
introduce an explicit serializer with a field allowlist and separate the
**model version** from the **snapshot format version**. As written the plan
conflates them, which forces a consumer-visible format bump for every internal
field the parser needs.

### B7. No pinned parser version, and no parser version in provenance

`pyproject.toml:17` declares `fparser>=0.2`. `SourceProvenance`
(`provenance/records.py:12`) records only source identity — no parser version,
no model version. Yet tracked artifacts embed fparser output verbatim:
`reports/comparisons/pr-252/symbol-diff.json` contains fparser's error strings,
and the fallback set depends on which files fparser accepts.

An fparser upgrade therefore silently changes tracked, gate-checked artifacts.
§7's cache-invalidation note mentions parser version but nothing pins or records
it.

Required in Phase 1: pin `fparser==<exact>` in `pyproject.toml`, add
`parser_version` / `fparser_version` / `model_version` to the provenance record
and the snapshot metadata, and treat an fparser bump as a reviewed change with
its own regression run.

### B8. Snapshot size is a Phase 1 design constraint, not a Phase 7 measurement

The current tracked v1 snapshot is **48.3 MB of JSON** for 648 files
(`snapshots/rich/main-cb442f7c05fc.rich.json`), committed as plain text with no
LFS filter in `.gitattributes`. It already carries `raw` on 21,507 assignments,
23,591 control steps, 8,785 calls and 7,079 I/O operations.

v2 as described adds raw statements, control-block spans and nesting, and
diagnostics — plausibly 2–4× — into a Git-tracked handoff artifact. §7 defers
the size budget to "before cutover", which is after the model shape is frozen in
Phase 1 and after PRs 2–7 have built on it.

Required: set the snapshot size budget and the storage decision (trim the
export, compress, or move to LFS) as a **Phase 1 exit gate**, since it
constrains what v2 may serialise.

## 3. Answers to the plan's questions

**1. Is `ProjectIndex v2` the correct canonical boundary?**
One canonical model is right, and deriving `FactStore` from it removes a genuine
double parse (today `parse_tree` and `FortranScanner` each walk the tree, and
`swatref docs facts-diff` builds a third). But make it three layers, not one
object:

- a `SourceText` layer — physical lines, logical lines, comment/string
  splitting, spans. Half of it already exists as `logical_lines()`,
  `split_fortran_comment()` and `_collect_doc_blocks()` in `schema_fortran.py`;
- `ProjectIndex v2` — the fact model;
- projections — `FactStore`, schema inputs, and the **export**, which must be a
  separately versioned type rather than `asdict(index)` (see B6).

Also state that the `FactStore` projection stays independently materialised and
cached. Today `docs render` degrades gracefully when the rich snapshot is absent
or commit-mismatched (`cli.py:429`, README §"Generated facts"). Making
`ProjectIndex` the only producer removes that unless the projection is a cached
artifact in its own right.

**2. Does the plan preserve current capabilities?**
Markdown, GitHub links, schema, comparison and Tamandua: yes, subject to B1,
B5, B6 and B7. Mermaid graphs: the capability does not exist (B3).

**3. Missing facts from the parity matrix?**
Beyond B1 and B2:

- `FactStore.add`'s bare-name collision policy (`facts.py:88-99`): procedures
  and modules win the bare-name slot, types get a `type::` key. Page
  frontmatter `symbol:` values, `[sym:...]` resolution and `page_by_symbol` all
  key on it. Phase 1's "stable record identities" must be a *superset-compatible*
  key or 1,095 reviewed pages need rewriting.
- `RichStore.get_of_kind()` (`rich.py:82`) fail-closed kind+file
  disambiguation — a tested contract, not an implementation detail.
- The `swatplus_reference_outside_state_refs` metadata family (`rich.py:23`,
  `refs.py:247`), keyed `kind:name:file` and consumed by `render.py:478`. It is
  distinct from the matrix's "Data flow" row.
- `annotate_dataflow()` (`fortran.py:105`) and its `reads`/`writes` semantics,
  which feed staleness `affected` propagation. The pr-252 run shows 235
  `affected` pages; changing this changes reviewer workload, so it needs a
  baseline number, not just a category.
- Source inventory: `parse_tree` scans `.f90` only (`fortran.py:44`) while
  `BuildConfig` scans `f90/F90/for/f/f95/F95` (`schema_config.py:17`). Moot on
  the pinned tree (all 648 files are `.f90`) but it must become one inventory.
- `SelectCaseDoc` deserves its own matrix row rather than a sub-clause of
  control flow: it is the decision-table vocabulary `schema/input.py` dispatches
  on (`input.py:2305`, `:2411`, `:2503`).

**4. Is AST + raw-source overlay appropriate?**
Yes — and it is the only workable design here, because `parse_file_ast` reads
with `ignore_comments=True` while SWAT+ carries its units and descriptions in
inline `! units |description` comments, including the gutter-continuation form
`_collect_doc_blocks` handles. Make the overlay the sole source of raw text per
B5.

**5. Is fallback behaviour strong enough?**
The *visibility* design is right and already partly implemented. The *coverage*
claim is not: today's fallback extracts symbols, uses and calls only, so a
fallback file contributes no args, variables, assignments, I/O or conditions.
For `ProjectIndex` parity that is a hole, and per B4 it is a permanent one for
two real files. Phase 5 should state the required fallback fact set explicitly
and gate on it.

**6. Is v1/v2 compatibility safe for Tamandua?**
No — see B6. It fails open today.

**7. Are the exit gates strong enough?**
Mostly, with three holes: no gate on page `source_hash` stability (B1); no gate
naming SPEC §7.1 gate 7 (rebuilding the four tracked schema/range/field-map
artifacts leaves no Git diff) even though `schema/input.py` is the biggest
`FortranScanner` consumer; and no size/perf gate at Phase 1, where the model
shape is actually decided (B8). Phase 7 should also pin the current grounding
baseline (4,045 checks / 141 errors / 3,904 warnings) rather than "pass",
because warnings are where silent regressions land.

**8. What should change before coding?**
The reframing in §1, the eight blocking items in §2, and one sequencing fix:
Phase 6 builds the parity harness *after* Phases 3–5 implement everything, while
PR 1 correctly puts the comparison schema first. Follow the PR order — the
harness is what makes Phases 3–5 reviewable.

## 4. Non-blocking suggestions

- Fold `swatref docs facts-diff` (`cli.py:143`) into the new harness; its
  count-only checks (arg/use/local counts and span length) are the "shallow
  comparison" Phase 6 replaces, and keeping both invites divergence.
- Phase 0 should record the 3 known thin-vs-rich disagreements as the accepted
  starting delta, with a decision on each.
- Consider moving `annotate_dataflow`'s regex line classification into the
  shared raw-source layer in Phase 2; it is the last place that re-implements
  comment/assignment splitting.
- `schema/input.py` imports `STRING_LITERAL_RE`, `parse_args` and
  `split_top_level_commas` from `schema_fortran` (`input.py:50`). Phase 8's "one
  raw-source utility layer" should name that import as part of the cleanup.
- The 62.0.0 release schema stores normalised `fortran_name` plus comment-derived
  `doc`, not raw field expressions — so it is better insulated from re-print
  drift than the `condition`/`fields` paths. Worth noting in the risk table so
  effort goes where the exposure actually is.
