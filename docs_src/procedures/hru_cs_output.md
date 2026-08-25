---
kind: procedure
symbol: hru_cs_output
title: hru_cs_output
status: filled
source_hash: d0e0166b9d573a1a
version_label: SWAT+ 62.0.0
args:
  ihru: Selects the HRU whose constituent balances are being summarized and written; the routine
    copies `ihru` into local index `j` and uses that HRU index to access the matching `hcsb_*`
    balance arrays and object connectivity.
locals:
  j: Local HRU index used throughout the routine after copying from `ihru`; it identifies
    which element of the balance arrays and object connectivity belongs to the current HRU.
    Initial value `0` is overwritten immediately by `j = ihru`.
  const: Temporary scaling factor used to average monthly mass and concentration totals over
    the number of days in the month. It is set from the month length and then used to divide
    selected monthly balance terms before monthly output.
  iob: Index into the object connectivity array `ob` for the current HRU. It is computed from
    `sp_ob1%hru + j - 1` so the routine can fetch the HRU GIS ID for the output records.
  ics: Loop counter over constituent species in `cs_db%num_cs`; every balance update and output
    record iterates across all simulated constituents for the current HRU.
uses:
  time_module: '`time_module` supplies the current simulation date and end-of-period flags
    that control which output branches run. The routine needs `time%day`, `time%mo`, `time%day_mo`,
    and `time%yrc` for record labels, plus `time%end_mo`, `time%end_yr`, and `time%end_sim`
    to decide when to roll daily totals into monthly, yearly, and average-annual summaries.'
  basin_module: '`basin_module` provides the print switches that decide whether each output
    period is emitted and whether CSV mirror files are written. `pco%cs_hru%d`, `pco%cs_hru%m`,
    `pco%cs_hru%y`, and `pco%cs_hru%a` gate daily, monthly, yearly, and average-annual writes,
    while `pco%csvout` controls the companion CSV outputs.'
  hydrograph_module: '`hydrograph_module` provides the object indexing needed to identify
    the HRU in the output. `sp_ob1%hru` maps the HRU sequence into the global object list,
    and `ob(iob)%gis_id` supplies the GIS identifier written to each record.'
  cs_module: '`cs_module` holds the HRU constituent balance arrays that this routine both
    accumulates and reports. The daily, monthly, yearly, and average-annual structures (`hcsb_d`,
    `hcsb_m`, `hcsb_y`, `hcsb_a`) store the constituent flux and storage terms that are summed,
    normalized, written, and reset here.'
  constituent_mass_module: '`constituent_mass_module` supplies `cs_db%num_cs`, the number
    of constituent species simulated. The loop bounds and all array section writes depend
    on that count so the routine processes exactly the configured constituent set.'
---

<!-- facts:header -->

Writes HRU constituent mass balance outputs at daily, monthly, yearly, and average annual scales.

## Bottom Line

`hru_cs_output` records constituent mass loading and concentration summaries for one HRU. It accumulates daily values into month, year, and average-annual balances, then writes the requested outputs to units 6021 through 6028 depending on the print codes in `pco%cs_hru` and the CSV flag `pco%csvout`.

