---
kind: procedure
symbol: open_cb_banner_pair
title: open_cb_banner_pair
status: filled
source_hash: 4af42124746f05c4
version_label: SWAT+ 62.0.0
args:
  u_txt: u_txt is the output unit number for the required plain-text HRU carbon-by-layer file.
    This procedure opens that unit, writes its banner and header, and leaves it ready for
    later data records.
  u_csv: u_csv is the output unit number for the optional CSV HRU carbon-by-layer file. It
    is only used when `pco%csvout` is `"y"`, in which case this routine opens it and writes
    the CSV banner and header.
  fname_txt: fname_txt is the filename passed to `open_output_file` for the text HRU carbon-by-layer
    output. It determines which file path is opened on `u_txt`.
  fname_csv: fname_csv is the filename passed to `open_output_file` for the CSV HRU carbon-by-layer
    output. It determines which file path is opened on `u_csv` when CSV output is enabled.
  banner_msg: banner_msg is the banner text written into each opened file after the basin
    and program names. It customizes the descriptive first line of both output formats.
locals:
  rl: rl is the record-length value passed to `open_output_file` so both output files are
    opened with enough space for the wide carbon-by-layer header and data rows.
---

<!-- facts:header -->

Opens the HRU carbon-by-layer text output file pair and writes their banner and column headers. It also records the chosen filenames in the model's unit-9000 listing output.

## Bottom Line

open_cb_banner_pair prepares one text output file unconditionally and a matching CSV file only when CSV output is enabled. For each file it opens the unit, writes a banner line with the basin name, program name, and supplied message, then writes the carbon-by-layer header that matches the later data rows.

The routine also writes the filenames to unit 9000 so the run log captures which HRU carbon-by-layer outputs were opened. Its work is purely file setup; later carbon-by-layer reporting depends on these files already being open with the correct record length and header format.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `output_landscape_init`, after that initializer has decided which HRU carbon-by-layer outputs are enabled and has supplied the output units, filenames, and banner text. The opened files and headers it creates are then used later when the model writes HRU carbon-by-layer results.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute record length | Sets `rl` to a fixed base size plus space for the three per-layer blocks and two scalar sums so the file opens with enough record length for the wide HRU carbon-by-layer layout. |
| 2. open text file | Opens the required text HRU carbon-by-layer output on `u_txt` using `fname_txt` and the computed record length. |
| 3. write text banner | Writes the basin name, program name, and supplied banner message as the first record in the text output file. |
| 4. write text header | Writes the fixed-width HRU carbon-by-layer column header to the text file, with the non-CSV formatting selected by `.false.`. |
| 5. log text filename | Writes a run-log entry on unit 9000 naming the text HRU output file that was opened. |
| 6. check CSV output flag | Tests `pco%csvout` to decide whether the CSV companion file should be opened and initialized. |
| 7. open CSV file | When CSV output is enabled, opens the companion HRU carbon-by-layer CSV file on `u_csv` using `fname_csv` and the same record length. |
| 8. write CSV banner | Writes the basin name, program name, and banner message to the CSV file as its first record. |
| 9. write CSV header | Writes the CSV-formatted HRU carbon-by-layer header so the file columns match later CSV data rows. |
| 10. log CSV filename | Writes a run-log entry on unit 9000 naming the CSV HRU output file that was opened. |

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
- warning: missing_doc: Procedure 'open_cb_banner_pair' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
