---
kind: procedure
symbol: basin_aquifer_output
title: basin_aquifer_output
status: filled
source_hash: 274efc9a3f4597d8
version_label: SWAT+ 62.0.0
locals:
  iaq: Loop counter over aquifers in the basin; it indexes `aqu_prm` and `aqu_d` while the
    routine area-weights each aquifer's contribution into `baqu_d`.
  const: 'Temporary scaling factor used twice: first as each aquifer''s basin-area fraction
    (`aqu_prm(iaq)%area_ha / bsn%area_tot_ha`), then as the number of days in the current
    month when converting monthly totals to monthly averages.'
uses:
  time_module: The routine depends on `time` to know the current simulation date and to detect
    period boundaries. Those flags control whether daily, monthly, yearly, or average-annual
    aquifer summaries are written and when accumulated values are normalized or reset.
  basin_module: The basin module provides the basin name and total basin area used in the
    weighted daily average, plus the print-control codes that decide whether basin aquifer
    output is written at daily, monthly, yearly, or average-annual intervals and whether CSV
    copies are emitted.
  aquifer_module: The aquifer module supplies the aquifer parameter and dynamic state arrays
    being summarized, along with the basin-level summary accumulators that this routine updates,
    normalizes, prints, and resets.
  calibration_data_module: The module is used in the `use` list, but the extracted lines show
    no specific symbol reference from it; the routine's observable behavior is therefore not
    tied to any resolved calibration-data component in the provided evidence.
  hydrograph_module: The hydrograph module provides `sp_ob%aqu`, the basin's aquifer-object
    count. That count sets the loop bound for summing all aquifer contributions into the basin
    daily aquifer summary.
---

<!-- facts:header -->

Aggregates aquifer state to basin-scale daily, monthly, yearly, and average-annual outputs. It writes those summaries to the aquifer basin output units when the matching print flags are enabled.

## Bottom Line

This subroutine builds basin-level aquifer summaries from the current aquifer states. It starts with the base aquifer-zone state, area-weights the individual aquifer contributions into a basin daily value, then rolls those values into monthly, yearly, and average-annual totals.

