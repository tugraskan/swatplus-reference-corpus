# Review — fparser2 Migration Plan

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
