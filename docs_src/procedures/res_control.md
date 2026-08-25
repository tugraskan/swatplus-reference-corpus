---
kind: procedure
symbol: res_control
title: res_control
status: filled
source_hash: 39fff4dee620f9e4
version_label: SWAT+ 62.0.0
args:
  jres: Selects the reservoir object to process; all storage, release, weather, and output
    state updates are applied to `res_ob(jres)`, `res(jres)`, and the matching linked hydrographs
    for that reservoir.
locals:
  ii: Loop counter used to split a subdaily reservoir outflow across `time%step` time steps
    when writing `ob(icmd)%ts(1,ii)`.
  idat: Points to the reservoir property record in `res_dat` for the current reservoir, so
    the routine can look up release type and constituent database indices.
  irel: Holds the decision-table release identifier taken from `res_dat(idat)%release` and
    passed to `dtbl_res`/`conditions`/`res_hydro` when the reservoir uses table-based release
    control.
  iob: Linked object index for the reservoir outlet connection; used to find the weather station,
    pass the correct object into nutrient processing, and accumulate object-level hydrograph
    totals.
  ictbl: Holds the release-table identifier used by `res_rel_conds` when the reservoir uses
    condition-table release control instead of decision tables.
  icon: Constituent database index taken from `res_dat(idat)%cs` and passed to `res_cs` to
    choose the reservoir constituent set.
  pvol_m3: Principal spillway target volume copied from `res_ob(jres)%pvol` and passed into
    `res_hydro` as the principal operating storage reference.
  evol_m3: Emergency spillway target volume copied from `res_ob(jres)%evol` and passed into
    `res_hydro` as the emergency operating storage reference.
  dep: Computed water depth over the reservoir surface from current reservoir flow and area;
    used as part of the release-conditions setup before calling `conditions`.
  weir_hgt: Copies the reservoir weir height from `res_ob(jres)%weir_hgt` for the release-condition
    evaluation setup.
  alpha_up: Exponential smoothing factor for increasing outflow; used to damp sudden jumps
    in `ht2%flo` when the new release is larger than the previous day’s release.
  alpha_down: Exponential smoothing factor for decreasing outflow; used to damp sudden drops
    in `ht2%flo` when the new release is smaller than the previous day’s release.
  dom: Current day-of-month copied from `time%day_mo` and used to detect month boundaries
    for the inflow and demand memory arrays.
  mon: Current month copied from `time%mo` and retained alongside the day and end-of-month
    flag for the daily control context.
  end_of_mo: End-of-month flag copied from `time%end_mo`; when set, the routine compresses
    daily arrays into monthly means and shifts the reservoir memory windows.
  n_days: Size of the current daily inflow array, used when appending today’s inflow and demand
    to the monthly storage arrays.
  daily_inflow: Stores today’s incoming flow volume (`ht1%flo`) so it can be appended to the
    reservoir’s monthly inflow history.
  temp_array: Temporary growth buffer used to append one more day to `res_ob(jres)%daily_inflow_array`
    or `res_ob(jres)%daily_demand_array` before `move_alloc` replaces the old array.
  daily_demand: Stores today’s irrigation demand for the reservoir so it can be appended to
    the monthly demand history.
  irrig_track_b: Remembers the last irrigation-track value processed so daily irrigation demand
    is only refreshed when the reservoir’s track code changes.
uses:
  basin_module: '`basin_module` provides the basin-wide control flags that decide whether
    reservoir lapse correction and groundwater seepage routing are active, and the print skip
    setting that gates reservoir output storage.'
  reservoir_data_module: '`reservoir_data_module` supplies the operational metadata for reservoir
    `jres`, including when it becomes active, whether release is simulated or measured, and
    which sediment, nutrient, salt, or constituent tables apply.'
  time_module: '`time_module` supplies the current calendar position and subdaily step count,
    which control activation timing, monthly accumulation, end-of-month averaging, and subdaily
    hydrograph splitting.'
  reservoir_module: '`reservoir_module` holds the reservoir object itself, including outlet
    connections, irrigation tracking, storage-volume coefficients, release lag parameters,
    and the daily arrays that this routine updates.'
  climate_module: '`climate_module` matters because reservoir evaporation and precipitation
    are computed from the assigned weather station’s daily PET and precipitation, and those
    weather values may be lapse-adjusted before use.'
  hydrograph_module: '`hydrograph_module` matters because this routine reads the incoming
    hydrograph, writes the reservoir outflow hydrograph, updates total inflow/outflow records,
    and stores subdaily routed flow slices.'
  conditional_module: '`conditional_module` supplies the reservoir decision-table database
    used when the reservoir release is driven by table conditions rather than a direct condition-table
    release value.'
  water_body_module: '`water_body_module` holds the reservoir water-body state that stores
    surface area and the daily evaporation, precipitation, and seepage volumes computed here.'
  constituent_mass_module: '`constituent_mass_module` matters because the routine updates
    reservoir pesticide, salt, and other constituent routing only when those constituent counts
    are enabled and copies the resulting masses into the outlet hydrographs.'
