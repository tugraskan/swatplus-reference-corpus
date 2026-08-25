---
kind: procedure
symbol: surface
title: surface
status: filled
source_hash: 36091e704a602ff5
version_label: SWAT+ 62.0.0
locals:
  j: Loop-free index variable set to the active HRU number from `ihru`, so the routine can
    read and update `hru(j)`, `surfq(j)`, and `irrig(j)` for the current HRU.
  ulu: Temporary copy of the current HRU’s urban land-use code from `hru(j)%luse%urb_lu`.
    It is initialized but not used further in the extracted code, so it appears to be a local
    holdover for land-use-dependent logic that is not present here.
  hruirrday: Initialized to zero as a daily irrigation-water accumulator for the active HRU,
    but it is not referenced again in the extracted source.
  irmmdt: Initialized to zero as a local integer flag or counter related to irrigation management,
    but it is not used further in the extracted source.
uses:
  basin_module: The basin control flags determine whether crack-flow adjustment is enabled.
    `bsn_cc%crk` gates the call to `sq_crackflow`, so basin-wide configuration changes whether
    daily runoff is reduced for flow into soil cracks.
  time_module: This module holds the active HRU index, the effective precipitation used to
    decide whether runoff is computed, the surface runoff depth, and the peak runoff rate.
    `surface` reads and updates those shared HRU states directly, so its hydrology and erosion
    branches depend on `hru_module` state.
  hydrograph_module: '`hydrograph_module` provides the irrigation transfer array. `surface`
    adds `irrig(j)%runoff` into HRU surface runoff before clearing it, so irrigation-generated
    runoff is merged into the day’s runoff total here.'
  hru_module: '`hru_module` supplies the active HRU’s land-use code through `hru(j)%luse%urb_lu`.
    That value is captured locally, showing that surface processing can depend on the current
    HRU’s land-use class even though the extracted code does not branch on it.'
  soil_module: The soil module matters because the erosion routines called from `surface`
    use soil properties to estimate sediment response. In the extracted contracts, `ero_ysed`
    reads soil rock content, so soil state affects the sediment yield produced downstream
    of runoff computation.
  urban_data_module: The urban data module is relevant because the active HRU’s land-use code
    is pulled from the HRU land-use structure and can be interpreted as an urban land-use
    identifier. That supports surface-runoff and sediment behavior for urban HRUs, even though
    no separate urban-data array is directly referenced in the extracted lines.
  output_landscape_module: The output landscape module matters because the erosion subroutines
    called here populate shared erosion diagnostics for the active HRU. Those stored outputs
    are what later reporting and landscape-scale summaries use to track runoff-driven sediment
    behavior.
---

<!-- facts:header -->

Models surface hydrology for the active HRU at the current time step. It computes runoff, adjusts for crack flow and irrigation runoff, then drives sediment-erosion calculations when flow is present.

## Bottom Line

This routine is the HRU-level surface hydrology and erosion driver. It updates daily surface runoff for the active HRU, optionally reduces that runoff for crack flow, adds irrigation runoff, and derives the day’s runoff reaching the main channel.

