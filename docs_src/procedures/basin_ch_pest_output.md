---
kind: procedure
symbol: basin_ch_pest_output
title: basin_ch_pest_output
status: filled
source_hash: 26829d02c575f4f3
version_label: SWAT+ 62.0.0
locals:
  ipest: Loop index for `cs_db%num_pests`; selects which pesticide is being summarized and
    written on each pass through the routine.
  iob: Holds the channel-object index used to fetch the basin/channel object name from `ob(iob)%name`;
    it is set from `sp_ob1%chandeg` before output.
  jrch: Loop index over channel-degree objects (`1..sp_ob%chandeg`) used to accumulate the
    pesticide balance from `chpst_d(jrch)%pest(ipest)` into the basin daily total.
  const: Temporary scaling factor used when converting accumulated monthly or yearly totals
    into averages; it is set from the number of days in the month or year before dividing/normalizing
    the period total.
uses:
  output_ls_pesticide_module: This module is used by the routine, but the packet does not
    resolve any specific symbols from it. That means it likely provides output-related definitions
    or shared interfaces that are needed for compilation rather than directly referenced in
    the executable lines shown here.
  ch_pesticide_module: 'The routine reads and updates basin and channel pesticide summary
    objects from `ch_pesticide_module`: `bchpst_d`, `bchpst_m`, `bchpst_y`, and `bchpst_a`
    hold the day/month/year/average-annual accumulators for each pesticide, `chpst_d(jrch)%pest(ipest)`
    supplies the channel-day contributions being summed, and `ch_pestbz` is the zero/baseline
    value used to reset period accumulators after output.'
  plant_module: The module is listed as a dependency, but no specific plant symbols appear
    in the extracted lines. It matters here because the routine is part of the broader landscape/pesticide
    output set and the build depends on these shared module interfaces being available even
    though the shown code does not reference a plant variable directly.
  plant_data_module: 'The module is listed as a dependency, but no specific plant-data symbols
    appear in the extracted lines. It matters here for the same reason as `plant_module`:
    the routine is compiled in the pesticide-output subsystem that shares state and interfaces
    across plant and landscape code paths.'
  time_module: 'The `time` object controls all period boundaries and the timestamp written
    to output: daily printing depends on `time%day`, `time%mo`, `time%day_mo`, and `time%yrc`,
    while monthly, yearly, and end-of-simulation branches depend on `time%end_mo`, `time%end_yr`,
    `time%day_end_yr`, `time%end_sim`, `time%yrs_prt`, and `time%days_prt`.'
  basin_module: The `pco` print-control object decides whether this routine writes daily,
    monthly, yearly, or average-annual output and whether it also emits CSV records. Its flags
    gate the writes to the basin pesticide output units, so these settings determine which
    summary streams are produced.
  output_landscape_module: This module is a dependency of the pesticide output path, so it
    provides shared landscape-output definitions or interfaces used by the broader output
    system even though no specific symbol from it is referenced in the extracted source lines.
  constituent_mass_module: The routine needs `cs_db%num_pests` to know how many pesticides
    to process and `cs_db%pests(ipest)` to label each output record with the pesticide name.
    Without this database, the routine would not know the loop bounds or the text name to
    write for each pesticide summary.
  hydrograph_module: 'The channel/hydrograph state provides the object context for the output
    record: `sp_ob1%chandeg` selects the channel object index used for `ob(iob)%name`, `sp_ob%chandeg`
    sets the channel-degree loop bound, and `ob(iob)%name` supplies the basin/channel object
    label written to the output files.'
---

<!-- facts:header -->

Writes basin/channel pesticide balance summaries for each simulated pesticide. It produces daily, monthly, yearly, and average-annual outputs when the corresponding print switches are enabled.

## Bottom Line

This routine loops over every simulated pesticide and builds a basin-level channel pesticide balance for the current day by starting from `ch_pestbz` and adding the channel-day values in `chpst_d(jrch)%pest(ipest)` across all channel-degrees. It then rolls that daily total into monthly, yearly, and average-annual accumulators in `bchpst_m`, `bchpst_y`, and `bchpst_a`.

