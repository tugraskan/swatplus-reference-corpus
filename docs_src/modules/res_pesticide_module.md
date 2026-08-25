---
kind: module
symbol: res_pesticide_module
title: res_pesticide_module
status: filled
source_hash: f9de9f92dbe49b8a
version_label: SWAT+ 62.0.0
variables:
  res_pestbz: Baseline zeroed `res_pesticide_processes` value, declared at module scope and
    initialized by component defaults to 0.0 kg for every process field. It is used as the
    reset value after monthly, yearly, and average-annual summaries are finalized, and as
    the starting point for basin daily aggregation in `basin_res_pest_output` and for period
    reset in `res_pesticide_output`.
  respst_d: Allocatable array of per-reservoir daily pesticide output containers (`res_pesticide_output`),
    saved at module scope. `res_allo` allocates one element per reservoir and its per-pesticide
    `pest` array; `res_pest` populates the daily process values; `res_pesticide_output` and
    `basin_res_pest_output` read these daily values to build print records.
  respst_m: Allocatable array of per-reservoir monthly pesticide output containers, saved
    at module scope. `res_allo` sizes it for each reservoir and each pesticide; `res_pesticide_output`
    accumulates daily balances into it and writes monthly output; `basin_res_pest_output`
    also uses the daily reservoir balances to build basin monthly totals.
  respst_y: Allocatable array of per-reservoir yearly pesticide output containers, saved at
    module scope. `res_allo` allocates it; `res_pesticide_output` rolls monthly totals into
    it and writes yearly output; `basin_res_pest_output` uses it to form basin yearly summaries.
  respst_a: Allocatable array of per-reservoir average-annual pesticide output containers,
    saved at module scope. `res_allo` allocates it; `res_pesticide_output` rolls yearly totals
    into it and writes average-annual output, then resets the finished summary to `res_pestbz`.
  brespst_d: Basin-level daily pesticide output container, declared at module scope. `basin_res_pest_output`
    rebuilds it from `res_pestbz` plus all reservoir daily outputs for each pesticide and
    writes the basin daily reservoir pesticide report.
  brespst_m: Basin-level monthly pesticide output container, declared at module scope. `basin_res_pest_output`
    accumulates the current day’s basin pesticide balance into it so month-end basin summaries
    can be written.
  brespst_y: Basin-level yearly pesticide output container, declared at module scope. `basin_res_pest_output`
    rolls completed monthly basin totals into it for year-end output.
  brespst_a: Basin-level average-annual pesticide output container, declared at module scope.
    `basin_res_pest_output` accumulates year-end basin totals into it and converts it to a
    simulation-average annual value when end-of-simulation output is written.
  respst: Single `res_pesticide_output` container at module scope, available as shared reservoir
    pesticide summary state. The context packet does not show a direct resolved use for this
    symbol, but it is part of the public module state and is allocated/initialized with the
    other reservoir pesticide output containers.
  respstz: Single `res_pesticide_output` container at module scope, available as shared reservoir
    pesticide summary state. The context packet does not show a direct resolved use for this
    symbol, but it is part of the public module state and is available alongside `respst`
    for reservoir pesticide bookkeeping.
  respest_hdr: Module-scope `res_pesticide_header` record holding the text labels for reservoir
    pesticide output columns. `header_pest` writes this record to the reservoir pesticide
    text and CSV files so the output tables use the correct pesticide balance headers.
type_components:
  res_pesticide_processes:
    tot_in: kg        !total pesticide into reservoir
    sol_out: kg        !soluble pesticide out of reservoir
    sor_out: kg        !sorbed pesticide out of reservoir
    react: kg        !pesticide lost through reactions in water layer
    metab: kg        !pesticide metabolized from parent in water layer
    volat: kg        !pesticide lost through volatilization
    settle: kg        !pesticide settling to sediment layer
    resus: kg        !pesticide resuspended into lake water
    difus: kg        !pesticide diffusing from sediment to water
    react_bot: kg        !pesticide lost from benthic sediment by reactions
    metab_bot: kg        !pesticide metabolized from parent in water layer
    bury: kg        !pesticide lost from benthic sediment by burial
    water: kg        !pesticide in water at end of day
    benthic: kg        !pesticide in benthic sediment at end of day
  res_pesticide_output:
    pest: pesticide hydrographs
  res_pesticide_header:
    day: Header label for the simulation day (`jday`) column.
    mo: Header label for the month (`mon`) column.
    day_mo: Header label for the day-of-month (`day`) column.
    yrc: Header label for the simulation year (`yr`) column.
    isd: Header label for the reservoir unit number column.
    id: Header label for the GIS id column.
    name: Header label for the reservoir name column.
    pest: Header label for the pesticide name column.
    tot_in: (kg)
    sol_out: (kg)
    sor_out: (kg)
    react: (kg)
    metab: (kg)
    volat: (kg)
    settle: (kg)
    resus: (kg)
    difus: (kg)
    react_bot: (kg)
    metab_bot: (kg)
    bury: (kg)
    water: (kg)
    benthic: (kg)
