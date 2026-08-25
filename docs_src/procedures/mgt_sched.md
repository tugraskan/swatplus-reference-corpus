---
kind: procedure
symbol: mgt_sched
title: mgt_sched
status: filled
source_hash: cef311106a3ee595
version_label: SWAT+ 62.0.0
args:
  isched: Selects which management schedule in `sched(isched)` supplies the current operation
    list and the next operation record to execute.
locals:
  icom: Plant-community database index used to crosswalk the current community to plant definitions;
    initialized to 0.
  idp: Plant database index for the active plant being processed or reported; initialized
    to 0.
  j: Current HRU index, set from `ihru` and used throughout the routine to access HRU state;
    initialized to 0.
  iharvop: Harvest-operation database index selected from `mgt%op1`; initialized to 0.
  idtill: Tillage-operation database index selected from `mgt%op1` or crosswalked from tillage
    names; initialized to 0.
  ifrt: Fertilizer/manure database index selected from `mgt%op1`; initialized to 0.
  iob: Spatial object index for the current HRU, used in pesticide handling; initialized to
    0.
  ipestcom: Loop index used to crosswalk pesticide community names to `cs_db%pests`; initialized
    to 0.
  ipest: Sequential pesticide index selected from the pesticide community; initialized to
    0.
  ipestop: Chemical-application database index used for pesticide application efficiency and
    surface fraction; initialized to 0.
  irrop: Irrigation-operation database index selected from `mgt%op1`; initialized to 0.
  jj: Loop counter used in drainage and soil-layer searches; initialized to 0.
  iburn: Fire-operation database index selected from `mgt%op1`; initialized to 0.
  ifertop: Chemical-application database index used for fertilizer/manure surface fraction;
    initialized to 0.
  iplt_bsn: Basin crop-yield index taken from the plant community's basin number; initialized
    to 0.
  ireg: Regional calibration index taken from `hru(j)%crop_reg`; initialized to 0.
  ilum: Land-use calibration loop index within a region; initialized to 0.
  fr_curb: Street-sweeping curb availability factor copied from `sweepop`; initialized to
    0.
  ires: Surface-storage index for the current HRU, taken from `hru(j)%dbs%surf_stor`; initialized
    to 0.
  ipud: Puddling-operation database index crosswalked from `mgt%op_plant`; initialized to
    0.
  ipdl: Puddling-operation loop index used to search `pudl_db`; initialized to 0.
  biomass: Temporary plant biomass value used to test harvest and kill thresholds and to log
    output; initialized to 0.
  frt_kg: Applied fertilizer or manure rate in kg/ha copied from `mgt%op3`; initialized to
    0.
  pest_kg: Applied pesticide rate in kg/ha after application-efficiency adjustment; initialized
    to 0.
  chg_par: Temporary new parameter value returned by `chg_par` for curve-number updates.
  wsa1: HRU area-derived scaling value computed from `hru(ihru)%area_ha * 10.`; initialized
    to 0.
  harveff: Harvest efficiency used for residue harvest branches; initialized to 0.
  idb: Generic database loop/index used for transplant, burn, and puddling crosswalks; initialized
    to 0.
  itr: Transplant database index selected from `transpl`; initialized to 0.
  iwr: Weir database index selected from `res_weir`; initialized to 0.
uses:
  plant_data_module: Provides plant-community definitions, plant database lookups, transplant
    records, and plant names/triggers needed to match management operations to the correct
    plant and to label output.
  mgt_operations_module: Holds the current management operation record and the operation databases
    that supply harvest, irrigation, fertilizer, pesticide, and sweeping parameters.
  tillage_data_module: Supplies tillage names and mixing efficiency used to execute and log
    tillage and puddling operations.
  basin_module: Provides management-output control and the basin carbon-code mode that changes
    tillage mixing behavior.
  hydrograph_module: Provides wetland flow state, irrigation transfer state, and spatial object
    indexing used by irrigation, fertilizer, and pesticide operations.
  hru_module: Provides HRU geometry, drainage, irrigation, curve-number, and plant-calibration
    state updated or read by management operations.
  soil_module: Provides soil water storage and layer count used in output and drainage calculations.
  plant_module: Provides plant community status, stress, mass, and basin yield accounting
    updated by planting, harvest, kill, irrigation, and calibration operations.
  time_module: Provides the current simulation date used in management output records.
  constituent_mass_module: Provides the pesticide community list used to crosswalk management
    pesticide names to sequential pesticide indices.
  organic_mineral_mass_module: Provides plant biomass, residue, and yield pools updated by
    harvest, kill, burn, and irrigation-related management.
  calibration_data_module: Provides soft-calibration controls and regional plant calibration
    accumulators updated by harvest operations.
  reservoir_data_module: No concrete source-backed references were provided in the context
    packet for this module.
  reservoir_module: No concrete source-backed references were provided in the context packet
    for this module.
  maximum_data_module: Provides maximum database element counts used to search transplant
    records.
  aquifer_module: No concrete source-backed references were provided in the context packet
    for this module.
