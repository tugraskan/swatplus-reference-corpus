---
kind: procedure
symbol: wet_salt_output
title: wet_salt_output
status: filled
source_hash: 0424794bc62aac3a
version_label: SWAT+ 62.0.0
args:
  j: Selects the wetland/HRU slot to process. The routine uses `j` to index the wetland salt
    output arrays (`wetsalt_d`, `wetsalt_m`, `wetsalt_y`, `wetsalt_a`) and to derive the object
    index `iob = sp_ob1%hru + j - 1` for the GIS/object identifier written to output.
locals:
  isalt: Loop index over salt ions. It is initialized to 0 and then reused in the daily, monthly,
    yearly, and annual accumulation and output loops across `1:cs_db%num_salts`.
  iob: Derived HRU/object index used to look up `ob(iob)%gis_id` for the output record. It
    is initialized to 0 and then set from `sp_ob1%hru + j - 1` before any writes.
  const: Temporary divisor used to convert accumulated monthly or yearly mass/concentration
    totals into averages. It is set first from the number of days in the month and later from
    `time%day_end_yr` for yearly averaging.
uses:
  output_ls_pesticide_module: The routine imports this module, but the provided source packet
    does not show any direct reference to its symbols inside `wet_salt_output`; it is therefore
    a build-time dependency rather than a visible data dependency in the extracted lines.
  res_pesticide_module: The routine imports this module, but the visible source lines do not
    use any pesticide-state members here; it is a shared dependency included alongside the
    salt output infrastructure.
  res_salt_module: '`res_salt_module` defines the wetland salt result structures that this
    routine reads, accumulates, averages, and resets. The arrays `wetsalt_m`, `wetsalt_d`,
    `wetsalt_y`, and `wetsalt_a` are the storage for daily, monthly, yearly, and average-annual
    salt-ion balances, and their fields are the values written to the output files.'
  plant_module: The module is imported by `wet_salt_output`, but no plant-module symbols are
    referenced in the extracted lines. It is part of the broader output dependency set and
    may be required by shared interfaces or compilation context.
  plant_data_module: The module is imported by `wet_salt_output`, but the shown code does
    not directly access plant data. It remains relevant as a compile-time dependency within
    the output subsystem.
  time_module: '`time_module` supplies the simulation clock fields that gate when monthly,
    yearly, and simulation-end output is produced and that are written into each record. The
    routine checks `time%end_mo`, `time%end_yr`, and `time%end_sim`, and it writes `time%day`,
    `time%mo`, `time%day_mo`, and `time%yrc` to every output line.'
  basin_module: '`basin_module` provides the print-control flags that decide whether daily,
    monthly, yearly, and average-annual salt output is written and whether CSV versions are
    emitted. `pco%salt_res%d`, `%m`, `%y`, `%a`, and `pco%csvout` directly govern the output
    branches in this routine.'
  output_landscape_module: The module is imported but no extracted line shows direct use of
    its symbols. It is part of the output infrastructure surrounding landscape/wetland reporting.
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_salts`, which sets
    the loop bounds for every salt-ion accumulation and write operation. Without the salt
    count, the routine would not know how many ion slots to process.'
  hydrograph_module: '`hydrograph_module` provides `sp_ob1%hru` and `ob(iob)%gis_id`. `sp_ob1%hru`
    is used to derive the object index for the selected wetland HRU, and `ob(iob)%gis_id`
    supplies the GIS identifier written into each output record.'
---

<!-- facts:header -->

Writes daily, monthly, yearly, and average annual wetland salt output for one HRU/wetland object.
It accumulates daily salt-ion balances into monthly, yearly, and all-simulation totals and emits text/CSV records when the configured print flags are enabled.

## Bottom Line

`wet_salt_output` reports salt-ion mass balance for wetland HRUs. For the selected HRU index `j`, it adds the current day’s wetland salt outputs into monthly totals, rolls monthly totals into yearly totals at month-end, and rolls yearly totals into average-annual totals at year-end when the relevant print flags are on.

It matters because it is the wetland salt reporting/aggregation step for the SWAT+ run: it preserves period totals in `wetsalt_m`, `wetsalt_y`, and `wetsalt_a`, writes the corresponding records to units 5090–5097, and resets period accumulators after they are reported.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine during HRU output processing, after `hru_output`, `hru_carbon_output`, and `wetland_output`, and only when the selected HRU has surface storage and `cs_db%num_salts > 0`. `wet_salt_output` then updates the wetland salt output accumulators and emits period records that downstream reporting files use for daily, monthly, yearly, and average-annual salt summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Derive the object index for this wetland HRU | Compute `iob = sp_ob1%hru + j - 1` so the routine can fetch the correct GIS/object id for the selected wetland HRU. |
| 2. Accumulate daily values into monthly totals | For each salt ion, add the daily inflow, outflow, seep, fertilizer, irrigation, diversion, mass, and concentration values from `wetsalt_d` into the month-to-date accumulators in `wetsalt_m`, and add daily water volume to the monthly volume total. |
| 3. Write daily wetland salt output when enabled | If `pco%salt_res%d` is enabled, write the daily formatted record to unit 5090 and, when `pco%csvout` is enabled, write the CSV version to unit 5091. |
| 4. Roll monthly totals into yearly totals at month end | When `time%end_mo == 1`, add the month totals from `wetsalt_m` into `wetsalt_y` for every salt ion and add monthly water volume to the yearly volume total. |
| 5. Convert monthly mass and concentration totals to averages | Compute the number of days in the current month with `float(ndays(time%mo + 1) - ndays(time%mo))`, then divide the monthly mass, concentration, and volume totals in `wetsalt_m` by that day count. |
| 6. Write monthly wetland salt output when enabled | If monthly salt-res output is enabled, write the formatted monthly record to unit 5092 and, if CSV output is enabled, write the CSV version to unit 5093. |
| 7. Reset monthly accumulators after reporting | Zero the monthly inflow, outflow, seep, fertilizer, irrigation, diversion, mass, concentration, and volume totals so the next month starts from a clean slate. |
| 8. Roll yearly totals into all-simulation totals at year end | When `time%end_yr == 1`, add the yearly totals from `wetsalt_y` into the all-simulation accumulators in `wetsalt_a` for every salt ion and add yearly volume to the annual total. |
| 9. Convert yearly totals to yearly averages | Use `time%day_end_yr` as the divisor and divide yearly mass, concentration, and volume totals in `wetsalt_y` by that count to obtain yearly averages. |
| 10. Write yearly wetland salt output when enabled | If yearly salt-res output is enabled, write the formatted yearly record to unit 5094 and, when CSV output is enabled, write the CSV version to unit 5095. |
| 11. Reset yearly accumulators after reporting | Zero the yearly inflow, outflow, seep, fertilizer, irrigation, diversion, mass, concentration, and volume totals for the next year. |
| 12. Produce average-annual output at simulation end | When the simulation ends and average-annual salt output is enabled, divide `wetsalt_a` by `time%nbyr`, write the formatted record to unit 5096, and write the CSV version to unit 5097 when requested. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `output_ls_pesticide_module state/types` | `No specific components were resolved in the source packet for this module.` |
| [sym:res_pesticide_module] | `res_pesticide_module state/types` | `No specific components were resolved in the source packet for this module.` |
| [sym:res_salt_module] | `wetsalt_m, wetsalt_d, wetsalt_y, wetsalt_a` | `wetsalt_m(j)%salt(isalt)%inflow, wetsalt_d(j)%salt(isalt)%inflow, wetsalt_m(j)%salt(isalt)%outflow, wetsalt_d(j)%salt(isalt)%outflow, wetsalt_m(j)%salt(isalt)%seep, wetsalt_d(j)%salt(isalt)%seep, wetsalt_m(j)%salt(isalt)%fert, wetsalt_d(j)%salt(isalt)%fert, wetsalt_m(j)%salt(isalt)%irrig, wetsalt_d(j)%salt(isalt)%irrig, wetsalt_m(j)%salt(isalt)%div, wetsalt_d(j)%salt(isalt)%div, wetsalt_m(j)%salt(isalt)%mass, wetsalt_d(j)%salt(isalt)%mass, wetsalt_m(j)%salt(isalt)%conc, wetsalt_d(j)%salt(isalt)%conc, wetsalt_m(j)%salt(1)%volm, wetsalt_d(j)%salt(1)%volm, wetsalt_y(j)%salt(isalt)%inflow, wetsalt_y(j)%salt(isalt)%outflow, wetsalt_y(j)%salt(isalt)%seep, wetsalt_y(j)%salt(isalt)%fert, wetsalt_y(j)%salt(isalt)%irrig, wetsalt_y(j)%salt(isalt)%div, wetsalt_y(j)%salt(isalt)%mass, wetsalt_y(j)%salt(isalt)%conc, wetsalt_y(j)%salt(1)%volm, wetsalt_a(j)%salt(isalt)%inflow, wetsalt_a(j)%salt(isalt)%outflow, wetsalt_a(j)%salt(isalt)%seep, wetsalt_a(j)%salt(isalt)%fert, wetsalt_a(j)%salt(isalt)%irrig, wetsalt_a(j)%salt(isalt)%div, wetsalt_a(j)%salt(isalt)%mass, wetsalt_a(j)%salt(isalt)%conc, wetsalt_a(j)%salt(1)%volm` |
| [sym:plant_module] | `plant_module state/types` | `No specific components were resolved in the source packet for this module.` |
| [sym:plant_data_module] | `plant_data_module state/types` | `No specific components were resolved in the source packet for this module.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%salt_res%d, pco%csvout, pco%salt_res%m, pco%salt_res%y, pco%salt_res%a` |
| [sym:output_landscape_module] | `output_landscape_module state/types` | `No specific components were resolved in the source packet for this module.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wetsalt_m(j)%salt(isalt)%inflow` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%inflow` grows by the current day's inflow from `wetsalt_d` so the routine can preserve a month-to-date wetland salt inflow total. |
| `wetsalt_m(j)%salt(isalt)%outflow` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%outflow` grows by the current day's outflow from `wetsalt_d` so the routine can preserve a month-to-date wetland salt outflow total. |
| `wetsalt_m(j)%salt(isalt)%seep` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%seep` grows by the current day's seepage from `wetsalt_d` so the routine can preserve a month-to-date seepage total. |
| `wetsalt_m(j)%salt(isalt)%fert` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%fert` grows by the current day's fertilizer salt contribution from `wetsalt_d` so the routine can preserve a month-to-date fertilizer total. |
| `wetsalt_m(j)%salt(isalt)%irrig` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%irrig` grows by the current day's irrigation-related salt amount from `wetsalt_d` so the routine can preserve a month-to-date irrigation total. |
| `wetsalt_m(j)%salt(isalt)%div` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%div` grows by the current day's diversion salt amount from `wetsalt_d` so the routine can preserve a month-to-date diversion total. |
| `wetsalt_m(j)%salt(isalt)%mass` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%mass` grows by the current day's salt mass from `wetsalt_d` so the routine can preserve a month-to-date mass total before monthly averaging and reset. |
| `wetsalt_m(j)%salt(isalt)%conc` | Every call; daily value is added to the monthly accumulator for each salt ion. | `wetsalt_m(j)%salt(isalt)%conc` grows by the current day's concentration value from `wetsalt_d` so the routine can preserve a month-to-date concentration total before monthly averaging and reset. |
| `wetsalt_m(j)%salt(1)%volm` | Every call; daily volume is added to the monthly volume accumulator. | `wetsalt_m(j)%salt(1)%volm` grows by the current day's wetland water volume from `wetsalt_d` so the monthly output can report a volume total/average alongside the salt-ion balances. |
| `wetsalt_y(j)%salt(isalt)%inflow` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%inflow` accumulates the month’s inflow total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%outflow` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%outflow` accumulates the month’s outflow total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%seep` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%seep` accumulates the month’s seepage total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%fert` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%fert` accumulates the month’s fertilizer contribution from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%irrig` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%irrig` accumulates the month’s irrigation-related salt total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%div` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%div` accumulates the month’s diversion total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%mass` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%mass` accumulates the month’s mass total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(isalt)%conc` | At month end (`time%end_mo == 1`); monthly total is added into the yearly accumulator. | `wetsalt_y(j)%salt(isalt)%conc` accumulates the month’s concentration total from `wetsalt_m` so yearly output can aggregate all months in the year. |
| `wetsalt_y(j)%salt(1)%volm` | At month end (`time%end_mo == 1`); monthly volume is added into the yearly volume accumulator. | `wetsalt_y(j)%salt(1)%volm` grows by the monthly wetland water volume from `wetsalt_m` so yearly output can carry the water volume alongside the salt totals. |
| `wetsalt_a(j)%salt(isalt)%inflow` | At year end (`time%end_yr == 1`); yearly total is added into the average-annual accumulator. | `wetsalt_a(j)%salt(isalt)%inflow` accumulates the year’s inflow total from `wetsalt_y` so the routine can later divide by the number of simulation years and report an average annual inflow. |
| `wetsalt_a(j)%salt(isalt)%outflow` | At year end (`time%end_yr == 1`); yearly total is added into the average-annual accumulator. | `wetsalt_a(j)%salt(isalt)%outflow` accumulates the year’s outflow total from `wetsalt_y` so the routine can later divide by the number of simulation years and report an average annual outflow. |
| `wetsalt_a(j)%salt(isalt)%seep` | At year end (`time%end_yr == 1`); yearly total is added into the average-annual accumulator. | `wetsalt_a(j)%salt(isalt)%seep` accumulates the year’s seepage total from `wetsalt_y` so the routine can later divide by the number of simulation years and report an average annual seepage. |
| `wetsalt_a(j)%salt(isalt)%fert` | At year end (`time%end_yr == 1`); yearly total is added into the average-annual accumulator. | `wetsalt_a(j)%salt(isalt)%fert` accumulates the year’s fertilizer contribution from `wetsalt_y` so the routine can later divide by the number of simulation years and report an average annual fertilizer input. |
| `wetsalt_a(j)%salt(isalt)%irrig` | At year end (`time%end_yr == 1`); yearly total is added into the average-annual accumulator. | `wetsalt_a(j)%salt(isalt)%irrig` accumulates the year’s irrigation-related salt total from `wetsalt_y` so the routine can later divide by the number of simulation years and report an average annual irrigation total. |
| `wetsalt_a(j)%salt(isalt)%div` | At year end (`time%end_yr == 1`); yearly total is added into the average-annual accumulator. | `wetsalt_a(j)%salt(isalt)%div` accumulates the year’s diversion total from `wetsalt_y` so the routine can later divide by the number of simulation years and report an average annual diversion total. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `wet_salt_output`. The initial addition in `df07e3f` introduced the subroutine and its daily, monthly, yearly, and average-annual salt output logic. `39fabde` initialized the local variables `isalt`, `iob`, and `const` to default values. `2fe89fd` changed the CSV `write` format on units 5091, 5093, 5095, and 5097 from `G0.3` to `G0.6` precision.

- `df07e3f` added the full wetland salt reporting routine, including accumulation into `wetsalt_m`, `wetsalt_y`, and `wetsalt_a`, output writes to units 5090-5097, period resets, and average-annual calculations.
- `39fabde` made the local counters and divisor explicit with initial values (`isalt=0`, `iob=0`, `const=0.`), reducing reliance on uninitialized locals.
- `2fe89fd` increased CSV numeric precision for wetland salt output records by changing the `G0.3` format to `G0.6` on the CSV units.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wet_salt_output' has no extracted documentation comment.
