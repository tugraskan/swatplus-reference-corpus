---
kind: procedure
symbol: res_read_conds
title: res_read_conds
status: filled
source_hash: f14dce7976ca1d9b
version_label: SWAT+ 62.0.0
locals:
  title: Header line read from `res_conds.dat`; it is used as the file's title/label and only
    checked for successful read before continuing.
  max_table: Number of reservoir condition tables declared in the input file; it controls
    allocation of `ctbl` and the outer loop over tables.
  tnum_conds: Temporary count of how many conditions a module contains; it is read from the
    file and used to allocate each module's `con` array and to loop over those conditions.
  ii: General loop index used first over conditions within a table and later over conditions
    within a module.
  ictbl: Outer loop index for each reservoir condition table loaded from `res_conds.dat`.
  isub_con: Temporary count of subconditions for the current condition record; it determines
    the size of each `scon` array before the full record is read.
  icc: Subcondition loop index used in implied-DO reads to fill each `scon(icc)` entry from
    the file.
  imod: Loop index over modules within the current reservoir condition table.
  eof: I/O status code from reading the title and table count; negative values indicate end-of-file
    or an unreadable/empty file state that causes an early return.
  i_exist: Logical flag from `inquire` that says whether `res_conds.dat` exists before attempting
    to open it.
uses:
  reservoir_conditions_module: '`reservoir_conditions_module` owns the global `ctbl` array
    and the derived-type components that this routine allocates and populates. The routine
    cannot build reservoir condition tables without those shared data structures.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%ctbl_res`, which records how
    many reservoir condition tables were loaded. That shared count is used to keep the model''s
    data-file bookkeeping consistent with what was read from disk.'
---

<!-- facts:header -->

Reads reservoir condition table definitions from `res_conds.dat` into the shared reservoir-condition database. It sizes and populates nested condition/module arrays and records the table count for later reservoir processing.

## Bottom Line

`res_read_conds` is a file-driven loader for reservoir condition tables. It opens `res_conds.dat`, checks that the file exists and contains a valid header/table count, then allocates the global `ctbl` array and fills each table's condition and module structures from the file records.

The routine matters because it builds the reservoir-condition data model used later in reservoir processing. It also stores the number of condition tables in `db_mx%ctbl_res`, which lets the wider model know how many reservoir-condition tables were loaded.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `proc_res` during reservoir setup, before reservoir objects are allocated and before reservoir data are read. `proc_res` calls it after the reservoir salt/CS database readers and before later reservoir initialization and reading steps, so the reservoir condition tables are available for downstream reservoir behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the input file exists | The routine uses `inquire(file="res_conds.dat", exist=i_exist)` to test for the reservoir-condition file and returns immediately if the file is missing. |
| 2. Open the reservoir-condition file and read its header | It opens `res_conds.dat` on unit 100, reads the title line, then reads `max_table`; if the read hits end-of-file or the table count is invalid, the routine exits without allocating anything. |
| 3. Allocate the top-level table array and save the table count | After validating `max_table`, the routine allocates `ctbl(max_table)` and stores the same count in `db_mx%ctbl_res` for shared model bookkeeping. |
| 4. Loop over each reservoir condition table | For each table, it reads the table name plus the declared numbers of conditions and modules, then allocates the `conds` and `mods` arrays to match those counts. |
| 5. Read each condition in the table | For every condition entry, it reads the subcondition count, backspaces to reread the full line, allocates the `scon` array, and then reads the condition count, all subcondition values, and the action value into `ctbl(ictbl)%conds(ii)`. |
| 6. Read each module in the table | For every module, it reads the module's condition count, allocates the module's `con` array, stores that count in `num_conds`, and then reads each module-condition record with its subconditions and action value. |
| 7. Return after all tables are populated | Once every table, condition, and module has been read and allocated, the routine returns to its caller with the shared reservoir-condition data populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_conditions_module] | `ctbl` | `ctbl(ictbl)%name, ctbl(ictbl)%num_conds, ctbl(ictbl)%num_modules, ctbl(ictbl)%conds(ii)%scon(isub_con), ctbl(ictbl)%conds(ii)%num_conds, ctbl(ictbl)%conds(ii)%scon(icc), ctbl(ictbl)%conds(ii)%action, ctbl(ictbl)%mods(imod)%con(tnum_conds), ctbl(ictbl)%mods(imod)%num_conds, ctbl(ictbl)%mods(imod)%con(ii)%scon(isub_con), ctbl(ictbl)%mods(imod)%con(ii)%num_conds, ctbl(ictbl)%mods(imod)%con(ii)%scon(icc), ctbl(ictbl)%mods(imod)%con(ii)%action` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ctbl_res` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ctbl_res` | After `max_table` is successfully read and is at least 1 | The routine records the number of reservoir condition tables loaded from `res_conds.dat` so other parts of the model can see how many tables were initialized. |
| `ctbl(ictbl)%mods(imod)%num_conds` | When each module's condition count is read for the current table | The routine copies the module's declared condition count from `tnum_conds` into the shared module record, making that count available after the file read completes. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved to three commits. The initial commit `df07e3f` added `res_read_conds.f90` with file existence checks, header reads, allocation of `ctbl`, population of nested condition/module arrays, and assignment to `db_mx%ctbl_res`. Commit `94b6dec` preserved the logic and only reformatted the source in the truncated diff shown. Commit `39fabde` again kept the routine logic the same while initializing local variables to zero/empty values and making small formatting edits.

- `df07e3f` introduced the routine and its core file-reading/allocation behavior, including the shared `db_mx%ctbl_res` assignment.
- `94b6dec` made no behavior change visible in the diff excerpt; it only restaged the same reading/allocation logic with formatting updates.
- `39fabde` initialized local variables (`title`, `max_table`, `tnum_conds`, `ii`, `ictbl`, `isub_con`, `icc`, `imod`, `eof`) and made formatting-only edits; the file-reading logic remained unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_conds' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into seven source-backed steps so the header read, table allocation, condition loading, and module loading are described separately.
- Lineage evidence resolved; summaries are based only on the provided diffs.
