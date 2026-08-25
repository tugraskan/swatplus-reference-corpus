---
kind: procedure
symbol: min_header_cols
title: min_header_cols
status: filled
source_hash: 62a9b081581ef13b
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
  min_cols: '`in` argument of type `character(len=*)`.'
locals:
  min_hdr_cols: Local variable of type `character(max_name_len)`.
  i: Local variable of type `integer`.
  ncols: Local variable of type `integer`.
  min_col: Local variable of type `character(len=:)`.
---

<!-- facts:header -->

Checks that every user-specified required column name appears in the header row; prints an error and stops the run if one is missing.

## Bottom Line

`min_header_cols` splits the required-column list, then for each name searches the header line with `index`; a missing required column writes an error to unit 9001 and stdout and `stop`s the program.

It enforces that mandatory input columns are present before parsing continues.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called after the header is read to fail fast when a required input column is absent.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. call | Executes `call split_line(min_cols, min_hdr_cols, ncols)`. |
| 2. loop | Loop over `do i = 1, ncols`. |
| 3. if | Conditional branch evaluating `index(self%line, min_col) == 0`. |
| 4. io | Executes `write(9001, '(4A)') "Error: Required column ", min_col, " not found in ", self%file_name`. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `utils.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'utils::min_header_cols' has no extracted documentation comment.
