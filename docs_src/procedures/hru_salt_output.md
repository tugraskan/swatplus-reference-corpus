---
kind: procedure
symbol: hru_salt_output
title: hru_salt_output
status: filled
source_hash: c79f16d1324d1ac4
version_label: SWAT+ 62.0.0
args:
  ihru: '`ihru` identifies the HRU currently being reported. The routine copies it into `j`
    and uses that HRU index to select the matching salt-balance entries in `hsaltb_d`, `hsaltb_m`,
    `hsaltb_y`, and `hsaltb_a`, and to locate the corresponding object id through `sp_ob1%hru
    + j - 1`.'
locals:
  j: HRU index used throughout the routine. It is initialized to 0, set from `ihru`, and then
    used to index the HRU-specific salt balance arrays and the matching object connectivity
    entry.
  const: Temporary day-count divisor used when converting accumulated monthly totals to monthly
    averages. It is set from the number of days in the current month and used only in the
    monthly branch.
  iob: Index into the hydrograph object list for the current HRU. It is derived from `sp_ob1%hru
    + j - 1` and used to fetch `ob(iob)%gis_id` for the output rows.
  isalt: Loop counter over salt ions. It is used to walk from 1 to `cs_db%num_salts` while
    accumulating and printing the per-ion salt flux components.
uses:
  time_module: '`time_module` provides the simulation clock fields that decide which period-end
    branches run and what date stamp is written with each record. `time%day`, `time%mo`, `time%day_mo`,
    and `time%yrc` are written to every output row, while `time%end_mo`, `time%end_yr`, and
    `time%end_sim` gate monthly, yearly, and average-annual processing.'
  basin_module: '`basin_module` supplies the print-code switches that enable or disable each
    output stream. `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, and `pco%salt_hru%a`
    determine whether the daily, monthly, yearly, and average-annual salt records are written,
    and `pco%csvout` controls the parallel CSV records.'
  hydrograph_module: '`hydrograph_module` provides the HRU-to-object mapping used to label
    each output line. `sp_ob1%hru` gives the first HRU object number so the routine can compute
    `iob`, and `ob(iob)%gis_id` supplies the GIS identifier written with each record.'
  salt_module: '`salt_module` contains the salt-balance accumulators being updated and reported.
    The routine sums daily values from `hsaltb_d` into `hsaltb_m`, monthly values from `hsaltb_m`
    into `hsaltb_y`, and scales `hsaltb_a` for average annual output, so these module arrays
    are the core data being emitted.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_salts`, which sets
    the loop bounds for every salt-ion vector written here. Without that count, the routine
    would not know how many ion-specific fields to accumulate or print in the repeated list-directed
    output.'
---

<!-- facts:header -->

Aggregates and prints HRU salt loadings and concentrations at daily, monthly, yearly, and average-annual intervals.

## Bottom Line

`hru_salt_output` takes the current HRU's daily salt-balance fluxes, adds them into monthly, yearly, and average-annual accumulators, and writes the selected outputs when the corresponding print codes are enabled. It reports the salt-ion mass pathways tracked in `salt_module` for each HRU and uses `time_module` to decide when period-end summaries should be produced.

