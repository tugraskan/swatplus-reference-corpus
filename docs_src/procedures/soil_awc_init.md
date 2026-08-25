---
kind: procedure
symbol: soil_awc_init
title: soil_awc_init
status: filled
source_hash: a9117f28910982ea
version_label: SWAT+ 62.0.0
args:
  isol: Selects which soil profile in `soil(isol)` is recalculated. The caller passes the
    HRU/soil index whose layer depth or density has just changed, and this routine rewrites
    that profile’s derived soil-water properties in place.
locals:
  ly: Loop counter over soil layers in the selected profile; initialized to 0 before iterating
    through the layers and reused in both passes.
  nly: Holds the number of layers in `soil(isol)` so the routine can iterate over the profile
    consistently.
  sumpor: Accumulates total pore volume across all layers, in mm of pore depth, so the profile-average
    porosity can be computed at the end.
  pormm: Stores the pore-volume contribution of the current layer, derived from porosity times
    layer thickness.
  drpor: Temporary drainable-porosity value for the current layer, computed as porosity minus
    the upper-water-content threshold.
  depth_prev: Tracks the bottom depth of the previous layer so current layer thickness can
    be computed as a difference from cumulative depth.
uses:
  soil_module: '`soil_module` is the core data store this routine updates. Its `soil` profiles
    provide the layer counts and physical properties being recalculated, and the results written
    back here become the soil-water inputs used by later hydrologic calculations.'
  basin_module: '`basin_module` is imported by the procedure, but no specific state or type
    from it is referenced in the extracted source lines. It still matters as a compile-time
    dependency for shared basin-level context, even though this routine does not read a named
    basin variable in the visible code.'
  time_module: '`time_module` is also imported, but the extracted source does not show any
    direct use of time variables or types. It matters here only as an available shared module
    dependency, not as an explicitly referenced runtime input in the visible routine body.'
---

<!-- facts:header -->

Initializes a soil profile’s water-capacity-related properties from available water content and layer geometry. It clamps unrealistic layer values, recomputes derived storage metrics, and updates profile-level water-table and average-property summaries used later by the model.

## Bottom Line

`soil_awc_init` recalculates layer-by-layer soil water storage parameters for one soil profile identified by `isol`. It uses the profile’s existing layer depth, bulk density, clay content, porosity, crack potential, and available water capacity to derive wilting point, field capacity, saturation-related storage, hydraulic coefficients, and crack-volume terms.