The routine matters because it is the HRU-level reporting step for the constituent-mass subsystem: it moves daily balance terms into monthly and yearly totals, normalizes period summaries at period end, and clears the monthly totals after they are reported so the next reporting period starts fresh.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during the HRU-processing sequence after the model has already computed the current day’s constituent balances. `command` calls it only when `cs_db%num_cs > 0`, so the routine assumes constituent tracking is active. Its results feed the model’s HRU constituent report files and also preserve accumulated monthly, yearly, and average-annual totals for later output within the same simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the input HRU to local indices | Copies `ihru` into `j` and computes `iob = sp_ob1%hru + j - 1` so the routine can access the current HRU’s balance arrays and GIS object metadata. |
| 2. Accumulate daily balances into the monthly store | Loops over `ics = 1, cs_db%num_cs` and adds each daily constituent balance term from `hcsb_d(j)%cs(ics)` into the corresponding monthly total in `hcsb_m(j)%cs(ics)`. |
| 3. Write daily HRU outputs when daily printing is enabled | If `pco%cs_hru%d == 'y'`, writes the daily balance record to unit 6021 and, when `pco%csvout == 'y'`, also writes the CSV version to unit 6022 using the current date, HRU index, GIS ID, and daily constituent terms. |
| 4. Roll monthly totals into yearly totals at month end | When `time%end_mo == 1`, adds each monthly constituent total in `hcsb_m(j)%cs(ics)` into the yearly store `hcsb_y(j)%cs(ics)` so the year accumulates the completed month. |
| 5. Compute monthly averages for selected terms | Sets `const` to the number of days in the just-finished month and divides monthly `soil`, `conc`, and `srbd` by that day count so the monthly report shows mean values for those terms. |
| 6. Write monthly HRU outputs when monthly printing is enabled | If `pco%cs_hru%m == 'y'`, writes the monthly record to unit 6023 and, when `pco%csvout == 'y'`, to unit 6024. These writes use the month-averaged monthly terms and the month-accumulated flux terms. |
| 7. Clear monthly accumulators after month-end reporting | Resets all monthly constituent balance terms in `hcsb_y(j)%cs(ics)` to zero after the month-end transfer so the next month starts with empty yearly-to-date monthly storage. |
| 8. Average yearly totals and write annual outputs at simulation end | When `time%end_sim == 1` and `pco%cs_hru%a == 'y'`, divides the annual totals in `hcsb_a(j)%cs(ics)` by `time%nbyr`, writes the annual record to unit 6027, and writes the CSV version to unit 6028 if requested. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr` |
| [sym:basin_module] | `pco` | `pco%cs_hru%d, pco%csvout, pco%cs_hru%m` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru` |
| [sym:cs_module] | `hcsb_m, hcsb_d, hcsb_y, hcsb_a` | `hcsb_m(j)%cs(ics)%soil, hcsb_d(j)%cs(ics)%soil, hcsb_m(j)%cs(ics)%surq, hcsb_d(j)%cs(ics)%surq, hcsb_m(j)%cs(ics)%sedm, hcsb_d(j)%cs(ics)%sedm, hcsb_m(j)%cs(ics)%latq, hcsb_d(j)%cs(ics)%latq, hcsb_m(j)%cs(ics)%urbq, hcsb_d(j)%cs(ics)%urbq, hcsb_m(j)%cs(ics)%wetq, hcsb_d(j)%cs(ics)%wetq, hcsb_m(j)%cs(ics)%tile, hcsb_d(j)%cs(ics)%tile, hcsb_m(j)%cs(ics)%perc, hcsb_d(j)%cs(ics)%perc, hcsb_m(j)%cs(ics)%wtsp, hcsb_d(j)%cs(ics)%wtsp, hcsb_m(j)%cs(ics)%irsw, hcsb_d(j)%cs(ics)%irsw, hcsb_m(j)%cs(ics)%irgw, hcsb_d(j)%cs(ics)%irgw, hcsb_m(j)%cs(ics)%irwo, hcsb_d(j)%cs(ics)%irwo, hcsb_m(j)%cs(ics)%rain, hcsb_d(j)%cs(ics)%rain, hcsb_m(j)%cs(ics)%dryd, hcsb_d(j)%cs(ics)%dryd, hcsb_m(j)%cs(ics)%fert, hcsb_d(j)%cs(ics)%fert, hcsb_m(j)%cs(ics)%uptk, hcsb_d(j)%cs(ics)%uptk, hcsb_m(j)%cs(ics)%rctn, hcsb_d(j)%cs(ics)%rctn, hcsb_m(j)%cs(ics)%sorb, hcsb_d(j)%cs(ics)%sorb, hcsb_m(j)%cs(ics)%conc, hcsb_d(j)%cs(ics)%conc, hcsb_m(j)%cs(ics)%srbd, hcsb_d(j)%cs(ics)%srbd, hcsb_y(j)%cs(ics)%soil, hcsb_y(j)%cs(ics)%surq, hcsb_y(j)%cs(ics)%sedm, hcsb_y(j)%cs(ics)%latq, hcsb_y(j)%cs(ics)%urbq, hcsb_y(j)%cs(ics)%wetq, hcsb_y(j)%cs(ics)%tile, hcsb_y(j)%cs(ics)%perc, hcsb_y(j)%cs(ics)%wtsp, hcsb_y(j)%cs(ics)%irsw, hcsb_y(j)%cs(ics)%irgw, hcsb_y(j)%cs(ics)%irwo, hcsb_y(j)%cs(ics)%rain, hcsb_y(j)%cs(ics)%dryd, hcsb_y(j)%cs(ics)%fert, hcsb_y(j)%cs(ics)%uptk, hcsb_y(j)%cs(ics)%rctn, hcsb_y(j)%cs(ics)%sorb, hcsb_y(j)%cs(ics)%conc, hcsb_y(j)%cs(ics)%srbd, hcsb_a(j)%cs(ics)%soil, hcsb_a(j)%cs(ics)%surq, hcsb_a(j)%cs(ics)%sedm, hcsb_a(j)%cs(ics)%latq, hcsb_a(j)%cs(ics)%urbq, hcsb_a(j)%cs(ics)%wetq, hcsb_a(j)%cs(ics)%tile, hcsb_a(j)%cs(ics)%perc` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hcsb_m(j)%cs(ics)%soil` | Every call, before any output branch | Adds the current day’s soil constituent mass from `hcsb_d` into the running monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%surq` | Every call, before any output branch | Adds the daily surface-runoff constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%sedm` | Every call, before any output branch | Adds the daily sediment-associated constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%latq` | Every call, before any output branch | Adds the daily lateral-flow constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%urbq` | Every call, before any output branch | Adds the daily urban-runoff constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%wetq` | Every call, before any output branch | Adds the daily wetland-outflow constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%tile` | Every call, before any output branch | Adds the daily tile-flow constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%perc` | Every call, before any output branch | Adds the daily percolation constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%wtsp` | Every call, before any output branch | Adds the daily wetland seepage constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%irsw` | Every call, before any output branch | Adds the daily surface-water irrigation constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%irgw` | Every call, before any output branch | Adds the daily groundwater irrigation constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%irwo` | Every call, before any output branch | Adds the daily irrigation-from-outside-watershed constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%rain` | Every call, before any output branch | Adds the daily rainfall-applied constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%dryd` | Every call, before any output branch | Adds the daily dry-deposition constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%fert` | Every call, before any output branch | Adds the daily fertilizer-applied constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%uptk` | Every call, before any output branch | Adds the daily crop uptake constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%rctn` | Every call, before any output branch | Adds the daily reaction-transfer constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%sorb` | Every call, before any output branch | Adds the daily sorption-transfer constituent mass into the monthly total for each constituent species. |
| `hcsb_m(j)%cs(ics)%conc` | Every call, before any output branch | Adds the daily concentration term into the monthly total for each constituent species, before it is later averaged for the monthly report. |
| `hcsb_m(j)%cs(ics)%srbd` | Every call, before any output branch | Adds the daily sorbed-mass term into the monthly total for each constituent species. |
| `hcsb_y(j)%cs(ics)%soil` | At `time%end_mo == 1` after monthly totals have been accumulated | Adds the completed month’s soil total from `hcsb_m` into the yearly accumulator for each constituent species. |
| `hcsb_y(j)%cs(ics)%surq` | At `time%end_mo == 1` after monthly totals have been accumulated | Adds the completed month’s surface-runoff total into the yearly accumulator for each constituent species. |
| `hcsb_y(j)%cs(ics)%sedm` | At `time%end_mo == 1` after monthly totals have been accumulated | Adds the completed month’s sediment total into the yearly accumulator for each constituent species. |
| `hcsb_y(j)%cs(ics)%latq` | At `time%end_mo == 1` after monthly totals have been accumulated | Adds the completed month’s lateral-flow total into the yearly accumulator for each constituent species. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The file was introduced in `df07e3f` with the full HRU constituent-output routine. `39fabde` changed the local variables `j`, `const`, `iob`, and `ics` from uninitialized to initialized-at-declaration values. `f1e61a3` only fixed a tab/spacing issue in one continuation line. `2fe89fd` changed the CSV output format for units 6022, 6024, 6026, and 6028 from `G0.3` to `G0.6`, increasing numeric precision in those comma-separated files.

- Introduced HRU constituent output logic with daily, monthly, yearly, and average-annual accumulation and reporting.
- Initialized local scalars at declaration to avoid uninitialized-use risk without changing the algorithm.
- Increased CSV numeric precision on all constituent HRU CSV output units from `G0.3` to `G0.6`.
- Applied a formatting-only tab fix with no behavioral change.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_cs_output' has no extracted documentation comment.
