---
kind: procedure
symbol: channel_output
title: channel_output
status: filled
source_hash: 7769f90d3ca2e2cb
version_label: SWAT+ 62.0.0
args:
  jrch: '`jrch` selects which channel-routing object to report; the routine uses it to index
    `ch_d`, `ch_m`, `ch_y`, and `ch_a`, and to derive the matching object record number `iob
    = sp_ob1%chan + jrch - 1`.'
locals:
  iob: '`iob` is the hydrograph object index for the channel being printed. It is initialized
    to 0, then set from `sp_ob1%chan + jrch - 1` so the routine can fetch the correct GIS
    id and object name from `ob(iob)` for the output records.'
uses:
  time_module: '`time_module` supplies the simulation clock and end-of-period flags that determine
    when channel output is emitted and when period totals are rolled up. The routine prints
    `time%day`, `time%mo`, `time%day_mo`, and `time%yrc`, and it branches on `time%end_mo`,
    `time%end_yr`, `time%end_sim`, and `time%yrs_prt` to decide monthly, yearly, and average-annual
    handling.'
  basin_module: '`basin_module` provides the print-control switches that enable or suppress
    each channel output branch. `pco%day_print`, `pco%int_day_cur`, and `pco%int_day` gate
    the daily branch, while `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a`, and `pco%csvout`
    decide whether fixed-format and CSV records are written for each reporting interval.'
  hydrograph_module: '`hydrograph_module` links the channel index to the broader object table
    used in output records. `sp_ob1%chan` gives the starting object number for channels, and
    `ob(iob)%name` supplies the object label that is written beside the channel values so
    the output can be tied back to the correct channel object.'
  channel_module: '`channel_module` holds the channel output state that this routine reports
    and updates. `ch_d`, `ch_m`, `ch_y`, `ch_a`, and `chz` are the daily input value, the
    accumulating monthly, yearly, and average-annual totals, and the reset value used after
    period boundaries.'
  climate_module: '`climate_module` is imported by the routine but no symbols from it are
    referenced in the extracted lines, so it currently appears to be an unused dependency
    here. It still matters for documentation because it may reflect a broader shared context
    in the source file, but the visible procedure logic does not depend on any extracted climate
    state.'
---

<!-- facts:header -->

Writes channel routing output at daily, monthly, yearly, and average-annual intervals. It accumulates channel totals in `ch_m`, `ch_y`, and `ch_a` and sends the selected records to fixed output units and optional CSV units.

## Bottom Line

`channel_output` is the channel reporting routine for one routed channel index `jrch`. On each call it builds the corresponding object index, rolls the current daily channel value into the monthly accumulator, and conditionally writes daily, monthly, yearly, and average-annual output records depending on the print codes in `pco` and the simulation calendar in `time`.

The routine matters because it is the point where channel states become model output. It preserves running totals across periods by resetting monthly and yearly accumulators to `chz` after they are reported, and the final average-annual result is normalized by `time%yrs_prt` before being written at end of simulation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`channel_output` runs from `command` once per channel object in the main output loop, after upstream simulation steps have populated `ch_d`, updated the calendar in `time`, and set the print codes in `pco`. Its results feed the model’s persistent output files and the period-reset of channel summary states that later calls depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute the channel object index and start the accumulation for this call. | The routine initializes `iob` from `sp_ob1%chan + jrch - 1` so it can map the requested channel number to the correct hydrograph object. It then adds the current daily channel value into the monthly accumulator with `ch_m(jrch) = ch_m(jrch) + ch_d(jrch)`. |
| 2. Write daily channel output when day printing is active. | If daily printing is enabled for the current day and the channel daily print flag is on, the routine writes the daily channel record to unit 2480. When CSV output is enabled, it also writes the same record to unit 2484. |
| 3. Roll month-end totals and write monthly output. | At the end of a month, the routine adds the current monthly accumulator into `ch_y(jrch)`, writes the monthly record to unit 2481 when monthly output is enabled, optionally writes CSV to unit 2485, and then resets `ch_m(jrch)` to `chz` for the next month. |
| 4. Roll year-end totals and write yearly output. | At the end of a year, the routine adds the yearly total into `ch_a(jrch)`, writes the yearly record to unit 2482 when yearly output is enabled, optionally writes CSV to unit 2486, and then resets `ch_y(jrch)` to `chz` for the next year. |
| 5. Normalize and write average-annual output at simulation end. | When the simulation ends and average-annual channel output is enabled, the routine divides `ch_a(jrch)` by `time%yrs_prt` to form the average annual value, writes it to unit 2483, and optionally writes the CSV record to unit 2487. |
| 6. Return to the caller after all requested output records are handled. | The routine ends with the fixed-format output label and a plain return, leaving the updated channel summary states in the module for later calls. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%chan%d, pco%csvout, pco%chan%m, pco%chan%y, pco%chan%a` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%chan, ob(iob)%name` |
| [sym:channel_module] | `ch_m, ch_d, ch_y, ch_a, chz` |  |
| [sym:climate_module] | `climate_module` | `none resolved from the extracted source` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch_m(jrch)` | `time%end_mo == 1` | `ch_m(jrch)` is reset to `chz` after the monthly value has been added into `ch_y(jrch)` and, if enabled, written as the month-end channel output. This clears the monthly accumulator so the next month starts from zero. |
| `ch_y(jrch)` | `time%end_yr == 1` | `ch_y(jrch)` is reset to `chz` after its accumulated yearly value has been added into `ch_a(jrch)` and, if enabled, written as the year-end channel output. This clears the yearly accumulator for the next year. |
| `ch_a(jrch)` | `time%end_sim == 1 .and. pco%chan%a == "y"` | `ch_a(jrch)` is divided by `time%yrs_prt` to convert the accumulated total into an average annual value before the final output record is written. The value remains in averaged form after the routine returns. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `channel_output`: df07e3f created the file with the current reporting logic, c7c8e22 added the latest source version without changing the visible behavior in the extracted span, 39fabde initialized `iob` to 0 and corrected a formatting comment indentation issue, and 2fe89fd changed the CSV numeric format from `G0.3` to `G0.6` for the daily, monthly, yearly, and average-annual CSV writes.

- df07e3f introduced the routine and its daily, monthly, yearly, and average-annual output branches, including the accumulator reset behavior.
- 39fabde made the local object index `iob` explicitly initialize to 0 before it is computed from `sp_ob1%chan + jrch - 1`, which is a code-quality change and does not alter the documented output algorithm.
- 2fe89fd increased CSV precision for all channel output intervals by changing the CSV write format from `G0.3` to `G0.6`, affecting the exported numeric text only.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'channel_output' has no extracted documentation comment.
- algorithm_steps revised: reordered the steps to match the source flow and split the final return into its own step.
- climate_module is imported in the source, but no extracted symbols from that module are referenced in the visible routine body; documentation should treat it as unused in this procedure unless additional source is provided.
