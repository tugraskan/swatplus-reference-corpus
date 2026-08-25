---
kind: procedure
symbol: to_lower
title: to_lower
status: filled
source_hash: 2b27e78dac50ab1e
version_label: SWAT+ 62.0.0
args:
  str: '`in` argument of type `character(len=*)`.'
locals:
  i: Local variable of type `integer`.
  code: Local variable of type `integer`.
---

<!-- facts:header -->

Pure function returning the input string with ASCII A–Z folded to lowercase; all other characters are unchanged.

## Bottom Line

`to_lower` walks the string character by character, converting only ASCII uppercase letters via `iachar`/`achar`; digits, symbols, spaces, and already-lowercase text pass through. The result length matches the input and no allocation is performed.

It is a dependency-free case-folding helper used to normalize column names and keywords when parsing input tables.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by the `table_reader` header parsing (`get_header_columns`, `output_column_warning`) and other input routines that compare names case-insensitively.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Loop over `do i = 1, len(str)`. |
| 2. if | Conditional branch evaluating `code >= iachar('A') .and. code <= iachar('Z')`. |
| 3. else | Alternative branch taken when the preceding condition is false. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

*No state changes recorded.*

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `utils.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'utils::to_lower' has no extracted documentation comment.
