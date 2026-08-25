---
kind: procedure
symbol: gwflow_output_init
title: gwflow_output_init
status: filled
source_hash: 9901381986e9bbe5
version_label: SWAT+ 62.0.0
locals:
  i_exist: Logical existence flag used with `inquire(file='gwflow.wbgroups',exist=i_exist)`
    to decide whether grouped groundwater water-balance output should be initialized.
  in_gw: Input unit number used to open and read `gwflow.wbgroups` when grouped groundwater
    output is configured.
  s: Loop or scratch index declared in the routine but not used in the visible source body.
  hydsep_hdr: String array declared as header storage, but it is not used in the visible body
    of `gwflow_output_init`.
  header: Scratch string used while reading headings from `gwflow.wbgroups` before the numeric
    counts and cell lists are read.
  i: Loop index for groundwater water-balance groups and for iterating over solute species;
    it also indexes the per-group and per-solute file setup blocks.
  j: Inner loop index used while reading the individual cells that belong to one groundwater
    water-balance group.
  n: Solute index used to loop over all solutes and to select the matching output file name
    and output unit offset.
  max_num: Maximum cell count per groundwater water-balance group, read from `gwflow.wbgroups`
    and used to size `gw_wb_grp_cells`.
  wb_cell: Temporary cell identifier read from `gwflow.wbgroups`; it is mapped through `cell_id_list`
    for structured grids and stored in the group cell list.
  group_area: Accumulator for the total area of the cells in one groundwater water-balance
    group, computed while the group’s cells are read.
uses:
  gwflow_module: The routine uses `gw_state(wb_cell)%area` to sum the area of each water-balance
    group, and `cell_id_list(wb_cell)` to translate structured-grid water-balance cell numbers
    into actual groundwater cell IDs. Those groundwater state arrays are what make the group
    bookkeeping and area totals meaningful.
  hydrograph_module: The candidate module is listed as a dependency, but no resolved outside
    reference from it is shown in the packet, so its direct role in this routine is uncertain
    from the provided evidence.
  sd_channel_module: The candidate module is listed as a dependency, but no resolved outside
    reference from it is shown in the packet, so its direct role in this routine is uncertain
    from the provided evidence.
  time_module: The candidate module is listed as a dependency, but no resolved outside reference
    from it is shown in the packet, so its direct role in this routine is uncertain from the
    provided evidence.
  constituent_mass_module: The solute file setup depends on `cs_db%num_salts` and `cs_db%num_cs`
    to decide which additional solute output files to create beyond nitrate and phosphorus.
    Those counters control whether salt-ion and other-constituent solute outputs are included.
  basin_module: The print-code structure `pco` controls whether each groundwater output family
    is enabled from `print.prt` and whether the day, month, year, or average-annual variants
    should be opened. That shared basin print-state overrides the default gwflow flags in
    this routine.
---

<!-- facts:header -->

Initializes all groundwater output files, headers, and related arrays for gwflow. It also applies print.prt overrides and prepares basin, cell, heat, and solute output streams used during the simulation.

## Bottom Line

`gwflow_output_init` is the groundwater output setup routine. It writes status messages, calls `gwflow_write_celldef` to create the cell-definition map, then opens and writes headers for basin-wide, cell-level, heat, and solute groundwater output files based on the current output flags.

