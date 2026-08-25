---
kind: procedure
symbol: basin_recall_output
title: basin_recall_output
status: filled
source_hash: 78385b8d9a5d14e0
version_label: SWAT+ 62.0.0
locals:
  irec: Loop counter used to walk through the active recall-object array `rec_d(1:sp_ob%recall)`
    and add each object’s contribution into `brec_d`.
uses:
  time_module: This routine uses the current simulation date and end-of-period flags from
    `time` to decide when to write daily, monthly, yearly, and average-annual recall outputs,
    and it uses `time%yrs_prt` to compute the final average annual value.
  basin_module: This module holds the basin print-control flags and basin name that gate the
    output and label every record. `pco%day_print`, `pco%int_day_cur`, and `pco%int_day` control
    daily output timing, `pco%recall_bsn%d/%m/%y/%a` select which basin recall periods are
    printed, `pco%csvout` enables the CSV companion files, and `bsn%name` is written with
    each record.
  hydrograph_module: This module provides the recall hydrograph containers that are summed
    and written. `sp_ob%recall` sets the number of active recall objects to accumulate, `rec_d`
    supplies each object’s contribution, `hz` is the base hydrograph value, and `brec_d`,
    `brec_m`, `brec_y`, and `brec_a` are the basin-level accumulators updated and output by
    this routine.
---

<!-- facts:header -->

Writes basin recall outputs at daily, monthly, yearly, and average-annual intervals. It assembles basin recall hydrograph values from the active recall objects and sends them to the configured output units.

## Bottom Line

basin_recall_output builds a basin-level recall output record each time it runs. It starts from the base basin hydrograph state in `hz`, adds every active recall object in `rec_d`, and then reports that total as the daily basin recall value `brec_d`.

It also accumulates longer-period summaries: `brec_m` is rolled up into `brec_y` at month end, `brec_y` is rolled up into `brec_a` at year end, and the average annual value is computed at simulation end using `time%yrs_prt`. Which records are written depends on `pco%day_print`, `pco%recall_bsn%{d,m,y,a}`, and `pco%csvout`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after basin-scale output work is enabled and after the recall-object arrays and basin print codes have already been initialized. It is part of the model’s output phase: it gathers recall hydrograph contributions for the current time step, writes any requested basin recall files, and leaves behind the period accumulators that later month-end, year-end, and simulation-end output decisions depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the daily basin recall total | Set `brec_d` to the base hydrograph value `hz` before adding any recall-object contributions. |
| 2. Accumulate active recall-object contributions | Loop from 1 to `sp_ob%recall` and add each `rec_d(irec)` into `brec_d`, producing the current basin daily recall total. |
| 3. Roll the daily total into the monthly accumulator | Add the current `brec_d` value to `brec_m` so the monthly total keeps accumulating across days. |
| 4. Write daily basin recall output when daily printing is active | If daily printing is enabled for the current interval and basin recall daily output is selected, write the daily record to unit 4500 and optionally to the CSV file on unit 4504. |
| 5. Roll the monthly total into the yearly accumulator at month end | When `time%end_mo == 1`, add `brec_m` into `brec_y`, optionally write the monthly record to units 4501 and 4505, and then reset `brec_m` to `hz` for the next month. |
| 6. Roll the yearly total into the average-annual accumulator at year end | When `time%end_yr == 1`, add `brec_y` into `brec_a`, optionally write the yearly record to units 4502 and 4506, and then reset `brec_y` to `hz` for the next year. |
| 7. Compute and write the average-annual basin recall at simulation end | If the simulation has ended and average-annual basin recall output is requested, divide `brec_a` by `time%yrs_prt` and write the average-annual record to units 4503 and 4507. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%recall_bsn%d, bsn%name, pco%csvout, pco%recall_bsn%m, pco%recall_bsn%y, pco%recall_bsn%a` |
| [sym:hydrograph_module] | `sp_ob, rec_d, brec_d, hz, brec_m, brec_y, brec_a` | `sp_ob%recall` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `brec_d` | When `pco%day_print == 'y' .and. pco%int_day_cur == pco%int_day` for the current time step. | At the daily print interval, `brec_d` is used as the basin-day recall result and written out; it is not reset here, so it continues to reflect the current daily sum until the next call. |
| `brec_m` | When `time%end_mo == 1`. | At month end, `brec_m` is rolled into `brec_y` and then reset to `hz`, so the monthly accumulator starts fresh for the next month. |
| `brec_y` | When `time%end_yr == 1`. | At year end, `brec_y` is rolled into `brec_a` and then reset to `hz`, so the yearly accumulator starts fresh for the next year. |
| `brec_a` | When `time%end_sim == 1 .and. pco%recall_bsn%a == 'y'`. | At the end of the simulation, `brec_a` is converted to an average annual value by dividing by `time%yrs_prt` before being written. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was added in commit df07e3f. A later commit, 39fabde, initialized `irec` to 0 without changing the algorithm. Commit 1b4a94c removed the division of `brec_d` by `bsn%area_tot_ha`, changing the daily recall calculation from an area-normalized value to the unnormalized summed value. Commit 2fe89fd changed the CSV formatting field width on units 4504, 4505, 4506, and 4507 from `G0.3` to `G0.6`.

- df07e3f introduced the procedure and its daily, monthly, yearly, and average-annual recall accumulation and output flow.
- 39fabde only initialized the local loop counter `irec`; it did not alter output behavior.
- 1b4a94c changed the daily basin recall calculation by removing division by `bsn%area_tot_ha`, so `brec_d` is now the raw sum of `hz` plus `rec_d` contributions.
- 2fe89fd widened CSV numeric formatting on the recall CSV outputs, improving printed precision without changing the underlying calculations.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_recall_output' has no extracted documentation comment.
