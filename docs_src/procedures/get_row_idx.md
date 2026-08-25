---
kind: procedure
symbol: get_row_idx
title: get_row_idx
status: filled
source_hash: 2a1eb9ed805e56f0
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
locals:
  row: 'Result variable: the `integer` value the function returns.'
---

<!-- facts:header -->

Accessor returning the `table_reader`'s current data-row index (`nrow`).

## Bottom Line

`get_row_idx` is a trivial getter that returns `self%nrow`, the reader's current row counter. It has no side effects beyond reading the object.

It lets callers query how many data rows have been consumed from the table.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by input-reading loops that track progress through a `table_reader`.

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
- warning: missing_doc: Procedure 'utils::get_row_idx' has no extracted documentation comment.