Its main job is output reporting: depending on the print codes in `pco` and the simulation time flags in `time`, it writes the selected aquifer summaries to the fixed output units `2090`-`2097`, including optional CSV records. These reports are what downstream users and post-processing tools rely on for basin aquifer diagnostics.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine after the model has set up basin print controls, time flags, aquifer parameters, and aquifer dynamic states. The results feed the aquifer basin output files used for daily, monthly, yearly, and average-annual reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the basin daily aquifer summary. | Start from `aquz`, which acts as the baseline basin aquifer state for the current timestep. |
| 2. Area-weight each aquifer into the daily basin value. | Loop over `iaq = 1, sp_ob%aqu`, compute each aquifer's basin-area fraction from `aqu_prm(iaq)%area_ha / bsn%area_tot_ha`, and add the weighted `aqu_d(iaq)` contribution into `baqu_d`. |
| 3. Accumulate the daily value into the monthly basin total. | Add the current daily basin aquifer summary to `baqu_m` so the month can later be averaged and reported. |
| 4. Write the daily basin aquifer output when daily printing is enabled. | If `pco%day_print` is active and the day-print interval matches, then write daily records to unit 2090 and optional CSV unit 2094 when `pco%aqu_bsn%d` and `pco%csvout` are enabled. |
| 5. Convert monthly accumulators to monthly averages and roll them into yearly accumulation. | At month end, divide the monthly storage, depth-to-water, and nitrate summaries by the number of days in the month, then add the monthly result into `baqu_y`. |
| 6. Write the monthly basin aquifer output when monthly printing is enabled. | If monthly aquifer printing is enabled, write the monthly record to unit 2091 and optional CSV unit 2095, then reset `baqu_m` back to `aquz` for the next month. |
| 7. Convert yearly accumulators to yearly averages and roll them into the simulation-total accumulator. | At year end, divide the yearly storage, depth-to-water, and nitrate summaries by 12, then add the yearly result into `baqu_a`. |
| 8. Write the yearly basin aquifer output when yearly printing is enabled. | If yearly aquifer printing is enabled, write the yearly record to unit 2092 and optional CSV unit 2096, then reset `baqu_y` back to `aquz` for the next year. |
| 9. Write the average-annual basin aquifer output at simulation end. | When the simulation ends and average-annual aquifer output is enabled, divide `baqu_a` by `time%yrs_prt`, then write the final average-annual record to unit 2093 and optional CSV unit 2097. |
| 10. Return to the caller. | Exit the routine after the output records have been written and the yearly or monthly accumulators have been reset as needed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `bsn, pco` | `bsn%area_tot_ha, pco%day_print, pco%int_day_cur, pco%int_day, pco%aqu_bsn%d, bsn%name, pco%csvout, pco%aqu_bsn%m, pco%aqu_bsn%y, pco%aqu_bsn%a` |
| [sym:aquifer_module] | `aqu_prm, baqu_m, baqu_y, aqu_d, baqu_d, aquz, baqu_a` | `aqu_prm(iaq)%area_ha, baqu_m%stor, baqu_m%dep_wt, baqu_m%no3_st, baqu_y%stor, baqu_y%dep_wt, baqu_y%no3_st` |
| [sym:calibration_data_module] | `No resolved imported state or types from `calibration_data_module` were identified in the extracted source.` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%aqu` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `baqu_d` | During every call, before any output checks. | `baqu_d` is rebuilt from `aquz` and then incremented with each aquifer's area-weighted daily contribution, so it becomes the basin's daily aquifer summary for the current timestep. |
| `baqu_m` | During every call, after `baqu_d` is assembled. | `baqu_m` receives the current daily basin aquifer summary each timestep, so it accumulates the month-to-date total before being converted to a monthly average at month end. |
| `baqu_m%stor` | At month end (`time%end_mo == 1`). | `baqu_m%stor` is divided by the number of days in the current month so the monthly storage summary becomes an average over the month. |
| `baqu_m%dep_wt` | At month end (`time%end_mo == 1`). | `baqu_m%dep_wt` is divided by the number of days in the current month so the monthly depth-to-water summary is normalized to a monthly average. |
| `baqu_m%no3_st` | At month end (`time%end_mo == 1`). | `baqu_m%no3_st` is divided by the number of days in the current month so the monthly aquifer nitrate storage summary is averaged before rolling into yearly totals. |
| `baqu_y` | At month end after the monthly values are normalized. | `baqu_y` accumulates the monthly aquifer summary into the yearly basin summary, so it grows across months until year end. |
| `baqu_y%stor` | At year end (`time%end_yr == 1`). | `baqu_y%stor` is divided by 12 so the yearly storage component becomes an average monthly value for the year. |
| `baqu_y%dep_wt` | At year end (`time%end_yr == 1`). | `baqu_y%dep_wt` is divided by 12 so the yearly depth-to-water component is normalized to a yearly average. |
| `baqu_y%no3_st` | At year end (`time%end_yr == 1`). | `baqu_y%no3_st` is divided by 12 so the yearly nitrate storage component becomes a yearly average before contributing to the long-term total. |
| `baqu_a` | At year end and after yearly normalization. | `baqu_a` accumulates the yearly basin aquifer summary into the simulation-total average-annual accumulator, then is later divided by the number of printed years at simulation end. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits show the routine's history. `df07e3f` added the subroutine with basin aquifer daily, monthly, yearly, and average-annual accumulation plus fixed-record and CSV writes. `39fabde` initialized local variables `iaq` and `const` to zero. `2fe89fd` changed all CSV writes from `G0.3` to `G0.6`, increasing numeric precision in the CSV output. The later code in the extracted span still reflects those precision updates and the same output flow.

- df07e3f introduced the routine and its full output workflow: area-weighted daily basin aquifer aggregation, month/year/end-of-simulation accumulation, print gating via `pco`, and writes to units 2090-2097.
- 39fabde only changed local variable initialization, setting `iaq = 0` and `const = 0.`; it did not alter the output algorithm.
- 2fe89fd changed the CSV write format on units 2094, 2095, 2096, and 2097 from `G0.3` to `G0.6`, increasing exported precision without changing the computed values.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_aquifer_output' has no extracted documentation comment.
