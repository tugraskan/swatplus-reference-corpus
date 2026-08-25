---
kind: procedure
symbol: cha_pesticide_output
title: cha_pesticide_output
status: filled
source_hash: 74eec78d71379849
version_label: SWAT+ 62.0.0
args:
  jrch: '`jrch` is the selected channel-deg object index passed in by the caller; the routine
    copies it to `j` and uses it to choose which `chpst_*` slot to update and which channel
    object name/ID to print.'
locals:
  ipest: Loop index over pesticide constituents in `cs_db%num_pests`; each iteration processes
    one pesticide name and one set of channel balance values.
  j: Working channel index copied from `jrch`; used to index the channel pesticide summary
    arrays and align output with the current channel-deg object.
  iob: Derived object index for the channel-deg entry in `ob`; computed from `sp_ob1%chandeg
    + j - 1` so the output record can print the correct GIS ID and object name.
  const: Temporary scaling factor used to convert period totals to a per-day or per-year average
    before the accumulated value is reset.
uses:
  output_ls_pesticide_module: No candidates were resolved to `output_ls_pesticide_module`
    in the extracted context, so no specific state from that module can be attributed here
    from the evidence packet.
  ch_pesticide_module: '`ch_pesticide_module` owns the four persistent channel pesticide summary
    arrays and the zero/reset constant `ch_pestbz`. This routine accumulates daily values
    into monthly, yearly, and average-annual totals using those arrays, then resets the period
    accumulators back to the baseline state after the corresponding output is written.'
  plant_module: No candidate state from `plant_module` is referenced in the extracted source
    lines, so it does not affect the documented behavior of this routine based on the available
    evidence.
  plant_data_module: No candidate state from `plant_data_module` is referenced in the extracted
    source lines, so it does not affect the documented behavior of this routine based on the
    available evidence.
  time_module: 'The `time` state controls every reporting gate in this routine: daily output
    uses the current day counters, monthly and yearly output depend on end-of-period flags,
    and average-annual output depends on end-of-simulation and the number of years printed.'
  basin_module: The `pco` print-code state turns each pesticide report on or off by period
    and determines whether CSV duplicates are written. Without these flags, the routine would
    still update the summary arrays but would skip the file output records.
  output_landscape_module: No candidate state from `output_landscape_module` was resolved
    in the context packet, so there is no source-backed module member to describe for this
    routine.
  constituent_mass_module: '`cs_db` provides the count of pesticide constituents to loop over
    and the pesticide names written to the report rows. That makes it the source of both the
    iteration bound and the human-readable constituent label in each output record.'
  hydrograph_module: '`sp_ob1%chandeg` anchors the channel-deg numbering used to derive `iob`,
    and `ob(iob)%name` provides the object name printed in the output rows. These hydrograph-module
    states tie the pesticide summaries to the correct channel object in the model network.'
---

<!-- facts:header -->

Writes channel pesticide balance output for one SWAT+ channel-deg object across daily, monthly, yearly, and average-annual reporting periods.

## Bottom Line

This routine loops over every simulated pesticide constituent and updates the running channel pesticide summaries for the selected channel-deg object. It then writes the current daily, monthly, yearly, and average-annual pesticide balances to the corresponding output units when the matching print flags and time conditions are active.

