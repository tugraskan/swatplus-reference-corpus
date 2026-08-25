---
kind: procedure
symbol: calsoft_hyd_bfr
title: calsoft_hyd_bfr
status: filled
source_hash: f0ca3dbb777a41a4
version_label: SWAT+ 62.0.0
locals:
  iter_all: Outer calibration-iteration count (1).
  iterall: Outer calibration-iteration counter.
uses:
  soil_module: Provides the calibration parameter limits (`ls_prms`) and data structures used
    by the component routines.
  plant_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  hydrograph_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  ru_module: Provides the calibration parameter limits (`ls_prms`) and data structures used
    by the component routines.
  aquifer_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  hru_lte_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  sd_channel_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  basin_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  maximum_data_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  calibration_data_module: Provides the calibration parameter limits (`ls_prms`) and data
    structures used by the component routines.
  conditional_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  reservoir_module: Provides the calibration parameter limits (`ls_prms`) and data structures
    used by the component routines.
  organic_mineral_mass_module: Provides the calibration parameter limits (`ls_prms`) and data
    structures used by the component routines.
  time_module: Provides the calibration parameter limits (`ls_prms`) and data structures used
    by the component routines.
---

<!-- facts:header -->

Controller for the before-flow-regime hydrology soft-calibration. It calls the per-component calibration routines (PET, ET, surface runoff, lateral flow, percolation) in sequence, managing the PET parameter range across a two-stage adjustment.

## Bottom Line

`calsoft_hyd_bfr` runs the before-flow-regime water-balance calibration by calling `calsoft_hyd_bfr_pet`, `_et`, `_surq`, `_latq`, and `_perc` in order. It first narrows the PET parameter range (`ls_prms(4)`) to half for an initial pet pass, then restores the full range for a second pass.

Each called routine adjusts its parameter and re-runs the model; this controller just sequences them and sets the allowed adjustment ranges.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `calsoft_control` when before-flow-regime hydrology calibration is enabled. It orchestrates the five component calibrations; the actual parameter adjustment and model re-runs happen in the called routines.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 2. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 3. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 4. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 5. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 6. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 7. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 8. call | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |
| 9. return | Sets the PET parameter range, then calls the per-component before-flow-regime calibration routines in sequence. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `no resolved imported state` |  |
| [sym:plant_module] | `no resolved imported state` |  |
| [sym:hydrograph_module] | `no resolved imported state` |  |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `no resolved imported state` |  |
| [sym:calibration_data_module] | `ls_prms` | `ls_prms(4)%neg, ls_prms(4)%pos, ls_prms(4)%lo, ls_prms(4)%up` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |
| [sym:organic_mineral_mass_module] | `no resolved imported state` |  |
| [sym:time_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ls_prms(4)%neg` | During the two-stage PET calibration (narrowed to half, then restored to full range). | Adjusts the lower change limit of the PET parameter (`ls_prms(4)%neg`): halved for the first pass, then restored for the second. |
| `ls_prms(4)%pos` | During the two-stage PET calibration (narrowed to half, then restored to full range). | Adjusts the upper change limit of the PET parameter (`ls_prms(4)%pos`): halved for the first pass, then restored for the second. |
| `ls_prms(4)%lo` | During the two-stage PET calibration (narrowed to half, then restored to full range). | Adjusts the absolute lower bound of the PET parameter (`ls_prms(4)%lo`): halved for the first pass, then restored for the second. |
| `ls_prms(4)%up` | During the two-stage PET calibration (narrowed to half, then restored to full range). | Adjusts the absolute upper bound of the PET parameter (`ls_prms(4)%up`): halved for the first pass, then restored for the second. |

## File I/O

<!-- facts:io -->


## Lineage

`calsoft_hyd_bfr.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calsoft_hyd_bfr.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_hyd_bfr' has no extracted documentation comment.
- Sequencing controller for before-flow-regime hydrology calibration; state changes are PET parameter-range adjustments. 13 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