type_summaries:
  res_pesticide_processes: One record holds the reservoir pesticide mass-balance terms for
    a single pesticide and reporting interval. It combines inflow, outflow, transformation,
    exchange, and storage terms, all in kilograms, and the component defaults initialize the
    record to zero.
  res_pesticide_output: One record holds a `pest` array of `res_pesticide_processes` values,
    indexed by pesticide, for a reservoir or basin reporting scope. It is the container used
    for daily, monthly, yearly, and average-annual output streams.
  res_pesticide_header: One record stores the literal column labels written at the top of
    reservoir pesticide report files. It includes time, identification, pesticide name, and
    the mass-balance column headers used by `header_pest`.
---

<!-- facts:header -->

`res_pesticide_module` owns the reservoir pesticide process-balance record types, the per-reservoir and basin summary containers used for daily/monthly/yearly/average outputs, and the reusable header record for reservoir pesticide report files. It is a declaration-and-operator module: no startup routine populates its state here, but other reservoir allocation, header-writing, and output procedures allocate, reset, aggregate, and print the variables it defines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a shared declaration container. Its derived-type component defaults initialize the process-balance records to zero, while `res_allo` allocates the per-reservoir arrays and other routines populate and reset them during simulation.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:basin_res_pest_output] | `unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | Reads the daily reservoir pesticide outputs and the baseline zero record, then builds basin-level daily, monthly, yearly, and average-annual pesticide summaries for writing to the reservoir basin output files. |
| [sym:header_pest] | `unit_2800, unit_9000, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807, unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815, unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823, unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007, unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015, unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839, unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855, unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | Writes the reservoir pesticide header record from this module to the active reservoir pesticide text and CSV files so later output rows have the correct column names. |
| [sym:res_cs_output] | `unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | The resolved source did not show a direct symbol use from this module, so this routine is only known to import the module as part of the reservoir constituent-output environment. |
| [sym:res_pesticide_output] | `unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | Accumulates daily reservoir pesticide balances into the monthly, yearly, and average-annual summary containers, writes the selected report rows, and resets finished summaries back to the zero baseline. |
| [sym:res_salt_output] | `unit_5040, unit_5041, unit_5042, unit_5043, unit_5044, unit_5045, unit_5046, unit_5047` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | The resolved source did not show a direct symbol use from this module, so this routine is only known to import the module as a shared reservoir-output dependency. |
| [sym:wet_cs_output] | `unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | The resolved source did not show any direct symbol use from this module, so the module is only known as an imported dependency in the wetland constituent-output workflow. |
| [sym:wet_salt_output] | `unit_5090, unit_5091, unit_5092, unit_5093, unit_5094, unit_5095, unit_5096, unit_5097` | `res_pestbz, respst_d, respst_m, respst_y, respst_a, brespst_d` | The resolved source did not show any direct symbol use from this module, so the module is only known as a shared dependency in the wetland salt-output workflow. |

## Key Consumers

The module is imported by reservoir pesticide computation, allocation, header-writing, and output routines. Some consumers use the pesticide process arrays directly; others only need the header record or the shared reservoir pesticide state container definitions.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_res_pest_output] | res_pesticide_module | Builds basin pesticide balances by starting from `res_pestbz`, summing each reservoir's daily pesticide outputs into `brespst_d%pest(ipest)`, and rolling those daily values into monthly, yearly, and average-annual basin summaries for output. |
| [sym:header_pest] | res_pesticide_module | Uses `respest_hdr` so the reservoir pesticide day, month, year, and average-annual files are opened and labeled with the correct pesticide header row before any results are written. |
| [sym:res_allo] | res_pesticide_module | Allocates the reservoir pesticide summary arrays (`respst_d`, `respst_m`, `respst_y`, `respst_a`) for each reservoir and each pesticide, making the output containers available before simulation updates begin. |
| [sym:res_cs_output] | res_pesticide_module | Imports the module as part of the reservoir output state environment, but the extracted procedure body did not resolve a direct use of any pesticide symbol. |
| [sym:res_pest] | res_pesticide_module | Populates `respst_d(jres)%pest(ipst)` with the daily pesticide mass-balance terms produced by the reservoir process, including input, reaction, volatilization, settling, resuspension, diffusion, burial, and end-of-day storage. |
| [sym:res_pesticide_output] | res_pesticide_module | Accumulated daily pesticide balances are copied into `respst_m`, then rolled into `respst_y` and `respst_a` at month-end and year-end, with finished summaries reset to `res_pestbz` after output. |
| [sym:res_salt_output] | res_pesticide_module | Imported alongside the reservoir salt reporting state as part of the broader reservoir output framework, but no direct pesticide symbol use was resolved in the extracted body. |
| [sym:wet_cs_output] | res_pesticide_module | Imported as a shared dependency in the wetland constituent-output workflow, but the extracted body did not resolve a direct use of any pesticide symbol from this module. |
| [sym:wet_salt_output] | res_pesticide_module | Imported as part of the wetland salt reporting environment, but the extracted body did not resolve a direct use of any pesticide symbol from this module. |

## Lineage

`res_pesticide_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_pesticide_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `res_pesticide_module` has no extracted module-level documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
