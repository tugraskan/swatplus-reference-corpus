---
kind: procedure
symbol: conditions
title: conditions
status: filled
source_hash: 5c33b56cf07b48f4
version_label: SWAT+ 62.0.0
args:
  ob_cur: '`ob_cur` is the current object index used as the default HRU/route object when
    a condition does not specify its own `ob_num`; many branches fall back to this value before
    looking up HRU, plant, soil, or water state.'
  idtbl: '`idtbl` identifies which decision table action set is being evaluated, so it is
    passed through to the comparison helpers and used when the routine writes the selected
    application day for probabilistic scheduling.'
locals:
  ob_num: Current object number used to resolve the target HRU, reservoir, or wetland when
    a condition row supplies `ob_num = 0`; otherwise it is taken from the condition row.
  ic: Loop index over each condition row in `d_tbl%conds`.
  ialt: Loop index over each alternative in the current condition row; used when disabling
    specific alternatives in `d_tbl%act_hit`.
  iac: Action index retrieved from `d_tbl%con_act(ic)` for the `days_act` condition so the
    routine can check the correct last-action counter.
  iob: Sequential object number derived from `sp_ob1` offsets for object classes such as HRUs
    and LTE HRUs when the condition references `ob` type codes.
  targ_val: Base value read from a source variable before applying the condition’s operator
    and constant, especially for soil-water and reservoir-volume style conditions.
  ran_num: Uniform random number drawn from `Aunif` for probability-based conditions.
  aunif: Local external function name for the uniform random generator referenced by `Aunif`;
    the declaration lets the routine call the stochastic helper.
  ires: Reservoir or wetland index used in volume, wet-depth, weir-height, and wetland-flow
    conditions.
  ipl: Plant index used when testing plant growth status or fetching a plant-specific state
    value.
  iipl: Inner loop plant index used to scan all plants in a community when searching by name
    or choosing the first growing plant.
  id: Decision-table or management database identifier used in tillage checks and action bookkeeping.
  isched: Management schedule index taken from the HRU so the tillage condition can inspect
    the active management database entries.
  iauto: Loop index over the active management schedule’s database entries during tillage-system
    checks.
  ivar_cur: Current integer value being compared against the table threshold for date and
    count-style conditions.
  ivar_tbl: Integer threshold derived from the condition constant, sometimes adjusted before
    calling `cond_integer`.
  targ: Computed comparison target after applying the condition’s operator and constant to
    a base value.
  pl_sum: Count of growing plants used to average plant stress values across the community.
  days_tot: Number of days in the active probability window or remaining period, used to convert
    a window into a daily application count.
  iwgn: Weather-generator parameter index obtained from the object’s weather station to access
    precipitation/PET ratio data.
  ly: Soil layer index used when calculating labile phosphorus through the 150 mm depth cutoff.
  strs_sum: Accumulated stress value across all growing plants before averaging for the water-,
    nitrogen-, or phosphorus-stress conditions.
  prob_cum: Local cumulative probability value for the land-use probability condition; distinct
    from the stored decision-table field of the same name.
  prob_apply: Computed probability threshold used to decide whether a land-use event should
    be applied on the current day.
  hru_exp_left: Expected number of HRUs still to be applied by the current day under the uniform
    land-use probability distribution.
  hru_act_left: Actual number of HRUs still left to apply, based on current application counts
    stored in the decision table.
  flo_m3: Channel or reservoir inflow converted to m3/s-style daily flow units before comparing
    it to the condition limit.
  wt_tot: Layer weight term used to convert phosphorus mass to concentration during the `p_lab_150`
    calculation.
  p_lab_tot: Accumulated labile phosphorus mass used to estimate concentration for the upper
    150 mm of soil.
  p_lab_ppm: Computed labile phosphorus concentration in ppm for the soil-depth condition.
  rto: Depth interpolation ratio used while stepping through soil layers for the 150 mm phosphorus
    calculation.
  pl_chk: Single-character flag used to remember whether a plant or tillage match was found
    during categorical checks.
