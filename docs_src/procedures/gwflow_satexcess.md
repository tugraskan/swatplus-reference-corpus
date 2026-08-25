---
kind: procedure
symbol: gwflow_satexcess
title: gwflow_satexcess
status: filled
source_hash: 8c3b8e0ccfd884d1
version_label: SWAT+ 62.0.0
args:
  chan_id: '`chan_id` selects which channel’s connected groundwater cells are processed; the
    routine uses it to look up `gw_satx_info(chan_id)` connections and to update the matching
    `ch_stor(chan_id)`, `ch_out_d(chan_id)`, and `ch_water(chan_id)` channel states.'
locals:
  k: Loop counter over the groundwater cells connected to the selected channel.
  s: Loop counter over groundwater solutes when saturation excess carries dissolved mass.
  cell_id: Holds the current groundwater cell id taken from `gw_satx_info(chan_id)%cells(k)`
    so the routine can test and update that cell’s state.
  isalt: Loop counter over salt ions in the channel-water constituent array.
  ics: Loop counter over generic constituents in the channel-water constituent array.
  sol_index: Tracks which entry in the packed `solmass` array corresponds to the current solute,
    salt, or constituent load.
  dum: Unused debug scratch variable; it is only assigned in `if(chan_id == 3)` and when `heat_flux
    > gw_heat` to trip a marker value.
  satx_depth: Vertical depth of groundwater above land surface for an overflowing cell, computed
    as head minus elevation.
  satx_volume: Volume of groundwater above the surface that is removed from the aquifer and
    added to the channel.
  solmass: Temporary per-solute mass array holding the groundwater-borne load to transfer
    to the channel, capped by available groundwater mass.
  heat_flux: Temporary heat energy transferred from groundwater to the channel for the current
    overflowing cell.
  chan_heat: Temporary channel heat content accumulator used to recompute channel temperature
    after adding groundwater heat.
  chan_flow: Snapshot of the channel flow before adding saturation excess, used as the flow
    basis for the pre-transfer heat content calculation.
  chan_temp: Temporary channel temperature value before and after recalculation of heat content.
  gw_temp: Snapshot of the groundwater temperature used in the heat calculation.
  gw_storage: Snapshot of groundwater storage retained for debug or comparison during the
    heat branch.
  gw_heat: Temporary groundwater heat content used to compare against the transferred heat
    flux.
uses:
  gwflow_module: '`gwflow_module` supplies the per-cell groundwater geometry, status, and
    flux summary arrays that make the saturation-excess test and bookkeeping possible. `gw_state(cell_id)`
    provides the active flag, head, elevation, area, specific yield, and storage needed to
    detect overflow and compute the removed volume; `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo`
    store the water-loss summary; `gw_heat_ss` and `gw_heat_ss_yr` store the heat-loss summary
    when heat routing is enabled.'
  hydrograph_module: '`hydrograph_module` holds the mutable channel storage and daily output
    records that receive the overflowed water and updated temperature. `ch_stor(chan_id)`
    is the live channel water state being increased, while `ch_out_d(chan_id)` mirrors the
    resulting channel temperature for downstream daily reporting.'
  constituent_mass_module: '`constituent_mass_module` defines how many salts and generic constituents
    exist and provides the per-channel water constituent arrays that receive the transferred
    loads. `cs_db%num_salts` and `cs_db%num_cs` bound the loops, and `ch_water(chan_id)%salt(isalt)`
    and `ch_water(chan_id)%cs(ics)` are incremented with the masses taken from groundwater.'
---

<!-- facts:header -->

Transfers groundwater saturation-excess water from connected cells into a channel, and updates channel heat and constituent loads when the relevant switches are on.

## Bottom Line

`gwflow_satexcess` scans the groundwater cells connected to one channel and, for each active cell whose groundwater head is above land surface, computes the excess groundwater volume above the ground surface. It records that loss in the groundwater summary arrays and adds the same volume to the channel storage flow.

