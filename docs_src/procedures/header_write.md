---
kind: procedure
symbol: header_write
title: header_write
status: filled
source_hash: 7a3271d39ab54280
version_label: SWAT+ 62.0.0
uses:
  basin_module: The basin module holds the global print-control structure (`pco`) that decides
    which basin-level output families are active, the basin name (`bsn%name`) that is written
    into every file header, and the program label (`prog`) that tags the files. `header_write`
    depends on these values to decide which files to open and to initialize each file with
    the basin identifier and model context.
  aquifer_module: The aquifer module provides the aquifer header and units records that are
    written into every basin aquifer output file. `header_write` uses these derived types
    so the aquifer output files begin with the correct column names and unit labels before
    any simulation values are appended.
  channel_module: The channel module provides the channel header and units records written
    into basin channel output files. `header_write` needs these definitions so the channel
    output files have the expected column layout and unit row for downstream record writing.
  reservoir_module: The reservoir module matters because this routine writes basin reservoir
    output headers, and those headers come from reservoir-specific state definitions. Even
    though the resolved outside-reference list did not identify individual reservoir-module
    symbols for this span, the module is included because basin reservoir output depends on
    reservoir header types being available here.
  hydrograph_module: The hydrograph module supplies the shared hydrologic header structures
    used across recall, routing-unit, basin reservoir, and related outputs. `header_write`
    writes these header objects directly so the output files carry the correct time/object
    labels and unit rows for hydrologic time series and budgets.
  sd_channel_module: The sd_channel_module provides the SWAT-DEG channel morphology and budget
    header structures. `header_write` uses them to initialize the basin SWAT-DEG channel output
    files, ensuring those files carry the correct morphology or budget column labels and units.
  maximum_data_module: The maximum data module matters because this routine opens many fixed-unit
    output files and the model-wide maximum limits govern those file allocations and related
    capacity assumptions. It is included here as a dependency for the output infrastructure
    even though no specific candidate reference from that module was resolved in the extracted
    span.
  calibration_data_module: The calibration data module provides the soft-calibration flags
    that enable the HRU calibration outputs. `header_write` checks `cal_soft`, `cal_codes%hyd_hru`,
    and `cal_codes%plt` to decide whether to create the calibration-related files and whether
    to open the hydrology calibration output stream.
  output_path_module: The output path module matters because `open_output_file` uses it to
    turn each relative filename into a full output path before opening the unit. `header_write`
    relies on that path resolution indirectly for every file it opens.
---

<!-- facts:header -->

Opens and seeds the suite of basin, calibration, and hydrologic output files used by SWAT+ reporting. It writes each file's identifying headers and registers the file path in the output listing when that output is enabled.

## Bottom Line

`header_write` is the central output-file setup routine run during model initialization. It checks the basin print codes and calibration flags, opens the corresponding text/CSV files, and writes the standard header rows that describe the data columns for aquifer, reservoir, recall, channel, SWAT-DEG channel, point-source recall, routing-unit, and soft-calibration outputs.

