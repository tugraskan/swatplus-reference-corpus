---
kind: procedure
symbol: calhard_control
title: calhard_control
status: filled
source_hash: 73d92f91c06bee14
version_label: SWAT+ 62.0.0
uses:
  aquifer_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  maximum_data_module: Provides the calibration data structures and HRU/region parameters
    that this routine reads and adjusts.
  hydrograph_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
---

<!-- facts:header -->

Re-initializes all objects and re-runs the full model for hard (manual/parameter) calibration.

## Bottom Line

`calhard_control` re-initializes every spatial object and re-runs the model once via `time_control`, labelling the run as a hard-calibration simulation.

It is a thin controller used to evaluate a hard-calibration parameter set; all the work is delegated to `re_initialize` and `time_control`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Part of the soft/hard calibration sequence (driven by `calsoft_control`/`calsoft_hyd_bfr`). It adjusts parameters to calibrate hard calibration, re-initializes objects, and re-runs the model via `time_control`. It runs only when calibration is enabled, before the production simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. call | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 2. call | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 3. return | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `no resolved imported state` |  |
| [sym:hydrograph_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cal_sim` | Before each re-run of the model. | Sets the label identifying the current calibration stage for the re-run. |

## File I/O

<!-- facts:io -->


## Lineage

`calhard_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calhard_control.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calhard_control' has no extracted documentation comment.
- Soft-calibration routine for hard calibration: compares simulated vs measured statistics, adjusts parameters, and re-runs via time_control. 3 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
