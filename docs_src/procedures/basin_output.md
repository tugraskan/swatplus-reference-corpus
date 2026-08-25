---
kind: procedure
symbol: basin_output
title: basin_output
status: filled
source_hash: d9378dfa476f5ee5
version_label: SWAT+ 62.0.0
locals:
  ihru: Loop counter over HRU and hru_lte output elements; it indexes the active landscape
    elements that will be aggregated into basin totals.
  iihru: Index into `lsu_elem` for the current landscape element referenced by `ihru`; it
    is used to fetch the object type, basin fraction, and object number that control whether
    the element contributes to basin output.
  const: Temporary scaling factor set to `lsu_elem(iihru)%bsn_frac` and reused when adding
    each element’s contribution to basin totals and when converting monthly or yearly averages.
  sw_init: Temporary saver for the basin water-balance initial soil-water state while `bwb_d`
    is reset and rebuilt; it is restored into the new basin record after zeroing.
  sno_init: Temporary saver for the basin water-balance initial snowpack state while `bwb_d`
    is reset and rebuilt; it is restored into the new basin record after zeroing.
uses:
  time_module: '`time` controls every reporting branch in this routine: it supplies the current
    day, month, year, end-of-month/end-of-year/end-of-simulation flags, and averaging factors
    used to decide when basin records are written and how annual values are normalized.'
  hydrograph_module: '`sp_ob` provides the counts of routed HRU objects and non-routed hru_lte
    objects, so the routine knows how far to loop when collecting basin contributions from
    landscape outputs.'
  calibration_data_module: '`lsu_elem` maps each loop index to the correct landscape object
    number and basin expansion fraction, and its object type tells the routine whether to
    read from the HRU arrays or the hru_lte arrays.'
  output_landscape_module: These basin and landscape output records hold the daily, monthly,
    yearly, and average-annual water-balance, nutrient-balance, losses, and plant-weather
    values that `basin_output` accumulates, resets, scales, and writes.
  basin_module: '`pco` contains the basin print switches that gate each output block, while
    `bsn%name` is written on every record to identify the basin in the output files.'
  carbon_module: '`carbon_module` is listed as a used module, so it affects compilation and
    may supply carbon-related state elsewhere in the build, but no directly referenced symbols
    were extracted in this routine.'
---

<!-- facts:header -->

Aggregates basin-level water, nutrient, losses, and plant-weather outputs from HRU and hru_lte objects, then writes them at daily, monthly, yearly, and average-annual intervals.

## Bottom Line

`basin_output` builds basin summaries by starting from zeroed basin output records, adding routed HRU contributions from `hwb_d`, `hnb_d`, `hls_d`, and `hpw_d`, then adding hru_lte contributions from `hltwb_d`, `hltnb_d`, `hltls_d`, and `hltpw_d`. It preserves the initial basin water-balance state across resets so the basin totals can be accumulated correctly over the simulation period.

