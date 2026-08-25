---
kind: procedure
symbol: gwflow_tile
title: gwflow_tile
status: filled
source_hash: f518613875870336
version_label: SWAT+ 62.0.0
args:
  chan_id: '`chan_id` selects the specific channel whose connected groundwater cells are processed
    and whose channel storage, temperature, and water-quality state are updated.'
locals:
  k: Loop counter over the groundwater cells connected to the current channel.
  cell_id: Holds the cell id for the current connected cell pulled from `gw_tile_info(chan_id)%cells(k)`.
  s: Loop counter over groundwater solutes when transferring dissolved mass from the cell
    to the channel.
  isalt: Loop counter over simulated salt ions in channel water quality mass updates.
  ics: Loop counter over simulated non-salt constituents in channel water quality mass updates.
  sol_index: Tracks which entry in the groundwater solute mass array corresponds to the next
    constituent transferred to channel water.
  chan_volume: Stores the channel water volume before tile drainage is added, so the routine
    can compute the mixed channel heat content using the pre-exchange volume.
  tile_elev: Computes the subsurface drain elevation for the current cell as land-surface
    elevation minus tile depth.
  head_diff: Stores the groundwater head above the drain; it is the driving head used in the
    Darcy-style tile drainage rate.
  q: Tile-drain outflow volume from the current cell to the channel for this call, capped
    by available groundwater storage.
  solmass: Temporary per-solute transfer mass from groundwater to channel, limited so the
    routine does not remove more solute mass than the cell contains.
  heat_flux: Temporary heat content moved with the tile drainage water from groundwater to
    the channel, limited by available groundwater heat storage.
  chan_heat: Temporary channel heat content used to recompute channel temperature after groundwater
    heat is added.
uses:
  gwflow_module: '`gwflow_module` provides the groundwater cell state and all groundwater
    summary arrays that this routine reads and updates. `gw_state(cell_id)%elev`, `%head`,
    and `%stor` control whether drainage occurs and how much water can be removed, while `gw_hyd_ss`,
    `gw_hyd_ss_yr`, `gw_hyd_ss_mo`, `gw_heat_ss`, and `gw_heat_ss_yr` record the tile-drain
    flux for hydrology and heat accounting.'
  hydrograph_module: '`hydrograph_module` holds the channel storage and output records that
    receive the drainage water and related temperature changes. `ch_stor(chan_id)%flo` is
    increased by the drained water, `ch_stor(chan_id)%temp` is recomputed from the mixed heat
    content, and `ch_out_d(chan_id)%temp` is set so the daily channel output reflects the
    updated temperature.'
  constituent_mass_module: '`constituent_mass_module` defines how many salts and other constituents
    the model tracks and provides the channel water-quality arrays that receive transferred
    mass. `cs_db%num_salts` and `cs_db%num_cs` determine the loop bounds, and `ch_water(chan_id)%salt(isalt)`
    and `%cs(ics)` are incremented with the groundwater solute masses moved by tile drainage.'
---

<!-- facts:header -->

Moves groundwater drainage from connected cells into a channel when tile drainage is enabled. It reduces cell storage, updates groundwater water/heat/solute summaries, and adds the transferred water and constituents to channel state.

## Bottom Line

When `gw_tile_flag` is on, `gwflow_tile` loops over the cells connected to a channel and simulates tile-drain outflow from any active cell whose groundwater head is above the drain elevation. The outflow is limited by available groundwater storage, then written back to `gw_state(cell_id)%stor` and to the groundwater hydrology summaries so the daily, monthly, and yearly balance terms reflect water leaving the aquifer.