It matters because it is the channel-side reporting point for pesticide mass balance: the routine converts the internal accumulator states in `chpst_d`, `chpst_m`, `chpst_y`, and `chpst_a` into the model's output files, and it resets the period accumulators after month, year, or simulation-end reporting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine inside the channel-deg output loop after the channel object network has been established and after `cs_db%num_tot > 0` confirms that pesticide constituents exist. Its results feed the channel pesticide output files and the end-of-period summary states that are reused on later reporting passes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the caller's channel index to the local object indices. | The routine copies `jrch` into `j` and derives `iob` from the first channel-deg object index plus the offset. This sets up the channel object lookup used by every later print statement. |
| 2. Loop over every pesticide constituent. | The routine iterates from 1 to `cs_db%num_pests`, processing one pesticide at a time for the selected channel object. |
| 3. Accumulate the daily pesticide balance into the monthly total. | Before any printing, the daily channel balance for the current pesticide is added into the monthly accumulator `chpst_m(j)%pest(ipest)`. |
| 4. Write daily pesticide output when daily printing is enabled. | If the daily print flags are active, the routine writes a daily pesticide balance record to unit 2808 and optionally duplicates it to the CSV unit 2812. |
| 5. On month end, roll monthly totals into the yearly accumulator and scale the monthly average. | When `time%end_mo == 1`, the routine adds the current monthly total into `chpst_y(j)%pest(ipest)`, computes the month-length factor in `const`, and divides the monthly accumulator by that factor so the stored monthly output is an average over the month length. |
| 6. Write monthly output when the monthly print flag is enabled. | If monthly pesticide output is requested, the routine writes the monthly balance to unit 2809 and optionally writes the CSV version to unit 2813. |
| 7. Reset the monthly accumulator after the month-end report. | The routine restores the monthly accumulator to `ch_pestbz` so the next month starts from a clean pesticide balance state. |
| 8. On year end, roll yearly totals into the average-annual accumulator and scale the yearly value. | When `time%end_yr == 1`, the routine adds the yearly total into `chpst_a(j)%pest(ipest)`, stores the ending-day count in `const`, and divides the yearly accumulator by that count so the stored yearly output is normalized. |
| 9. Write yearly output when the yearly print flag is enabled. | If yearly pesticide output is requested, the routine writes the yearly balance to unit 2810 and optionally writes the CSV version to unit 2814. |
| 10. At simulation end, average the accumulated annual pesticide balance and write the average-annual report. | When the simulation ends and average-annual pesticide output is enabled, the routine divides the annual accumulator by `time%yrs_prt`, restores the units needed for the stored average, writes the result to unit 2811 and optionally to unit 2815, then resets the average-annual accumulator to `ch_pestbz`. |
| 11. Finish the pesticide loop and return. | After all pesticides are processed, the routine exits the loop, returns to the caller, and ends the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `none resolved` |  |
| [sym:ch_pesticide_module] | `chpst_m, chpst_d, chpst_y, chpst_a, ch_pestbz` | `chpst_m(j)%pest(ipest), chpst_d(j)%pest(ipest), chpst_y(j)%pest(ipest), chpst_a(j)%pest(ipest)` |
| [sym:plant_module] | `none resolved` |  |
| [sym:plant_data_module] | `none resolved` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `none resolved` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%chandeg, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chpst_m(j)%pest(ipest)` | During every pesticide loop iteration, before period-specific printing; the monthly accumulator is then reset at month end after the monthly report. | `chpst_m(j)%pest(ipest)` first gathers the daily channel pesticide balance into the month total, then is converted to a monthly-average form at month end, and finally is cleared back to `ch_pestbz` so the next month starts fresh. |
| `chpst_y(j)%pest(ipest)` | When `time%end_yr == 1`, after the monthly state has already been rolled forward for the current year. | `chpst_y(j)%pest(ipest)` accumulates the year total from the monthly state and is then normalized by the year-end day count, so it represents the yearly balance to be written at year end. |
| `chpst_a(j)%pest(ipest)` | When `time%end_sim == 1` and average-annual pesticide output is enabled by `pco%pest%a == 'y'`. | `chpst_a(j)%pest(ipest)` accumulates the yearly values across the full simulation, is converted to an average annual value using `time%yrs_prt`, and is then reset to `ch_pestbz` after the final report is written. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior-changing commits. The routine was created in df07e3f with the full channel pesticide output loop, daily/monthly/yearly/average-annual writes, and accumulator resets. In 39fabde the local working variables were initialized to zero, and in 2fe89fd the CSV companion writes for units 2812, 2813, 2814, and 2815 were changed from `G0.3` to `G0.6` formatting while preserving the same output structure and the average-annual reset.

- df07e3f introduced the subroutine and established the pesticide balance workflow: daily accumulation into `chpst_m`, month-end and year-end rollups, simulation-end averaging, output-unit writes, and resets to `ch_pestbz`.
- 39fabde made the loop counters and temporary scalar deterministic by initializing `ipest`, `j`, `iob`, and `const` at declaration, reducing dependence on uninitialized local state.
- 2fe89fd increased CSV output precision for the pesticide reports on units 2812, 2813, 2814, and 2815 from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cha_pesticide_output' has no extracted documentation comment.
- No resolved outside references were provided for output_ls_pesticide_module, plant_module, plant_data_module, or output_landscape_module in the extracted context.
- The source contains an apparent legacy line `chpst_m(j)%pest(ipest) = chpst_m(j)%pest(ipest) // const`; the overlay documents its apparent intended role as period normalization, but the exact operator semantics are source-uncertain.
