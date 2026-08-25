---
kind: procedure
symbol: ru_salt_output
title: ru_salt_output
status: filled
source_hash: 54e9db2eb30b71cd
version_label: SWAT+ 62.0.0
args:
  iru: '`iru` identifies which routing unit is being processed; the routine uses it to index
    the routing-unit salt balance arrays and to derive the matching object index `iob = sp_ob1%ru
    + iru - 1` for the GIS identifier written to output.'
locals:
  iob: Maps the routing-unit index `iru` to the corresponding connectivity/object record in
    `ob`, so the output line can include `ob(iob)%gis_id`. Initial value 0 is overwritten
    immediately by `iob = sp_ob1%ru + iru - 1`.
  isalt: Loop counter over salt ions. It ranges from 1 to `cs_db%num_salts` and is used to
    accumulate, print, and clear the per-salt values for each routing-unit hydrograph.
  ihyd: 'Loop counter over the five hydrograph categories (`hd(1)` through `hd(5)`) used for
    routing-unit salt outputs: total out, percolation, surface runoff, lateral flow, and tile
    flow.'
uses:
  time_module: '`time_module` supplies the current simulation date and the end-of-period flags
    that control when daily, monthly, yearly, and average-annual salt output is written. Its
    fields also provide the calendar values printed on each record and `time%nbyr`, which
    is used to convert annual totals into average annual values.'
  basin_module: '`basin_module` provides the print-control flags in `pco`. Those flags decide
    whether this routine writes daily, monthly, yearly, or average-annual salt files, and
    whether it also emits the CSV-formatted versions of those records.'
  hydrograph_module: '`hydrograph_module` provides the routing-unit object mapping used to
    attach each output row to the correct GIS object. `sp_ob1%ru` is used to locate the routing-unit
    block in `ob`, and `ob(iob)%gis_id` is written as the identifier for each record.'
  salt_module: '`salt_module` owns the routing-unit salt balance storage that this routine
    reads, accumulates, prints, and clears. The daily, monthly, yearly, and average-annual
    arrays for routing-unit salt loads and HRU-to-routing-unit salt components are all updated
    here.'
  constituent_mass_module: '`constituent_mass_module` provides the number of salt ions to
    loop over and the routing-unit constituent hydrograph arrays that hold the mass values
    written here. Without `cs_db%num_salts`, the routine would not know how many salt-ion
    entries to process per hydrograph.'
---

<!-- facts:header -->

Aggregates routing-unit salt loads from daily to monthly, yearly, and average-annual totals, then writes period output records for each routing unit when enabled.

## Bottom Line

`ru_salt_output` collects the current day's salt mass results for one routing unit and rolls them into the monthly accumulators. It then prints the daily results if daily salt output is enabled, using the routing-unit GIS id and the salt mass terms stored in `rusaltb_d` and `ru_hru_saltb_d`.

