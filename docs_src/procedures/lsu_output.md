---
kind: procedure
symbol: lsu_output
title: lsu_output
status: filled
source_hash: 625898ce60c2ba36
version_label: SWAT+ 62.0.0
locals:
  ilsu: Loop index for the LSU output region being processed and written. It selects the current
    element in `db_mx%lsu_out`, the `lsu_out`, `ruwb_*`, `runb_*`, `ruls_*`, and `rupw_*`
    arrays, and is also passed through to the output records as the LSU identifier.
  ielem: Loop index over the member elements listed in `lsu_out(ilsu)%num`. It walks the calibration
    mapping for one LSU so the routine can fetch each contributing HRU or HRU_LTE and weight
    its outputs into the LSU totals.
  ihru: Element index pulled from `lsu_out(ilsu)%num(ielem)`. It identifies the specific HRU
    or HRU_LTE whose daily outputs are being accumulated into the current LSU summary.
  iob: Object index used to fetch `ob(iob)%gis_id` for the current LSU. It is set from `sp_ob1%ru
    + ilsu - 1` so the output rows can carry the right GIS/object label.
  const: Area-weighting factor copied from `lsu_elem(ihru)%ru_frac`. The routine multiplies
    HRU or HRU_LTE outputs by this fraction before adding them to LSU totals, so `const` controls
    each element’s contribution.
  sw_init: Temporary hold for the current LSU’s starting soil-water value when the routine
    resets daily, monthly, yearly, or average-annual water-balance accumulators. It preserves
    the carry-over initial condition across the zeroing step.
  sno_init: Temporary hold for the current LSU’s starting snow-pack value when the routine
    resets water-balance accumulators. It preserves the carry-over snow initial condition
    across period boundaries.
uses:
  time_module: '`time_module` provides the simulation clock and period-end flags that decide
    when daily, monthly, yearly, and end-of-simulation reports are written. Its fields also
    supply the date labels written into every LSU output record.'
  basin_module: '`pco` holds the print-code switches that gate each LSU report stream. The
    routine checks these flags to decide whether to write water, nutrient, loss, and plant-weather
    output for daily, monthly, yearly, and average-annual periods, and whether to emit CSV
    companions.'
  maximum_data_module: '`db_mx%lsu_out` sets the number of LSU output regions to iterate over.
    Without that bound the routine would not know how many LSU accumulator slots and output
    rows to process.'
  calibration_data_module: '`lsu_out` and `lsu_elem` define the LSU-to-HRU/HRU_LTE membership
    map and labels. The routine uses `lsu_out(ilsu)%num_tot` and `lsu_out(ilsu)%num(ielem)`
    to find contributors, `lsu_elem(ihru)%ru_frac` to weight them, and `lsu_out(ilsu)%name`
    to label each output line.'
  hydrograph_module: '`sp_ob1%ru` provides the starting RU object index used to derive `iob`
    for the current LSU. That lets the routine print the correct `ob(iob)%gis_id` alongside
    each LSU summary.'
  output_landscape_module: '`output_landscape_module` owns the daily, monthly, yearly, and
    average-annual LSU result containers that this routine fills and then writes. The routine
    reads member HRU/HRU_LTE outputs from the HRU arrays and stores the aggregated LSU values
    in the `ruwb_*`, `runb_*`, `ruls_*`, and `rupw_*` structures before output.'
---

<!-- facts:header -->

Aggregates HRU- and HRU_LTE-level outputs to landscape-unit (LSU) daily, monthly, yearly, and average-annual summaries, then writes those summaries to fixed output units and optional CSV files.

## Bottom Line

`lsu_output` is the LSU reporting routine. For each LSU, it first clears the daily summary containers, then loops over the LSU’s member elements and area-weights the matching HRU or HRU_LTE outputs into LSU daily water balance, nutrient balance, loss, and plant-weather totals.