---

<!-- facts:header -->

Routes daily reservoir inflow through storage, release rules, water balance, and constituent updates for one reservoir object.

## Bottom Line

`res_control` is the main daily control routine for a reservoir. It starts from the incoming hydrograph for reservoir `jres`, applies climate lapse adjustment if enabled, evaluates the reservoir’s release logic, and updates storage, surface area, seepage, evaporation, and outflow records.

It also updates monthly inflow and irrigation-demand memory, passes flow and constituent loads to the linked hydrograph objects, and marks the reservoir as processed for water-allocation logic. The routine matters because it is the place where reservoir routing, water quality, and output bookkeeping are tied together for the day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine when the current object is a reservoir and has routed inflow to process, and `wallo_control` also calls it after a water-allocation transfer to force the reservoir state to be updated for that day. Its results feed downstream reservoir storage, routed outflow, constituent loads, and daily reservoir output records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize hydrograph state from the incoming reservoir object | Copies the incoming surface hydrograph into `ht1`, clears the outgoing hydrograph with `resz`, and clears outgoing constituents with `hin_csz` so the day's routing starts from the current inflow only. |
| 2. Check whether the reservoir is operational yet | Skips all reservoir routing until the simulation date is past the reservoir’s startup year and month in `res_hyd(jres)`. |
| 3. Load linked object and weather station, then apply optional lapse correction | Finds the linked outlet object and weather station, copies the station weather into `w`, optionally calls `cli_lapse`, and writes the adjusted weather back to `wst(iwst)%weat`. |
| 4. Bind the shared water-body pointers and add inflow to reservoir storage | Points `wbody` and related pointers at the reservoir storage and parameter records, then adds the incoming hydrograph `ht1` into `res(jres)`. |
| 5. Capture daily time context and compute irrigation demand for the day | Copies day, month, and end-of-month flags from `time`, stores the current inflow, and sets `daily_demand` either to zero or to `res_ob(jres)%d_irrig_day` depending on whether the irrigation track changed. |
| 6. Append daily inflow and demand into the reservoir’s monthly arrays | At the start of a month, reallocates the daily arrays to size one and stores the first day’s values; otherwise it grows each array with `temp_array` and `move_alloc` to append today’s inflow and demand. |
| 7. Roll monthly means into the reservoir memory at month end | When `end_of_mo == 1`, shifts the rolling monthly history left and stores the mean daily inflow and irrigation demand for the month in the last memory slot. |
| 8. Evaluate release control and route reservoir outflow | Looks up the reservoir data record, then either evaluates the decision-table branch with `conditions` and `res_hydro` or the conditions-table branch with `res_rel_conds`; the resulting outflow is then smoothed with the lag-up/lag-down factors and saved in `prev_flo`. |
| 9. Compute daily evaporation, precipitation, and seepage losses | Uses weather PET and precipitation to compute evaporation and precipitation volumes, then either applies the simple seepage formula or calls `gwflow_reservoir` when groundwater flow is active. |
| 10. Update reservoir storage with precipitation, outflow, evaporation, and seepage | Adds precipitation to reservoir storage, subtracts routed outflow, evaporation, and seepage, and clips the losses if they would drive storage negative. |
| 11. Recompute surface area from updated storage | Uses the reservoir volume-area power law to update `res_wat_d(jres)%area_ha` when storage remains positive, otherwise sets area to zero. |
| 12. Route nutrient, pesticide, salt, and generic constituent masses | Calls `res_nutrient`, `res_pest`, `res_salt`, and `res_cs` as enabled, and copies the resulting masses back into `obcs(icmd)%hd(1)` for downstream routing. |
| 13. Publish routed hydrographs and cumulative totals | Writes the final outflow to `ob(icmd)%hd(1)`, updates total inflow and outflow hydrographs, and spreads the outflow across subdaily time slices when `time%step > 1`. |
| 14. Store daily reservoir output records and mark the reservoir processed | Copies daily inflow and outflow to `res_in_d` and `res_out_d` after the output-skip years, then sets `res_ob(jres)%wallo_call = 1` so water-allocation logic knows the reservoir has already been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc, pco` | `bsn_cc%lapse, bsn_cc%gwflow, pco%nyskip` |
| [sym:reservoir_data_module] | `res_hyd, res_dat, res_prm` | `res_hyd(jres)%iyres, res_hyd(jres)%mores, res_dat(idat)%release, res_hyd(jres)%evrsv, res_hyd(jres)%k, res_dat(idat)%cs` |
| [sym:time_module] | `time` | `time%yrc, time%mo, time%day_mo, time%end_mo, time%step, time%yrs` |
| [sym:reservoir_module] | `res_ob` | `res_ob(jres)%ob, res_ob(jres)%irrig_track, res_ob(jres)%d_irrig_day, res_ob(jres)%daily_inflow_array(1), res_ob(jres)%daily_demand_array(1), res_ob(jres)%props, res_ob(jres)%pvol, res_ob(jres)%evol, res_ob(jres)%weir_hgt, res_ob(jres)%prev_flo, res_ob(jres)%br1, res_ob(jres)%br2, res_ob(jres)%wallo_call` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat, wst(iwst)%weat%pet, wst(iwst)%weat%precip` |
| [sym:hydrograph_module] | `ob, ht1, wbody, ht2, res, hd, ts, res_in_d, res_out_d, icmd` | `ob(icmd)%hin, ob(iob)%wst, ht1%flo, wbody%flo, ht2%flo, res(jres)%flo, ob(icmd)%hd(1), ob(icmd)%hin_tot, ob(icmd)%hout_tot, ob(icmd)%ts(1,ii)` |
| [sym:conditional_module] | `dtbl_res` |  |
| [sym:water_body_module] | `res_wat_d` | `res_wat_d(jres)%area_ha, res_wat_d(jres)%evap, res_wat_d(jres)%precip, res_wat_d(jres)%seep` |
| [sym:constituent_mass_module] | `cs_db, obcs, hcs2` | `cs_db%num_pests, obcs(icmd)%hd(1)%pest, hcs2%pest, cs_db%num_salts, obcs(icmd)%hd(1)%salt, hcs2%salt, cs_db%num_cs, obcs(icmd)%hd(1)%cs, hcs2%cs, cs_db%num_tot, obcs(icmd)%hd(1), obcs(icmd)%hin(1)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ht1` | After the reservoir becomes operational (`time%yrc > res_hyd(jres)%iyres` or same year with `time%mo >= res_hyd(jres)%mores`). | `ht1` is loaded from `ob(icmd)%hin` at the start of the call, so it becomes the reservoir’s incoming hydrograph for all later balance and output calculations. |
| `ht2` | After the reservoir becomes operational and before routing outflow. | `ht2` starts as `resz` and is then filled by release-control logic, so it becomes the reservoir’s routed outflow hydrograph for the day. |
| `hcs2` | After the reservoir becomes operational and before constituent routing. | `hcs2` starts as `hin_csz` and is later filled by constituent routines, so it represents the outgoing constituent hydrograph for the reservoir. |
| `iwst` | After the reservoir becomes operational and weather station lookup is known. | `iwst` is set from the linked object’s weather-station index so the routine can read and rewrite the correct station record when applying lapse correction and weather-driven water-balance terms. |
| `w` | After the reservoir becomes operational. | `w` is assigned the weather record from `wst(iwst)%weat` and may be modified by `cli_lapse` before being written back to the weather station. |
| `wst(iwst)%weat` | If `bsn_cc%lapse == 1` after loading `w` from the weather station. | The weather record is overwritten with the lapse-adjusted values in `w`, so later evaporation and precipitation calculations use corrected climate inputs. |
| `wbody` | After binding `wbody => res(jres)` and before water-balance updates. | `wbody` becomes the shared pointer to the reservoir hydrograph state, so later sediment and nutrient routines can update the same object through the pointer. |
| `wbody_wb` | After binding `wbody_wb => res_wat_d(jres)` and before water-balance updates. | `wbody_wb` becomes the shared pointer to the reservoir water-body diagnostic record, so the daily area, evaporation, precipitation, and seepage terms can be stored there. |
| `wbody_prm` | After binding `wbody_prm => res_prm(jres)` and before release and quality calculations. | `wbody_prm` becomes the shared pointer to the reservoir parameter record, which supplies reservoir-specific coefficients used by downstream water-body calculations. |
| `res(jres)` | When inflow is added, release is subtracted, and balance corrections are applied. | `res(jres)` changes throughout the routine as storage is increased by inflow and precipitation and reduced by release, evaporation, and seepage; it is the reservoir’s main water store. |
| `res_ob(jres)%daily_inflow_array(1)` | When the monthly inflow array is initialized or appended. | The first slot is set to today’s inflow on day 1 of the month, so the reservoir can compute a monthly mean inflow at month end. |
| `res_ob(jres)%daily_demand_array(1)` | When the monthly demand array is initialized or appended. | The first slot is set to today’s irrigation demand on day 1 of the month, so the reservoir can compute a monthly mean irrigation demand at month end. |
| `res_ob(jres)%I_mon_past(1:12*(res_ob(jres)%N_memory)-1)` | At `end_of_mo == 1` when the rolling monthly memory is updated. | The older inflow-memory values are shifted left by one monthly slot to make room for the newest monthly mean inflow. |
| `res_ob(jres)%I_mon_past(12*(res_ob(jres)%N_memory))` | At `end_of_mo == 1` when the rolling monthly memory is updated. | The last inflow-memory slot receives the current month’s mean daily inflow, preserving the most recent monthly history. |
| `res_ob(jres)%d_mon_past(1:12*(res_ob(jres)%N_memory)-1)` | At `end_of_mo == 1` when the rolling monthly memory is updated. | The older irrigation-demand history is shifted left so the array can hold the current month’s mean demand in the final slot. |
| `res_ob(jres)%d_mon_past(12*(res_ob(jres)%N_memory))` | At `end_of_mo == 1` when the rolling monthly memory is updated. | The last irrigation-demand memory slot receives the current month’s mean daily irrigation demand. |
| `d_tbl` | When the reservoir uses decision-table release control (`res_ob(jres)%rel_tbl == 'd'`). | `d_tbl` becomes associated with the selected reservoir decision table `dtbl_res(irel)`, so the release-condition routines operate on the correct table record. |
| `ht2%flo` | After `res_hydro` computes outflow in the decision-table branch. | `ht2%flo` is adjusted by the lag-up or lag-down smoothing to prevent abrupt release jumps before the outflow is stored back into `prev_flo`. |
| `res_ob(jres)%prev_flo` | After smoothing the decision-table outflow. | `prev_flo` is updated to the final routed outflow so the next day can compare against it and choose the proper lag factor. |
| `res_wat_d(jres)%evap` | Each day in the water-balance section. | Evaporation is recomputed from weather PET, the reservoir evaporation coefficient, and the current surface area; it is then reduced if storage would go negative. |
| `res_wat_d(jres)%precip` | Each day in the water-balance section. | Precipitation volume is recomputed from weather precipitation and the current surface area and then added to reservoir storage. |
| `res_wat_d(jres)%seep` | When groundwater flow is not active (`bsn_cc%gwflow == 0`) or when `gwflow_reservoir` handles seepage. | Seepage is set by the simple reservoir seepage formula when gwflow is inactive, or by `gwflow_reservoir` when groundwater exchange is active; it is then reduced if storage would go negative. |
| `res(jres)%flo` | After precipitation, outflow, evaporation, and seepage are applied. | `res(jres)%flo` is the reservoir’s remaining storage volume after the daily water balance and any negative-storage corrections. |
| `res_wat_d(jres)%area_ha` | After recomputing the water-body area from updated storage. | The reservoir surface area is recalculated from storage using the power law when storage remains positive, otherwise it is set to zero. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:1.1.1 | Reservoir daily water balance | $V=V_{stored}+V_{flowin}-V_{flowout}+V_{pcp}-V_{evap}-V_{seep}$ | V=V_stored+V_flowin-V_flowout+V_pcp-V_evap-V_seep distributed: inflow line 59 (res+=ht1); precip 171; outflow subtracted 174; evap 181; seep 188. |
| 8:1.1.2 | Reservoir surface area from volume (power law) | $SA=\beta_{sa}*V^{expsa}$ | area_ha=br1*flo**br2; br1=beta_sa, br2=expsa. Exact match SA=beta_sa*V^expsa. |
| 8:1.1.5 | Reservoir precipitation volume | $V_{pcp}=10*R_{day}*SA$ | precip=10.*wst%weat%precip*area_ha; exact match V_pcp=10*R_day*SA. |
| 8:1.1.6 | Reservoir evaporation volume | $V_{evap}=10*\eta*E_o*SA$ | evap=10.*evrsv*wst%weat%pet*area_ha; evrsv=eta, pet=E_o. Exact match V_evap=10*eta*E_o*SA. |
| 8:1.1.7 | Reservoir seepage volume | $V_{seep}=240*K_{sat}*SA$ | seep=240.*res_hyd%k*area_ha; k=K_sat (mm/hr). Exact match V_seep=240*K_sat*SA. |

## Lineage

`res_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 16 non-merge commit(s) since, most recently `c38f3b8` (2026-04-05, "clean up and bugfixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_control.f90` are listed.

- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `080211e` (2026-03-09) — water allocation operating properly
- `d3c291b` (2026-01-31) — integrate new reservoir routines
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `7667e4b` (2025-07-16) — Update res_control.f90
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_control' has no extracted documentation comment.
- algorithm_steps revised: merged the draft’s generic steps into a source-aligned 14-step sequence and replaced broad line spans with concrete line ranges from the source block.
- Source uncertainty note: `callers[1]` is inferred from the `wallo_control` snippet showing the call site after a water transfer is applied.
- Source uncertainty note: `conditions` and `res_hydro` contracts were used as provided in the context packet; their internal details were not re-derived from `res_control`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
