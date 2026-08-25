---
kind: procedure
symbol: ru_cs_output
title: ru_cs_output
status: filled
source_hash: fda7ee393f744734
version_label: SWAT+ 62.0.0
args:
  iru: Routing-unit index identifying which RU’s constituent balances and output rows to process;
    it is combined with `sp_ob1%ru` to locate the matching object entry in `ob`.
locals:
  iob: Sequential object index for the routing unit in `ob`; initialized to 0 and set to `sp_ob1%ru
    + iru - 1` so the routine can print the correct GIS/object identifier.
  ics: Loop counter over constituents; initialized to 0 and used to traverse `1:cs_db%num_cs`
    for every constituent tracked by the model.
  ihyd: Loop counter over the five hydrograph pathways; initialized to 0 and used for total
    out, percolation, surface runoff, lateral flow, and tile flow.
uses:
  time_module: '`time_module` supplies the current simulation date and end-of-period flags.
    Those fields control which output blocks run and provide the date columns written to each
    record.'
  basin_module: '`basin_module` provides `pco`, the print-control flags that turn daily, monthly,
    yearly, and average-annual constituent output on or off, and the CSV-output switch used
    for the companion files.'
  hydrograph_module: '`hydrograph_module` supplies the routing-object table `ob` and the starting
    RU offset `sp_ob1%ru`. Those values are needed to map `iru` to the correct object record
    and write its GIS identifier.'
  cs_module: '`cs_module` holds the routing-unit constituent balance arrays that this routine
    accumulates, prints, and clears. The daily, monthly, yearly, and average arrays for both
    hydrograph totals and HRU-derived constituent fluxes all live here.'
  constituent_mass_module: '`constituent_mass_module` defines how many constituents are tracked
    and stores the routing-unit constituent hydrograph arrays. `cs_db%num_cs` sets the loop
    bounds, and `rucsb_*` provides the per-constituent total-out, percolation, runoff, lateral-flow,
    and tile-flow values written by this routine.'
---

<!-- facts:header -->

Writes routing-unit constituent mass output at daily, monthly, yearly, and average annual intervals. It also rolls daily totals into monthly, yearly, and long-term averages, then resets period accumulators after each print block.

## Bottom Line

`ru_cs_output` is the constituent-output routine for a routing unit. Given a routing-unit index `iru`, it gathers the current day’s constituent mass results and prints them in the configured intervals: daily, monthly, yearly, and average annual.

