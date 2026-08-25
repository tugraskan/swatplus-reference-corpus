---
kind: procedure
symbol: zeroini
title: zeroini
status: filled
source_hash: 16c83686332cbc86
version_label: SWAT+ 62.0.0
locals:
  snocov2: Local working copy of the second snow-cover shape parameter; set to zero for completeness
    but not propagated outside this subroutine.
uses:
  hru_module: These scalars hold default snow-cover and soil-crack initial conditions for
    every HRU and must be reset before the model begins computations.
  soil_module: The module is imported without an ONLY list, but no symbols from it are used
    in zeroini.
  time_module: Imported for completeness of common initialization routines; no variables are
    referenced here.
---

<!-- facts:header -->

Zeros key snow-cover and soil-crack initialization scalars before the simulation begins.

## Bottom Line

zeroini is an infrastructure helper that makes sure several single-value initialization variables start at a known value (zero).  It is invoked once from allocate_parms during global model set-up, before any hydrologic or routing calculations require the values.

By explicitly writing zeros into snocov1 (snow cover shape parameter 1) and volcrmin (minimum allowable soil-crack volume) this routine prevents stale values from earlier runs or un-initialized memory from influencing the current simulation.  The local variable snocov2 is declared and cleared for symmetry with the first snow-cover parameter, but because it is local it has no effect on the module state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

allocate_parms performs a sequence of zero* routines to clear global state, with zeroini handling the single-value snow and crack parameters.  All later snow evolution and soil crack routines assume these scalars start at zero, so this routine must run once before any daily simulation loop begins.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Zero snow-cover parameter 1 | Set module variable snocov1 to 0.0 so that the snow cover equation starts from a pristine state. |
| 2. Zero local snow-cover parameter 2 | Reset local variable snocov2 to 0.0 (does not affect module state). |
| 3. Zero minimum crack volume | Set module variable volcrmin to 0.0 to ensure no residual crack storage at start-up. |
| 4. Return to caller | Exit the subroutine; initialization of these scalars is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `snocov1, volcrmin` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `snocov1` | Always when zeroini is called during model initialization | Reset to 0.0 so snow cover calculation starts correctly. |
| `volcrmin` | Always when zeroini is called during model initialization | Reset to 0.0 so soil-crack volume starts at minimum. |

## File I/O

<!-- facts:io -->


## Lineage

Three commits touched this file: df07e3f ("init all") which introduced the routine, 94b6dec which synced source from Bitbucket, and 39fabde which performed automated variable initialization cleanup.  None of the commit messages indicate functional logic changes to zeroini—only housekeeping and source migration.

- {'commit': '39fabde', 'effect': 'Confirmed that variable initialization is explicitly set to zero, matching the purpose of this routine.'}
- {'commit': '94b6dec', 'effect': 'Source migrated from Bitbucket repository; no functional change stated.'}
- {'commit': 'df07e3f', 'effect': 'Initial addition of zeroini to the code base.'}

## Review Notes

- algorithm_steps revised: expanded single return into four explicit assignment steps to reflect actual executable statements and aid graph readability.
- warning: missing_doc: Procedure 'zeroini' has no developer comment block beyond a brief PURPOSE header.
