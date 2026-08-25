---
kind: procedure
symbol: header_lu_change
title: header_lu_change
status: filled
source_hash: 88e35f816589c2ed
version_label: SWAT+ 62.0.0
uses:
  basin_module: '`basin_module` provides the basin name (`bsn%name`) and program name (`prog`)
    that are written into the output header, so this module supplies the identity text that
    tags the file contents.'
  output_path_module: '`output_path_module` matters because it supplies `open_output_file`,
    which resolves the output path and opens unit 3612 with the requested record length before
    any header text is written.'
---

<!-- facts:header -->

Writes the header for the land-use change output file.

## Bottom Line

`header_lu_change` opens the SWAT+ land-use-change output file, writes a basin/program identifier header, and then writes the column labels for the file. It is a small formatting routine, but it matters because later land-use-change reporting depends on this file being created with the expected header layout.

The routine also records the output file name in the DTBL listing stream so the model’s output table bookkeeping can reference `lu_change_out.txt`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_open` calls `header_lu_change` during startup after it has begun writing output-file headers for other components. Before this call, `proc_open` has already set up the header-writing sequence, and `header_lu_change` contributes the land-use-change header that downstream output parsing and reporting expect when SWAT+ later writes land-use-change results.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. open output file | Open unit 3612 for the land-use-change output file `lu_change_out.txt` with record length 800 so header text can be written to a ready output stream. |
| 2. write basin header | Write the basin name and program identifier from `basin_module` to the open output file as the first header line. |
| 3. write column labels | Write the fixed formatted column heading line for the land-use-change table, defining the fields hru, year, mon, day, operation, lu_before, and lu_after. |
| 4. log DTBL entry | Write the output-table listing entry for `lu_change_out.txt` to unit 9000 so the model’s DTBL bookkeeping knows this file exists. |
| 5. return | Return to the caller after the output file header has been fully initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn, prog` | `bsn%name` |
| [sym:output_path_module] | `open_output_file` | `output_path_module::open_output_file` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_lu_change.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `504d2b3` (2025-12-11, "Align Use statements and adjusting whitespace."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_lu_change.f90` are listed.

- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_lu_change' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
