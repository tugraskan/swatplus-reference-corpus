---
kind: module
symbol: res_cs_module
title: res_cs_module
status: filled
source_hash: 64a20a889dbc578b
version_label: SWAT+ 62.0.0
variables:
  res_csbz: Shared zero-initialized `res_cs_balance` scratch record for reservoir or wetland
    constituent bookkeeping. It is declared in this module and used by constituent balance
    routines as a reusable balance component container; source evidence shows the structured
    fields are all mass or volume terms in kg, g/m3, and m3.
  rescs_d: Daily reservoir constituent output array. `res_allo` allocates it, `res_cs` fills
    it for each reservoir and constituent, `cs_balance` resets its fields at day start, and
    `res_cs_output` accumulates it into longer-period summaries.
  rescs_m: Monthly reservoir constituent output array. It is allocated in `res_allo` and accumulated
    by `res_cs_output` from the daily reservoir constituent balances before monthly output
    is written.
  rescs_y: Yearly reservoir constituent output array. It is allocated in `res_allo` and accumulated
    by `res_cs_output` from monthly totals for annual reservoir constituent reporting.
  rescs_a: Average-annual reservoir constituent output array. It is allocated in `res_allo`
    and accumulated by `res_cs_output` for all-years reservoir constituent reporting.
  wetcs_d: Daily wetland constituent output array. `hru_allo` allocates it, `wet_cs` and `cs_fert_wet`
    update its daily flux and state terms, `cs_irrig` and `gwflow_pump_allo` add irrigation
    transfers, and `cs_balance` resets it at day start.
  wetcs_m: Monthly wetland constituent output array. It is allocated in `hru_allo` and accumulated
    by `wet_cs_output` from the daily wetland constituent balances for monthly reporting.
  wetcs_y: Yearly wetland constituent output array. It is allocated in `hru_allo` and accumulated
    by `wet_cs_output` from monthly wetland totals for annual reporting.
  wetcs_a: Average-annual wetland constituent output array. It is allocated in `hru_allo`
    and accumulated by `wet_cs_output` for all-years wetland constituent reporting.
  res_cs_data: Shared allocatable table of `reservoir_cs_data` records loaded from `cs_res`
    by `res_read_csdb`. It provides the reservoir/wetland constituent species name and the
    parameter values used by `res_initial`, `wet_initial`, `res_cs`, and `wet_cs`.
  rescs_hdr: Shared `res_cs_header` record containing the column labels written to reservoir
    constituent daily, monthly, yearly, and average-annual output files by `header_const`.
    It is a fixed label container, not simulation state.
type_components:
  res_cs_balance:
    inflow: kg        !constituent entering the reservoir
    outflow: kg        !constituent leaving the reservoir via streamflow
    seep: kg        !constituent leaving the reservoir via seepage to aquifer
    settle: kg        !constituent settling to bottom of reservoir
    rctn: kg        !constituent removal due to chemical reaction
    prod: kg        !constituent produced due to chemical reaction
    fert: kg        !constituent added in fertilizer (to wetland)
    irrig: kg        !constituent removed from the reservoir via irrigation diversion
    div: kg        !constituent removed or added via diversion
    mass: kg        !constituent in reservoir water at end of day
    conc: g/m3      !constituent concentration in reservoir at end of day
    volm: m3        !volume of water in the reservoir
  res_cs_output:
    cs: constituents hydrographs
  reservoir_cs_data:
    name: constituent lookup name used to match reservoir and wetland input records
    v_seo4: m/day      |settling rate for selenate
    v_seo3: m/day      |settling rate for selinite
    v_born: m/day      |settling rate for boron
    k_seo4: 1/day      |first-order degradation constant for selenate
    k_seo3: 1/day      |first-order degradation constant for selenite
    k_born: 1/day      |first-order degradation constant for boron
    theta_seo4: none       |temperature adjustment for selenate degradation
    theta_seo3: none       |temperature adjustment for selenite degradation
    theta_born: none       |temperature adjustment for boron degradation
    c_seo4: g/m3       |initial concentration of selenate
    c_seo3: g/m3       |initial concentration of selenite
    c_born: g/m3       |initial concentration of boron
  res_cs_header:
    day: daily Julian day header label
    mo: month header label
    day_mo: day-of-month header label
    yrc: year header label
    isd: reservoir or wetland unit number header label
    id: GIS identifier header label
    seo4in: selenate inflow column label
    seo3in: selenite inflow column label
    bornin: boron inflow column label
    seo4out: selenate outflow column label
    seo3out: selenite outflow column label
    bornout: boron outflow column label
    seo4seep: selenate seepage column label
    seo3seep: selenite seepage column label
    bornseep: boron seepage column label
    seo4setl: selenate settling column label
    seo3setl: selenite settling column label
    bornsetl: boron settling column label
    seo4rctn: selenate reaction-loss column label
    seo3rctn: selenite reaction-loss column label
    bornrctn: boron reaction-loss column label
    seo4prod: selenate production column label
    seo3prod: selenite production column label
    bornprod: boron production column label
    seo4fert: selenate fertilizer column label
    seo3fert: selenite fertilizer column label
    bornfert: boron fertilizer column label
    seo4irr: selenate irrigation column label
    seo3irr: selenite irrigation column label
    bornirr: boron irrigation column label
    seo4div: selenate diversion column label
    seo3div: selenite diversion column label
    borndiv: boron diversion column label
    seo4: selenate mass column label
    seo3: selenite mass column label
    born: boron mass column label
    seo4c: selenate concentration column label
    seo3c: selenite concentration column label
    bornc: boron concentration column label
    volm: water volume column label
