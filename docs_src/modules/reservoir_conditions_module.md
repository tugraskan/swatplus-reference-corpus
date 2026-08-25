---
kind: module
symbol: reservoir_conditions_module
title: reservoir_conditions_module
status: filled
source_hash: 36c8a22fc1a2265c
version_label: SWAT+ 62.0.0
variables:
  release: Shared real-valued reservoir release amount. It is initialized to `0.` in the module
    and is written by `res_read` when a named release table is resolved and by `res_rel_conds`
    when no condition block matches. In the source comments and callers it functions as the
    selected release flow index/value used by reservoir release control.
  day: Shared integer day value for reservoir-condition evaluation. It is initialized to `0`
    in the module and read by `res_rel_conds` when a condition clause uses the `day` variable.
    The source does not show this module setting `day`; it is external state supplied to the
    release-condition workflow.
  hit: Shared one-character pass/fail flag for condition evaluation. It is initialized to
    an empty string and set to `'y'` before scanning a condition block in `res_rel_conds`;
    `cond_integer_c` and `cond_real_c` change it to `'n'` when a comparison fails. Downstream
    code uses it to stop scanning once a matching condition block is found or to detect failed
    comparisons.
  ctbl: Allocatable array of `reservoir_condition_tables` records holding all reservoir condition
    tables loaded from `res_conds.dat`. It is allocated and filled by `res_read_conds`, then
    read by `res_read` to resolve `ctbl_` release names and by `res_rel_conds` to evaluate
    condition clauses and module actions.
type_components:
  cond:
    var: Character variable selector naming the state field to test, such as `stor`, `inflo`,
      `pdsi`, or `day`.
    op: Two-character comparison operator to apply, such as `<`, `>`, `<=`, `>=`, `=`, or
      `/=`.
    val: Right-hand-side comparison value stored as a real number in the table record.
  conditions:
    num_conds: Number of subconditions in this rule.
    action: Action value associated with the rule; `res_rel_conds` uses it as the module selector
      after the top-level rule matches.
    scon: Allocatable array of `cond` records containing the individual comparison clauses
      for this rule.
  modules:
    num_conds: Number of condition records in the module branch.
    con: Allocatable array of `conditions` records that define the module's condition sets.
  reservoir_condition_tables:
    name: Table name used to match release definitions such as `ctbl_...`.
    num_tbl: Table count metadata field stored with the table set.
    num_conds: Number of top-level condition rules in this table.
    num_modules: Number of module branches associated with this table.
    conds: Allocatable array of top-level `conditions` records for the table.
    mods: Allocatable array of `modules` records for module-specific condition branches.
type_summaries:
  cond: One comparison clause inside a reservoir release condition table.
  conditions: One top-level reservoir release rule made of one or more subconditions plus
    a resulting action.
  modules: One module-specific branch under a reservoir condition table, containing its own
    set of comparison rules.
  reservoir_condition_tables: A complete reservoir condition-table entry loaded from `res_conds.dat`.
---

<!-- facts:header -->

Declares the shared reservoir release-state variables and the nested derived types used to store reservoir condition tables. It owns the global condition-table array `ctbl` plus the current evaluation state `release`, `day`, and `hit`, which are populated by the reservoir input loaders and consumed by release-condition evaluation and comparison helpers.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container for shared reservoir-condition state; its scalar variables are initialized in the declarations, while the table array is populated later by `res_read_conds` from `res_conds.dat`. The source does not show any contained initialization procedures.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:res_read] | `reservoir.res` | `release, day, hit, ctbl` | Reads reservoir definitions and resolves a release name beginning with `ctbl_` against `ctbl(irel)%name`, storing the matching table index in `res_dat(ires)%release` and marking the reservoir as using a conditions table via `res_ob(ires)%rel_tbl = "c"`. It does not populate `ctbl`; it consumes it after `res_read_conds` has loaded the tables. |
| [sym:res_read_conds] | `res_conds.dat` | `release, day, hit, ctbl` | Allocates and fills the shared `ctbl` array from the reservoir condition-table file, including each table's `name`, top-level `conds`, and module branches `mods`. This loader owns the table initialization for the module state. |

## Key Consumers

The module is used by one file-driven loader and three release-evaluation helpers. `res_read_conds` populates the shared table database, `res_read` resolves named release tables against it, and `cond_integer_c`, `cond_real_c`, and `res_rel_conds` use the shared `hit`, `day`, `release`, and `ctbl` state during condition testing and release selection.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:res_read] | reservoir_conditions_module | `res_read` uses the shared `ctbl` registry to resolve release names that begin with `ctbl_`. The later effect is that the reservoir object is linked to a specific condition table index and flagged as condition-table driven. |
| [sym:res_read_conds] | reservoir_conditions_module | `res_read_conds` allocates and populates the module's global `ctbl` array, creating the reservoir condition-table database that later release-selection code reads. |
| [sym:cond_integer_c] | reservoir_conditions_module | Updates the shared `hit` flag to `'n'` when an integer comparison fails, so the surrounding reservoir-condition scan can stop evaluating the current rule set. |
| [sym:cond_real_c] | reservoir_conditions_module | Updates the shared `hit` flag to `'n'` when a real-valued comparison fails, allowing the surrounding reservoir-condition scan to record that the tested clause did not pass. |
| [sym:res_rel_conds] | reservoir_conditions_module | Reads `ctbl` to scan reservoir release conditions, uses `hit` as the shared pass/fail flag for each clause, checks `day` for date-based rules, and writes `release` when no top-level rule matches or when the selected module does not satisfy its subconditions. |

## Lineage

`reservoir_conditions_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `reservoir_conditions_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `reservoir_conditions_module` has no extracted module-level documentation comment.
- No commits were resolved for the requested source span, so lineage impacts are unavailable.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
