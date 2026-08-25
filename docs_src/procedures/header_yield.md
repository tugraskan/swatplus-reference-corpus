---
kind: procedure
symbol: header_yield
title: header_yield
status: filled
source_hash: cee4631f29090780
version_label: SWAT+ 62.0.0
uses:
  basin_module: basin_module provides the print-control flags and basin metadata that decide
    whether yield files are opened and what header text is written. `pco%mgtout`, `pco%csvout`,
    and `pco%crop_yld` gate the branches, while `bsn%name`, `prog`, and `bsn_yld_hdr` supply
    the identifying records written into the basin crop-yield files.
  hydrograph_module: hydrograph_module contributes `sp_ob%hru`, which is used as the availability
    check for HRU-based crop-yield reporting. If there are no HRUs, the basin crop-yield files
    are not opened because there is no landscape object base to report.
  output_path_module: output_path_module matters because it supplies the file-opening routine
    used here to create the output files with the requested record length and path handling.
---

<!-- facts:header -->

Opens and labels yield output files for management and basin crop-yield reporting.

## Bottom Line

header_yield is a small output-header routine. It opens the yield output files when the relevant print codes request them, then writes identifying header lines to the general output log so downstream files can be traced by name.

It also prepares basin crop-yield annual and average-annual files when HRU objects exist and crop-yield output is enabled. Those files receive a basin name/program line and a shared yield-header record before later code appends simulation results.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the opening sequence in `proc_open`, after the broader output system has been initialized and before later headers and simulation writers need their destination files. `proc_open` calls it as part of the header-writing block, so its job is to create and label the yield-related files early enough that later crop-yield reporting can append to them safely.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether management output is enabled. | If `pco%mgtout` is `y`, the routine begins the yield-output branch; otherwise it skips the yield file setup entirely. |
| 2. Open the main yield file and log it. | Creates unit 4700 for `yield.out` and writes a banner line to unit 9000 so the output log records that the file exists. |
| 3. Optionally open the CSV yield file and log it. | If `pco%csvout` is `y`, creates unit 4701 for `yield.csv` and writes the corresponding banner line to unit 9000. |
| 4. Check whether basin crop-yield output is allowed. | Only when HRUs exist (`sp_ob%hru > 0`) and crop-yield output is requested (`pco%crop_yld` is `y` or `b`) does the routine continue into basin crop-yield file setup. |
| 5. Open the annual basin crop-yield file and write its headers. | Creates unit 5100 for `basin_crop_yld_yr.txt`, writes the basin name and program identifier, writes the yield header record, and logs the file name to unit 9000. |
| 6. Open the average-annual basin crop-yield file and write its headers. | Creates unit 5101 for `basin_crop_yld_aa.txt`, writes the basin name and program identifier, writes the same header record, and logs the file name to unit 9000. |
| 7. Return to the caller. | Ends the subroutine after the header files have been opened and labeled. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog, bsn_yld_hdr` | `pco%mgtout, pco%csvout, pco%crop_yld, bsn%name` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:output_path_module] | `output_path_module::open_output_file` | `open_output_file` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_yield.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `504d2b3` (2025-12-11, "Align Use statements and adjusting whitespace."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_yield.f90` are listed.

- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `374c54c` (2025-12-04) — make crop_yld output to respect print.prt option
- `16e54aa` (2024-07-05) — BB 61.0.1
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_yield' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
