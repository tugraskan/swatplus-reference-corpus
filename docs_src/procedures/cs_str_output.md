---
kind: procedure
symbol: cs_str_output
title: cs_str_output
status: filled
source_hash: 9045555cb42f1ae8
version_label: SWAT+ 62.0.0
locals:
  i: Loop counter used to walk through the `cs_str_obs` list for each output field block and
    again when writing the assembled record.
  chan_id: Holds the current channel index pulled from `cs_str_obs(i)` so the routine can
    read that channel's flow or constituent values.
  elem_count: Counts how many values have been placed into `line_array`; it advances as each
    output field block is appended and controls how many values are written.
  line_array: Temporary record buffer that collects the year/day plus all selected channel
    output values before the single formatted write to unit 8200.
uses:
  hydrograph_module: This module supplies `ch_out_d`, the daily channel hydrology output array.
    `cs_str_output` reads `flo` and `no3` from it for each selected channel, so the hydrology
    outputs are part of the constituent report record.
  constituent_mass_module: This module provides the stream-observation controls `cs_obs_file`,
    `cs_str_nobs`, and `cs_str_obs`. They determine whether the routine writes anything and
    which channel IDs are sampled for the daily output record.
  ch_cs_module: This module supplies `chcs_d`, the daily channel constituent output array.
    `cs_str_output` reads selenium concentration and total outflow fields from it to populate
    the output line.
  time_module: This module supplies the current simulation date fields `time%yrc` and `time%day`,
    which are written at the start of each record so the daily constituent output is time-stamped.
---

<!-- facts:header -->

Writes the daily constituent stream-observation output line for the channels listed in the stream observation set. It gathers flow, concentrations, and loads from channel state and sends them to the daily output file.

## Bottom Line

cs_str_output is a daily reporting routine for selected channel observation points. When `cs_obs_file` is enabled, it assembles one record containing the current year/day plus flow, selenium concentrations, selenium loads, and nitrate load for every channel listed in `cs_str_obs`.

The routine does not compute new water-quality behavior; it packages values already stored in `ch_out_d` and `chcs_d` and writes them to output unit 8200. That makes it part of the model's daily diagnostics/reporting path for constituent transport.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the daily command/output workflow after upstream routines have populated `ch_out_d`, `chcs_d`, and the stream-observation list in `constituent_mass_module`. The `command` routine calls it when `cs_db%num_cs > 0`, and its written records are then used as the model's daily constituent stream output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check output flag | Tests `cs_obs_file` to decide whether daily stream constituent output is enabled. If the flag is off, the routine skips all record assembly and returns without writing. |
| 2. reset daily buffer | Clears `line_array` and resets `elem_count` so the day's output record starts empty and values are packed from the first position. |
| 3. collect flow | Loops over the stream-observation channel list, stores each channel ID in `chan_id`, and appends that channel's daily flow from `ch_out_d(chan_id)%flo` to the record buffer. |
| 4. collect se4 concentration | Loops over the same channel list again and appends selenium-4 concentration from `chcs_d(chan_id)%cs(1)%conc` for each observed channel. |
| 5. collect se3 concentration | Loops over the channel list and appends selenium-3 concentration from `chcs_d(chan_id)%cs(2)%conc` for each observed channel. |
| 6. collect se4 load | Loops over the channel list and appends selenium-4 daily load from `chcs_d(chan_id)%cs(1)%tot_out` for each observed channel. |
| 7. collect se3 load | Loops over the channel list and appends selenium-3 daily load from `chcs_d(chan_id)%cs(2)%tot_out` for each observed channel. |
| 8. collect nitrate load | Loops over the channel list and appends nitrate daily load from `ch_out_d(chan_id)%no3` for each observed channel. |
| 9. write daily record | Writes the current year, current day, and all buffered values in `line_array` to output unit 8200 using the formatted record layout. |
| 10. return | Ends the subroutine after the optional write is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ch_out_d` |  |
| [sym:constituent_mass_module] | `cs_str_obs, cs_obs_file, cs_str_nobs` |  |
| [sym:ch_cs_module] | `chcs_d` |  |
| [sym:time_module] | `time` | `time%yrc, time%day` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three changes: the routine was added in commit df07e3f, variable initial values were set in 39fabde, and 2ee1889 changed the closing statement to `end subroutine cs_str_output`.

- df07e3f introduced the full `cs_str_output` routine, including the conditional daily stream-observation write, buffer assembly loops, and formatted write to unit 8200.
- 39fabde initialized the local variables `i`, `chan_id`, `elem_count`, and `line_array`, affecting their starting values before each daily assembly pass.
- 2ee1889 changed only the subroutine terminator form to `end subroutine cs_str_output` without altering the routine's output logic.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cs_str_output' has no extracted documentation comment.
