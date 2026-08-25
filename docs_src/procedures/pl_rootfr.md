---
kind: procedure
symbol: pl_rootfr
title: pl_rootfr
status: filled
source_hash: 35cf157cb3cc12d1
version_label: SWAT+ 62.0.0
args:
  j: '`j` selects the HRU/plant-community entry to update; the routine uses it to read `pcom(j)`
    and `soil(j)` and to write the resulting layer root fractions back into that same community.'
locals:
  cum_rd: Tracks the cumulative root depth used for the current layer. It is capped at the
    plant rooting depth so each layer’s fraction is calculated only over the depth interval
    that lies within roots.
  cum_d: Declared but not used in the current source; it appears to be a leftover accumulator
    for cumulative soil depth from older versions of the routine.
  cum_rf: Accumulates the running sum of computed root fractions across layers so the routine
    can detect and correct any overshoot above 1.0 before final normalization.
  x1: Stores the lower normalized depth bound for the current layer before evaluating the
    root distribution integral.
  x2: Stores the upper normalized depth bound for the current layer before evaluating the
    root distribution integral.
  k: Records the deepest layer reached by the first accumulation loop so the second loop knows
    where to stop renormalizing.
  ly: Loop index over soil layers. It is reused in both the accumulation and normalization
    passes.
  a: Constant coefficient in the normalized root-density equation.
  b: Constant exponent coefficient in the normalized root-density equation.
  c: Constant offset term in the normalized root-density equation.
  d: Normalization constant for the root-distribution integral; it scales the layer fractions
    so the total integrates to one.
  rtfr: Local scratch value for a layer root fraction in older versions of the routine; in
    the current source it is reset but not otherwise used in the final assignment path.
  xx1: Holds the exponential argument for the lower depth bound after clipping it to prevent
    overflow.
  xx2: Holds the exponential argument for the upper depth bound after clipping it to prevent
    overflow.
  xx: Stores the previous cumulative root-fraction total so the routine can back-correct the
    current layer when the running sum exceeds 1.0.
uses:
  hru_module: The `ipl` index from `hru_module` identifies which plant in the current community
    is being processed. `pl_rootfr` updates the root-fraction array for that plant, so the
    plant index must already be set by the caller.
  soil_module: The soil profile supplies the layer count and layer geometry used to slice
    rooting depth into per-layer fractions. `soil(j)%nly`, `soil(j)%phys(ly)%d`, and `soil(j)%phys(ly)%thick`
    determine how much of each layer lies inside the rooting zone.
  plant_module: The plant-community arrays hold the rooting depth and the destination array
    for layer fractions. `root_dep` defines the target depth, and `rtfr` is the per-layer
    output that later routines use to allocate root-derived material.
---

<!-- facts:header -->

Distributes a plant's root fraction across soil layers based on its rooting depth and the soil profile. The routine stores normalized layer fractions in `pcom(j)%plg(ipl)%rtfr` for later residue allocation and root-growth tracking.

## Bottom Line

`pl_rootfr` computes how much of a plant’s roots are assigned to each soil layer in the current HRU. It uses the plant’s rooting depth together with the layer depths and thicknesses to build a layer-by-layer root-fraction profile, then normalizes that profile so the fractions sum to 1.0.

