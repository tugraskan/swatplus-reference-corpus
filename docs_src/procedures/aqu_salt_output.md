---
kind: procedure
symbol: aqu_salt_output
title: aqu_salt_output
status: filled
source_hash: a09abcd53bcce0cc
version_label: SWAT+ 62.0.0
args:
  iaq: '`iaq` selects which aquifer object to report. The routine maps it to the global object
    index with `iob = sp_ob1%aqu + iaq - 1` and then reads and accumulates the salt-balance
    arrays for that aquifer.'
locals:
  const: '`const` is a temporary divisor used to turn accumulated mass and concentration totals
    into period averages. It is set from the number of days in the month at month end and
    from `time%day_end_yr` at year end.'
  iob: '`iob` is the global object index for the aquifer currently being reported. It combines
    the aquifer offset in `sp_ob1%aqu` with the local aquifer number `iaq` so the routine
    can fetch the matching GIS/object ID from `ob(iob)%gis_id`.'
  isalt: '`isalt` is the loop index over salt ions. The routine uses it to step through all
    salts in `cs_db%num_salts` when accumulating and writing salt-specific fluxes.'
uses:
  time_module: The time state determines which reporting branches run and supplies the date
    fields written to each record. `time%end_mo`, `time%end_yr`, and `time%end_sim` gate monthly,
    yearly, and average-annual output, while the day/month/year fields are included in every
    output line.
  basin_module: The basin print-code state controls whether each aquifer salt report is emitted
    at daily, monthly, yearly, or average-annual intervals, and whether CSV companion records
    are also written. Without these flags, the routine would still accumulate summaries but
    would skip the corresponding output files.
  aquifer_module: These aquifer salt-balance arrays are the actual source and target of the
    reporting logic. The routine sums daily values into monthly totals, monthly totals into
    yearly totals, and yearly totals into average-annual totals, then resets the shorter-period
    accumulators after writing.
  hydrograph_module: The hydrograph object connectivity provides the GIS/object identifier
    for the aquifer being printed, and the aquifer offset defines which global object index
    to use. This matters because every output row is labeled with `ob(iob)%gis_id` rather
    than only the local aquifer number.
  salt_aquifer: The salt database dimensions control how many salt ions are iterated over
    in each accumulation and write statement. The routine loops from 1 to `cs_db%num_salts`,
    so this module sets the size of every per-salt output vector.
  constituent_mass_module: The number of simulated salts determines whether the salt-output
    branch runs at all. `command` only calls this routine when `cs_db%num_salts > 0`, and
    inside the routine the same value sets the loop bounds for all per-salt fields.
---

<!-- facts:header -->

Writes aquifer salt balance output at daily, monthly, yearly, and average-annual intervals. It also accumulates daily fluxes into monthly, yearly, and total summary states for later reporting.

## Bottom Line

This subroutine reports salt-ion mass balance results for one aquifer object identified by `iaq`. It gathers the current daily fluxes and storage values from the aquifer salt balance arrays, writes them to the configured output files when the corresponding print flags are enabled, and rolls the daily values into monthly, yearly, and average-annual summaries.

