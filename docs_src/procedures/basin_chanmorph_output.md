---
kind: procedure
symbol: basin_chanmorph_output
title: basin_chanmorph_output
status: filled
source_hash: 2572f58a58cd91aa
version_label: SWAT+ 62.0.0
locals:
  const: Scratch scalar used to hold the number of days in the current month or the number
    of days in the year-end averaging period before converting accumulated totals into period
    averages. It is initialized to 0. and then assigned only inside the monthly and yearly
    branches.
uses:
  time_module: The routine keys all reporting decisions off the current simulation date and
    end-of-period flags from `time`. It needs `time%day`, `time%mo`, `time%day_mo`, and `time%yrc`
    to label each record, and it uses `time%end_mo`, `time%end_yr`, `time%end_sim`, `time%day_end_yr`,
    `time%yrs_prt`, and `time%days_prt` to decide when monthly, yearly, and average-annual
    basin summaries should be finalized and normalized.
  basin_module: The basin print-code settings control whether any record is written for the
    current day and which summary intervals are enabled for the basin channel-morphology outputs.
    `bsn%name` is the basin label written into every record, and `pco%csvout` selects the
    companion CSV writes on units 2124, 2125, 2126, and 2127.
  sd_channel_module: These channel-output accumulators are the state being rolled up and reset
    here. `chsd_d` provides the per-channel daily contributions, `bchsd_d`, `bchsd_m`, `bchsd_y`,
    and `bchsd_a` store the basin-level daily, monthly, yearly, and average-annual summaries,
    and `chsdz` is the zeroed template assigned back after a period has been accumulated.
  hydrograph_module: The loop bound `sp_ob%chandeg` tells the routine how many SWAT-deg channel
    objects contribute to the basin total, and `ich` is the loop index used to visit each
    one. Without `hydrograph_module`, the routine would not know how many `chsd_d(ich)` entries
    to sum or reset.
---

<!-- facts:header -->

Aggregates SWAT+ channel-morphology outputs for the basin and writes them at daily, monthly, yearly, and average-annual intervals. It also emits CSV-formatted copies when configured.

## Bottom Line

This routine rolls up subbasin channel-morphology output from all SWAT-deg channels into basin totals, then writes those totals to the basin channel-morphology output files. It handles daily, monthly, yearly, and end-of-simulation average-annual reporting using the current simulation time and print-code flags.

