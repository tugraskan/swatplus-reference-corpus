---
kind: procedure
symbol: command
title: command
status: filled
source_hash: 5f63c7ee09541881
version_label: SWAT+ main @ cb442f7c05fc
locals:
  hyd_flo: Sub-daily flow hydrograph buffer (dimensioned by time step).
  in: Counter over an object's receiving (incoming) hydrographs.
  iob: Index of an upstream (source) object contributing inflow.
  iday: Day index into the object's stored hydrographs.
  isd: SWAT-deg channel counter.
  ires: Reservoir number.
  irec: Recall (point-source) counter.
  iout: Counter over an object's outflow (downstream) connections.
  ihtyp: Hydrograph-type index.
  iaq: Aquifer counter.
  j: General counter.
  ihyd: Incoming hydrograph-type index for the current connection.
  idr: Delivery-ratio index.
  iwro: Water-routing object index.
  conv: Unit conversion factor.
  frac_in: Fraction of an upstream object's hydrograph delivered to this object.
  ts1: Sub-daily time-step start index.
  ts2: Sub-daily time-step end index.
  iw: Water-allocation object counter.
  iwallo: Water-allocation database index passed to `wallo_control`.
  i_count: gwflow counter.
  i_mfl: gwflow counter.
  i_chan: gwflow channel counter.
  iob_chan: gwflow object index for a channel.
  sumflo: Accumulated flow used in gwflow channel handling.
uses:
  time_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  hydrograph_module: Provides object/hydrograph/constituent state and module data used to
    route inflow and dispatch control routines.
  ru_module: Provides object/hydrograph/constituent state and module data used to route inflow
    and dispatch control routines.
  channel_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  hru_lte_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  aquifer_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  sd_channel_module: Provides object/hydrograph/constituent state and module data used to
    route inflow and dispatch control routines.
  reservoir_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  organic_mineral_mass_module: Provides object/hydrograph/constituent state and module data
    used to route inflow and dispatch control routines.
  constituent_mass_module: Provides object/hydrograph/constituent state and module data used
    to route inflow and dispatch control routines.
  hru_module: Provides object/hydrograph/constituent state and module data used to route inflow
    and dispatch control routines.
  basin_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  maximum_data_module: Provides object/hydrograph/constituent state and module data used to
    route inflow and dispatch control routines.
  gwflow_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  soil_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  recall_module: Provides object/hydrograph/constituent state and module data used to route
    inflow and dispatch control routines.
  water_allocation_module: Provides object/hydrograph/constituent state and module data used
    to route inflow and dispatch control routines.
---

<!-- facts:header -->

Steps through every spatial object in routing order each day. For each object it sums the incoming hydrographs from upstream objects, calls the object's control routine (HRU, channel, reservoir, aquifer, routing unit, etc.), and then calls the object's output routines.

After the HRU loop, it calls the legacy carbon writers once for each enabled output interval. Those writers iterate over all HRUs internally, so placing the calls outside the loop prevents duplicated output rows.

## Bottom Line

`command` is the daily routing driver. Starting from the first spatial object, it walks the object list (`icmd`), and for each object zeros the incoming hydrographs, accumulates flow/sediment/nutrient/constituent loads from all receiving (upstream) objects — separated into surface, lateral, tile, and aquifer components for land objects — then dispatches to the matching control routine by object type.

