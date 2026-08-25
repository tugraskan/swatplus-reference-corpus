---
kind: procedure
symbol: cal_conditions
title: cal_conditions
status: filled
source_hash: 9630ca0390aa21b9
version_label: SWAT+ 62.0.0
locals:
  chg_parm: Holds the current calibration parameter name from the update record and drives
    later dispatch to the correct parameter update.
  chg_typ: Holds the change mode string, such as absolute or percentage change, passed to
    `chg_par`.
  cond_met: Tracks whether all conditions for the current update remain satisfied; starts
    as yes and is flipped to no when any condition fails.
  pl_find: Temporary flag used while scanning plants in an HRU to see whether the target plant
    name is present.
  lyr: Loop counter and selected layer index used for soil layers, reservoir storage zones,
    and plant-related updates.
  iyr: Converted climate-year index relative to `time%yrc` for accessing time-series arrays.
  ichg_par: Outer loop counter over calibration updates in `db_mx%cal_upd`.
  ispu: Loop counter over the element list attached to one update record.
  ielem: Current target element index selected from the update record and reused for module
    lookups.
  chg_val: Requested change magnitude passed into `chg_par` for the current update.
  absmin: Lower bound for the calibrated value, taken from the calibration parameter table.
  absmax: Upper bound for the calibrated value, taken from the calibration parameter table.
  num_db: Calibration database index for the current update record; used to fetch bounds and
    object type.
  ic: Loop counter over the conditions attached to one update record.
  ipg: Climate station or precipitation-group index selected from the update record.
  ipl: Loop counter over plants in a plant community.
  iyear: Absolute calendar year loop variable used when updating climate time series.
  val_cur: Temporary holder for the current climate time-series value before it is passed
    to `chg_par`.
  chg_par: Declared as a real scalar in the source, but the routine also calls the external
    function `chg_par` with the current value to compute a bounded updated value.
  iday: Day-of-year loop variable used when updating climate time series.
  ig: Climate temperature-group index used when updating temperature time series.
  nvar: Marks the number of plant calibration variables handled in the plant branch; set to
    2 before plant dispatch.
  cal_lyr1: Lower soil-layer bound after normalization for soil-object updates.
  cal_lyr2: Upper soil-layer bound after normalization for soil-object updates.
  iplant: Flag used in the plant `epco` branch to record whether a plant-specific condition
    was found.
uses:
  maximum_data_module: Provides the maximum number of calibration updates to iterate over
    in the outer loop.
  calibration_data_module: Supplies the update records, their condition lists, target object
    type, and calibration bounds that control all dispatch and value changes.
  conditional_module: Used to compare reservoir object type names against the target type
    in conditional checks.
  hru_lte_module: Imported by the routine, but no resolved outside references were identified
    in the provided context.
  hru_module: Provides HRU-level land-use management and calibration-group labels used by
    the `landuse` and `cal_group` condition checks.
  soil_module: Provides soil profile attributes used by the `hsg`, `texture`, and soil-layer
    range logic.
  plant_module: Provides plant community membership and plant-state variables used by the
    `plant`, `plt`, and plant-specific update branches.
  plant_data_module: Provides the plant class label used by the `pl_class` condition check.
  time_module: Provides the current calendar year used to convert absolute climate years into
    array indices.
  reservoir_module: Provides reservoir principal-spillway volume used by the `res_pvol` range
    condition.
  climate_module: Provides precipitation and temperature time-series arrays that can be modified
    over selected date ranges.
---

<!-- facts:header -->

Applies calibration updates when their conditions are satisfied. It checks each requested update against object-specific filters, then dispatches the change to the matching soil, reservoir, plant, climate, or other calibration target.

## Bottom Line

`cal_conditions` is the calibration dispatcher for conditional updates. It walks the configured update list, tests each update's conditions against the current HRU, soil, reservoir, plant, and climate state, and only then applies the requested parameter change.