type_summaries:
  res_cs_balance: reservoir balance components
  res_cs_output: Reservoir constituent hydrograph record used for reporting one reservoir
    over a time scale.
  reservoir_cs_data: reservoir constituent parameters
  res_cs_header: output file headers
---

<!-- facts:header -->

`res_cs_module` owns the shared reservoir and wetland constituent bookkeeping state for SWAT+: the daily/monthly/yearly/average-annual mass-balance arrays, the reservoir constituent parameter table, and the output header record used by reservoir and wetland constituent reports. It is initialized indirectly by allocation and reader routines such as `res_allo`, `hru_allo`, `res_read_csdb`, `res_read_salt_cs`, `wet_read_salt_cs`, `res_initial`, and `wet_initial`, and it is consumed by the reservoir/wetland process and output routines that update or print constituent balances.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it has no contained procedures. Its arrays and records are populated by allocation routines and reader/initializer procedures elsewhere in the model.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Resets reservoir and wetland constituent daily balance arrays to zero at day start so new fluxes can be accumulated cleanly. |
| [sym:gwflow_canal_div] | `unit_canal_name, unit_out_canal_bal, unit_out_canal_sol` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Uses the wetland constituent balance array as part of canal-groundwater solute accounting in the shared constituent bookkeeping structure. |
| [sym:header_const] | `unit_6080, unit_6082, unit_6084, unit_6086, unit_6021, unit_6022, unit_6023, unit_6024, unit_6025, unit_6026, unit_6027, unit_6028, unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067, unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037, unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047, unit_6070, unit_6071, unit_6072, unit_6073, unit_6074, unit_6075, unit_6076, unit_6077, unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Writes the reservoir and wetland constituent header record so reservoir constituent output files use the module's shared column labels. |
| [sym:res_cs_output] | `unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Reads and updates reservoir constituent summary arrays, rolling daily values into monthly, yearly, and average-annual output records. |
| [sym:res_initial] | `unit_105` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Reads reservoir constituent initial concentrations from `res_cs_data` and uses them to seed reservoir water-quality state. |
| [sym:res_read] | `reservoir.res` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Imports the module so reservoir setup has the shared constituent definitions available alongside the main reservoir records. |
| [sym:res_read_csdb] | `cs_res` | `res_csbz, rescs_m, rescs_y, rescs_a, wetcs_d` | Allocates and fills `res_cs_data` from the `cs_res` database file so later reservoir and wetland routines can look up constituent parameters by index. |
| [sym:res_read_salt_cs] | `reservoir.res_cs` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Uses `res_cs_data` names to resolve reservoir constituent name strings into numeric constituent-table indexes. |
| [sym:wet_cs_output] | `unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Reads and updates wetland constituent summary arrays, rolling daily values into monthly, yearly, and average-annual output records. |
| [sym:wet_read] | `wetland.wet` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Imports the module so wetland setup can use the shared constituent definitions alongside the main wetland records. |
| [sym:wet_read_salt_cs] | `wetland.wet_cs` | `res_csbz, rescs_d, rescs_m, rescs_y, rescs_a, wetcs_d` | Uses `res_cs_data` names to resolve wetland constituent name strings into numeric constituent-table indexes. |

## Key Consumers

The module is imported by allocation, reader, initialization, process, and output routines for reservoir and wetland constituent accounting. Reservoir-side routines use it to size and populate constituent water-quality state; wetland-side routines use it to do the same for wetland pools and their output summaries; setup routines use `res_cs_data` and `rescs_hdr` to connect text-file records and headers to the model's numeric state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cs_balance] | `wetcs_d`, `rescs_d` | Reservoir and wetland constituent daily balance arrays are cleared at the start of the basin balance summary so the next day’s constituent fluxes begin from zero. |
| [sym:header_const] | res_cs_module | `header_const` writes `rescs_hdr` into the reservoir constituent output files, ensuring the daily, monthly, yearly, and average-annual reservoir reports use the shared constituent column labels. |
| [sym:res_cs_output] | res_cs_module | `res_cs_output` uses the reservoir constituent arrays to accumulate daily values into monthly, yearly, and average-annual reservoir balance records. |
| [sym:res_initial] | res_cs_module | `res_initial` reads `res_cs_data(icon)%c_seo4`, `res_cs_data(icon)%c_seo3`, and `res_cs_data(icon)%c_born` to seed the reservoir's initial selenium and boron concentrations and masses. |
| [sym:res_read_csdb] | res_cs_module | `res_read_csdb` allocates and fills the shared `res_cs_data` table from `cs_res`, making reservoir constituent parameter records available to later setup and simulation routines. |
| [sym:res_read_salt_cs] | res_cs_module | `res_read_salt_cs` uses `res_cs_data` names to resolve the reservoir constituent file's string references into numeric constituent indexes. |
| [sym:wet_cs_output] | res_cs_module | `wet_cs_output` uses the wetland constituent arrays to accumulate daily values into monthly, yearly, and average-annual wetland balance records. |
| [sym:wet_read_salt_cs] | res_cs_module | `wet_read_salt_cs` uses `res_cs_data` names to resolve wetland constituent file string references into numeric constituent indexes. |
| [sym:gwflow_canal_div] | `wetcs_d` | The wetland constituent-balance array participates in the shared solute accounting path used when canal seepage exchanges are summarized for groundwater and downstream balance outputs. |
| [sym:res_read] | res_cs_module | `res_read` imports the module so reservoir setup can access the shared constituent definitions alongside the main reservoir records. |
| [sym:wet_read] | res_cs_module | `wet_read` imports the module so wetland setup can access the shared constituent definitions alongside the main wetland records. |
| [sym:cs_fert_wet] | `wetcs_d` | `cs_fert_wet` writes fertilizer-applied masses into `wetcs_d(jj)%cs(1:3)%fert` so wetland constituent output records capture the added seo4, seo3, and boron mass. |
| [sym:gwflow_pump_allo] | `wetcs_d` | `gwflow_pump_allo` records pumped constituent mass in `wetcs_d(hru_id)%cs(ics)%irrig` when groundwater irrigation water is applied to a wetland HRU. |
| [sym:cs_irrig] | res_cs_module | `cs_irrig` records irrigation-related constituent removals in `rescs_d` and `wetcs_d` so reservoir and wetland mass-balance output reflects how much mass left source water with irrigation withdrawals. |
| [sym:hru_allo] | res_cs_module | `hru_allo` allocates the wetland constituent output arrays so wetland constituent balances can be recorded at daily, monthly, yearly, and average-annual time scales. |
| [sym:res_allo] | res_cs_module | `res_allo` allocates the reservoir constituent output arrays so non-salt reservoir constituent tracking has storage before reservoir simulation begins. |
| [sym:res_cs] | res_cs_module | `res_cs` fills `rescs_d` with daily reservoir inflow, outflow, seepage, settling, reaction, irrigation, mass, and concentration terms using the parameter values in `res_cs_data`. |
| [sym:wet_cs] | res_cs_module | `wet_cs` fills `wetcs_d` with daily wetland constituent inflow, outflow, seepage, settling, reaction, mass, and concentration terms using the parameter values in `res_cs_data`. |
| [sym:wet_initial] | res_cs_module | `wet_initial` reads the shared constituent initial concentrations from `res_cs_data` and copies them into `wet_water(iihru)` during wetland startup. |
| [sym:sim_initday] | res_cs_module | `sim_initday` includes the module so reservoir carbon/constituent bookkeeping can be reset together with other daily model state at day start. |

## Lineage

`res_cs_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `f1e61a3` (2024-10-08, "fixed tabs"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_cs_module.f90` are listed.

- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `res_cs_module` has no extracted module-level documentation comment.
- No lineage commits were resolved for this source span, so no diff-based history can be summarized.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
