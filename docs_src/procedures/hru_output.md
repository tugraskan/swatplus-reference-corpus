---
kind: procedure
symbol: hru_output
title: hru_output
status: filled
source_hash: 7cc3f6835e75e00f
version_label: SWAT+ 62.0.0
args:
  ihru: Selects the HRU index to process. The routine copies this into `j` and uses it to
    access the HRU, land-use, output, and object records for that one HRU.
locals:
  idp: Plant index used when writing crop-yield summaries; it is set from `pcom(j)%plcur(ipl)%idplt`
    inside the end-of-simulation yield loop.
  j: Working HRU index; initialized from `ihru` and used throughout the routine to index HRU
    state and output arrays.
  iob: Object-connectivity index for the current HRU; computed as `sp_ob1%hru + j - 1` so
    the routine can fetch `ob(iob)%gis_id` and `ob(iob)%name` for output rows.
  ipl: Loop index over plants in the current HRU community when writing average annual crop
    yields.
  ilu: Land-use-management index for the current HRU; taken from `hru(j)%land_use_mgt` and
    used to fetch `lum(ilu)%plant_cov` and `lum(ilu)%mgt_ops` for output labels.
  bm_max_m: Temporary storage for monthly maximum biomass so `hpw_m(j)%bm_max` can be preserved
    across monthly accumulation and reset logic.
  bm_max_y: Temporary storage for yearly maximum biomass so `hpw_y(j)%bm_max` can be preserved
    across yearly accumulation and reset logic.
  bm_max_a: Temporary storage for annual maximum biomass so `hpw_a(j)%bm_max` can be restored
    before annual plant-weather output.
  const: Scaling factor used when converting accumulated monthly or yearly totals to averages;
    set to the number of days in the month or to `time%day_end_yr`.
  sw_init: Temporary storage for initial soil-water value before resetting annual water-balance
    state.
  sno_init: Temporary storage for initial snow-pack value before resetting annual water-balance
    state.
  percn_aa: Average annual percolation/leaching summary used only for the annual losses output
    row; computed from `hpw_a(j)%percn / time%yrs_prt`.
uses:
  plant_module: Provides the plant name written in the crop-yield output rows at the end of
    the simulation.
  plant_data_module: Provides the plant-community structure used to loop over crops and compute
    average harvested yield per plant.
  time_module: Controls when daily, monthly, yearly, and average-annual branches run and supplies
    the date fields written to output.
  basin_module: Holds the print-code switches that decide which HRU output branches are written
    and whether CSV companion files are produced.
  output_landscape_module: Supplies the HRU output accumulator arrays and zero-state templates
    that are summed, averaged, reset, and written by this routine.
---

<!-- facts:header -->

Writes HRU water, nutrient, losses, plant-weather, carbon snapshot, and crop-yield outputs at daily, monthly, yearly, and average-annual reporting points.

## Bottom Line

`hru_output` is the HRU-level reporting routine. It gathers daily accumulations into monthly, yearly, and average-annual summaries, then writes the requested records for water balance, nutrient balance, losses, plant weather, soil carbon snapshots, and crop yields based on the print codes in `pco` and the current simulation time.

