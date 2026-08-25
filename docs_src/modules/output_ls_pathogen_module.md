---
kind: module
symbol: output_ls_pathogen_module
title: output_ls_pathogen_module
status: filled
source_hash: 9c95472f42f15b13
version_label: SWAT+ 62.0.0
variables:
  pathbz: '`pathbz` is a module-level `pathogen_balance` scalar initialized by default to
    zero-valued fields. It is used as the zero template in `hru_pathogen_output` when clearing
    average-annual balances after output. No input file populates it directly.'
  hpath_bal: '`hpath_bal` is an allocatable array of `object_pathogen_balance` records for
    HRU-level pathogen balances. `hru_output_allo` allocates `hpath_bal(ihru)%path(cs_db%num_paths)`,
    `pathogen_init` seeds `hpath_bal(ihru)%path(ipath)%plant`, and `path_ls_process`, `path_ls_runoff`,
    `path_ls_swrouting`, and `hru_pathogen_output` read and update the per-pathogen fields.
    It stores current HRU pathogen state in kg/ha terms for reporting and transport bookkeeping.'
  hpathb_m: '`hpathb_m` is the allocatable monthly HRU pathogen accumulator array. `hru_output_allo`
    allocates it, `hru_pathogen_output` accumulates current balances into `hpathb_m(j)%path(ipath)`
    and writes monthly output from it, and it is reset or divided by the month length inside
    that routine. Units remain kg/ha for each balance component.'
  hpathb_y: '`hpathb_y` is the allocatable yearly HRU pathogen accumulator array. `hru_output_allo`
    allocates it, `hru_pathogen_output` adds monthly balances into `hpathb_y(j)%path(ipath)`
    and writes yearly output from it, and downstream average-annual output uses its accumulated
    values. Units remain kg/ha.'
  hpathb_a: '`hpathb_a` is the allocatable average-annual HRU pathogen accumulator array.
    `hru_output_allo` allocates it, `hru_pathogen_output` accumulates annual values into `hpathb_a(j)%path(ipath)`
    and writes average-annual output from it, then clears it back to `pathbz` after output.
    Units remain kg/ha.'
  rupathb_d: '`rupathb_d` is an allocatable `object_pathogen_balance` array for runoff-pathogen
    daily balances. It is declared in this module and allocated elsewhere for runoff reporting,
    but the provided source span does not show a reader or writer using it directly.'
  rupathb_m: '`rupathb_m` is an allocatable `object_pathogen_balance` array for runoff-pathogen
    monthly balances. It is module-owned storage for runoff reporting; the provided source
    span does not show a direct consumer in these excerpts.'
  rupathb_y: '`rupathb_y` is an allocatable `object_pathogen_balance` array for runoff-pathogen
    yearly balances. It is module-owned storage for runoff reporting; the provided source
    span does not show a direct consumer in these excerpts.'
  rupathb_a: '`rupathb_a` is an allocatable `object_pathogen_balance` array for runoff-pathogen
    average-annual balances. It is module-owned storage for runoff reporting; the provided
    source span does not show a direct consumer in these excerpts.'
  bpathb_d: '`bpathb_d` is a scalar `object_pathogen_balance` for basin daily pathogen accounting.
    The source span only shows its declaration; no direct use is visible in the provided excerpts.'
  bpathb_m: '`bpathb_m` is a scalar `object_pathogen_balance` for basin monthly pathogen accounting.
    The source span only shows its declaration; no direct use is visible in the provided excerpts.'
  bpathb_y: '`bpathb_y` is a scalar `object_pathogen_balance` for basin yearly pathogen accounting.
    The source span only shows its declaration; no direct use is visible in the provided excerpts.'
  bpathb_a: '`bpathb_a` is a scalar `object_pathogen_balance` for basin average-annual pathogen
    accounting. The source span only shows its declaration; no direct use is visible in the
    provided excerpts.'
  pathb_hdr: '`pathb_hdr` is the module-level `output_pathbal_header` record containing the
    column labels written at the top of HRU pathogen output files. `header_path` writes it
    to the text and CSV output units for daily, monthly, yearly, and average-annual pathogen
    reports.'
type_components:
  pathogen_balance:
    plant: 'kg/ha: pathogen mass on plant foliage; the source also shows commented-out original
      name metadata for the field.'
    soil: 'kg/ha: pathogen on the soil/enrichment state carried by the balance record.'
    sed: 'kg/ha: pathogen loading from the HRU that is attached to sediment.'
    surq: 'kg/ha: pathogen lost in surface runoff on the current day in the HRU.'
    latq: 'kg/ha: pathogen in lateral flow in the HRU for the day; declared in the type definition
      but not updated in the shown procedures.'
    perc1: 'kg/ha: pathogen leached past the first soil layer.'
    apply_sol: 'kg/ha: pathogen applied to soil.'
    apply_plt: 'kg/ha: pathogen applied to plant.'
    regro: 'kg/ha: pathogen regrowth.'
    die_off: 'kg/ha: pathogen die-off.'
    wash: 'kg/ha: pathogen washed off from plant to soil.'
  object_pathogen_balance:
    path: Allocatable array of `pathogen_balance` records, one per pathogen type in the owning
      object.
  output_pathbal_header:
    day: Column label for the daily time-step field (`jday`).
    mo: Column label for month (`mon`).
    day_mo: Column label for day-of-month (`day`).
    yrc: Column label for year (`yr`).
    isd: Column label for the HRU or unit identifier (`unit`).
    id: Column label for the GIS identifier (`gis_id`).
    name: Column label for the object name.
    plant: Column label for plant-associated pathogen balance (`plant_kg/h`).
    soil: Column label for soil-associated pathogen balance (`soil_kg/h`).
    sed: Column label for sediment-associated pathogen balance (`sed_kg/h`).
    surq: Column label for surface-runoff pathogen balance (`surq_kg/h`).
    latq: Column label for lateral-flow pathogen balance (`latq_kg/h`).
    perc: Column label for percolation/leaching pathogen balance (`perc_kg/h`).
    apply: Column label for pathogen application balance (`apply_kg/h`).
    decay: Column label for pathogen decay balance (`decay_kg/h`).