At month-end it transfers monthly totals into yearly accumulators, writes monthly output when requested, and clears the monthly daily-sum buffers. At year-end it does the same for yearly-to-average-annual accumulation, divides the annual accumulators by `time%nbyr`, and writes average annual output when requested. The routine matters because it is the reporting point for routing-unit salt mass balance outputs and resets the period buffers after each print cycle.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls `ru_salt_output` inside the routing-unit loop after `ru_output(j)` and only when `cs_db%num_salts > 0`. The routine runs during the model's output phase for each routing unit, using daily salt results already accumulated in the salt balance arrays. Its results feed the printed salt output files and its zeroing of the daily/monthly/yearly scratch arrays ensures the next period starts clean.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the routing unit to its object record | Compute `iob = sp_ob1%ru + iru - 1` so the routine can fetch the matching routing-unit object connectivity record and write its GIS identifier with each output line. |
| 2. Add daily salt totals into the monthly accumulators | For each salt ion and each of the five hydrograph categories, add the daily routing-unit salt masses into the monthly routing-unit balances. Also accumulate the HRU-to-routing-unit salt terms (`wtsp`, `irsw`, `irgw`, `irwo`, `rain`, `dryd`, `road`, `fert`, `amnd`, `uptk`, and `diss`) into the monthly HRU balance arrays. |
| 3. Write daily salt output when enabled | If `pco%salt_ru%d == 'y'`, write the daily salt report to unit 5070. If `pco%csvout == 'y'`, also write the same daily data as CSV to unit 5071. The routine prints the date, routing-unit id, GIS id, all daily routing-unit hydrograph salt totals, and the HRU salt balance terms. |
| 4. Clear the daily salt buffers | Reset the daily routing-unit and HRU salt balance arrays to zero after the daily values have been accumulated and printed, so the next day starts with empty daily scratch values. |
| 5. On month end, roll monthly totals into yearly accumulators | When `time%end_mo == 1`, add the monthly routing-unit and HRU salt totals into the yearly accumulator arrays. This preserves the monthly period totals for the annual summaries. |
| 6. Write monthly salt output when enabled | If monthly salt output is enabled, write the month-end report to unit 5072 and, when CSV output is enabled, write the CSV form to unit 5073. The report uses the monthly accumulator arrays and includes the date, routing-unit id, and GIS id. |
| 7. Clear the monthly salt buffers | After monthly reporting, reset the monthly routing-unit and HRU salt balance arrays to zero so the next month accumulates from a clean slate. |
| 8. On year end, roll yearly totals into average-annual accumulators | When `time%end_yr == 1`, add the yearly routing-unit and HRU salt totals into the average-annual accumulator arrays. This stores the year-end totals needed for the final average-annual report. |
| 9. Write yearly salt output when enabled | If yearly salt output is enabled, write the year-end report to unit 5074 and, when CSV output is enabled, write the CSV form to unit 5075. The report uses the yearly accumulator arrays and includes the current date and routing-unit identifiers. |
| 10. Clear the yearly salt buffers | After yearly reporting, reset the yearly routing-unit and HRU salt balance arrays to zero so the next year can accumulate independently. |
| 11. At end of simulation, average annual totals and write final output | If `time%end_sim == 1` and average-annual salt output is enabled, divide the annual routing-unit and HRU salt accumulators by `time%nbyr` to compute per-year averages, then write the formatted report to unit 5076 and the CSV report to unit 5077 when requested. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%salt_ru%d, pco%csvout, pco%salt_ru%m, pco%salt_ru%y, pco%salt_ru%a` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%ru` |
| [sym:salt_module] | `ru_hru_saltb_m, ru_hru_saltb_d, ru_hru_saltb_y, ru_hru_saltb_a` | `ru_hru_saltb_m(iru)%salt(isalt)%wtsp, ru_hru_saltb_d(iru)%salt(isalt)%wtsp, ru_hru_saltb_m(iru)%salt(isalt)%irsw, ru_hru_saltb_d(iru)%salt(isalt)%irsw, ru_hru_saltb_m(iru)%salt(isalt)%irgw, ru_hru_saltb_d(iru)%salt(isalt)%irgw, ru_hru_saltb_m(iru)%salt(isalt)%irwo, ru_hru_saltb_d(iru)%salt(isalt)%irwo, ru_hru_saltb_m(iru)%salt(isalt)%rain, ru_hru_saltb_d(iru)%salt(isalt)%rain, ru_hru_saltb_m(iru)%salt(isalt)%dryd, ru_hru_saltb_d(iru)%salt(isalt)%dryd, ru_hru_saltb_m(iru)%salt(isalt)%road, ru_hru_saltb_d(iru)%salt(isalt)%road, ru_hru_saltb_m(iru)%salt(isalt)%fert, ru_hru_saltb_d(iru)%salt(isalt)%fert, ru_hru_saltb_m(iru)%salt(isalt)%amnd, ru_hru_saltb_d(iru)%salt(isalt)%amnd, ru_hru_saltb_m(iru)%salt(isalt)%uptk, ru_hru_saltb_d(iru)%salt(isalt)%uptk, ru_hru_saltb_m(iru)%salt(1)%diss, ru_hru_saltb_d(iru)%salt(1)%diss, ru_hru_saltb_y(iru)%salt(isalt)%wtsp, ru_hru_saltb_y(iru)%salt(isalt)%irsw, ru_hru_saltb_y(iru)%salt(isalt)%irgw, ru_hru_saltb_y(iru)%salt(isalt)%irwo, ru_hru_saltb_y(iru)%salt(isalt)%rain, ru_hru_saltb_y(iru)%salt(isalt)%dryd, ru_hru_saltb_y(iru)%salt(isalt)%road, ru_hru_saltb_y(iru)%salt(isalt)%fert, ru_hru_saltb_y(iru)%salt(isalt)%amnd, ru_hru_saltb_y(iru)%salt(isalt)%uptk, ru_hru_saltb_y(iru)%salt(1)%diss, ru_hru_saltb_a(iru)%salt(isalt)%wtsp, ru_hru_saltb_a(iru)%salt(isalt)%irsw, ru_hru_saltb_a(iru)%salt(isalt)%irgw, ru_hru_saltb_a(iru)%salt(isalt)%irwo, ru_hru_saltb_a(iru)%salt(isalt)%rain, ru_hru_saltb_a(iru)%salt(isalt)%dryd, ru_hru_saltb_a(iru)%salt(isalt)%road, ru_hru_saltb_a(iru)%salt(isalt)%fert, ru_hru_saltb_a(iru)%salt(isalt)%amnd, ru_hru_saltb_a(iru)%salt(isalt)%uptk, ru_hru_saltb_a(iru)%salt(1)%diss` |
| [sym:constituent_mass_module] | `cs_db, rusaltb_m, rusaltb_d, rusaltb_y, rusaltb_a` | `cs_db%num_salts, rusaltb_m(iru)%hd(ihyd)%salt(isalt), rusaltb_d(iru)%hd(ihyd)%salt(isalt), rusaltb_d(iru)%hd(1)%salt(isalt), rusaltb_d(iru)%hd(2)%salt(isalt), rusaltb_d(iru)%hd(3)%salt(isalt), rusaltb_d(iru)%hd(4)%salt(isalt), rusaltb_d(iru)%hd(5)%salt(isalt), rusaltb_y(iru)%hd(ihyd)%salt(isalt), rusaltb_m(iru)%hd(1)%salt(isalt), rusaltb_m(iru)%hd(2)%salt(isalt), rusaltb_m(iru)%hd(3)%salt(isalt), rusaltb_m(iru)%hd(4)%salt(isalt), rusaltb_m(iru)%hd(5)%salt(isalt), rusaltb_a(iru)%hd(ihyd)%salt(isalt), rusaltb_y(iru)%hd(1)%salt(isalt), rusaltb_y(iru)%hd(2)%salt(isalt), rusaltb_y(iru)%hd(3)%salt(isalt), rusaltb_y(iru)%hd(4)%salt(isalt), rusaltb_y(iru)%hd(5)%salt(isalt), rusaltb_a(iru)%hd(1)%salt(isalt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rusaltb_m(iru)%hd(ihyd)%salt(isalt)` | Each call, while looping over `isalt = 1, cs_db%num_salts` and `ihyd = 1,5`, before the daily buffers are cleared. | The monthly routing-unit salt hydrograph totals are incremented by the current day's values, so `rusaltb_m(iru)%hd(ihyd)%salt(isalt)` becomes the running monthly sum for that salt and hydrograph category. |
| `ru_hru_saltb_m(iru)%salt(isalt)%wtsp` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly HRU-to-routing-unit wetland seepage salt total is incremented by the current day's `ru_hru_saltb_d(iru)%salt(isalt)%wtsp`, so the monthly accumulator stores the running total for that salt ion. |
| `ru_hru_saltb_m(iru)%salt(isalt)%irsw` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly HRU-to-routing-unit surface-water irrigation salt total is incremented by the current day's value, accumulating the monthly delivery of surface-water irrigation salts. |
| `ru_hru_saltb_m(iru)%salt(isalt)%irgw` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly HRU-to-routing-unit groundwater irrigation salt total is incremented by the current day's value, accumulating the monthly delivery of groundwater irrigation salts. |
| `ru_hru_saltb_m(iru)%salt(isalt)%irwo` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly HRU-to-routing-unit other-water irrigation salt total is incremented by the current day's value, accumulating salts applied from outside the watershed. |
| `ru_hru_saltb_m(iru)%salt(isalt)%rain` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly rainfall salt addition total is incremented by the current day's value, so the accumulator tracks the monthly salt input from rainfall. |
| `ru_hru_saltb_m(iru)%salt(isalt)%dryd` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly dry deposition salt addition total is incremented by the current day's value, tracking the monthly atmospheric dry deposition load. |
| `ru_hru_saltb_m(iru)%salt(isalt)%road` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly road-salt addition total is incremented by the current day's value, tracking monthly road salt loading. |
| `ru_hru_saltb_m(iru)%salt(isalt)%fert` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly fertilizer salt addition total is incremented by the current day's value, tracking the monthly salt load from fertilizer. |
| `ru_hru_saltb_m(iru)%salt(isalt)%amnd` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly amendment salt addition total is incremented by the current day's value, tracking the monthly salt load from amendments. |
| `ru_hru_saltb_m(iru)%salt(isalt)%uptk` | Each call, while looping over `isalt = 1, cs_db%num_salts`, before the daily buffers are cleared. | The monthly crop uptake salt total is incremented by the current day's value, tracking the monthly salt mass taken up by crops. |
| `ru_hru_saltb_m(iru)%salt(1)%diss` | Each call, after the daily accumulation, before the daily buffers are cleared. | The dissolved salt term for the first salt ion is incremented by the current day's dissolved transfer value, so the monthly dissolved salt total is retained separately from the per-ion looped terms. |
| `rusaltb_d(iru)%hd(ihyd)%salt(isalt)` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly routing-unit salt hydrograph totals are incremented by the current month's values, so `rusaltb_y(iru)%hd(ihyd)%salt(isalt)` becomes the running yearly sum for each salt and hydrograph category. |
| `ru_hru_saltb_d(iru)%salt(isalt)%wtsp` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly HRU-to-routing-unit wetland seepage salt total is incremented by the current month's value, accumulating the annual total for that salt ion. |
| `ru_hru_saltb_d(iru)%salt(isalt)%irsw` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly HRU-to-routing-unit surface-water irrigation salt total is incremented by the current month's value, accumulating the annual delivery of surface-water irrigation salts. |
| `ru_hru_saltb_d(iru)%salt(isalt)%irgw` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly HRU-to-routing-unit groundwater irrigation salt total is incremented by the current month's value, accumulating the annual delivery of groundwater irrigation salts. |
| `ru_hru_saltb_d(iru)%salt(isalt)%irwo` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly HRU-to-routing-unit other-water irrigation salt total is incremented by the current month's value, accumulating salts applied from outside the watershed over the year. |
| `ru_hru_saltb_d(iru)%salt(isalt)%rain` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly rainfall salt addition total is incremented by the current month's value, tracking the annual salt input from rainfall. |
| `ru_hru_saltb_d(iru)%salt(isalt)%dryd` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly dry deposition salt addition total is incremented by the current month's value, tracking the annual atmospheric dry deposition load. |
| `ru_hru_saltb_d(iru)%salt(isalt)%road` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly road-salt addition total is incremented by the current month's value, tracking the annual road salt loading. |
| `ru_hru_saltb_d(iru)%salt(isalt)%fert` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly fertilizer salt addition total is incremented by the current month's value, tracking the annual salt load from fertilizer. |
| `ru_hru_saltb_d(iru)%salt(isalt)%amnd` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly amendment salt addition total is incremented by the current month's value, tracking the annual salt load from amendments. |
| `ru_hru_saltb_d(iru)%salt(isalt)%uptk` | At month end, when `time%end_mo == 1` and before the monthly buffers are cleared. | The yearly crop uptake salt total is incremented by the current month's value, tracking the annual salt mass taken up by crops. |
| `rusaltb_y(iru)%hd(ihyd)%salt(isalt)` | At simulation end, when `time%end_sim == 1` and before the average-annual report is written. | The average-annual routing-unit salt hydrograph totals are formed by dividing the accumulated annual sums by `time%nbyr`, so `rusaltb_y` values become per-year averages stored in `rusaltb_a` for final reporting. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved four commits affecting `ru_salt_output`. The initial addition in `df07e3f` introduced the subroutine, the daily/monthly/yearly/average-annual accumulation logic, and all output records. `35b029c` made a small whitespace-only cleanup near the end of the routine. `39fabde` initialized the local loop/index variables `iob`, `isalt`, and `ihyd` to zero and adjusted the doc-comment formatting. `f1e61a3` and `2fe89fd` changed only the CSV write formats, raising the `G0` precision from `G0.3` to `G0.6` for the CSV output records on units 5071, 5073, 5075, and 5077.

- df07e3f added the full routing-unit salt output procedure, including accumulation of daily values into monthly, yearly, and average-annual arrays, the zeroing of period buffers, and the formatted/CSV writes to units 5070-5077.
- 35b029c made a non-behavioral whitespace cleanup near the end of the subroutine without changing the algorithm.
- 39fabde initialized `iob`, `isalt`, and `ihyd` at declaration time and aligned the comment formatting, which does not change the output logic but makes the local state explicit.
- f1e61a3 corrected indentation in two CSV write continuations; the write targets and control flow were unchanged.
- 2fe89fd increased the CSV numeric format precision from `G0.3` to `G0.6` for the salt output CSV files, affecting the textual representation written to units 5071, 5073, 5075, and 5077.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ru_salt_output' has no extracted documentation comment.
- algorithm_steps revised: compressed the draft into the actual source sequence and split the algorithm into accumulation, output, zeroing, and end-of-period phases.
- Source indicates no outgoing calls were extracted for this subroutine.
- Lineage resolved from Git history; no unresolved-commit fallback needed.