---

<!-- facts:header -->

Schedules and executes one management operation for the current HRU and date.

## Bottom Line

`mgt_sched` is the management dispatcher for a single HRU. It inspects the current scheduled operation in `sched(isched)%mgt_ops(hru(j)%cur_op)`, executes the matching plant, harvest, tillage, irrigation, fertilizer, pesticide, grazing, drainage, or wetland action, then advances the HRU's operation pointer to the next scheduled record.

It also updates shared HRU, plant, soil, wetland, and calibration state so later growth, hydrology, nutrient, and output routines see the effects of the operation. When management output is enabled, it writes detailed event records to unit 2612.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by `mgt_operatn` when the current scheduled management record matches the current month and day. It executes one management operation for the current HRU, then advances `hru(j)%cur_op` and loads the next record from `sched(isched)%mgt_ops`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize HRU context | Set the current HRU index and derive surface-storage, object, and area scaling values used by later branches. |
| 2. Crosswalk plant operation | If the operation is not fertilizer, reset `mgt%op2` and search the plant community database to identify which plant slot matches `mgt%op_char`. |
| 3. Dispatch by operation code | Select the management branch based on `mgt%op`. |
| 4. Plant or transplant crop | For `plnt`, mark the target plant growing, call plant initialization, optionally transplant, and write plant or transplant output records. |
| 5. Update monsoon state | For `mons`, reset or flag monsoon-related plant phenology based on the trigger and operation flag. |
| 6. Harvest or residue harvest | For `harv`, choose the harvest type, call the matching harvest routine, accumulate yield and calibration totals, and log harvest output. |
| 7. Kill plants | For `kill`, kill the targeted plant, log the event, and reset plant heat-unit accumulation. |
| 8. Harvest and kill | For `hvkl`, harvest first if biomass exceeds the threshold, then kill the plant, update yield and calibration totals, and clear plant stress and phenology state. |
| 9. Mix tillage or puddling | For `till` and `pudl`, choose the appropriate tillage-mixing routine based on carbon mode or wetness, then log the operation. |
| 10. Apply irrigation | For `irrm` and `irpm`, compute applied and runoff irrigation amounts, update yearly irrigation totals, and write irrigation output. |
| 11. Apply fertilizer or manure | For `fert` and `manu`, route the application through wet or dry fertilizer routines, update nutrient pools, and log the application. |
| 12. Apply pesticide | For `pest`, crosswalk the pesticide community, compute applied mass from application efficiency, call `pest_apply`, and log the event. |
| 13. Handle grazing, CN, burn, sweep | For `graz`, `cnup`, `burn`, and `swep`, update grazing state, curve number, burn state, or sweep parameters and write the corresponding output records. |
| 14. Handle drainage, weir, skip | For `dwm`, `weir`, `irrp`, `pudl`, and `skip`, update drainage or wetland irrigation state, adjust wetland structures, or mark the HRU to skip a year. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pcomdb, transpl, pldb` | `pcomdb(icom)%pl(ipl)%cpnm, pcomdb(icom)%pl(ipl)%db_num, transpl(idb)%name, pldb(idp)%plantnm, pldb(idp)%trig` |
| [sym:mgt_operations_module] | `mgt, harvop_db, irrop_db, chemapp_db, sweepop` | `mgt%op, mgt%op2, mgt%op_char, mgt%op3, mgt%op_plant, mgt%op1, harvop_db(iharvop)%bm_min, harvop_db(iharvop)%typ, irrop_db(irrop)%amt_mm, irrop_db(irrop)%eff, irrop_db(irrop)%surq, irrop_db(irrop)%name, mgt%op4, chemapp_db(ipestop)%app_eff, sweepop%eff, sweepop%fr_curb` |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idtill)%tillnm` |
| [sym:basin_module] | `pco, bsn_cc` | `pco%mgtout, bsn_cc%cswat` |
| [sym:hydrograph_module] | `irrig, wet, sp_ob` | `irrig(j)%applied, irrig(j)%runoff, wet(j)%flo, sp_ob%hru` |
| [sym:hru_module] | `hru, phubase, sol_sumsolp, sol_sumno3` | `hru(j)%dbs%surf_stor, hru(j)%obj_no, hru(ihru)%area_ha, hru(j)%area_ha, hru(j)%crop_reg, hru(j)%irr_yr, hru(j)%lumv%sdr_dep` |
| [sym:soil_module] | `soil` | `soil(j)%sw, soil(j)%nly` |
| [sym:plant_module] | `pcom, bsn_crop_yld` | `pcom(j)%pcomdb, pcom(j)%npl, pcom(j)%days_plant, pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%lai_pot, pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plcur(ipl)%mseas, pcom(j)%days_harv, pcom(j)%plcur(ipl)%harv_num, pcom(j)%plcur(ipl)%harv_num_yr, pcom(j)%plcur(ipl)%bsn_num, bsn_crop_yld(iplt_bsn)%area_ha, bsn_crop_yld(iplt_bsn)%yield, pcom(j)%plstr(ipl)%sum_n, pcom(j)%plstr(ipl)%sum_p, pcom(j)%plstr(ipl)%sum_tmp, pcom(j)%plstr(ipl)%sum_w, pcom(j)%plstr(ipl)%sum_a, pcom(j)%days_kill, pcom(j)%plstr(ipl), pcom(j)%days_irr` |
| [sym:time_module] | `time` | `time%yrc, time%mo, time%day_mo` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipestcom)` |
| [sym:organic_mineral_mass_module] | `pl_mass, pl_yield` | `pl_mass(j)%tot(ipl)%m, pl_mass(j)%rsd_tot%m, pl_mass(j)%yield_tot(ipl), pl_mass(j)%yield_yr(ipl), pl_yield%m` |
| [sym:calibration_data_module] | `cal_codes, plcal` | `cal_codes%plt, plcal(ireg)%lum_num, plcal(ireg)%lum(ilum)%meas%name, plcal(ireg)%lum(ilum)%ha, plcal(ireg)%lum(ilum)%sim%yield` |
| [sym:reservoir_data_module] | `none identified in provided context` | `none identified in provided context` |
| [sym:reservoir_module] | `none identified in provided context` | `none identified in provided context` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%transplant` |
| [sym:aquifer_module] | `none identified in provided context` | `none identified in provided context` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mgt%op2` | At entry, for any operation other than `fert`, when the community has more than one plant. | Identifies which plant in the community the operation targets by matching `mgt%op_char` to a plant name; 0 if no match. |
| `pcom(j)%days_plant` | In the `plnt` (plant) operation. | Resets the days-since-last-plant counter to 1 when a planting operation runs. |
| `pcom(j)%plcur(ipl)%gro` | In `plnt` when the crop is not already growing, and in `mons` when resetting monsoon phenology. | Sets the plant's growing flag to "y" to start its growth cycle. |
| `pcom(j)%plcur(ipl)%idorm` | In `plnt` (and monsoon reset) when a plant starts growing. | Clears the dormancy flag ("n") so the newly planted/started crop is not dormant. |
| `pcom(j)%plcur(ipl)%phuacc` | Reset to 0 in `mons` (phenology reset), `kill`, and `hvkl`. | Resets accumulated potential heat units to zero, restarting the plant's phenological clock. |
| `pcom(j)%plcur(ipl)%mseas` | In `mons` (monsoon period): set "n" when resetting, "y" when `mgt%op3 == 1`. | Toggles the monsoon-season flag that controls moisture-triggered growth initiation. |
| `pcom(j)%days_harv` | In `harv` and `hvkl` operations when a target plant is harvested. | Resets the days-since-last-harvest counter to 1. |
| `pl_mass(j)%yield_tot(ipl)` | In `harv` and `hvkl`, after a harvest call. | Accumulates total harvested yield for the plant across the simulation. |
| `pl_mass(j)%yield_yr(ipl)` | In `harv` and `hvkl`, after a harvest call. | Accumulates harvested yield for the plant within the current year. |
| `pcom(j)%plcur(ipl)%harv_num` | In `harv` and `hvkl`, after a harvest call. | Increments the total harvest count for the plant. |
| `pcom(j)%plcur(ipl)%harv_num_yr` | In `harv` and `hvkl`, after a harvest call. | Increments the within-year harvest count for the plant. |
| `bsn_crop_yld(iplt_bsn)%area_ha` | In `harv` and `hvkl`, summing basin crop statistics. | Adds the HRU area to the basin-level harvested area for the crop. |
| `bsn_crop_yld(iplt_bsn)%yield` | In `harv` and `hvkl`, summing basin crop statistics. | Adds the HRU's harvested mass to the basin crop yield total. |
| `plcal(ireg)%lum(ilum)%ha` | In `harv`/`hvkl` when plant soft-calibration is on (`cal_codes%plt == "y"`) and the HRU is in a crop region. | Accumulates harvested area for the region/land-use used in soft calibration. |
| `plcal(ireg)%lum(ilum)%sim%yield` | In `harv`/`hvkl` when plant soft-calibration is on and the land-use name matches. | Accumulates simulated regional yield for soft calibration. |
| `pcom(j)%days_kill` | In `kill` and `hvkl` operations when a target plant is killed. | Resets the days-since-last-kill counter to 1. |
| `pcom(j)%plstr(ipl)` | In `hvkl`, after harvest/kill of the plant. | Resets the plant stress accumulators to the zero template `plstrz`. |
| `phubase(j)` | Reset to 0 in `hvkl` after harvest and kill. | Resets the base heat-unit accumulator for the HRU after the crop is harvested and killed. |
| `ipl` | Set throughout: as the plant loop index and as `Max(1, mgt%op2)` in tillage/graze/sweep, and 1 in irrigation/fertilizer branches. | Selects the plant within the community that the current operation acts on or writes output for. |
| `irrig(j)%applied` | In `irrm` and `irpm` (scheduled irrigation) operations. | Computes the depth of irrigation water applied to the soil, net of efficiency and surface-runoff loss. |
| `irrig(j)%runoff` | In `irrm` and `irpm` (scheduled irrigation) operations. | Computes the portion of applied irrigation that becomes surface runoff. |
| `pcom(j)%days_irr` | In irrigation operations (`irrm`, `irrp`, `irpm`). | Resets the days-since-last-irrigation counter to 1. |
| `hru(j)%irr_yr` | In `irrm` and `irpm` irrigation operations. | Adds the applied irrigation to the year-to-date irrigation total for decision-table conditioning. |
| `mgt%op1` | In the `pest` operation, after cross-walking the pesticide name to the community. | Stores the resolved pesticide community index back into `mgt%op1` for use as the pesticide type. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_sched.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 28 non-merge commit(s) since, most recently `4074140` (2026-06-05, "Fix duplicate HARVEST output for non-target dead plants in multi-plant communiti…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_sched.f90` are listed.

- `4074140` (2026-06-05) — Fix duplicate HARVEST output for non-target dead plants in multi-plant communities
- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `99e9b55` (2026-05-07) — Corrected spelling error in harv_ops. fixed mgt_harvreside to correctly harvest the right amount of residue and no more the bm_min allows. A…
- `f1d1ac1` (2026-04-22) — Hopefulle some finally cleanup to implement cswat == 3 to cswat = 1. Added/changed subroutines in external specificaitons due to subroutine…
- `3389f29` (2026-04-22) — Numerous changes to account for the removal of the old cswat ==1 and moving cswat == 3 to cswat =1. Also some code formatting changes to get…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- File I/O verified against the source: 25 write statements, no reads, opens, closes or rewinds. Every one targets unit 2612 and every one is guarded by `pco%mgtout == "y"`, so the routine produces management-output records only when management output is switched on. The unit is not opened or closed here, so the connection is established elsewhere.
- `chg_par` is a function invoked in an expression at `mgt_sched.f90:457`, not a `call` statement; its `callees` entry cites the assignment line rather than a call site.
- algorithm_steps were left as the fill model produced them: the 14 spans are already contiguous and non-overlapping across mgt_sched.f90:63-624, one per `mgt%op` branch.
- `mgt_sched` carries no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