After the object is simulated it routes the outflow to downstream objects and invokes the per-object and basin output routines. It is the central loop that ties together the land phase, channel/reservoir/aquifer routing, water allocation, and all output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called once per day from `time_control`, the top of the simulation time loop. It is the routing dispatcher: it orchestrates the per-object control routines (which do the physics) in upstream-to-downstream order, so every object's inflow is assembled from already-simulated upstream objects. Its outputs feed the object and basin output files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Iterate the dispatched collection | Walks the spatial-object list via `icmd` until it reaches 0, processing one object per iteration in routing order. |
| 2. Dispatch by selected value | Selects processing by the object's type (`ob(icmd)%typ`): HRU, RU, HRU-LTE, channel, reservoir, aquifer, recall, etc. |
| 3. Handle `hru*` (2 cases) | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 4. Handle `ru` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 5. Handle `gwflow` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 6. Handle `aqu` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 7. Handle `res` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 8. Handle `recall` | Calls the matching object control routine (e.g. `hru_control`, `sd_channel_control3`, `res_control`, `aqu_1d_control`) and then the object's output routines. |
| 9. Handle `dr` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 10. Handle `outlet` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 11. Handle `chandeg` | Performs this step of the per-object daily routing loop (assemble inflow, dispatch to the control routine, route outflow, write output). |
| 12. Emit legacy carbon reports once | After the HRU loop, calls the enabled legacy carbon and carbon-variable writers once per daily, monthly, or yearly output event; each writer traverses all HRUs internally. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%step` |
| [sym:hydrograph_module] | `sp_ob1, ob, hdsep1, sp_ob` | `sp_ob1%objs, ob(icmd)%typ, ob(icmd)%day_cur, ob(icmd)%day_max, ob(icmd)%hin, ob(icmd)%hin_sur, ob(icmd)%hin_lat, ob(icmd)%hin_til, ob(icmd)%tsin, ob(icmd)%peakrate, ob(icmd)%rcv_tot, ob(icmd)%obj_in(in), ob(icmd)%ihtyp_in(in), ob(icmd)%frac_in(in), ob(iob)%peakrate, ob(icmd)%obtyp_in(in), ob(icmd)%htyp_in(in), ob(iob)%hd(3), ob(iob)%hd(5), ob(iob)%hd(4), ob(iob)%hd(ihyd), ob(icmd)%hin_aqu, ob(iob)%hd(1), hdsep1%flo_surq, ob(iob)%hdsep%flo_surq, hdsep1%flo_latq, ob(iob)%hdsep%flo_latq, hdsep1%flo_gwsw, ob(iob)%hdsep%flo_gwsw, hdsep1%flo_swgw, ob(iob)%hdsep%flo_swgw, hdsep1%flo_satex, ob(iob)%hdsep%flo_satex, hdsep1%flo_satexsw, ob(iob)%hdsep%flo_satexsw, hdsep1%flo_tile, ob(iob)%hdsep%flo_tile, ob(icmd)%hdsep_in%flo_surq, ob(icmd)%hdsep_in%flo_latq, ob(icmd)%hdsep_in%flo_gwsw, ob(icmd)%hdsep_in%flo_swgw, ob(icmd)%hdsep_in%flo_satex, ob(icmd)%hdsep_in%flo_satexsw, ob(icmd)%hdsep_in%flo_tile, ob(icmd)%hin_d(in), ob(iob)%day_cur, ob(iob)%typ, ob(iob)%hyd_flo(iday,:), ob(iob)%hd(4)%flo, ob(iob)%hd(5)%flo, ob(iob)%num, ob(icmd)%area_ha, ob(icmd)%hin_sur%flo, ob(icmd)%hin_lat%flo, ob(icmd)%hin_til%flo, ob(icmd)%num, sp_ob%gwflow, ob(icmd)%dfn_tot` |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:channel_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |
| [sym:organic_mineral_mass_module] | `no resolved imported state` |  |
| [sym:constituent_mass_module] | `cs_db, obcs` | `cs_db%num_tot, obcs(icmd)%hin, obcs(icmd)%hin_sur, obcs(icmd)%hin_lat, obcs(icmd)%hin_til, obcs(icmd)%hin_sur(1), obcs(iob)%hd(3), obcs(icmd)%hin_til(1), obcs(iob)%hd(5), obcs(icmd)%hin_lat(1), obcs(iob)%hd(4), obcs(iob)%hd(ihyd), obcs(icmd)%hin_aqu(1), obcs(iob)%hd(1), obcs(icmd)%hin(1), obcs(icmd)%hcsin_d(in)` |
| [sym:hru_module] | `ihru, hru` | `ihru, hru` |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wallo_db` |
| [sym:gwflow_module] | `no resolved imported state` |  |
| [sym:soil_module] | `no resolved imported state` |  |
| [sym:recall_module] | `recall_db` | `recall_db(irec)%org_min%tstep` |
| [sym:water_allocation_module] | `wallo` | `wallo(:)%trn_cur, wallo(iwallo)%trn_cur, wallo(iwallo)%trn_obs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `icmd` | At loop start and end of each iteration. | Index of the spatial object currently being processed. `icmd = sp_ob1%objs`, then advanced to `ob(icmd)%cmd_next` each loop. |
| `wallo(:)%trn_cur` | At entry, before the object loop. | Resets the current water-allocation transfer counter for all allocation objects. `wallo(:)%trn_cur = 1`. |
| `ob(icmd)%day_cur` | Each iteration, per object. | Advances the current-day index into the object's stored hydrographs (HRUs/RUs may lag into the next day). `ob(icmd)%day_cur = ob(icmd)%day_cur + 1` (wraps at `day_max`). |
| `ob(icmd)%hin` | Zeroed then summed from upstream. | Total incoming hydrograph for the object. `ob(icmd)%hin = hz`, then `+ frac_in * ob(iob)%hd(ihyd)` for non-land objects. |
| `ob(icmd)%hin_sur` | Zeroed then accumulated. | Surface-runoff component of inflow (for land objects). `ob(icmd)%hin_sur = hz`, then `+ frac_in * ob(iob)%hd(3 or ihyd)`. |
| `ob(icmd)%hin_lat` | Zeroed then accumulated. | Lateral-flow component of inflow. `ob(icmd)%hin_lat = hz`, then `+ frac_in * ob(iob)%hd(4 or ihyd)`. |
| `ob(icmd)%hin_til` | Zeroed then accumulated. | Tile-flow component of inflow. `ob(icmd)%hin_til = hz`, then `+ frac_in * ob(iob)%hd(5 or ihyd)`. |
| `ht1` | Zeroed then used to accumulate `ob(icmd)%hin`. | Working hydrograph for one upstream contribution. `ht1 = hz`, then `ht1 = frac_in * ob(iob)%hd(ihyd)` for non-land objects. |
| `obcs(icmd)%hin` | When constituents are active. | Total incoming constituent hydrograph, zeroed. `obcs(icmd)%hin = hin_csz` when constituents are simulated. |
| `obcs(icmd)%hin_sur` | When constituents are active. | Surface-component constituent inflow, zeroed. `obcs(icmd)%hin_sur = hin_csz`. |
| `obcs(icmd)%hin_lat` | When constituents are active. | Lateral-component constituent inflow, zeroed. `obcs(icmd)%hin_lat = hin_csz`. |
| `obcs(icmd)%hin_til` | When constituents are active. | Tile-component constituent inflow, zeroed. `obcs(icmd)%hin_til = hin_csz`. |
| `hcs1` | At per-object setup. | Working constituent hydrograph 1, zeroed. `hcs1 = hin_csz`. |
| `hcs2` | At per-object setup. | Working constituent hydrograph 2, zeroed. `hcs2 = hin_csz`. |
| `hcs3` | At per-object setup. | Working constituent hydrograph 3, zeroed. `hcs3 = hin_csz`. |
| `ob(icmd)%tsin` | At per-object setup. | Sub-daily inflow time series, zeroed. `ob(icmd)%tsin = 0.`. |
| `ob(icmd)%peakrate` | Zeroed then taken from the upstream object. | Peak flow rate carried for the object. `ob(icmd)%peakrate = 0.`, then `= ob(iob)%peakrate` from upstream. |
| `ob(icmd)%obtyp_in(in)` | Used in the receiving loop to route inflow into the right component. | Type of the in-th upstream object; selects how its hydrograph is split. Read to branch the inflow accumulation (`"hru"`/`"ru"`/`"hru_lte"` vs other). |
| `obcs(icmd)%hin_sur(1)` | Summed across upstream objects. | Accumulated surface-component constituent inflow. `obcs(icmd)%hin_sur(1) = obcs(icmd)%hin_sur(1) + frac_in * obcs(iob)%hd(3 or ihyd)`. |
| `obcs(icmd)%hin_til(1)` | Summed across upstream objects. | Accumulated tile-component constituent inflow. `obcs(icmd)%hin_til(1) = obcs(icmd)%hin_til(1) + frac_in * obcs(iob)%hd(5 or ihyd)`. |
| `obcs(icmd)%hin_lat(1)` | Summed across upstream objects. | Accumulated lateral-component constituent inflow. `obcs(icmd)%hin_lat(1) = obcs(icmd)%hin_lat(1) + frac_in * obcs(iob)%hd(4 or ihyd)`. |
| `ob(icmd)%hin_aqu` | Summed for `"aqu"` hydrograph types. | Aquifer-component inflow to the object. `ob(icmd)%hin_aqu = ob(icmd)%hin_aqu + frac_in * ob(iob)%hd(ihyd)` for aquifer-type inflow. |
| `obcs(icmd)%hin_aqu(1)` | Summed for aquifer hydrograph types. | Aquifer-component constituent inflow. `obcs(icmd)%hin_aqu(1) = obcs(icmd)%hin_aqu(1) + frac_in * obcs(iob)%hd(ihyd)`. |
| `hdsep1%flo_surq` | Per upstream contribution, accumulated into `ob(icmd)%hdsep_in`. | Surface-runoff component for hydrograph separation tracking. `hdsep1%flo_surq = frac_in * ob(iob)%hdsep%flo_surq` (then added to `hdsep_in`). |

## File I/O

<!-- facts:io -->


## Lineage

`command.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 34 non-merge commit(s) since, most recently `cb442f7` (2026-07-06, "updating reference dataset to revision 62"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `command.f90` are listed.

- `cb442f7` (2026-07-06) — updating reference dataset to revision 62
- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `821a63e` (2026-06-02) — reinstate CSU outputs and print flags
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `b7fd8ef` (2026-05-18) — Updated code in command.f90 to be more clear with when soil_nutcarb.write is being called.
- `d7ecb7a` (2026-05-07) — Added if (allocated(x) statements to prevent gfortran runtime errors in situations where water allocation is not being run.
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'command' has no extracted documentation comment.
- Central daily routing loop with 70+ callees (mostly per-object control and output routines); state changes are the per-object inflow-hydrograph assembly. 10 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
