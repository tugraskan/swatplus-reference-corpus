---
kind: procedure
symbol: header_wetland
title: header_wetland
status: filled
source_hash: 9a3631ea08d7eb1e
version_label: SWAT+ 62.0.0
uses:
  basin_module: The routine uses `basin_module` for the basin identifier and output-control
    flags that decide which wetland headers to emit. `bsn%name` and `prog` are written at
    the top of each file, while `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a`, and `pco%csvout`
    gate the daily, monthly, yearly, average-annual, and CSV branches.
  reservoir_module: This routine is part of the reservoir/wetland output header setup, and
    the reservoir module is imported because the wetland header procedure belongs to that
    reservoir-output family. The packet does not resolve specific reservoir_module symbols
    used here, so its role can only be confirmed at the module level from the source imports
    and section labels.
  hydrograph_module: The hydrograph module provides the header structures that are actually
    written into the wetland files. `ch_wbod_hdr`, `hyd_stor_hdr`, `hyd_in_hdr`, `hyd_out_hdr`,
    `ch_wbod_hdr_units`, and `hyd_hdr_units3` supply the column names and unit labels for
    the text and CSV header rows.
  output_path_module: This module matters because `header_wetland` relies on `open_output_file`
    to create each target file on the correct output path before writing header records. The
    helper also applies the record length argument used for these output units.
---

<!-- facts:header -->

Opens wetland/reservoir header files and writes the basin name plus column headers for daily, monthly, yearly, and average annual wetland outputs.

## Bottom Line

`header_wetland` prepares the header records for wetland/reservoir output files. For each enabled print interval in `pco%res` it opens the matching text file, writes the basin name and program string, then writes the header labels and units from `hydrograph_module`.

If `pco%csvout` is enabled, it also opens the matching CSV file and writes comma-separated header rows. Each file path is recorded to unit 9000 with a `RES_WET` label so the model’s output catalog can track which wetland files were created.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during output initialization, as called from `proc_open`, after the global print codes and output-path machinery have been set up. It prepares the wetland/reservoir header files that later day, month, year, and average-annual simulations will append data to.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check daily wetland output control | The routine first tests `pco%res%d` to see whether daily reservoir/wetland output is enabled. If so, it opens `wetland_day.txt` on unit 2548, writes the basin/program identification, writes the wetland header names and units, and, when `pco%csvout` is enabled, opens `wetland_day.csv` on unit 2552 and writes the same information in CSV form. |
| 2. Check monthly wetland output control | The routine tests `pco%res%m` and, if monthly output is enabled, opens `wetland_mon.txt` on unit 2549, writes the basin/program line, writes the header names and units, and conditionally opens `wetland_mon.csv` on unit 2553 for comma-separated header records. |
| 3. Check yearly wetland output control | The routine tests `pco%res%y` and, if yearly output is enabled, opens `wetland_yr.txt` on unit 2550, writes the basin/program line, writes the header names and units, and conditionally opens `wetland_yr.csv` on unit 2554 for CSV header records. |
| 4. Check average-annual wetland output control | The routine tests `pco%res%a` and, if average-annual output is enabled, opens `wetland_aa.txt` on unit 2551, writes the basin/program line and the header records, and conditionally opens `wetland_aa.csv` on unit 2555 for CSV output. |
| 5. Return to caller | After finishing the enabled output branches, the routine returns to `proc_open` without changing any modeled hydrologic state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%res%d, bsn%name, pco%csvout, pco%res%m, pco%res%y, pco%res%a` |
| [sym:reservoir_module] | `reservoir_module` |  |
| [sym:hydrograph_module] | `ch_wbod_hdr, hyd_stor_hdr, hyd_in_hdr, hyd_out_hdr, ch_wbod_hdr_units, hyd_hdr_units3` |  |
| [sym:output_path_module] | `output_path_module` | `open_output_file` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_wetland.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_wetland.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_wetland' has no extracted documentation comment.
- No resolved lineage commits for header_wetland.f90:1-77.
- reservoir_module symbols were not resolved in the packet; only the module import and reservoir/wetland section labels support its inclusion.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
