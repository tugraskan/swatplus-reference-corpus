---
kind: module
symbol: output_ls_salt_module
title: output_ls_salt_module
status: filled
source_hash: 619bf5492fa00d83
version_label: SWAT+ 62.0.0
variables:
  saltbz: Shared salt-balance accumulator of type `salt_balance`, initialized to zero via
    component defaults in `salt_balance` and used as the module-level working record for salt
    output calculations.
  hsaltb_d: Allocatable array of `object_salt_balance` for HRU salt balance output at daily
    resolution. The contained `salt` arrays are populated by downstream output routines; this
    module only declares the storage.
  hsaltb_m: Allocatable array of `object_salt_balance` for HRU salt balance output at monthly
    resolution. It is module-owned shared storage and is not initialized here beyond allocation
    state.
  hsaltb_y: Allocatable array of `object_salt_balance` for HRU salt balance output at yearly
    resolution. It stores per-object `salt` records for later reporting.
  hsaltb_a: Allocatable array of `object_salt_balance` for HRU salt balance output at annual
    resolution. It holds accumulated `salt` records for reporting.
  rusaltb_d: Allocatable array of `object_salt_balance` for routing-unit salt balance output
    at daily resolution. The module declares the container; downstream routines populate its
    `salt` components.
  rusaltb_m: Allocatable array of `object_salt_balance` for routing-unit salt balance output
    at monthly resolution.
  rusaltb_y: Allocatable array of `object_salt_balance` for routing-unit salt balance output
    at yearly resolution.
  rusaltb_a: Allocatable array of `object_salt_balance` for routing-unit salt balance output
    at annual resolution.
  bsaltb_d: Single `object_salt_balance` record for basin salt balance output at daily resolution.
    It is module-owned shared state for basin reporting.
  bsaltb_m: Single `object_salt_balance` record for basin salt balance output at monthly resolution.
  bsaltb_y: Single `object_salt_balance` record for basin salt balance output at yearly resolution.
  bsaltb_a: Single `object_salt_balance` record for basin salt balance output at annual resolution.
  saltb_hdr: Shared `output_saltbal_header` record holding the column labels used in salt
    balance output tables.
---

<!-- facts:header -->

Declares the salt-balance data structures and shared module state used to accumulate and format salt output for SWAT+ landscape output. It owns the per-balance record, grouped object arrays for daily/monthly/yearly/annual aggregation, and the header labels used when writing salt balance output tables.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container: it defines shared types, default-initialized scalar state, and allocatable output containers. No startup routine appears in this source file; the arrays are expected to be allocated and filled by other SWAT+ output code.

## Key Consumers

No importing procedures were resolved for this module in the provided context, so there is no source-backed list of consumers to summarize.

## Lineage

`output_ls_salt_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `output_ls_salt_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No procedures were resolved as importers of this module in the provided context.
- No completed procedure overlays with module-specific evidence were available for later-effect attribution.
- Module `output_ls_salt_module` has no extracted module-level documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