When the print controls in `pco` and `time` say to do so, it writes the basin/channel pesticide summaries to the basin pesticide output units and optional CSV units. The output records include the current date, the object name from `ob(iob)%name`, the pesticide name from `cs_db%pests(ipest)`, and the summarized balance value for the current period.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after the model has set up channel, pesticide, timing, and print-control state. `command` calls it only when there are channel-degree objects and at least one pesticide simulated, and the values it writes are later consumed by the basin pesticide output files for daily, monthly, yearly, and average-annual reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the channel-object index used in output records. | Set `iob` to `sp_ob1%chandeg`, which selects the channel object whose name is written on all pesticide output records. |
| 2. Loop over each simulated pesticide. | For every pesticide in `cs_db%num_pests`, start the daily basin balance from the baseline value `ch_pestbz`. |
| 3. Accumulate daily channel contributions. | Sum `chpst_d(jrch)%pest(ipest)` across all channel-degree objects so `bchpst_d%pest(ipest)` becomes the basin daily total for that pesticide. |
| 4. Add the daily total into the monthly accumulator. | Carry the current daily balance into `bchpst_m%pest(ipest)` so the month-to-date total keeps growing between month-end prints. |
| 5. Write daily output when daily printing is enabled. | If the current day is a configured print day and daily pesticide output is enabled, write the daily record to unit 2832 and optionally the CSV record to unit 2836. |
| 6. Roll monthly output at month end. | At the end of a month, add the month total into `bchpst_y`, scale the month total by the number of days in the month, write monthly output to units 2833 and 2837 if enabled, then reset `bchpst_m` to `ch_pestbz` for the next month. |
| 7. Roll yearly output at year end. | At the end of a year, add the year total into `bchpst_a`, scale the year total by `time%day_end_yr`, write yearly output to units 2834 and 2838 if enabled, and leave the annual accumulation ready for the next period. |
| 8. Write average-annual output at simulation end. | If the simulation has ended and average-annual pesticide output is enabled, normalize `bchpst_a` by `time%yrs_prt` and `time%days_prt`, write the average-annual record to units 2835 and 2839, then reset `bchpst_a` to `ch_pestbz`. |
| 9. Advance to the next pesticide. | Continue the outer loop until every pesticide has been processed. |
| 10. Return to the caller. | Exit the subroutine after all requested pesticide output records have been written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `output_ls_pesticide_module state and types` | `Imported module state is not identified by a resolved candidate reference in the packet.` |
| [sym:ch_pesticide_module] | `bchpst_d, chpst_d, bchpst_m, bchpst_y, bchpst_a, ch_pestbz` | `bchpst_d%pest(ipest), chpst_d(jrch)%pest(ipest), bchpst_m%pest(ipest), bchpst_y%pest(ipest), bchpst_a%pest(ipest)` |
| [sym:plant_module] | `plant_module state and types` | `Imported module state is not identified by a resolved candidate reference in the packet.` |
| [sym:plant_data_module] | `plant_data_module state and types` | `Imported module state is not identified by a resolved candidate reference in the packet.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `output_landscape_module state and types` | `Imported module state is not identified by a resolved candidate reference in the packet.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob` | `sp_ob1%chandeg, sp_ob%chandeg, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bchpst_d%pest(ipest)` | Each time a new pesticide loop iteration begins, before daily accumulation and again after month/year/simulation-end resets. | The daily basin pesticide balance is rebuilt for the current pesticide and then cleared back to `ch_pestbz` after period output, so the next period starts from the zero/baseline pesticide state. |
| `bchpst_m%pest(ipest)` | At every iteration of the pesticide loop, and especially when `time%end_mo == 1` triggers the month-end branch. | The monthly accumulator collects daily pesticide balances across the month and is then converted to a month-average value for output before being reset to `ch_pestbz` at month end. |
| `bchpst_y%pest(ipest)` | When `time%end_yr == 1` is true. | The yearly accumulator receives the completed monthly total, is normalized by the number of days in the year for output, and then is kept ready for later period accumulation by the annual reset logic. |
| `bchpst_a%pest(ipest)` | When `time%end_sim == 1 .and. pco%pest%a == 'y'`. | The average-annual accumulator is normalized across the full simulation window, written to the average-annual output files, and then reset to the baseline pesticide state. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was added in commit df07e3f as a new basin channel pesticide output subroutine. Later commit 39fabde initialized its local variables (`ipest`, `iob`, `jrch`, and `const`) at declaration, and commit 2fe89fd changed the CSV write formats from `G0.3` to `G0.6` for the daily, monthly, yearly, and average-annual CSV outputs.

- df07e3f introduced the routine and its full daily/monthly/yearly/average-annual pesticide output flow, including the period accumulators and file writes.
- 39fabde only changed local variable initialization, which affects robustness but not the output algorithm itself.
- 2fe89fd changed the CSV formatting precision for the four CSV output units, improving numeric output detail without changing the period logic.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_ch_pest_output' has no extracted documentation comment.
- algorithm_steps revised: split the core logic into explicit setup, accumulation, daily/monthly/yearly/average-annual output, and return steps to match the visible control flow.
- The packet resolves no concrete symbols from `output_ls_pesticide_module`, `plant_module`, or `plant_data_module`; their descriptions are therefore limited to dependency-level relevance rather than specific component usage.
