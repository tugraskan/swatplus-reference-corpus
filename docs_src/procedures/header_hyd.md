---
kind: procedure
symbol: header_hyd
title: header_hyd
status: filled
source_hash: 4a6ab9248351ab25
version_label: SWAT+ 62.0.0
uses:
  basin_module: '`basin_module` supplies the print-control flags that decide which branches
    run (`pco%hydcon`, `pco%csvout`, and the `pco%hyd%d/%m/%y/%a` interval flags). It also
    provides `bsn%name` and `prog`, which are written into each file header so the output
    records identify the basin and model run.'
  hydrograph_module: '`hydrograph_module` provides the reusable header structures that are
    written into the hydrograph output files. The routine uses `hyd_hdr_time`, `hyd_hdr_obj`,
    `hyd_hdr`, `hyd_hdr_units2`, and `hyd_hdr_units` so every opened file gets a consistent
    header layout.'
  output_path_module: '`output_path_module` matters because `header_hyd` does not open files
    directly. It calls `open_output_file` for every enabled output, and that routine uses
    the output-path machinery to resolve the actual destination path before opening the unit.'
---

<!-- facts:header -->

Writes hydrograph header records to the basin output files that are enabled in `pco`. It opens the corresponding text and optional CSV files for hydcon, hydout, hydin, and deposition outputs, then writes standard header rows and a file registry entry for each one.

## Bottom Line

`header_hyd` is the header setup routine for hydrograph-related outputs. It checks the basin print-control flags in `pco` and, for each enabled output period, opens the matching text file and optional CSV file, then writes the basin name, program name, and the header objects from `hydrograph_module`.

It also writes a summary line to unit 9000 for each file that is opened, using the `HYDCON`, `HYDOUT`, `HYDIN`, and `DEPO` tags. That registry output lets the model track which hydrograph files were created during startup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`header_hyd` runs during startup file initialization, after `proc_open` has already begun the broader output setup and after `output_landscape_init` plus several other header routines have run. `proc_open` calls it specifically to create all enabled hydrograph and deposition output files before simulation output begins, so later model components can append records to those units with the expected header format already in place.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether hydrograph connection output is enabled. | If `pco%hydcon` is enabled, open `hydcon.out` on unit 7000 and, when CSV output is enabled too, also open `hydcon.csv` on unit 7001. Record both file names on unit 9000 so the output registry reflects what was created. |
| 2. Build daily hydout outputs when requested. | If `pco%hyd%d` is enabled, open `hydout_day.txt` on unit 2580, write the basin/program identification line, write the time/object/header lines, and register the file on unit 9000. If CSV output is enabled, open `hydout_day.csv` on unit 2584, write the same identification and header content with CSV formatting, and register the CSV file on unit 9000. |
| 3. Build monthly hydout outputs when requested. | If `pco%hyd%m` is enabled, open `hydout_mon.txt` on unit 2581, write the basin/program line and hydrograph headers, and log it on unit 9000. When CSV output is enabled, open `hydout_mon.csv` on unit 2585, write the same headers in CSV form, and log that file too. |
| 4. Build yearly hydout outputs when requested. | If `pco%hyd%y` is enabled, open `hydout_yr.txt` on unit 2582, write the standard hydout headers, and register the file. If CSV output is enabled, open `hydout_yr.csv` on unit 2586, write the CSV header rows, and register it on unit 9000. |
| 5. Build average-annual hydout outputs when requested. | If `pco%hyd%a` is enabled, open `hydout_aa.txt` on unit 2583, write the basin/program and header rows, and register the file. If CSV output is enabled, open `hydout_aa.csv` on unit 2587, write the matching CSV header rows, and register it on unit 9000. |
| 6. Build daily hydin outputs when requested. | If `pco%hyd%d` is enabled, open `hydin_day.txt` on unit 2560, write the basin/program and hyd header rows, and log the file on unit 9000. If CSV output is enabled, open `hydin_day.csv` on unit 2564, write the CSV-formatted header rows, and register it. |
| 7. Build monthly hydin outputs when requested. | If `pco%hyd%m` is enabled, open `hydin_mon.txt` on unit 2561, write the standard header rows, and register the file. If CSV output is enabled, open `hydin_mon.csv` on unit 2565, write the CSV header rows, and log that file. |
| 8. Build yearly hydin outputs when requested. | If `pco%hyd%y` is enabled, open `hydin_yr.txt` on unit 2562, write the standard header rows, and register the file. If CSV output is enabled, open `hydin_yr.csv` on unit 2566, write the CSV header rows, and register it on unit 9000. |
| 9. Build average-annual hydin outputs when requested. | If `pco%hyd%a` is enabled, open `hydin_aa.txt` on unit 2563, write the standard header rows, and register the file. If CSV output is enabled, open `hydin_aa.csv` on unit 2567, write the CSV header rows, and register it. |
| 10. Build daily deposition outputs when requested. | If `pco%hyd%d` is enabled, open `deposition_day.txt` on unit 2700, write the basin/program line and deposition headers, and register it on unit 9000. If CSV output is enabled, open `deposition_day.csv` on unit 2704, write the CSV header rows, and log that file too. |
| 11. Build monthly deposition outputs when requested. | If `pco%hyd%m` is enabled, open `deposition_mon.txt` on unit 2701, write the deposition headers, and register the file. If CSV output is enabled, open `deposition_mon.csv` on unit 2705, write the CSV header rows, and register it on unit 9000. |
| 12. Build yearly deposition outputs when requested. | If `pco%hyd%y` is enabled, open `deposition_yr.txt` on unit 2702, write the deposition headers, and register it. If CSV output is enabled, open `deposition_yr.csv` on unit 2706, write the CSV header rows, and register that file. |
| 13. Build average-annual deposition outputs when requested. | If `pco%hyd%a` is enabled, open `deposition_aa.txt` on unit 2703, write the deposition headers, and register the file. If CSV output is enabled, open `deposition_aa.csv` on unit 2707, write the CSV header rows, and log it on unit 9000. |
| 14. Return to caller. | Finish the subroutine after all enabled output files have been opened and initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%hydcon, pco%csvout, pco%hyd%d, bsn%name, pco%hyd%m, pco%hyd%y, pco%hyd%a` |
| [sym:hydrograph_module] | `hyd_hdr_time, hyd_hdr_obj, hyd_hdr, hyd_hdr_units2, hyd_hdr_units` |  |
| [sym:output_path_module] | `get_output_filename, open_output_file` | `open_output_file opens the named output file on the requested unit using the full path returned by `get_output_filename`; both are needed because `header_hyd` delegates all file opening to this module.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_hyd.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_hyd.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `16e54aa` (2024-07-05) — BB 61.0.1
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_hyd' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps and added the final return step; source lines now cite the visible line-number block.
- No Git lineage commits were resolved for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
