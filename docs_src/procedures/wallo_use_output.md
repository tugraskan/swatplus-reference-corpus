---
kind: procedure
symbol: wallo_use_output
title: wallo_use_output
status: filled
source_hash: 343e5753d670ca84
version_label: SWAT+ 62.0.0
args:
  iwallo: '`iwallo` identifies the water-allocation database object whose use outputs are
    being printed; the routine is called once per allocation object from `command`, but the
    current loop uses `db_mx%uses` to iterate over the stored use entries.'
locals:
  iuse: Loop index for each use entry being reported; it selects the current `wal_use_*` slot
    and the matching `om_use_name(iuse)` label.
uses:
  time_module: '`time_module` provides the current simulation date and end-of-period flags
    that decide when daily, monthly, yearly, and average-annual output records are written,
    and it supplies `time%yrs_prt` for the final average-annual division.'
  hydrograph_module: '`hydrograph_module` holds the per-use accumulation arrays and the reset
    value `hz`; these arrays are both written to the output files and cleared or carried forward
    after each reporting interval.'
  water_allocation_module: '`water_allocation_module` supplies the human-readable use-name
    labels, so each output record can be tied to the correct water-allocation use object.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%uses`, which sets how many use
    entries are processed in the loop; without it the routine would not know how many outputs
    to emit.'
---

<!-- facts:header -->

Writes water-allocation use summary outputs for each use object at daily, monthly, yearly, and average-annual checkpoints.

## Bottom Line

`wallo_use_output` loops over the defined water-allocation use objects and writes their use totals to the standard report units and optional CSV files. It records daily use, monthly accumulated use, yearly accumulated use, and average annual use, depending on the corresponding `pco%water_allo` flags and simulation end conditions.

The routine also resets the period accumulators after each report is written so the next reporting window starts fresh. Those outputs are the bookkeeping products later used in the water-allocation reporting workflow, and the routine is called from `command` during the model's output-printing phase.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine during the main output-printing phase after the model has advanced far enough that `time%yrs > pco%nyskip`. It runs once for each water-allocation output object (`iwro` in `command`), and its results feed the water-allocation report files that summarize use by daily, monthly, yearly, and average-annual periods.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over use entries | Iterate through every use entry using `iuse = 1, db_mx%uses` so the routine can process each water-allocation use object in turn. |
| 2. Write daily use output when enabled | If `pco%water_allo%d` is enabled, write the daily report record to unit 3110 and, when `pco%csvout` is enabled, also write the CSV row to unit 3114 using the current date, use name, and `wal_use_omd(iuse)`. |
| 3. Reset daily accumulator | After the daily branch, clear `wal_use_omd(iuse)` by assigning `hz` so the next daily accumulation starts from zero. |
| 4. On month end, fold monthly use into yearly total | When `time%end_mo == 1`, add the monthly total `wal_use_omm(iuse)` into `wal_use_omy(iuse)` so the year-to-date total includes the just-finished month. |
| 5. Write monthly output when enabled | If monthly printing is enabled through `pco%water_allo%m`, write the monthly report record to unit 3111 and, if CSV output is on, write the CSV record to unit 3115 using `wal_use_omm(iuse)`. |
| 6. Reset monthly accumulator | Clear `wal_use_omm(iuse)` by setting it to `hz` after the month-end reporting work is finished. |
| 7. On year end, fold yearly use into simulation total | When `time%end_yr == 1`, add the year-to-date total `wal_use_omy(iuse)` into `wal_use_oma(iuse)` so the simulation-wide accumulator includes the finished year. |
| 8. Write yearly output when enabled | If yearly printing is enabled through `pco%water_allo%y`, write the yearly report record to unit 3112 and, when CSV output is enabled, also write the CSV row to unit 3116 using `wal_use_omy(iuse)`. |
| 9. Reset yearly accumulator | Clear `wal_use_omy(iuse)` by assigning `hz` so the next year starts from zero. |
| 10. At simulation end, compute average annual use | When `time%end_sim == 1`, divide `wal_use_oma(iuse)` by `time%yrs_prt` to convert the accumulated simulation total into an average annual value. |
| 11. Write average-annual output when enabled | If average-annual printing is enabled through `pco%water_allo%a`, write the final report record to unit 3113 and, when CSV output is enabled, also write the CSV record to unit 3117 using `wal_use_oma(iuse)`. |
| 12. Finish the loop and return | End the `iuse` loop, return to the caller, and leave the routine after all selected output records have been written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `wal_use_omd, wal_use_omy, wal_use_omm, wal_use_oma, hz` |  |
| [sym:water_allocation_module] | `om_use_name` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%uses` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wal_use_omd(iuse)` | After the daily report branch, for every `iuse` on each call. | `wal_use_omd(iuse)` is cleared to `hz` after its daily value is written so the next daily accumulation starts fresh. |
| `wal_use_omy(iuse)` | At `time%end_mo == 1`, after the month-end monthly report path. | `wal_use_omy(iuse)` is incremented by `wal_use_omm(iuse)` to carry the finished month's use into the yearly running total, then `wal_use_omm(iuse)` is reset to `hz`. |
| `wal_use_omm(iuse)` | At `time%end_yr == 1`, after the year-end yearly report path. | `wal_use_omm(iuse)` is the monthly accumulator used in the yearly rollup; the routine clears it to `hz` after the year-end bookkeeping so the next monthly cycle starts from zero. |
| `wal_use_oma(iuse)` | At `time%end_sim == 1`, after the final simulation report path. | `wal_use_oma(iuse)` is converted from a simulation-total accumulator to an average annual value by dividing by `time%yrs_prt`. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `wallo_use_output`: `d70017a` added the routine and established the output loops and record-writing structure, and `080211e` changed the loop bound from `wallo(iwallo)%uses` to `db_mx%uses` and added `maximum_data_module`. `2fe89fd` did not change behavior, only widened the CSV numeric format from `G0.3` to `G0.6` on the CSV output lines.

- Introduced `wallo_use_output` as a new water-allocation reporting subroutine that writes daily, monthly, yearly, and average-annual use summaries and resets the accumulators after each period.
- Expanded the loop bound to `db_mx%uses` and imported `maximum_data_module`, so the routine now iterates over the database-wide use count instead of the caller-specific `wallo(iwallo)%uses`.
- Changed only CSV formatting precision from `G0.3` to `G0.6` on the CSV output units 3114, 3115, 3116, and 3117; the underlying calculations and control flow were unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wallo_use_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the routine into detailed period-based steps and kept source_lines aligned to the provided numbered source block.
- Source shows `iwallo` is currently unused inside the routine; the loop uses `db_mx%uses` instead, so the argument's intended control role is uncertain from this snippet alone.
