---
kind: procedure
symbol: gwflow_channel_exch
title: gwflow_channel_exch
status: filled
source_hash: 85df644ba6d9655f
version_label: SWAT+ 62.0.0
args:
  chan_id: Selects which channel object, geometry, storage, and constituent pools are used;
    the routine processes only the groundwater cells connected to that one channel.
locals:
  k: Loop index over the connected groundwater cells for the selected channel.
  s: Loop index over groundwater solutes when transferring mass between the channel and aquifer.
  cell_id: Holds the groundwater cell id for the current channel connection being processed.
  isalt: Loop index over salt species in the channel water mass arrays.
  ics: Loop index over other tracked constituent species in the channel water mass arrays.
  sol_index: Maps the solute loop to the correct channel concentration slot as salts and other
    constituents are appended after NO3 and soluble P.
  dum: Scratch flag used to mark an unexpected negative computed constituent concentration
    in the channel water branch.
  chan_depth: Stores the channel water depth used to derive channel stage and the exchange
    head difference.
  chan_width: Stores the channel width used with connection length to compute exchange area.
  chan_length: Stores the length of the channel segment inside the current groundwater cell
    connection.
  bed_elev: Stores the channel-bed elevation for the current connection, adjusted by any global
    bed-elevation change.
  bed_k: Stores the hydraulic conductivity of the channel bed used in Darcy-law exchange calculations.
  bed_thick: Stores the thickness of the channel bed used as the flow path length in Darcy-law
    exchange calculations.
  chan_stage: Stores the water-surface elevation in the channel for the current connection.
  flow_area: Stores the channel-bed area available for exchange between the channel and the
    connected cell.
  gw_head: Stores the current groundwater head in the connected cell so the routine can compare
    it with channel stage and bed elevation.
  q: Stores the signed exchange flow rate between channel and aquifer for the current cell
    connection.
  head_diff: Stores the head difference used to compute the Darcy-law gradient for the current
    exchange direction.
  chan_volume: Stores the channel water volume before exchange so water and solute removals
    can be limited by what is available.
  stor_change: Temporary copy of the signed water exchange used to update groundwater storage.
  sat_change: Temporary saturated-thickness change computed from storage change, specific
    yield, and area.
  chan_csol: Holds computed channel-water solute concentrations used when water leaves the
    channel and enters groundwater.
  solmass: Holds the mass of each solute transferred for the current cell connection before
    updating channel and groundwater summaries.
  chan_heat: Holds the total heat content of the channel water before and after the exchange
    step.
  heat_flux: Holds the signed heat mass/energy exchanged for the current cell connection.
  chan_flow: Captures the channel water volume before the current exchange so heat content
    can be based on the pre-exchange channel storage.
  chan_temp: Temporary channel temperature used while recomputing channel temperature after
    heat exchange.
uses:
  gwflow_module: The groundwater module supplies the per-cell head, storage, area, and specific-yield
    state that determine whether exchange can occur, how much water can be removed, and how
    the cell head and summary flux arrays are updated. It also holds the daily, monthly, yearly,
    and heat/solute summary arrays that this routine writes to so later groundwater balance
    reporting can use the flux totals.
  hydrograph_module: The hydrograph module owns the channel storage and temperature records
    that this routine reads and updates. Those channel state values are the source and sink
    for exchanged water, heat, NO3, soluble phosphorus, salts, and other constituents, so
    the channel hydrographs must reflect the post-exchange condition.
  sd_channel_module: The SWAT-DEG channel geometry supplies the channel depth and width used
    to derive channel stage and exchange area for each channel-cell connection. Without that
    geometry, the Darcy-law exchange rate and the channel-water temperature/solute updates
    would not be tied to the correct physical reach.
  constituent_mass_module: The constituent-mass module provides the counts of salt and other
    constituent species and the channel water mass arrays that are updated during solute exchange.
    Those counts control the salt and constituent loops, and the per-channel mass arrays receive
    the transferred masses.
  time_module: The routine imports `time_module`, but the extracted source does not show any
    time-module symbol actually used in the visible lines, so its practical role here is uncertain
    from the provided evidence.
---

<!-- facts:header -->

Computes exchange of water, heat, and dissolved constituents between a channel and its connected groundwater cells.

## Bottom Line

For each active groundwater cell connected to a channel, `gwflow_channel_exch` computes a Darcy-law exchange flow based on channel stage, bed properties, and groundwater head. It then limits the exchange by available channel or aquifer storage and records the resulting water flux in groundwater summary arrays.

