---
kind: procedure
symbol: ch_salt_output
title: ch_salt_output
status: filled
source_hash: b1035f44257f676f
version_label: SWAT+ 62.0.0
args:
  jrch: '`jrch` is the channel reach index for the current call; the routine uses it directly
    as `iru` to select which channel''s salt summaries to accumulate and write.'
locals:
  isalt: '`isalt` is the salt-ion loop index. It runs from 1 to `cs_db%num_salts` to update
    and write each simulated salt constituent.'
  iru: '`iru` is the working channel index copied from `jrch`. It identifies which `chsalt_*`
    entry and which output row belong to the current reach.'
  iob: '`iob` is the object-connectivity index for the current channel reach. The routine
    computes it from `sp_ob1%chandeg` and uses it to fetch `ob(iob)%gis_id` for the output
    record.'
  const: '`const` holds the divisor used to convert accumulated water and concentration sums
    into period-mean values at month-end and year-end. It is set from the number of days in
    the month or from `time%day_end_yr`.'
uses:
  output_ls_pesticide_module: This module is imported by the procedure, so its exported declarations
    may be required for compilation even though no specific symbol from it is referenced in
    the extracted source.
  ch_salt_module: '`ch_salt_module` supplies the shared salt accumulators that this routine
    updates and writes. The daily, monthly, yearly, and average annual records all come from
    `chsalt_d`, `chsalt_m`, `chsalt_y`, and `chsalt_a`, so the routine''s entire purpose is
    to move values through those storage layers and emit them.'
  plant_module: The module is imported but no symbol from it is referenced in the extracted
    body. It matters because the source may depend on its public declarations indirectly or
    by interface consistency, even though this specific routine does not show a direct use.
  plant_data_module: The module is imported but no symbol from it is referenced in the extracted
    body. It may be included to satisfy shared model interfaces, but the routine does not
    directly read plant data here.
  time_module: '`time` controls when each output block runs (`end_mo`, `end_yr`, `end_sim`)
    and provides the date fields written to every record. It also provides `day_end_yr` and
    `nbyr`, which are used to compute average monthly and average annual values.'
  basin_module: '`pco` contains the print flags that gate each output stream. The routine
    checks `pco%salt_chn%d`, `%m`, `%y`, and `%a` to decide whether to write daily, monthly,
    yearly, or average annual salt reports, and `pco%csvout` to decide whether to emit the
    CSV companion files.'
  output_landscape_module: The module is imported, but no specific symbol from it appears
    in the extracted source. It still matters as a dependency because the routine belongs
    to the broader output subsystem and may rely on shared output definitions from this module.
  constituent_mass_module: '`cs_db%num_salts` sets the number of salt constituents to iterate
    over. Every accumulation loop and every write statement uses it to size the salt-vector
    output for the current model setup.'
  hydrograph_module: '`sp_ob1%chandeg` defines the starting object index for channel-degrees
    in the global object list. The routine adds `jrch - 1` to it to locate `ob(iob)%gis_id`,
    which is written to identify the channel reach in the output files.'
---

<!-- facts:header -->

Writes channel salt mass outputs for daily, monthly, yearly, and average annual reporting. It also rolls daily channel salt totals into monthly, yearly, and end-of-simulation summary accumulators.

## Bottom Line

ch_salt_output is the channel-salt reporting subroutine. Given a channel reach index, it maps that reach to the internal channel object, appends the current day’s salt totals into monthly accumulators, and conditionally writes daily, monthly, yearly, and average-annual reports.

