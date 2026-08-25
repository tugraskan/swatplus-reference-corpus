---
kind: procedure
symbol: hru_lte_output
title: hru_lte_output
status: filled
source_hash: 9523ca412842e215
version_label: SWAT+ 62.0.0
args:
  isd: '`isd` is the HRU-LTE sequence number being processed on this call. The routine uses
    it to index the per-HRU-LTE output arrays and to derive the matching hydrograph object
    index via `sp_ob1%hru_lte + isd - 1`.'
locals:
  iob: '`iob` holds the object-connectivity index for the current HRU-LTE element. It starts
    at 0 and is set from `sp_ob1%hru_lte + isd - 1` so the routine can fetch `ob(iob)%gis_id`
    and `ob(iob)%name` for output records.'
  const: '`const` is a temporary real scaler used when normalizing accumulated monthly and
    yearly values to averages. It is assigned the number of days in the month or the number
    of days in the year, then used as the divisor in the type-defined averaging operation.'
uses:
  time_module: '`time_module` supplies the simulation clock and boundary flags that decide
    when this routine writes daily, monthly, yearly, and average-annual records. The day,
    month, year, and end-of-period indicators also provide the date fields stored in each
    output line.'
  basin_module: '`basin_module` provides the print-control flags that turn each HRU-LTE output
    class on or off, including daily/monthly/yearly/average-annual settings and CSV output
    mode. Without `pco`, the routine would not know which summary files to write.'
  output_landscape_module: '`output_landscape_module` contains the HRU-LTE accumulation arrays
    and zero-state templates that this routine updates and resets. Those arrays are the actual
    water-balance, nutrient-balance, losses, and plant-weather states being reported.'
  hydrograph_module: '`hydrograph_module` provides the spatial object numbering and object
    metadata used to map `isd` to the correct HRU-LTE object and label each output row. It
    matters because the routine writes `ob(iob)%gis_id` and `ob(iob)%name` alongside the summarized
    values.'
---

<!-- facts:header -->

Accumulates HRU-LTE daily outputs into monthly, yearly, and average-annual summaries, and writes those summaries to the configured output units.

## Bottom Line

`hru_lte_output` is the HRU-LTE reporting routine. Each call identifies the object index for one HRU-LTE element, adds the current day’s water balance, nutrient balance, losses, and plant-weather values into the running monthly totals, and then conditionally writes daily output records if daily printing is enabled.

