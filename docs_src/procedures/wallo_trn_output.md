---
kind: procedure
symbol: wallo_trn_output
title: wallo_trn_output
status: filled
source_hash: 49dd85ef317ada4d
version_label: SWAT+ 62.0.0
args:
  iwallo: '`iwallo` selects which water-allocation object in `wallo` is processed; the routine
    uses it to index the transfer list, source list, and matching hydrograph accumulators
    for that allocation object.'
locals:
  itrn: '`itrn` is the transfer-object loop index. It starts at 0 and advances from 1 to `wallo(iwallo)%trn_obs`
    to visit each transfer within the selected water-allocation object.'
  isrc: '`isrc` is the source-object loop index. It starts at 0 and is reused to step through
    each source in the current transfer, both when accumulating values and when writing output
    records.'
uses:
  time_module: '`time_module` supplies the simulation clock and period flags that determine
    when each report is written: daily fields (`time%day`, `time%mo`, `time%day_mo`, `time%yrc`)
    are emitted on every daily print, while `time%end_mo`, `time%end_yr`, `time%end_sim`,
    and `time%yrs_prt` control monthly, yearly, and average-annual reporting and scaling.'
  hydrograph_module: '`hydrograph_module` holds the per-source hydrograph outputs that this
    routine updates and writes. The `hd` components in `wal_omm`, `wal_omd`, `wal_omy`, and
    `wal_oma` are the numeric values being accumulated, printed, and then reset between report
    periods.'
  water_allocation_module: '`water_allocation_module` provides the selected allocation object
    and its transfer/source structure, including the number of transfers, number of sources
    per transfer, transfer type, and source identifiers. Those fields define how many records
    are written and what labels each record carries.'
---

<!-- facts:header -->

Writes water-allocation transfer output for one `wallo` object at daily, monthly, yearly, and average-annual reporting points.

## Bottom Line

This subroutine loops over every transfer object in one water-allocation object and prints source-by-source hydrograph output for the current simulation time. It produces separate records for daily, monthly, yearly, and average-annual summaries, with optional CSV-formatted duplicates when `pco%csvout` is enabled.

The routine also rolls accumulated totals forward between reporting periods. After a daily, monthly, or yearly print, it resets the corresponding hydrograph holders to `hz`, and at the end of simulation it converts the average-annual total by dividing by `time%yrs_prt` before writing the final output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the main command-level output phase after the model has advanced time and after water-allocation calculations have populated the `wal_omd`, `wal_omm`, `wal_omy`, and `wal_oma` accumulators. `command` calls it inside the loop over `db_mx%wallo_db`, so later reporting behavior depends on the records it writes and the accumulator resets it performs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over transfer objects | For the selected allocation object, iterate through each transfer object from 1 to `wallo(iwallo)%trn_obs`. |
| 2. Accumulate daily unmet demand into monthly output | For every source in the transfer, add the daily unmet-demand hydrograph value in `wal_omd` into the monthly accumulator `wal_omm`. |
| 3. Write daily records | If daily water-allocation printing is enabled, write the daily report to unit 3110 and, when CSV output is enabled, duplicate it to unit 3114. |
| 4. Reset daily hydrograph holders | After the daily print branch, replace each daily unmet-demand source hydrograph with `hz` so the next day starts from a clean daily accumulator. |
| 5. On month end, accumulate monthly totals | When `time%end_mo == 1`, add each monthly accumulator value from `wal_omm` into the yearly accumulator `wal_omy`. |
| 6. Write monthly records | If monthly water-allocation printing is enabled, write the monthly report to unit 3111 and, when CSV output is enabled, duplicate it to unit 3115. |
| 7. Reset monthly hydrograph holders | After monthly output, reset each monthly unmet-demand holder in `wal_omm` to `hz` so the next month starts with empty monthly totals. |
| 8. On year end, accumulate yearly totals | When `time%end_yr == 1`, add each yearly accumulator value from `wal_omy` into the average-annual accumulator `wal_oma`. |
| 9. Write yearly records | If yearly water-allocation printing is enabled, write the yearly report to unit 3112 and, when CSV output is enabled, duplicate it to unit 3116. |
| 10. Reset yearly hydrograph holders | After yearly output, reset each yearly unmet-demand holder in `wal_omy` to `hz` so the next year starts with empty yearly totals. |
| 11. On simulation end, compute average annual values | When `time%end_sim == 1`, divide each accumulated average-annual source value in `wal_oma` by `time%yrs_prt`. |
| 12. Write average-annual records | If average-annual water-allocation printing is enabled, write the final summary to unit 3113 and, when CSV output is enabled, duplicate it to unit 3117. |
| 13. Advance to the next transfer | Finish the current transfer loop and continue until every transfer object has been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `wal_omm, wal_omd, wal_omy, wal_oma, hz` | `wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd` |
| [sym:water_allocation_module] | `wallo` | `wallo(iwallo)%trn_obs, wallo(iwallo)%trn(itrn)%src_num, wallo(iwallo)%trn(itrn)%trn_typ, wallo(iwallo)%trn(itrn)%num, wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wal_omm(iwallo)%trn(itrn)%src(isrc)%hd` | During the daily output branch for each source, after the daily record has been written. | The daily unmet-demand source hydrograph in `wal_omm` is copied into the daily report and then later cleared back to `hz` through `wal_omd`; this prepares the daily accumulator for the next day. |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` | During the daily output branch for each source, immediately after the daily report is written. | The daily hydrograph holder in `wal_omd` is reset to `hz` so the next day starts with a clean daily value rather than carrying the previous day's output forward. |
| `wal_omy(iwallo)%trn(itrn)%src(isrc)%hd` | At month end when `time%end_mo == 1`, after the monthly report is written. | The monthly hydrograph holder in `wal_omy` is reset to `hz` so the next month can accumulate a fresh monthly total after the yearly accumulator has been updated. |
| `wal_oma(iwallo)%trn(itrn)%src(isrc)%hd` | At simulation end when `time%end_sim == 1`, after the average-annual values are divided by `time%yrs_prt`. | The average-annual hydrograph holder in `wal_oma` is converted from a summed total into a per-year average for the final report; this value is not reset here because it is the end-of-simulation summary. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. Commit d70017a added `wallo_trn_output.f90` with the current transfer-output loops, accumulator updates, and writes to units 3110/3111/3112/3113 plus CSV duplicates. Commit 2fe89fd did not change the routine's behavior, but updated the CSV format descriptors on units 3114/3115/3116/3117 from `G0.3` to `G0.6`.

- d70017a introduced the routine and its daily, monthly, yearly, and average-annual water-allocation output flow, including the resets of `wal_omd`, `wal_omm`, `wal_omy`, and the final scaling of `wal_oma` by `time%yrs_prt`.
- 2fe89fd changed only the CSV output formatting precision on units 3114, 3115, 3116, and 3117; it did not alter which values are written or when the routine runs.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wallo_trn_output' has no extracted documentation comment.
