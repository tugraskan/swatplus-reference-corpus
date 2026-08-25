---
kind: procedure
symbol: header_const
title: header_const
status: filled
source_hash: da3bfa3b827460ff
version_label: SWAT+ 62.0.0
uses:
  basin_module: This module supplies the basin-level print codes, basin name, program name,
    and constituent header definitions that control which output files are opened and what
    header content is written. `header_const` reads the `pco%cs_*` flags to decide whether
    each basin, HRU, aquifer, channel, reservoir, or routing-unit constituent file should
    be created, and it writes `bsn%name`, `prog`, and the header structures into those files.
  reservoir_module: This module provides the reservoir and wetland constituent header structure
    that `header_const` writes to the reservoir/wetland output files. Those files need the
    header symbol from `reservoir_module` so the output columns match the reservoir-related
    constituent variables reported later in the run.
  hydrograph_module: This module provides `sp_ob`, which tells `header_const` whether aquifer,
    channel, reservoir, and routing-unit objects exist in the model. The routine uses those
    object counts to avoid opening output files for object types that are not present, even
    if print flags are enabled.
  constituent_mass_module: This module provides `cs_db%num_cs`, the guard that disables all
    constituent header output when no constituents are simulated. The routine also uses `rucsb_hdr`
    from this module to write the routing-unit constituent column header line.
  ch_cs_module: This module defines `chcs_hdr`, the channel constituent header record written
    into the channel output files. `header_const` uses it to print the column names for channel
    constituent fluxes and state variables in text and CSV formats.
  res_cs_module: This module defines `rescs_hdr`, the reservoir/wetland constituent header
    record written into the reservoir and wetland output files. `header_const` uses it so
    those files share the correct column labels for reservoir and wetland state and flux variables.
  cs_module: This module defines the basin balance header `csb_hdr` and the HRU header `cs_hdr_hru`
    that `header_const` writes into basin and HRU constituent files. Those structures carry
    the exact output column labels for the basin balance and HRU constituent summaries.
  cs_aquifer: This module defines `cs_hdr_aqu`, the aquifer constituent header record written
    into aquifer output files. `header_const` uses it to label aquifer fluxes, storage, and
    concentration fields consistently across daily, monthly, yearly, and average-annual outputs.
  output_path_module: This module supplies the file-opening helper that turns a logical filename
    into a real output file path and opens the unit. `header_const` relies on it for every
    constituent output file so the file locations and record lengths are handled consistently
    by the output-path system.
---

<!-- facts:header -->

Initializes constituent output files and header records for basin, HRU, aquifer, channel, reservoir, routing-unit, and wetland outputs.

## Bottom Line

`header_const` is the SWAT+ constituent-output setup routine. It checks the configured print flags and the number of simulated constituents, then opens the corresponding text and optional CSV files and writes each file's descriptive header rows before simulation output begins.

