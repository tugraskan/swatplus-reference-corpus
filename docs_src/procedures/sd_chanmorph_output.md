---
kind: procedure
symbol: sd_chanmorph_output
title: sd_chanmorph_output
status: filled
source_hash: 30f46b1670ccff84
version_label: SWAT+ 62.0.0
args:
  ichan: Selects which swat-deg channel slot to report. The routine uses `ichan` to index
    the channel summary arrays (`chsd_d`, `chsd_m`, `chsd_y`, `chsd_a`) and to derive the
    matching object index in `ob` for the output record.
locals:
  iob: Holds the connected object index for the swat-deg channel being reported. It is computed
    from `sp_ob1%chandeg + ichan - 1` so the routine can fetch `ob(iob)%gis_id` and `ob(iob)%name`
    for the output lines.
  const: Temporary divisor used to convert accumulated monthly or yearly totals into averages.
    It is set to the number of days in the month or to `time%day_end_yr` before dividing the
    running sum.
uses:
  sd_channel_module: '`sd_channel_module` supplies the channel-morphology summary storage
    that this routine updates and writes. The arrays `chsd_d`, `chsd_m`, `chsd_y`, `chsd_a`,
    and the zeroed prototype `chsdz` are the values being accumulated, reset, averaged, and
    emitted.'
  basin_module: '`basin_module` provides the print-control flags that decide whether each
    output period is produced and whether CSV sidecar files are written. Without `pco`, the
    routine would not know if daily, monthly, yearly, or average-annual output should be written
    for swat-deg channels.'
  time_module: '`time_module` supplies the simulation clock and period-end markers that trigger
    each branch of the routine. Fields such as `time%end_mo`, `time%end_yr`, `time%end_sim`,
    and the date fields written to the records determine when summaries roll over and what
    timestamp is written.'
  hydrograph_module: '`hydrograph_module` provides the object lookup used to label each output
    record with the connected channel object. `sp_ob1%chandeg` sets the base swat-deg channel
    offset, and `ob(iob)%gis_id`/`ob(iob)%name` identify the object in the output rows.'
---

<!-- facts:header -->

Writes SWAT+ channel-morphology outputs for a single swat-deg channel. It records daily, monthly, yearly, and average-annual summaries to the configured output units and CSV companions.

## Bottom Line

sd_chanmorph_output updates the running channel-morphology summaries for one swat-deg channel, then writes them when the current date hits a daily, monthly, yearly, or end-of-simulation print point. It uses the print-code flags in `pco` to decide which periods to emit and which file units to write.

The routine matters because it is the output checkpoint for `chsd_d`, `chsd_m`, `chsd_y`, and `chsd_a`: it accumulates the current day into monthly totals, rolls monthly totals into yearly totals, averages period totals by day counts, and emits formatted records keyed by simulation time and channel object identity.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after the channel-morphology state for a swat-deg channel has been updated for the current timestep. `command` calls it inside the swat-deg channel loop after upstream model work has populated `chsd_d(ichan)` and the time/print-control state; downstream reporting depends on the updated period totals and the written records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the channel index to an object index. | Compute `iob` from `sp_ob1%chandeg + ichan - 1` so the routine can label the output with the correct connected object metadata. |
| 2. Accumulate the current day into the monthly running total. | Add `chsd_d(ichan)` into `chsd_m(ichan)` before any period-end reporting so the month total includes the current day. |
| 3. Write daily output when daily printing is enabled for the current print interval. | If `pco%day_print` is enabled and `pco%int_day_cur == pco%int_day`, then write the daily record to unit 4800 and, when `pco%csvout == 'y'`, to unit 4804. |
| 4. Roll month-end values into the yearly accumulator and average the monthly total. | At `time%end_mo == 1`, add the monthly sum to `chsd_y(ichan)`, set `const` to the number of days in the month, and divide `chsd_m(ichan)` by `const` to form the monthly average. |
| 5. Emit monthly output if monthly reporting is enabled. | If `pco%sd_chan%m == 'y'`, write the monthly record to unit 4801 and, when CSV output is enabled, to unit 4805; then reset `chsd_m(ichan)` to `chsdz` for the next month. |
| 6. Roll year-end values into the average-annual accumulator and average the yearly total. | At `time%end_yr == 1`, add the yearly sum to `chsd_a(ichan)`, set `const` to `time%day_end_yr`, and divide `chsd_y(ichan)` by `const` to form the yearly average. |
| 7. Emit yearly output if yearly reporting is enabled. | If `pco%sd_chan%y == 'y'`, write the yearly record to unit 4802 and, when CSV output is enabled, to unit 4806. |
| 8. Average the full-simulation total and emit average-annual output at simulation end. | At `time%end_sim == 1`, divide `chsd_a(ichan)` by `time%days_prt` and `time%yrs_prt`, then write the average-annual record to unit 4803 and, when CSV output is enabled, to unit 4807. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `chsd_m, chsd_d, chsd_y, chsd_a, chsdz` |  |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%sd_chan%d, pco%csvout, pco%sd_chan%m, pco%sd_chan%y, pco%sd_chan%a` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%days_prt, time%yrs_prt` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%chandeg, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chsd_m(ichan)` | When the routine starts for every call, before any period-end tests. | `chsd_m(ichan)` is incremented by the current daily value `chsd_d(ichan)`, building the month-to-date total that later gets averaged and optionally written at month end. |
| `chsd_y(ichan)` | When `time%end_mo == 1`, after the month-to-date total has been added to `chsd_y(ichan)`. | `chsd_y(ichan)` receives the completed month total and then serves as the yearly running sum source; after accumulation it is divided by the number of days in the month to form the monthly average for output. |
| `chsd_a(ichan)` | When `time%end_yr == 1`, after the yearly total has been added to `chsd_a(ichan)`. | `chsd_a(ichan)` receives the completed year total and then serves as the average-annual running sum source; the yearly value is divided by `time%day_end_yr` before yearly output is written. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior changes. The procedure was introduced in df07e3f with daily, monthly, yearly, and average-annual output branches. In 39fabde, the local scratch variables `iob` and `const` were initialized at declaration. In 2fe89fd, only the CSV format strings changed from `G0.3` to `G0.6` on units 4804, 4805, 4806, and 4807.

- df07e3f added the full `sd_chanmorph_output` subroutine with accumulation, period-end averaging, and writes to units 4800-4807.
- 39fabde initialized `iob` and `const` in the local declarations, removing uninitialized-scratch-variable risk.
- 2fe89fd increased CSV numeric precision from `G0.3` to `G0.6` for the four CSV companion outputs.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sd_chanmorph_output' has no extracted documentation comment.
