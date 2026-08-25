---
kind: procedure
symbol: init
title: init
status: filled
source_hash: 16fe21df2a9449dd
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
  unit: '`in` argument of type `integer`.'
  start_row_numbr: '`in` argument of type `integer`.'
  start_data_row_numbr: '`in` argument of type `integer`.'
  file_name: Local variable of type `character(len=*)`.
---

<!-- facts:header -->

Initializes a `table_reader` object — clears its buffers and sets the unit, file name, and start-row numbers — and warns if the file is missing or null.

## Bottom Line

`init` is the `table_reader` type's setup method. It resets the working strings, then applies any supplied `unit`, `file_name`, `start_row_numbr` (floored at 1), and `start_data_row_numbr`. It then `inquire`s whether the file exists and writes a warning to unit 9001 and stdout if it is missing or named `null`.

It prepares a reader before the header and data rows of a SWAT+ input table are parsed.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by input-reading routines to configure a `table_reader` before `get_header_columns`/`get_row_fields` walk the file.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `present(unit)) self%unit = unit`. |
| 2. if | Conditional branch evaluating `present(file_name)) self%file_name = file_name`. |
| 3. if | Conditional branch evaluating `present(start_row_numbr)`. |
| 4. if | Conditional branch evaluating `start_row_numbr < 1`. |
| 5. if | Conditional branch evaluating `present(start_data_row_numbr)) self%start_data_row_numbr = start_data_row_numbr`. |
| 6. if | Conditional branch evaluating `.not. self%file_exists .or. trim(self%file_name) == "null"`. |
| 7. io | Executes `write(9001,'(3A)') 'Warning: Input file named ', self%file_name, ' is missing or null.'`. |

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
- warning: missing_doc: Procedure 'utils::init' has no extracted documentation comment.