It also reads `gwflow.wbgroups` when present, builds grouped-cell tracking arrays, and zeroes the solute accumulator arrays that will collect daily, monthly, yearly, and average-annual totals later in the run. The routine matters because it establishes every groundwater output file and the shared bookkeeping those later writers rely on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during groundwater model initialization, after `gwflow_read` has loaded configuration and set the output flags but before any simulation steps begin. `gwflow_read` calls `gwflow_output_init` at the end of its setup phase so the output files, group arrays, and solute accumulators are ready before the model starts producing day-, month-, year-, and average-annual results.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Announce groundwater output setup and create the cell-definition map | The routine writes startup messages to `out_gw`, calls `gwflow_write_celldef` to write the groundwater cell-definition file, and logs that the cell-definition file was written. |
| 2. Override groundwater water-balance print flags from `print.prt` | If the corresponding `pco%gwflow_*` print-code blocks were already read, the routine resets the groundwater output flags and re-enables day/month/year/average-annual or other variants according to the `y`/`m`/`a` characters in `pco`. |
| 3. Open and format basin groundwater water-balance files | When the basin groundwater output flags are active, the routine opens the day, month, year, and average-annual basin water-balance files and writes their titles, formatted headers, and units rows. |
| 4. Discover and load groundwater water-balance cell groups | If `gwflow.wbgroups` exists, the routine sets `gw_group_flag`, opens the file, reads the group count and maximum size, allocates the group arrays, reads each group's cell list, maps structured-grid cell ids through `cell_id_list` when needed, accumulates group area from `gw_state(wb_cell)%area`, opens each group output file, writes its headers, and closes the input file. |
| 5. Open basin groundwater heat-balance files | If `gw_heat_flag` is enabled, the routine writes a second startup message and opens the day, year, and average-annual groundwater heat-balance files, then writes their titles, headers, and units rows. |
| 6. Allocate solute accumulation arrays | When groundwater solute output is enabled, the routine allocates the monthly, yearly, and total accumulator arrays for each simulated solute and initializes the loops that will populate file names and outputs. |
| 7. Prepare daily solute basin output files | For each solute, if daily output is enabled the routine assigns the appropriate file name based on solute type, opens the output file, writes the title and formatted header rows, and leaves the daily arrays ready for later accumulation. |
| 8. Prepare monthly solute basin output files and reset monthly accumulators | For each solute, if monthly output is enabled the routine assigns the monthly file name, opens the file, writes the title and headers, and zeros the monthly accumulator arrays for that solute. |
| 9. Prepare yearly solute basin output files and reset yearly accumulators | For each solute, if yearly output is enabled the routine assigns the yearly file name, opens the file, writes the title and headers, and zeros the yearly accumulator arrays for that solute. |
| 10. Prepare average-annual solute basin output files and reset total accumulators | For each solute, if average-annual output is enabled the routine assigns the average-annual file name, opens the file, writes the title and headers, and zeros the total accumulator arrays for that solute. |
| 11. Open cell-level groundwater output files | The routine opens the cell-level day, month, year, and average-annual groundwater output files as enabled and writes their descriptive titles, unit notes, and formatted column header rows. |
| 12. Define the shared basin header format and return | The routine defines the shared `8000` format used by the basin-level headers and returns once all output files and accumulator arrays are prepared. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, cell_id_list` | `gw_state(wb_cell)%area` |
| [sym:hydrograph_module] | `No candidate outside references were resolved to `hydrograph_module`; the routine only `use`s the module, but the provided packet does not show any imported symbols from it being read here.` |  |
| [sym:sd_channel_module] | `No candidate outside references were resolved to `sd_channel_module`; the module is listed as a dependency, but the packet shows no specific symbol from it being used in this routine.` |  |
| [sym:time_module] | `No candidate outside references were resolved to `time_module`; the module is listed as a dependency, but the packet does not show a specific imported state or type used here.` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts, cs_db%num_cs` |
| [sym:basin_module] | `pco` | `pco%gwflow_wb%already_read_in, pco%gwflow_wb%d, pco%gwflow_wb%m, pco%gwflow_wb%y, pco%gwflow_wb%a, pco%gwflow_obs%already_read_in, pco%gwflow_obs%d, pco%gwflow_pump%already_read_in, pco%gwflow_pump%d, pco%gwflow_pump%m, pco%gwflow_pump%y, pco%gwflow_pump%a, pco%gwflow_heat%already_read_in, pco%gwflow_heat%d, pco%gwflow_heat%y, pco%gwflow_heat%a, pco%gwflow_solute%already_read_in, pco%gwflow_solute%d, pco%gwflow_solute%m, pco%gwflow_solute%y, pco%gwflow_solute%a, pco%gwflow_flux%already_read_in, pco%gwflow_flux%d, pco%gwflow_flux%y` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gwflag_day` | When `pco%gwflow_wb%already_read_in` is true, the routine clears the groundwater water-balance flags and then sets `gwflag_day` to 1 only if `pco%gwflow_wb%d == 'y'`, `gwflag_mon` to 1 only if `pco%gwflow_wb%m == 'y'`, `gwflag_yr` to 1 only if `pco%gwflow_wb%y == 'y'`, and `gwflag_aa` to 1 only if `pco%gwflow_wb%a == 'y'`. | This makes the basin water-balance outputs follow `print.prt` when those print codes were supplied, replacing whatever groundwater input flags were already present so later file setup only happens for the requested intervals. |
| `gwflag_obs` | When `pco%gwflow_obs%already_read_in` is true, the routine resets `gwflag_obs` to 0 and then sets it to 1 only if `pco%gwflow_obs%d == 'y'`. | This lets `print.prt` control whether observation-well groundwater output is enabled, so later observation output routines only run when the daily observation flag was requested. |
| `gwflag_pump` | When `pco%gwflow_pump%already_read_in` is true, the routine resets `gwflag_pump` to 0 and sets it to 1 if any of `pco%gwflow_pump%d`, `%m`, `%y`, or `%a` equals `'y'`. | This enables HRU pumping output whenever any pump output interval was requested in `print.prt`, allowing the later pumping diagnostics to be written at at least one interval. |
| `pco%gwflow_pump%y` | When `pco%gwflow_pump%already_read_in` is true and one of the pump print intervals is `'y'`, the routine sets `pco%gwflow_pump%y` by reading the `print.prt` interval state through the `pco` structure, which in practice is reflected by enabling yearly-capable pump output handling in this setup phase. | This yearly interval flag matters because the pump output subsystem later uses the `pco` interval settings to decide whether yearly pumping output should be generated. |
| `gwflag_heat` | When `pco%gwflow_heat%already_read_in` is true, the routine resets `gwflag_heat` to 0 and sets it to 1 if any of `pco%gwflow_heat%d`, `%y`, or `%a` equals `'y'`. | This gates groundwater heat-balance file creation so the heat outputs are only opened when `print.prt` or input settings request them. |
| `pco%gwflow_heat%a` | When `pco%gwflow_heat%already_read_in` is true and a heat interval is requested, the routine sets `pco%gwflow_heat%a` through the `pco` print-code structure as part of enabling average-annual heat output control. | The average-annual heat interval matters because the routine opens the average-annual heat file only when that output channel is enabled. |
| `gwflag_solute` | When `pco%gwflow_solute%already_read_in` is true, the routine resets `gwflag_solute` to 0 and sets it to 1 if any of `pco%gwflow_solute%d`, `%m`, `%y`, or `%a` equals `'y'`. | This activates groundwater solute output setup only when at least one solute reporting interval is requested, preventing unnecessary file creation and array allocation. |
| `pco%gwflow_solute%y` | When `pco%gwflow_solute%already_read_in` is true and a solute interval is requested, the routine sets `pco%gwflow_solute%y` through the `pco` structure as part of the print-code-driven solute reporting configuration. | The yearly solute interval matters because it controls whether the routine prepares the yearly solute output files and their accumulators. |
| `gwflag_flux` | When `pco%gwflow_flux%already_read_in` is true, the routine resets `gwflag_flux` to 0 and sets it to 1 if either `pco%gwflow_flux%d` or `pco%gwflow_flux%y` equals `'y'`. | This turns on the groundwater flux diagnostic output channel only when daily or yearly flux diagnostics are explicitly requested. |
| `gw_group_flag` | When `gwflow.wbgroups` exists and is successfully found by `inquire(file='gwflow.wbgroups',exist=i_exist)`, the routine sets `gw_group_flag = 1`. | This marks that groundwater water-balance group outputs are available, which later enables allocation of group arrays and creation of per-group files. |
| `gw_wb_grp_ncell` | When `gwflow.wbgroups` exists, the routine reads `gw_wb_grp_ncell` from the file and allocates it to the declared number of cell groups, then initializes it to zero before the per-group loop. | This stores how many cells belong to each groundwater water-balance group so later routines can accumulate group totals over the correct cells. |
| `gw_wb_grp_cells(i,j)` | When reading each group from `gwflow.wbgroups`, for every positive `wb_cell` the routine stores that cell into `gw_wb_grp_cells(i,j)` after applying the structured-grid mapping when `grid_type == 'structured'`. | This records the actual cell membership of each groundwater water-balance group so the group output files can later aggregate fluxes by the correct cell list. |
| `file_name_scalar` | When `gwflag_day.eq.1` and solute output is being prepared, the routine assigns `file_name_scalar` from `'gwflow_group_wb_day_'//aString` after formatting the group index with `write(aString,1091) i`. | This builds the concrete group-specific output file name so each groundwater water-balance group gets its own day file. |
| `file_name(1)` | When `gwflag_day.eq.1` and `n=1` within the solute file setup loop, the routine assigns `file_name(1) = 'gwflow_basin_sol_no3_day.txt'`. | This selects the daily nitrate basin output file before opening the corresponding solute file. |
| `file_name(2)` | When `gwflag_day.eq.1` and `n=2` within the solute file setup loop, the routine assigns `file_name(2) = 'gwflow_basin_sol_p_day.txt'`. | This selects the daily phosphorus basin output file before opening the corresponding solute file. |
| `file_name(3)` | When `gwflag_day.eq.1` and `cs_db%num_salts > 0`, the routine assigns salt-ion daily file names to `file_name(3)` through `file_name(10)` for sulfate, calcium, magnesium, sodium, potassium, chloride, carbonate, and bicarbonate. | These file names let the routine create daily basin outputs for each salt ion only when salt chemistry is active. |
| `file_name(4)` | When `gwflag_day.eq.1` and `cs_db%num_cs > 0`, the routine assigns constituent daily file names to `file_name(11)` and `file_name(12)` for selenate and selenite. | These file names enable daily basin outputs for the other constituent species only when that chemistry set is active. |
| `file_name(5)` | When `gwflag_mon.eq.1` and `n=1`, the routine assigns `file_name(1) = 'gwflow_basin_sol_no3_mon.txt'`. | This selects the monthly nitrate basin output file before opening the corresponding solute file. |
| `file_name(6)` | When `gwflag_mon.eq.1` and `n=2`, the routine assigns `file_name(2) = 'gwflow_basin_sol_p_mon.txt'`. | This selects the monthly phosphorus basin output file before opening the corresponding solute file. |
| `file_name(7)` | When `gwflag_yr.eq.1` and `n=1`, the routine assigns `file_name(1) = 'gwflow_basin_sol_no3_yr.txt'`. | This selects the yearly nitrate basin output file before opening the corresponding solute file. |
| `file_name(8)` | When `gwflag_yr.eq.1` and `n=2`, the routine assigns `file_name(2) = 'gwflow_basin_sol_p_yr.txt'`. | This selects the yearly phosphorus basin output file before opening the corresponding solute file. |
| `file_name(9)` | When `gwflag_aa.eq.1` and `n=1`, the routine assigns `file_name(1) = 'gwflow_basin_sol_no3_aa.txt'`. | This selects the average-annual nitrate basin output file before opening the corresponding solute file. |
| `file_name(10)` | When `gwflag_aa.eq.1` and `n=2`, the routine assigns `file_name(2) = 'gwflow_basin_sol_p_aa.txt'`. | This selects the average-annual phosphorus basin output file before opening the corresponding solute file. |
| `file_name(11)` | When `gwflag_aa.eq.1` and `n=11` or `n=12`, the routine assigns `file_name(11)` and `file_name(12)` to the average-annual selenate and selenite file names. | These file names enable the average-annual outputs for the other constituent species only when that chemistry set is active. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_output_init` was introduced in 9d9069f as a stub that only returned. In 1567fba it was expanded into the full groundwater output initializer, with the body extracted from `gwflow_read` to open output files, write headers, allocate solute arrays, and prepare group output. In b78c4ea the routine was updated to add `file_name_scalar`, change header text formatting, and use more aligned output labels. In 7ff5029 it was further revised to integrate `basin_module::pco`, apply `print.prt` overrides, and call `gwflow_write_celldef` before the file setup blocks.

- 9d9069f created `gwflow_output_init` as an empty subroutine stub.
- 1567fba moved groundwater output initialization out of `gwflow_read` and added the actual file opens, header writes, group parsing, solute allocations, and cell-level output setup.
- b78c4ea added `file_name_scalar` and adjusted groundwater output header label spacing.
- 7ff5029 added `use basin_module, only : pco, bsn`, print.prt-driven output flag overrides, and the call to `gwflow_write_celldef` before file setup.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_output_init' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 12 ordered steps that follow the actual initialization flow and keep cited line ranges within the provided `Source With Line Numbers` block.
- Outside references for `hydrograph_module`, `sd_channel_module`, and `time_module` were listed as dependencies, but no resolved candidate refs for those modules were provided in the packet; their direct role is therefore uncertain from the evidence shown.
- The source writes a formatted `output` log to `out_gw` repeatedly; the packet does not identify the underlying unit declaration, so that unit name is described only as used in the routine.
