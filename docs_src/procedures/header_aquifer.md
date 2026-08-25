---
kind: procedure
symbol: header_aquifer
title: header_aquifer
status: filled
source_hash: fc354b569cfe758a
version_label: SWAT+ 62.0.0
uses:
  aquifer_module: aquifer_module provides the shared aquifer header structures `aqu_hdr` and
    `aqu_hdr_units`. This routine writes those structures directly into every aquifer output
    file, so the module supplies the column names and units being emitted.
  basin_module: basin_module provides the basin name, program label, and print-code switches
    that control whether aquifer headers are written for daily, monthly, yearly, and average-annual
    outputs. Its `pco` flags determine which files are opened, and `bsn%name` and `prog` are
    written as file identification lines.
  hydrograph_module: hydrograph_module provides `sp_ob%aqu`, the aquifer object count used
    as a guard before any aquifer output files are opened. If no aquifer objects exist, this
    routine skips the corresponding header writes entirely.
  output_path_module: output_path_module matters because `open_output_file` is the routine
    called here, and it uses that module’s path-resolution helper to open the output files
    in the configured output directory. Without it, the header files would not be created
    at the correct path.
---

<!-- facts:header -->

Writes aquifer output file headers for day, month, year, and average annual reporting. It opens the needed files only when aquifer outputs are enabled and aquifer objects exist.

## Bottom Line

header_aquifer prepares the header rows for all aquifer output streams. For each enabled reporting period, it opens the matching text file and, when CSV output is enabled, the matching CSV file, then writes basin/program identification plus aquifer column labels and units.

It also logs the created output filenames to unit 9000. The routine matters because downstream aquifer reporting depends on these header rows being present before any daily, monthly, yearly, or average-annual values are written.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `proc_open` after the general output setup has already been performed by `output_landscape_init`. Its job is to open aquifer-specific files and emit their headers before later model execution writes aquifer results into those files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether aquifer objects exist. | The routine only proceeds with aquifer header output when `sp_ob%aqu > 0`, so it skips all aquifer file creation if there are no aquifer spatial objects in the simulation. |
| 2. Open and label the daily text file when requested. | If `pco%aqu%d` is enabled, the routine opens `aquifer_day.txt` on unit 2520, writes the basin name and program line, writes aquifer headers and units, and logs the filename on unit 9000. |
| 3. Open and label the daily CSV file when CSV output is enabled. | If `pco%csvout` is `y`, the routine opens `aquifer_day.csv` on unit 2524, writes the basin name and program line, writes the aquifer headers and units in comma-separated form, and logs the filename on unit 9000. |
| 4. Open and label the monthly text file when requested. | If `pco%aqu%m` is enabled, the routine opens `aquifer_mon.txt` on unit 2521, writes the basin name and program line, writes aquifer headers and units, and logs the filename on unit 9000. |
| 5. Open and label the monthly CSV file when CSV output is enabled. | If `pco%csvout` is `y`, the routine opens `aquifer_mon.csv` on unit 2525, writes the basin name and program line, writes the aquifer headers and units in comma-separated form, and logs the filename on unit 9000. |
| 6. Open and label the yearly text file when requested. | If `pco%aqu%y` is enabled, the routine opens `aquifer_yr.txt` on unit 2522, writes the basin name and program line, writes aquifer headers and units, and logs the filename on unit 9000. |
| 7. Open and label the yearly CSV file when CSV output is enabled. | If `pco%csvout` is `y`, the routine opens `aquifer_yr.csv` on unit 2526, writes the basin name and program line, writes the aquifer headers and units in comma-separated form, and logs the filename on unit 9000. |
| 8. Open and label the average-annual text file when requested. | If `pco%aqu%a` is enabled, the routine opens `aquifer_aa.txt` on unit 2523, writes the basin name and program line, writes aquifer headers and units, and logs the filename on unit 9000. |
| 9. Open and label the average-annual CSV file when CSV output is enabled. | If `pco%csvout` is `y`, the routine opens `aquifer_aa.csv` on unit 2527, writes the basin name and program line, writes the aquifer headers and units in comma-separated form, and logs the filename on unit 9000. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:aquifer_module] | `aqu_hdr, aqu_hdr_units` |  |
| [sym:basin_module] | `pco, bsn, prog` | `pco%aqu%d, bsn%name, pco%csvout, pco%aqu%m, pco%aqu%y, pco%aqu%a` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%aqu` |
| [sym:output_path_module] | `get_output_filename, open` | `get_output_filename(filename), full_path, recl_val, iunit` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_aquifer.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_aquifer.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_aquifer' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into per-branch steps for each aquifer period and CSV path so the source-line evidence matches the actual control flow.
- No resolved commits were available in the Git Lineage Evidence section.
- `output_path_module` has no resolved outside references in the packet; the dependency is inferred from `open_output_file` being called here.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