If runoff is present, it then computes peak flow and runs the erosion-related routines that depend on runoff depth and peak discharge. Those results feed the HRU’s daily runoff and sediment outputs used later in routing and reporting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `hru_control` after management operations and before wetland short-circuit logic. `hru_control` sets the active HRU context and then calls `surface` for non-wetland HRUs so that runoff, peak flow, crack-flow adjustment, and sediment yield are computed for the day; later routing and output behavior depend on `qday`, `qp_cms`, `surfq(j)`, and the erosion states produced here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize active HRU context | Copy the current HRU index from `ihru` into `j`, capture the HRU’s urban land-use code in `ulu`, and zero the local irrigation-day helper variables. |
| 2. update curve number | Call `sq_dailycn` to compute the current HRU’s daily curve number from its present hydrologic state. |
| 3. compute runoff when precipitation is effective | If `precip_eff > 0.1`, call `sq_volq` to compute daily surface runoff depth for the HRU. |
| 4. reduce runoff for crack flow when enabled | If runoff exists and basin crack-flow routing is enabled, call `sq_crackflow` to remove runoff lost into soil cracks. |
| 5. add irrigation runoff | Add `irrig(j)%runoff` into `surfq(j)` and then clear the irrigation runoff store for the HRU. |
| 6. set daily runoff reaching channel | Assign the adjusted HRU surface runoff depth to `qday`, representing the runoff reaching the main channel during the day. |
| 7. compute peak runoff if runoff is present | When `qday` is above the tiny-flow threshold, call `ero_pkq` to compute the peak runoff rate `qp_cms`. |
| 8. compute erosion factors and splash/overland erosion | If daily runoff and peak flow are both present, call `ero_eiusle` and `ero_ovrsed` to compute rainfall erosivity and sediment yield from rainfall splash and overland flow. |
| 9. compute cover factor and sediment yield | If surface runoff and peak flow are both present, call `ero_cfactor` and `ero_ysed` to update the cover-management factor and final sediment yield. |
| 10. prevent negative daily runoff | Clip `qday` to zero if it became negative. |
| 11. return to caller | Exit `surface` after the HRU runoff and erosion states have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%crk` |
| [sym:time_module] | `hru, surfq, ihru, qp_cms, precip_eff, qday` | `hru(j)%luse%urb_lu; surfq(j); ihru; qp_cms; precip_eff; qday` |
| [sym:hydrograph_module] | `irrig` | `irrig(j)%runoff` |
| [sym:hru_module] | `hru, surfq, ihru, qp_cms, precip_eff, qday` | `hru(j)%luse%urb_lu` |
| [sym:soil_module] | `soil state used by erosion routines` | `soil(j)%phys(1)%rock` |
| [sym:urban_data_module] | `urban land-use parameters used via the current HRU land-use record` | `hru(j)%luse%urb_lu` |
| [sym:output_landscape_module] | `erosion output records` | `ero_output(j)%ero_d%c; ero_output(j)%ero_d%rsd_m; ero_output(j)%ero_d%grcov_frac; ero_output(j)%ero_d%rsd_covfact; ero_output(j)%ero_d%bio_covfact; ero_output(j)%ero_d%sedyld; ero_output(j)%ero_d%precip; ero_output(j)%ero_d%surfq; ero_output(j)%ero_d%peak; ero_output(j)%ero_ave` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `surfq(j)` | After runoff is computed and possibly reduced for crack flow, then irrigation runoff is added: `surfq(j) = surfq(j) + irrig(j)%runoff`. | `surfq(j)` becomes the HRU’s adjusted daily surface runoff depth. It is changed here to include irrigation runoff after any crack-flow reduction, so later runoff and erosion logic works with the final surface-flow amount. |
| `irrig(j)%runoff` | Always after `surfq(j)` is updated: `irrig(j)%runoff = 0.` | `irrig(j)%runoff` is cleared once its runoff contribution has been transferred into `surfq(j)`, preventing the same irrigation runoff from being counted again later in the day. |
| `qday` | After runoff processing and before return: `qday = surfq(j)` and `if (qday < 0.) qday = 0.` | `qday` stores the daily runoff delivered to the main channel for the active HRU, then is clipped to zero if numerical or adjustment effects made it negative. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.3.8 | Infiltration after crack-flow runoff adjustment | $w_{inf}=R_{day}-Q_{surf}$ | Runoff is first computed, then reduced by sq_crackflow; effective infiltration is therefore rainfall minus the adjusted runoff, but it is not stored as a separate winf variable. |

## Lineage

`surface.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `surface.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `56f2463` (2024-12-12) — Source Code updates 12/12 - Some .vs changes got accidently commited.
- `dab22e1` (2024-10-08) — Remove unused format labels in Fortran source files
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'surface' has no extracted documentation comment.
- algorithm_steps revised: condensed the raw line-by-line control flow into 11 model steps while preserving the source-line citations.
- time_module, soil_module, urban_data_module, and output_landscape_module had no resolved candidate references in the packet; their roles are inferred only from the routine context and extracted callee contracts where available.
- ulu, hruirrday, and irmmdt are initialized but not used later in the extracted source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
