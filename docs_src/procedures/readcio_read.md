---
kind: procedure
symbol: readcio_read
title: readcio_read
status: filled
source_hash: 5d18878d7c338940
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the first line from `file.cio`, which is read and discarded as a title/header
    record before the file-name records are processed.
  name: Temporary label field read from each `file.cio` record before the associated module
    variable is filled; it holds the left-hand token on each line.
  out_path_value: Buffers the output-path text parsed from the output-path record in `file.cio`
    so it can be passed to `init_output_path`.
  line_buffer: Captures the full raw output-path line so the routine can trim and split it
    manually, preserving spaces in the path value.
  eof: I/O status flag for the repeated reads from unit 107; negative values signal end-of-file
    and stop the scan early.
  idx: Holds the position of the first blank after the output-path label so the code can slice
    out the remainder of the line as the path value.
  i_exist: Logical result of `inquire(file="file.cio", exist=i_exist)`; it decides whether
    the routine attempts to open and read `file.cio` at all.
  i: Loop counter for the bounded `do i = 1, 31` scan through the expected `file.cio` records.
uses:
  input_file_module: The many `input_file_module` variables are the destination state for
    the records read from `file.cio`; this routine populates them so the rest of the model
    knows which named input files to open for simulation, basin, climate, routing, management,
    soil, and weather-path data.
  output_path_module: '`output_path_module` matters because `readcio_read` passes the parsed
    output-path text into `init_output_path`, which sets the shared `out_path` used by later
    output-file construction and directory handling.'
---

<!-- facts:header -->

Reads `file.cio` to load the model's configured input-file names and optional weather/output paths. It also initializes the shared output-path state used by later file-opening routines.

## Bottom Line

`readcio_read` is the startup routine that opens `file.cio`, skips the title line, and reads the configured file names into the shared `input_file_module` variables such as `in_sim`, `in_basin`, `in_cli`, and the rest of the model input-file selectors. It also reads the output-path line, parses the path text after the label, and stores that result for output-path setup.

After the `file.cio` records are loaded, the routine closes the file and calls `init_output_path(out_path_value)` from `output_path_module`. That makes the output directory/path available to later basin initialization and file-opening code that depends on the shared output-path state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs near the start of basin setup, before later file-opening and initialization work in `proc_bsn`. `proc_bsn` calls it first so the shared file-name variables and output-path state are ready before diagnostics, output files, and other basin inputs are opened.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Test whether file.cio exists | The routine checks for `file.cio` with `inquire` and only proceeds with parsing if the file is present. |
| 2. Open file.cio and skip the title line | It opens unit 107 on `file.cio` and reads the first record into `titldum` so the rest of the records can be treated as configuration data. |
| 3. Loop through the configured file-name records | Inside the bounded loop, the routine reads each labeled record from `file.cio` into `name` plus the appropriate shared input-file variable, stopping early if end-of-file is reached. |
| 4. Read and parse the output-path line | It reads the whole output-path record as text, trims leading blanks, finds the first separator blank, and extracts the remainder into `out_path_value`; if no value is available, it clears the path string. |
| 5. Close the configuration file | After scanning completes, the routine closes unit 107 to finish the `file.cio` access. |
| 6. Initialize the shared output path | It calls `init_output_path(out_path_value)` so the shared output-path module state is normalized and ready for later output-file creation. |
| 7. Return to caller | The subroutine returns after the file-name and output-path setup is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_sim, in_basin, in_cli, in_con, in_cha, in_res, in_ru, in_hru, in_exco, in_rec, in_delr, in_aqu, in_herd, in_watrts, in_link, in_hyd, in_str, in_parmdb, in_ops, in_lum, in_chg, in_init, in_sol, in_cond, in_regs, in_path_pcp, in_path_tmp, in_path_slr, in_path_hmd, in_path_wnd` |  |
| [sym:output_path_module] | `out_path, init_output_path` | `out_path` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`readcio_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `9299ca5` (2025-12-04, "allow specifying output directory"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `readcio_read.f90` are listed.

- `9299ca5` (2025-12-04) — allow specifying output directory
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'readcio_read' has no extracted documentation comment.
- No Git lineage commits were resolved for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