type_summaries:
  pathogen_balance: One `pathogen_balance` record stores the current pathogen mass balance
    terms for a single pathogen path, including plant, soil, runoff, sediment, leaching, application,
    regrowth, die-off, and wash-off components in kg/ha.
  object_pathogen_balance: One `object_pathogen_balance` record groups a dynamically allocated
    array of `pathogen_balance` records for one HRU, runoff object, or basin accumulator container.
  output_pathbal_header: One `output_pathbal_header` record stores the fixed text labels written
    as the header row for pathogen balance output files.
---

<!-- facts:header -->

`output_ls_pathogen_module` owns the pathogen balance state used by SWAT+ HRU pathogen initialization, transport, and reporting. It defines the per-pathogen balance record, the grouped HRU/basin accumulator containers for daily, monthly, yearly, and average-annual output, and the header record written to HRU pathogen output files. The module is initialized by `hru_output_allo`, `pathogen_init`, and the pathogen output routines that reset or accumulate these balances during the simulation.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-operator container with no contained startup routine. Its arrays are allocated by `hru_output_allo`, its plant state is seeded by `pathogen_init`, and the reporting routines populate, accumulate, and clear the balance records during simulation.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:header_path] | `unit_2790, unit_9000, unit_2794, unit_2791, unit_2795, unit_2792, unit_2796, unit_2793, unit_2797` | `pathb_hdr` | Writes `pathb_hdr` to the daily, monthly, yearly, and average-annual HRU pathogen output headers, along with the basin/program banner and file-name registry entry. |
| [sym:hru_pathogen_output] | `unit_2790, unit_2794, unit_2791, unit_2795, unit_2792, unit_2796, unit_2793, unit_2797` | `pathbz, hpath_bal, hpathb_m, hpathb_y, hpathb_a` | Accumulates current HRU pathogen balances into monthly, yearly, and average-annual arrays, writes daily/monthly/yearly/average-annual pathogen output records, and clears the average-annual balance back to `pathbz` after output. |
| [sym:pathogen_init] | `soil-plant initialization database via `sol_plt_ini` and `path_soil_ini`` | `hpath_bal` | Seeds the HRU pathogen balance state by storing the initial plant-associated pathogen amount in `hpath_bal(ihru)%path(ipath)%plant` during HRU initialization. |

## Key Consumers

The module is used by four groups of routines: file-header setup, HRU output allocation, pathogen initialization, and the pathogen transport/reporting routines that update and write balances.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:header_path] | output_ls_pathogen_module | Uses `pathb_hdr` to write the pathogen balance header row into each enabled HRU pathogen output file after the basin/program banner line. |
| [sym:hru_output_allo] | output_ls_pathogen_module | Allocates `hpath_bal`, `hpathb_m`, `hpathb_y`, and `hpathb_a` so later HRU pathogen reporting routines can store daily, monthly, yearly, and average-annual balances by HRU and pathogen. |
| [sym:hru_pathogen_output] | output_ls_pathogen_module | Reads and updates the HRU pathogen balance arrays, accumulating the current day into monthly and yearly totals and emitting the configured pathogen output records at each reporting interval. |
| [sym:path_ls_process] | output_ls_pathogen_module | Stores wash-off and net die-off in `hpath_bal(j)%path(ipath)%wash` and `hpath_bal(j)%path(ipath)%die_off` so later pathogen balance reporting can describe foliage-to-soil transfer and combined daily losses. |
| [sym:path_ls_runoff] | output_ls_pathogen_module | Stores the daily soluble runoff export in `surq` and sediment-attached export in `sed` for each pathogen so later transport and balance routines can report HRU pathogen losses. |
| [sym:path_ls_swrouting] | output_ls_pathogen_module | Stores percolation loss in `hpath_bal(j)%path(ipath)%perc1` so downstream pathogen balance output reflects leaching below the first soil layer. |
| [sym:pathogen_init] | output_ls_pathogen_module | Initializes the module's HRU pathogen balance state by assigning the starting plant pathogen load for each HRU and pathogen type. |

## Lineage

`output_ls_pathogen_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `output_ls_pathogen_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was present in the source span.
- The source shows `latq` in the `pathogen_balance` type, but the extracted procedure evidence does not show a writer for that field in the provided snippets.
- The source span declares runoff and basin pathogen balance containers (`rupathb_*`, `bpathb_*`), but the provided excerpts do not show direct readers or writers for those arrays.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
