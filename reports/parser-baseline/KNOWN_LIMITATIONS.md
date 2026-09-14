# Phase 0 known parser limitations

These are known properties of the reference rich scanner. They are recorded so
the fparser2 migration does not accidentally turn an existing limitation into a
required feature.

- Function-style calls start as broad `name(...)` candidates. Semantic
  resolution distinguishes internal functions from arrays and intrinsics; an
  unresolved candidate is retained in memory but omitted from the portable v2
  snapshot.
- The portable snapshot records unresolved explicit `CALL` statements, but the
  compact Markdown `FactStore` exposes resolved internal graph edges only.
- `called_by` retains bare caller names for rich-v3 compatibility. Each
  `CallRef` now carries its exact resolved definition identity or all equally
  visible candidates internally; generic/interface and type-bound dispatch are
  not modeled yet.
- `call_paths` contains deterministic maximal identity chains through exact
  resolved targets. A path ends at a leaf or with one repeated identity that
  marks a cycle closure. Parser-produced `ReviewFlag` collections now report
  ambiguous calls, but they are not yet comprehensive across later Phase 4
  relationship families.
- Control-flow steps carry their block nesting (Phase 1): `depth`, `block_id`,
  `parent_id`, `branch_of` and the opener's `end_line` let a consumer rebuild
  the block tree. Only the three constructs the pinned source uses are tracked
  -- `if ... then`, `do` and `select case`. A survey finds no `where` blocks,
  `forall`, `associate`, `block` or `critical` in it, so the constructs whose
  single-line and block forms are ambiguous are left untracked rather than
  guessed at; if one appears upstream its `end` would be ignored rather than
  mis-nested. This is still not a control-flow graph: loop rejoin, `exit`,
  `cycle` and `goto` are not modelled, and an arm records which construct it
  belongs to but not which condition selects it. On the pinned source 7,876 of
  7,877 constructs close; the one exception is the `if` at
  `gwflow_pond.f90:53`, where an independent line count of that file also finds
  one more opener than closer, so it reflects the source rather than the
  tracker. An unclosed construct keeps `end_line` unset rather than swallowing
  the rest of the procedure.
- Assignments now carry first-class `target`, `target_root` and `expression`
  fields alongside the raw statement and summary (Phase 1). The raw text is
  retained deliberately: it is the only record of the statement as written.
  Assignments inside a conditional are still a flat source-order list, so the
  branch an assignment sits in is not represented.
- The rich scanner is line-oriented; nested or unusually formatted declarations
  remain migration risks. Two historical span disagreements (`salt_balance`
  and `output_saltbal_header`) were actually name-only comparison collisions:
  the old report compared types in `output_ls_salt_module.f90` with types in
  `salt_module.f90`. Kind-plus-file matching agrees at 23 and 33 lines,
  respectively. The named cases retain and verify this correction.
- The source layer records an internal read -- one whose "unit" is a character
  variable rather than a file -- as an ordinary I/O operation, so it can appear
  as an `io_files` key. At the pinned commit the single instance is
  `unit_code_val`, from `gwflow_read.f90`'s `read(code_val,*)` statements.
  Telling an internal read from a file read needs the declared type of the
  unit expression, which is Phase 3 semantic work.
- fparser2 rejects the accepted `expr*-1` spelling in two pinned SWAT+ files.
  Those files use fallback parsing and must remain visible in diagnostics.
- The compact fact store uses qualified fallback keys such as
  `type::salt_balance` when a type and a procedure share one bare name.
- Same-kind duplicate names can still collapse in `FactStore`; `RichStore`
  retains all records and kind-plus-file lookup is required to disambiguate.
- On a stale cache, migration-only `docs facts-diff` currently performs one rich
  scan and two fparser2 source walks. The redundant diagnostic walk is removed
  at cutover.
- Parse time and peak process resident memory vary by machine. They are recorded in
  `PERFORMANCE.md` for comparison but are not byte-for-byte CI gates.
- `fparser` is pinned to an exact version. Its version string and its
  `FortranSyntaxError` text are both inside byte-compared artifacts, so an
  upgrade drifts the baseline and the rich snapshot for reasons unrelated to the
  parser under test. Upgrading it is a reviewed re-baseline; `swatref docs
  baseline` names the moved contract when that is the cause.
- The source-link audit resolves emitted URLs against the pinned local checkout
  rather than requesting them over the network. It proves commit, file, and line
  bounds; it does not prove GitHub will serve them.
- Every named regression case must assert something beyond the existence of its
  file and symbol. A case carrying no expectation is reported as unverified
  rather than passing silently.

## Grounding warning adjustment

The earlier 3,867 warning count becomes 3,869 because the compact call graph
now excludes unresolved intrinsic/external calls. The two additional warnings
are `DATE_AND_TIME` on `proc_date_time.md` and `move_alloc` on `res_control.md`.
They no longer enter page scope through graph edges. Their explicit source
calls remain in the rich snapshot; neither warning is a grounding error.
