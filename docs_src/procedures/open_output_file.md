---
kind: procedure
symbol: open_output_file
title: open_output_file
status: filled
source_hash: 16deb9d393486595
version_label: SWAT+ 62.0.0
args:
  iunit: '`in` argument of type `integer`.'
  filename: '`in` argument of type `character(len=*)`.'
  recl_val: '`in` argument of type `integer`.'
locals:
  full_path: Local variable of type `character(len=512)`.
---

<!-- facts:header -->

Convenience wrapper that opens an output file at the configured output path, optionally with a record length.

## Bottom Line

`open_output_file` resolves the full path with `get_output_filename`, then `OPEN`s the given unit — passing `recl` when the optional `recl_val` is supplied, otherwise opening with default record length.

It is the standard entry point the header and writer routines use so that every output file honours the configured `out_path`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called throughout the output layer (header_* and *_output routines) whenever an output unit is opened.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `present(recl_val)`. |
| 2. io | Executes `open (iunit, file=trim(full_path), recl=recl_val)`. |
| 3. else | Alternative branch taken when the preceding condition is false. |
| 4. io | Executes `open (iunit, file=trim(full_path))`. |
| 5. return | Executes `return`. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_path_module.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
