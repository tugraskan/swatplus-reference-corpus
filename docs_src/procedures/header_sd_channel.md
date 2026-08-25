---
kind: procedure
symbol: header_sd_channel
title: header_sd_channel
status: filled
source_hash: edc57f3760c17bb1
version_label: SWAT+ 62.0.0
uses:
  sd_channel_module: 'This module owns the header objects that are written here: `sdch_hdr_subday`,
    `sdch_hdr_units_sub`, `sdch_hdr`, `sdch_hdr_units`, `sdch_bud_hdr`, and `sdch_bud_hdr_units`.
    `header_sd_channel` does not construct these values itself; it serializes the module-defined
    label and units records into each output file.'
  basin_module: This module supplies the basin-level print controls and identifying metadata
    that decide which files to create and what program/basin banner to write at the top of
    each file. `pco%sd_chan%d`, `%m`, `%y`, `%a`, and `%csvout` gate the output branches,
    while `bsn%name` and `prog` become the header banner text written to every opened file.
  hydrograph_module: This module owns the channel and hydrology header records that are written
    to the daily, monthly, yearly, and average-annual SWAT-DEG channel files. `sp_ob%chandeg`
    is also the object-count gate that prevents channel-specific output from being written
    when no SWAT-DEG channel object exists.
  output_path_module: '`output_path_module` matters because `header_sd_channel` uses `open_output_file`
    to create each output unit on the correct full path before writing header records. That
    routine resolves the filename and performs the `open`, so this subroutine can focus on
    populating the file contents.'
---

<!-- facts:header -->

Writes SWAT-DEG channel header records for subdaily, daily, monthly, yearly, average-annual, and budget outputs.

## Bottom Line

`header_sd_channel` opens the channel output files that are enabled by the basin print codes and writes the appropriate header rows for each SWAT-DEG channel result file. It covers both plain-text and CSV variants, and it distinguishes channel morphology outputs from channel budget outputs.

The routine is called during output initialization, after basin and object-print settings are available, so later channel simulations can append data with consistent column labels and units.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_open`, which is the output-setup workflow that calls the various header-writing routines after the model has loaded basin print controls and object counts. Its results are the header lines that later SWAT-DEG channel output routines append data beneath, so the file structure and units are established before any time-step results are written.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether SWAT-DEG channel objects exist and whether subdaily output is enabled. | The routine first gates all channel output on `sp_ob%chandeg > 0`, then enters the subdaily branch only if `pco%sd_chan%d` is 'y' and `time%step > 1`. |
| 2. Open and label the subdaily text file when subdaily output is active. | It opens `channel_sd_subday.txt` on unit 2508, writes the basin/program banner, writes `sdch_hdr_subday` and `sdch_hdr_units_sub`, and records the file name on unit 9000. |
| 3. Optionally write the subdaily CSV file. | If CSV output is enabled, it opens `channel_sd_subday.csv` on unit 4814 and writes the same subdaily header and units records in CSV-friendly form, then logs the file name on unit 9000. |
| 4. Open and label the daily channel text and optional CSV files. | The routine opens `channel_sd_day.txt`, writes the basin/program banner and the channel water-body and hydrology header/unit rows, then logs the file name; if CSV output is enabled, it also opens `channel_sd_day.csv` and writes the same content with CSV formatting. |
| 5. Open and label the monthly channel text and optional CSV files. | If monthly output is enabled, it opens `channel_sd_mon.txt`, writes the banner and daily hydrology headers, and logs the file name; if CSV output is enabled, it also opens `channel_sd_mon.csv` and writes the CSV-formatted header rows. |
| 6. Open and label the yearly channel text and optional CSV files. | If yearly output is enabled, it opens `channel_sd_yr.txt`, writes the banner and hydrology headers, and logs the file name; if CSV output is enabled, it also opens `channel_sd_yr.csv` and writes the CSV-formatted header rows. |
| 7. Open and label the average-annual channel text and optional CSV files. | If average-annual output is enabled, it opens `channel_sd_aa.txt`, writes the banner and hydrology headers, and logs the file name; if CSV output is enabled, it also opens `channel_sd_aa.csv` and writes the CSV-formatted header rows. |
| 8. Open and label the daily channel-morphology text and optional CSV files. | When channel morphology output is enabled for the day interval, it opens `channel_sdmorph_day.txt`, writes the banner plus `sdch_hdr` and `sdch_hdr_units`, and logs the file name; the CSV branch opens `channel_sdmorph_day.csv` and writes the same morphology headers in CSV form. |
| 9. Open and label the monthly channel-morphology text and optional CSV files. | If monthly morphology output is enabled, it opens `channel_sdmorph_mon.txt`, writes the banner and morphology headers, and logs the file name; if CSV output is enabled, it also opens `channel_sdmorph_mon.csv` and writes the CSV-formatted rows. |
| 10. Open and label the yearly channel-morphology text and optional CSV files. | If yearly morphology output is enabled, it opens `channel_sdmorph_yr.txt`, writes the banner and morphology headers, and logs the file name; if CSV output is enabled, it also opens `channel_sdmorph_yr.csv` and writes the CSV-formatted rows. |
| 11. Open and label the average-annual channel-morphology text and optional CSV files. | If average-annual morphology output is enabled, it opens `channel_sdmorph_aa.txt`, writes the banner and morphology headers, and logs the file name; if CSV output is enabled, it also opens `channel_sdmorph_aa.csv` and writes the CSV-formatted rows. |
| 12. Open and label the daily channel budget text and optional CSV files. | When daily budget output is enabled, it opens `sd_chanbud_day.txt`, writes the banner and budget headers, and logs the file name; if CSV output is enabled, it also opens `sd_chanbud_day.csv` and writes the CSV-formatted budget headers. |
| 13. Open and label the monthly, yearly, and average-annual channel budget files. | The routine repeats the same pattern for `sd_chanbud_mon.txt`/`.csv`, `sd_chanbud_yr.txt`/`.csv`, and `sd_chanbud_aa.txt`/`.csv`: open the file, write the basin/program banner, write the budget header and unit rows, and log the filename on unit 9000. |
| 14. Return after all enabled header files have been initialized. | After the conditional output branches finish, the subroutine returns to its caller with all enabled SWAT-DEG channel header files opened and populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sdch_hdr_subday, sdch_hdr_units_sub, sdch_hdr, sdch_hdr_units, sdch_bud_hdr, sdch_bud_hdr_units` |  |
| [sym:basin_module] | `pco, bsn, prog` | `pco%sd_chan%d, bsn%name, pco%csvout, pco%sd_chan%m, pco%sd_chan%y, pco%sd_chan%a` |
| [sym:hydrograph_module] | `sp_ob, ch_wbod_hdr, hyd_stor_hdr, hyd_in_hdr, hyd_out_hdr, wtmp_hdr, ch_wbod_hdr_units, hyd_hdr_units3, hyd_hdr_units1, wtmp_units` | `sp_ob%chandeg` |
| [sym:output_path_module] | `open_output_file` | `open_output_file` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_sd_channel.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_sd_channel.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `406df33` (2025-12-04) — fix creation of empty file when daily channel output is disabled in print.prt
- `f1e61a3` (2024-10-08) — fixed tabs
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_sd_channel' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
