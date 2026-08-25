---
kind: procedure
symbol: get_col_count
title: get_col_count
status: filled
source_hash: 23d25efcc04df3d1
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
locals:
  col: 'Result variable: the `integer` value the function returns.'
---

<!-- facts:header -->

Accessor returning the `table_reader`'s detected column count (`ncols`).

## Bottom Line

`get_col_count` is a trivial getter that returns `self%ncols`, the number of columns found in the header row.

It lets callers size their reads to the table's column count.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by input-reading routines after `get_header_columns` has established the column count.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. return | Executes `return`. |

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

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'utils::get_col_count' has no extracted documentation comment.
