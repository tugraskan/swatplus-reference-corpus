---
kind: procedure
symbol: proc_aqu
title: proc_aqu
status: filled
source_hash: b5a54c8526e1434e
version_label: SWAT+ 62.0.0
uses:
  hydrograph_module: The subroutine has no formal arguments, so any data it needs or initializes
    must come from module-scoped state made available through `hydrograph_module`. That shared
    state is what the called aquifer routines use to read database records and populate aquifer
    initial conditions.
---

<!-- facts:header -->

Initializes aquifer setup by chaining the aquifer database read, aquifer state initialization, and initial-condition reads.

## Bottom Line

`proc_aqu` is a small driver subroutine for aquifer setup. It has no arguments of its own; instead, it relies on `hydrograph_module`-shared state and calls four aquifer routines in sequence to load aquifer properties, initialize aquifer storage, and read the initial aquifer and constituent condition files.

This routine matters because it performs the one-time aquifer bootstrap before simulation time stepping begins. The later aquifer and constituent balance routines depend on the state created by `aqu_read`, `aqu_initial`, `aqu_read_init`, and `aqu_read_init_cs`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during aquifer initialization, before the model starts using aquifer water and constituent states. `aqu_read` prepares the aquifer database that the later setup routines depend on, and the results feed the aquifer and constituent mass-balance behavior used throughout the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. call | Read aquifer property records into shared aquifer database storage so the model knows which aquifer entries and parameters are available. |
| 2. call | Initialize aquifer working arrays and balance storage using the aquifer database that was just loaded. |
| 3. call | Read and stage aquifer initial-condition data for later initialization of each aquifer object. |
| 4. call | Read and apply aquifer initial constituent setup, including starting pesticide, pathogen, salt, and constituent states. |
| 5. return | Finish the aquifer setup sequence and return to the caller with aquifer initialization complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `hydrograph_module shared state and types` | `module use only; no specific imported variables or derived types were resolved in the extracted source` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_aqu.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_aqu.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_aqu' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
