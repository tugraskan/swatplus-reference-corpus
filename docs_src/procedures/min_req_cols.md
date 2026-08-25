---
kind: procedure
symbol: min_req_cols
title: min_req_cols
status: filled
source_hash: 771057e865411f2c
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
  min_cols: '`in` argument of type `character(len=*)`.'
---

<!-- facts:header -->

Setter that stores the caller's minimum-required-column list on the `table_reader` (`min_cols`).

## Bottom Line

`min_req_cols` simply trims and stores the supplied required-column string in `self%min_cols` for a later header check.

It records which columns a reader must find before `min_header_cols` validates the header.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called before header validation to declare the columns a table must contain.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Review source manually | No major control-flow steps were extracted automatically. |

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
- warning: missing_doc: Procedure 'utils::min_req_cols' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
