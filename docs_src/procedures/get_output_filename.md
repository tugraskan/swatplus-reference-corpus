---
kind: procedure
symbol: get_output_filename
title: get_output_filename
status: filled
source_hash: 54aa1a3f306224b2
version_label: SWAT+ 62.0.0
args:
  filename: '`in` argument of type `character(len=*)`.'
locals:
  full_path: 'Result variable: the `character(len=512)` value the function returns.'
---

<!-- facts:header -->

Builds a full output-file path by prepending the module's `out_path` prefix to a bare filename.

## Bottom Line

`get_output_filename` returns `out_path//filename` when an output prefix has been configured, or the filename unchanged when it has not. It is a pure helper with no side effects.

It centralizes output-path handling so individual writer routines only need to pass a bare filename.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by `open_output_file` (and any routine building an output path) after `init_output_path` has set `out_path`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `len_trim(out_path) > 0`. |
| 2. else | Alternative branch taken when the preceding condition is false. |
| 3. return | Executes `return`. |

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

- No direct file I/O was extracted for this procedure.
