---
kind: procedure
symbol: get_num_data_lines
title: get_num_data_lines
status: filled
source_hash: 0db8625f3421838c
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
locals:
  imax: 'Result variable: the `integer` value the function returns.'
  eof: Local variable of type `integer`.
  i: Local variable of type `integer`.
  ignore_last_col: Local variable of type `logical`.
---

<!-- facts:header -->

Scans the whole table file to count valid data rows — non-empty, non-comment, and matching the header column count — leaving the file positioned at EOF.

## Bottom Line

`get_num_data_lines` rewinds/opens the file, skips to the start row, treats the first meaningful line as the header (setting `ncols`, dropping a trailing `description` column), then counts subsequent rows that are non-empty, comment-stripped, and have at least the header's column count. It leaves the file at EOF, so callers must rewind before reading data.

It is used to pre-size arrays before the actual data rows are read.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by input-reading routines to determine how many records a table holds before allocating and reading them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Scan input records | Executes the source at the referenced lines. |
| 2. Store final state | Executes the source at the referenced lines. |

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
- warning: missing_doc: Procedure 'utils::get_num_data_lines' has no extracted documentation comment.
