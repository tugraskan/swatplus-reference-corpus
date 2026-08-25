---
kind: procedure
symbol: gwflow_floodplain
title: gwflow_floodplain
status: filled
source_hash: 5035f7efc7414575
version_label: SWAT+ 62.0.0
grounding_allow:
- k
- s
- cell_id
- chan_cell
- isalt
- ics
- sol_index
- chan_depth
- chan_width
- chan_length
- bed_elev
- bed_k
- bed_thick
- chan_stage
- flow_area
- riv_flow_area
- gw_head
- q
- chan_volume
- chan_csol
- solmass
- heat_flux
- chan_heat
locals:
  k: Loop counter over the floodplain connections listed for `chan_id` in `gw_fpln_info(chan_id)%cells`.
  s: Loop counter over groundwater/channel solutes in `gw_nsolute` when transferring solute
    mass.
  cell_id: The groundwater grid cell currently connected to the channel and being processed.
  chan_cell: If the connected groundwater cell overlaps a river cell, this holds the matching
    channel-cell index used to compute the river portion of the exchange area.
  isalt: Loop counter for salt ions in `ch_water(chan_id)%salt` when salts are enabled.
  ics: Loop counter for other constituents in `ch_water(chan_id)%cs` when constituent tracking
    is enabled.
  sol_index: Maps the groundwater solute loop index onto the channel concentration/mass array
    positions as salts and constituents are appended after NO3 and soluble P.
  chan_depth: Channel water depth copied from `sd_ch(chan_id)%chd` for the current exchange
    calculation.
  chan_width: Declared channel width local, but no assigned use is visible in the extracted
    source for this routine.
  chan_length: Declared channel length local, but no assigned use is visible in the extracted
    source for this routine.
  bed_elev: Ground surface or bed reference elevation for the connected groundwater cell,
    used with channel depth to form channel stage.
  bed_k: Floodplain hydraulic conductivity for this channel-cell connection, read from `gw_fpln_info(chan_id)%hydc(k)`
    and used in the exchange calculation.
  bed_thick: Declared bed thickness local, but no assigned use is visible in the extracted
    source for this routine.
  chan_stage: Computed water-surface elevation in the channel at the connected cell, used
    to decide exchange direction.
  flow_area: Effective groundwater exchange area for the current connection, reduced when
    the connected cell also represents part of the river channel.
  riv_flow_area: Portion of the exchange area that belongs to the river cell overlap and must
    be subtracted from the total floodplain area.
  gw_head: Declared groundwater head local, but the routine compares the cell head directly
    and does not assign this variable in the extracted source.
  q: Signed water exchange rate between groundwater and channel for the current connection;
    negative means aquifer-to-channel discharge, positive means channel-to-aquifer seepage.
  chan_volume: Channel water volume at the start of the routine, used to convert channel mass
    inventories into concentrations when water moves into the aquifer.
  chan_csol: Temporary array holding channel solute concentrations in g/m3 for each tracked
    solute during channel-to-aquifer exchange.
  solmass: Temporary array holding the mass transferred for each solute/concentrant during
    the current connection exchange.
  heat_flux: Temporary heat mass transferred between groundwater and channel for the current
    connection.
  chan_heat: Temporary total heat content in the channel, used to rebalance channel temperature
    after heat transfer.
uses:
  gwflow_module: '`gwflow_module` supplies the groundwater cell states, floodplain connection
    metadata, and groundwater summary arrays that this routine reads to determine geometry,
    exchange direction, storage limits, and to record the resulting hydrology, heat, and solute
    fluxes.'
  hydrograph_module: '`hydrograph_module` provides `ch_stor`, the per-channel water storage
    record that holds the channel volume, temperature, and tracked channel masses that are
    reduced or increased by floodplain exchange.'
  sd_channel_module: '`sd_channel_module` provides the channel geometry used to form the exchange
    stage and overlap geometry, especially channel depth and width for the current `chan_id`.'
  constituent_mass_module: '`constituent_mass_module` provides the counts of tracked salts
    and other constituents and the channel mass arrays that are updated when solute mass is
    transferred between groundwater and the channel.'
