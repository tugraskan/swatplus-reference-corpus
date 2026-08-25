---
kind: procedure
symbol: sd_chanbud_output
title: sd_chanbud_output
status: filled
source_hash: 0e43c0a9210c9a76
version_label: SWAT+ 62.0.0
args:
  ichan: Selects which swat-deg channel object to report. The routine uses `ichan` to index
    the sediment budget arrays and to map to the corresponding object entry through `sp_ob1%chandeg
    + ichan - 1`.
locals:
  iob: Holds the object index in `ob` for the requested swat-deg channel. It is initialized
    to 0 and then set from `sp_ob1%chandeg + ichan - 1` so the routine can write the correct
    GIS ID and object name.
uses:
  sd_channel_module: This module owns the channel sediment budget accumulators that this routine
    reads, updates, and resets. `ch_sed_bud`, `ch_sed_bud_m`, `ch_sed_bud_y`, `ch_sed_bud_a`,
    and `ch_sed_budz` supply the values written to output and the running totals maintained
    across day, month, year, and simulation-end boundaries.
  basin_module: This module provides the print-control settings that decide whether each output
    block is written. `pco%day_print`, `pco%int_day_cur`, `pco%int_day`, `pco%sd_chan%d`,
    `pco%csvout`, `pco%sd_chan%m`, `pco%sd_chan%y`, and `pco%sd_chan%a` gate the daily, monthly,
    yearly, and average-annual records and the CSV companion files.
  time_module: This module provides the current simulation date and end-of-period markers
    that trigger the monthly, yearly, and final average-annual logic. The routine uses these
    time fields to know which budget accumulator to write and when to roll or finalize it.
  hydrograph_module: This module provides the channel object map used to label the output
    records. `sp_ob1%chandeg` identifies the first swat-deg channel object index, and `ob(iob)%name`
    supplies the object label written alongside the sediment budget values.
---

<!-- facts:header -->

Writes channel sediment budget outputs for one swat-deg channel object. It reports daily, monthly, yearly, and average-annual sediment budget values when the corresponding print flags are enabled.

## Bottom Line

sd_chanbud_output formats and writes sediment budget results for a single swat-deg channel index `ichan`. It uses the current simulation date, the mapped object name/ID, and the channel sediment budget state to produce output records on fixed-numbered files and optional CSV files.

The routine also rolls the current daily budget into the monthly, yearly, and average-annual accumulators and resets the period accumulators after month and year boundaries. That makes it part of the bookkeeping that keeps channel sediment budget totals aligned with the model's print intervals.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the command workflow after channel outputs are being produced for each swat-deg channel, as shown by `command` calling it inside the `do jrch = 1, sp_ob%chandeg` loop. `command` has already established the active object loop and current time state, and the results feed the sediment budget output files used for daily, monthly, yearly, and simulation-average reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the requested channel to its object record | The routine initializes `iob` and converts the swat-deg channel index `ichan` into the corresponding `ob` array index by offsetting from `sp_ob1%chandeg`. |
| 2. Accumulate the current channel budget into the monthly total | The current channel sediment budget `ch_sed_bud(ichan)` is added into `ch_sed_bud_m(ichan)` so the month-to-date total is available for later monthly reporting. |
| 3. Write daily sediment-budget output when the daily print interval is active | If daily printing is enabled for the current interval and channel sediment day output is turned on, the routine writes a daily formatted record to unit 4808 and, when CSV output is enabled, a CSV line to unit 4812. |
| 4. Roll the monthly total into the yearly accumulator at month end | When the model reaches the end of a month, the routine adds the monthly total into `ch_sed_bud_y(ichan)`, writes monthly output if enabled, and then resets `ch_sed_bud_m(ichan)` to `ch_sed_budz` for the next month. |
| 5. Write yearly sediment-budget output at year end | At the end of a year, the routine adds the yearly total into `ch_sed_bud_a(ichan)`, writes yearly output if enabled, and then resets `ch_sed_bud_y(ichan)` to `ch_sed_budz` for the next year. |
| 6. Finalize and write the average-annual sediment budget at simulation end | When the simulation ends, the routine divides `ch_sed_bud_a(ichan)` by `time%yrs_prt` to form the average annual value and writes the average-annual formatted record and optional CSV record if enabled. |
| 7. Return to the caller | The subroutine returns after all eligible output and accumulator updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `ch_sed_bud_m, ch_sed_bud, ch_sed_bud_y, ch_sed_bud_a, ch_sed_budz` |  |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%sd_chan%d, pco%csvout, pco%sd_chan%m, pco%sd_chan%y, pco%sd_chan%a` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%chandeg, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch_sed_bud_m(ichan)` | At every call, before any print-interval checks, the routine adds `ch_sed_bud(ichan)` into `ch_sed_bud_m(ichan)`. | `ch_sed_bud_m(ichan)` becomes the running monthly sum of the current channel sediment budget. It changes every time the routine runs so the monthly total can be written at month end. |
| `ch_sed_bud_y(ichan)` | When `time%end_mo == 1`, the routine adds `ch_sed_bud_m(ichan)` into `ch_sed_bud_y(ichan)` and then resets `ch_sed_bud_m(ichan)` to `ch_sed_budz`. | `ch_sed_bud_y(ichan)` becomes the running yearly sum of completed monthly totals. It changes at each month boundary so the yearly budget keeps accumulating across months. |
| `ch_sed_bud_a(ichan)` | When `time%end_yr == 1`, the routine adds `ch_sed_bud_y(ichan)` into `ch_sed_bud_a(ichan)` and then resets `ch_sed_bud_y(ichan)` to `ch_sed_budz`. | `ch_sed_bud_a(ichan)` becomes the running accumulation used for the final average-annual budget. It changes at each year boundary so the simulation-end average can be formed from the annual totals. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source changes to `sd_chanbud_output`: the file was added in 94b6dec, then 39fabde initialized `iob` and a now-removed `const` local, e08326e changed the monthly/yearly accumulator flow so `ch_sed_bud_y` is updated and `ch_sed_bud_m`/`ch_sed_bud_y` are reset to `ch_sed_budz`, 2ee1889 removed the unused `const`, and 2fe89fd changed all CSV writes from `G0.3` to `G0.6` formatting.

- 94b6dec introduced the subroutine and its day/month/year/average-annual sediment-budget output structure with direct writes to the numbered units.
- 39fabde initialized local variables `iob` and `const`; the later removal of `const` shows it became unused in the final routine shape.
- e08326e changed the monthly and yearly bookkeeping by adding monthly totals into `ch_sed_bud_y`, resetting `ch_sed_bud_m` to `ch_sed_budz`, and resetting `ch_sed_bud_y` to `ch_sed_budz` after the yearly block.
- 2fe89fd increased CSV numeric precision for the daily, monthly, yearly, and average-annual output files by switching the CSV edit descriptor to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sd_chanbud_output' has no extracted documentation comment.
