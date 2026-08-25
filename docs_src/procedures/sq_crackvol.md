---
kind: procedure
symbol: sq_crackvol
title: sq_crackvol
status: filled
source_hash: cd397d9188ab19c1
version_label: SWAT+ 62.0.0
locals:
  crlag: Daily lag factor selected for the current layer update. It starts at 0, then is set
    to `crlagdry` or `crlagwet` depending on soil wetness and whether crack volume is expanding
    or not.
  crlagdry: Lag factor used when the soil is dry and the new crack volume is larger than the
    stored crack volume. A value of `.99` makes crack opening change slowly under drying conditions.
  crlagwet: Lag factor used when the soil is wet or when crack volume is not increasing. A
    value of `0.` makes the routine move crack volume directly to the newly computed value
    instead of preserving the old one.
  j: HRU index copied from `ihru`. It selects which `soil(j)` profile this call updates.
  l: Loop counter for soil layers within the active HRU soil profile.
  volcrnew: Newly computed potential crack volume for the current soil layer from layer crack
    depth, field capacity, and current stored water. It is the target value that the lagged
    update moves toward.
uses:
  hru_module: '`hru_module` provides the active HRU index `ihru` so the routine knows which
    soil profile to process, plus `volcrmin` and `voltot`, which are the profile-level crack-volume
    states this routine resets and accumulates.'
  soil_module: '`soil_module` holds the active soil profile and its nested layer/physical
    properties. `sq_crackvol` reads `nly`, `phys(l)%crdep`, `phys(l)%fc`, `phys(l)%st`, `sw`,
    and `sumfc` to compute crack volume, and it writes back `ly(l)%volcr` for each layer.'
---

<!-- facts:header -->

Computes crack volume for each soil layer in the current HRU and sums the profile crack volume. It uses soil moisture state to lag crack opening when conditions are dry or wet.

## Bottom Line

`sq_crackvol` updates crack volume for the active HRU soil profile. For each soil layer it estimates a new potential crack volume from layer crack depth, field capacity, and stored water, then blends that value with the previous layer crack volume using a dry or wet lag factor.

The routine also accumulates `voltot`, the total crack volume for the profile, by adding each layer’s crack volume plus the minimum crack volume allowance. That total is used by the HRU water-balance/crack-flow logic that follows in the daily control flow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`sq_crackvol` runs inside `hru_control` during the daily HRU update, after aquifer inflow routing and before evapotranspiration and management operations. `hru_control` prepares the active HRU context by setting `ihru` and checking `bsn_cc%crk`; when crack flow is enabled, this routine refreshes layer crack volume so later runoff and soil-water calculations can account for bypass flow through cracks.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select active HRU and reset total | The routine copies the current HRU index from `ihru` into `j` and initializes `voltot` to zero so the crack-volume total can be rebuilt for this HRU. |
| 2. loop over soil layers | It iterates through every layer in the active soil profile using `do l = 1, soil(j)%nly`. |
| 3. initialize layer update state | For each layer it clears `volcrnew` and `crlag` before computing the layer’s new crack target. |
| 4. compute new potential crack volume | It calculates the layer’s potential crack volume from crack depth and the gap between field capacity and current stored water, normalized by field capacity. |
| 5. choose dry or wet lag | If profile water is below 90% of profile field capacity, the routine uses the dry lag only when the new crack volume is larger than the stored one; otherwise it uses the wet lag. If the profile is not that dry, it uses the wet lag directly. |
| 6. update stored layer crack volume | It blends the previous layer crack volume with the newly computed value using the selected lag factor, writing the updated result back to `soil(j)%ly(l)%volcr`. |
| 7. prevent negative crack volume | If the update produces a negative crack volume, the routine clips it to zero. |
| 8. accumulate profile total | It adds the layer crack volume plus `volcrmin` to the profile total `voltot`. |
| 9. finish | After all layers are processed, the routine returns to the caller with updated layer crack volumes and total crack volume in module state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `ihru, volcrmin, voltot` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(l)%crdep, soil(j)%phys(l)%fc, soil(j)%phys(l)%st, soil(j)%sw, soil(j)%sumfc, soil(j)%ly(l)%volcr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `voltot` | For each layer after `voltot` is reset and the updated `soil(j)%ly(l)%volcr` has been computed. | `voltot` is rebuilt as the sum of every layer’s crack volume plus `volcrmin`. This gives the HRU-level crack-volume total used by later water-balance and crack-flow behavior. |
| `soil(j)%ly(l)%volcr` | For each layer, after the potential crack volume is computed and the dry/wet lag factor is selected. | `soil(j)%ly(l)%volcr` is overwritten with a lagged blend of the previous stored crack volume and the newly computed target crack volume, then clipped at zero if needed. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.3.1 | Crack volume from drying below field capacity | $crk_{ly,i}=crk_{max,ly}*\frac{coef_{crk}*FC_{ly}-SW_{ly}}{coef_{crk}*FC_{ly}}$ | Verified against SWAT+ 62.0.0 (sq_crackvol.f90:34). volcrnew = crdep*(fc-st)/fc |
| 2:3.3.3 | Wet/no-growth crack update branch | $crk_{ly}=crk_{ly,i}$ | Verified against SWAT+ 62.0.0 (sq_crackvol.f90:45). volcr = crlag*volcr + (1-crlag)*volcrnew` lag |
| 2:3.3.5 | Total crack volume | $crk=\sum^n_{ly=1} crk_{ly}$ | Verified against SWAT+ 62.0.0 (sq_crackvol.f90:28). voltot` accumulation over layers |

## Lineage

Two resolved commits changed `sq_crackvol`. The initial add in `df07e3f` introduced the subroutine, the crack-volume calculation, the dry/wet lag branches, the nonnegative clamp, and the accumulation of `voltot`. Later, `39fabde` changed only the local variable declarations by giving `crlag`, `j`, `l`, and `volcrnew` explicit initial values; the algorithm itself remained the same.

- df07e3f introduced the full crack-volume update routine, including the layer loop, lag selection, layer-state rewrite, and total crack-volume accumulation.
- 39fabde did not change the crack-volume algorithm; it only initialized `crlag`, `j`, `l`, and `volcrnew` at declaration time.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_crackvol' has no extracted documentation comment.
