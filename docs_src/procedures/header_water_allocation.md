---
kind: procedure
symbol: header_water_allocation
title: header_water_allocation
status: filled
source_hash: 9f251ff605e81193
version_label: SWAT+ 62.0.0
uses:
  maximum_data_module: The routine gates all water-allocation header output on `db_mx%wallo_db
    > 0`, so the `maximum_data_module` flag controls whether any of these files are produced
    at all.
  water_allocation_module: The `water_allocation_module` provides the header data structures
    being written, `wallo_hdr` and `wallo_hdr_units`, so it supplies the row contents for
    every output file.
  basin_module: The `basin_module` supplies the basin name, program identifier, and print-code
    switches that determine which water-allocation files are opened and what identification
    lines are written into them.
  output_path_module: The `output_path_module` matters because it provides `open_output_file`,
    which resolves the output path and opens each report unit before the header writes occur.
---

<!-- facts:header -->

Writes water-allocation output headers for daily, monthly, yearly, and average-annual reports. It opens the needed text and optional CSV files and records basin name, program name, and header labels.

## Bottom Line

`header_water_allocation` prepares the header rows for water-allocation output files. When water-allocation database output is enabled, it opens the configured day, month, year, and average-annual report files and writes basin/program identification plus the header label and unit lines.

For each enabled print interval, it also writes a line to `unit_9000` naming the corresponding water-allocation file so the run log or master output listing reflects which reports were created. If CSV output is enabled through `pco%csvout`, it opens and writes a matching `.csv` header file alongside the `.txt` file.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_open`, after the basin print configuration and water-allocation header data have been set up. Its job is to create the header records for any enabled water-allocation outputs so later simulation code can append results to already-open files with the correct labels and units.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether water-allocation database output is enabled. | The routine first tests `db_mx%wallo_db > 0`; if that database/output element is not enabled, none of the water-allocation headers are written. |
| 2. Emit the daily text header when daily output is requested. | If `pco%water_allo%d == 'y'`, it opens unit 3110 for `water_allo_day.txt`, writes the basin/program line, the header labels, and the header units, then writes a log line to unit 9000 naming the text file. |
| 3. Emit the daily CSV header when CSV output is enabled. | If `pco%csvout == 'y'`, it opens unit 3114 for `water_allo_day.csv`, writes the basin/program line and comma-separated header and units rows, then logs the CSV filename to unit 9000. |
| 4. Emit the monthly text header when monthly output is requested. | If `pco%water_allo%m == 'y'`, it opens unit 3111 for `water_allo_mon.txt`, writes the basin/program line, the header labels, and the header units, then logs the text file name to unit 9000. |
| 5. Emit the monthly CSV header when CSV output is enabled. | If `pco%csvout == 'y'`, it opens unit 3115 for `water_allo_mon.csv`, writes the basin/program line and comma-separated header and units rows, then logs the CSV filename to unit 9000. |
| 6. Emit the yearly text header when yearly output is requested. | If `pco%water_allo%y == 'y'`, it opens unit 3112 for `water_allo_yr.txt`, writes the basin/program line, the header labels, and the header units, then logs the text file name to unit 9000. |
| 7. Emit the yearly CSV header when CSV output is enabled. | If `pco%csvout == 'y'`, it opens unit 3116 for `water_allo_yr.csv`, writes the basin/program line and comma-separated header and units rows, then logs the CSV filename to unit 9000. |
| 8. Emit the average-annual text header when average-annual output is requested. | If `pco%water_allo%a == 'y'`, it opens unit 3113 for `water_allo_aa.txt`, writes the basin/program line, the header labels, and the header units, then logs the text file name to unit 9000. |
| 9. Emit the average-annual CSV header when CSV output is enabled. | If `pco%csvout == 'y'`, it opens unit 3117 for `water_allo_aa.csv`, writes the basin/program line and comma-separated header and units rows, then logs the CSV filename to unit 9000. |
| 10. Return to caller after the header files are prepared. | The subroutine ends with a plain return after all requested output headers have been written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wallo_db` |
| [sym:water_allocation_module] | `wallo_hdr, wallo_hdr_units` |  |
| [sym:basin_module] | `pco, bsn, prog` | `pco%water_allo%d, bsn%name, pco%csvout, pco%water_allo%m, pco%water_allo%y, pco%water_allo%a` |
| [sym:output_path_module] | `get_output_filename, open, file, recl` | `get_output_filename, open_output_file` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_water_allocation.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_water_allocation.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_water_allocation' has no extracted documentation comment.
- Source shows no explicit close/rewind operations; it only opens report units and writes header records.
- output_path_module reference is inferred from the imported open_output_file routine and its path-resolution helper.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
