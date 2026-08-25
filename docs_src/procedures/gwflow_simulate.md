---
kind: procedure
symbol: gwflow_simulate
title: gwflow_simulate
status: filled
source_hash: 1e1cd03b1573cd6e
version_label: SWAT+ 62.0.0
locals:
  i: Loop index over cells, groups, HRUs, or observations depending on the branch.
  j: Nested loop index for group members, tile cells, or channel-depth records.
  k: Loop index for observation wells in the observation-cache section.
  s: Loop index over solutes.
  dum: Scratch integer used only when reading the next-day channel-depth record.
  cell_id: Temporary cell identifier used when summing group or observation-cell values.
  num_months: Declared but not used in the visible source.
  sum: Running accumulator used for average depth-to-water and average temperature calculations.
  gw_storage: Scratch copy of groundwater volume used while computing beginning-of-day storage
    and heat.
  gw_heat: Scratch copy of groundwater heat content used while computing beginning-of-day
    heat.
  gw_temp: Scratch copy of groundwater temperature used in the heat branch.
  gwsw_sum: Per-group accumulator for groundwater-channel exchange totals.
  obs_vals: Temporary array holding observation-cell flow values before they are written.
  sum_tile: Per-tile-group total tile drainage flow converted to discharge rate.
  sum_mass: Per-tile-group solute mass accumulator used to compute tile concentrations.
  c_tile: Per-tile-group solute concentration array written to tile output when solutes are
    active.
  num_ts: Number of groundwater flow substeps implied by the configured time step.
  count: Counter for the number of active cells included in an average.
  depth_wt_avg: Average depth to the water table across active cells.
  temp_avg: Average groundwater temperature across active cells.
  arrays_allocated: One-time guard that prevents repeated allocation of the saved local arrays.
uses:
  gwflow_module: Provides the groundwater cell state, source/sink summary arrays, and accumulated
    head/storage fields that this routine updates and later reports.
  hydrograph_module: Provides the number of HRUs used when accumulating and reporting pumping
    totals.
  hru_module: Supplies HRU pumping totals and flags that are accumulated, sampled, and reset
    in this routine.
  sd_channel_module: Controls tile-drain, canal, observation-cell, and channel-depth branches,
    and holds the canal diversion records updated here.
  time_module: Provides the current simulation date and end-of-period flags used in output
    timing and file reads.
  soil_module: Imported by the procedure, but no resolved outside references from this module
    were identified in the context packet.
---

<!-- facts:header -->

Runs the groundwater flow step for one simulation day. It updates groundwater storage, heat, and solute bookkeeping, then writes daily, monthly, yearly, and average-annual groundwater outputs when their time triggers are met.

## Bottom Line

This subroutine is the main daily driver for the gwflow component. It computes current groundwater storage from head and aquifer geometry, calls the specialized source/sink routines for recharge, ET, phreatophytes, pumping, canals, ponds, and lateral flow, and then assembles the resulting water, heat, and solute balances.