The routine matters because later SWAT+ soil-water and routing behavior depends on these derived values being internally consistent. It also updates profile totals such as `sumfc`, `sumul`, `sumwp`, `sw`, `swpwt`, `wat_tbl`, `avpor`, and `avbd`, so downstream routines see a normalized soil state after edits to layer depth or density.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after a caller such as `cal_parm_select` changes a soil layer property like depth or bulk density. The caller immediately invokes `soil_awc_init` to rebuild dependent soil-water parameters, and then `curno` uses the updated soil profile so curve-number and related runoff behavior stay aligned with the revised soil state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load layer count and start first pass | Read the selected profile’s layer count from `soil(isol)%nly` and loop over every layer to normalize layer-specific water parameters before computing profile totals. |
| 2. bound available water capacity | Force each layer’s available water capacity into a usable range: raise values near zero to 0.005 and cap excessively large values at 0.8. |
| 3. compute wilting point and field capacity start | Derive layer wilting point from clay and bulk density, then set upper-water content and porosity from the current physical properties. |
| 4. keep upper-water content below porosity | If the upper-water content would exceed porosity, reduce it to stay below porosity and recompute wilting point; if that still leaves wilting point nonpositive, fall back to a fixed 75/25 split of porosity. |
| 5. compute drainable porosity and layer water-table factor | Calculate drainable porosity as porosity minus upper-water content, then convert that value to the layer’s variable water-table factor and store it in `soil(isol)%ly(ly)%vwt`. |
| 6. reset profile totals | Initialize cumulative depth and profile storage accumulators so the second pass can build total porosity and water-storage summaries from scratch. |
| 7. start second pass and compute layer thickness | Loop over the layers again, compute each layer thickness from the current depth minus the previous depth, and add that layer’s pore-volume contribution to the running porosity total. |
| 8. compute saturation and field-capacity storages | Derive each layer’s upper-limit storage and field-capacity storage, then accumulate them into profile totals `sumul` and `sumfc`. |
| 9. compute standing storage and hydraulic coefficient | Set the layer’s standing-water storage from field capacity and the profile field-capacity fraction, then compute the hydraulic coefficient and enforce a minimum value of 1. |
| 10. compute wilting-point storage, crack depth, and crack volume | Convert wilting point to millimeters, add it to the profile total, and derive crack-depth potential and layer crack volume from layer depth and field-capacity storage. |
| 11. store current depth for next layer | Save the current layer depth as `depth_prev` so the next loop iteration can compute the next layer’s thickness correctly. |
| 12. finalize profile water state and water table | Copy total standing soil water into `swpwt` and, if the profile field-capacity fraction is greater than 1, compute a water-table depth estimate; otherwise set the water-table depth to zero. |
| 13. compute profile-average porosity and bulk density | Use the accumulated pore volume and total profile depth to calculate average porosity, then convert that porosity to average bulk density. |
| 14. return to caller | Exit after all layer and profile summary values have been rewritten in `soil(isol)`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `soil` | `soil(isol)%nly, soil(isol)%phys(ly)%awc, soil(isol)%phys(ly)%wp, soil(isol)%phys(ly)%clay, soil(isol)%phys(ly)%bd, soil(isol)%phys(ly)%up, soil(isol)%phys(ly)%por, soil(isol)%ly(ly)%vwt, soil(isol)%sumfc, soil(isol)%sumul, soil(isol)%sw, soil(isol)%sumwp, soil(isol)%phys(ly)%thick, soil(isol)%phys(ly)%d, soil(isol)%phys(ly)%ul, soil(isol)%phys(ly)%fc, soil(isol)%phys(ly)%st, soil(isol)%ffc, soil(isol)%phys(ly)%hk, soil(isol)%phys(ly)%k, soil(isol)%phys(ly)%wpmm, soil(isol)%phys(ly)%crdep, soil(isol)%crk, soil(isol)%ly(ly)%volcr, soil(isol)%swpwt, soil(isol)%wat_tbl, soil(isol)%det_lag, soil(isol)%phys(nly)%d, soil(isol)%avpor, soil(isol)%avbd` |
| [sym:basin_module] | `basin_module` |  |
| [sym:time_module] | `time_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(isol)%phys(ly)%wp` | When a layer’s calculated wilting-point water content is nonpositive, it is forced to 0.005 after being computed from clay and bulk density. | `soil(isol)%phys(ly)%wp` is normalized to a small positive lower bound so later storage calculations do not use an invalid or zero wilting point. |
| `soil(isol)%phys(ly)%up` | When the layer’s `up` value would be greater than or equal to porosity, it is reduced to `porosity - 0.05`, and if that still leaves `wp` nonpositive the routine resets `up` to `porosity * 0.75` and `wp` to `porosity * 0.25`. | `soil(isol)%phys(ly)%up` is adjusted to stay physically below saturation so the implied field-capacity state remains feasible for the layer. |
| `soil(isol)%phys(ly)%por` | Porosity is recomputed for every layer from bulk density as `1. - bd / 2.65`. | `soil(isol)%phys(ly)%por` becomes the layer’s total pore fraction, which is then used to derive drainable pore space and profile-average porosity. |
| `soil(isol)%ly(ly)%vwt` | For every layer, after drainable porosity is computed from porosity minus upper-water content. | `soil(isol)%ly(ly)%vwt` stores the layer’s variable water-table factor derived from its drainable porosity. |
| `soil(isol)%sumfc` | During the second pass through the layers, after each layer’s field-capacity storage is computed. | `soil(isol)%sumfc` accumulates the profile’s total field-capacity water storage across all layers. |
| `soil(isol)%sumul` | During the second pass through the layers, after each layer’s saturation-related storage is computed. | `soil(isol)%sumul` accumulates the profile’s total saturation-side storage across all layers. |
| `soil(isol)%sw` | During the second pass through the layers, after each layer’s standing storage is computed. | `soil(isol)%sw` becomes the profile’s total standing soil water storage summed across layers. |
| `soil(isol)%sumwp` | During the second pass through the layers, after each layer’s wilting-point storage in millimeters is computed. | `soil(isol)%sumwp` accumulates the profile’s total wilting-point water storage across layers. |
| `soil(isol)%phys(ly)%thick` | During the second pass, each layer’s depth bottom minus the previous layer bottom is computed. | `soil(isol)%phys(ly)%thick` is reset to the actual thickness of the current soil layer so all later storage formulas use layer thickness rather than cumulative depth. |
| `soil(isol)%phys(ly)%ul` | During the second pass, after layer porosity and wilting point are known. | `soil(isol)%phys(ly)%ul` is recomputed as the layer’s saturation-side water storage above wilting point. |
| `soil(isol)%phys(ly)%fc` | During the second pass, after the layer’s upper-water and wilting-point contents are known. | `soil(isol)%phys(ly)%fc` is recomputed as the layer’s field-capacity storage in millimeters. |
| `soil(isol)%phys(ly)%st` | During the second pass, after field-capacity storage is available and the soil profile field-capacity fraction `ffc` is applied. | `soil(isol)%phys(ly)%st` becomes the layer’s standing soil-water storage used in the profile water sum. |
| `soil(isol)%phys(ly)%hk` | During the second pass, after `ul` and `fc` are computed for a layer. | `soil(isol)%phys(ly)%hk` is recalculated as a hydraulic-response coefficient and limited to a minimum of 1 so it does not drop below the model’s floor. |
| `soil(isol)%phys(ly)%wpmm` | During the second pass, after wilting-point content and layer thickness are known. | `soil(isol)%phys(ly)%wpmm` stores the layer wilting-point water content expressed in millimeters. |
| `soil(isol)%phys(ly)%crdep` | During the second pass, after the layer’s depth and thickness are known. | `soil(isol)%phys(ly)%crdep` is recalculated as crack-depth potential, which later feeds layer crack-volume calculations. |
| `soil(isol)%ly(ly)%volcr` | During the second pass, after crack-depth potential and field-capacity storage are known. | `soil(isol)%ly(ly)%volcr` stores the crack volume for the layer based on crack-depth potential and the gap between field capacity and standing storage. |
| `soil(isol)%swpwt` | After the second pass completes the layer storage totals. | `soil(isol)%swpwt` is set equal to the profile’s standing soil water so the profile keeps a water-table-related water total. |
| `soil(isol)%wat_tbl` | If the profile field-capacity fraction `ffc` is greater than 1. | `soil(isol)%wat_tbl` is estimated from detachment lag, field-capacity storage, and total profile depth; otherwise it is set to zero. |
| `soil(isol)%avpor` | After the layer porosity contributions have been accumulated across the profile. | `soil(isol)%avpor` becomes the profile-average porosity computed from total pore volume divided by total depth. |
| `soil(isol)%avbd` | Immediately after average porosity is computed. | `soil(isol)%avbd` becomes the profile-average bulk density implied by the average porosity. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `soil_awc_init`. The file was added in `df07e3f`, which introduced the routine with its soil-parameter recalculation logic. `94b6dec` brought the file into the newer source tree without changing the visible logic in the extracted span. `39fabde` made a small behavioral-safe cleanup by initializing the local variables `ly`, `nly`, `sumpor`, `pormm`, `drpor`, and `depth_prev` to zero/default values at declaration time.

- df07e3f introduced the full `soil_awc_init` subroutine, including the two-pass recalculation of layer moisture limits, storage totals, crack-volume terms, water-table estimate, and average profile properties.
- 94b6dec preserved the procedure while importing it into the later source tree; the visible diff in the extracted span does not show functional changes to the routine body.
- 39fabde initialized the local counters and accumulators at declaration, reducing dependence on prior values and making the routine safer if future edits change control flow.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'soil_awc_init' has no extracted documentation comment.