If heat or solute routing is enabled, the routine also transfers heat and constituent mass between the same channel-cell pair. Those updates keep channel storage, groundwater storage, and the daily/monthly/yearly groundwater exchange summaries consistent for later balance calculations in `gwflow_simulate`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `sd_channel_control3` after gwflow has been enabled for the channel and before the other groundwater-channel interaction routines (`gwflow_canal`, `gwflow_tile`, and `gwflow_satexcess`). Its results feed the groundwater water, heat, and constituent balance summaries that `gwflow_simulate` uses later in the day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the selected channel's stored volume and geometry, then iterate over each groundwater-cell connection. | The routine starts with the current channel storage and the channel width/depth, then loops through every connected cell listed in `gw_chan_info(chan_id)%ncon` and fetches each `cell_id` from the connection list. |
| 2. Skip inactive groundwater cells and load connection-specific bed and reach properties for the active ones. | Only active groundwater cells are processed. For each active connection the routine loads channel length, bed elevation, bed conductivity, and bed thickness from the channel-connection arrays. |
| 3. Derive the current channel stage and exchange area, optionally using a daily depth zone. | If depth zoning is enabled, the channel depth is replaced with the daily depth lookup. The routine then computes channel stage and the channel-bed flow area used for exchange. |
| 4. Compute the signed Darcy-law exchange rate from groundwater head, bed elevation, and channel stage. | The routine compares groundwater head with bed elevation and channel stage to determine whether water leaks from the channel to the aquifer or from the aquifer to the channel, then calculates the corresponding signed flow rate `Q`. |
| 5. Limit the exchange by available groundwater or channel water, then accumulate the daily hydrology summary fluxes. | Negative flow is capped by the groundwater storage available to remove; positive flow is capped by the channel volume available to remove. The resulting flow is accumulated into `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo` for the cell. |
| 6. Update channel storage and, when heat is enabled, exchange heat and recompute channel temperature. | The routine subtracts the water leaving the channel from `ch_stor(chan_id)%flo`. If heat routing is active, it transfers heat between groundwater and channel, updates `gw_heat_ss` and `gwheat_state`, recomputes the channel heat content and temperature, mirrors the result into `ch_out_d`, and records the yearly heat summary. |
| 7. When solute routing is enabled and flow leaves groundwater, move groundwater solute mass into channel water and summary arrays. | For aquifer-to-channel flow, the routine loops through all modeled solutes, transfers mass from the groundwater cell, and adds that mass to channel NO3, soluble P, salts, and other constituent pools as appropriate. It also records the groundwater-side solute exchange in daily, monthly, and yearly summary arrays. |
| 8. When solute routing is enabled and flow enters groundwater, compute channel concentrations, remove mass from channel pools, and record groundwater solute gains. | For channel-to-aquifer flow, the routine computes channel solute concentrations from current channel water storage, converts them to transferred mass, caps that mass by what is available in the channel, subtracts the mass from channel NO3, soluble P, salts, and other constituent pools, and stores the resulting groundwater-side solute exchange in daily, monthly, and yearly summaries. |
| 9. Finish after all connected cells have been processed. | After every active connection is handled, the subroutine exits and returns control to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, gw_bed_change, gw_chan_dep_flag` | `gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%gwsw, gw_hyd_ss(cell_id)%swgw, gw_state(cell_id)%spyd, gw_state(cell_id)%area, gw_hyd_ss_yr(cell_id)%gwsw, gw_hyd_ss_mo(cell_id)%gwsw, gw_heat_ss(cell_id)%gwsw, gw_heat_ss(cell_id)%swgw, gw_heat_ss_yr(cell_id)%gwsw` |
| [sym:hydrograph_module] | `ch_stor, ch_out_d` | `ch_stor(chan_id)%flo, ch_stor(chan_id)%temp, ch_out_d(chan_id)%temp, ch_stor(chan_id)%no3, ch_stor(chan_id)%solp` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(chan_id)%chd, sd_ch(chan_id)%chw` |
| [sym:constituent_mass_module] | `cs_db, ch_water` | `cs_db%num_salts, ch_water(chan_id)%salt(isalt), cs_db%num_cs, ch_water(chan_id)%cs(ics)` |
| [sym:time_module] | `time_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%gwsw` | When `gw_heat_flag == 1` and the current exchange is aquifer-to-channel (`Q < 0`), heat is moved from groundwater into channel water. | This daily heat flux records groundwater heat discharge to the channel so the groundwater heat balance and later summaries reflect heat leaving the cell. |
| `gw_hyd_ss(cell_id)%swgw` | When `gw_heat_flag == 1` and the current exchange is channel-to-aquifer (`Q >= 0`), heat is moved from channel water into the groundwater cell. | This daily heat flux records channel heat seepage into groundwater so the groundwater heat balance and later summaries include heat gained by the cell. |
| `gw_state(cell_id)%stor` | For every active cell connection after `Q` is finalized. | Groundwater storage is incremented or decremented by the signed exchange flow so the cell retains the remaining water volume after channel interaction. |
| `gw_state(cell_id)%head` | For every active cell connection after storage is updated. | Groundwater head is adjusted by the storage change divided by specific yield and cell area, converting the exchanged volume into a saturated-thickness/head update. |
| `gw_hyd_ss_yr(cell_id)%gwsw` | When `Q` is negative and the cell is active. | The yearly groundwater hydrology summary accumulates groundwater-to-channel water discharge for later annual reporting. |
| `gw_hyd_ss_mo(cell_id)%gwsw` | When `Q` is negative and the cell is active. | The monthly groundwater hydrology summary accumulates groundwater-to-channel water discharge for later monthly reporting. |
| `ch_stor(chan_id)%flo` | After the signed exchange flow is finalized for the active cell connection. | Channel water volume is reduced when flow leaves the channel and increased when water enters the channel, keeping channel storage consistent with the exchange. |
| `gw_heat_ss(cell_id)%gwsw` | When `gw_heat_flag == 1` for an active exchange. | The daily groundwater heat exchange summary records heat transferred between the aquifer and channel for the current cell connection. |
| `gwheat_state(cell_id)%stor` | When `gw_heat_flag == 1` and `Q < 0`. | Groundwater heat storage is adjusted by the transferred heat so the cell's remaining heat content matches the aquifer-to-channel flux. |
| `gw_heat_ss(cell_id)%swgw` | When `gw_heat_flag == 1` and `Q >= 0`. | Channel-to-aquifer heat transfer is recorded against the groundwater heat summary for the receiving cell. |
| `ch_stor(chan_id)%temp` | When `gw_heat_flag == 1` after heat exchange is applied. | Channel temperature is recomputed from updated heat content and current channel volume so the channel state reflects the post-exchange energy balance. |
| `ch_out_d(chan_id)%temp` | When `gw_heat_flag == 1` after the channel temperature is recomputed. | The daily output temperature record is synchronized with the updated channel temperature for downstream channel reporting. |
| `gw_heat_ss_yr(cell_id)%gwsw` | When `gw_heat_flag == 1` for an active exchange. | Yearly groundwater heat summary accumulates the heat exchanged with the channel for annual reporting. |
| `gwsol_ss(cell_id)%solute(s)%gwsw` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`). | The daily groundwater solute summary records solute mass leaving the groundwater cell for the current solute. |
| `gwsol_ss_sum(cell_id)%solute(s)%gwsw` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`). | The annual groundwater solute summary accumulates the same solute mass for year-level reporting. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%gwsw` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`). | The monthly groundwater solute summary accumulates the same solute mass for month-level reporting. |
| `ch_stor(chan_id)%no3` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`). | Channel NO3 mass increases by the solute mass leaving groundwater, preserving the channel mass balance. |
| `ch_stor(chan_id)%solp` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`). | Channel soluble phosphorus mass increases by the solute mass leaving groundwater, preserving the channel mass balance. |
| `ch_water(chan_id)%salt(isalt)` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`) with salts enabled. | Each channel salt mass is increased by the transferred groundwater solute mass so salt balance follows the water exchange. |
| `ch_water(chan_id)%cs(ics)` | When `gw_solute_flag == 1` and the exchange is aquifer-to-channel (`Q < 0`) with other constituents enabled. | Each channel constituent mass is increased by the transferred groundwater solute mass so constituent balance follows the water exchange. |
| `gwsol_ss(cell_id)%solute(s)%swgw` | When `gw_solute_flag == 1` and the exchange is channel-to-aquifer (`Q >= 0`). | The daily groundwater solute summary records solute mass entering the groundwater cell from the channel. |
| `gwsol_ss_sum(cell_id)%solute(s)%swgw` | When `gw_solute_flag == 1` and the exchange is channel-to-aquifer (`Q >= 0`). | The annual groundwater solute summary accumulates channel-derived solute mass for year-level reporting. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%swgw` | When `gw_solute_flag == 1` and the exchange is channel-to-aquifer (`Q >= 0`). | The monthly groundwater solute summary accumulates channel-derived solute mass for month-level reporting. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved five commits affecting this procedure. The file was introduced in 9d9069f with the basic groundwater-channel exchange implementation using `ch_stor` and no heat or time imports. Commit e6ca4de expanded the routine to import `ch_out_d` and `time_module`, added storage-change helpers and channel heat/temperature tracking, and implemented heat exchange plus richer solute bookkeeping. The remaining resolved commits only note repository-wide updates or input/data fixes without an extracted diff for this file.

- 9d9069f introduced `gwflow_channel_exch` with the core water-exchange loop, Darcy-law flow calculation, groundwater storage/head updates, and basic solute transfer between `gw_state` and `ch_stor`.
- e6ca4de added heat exchange and temperature updates, imported `ch_out_d` and `time_module`, and extended the procedure to track `stor_change`, `sat_change`, `chan_heat`, `heat_flux`, `chan_flow`, and `chan_temp`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_channel_exch' has no extracted documentation comment.
- time_module is imported in the source, but no visible symbol from that module was identified in the extracted lines; its use is uncertain from the provided evidence.
