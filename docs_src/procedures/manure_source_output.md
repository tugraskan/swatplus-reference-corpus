---
kind: procedure
symbol: manure_source_output
title: manure_source_output
status: filled
source_hash: b94d16cda1720901
version_label: SWAT+ 62.0.0
args:
  imallo: Selects which manure allocation object in `mallo(:)` to report. The routine uses
    `mallo(imallo)%src_obs` and `mallo(imallo)%src(:)` as the source list for that one allocation
    group.
locals:
  itrn: A report label written into every output row. In this procedure it stays at its initialized
    value of 0, so it functions as a placeholder identifier rather than a computed transport/demand
    number.
  isrc: Loop index over the manure source objects within `mallo(imallo)`. It advances from
    1 to `mallo(imallo)%src_obs` so each source gets its own output record(s).
uses:
  time_module: The routine needs the current simulation date and end-of-period flags from
    `time` to decide whether to write daily, monthly, yearly, or average annual output. The
    same fields are also written to every record so the output lines can be tied to the correct
    day, month, year, and simulation ending period.
  hydrograph_module: The `hydrograph_module` is the source of `pco`, which controls whether
    each reporting branch is enabled and whether a matching CSV-formatted line is also written.
    Without those flags, the routine would not know which periods to emit or whether to duplicate
    the output in CSV form.
  manure_allocation_module: The manure allocation module supplies the allocation object tree
    that this routine reports on. It provides the source count, each source's identifiers,
    and the balance accumulators (`bal_d`, `bal_m`, `bal_y`, `bal_a`) that are written and
    then reset here.
---

<!-- facts:header -->

Prints manure-source balance output for each source object in a manure allocation group. It reports daily, monthly, yearly, and average annual balance totals to fixed output units and optional CSV files.

## Bottom Line

manure_source_output walks through every manure source object in the selected allocation set (`imallo`) and prints the current source balance totals at the daily, monthly, yearly, and average annual reporting points. The routine uses the simulation clock and the allocation object state to decide when each report is written.

After each reporting write, it resets the corresponding accumulator (`bal_d`, `bal_m`, or `bal_y`) back to `malloz`, so later time periods start from a clean subtotal. That makes the routine part of the reporting/accumulation cycle rather than a calculator of new manure amounts.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after the manure allocation database has been set up and the model is in its output phase. `command` calls it once for each allocation object (`iwro`) so the manure-source reporting files stay synchronized with the rest of the allocation outputs, and later post-processing depends on these written daily, monthly, yearly, and average-annual balance records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over source objects | The routine iterates from source 1 through `mallo(imallo)%src_obs`, so every manure source attached to the selected allocation object is handled in turn. |
| 2. Accumulate the daily subtotal | Before any reporting decisions, it adds the current daily balance `bal_d` into the running monthly subtotal `bal_m` for that source. |
| 3. Write daily output if enabled | If `pco%water_allo%d` is enabled, the routine writes a daily balance record to unit 3200 and, when `pco%csvout` is enabled, also writes the same daily fields to unit 3201 in CSV format. |
| 4. Clear the daily accumulator | After the daily reporting branch, it resets `bal_d` to `malloz` so the next day starts with a blank daily balance object. |
| 5. On month-end, accumulate and write monthly output | When `time%end_mo == 1`, it adds the monthly subtotal `bal_m` into `bal_y`, writes month-end output to unit 3202 and optional CSV to unit 3203 if `pco%water_allo%m` is enabled, and then clears `bal_m` back to `malloz`. |
| 6. On year-end, accumulate and write yearly output | When `time%end_yr == 1`, it adds `bal_y` into `bal_a`, writes year-end output to unit 3204 and optional CSV to unit 3205 if `pco%water_allo%y` is enabled, and then resets `bal_y` to `malloz`. |
| 7. On simulation end, compute and write average annual output | When `time%end_sim == 1`, it converts `bal_a` into an average annual value by dividing by `time%yrs_prt`, then writes the final annual summary to unit 3206 and optional CSV to unit 3207 if `pco%water_allo%a` is enabled. |
| 8. Finish the source loop and return | After all sources are processed, the routine returns to its caller; the format statement at the end supports the formatted write statements used above. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `pco` | `pco%water_allo%d, pco%water_allo%m, pco%water_allo%y, pco%water_allo%a, pco%csvout` |
| [sym:manure_allocation_module] | `mallo, malloz` | `mallo(imallo)%src_obs, mallo(imallo)%src(isrc)%bal_m, mallo(imallo)%src(isrc)%bal_d, mallo(imallo)%src(isrc)%num, mallo(imallo)%src(isrc)%mois_typ, mallo(imallo)%src(isrc)%manure_typ, mallo(imallo)%src(isrc)%bal_y, mallo(imallo)%src(isrc)%bal_a` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mallo(imallo)%src(isrc)%bal_m` | Every source iteration, before daily output is written. | `mallo(imallo)%src(isrc)%bal_m` is incremented by the current daily balance `bal_d`, so it accumulates the running monthly total for that source. The monthly total is then used for month-end reporting and later cleared after the month-end branch. |
| `mallo(imallo)%src(isrc)%bal_d` | After the daily write branch, every source iteration. | `mallo(imallo)%src(isrc)%bal_d` is reset to `malloz`, so the next day starts with a fresh daily source-balance object instead of carrying the current day's amounts forward. |
| `mallo(imallo)%src(isrc)%bal_y` | When `time%end_mo == 1`. | `mallo(imallo)%src(isrc)%bal_y` is increased by the current monthly subtotal `bal_m`, building the running yearly total across months. After the month-end output is written, `bal_m` is cleared for the next month. |
| `mallo(imallo)%src(isrc)%bal_a` | When `time%end_yr == 1`. | `mallo(imallo)%src(isrc)%bal_a` is increased by the current yearly subtotal `bal_y`, building the long-term total used for average annual reporting. After that, `bal_y` is cleared for the next year. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior changes. The routine was added in df07e3f with daily, monthly, yearly, and average-annual manure-source output using `idmd` as the written identifier. In 39fabde, `isrc` and `idmd` were initialized to zero. In 914f365, `idmd` was renamed to `itrn` throughout the routine and the written edit descriptors and field names were updated to use `itrn`. In 2fe89fd, the CSV edit descriptor for units 3201, 3203, 3205, and 3207 was changed from `G0.3` to `G0.6`.

- df07e3f introduced the full manure-source reporting subroutine with daily, monthly, yearly, and average-annual accumulation and writes.
- 39fabde initialized the local loop variables so `idmd`/`itrn` and `isrc` start from zero instead of undefined values.
- 914f365 replaced the written identifier `idmd` with `itrn` and aligned all output lines with the renamed demand object terminology.
- 2fe89fd increased CSV output precision from `G0.3` to `G0.6` on all CSV write units.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'manure_source_output' has no extracted documentation comment.
