---
kind: procedure
symbol: header_cs
title: header_cs
status: filled
source_hash: 26295ab98cc2bf27
version_label: SWAT+ 62.0.0
locals:
  ipest: Loop index for pesticide constituent arrays when writing pesticide header records.
  ipath: Loop index for pathogen constituent arrays when writing pathogen header records.
  imet: Loop index for heavy-metal constituent arrays when writing metal header records.
  isalt: Loop index for salt constituent arrays when writing salt header records.
uses:
  hydrograph_module: The hydrology control flags decide which daily, monthly, yearly, and
    average-annual header files are opened, while the basin name and program name are written
    into every file header. The csin_hyd_hdr and csout_hyd_hdr records, together with the
    per-constituent arrays, provide the actual header content that labels each constituent
    output stream.
  constituent_mass_module: The constituent-mass database supplies the simulated counts for
    pests, pathogens, metals, and salts. header_cs uses those counts to decide whether each
    constituent category should be written and how many array elements to include in the header
    records.
  output_path_module: The output-path module matters because open_output_file comes from it
    and is used to create each output unit on the correct SWAT+ output path. That path handling
    is what makes the header files land in the model's configured output directory instead
    of the working directory.
---

<!-- facts:header -->

Opens and writes SWAT+ hydrology constituent header files for pesticide, pathogen, metal, and salt outputs. It creates text and optional CSV headers for daily, monthly, yearly, and average annual HYDIN/HYDOUT streams.

## Bottom Line

header_cs is a file-header routine for SWAT+ constituent hydrology outputs. It checks the configured hydrology output flags and the simulated constituent counts, then opens the matching output units and writes the basin/program header plus the appropriate constituent header records.

It matters because the downstream hydrology constituent files need these header lines before any time-series records are written. The routine covers both input-side HYDIN files and output-side HYDOUT files, with optional CSV mirrors when CSV output is enabled.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at the start of the hydrology constituent output setup, after upstream code has populated pco, bsn, prog, cs_db, and the constituent header arrays. Its results are the opened output files with their header lines, which later hydrology output routines depend on when they append the actual daily or aggregated records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether daily hydrology constituent headers should be produced. | The routine starts the HYDIN daily branch only when the daily hydrology flag is enabled. |
| 2. Write daily pesticide HYDIN headers when pesticides are simulated. | If at least one pesticide is active, the routine opens the daily pesticide text file, writes the basin/program line and the pesticide header record, and writes the CSV version when CSV output is enabled. |
| 3. Write daily pathogen HYDIN headers when pathogens are simulated. | If at least one pathogen is active, the routine opens the daily pathogen text file, writes the basin/program line and the pathogen header record, and optionally writes the CSV mirror. |
| 4. Write daily heavy-metal HYDIN headers when metals are simulated. | If at least one heavy metal is active, the routine opens the daily metal text file, writes the basin/program line and the metal header record, and optionally writes the CSV mirror. |
| 5. Write daily salt HYDIN headers when salts are simulated. | If at least one salt is active, the routine opens the daily salt text file, writes the basin/program line and the salt header record, and optionally writes the CSV mirror. |
| 6. Check whether monthly hydrology constituent headers should be produced. | The routine starts the HYDIN monthly branch only when the monthly hydrology flag is enabled. |
| 7. Write monthly pesticide HYDIN headers when pesticides are simulated. | If at least one pesticide is active, the routine opens the monthly pesticide text file, writes the basin/program line and the pesticide header record, and optionally writes the CSV mirror. |
| 8. Write monthly pathogen HYDIN headers when pathogens are simulated. | If at least one pathogen is active, the routine opens the monthly pathogen text file, writes the basin/program line and the pathogen header record, and optionally writes the CSV mirror. |
| 9. Write monthly heavy-metal HYDIN headers when metals are simulated. | If at least one heavy metal is active, the routine opens the monthly metal text file, writes the basin/program line and the metal header record, and optionally writes the CSV mirror. |
| 10. Write monthly salt HYDIN headers when salts are simulated. | If at least one salt is active, the routine opens the monthly salt text file, writes the basin/program line and the salt header record, and optionally writes the CSV mirror. |
| 11. Check whether yearly hydrology constituent headers should be produced. | The routine starts the HYDIN yearly branch only when the yearly hydrology flag is enabled. |
| 12. Write yearly pesticide, pathogen, metal, and salt HYDIN headers when each category is simulated. | Within the yearly branch, the routine opens each active constituent file, writes the basin/program line and the matching header record, and optionally writes the CSV mirror for each category. |
| 13. Check whether average-annual hydrology constituent headers should be produced, then write HYDIN outputs for active constituents. | When average-annual output is enabled, the routine opens each active HYDIN file, writes the basin/program line and the matching header record, and optionally writes the CSV mirror for each constituent category. |
| 14. Write daily, monthly, yearly, and average-annual HYDOUT headers for active constituents. | The routine repeats the same file-opening and header-writing pattern for the HYDOUT files, using the output header type for each active constituent category and the configured text or CSV unit. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `pco%hyd%d, pco%hyd%m, pco%hyd%y, pco%hyd%a, pco%csvout, bsn%name, prog, csin_hyd_hdr, csout_hyd_hdr, cs_pest_solsor(ipest), cs_path_solsor(ipath), cs_hmet_solsor(imet), cs_salt_solsor(isalt)` | `pco%hyd%d, pco%hyd%m, pco%hyd%y, pco%hyd%a, pco%csvout, bsn%name, prog, csin_hyd_hdr, csout_hyd_hdr, cs_pest_solsor(ipest), cs_path_solsor(ipath), cs_hmet_solsor(imet), cs_salt_solsor(isalt)` |
| [sym:constituent_mass_module] | `cs_db, cs_pest_solsor, cs_path_solsor, cs_hmet_solsor, cs_salt_solsor, csin_hyd_hdr, csout_hyd_hdr` | `cs_db%num_pests, cs_db%num_paths, cs_db%num_metals, cs_db%num_salts` |
| [sym:output_path_module] | `pco%hyd%d, pco%hyd%m, pco%hyd%y, pco%hyd%a, pco%csvout, bsn%name, prog` | `pco%hyd%d, pco%hyd%m, pco%hyd%y, pco%hyd%a, pco%csvout, bsn%name, prog` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

One source-backed lineage commit was resolved for header_cs. The initial addition in 504d2b3 introduced the subroutine, its module uses, the local loop indices, and the full set of HYDIN/HYDOUT header-writing branches for text and CSV outputs.

- 504d2b3 added header_cs as a new subroutine and implemented the output-file opening and header-writing logic for hydrology constituent files across daily, monthly, yearly, and average-annual branches.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_cs' has no extracted documentation comment.
