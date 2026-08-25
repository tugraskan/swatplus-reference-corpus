---
kind: procedure
symbol: header_snutc
title: header_snutc
status: filled
source_hash: 93da705377237ddb
version_label: SWAT+ 62.0.0
uses:
  hydrograph_module: This module supplies `sp_ob%hru`, which is the guard used to decide whether
    HRU-related output should be initialized at all. If no HRUs exist, the HRU output files
    are not opened.
  soil_nutcarb_module: This module provides the header and unit records that are written into
    the output files. `header_snutc` uses these derived types to emit the column names and
    units for the carbon summaries.
  output_path_module: '`output_path_module` matters because it owns `open_output_file`, which
    resolves and opens the named output files on the proper path. It also provides the basin/program
    context (`bsn%name` and `prog`) that is written as the first record in each file.'
---

<!-- facts:header -->

Opens and initializes three carbon output files for HRU and basin reporting.

## Bottom Line

When the simulation has HRU output capacity, `header_snutc` opens the soil-carbon output files and writes their identifying header records. It does this for HRU organic carbon, HRU total carbon, and basin total carbon outputs.

The routine does not compute carbon values itself; it prepares the file streams and metadata so later code can append time-step data in the correct files and with the correct column labels and units.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during output-file setup, before carbon results are written for HRU or basin reporting. Its inputs are prepared by the broader model state: `sp_ob%hru` indicates whether HRU outputs should be enabled, `bsn%name` and `prog` identify the run, and the carbon header/unit structures come from `soil_nutcarb_module`. Later reporting code depends on these files being open and pre-seeded with header records before it appends data rows.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether HRU output is enabled. | The routine tests `sp_ob%hru > 0` to determine whether the HRU-oriented carbon output setup should be performed. |
| 2. Open and seed the HRU organic-carbon file. | It opens `hru_orgc.txt` on unit 2610 with record length 800, writes the basin/program identification line, writes the `HRU_ORGC` file tag to the output listing on unit 9000, and writes the organic-carbon header and units records from `orgc_hdr` and `orgc_units`. |
| 3. Open and seed the HRU total-carbon file. | It opens `hru_totc.txt` on unit 2611 with record length 800, then writes the basin/program identification line, the `HRU_TOTC` file tag, and the total-carbon header and units records from `totc_hdr` and `totc_units`. |
| 4. Open and seed the basin total-carbon file. | It opens `basin_totc.txt` on unit 2613 with record length 800, then writes the basin/program identification line, the `BSN_TOTC` file tag, and the total-carbon header and units records from `totc_hdr` and `totc_units`. |
| 5. Return to the caller. | The subroutine exits after the output files have been prepared. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:soil_nutcarb_module] | `orgc_hdr, orgc_units, totc_hdr, totc_units` |  |
| [sym:output_path_module] | `open_output_file, bsn, prog` | `open_output_file; bsn%name; prog` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_snutc.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `504d2b3` (2025-12-11, "Align Use statements and adjusting whitespace."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_snutc.f90` are listed.

- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_snutc' has no extracted documentation comment.
- algorithm_steps revised: split the original two-step draft into explicit file-setup phases for the three output files, plus the return step, to match the source line structure.
- The source shows the HRU guard only on line 10; the later two file blocks are not guarded in the active code because their `if` statements are commented out.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
