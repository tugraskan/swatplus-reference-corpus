---
kind: procedure
symbol: split_line
title: split_line
status: filled
source_hash: f2693a005a7ea8d4
version_label: SWAT+ 62.0.0
args:
  line2: '`in` argument of type `character(len=*)`.'
  fields2: '`out` argument of type `character(len=*)`.'
  nfields: '`out` argument of type `integer`.'
  delim: '`in` argument of type `character(len=1)`.'
  maxsplit: '`in` argument of type `integer`.'
locals:
  pos1: Local variable of type `integer`.
  pos2: Local variable of type `integer`.
  len_line: Local variable of type `integer`.
  splits_done: Local variable of type `integer`.
  current_delim: Local variable of type `character(len=1)`.
  use_custom_delim: Local variable of type `logical`.
---

<!-- facts:header -->

Splits a line into fixed-size string fields — on a given single-character delimiter (empty fields preserved) or, by default, on whitespace (runs collapsed) — honouring an optional maxsplit.

## Bottom Line

`split_line` fills a caller-provided fixed-size array with the fields of a line and returns the count. With an explicit delimiter it preserves empty fields (leading, trailing, and consecutive delimiters); without one it splits on spaces/tabs, collapsing runs and ignoring leading/trailing whitespace. An optional `maxsplit` caps the number of splits, with the remainder becoming the last field.

It deliberately avoids allocatable/deferred-length arrays to stay debugger-friendly, and is the tokenizer under the `table_reader` header and data parsing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by `get_num_data_lines`, `get_header_columns`, `get_row_fields`, and `min_header_cols` to tokenize input-table lines.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Iterate configured work | Executes the source at the referenced lines. |
| 2. Evaluate branch conditions | Executes the source at the referenced lines. |
| 3. Call model routines | Executes the source at the referenced lines. |
| 4. Update shared state | Executes the source at the referenced lines. |

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
- warning: missing_doc: Procedure 'utils::split_line' has no extracted documentation comment.