Its main job is to gate calibration changes so they affect only the intended objects, layers, dates, or plant members. That makes it the control point between the calibration input tables and the later model state that actually gets modified.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_cal` calls this routine immediately after reading calibration data and plant parameters, so the update tables and plant state are ready before conditional calibration is applied. The results feed later soft-calibration and landscape-calibration setup, and they also modify plant, soil, reservoir, and climate state used by subsequent model execution.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over updates | Iterate over each configured calibration update and each target element listed for that update. |
| 2. Load update fields | Copy the current update record fields into local variables, including the target name, change type, change amount, and calibration bounds. |
| 3. Assume conditions pass | Initialize the condition flag to yes and begin scanning the update's condition list. |
| 4. Test condition list | Evaluate each condition type against the current element state, including reservoir volume, soil group, reservoir type, soil texture, plant membership, plant class, land-use label, and calibration group. |
| 5. Skip unmet updates | Only continue into the update logic when all conditions remain satisfied. |
| 6. Dispatch by object type | Use the calibration object's type to choose the soil, reservoir, plant, climate, or generic update path. |
| 7. Update soil layers | For soil objects, normalize the requested layer bounds and apply the calibration change to each selected layer. |
| 8. Update reservoir zones | For reservoir decision-table updates, select the appropriate storage zone and apply only the supported reservoir parameters for that zone. |
| 9. Update plant states | For plant updates, modify plant heat units, potential LAI, or harvest index for matching plants in the community. |
| 10. Update climate series | For climate updates, walk the selected stations and date range, then change precipitation or temperature time-series values in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cal_upd` |
| [sym:calibration_data_module] | `cal_upd, cal_parms` | `cal_upd(ichg_par)%num_elem, cal_upd(ichg_par)%num(ispu), cal_upd(ichg_par)%name, cal_upd(ichg_par)%chg_typ, cal_upd(ichg_par)%val, cal_upd(ichg_par)%num_db, cal_upd(ichg_par)%conds, cal_upd(ichg_par)%cond(ic)%var, cal_upd(ichg_par)%val1, cal_upd(ichg_par)%val2, cal_upd(ichg_par)%cond(ic)%targc, cal_parms(num_db)%ob_typ, cal_upd(ichg_par)%lyr1, cal_upd(ichg_par)%lyr2, cal_upd(ichg_par)%year1, cal_upd(ichg_par)%year2, cal_upd(ichg_par)%day1, cal_upd(ichg_par)%num(ielem), cal_upd(ichg_par)%day2` |
| [sym:conditional_module] | `dtbl_res` | `dtbl_res(ielem)%name` |
| [sym:hru_lte_module] | `none` |  |
| [sym:hru_module] | `hru` | `hru(ielem)%land_use_mgt_c, hru(ielem)%cal_group` |
| [sym:soil_module] | `soil, sol` | `soil(ielem)%hydgrp, soil(ielem)%texture, soil(ielem)%nly` |
| [sym:plant_module] | `pcom` | `pcom(ielem)%npl, pcom(ielem)%pl(ipl), pcom(ielem)%plcur(ipl)%phumat, pcom(ielem)%plcur(ipl)%lai_pot, pcom(ielem)%plcur(ipl)%harv_idx` |
| [sym:plant_data_module] | `pl_class` |  |
| [sym:time_module] | `time` | `time%yrc` |
| [sym:reservoir_module] | `res_ob` | `res_ob(ielem)%pvol` |
| [sym:climate_module] | `pcp, tmp` | `pcp(ipg)%ts(iday,iyr), tmp(ig)%ts(iday,iyr)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `generic calibration target selected by `cal_parm_select`` | All conditions satisfied and object type is not sol/cli/plt/rdt | Applies a direct calibration change to the selected object or parameter using the current update record. |
| `soil layers selected by `cal_lyr1:cal_lyr2`` | `cal_parms(num_db)%ob_typ == "sol"` | Applies the calibration change to each soil layer in the requested range after clamping the range to valid soil-layer bounds. |
| `reservoir decision-table storage zone selected by `lyr`` | `cal_parms(num_db)%ob_typ == "rdt"` and `chg_parm` is `drawdown_days` or `withdraw_rate` | Applies the calibration change to the supported reservoir decision-table parameter for the selected storage zone. |
| `pcom(ielem)%plcur(ipl)%phumat` | `cal_parms(num_db)%ob_typ == "plt"` and plant name matches a condition target | Updates plant heat units to maturity for matching plants in the community. |
| `pcom(ielem)%plcur(ipl)%lai_pot` | `cal_parms(num_db)%ob_typ == "plt"` and `cal_upd(ichg_par)%name == "epco"` | Updates potential LAI for the matched plant, or for all plants if no plant condition is present. |
| `pcom(ielem)%plcur(ipl)%lai_pot` | `cal_parms(num_db)%ob_typ == "plt"` and `cal_upd(ichg_par)%name == "lai_pot"` | Updates potential LAI for each plant whose name matches the condition target. |
| `pcom(ielem)%plcur(ipl)%harv_idx` | `cal_parms(num_db)%ob_typ == "plt"` and `cal_upd(ichg_par)%name == "harv_idx"` | Updates harvest index for each plant whose name matches the condition target. |
| `pcp(ipg)%ts(iday,iyr)` | `cal_parms(num_db)%ob_typ == "cli"` and `cal_upd(ichg_par)%name == "precip"` | Replaces precipitation time-series values over the selected years and days with calibrated values. |
| `tmp(ig)%ts(iday,iyr)` | `cal_parms(num_db)%ob_typ == "cli"` and `cal_upd(ichg_par)%name == "temp"` | Replaces temperature time-series values over the selected years and days with calibrated values. |

## File I/O

<!-- facts:io -->


## Lineage

`cal_conditions.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 13 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cal_conditions.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `29e2d36` (2025-10-29) — Bug fixes and changes related to water allocation
- `10e5ddc` (2025-08-27) — 08272025 updates
- `d81f796` (2025-04-18) — various comment fixes
- `4d173cc` (2025-04-17) — merge
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cal_conditions' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
