---
kind: procedure
symbol: proc_bsn
title: proc_bsn
status: filled
source_hash: f6938b4cc2afd22a
version_label: SWAT+ 62.0.0
uses:
  time_module: proc_bsn uses the shared simulation time state to convert the configured time-step
    count into minutes per step after `time_read` loads the time settings.
  output_path_module: proc_bsn calls `open_output_file`, which uses `output_path_module` to
    resolve output filenames into full paths before opening the basin output units.
---

<!-- facts:header -->

Initial basin setup routine for SWAT+.

## Bottom Line

proc_bsn is the basin-level initialization subroutine that runs early in model setup. It loads configuration and basin input data, opens several standard output files, derives the simulation time-step length, and initializes carbon-related controls needed by later basin and output routines.

Its main job is to prepare shared module state before the rest of the basin simulation proceeds. In particular, it calls the readers for control codes, objects, time, basin parameters, print codes, CO2, and carbon settings, and it sets `time%dtm` from the configured number of time steps per day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

proc_bsn runs during basin setup, after the model has read the configuration needed to locate input and output files. It prepares shared basin state before later simulation routines depend on the loaded control codes, object tables, time settings, basin parameters, print controls, CO2 forcing, and carbon settings.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read control file | Read the model control file so configured file paths and names are available for the basin setup sequence. |
| 2. Open output listings | Open the standard basin output files and write identifying banner lines to the files-out and diagnostics listings. |
| 3. Read basin setup inputs | Load basin control codes, basin object definitions, and simulation time settings into shared state. |
| 4. Derive time step minutes | Convert the configured number of time steps per day into minutes per step and store the result in `time%dtm`. |
| 5. Read basin parameters | Read basin parameters, apply basin defaults, and load print-code settings for later output control. |
| 6. Read carbon forcing | Load CO2 forcing, basin carbon parameters, and carbon layer-count settings needed by later carbon routines. |
| 7. Return | Exit the basin setup routine after all shared state has been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%dtm, time%step` |
| [sym:output_path_module] | `get_output_filename` | `get_output_filename` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `time%dtm` | After `time_read` has populated `time%step` | Sets the simulation time-step length in minutes using `time%dtm = 1440. / time%step`. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_bsn.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 11 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_bsn.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `5a0197e` (2026-03-09) — Ensure output files respect configured output path by calling readcio_read first (#151)
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `d324ded` (2025-11-25) — potential bug fixed: Fortran runtime error End of record when writing area_calc.out
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No source-backed lineage evidence was available; lineage summary is intentionally limited to that fact.
- The routine opens and writes standard output files during basin setup; the file paths are resolved through `open_output_file` and `output_path_module`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
