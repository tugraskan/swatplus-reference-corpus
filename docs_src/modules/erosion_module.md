---
kind: module
symbol: erosion_module
title: erosion_module
status: filled
source_hash: bbddb188ed5e14c0
version_label: SWAT+ 62.0.0
variables:
  ero_output: Allocated as `dimension(:)` by HRU in `proc_hru`; each element is an `erosion_output`
    record that stores event counts, the latest erosion-event diagnostics, and the event-average
    diagnostics used by `ero_cfactor` and `ero_ysed`.
  ero_hdr: Static `erosion_output_header` record initialized in the module with the column
    labels written to `erosion.out` by `proc_hru`. It is not computed at runtime.
  ero_hdr_units: Static `erosion_header_units` record initialized in the module with the units
    row written to `erosion.out` by `proc_hru`. It is not computed at runtime.
  ero_1: Module-level scratch variable of type `erosion_output_variables` for overloaded `+`
    and `/` operators.
  ero_2: Module-level scratch variable of type `erosion_output_variables` for overloaded `+`
    and `/` operators.
  ero_3: Module-level scratch variable of type `erosion_output_variables` for overloaded `+`
    and `/` operators.
type_components:
  erosion_output_variables:
    sedyld: t/ha       |sediment yield
    precip: mm         |precipitation
    surfq: mm         |surface runoff
    peak: m3/s       |peak rate
    k: '|usle k factor'
    s: m/m        |slope
    l: m          |slope length
    ls: '|usle ls factor'
    p: '|usle p factor'
    c: '|usle c factor'
    rsd_m: kg/ha      |surface residue mass
    grcov_frac: frac       |ground cover fraction
    rsd_covfact: '|residue cover factor'
    bio_covfact: '|growing biomass factor'
  erosion_output:
    n_events: number of erosion events
    ero_d: ersion variables at each erosion event
    ero_ave: erosion variables averaged by number of events
  erosion_output_header:
    hru: Column label for the HRU identifier printed in `erosion.out`.
    neve: Column label for the number of erosion events.
    sedyld: Column label for sediment yield.
    precip: Column label for precipitation.
    peak: Column label for peak rate.
    k: Column label for the USLE K factor.
    s: Column label for slope.
    l: Column label for slope length.
    ls: Column label for the USLE LS factor.
    p: Column label for the USLE P factor.
    c: Column label for the USLE C factor.
    rsd_m: Column label for surface residue mass.
    grcov_frac: Column label for ground cover fraction.
    rsd_covfact: Column label for residue cover factor.
    bio_covfact: Column label for growing biomass factor.
  erosion_header_units:
    hru: Blank units field for the HRU identifier column.
    neve: Blank units field for the event-count column.
    sedyld: Units field `t/ha` for sediment yield.
    precip: Units field `mm` for precipitation.
    peak: Units field `m3/s` for peak rate.
    k: Blank units field for the USLE K factor.
    s: Units field `m/m` for slope.
    l: Units field `m` for slope length.
    ls: Blank units field for the USLE LS factor.
    p: Blank units field for the USLE P factor.
    c: Blank units field for the USLE C factor.
    rsd_m: Units field `kg/ha` for surface residue mass.
    grcov_frac: Units field `frac` for ground cover fraction.
    rsd_covfact: Blank units field for residue cover factor.
    bio_covfact: Blank units field for growing biomass factor.
type_summaries:
  erosion_output_variables: One erosion-event or erosion-average diagnostic record holding
    sediment, runoff, cover-factor, and site-attribute values for a single HRU event.
  erosion_output: Per-HRU erosion state containing the number of erosion events, the latest
    event record, and the accumulated event-average record.
  erosion_output_header: Static column-name record for the erosion output file header written
    by `proc_hru`.
  erosion_header_units: Static units row for the erosion output file header written by `proc_hru`.
---

<!-- facts:header -->

Defines the erosion diagnostics state shared by HRU erosion routines. It owns the per-HRU `ero_output` array, the erosion output header/unit labels, and helper records used to add and average `erosion_output_variables` values; `proc_hru` allocates and writes the headers, while `ero_cfactor` and `ero_ysed` populate the per-HRU/event diagnostics.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-helper container. Its header records and operator scratch variables are initialized in the module declarations, and `proc_hru` allocates `ero_output` before erosion routines begin filling it during the run.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:proc_hru] | `unit_4001, unit_4000, unit_9000` | `ero_output, ero_hdr, ero_hdr_units, ero_1, ero_2, ero_3` | Allocates the per-HRU erosion array and writes the erosion header and units records to `erosion.out` during HRU setup. |

## Key Consumers

The module is used by HRU setup and the erosion-cover/sediment routines. `proc_hru` prepares the output file and allocates the per-HRU storage, `ero_cfactor` fills cover-factor diagnostics, and `ero_ysed` fills daily sediment-yield diagnostics and event averages.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:proc_hru] | erosion_module | Allocates `ero_output` and writes `ero_hdr` and `ero_hdr_units` to `erosion.out` during HRU initialization. |
| [sym:ero_cfactor] | erosion_module | Stores the current HRU's USLE cover-factor diagnostics in `ero_output(j)%ero_d`, including the final `c` factor and its residue and biomass components. |
| [sym:ero_ysed] | erosion_module | Stores the daily sediment-yield diagnostics in `ero_output(j)%ero_d`, increments the erosion-event summary, and accumulates `ero_ave`. |

## Lineage

`erosion_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `15ff92f` (2026-04-08, "Refactor erosion and pesticide modules to incorporate biomass and ground cover f…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `erosion_module.f90` are listed.

- `15ff92f` (2026-04-08) — Refactor erosion and pesticide modules to incorporate biomass and ground cover factors in calculations
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `erosion_module` has no extracted module-level documentation comment.
- The source comment for `erosion_output%ero_d` is truncated in the captured file (`ersion variables at each erosion event`).
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