uses:
  conditional_module: The conditional table object holds the rule set, comparison operators,
    alternative hit flags, and application-window bookkeeping that this subroutine evaluates
    and updates. Without `d_tbl`, there would be no condition rows to inspect, no `act_hit`
    array to disable alternatives, and no counters such as `days_prob`, `prob_cum`, `hru_lu_cur`,
    or `hru_ha_cur` to maintain.
  climate_module: This module supplies the daily weather and generator parameters used by
    precipitation, heat-unit, and precipitation-to-PET ratio conditions. `conditions` reads
    station-linked state such as `phubase0`, `precip`, `precip_next`, and the generator’s
    `p_pet_rto` to compare climate against the decision-table thresholds.
  time_module: The simulation clock determines date-based conditions and probability windows.
    `conditions` checks fields like `day_start`, `day`, `mo`, `yrc`, `yrs`, `yrc_start`, and
    `day_end_yr` to decide whether a rule is active today, whether a window crosses year boundaries,
    and how to compute seasonal probabilities.
  hru_module: HRU state provides the object-specific management and physical attributes that
    many conditions test. The routine uses HRU irrigation totals, slope, tile-drain flag,
    land-use/management code, and calibration group to decide whether a rule should pass for
    the current object.
  soil_module: Soil state is needed for water, erodibility, temperature, and phosphorus-related
    conditions. `conditions` compares the current profile water storage with field capacity
    or saturation limits, checks the top-layer USLE K factor, reads hydrologic soil group,
    and uses layer geometry and mass properties for the phosphorus concentration calculation.
  plant_module: Plant community state drives plant-growth, phenology, stress, and management-window
    conditions. The routine checks how many plants are present, whether each plant is growing,
    accumulated heat units, plant names, last planting/harvest/irrigation day counters, rotation
    year, LAI, and the auto-operation schedule fields inside the plant community.
  reservoir_module: Reservoir and wetland storage state is required for the volume, inflow,
    wet-depth, and weir-height conditions. These rules compare current water volume or discharge
    against threshold expressions so the model can trigger releases, irrigation, or wetland
    actions.
  reservoir_data_module: The reservoir-data module is not referenced by any resolved component
    in the extracted source, and no explicit state from it is visible in the routine body.
    It is imported, but the packet does not expose a concrete used symbol from this module
    for `conditions`.
  sd_channel_module: The SWAT-DEG channel state is required for the `ch_order` categorical
    condition. `conditions` checks the current channel order so it can allow or suppress alternatives
    based on stream network position.
  hydrograph_module: These object-connectivity and flow fields map the current object number
    to its weather station, channel degree segment, or irrigation demand source. `conditions`
    needs them to translate an HRU or channel index into the correct weather input, channel
    inflow, or irrigation demand state before testing the condition.
  output_landscape_module: Tile-flow output is used directly by the `tile_flo` condition,
    which compares the landscape tile drainage flux to the decision-table limit. This state
    matters because the routine uses it to trigger management based on subsurface drainage
    export.
  aquifer_module: Groundwater depth is the quantity tested by the aquifer-depth condition.
    `conditions` compares the current water-table depth against the table limit to decide
    whether the corresponding alternatives remain active.
  organic_mineral_mass_module: Plant biomass and soil phosphorus/carbon pools are needed for
    biomass, ground cover, labile phosphorus, and soil-carbon conditions. These values let
    the routine compare live vegetation mass and soil chemistry against management thresholds.
  mgt_operations_module: Management-operation state is required for the tillage condition.
    The routine inspects the active HRU schedule and the linked decision-table names to determine
    whether a requested tillage system is present in the current management database.
  water_allocation_module: Water-allocation state is needed for the irrigation-demand-by-water-right
    condition. `conditions` compares the current demand stored in the allocation object against
    the decision-table limit so water-right-based actions can be enabled or suppressed.
---

<!-- facts:header -->

Evaluates every active conditional rule for a decision table and marks which alternatives still pass. It compares live HRU, climate, plant, soil, time, reservoir, channel, aquifer, and wetland state against the table’s limits.

## Bottom Line

`conditions` is the decision-table evaluator used by management, reservoir, wetland, water-allocation, and time-control workflows. For the table pointed to by `d_tbl`, it loops through each condition row, computes the current model value for that condition, and disables any alternative whose operator test fails by setting `d_tbl%act_hit` entries to "n".