The routine also accumulates daily values into monthly totals, monthly totals into yearly totals, and yearly totals into simulation-average annual values. After each reporting window, it zeros the shorter-period accumulators so the next period starts fresh. This is the routine that turns the internal constituent balance arrays into the `.out` and optional `.csv` outputs used for reporting and post-processing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ru_cs_output` runs from the main command/output driver after routing and constituent balances for the current timestep have already been computed. `command` calls it for each routing unit when `cs_db%num_cs > 0`, so it depends on upstream simulation steps having filled the daily constituent arrays. Its printed results feed the routine’s output files and provide the summary records used at the end of the daily, monthly, yearly, and simulation-average reporting windows.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the routing-unit index to the global object list. | Compute `iob = sp_ob1%ru + iru - 1` so the routine can look up the routing unit’s object connectivity entry and print the correct GIS/object identifier. |
| 2. Accumulate current-day values into monthly running totals. | For every constituent and each of the five hydrograph pathways, add the daily routing-unit constituent masses to the monthly accumulators in `rucsb_m` and `ru_hru_csb_m`. |
| 3. Write daily constituent output when daily printing is enabled. | If `pco%cs_ru%d == 'y'`, write the day’s total-out, percolation, surface-runoff, lateral-flow, tile-flow, and HRU-flux values to unit 6070 in formatted output. |
| 4. Optionally write a daily CSV record. | If `pco%csvout == 'y'`, write the same daily constituent data to unit 6071 in CSV-style format. |
| 5. Clear daily accumulators after the daily report block. | Reset the daily routing-unit and HRU constituent arrays to zero so the next day starts with empty daily totals. |
| 6. On month end, roll monthly totals into yearly totals. | When `time%end_mo == 1`, add the monthly routing-unit and HRU constituent totals into the yearly accumulators in `rucsb_y` and `ru_hru_csb_y`. |
| 7. Write monthly output when monthly printing is enabled. | If `pco%cs_ru%m == 'y'`, write the month-accumulated routing-unit and HRU constituent totals to unit 6072. |
| 8. Optionally write a monthly CSV record. | If `pco%csvout == 'y'`, write the monthly constituent record to unit 6073 in CSV format. |
| 9. Clear monthly accumulators after the month-end report. | Reset the monthly routing-unit and HRU constituent arrays to zero so the next month starts fresh. |
| 10. On year end, roll yearly totals into average-annual totals. | When `time%end_yr == 1`, add the yearly routing-unit and HRU constituent totals into the average-annual accumulators in `rucsb_a` and `ru_hru_csb_a`. |
| 11. Write yearly output when yearly printing is enabled. | If `pco%cs_ru%y == 'y'`, write the year-accumulated routing-unit and HRU constituent totals to unit 6074. |
| 12. Optionally write a yearly CSV record. | If `pco%csvout == 'y'`, write the yearly constituent record to unit 6075 in CSV format. |
| 13. Clear yearly accumulators after the year-end report. | Reset the yearly routing-unit and HRU constituent arrays to zero so the next simulation year starts empty. |
| 14. At simulation end, compute and write average-annual output. | If `time%end_sim == 1` and average-annual output is enabled, divide the accumulated annual totals by `time%nbyr` and write the final average-annual records to units 6076 and 6077. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%cs_ru%d, pco%csvout, pco%cs_ru%m, pco%cs_ru%y, pco%cs_ru%a` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%ru` |
| [sym:cs_module] | `ru_hru_csb_m, ru_hru_csb_d, ru_hru_csb_y, ru_hru_csb_a` | `ru_hru_csb_m(iru)%cs(ics)%sedm, ru_hru_csb_d(iru)%cs(ics)%sedm, ru_hru_csb_m(iru)%cs(ics)%wtsp, ru_hru_csb_d(iru)%cs(ics)%wtsp, ru_hru_csb_m(iru)%cs(ics)%irsw, ru_hru_csb_d(iru)%cs(ics)%irsw, ru_hru_csb_m(iru)%cs(ics)%irgw, ru_hru_csb_d(iru)%cs(ics)%irgw, ru_hru_csb_m(iru)%cs(ics)%irwo, ru_hru_csb_d(iru)%cs(ics)%irwo, ru_hru_csb_m(iru)%cs(ics)%rain, ru_hru_csb_d(iru)%cs(ics)%rain, ru_hru_csb_m(iru)%cs(ics)%dryd, ru_hru_csb_d(iru)%cs(ics)%dryd, ru_hru_csb_m(iru)%cs(ics)%fert, ru_hru_csb_d(iru)%cs(ics)%fert, ru_hru_csb_m(iru)%cs(ics)%uptk, ru_hru_csb_d(iru)%cs(ics)%uptk, ru_hru_csb_m(iru)%cs(ics)%rctn, ru_hru_csb_d(iru)%cs(ics)%rctn, ru_hru_csb_m(iru)%cs(ics)%sorb, ru_hru_csb_d(iru)%cs(ics)%sorb, ru_hru_csb_y(iru)%cs(ics)%sedm, ru_hru_csb_y(iru)%cs(ics)%wtsp, ru_hru_csb_y(iru)%cs(ics)%irsw, ru_hru_csb_y(iru)%cs(ics)%irgw, ru_hru_csb_y(iru)%cs(ics)%irwo, ru_hru_csb_y(iru)%cs(ics)%rain, ru_hru_csb_y(iru)%cs(ics)%dryd, ru_hru_csb_y(iru)%cs(ics)%fert, ru_hru_csb_y(iru)%cs(ics)%uptk, ru_hru_csb_y(iru)%cs(ics)%rctn, ru_hru_csb_y(iru)%cs(ics)%sorb, ru_hru_csb_a(iru)%cs(ics)%sedm, ru_hru_csb_a(iru)%cs(ics)%wtsp, ru_hru_csb_a(iru)%cs(ics)%irsw, ru_hru_csb_a(iru)%cs(ics)%irgw, ru_hru_csb_a(iru)%cs(ics)%irwo, ru_hru_csb_a(iru)%cs(ics)%rain, ru_hru_csb_a(iru)%cs(ics)%dryd, ru_hru_csb_a(iru)%cs(ics)%fert, ru_hru_csb_a(iru)%cs(ics)%uptk, ru_hru_csb_a(iru)%cs(ics)%rctn, ru_hru_csb_a(iru)%cs(ics)%sorb` |
| [sym:constituent_mass_module] | `cs_db, rucsb_m, rucsb_d, rucsb_y, rucsb_a` | `cs_db%num_cs, rucsb_m(iru)%hd(ihyd)%cs(ics), rucsb_d(iru)%hd(ihyd)%cs(ics), rucsb_d(iru)%hd(1)%cs(ics), rucsb_d(iru)%hd(2)%cs(ics), rucsb_d(iru)%hd(3)%cs(ics), rucsb_d(iru)%hd(4)%cs(ics), rucsb_d(iru)%hd(5)%cs(ics), rucsb_y(iru)%hd(ihyd)%cs(ics), rucsb_m(iru)%hd(1)%cs(ics), rucsb_m(iru)%hd(2)%cs(ics), rucsb_m(iru)%hd(3)%cs(ics), rucsb_m(iru)%hd(4)%cs(ics), rucsb_m(iru)%hd(5)%cs(ics), rucsb_a(iru)%hd(ihyd)%cs(ics), rucsb_y(iru)%hd(1)%cs(ics), rucsb_y(iru)%hd(2)%cs(ics), rucsb_y(iru)%hd(3)%cs(ics), rucsb_y(iru)%hd(4)%cs(ics), rucsb_y(iru)%hd(5)%cs(ics), rucsb_a(iru)%hd(1)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rucsb_m(iru)%hd(ihyd)%cs(ics)` | Every call, before the daily output is written. | `rucsb_m(iru)%hd(ihyd)%cs(ics)` is incremented by the day’s `rucsb_d(iru)%hd(ihyd)%cs(ics)` for each constituent and hydrograph pathway, so the monthly total-out, percolation, runoff, lateral-flow, and tile-flow sums accumulate across days. |
| `ru_hru_csb_m(iru)%cs(ics)%sedm` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%sedm` is increased by the day’s HRU sediment-associated constituent mass, building the monthly sediment flux total used in monthly output and later rollups. |
| `ru_hru_csb_m(iru)%cs(ics)%wtsp` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%wtsp` is increased by the day’s wetland seepage constituent mass, contributing to the monthly HRU constituent totals. |
| `ru_hru_csb_m(iru)%cs(ics)%irsw` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%irsw` is increased by the day’s surface-water irrigation constituent mass, so the monthly total includes irrigation-derived loading. |
| `ru_hru_csb_m(iru)%cs(ics)%irgw` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%irgw` is increased by the day’s groundwater irrigation constituent mass, contributing to the monthly total for that flux source. |
| `ru_hru_csb_m(iru)%cs(ics)%irwo` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%irwo` is increased by the day’s external irrigation constituent mass, so the monthly balance includes off-watershed irrigation inputs. |
| `ru_hru_csb_m(iru)%cs(ics)%rain` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%rain` is increased by the day’s rainfall-associated constituent mass, accumulating the monthly atmospheric input from rain. |
| `ru_hru_csb_m(iru)%cs(ics)%dryd` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%dryd` is increased by the day’s dry-deposition constituent mass, accumulating the monthly atmospheric deposition input. |
| `ru_hru_csb_m(iru)%cs(ics)%fert` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%fert` is increased by the day’s fertilizer-associated constituent mass, building the monthly fertilizer input total. |
| `ru_hru_csb_m(iru)%cs(ics)%uptk` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%uptk` is increased by the day’s plant uptake constituent mass, so the monthly balance tracks crop removal. |
| `ru_hru_csb_m(iru)%cs(ics)%rctn` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%rctn` is increased by the day’s reaction-transfer constituent mass, accumulating chemical reaction effects for the month. |
| `ru_hru_csb_m(iru)%cs(ics)%sorb` | Every call, before the daily output is written. | `ru_hru_csb_m(iru)%cs(ics)%sorb` is increased by the day’s sorption-transfer constituent mass, accumulating the month’s sorption-related flux. |
| `rucsb_d(iru)%hd(ihyd)%cs(ics)` | At month end, when `time%end_mo == 1`. | `rucsb_d(iru)%hd(ihyd)%cs(ics)` is reset to zero after the daily output has been rolled up into monthly totals, clearing the daily hydrograph state for the next day. |
| `ru_hru_csb_d(iru)%cs(ics)%sedm` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%sedm` is reset to zero after its monthly contribution has been added to the yearly total, clearing the daily HRU state. |
| `ru_hru_csb_d(iru)%cs(ics)%wtsp` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%wtsp` is reset to zero after being rolled into yearly totals, so the next month starts with no daily carryover. |
| `ru_hru_csb_d(iru)%cs(ics)%irsw` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%irsw` is reset to zero after monthly-to-yearly accumulation, clearing the daily irrigation input state. |
| `ru_hru_csb_d(iru)%cs(ics)%irgw` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%irgw` is reset to zero after monthly-to-yearly accumulation, clearing the daily groundwater-irrigation state. |
| `ru_hru_csb_d(iru)%cs(ics)%irwo` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%irwo` is reset to zero after monthly-to-yearly accumulation, clearing the daily external-irrigation state. |
| `ru_hru_csb_d(iru)%cs(ics)%rain` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%rain` is reset to zero after monthly-to-yearly accumulation, clearing the daily rainfall input state. |
| `ru_hru_csb_d(iru)%cs(ics)%dryd` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%dryd` is reset to zero after monthly-to-yearly accumulation, clearing the daily dry-deposition input state. |
| `ru_hru_csb_d(iru)%cs(ics)%fert` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%fert` is reset to zero after monthly-to-yearly accumulation, clearing the daily fertilizer input state. |
| `ru_hru_csb_d(iru)%cs(ics)%uptk` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%uptk` is reset to zero after monthly-to-yearly accumulation, clearing the daily uptake state. |
| `ru_hru_csb_d(iru)%cs(ics)%rctn` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%rctn` is reset to zero after monthly-to-yearly accumulation, clearing the daily reaction state. |
| `ru_hru_csb_d(iru)%cs(ics)%sorb` | At month end, when `time%end_mo == 1`. | `ru_hru_csb_d(iru)%cs(ics)%sorb` is reset to zero after monthly-to-yearly accumulation, clearing the daily sorption state. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f as a new subroutine for routing-unit constituent output. Commit 39fabde initialized the local counters `iob`, `ics`, and `ihyd` to zero. Commit f1e61a3 kept the logic unchanged but fixed formatting in the comments and indentation. Commit 2fe89fd changed the CSV write format specifier from `G0.3` to `G0.6` in the daily, monthly, yearly, and average-annual CSV outputs.

- df07e3f added the full `ru_cs_output` routine, including daily/monthly/yearly/average-annual accumulation, output writes, and zeroing of the period accumulators.
- 39fabde initialized the local loop counters `iob`, `ics`, and `ihyd` at declaration, making their starting values explicit.
- 2fe89fd increased CSV numeric precision for units 6071, 6073, 6075, and 6077 by changing the format from `G0.3` to `G0.6`.
- f1e61a3 made only formatting/comment alignment changes and did not alter the procedure’s behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ru_cs_output' has no extracted documentation comment.