It matters because it is the aquifer-salt reporting point used by the command workflow after aquifer results have been computed. The routine also resets the monthly and yearly accumulators after printing so the next reporting period starts cleanly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after `aquifer_output(iaq)` and only when `cs_db%num_salts > 0`. It depends on aquifer salt-balance values already being populated by earlier model calculations, and its written summaries are used for the model's daily, monthly, yearly, and final aquifer salt reporting products.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute the global aquifer object index. | Maps the local aquifer number `iaq` to the global object index `iob` using the aquifer offset stored in `sp_ob1%aqu`. This lets the routine fetch the object GIS ID for labels in every output record. |
| 2. Accumulate daily values into monthly totals. | For each salt ion, adds the current daily recharge, seepage, stream loading, irrigation removal, diversion removal, mass, and concentration to the monthly accumulator `asaltb_m(iaq)`. It also accumulates the dissolved-phase total in `asaltb_m(iaq)%salt(1)%diss`. |
| 3. Write daily aquifer-salt output when enabled. | If `pco%salt_aqu%d` is enabled, writes one daily record to unit 5060 with the date, aquifer ID, GIS ID, and all daily salt-balance fields. If CSV output is enabled, writes the same daily data to unit 5061 in comma-separated format. |
| 4. On month end, roll monthly totals into yearly totals. | When `time%end_mo == 1`, adds the monthly accumulator values from `asaltb_m(iaq)` into the yearly accumulator `asaltb_y(iaq)` for every salt ion and for dissolved mass. |
| 5. Average monthly mass and concentration. | Computes the number of days in the current month with `float (ndays(time%mo + 1) - ndays(time%mo))` and divides the monthly mass and concentration totals by that day count so the monthly output reports averages rather than sums. |
| 6. Write monthly aquifer-salt output when enabled. | If `pco%salt_aqu%m` is enabled, writes the monthly report to unit 5062 and, if CSV output is enabled, to unit 5063. These records contain the monthly accumulated and averaged salt-balance values. |
| 7. Clear monthly accumulators after printing. | Resets all monthly salt-balance accumulators for the current aquifer to zero so the next month starts with clean totals. |
| 8. On year end, roll yearly totals into average-annual totals. | When `time%end_yr == 1`, adds the yearly accumulator values from `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for every salt ion and for dissolved mass. |
| 9. Average yearly mass and concentration. | Uses `time%day_end_yr` as the divisor to convert the yearly accumulated mass and concentration totals into per-day average yearly values before output. |
| 10. Write yearly aquifer-salt output when enabled. | If `pco%salt_aqu%y` is enabled, writes the yearly report to unit 5064 and, if CSV output is enabled, to unit 5065. These records contain the yearly accumulated and averaged salt-balance values. |
| 11. Clear yearly accumulators after printing. | Resets all yearly salt-balance accumulators for the current aquifer to zero so the next year starts with clean totals. |
| 12. On simulation end, compute average annual output. | When the simulation ends and average-annual output is enabled, divides the accumulated annual totals by `time%nbyr` to produce average-annual salt-balance values. |
| 13. Write average-annual aquifer-salt output. | Writes the final average-annual report to unit 5066 and, if CSV output is enabled, to unit 5067. These records contain the simulation-end average-annual salt-balance values. |
| 14. Return to caller. | Exits the subroutine after all requested output branches and accumulator updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%salt_aqu%d, pco%csvout, pco%salt_aqu%m, pco%salt_aqu%y, pco%salt_aqu%a` |
| [sym:aquifer_module] | `asaltb_d, asaltb_m, asaltb_y, asaltb_a` | `asaltb_d(iaq)%salt(isalt)%diss, asaltb_d(iaq)%salt(isalt)%rchrg, asaltb_d(iaq)%salt(isalt)%seep, asaltb_d(iaq)%salt(isalt)%saltgw, asaltb_d(iaq)%salt(isalt)%irr, asaltb_d(iaq)%salt(isalt)%div, asaltb_d(iaq)%salt(isalt)%mass, asaltb_d(iaq)%salt(isalt)%conc, asaltb_m(iaq)%salt(isalt)%diss, asaltb_m(iaq)%salt(isalt)%rchrg, asaltb_m(iaq)%salt(isalt)%seep, asaltb_m(iaq)%salt(isalt)%saltgw, asaltb_m(iaq)%salt(isalt)%irr, asaltb_m(iaq)%salt(isalt)%div, asaltb_m(iaq)%salt(isalt)%mass, asaltb_m(iaq)%salt(isalt)%conc, asaltb_y(iaq)%salt(isalt)%diss, asaltb_y(iaq)%salt(isalt)%rchrg, asaltb_y(iaq)%salt(isalt)%seep, asaltb_y(iaq)%salt(isalt)%saltgw, asaltb_y(iaq)%salt(isalt)%irr, asaltb_y(iaq)%salt(isalt)%div, asaltb_y(iaq)%salt(isalt)%mass, asaltb_y(iaq)%salt(isalt)%conc, asaltb_a(iaq)%salt(isalt)%diss, asaltb_a(iaq)%salt(isalt)%rchrg, asaltb_a(iaq)%salt(isalt)%seep, asaltb_a(iaq)%salt(isalt)%saltgw, asaltb_a(iaq)%salt(isalt)%irr, asaltb_a(iaq)%salt(isalt)%div, asaltb_a(iaq)%salt(isalt)%mass, asaltb_a(iaq)%salt(isalt)%conc` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%aqu` |
| [sym:salt_aquifer] | `asaltb_m, asaltb_d, asaltb_y, asaltb_a` | `asaltb_m(iaq)%salt(isalt)%rchrg, asaltb_d(iaq)%salt(isalt)%rchrg, asaltb_m(iaq)%salt(isalt)%seep, asaltb_d(iaq)%salt(isalt)%seep, asaltb_m(iaq)%salt(isalt)%saltgw, asaltb_d(iaq)%salt(isalt)%saltgw, asaltb_m(iaq)%salt(isalt)%irr, asaltb_d(iaq)%salt(isalt)%irr, asaltb_m(iaq)%salt(isalt)%div, asaltb_d(iaq)%salt(isalt)%div, asaltb_m(iaq)%salt(isalt)%mass, asaltb_d(iaq)%salt(isalt)%mass, asaltb_m(iaq)%salt(isalt)%conc, asaltb_d(iaq)%salt(isalt)%conc, asaltb_m(iaq)%salt(1)%diss, asaltb_d(iaq)%salt(1)%diss, asaltb_y(iaq)%salt(isalt)%rchrg, asaltb_y(iaq)%salt(isalt)%seep, asaltb_y(iaq)%salt(isalt)%saltgw, asaltb_y(iaq)%salt(isalt)%irr, asaltb_y(iaq)%salt(isalt)%div, asaltb_y(iaq)%salt(isalt)%mass, asaltb_y(iaq)%salt(isalt)%conc, asaltb_y(iaq)%salt(1)%diss, asaltb_a(iaq)%salt(isalt)%rchrg, asaltb_a(iaq)%salt(isalt)%seep, asaltb_a(iaq)%salt(isalt)%saltgw, asaltb_a(iaq)%salt(isalt)%irr, asaltb_a(iaq)%salt(isalt)%div, asaltb_a(iaq)%salt(isalt)%mass, asaltb_a(iaq)%salt(isalt)%conc, asaltb_a(iaq)%salt(1)%diss` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `asaltb_m(iaq)%salt(isalt)%rchrg` | Every call, before any output branches are tested. | Adds the current daily recharge, seepage, stream loading, irrigation removal, diversion removal, mass, and concentration values from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(isalt)%seep` | Every call, before any output branches are tested. | Adds the current daily seepage value from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(isalt)%saltgw` | Every call, before any output branches are tested. | Adds the current daily aquifer-to-stream salt loading from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(isalt)%irr` | Every call, before any output branches are tested. | Adds the current daily irrigation-removal salt mass from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(isalt)%div` | Every call, before any output branches are tested. | Adds the current daily diversion-removal salt mass from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(isalt)%mass` | Every call, before any output branches are tested. | Adds the current daily salt mass from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(isalt)%conc` | Every call, before any output branches are tested. | Adds the current daily groundwater concentration from `asaltb_d(iaq)` into the month accumulator `asaltb_m(iaq)` for each salt ion. |
| `asaltb_m(iaq)%salt(1)%diss` | Every call, before any output branches are tested. | Adds the current daily dissolved-phase salt total from `asaltb_d(iaq)` into the month accumulator for dissolved salt. |
| `asaltb_y(iaq)%salt(isalt)%rchrg` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's recharge value. |
| `asaltb_y(iaq)%salt(isalt)%seep` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's seepage value. |
| `asaltb_y(iaq)%salt(isalt)%saltgw` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's aquifer-to-stream loading. |
| `asaltb_y(iaq)%salt(isalt)%irr` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's irrigation removal. |
| `asaltb_y(iaq)%salt(isalt)%div` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's diversion removal. |
| `asaltb_y(iaq)%salt(isalt)%mass` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's mass total. |
| `asaltb_y(iaq)%salt(isalt)%conc` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator `asaltb_y(iaq)` for each salt ion's concentration total. |
| `asaltb_y(iaq)%salt(1)%diss` | When `time%end_mo == 1` after monthly accumulation is complete. | Adds the month accumulator `asaltb_m(iaq)` into the year accumulator for dissolved salt. |
| `asaltb_a(iaq)%salt(isalt)%rchrg` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's recharge value. |
| `asaltb_a(iaq)%salt(isalt)%seep` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's seepage value. |
| `asaltb_a(iaq)%salt(isalt)%saltgw` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's aquifer-to-stream loading. |
| `asaltb_a(iaq)%salt(isalt)%irr` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's irrigation removal. |
| `asaltb_a(iaq)%salt(isalt)%div` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's diversion removal. |
| `asaltb_a(iaq)%salt(isalt)%mass` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's mass total. |
| `asaltb_a(iaq)%salt(isalt)%conc` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator `asaltb_a(iaq)` for each salt ion's concentration total. |
| `asaltb_a(iaq)%salt(1)%diss` | When `time%end_yr == 1` after yearly accumulation is complete. | Adds the year accumulator `asaltb_y(iaq)` into the average-annual accumulator for dissolved salt. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows four behavior-changing edits in this procedure. On 2024-05-30 the routine was introduced with the current aquifer salt reporting logic, including daily, monthly, yearly, and average-annual accumulation and output branches. On 2024-07-16 the salt-aquifer module import was corrected from `salt_aquifer` to `salt_aquifer_module` to fix compilation, then on 2024-07-24 that change was reverted back to `salt_aquifer`. On 2024-08-08 the local variables `const`, `iob`, and `isalt` were initialized. On 2024-10-08 and again on 2026-04-21 the CSV `G0.3` format descriptors were changed to `G0.6` for units 5061, 5063, 5065, and 5067, increasing printed precision.

- Introduced the full aquifer salt output routine with daily, monthly, yearly, and average-annual accumulation and reporting branches.
- Changed the module import from `salt_aquifer` to `salt_aquifer_module` to satisfy compilation, then reverted it back in a later revert commit.
- Initialized `const`, `iob`, and `isalt` at declaration time so the routine starts with defined local values.
- Increased CSV numeric output precision from `G0.3` to `G0.6` for the aquifer salt CSV files.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aqu_salt_output' has no extracted documentation comment.
