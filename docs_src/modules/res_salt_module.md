---
kind: module
symbol: res_salt_module
title: res_salt_module
status: filled
source_hash: 76a79481e735fa9c
version_label: SWAT+ 62.0.0
variables:
  res_saltbz: Default-initialized single `res_salt_balance` record used as the module's scalar
    salt-balance template/state container. Its fields start at zero and represent the same
    salt terms as the per-object output records; consumers are the reservoir and wetland salt
    balance routines that update or mirror these components.
  ressalt_d: Allocatable daily reservoir salt-output arrays. Each element holds one reservoir's
    per-salt daily balance records, initialized/allocated by `res_allo` and filled by `res_salt`;
    later written and reset by `res_salt_output` and summarized by `salt_balance`.
  ressalt_m: Allocatable monthly reservoir salt-output arrays. Each element accumulates daily
    reservoir salt terms for monthly reporting, allocated by `res_allo`, accumulated by `res_salt_output`,
    and written/reset at month end.
  ressalt_y: Allocatable yearly reservoir salt-output arrays. Each element accumulates daily
    reservoir salt terms for annual reporting, allocated by `res_allo` and rolled forward
    by `res_salt_output`.
  ressalt_a: Allocatable average-annual reservoir salt-output arrays. Each element stores
    cumulative reservoir salt terms for end-of-simulation averaging, allocated by `res_allo`
    and updated by `res_salt_output`.
  wetsalt_d: Allocatable daily wetland salt-output arrays. Each element holds one wetland/HRU's
    per-salt daily balance records, allocated by `hru_allo`, filled by `wet_salt`, `salt_fert_wet`,
    and `salt_irrig`, then summarized by `wet_salt_output` and basin totals in `salt_balance`.
  wetsalt_m: Allocatable monthly wetland salt-output arrays. Each element accumulates daily
    wetland salt terms for monthly reporting, allocated by `hru_allo`, accumulated by `wet_salt_output`,
    and cleared after monthly output.
  wetsalt_y: Allocatable yearly wetland salt-output arrays. Each element accumulates daily
    wetland salt terms for annual reporting, allocated by `hru_allo` and rolled forward by
    `wet_salt_output`.
  wetsalt_a: Allocatable average-annual wetland salt-output arrays. Each element stores cumulative
    wetland salt terms for end-of-simulation averaging, allocated by `hru_allo` and updated
    by `wet_salt_output`.
  res_salt_data: Allocatable reservoir salt database loaded from `salt_res`. Each record stores
    a reservoir salt name and its per-salt-ion initial concentrations in `c_init`; it is populated
    by `res_read_saltdb` and read by `res_initial`, `wet_initial`, `res_read_salt_cs`, and
    `wet_read_salt_cs`.
  ressalt_hdr: Module-level reservoir salt output header record with fixed column labels and
    default text values. It is written by `header_salt` to the reservoir salt output units
    and CSV files.
type_components:
  res_salt_balance:
    inflow: kg        !salt entering the reservoir via streamflow
    outflow: kg        !salt leaving the reservoir via streamflow
    seep: kg        !salt leaving the reservoir via seepage to aquifer
    fert: kg        !salt added to reservoir (wetland) via fertilizer
    irrig: kg        !salt removed from the reservoir via irrigation diversion
    div: kg        !salt mass removed or added via diversion
    mass: kg        !salt in reservoir water at end of day
    conc: g/m3      !salt concentration in reservoir at end of day
    volm: m3        !volume of water in the reservoir
  res_salt_output:
    salt: salt hydrographs
  reservoir_salt_data:
    name: Reservoir salt identifier read from `salt_res` and matched against reservoir or
      wetland salt names in the CS readers.
    c_init: g/m3       |initial concentration of each salt ion
  res_salt_header:
    day: Day-of-year label printed in the reservoir salt tables.
    mo: Month label printed in the reservoir salt tables.
    day_mo: Day-of-month label printed in the reservoir salt tables.
    yrc: Year label printed in the reservoir salt tables.
    isd: Model unit/object label printed in the reservoir salt tables.
    id: GIS or object identifier label printed in the reservoir salt tables.
    so4in: Sulfate inflow column label.
    cain: Calcium inflow column label.
    mgin: Magnesium inflow column label.
    nain: Sodium inflow column label.
    kin: Potassium inflow column label.
    clin: Chloride inflow column label.
    co3in: Carbonate inflow column label.
    hco3in: Bicarbonate inflow column label.
    so4out: Sulfate outflow column label.
    caout: Calcium outflow column label.
    mgout: Magnesium outflow column label.
    naout: Sodium outflow column label.
    kout: Potassium outflow column label.
    clout: Chloride outflow column label.
    co3out: Carbonate outflow column label.
    hco3out: Bicarbonate outflow column label.
    so4seep: Sulfate seepage column label.
    caseep: Calcium seepage column label.
    mgseep: Magnesium seepage column label.
    naseep: Sodium seepage column label.
    kseep: Potassium seepage column label.
    clseep: Chloride seepage column label.
    co3seep: Carbonate seepage column label.
    hco3seep: Bicarbonate seepage column label.
    so4fert: Sulfate fertilizer column label.
    cafert: Calcium fertilizer column label.
    mgfert: Magnesium fertilizer column label.
    nafert: Sodium fertilizer column label.
    kfert: Potassium fertilizer column label.
    clfert: Chloride fertilizer column label.
    co3fert: Carbonate fertilizer column label.
    hco3fert: Bicarbonate fertilizer column label.
    so4irr: Sulfate irrigation column label.
    cairr: Calcium irrigation column label.
    mgirr: Magnesium irrigation column label.
    nairr: Sodium irrigation column label.
    kirr: Potassium irrigation column label.
    clirr: Chloride irrigation column label.
    co3irr: Carbonate irrigation column label.
    hco3irr: Bicarbonate irrigation column label.
    so4div: Sulfate diversion column label.
    cadiv: Calcium diversion column label.
    mgdiv: Magnesium diversion column label.
    nadiv: Sodium diversion column label.
    kdiv: Potassium diversion column label.
    cldiv: Chloride diversion column label.
    co3div: Carbonate diversion column label.
    hco3div: Bicarbonate diversion column label.
    so4: Sulfate mass column label.
    ca: Calcium mass column label.
    mg: Magnesium mass column label.
    na: Sodium mass column label.
    k: Potassium mass column label.
    cl: Chloride mass column label.
    co3: Carbonate mass column label.
    hco3: Bicarbonate mass column label.
    so4c: Sulfate concentration column label.
    cac: Calcium concentration column label.
    mgc: Magnesium concentration column label.
    nac: Sodium concentration column label.
    kc: Potassium concentration column label.
    clc: Chloride concentration column label.
    co3c: Carbonate concentration column label.
    hco3c: Bicarbonate concentration column label.
    volm: Water-volume column label.
