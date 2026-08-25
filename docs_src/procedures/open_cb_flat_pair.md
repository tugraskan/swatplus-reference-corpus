---
kind: procedure
symbol: open_cb_flat_pair
title: open_cb_flat_pair
status: filled
source_hash: 129fc8d2ef0ae1cd
version_label: SWAT+ 62.0.0
args:
  u_txt: '`u_txt` is the already-chosen Fortran unit number for the required text output file.
    The routine opens and writes to that unit unconditionally.'
  u_csv: '`u_csv` is the Fortran unit number reserved for the CSV companion file. The routine
    only opens and writes to this unit when `pco%csvout` is `''y''`.'
  fname_txt: '`fname_txt` supplies the text filename passed to `open_output_file` and is also
    written to unit 9000 as the HRU file label for the text output.'
  fname_csv: '`fname_csv` supplies the CSV filename passed to `open_output_file` and is also
    written to unit 9000 as the HRU file label for the CSV output.'
  var_names: '`var_names` is the ordered list of column names written by `cb_write_flat_header`
    for each output file; it controls the variable header content after the fixed ID columns.'
---

<!-- facts:header -->

Opens a pair of non-layered carbon state output files and writes their identifying headers. It supports optional CSV output, so the same report can be produced in text and CSV formats.

## Bottom Line

`open_cb_flat_pair` initializes one required text output file and, when CSV output is enabled, a matching CSV file for a non-layered carbon state report. It opens each file, writes the run identifiers (`bsn%name`, `prog`), and writes a flat variable header with `cb_write_flat_header`.

It also records the file names to unit 9000 so the model’s file listing/registry reflects the opened HRU carbon state outputs. This routine is used for HRU-level carbon state files that do not include soil-layer suffixes.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`output_landscape_init` calls this routine during output setup, after deciding which HRU carbon-state reports are enabled. It prepares the text file always and the CSV file only when `pco%csvout` is `'y'`; downstream carbon output writes depend on these files and their headers being opened and established first.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. call | Open the required text output file on unit `u_txt` with the given filename and record length 8000. |
| 2. io | Write the basin name and program identifier to the text file so the file records its source run. |
| 3. call | Write the non-layered carbon header to the text file using the supplied variable names and text formatting. |
| 4. io | Record the HRU text filename in unit 9000 as part of the model’s output listing. |
| 5. if | Check whether CSV output is enabled with `pco%csvout == "y"` before creating the companion CSV file. |
| 6. call | Open the companion CSV output file on unit `u_csv` with the given filename and record length 8000. |
| 7. io | Write the basin name and program identifier to the CSV file so the file records its source run. |
| 8. call | Write the non-layered carbon header to the CSV file using comma-separated formatting and the supplied variable names. |
| 9. io | Record the HRU CSV filename in unit 9000 as part of the model’s output listing. |

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

`output_landscape_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 48 non-merge commit(s) since, most recently `6329ff2` (2026-06-05, "Fix carbon.bsn reader and LSU carbon output unit collisions"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `output_landscape_init.f90` are listed.

- `6329ff2` (2026-06-05) — Fix carbon.bsn reader and LSU carbon output unit collisions
- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `821a63e` (2026-06-02) — reinstate CSU outputs and print flags
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `28c64c3` (2026-05-14) — Removed output files no longer needed. hru_soilc_stat hru_rsdc_stat, hru_soilcarb_mb_stat
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'open_cb_flat_pair' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
