---
kind: procedure
symbol: mallo_control
title: mallo_control
status: filled
source_hash: e1c95bf718c9a225
version_label: SWAT+ 62.0.0
args:
  imallo: Selects which manure-allocation object in `mallo` this call processes.
locals:
  itrn: 'Iterates over each manure demand object in `mallo(imallo)%trn`. Initial value: `0`.'
  isrc: 'Holds the source-object index for the current demand and is reset before use. Initial
    value: `0`.'
  j: 'Holds the HRU/object number associated with the current demand and is passed to decision-table
    evaluation and logging. Initial value: `0`.'
  id: 'Holds the decision-table index for the current demand and is used to point `d_tbl`
    at `dtbl_lum(id)`. Initial value: `0`.'
  ifrt: 'Holds the fertilizer database index selected from the demand''s source object before
    calling `pl_fert`. Initial value: `0`.'
  ifertop: 'Holds the chemical application operation index selected from the demand''s application
    settings before calling `pl_fert`. Initial value: `0`.'
  frt_kg: 'Holds the manure/fertilizer application amount in kg/ha for the current demand.
    Initial value: `0.`.'
uses:
  manure_allocation_module: Defines the manure-allocation object, its source and demand records,
    the daily source balance, and the zeroed template records used by this routine.
  hru_module: Provides HRU state and fertilizer/nutrient accumulators used for application
    bookkeeping and management output.
  basin_module: Controls whether management output is written to unit 2612.
  time_module: Provides the current simulation date used to trigger monthly production and
    to label output records.
  plant_module: Provides plant-community state referenced in management output.
  soil_module: Provides soil-water state referenced in management output.
  organic_mineral_mass_module: Provides plant biomass and residue mass values written to management
    output.
  conditional_module: Provides the decision-table target pointer used before calling the condition
    and action evaluators.
---

<!-- facts:header -->

Allocates manure applications for one manure-allocation object on the current simulation day. It updates source storage, applies fertilizer/manure to HRUs when conditions are met, and optionally writes management output.

## Bottom Line

`mallo_control` is the manure-allocation driver for one `mallo(imallo)` object. On the first day of each month it adds that source's monthly production into daily storage, then it scans each demand object, evaluates the linked decision table, and executes the resulting management actions.

If a demand object has a positive manure application amount, the routine maps the demand back to its source, calls `pl_fert` to apply the material to the current HRU, subtracts the applied amount from source storage, records the withdrawal on the demand object, and writes a management log line when `pco%mgtout` is enabled.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `time_control` during the daily management-allocation phase after decision-table evaluation has been prepared for the current simulation day. It feeds manure application, source-balance updates, and optional management logging that later model routines can rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. reset allocation state | Reset the source index and application amount, then zero the allocation object's daily totals by copying `malloz` into `mallo(imallo)%tot`. |
| 2. add monthly production | On the first day of the month, add the current month's manure production to source storage and record that day's production in the daily balance. |
| 3. evaluate demand tables | Loop over each demand object, and for those with a valid decision table, point `d_tbl` at the table, then call `conditions` and `actions` to evaluate and execute the management rule. |
| 4. scan demands for withdrawal | Loop over the demand objects again and, for demands with a positive application amount and sufficient source storage, load the source, fertilizer, HRU, and application-method indices needed for application. |
| 5. apply fertilizer or manure | Call `pl_fert` to place the selected fertilizer/manure on the current HRU, then clear the demand object's manure-amount record back to the zero template. |
| 6. update source balances | Subtract the applied amount from source storage, record the withdrawal in the source daily balance, and store the withdrawal on the demand object's per-source withdrawal array. |
| 7. write management output | If management output is enabled, write a record containing the HRU, date, fertilizer name, plant/soil state, and nutrient amounts to unit 2612. |
| 8. return | Exit the subroutine after all demand objects have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:manure_allocation_module] | `mallo, malloz, manure_amtz` | `mallo(imallo)%tot, mallo(imallo)%src(isrc)%bal_d%stor, mallo(imallo)%src(isrc)%prod_mon, mallo(imallo)%src(isrc)%bal_d%prod, mallo(imallo)%trn_obs, mallo(imallo)%trn(itrn)%dtbl, mallo(imallo)%trn(itrn)%dtbl_num, mallo(imallo)%trn(itrn)%ob_num, mallo(imallo)%trn(itrn)%manure_amt%app_t_ha, mallo(imallo)%trn(itrn)%manure_amt%src_obj, mallo(imallo)%src(isrc)%fertdb, mallo(imallo)%trn(itrn)%manure_amt%app_method, mallo(imallo)%trn(itrn)%manure_amt, mallo(imallo)%src(isrc)%bal_d%withdr, mallo(imallo)%trn(itrn)%withdr(isrc)` |
| [sym:hru_module] | `phubase, sol_sumno3, sol_sumsolp, ihru, ipl, fertno3, fertnh3, fertorgn, fertsolp, fertorgp` |  |
| [sym:basin_module] | `pco` | `pco%mgtout` |
| [sym:time_module] | `time` | `time%day_mo, time%yrc, time%mo` |
| [sym:plant_module] | `pcom` |  |
| [sym:soil_module] | `soil` | `soil(j)%sw` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%tot(ipl)%m, pl_mass(j)%rsd_tot%m` |
| [sym:conditional_module] | `dtbl_lum, d_tbl` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mallo(imallo)%tot` | At the start of every call | Reset to the zeroed `malloz` template so the allocation object's daily totals begin clean for this simulation day. |
| `mallo(imallo)%src(isrc)%bal_d%stor` | On the first day of the month | Increased by the current month's production for the source object, adding newly produced manure to storage. |
| `mallo(imallo)%src(isrc)%bal_d%prod` | On the first day of the month | Set to the current day's monthly production value so the daily balance records how much was produced. |
| `d_tbl` | When a demand object has a valid decision table | Pointer is associated with `dtbl_lum(id)` so `conditions` and `actions` operate on the correct decision table. |
| `ihru` | When a demand object has a valid decision table | Not changed here directly; it is set later when a demand is converted into an application and the current HRU is identified. |
| `mallo(imallo)%trn(itrn)%manure_amt` | When a demand object qualifies for application | Reset to `manure_amtz` after `pl_fert` so the demand record is cleared once the application has been executed. |
| `mallo(imallo)%src(isrc)%bal_d%withdr` | When a demand object qualifies for application | Set to the applied amount `frt_kg` to record the source's daily withdrawal. |
| `mallo(imallo)%trn(itrn)%withdr(isrc)` | When a demand object qualifies for application | Set to the applied amount `frt_kg` to record the withdrawal against the demand object for that source. |

## File I/O

<!-- facts:io -->


## Lineage

`mallo_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `72206bc` (2026-01-07, "Enhance water allocation with recall support and update soil cover calculations"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mallo_control.f90` are listed.

- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `fd90e36` (2025-02-06) — variable initialization changes
- `eb22103` (2024-12-05) — Refactor residue management to use new soil1 structure
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No Git lineage commits were resolved for this source span.
- `mallo_control` has no extracted documentation comment in the provided source.
- The management-output write uses unit 2612, but the open/close lifecycle is not shown in this procedure.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
