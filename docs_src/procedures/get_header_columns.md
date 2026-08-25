---
kind: procedure
symbol: get_header_columns
title: get_header_columns
status: filled
source_hash: e9c726cc82aca29f
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
  eof: Local variable of type `integer`.
locals:
  i: Local variable of type `integer`.
  ignore_last_col: Local variable of type `logical`.
---

<!-- facts:header -->

Locates and reads the header row, splits it into lowercased, trimmed column names stored on the `table_reader`, and sets `ncols`.

## Bottom Line

`get_header_columns` rewinds the file, skips the title line and any blank/comment-only lines, takes the first meaningful line as the header, splits it into column names, folds them to lowercase and trims them into `self%header_cols`, sets `self%ncols`, and marks `found_header_row`. It leaves the file positioned just after the header. `eof` returns the final IOSTAT.

It normalizes the header so later reads and column look-ups are case-insensitive.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by input-reading routines after `init` to establish the table's columns before data rows are read.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Scan input records | Executes the source at the referenced lines. |
| 2. Allocate target storage | Executes the source at the referenced lines. |
| 3. Read records into state | Executes the source at the referenced lines. |
| 4. Store final state | Executes the source at the referenced lines. |

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
- warning: missing_doc: Procedure 'utils::get_header_columns' has no extracted documentation comment.
