---
kind: module
symbol: hydrology_data_module
title: hydrology_data_module
status: filled
source_hash: eba10cb82b29db27
version_label: SWAT+ 62.0.0
variables:
  hyd_db: Allocatable shared array of `type(hydrology_db)` records declared in `hydrology_data_module.f90:27`.
    It has no intrinsic units because it is a record container; the individual fields carry
    units and meanings from the `hydrology_db` type. It is populated by `hydrol_read` from
    `hydrology.hyd` and later searched by `hru_read` and copied by `topohyd_init`.
type_components:
  hydrology_db:
    name: none          |0          |0      |name
    lat_ttime: days          |0-120      |0      |Exponential of the lateral flow travel time
    lat_sed: g/L           |sediment concentration in lateral flow
    canmx: mm H2O        |maximum canopy storage
    esco: none          |soil evaporation compensation factor (0-1)
    epco: none          |plant water uptake compensation factor (0-1)
    erorgn: none          |organic N enrichment ratio, if left blank
    erorgp: '%             |the model will calculate for every event

      none          |organic P enrichment ratio, if left blank'
    cn3_swf: '%             |the model will calculate for every event

      none          |soil water at cn3 - 0=fc; .99=near saturation'
    biomix: none          |biological mixing efficiency.
    perco: '%             |Mixing of soil due to activity of earthworms and other soil biota.

      %             |Mixing is performed at the end of every calendar year.

      none          |0-1           |percolation coefficient - linear adjustment to daily perc'
    lat_orgn: ppm           |organic N concentration in lateral flow
    lat_orgp: ppm           |organic P concentration in lateral flow
    pet_co: none          |coefficient related to radiation used in Hargreaves equation
    latq_co: none          |0-1           |lateral soil flow coefficient - linear adjustment
      to daily lat flow
type_summaries:
  hydrology_db: hydrology.hyd
---

<!-- facts:header -->

Defines the shared hydrology database type `hydrology_db` and the allocatable array `hyd_db` that stores hydrology parameter records loaded from `hydrology.hyd`. The module is a common state container used by hydrology file reading and HRU initialization routines, which rely on it to look up named hydrology parameter sets and copy them into HRU state.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module itself only declares the hydrology record type and shared database array. `hydrol_read` allocates and fills `hyd_db` from `hydrology.hyd`, and `topohyd_init` then copies selected records into each HRU's live hydrology state.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:hydrol_read] | `hydrology.hyd` | `hyd_db` | Allocates the shared hydrology database and reads each `hydrology_db` record from `hydrology.hyd` into `hyd_db`. |

## Key Consumers

The module is used by hydrology database loading and by HRU setup routines that resolve hydrology names to database records and copy the selected parameters into each HRU.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:hru_read] | hydrology_data_module | Uses `hyd_db` to match each HRU's hydrology name to a numeric database index, so the HRU can store `hru_db(i)%dbs%hyd` for later initialization and process routines. |
| [sym:hydrol_read] | hydrology_data_module | Allocates and fills the shared `hyd_db` array from `hydrology.hyd`, making the hydrology parameter records available to later setup and calculation code. |
| [sym:topohyd_init] | hydrology_data_module | Reads the selected hydrology record from `hyd_db` and copies its parameters into each HRU's live hydrology state, so later HRU process code uses HRU-specific values. |

## Lineage

`hydrology_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hydrology_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `hydrology_data_module` has no extracted module-level documentation comment.
- No imported modules are declared in `hydrology_data_module`; it is a declaration container for the hydrology record type and shared array.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
