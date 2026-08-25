---
kind: procedure
symbol: proc_cal
title: proc_cal
status: filled
source_hash: e3cb6c25b0da1677
version_label: SWAT+ 62.0.0
uses:
  hydrograph_module: Imported for shared hydrologic/model state used by the calibration setup
    routines that `proc_cal` invokes.
  calibration_data_module: Provides the calibration mode flags that control whether `cal_allo_init`
    runs at the end of the setup sequence.
---

<!-- facts:header -->

Initializes calibration setup by reading calibration inputs, region definitions, and object-specific calibration tables.

## Bottom Line

`proc_cal` is the calibration bootstrap routine. It reads the calibration parameter and change files, loads plant, landscape, aquifer, channel, reservoir, and recall calibration definitions, and then conditionally initializes calibration allocation state when soft or hard calibration is enabled.

It matters because later calibration and simulation routines depend on the shared tables and region memberships populated here. Without this setup, the model would not know which objects, regions, or parameters are eligible for calibration.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_cal` runs during calibration initialization, before calibration-sensitive model work begins. It prepares the shared calibration tables and region memberships that later plant, landscape, aquifer, channel, reservoir, and recall calibration routines use, and it finishes by initializing calibration allocations when either soft or hard calibration is enabled.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read calibration inputs | Read the calibration parameter and change files that seed the calibration database. |
| 2. Load plant calibration data | Load plant calibration regions and plant calibration parameters, then apply calibration conditions once the plant setup is available. |
| 3. Read soft calibration codes | Read the soft-calibration flags that control which calibration modes are active. |
| 4. Load landscape calibration data | Load landscape soft-calibration regions and landscape calibration parameter definitions. |
| 5. Load object calibration elements | Load aquifer, channel, reservoir, and recall element memberships needed for object-specific calibration setup. |
| 6. Load channel calibration parameters | Load channel order and channel parameter calibration data after channel memberships are known. |
| 7. Initialize calibration allocation | If either soft or hard calibration is enabled, initialize calibration allocation and baseline state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `hydrograph_module state` |  |
| [sym:calibration_data_module] | `cal_soft, cal_hard` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cal_allo_init` | cal_soft == "y" .or. cal_hard == "y" | Triggers calibration-time allocation and baseline-state initialization only when calibration is enabled. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_cal.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_cal.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_cal' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
