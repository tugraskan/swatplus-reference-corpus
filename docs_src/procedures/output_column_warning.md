---
kind: procedure
symbol: output_column_warning
title: output_column_warning
status: filled
source_hash: c07a8bdc6cb0044e
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
  i: '`in` argument of type `integer`.'
---

<!-- facts:header -->

Issues a one-time warning when an unrecognized column header is encountered in an input file, suppressing repeats for that column.

## Bottom Line

`output_column_warning` checks `self%col_okay(i)`; on the first time an unknown column `i` is seen it clears the flag and writes a warning (lowercased column name, file name) to unit 9001 and stdout, then stays silent for that column thereafter.

It informs the user about columns present in the file but not recognized by the reader, without flooding the log.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by input-reading routines when a header column does not match any expected name.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `self%col_okay(i) .eqv. .true.`. |
| 2. io | Executes `write(9001,'(5A)') 'Warning: unknown column header named ', to_lower(trim(self%header_cols(i))), ' in the input file ...`. |
| 3. return | Executes `return`. |

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
- warning: missing_doc: Procedure 'utils::output_column_warning' has no extracted documentation comment.
