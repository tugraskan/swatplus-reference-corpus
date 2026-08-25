---
kind: module
symbol: aqu_pesticide_module
title: aqu_pesticide_module
status: filled
source_hash: ecb4053aa8a6f771
version_label: SWAT+ 62.0.0
variables:
  aqu_pestbz: Zero-valued baseline `aqu_pesticide_processes` record used as a reset/seed object
    for basin daily pesticide accumulation in `basin_aqu_pest_output`. Its fields are in kg
    and the record is also used as a clean starting value when rebuilding basin summaries.
  aqupst_d: Allocatable per-aquifer daily pesticide output array of `aqu_pesticide_output`
    records. It is allocated in `aqu_initial`, seeded from current aquifer pesticide mass
    in `aqu_pest_output_init`, updated by `aqu_1d_control` for daily mass-balance terms, and
    written by `aqu_pesticide_output` and `basin_aqu_pest_output`. The contained `pest` records
    store kg mass balances.
  aqupst_m: Allocatable per-aquifer monthly pesticide output array of `aqu_pesticide_output`
    records. It is allocated in `aqu_initial`, initialized from current aquifer pesticide
    mass in `aqu_pest_output_init`, accumulated from daily values in `aqu_pesticide_output`,
    and used by the monthly aquifer pesticide reports. Component values are kg.
  aqupst_y: Allocatable per-aquifer yearly pesticide output array of `aqu_pesticide_output`
    records. It is allocated in `aqu_initial`, initialized from current aquifer pesticide
    mass in `aqu_pest_output_init`, accumulated from monthly values in `aqu_pesticide_output`,
    and used by the yearly aquifer pesticide reports. Component values are kg.
  aqupst_a: Allocatable per-aquifer average-annual pesticide output array of `aqu_pesticide_output`
    records. It is allocated in `aqu_initial`, initialized from current aquifer pesticide
    mass in `aqu_pest_output_init`, accumulated from yearly values in `aqu_pesticide_output`,
    and used by the average-annual aquifer pesticide reports. Component values are kg.
  baqupst_d: Basin-wide daily pesticide output record used for aquifer pesticide reporting.
    Its `pest` array is allocated in `aqu_initial`, cleared and filled from per-aquifer daily
    values in `basin_aqu_pest_output`, and then written to the basin daily aquifer pesticide
    files. Component values are kg.
  baqupst_m: Basin-wide monthly pesticide output record used for aquifer pesticide reporting.
    Its `pest` array is allocated in `aqu_initial`, accumulated from basin daily results in
    `basin_aqu_pest_output`, and written to the basin monthly aquifer pesticide files. Component
    values are kg.
  baqupst_y: Basin-wide yearly pesticide output record used for aquifer pesticide reporting.
    Its `pest` array is allocated in `aqu_initial`, accumulated from monthly results in `basin_aqu_pest_output`,
    and written to the basin yearly aquifer pesticide files. Component values are kg.
  baqupst_a: Basin-wide average-annual pesticide output record used for aquifer pesticide
    reporting. Its `pest` array is allocated in `aqu_initial`, accumulated from yearly results
    in `basin_aqu_pest_output`, and written to the basin average-annual aquifer pesticide
    files. Component values are kg.
  aqupst: Single `aqu_pesticide_output` record available as a public module variable, but
    no resolved procedure in the context packet references it directly. It exists as shared
    storage of the same process-record shape as the array entries.
  aqupstz: Single `aqu_pesticide_output` record available as a public module variable, but
    no resolved procedure in the context packet references it directly. It exists as shared
    storage of the same process-record shape as the array entries.
  aqupest_hdr: Header record holding column labels for aquifer pesticide output files. It
    is written by `header_pest` to basin aquifer pesticide text and CSV files so the output
    columns match the process fields in the module's pesticide records.
type_components:
  aqu_pesticide_processes:
    tot_in: kg total pesticide into aquifer
    sol_flo: kg soluble pesticide out of aquifer
    sor_flo: kg sorbed pesticide out of aquifer
    sol_perc: kg pesticide leaving by percolation
    react: kg pesticide lost through reactions
    metab: kg amount of pesticide metabolized from parent
    stor_ave: kg average end-of-day pesticide in aquifer during the time period
    stor_init: kg pesticide in aquifer at the start of the day
    stor_final: kg pesticide in aquifer at the end of the day
  aqu_pesticide_output:
    pest: Array of pesticide hydrograph/process records for the reporting scope
  aqu_pesticide_header:
    day: column label for day of year
    mo: column label for month
    day_mo: column label for day-of-month
    yrc: column label for simulation year
    isd: column label for unit index
    id: column label for GIS ID
    name: column label for object name
    pest: column label for pesticide name
    tot_in: column label for total pesticide input mass in mg
    sol_out: column label for soluble outflow mass in mg
    sor_out: column label for sorbed outflow mass in mg
    sol_perc: column label for percolation loss mass in mg
    react: column label for reaction loss mass in mg
    metab: column label for metabolized mass in mg
    stor_ave: column label for average storage mass in mg
    stor_init: column label for initial storage mass in mg
    stor_final: column label for final storage mass in mg
type_summaries:
  aqu_pesticide_processes: One aquifer pesticide balance record holding mass terms for a single
    pesticide over a reporting period.
  aqu_pesticide_output: Container for an array of aquifer pesticide balance records for one
    reporting scope, such as one aquifer object or the basin aggregate.
  aqu_pesticide_header: Text header labels for aquifer pesticide output tables and CSV files.
