---
kind: procedure
symbol: wallo_treat_output
title: wallo_treat_output
status: filled
source_hash: b700894d0df7b778
version_label: SWAT+ 62.0.0
args:
  iwallo: Selects which water-allocation database item the caller is processing; the routine
    itself does not branch on `iwallo` for its loop bounds, but it is the object index passed
    in from `command` and identifies the treatment group being reported.
locals:
  itrt: Loop index for each water-treatment object being reported; it steps through the treatment
    objects and indexes the `wal_tr_*` arrays and `om_treat_name` entries.
uses:
  time_module: The `time` fields determine which summary period is ending and provide the
    date fields written to each output record, so they control both record content and when
    monthly, yearly, and simulation-end accumulators are rolled up or reset.
  hydrograph_module: The `wal_tr_omd`, `wal_tr_omm`, `wal_tr_omy`, and `wal_tr_oma` arrays
    hold the treatment-output totals that this routine writes and updates, and `hz` supplies
    the zeroed hydrologic value used to reset the running period totals.
  water_allocation_module: The treatment-name array supplies the human-readable label written
    alongside each treatment object so the output files can be tied back to a specific water-allocation
    treatment.
  maximum_data_module: The `db_mx%wtp` limit sets how many treatment objects exist, so it
    controls the upper bound of the reporting loop.
---

<!-- facts:header -->

Writes water-treatment output records for each treatment object, reporting daily, monthly, yearly, and average-annual treated-water amounts.

## Bottom Line

`wallo_treat_output` loops over every water-treatment object and writes the current treated-water totals to the water-allocation output streams. It is the reporting step for treatment outputs, not the place where the treatment amounts are computed.

The routine emits separate records for daily, monthly, yearly, and average-annual summaries when the corresponding water-allocation print flags are enabled. It also resets or accumulates the `wal_tr_*` summary states at each time boundary so later periods can report the correct totals.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the water-allocation output phase after `command` has established that output should be printed for the current simulation year and is iterating through `db_mx%wallo_db`. Its results feed the treatment output files that downstream users use to inspect daily, monthly, yearly, and average-annual water-treatment behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over treatment objects | Iterate from the first treatment object through `db_mx%wtp`, so every water-treatment entry gets its outputs handled in turn. |
| 2. Write daily treatment output when enabled | If daily water-allocation printing is enabled, write the current date, treatment index, treatment name, and daily treated-water amount to the daily output units, including CSV output when requested. |
| 3. Reset the daily accumulator | After the daily record is handled, reset `wal_tr_omd(itrt)` to `hz` so the next accumulation period starts from zero. |
| 4. Roll monthly totals at month end and write monthly output when enabled | When the month ends, add the monthly amount into the yearly accumulator, write the monthly record if monthly printing is enabled, and then reset the monthly accumulator to `hz`. |
| 5. Roll yearly totals at year end and write yearly output when enabled | When the year ends, add the yearly total into the average-annual accumulator, write the yearly record if yearly printing is enabled, and then reset the yearly accumulator to `hz`. |
| 6. Finalize average-annual output at simulation end | At the end of the simulation, divide the accumulated annual total by `time%yrs_prt`, then write the average-annual record when enabled, including CSV output when requested. |
| 7. Finish the treatment-object loop and return | Close out the loop, return to the caller, and leave the format statement available for the printed output layout. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `wal_tr_omd, wal_tr_omy, wal_tr_omm, wal_tr_oma, hz` |  |
| [sym:water_allocation_module] | `om_treat_name` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wtp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wal_tr_omd(itrt)` | At every daily reporting pass, after the daily output is written. | `wal_tr_omd(itrt)` is cleared to `hz` so the next day's treated-water accumulation starts fresh after the daily value has been reported. |
| `wal_tr_omy(itrt)` | At month end when `time%end_mo == 1`, after the monthly total has been folded into the yearly accumulator. | `wal_tr_omy(itrt)` is cleared to `hz` so the next month's treated-water accumulation starts fresh after its value has been rolled into the year total. |
| `wal_tr_omm(itrt)` | At month end when `time%end_mo == 1`, before the next month begins. | `wal_tr_omm(itrt)` is cleared to `hz` so the monthly treated-water total restarts for the next month after the month-end report. |
| `wal_tr_oma(itrt)` | At year end when `time%end_yr == 1`, after the yearly total has been folded into the average-annual accumulator. | `wal_tr_oma(itrt)` is accumulated across years and then converted to an average at simulation end; it represents the long-term treatment total that is finalized when `time%end_sim == 1`. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `wallo_treat_output`. The newer commit `2fe89fd` updated the CSV output format specifier from `G0.3` to `G0.6` on all four CSV write statements. The earlier commit `080211e` added `maximum_data_module` to the uses list and changed the loop bound from `wallo(iwallo)%wtp` to `db_mx%wtp`.

- 2fe89fd: widened CSV numeric formatting on units 3114, 3115, 3116, and 3117 from `G0.3` to `G0.6`, improving precision in exported treatment summaries.
- 080211e: switched the treatment loop bound to `db_mx%wtp` and introduced `maximum_data_module`, so the routine now iterates over the database-wide treatment count rather than the caller-specific `wallo(iwallo)%wtp` value.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wallo_treat_output' has no extracted documentation comment.
