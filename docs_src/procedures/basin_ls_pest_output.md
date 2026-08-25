---
kind: procedure
symbol: basin_ls_pest_output
title: basin_ls_pest_output
status: filled
source_hash: 7d5357b884d964a6
version_label: SWAT+ 62.0.0
locals:
  ipest: Loop index for the current pesticide in cs_db%pests; selects which pesticide balance
    record is being accumulated and printed.
  ls: Loop index over landscape/HRU entries in sp_ob%hru; used to visit each contributing
    landscape element when forming the basin total.
  iihru: Intermediate HRU/object index taken from lsu_elem(ls)%obtypno so the routine can
    fetch the matching HRU pesticide balance in hpestb_d(iihru).
  iob: Holds the object index for the basin/HRU output name, copied from sp_ob1%hru and later
    used as ob(iob)%name in the output records.
  const: Temporary real factor used during monthly and yearly normalization steps; it receives
    the number of days in the current month or the year-end day count before the accumulated
    balance is scaled.
uses:
  output_ls_pesticide_module: '`output_ls_pesticide_module` defines the pesticide balance
    containers that this routine reads, accumulates, normalizes, prints, and resets: the daily/monthly/yearly/annual
    basin totals in bpestb_d, bpestb_m, bpestb_y, bpestb_a, the per-HRU balance array hpestb_d,
    and the zero-valued pesticide balance template pestbz.'
  plant_module: '`plant_module` is imported by the routine but no symbol from it is referenced
    in the extracted source lines, so it appears to be an unused dependency here.'
  plant_data_module: '`plant_data_module` is also imported but not referenced in the shown
    procedure body; it may be retained for consistency with related output routines even though
    this routine does not use its symbols directly.'
  time_module: '`time_module` provides the simulation clock and end-of-period flags that control
    when each summary is written and when accumulated daily values roll up into monthly, yearly,
    and average-annual totals.'
  basin_module: '`basin_module` supplies the print-control structure pco, which gates daily,
    monthly, yearly, and average-annual pesticide output and determines whether CSV versions
    are emitted.'
  calibration_data_module: '`calibration_data_module` supplies the LSU-to-HRU mapping and
    basin fraction metadata used while traversing landscape elements to identify the HRU index
    tied to each landscape entry.'
  output_landscape_module: '`output_landscape_module` is imported but no symbol from it is
    referenced in the extracted source lines, so it does not affect the visible logic of this
    routine.'
  constituent_mass_module: '`constituent_mass_module` provides cs_db, which tells the routine
    how many pesticides exist and supplies the pesticide names written into each output record.'
  hydrograph_module: '`hydrograph_module` provides the spatial object counts and object names
    that identify the basin/HRU context for the written records; without these indices and
    names the output lines could not be tagged to the correct object.'
---

<!-- facts:header -->

Aggregates pesticide balance output for all HRUs and writes daily, monthly, yearly, and average-annual basin-level pesticide summaries when the configured print intervals are active.

## Bottom Line

This subroutine builds basin-scale pesticide balance totals by looping over every simulated pesticide and summing HRU-level pesticide balances into daily, monthly, yearly, and average-annual accumulators. It then writes those totals to the basin pesticide output files when the corresponding print flags and time-end conditions are met.