The routine handles a wide range of condition types: real-valued thresholds such as stress, precipitation, flow, volume, depth, biomass, and P-related values; integer/date thresholds such as days since planting or simulation day; categorical checks such as land use, calibration group, plant membership, hydrologic soil group, tillage system, and channel order; and probabilistic windows that can also assign `pcom(ob_cur)%dtbl(idtbl)%apply_day` and update probability bookkeeping.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`conditions` runs after a caller has selected and pointed `d_tbl` at the relevant decision-table record, such as `dtbl_lum`, `dtbl_res`, `dtbl_scen`, or `dtbl_flo`. The caller also passes the current object index or an object-specific index pair, and later `actions` relies on the resulting `d_tbl%act_hit` flags and probabilistic fields to decide which management action, release, or update actually executes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize decision-table hits | Set every alternative in the active decision table to an initial hit state of "y", then loop through each condition row in `d_tbl%conds` and dispatch by the row’s condition name. |
| 2. Evaluate plant stress and climate thresholds | For stress and climate conditions, gather the current object’s plant stress or weather value, average across growing plants when needed, resolve the correct HRU-to-weather-station mapping, and pass the real-valued result to `cond_real`. |
| 3. Test plant-growth state and days-since counters | Check whether specific plants are growing, whether a named plant exists in the community, and whether the elapsed-day counters for planting, harvest, irrigation, action, or simulation start satisfy the integer threshold via `cond_integer`. |
| 4. Compare HRU, soil, and calendar attributes | Compare irrigation totals, slope, soil-water state, Julian day, month, rotation year, perennial maturity year, biomass, LAI, USLE factors, hydrologic soil group, precipitation/PET ratio, soil phosphorus concentration, soil temperature, and soil carbon against the table limits. |
| 5. Filter tiledrain, probability, and land-use rules | Disable alternatives based on tile-drain status, draw random numbers for fixed and windowed probabilities, update probability-window bookkeeping, and reset land-use application counters when the active period ends. |
| 6. Compare channel, reservoir, wetland, and aquifer quantities | Translate object indices to channel, reservoir, or wetland state, compare channel flow, tile flow, irrigation demand, reservoir volume, reservoir inflow, wetland depth, weir height, wetland flow, and aquifer depth against the limit values, and disable alternatives that fail. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:conditional_module] | `d_tbl` | `d_tbl%act_hit, d_tbl%conds, d_tbl%cond(ic)%var, d_tbl%cond(ic)%ob_num, d_tbl%cond(ic)%lim_const, d_tbl%alts, d_tbl%act_hit(ialt), d_tbl%cond(ic)%ob, d_tbl%alt(ic,ialt), d_tbl%cond(ic)%lim_var, d_tbl%con_act(ic), d_tbl%cond(ic)%lim_op, d_tbl%frac_app, d_tbl%day_prev, d_tbl%days_prob, d_tbl%prob_cum, d_tbl%hru_lu, d_tbl%hru_lu_cur, d_tbl%hru_ha_cur` |
| [sym:climate_module] | `wst, wgn_pms` | `wst(iwst)%weat%phubase0, wst(iwst)%weat%precip, wst(iwst)%weat%precip_next, wst(iwst)%wco%wgn, wgn_pms(iwgn)%p_pet_rto` |
| [sym:time_module] | `time` | `time%day_start, time%day, time%mo, time%yrc, time%yrs, time%yrc_start, time%day_end_yr` |
| [sym:hru_module] | `hru` | `hru(ob_num)%irr_yr, hru(ob_num)%topo%slope, hru(ob_num)%lumv%usle_p, hru(ob_num)%tiledrain, hru(ob_num)%land_use_mgt_c, hru(ob_num)%cal_group` |
| [sym:soil_module] | `soil` | `soil(ob_num)%sumfc, soil(ob_num)%sumul, soil(ob_num)%sw, soil(ob_num)%ly(1)%usle_k, soil(ob_num)%hydgrp, soil(ob_num)%phys(1)%bd, soil(ob_num)%phys(1)%thick, soil(ob_num)%nly, soil(ob_num)%phys(ly)%d, soil(ob_num)%phys(ly-1)%d, soil(ob_num)%phys(ly)%bd, soil(ob_num)%phys(ly)%thick, soil(ob_num)%phys(2)%tmp` |
| [sym:plant_module] | `pcom` | `pcom(ob_num)%npl, pcom(ob_num)%plcur(ipl)%gro, pcom(ob_num)%plstr(ipl)%strsw, pcom(ob_num)%plstr(ipl)%strsn, pcom(ob_num)%plstr(ipl)%strsp, pcom(ob_num)%plcur(iipl)%phuacc, pcom(ob_num)%plcur(ipl)%phuacc, pcom(ob_num)%pl(iipl), pcom(ob_num)%days_plant, pcom(ob_num)%days_harv, pcom(ob_num)%days_irr, pcom(ob_num)%dtbl(idtbl)%days_act(iac), pcom(ob_num)%rot_yr, pcom(ob_num)%plcur(1)%curyr_mat, pcom(ob_num)%lai_sum, pcom(ob_cur)%dtbl(idtbl)%apply_day` |
| [sym:reservoir_module] | `res_ob, res, wet_ob, wet` | `res_ob(ires)%pvol, res_ob(ires)%evol, res(ires)%flo, wet_ob(ires)%depth, wet_ob(ires)%weir_hgt, wet_ob(ires)%pvol, wet_ob(ires)%evol, wet(ires)%flo` |
| [sym:reservoir_data_module] | `rndseed_cond` | `rndseed_cond` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(ob_num)%order` |
| [sym:hydrograph_module] | `sp_ob1, ob, ht2, irrig` | `sp_ob1%hru, sp_ob1%hru_lte, ob(iob)%wst, ob(ob_num)%wst, sp_ob1%chandeg, ht2%flo, irrig(ob_num)%demand` |
| [sym:output_landscape_module] | `hwb_d` | `hwb_d(ob_num)%qtile` |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(ob_num)%dep_wt` |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1` | `pl_mass(ob_num)%ab_gr_com%m, soil1(ob_num)%mp(1)%lab, soil1(ob_num)%mp(ly)%lab, soil1(ob_num)%cbn(1)` |
| [sym:mgt_operations_module] | `sched, dtbl_lum` | `sched(isched)%num_autos, sched(isched)%num_db(iauto), dtbl_lum(id)%name` |
| [sym:water_allocation_module] | `wallo` | `wallo(ob_num)%tot%demand` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `d_tbl%act_hit` | At the start of every call, before any condition rows are evaluated. | All alternatives are reset to "y" so each rule row begins with every alternative eligible until a condition explicitly turns one off. |
| `d_tbl%act_hit(ialt)` | When a specific alternative fails an operator test inside a condition row, or when a categorical check finds a mismatch. | The routine sets the failing alternative to "n" to mark it as ineligible for downstream action selection. |
| `iwst` | When a probability-based or HRU-mapping branch resolves the current weather station or similar object-specific index. | The weather-station index is updated to the station attached to the active object so precipitation and heat-unit conditions read the correct weather record. |
| `pcom(ob_cur)%dtbl(idtbl)%apply_day` | When the `prob_unif` branch chooses or clears a specific application day for the active HRU and decision table. | The routine stores the randomly selected day of application, or zero when the event is not scheduled for this window, so later action logic can check the exact day. |
| `d_tbl%days_prob` | When `prob_unif1` advances into a new day and the probability window still has days remaining. | The routine decrements the number of days left in the window, and also resets it when a new year-started window begins. |
| `d_tbl%prob_cum` | When `prob_unif1` advances into a new day and the window is active. | The routine recomputes the cumulative single-day probability for the current day of the window so the random draw can decide whether the event occurs. |
| `d_tbl%day_prev` | When `prob_unif1` detects a new day inside an active window. | The routine records the current day so it does not repeat the day-in-window update more than once per day. |
| `d_tbl%hru_lu_cur` | During `prob_unif_lu`, if the current day lies inside the land-use probability window and the random draw allows the event to proceed. | This counter tracks how many HRUs in the land-use group have already been applied for the current window. |
| `d_tbl%hru_ha_cur` | During `prob_unif_lu`, if the current day lies inside the land-use probability window and the random draw allows the event to proceed. | This field tracks how many hectares of the land-use group have already been applied for the current window. |

## File I/O

<!-- facts:io -->


## Lineage

`conditions.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `conditions.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `10e5ddc` (2025-08-27) — 08272025 updates
- `a03cc8b` (2025-06-26) — Add yearly irrigation calculations across modules
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'conditions' has no extracted documentation comment.
- algorithm_steps revised: condensed the original draft’s many overlapping step groups into six source-backed phases that match the visible control flow and line ranges.
- Source uses `wst`/`ob`/`sd_ch`/`res_ob`/`wet_ob`/`wet`/`dtbl_lum`/`dtbl_res`/`dtbl_flo`/`sched` in branches, but only the components visible in the packet were described.
- The `p_lab_150` branch computes `rto` but the extracted source does not use it after assignment; its purpose is therefore uncertain from the visible code.
- The `reservoir_data_module`, `reservoir_module`, and `sd_channel_module` imports are present, but only `sd_ch` is directly resolved in the extracted source packet.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
