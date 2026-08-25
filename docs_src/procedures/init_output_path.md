---
kind: procedure
symbol: init_output_path
title: init_output_path
status: filled
source_hash: 6dc27667cdfc62fc
version_label: SWAT+ 62.0.0
args:
  path_in: '`in` argument of type `character(len=*)`.'
locals:
  path_work: Local variable of type `character(len=256)`.
  path_mkdir: Local variable of type `character(len=256)`.
  cmd: Local variable of type `character(len=512)`.
  os_env: Local variable of type `character(len=32)`.
  i: Local variable of type `integer`.
  path_len: Local variable of type `integer`.
  stat: Local variable of type `integer`.
  is_windows: Local variable of type `logical`.
  dir_exists: Local variable of type `logical`.
---

<!-- facts:header -->

Validates the configured output-directory path and, if one is set, creates it, storing the prefix in the module variable `out_path` used for every output file.

## Bottom Line

`init_output_path` runs once during output setup. It detects the operating system, then treats a `null`/`NULL`/empty path as "current directory" (empty prefix). For a real path it normalizes the string, ensures the directory exists (creating it if needed), stores it in `out_path`, and prints a confirmation.

`out_path` is module state read by `get_output_filename` and `open_output_file`, so this routine's result silently prefixes the location of every SWAT+ output file.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called during simulation start-up before any output files are opened. Its `out_path` result is consumed by `get_output_filename`/`open_output_file` for the lifetime of the run.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Executes the source at the referenced lines. |
| 2. Loop over output items | Executes the source at the referenced lines. |
| 3. Write output records | Executes the source at the referenced lines. |
| 4. Update output state | Executes the source at the referenced lines. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

*No state changes recorded.*

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_path_module.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
