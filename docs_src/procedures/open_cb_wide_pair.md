---
kind: procedure
symbol: open_cb_wide_pair
title: open_cb_wide_pair
status: filled
source_hash: 78a888349df571bb
version_label: SWAT+ 62.0.0
args:
  u_txt: Unit number for the text output file. This routine opens that unit, writes the banner
    and header to it, and always uses it regardless of the CSV setting.
  u_csv: Unit number for the CSV output file. This unit is only opened and written when `pco%csvout
    == "y"`.
  fname_txt: Name of the text output file to open through `open_output_file`, using the computed
    record length `rl`.
  fname_csv: Name of the CSV output file to open if CSV output is enabled, using the same
    computed record length `rl`.
  var_names: Array of variable base names used by `cb_write_wide_header` to build the per-layer
    column labels for the wide file format.
locals:
  rl: Record length passed to `open_output_file`; it is sized to fit the identifier columns
    plus the depth columns and one per-layer block for each requested variable.
---

<!-- facts:header -->

Opens a pair of wide per-layer carbon output files and writes their headers. The text file is always opened; the CSV file is opened only when CSV output is enabled.

## Bottom Line

This subroutine prepares the hru_n_p_pool_stat output pair for carbon/nutrient pool reporting. It computes a record length that can hold the fixed ID columns plus one depth block per layer and one block per requested variable, then opens the text file and writes its banner and column header.

If `pco%csvout == "y"`, it repeats the same setup for the CSV file. In both cases it also writes a file label to unit 9000 so the run’s output inventory records which HRU file was opened.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `output_landscape_init` while the model is setting up HRU carbon and nutrient pool outputs. `output_landscape_init` decides whether each period’s files should exist and passes the corresponding units, file names, and variable-name list; later output routines depend on these files already being open with the correct wide-column header layout.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. open text file | Open the text output unit with the computed record length so the wide per-layer file can be written safely. |
| 2. write text banner | Write the basin name and program tag to the text file as its banner line. |
| 3. write text header | Emit the wide column header row for the text file using the supplied variable names and text formatting. |
| 4. log text file | Record the HRU text filename on unit 9000 for the output file inventory. |
| 5. check csv option | Test whether CSV output is enabled before preparing the CSV side of the pair. |
| 6. open csv file | Open the CSV output unit with the same record length when CSV output is requested. |
| 7. write csv banner | Write the basin name and program tag to the CSV file as its banner line. |
| 8. write csv header | Emit the wide column header row for the CSV file using the supplied variable names and CSV formatting. |
| 9. log csv file | Record the HRU CSV filename on unit 9000 for the output file inventory. |

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
- warning: missing_doc: Procedure 'open_cb_wide_pair' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