It matters because this is where HRU state is turned into the model's standard output files. It also updates a few downstream flags and summary fields, including irrigation status, annual precipitation/flow summaries, and the values passed to the soil carbon snapshot writers.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `command` after each HRU is simulated, to write that HRU's output records. It reflects the daily HRU state accumulators (`hwb_d`, `hnb_d`, `hls_d`, `hpw_d`, etc.) into the HRU output files and rolls them up into monthly, yearly, and average-annual totals. It only writes; it does not change model state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Accumulate daily into monthly | Resolve the HRU index, its spatial object and its land-use record, then add the daily water balance, nutrient balance, losses and plant/weather structures into their monthly accumulators. Maximum biomass is handled separately at every level: the monthly, yearly and annual `bm_max` values are saved before the summation and restored afterwards, then each is raised to the running maximum of today's biomass, because `bm_max` is a peak rather than a quantity that should be summed. Finally set the final soil water and snowpack from current state and report each as the mean of its initial and final value. |
| 2. Write daily records | On a daily print step, write the water balance, nutrient balance, losses and plant/weather records to units 2000, 2020, 2030 and 2040, each guarded by its own `pco%*_hru%d` flag and each mirrored to a CSV unit (2004, 2024, 2034, 2044) when CSV output is enabled. Every record carries the date, HRU number, GIS id, object name and the land use's plant cover and management schedule. Between the water balance and nutrient balance writes, the day's final soil water and snowpack are rolled forward into the next interval's initial values at `hru_output.f90:71-72` — inside this print block, so the baseline only advances on days the model actually prints. |
| 3. Accumulate monthly into yearly | At end of month, add the monthly water balance, nutrient balance, losses and plant/weather totals into the yearly accumulators, preserving the yearly `bm_max` peak across the summation. Then convert the monthly plant/weather and water balance structures from sums to daily means by dividing by the number of days in the month, and restore the monthly `bm_max` that the division would otherwise have scaled. |
| 4. Write monthly records and reset | Carry the daily final soil water and snowpack onto the monthly record, then write the four monthly outputs to units 2001, 2021, 2031 and 2041 under their `pco%*_hru%m` flags, with CSV mirrors on 2005, 2025, 2035 and 2045. The monthly plant/weather record takes its plant N and P from the current community mass rather than from the accumulator. Afterwards zero all four monthly structures, carrying the final soil water and snowpack forward as the next month's initial values. |
| 5. Accumulate yearly into annual | At end of year, add the yearly structures into the average-annual accumulators, then convert the yearly water balance and plant/weather structures to daily means by dividing by the number of days in the year. Restore both the yearly and annual `bm_max` peaks afterwards so the division does not scale them. |
| 6. Write yearly records | Set the yearly final soil water and snowpack from the daily values and flag the HRU as irrigated for soft calibration when average-annual irrigation exceeds 10 mm. Write the four yearly outputs to units 2002, 2022, 2032 and 2042 under their `pco%*_hru%y` flags with CSV mirrors on 2006, 2026, 2036 and 2046, again taking plant N and P for the plant/weather record from the current community mass. Clear the yearly maximum biomass at the end. |
| 7. Average and write annual water balance | At end of simulation, convert the annual water balance to a per-year then per-day mean using the printed year and day counts, preserving the initial soil water and snowpack across the division and taking final values from the daily record. Write it to unit 2003 under `pco%wb_hru%a` with a CSV mirror on 2007. Then publish the HRU's long-term means for later use — average annual precipitation and the five-element flow vector holding water yield, percolation, surface runoff, lateral flow and tile flow — and zero the accumulator. |
| 8. Average and write remaining annual records | Average and write the remaining three average-annual records, each guarded by end of simulation and its own annual print flag: nutrient balance to unit 2023, losses to 2033 with a separately averaged percolated-nitrogen term, and plant/weather to 2043 with the current community N and P and the restored maximum biomass. Each is written with a CSV mirror and then zeroed, and the plant/weather branch publishes the HRU's aeration stress for later use. |
| 9. Write end-of-simulation soil snapshots | Write the end-of-simulation soil nutrient and carbon snapshots. Both `soil_nutcarb_write` and `soil_nutcarb_write_legacy` iterate every HRU internally, so each is called only when `j == 1`; calling them per-HRU previously produced sp_ob%hru-squared rows in `hru_soil_snap_tot.txt`. The first is gated by the `cb_snap_hru` annual flag, the second by any non-`n` `cb_hru` row in print.prt. |
| 10. Write average annual crop yields | When average-annual crop yield output is selected, divide each plant's accumulated yield by its harvest count to give a mean yield per harvest, then write one record per plant in the community to unit 4008, with a CSV mirror on 4009, labelled with the plant name from the plant database. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_module] | `pldb` | `pldb(idp)%plantnm` |
| [sym:plant_data_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%harv_num` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%wb_hru%d, pco%csvout, pco%nb_hru%d, pco%ls_hru%d, pco%pw_hru%d, pco%wb_hru%m, pco%nb_hru%m, pco%ls_hru%m, pco%pw_hru%m, pco%wb_hru%y, pco%nb_hru%y, pco%ls_hru%y, pco%pw_hru%y, pco%wb_hru%a` |
| [sym:output_landscape_module] | `hwb_d, hwb_m, hwb_y, hwb_a, hnb_d, hnb_m, hnb_y, hnb_a, hls_d, hls_m, hls_y, hls_a, hpw_d, hpw_m, hpw_y, hpw_a, hwbz, hnbz, hlsz, hpwz` | `hwb_d(j)%sw_init, hwb_d(j)%sw_final, hwb_d(j)%sw, hwb_d(j)%sno_init, hwb_d(j)%sno_final, hwb_d(j)%snopack, hwb_m(j)%sw_init, hwb_m(j)%sw_final, hwb_m(j)%sno_init, hwb_m(j)%sno_final, hwb_y(j)%sw_final, hwb_y(j)%sno_final, hwb_a(j)%sw_init, hwb_a(j)%sw_final, hwb_a(j)%sno_init, hwb_a(j)%sno_final, hpw_d(j)%bioms, hpw_d(j)%bm_max, hpw_m(j)%bm_max, hpw_m(j)%nplnt, hpw_m(j)%pplnt, hpw_y(j)%bm_max, hpw_y(j)%nplnt, hpw_y(j)%pplnt, hpw_a(j)%bm_max, hpw_a(j)%nplnt, hpw_a(j)%pplnt, hls_d(j), hls_m(j), hls_y(j), hls_a(j), hnb_d(j), hnb_m(j), hnb_y(j), hnb_a(j), hwbz, hnbz, hlsz, hpwz` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hwb_m(j)` | Every call, before any print check. | Daily HRU water balance is added into the monthly accumulator at `hru_output.f90:42`. It is later converted to a daily mean by dividing by the days in the month at `hru_output.f90:113`, and zeroed to `hwbz` at `hru_output.f90:162` once the monthly record has been written. |
| `hnb_m(j)` | Every call. | Daily nutrient balance is added into the monthly accumulator at `hru_output.f90:43`. Unlike the water balance it is not divided by days in the month — it stays a monthly total — and is zeroed to `hnbz` at `hru_output.f90:165`. |
| `hls_m(j)` | Every call. | Daily losses (sediment, organic and mineral nutrient export) are added into the monthly accumulator at `hru_output.f90:44` and zeroed to `hlsz` at `hru_output.f90:167`. Also a monthly total rather than a mean. |
| `hpw_m(j)` | Every call. | Daily plant and weather variables are added into the monthly accumulator at `hru_output.f90:48`, converted to a daily mean at `hru_output.f90:112`, and zeroed to `hpwz` at `hru_output.f90:166`. |
| `hpw_m(j)%bm_max` | Every call, and again at end of month. | Monthly peak biomass. Saved before the monthly summation and restored after it (`hru_output.f90:45, 49`) so it is not summed, then raised to today's biomass at `hru_output.f90:51`. Saved and restored a second time around the days-in-month division at `hru_output.f90:103, 115` so the division does not scale a peak. |
| `hpw_d(j)%bm_max` | Every call, and again before the daily plant/weather write. | Set to the day's biomass at `hru_output.f90:50` so the daily record reports today's value rather than a carried-over peak; set again at `hru_output.f90:91` immediately before the daily plant/weather write. |
| `hpw_y(j)%bm_max` | Every call, and again at end of year. | Yearly peak biomass, raised to today's biomass at `hru_output.f90:52`. Saved and restored around both the monthly accumulation (`hru_output.f90:107, 109`) and the days-in-year division (`hru_output.f90:172, 182`), then cleared to zero at `hru_output.f90:229` once the yearly record is written. |
| `hpw_a(j)%bm_max` | Every call, and again at end of year and end of simulation. | Average-annual peak biomass, raised to today's biomass at `hru_output.f90:53`, restored after the yearly accumulation at `hru_output.f90:183`, and restored once more before the average-annual plant/weather write at `hru_output.f90:293`. |
| `hwb_d(j)%sw_final` | Every call. | Set from the current soil profile water content at `hru_output.f90:55`, closing the day's water balance. Also copied onto the monthly, yearly and annual records at `hru_output.f90:118, 186, 241`. |
| `hwb_d(j)%sw` | Every call. | Reported daily soil water is the mean of the day's initial and final values (`hru_output.f90:56`), not the end-of-day snapshot, so the printed value represents the day rather than its final instant. |
| `hwb_d(j)%sno_final` | Every call. | Set from the HRU's snow water equivalent at `hru_output.f90:57` and propagated to the monthly, yearly and annual records at `hru_output.f90:119, 187, 243`. |
| `hwb_d(j)%snopack` | Every call. | Reported daily snowpack is the mean of the day's initial and final snow water equivalent (`hru_output.f90:58`), matching the treatment of soil water. |
| `hwb_d(j)%sw_init` | Only on a daily print step. | Rolled forward from the day's final soil water at `hru_output.f90:71`. Because this assignment sits inside the daily-print block, the roll-forward only happens on days the model prints, which ties the initial-value baseline to the print interval. |
| `hwb_d(j)%sno_init` | Only on a daily print step. | Rolled forward from the day's final snow water equivalent at `hru_output.f90:72`, inside the same daily-print block and subject to the same coupling to the print interval. |
| `hwb_y(j)` | End of month. | Monthly water balance is added into the yearly accumulator at `hru_output.f90:104`, converted to a daily mean by dividing by the days in the year at `hru_output.f90:179`, and carried into the annual accumulator at `hru_output.f90:173`. |
| `hnb_y(j)` | End of month. | Monthly nutrient balance is added into the yearly accumulator at `hru_output.f90:105` and carried into the annual accumulator at `hru_output.f90:174`; it is not divided by days. |
| `hls_y(j)` | End of month. | Monthly losses are added into the yearly accumulator at `hru_output.f90:106` and carried into the annual accumulator at `hru_output.f90:175`; also not divided by days. |
| `hpw_y(j)` | End of month. | Monthly plant and weather values are added into the yearly accumulator at `hru_output.f90:108`, converted to a daily mean at `hru_output.f90:180`, and carried into the annual accumulator at `hru_output.f90:176`. |
| `hwb_m(j)%sw_final` | End of month. | Taken from the daily final soil water at `hru_output.f90:118` so the monthly record closes on the same value the day did, then used at `hru_output.f90:160` as the next month's initial soil water. |
| `hwb_m(j)%sno_final` | End of month. | Taken from the daily final snow water equivalent at `hru_output.f90:119` and used at `hru_output.f90:161` as the next month's initial snowpack. |
| `hpw_m(j)%nplnt` | End of month, when monthly plant/weather output is on. | Overwritten at `hru_output.f90:149` with the plant community's current total nitrogen mass immediately before the write, so the monthly record reports a month-end standing value rather than an average of daily values. |
| `hpw_m(j)%pplnt` | End of month, when monthly plant/weather output is on. | Overwritten at `hru_output.f90:150` with the plant community's current total phosphorus mass, on the same month-end-snapshot basis as `nplnt`. |
| `hwb_m(j)%sw_init` | End of month, after the monthly record is written. | Restored at `hru_output.f90:163` from the value saved at `hru_output.f90:160`, so zeroing the monthly structure does not lose the soil water baseline that the next month's mean depends on. |
| `hwb_m(j)%sno_init` | End of month, after the monthly record is written. | Restored at `hru_output.f90:164` from the value saved at `hru_output.f90:161`, preserving the snowpack baseline across the monthly reset. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_output.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 19 non-merge commit(s) since, most recently `821a63e` (2026-06-02, "reinstate CSU outputs and print flags"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_output.f90` are listed.

- `821a63e` (2026-06-02) — reinstate CSU outputs and print flags
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `2fe89fd` (2026-04-21) — CSV output file fixes
- `96d5513` (2026-02-10) — Fixed fomat for percn in hru_ls
- `2cd7698` (2026-02-03) — Changes made to increase field width plus a space when writing out output losses in the file hru_ls_[day, mon, yr]
- `df07e3f` (2024-03-05) — init all

## Review Notes

- This overlay was rebuilt rather than edited. The batch fill returned a truncated object: eight required keys were absent entirely (dependency_graph, calls_graph, called_by_graph, core_graph, state_changes, summary_variables, state_flow_graph, evidence) and only 4 of the algorithm_steps survived, two of which overlapped at line 260. The request set max_output_tokens to 20000, which is the most likely cause. The parser-owned keys were restored verbatim from the packet's own Draft Overlay Skeleton; state_changes and summary_variables arrived with all 24 entries still unfilled placeholders and were authored from the source block.
- algorithm_steps revised: replaced the 4 surviving steps (two of which overlapped) with 10 contiguous, non-overlapping spans across hru_output.f90:37-346, one per accumulate/print/reset phase. The soil water and snowpack roll-forward at hru_output.f90:71-72 is described inside the daily-print step rather than given its own step, because it physically sits inside `if (pco%day_print == "y" ...)` and a nested span would be swallowed by the enclosing step in the renderer's range lookup.
- Behavioral note worth a modeller's eye: `hwb_d(j)%sw_init` and `sno_init` are advanced at `hru_output.f90:71-72`, inside the daily-print block. On a run with `pco%int_day > 1` the baseline is therefore only advanced on print steps, so the reported daily mean soil water and snowpack average across the whole print interval rather than across one day. This is the source's actual behavior, not a transcription error.
- The two callees are each guarded by `j == 1` because they iterate all HRUs internally; the source comment at `hru_output.f90:306-308` records that calling them per-HRU previously produced sp_ob%hru-squared rows in hru_soil_snap_tot.txt.
- Water balance and plant/weather structures are converted to daily means with the `//` operator, but nutrient balance and losses are not — they remain period totals. The `bm_max` fields are saved and restored around every summation and division so a peak is never summed or averaged.
- File I/O verified against the source: 34 write statements, no reads, opens, closes or rewinds. Units 2000-2007, 2020-2027, 2030-2037 and 2040-2047 carry the water balance, nutrient balance, losses and plant/weather records at daily, monthly, yearly and average-annual steps, with the higher unit in each block being the CSV mirror written when `pco%csvout == "y"`. Units 4008 and 4009 carry average annual crop yields.
- `hru_output` has a PURPOSE header at `hru_output.f90:34-35` but no per-declaration documentation comments.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