type_summaries:
  res_salt_balance: One reservoir or wetland salt mass-balance record for a single salt ion
    and time step, storing fluxes, end-of-step storage, concentration, and volume.
  res_salt_output: A container of per-salt reservoir salt-balance records for one reservoir
    and one reporting interval.
  reservoir_salt_data: Reservoir salt-lookup record loaded from the external salt database.
  res_salt_header: Fixed text labels used as the header row for reservoir salt output files.
---

<!-- facts:header -->

`res_salt_module` owns the shared salt-state records used by reservoir and wetland salt accounting: one daily balance record, daily/monthly/yearly/average-annual output arrays for reservoirs and wetlands, the reservoir salt lookup table loaded from input, and the header strings used when salt output files are written. Allocation and initialization happen in setup and reader routines such as `res_allo`, `hru_allo`, `res_read_saltdb`, `res_initial`, and `wet_initial`; simulation and reporting routines such as `res_salt`, `wet_salt`, `salt_irrig`, `salt_fert_wet`, `salt_balance`, `res_salt_output`, and `wet_salt_output` depend on this shared state.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a shared declaration container; it does not contain setup code itself. Its arrays and lookup tables are allocated and populated by other routines, especially `res_allo`, `hru_allo`, `res_read_saltdb`, `res_initial`, and `wet_initial`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:gwflow_canal_div] | `unit_canal_name, unit_out_canal_bal, unit_out_canal_sol` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Uses the wetland salt output array in shared solute bookkeeping for canal-groundwater exchange. |
| [sym:header_salt] | `unit_5080, unit_5082, unit_5084, unit_5086, unit_5021, unit_5022, unit_5023, unit_5024, unit_5025, unit_5026, unit_5027, unit_5028, unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067, unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037, unit_5040, unit_5041, unit_5042, unit_5043, unit_5044, unit_5045, unit_5046, unit_5047, unit_5070, unit_5071, unit_5072, unit_5073, unit_5074, unit_5075, unit_5076, unit_5077, unit_5090, unit_5091, unit_5092, unit_5093, unit_5094, unit_5095, unit_5096, unit_5097` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Writes the module's reservoir salt header record to the configured reservoir salt output files and CSV files. |
| [sym:res_initial] | `unit_105` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Reads reservoir initial state and uses `res_salt_data` to seed reservoir salt concentrations when a salt database is configured. |
| [sym:res_read] | `reservoir.res` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Loads reservoir definitions before later salt initialization and reporting routines use the shared reservoir state. |
| [sym:res_read_salt_cs] | `reservoir.res_cs` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Resolves reservoir salt names from the constituent file into numeric lookup indices using `res_salt_data`. |
| [sym:res_read_saltdb] | `salt_res` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Reads the external reservoir salt database and allocates `res_salt_data` for downstream initialization routines. |
| [sym:res_salt_output] | `unit_5040, unit_5041, unit_5042, unit_5043, unit_5044, unit_5045, unit_5046, unit_5047` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Accumulates, averages, writes, and clears reservoir salt summaries in the reservoir output workflow. |
| [sym:salt_balance] | `unit_5080, unit_5082, unit_5084, unit_5086` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Builds basin-scale salt totals from reservoir and wetland daily balance arrays and then resets the daily terms. |
| [sym:wet_read] | `wetland.wet` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Loads wetland definitions before wetland salt state is initialized elsewhere. |
| [sym:wet_read_salt_cs] | `wetland.wet_cs` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Resolves wetland salt names from the wetland constituent file into numeric lookup indices using `res_salt_data`. |
| [sym:wet_salt_output] | `unit_5090, unit_5091, unit_5092, unit_5093, unit_5094, unit_5095, unit_5096, unit_5097` | `res_saltbz, ressalt_d, ressalt_m, ressalt_y, ressalt_a, wetsalt_d` | Accumulates, averages, writes, and clears wetland salt summaries in the wetland output workflow. |