It matters because it is the routine that turns landscape-level output state into basin-level print records. Which records are written depends on `time` flags and basin print codes in `pco`, and the results feed the model’s basin output files for daily, monthly, yearly, and average-annual reporting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`basin_output` runs after the basin and landscape output state has been populated for the current timestep, and `command` calls it once the model has finished the setup and spatial object counts needed to know whether basin-level output should be generated. Its results are the basin-level files that downstream users rely on for daily, monthly, yearly, and average-annual summaries of water balance, nutrients, losses, and plant-weather variables.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Save and reset basin daily base state | The routine saves the current basin daily initial soil-water and snowpack values, resets `bwb_d` to the zeroed template `hwbz`, restores the saved initial values, and zeroes the basin daily nutrient, losses, and plant-weather summaries from `hnbz`, `hlsz`, and `hpwz`. |
| 2. Add routed HRU contributions | It loops over routed HRUs (`1..sp_ob%hru`), maps each index through `lsu_elem(ihru)%obtypno`, checks that the element contributes to the basin (`bsn_frac > 1.e-12`), and if the object type is `hru` it accumulates the weighted HRU water, nutrient, losses, and plant-weather outputs into the basin daily totals. |
| 3. Add non-routed hru_lte contributions | It loops over hru_lte objects (`1..sp_ob%hru_lte`), uses the same basin-fraction filter, and if the object type is `hlt` it adds the weighted hru_lte water, nutrient, losses, and plant-weather outputs into the same basin daily totals. |
| 4. Accumulate daily totals into monthly totals | The routine adds the day’s basin totals to the running monthly accumulators `bwb_m`, `bnb_m`, `bls_m`, and `bpw_m` so month-end averages can be computed later. |
| 5. Write daily basin outputs when enabled | On a print day (`pco%day_print == 'y'` and `pco%int_day_cur == pco%int_day`), it writes daily basin water, nutrient, losses, and plant-weather records for each enabled basin print code, and writes CSV versions when `pco%csvout == 'y'`. It also derives `bwb_d%sw` and `bwb_d%snopack` before writing the water balance, then carries the final daily values into the next step by resetting `bwb_d%sw_init` and `bwb_d%sno_init` to the daily final values. |
| 6. Roll monthly accumulators into yearly totals and normalize monthly outputs | At month end (`time%end_mo == 1`), it adds monthly totals into yearly accumulators, computes the month length with `ndays(time%mo + 1) - ndays(time%mo)`, scales the monthly water-balance and plant-weather values by that month length, writes monthly basin records when enabled, and then reinitializes the monthly basin output records from the zeroed templates while preserving the carried-in initial soil-water state. |
| 7. Roll yearly accumulators into average-annual totals and normalize yearly outputs | At year end (`time%end_yr == 1`), it adds yearly totals into average-annual accumulators, scales the yearly water-balance and plant-weather values by `time%day_end_yr`, writes yearly basin records when enabled, and then reinitializes the yearly basin output records from the zeroed templates while preserving the carried-in initial soil-water state. |
| 8. Compute and write average-annual basin outputs | At the end of the simulation (`time%end_sim == 1`), it divides the average-annual totals by `time%yrs_prt`, adjusts the average-annual water-balance and plant-weather outputs with `time%days_prt`, restores the final daily water-balance end states for water outputs, and writes the average-annual basin records and CSV records for each enabled print code. |
| 9. Return after formats | The routine exits after the output writes; the trailing format statements define the record layouts used by the formatted writes above. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%hru_lte` |
| [sym:calibration_data_module] | `lsu_elem` | `lsu_elem(ihru)%obtypno, lsu_elem(iihru)%bsn_frac, lsu_elem(iihru)%obtyp` |
| [sym:output_landscape_module] | `bwb_d, hwb_d, hltwb_d, bwb_m, bwb_y, bwb_a, hnb_d, hls_d, hpw_d, hltnb_d, hltls_d, hltpw_d, hwbz, bnb_d, hnbz, bls_d, hlsz, bpw_d, hpwz, bnb_m, bls_m` | `bwb_d%sw_init, bwb_d%sno_init, bwb_d%sw_final, hwb_d(iihru)%sw_final, bwb_d%sno_final, hwb_d(iihru)%sno_final, hltwb_d(iihru)%sw_final, hltwb_d(iihru)%sno_final, bwb_d%sw, bwb_d%snopack, bwb_m%sw_final, bwb_m%sno_final, bwb_m%sw_init, bwb_m%sno_init, bwb_y%sw_final, bwb_y%sno_final, bwb_y%sw_init, bwb_y%sno_init, bwb_a%sw_init, bwb_a%sno_init, bwb_a%sw_final, bwb_a%sno_final, bwb_a%precip` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%wb_bsn%d, bsn%name, pco%csvout, pco%nb_bsn%d, pco%ls_bsn%d, pco%pw_bsn%d, pco%wb_bsn%m, pco%nb_bsn%m, pco%ls_bsn%m, pco%pw_bsn%m, pco%wb_bsn%y, pco%nb_bsn%y, pco%ls_bsn%y, pco%pw_bsn%y, pco%wb_bsn%a, pco%nb_bsn%a, pco%ls_bsn%a, pco%pw_bsn%a` |
| [sym:carbon_module] | `carbon_module` | `no resolved imported state or types were extracted from `carbon_module` for this routine` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bwb_d` | At the start of every call before summing HRU outputs | `bwb_d` is reset to the zeroed daily basin water-balance template `hwbz`, then rebuilt from the current day’s routed contributions so it represents the basin-wide daily water balance for this timestep. |
| `bwb_d%sw_init` | At the start of every call while preserving prior initial values | The initial soil-water state is saved, the basin record is reset, and the saved value is restored so the daily basin water-balance keeps the correct starting soil-water amount. |
| `bwb_d%sno_init` | At the start of every call while preserving prior initial values | The initial snowpack state is saved, the basin record is reset, and the saved value is restored so the daily basin water-balance keeps the correct starting snowpack amount. |
| `bnb_d` | After daily aggregation and before daily writes | `bnb_d` is rebuilt from zero and then filled with the weighted HRU and hru_lte nutrient-balance contributions, so it holds the basin’s daily nutrient balance before any print step. |
| `bls_d` | After daily aggregation and before daily writes | `bls_d` is rebuilt from zero and then filled with the weighted HRU and hru_lte losses contributions, so it holds the basin’s daily losses summary before output. |
| `bpw_d` | After daily aggregation and before daily writes | `bpw_d` is rebuilt from zero and then filled with the weighted HRU and hru_lte plant-weather contributions, so it holds the basin’s daily plant-weather summary before output. |
| `bwb_d%sw_final` | During daily output when `pco%wb_bsn%d == 'y'` | The basin daily final soil-water value is updated by summing the weighted HRU and hru_lte `sw_final` contributions, so the written record reflects the basin-average ending soil water for the day. |
| `bwb_d%sno_final` | During daily output when `pco%wb_bsn%d == 'y'` | The basin daily final snowpack value is updated by summing the weighted HRU and hru_lte `sno_final` contributions, so the written record reflects the basin-average ending snowpack for the day. |
| `bwb_m` | At each month end before monthly output is written | `bwb_m` accumulates daily basin water-balance totals through the month, is divided by the month length at month end, and is then written as the basin monthly water-balance summary. |
| `bnb_m` | At each month end before monthly output is written | `bnb_m` accumulates daily basin nutrient totals through the month and is then written as the basin monthly nutrient-balance summary. |
| `bls_m` | At each month end before monthly output is written | `bls_m` accumulates daily basin losses through the month and is then written as the basin monthly losses summary. |
| `bpw_m` | At each month end before monthly output is written | `bpw_m` accumulates daily basin plant-weather totals through the month, is divided by the month length, and is then written as the basin monthly plant-weather summary. |
| `bwb_d%sw` | After daily output when the water balance record is written | `bwb_d%sw` is computed as the average of the initial and final daily soil-water values, so the printed daily water balance includes the mean soil-water content for the timestep. |
| `bwb_d%snopack` | After daily output when the water balance record is written | `bwb_d%snopack` is computed as the average of the initial and final daily snowpack values, so the printed daily water balance includes the mean snowpack water equivalent for the timestep. |
| `bwb_y` | At each year end before yearly output is written | `bwb_y` accumulates monthly basin water-balance totals across the year, is divided by the year length at year end, and is then written as the basin yearly water-balance summary. |
| `bnb_y` | At each year end before yearly output is written | `bnb_y` accumulates monthly basin nutrient totals across the year and is then written as the basin yearly nutrient-balance summary. |
| `bls_y` | At each year end before yearly output is written | `bls_y` accumulates monthly basin losses across the year and is then written as the basin yearly losses summary. |
| `bpw_y` | At each year end before yearly output is written | `bpw_y` accumulates monthly basin plant-weather totals across the year, is divided by the year length at year end, and is then written as the basin yearly plant-weather summary. |
| `bwb_m%sw_final` | At each month-end reset after monthly output is written | The monthly basin water-balance final soil-water value is refreshed from the current daily basin final state so the monthly summary carries the end-of-month soil-water amount before the record is reset. |
| `bwb_m%sno_final` | At each month-end reset after monthly output is written | The monthly basin water-balance final snowpack value is refreshed from the current daily basin final state so the monthly summary carries the end-of-month snowpack amount before the record is reset. |
| `bwb_m%sw_init` | At each month-end reset after monthly output is written | The monthly basin water-balance initial soil-water value is carried forward from the monthly final state before `bwb_m` is reset, preserving continuity into the next month. |
| `bwb_m%sno_init` | At each month-end reset after monthly output is written | The monthly basin water-balance initial snowpack value is carried forward from the monthly final state before `bwb_m` is reset, preserving continuity into the next month. |
| `bwb_a` | At end of simulation before average-annual water output is written | `bwb_a` accumulates yearly basin water-balance totals across the whole simulation, is normalized by simulation years and days, and then is written as the average-annual basin water balance. |
| `bnb_a` | At end of simulation before average-annual nutrient output is written | `bnb_a` accumulates yearly basin nutrient totals across the whole simulation, is divided by the simulation year count, and then is written as the average-annual basin nutrient balance. |

## File I/O

<!-- facts:io -->


## Lineage

The source history shows four resolved changes to `basin_output`. It was introduced in `df07e3f` with the full basin aggregation and output logic. `39fabde` only initialized local variables (`ihru`, `iihru`, `const`, `sw_init`, `sno_init`). `daae0d8` commented out several `nplnt` assignments in monthly, yearly, and average-annual plant-weather blocks. `2fe89fd` changed the CSV `G0.3` formats to `G0.6` for basin CSV writes. `0d9bb63` restructured the average-annual section so the end-of-simulation calculations run under `time%end_sim == 1` and the actual writes remain gated by the basin print codes.

- `df07e3f` created the routine with daily, monthly, yearly, and average-annual basin aggregation from HRU and hru_lte outputs, including the reset-and-accumulate pattern used throughout the procedure.
- `39fabde` changed the local counters and temporary scalars to start at zero, removing uninitialized local state risk in the basin aggregation loops and print calculations.
- `daae0d8` disabled the `nplnt` assignments in monthly, yearly, and average-annual plant-weather output blocks, changing which plant-weather fields are copied into basin summaries before writing.
- `2fe89fd` increased CSV numeric precision from `G0.3` to `G0.6` in the basin CSV output writes, affecting the textual precision of the exported records.
- `0d9bb63` moved average-annual computations under a plain `time%end_sim == 1` check and nested the basin print-code guards inside it, so the calculations now occur at simulation end even when the actual average-annual write is disabled.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_output' has no extracted documentation comment.
- algorithm_steps revised: collapsed the draft into the nine source-backed execution phases visible in basin_output.f90 and kept the full control flow from daily through average-annual output.
- `carbon_module` is used but no direct symbols were extracted from the provided context; its specific contribution here is uncertain from this packet alone.