When heat or constituent routing is enabled, the routine also transfers groundwater heat and groundwater-borne loads into the channel state: channel temperature is recomputed from the added heat, and channel NO3, soluble P, salts, and other constituents are incremented from the transferred mass. These updates feed later groundwater and channel balance calculations, including the `gwflow_simulate` balance bookkeeping noted in the source comment.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel groundwater interaction processing, after `sd_channel_control3` has set up the channel-time-step hydrology and before the channel inflow/output states are finalized. `sd_channel_control3` calls it only when `bsn_cc%gwflow.eq.1`, so its results affect the groundwater balance arrays and the channel storage, temperature, and constituent state used later in the same routing step and in `gwflow_simulate` balance accounting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Enter and declare working variables, including counters, temporary flux accumulators, and scratch values for water, heat, and constituent transfer. | Sets up the routine’s local bookkeeping for per-cell traversal and for optional heat and constituent transfer calculations. |
| 2. Execute a small debug branch for channel 3 by setting `dum` when `chan_id == 3`. | Leaves a marker value in `dum`; this does not affect the modeled transfer path in the visible source. |
| 3. Exit immediately unless saturation-excess groundwater flow is enabled by `gw_satx_flag == 1`. | Skips all channel-cell processing when the groundwater saturation-excess process is turned off. |
| 4. Loop through the connected groundwater cells for the selected channel using `gw_satx_info(chan_id)%ncon` and `gw_satx_info(chan_id)%cells(k)`. | Visits each groundwater cell linked to the channel so the routine can test it for overflow conditions. |
| 5. Process only active cells and only when groundwater head is above land surface. | Filters to active groundwater cells that actually have saturation-excess conditions (`head > elev`). |
| 6. Compute the saturation-excess volume, count the event, and write the water loss to daily, monthly, and yearly groundwater hydrology summaries. | Derives the excess depth and volume from groundwater head, area, and specific yield, then stores the negative aquifer flux in `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo`. |
| 7. Add the excess volume to channel water storage and preserve the pre-addition flow for later heat calculations. | Updates `ch_stor(chan_id)%flo` with the transferred water and keeps the prior flow in `chan_flow` so heat content can be recomputed consistently. |
| 8. If groundwater heat routing is enabled, compute groundwater heat transfer and update channel temperature. | Uses groundwater temperature and transferred volume to form a heat flux, records the negative groundwater heat loss in `gw_heat_ss` and `gw_heat_ss_yr`, adds that heat to the channel, and recalculates `ch_stor(chan_id)%temp` and `ch_out_d(chan_id)%temp` from the new flow and heat content. |
| 9. If groundwater solute routing is enabled, compute transferred solute mass for each groundwater solute. | For each groundwater solute, computes mass from concentration and saturation-excess volume, caps it at available groundwater mass, and stores the negative aquifer loss in `gwsol_ss`, `gwsol_ss_sum`, and `gwsol_ss_sum_mo`. |
| 10. Add the transferred groundwater-borne loads to channel NO3 and soluble P. | Converts the first two solute masses from grams to kilograms and accumulates them in `ch_stor(chan_id)%no3` and `ch_stor(chan_id)%solp`. |
| 11. If salt routing is enabled, add the packed salt masses into the channel salt array. | Walks the configured salt count and accumulates each salt mass into `ch_water(chan_id)%salt(isalt)`. |
| 12. If generic constituent routing is enabled, add the packed constituent masses into the channel constituent array. | Walks the configured constituent count and accumulates each constituent mass into `ch_water(chan_id)%cs(ics)`. |
| 13. Finish the cell loop, exit the process-flag guard, and return to the caller. | Completes processing for all linked cells and returns control to `sd_channel_control3`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr` | `gw_state(cell_id)%elev, gw_state(cell_id)%head, gw_state(cell_id)%area, gw_state(cell_id)%spyd, gw_hyd_ss(cell_id)%satx, gw_hyd_ss_yr(cell_id)%satx, gw_hyd_ss_mo(cell_id)%satx, gw_state(cell_id)%stor, gw_heat_ss(cell_id)%satx, gw_heat_ss_yr(cell_id)%satx` |
| [sym:hydrograph_module] | `ch_stor, ch_out_d` | `ch_stor(chan_id)%flo, ch_stor(chan_id)%temp, ch_out_d(chan_id)%temp, ch_stor(chan_id)%no3, ch_stor(chan_id)%solp` |
| [sym:constituent_mass_module] | `cs_db, ch_water` | `cs_db%num_salts, ch_water(chan_id)%salt(isalt), cs_db%num_cs, ch_water(chan_id)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `satx_count` | When `gw_satx_flag == 1`, the routine is iterating a connected cell and `gw_state(cell_id)%head > gw_state(cell_id)%elev`. | Increments the saturation-excess event counter so output can track how many connected cells overflowed during the call. |
| `gw_hyd_ss(cell_id)%satx` | When `gw_satx_flag == 1`, the selected cell is active, and `gw_state(cell_id)%head > gw_state(cell_id)%elev`. | Stores the per-cell saturation-excess water loss as a negative groundwater flux for the current day. |
| `gw_hyd_ss_yr(cell_id)%satx` | When `gw_satx_flag == 1`, the selected cell is active, and `gw_state(cell_id)%head > gw_state(cell_id)%elev`. | Accumulates the year-to-date saturation-excess groundwater loss for that cell. |
| `gw_hyd_ss_mo(cell_id)%satx` | When `gw_satx_flag == 1`, the selected cell is active, and `gw_state(cell_id)%head > gw_state(cell_id)%elev`. | Accumulates the month-to-date saturation-excess groundwater loss for that cell. |
| `ch_stor(chan_id)%flo` | When `gw_satx_flag == 1`, the selected cell is active, and `gw_state(cell_id)%head > gw_state(cell_id)%elev`. | Adds the saturation-excess volume to channel flow storage so the channel receives the groundwater water volume. |
| `gw_heat_ss(cell_id)%satx` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_heat_flag == 1`. | Stores the per-cell daily groundwater heat loss as a negative flux for the heat balance. |
| `gw_heat_ss_yr(cell_id)%satx` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_heat_flag == 1`. | Accumulates the year-to-date groundwater heat loss for that cell. |
| `ch_stor(chan_id)%temp` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_heat_flag == 1`. | Recomputes the live channel temperature from the updated heat content and flow, or sets it to zero if the channel flow is not positive. |
| `ch_out_d(chan_id)%temp` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_heat_flag == 1`. | Copies the updated channel temperature into the daily output record for channel diagnostics. |
| `gwsol_ss(cell_id)%solute(s)%satx` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_solute_flag == 1`. | Stores the per-cell solute mass leaving groundwater as a negative groundwater flux for the current solute. |
| `gwsol_ss_sum(cell_id)%solute(s)%satx` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_solute_flag == 1`. | Accumulates the year-to-date groundwater solute loss for each solute in the per-cell summary array. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%satx` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_solute_flag == 1`. | Accumulates the month-to-date groundwater solute loss for each solute in the per-cell summary array. |
| `ch_stor(chan_id)%no3` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_solute_flag == 1`. | Adds groundwater-borne nitrate mass to the channel storage record, converting grams to kilograms. |
| `ch_stor(chan_id)%solp` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, and `gw_solute_flag == 1`. | Adds groundwater-borne soluble phosphorus mass to the channel storage record, converting grams to kilograms. |
| `ch_water(chan_id)%salt(isalt)` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, `gw_solute_flag == 1`, and `gwsol_salt == 1`. | Adds the transferred salt mass for each configured salt ion to the channel water constituent store. |
| `ch_water(chan_id)%cs(ics)` | When `gw_satx_flag == 1`, the selected cell is active, `gw_state(cell_id)%head > gw_state(cell_id)%elev`, `gw_solute_flag == 1`, and `gwsol_cons == 1`. | Adds the transferred generic constituent mass for each configured constituent to the channel water constituent store. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in the initial lineage source snapshot (`df07e3f`/`9d9069f`), and later `e6ca4de` expanded it to include channel output heat handling and more complete transfer bookkeeping. The diff shows the routine gained `ch_out_d` use, new local heat variables, the channel-flow snapshot used for temperature recomputation, and debug marker branches; the saturation-excess water, solute, salt, and constituent transfer loops were retained.

- `9d9069f` introduced `gwflow_satexcess` as a new saturation-excess transfer routine that computed excess groundwater volume, updated groundwater summary arrays, and added the same volume to channel flow storage.
- `e6ca4de` extended the routine with `ch_out_d` temperature output, additional heat-transfer bookkeeping (`chan_flow`, `chan_heat`, `gw_temp`, `gw_storage`, `gw_heat`), and debug markers, while preserving the existing water and solute transfer logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_satexcess' has no extracted documentation comment.
- algorithm_steps revised: merged the original block splits into 13 source-backed steps that follow the actual control flow in lines 31-133.
- `sol_index` and `dum` are present in the source but appear to serve indexing/debug roles only; `dum` is explicitly used as a marker in two branches.
- The source contains tab-indented debug lines and an `if(chan_id == 3)` marker branch; these look non-physical but are part of the tracked source.
