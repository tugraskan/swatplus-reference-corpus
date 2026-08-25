---
kind: procedure
symbol: gwflow_canal
title: gwflow_canal
status: filled
source_hash: 1fe7603f3457e384
version_label: SWAT+ 62.0.0
args:
  chan_id: Identifies the channel whose canal connections are processed. The routine uses
    `chan_id` to look up the channel’s canal list, each canal’s geometry and active-day window,
    and the matching channel storage and constituent state that must be updated.
locals:
  c: Loop counter over the canals connected to the input channel.
  k: Loop counter over the grid cells connected to the current canal.
  s: Loop counter over groundwater solutes when transferring solute mass.
  canal_id: Holds the current canal identifier pulled from the channel-to-canal linkage list.
  cell_id: Holds the groundwater cell ID connected to the current canal connection.
  day_beg: Stores the start day of the canal’s active period for the current channel-canal
    link.
  day_end: Stores the end day of the canal’s active period for the current channel-canal link.
  isalt: Loop counter for salt ions transferred with canal water.
  ics: Loop counter for other constituents transferred with canal water.
  sol_index: Tracks the position in the channel solute mass array as water-quality species
    are packed in order.
  dum: Declared but not used in the extracted code; likely a leftover placeholder variable.
  chan_volume: Captures the channel water volume before exchange so concentrations and heat
    can be computed from the pre-exchange storage.
  width: Stores the canal width for the current canal connection and is used to build seepage
    area.
  depth: Stores canal depth and is used to compute canal bed elevation and seepage geometry.
  thick: Stores canal bed thickness used in the seepage gradient term.
  length: Stores the connected cell length of canal influence and contributes to seepage area.
  stage: Stores the canal water surface elevation used when comparing against groundwater
    head.
  bed_k: Stores the canal-bed hydraulic conductivity used in the exchange-rate calculation.
  reduc: Declared in the source but not used in the extracted lines; likely reserved for a
    reduction factor or related feature.
  daycount_real: Declared in the source but not used in the extracted lines; likely a placeholder
    for a real-valued day counter.
  flow_area: Holds the seepage area used in the Darcy-style canal exchange calculation.
  canal_bed: Stores the canal bed elevation for the current cell, computed from stage minus
    depth.
  head_diff: Stores the effective head difference used to compute the exchange magnitude for
    the current groundwater/canal configuration.
  q: Holds the signed canal-groundwater exchange rate in m3/day; positive means water enters
    the aquifer and negative means water leaves the aquifer.
  chan_csol: Temporary array of channel-water solute concentrations used to compute mass transfer
    from channel water into the canal/aquifer system.
  solmass: Temporary array of solute masses transferred for the current cell exchange calculation.
  conc_nh3: Temporary NH3 concentration in channel water used when exchange moves water out
    of the channel.
  conc_no2: Temporary NO2 concentration in channel water used when exchange moves water out
    of the channel.
  conc_dox: Temporary dissolved oxygen concentration in channel water used when exchange moves
    water out of the channel.
  conc_orgn: Temporary organic nitrogen concentration in channel water used when exchange
    moves water out of the channel.
  mass_nh3: Temporary NH3 mass transferred for the current exchange event.
  mass_no2: Temporary NO2 mass transferred for the current exchange event.
  mass_dox: Temporary dissolved oxygen mass transferred for the current exchange event.
  mass_orgn: Temporary organic nitrogen mass transferred for the current exchange event.
  heat_flux: Temporary heat amount transferred between groundwater and channel for the current
    exchange event.
  chan_heat: Temporary total heat content of the channel water used to update channel temperature
    after exchange.
uses:
  gwflow_module: The groundwater module supplies the per-cell groundwater state and the daily/monthly/yearly
    source-sink summary arrays that this routine updates. Without `gw_state`, `gw_hyd_ss`,
    `gw_hyd_ss_yr`, `gw_hyd_ss_mo`, `gw_heat_ss`, and `gw_heat_ss_yr`, the canal seepage calculation
    would have nowhere to read groundwater heads from or store the resulting water and heat
    fluxes.
  hydrograph_module: The channel storage arrays hold the channel water volume and water-quality/temperature
    state that canal seepage removes from or adds to. `ch_stor` provides the live channel
    inventory for flow, temperature, and nutrients, while `ch_out_d` receives the updated
    channel temperature for downstream daily output.
  time_module: The current simulation day controls whether each canal is active on this call.
    `time%day` is compared to each canal’s begin/end window so exchange is only applied during
    the configured operating period.
  constituent_mass_module: This module provides the counts of simulated salts and constituents
    and the channel-water arrays that hold their masses. Those counts drive the transfer loops,
    and the channel-water storage arrays are reduced when canal exchange removes salt ions
    or other constituents from channel water.
---

<!-- facts:header -->