---

<!-- facts:header -->

`aqu_pesticide_module` owns the shared aquifer pesticide state used for balance tracking and reporting: the `aqu_pesticide_processes` record, the per-aquifer and basin output containers for daily/monthly/yearly/average-annual summaries, and the header record used when writing pesticide output files. It is initialized by aquifer setup and pesticide output initialization routines, and then consumed by daily aquifer control, basin aquifer pesticide output, and the aquifer pesticide file writers.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-operator container; it does not read files itself. Its allocatable output arrays are created in `aqu_initial`, while `aqu_pest_output_init` seeds the per-aquifer and basin pesticide start values from current aquifer pesticide state.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:aqu_pest_output_init] | `no file input; uses current aquifer pesticide state from `cs_aqu`` | `aqu_pestbz, aqupst_d, aqupst_m, aqupst_y, aqupst_a, baqupst_d` | Initializes the aquifer pesticide output containers by zeroing basin start storage and copying each aquifer's current pesticide mass into the daily, monthly, yearly, and average-annual start values. |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `aqu_pestbz, aqupst_d, aqupst_m, aqupst_y, aqupst_a, baqupst_d` | Reads the shared aquifer pesticide output state to accumulate daily values into monthly, yearly, and average-annual summaries, then writes the aquifer-level report records when print flags are enabled. |
| [sym:aqu_read_init] | `initial.aqu` | `aqu_pestbz, aqupst_d, aqupst_m, aqupst_y, aqupst_a, baqupst_d` | The context packet resolves this as a module importer for aquifer initialization. The file reader stages aquifer initialization records that later routines use to establish the initial aquifer state; no direct use of these pesticide variables is shown in the extracted body. |
| [sym:aqu_read_init_cs] | `initial.aqu_cs` | `aqu_pestbz, aqupst_d, aqupst_m, aqupst_y, aqupst_a, baqupst_d` | Loads aquifer constituent initial conditions and converts them into starting mass state for `cs_aqu`; this module is imported so pesticide-related aquifer state can be available during initialization, but the extracted references in the packet focus on `cs_aqu` rather than these output containers. |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `aqu_pestbz, aqupst_d, aqupst_m, aqupst_y, aqupst_a, baqupst_d` | Aggregates the per-aquifer daily pesticide process records into the basin daily record and rolls those totals forward into monthly, yearly, and average-annual basin summaries before writing the basin output files. |
| [sym:header_pest] | `unit_2800, unit_9000, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807, unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815, unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823, unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007, unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015, unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839, unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855, unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `aqu_pestbz, aqupst_d, aqupst_m, aqupst_y, aqupst_a, baqupst_d` | Writes the aquifer pesticide header record so all basin aquifer pesticide output files use the column labels defined by this module. |

## Key Consumers

The module is imported by aquifer initialization, daily aquifer control, basin aquifer pesticide reporting, and the pesticide header writer. Those routines either allocate the output containers, seed their initial storage, update daily process terms, or write the final output files.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_pest_output_init] | aqu_pesticide_module | This routine seeds the shared aquifer pesticide output containers from current aquifer masses. Later pesticide reporting starts from those initialized `stor_init` values. |
| [sym:aqu_pesticide_output] | aqu_pesticide_module | This routine updates the shared daily, monthly, yearly, and average-annual pesticide summaries and writes the aquifer-level pesticide output records. |
| [sym:basin_aqu_pest_output] | aqu_pesticide_module | This routine assembles basin aquifer pesticide summaries from the per-aquifer daily records, carries them into monthly and yearly accumulators, and writes the basin pesticide output records. |
| [sym:header_pest] | aqu_pesticide_module | This routine writes `aqupest_hdr` into the aquifer pesticide text and CSV output files so the basin aquifer pesticide reports have the correct column labels. |
| [sym:aqu_read_init] | aqu_pesticide_module | This importer participates in aquifer initialization. The module provides public aquifer state definitions that are available during the setup phase, although the extracted body evidence in the packet does not show direct writes to the pesticide output arrays. |
| [sym:aqu_read_init_cs] | aqu_pesticide_module | This importer participates in aquifer constituent setup. The module makes the pesticide state types available while `cs_aqu` is being initialized from `initial.aqu_cs`. |
| [sym:aqu_1d_control] | aqu_pesticide_module | This routine writes the daily pesticide mass-balance terms into `aqupst_d`, including reaction, metabolite, storage, and outflow quantities, so the next reporting stage can print the day’s aquifer pesticide balance. |
| [sym:aqu_initial] | aqu_pesticide_module | This routine allocates the per-aquifer and basin aquifer pesticide containers so later initialization and reporting steps have storage to fill. |

## Lineage

`aqu_pesticide_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `aqu_pesticide_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `aqu_pesticide_module` has no extracted module-level documentation comment.
- The context packet resolves eight importing procedures, but direct body evidence is only shown for a subset of the pesticide output/initialization paths; importer roles for `aqu_read_init` and `aqu_read_init_cs` are based on the completed procedure overlay evidence rather than direct references to the module's pesticide variables.
- `aqupst` and `aqupstz` are declared public module variables, but no resolved procedure in the context packet references them directly.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
