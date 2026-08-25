---
kind: procedure
symbol: print_prt_error
title: print_prt_error
status: filled
source_hash: 4e4803c206dd1726
version_label: SWAT+ 62.0.0
args:
  name: '`in` argument of type `character (len=16)`.'
locals:
  r: 'Result variable: the `integer` value the function returns.'
---

<!-- facts:header -->

Prints a fatal error that a print object is duplicated in `print.prt` and aborts the run.

## Bottom Line

`print_prt_error` writes an error message naming the duplicated print object in the `print.prt` input file, then calls `error stop` to abort. Its integer result is set to 1 but the routine does not return normally.

It enforces that each print object appears only once in the print-control input.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by the `print.prt` reader when it detects a duplicate print-object entry.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. io | Executes `write(*, fmt="(a,a,a)", advance="no") "Error: ", name, "print object is duplicated in the input file print.prt. Abort...`. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `basin_module.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_module::print_prt_error' has no extracted documentation comment.