If groundwater heat or solute transport is active, the same drainage flux also moves heat and dissolved material from groundwater into the channel. The routine updates the groundwater heat summaries, channel temperature, channel NO3/soluble P, and optional salt/constituent masses so downstream channel routing and water-quality accounting see the transferred loads.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `sd_channel_control3` after the groundwater-flow branch is activated with `bsn_cc%gwflow.eq.1` and after other channel-groundwater exchange routines are called. It uses the channel and groundwater state already prepared for the current channel and then feeds updated channel flow, temperature, and constituent loads into the later channel routing and output calculations that depend on `ch_stor`, `ch_out_d`, and the groundwater summary arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether tile drainage is enabled. | The routine exits immediately unless `gw_tile_flag == 1`; when active, it captures the starting channel water volume from `ch_stor(chan_id)%flo` before any groundwater inflow is added. |
| 2. Walk the connected groundwater cells for this channel. | It loops from 1 to `gw_tile_info(chan_id)%ncon` and pulls each connected `cell_id` from `gw_tile_info(chan_id)%cells(k)`. |
| 3. Skip inactive cells and compute drain elevation. | Only cells with `gw_state(cell_id)%stat == 1` are processed, and the tile-drain elevation is computed as ground elevation minus `gw_tile_depth(cell_id)`. |
| 4. Drain groundwater only when the water table is above the tile. | If groundwater head exceeds the tile elevation, the routine computes the head difference, applies `gw_tile_drain_area(cell_id) * gw_tile_K(cell_id) * head_diff`, caps the flow by available storage, and subtracts `Q` from `gw_state(cell_id)%stor`. |
| 5. Record hydrology fluxes and add water to the channel. | The drainage flux is stored as a negative source/sink term in `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo`, then added to `ch_stor(chan_id)%flo`. |
| 6. Convert the drained water to heat transfer when heat routing is on. | When `gw_heat_flag == 1`, the routine computes heat content carried by the drainage water, limits it by available groundwater heat storage, records the negative heat flux in `gw_heat_ss` and `gw_heat_ss_yr`, mixes the heat into the channel, recomputes `ch_stor(chan_id)%temp`, and mirrors that temperature to `ch_out_d(chan_id)%temp`. |
| 7. Transfer dissolved groundwater solutes to the channel when solute routing is on. | When `gw_solute_flag == 1`, the routine loops over `gw_nsolute`, computes each solute mass as `Q * gwsol_state(cell_id)%solute(s)%conc`, caps it by available mass, records negative tile fluxes in `gwsol_ss`, `gwsol_ss_sum`, and `gwsol_ss_sum_mo`, and adds the transferred mass to channel NO3, soluble P, salts, and other constituents. |
| 8. Finish the cell and channel update. | The routine closes the active-cell and active-channel checks, ends the connected-cell loop, returns to the caller, and leaves the updated groundwater and channel state in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr` | `gw_state(cell_id)%elev, gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%tile, gw_hyd_ss_yr(cell_id)%tile, gw_hyd_ss_mo(cell_id)%tile, gw_heat_ss(cell_id)%tile, gw_heat_ss_yr(cell_id)%tile` |
| [sym:hydrograph_module] | `ch_stor, ch_out_d` | `ch_stor(chan_id)%flo, ch_stor(chan_id)%temp, ch_out_d(chan_id)%temp, ch_stor(chan_id)%no3, ch_stor(chan_id)%solp` |
| [sym:constituent_mass_module] | `cs_db, ch_water` | `cs_db%num_salts, ch_water(chan_id)%salt(isalt), cs_db%num_cs, ch_water(chan_id)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(cell_id)%stor` | When `gw_tile_flag == 1`, `gw_state(cell_id)%stat == 1`, `gw_state(cell_id)%head > tile_elev`, and the computed outflow `Q` is limited and subtracted. | The available groundwater storage in the current cell is reduced by the tile-drain flux so the cell cannot supply more water than it contains. |
| `gw_hyd_ss(cell_id)%tile` | Under the same tile-drain conditions when `Q` has been computed for the active cell. | The daily groundwater hydrology summary records a negative tile-drain flux for this cell, indicating water leaving the aquifer to the channel. |
| `gw_hyd_ss_yr(cell_id)%tile` | When tile drainage occurs for the current cell during this call. | The yearly groundwater hydrology summary accumulates the same negative tile-drain flux so annual reporting reflects total groundwater losses to the channel. |
| `gw_hyd_ss_mo(cell_id)%tile` | When tile drainage occurs for the current cell during this call. | The monthly groundwater hydrology summary accumulates the same negative tile-drain flux so monthly reporting reflects total groundwater losses to the channel. |
| `ch_stor(chan_id)%flo` | When an active cell drains groundwater to the channel and `Q` has been computed. | Channel flow storage increases by the drained water volume, representing groundwater entering the channel routing store. |
| `gw_heat_ss(cell_id)%tile` | When `gw_heat_flag == 1` and tile drainage occurs. | The daily groundwater heat summary records a negative heat flux equal to the heat carried out of the aquifer by tile drainage water. |
| `gw_heat_ss_yr(cell_id)%tile` | When `gw_heat_flag == 1` and tile drainage occurs. | The yearly groundwater heat summary accumulates the same negative heat transfer so annual heat accounting includes tile drainage losses. |
| `ch_stor(chan_id)%temp` | When `gw_heat_flag == 1` and the drained water heat is mixed into the channel. | Channel water temperature is recomputed after adding groundwater heat content, so the channel state reflects the warmed or cooled mixed water. |
| `ch_out_d(chan_id)%temp` | When `gw_heat_flag == 1` and channel temperature has been recomputed. | The daily channel output temperature is set equal to the updated channel storage temperature so downstream output uses the post-exchange value. |
| `gwsol_ss(cell_id)%solute(s)%tile` | When `gw_solute_flag == 1`, the current cell drains, and each solute mass is computed for `s=1,gw_nsolute`. | The daily groundwater solute summary records negative tile-drain fluxes for each solute moved from groundwater to the channel. |
| `gwsol_ss_sum(cell_id)%solute(s)%tile` | When `gw_solute_flag == 1` and tile drainage occurs. | The cumulative groundwater solute summary accumulates the tile-drain solute losses so total-source accounting retains the transferred mass. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%tile` | When `gw_solute_flag == 1` and tile drainage occurs. | The monthly cumulative groundwater solute summary accumulates the same transferred masses for month-scale reporting. |
| `ch_stor(chan_id)%no3` | When `gw_solute_flag == 1`, after `solmass(1)` is computed for NO3 and capped by available groundwater solute mass. | Channel NO3 mass increases by the groundwater-derived nitrate mass transferred by tile drainage. |
| `ch_stor(chan_id)%solp` | When `gw_solute_flag == 1`, after `solmass(2)` is computed for soluble phosphorus and capped by available groundwater solute mass. | Channel soluble phosphorus mass increases by the groundwater-derived solute mass transferred by tile drainage. |
| `ch_water(chan_id)%salt(isalt)` | When `gw_solute_flag == 1` and `gwsol_salt == 1`, for each salt index up to `cs_db%num_salts`. | Channel salt mass increases by the groundwater solute mass assigned to each tracked salt ion. |
| `ch_water(chan_id)%cs(ics)` | When `gw_solute_flag == 1` and `gwsol_cons == 1`, for each constituent index up to `cs_db%num_cs`. | Channel constituent mass increases by the groundwater solute mass assigned to each tracked non-salt constituent. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_tile` was introduced in commit `df07e3f` as part of the initial source import. `94b6dec` kept the same drainage logic but updated the module import to `use hydrograph_module, only : ch_stor` and left the routine structurally unchanged. `9d9069f` changed the groundwater summary targets from `gw_ss`/`gw_ss_sum` to `gw_hyd_ss`/`gw_hyd_ss_yr`/`gw_hyd_ss_mo` and added the heat-transfer branch plus `ch_out_d(chan_id)%temp` handling. `e6ca4de` extended the routine to use `ch_out_d` and refined heat handling and array references. `39fabde` only initialized local scalars to zero and did not change the algorithm.

- df07e3f established the original tile-drain procedure: loop connected cells, compute Darcy-style outflow, update groundwater storage, add flow to the channel, and transfer solute mass.
- 94b6dec preserved the tile-drain algorithm while aligning the implementation with the imported source and explicit `ch_stor` dependency.
- 9d9069f redirected the hydrology summary writes to the newer `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo` arrays and added heat-state updates, including channel temperature output.
- e6ca4de kept the same drainage behavior but added `ch_out_d(chan_id)%temp` synchronization and refined the heat-transfer branch with the expanded `ch_out_d` dependency.
- 39fabde changed only local variable initialization, preventing undefined initial values without changing model logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_tile' has no extracted documentation comment.
- algorithm_steps revised: condensed repeated low-level lines into 8 source-backed model steps and aligned the steps with the current line-numbered source block.
- Source uncertainty note: `sol_index` is used to index solute-to-constituent transfers, but no separate declaration comment explains its mapping beyond the source loop order.