## Key Consumers

This module is imported by the reservoir and wetland salt balance, initialization, allocation, input-reading, and output routines. The main consumers are `res_allo` and `hru_allo` for allocation, `res_read_saltdb`, `res_initial`, `wet_initial`, `res_read_salt_cs`, and `wet_read_salt_cs` for loading and resolving salt definitions, and `res_salt`, `wet_salt`, `salt_irrig`, `salt_fert_wet`, `res_salt_output`, `wet_salt_output`, `salt_balance`, and `header_salt` for simulation and reporting.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:salt_balance] | `wetsalt_d`, `ressalt_d` | Adds reservoir and wetland daily salt fluxes into basin-wide salt totals, writes the daily/monthly/yearly/average reports, and clears the daily reservoir and wetland salt terms after reporting. |
| [sym:header_salt] | res_salt_module | Writes the fixed reservoir-salt header record to the reservoir salt output units and CSV files. |
| [sym:res_initial] | res_salt_module | Seeds reservoir salt concentrations from `res_salt_data(icon)%c_init(isalt)` when the reservoir uses a salt initialization file. |
| [sym:res_read_salt_cs] | res_salt_module | Matches reservoir salt names from `reservoir.res_cs` against `res_salt_data` and stores the resolved salt-table index in reservoir data. |
| [sym:res_read_saltdb] | res_salt_module | Allocates and fills the reservoir salt database from `salt_res`, including each record's salt-ion initial concentrations. |
| [sym:res_salt_output] | res_salt_module | Accumulates reservoir daily salt balances into monthly, yearly, and average-annual outputs, writes the selected records, and resets the monthly accumulators at period boundaries. |
| [sym:wet_read_salt_cs] | res_salt_module | Matches wetland salt names from `wetland.wet_cs` against `res_salt_data` and stores the resolved salt-table index in wetland data. |
| [sym:wet_salt_output] | res_salt_module | Accumulates wetland daily salt balances into monthly, yearly, and average-annual outputs, writes the selected records, and clears the monthly accumulators at period boundaries. |
| [sym:gwflow_canal_div] | `wetsalt_d` | Records canal-groundwater solute transfer in the shared accounting framework that also carries wetland salt balance outputs. |
| [sym:gwflow_pump_allo] | `wetsalt_d` | Stores irrigation-delivered salt mass in the wetland daily salt balance output when pumped groundwater is routed to wetland HRUs. |
| [sym:hru_allo] | res_salt_module | Allocates the wetland salt output arrays so later wetland salt balances have daily, monthly, yearly, and average-annual storage. |
| [sym:res_allo] | res_salt_module | Allocates the reservoir salt output arrays so later reservoir salt balances have daily, monthly, yearly, and average-annual storage. |
| [sym:res_salt] | res_salt_module | Initializes and fills per-reservoir salt balance terms for the current day before they are written to reservoir output. |
| [sym:salt_fert_wet] | res_salt_module | Adds fertilizer-derived salt masses to wetland water storage and records the fertilizer contribution in the daily wetland salt balance. |
| [sym:salt_irrig] | res_salt_module | Tracks reservoir withdrawals and wetland additions for irrigation-driven salt transfers in the reservoir and wetland daily salt balances. |
| [sym:wet_initial] | res_salt_module | Seeds wetland salt concentrations from `res_salt_data(icon)%c_init` when the wetland uses a salt initialization file. |
| [sym:wet_read] | res_salt_module | Loads wetland definitions before later wetland salt initialization and routing routines use them. |
| [sym:wet_salt] | res_salt_module | Initializes and fills per-wetland daily salt balance terms before they are written to wetland output and runoff summaries. |

## Lineage

`res_salt_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `f1e61a3` (2024-10-08, "fixed tabs"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_salt_module.f90` are listed.

- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level import section was extracted; the module appears to be a pure declaration container.
- No commits were resolved for this source span in the provided Git lineage evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