It matters because it is the only extracted place where channel salt mass-balance results are aggregated across time scales and emitted to the configured output streams. It also resets month-end and year-end accumulators so each reporting period starts cleanly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during channel processing after the channel salt state has been updated for the current reach. Its outputs feed the model's daily, monthly, yearly, and average-annual channel salt report files, and its zeroing of period accumulators after report writing is essential so later reaches and later time periods do not double-count the same salt mass.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the caller’s reach index to the internal channel object index. | The routine copies `jrch` into `iru` and computes `iob` from `sp_ob1%chandeg + iru - 1` so it can reference the correct channel object and GIS identifier for the current reach. |
| 2. Add the current day’s salt values into the monthly accumulators. | For each simulated salt ion, the routine adds the daily totals from `chsalt_d(iru)` into the running monthly totals in `chsalt_m(iru)` for inflow, groundwater inflow, outflow, seepage, irrigation, diversion, water, and concentration. |
| 3. Write daily channel salt output when enabled. | If `pco%salt_chn%d` is enabled, the routine writes the daily formatted report to unit 5030 and, if CSV output is enabled, writes the same daily record to unit 5031. |
| 4. At month-end, roll monthly totals into yearly accumulators. | When `time%end_mo` is set, the routine adds each monthly salt summary from `chsalt_m(iru)` into the corresponding yearly accumulator in `chsalt_y(iru)`. |
| 5. Convert monthly water and concentration totals to month means. | The routine sets `const` to the number of days in the current month and divides the monthly `water` and `conc` sums by that count so the monthly report stores period-average values for those fields. |
| 6. Write monthly channel salt output when enabled. | If monthly salt output is enabled, the routine writes the monthly formatted report to unit 5032 and, if CSV output is enabled, writes the monthly CSV record to unit 5033. |
| 7. Reset monthly accumulators after month-end reporting. | After the monthly records are written, the routine zeros all monthly salt accumulators in `chsalt_m(iru)` so the next month starts from a clean slate. |
| 8. At year-end, roll yearly totals into average-annual accumulators. | When `time%end_yr` is set, the routine adds the yearly salt summaries from `chsalt_y(iru)` into the average-annual accumulator `chsalt_a(iru)`. |
| 9. Convert yearly water and concentration totals to annual means. | The routine sets `const` to `time%day_end_yr` and divides the yearly `water` and `conc` sums by that value so the yearly output stores average values for those fields. |
| 10. Write yearly channel salt output when enabled. | If yearly salt output is enabled, the routine writes the yearly formatted report to unit 5034 and, if CSV output is enabled, writes the yearly CSV record to unit 5035. |
| 11. Reset yearly accumulators after year-end reporting. | After the yearly records are written, the routine zeros all yearly salt accumulators in `chsalt_y(iru)` so the next year starts fresh. |
| 12. At the end of the simulation, compute average annual values. | If the simulation is ending and average-annual output is enabled, the routine divides the accumulated average-annual totals in `chsalt_a(iru)` by `time%nbyr` so the final report is normalized across the run length. |
| 13. Write average-annual channel salt output when enabled. | The routine writes the final average-annual formatted report to unit 5036 and, if CSV output is enabled, writes the final CSV record to unit 5037. |
| 14. Return to the caller. | The subroutine exits after all requested output streams have been handled and the relevant accumulators have been updated or cleared. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `No candidate outside references were resolved to `output_ls_pesticide_module`.` | `No outside components were identified for `output_ls_pesticide_module` in the provided evidence.` |
| [sym:ch_salt_module] | `chsalt_m, chsalt_d, chsalt_y, chsalt_a` | `chsalt_m(iru)%salt(isalt)%tot_in, chsalt_d(iru)%salt(isalt)%tot_in, chsalt_m(iru)%salt(isalt)%gw_in, chsalt_d(iru)%salt(isalt)%gw_in, chsalt_m(iru)%salt(isalt)%tot_out, chsalt_d(iru)%salt(isalt)%tot_out, chsalt_m(iru)%salt(isalt)%seep, chsalt_d(iru)%salt(isalt)%seep, chsalt_m(iru)%salt(isalt)%irr, chsalt_d(iru)%salt(isalt)%irr, chsalt_m(iru)%salt(isalt)%div, chsalt_d(iru)%salt(isalt)%div, chsalt_m(iru)%salt(isalt)%water, chsalt_d(iru)%salt(isalt)%water, chsalt_m(iru)%salt(isalt)%conc, chsalt_d(iru)%salt(isalt)%conc, chsalt_y(iru)%salt(isalt)%tot_in, chsalt_y(iru)%salt(isalt)%gw_in, chsalt_y(iru)%salt(isalt)%tot_out, chsalt_y(iru)%salt(isalt)%seep, chsalt_y(iru)%salt(isalt)%irr, chsalt_y(iru)%salt(isalt)%div, chsalt_y(iru)%salt(isalt)%water, chsalt_y(iru)%salt(isalt)%conc, chsalt_a(iru)%salt(isalt)%tot_in, chsalt_a(iru)%salt(isalt)%gw_in, chsalt_a(iru)%salt(isalt)%tot_out, chsalt_a(iru)%salt(isalt)%seep, chsalt_a(iru)%salt(isalt)%irr, chsalt_a(iru)%salt(isalt)%div, chsalt_a(iru)%salt(isalt)%water, chsalt_a(iru)%salt(isalt)%conc` |
| [sym:plant_module] | `No candidate outside references were resolved to `plant_module`.` | `No outside components were identified for `plant_module` in the provided evidence.` |
| [sym:plant_data_module] | `No candidate outside references were resolved to `plant_data_module`.` | `No outside components were identified for `plant_data_module` in the provided evidence.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%salt_chn%d, pco%csvout, pco%salt_chn%m, pco%salt_chn%y, pco%salt_chn%a` |
| [sym:output_landscape_module] | `No candidate outside references were resolved to `output_landscape_module`.` | `No outside components were identified for `output_landscape_module` in the provided evidence.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%chandeg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chsalt_m(iru)%salt(isalt)%tot_in` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%tot_in` accumulates the day’s channel salt inflow by adding `chsalt_d(iru)%salt(isalt)%tot_in` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%gw_in` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%gw_in` accumulates the day’s groundwater contribution by adding `chsalt_d(iru)%salt(isalt)%gw_in` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%tot_out` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%tot_out` accumulates the day’s total salt export by adding `chsalt_d(iru)%salt(isalt)%tot_out` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%seep` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%seep` accumulates the day’s seepage loss by adding `chsalt_d(iru)%salt(isalt)%seep` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%irr` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%irr` accumulates the day’s irrigation-related salt transfer by adding `chsalt_d(iru)%salt(isalt)%irr` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%div` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%div` accumulates the day’s diversion-related salt transfer by adding `chsalt_d(iru)%salt(isalt)%div` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%water` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%water` accumulates the daily end-of-day channel water salt mass by adding `chsalt_d(iru)%salt(isalt)%water` into the monthly total. |
| `chsalt_m(iru)%salt(isalt)%conc` | Each time the subroutine runs, before any prints, for every salt ion in `1..cs_db%num_salts`. | `chsalt_m(iru)%salt(isalt)%conc` accumulates the daily end-of-day channel concentration by adding `chsalt_d(iru)%salt(isalt)%conc` into the monthly total. |
| `chsalt_y(iru)%salt(isalt)%tot_in` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%tot_in` accumulates the month’s channel salt inflow by adding the monthly total from `chsalt_m(iru)%salt(isalt)%tot_in` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%gw_in` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%gw_in` accumulates the month’s groundwater inflow by adding the monthly total from `chsalt_m(iru)%salt(isalt)%gw_in` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%tot_out` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%tot_out` accumulates the month’s total export by adding the monthly total from `chsalt_m(iru)%salt(isalt)%tot_out` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%seep` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%seep` accumulates the month’s seepage loss by adding the monthly total from `chsalt_m(iru)%salt(isalt)%seep` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%irr` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%irr` accumulates the month’s irrigation-related transfer by adding the monthly total from `chsalt_m(iru)%salt(isalt)%irr` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%div` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%div` accumulates the month’s diversion-related transfer by adding the monthly total from `chsalt_m(iru)%salt(isalt)%div` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%water` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%water` accumulates the monthly water salt mass by adding the monthly total from `chsalt_m(iru)%salt(isalt)%water` into the yearly sum. |
| `chsalt_y(iru)%salt(isalt)%conc` | When `time%end_mo == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_y(iru)%salt(isalt)%conc` accumulates the monthly concentration by adding the monthly total from `chsalt_m(iru)%salt(isalt)%conc` into the yearly sum. |
| `chsalt_a(iru)%salt(isalt)%tot_in` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%tot_in` accumulates the yearly channel salt inflow by adding `chsalt_y(iru)%salt(isalt)%tot_in` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%gw_in` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%gw_in` accumulates the yearly groundwater inflow by adding `chsalt_y(iru)%salt(isalt)%gw_in` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%tot_out` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%tot_out` accumulates the yearly export by adding `chsalt_y(iru)%salt(isalt)%tot_out` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%seep` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%seep` accumulates the yearly seepage loss by adding `chsalt_y(iru)%salt(isalt)%seep` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%irr` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%irr` accumulates the yearly irrigation-related transfer by adding `chsalt_y(iru)%salt(isalt)%irr` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%div` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%div` accumulates the yearly diversion-related transfer by adding `chsalt_y(iru)%salt(isalt)%div` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%water` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%water` accumulates the yearly water salt mass by adding `chsalt_y(iru)%salt(isalt)%water` into the average-annual total. |
| `chsalt_a(iru)%salt(isalt)%conc` | When `time%end_yr == 1`, for every salt ion in `1..cs_db%num_salts`. | `chsalt_a(iru)%salt(isalt)%conc` accumulates the yearly concentration by adding `chsalt_y(iru)%salt(isalt)%conc` into the average-annual total. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four changes to `ch_salt_output`: the procedure was introduced in df07e3f; c7c8e22 carried that initial implementation forward unchanged; 39fabde initialized the local loop and working variables (`isalt`, `iru`, `iob`, `const`); and 2fe89fd changed the CSV write formats from `G0.3` to `G0.6` for the daily, monthly, yearly, and average-annual CSV outputs.

- df07e3f added the full `ch_salt_output` subroutine with daily, monthly, yearly, and average-annual accumulation and write logic.
- 39fabde changed the local variable declarations to initialize `isalt`, `iru`, `iob`, and `const` to zero.
- 2fe89fd increased CSV numeric formatting precision by changing the `write` format from `G0.3` to `G0.6` on units 5031, 5033, 5035, and 5037.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_salt_output' has no extracted documentation comment.
