---
kind: procedure
symbol: basin_chanbud_output
title: basin_chanbud_output
status: filled
source_hash: de152ca93a78051d
version_label: SWAT+ 62.0.0
uses:
  time_module: 'The time state tells this routine which reporting boundary has been reached:
    daily print timing, end-of-month, end-of-year, and end-of-simulation all gate the different
    output branches. The same time fields also supply the date stamp written into each record
    and the years-per-print divisor used for average annual output.'
  basin_module: The basin print-control state decides whether basin channel sediment budget
    output is enabled for each period and whether CSV duplicates should be emitted. The basin
    name is also written into each record so the output can be tied back to the basin being
    simulated.
  sd_channel_module: These sediment budget objects hold the per-channel source values and
    the basin-level accumulators that this routine reads, updates, writes out, and resets.
    Without this module's state, the routine would have no place to collect the daily sum
    or preserve the monthly, yearly, and average-annual totals.
  hydrograph_module: The spatial object count provides the number of SWAT-deg channel elements
    to traverse in the summation loop. The loop index `ich` is the channel object selector
    used to pull each channel's sediment budget into the basin total.
---

<!-- facts:header -->

Aggregates and outputs sediment budget totals for SWAT+ channel-deg basin reporting. It writes daily, monthly, yearly, and average-annual sediment budget records, with optional CSV copies.

## Bottom Line

basin_chanbud_output accumulates channel sediment budget output from all SWAT-deg channel objects into basin-level daily, monthly, yearly, and average-annual totals. It then writes those totals to the configured output units when the matching print flags and time boundaries are active.

The routine also resets the per-channel budget entries back to the zero-state object after they are summed, so each channel contribution is only counted once per reporting period. Its results feed the basin sediment budget files used by the model's reporting workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after channel-deg objects exist and the basin print controls and time flags have been prepared. It depends on upstream routing/output accumulation having already populated `ch_sed_bud`, `ch_sed_budz`, and the basin print settings, and its written totals support the sediment budget reporting files for daily, monthly, yearly, and average-annual model output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the daily basin total from the zero-state channel budget. | The routine starts the daily basin sediment budget with `ch_sed_budz`, the zero/reset channel budget object that represents the current channel-state baseline before summing all SWAT-deg channels. |
| 2. Sum all SWAT-deg channel budgets into the basin daily total and reset each channel entry. | It loops `ich` from 1 to `sp_ob%chandeg`, adds each `ch_sed_bud(ich)` into `bch_sed_bud_d`, and then resets that channel's entry back to `ch_sed_budz` so the same channel contribution is not counted again in the next reporting cycle. |
| 3. Accumulate the daily total into the monthly basin total. | After the channel loop, the routine adds the daily basin total to `bch_sed_bud_m`, building the monthly running sum. |
| 4. Write daily basin sediment output when day-print timing and daily channel print codes are enabled. | When `pco%day_print` is active and the current day matches the daily print interval, the routine writes the daily basin sediment budget to unit 2128 and, if CSV output is enabled, to unit 2132. |
| 5. Roll monthly totals into the yearly accumulator at month end, write monthly output if enabled, and reset the monthly accumulator. | At `time%end_mo == 1`, the routine adds `bch_sed_bud_m` into `bch_sed_bud_y`, writes monthly output to unit 2129 and optional CSV unit 2133 when monthly printing is enabled, and then resets `bch_sed_bud_m` to `ch_sed_budz` for the next month. |
| 6. Roll yearly totals into the average-annual accumulator, write yearly output if enabled, and reset the yearly accumulator. | At `time%end_yr == 1`, the routine adds `bch_sed_bud_y` into `bch_sed_bud_a`, writes yearly output to unit 2130 and optional CSV unit 2134 when yearly printing is enabled, and then resets `bch_sed_bud_y` to `ch_sed_budz`. |
| 7. Compute and write the average-annual basin sediment budget at the end of simulation. | When the simulation ends and average-annual printing is enabled, the routine divides `bch_sed_bud_a` by `time%yrs_prt` and writes the resulting average-annual record to unit 2131 and optional CSV unit 2135. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%sd_chan_bsn%d, bsn%name, pco%csvout, pco%sd_chan_bsn%m, pco%sd_chan_bsn%y, pco%sd_chan_bsn%a` |
| [sym:sd_channel_module] | `ch_sed_bud, bch_sed_bud_d, ch_sed_budz, bch_sed_bud_m, bch_sed_bud_y, bch_sed_bud_a` |  |
| [sym:hydrograph_module] | `sp_ob, ich` | `sp_ob%chandeg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bch_sed_bud_d` | After `bch_sed_bud_d = ch_sed_budz` and during the `do ich = 1, sp_ob%chandeg` summation loop. | `bch_sed_bud_d` is rebuilt each call as the basin-wide daily channel sediment budget: it starts from the reset baseline, accumulates every `ch_sed_bud(ich)` contribution, and becomes the value written to daily output. |
| `ch_sed_bud(ich)` | Inside the `do ich = 1, sp_ob%chandeg` loop for each channel object. | `ch_sed_bud(ich)` is cleared back to `ch_sed_budz` after its contribution has been added into the basin daily total, so the channel's sediment budget is consumed for this reporting pass and ready for the next cycle. |
| `bch_sed_bud_m` | At routine entry and again after the monthly print branch when `time%end_mo == 1`. | `bch_sed_bud_m` is increased by the daily basin total during the call, then reset to `ch_sed_budz` at month end after its value has been written and rolled into the yearly accumulator. |
| `bch_sed_bud_y` | At month-end and again after the yearly print branch when `time%end_yr == 1`. | `bch_sed_bud_y` accumulates the completed monthly total into the year-to-date sum, then is reset to `ch_sed_budz` after yearly output so the next year starts clean. |
| `bch_sed_bud_a` | At year-end and before average-annual output at `time%end_sim == 1`. | `bch_sed_bud_a` collects yearly totals across the simulation and is then divided by `time%yrs_prt` at the end of the run to form the average-annual basin sediment budget that gets written out. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `basin_chanbud_output`: the file was added in fde5d7c, 39fabde initialized `const` to 0. before it was later removed, e08326e removed a blank line and left the monthly-to-yearly update in place, and 2fe89fd changed the CSV write formats from `G0.3` to `G0.6` for daily, monthly, yearly, and average-annual CSV output.

- fde5d7c added the subroutine with daily, monthly, yearly, and average-annual basin channel sediment budget accumulation and output.
- 39fabde changed the local `const` declaration to initialize it to 0., but did not change the active output logic because `const` is otherwise unused in the shown source.
- e08326e made only a formatting cleanup in this routine by removing a blank line before the yearly reset assignment; the sediment accounting logic stayed the same.
- 2fe89fd updated all CSV writes for this routine to use `G0.6` formatting instead of `G0.3`, improving numeric output precision without changing which records are written.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_chanbud_output' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into seven source-faithful steps aligned with the visible control flow.
- Source shows no outgoing calls from this routine.
- The local variable `const` appears in lineage history but is unused in the current source span.
