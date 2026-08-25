---
kind: module
symbol: tiles_data_module
title: tiles_data_module
status: filled
source_hash: 42ee2b944ae54bd0
version_label: SWAT+ 62.0.0
variables:
  sdr: '`sdr` is an allocatable array of `subsurface_drainage` records declared in this module.
    It has no local initialization in the source file; other routines populate and query it
    by name, and `actions` reads its `name` field when applying structural install/uninstall
    operations.'
type_components:
  subsurface_drainage:
    name: Character identifier for a drainage record; initialized to `"null"` and used as
      the lookup key in management actions.
    depth: '|mm            |depth of drain tube from the soil surface'
    time: '|hrs           |time to drain soil to field capacity'
    lag: '|hours         |drain tile lag time'
    radius: '|mm            |effective radius of drains'
    dist: '|m             |distance between two drain tubes or tiles'
    drain_co: '|mm/day        |drainage coefficient'
    pumpcap: '|mm/hr         |pump capacity (default pump capacity = 1.042mm/hr or 25mm/day)'
    latksat: '|none          |multiplication factor to determine conk(j1,j) from sol_k(j1,j)
      for HRU'
type_summaries:
  subsurface_drainage: One `subsurface_drainage` record defines the named parameters for a
    tile drain or related drainage structure.
---

<!-- facts:header -->

Declares the `subsurface_drainage` derived type and the allocatable `sdr` array that stores tile-drain and related structural drainage definitions used when management actions look up named drainage records.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only. It defines the drainage record type and the allocatable `sdr` state, but no contained procedures or startup routines appear in the source span to populate them.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `sdr` | Reads `sdr(istr)%name` to find matching drainage definitions during tile, septic, filter strip, grass waterway, and user BMP install actions, then writes the selected names to the land-use change log. |

## Key Consumers

The only extracted importer is `actions`, which uses this module as a lookup table for structural land-management actions that need named drainage records.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:actions] | tiles_data_module | During structural install and related management cases, `actions` matches file pointers against `sdr%name`, passes the selected drainage record into `structure_set_parms`, and logs the old/new names to unit 3612. |

## Lineage

`tiles_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `815ec79` (2026-01-07, "water allocation updates"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `tiles_data_module.f90` are listed.

- `815ec79` (2026-01-07) — water allocation updates
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `tiles_data_module` has no extracted module-level documentation comment.
- No completed procedure overlays with module-specific evidence were available; `used_by[].effect` is based on source snippets from `actions.f90`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
