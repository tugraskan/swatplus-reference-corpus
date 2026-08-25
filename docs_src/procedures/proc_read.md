---
kind: procedure
symbol: proc_read
title: proc_read
status: filled
source_hash: 0c25a843d6362c64
version_label: SWAT+ 62.0.0
---

<!-- facts:header -->

Initializes the model's shared input databases by calling a long sequence of reader routines for climate, constituents, salts, carbon, and core landscape tables.

## Bottom Line

proc_read is a top-level setup subroutine with no arguments. It does not compute a single physical process itself; instead, it drives the model startup sequence by calling the various reader routines that populate shared climate, chemistry, landscape, and database state.

Those calls load the tables and flags needed by later SWAT+ behavior, including climate station/deposition data, pesticide/pathogen/heavy-metal/constituent inputs, salt and carbon setup, topography, fields, hydrology, shade factors, snow, soil, and LTE soil data.

## Arguments

<!-- facts:arguments -->

## Where It Fits

proc_read runs during model initialization after the shared input environment has already been set up for file access. It has no formal arguments, so the needed state must already exist in the imported modules used by the reader routines. Its results feed later model startup and simulation behavior by making the loaded databases and feature flags available to the rest of SWAT+.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare the subroutine and its external reader dependencies. | Defines proc_read with no arguments and lists the external routines it will invoke. This establishes the procedure as an initialization driver rather than a computation kernel. |
| 2. Read channel temperature and climate station/deposition inputs. | Calls the channel temperature reader, the atmospheric deposition climate reader, and the weather-station reader in sequence so climate-related shared state is available before other databases are loaded. |
| 3. Load constituent, pesticide-metabolite, and soil-plant initialization databases. | Reads the constituent database, pesticide metabolites, soil-plant initialization table, and soil-test nutrient database that support later chemical and HRU initialization. |
| 4. Load pesticide, pathogen, and heavy-metal HRU/aquifer initial-condition data. | Populates the shared initial-condition arrays for pesticides, pathogens, and heavy metals so later simulation setup can use the loaded basin chemistry state. |
| 5. Load salt simulation inputs for HRU, aquifer, irrigation, plant, climate, road-salt, uptake, urban, and fertilizer data. | Runs the salt-related readers in a fixed order to load all shared salt databases and feature flags needed for salt transport and application behavior. |
| 6. Load constituent simulation inputs for HRU, aquifer, climate, irrigation, plant, uptake, reaction, urban, and fertilizer data. | Runs the constituent-related readers so the model has the HRU, aquifer, atmospheric deposition, irrigation, plant, uptake, reaction, urban, and fertilizer constituent state required later. |
| 7. Load core landscape and hydrologic support databases. | Reads topography, field, and hydrology inputs, which provide the landscape and hydrologic definitions used by later model setup and routing. |
| 8. Load shade, snow, and soil databases, then return. | Reads shade factors, snow properties, the main soil database, and the LTE soil database before returning to the caller with all initialization reads complete. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_read.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `1c812c1` (2025-08-21) — Refactor soil-plant initialization and pesticide calculations
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_read' has no extracted documentation comment.
- No commits were resolved for this source span in the Git lineage evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
