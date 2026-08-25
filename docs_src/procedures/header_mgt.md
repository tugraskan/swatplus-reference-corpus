---
kind: procedure
symbol: header_mgt
title: header_mgt
status: filled
source_hash: ba7247eda1c98148
version_label: SWAT+ 62.0.0
uses:
  basin_module: The `basin_module` supplies the print switch `pco%mgtout`, the basin identifier
    `bsn%name`, the program label `prog`, and the header record templates `mgt_hdr` and `mgt_hdr_unt1`.
    Those values control whether the file is written and what header text is emitted.
  output_path_module: '`output_path_module` provides `open_output_file`, which resolves the
    output path and opens unit 2612 with the requested record length. `header_mgt` depends
    on that module to create the management output file in the correct location before writing
    header records.'
---

<!-- facts:header -->

Writes the management output file header when management output is enabled. It opens `mgt_out.txt` and records basin, program, and header lines that label the file contents.

## Bottom Line

`header_mgt` is a small output setup routine for SWAT+ management reporting. When the basin print code `pco%mgtout` is set to `"y"`, it opens the management output file and writes the basin name, program name, and two header records so the file can be interpreted downstream.

The routine matters because it prepares the `mgt.out`/`mgt_out.txt` header at the start of an output workflow. Later management-output routines rely on this file being open and pre-labeled before they append detailed records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during output-file initialization, after `proc_open` starts assembling the suite of header writers for model outputs. `proc_open` calls it after other header routines and before later output routines append content, so the management file exists and is labeled before management results are written.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Check the basin management print code `pco%mgtout`. Only if it is set to `"y"` does the routine create and populate the management output header. |
| 2. call | Open unit 2612 on `mgt_out.txt` with record length 800 by calling `open_output_file`. This prepares the management output file for sequential header writes. |
| 3. io | Write the basin name and program name to unit 2612 so the management file starts with identifying information. |
| 4. io | Write the `mgt_hdr` header record to unit 2612 as the next line of the management file header. |
| 5. io | Write the `mgt_hdr_unt1` header record to unit 2612 to complete the formatted management header block. |
| 6. io | Write a label line to unit 9000 indicating that `mgt_out.txt` has been created for management output. |
| 7. return | Return to the caller after the optional header writes are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog, mgt_hdr, mgt_hdr_unt1` | `pco%mgtout, bsn%name` |
| [sym:output_path_module] | `get_output_filename, open` | `get_output_filename(filename), full_path, recl_val, iunit` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_mgt.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `504d2b3` (2025-12-11, "Align Use statements and adjusting whitespace."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_mgt.f90` are listed.

- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `54a9d44` (2024-08-12) — NP_flow.f90 - Subroutine NP_FLOW REMOVED
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_mgt' has no extracted documentation comment.
- No resolved lineage commits were available for this source span.
- output_path_module appears only through `open_output_file`; the raw source shows `get_output_filename` and `open`, but no additional candidate outside references were resolved there.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
