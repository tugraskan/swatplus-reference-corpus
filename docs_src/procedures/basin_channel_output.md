---
kind: procedure
symbol: basin_channel_output
title: basin_channel_output
status: filled
source_hash: 913e0749ab9e307b
version_label: SWAT+ 62.0.0
locals:
  ich: Loop counter that walks through each channel object from 1 to `sp_ob%chan` so the routine
    can accumulate every channel's daily output into the basin total and then clear the per-channel
    daily slot.
uses:
  time_module: The `time` state tells the routine what kind of reporting boundary it is on.
    `time%day`, `time%mo`, `time%day_mo`, and `time%yrc` are written into every record, while
    `time%end_mo`, `time%end_yr`, `time%end_sim`, and `time%yrs_prt` decide when monthly,
    yearly, and average-annual basin channel totals should be finalized and written.
  basin_module: The basin print-control state determines whether this routine writes anything
    and in what format. `pco%day_print` and `pco%int_day_cur` gate daily output timing, `pco%chan_bsn%d`,
    `%m`, `%y`, and `%a` enable the daily, monthly, yearly, and average-annual basin channel
    reports, `pco%csvout` adds the CSV companion records, and `bsn%name` identifies the basin
    in each output row.
  channel_module: The channel output structures hold the actual values being summarized. `ch_d`
    stores each channel's current daily output, `bch_d` through `bch_a` store the basin-level
    daily, monthly, yearly, and average-annual summaries, and `chz` is the zeroed/reset value
    used to clear a channel or summary accumulator after it has been rolled up.
  hydrograph_module: The spatial object count provides the channel population size. `sp_ob%chan`
    is the upper bound for the loop over `ch_d(ich)`, so it controls how many channel outputs
    are included in the basin daily total.
---

<!-- facts:header -->

Aggregates channel output for the basin and writes it at daily, monthly, yearly, and average-annual intervals. It resets the channel-level daily totals after summing them into basin totals.

## Bottom Line

basin_channel_output collects per-channel output from `ch_d(ich)` across all channel objects, stores the basin-wide daily sum in `bch_d`, and then rolls that daily sum into monthly, yearly, and average-annual basin channel totals.

It only writes records when the relevant print flags are enabled in `pco` and the time state says the current day, month, year, or simulation end has been reached. The routine's output is what produces the basin channel summary files for standard text output and optional CSV output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after basin and channel simulation state has been updated for the current time step and after channel objects exist in `sp_ob%chan`. Its outputs feed the basin channel summary files used for daily, monthly, yearly, and simulation-average reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the basin daily channel accumulator | Set `ich` to its local counter role, then start the basin daily total by copying the zero channel template `chz` into `bch_d`. |
| 2. Sum all channel daily output into the basin total | Loop from channel 1 through `sp_ob%chan`, add each channel's daily output `ch_d(ich)` into `bch_d`, and immediately reset that channel slot back to `chz` so the daily value is cleared after roll-up. |
| 3. Accumulate the basin daily total into the monthly total | Add the newly computed basin daily total to `bch_m` so the month-to-date accumulator includes the current day. |
| 4. Write daily basin channel output when daily printing is due | If daily printing is enabled and the current day matches the print interval, write the daily basin channel record to unit 2110 and, when CSV output is enabled, also write the CSV version to unit 2114. |
| 5. Finalize the month and write monthly basin channel output | At end of month, add the monthly accumulator `bch_m` into the yearly accumulator `bch_y`, write the monthly basin record to unit 2111 and optional CSV unit 2115 when monthly output is enabled, then reset `bch_m` to `chz` for the next month. |
| 6. Finalize the year and write yearly basin channel output | At end of year, add the yearly accumulator `bch_y` into the average-annual accumulator `bch_a`, write the yearly basin record to unit 2112 and optional CSV unit 2116 when yearly output is enabled, then reset `bch_y` to `chz`. |
| 7. Compute and write average-annual basin channel output | At simulation end, if average-annual basin channel output is enabled, divide `bch_a` by `time%yrs_prt` to form the mean annual value, then write the final record to unit 2113 and optional CSV unit 2117. |
| 8. Return to caller | Use the shared format statement for the fixed-width report layout, then return from the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%chan_bsn%d, bsn%name, pco%csvout, pco%chan_bsn%m, pco%chan_bsn%y, pco%chan_bsn%a` |
| [sym:channel_module] | `ch_d, bch_d, chz, bch_m, bch_y, bch_a` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%chan` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bch_d` | When the routine starts, before any channel accumulation. | `bch_d` is initialized from `chz` and then rebuilt as the basin-wide sum of all channel daily outputs for the current time step. |
| `ch_d(ich)` | During the loop over `ich = 1, sp_ob%chan`. | Each `ch_d(ich)` is added into `bch_d` and then reset to `chz`, so the per-channel daily output is consumed once and cleared after basin roll-up. |
| `bch_m` | After `bch_d` has been formed, every day. | `bch_m` accumulates the basin daily totals across the month; it is incremented by `bch_d` and later reset to `chz` at month end after being written. |
| `bch_y` | At `time%end_yr == 1`. | `bch_y` accumulates the month totals into a yearly total; it is incremented by `bch_m` at each month end and reset to `chz` after yearly output is written. |
| `bch_a` | At `time%end_sim == 1` and when average-annual basin channel output is enabled. | `bch_a` is converted from an accumulated multi-year total into an average annual value by dividing by `time%yrs_prt` before the final simulation-end record is written. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three changes to `basin_channel_output`: the procedure was added in `df07e3f`, the temporary counter `ich` was initialized in `39fabde`, and `2fe89fd` raised the CSV output format from `G0.3` to `G0.6` on all four CSV write statements.

- df07e3f created the routine with daily, monthly, yearly, and average-annual basin channel rollups and writes.
- 39fabde changed the local counter declaration to `integer :: ich = 0`; no behavioral logic changed in the diff beyond the initializer.
- 2fe89fd changed the CSV writes on units 2114, 2115, 2116, and 2117 from `G0.3` to `G0.6`, increasing CSV numeric precision.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_channel_output' has no extracted documentation comment.
