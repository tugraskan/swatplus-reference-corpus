---
kind: procedure
symbol: header_reservoir
title: header_reservoir
status: filled
source_hash: cb676c865367993d
version_label: SWAT+ 62.0.0
uses:
  basin_module: The basin module supplies the print-control flags that decide which reservoir
    intervals are active, the basin name and program label that are written into every output
    header, and the `csvout` switch that controls whether CSV companions are created. Without
    `pco`, `bsn%name`, and `prog`, this routine would not know what files to open or what
    identification lines to write.
  reservoir_module: The reservoir module is used by the subroutine import list, but the provided
    evidence packet did not resolve any concrete symbols from it for this routine. Based on
    the source shown here, the routine's visible behavior depends on basin, hydrograph, and
    output-path state, not on a named reservoir-module component.
  hydrograph_module: The hydrograph module provides the reservoir object count that gates
    all reservoir output (`sp_ob%res`) and the header/type variables that are written to each
    file. Those shared header records define the columns and units for reservoir day, month,
    year, and average-annual outputs.
  output_path_module: The output-path module matters because `open_output_file` is the routine
    used to create each output file on the correct path. This subroutine relies on that helper
    to translate the filename into a full path and open the unit before any header lines are
    written.
---

<!-- facts:header -->

Opens reservoir output files and writes their header rows for daily, monthly, yearly, and average-annual reservoir outputs.

## Bottom Line

`header_reservoir` sets up reservoir output files before the model starts writing time-series results. It checks the reservoir print flags in `pco%res` and only opens the daily, monthly, yearly, or average-annual outputs when reservoirs exist (`sp_ob%res > 0`).

For each enabled interval, it opens a text file and, when `pco%csvout == 'y'`, a CSV companion file, then writes basin/program identifiers and header/unit rows for the reservoir channel/waterbody and storage/inflow/outflow variables. It also records the created filenames to the shared output listing on unit 9000.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during output setup, called from `proc_open` after earlier header routines have prepared other model output files. It depends on basin print settings and reservoir object counts being initialized first, and its results determine whether the reservoir simulation later has open text and CSV files ready for writing daily, monthly, yearly, and average-annual records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether reservoir outputs should be created. | The routine tests each reservoir print interval flag together with `sp_ob%res > 0` so it only creates reservoir outputs when reservoirs exist in the spatial setup and the selected interval is enabled. |
| 2. Open and initialize the daily text file. | When daily reservoir output is enabled, it opens `reservoir_day.txt` on unit 2540 and writes the basin/program line, the reservoir header line, and the corresponding units line. It also records the file name on unit 9000. |
| 3. Optionally open and initialize the daily CSV file. | If CSV output is enabled, it opens `reservoir_day.csv` on unit 2544, writes the same basin/program identification line, then writes comma-delimited header and units rows, and logs the CSV filename to unit 9000. |
| 4. Open and initialize the monthly text file. | When monthly reservoir output is enabled, it opens `reservoir_mon.txt` on unit 2541 and writes the basin/program line, the reservoir header line, and the units line. It also records the file name on unit 9000. |
| 5. Optionally open and initialize the monthly CSV file. | If CSV output is enabled, it opens `reservoir_mon.csv` on unit 2545, writes the basin/program line, then writes comma-delimited header and units rows, and logs the CSV filename on unit 2545. |
| 6. Open and initialize the yearly text file. | When yearly reservoir output is enabled, it opens `reservoir_yr.txt` on unit 2542 and writes the basin/program line, the reservoir header line, and the units line. It also records the file name on unit 9000. |
| 7. Optionally open and initialize the yearly CSV file. | If CSV output is enabled, it opens `reservoir_yr.csv` on unit 2546, writes the basin/program line, then writes comma-delimited header and units rows, and logs the CSV filename on unit 9000. |
| 8. Open and initialize the average-annual text file. | When average-annual reservoir output is enabled, it opens `reservoir_aa.txt` on unit 2543 and writes the basin/program line, the reservoir header line, and the units line. It also records the file name on unit 9000. |
| 9. Optionally open and initialize the average-annual CSV file. | If CSV output is enabled, it opens `reservoir_aa.csv` on unit 2547, writes the basin/program line, then writes comma-delimited header and units rows, and logs the CSV filename on unit 9000. |
| 10. Return to the caller. | After the enabled files and headers are written, the subroutine returns to the initialization workflow in `proc_open`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%res%d, bsn%name, pco%csvout, pco%res%m, pco%res%y, pco%res%a` |
| [sym:reservoir_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:hydrograph_module] | `sp_ob, res, ch_wbod_hdr, hyd_stor_hdr, hyd_in_hdr, hyd_out_hdr, ch_wbod_hdr_units, hyd_hdr_units3` | `sp_ob%res` |
| [sym:output_path_module] | `No candidate outside references were resolved to this module.` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_reservoir.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_reservoir.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `16e54aa` (2024-07-05) — BB 61.0.1
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_reservoir' has no extracted documentation comment.
- algorithm_steps revised: split the original two-step sketch into ten source-backed steps to match the conditional branches and file-writing sequence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