Moves water, heat, and selected constituents between a specified channel and its connected irrigation canals and grid cells. It only acts when canal exchange is enabled and the current day falls within each canal’s active window.

## Bottom Line

`gwflow_canal` computes seepage exchange between a channel-fed canal system and the groundwater cells connected to each canal. For each active canal on the input channel, it evaluates the head difference, applies a Darcy-style exchange rate, and then updates groundwater storage plus the channel’s water volume when flow goes from the channel/canal into the aquifer or back the other way.

When heat and solute options are enabled, the same exchange also moves heat and selected water-quality masses. The routine reduces channel water constituents when water leaves the channel, adds mass to the groundwater-side flux summaries, and records daily/monthly/yearly canal exchange totals for later groundwater and channel accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `sd_channel_control3` after channel groundwater exchange has been initialized for the current channel. It runs during the groundwater-interaction phase of channel control, and its updates matter to the later groundwater balance, channel storage, heat accounting, and constituent-mass summaries that other routines consume.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Exit immediately unless canal exchange is enabled. | The routine first checks `gw_canal_flag`; if canal-cell exchange is disabled, it returns without changing any state. |
| 2. Capture pre-exchange channel water and concentrations. | It stores the starting channel volume, builds channel solute concentration arrays from current channel water, and records NH3, NO2, DOX, and organic nitrogen concentrations when the channel volume is large enough for meaningful exchange calculations. |
| 3. Loop over canals attached to the channel. | For each connected canal, the routine loads canal ID, width, depth, thickness, and active-day bounds from the channel-to-canal linkage data. |
| 4. Process only canals that are active on the current day. | The canal is skipped unless the current simulation day lies inside the canal’s configured begin/end window. |
| 5. Loop over groundwater cells connected to the active canal. | For each connected cell, the routine reads the cell ID and continues only if the groundwater cell is active. |
| 6. Build seepage geometry and compute signed exchange rate. | Using canal length, width, stage, depth, bed thickness, and hydraulic conductivity, the routine computes seepage area, canal-bed elevation, head difference, and signed Darcy-style exchange rate `Q` for the current cell-canal pair. |
| 7. Update groundwater and channel water storage for the exchange. | If flow goes from the canal into the aquifer, groundwater storage summaries increase and channel flow is reduced; regardless of sign, daily and longer-term groundwater water summaries receive the exchange amount. |
| 8. Transfer heat when groundwater heat routing is active. | If heat exchange is enabled, the routine computes heat content in the channel, transfers heat between the channel and groundwater subject to available storage limits, updates groundwater heat storage, recalculates channel temperature, and stores the updated temperature in the daily output array. |
| 9. Transfer solutes when groundwater solute routing is active. | If solute exchange is enabled, the routine computes solute mass moved by the exchange, limits withdrawals by available mass in the source water, subtracts masses from channel water or channel storage as needed, and accumulates the transferred masses into groundwater solute summary arrays. |
| 10. Finish the nested loops and return. | After all active canals and connected cells have been processed, the subroutine exits and leaves the updated channel, groundwater, heat, and solute states for later model accounting. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr` | `gw_state(cell_id)%stat, gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%canl, gw_hyd_ss_yr(cell_id)%canl, gw_hyd_ss_mo(cell_id)%canl, gw_heat_ss(cell_id)%canl, gw_heat_ss_yr(cell_id)%canl` |
| [sym:hydrograph_module] | `ch_stor, ch_out_d` | `ch_stor(chan_id)%flo, ch_stor(chan_id)%nh3, ch_stor(chan_id)%no2, ch_stor(chan_id)%dox, ch_stor(chan_id)%orgn, ch_stor(chan_id)%temp, ch_out_d(chan_id)%temp, ch_stor(chan_id)%no3, ch_stor(chan_id)%solp` |
| [sym:time_module] | `time` | `time%day` |
| [sym:constituent_mass_module] | `cs_db, ch_water` | `cs_db%num_salts, cs_db%num_cs, ch_water(chan_id)%salt(isalt), ch_water(chan_id)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_heat_flag == 1` with a nonzero exchange rate. | This per-cell heat-exchange summary accumulates the heat moved between the canal and groundwater during the current call. It is updated so downstream heat-balance routines can account for canal seepage heat flux. |
| `gw_state(cell_id)%stor` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and the computed exchange is positive enough to be stored in groundwater water accounting. | Groundwater storage is increased by canal seepage entering the aquifer and reduced through the exchange bookkeeping so later groundwater balance calculations see the new storage state. |
| `ch_stor(chan_id)%flo` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `Q > 0` or `Q < 0` changes the channel volume calculation path. | Channel water volume is reduced when seepage leaves the channel to groundwater, so the channel storage used by later routines reflects the water lost to canal exchange. |
| `gw_hyd_ss_yr(cell_id)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_heat_flag == 1`. | The yearly heat-exchange summary accumulates the heat transferred between the canal and groundwater during this call for annual reporting. |
| `gw_hyd_ss_mo(cell_id)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_heat_flag == 1`. | The monthly heat-exchange summary accumulates the same canal heat transfer so monthly reporting can use the canal seepage heat budget. |
| `gwheat_state(cell_id)%stor` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_heat_flag == 1` with heat leaving the groundwater cell. | Groundwater heat storage is adjusted by the exchanged heat so the cell’s remaining thermal inventory stays consistent with the canal interaction. |
| `ch_stor(chan_id)%temp` | When `gw_canal_flag == 1`, the canal is active, the cell is active, and `gw_heat_flag == 1` after heat exchange is applied. | Channel temperature is recomputed from the updated channel heat content and remaining channel volume, so the channel state reflects heat lost or gained through canal seepage. |
| `ch_out_d(chan_id)%temp` | When `gw_canal_flag == 1`, the canal is active, the cell is active, and `gw_heat_flag == 1` after the channel temperature update. | The daily output temperature array is kept in sync with the updated channel temperature so downstream output routines print the post-exchange value. |
| `gw_heat_ss(cell_id)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_heat_flag == 1` with heat exchange computed. | This daily canal heat flux accumulator stores the heat exchanged between the channel/canal water and groundwater for the current cell. |
| `gw_heat_ss_yr(cell_id)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_heat_flag == 1` with heat exchange computed. | This yearly canal heat flux accumulator stores the same heat transfer so annual summaries can report canal-related heat movement. |
| `ch_stor(chan_id)%no3` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1` with positive exchange from groundwater or channel to the opposite side. | Channel nitrate mass is reduced when nitrate is exported from channel water during canal seepage so later channel water-quality calculations use the remaining mass. |
| `ch_stor(chan_id)%solp` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1` with positive exchange from channel water. | Channel soluble phosphorus mass is reduced when the exchange removes water from the channel, keeping the channel mass inventory consistent with the seepage loss. |
| `ch_stor(chan_id)%nh3` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1` with positive exchange from channel water. | Channel ammonia mass is reduced by the amount moved with canal seepage, so the channel constituent store reflects the loss. |
| `ch_stor(chan_id)%no2` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1` with positive exchange from channel water. | Channel nitrite mass is reduced by the amount moved with canal seepage, preserving mass balance after the exchange. |
| `ch_stor(chan_id)%dox` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1` with positive exchange from channel water. | Channel dissolved oxygen mass is reduced by the amount moved with canal seepage, keeping the channel water-quality state consistent with the transfer. |
| `ch_stor(chan_id)%orgn` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1` with positive exchange from channel water. | Channel organic nitrogen mass is reduced by the amount moved with canal seepage, so the channel organic-N inventory matches the post-exchange state. |
| `ch_water(chan_id)%salt(isalt)` | When `gw_canal_flag == 1`, the canal is active, the connected cell is active, `gwsol_salt == 1`, and the exchange moves channel water into the aquifer or vice versa. | Each salt-ion mass in channel water is reduced when that salt is carried with the exchanged canal water, and the amount is limited to what is available in channel storage. |
| `ch_water(chan_id)%cs(ics)` | When `gw_canal_flag == 1`, the canal is active, the connected cell is active, `gwsol_cons == 1`, and the exchange moves channel water into the aquifer or vice versa. | Each simulated constituent mass in channel water is reduced when it is carried with the exchanged canal water, with withdrawals capped by the available channel constituent mass. |
| `gwsol_ss(cell_id)%solute(s)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1`. | This daily groundwater solute summary accumulates the mass exchanged with the canal so the cell’s solute budget includes canal seepage. |
| `gwsol_ss_sum(cell_id)%solute(s)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1`. | This cumulative groundwater solute summary stores the same canal-exchange mass for total budget reporting over the simulation period. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%canl` | When `gw_canal_flag == 1`, the canal is active for the current day, the connected cell is active, and `gw_solute_flag == 1`. | This monthly cumulative groundwater solute summary stores canal-exchange mass for monthly output and bookkeeping. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavior-changing edits. In 9d9069f, `gwflow_canal` was introduced as a new subroutine that calculates canal-to-groundwater exchange, using `use hydrograph_module, only : ch_stor` and the initial water/solute transfer logic. In 0ece228, the routine was extended for canals that remove water from a specified channel, added `ch_out_d` to the hydrograph imports, introduced the unused local `dum`, and expanded the body with the later water, heat, and solute bookkeeping that writes to `gw_hyd_ss`, `gw_heat_ss`, `gwsol_ss`, and channel storages.

- 9d9069f: created `gwflow_canal` and established the core canal seepage calculation and initial channel-water/solute transfer behavior.
- 0ece228: expanded the routine to include `ch_out_d`, additional local state, and the canal-specific water, heat, and solute accounting paths visible in the current source.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_canal' has no extracted documentation comment.