---

<!-- facts:header -->

Moves water, heat, and dissolved constituents between a channel and the groundwater floodplain cells connected to that channel.

## Bottom Line

For one channel at a time, `gwflow_floodplain` loops over the connected floodplain cells, computes Darcy-style exchange based on channel stage, groundwater head, bed hydraulic conductivity, and effective exchange area, then caps the exchange so it cannot remove more water than is available from either side. It updates channel storage and groundwater storage accordingly.

If heat and solute transport are enabled, the same exchange is applied to heat and to channel solute/constituent masses: groundwater-to-channel exchange adds heat and mass to channel storages, while channel-to-groundwater exchange removes them and records the fluxes in groundwater source/sink summary arrays for later balance calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs only when `sd_channel_sediment3` detects overbank flooding and `bsn_cc%gwflow.eq.1`, so the sediment/overbank workflow has already identified a channel needing floodplain groundwater exchange. Its results feed back into channel storage, groundwater storage, and the `gw_hyd_ss`, `gw_heat_ss`, and `gwsol_ss` summary arrays that `gwflow_simulate` uses for groundwater balance accounting and later reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Capture the starting channel water volume and guard execution on floodplain connectivity being available. | The routine stores `ch_stor(chan_id)%flo` in `chan_volume` and proceeds only when `gw_fp_flag == 1` and `gw_fpln_info` is allocated, so all later exchange logic is skipped unless floodplain data are loaded. |
| 2. Loop over each floodplain connection for the channel and skip inactive groundwater cells. | For each connected cell listed in `gw_fpln_info(chan_id)%cells(k)`, the routine processes exchange only if `gw_state(cell_id)%stat` indicates the groundwater cell is active. |
| 3. Assemble channel, cell, and connection properties used in the exchange calculation. | It reads channel depth from `sd_ch(chan_id)%chd`, cell elevation from `gw_state(cell_id)%elev`, hydraulic conductivity from `gw_fpln_info(chan_id)%hydc(k)`, and the connection area from `gw_fpln_info(chan_id)%area(k)`, then computes channel stage as `bed_elev + chan_depth`. |
| 4. Reduce the exchange area when the connection overlaps a river cell. | If `gw_fpln_info(chan_id)%mtch(k)` is positive, the routine uses `gw_chan_len(chan_cell)` and channel width to compute the river portion of the area, subtracts that from the floodplain area, and floors the result at zero so the overlap is not counted twice. |
| 5. Compute signed seepage/discharge flow using the cell head relative to channel stage. | The routine sets `Q` to zero, then uses the difference between `gw_state(cell_id)%head` and `chan_stage` to choose direction: if groundwater head is above the channel stage it sets negative discharge from aquifer to channel, otherwise positive seepage from channel to aquifer, both scaled by `bed_K * flow_area`. |
| 6. Limit water exchange to available groundwater storage or channel water and update both storages. | When `Q < 0`, the routine caps outflow so it cannot exceed `gw_state(cell_id)%stor` and subtracts the discharged water from groundwater storage. When `Q >= 0`, it caps seepage so it cannot exceed `ch_stor(chan_id)%flo` and adds that water to groundwater storage, then adjusts channel volume by subtracting the net exchange from `ch_stor(chan_id)%flo`. |
| 7. Accumulate the hydrologic floodplain flux in daily, monthly, and yearly groundwater summaries. | The net flux `Q` is stored in `gw_hyd_ss(cell_id)%fpln` and added to the month and year accumulators so later groundwater balance reporting includes floodplain exchange. |
| 8. If heat transport is enabled, move heat with the same exchange direction and update channel temperature. | The routine converts channel temperature and flow to heat content, transfers heat from groundwater to channel or channel to groundwater with limits based on available heat/storage, updates `gwheat_state(cell_id)%stor`, recomputes `ch_stor(chan_id)%temp` from remaining channel heat and water, and records the heat flux in `gw_heat_ss` daily and yearly arrays. |
| 9. If solute transport is enabled and water moves from groundwater to channel, remove solute mass from the cell and add it to channel inventories. | For `Q < 0`, the routine computes solute mass leaving the cell from groundwater concentrations, caps removal at the available groundwater mass, stores the flux in `gwsol_ss` and the cumulative summary arrays, and adds the mass to channel NO3, soluble P, salts, and other constituent inventories using `sol_index` to map array positions. |
| 10. If solute transport is enabled and water moves from channel to groundwater, derive channel concentrations and remove the corresponding mass from channel inventories. | For `Q >= 0`, the routine uses `chan_volume` to convert channel mass inventories to concentrations when enough water is present, computes transferred mass, caps it at the available channel mass for each tracked component, subtracts it from `ch_stor`, `ch_water%salt`, and `ch_water%cs`, and records the resulting flux in `gwsol_ss` and its monthly and yearly sums. |
| 11. Continue to the next connected cell and exit when all connections have been processed. | The routine finishes the active-cell test, advances through all floodplain connections, and returns after processing the full set or after skipping execution when floodplain exchange is disabled. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, gw_chan_len` | `gw_state(cell_id)%elev, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%fpln, gw_hyd_ss_yr(cell_id)%fpln, gw_hyd_ss_mo(cell_id)%fpln, gw_heat_ss(cell_id)%fpln, gw_heat_ss_yr(cell_id)%fpln` |
| [sym:hydrograph_module] | `ch_stor` | `ch_stor(chan_id)%flo, ch_stor(chan_id)%temp, ch_stor(chan_id)%no3, ch_stor(chan_id)%solp` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(chan_id)%chd, sd_ch(chan_id)%chw` |
| [sym:constituent_mass_module] | `cs_db, ch_water` | `cs_db%num_salts, ch_water(chan_id)%salt(isalt), cs_db%num_cs, ch_water(chan_id)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(cell_id)%stor` | When floodplain exchange is active and the computed `Q` would remove more water than the groundwater cell has available, or when the signed exchange rate is applied for the current connection. | `gw_state(cell_id)%stor` is reduced by aquifer-to-channel discharge or increased by channel-to-aquifer seepage, with the flux capped so the cell cannot lose more groundwater than it stores. |
| `ch_stor(chan_id)%flo` | When the current connection produces a nonzero `Q`, after storage limits are applied. | `ch_stor(chan_id)%flo` is reduced when channel water seeps into the aquifer and increased when groundwater discharges into the channel, so the channel storage reflects the net floodplain exchange. |
| `gw_hyd_ss(cell_id)%fpln` | Each active connected cell after the hydrologic exchange `Q` is computed. | `gw_hyd_ss(cell_id)%fpln` accumulates the daily floodplain water flux for the cell, using the signed exchange rate as the recorded source/sink value. |
| `gw_hyd_ss_yr(cell_id)%fpln` | Each active connected cell after the hydrologic exchange `Q` is computed. | `gw_hyd_ss_yr(cell_id)%fpln` accumulates the same floodplain water flux into the yearly groundwater summary. |
| `gw_hyd_ss_mo(cell_id)%fpln` | Each active connected cell after the hydrologic exchange `Q` is computed. | `gw_hyd_ss_mo(cell_id)%fpln` accumulates the same floodplain water flux into the monthly groundwater summary. |
| `gwheat_state(cell_id)%stor` | When `gw_heat_flag == 1` and the current exchange transfers heat between groundwater and channel water. | `gwheat_state(cell_id)%stor` is adjusted by the heat flux removed from or added to the groundwater cell so the heat storage matches the exchanged energy. |
| `ch_stor(chan_id)%temp` | When `gw_heat_flag == 1` and the channel has nonzero remaining water after heat exchange. | `ch_stor(chan_id)%temp` is recomputed from the channel’s remaining heat content and water volume after the exchange changes the heat balance. |
| `gw_heat_ss(cell_id)%fpln` | When `gw_heat_flag == 1` for every active connected cell. | `gw_heat_ss(cell_id)%fpln` stores the daily heat flux exchanged through the floodplain connection for later heat accounting. |
| `gw_heat_ss_yr(cell_id)%fpln` | When `gw_heat_flag == 1` for every active connected cell. | `gw_heat_ss_yr(cell_id)%fpln` accumulates the yearly heat flux exchanged through the floodplain connection. |
| `gwsol_ss(cell_id)%solute(s)%fpln` | When `gw_solute_flag == 1` and `Q < 0`, meaning groundwater is discharging to the channel. | `gwsol_ss(cell_id)%solute(s)%fpln` stores the solute mass removed from groundwater for the current cell and solute index. |
| `gwsol_ss_sum(cell_id)%solute(s)%fpln` | When `gw_solute_flag == 1` and `Q < 0`, meaning groundwater is discharging to the channel. | `gwsol_ss_sum(cell_id)%solute(s)%fpln` accumulates the total floodplain solute mass exchange for the cell across the simulation period. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%fpln` | When `gw_solute_flag == 1` and `Q < 0`, meaning groundwater is discharging to the channel. | `gwsol_ss_sum_mo(cell_id)%solute(s)%fpln` accumulates the monthly floodplain solute mass exchange for the cell. |
| `ch_stor(chan_id)%no3` | When `gw_solute_flag == 1` and `Q >= 0`, meaning water is leaving the channel for groundwater. | `ch_stor(chan_id)%no3` is reduced by the NO3 mass transferred out of channel water, capped so it cannot fall below the available channel NO3 inventory. |
| `ch_stor(chan_id)%solp` | When `gw_solute_flag == 1` and `Q >= 0`, meaning water is leaving the channel for groundwater. | `ch_stor(chan_id)%solp` is reduced by the soluble phosphorus mass transferred out of channel water, capped by the available inventory. |
| `ch_water(chan_id)%salt(isalt)` | When `gw_solute_flag == 1`, `gwsol_salt == 1`, and the exchange direction requires channel-to-groundwater solute removal or groundwater-to-channel mass addition. | `ch_water(chan_id)%salt(isalt)` is increased when groundwater discharges to the channel and decreased when channel water seeps to groundwater, reflecting the transferred salt-ion mass. |
| `ch_water(chan_id)%cs(ics)` | When `gw_solute_flag == 1`, `gwsol_cons == 1`, and the exchange direction requires channel-to-groundwater solute removal or groundwater-to-channel mass addition. | `ch_water(chan_id)%cs(ics)` is increased when groundwater discharges to the channel and decreased when channel water seeps to groundwater, reflecting the transferred tracked constituent mass. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved. The earliest resolved commit, `9d9069f`, introduced `gwflow_floodplain` as a stub subroutine. `05cc429` expanded it into the full floodplain exchange routine, adding the groundwater, channel, heat, and solute transfer logic. `3cc92b5` then tightened the entry condition so the routine runs only when floodplain exchange is enabled and `gw_fpln_info` is allocated.

- `9d9069f` created the routine skeleton for floodplain groundwater exchange.
- `05cc429` added the full exchange algorithm, including channel-volume updates, groundwater storage updates, heat transfer, and solute/salt/constituent mass transfers.
- `3cc92b5` changed the activation guard from `gw_fp_flag == 1` to `gw_fp_flag == 1 .and. allocated(gw_fpln_info)`, preventing the routine from running before connection data are loaded.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_floodplain' has no extracted documentation comment.
- algorithm_steps revised: condensed the 8 draft blocks into 11 behavior-based steps grounded in the visible source lines.
- The extracted source declares `chan_width`, `chan_length`, `bed_thick`, `gw_head`, and `chan_heat`, but the visible routine does not assign all of them; the documentation reflects only uses visible in the provided source.
