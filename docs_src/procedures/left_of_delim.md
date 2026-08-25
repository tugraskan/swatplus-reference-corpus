---
kind: procedure
symbol: left_of_delim
title: left_of_delim
status: filled
source_hash: 8292fdc5839e039b
version_label: SWAT+ 62.0.0
args:
  input: '`in` argument of type `character(len=*)`.'
  delim: '`in` argument of type `character(len=1)`.'
  result: '`out` argument of type `character(len=:)`.'
locals:
  pos: Local variable of type `integer`.
---

<!-- facts:header -->

Returns the part of a string before the first occurrence of a delimiter (e.g. the text left of a `#` comment); the whole string if the delimiter is absent.

## Bottom Line

`left_of_delim` uses `index` to find the first delimiter and returns everything before it (excluding the delimiter) in an allocatable result; if the delimiter is not found it returns the whole input. Whitespace before the delimiter is preserved.

It is the comment-stripping primitive used when reading SWAT+ input tables, typically with `#` as the delimiter.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by `table_reader` row/header parsing (`get_num_data_lines`, `get_header_columns`, `get_row_fields`) to drop trailing comments.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `pos == 0`. |
| 2. else | Alternative branch taken when the preceding condition is false. |

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
- warning: missing_doc: Procedure 'utils::left_of_delim' has no extracted documentation comment.