The routine matters because later constituent reporting depends on these files already being open with the correct labels, units, and record layout. It also suppresses output for object types that are not present, such as aquifer, channel, reservoir, or routing-unit output when the corresponding spatial object count is zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model's output-file setup phase, after `proc_open` has already opened other header files and before `header_write` continues the output initialization sequence. Its results are then used by the constituent simulation itself, which expects the relevant output units to exist and already contain the descriptive header rows before time-stepping starts.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check basin constituent output flags and constituent count. | The routine begins each basin constituent branch by testing the requested print interval flag in `pco%cs_basin` and requiring `cs_db%num_cs > 0` so it only writes basin constituent headers when constituents are actually simulated. |
| 2. Open and populate basin constituent header files. | For daily, monthly, yearly, and average-annual basin output, it opens the corresponding text file and writes the basin name, program name, descriptive title, unit definitions, constituent-flux labels, and finally `csb_hdr`. |
| 3. Check HRU constituent output flags and constituent count. | The HRU branches are gated the same way, using `pco%cs_hru` and `cs_db%num_cs > 0` so HRU constituent files are only created when they are requested and meaningful. |
| 4. Open and populate HRU constituent text and CSV headers. | For each HRU period, it opens the text file, writes the title and unit definitions, writes `cs_hdr_hru`, and, when `pco%csvout == 'y'`, opens the matching CSV file and writes the CSV header line. |
| 5. Check whether aquifers exist before writing aquifer output. | Aquifer constituent output is nested inside `if (sp_ob%aqu > 0)` so the routine only creates aquifer files when the model actually contains aquifer objects. |
| 6. Open and populate aquifer constituent text and CSV headers. | For daily, monthly, yearly, and average-annual aquifer outputs, it opens the corresponding files, writes aquifer titles and variable definitions, writes `cs_hdr_aqu`, and optionally writes CSV headers when CSV output is enabled. |
| 7. Check whether channels exist before writing channel output. | Channel constituent output is only prepared when `sp_ob%chandeg > 0`, which prevents channel files from being opened in models without SWAT-DEG channels. |
| 8. Open and populate channel constituent text and CSV headers. | For each channel reporting period, it opens the text file, writes the channel title and flux definitions, writes `chcs_hdr`, and optionally writes a CSV file using the same header structure. |
| 9. Check whether reservoirs exist before writing reservoir output. | Reservoir and wetland constituent output is gated by `sp_ob%res > 0` so these files are only produced when reservoir objects are present in the model. |
| 10. Open and populate reservoir constituent text and CSV headers. | For daily, monthly, yearly, and average-annual reservoir outputs, it opens the corresponding files, writes reservoir titles and variable definitions, writes `rescs_hdr`, and optionally writes reservoir CSV headers. |
| 11. Check whether routing units exist before writing routing-unit output. | Routing-unit output is only prepared when `sp_ob%ru > 0`, so the routine skips these files in models without routing-unit objects. |
| 12. Open and populate routing-unit constituent text and CSV headers. | For each routing-unit reporting period, it opens the text file, writes the routing-unit flux definitions, writes `rucsb_hdr`, and optionally writes the CSV version with the same header line. |
| 13. Reuse reservoir output flags for wetland output and write wetland headers. | Wetland output is handled under the reservoir object check, using `pco%cs_res` to decide whether to create wetland daily, monthly, yearly, or average-annual files and writing `rescs_hdr` into each one, with optional CSV support. |
| 14. Return after all eligible files have been opened and initialized. | After completing the conditional header writes, the routine exits and leaves the opened output units ready for later time-step writes. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, prog` | `pco%cs_basin%d, bsn%name, pco%cs_basin%m, pco%cs_basin%y, pco%cs_basin%a, pco%cs_hru%d, pco%csvout, pco%cs_hru%m, pco%cs_hru%y, pco%cs_hru%a, pco%cs_aqu%d, pco%cs_aqu%m, pco%cs_aqu%y, pco%cs_aqu%a, pco%cs_chn%d, pco%cs_chn%m, pco%cs_chn%y, pco%cs_chn%a, pco%cs_res%d, pco%cs_res%m, pco%cs_res%y, pco%cs_res%a, pco%cs_ru%d, pco%cs_ru%m, pco%cs_ru%y, pco%cs_ru%a` |
| [sym:reservoir_module] | `rescs_hdr` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%aqu, sp_ob%chandeg, sp_ob%res, sp_ob%ru` |
| [sym:constituent_mass_module] | `cs_db, rucsb_hdr` | `cs_db%num_cs` |
| [sym:ch_cs_module] | `chcs_hdr` |  |
| [sym:res_cs_module] | `rescs_hdr` |  |
| [sym:cs_module] | `csb_hdr, cs_hdr_hru` |  |
| [sym:cs_aquifer] | `cs_hdr_aqu` |  |
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

`header_const.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_const.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_const' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps to cover the full routine flow.
- Source ownership for `reservoir_module` and `output_path_module` is uncertain from the available candidate refs; description is based on the visible use sites and imported helper contract.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