It also handles the gwflow reporting cycle: it accumulates monthly and yearly averages, writes daily flux and observation outputs, emits month-end and year-end summaries, and clears the daily flux arrays so the next day starts from zeroed source/sink terms.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from the command driver when the current object is a gwflow object. It runs after the model has already set up the current time step and spatial context, and its results feed the groundwater daily, monthly, yearly, and final average-annual reporting chain.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Allocate saved arrays | On the first call, allocate the saved group and tile arrays that hold daily summaries, then mark them allocated so later calls reuse the same storage. |
| 2. Log routine call | Write a simple trace line to the groundwater output unit showing the current year and day. |
| 3. Compute groundwater storage | For each active cell, compute available groundwater storage from head, bottom elevation, area, and specific yield. If heat is active, convert that storage into heat content and store it in the heat summary state. |
| 4. Run source-sink routines | Call the specialized routines for recharge, groundwater ET, phreatophytes, external pumping, canal seepage, ponds, and canal diversions. Also accumulate HRU pumping totals, tile-drain summaries, and canal diversion bookkeeping needed for later reporting. |
| 5. Sum daily flux totals | Sum the daily water, heat, and solute source/sink terms into the per-cell summary arrays, and write group and observation-cell flux outputs when the corresponding flags are enabled. |
| 6. Prepare flow step state | Record beginning-of-day volume, heat, and solute mass, determine the number of flow substeps, clear the new/old head and concentration accumulators, and then call the lateral-flow solver. |
| 7. Accumulate reporting averages | Add the current head, temperature, and solute concentration to the monthly and yearly accumulators and compute basin-average depth to water table and groundwater temperature. |
| 8. Cache observation values | Copy the current head, temperature, and solute concentration for each observation well into the observation arrays used by the output routines. |
| 9. Record end-of-day state | Compute end-of-day groundwater volume, heat, and solute mass for active cells so the daily balance routines can compare beginning and ending state. |
| 10. Write periodic outputs | Call the daily output routine, then trigger monthly, yearly, and final average-annual output routines when the current date reaches those reporting boundaries. |
| 11. Clear daily flux arrays | Reset the daily groundwater, heat, and solute source/sink arrays to zero so the next day starts with clean accumulators, and clear the mass-reaction total. |
| 12. Read next channel depths | If channel-depth updates are enabled, read the next record of channel depths for use on the following day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_heat_ss` | `gw_state(i)%botm, gw_state(i)%stor, gw_state(i)%head, gw_state(i)%area, gw_state(i)%spyd, gw_hyd_ss(i)%totl, gw_hyd_ss(i)%rech, gw_hyd_ss(i)%gwet, gw_hyd_ss(i)%satx, gw_hyd_ss(i)%soil, gw_hyd_ss(i)%ppag, gw_hyd_ss(i)%ppex, gw_hyd_ss(i)%tile, gw_hyd_ss(i)%resv, gw_hyd_ss(i)%wetl, gw_hyd_ss(i)%canl, gw_hyd_ss(i)%fpln, gw_hyd_ss(i)%pond, gw_hyd_ss(i)%phyt, gw_hyd_ss(cell_id)%swgw, gw_hyd_ss(cell_id)%satx, gw_heat_ss(i)%totl, gw_heat_ss(i)%rech, gw_heat_ss(i)%gwet, gw_heat_ss(i)%gwsw, gw_heat_ss(i)%swgw, gw_heat_ss(i)%satx, gw_heat_ss(i)%soil, gw_heat_ss(i)%ppag, gw_heat_ss(i)%ppex, gw_heat_ss(i)%tile, gw_heat_ss(i)%resv, gw_heat_ss(i)%wetl, gw_heat_ss(i)%canl, gw_heat_ss(i)%fpln, gw_heat_ss(i)%pond, gw_state(i)%vbef, gw_state(i)%hnew, gw_state(i)%hold, gw_state(i)%hdmo, gw_state(i)%hdyr` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:hru_module] | `hru_pump, hru_pump_mo, hru_pump_yr, hru_pump_obs, hru_pump_ids, hru_pump_flag, gwflag_pump, num_hru_pump_obs` | `hru_pump(i), hru_pump_mo(i), hru_pump_yr(i), hru_pump_obs(i), hru_pump_ids(i), hru_pump_flag, gwflag_pump, num_hru_pump_obs` |
| [sym:sd_channel_module] | `gw_tile_flag, gw_tile_group_flag, gw_tile_num_group, num_tile_cells, gw_tile_groups, gw_solute_flag, gw_nsolute, gwflag_flux, gw_gwsw_group_flag, gw_gwsw_ngroup, gw_gwsw_ncell, gw_gwsw_group, gw_chan_obs_flag, gw_chan_nobs, gw_chan_obs_cell, gw_chan_dep_flag, gw_chan_ndpzn, gw_chan_dep, gw_ncanal, gw_canl_div_info` | `gw_tile_flag, gw_tile_group_flag, gw_tile_num_group, num_tile_cells(i), gw_tile_groups(i,j), gw_solute_flag, gw_nsolute, gwflag_flux, gw_gwsw_group_flag, gw_gwsw_ngroup, gw_gwsw_ncell(i), gw_gwsw_group(i,j), gw_chan_obs_flag, gw_chan_nobs, gw_chan_obs_cell(i), gw_chan_dep_flag, gw_chan_ndpzn, gw_chan_dep(j), gw_ncanal, gw_canl_div_info(i)%divr, gw_canl_div_info(i)%div, gw_canl_div_info(i)%stor, gw_canl_div_info(i)%out_pond, gw_canl_div_info(i)%out_seep` |
| [sym:time_module] | `time` | `time%yrc, time%day, time%mo, time%day_mo, time%yrs, time%end_mo, time%end_yr, time%yrc_end, time%day_end` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gwsw_sum(:)` | On first call when arrays_allocated is false and gw_gwsw_ngroup > 0 | Allocated once to hold per-group groundwater-channel exchange totals. |
| `sum_tile(:)` | On first call when arrays_allocated is false and gw_tile_num_group > 0 | Allocated once to hold per-group tile drainage flow totals. |
| `sum_mass(:,:)` | On first call when arrays_allocated is false and gw_tile_num_group > 0 | Allocated once to hold per-group tile solute mass totals. |
| `c_tile(:,:)` | On first call when arrays_allocated is false and gw_tile_num_group > 0 | Allocated once to hold per-group tile solute concentrations. |
| `gw_state(i)%stor` | Each day for active cells with head above bottom | Set to the available groundwater volume computed from saturated thickness, area, and specific yield. |
| `gwheat_state(i)%stor` | Each day when gw_heat_flag == 1 | Set to groundwater heat content computed from temperature, density, heat capacity, and storage. |
| `hru_pump_mo(i)` | Each day | Incremented by the current daily pumping amount for each HRU. |
| `hru_pump_yr(i)` | Each day | Incremented by the current daily pumping amount for each HRU. |
| `hru_pump_obs(i)` | When hru_pump_flag == 1 and gwflag_pump == 1 | Loaded from the selected HRU pumping totals for observation output. |
| `hru_pump` | After pumping totals are recorded | Reset to zero so the next day starts with a clean pumping accumulator. |
| `sum_tile(i)` | When gw_tile_flag == 1 and gw_tile_group_flag == 1 | Computed from tile drainage fluxes in the member cells and converted to m3/s. |
| `sum_mass(i,s)` | When gw_tile_flag == 1 and gw_tile_group_flag == 1 and gw_solute_flag == 1 | Accumulated tile-drain solute mass for each group and solute. |
| `c_tile(i,s)` | When gw_tile_flag == 1 and gw_tile_group_flag == 1 and gw_solute_flag == 1 | Computed as tile solute concentration from mass divided by flow, or set to zero when flow is zero. |
| `out_tile_cells` | When gwflag_flux == 1 and gw_tile_flag == 1 and gw_tile_group_flag == 1 | Receives the tile-group flow and concentration output record. |
| `gw_hyd_ss(i)%totl` | Each day for active cells | Set to the sum of the daily water source/sink terms excluding gwsw and swgw. |
| `gwsw_sum(i)` | When gw_gwsw_group_flag == 1 | Accumulated from groundwater-channel exchange terms for each group. |
| `out_gwsw_groups` | When gwflag_flux == 1 and gw_gwsw_group_flag == 1 | Receives the grouped groundwater-channel exchange output record. |
| `obs_vals(:)` | When gw_chan_obs_flag == 1 | Filled with observation-cell flow values, and with NO3 values when solute output is active. |
| `gw_heat_ss(i)%totl` | When gw_heat_flag == 1 | Set to the sum of the daily heat source/sink terms for active cells. |
| `gwsol_ss(i)%solute(s)%totl` | When gw_solute_flag == 1 | Set to the sum of the daily solute source/sink terms for active cells. |
| `gw_state(i)%vbef` | Each day for active cells | Set to the beginning-of-day groundwater volume. |
| `gwheat_state(i)%hbef` | Each day when gw_heat_flag == 1 | Set to the beginning-of-day groundwater heat content. |
| `gwsol_state(i)%solute(s)%mbef` | Each day when gw_solute_flag == 1 | Set to the beginning-of-day solute mass. |
| `gw_state(i)%hnew` | Each day | Cleared before the lateral-flow solver computes the new head. |
| `gw_state(i)%hold` | Each day | Cleared before the lateral-flow solver stores the previous head. |
| `gwheat_state(i)%tnew` | Each day when gw_heat_flag == 1 | Cleared before the lateral-flow solver computes the new temperature. |
| `gwsol_state(i)%solute(s)%cnew` | Each day when gw_solute_flag == 1 | Cleared before the lateral-flow solver computes the new concentration. |
| `gw_state(i)%hdmo` | Each day after lateral flow | Accumulated with the current head for monthly averaging. |
| `gw_state(i)%hdyr` | Each day after lateral flow | Accumulated with the current head for yearly averaging. |
| `gwheat_state(i)%tpmo` | Each day when gw_heat_flag == 1 | Accumulated with the current temperature for monthly averaging. |
| `gwheat_state(i)%tpyr` | Each day when gw_heat_flag == 1 | Accumulated with the current temperature for yearly averaging. |
| `gwsol_state(i)%solute(s)%cnmo` | Each day when gw_solute_flag == 1 | Accumulated with the current concentration for monthly averaging. |
| `gwsol_state(i)%solute(s)%cnyr` | Each day when gw_solute_flag == 1 | Accumulated with the current concentration for yearly averaging. |
| `gw_state(i)%vaft` | Each day for active cells | Set to the end-of-day groundwater volume. |
| `gwheat_state(i)%haft` | Each day when gw_heat_flag == 1 | Set to the end-of-day groundwater heat content. |
| `gwsol_state(i)%solute(s)%maft` | Each day when gw_solute_flag == 1 | Set to the end-of-day solute mass. |
| `gwflow_output_mon` | When time%end_mo == 1 | Called to write month-end groundwater summaries. |
| `gwflow_output_yr` | When time%end_yr == 1 | Called to write year-end groundwater summaries. |
| `gwflow_output_aa` | When time%yrc == time%yrc_end and time%day == time%day_end | Called to write the final average-annual groundwater summaries. |
| `gw_hyd_ss(i)%rech` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%gwet` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%gwsw` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%swgw` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%satx` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%soil` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%latl` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%bndr` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%ppag` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%ppdf` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%ppex` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%tile` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%resv` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%wetl` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%canl` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%fpln` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%pond` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%phyt` | Each day after reporting | Reset to zero for the next day. |
| `gw_hyd_ss(i)%totl` | Each day after reporting | Reset to zero for the next day. |
| `gw_heat_ss(i)%rech` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%gwet` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%gwsw` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%swgw` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%satx` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%soil` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%latl` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%disp` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%bndr` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%ppag` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%ppex` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%tile` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%resv` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%wetl` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%canl` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%fpln` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%pond` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gw_heat_ss(i)%totl` | Each day after reporting when gw_heat_flag == 1 | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%rech` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%gwsw` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%swgw` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%satx` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%soil` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%ppag` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%ppex` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%tile` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%resv` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%wetl` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%canl` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%fpln` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%pond` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%advn` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%disp` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%rcti` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%rcto` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%minl` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%sorb` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%totl` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day for solutes 1 and 2. |
| `gwsol_ss(i)%solute(s)%gwsw` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%swgw` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%satx` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%soil` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%ppag` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%ppex` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%tile` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%resv` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%wetl` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%canl` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%fpln` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%pond` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%advn` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%disp` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `gwsol_ss(i)%solute(s)%totl` | Each day after reporting when gw_solute_flag == 1 for solutes 3..gw_nsolute | Reset to zero for the next day. |
| `mass_rct` | Each day after reporting when gw_solute_flag == 1 | Reset to zero for the next day. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_simulate.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 16 non-merge commit(s) since, most recently `c38f3b8` (2026-04-05, "clean up and bugfixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `gwflow_simulate.f90` are listed.

- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `7ff5029` (2026-04-02) — gwflow re-merge: output redesign - long format, print.prt integration, standardized output
- `72aa70a` (2026-03-31) — gwflow re-merge: core flow solver - simulate driver, lateral flow, output system
- `1567fba` (2026-03-31) — gwflow re-merge: input system - gwflow_read, output init extraction, NAM/USGS/stats removal
- `df07e3f` (2024-03-05) — init all

## Review Notes

- File I/O verified against the source: 7 writes and 1 read, no opens, closes or rewinds, and every `io_references` entry matches a real statement at the cited line. The writes go to named unit variables rather than numeric literals — `out_gw` (an unconditional trace line at gwflow_simulate.f90:63), `out_hru_pump_obs`, `out_tile_cells`, `out_gwsw_groups`, `out_gwsw_chanobs_flow` and `out_gwsw_chanobs_no3`. All except the trace line are guarded by `gwflag_flux == 1`, with the solute records additionally guarded by `gw_solute_flag == 1`. The single read pulls next-day channel depths from unit 1421 under `gw_chan_dep_flag == 1`.
- algorithm_steps were left as the fill model produced them: the 12 spans are already contiguous and non-overlapping across gwflow_simulate.f90:51-581.
- `gwflow_simulate` carries no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