The routine matters because it is the HRU-level salt reporting point: daily values are accumulated into `hsaltb_m`, then into `hsaltb_y`, and finally into `hsaltb_a` at the end of the simulation. Those accumulated states are what later monthly, yearly, and average-annual output records print, so this routine controls the salt output files without changing the core transport physics.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine once per HRU when `cs_db%num_salts > 0`, after the daily salt balances have been computed for that HRU and before the rest of the constituent output routines run. Its results feed the model's HRU salt output files and the period accumulators that subsequent monthly, yearly, and average-annual reporting depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the current HRU to object indices | Copy the input HRU index into `j` and compute the corresponding object index `iob` from `sp_ob1%hru + j - 1` so the routine can label output rows with the correct GIS identifier. |
| 2. Add daily salt fluxes into monthly accumulators | Loop over all salt ions and add each daily flux component from `hsaltb_d(j)` into the matching monthly accumulator in `hsaltb_m(j)`. The routine also accumulates dissolved salt mass for ion 1. |
| 3. Write daily HRU salt output when enabled | If `pco%salt_hru%d` is enabled, write the daily salt report to unit 5021 and, when `pco%csvout` is also enabled, write the CSV version to unit 5022. Both records include date fields, HRU id, GIS id, and the daily salt-ion flux arrays from `hsaltb_d(j)`. |
| 4. Roll monthly totals into yearly accumulators at month end | When `time%end_mo == 1`, add the monthly salt totals from `hsaltb_m(j)` into `hsaltb_y(j)` for every salt ion and the dissolved salt term. |
| 5. Compute monthly averages for reporting | Compute `const` as the number of days in the current month and divide the monthly soil and concentration totals in `hsaltb_m(j)` by that day count to form monthly averages. |
| 6. Write monthly HRU salt output when enabled | If `pco%salt_hru%m` is enabled, write the monthly report to unit 5023 and, when `pco%csvout` is enabled, write the CSV version to unit 5024. These records report the month-averaged salt values stored in `hsaltb_m(j)`. |
| 7. Reset monthly accumulators after the month-end report | Zero out the monthly accumulator fields in `hsaltb_y(j)` after the month-end processing so the next month starts with clean yearly-increment inputs from subsequent monthly totals. |
| 8. Roll yearly totals into average-annual accumulators at year end | When `time%end_yr == 1`, add the yearly salt totals from `hsaltb_y(j)` into the average-annual accumulator `hsaltb_a(j)` for every salt ion and dissolved salt term. |
| 9. Write yearly HRU salt output when enabled | If `pco%salt_hru%y` is enabled, write the yearly report to unit 5025 and, when `pco%csvout` is enabled, write the CSV version to unit 5026. These records report the yearly values stored in `hsaltb_y(j)` and then clear the yearly accumulators for the next year. |
| 10. Average annual totals at end of simulation | When `time%end_sim == 1` and average-annual output is enabled, divide the accumulated annual salt totals in `hsaltb_a(j)` by `time%nbyr` to form mean annual values. |
| 11. Write average-annual HRU salt output when enabled | Write the average-annual report to unit 5027 and, when `pco%csvout` is enabled, write the CSV version to unit 5028. These records contain the simulation-average salt values from `hsaltb_a(j)`. |
| 12. Finish the subroutine | Return to the caller after all enabled period outputs and accumulator updates are complete. |
| 13. Daily accumulation of all salt-ion flux components | For each salt ion, accumulate soil, surface runoff, lateral flow, urban runoff, wetland runoff, tile flow, percolation, wetland seepage, irrigation, rainfall, dry deposition, road salt, fertilizer, amendment, uptake, and concentration into the monthly totals. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr` |
| [sym:basin_module] | `pco` | `pco%salt_hru%d, pco%csvout, pco%salt_hru%m` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru` |
| [sym:salt_module] | `hsaltb_m, hsaltb_d, hsaltb_y, hsaltb_a` | `hsaltb_m(j)%salt(isalt)%soil, hsaltb_d(j)%salt(isalt)%soil, hsaltb_m(j)%salt(isalt)%surq, hsaltb_d(j)%salt(isalt)%surq, hsaltb_m(j)%salt(isalt)%latq, hsaltb_d(j)%salt(isalt)%latq, hsaltb_m(j)%salt(isalt)%urbq, hsaltb_d(j)%salt(isalt)%urbq, hsaltb_m(j)%salt(isalt)%wetq, hsaltb_d(j)%salt(isalt)%wetq, hsaltb_m(j)%salt(isalt)%tile, hsaltb_d(j)%salt(isalt)%tile, hsaltb_m(j)%salt(isalt)%perc, hsaltb_d(j)%salt(isalt)%perc, hsaltb_m(j)%salt(isalt)%wtsp, hsaltb_d(j)%salt(isalt)%wtsp, hsaltb_m(j)%salt(isalt)%irsw, hsaltb_d(j)%salt(isalt)%irsw, hsaltb_m(j)%salt(isalt)%irgw, hsaltb_d(j)%salt(isalt)%irgw, hsaltb_m(j)%salt(isalt)%irwo, hsaltb_d(j)%salt(isalt)%irwo, hsaltb_m(j)%salt(isalt)%rain, hsaltb_d(j)%salt(isalt)%rain, hsaltb_m(j)%salt(isalt)%dryd, hsaltb_d(j)%salt(isalt)%dryd, hsaltb_m(j)%salt(isalt)%road, hsaltb_d(j)%salt(isalt)%road, hsaltb_m(j)%salt(isalt)%fert, hsaltb_d(j)%salt(isalt)%fert, hsaltb_m(j)%salt(isalt)%amnd, hsaltb_d(j)%salt(isalt)%amnd, hsaltb_m(j)%salt(isalt)%uptk, hsaltb_d(j)%salt(isalt)%uptk, hsaltb_m(j)%salt(isalt)%conc, hsaltb_d(j)%salt(isalt)%conc, hsaltb_m(j)%salt(1)%diss, hsaltb_d(j)%salt(1)%diss, hsaltb_y(j)%salt(isalt)%soil, hsaltb_y(j)%salt(isalt)%surq, hsaltb_y(j)%salt(isalt)%latq, hsaltb_y(j)%salt(isalt)%urbq, hsaltb_y(j)%salt(isalt)%wetq, hsaltb_y(j)%salt(isalt)%tile, hsaltb_y(j)%salt(isalt)%perc, hsaltb_y(j)%salt(isalt)%wtsp, hsaltb_y(j)%salt(isalt)%irsw, hsaltb_y(j)%salt(isalt)%irgw, hsaltb_y(j)%salt(isalt)%irwo, hsaltb_y(j)%salt(isalt)%rain, hsaltb_y(j)%salt(isalt)%dryd, hsaltb_y(j)%salt(isalt)%road, hsaltb_y(j)%salt(isalt)%fert, hsaltb_y(j)%salt(isalt)%amnd, hsaltb_y(j)%salt(isalt)%uptk, hsaltb_y(j)%salt(isalt)%conc, hsaltb_y(j)%salt(1)%diss, hsaltb_a(j)%salt(isalt)%soil, hsaltb_a(j)%salt(isalt)%surq, hsaltb_a(j)%salt(isalt)%latq, hsaltb_a(j)%salt(isalt)%urbq, hsaltb_a(j)%salt(isalt)%wetq, hsaltb_a(j)%salt(isalt)%tile, hsaltb_a(j)%salt(isalt)%perc, hsaltb_a(j)%salt(isalt)%wtsp, hsaltb_a(j)%salt(isalt)%irsw, hsaltb_a(j)%salt(isalt)%irgw, hsaltb_a(j)%salt(isalt)%irwo` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hsaltb_m(j)%salt(isalt)%soil` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%soil` increases by the current day's soil salt flux from `hsaltb_d(j)%salt(isalt)%soil`, so the monthly accumulator stores the sum of daily soil fluxes until month-end reporting. |
| `hsaltb_m(j)%salt(isalt)%surq` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%surq` increases by the current day's surface runoff salt flux from `hsaltb_d(j)%salt(isalt)%surq`, building the monthly total used for month-end output. |
| `hsaltb_m(j)%salt(isalt)%latq` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%latq` increases by the current day's lateral flow salt flux from `hsaltb_d(j)%salt(isalt)%latq`, so the monthly report can show the accumulated lateral-flow load. |
| `hsaltb_m(j)%salt(isalt)%urbq` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%urbq` increases by the current day's urban runoff salt flux from `hsaltb_d(j)%salt(isalt)%urbq`, preserving the month-to-date total for urban runoff. |
| `hsaltb_m(j)%salt(isalt)%wetq` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%wetq` increases by the current day's wetland runoff salt flux from `hsaltb_d(j)%salt(isalt)%wetq`, so the monthly accumulator can be reported at month end. |
| `hsaltb_m(j)%salt(isalt)%tile` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%tile` increases by the current day's tile-flow salt flux from `hsaltb_d(j)%salt(isalt)%tile`, accumulating the monthly tile contribution. |
| `hsaltb_m(j)%salt(isalt)%perc` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%perc` increases by the current day's percolation salt flux from `hsaltb_d(j)%salt(isalt)%perc`, preserving the month-to-date leaching total. |
| `hsaltb_m(j)%salt(isalt)%wtsp` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%wtsp` increases by the current day's wetland seepage salt flux from `hsaltb_d(j)%salt(isalt)%wtsp`, accumulating the monthly seepage load. |
| `hsaltb_m(j)%salt(isalt)%irsw` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%irsw` increases by the current day's surface-water irrigation salt flux from `hsaltb_d(j)%salt(isalt)%irsw`, so the monthly accumulator retains the irrigation input total. |
| `hsaltb_m(j)%salt(isalt)%irgw` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%irgw` increases by the current day's groundwater irrigation salt flux from `hsaltb_d(j)%salt(isalt)%irgw`, adding that irrigation source to the monthly total. |
| `hsaltb_m(j)%salt(isalt)%irwo` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%irwo` increases by the current day's outside-watershed irrigation salt flux from `hsaltb_d(j)%salt(isalt)%irwo`, keeping the monthly sum for that source. |
| `hsaltb_m(j)%salt(isalt)%rain` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%rain` increases by the current day's rainfall salt addition from `hsaltb_d(j)%salt(isalt)%rain`, contributing to the monthly atmospheric input total. |
| `hsaltb_m(j)%salt(isalt)%dryd` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%dryd` increases by the current day's dry-deposition salt addition from `hsaltb_d(j)%salt(isalt)%dryd`, so the monthly total includes that deposition pathway. |
| `hsaltb_m(j)%salt(isalt)%road` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%road` increases by the current day's road-salt addition from `hsaltb_d(j)%salt(isalt)%road`, accumulating the monthly road application source. |
| `hsaltb_m(j)%salt(isalt)%fert` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%fert` increases by the current day's fertilizer salt addition from `hsaltb_d(j)%salt(isalt)%fert`, so the month-end output reflects fertilizer inputs. |
| `hsaltb_m(j)%salt(isalt)%amnd` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%amnd` increases by the current day's amendment salt addition from `hsaltb_d(j)%salt(isalt)%amnd`, accumulating the monthly amendment source. |
| `hsaltb_m(j)%salt(isalt)%uptk` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%uptk` increases by the current day's crop uptake salt term from `hsaltb_d(j)%salt(isalt)%uptk`, preserving the month-to-date uptake total. |
| `hsaltb_m(j)%salt(isalt)%conc` | During every call, inside the loop `do isalt=1,cs_db%num_salts` | `hsaltb_m(j)%salt(isalt)%conc` increases by the current day's concentration contribution from `hsaltb_d(j)%salt(isalt)%conc`, so the monthly average can later be computed from the accumulated concentration total. |
| `hsaltb_m(j)%salt(1)%diss` | During every call, after the daily accumulation loop | `hsaltb_m(j)%salt(1)%diss` increases by the current day's dissolved salt transfer from `hsaltb_d(j)%salt(1)%diss`, tracking the dissolved-phase term alongside the other monthly salt quantities. |
| `hsaltb_y(j)%salt(isalt)%soil` | When `time%end_mo == 1` | `hsaltb_y(j)%salt(isalt)%soil` increases by the just-completed monthly soil total from `hsaltb_m(j)%salt(isalt)%soil`, building the yearly accumulator used for month-end reporting of yearly totals. |
| `hsaltb_y(j)%salt(isalt)%surq` | When `time%end_mo == 1` | `hsaltb_y(j)%salt(isalt)%surq` increases by the monthly surface-runoff total from `hsaltb_m(j)%salt(isalt)%surq`, so yearly output carries the accumulated surface runoff salt load. |
| `hsaltb_y(j)%salt(isalt)%latq` | When `time%end_mo == 1` | `hsaltb_y(j)%salt(isalt)%latq` increases by the monthly lateral-flow total from `hsaltb_m(j)%salt(isalt)%latq`, rolling the monthly lateral salt load into the yearly accumulator. |
| `hsaltb_y(j)%salt(isalt)%urbq` | When `time%end_mo == 1` | `hsaltb_y(j)%salt(isalt)%urbq` increases by the monthly urban-runoff total from `hsaltb_m(j)%salt(isalt)%urbq`, contributing that pathway to the yearly sums. |
| `hsaltb_y(j)%salt(isalt)%wetq` | When `time%end_mo == 1` | `hsaltb_y(j)%salt(isalt)%wetq` increases by the monthly wetland-runoff total from `hsaltb_m(j)%salt(isalt)%wetq`, so yearly output can report the accumulated wetland runoff salt load. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `hru_salt_output`. The file was introduced in df07e3f with the full HRU salt output workflow; 35b029c made only a whitespace cleanup near the end statement; 39fabde initialized the local variables `j`, `const`, `iob`, and `isalt` in the declarations; f1e61a3 fixed indentation in the daily CSV write line; and 2fe89fd increased the CSV `G0` edit descriptor precision from `G0.3` to `G0.6` for the CSV output writes on units 5022, 5024, 5026, and 5028.

- df07e3f added the subroutine and its daily, monthly, yearly, and average-annual salt accumulation/output flow.
- 39fabde changed the local declarations so `j`, `const`, `iob`, and `isalt` start at zero instead of being uninitialized.
- f1e61a3 only adjusted whitespace/tab alignment in the daily CSV write line and did not change runtime behavior.
- 2fe89fd changed CSV output formatting by widening the `G0` precision from `G0.3` to `G0.6` on the CSV-only write statements for the daily, monthly, yearly, and annual files.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_salt_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the algorithm to include the month-end yearly accumulation, monthly/yearly/annual output, and resets visible in the source.
