---
kind: procedure
symbol: get_row_fields
title: get_row_fields
status: filled
source_hash: a614b1cf901a2f47
version_label: SWAT+ 62.0.0
args:
  self: '`inout` argument of type `class(table_reader)`.'
  eof: '`out` argument of type `integer`.'
locals:
  i: Local variable of type `integer`.
---

<!-- facts:header -->

Reads forward to the next valid data row — stripping comments and blank lines — splits it into trimmed fields, and warns and skips rows with the wrong column count.

## Bottom Line

`get_row_fields` reads lines until it finds a valid data row: it removes text after `#`, skips empty lines, splits the row into `self%row_field` (setting `self%nfields`), caps the field count at `ncols`, and warns to unit 9001/stdout while skipping any row with too few columns. It stops at the first valid row or EOF, returning the IOSTAT in `eof`.

It is the per-row reader used to iterate the data section of a SWAT+ input table.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called in a loop by input-reading routines to pull one data record at a time from a `table_reader`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Executes `do`. |
| 2. io | Executes `read(self%unit, '(A)', iostat=eof) self%line`. |
| 3. if | Conditional branch evaluating `eof /= 0) exit`. |
| 4. if | Conditional branch evaluating `self%lrow <= self%start_data_row_numbr) cycle`. |
| 5. call | Executes `call left_of_delim(self%line, '#', self%left_str)`. |
| 6. if | Conditional branch evaluating `len(self%left_str) == 0`. |
| 7. call | Executes `call split_line(self%line, self%row_field, self%nfields)`. |
| 8. loop | Loop over `do i=1, self%nfields`. |
| 9. if | Conditional branch evaluating `self%nfields > self%ncols) self%nfields = self%ncols`. |
| 10. if | Conditional branch evaluating `self%ncols > self%nfields`. |
| 11. io | Executes `write(9001,'(A,I3, 3A)') 'Warning: Row ', self%lrow - 1, ' in the input file ', self%file_name, ' has the wrong numbe...`. |
| 12. return | Executes `return`. |

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
- warning: missing_doc: Procedure 'utils::get_row_fields' has no extracted documentation comment.