It also rolls those daily totals into month, year, and whole-simulation average-annual accumulators. When the print-code flags in `pco` say a report should be written, the routine emits formatted records to units 2140–2177, using `time` fields and LSU metadata such as `ob(iob)%gis_id` and `lsu_out(ilsu)%name` to label each output row.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after the model has built LSU membership and populated the HRU and HRU_LTE daily/monthly/yearly output arrays. Its results feed the LSU water, nutrient, loss, and plant-weather output files that document simulation progress through the run and the final average-annual summaries at the end of the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Clear daily LSU accumulators | For each LSU, save the current soil-water and snow initial values, reset the daily water-balance, nutrient-balance, losses, and plant-weather accumulators to their zero templates, then restore the saved initial values into the daily water-balance container. |
| 2. Build each LSU from member HRUs | Loop over the LSU membership list, look up each member HRU or HRU_LTE from `lsu_out(ilsu)%num`, derive the object index `iob`, and add the member outputs to the LSU totals using the LSU fraction `lsu_elem(ihru)%ru_frac` when the member type is `hru` or `hlt`. |
| 3. Roll daily totals into monthly sums | Accumulate the current day’s LSU totals into the monthly containers so the month-end branch can compute monthly summaries from the running sums. |
| 4. Write daily LSU reports when scheduled | When daily printing is enabled and the current day matches the print interval, compute daily average water content and snowpack, then write the daily water-balance, nutrient-balance, losses, and plant-weather records to their fixed output units and optional CSV units. |
| 5. Close out the monthly period | At month end, copy the monthly totals into yearly accumulators, convert the monthly water and plant-weather totals to per-day averages, write any enabled monthly LSU reports, carry the ending water state forward as the next month’s initial state, and reset the monthly containers for the next cycle. |
| 6. Close out the yearly period | At year end, add the yearly totals into the average-annual accumulators, convert the yearly water and plant-weather totals to per-day averages using `time%day_end_yr`, write any enabled yearly LSU reports, carry the ending water state forward, and reset the yearly containers for the next cycle. |
| 7. Write end-of-simulation averages | On the final simulation step, divide the average-annual accumulators by `time%yrs_prt`, restore the daily end-state water and plant-weather fields needed by the report formats, and write any enabled average-annual LSU reports to the fixed output units and CSV files. |
| 8. Return to caller | Exit after all LSU regions have been processed and their scheduled reports written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%wb_lsu%d, pco%csvout, pco%nb_lsu%d, pco%ls_lsu%d, pco%pw_lsu%d, pco%wb_lsu%m, pco%nb_lsu%m, pco%ls_lsu%m, pco%pw_lsu%m, pco%wb_lsu%y, pco%nb_lsu%y, pco%ls_lsu%y, pco%pw_lsu%y, pco%wb_lsu%a, pco%nb_lsu%a, pco%ls_lsu%a, pco%pw_lsu%a` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:calibration_data_module] | `lsu_out, lsu_elem` | `lsu_out(ilsu)%num_tot, lsu_out(ilsu)%num(ielem), lsu_elem(ihru)%ru_frac, lsu_elem(ihru)%obtyp, lsu_out(ilsu)%name` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%ru` |
| [sym:output_landscape_module] | `ruwb_d, hwb_d, hltwb_d, ruwb_m, rupw_m, rupw_d, ruwb_y, rupw_y, ruwb_a, rupw_a, runb_d, ruls_d, hnb_d, hls_d, hpw_d, hltnb_d` | `ruwb_d(ilsu)%sw_init, ruwb_d(ilsu)%sno_init, ruwb_d(ilsu)%sw_final, hwb_d(ihru)%sw_final, ruwb_d(ilsu)%sno_final, hwb_d(ihru)%sno_final, hltwb_d(ihru)%sw_final, ruwb_d(ilsu)%sw, ruwb_d(ilsu)%snopack, ruwb_m(ilsu)%sw_final, ruwb_m(ilsu)%sno_final, ruwb_m(ilsu)%sw_init, ruwb_m(ilsu)%sno_init, rupw_m(ilsu)%nplnt, rupw_d(ilsu)%nplnt, rupw_m(ilsu)%pplnt, rupw_d(ilsu)%pplnt, ruwb_y(ilsu)%sw_final, ruwb_y(ilsu)%sno_final, ruwb_y(ilsu)%sw_init, ruwb_y(ilsu)%sno_init, rupw_y(ilsu)%nplnt, rupw_y(ilsu)%pplnt, ruwb_a(ilsu)%sw_init, ruwb_a(ilsu)%sno_init, ruwb_a(ilsu)%sw_final, ruwb_a(ilsu)%sno_final, rupw_a(ilsu)%nplnt, rupw_a(ilsu)%pplnt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ruwb_d(ilsu)` | At the start of each LSU loop, before new HRU contributions are summed. | `ruwb_d(ilsu)` is reset to the zero template `hwbz` so the current day’s LSU water balance can be rebuilt from member outputs. |
| `ruwb_d(ilsu)%sw_init` | At the start of each LSU loop, after saving the previous initial value. | `ruwb_d(ilsu)%sw_init` is restored so the day’s water-balance output keeps the carry-over soil-water starting point after the container reset. |
| `ruwb_d(ilsu)%sno_init` | At the start of each LSU loop, after saving the previous initial value. | `ruwb_d(ilsu)%sno_init` is restored so the day’s water-balance output keeps the carry-over snow starting point after the container reset. |
| `runb_d(ilsu)` | During the LSU membership summation when a member has `lsu_elem(ihru)%obtyp == "hru"` or `"hlt"` and `lsu_elem(ihru)%ru_frac > 1.e-9`. | `runb_d(ilsu)` accumulates the area-weighted daily nutrient balance from the contributing HRU or HRU_LTE. |
| `ruls_d(ilsu)` | During the LSU membership summation when a member has `lsu_elem(ihru)%obtyp == "hru"` or `"hlt"` and `lsu_elem(ihru)%ru_frac > 1.e-9`. | `ruls_d(ilsu)` accumulates the area-weighted daily losses from the contributing HRU or HRU_LTE. |
| `rupw_d(ilsu)` | During the LSU membership summation when a member has `lsu_elem(ihru)%obtyp == "hru"` or `"hlt"` and `lsu_elem(ihru)%ru_frac > 1.e-9`. | `rupw_d(ilsu)` accumulates the area-weighted daily plant-weather output from the contributing HRU or HRU_LTE. |
| `ruwb_d(ilsu)%sw_final` | During the LSU membership summation when a member has `lsu_elem(ihru)%obtyp == "hru"` or `"hlt"` and `lsu_elem(ihru)%ru_frac > 1.e-9`. | `ruwb_d(ilsu)%sw_final` is increased by the weighted final soil-water value from the contributing HRU or HRU_LTE. |
| `ruwb_d(ilsu)%sno_final` | During the LSU membership summation when a member has `lsu_elem(ihru)%obtyp == "hru"` or `"hlt"` and `lsu_elem(ihru)%ru_frac > 1.e-9`. | `ruwb_d(ilsu)%sno_final` is increased by the weighted final snow-pack value from the contributing HRU or HRU_LTE. |
| `ruwb_m(ilsu)` | At month end, after daily LSU totals have been accumulated. | `ruwb_m(ilsu)` is updated by adding the current daily LSU water-balance totals, building the month-to-date summary. |
| `runb_m(ilsu)` | At month end, after daily LSU totals have been accumulated. | `runb_m(ilsu)` is updated by adding the current daily LSU nutrient-balance totals, building the month-to-date summary. |
| `ruls_m(ilsu)` | At month end, after daily LSU totals have been accumulated. | `ruls_m(ilsu)` is updated by adding the current daily LSU losses totals, building the month-to-date summary. |
| `rupw_m(ilsu)` | At month end, after daily LSU totals have been accumulated. | `rupw_m(ilsu)` is updated by adding the current daily LSU plant-weather totals, building the month-to-date summary. |
| `ruwb_d(ilsu)%sw` | When the daily LSU water-balance report is prepared. | `ruwb_d(ilsu)%sw` is set to the mean of the initial and final daily soil-water values so the report prints an average soil-water content for the step. |
| `ruwb_d(ilsu)%snopack` | When the daily LSU water-balance report is prepared. | `ruwb_d(ilsu)%snopack` is set to the mean of the initial and final daily snow-pack values so the report prints an average snow-water equivalent for the step. |
| `ruwb_y(ilsu)` | At year end, after daily LSU totals have been accumulated into yearly totals. | `ruwb_y(ilsu)` is updated by adding the current monthly or yearly water-balance totals so the year-to-date summary can be written and later rolled into average-annual output. |
| `runb_y(ilsu)` | At year end, after daily LSU totals have been accumulated into yearly totals. | `runb_y(ilsu)` is updated by adding the current monthly or yearly nutrient-balance totals so the year-to-date summary can be written and later rolled into average-annual output. |
| `ruls_y(ilsu)` | At year end, after daily LSU totals have been accumulated into yearly totals. | `ruls_y(ilsu)` is updated by adding the current monthly or yearly losses totals so the year-to-date summary can be written and later rolled into average-annual output. |
| `rupw_y(ilsu)` | At year end, after daily LSU totals have been accumulated into yearly totals. | `rupw_y(ilsu)` is updated by adding the current monthly or yearly plant-weather totals so the year-to-date summary can be written and later rolled into average-annual output. |
| `ruwb_m(ilsu)%sw_final` | At the start of the next month after the month-end report has been written. | `ruwb_m(ilsu)%sw_final` is refreshed from the current daily soil-water final value so the next monthly cycle starts from the correct carry-over state. |
| `ruwb_m(ilsu)%sno_final` | At the start of the next month after the month-end report has been written. | `ruwb_m(ilsu)%sno_final` is refreshed from the current daily snow final value so the next monthly cycle starts from the correct carry-over state. |
| `ruwb_m(ilsu)%sw_init` | At the start of the next month after the month-end report has been written. | `ruwb_m(ilsu)%sw_init` is set to the monthly final soil-water value so the carry-over initial condition is preserved for the next month. |
| `ruwb_m(ilsu)%sno_init` | At the start of the next month after the month-end report has been written. | `ruwb_m(ilsu)%sno_init` is set to the monthly final snow value so the carry-over initial condition is preserved for the next month. |
| `rupw_m(ilsu)%nplnt` | At month end when `pco%pw_lsu%m == 'y'`. | `rupw_m(ilsu)%nplnt` is set from the daily LSU plant-weather value so the monthly report prints the end-of-period plant nitrogen uptake value rather than the accumulated total. |
| `rupw_m(ilsu)%pplnt` | At month end when `pco%pw_lsu%m == 'y'`. | `rupw_m(ilsu)%pplnt` is set from the daily LSU plant-weather value so the monthly report prints the end-of-period plant phosphorus uptake value rather than the accumulated total. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source-affecting revisions and two no-op newline cleanups. The substantive 2024 additions established the current lsu_output implementation and the 2024 variable-initialization change set local counters and temporaries to zero; later 2026 CSV-output fixes changed the CSV numeric format from G0.3 to G0.6 in the LSU output writes. Two later commits only adjusted trailing newlines without changing procedure behavior.

- 39fabde initialized the local counters and temporaries (`ilsu`, `ielem`, `ihru`, `iob`, `const`, `sw_init`, `sno_init`) to zero at declaration.
- 2fe89fd widened the CSV write formats in the LSU output branches from `G0.3` to `G0.6`, affecting the precision of units 2144, 2145, 2146, 2147, 2154, 2155, 2156, 2164, 2165, 2166, 2175, 2176, and 2177.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'lsu_output' has no extracted documentation comment.
