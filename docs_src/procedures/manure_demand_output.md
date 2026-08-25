---
kind: procedure
symbol: manure_demand_output
title: manure_demand_output
status: filled
source_hash: 421b24e79e6d34b7
version_label: SWAT+ 62.0.0
args:
  imallo: '`imallo` selects which manure allocation object in `mallo` this routine reports
    on. The value is used to pick the specific source and demand arrays whose withdrawals
    are summed and written.'
locals:
  itrn: Loop index over `mallo(imallo)%trn_obs`, the demand/transaction objects being reported.
    It replaces the older `idmd` name and is also written to the output records as the demand-object
    index.
  isrc: Loop index over `mallo(imallo)%src_obs`, the source objects attached to each demand
    object. It is used to accumulate and then write per-source withdrawal totals for each
    demand transaction.
uses:
  time_module: The `time` state controls when each output block runs and what date stamp is
    written. Its day, month, year, and end-of-period flags decide whether the routine writes
    daily, monthly, yearly, or simulation-average records and whether monthly or yearly totals
    are rolled up.
  hydrograph_module: The `hydrograph_module` provides the `pco` control flags that turn each
    reporting tier on or off. `manure_demand_output` uses those flags to decide whether to
    write the human-readable table output, the CSV companion output, and which periods are
    active.
  manure_allocation_module: The `manure_allocation_module` provides the `mallo` data structure
    that holds the demand objects, source objects, and withdrawal accumulators this routine
    reports. Without those arrays and counters, the subroutine would have no source-to-demand
    values to sum, reset, or write.
---

<!-- facts:header -->

Writes manure allocation demand output for one manure allocation object. It reports daily, monthly, yearly, and average annual withdrawals by demand target and source.

## Bottom Line

manure_demand_output loops through each demand transaction in one manure allocation object and records how much manure or nutrient withdrawal came from each source. It accumulates daily withdrawals into monthly totals, monthly into yearly totals, and yearly into average-annual totals before writing those summaries to the allocation output units.

The routine is a reporting step only: it does not solve the allocation itself, but it preserves the running totals needed for the daily, monthly, yearly, and simulation-average outputs. Those outputs depend on the current simulation time flags and the `mallo(imallo)` demand/source arrays prepared earlier in the water-allocation workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during the manure allocation output phase, after allocation objects have been assembled in `mallo`. Its results feed the reporting files for daily, monthly, yearly, and average-annual manure demand summaries, so downstream users of the output files depend on it for the accumulated withdrawal totals.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over demand objects in the selected allocation | Iterate through each transaction/demand object stored in `mallo(imallo)%trn`, using `itrn` to visit every demand target in the selected manure allocation object. |
| 2. Accumulate daily withdrawal into the monthly running total | For each source, add the current daily withdrawal `withdr` into `withdr_m` so the monthly total reflects the day's allocation before daily values are cleared. |
| 3. Write daily records when daily output is enabled | If daily water-allocation output is active, write the daily record to unit 3210 and, when CSV output is also active, write the CSV version to unit 3211. |
| 4. Clear daily withdrawals after reporting | Reset each source's `withdr` array element to zero so the next day starts with no carried-over daily withdrawal. |
| 5. Roll monthly totals into yearly totals at month end | When `time%end_mo == 1`, add the monthly totals in `withdr_m` into the yearly accumulator `withdr_y` for every source. |
| 6. Write monthly records when month-end output is enabled | If monthly output is active, write the monthly record to unit 3212 and optionally the CSV version to unit 3213. |
| 7. Clear monthly withdrawals after month-end reporting | Zero `withdr_m` so the next month starts a fresh accumulation for each source. |
| 8. Roll yearly totals into average-annual totals at year end | When `time%end_yr == 1`, add the yearly totals in `withdr_y` into the average-annual accumulator `withdr_a` for every source. |
| 9. Write yearly records when year-end output is enabled | If yearly output is active, write the yearly record to unit 3214 and, when CSV output is enabled, write the CSV version to unit 3215. |
| 10. Clear yearly withdrawals after yearly reporting | Zero `withdr_y` so the next year starts with a clean yearly accumulation. |
| 11. Convert annual totals to average-annual values at simulation end | When the simulation ends, divide each source's accumulated `withdr_a` by `time%yrs_prt` to produce the average annual withdrawal value. |
| 12. Write average-annual records when simulation-end output is enabled | If average-annual output is active, write the final average-annual record to unit 3216 and, when CSV output is enabled, write the CSV version to unit 3217. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `pco` | `pco%water_allo%d, pco%water_allo%m, pco%water_allo%y, pco%water_allo%a, pco%csvout` |
| [sym:manure_allocation_module] | `mallo` | `mallo(imallo)%trn_obs, mallo(imallo)%src_obs, mallo(imallo)%trn(itrn)%withdr_m(isrc), mallo(imallo)%trn(itrn)%withdr(isrc), mallo(imallo)%trn(itrn)%ob_typ, mallo(imallo)%trn(itrn)%ob_num, mallo(imallo)%src(isrc)%num, mallo(imallo)%src(isrc)%mois_typ, mallo(imallo)%src(isrc)%manure_typ, mallo(imallo)%trn(itrn)%withdr_y(isrc), mallo(imallo)%trn(itrn)%withdr_a(isrc)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mallo(imallo)%trn(itrn)%withdr_m(isrc)` | During the per-source accumulation loop for every demand object, before the daily withdrawal is reset. | `withdr_m` is incremented by the current day's `withdr` so the routine preserves a monthly running total of daily withdrawals for each source. It is then available for the month-end report and for rolling into yearly totals. |
| `mallo(imallo)%trn(itrn)%withdr(isrc)` | Immediately after daily output is written for the current demand object. | `withdr` is reset to zero so the next day can accumulate new withdrawals without carrying over the previous day's values. This makes the field strictly a daily quantity. |
| `mallo(imallo)%trn(itrn)%withdr_y(isrc)` | At month end when `time%end_mo == 1`. | `withdr_y` accumulates the completed monthly total from `withdr_m`, creating the year-to-date withdrawal total for each source. |
| `mallo(imallo)%trn(itrn)%withdr_a(isrc)` | At simulation end when `time%end_sim == 1`. | `withdr_a` is divided by `time%yrs_prt` to convert the accumulated annual total into an average annual value across the printed simulation period. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior changes. The routine was introduced in df07e3f as a new manure allocation output subroutine using `idmd` and the `dmd` demand arrays. In 914f365 those demand references were renamed from `dmd`/`idmd` to `trn`/`itrn`, and the loops and write statements were updated to use the new names. In 2fe89fd the CSV write format on units 3211, 3213, 3215, and 3217 was changed from `G0.3` to `G0.6`, increasing numeric output precision.

- df07e3f created the subroutine with daily, monthly, yearly, and average-annual manure demand output using the original `dmd` demand-object naming.
- 914f365 renamed the demand-object naming in this routine from `dmd`/`idmd` to `trn`/`itrn` and updated the associated loops, accumulations, and writes to the new manure allocation structure.
- 2fe89fd changed the CSV output format for the manure demand files on units 3211, 3213, 3215, and 3217 from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'manure_demand_output' has no extracted documentation comment.
- hydrograph_module usage appears to be through `pco`; no direct component references were extracted from the source lines, so `outside_state[1]` is based on candidate references and the visible write conditions.
