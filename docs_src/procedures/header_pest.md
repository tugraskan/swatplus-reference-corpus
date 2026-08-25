---
kind: procedure
symbol: header_pest
title: header_pest
status: filled
source_hash: c0cc4d2d93d26dde
version_label: SWAT+ 62.0.0
uses:
  basin_module: '`basin_module` provides the basin name, program identifier, and print-control
    flags that gate every pesticide header branch. `header_pest` uses `bsn%name` and `prog`
    as file-identifying metadata, and it reads `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a`,
    and `pco%csvout` to decide whether daily, monthly, yearly, average-annual, and CSV pesticide
    outputs should be opened and written.'
  reservoir_module: '`reservoir_module` is used for reservoir-related pesticide output support.
    `header_pest` opens reservoir pesticide header files, and the reservoir module is the
    source of the reservoir pesticide header/state definitions needed for those records.'
  hydrograph_module: '`hydrograph_module` matters because `sp_ob` carries the spatial object
    counts that decide whether HRU, channel, reservoir, and aquifer pesticide output branches
    run at all. `header_pest` uses `sp_ob%hru`, `sp_ob%chandeg`, `sp_ob%res`, and `sp_ob%aqu`
    as existence checks before opening the corresponding header files.'
  output_ls_pesticide_module: '`output_ls_pesticide_module` provides `pestb_hdr`, the HRU
    and basin land-surface pesticide header record written into the pesticide output files.
    `header_pest` calls it when creating the HRU and basin land-surface pesticide headers
    so the resulting files have the correct column labels.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_tot`, which indicates
    whether any constituents are being simulated. `header_pest` uses that count to suppress
    pesticide output file creation when there are no simulated constituents.'
  ch_pesticide_module: '`ch_pesticide_module` provides `chpest_hdr`, the channel pesticide
    header record written to channel and basin-channel pesticide files. `header_pest` needs
    it to populate the channel pesticide header rows in the opened files.'
  res_pesticide_module: '`res_pesticide_module` provides `respest_hdr`, the reservoir pesticide
    header record written to reservoir and basin-reservoir pesticide files. `header_pest`
    uses it so those outputs start with the correct reservoir pesticide column names.'
  aqu_pesticide_module: '`aqu_pesticide_module` provides `aqupest_hdr`, the aquifer pesticide
    header record written to basin aquifer and aquifer pesticide files. `header_pest` writes
    this header so the aquifer pesticide outputs are labeled consistently with the simulated
    aquifer variables.'
  output_path_module: '`output_path_module` matters because it supplies the file-opening helper
    that resolves each relative output filename to a full path before the file is opened.
    `header_pest` relies on that behavior indirectly through `open_output_file` so its pesticide
    headers are written to the configured output directory.'
---

<!-- facts:header -->

Opens and writes pesticide output headers for HRU, channel, reservoir, aquifer, and basin-level pesticide reports. It creates the text and optional CSV header files only for active spatial objects and configured print intervals.

## Bottom Line

`header_pest` is the header-writing setup routine for all pesticide output streams. It checks which spatial object groups exist and which pesticide print intervals are enabled, then opens the corresponding output files and writes the basin name, program tag, and the appropriate pesticide column header record to each file.

It matters because later pesticide simulations depend on these files already being created with consistent headers. When CSV output is enabled, it also creates matching `.csv` files and registers each file name in the output listing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_open` calls `header_pest` during the model output initialization sequence, after other header routines have already prepared their own output files and before `header_write` finishes the shared header setup. The routine depends on upstream initialization of basin print settings, simulated object counts, and pesticide header structures; its results are then used whenever the model writes pesticide time-series or summary outputs later in the run.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether HRU pesticide outputs are applicable. | The routine first tests whether any HRUs exist and whether pesticide outputs are enabled for daily, monthly, yearly, or average-annual intervals, along with at least one simulated constituent. |
| 2. Open and seed HRU pesticide files. | When the daily HRU branch is active, it opens the HRU pesticide text file, writes the basin/program identifiers, writes the output registration line, and writes the HRU pesticide header. If CSV output is enabled, it opens the matching CSV file and writes the same identification and header content in CSV form. |
| 3. Repeat HRU header creation for monthly, yearly, and average-annual outputs. | The routine performs the same open-and-header sequence for the monthly, yearly, and average-annual HRU pesticide files, creating matching CSV files when requested. |
| 4. Check whether channel pesticide outputs are applicable. | The routine tests whether channel objects exist and whether pesticide outputs are enabled for the selected intervals with simulated constituents present. |
| 5. Open and seed channel pesticide files. | It opens the channel pesticide text files, writes the basin/program identifiers and channel pesticide header, and creates the optional CSV variants with the same header data. |
| 6. Check whether reservoir pesticide outputs are applicable. | The routine tests whether reservoir objects exist and whether pesticide outputs are enabled for the current intervals with simulated constituents present. |
| 7. Open and seed reservoir pesticide files. | It opens the reservoir pesticide text files, writes the basin/program identifiers and reservoir pesticide header, and writes matching CSV files when CSV output is enabled. |
| 8. Check whether basin aquifer pesticide outputs are applicable. | The routine tests whether aquifer objects exist and whether pesticide outputs are enabled for the current intervals with simulated constituents present. |
| 9. Open and seed basin aquifer pesticide files. | It opens the basin aquifer pesticide text files, writes the basin/program identifiers and aquifer pesticide header, and creates CSV counterparts when requested. |
| 10. Check whether aquifer pesticide outputs are applicable. | The routine again tests for aquifer objects and enabled pesticide output intervals before writing aquifer-specific files. |
| 11. Open and seed aquifer pesticide files. | It opens the aquifer pesticide text files, writes the basin/program identifiers and aquifer pesticide header, and generates optional CSV files with the same header content. |
| 12. Check whether basin channel pesticide outputs are applicable. | The routine tests whether channel objects exist and whether the basin-level channel pesticide outputs are enabled for the selected intervals with simulated constituents present. |
| 13. Open and seed basin channel and basin reservoir pesticide files, then basin land-surface pesticide files. | It opens the basin channel and basin reservoir pesticide files, writes their headers and CSV variants, and then does the same for basin land-surface pesticide files using the land-surface pesticide header. |
| 14. Return to the caller after all eligible header files are initialized. | The routine finishes without modifying simulation state beyond the opened output files and their initial header records. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%pest%d, bsn%name, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:reservoir_module] | `sp_ob` | `sp_ob%res, sp_ob%aqu` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%chandeg, sp_ob%res, sp_ob%aqu` |
| [sym:output_ls_pesticide_module] | `pestb_hdr` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_tot` |
| [sym:ch_pesticide_module] | `chpest_hdr` |  |
| [sym:res_pesticide_module] | `respest_hdr` |  |
| [sym:aqu_pesticide_module] | `aqupest_hdr` |  |
| [sym:output_path_module] | `full-path resolution helper used by open_output_file` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_pest.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_pest.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_pest' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
