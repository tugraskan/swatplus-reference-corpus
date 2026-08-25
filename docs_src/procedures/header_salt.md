---
kind: procedure
symbol: header_salt
title: header_salt
status: filled
source_hash: 14c248fc8be6d1b3
version_label: SWAT+ 62.0.0
uses:
  basin_module: The basin print-code flags in pco decide whether each basin, HRU, aquifer,
    channel, reservoir, routing-unit, and wetland salt file should be opened, and bsn%name
    and prog provide the identifying label written at the top of each file. cs_db%num_salts
    gates every branch so headers are only produced when salt ions are actually being simulated.
  reservoir_module: The reservoir salt header record supplies the named columns written into
    reservoir and wetland salt output files, so header_salt needs it to label the reservoir/wetland
    time-series records consistently.
  hydrograph_module: sp_ob tells header_salt whether aquifer, channel, reservoir, and routing-unit
    object types exist in the model. Those counts guard the corresponding output blocks so
    the routine only opens files for object classes that are present.
  constituent_mass_module: cs_db%num_salts is the simulation-wide switch for salt constituents,
    so it prevents any salt header file from being opened when no salts are defined. rusaltb_hdr
    provides the routing-unit salt column names written to the routing-unit output files.
  ch_salt_module: chsalt_hdr contains the channel-salt column header structure that is written
    after the descriptive text in the channel output files.
  res_salt_module: ressalt_hdr contains the reservoir-salt column header structure that is
    written after the descriptive text in the reservoir and wetland output files.
  salt_module: saltb_hdr and salt_hdr_hru provide the basin and HRU salt header records that
    are written into the basin and HRU output files after the text descriptions.
  salt_aquifer: salt_hdr_aqu provides the aquifer-salt header record written into the aquifer
    output files after the descriptive text.
  output_path_module: open_output_file is the shared I/O helper used to create and open each
    named results file on a fixed unit number before header text is written.
---

<!-- facts:header -->

Builds the salt output file headers and opens the corresponding output files when salt reporting is enabled.

## Bottom Line

header_salt is a setup routine for salt results files. It checks the configured print intervals and the number of salt ions simulated, then opens the basin, HRU, aquifer, channel, reservoir, routing-unit, and wetland output files and writes each file's title, units/definitions, and column header record.

It matters because later model runs write time-series salt results into these pre-opened units using the header layouts prepared here. If salt is not being simulated or a given output class is disabled, the routine skips that file entirely.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model startup from proc_open, after the general output framework has been initialized and before simulation output begins. proc_open calls it once the other header routines have been scheduled, and the opened units and written headers are then used later when the model writes salt results during the run.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether each salt output class is enabled and whether salts exist. | For each basin, HRU, aquifer, channel, reservoir, routing-unit, and wetland branch, the routine tests the corresponding pco%salt_* interval flag and cs_db%num_salts > 0, and for some object classes also checks sp_ob counts such as aqu, chandeg, res, and ru before proceeding. |
| 2. Open the basin salt files and write their title and header text. | When basin salt output is enabled, the routine opens the day, month, year, and average-annual basin files, writes bsn%name and prog, prints a human-readable description of basin salt fluxes and units, and ends each section by writing saltb_hdr. |
| 3. Open the HRU salt files and write their title and header text, including optional CSV files. | For each HRU interval, the routine opens the text output file, writes the basin name and program label, emits the HRU salt variable descriptions, writes salt_hdr_hru, and when pco%csvout is enabled also opens the matching CSV file and writes the same column header in comma-delimited form. |
| 4. Open the aquifer salt files and write their title and header text, including optional CSV files. | If aquifers exist and the aquifer salt interval is enabled, the routine opens the aquifer day, month, year, and average-annual files, writes basin/program identifiers, prints aquifer salt descriptions and units, writes salt_hdr_aqu, and optionally creates the CSV companion files. |
| 5. Open the channel salt files and write their title and header text, including optional CSV files. | If channel objects exist, the routine opens the channel day, month, year, and average-annual files, writes the text descriptions for inflow, outflow, seepage, irrigation, diversion, storage, and concentration, writes chsalt_hdr, and creates CSV files when requested. |
| 6. Open the reservoir salt files and write their title and header text, including optional CSV files. | If reservoirs exist, the routine opens the reservoir day, month, year, and average-annual files, writes the reservoir salt descriptions and units, writes ressalt_hdr, and optionally creates CSV files for the same header layout. |
| 7. Open the routing-unit salt files and write their title and header text, including optional CSV files. | If routing units exist, the routine opens the routing-unit day, month, year, and average-annual files, writes the routing-unit salt descriptions and units, writes rusaltb_hdr, and optionally opens CSV companions with the same header record. |
| 8. Open the wetland salt files and write their title and header text, including optional CSV files. | If wetland output is enabled, the routine opens the wetland day, month, year, and average-annual files, writes the wetland salt descriptions and units, writes ressalt_hdr, and optionally opens CSV companions for the wetland header record. |
| 9. Return to the caller. | After all enabled header files are opened and initialized, the routine exits without producing any computational result other than the prepared output files. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%salt_basin%d, bsn%name, pco%salt_basin%m, pco%salt_basin%y, pco%salt_basin%a, pco%salt_hru%d, pco%csvout, pco%salt_hru%m, pco%salt_hru%y, pco%salt_hru%a, pco%salt_aqu%d, pco%salt_aqu%m, pco%salt_aqu%y, pco%salt_aqu%a, pco%salt_chn%d, pco%salt_chn%m, pco%salt_chn%y, pco%salt_chn%a, pco%salt_res%d, pco%salt_res%m, pco%salt_res%y, pco%salt_res%a, pco%salt_ru%d, pco%salt_ru%m, pco%salt_ru%y, pco%salt_ru%a, pco%salt_wet%d, pco%salt_wet%m, pco%salt_wet%y, pco%salt_wet%a` |
| [sym:reservoir_module] | `ressalt_hdr` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%aqu, sp_ob%chandeg, sp_ob%res, sp_ob%ru` |
| [sym:constituent_mass_module] | `cs_db, rusaltb_hdr` | `cs_db%num_salts` |
| [sym:ch_salt_module] | `chsalt_hdr` |  |
| [sym:res_salt_module] | `ressalt_hdr` |  |
| [sym:salt_module] | `saltb_hdr, salt_hdr_hru` |  |
| [sym:salt_aquifer] | `salt_hdr_aqu` |  |
| [sym:output_path_module] | `open_output_file` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_salt.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 9 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_salt.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_salt' has no extracted documentation comment.
- algorithm_steps revised: replaced the two draft steps with nine source-backed stages that follow the routine's actual branch structure and output classes.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