Its job is not to compute simulation results; it prepares the output destinations and metadata so later parts of the model can stream time-series records into files whose structure is already established. When CSV output is enabled, it opens parallel `.csv` files and writes comma-delimited header records too.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the output-opening phase, after `proc_open` has already set up the broader output/header workflow and before any simulation records are written. `proc_open` calls it after the other header routines so the basin-wide output files are opened and seeded in one place. Later model output writing depends on these file units and header rows being in place so time-series and budget records can be appended with the correct layout.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether each output family is enabled. | The routine tests print codes such as `pco%fdcout`, `cal_soft`, `cal_codes%hyd_hru`, and the basin interval flags (`pco%aqu_bsn`, `pco%res_bsn`, `pco%recall`, `pco%chan_bsn`, `pco%sd_chan_bsn`, `pco%recall_bsn`, `pco%ru`) to decide which files to initialize. |
| 2. Open the flow-duration output if requested. | When `pco%fdcout == 'y'`, it opens `flow_duration_curve.out` on unit 6000, writes the basin name and program label, writes the flow-duration header object, and records the file in unit 9000. |
| 3. Open soft-calibration HRU output if soft calibration is active. | When `cal_soft == 'y'`, it opens `hru-out.cal`, writes the basin/program identifier line, writes `calb_hdr`, and logs the output path to unit 9000. |
| 4. Open calibration-related hydrology files when requested. | If `cal_codes%hyd_hru /= 'n'`, it opens `hru-new.cal`; if `cal_codes%hyd_hru /= 'n' .or. cal_codes%plt == 'y'`, it opens `hydrology-cal.hyd`. |
| 5. Open basin aquifer output files and optional CSV companions. | For each enabled aquifer interval (`d`, `m`, `y`, `a`), it opens the corresponding text file, writes `bsn%name`, `prog`, `aqu_hdr`, and `aqu_hdr_units`, and, when `pco%csvout == 'y'`, opens and seeds the matching CSV file. |
| 6. Open basin reservoir output files and optional CSV companions. | For each enabled reservoir interval, it opens the reservoir output file, writes the basin/program line, writes the water-body, storage, inflow, and outflow headers plus units, and mirrors the same headers into CSV files when CSV output is enabled. |
| 7. Open recall output files and optional CSV companions. | For each enabled recall interval, it opens the recall file, writes `hyd_hdr_time` and `hyd_hdr`, writes `hyd_hdr_units`, and creates the matching CSV file with the same header content if `pco%csvout == 'y'`. |
| 8. Open basin channel output files and optional CSV companions. | For each enabled channel interval, it opens the basin channel file, writes `ch_hdr` and `ch_hdr_units`, and creates the CSV companion file with the same header records when requested. |
| 9. Open basin SWAT-DEG channel output files and optional CSV companions. | For each enabled SWAT-DEG channel interval, it opens the basin SD-channel file, writes the morphology/budget headers from `ch_wbod_hdr`, `hyd_stor_hdr`, `hyd_in_hdr`, `hyd_out_hdr`, and writes the corresponding unit headers, with CSV companions opened and seeded as well. |
| 10. Open basin SWAT-DEG channel morphology output files and optional CSV companions. | For each enabled SD-channel morphology interval, it opens the morphology file, writes `sdch_hdr` and `sdch_hdr_units`, and mirrors those headers into a CSV file when CSV output is enabled. |
| 11. Open basin SWAT-DEG channel budget output files and optional CSV companions. | For each enabled SD-channel budget interval, it opens the budget file, writes `sdch_bud_hdr` and `sdch_bud_hdr_units`, and opens the paired CSV file with the same headers if required. |
| 12. Open basin point-source recall output files and optional CSV companions. | For each enabled basin recall interval, it opens the point-source recall file, writes `rec_hdr_time` and `hyd_hdr` plus `hyd_hdr_units`, and writes the same header set to the CSV version when requested. |
| 13. Open routing-unit output files and optional CSV companions. | For each enabled routing-unit interval, it opens the routing-unit output file, writes `hyd_hdr_time`, `hyd_hdr`, and `hyd_hdr_units`, and creates the CSV companion file with matching headers when CSV output is active. |
| 14. Return to the caller after all selected output files are initialized. | The subroutine exits once all eligible output files have been opened and seeded with their header records. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%fdcout, bsn%name, pco%aqu_bsn%d, pco%csvout, pco%aqu_bsn%m, pco%aqu_bsn%y, pco%aqu_bsn%a, pco%res_bsn%d, pco%res_bsn%m, pco%res_bsn%y, pco%res_bsn%a, pco%recall%d, pco%recall%m, pco%recall%y, pco%recall%a, pco%chan_bsn%d, pco%chan_bsn%m, pco%chan_bsn%y, pco%chan_bsn%a, pco%sd_chan_bsn%d, pco%sd_chan_bsn%m, pco%sd_chan_bsn%y, pco%sd_chan_bsn%a, pco%recall_bsn%d, pco%recall_bsn%m, pco%recall_bsn%y, pco%recall_bsn%a, pco%ru%d, pco%ru%m, pco%ru%y, pco%ru%a` |
| [sym:aquifer_module] | `aqu_hdr, aqu_hdr_units` |  |
| [sym:channel_module] | `ch_hdr, ch_hdr_units` |  |
| [sym:reservoir_module] | `res_hdr, res_hdr_units` | `res_hdr, res_hdr_units` |
| [sym:hydrograph_module] | `fdc_hdr, calb_hdr, ch_wbod_hdr, hyd_stor_hdr, hyd_in_hdr, hyd_out_hdr, ch_wbod_hdr_units, hyd_hdr_units3, hyd_hdr_time, hyd_hdr, hyd_hdr_units, recall, hyd_hdr_units1, rec_hdr_time` |  |
| [sym:sd_channel_module] | `sdch_hdr, sdch_hdr_units, sdch_bud_hdr, sdch_bud_hdr_units` |  |
| [sym:maximum_data_module] | `max_file, max_print, max_run` | `max_file, max_print, max_run` |
| [sym:calibration_data_module] | `cal_codes, cal_soft` | `cal_codes%hyd_hru, cal_codes%plt` |
| [sym:output_path_module] | `get_output_filename, output_directory` | `get_output_filename, output_directory` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_write.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_write.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_write' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps so each major output family is represented separately.
- Some outside-state entries are inferred from surrounding output infrastructure where no resolved candidate reference was available in the extracted span; treat those module-level `outside` identifiers as uncertain.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