The routine matters because it is the basin-level reporting step for pesticide mass balance: it uses the current simulation time, output-print controls, landscape mapping, and pesticide database names to produce the records that downstream output files and summary reports rely on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the main command-driven output phase, after the model has already populated pesticide balances for HRUs and set the current time/output-control flags. Its results feed the basin pesticide report files for daily, monthly, yearly, and average-annual summaries that users inspect after the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the basin object index. | The routine copies sp_ob1%hru into iob so later output rows can be labeled with the correct object name from ob(iob)%name. |
| 2. Loop over each pesticide. | The outer loop runs from 1 to cs_db%num_pests so the routine processes one pesticide balance at a time. |
| 3. Start the daily basin total from zero. | bpestb_d%pest(ipest) is reset to pestbz before summing contributions for the current pesticide. |
| 4. Sum HRU contributions into the daily basin total. | The inner landscape loop walks through sp_ob%hru entries, maps each landscape element to an HRU index with lsu_elem(ls)%obtypno, reads the basin fraction into const, and adds hpestb_d(iihru)%pest(ipest) into the daily basin pesticide balance. |
| 5. Accumulate the daily total into the monthly total. | The daily basin pesticide balance is added into bpestb_m%pest(ipest) so the month-to-date sum can be tracked across days. |
| 6. Write daily output when daily printing is enabled. | If day-printing is enabled and the day interval is active, the routine writes the daily basin pesticide balance to unit 2864 and, when CSV output is enabled, also writes the same record to unit 2868. |
| 7. Roll monthly totals into the yearly accumulator at month end. | When time%end_mo equals 1, the routine adds the monthly total into bpestb_y%pest(ipest), computes the number of days in the month using ndays, normalizes the monthly balance by that day count, writes monthly output if requested, and then resets the monthly accumulator to pestbz. |
| 8. Roll yearly totals into the average-annual accumulator at year end. | When time%end_yr equals 1, the routine adds the yearly total into bpestb_a%pest(ipest), divides by the year-end day count in time%day_end_yr, writes yearly output if requested, and leaves the yearly accumulator ready for the next cycle. |
| 9. Write average-annual output at the end of the simulation. | If this is the end of the simulation and average-annual printing is enabled, the routine normalizes bpestb_a%pest(ipest) by time%yrs_prt and time%days_prt, writes the final average-annual record to unit 2867 and optional CSV unit 2871, and then resets the accumulator to pestbz. |
| 10. Continue to the next pesticide and return. | After all pesticides are processed, the routine exits the loop, returns to the caller, and leaves the format statement available for the fixed-format writes above. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `bpestb_d, hpestb_d, bpestb_m, bpestb_y, bpestb_a, pestbz` | `bpestb_d%pest(ipest), hpestb_d(iihru)%pest(ipest), bpestb_m%pest(ipest), bpestb_y%pest(ipest), bpestb_a%pest(ipest)` |
| [sym:plant_module] | `plant_module` |  |
| [sym:plant_data_module] | `plant_data_module` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:calibration_data_module] | `lsu_elem` | `lsu_elem(ls)%obtypno, lsu_elem(iihru)%bsn_frac` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob` | `sp_ob1%hru, sp_ob%hru, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bpestb_d%pest(ipest)` | At the start of each pesticide loop, before HRU contributions are added. | bpestb_d%pest(ipest) is cleared to the zero pesticide-balance template so the routine can rebuild the basin daily total from the HRU-level values for the current pesticide. |
| `bpestb_m%pest(ipest)` | After the daily total has been formed and before the monthly branch resets the accumulator. | bpestb_m%pest(ipest) is incremented by the current day’s basin pesticide balance, then later normalized by the number of days in the month and reset to pestbz at month end. |
| `bpestb_y%pest(ipest)` | When time%end_mo == 1. | bpestb_y%pest(ipest) is increased by the month’s accumulated pesticide balance so the yearly total carries forward all completed months. |
| `bpestb_a%pest(ipest)` | When time%end_yr == 1 and again when time%end_sim == 1 for the final average-annual record. | bpestb_a%pest(ipest) is first increased by the year’s accumulated balance, then normalized for average-annual output at simulation end, written, and reset to pestbz. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four changes to basin_ls_pest_output: the file was added in df07e3f, the format statement was widened in 35b029c from 14e12.4 to 16e12.4, 39fabde initialized the local loop/index variables and const to zero, and 2fe89fd changed the CSV write formats from G0.3 to G0.6 for the daily, monthly, yearly, and average-annual CSV outputs.

- df07e3f introduced the subroutine and its daily/monthly/yearly/average-annual pesticide output workflow.
- 35b029c expanded the fixed-format output field count in format 100 to accommodate the record contents.
- 39fabde added explicit zero initialization for ipest, ls, iihru, iob, and const.
- 2fe89fd increased CSV numeric precision from G0.3 to G0.6 for all CSV pesticide balance writes.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_ls_pest_output' has no extracted documentation comment.
- plant_module and plant_data_module are imported but not referenced in the extracted source lines.
- output_landscape_module is imported but not referenced in the extracted source lines.
- The expression `bpestb_m%pest(ipest) = bpestb_m%pest(ipest) // const` and the matching yearly form appear as vector/derived-type scaling in the source context; the exact operator semantics were not expanded in the packet, so the description uses the visible intent rather than inferring a lower-level type implementation.
