---
kind: procedure
symbol: header_path
title: header_path
status: filled
source_hash: 9871c94e9f9a8819
version_label: SWAT+ 62.0.0
uses:
  basin_module: This routine depends on `basin_module` for the print-control flags that decide
    whether each HRU pathogen file should be created (`pco%wb_hru%d`, `%m`, `%y`, `%a`) and
    whether CSV companions should be written (`pco%csvout`). It also uses the basin name (`bsn%name`)
    and program label (`prog`) as the first header line in every output file, so the files
    are identifiable in downstream output processing.
  reservoir_module: The source `use reservoir_module` appears in the procedure scope, but
    the extracted lines do not reference any reservoir_module symbols. It matters only as
    an imported dependency for the compilation context, not for any visible behavior in this
    routine.
  output_ls_pathogen_module: '`output_ls_pathogen_module` provides `pathb_hdr`, the header
    record written into each HRU pathogen output file after the basin/program line. That header
    defines the pathogen balance columns that downstream readers expect in the file body.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_tot`, the guard
    that determines whether any pathogen output is produced at all. The routine only opens
    and labels files when at least one constituent is being simulated.'
  output_path_module: The source imports `output_path_module` because it contains `open_output_file`,
    the helper used to open each output unit with the requested record length before headers
    are written.
---

<!-- facts:header -->

Opens and writes the headers for HRU pathogen output files at daily, monthly, yearly, and average-annual intervals. It creates both text and optional CSV headers when HRU pathogen output is enabled and constituents are present.

## Bottom Line

`header_path` is a file-header setup routine for HRU pathogen output. For each enabled reporting interval, it opens the corresponding output file, writes a basin/program banner line, writes the `pathb_hdr` column header, and records the file name on unit 9000 so the output manager knows which HRU_PATH file was created.

If CSV output is enabled, it also opens a matching `.csv` file and writes the same identifying header content in CSV-friendly form. The routine only acts when `cs_db%num_tot > 0`, so it suppresses pathogen output entirely when no constituents are being simulated.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model/open-file initialization, when `proc_open` calls it after the other header setup routines. `proc_open` has already prepared the shared basin print controls and program labels, and the files opened here must exist before later HRU pathogen simulation output can append data records to them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether daily HRU pathogen output should be produced. | The routine starts the daily block and only continues when daily HRU output is enabled in `pco%wb_hru%d` and at least one constituent exists in `cs_db%num_tot`. |
| 2. Open the daily text file and write its headers. | It opens unit 2790 on `hru_path_day.txt`, writes the basin/program identification line, writes the `pathb_hdr` column header, and records the file name on unit 9000. |
| 3. Optionally create the daily CSV file. | When `pco%csvout` is enabled, it opens unit 2794 on `hru_path_day.csv`, writes the same basin/program identifier, writes the header in CSV format, and logs the CSV file name on unit 9000. |
| 4. Check whether monthly HRU pathogen output should be produced. | The routine begins the monthly block and only continues when monthly HRU output is enabled in `pco%wb_hru%m` and at least one constituent exists in `cs_db%num_tot`. |
| 5. Open the monthly text file and write its headers. | It opens unit 2791 on `hru_path_mon.txt`, writes the basin/program identification line, writes the `pathb_hdr` column header, and records the file name on unit 9000. |
| 6. Optionally create the monthly CSV file. | When `pco%csvout` is enabled, it opens unit 2795 on `hru_path_mon.csv`, writes the same basin/program identifier, writes the header in CSV format, and logs the CSV file name on unit 9000. |
| 7. Check whether yearly HRU pathogen output should be produced. | The routine begins the yearly block and only continues when yearly HRU output is enabled in `pco%wb_hru%y` and at least one constituent exists in `cs_db%num_tot`. |
| 8. Open the yearly text file and write its headers. | It opens unit 2792 on `hru_path_yr.txt`, writes the basin/program identification line, writes the `pathb_hdr` column header, and records the file name on unit 9000. |
| 9. Optionally create the yearly CSV file. | When `pco%csvout` is enabled, it opens unit 2796 on `hru_path_yr.csv`, writes the same basin/program identifier, writes the header in CSV format, and logs the CSV file name on unit 9000. |
| 10. Check whether average-annual HRU pathogen output should be produced. | The routine begins the average-annual block and only continues when average-annual HRU output is enabled in `pco%wb_hru%a` and at least one constituent exists in `cs_db%num_tot`. |
| 11. Open the average-annual text file and write its headers. | It opens unit 2793 on `hru_path_aa.txt`, writes the basin/program identification line, writes the `pathb_hdr` column header, and records the file name on unit 9000. |
| 12. Optionally create the average-annual CSV file. | When `pco%csvout` is enabled, it opens unit 2797 on `hru_path_aa.csv`, writes the same basin/program identifier, writes the header in CSV format, and logs the CSV file name on unit 9000. |
| 13. Return to the caller. | The subroutine exits after all enabled headers have been emitted. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%wb_hru%d, bsn%name, pco%csvout, pco%wb_hru%m, pco%wb_hru%y, pco%wb_hru%a` |
| [sym:reservoir_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:output_ls_pathogen_module] | `pathb_hdr` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_tot` |
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

`header_path.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_path.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_path' has no extracted documentation comment.
- No resolved lineage commits were available for this source span.
- output_path_module is used only for `open_output_file` in the extracted lines; no other symbols from that module were resolved here.
- reservoir_module is imported but no symbols from it were referenced in the extracted source lines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