At month end, year end, and simulation end, it rolls the accumulated values into yearly and average-annual totals, prints the enabled summaries, and then resets the lower-period accumulators back to their zero-state templates. The routine matters because it is the point where HRU-LTE results become the model’s reportable output streams.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine once for each HRU-LTE object in its `do isd = 1, sp_ob%hru_lte` loop. The routine assumes the simulation clock, print-control flags, and output arrays have already been prepared elsewhere, and later reporting depends on the accumulated monthly, yearly, and average-annual values it writes and resets.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the HRU-LTE sequence number to the object index. | Initialize the local object index from `sp_ob1%hru_lte + isd - 1` so the routine can look up the matching HRU-LTE metadata in `ob(iob)`. |
| 2. Accumulate the current day into monthly totals. | Add the day-level water balance, nutrient balance, losses, and plant-weather values into the month accumulators for this HRU-LTE. |
| 3. Write daily outputs when daily printing is enabled. | If daily printing is active for the current interval, write the enabled daily water-balance, losses, and plant-weather records, including CSV copies when requested. |
| 4. Roll monthly totals into yearly totals at month end. | When `time%end_mo == 1`, add the month accumulators into the yearly accumulators for water balance, nutrient balance, losses, and plant weather. |
| 5. Normalize selected monthly accumulators for reporting and print month-end summaries. | Compute the number of days in the month, scale the monthly water-balance and plant-weather totals by that month length, write any enabled monthly summary records, then restore the monthly accumulators to their zero-state templates. |
| 6. Roll yearly totals into average-annual totals at year end. | When `time%end_yr == 1`, add the year accumulators into the average-annual accumulators for water balance, nutrient balance, losses, and plant weather. |
| 7. Normalize selected yearly accumulators and print year-end summaries. | Use the year length to average selected yearly values, then write any enabled yearly summary records for water balance, losses, and plant weather. |
| 8. Produce simulation-average water-balance output at the end of the run. | At simulation end, divide the accumulated water-balance total by the printed years and days, write the average-annual water-balance record, and reset the average-annual water-balance state to `hwbz`. |
| 9. Produce simulation-average losses output at the end of the run. | At simulation end, average the accumulated losses total by the printed years, write the average-annual losses record, and reset the average-annual losses state to `hlsz`. |
| 10. Produce simulation-average plant-weather output at the end of the run. | At simulation end, divide the accumulated plant-weather total by the printed years and days, write the average-annual plant-weather record, and reset the average-annual plant-weather state to `hpwz`. |
| 11. Return to the caller after all enabled outputs are handled. | Finish the subroutine after the formatted write statements and format definitions. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%wb_sd%d, pco%csvout, pco%ls_sd%d, pco%pw_sd%d, pco%wb_sd%m, pco%ls_sd%m, pco%pw_sd%m, pco%wb_sd%y, pco%ls_sd%y, pco%pw_sd%y, pco%wb_sd%a, pco%ls_sd%a, pco%pw_sd%a` |
| [sym:output_landscape_module] | `hltwb_m, hltwb_d, hltnb_m, hltnb_d, hltls_m, hltls_d, hltpw_m, hltpw_d, hltwb_y, hltnb_y, hltls_y, hltpw_y, hltwb_a, hltnb_a, hltls_a, hltpw_a, hwbz, hnbz, hpwz, hlsz` |  |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru_lte, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hltwb_m(isd)` | Every call, before any period checks. | `hltwb_m(isd)` is increased by the current day’s water-balance output so the routine can build the month total for this HRU-LTE. |
| `hltnb_m(isd)` | Every call, before any period checks. | `hltnb_m(isd)` is increased by the current day’s nutrient-balance output so the month accumulation is preserved for later reporting. |
| `hltls_m(isd)` | Every call, before any period checks. | `hltls_m(isd)` is increased by the current day’s losses output so the month accumulation is preserved for later reporting. |
| `hltpw_m(isd)` | Every call, before any period checks. | `hltpw_m(isd)` is increased by the current day’s plant-weather output so the month accumulation is preserved for later reporting. |
| `hltwb_y(isd)` | When `time%end_mo == 1`. | `hltwb_y(isd)` receives the completed month’s water-balance total so yearly accumulation can continue after the month closes. |
| `hltnb_y(isd)` | When `time%end_mo == 1`. | `hltnb_y(isd)` receives the completed month’s nutrient-balance total so yearly accumulation can continue after the month closes. |
| `hltls_y(isd)` | When `time%end_mo == 1`. | `hltls_y(isd)` receives the completed month’s losses total so yearly accumulation can continue after the month closes. |
| `hltpw_y(isd)` | When `time%end_mo == 1`. | `hltpw_y(isd)` receives the completed month’s plant-weather total so yearly accumulation can continue after the month closes. |
| `hltwb_a(isd)` | When `time%end_yr == 1`. | `hltwb_a(isd)` receives the completed year’s water-balance total so average-annual accumulation can continue after the year closes. |
| `hltnb_a(isd)` | When `time%end_yr == 1`. | `hltnb_a(isd)` receives the completed year’s nutrient-balance total so average-annual accumulation can continue after the year closes. |
| `hltls_a(isd)` | When `time%end_yr == 1`. | `hltls_a(isd)` receives the completed year’s losses total so average-annual accumulation can continue after the year closes. |
| `hltpw_a(isd)` | When `time%end_yr == 1`. | `hltpw_a(isd)` receives the completed year’s plant-weather total so average-annual accumulation can continue after the year closes. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was introduced in commit df07e3f as a new source file that already contained the daily, monthly, yearly, and average-annual HRU-LTE output logic. Commit 39fabde initialized the local variables `iob` and `const` to zero and zero-point-zero without changing the output flow. Commit 2fe89fd updated the CSV writes from `G0.3` to `G0.6` formatting in the active daily, monthly, yearly, and average-annual CSV branches, including the commented-out nutrient CSV lines.

- df07e3f added the full `hru_lte_output` subroutine and its period-based accumulation and write logic.
- 39fabde only changed local-variable initialization (`iob = 0`, `const = 0.`) and did not alter the routine’s output behavior.
- 2fe89fd changed CSV formatting precision from `G0.3` to `G0.6` for the active CSV output branches, affecting how exported numeric values are rendered.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_lte_output' has no extracted documentation comment.