If the plant has essentially no rooting depth, the routine assigns all roots to the first layer and returns immediately. Otherwise, later management and growth routines use the stored `rtfr` values to distribute dead root mass into soil layers after harvest, kill operations, and plant initialization.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a plant’s rooting profile needs to be refreshed, such as during plant initialization, growth updates, harvest/tuber removal, or kill operations. The caller must already have set the current HRU/plant indices and the plant’s rooting depth, and later residue-placement logic depends on the resulting `rtfr` array to distribute dead roots into soil layers.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize/reset | Clear the layer index and zero the full `rtfr` array so the routine starts from a clean slate before computing a new root distribution. |
| 2. short-circuit for shallow roots | If the plant rooting depth is effectively zero, assign all root fraction to the first layer and return immediately instead of doing the depth integration. |
| 3. set distribution constants | Load the fixed coefficients and normalization factor used in the Dwyer-style normalized root-density equation. |
| 4. initialize accumulators | Reset the layer tracker, cumulative root-fraction total, and local scratch fraction before entering the layer loop. |
| 5. walk soil layers | For each soil layer, compute the portion of rooting depth that belongs in that layer by clipping the cumulative depth to the plant root depth or the layer depth, whichever is smaller. |
| 6. build normalized bounds | Convert the layer bounds into normalized depth coordinates and clamp the exponential arguments to avoid overflow when evaluating the exponential terms. |
| 7. compute layer root fraction | Evaluate the layer’s root fraction from the integrated root-density expression and add it to the running total. |
| 8. cap overshoot | If the running sum exceeds 1.0, trim the current layer so the total cannot rise above a full root distribution. |
| 9. remember deepest used layer | Record the last layer that received roots and stop the accumulation loop once the rooting depth has been fully covered. |
| 10. renormalize assigned layers | Divide each populated layer fraction by the final cumulative total so the stored fractions sum to exactly 1.0, then stop at the deepest affected layer. |
| 11. return | Exit after the per-layer root-fraction array has been updated for the selected HRU and plant. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `ipl` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(ly)%d, soil(j)%phys(ly)%thick` |
| [sym:plant_module] | `pcom` | `pcom(j)%plg(ipl)%rtfr, pcom(j)%plg(ipl)%root_dep, pcom(j)%plg(ipl)%rtfr(1), pcom(j)%plg(ipl)%rtfr(ly)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plg(ipl)%rtfr` | When the plant has a nonzero rooting depth and the layer loop reaches each soil layer. | `pcom(j)%plg(ipl)%rtfr` is rebuilt as the normalized distribution of root fraction across all relevant soil layers for the selected plant community entry. |
| `pcom(j)%plg(ipl)%rtfr(1)` | If `pcom(j)%plg(ipl)%root_dep < 1.e-6`. | `pcom(j)%plg(ipl)%rtfr(1)` is forced to 1.0 so a plant with effectively no rooting depth is treated as having all roots in the top layer. |
| `pcom(j)%plg(ipl)%rtfr(ly)` | During the layer loop when the computed cumulative root fraction for a layer is available and the routine is still within the rooting zone. | `pcom(j)%plg(ipl)%rtfr(ly)` receives the computed share for that layer, then is renormalized so the full profile sums to one. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows five behavior-changing commits. The earliest available source imported `pl_rootfr` with a zero-argument form and later commits progressively changed it to use `j`, refactored the HRU and plant indexing, reset layer fractions before recomputation, and corrected the zero-root-depth branch and uninitialized-layer use. The final visible change in the resolved history was b992868, which added `ly = 0`, zeroed `pcom(j)%plg(ipl)%rtfr`, and changed the short-circuit assignment from an uninitialized `ly` index to layer 1.

- 94b6dec introduced the modern layer-distribution routine structure, including per-layer root-fraction computation and normalization over the soil profile.
- 39fabde added default zero initialization for the accumulators and local root-fraction variable so the routine starts from a clean state.
- febcf0c changed the procedure to operate on the current HRU/plant selection and added growing-plant handling, including the root-depth short circuit.
- 3e18acf changed the interface to `pl_rootfr(j)` and switched the routine to use the caller-supplied HRU index rather than the older `ihru`/`jj` pattern.
- b992868 reset the plant root-fraction array at entry and fixed the zero-root-depth branch so it writes to layer 1 instead of using `ly` before assignment.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_rootfr' has no extracted documentation comment.
- algorithm_steps revised: condensed the original 12-step draft into 11 source-backed steps to match the visible control flow and to keep step descriptions aligned with the line-numbered source.
- Source is somewhat inconsistent with the older lineage history: the current file uses `j` and `ipl` directly, while older diffs show prior `ihru`/`jj`/`ipl_grow` usage.