The routine matters because it resets the channel-level daily accumulators after they are summed, preserves running monthly and yearly totals, and sends the finished summary records to the standard and CSV output units. Downstream reporting depends on these basin-level summaries rather than the individual channel object accumulators.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after SWAT+ has advanced the simulation time and populated the channel-morphology accumulators for the current step. Its outputs feed the basin-level channel-morphology report files, so later reporting depends on the totals and resets performed here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the basin daily total from the zero template. | Set `const` to 0. and copy `chsdz` into `bchsd_d` so the daily basin total starts from the zeroed output structure. |
| 2. Sum all SWAT-deg channel daily outputs into the basin total and clear each channel accumulator. | Loop over `ich = 1, sp_ob%chandeg`, add each `chsd_d(ich)` into `bchsd_d`, and reset each channel entry back to `chsdz` after it has been included. |
| 3. Add the daily basin total into the running monthly accumulator. | Accumulate the current day into `bchsd_m` so month-end reporting can use all daily contributions since the last reset. |
| 4. Write the daily basin summary when daily printing is enabled for the current day. | If `pco%day_print` is enabled and the daily interval counter matches `pco%int_day`, then, when `pco%sd_chan_bsn%d` is enabled, write the daily record to unit 2120 and optionally write the CSV record to unit 2124. |
| 5. At month end, roll the monthly accumulator into the yearly total and convert the monthly total to an average per day. | When `time%end_mo == 1`, add `bchsd_m` into `bchsd_y`, compute the number of days in the month from `ndays(time%mo + 1) - ndays(time%mo)`, store that in `const`, and divide `bchsd_m` by `const` using the overloaded `//` operator. |
| 6. Write the monthly basin summary when monthly printing is enabled, then reset the monthly accumulator. | If `pco%sd_chan_bsn%m` is enabled, write the monthly record to unit 2121 and optionally to CSV unit 2125, then reset `bchsd_m` back to `chsdz` for the next month. |
| 7. At year end, roll the yearly accumulator into the average-annual total and normalize by year length. | When `time%end_yr == 1`, add `bchsd_y` into `bchsd_a`, assign `time%day_end_yr` to `const`, and divide `bchsd_a` by `const` using `//` so the annual total becomes a daily average over the year. |
| 8. Write the yearly basin summary when yearly printing is enabled, then reset the yearly accumulator. | If `pco%sd_chan_bsn%y` is enabled, write the yearly record to unit 2122 and optionally to CSV unit 2126, then clear `bchsd_y` back to `chsdz`. |
| 9. At the end of the simulation, convert the average-annual total to the final mean and write it. | When `time%end_sim == 1` and `pco%sd_chan_bsn%a == 'y'`, divide `bchsd_a` by `time%yrs_prt`, multiply or adjust it by `time%days_prt` through the overloaded `//` operator, and write the final average-annual record to unit 2123 and optionally to CSV unit 2127. |
| 10. Return to the caller. | The format statement remains available for the earlier writes, then the subroutine exits with `return` and `end subroutine basin_chanmorph_output`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%sd_chan_bsn%d, bsn%name, pco%csvout, pco%sd_chan_bsn%m, pco%sd_chan_bsn%y, pco%sd_chan_bsn%a` |
| [sym:sd_channel_module] | `chsd_d, bchsd_d, chsdz, bchsd_m, bchsd_y, bchsd_a` |  |
| [sym:hydrograph_module] | `sp_ob, ich` | `sp_ob%chandeg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bchsd_d` | After the channel loop has summed all `chsd_d(ich)` values, before any daily write occurs. | `bchsd_d` is rebuilt as the basin-wide daily channel-morphology total and becomes the record written for daily output. It also feeds the monthly accumulator immediately afterward. |
| `chsd_d(ich)` | During `do ich = 1, sp_ob%chandeg` for every channel object. | Each `chsd_d(ich)` entry is cleared back to `chsdz` after its contribution is added to the basin total, so the next time step starts from a zeroed daily channel state. |
| `bchsd_m` | Every call, after `bchsd_d` has been formed; additionally converted and reset at month end. | `bchsd_m` accumulates daily basin totals across the month, is converted to a per-day monthly mean at month end, and is then reset to `chsdz` for the next monthly period. |
| `bchsd_y` | When `time%end_yr == 1`. | `bchsd_y` collects monthly totals across the year and is used as the yearly summary written at year end; after the write, it is reset to `chsdz`. |
| `bchsd_a` | When `time%end_yr == 1` and again when `time%end_sim == 1`. | `bchsd_a` accumulates yearly totals, is normalized to an average using the year-length and simulation-length divisors, and provides the final average-annual basin channel-morphology record. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved three commits that touched this routine. The initial addition in `df07e3f` introduced the subroutine, its module uses, the daily/monthly/yearly/average-annual accumulation logic, and the output writes. Commit `39fabde` initialized `const` to `0.` without changing the algorithm. Commit `2fe89fd` changed the CSV write format on units 2124, 2125, 2126, and 2127 from `G0.3` to `G0.6` while leaving the rest of the routine unchanged.

- df07e3f added the full basin channel-morphology summarization routine, including the channel summation loop, period-end resets, and writes to units 2120/2121/2122/2123 and their CSV companions.
- 39fabde changed only the declaration of `const` to `real :: const = 0.`, making the scratch variable explicitly initialized before monthly and yearly normalization.
- 2fe89fd updated the CSV output formatting on units 2124, 2125, 2126, and 2127 from `G0.3` to `G0.6`, improving numeric precision in the CSV copies.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_chanmorph_output' has no extracted documentation comment.
- algorithm_steps revised: expanded to reflect the actual source branches and the final return statement.
- Source uses overloaded `//` with real-valued accumulators; the exact operator meaning is not defined in the provided packet, so descriptions avoid guessing beyond the visible assignments.
