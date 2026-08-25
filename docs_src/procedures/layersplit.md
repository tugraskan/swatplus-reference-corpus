---
kind: procedure
symbol: layersplit
title: layersplit
status: filled
source_hash: b1f795459650cfc0
version_label: SWAT+ 62.0.0
args:
  dep_new: '`dep_new` is the depth, in the same units as `soil(ihru)%phys(:)%d`, where the
    routine should create a new layer boundary. The subroutine scans for the first layer deeper
    than this value and splits that layer at `dep_new`.'
locals:
  nly: Holds the original number of soil layers in `soil(ihru)%nly` so the routine can copy
    the existing profile into temporary arrays before rebuilding it.
  nly1: Stores the expanded layer count after the split; it is the new size used when reallocating
    `soil(ihru)%ly` and `soil(ihru)%phys`.
  lyn: Loop index used while copying the original layers back into the rebuilt arrays, first
    for the layers above the split and then for the layers below it.
  ly: Main loop index over the original layer positions. It is also used to identify the first
    layer whose bottom depth exceeds `dep_new`.
uses:
  hru_module: '`ihru` selects which HRU''s soil profile is being modified. `layersplit` operates
    on `soil(ihru)`, so the current HRU index determines exactly which profile is split.'
  soil_module: '`soil_module` supplies the soil-profile arrays and the layer-structure types
    that are being copied, deallocated, reallocated, and rewritten. The routine depends on
    `soil(ihru)%nly` to know the original layer count and on `soil(ihru)%ly` and `soil(ihru)%phys`
    to preserve and update the layer geometry and physical depths.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is imported by the routine,
    but no symbols from it are resolved in the extracted source span. It may matter because
    the split changes soil-layer structure that mass-accounting routines later use, but this
    source excerpt does not show any direct use of that module''s state.'
  constituent_mass_module: '`constituent_mass_module` is also imported without any resolved
    symbol use in the extracted source span. It matters only insofar as layer splitting can
    affect downstream constituent-mass bookkeeping, but no direct access to that module''s
    state is visible here.'
---

<!-- facts:header -->

Splits a soil profile at a specified depth by inserting a new layer boundary. It copies the old layer arrays aside, reallocates the profile, and preserves the original layer data above and below the split.

## Bottom Line

`layersplit` is a soil-profile editing routine used during initialization. Given a target depth `dep_new`, it finds the first existing layer whose bottom depth is deeper than that target and then inserts a new layer boundary there by rebuilding the HRU's `soil(ihru)%ly` and `soil(ihru)%phys` arrays.

This matters because later carbon, nutrient, and water calculations depend on the revised soil layering. After the split, the routine updates layer depths and thicknesses so the model can treat the new boundary as a real soil layer interface.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`layersplit` runs during `soils_init` after separator-depth logic has chosen one or more split depths and before the code allocates downstream soil, carbon, and nutrient arrays. Its output is the revised layer structure that later initialization and simulation code relies on for layer-by-layer state arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Cache the current soil layer count and copy the current layer descriptions and physical properties into temporary arrays. | Reads `soil(ihru)%nly` into `nly`, allocates `layer1` and `phys1`, and copies each original layer into those temporary arrays so the profile can be rebuilt without losing information. |
| 2. Remove the original soil arrays from the active HRU profile. | Deallocates `soil(ihru)%phys` and `soil(ihru)%ly` to make room for a newly sized profile. |
| 3. Scan layers from the second layer downward until the target split depth falls inside an existing layer. | Loops over `ly = 2, nly` and checks whether the stored bottom depth `phys1(ly)%d` is deeper than `dep_new`. |
| 4. Increase the HRU layer count and allocate new soil arrays sized for the inserted boundary. | Adds one to `soil(ihru)%nly`, saves the new count in `nly1`, and allocates `soil(ihru)%ly(nly1)` and `soil(ihru)%phys(nly1)`. |
| 5. Copy the layers above and including the split point into the new arrays, then overwrite the split layer depth and thickness. | Copies layers `1:ly` from the temporary arrays into the rebuilt profile; when the loop reaches the split layer, it sets that layer's bottom depth to `dep_new` and recomputes its thickness from the previous layer bottom depth. |
| 6. Copy the remaining original layers into positions shifted down by one to fill the lower part of the rebuilt profile. | Copies layers from `ly` through `nly` into `lyn+1` so the lower part of the profile moves down one slot; when copying the split layer's lower counterpart, it sets the new thickness to the original bottom depth minus `dep_new`. |
| 7. Exit after the first matching split depth and clean up the temporary copies. | Leaves the scan once the split is performed, deallocates `layer1` and `phys1`, and returns to the caller with the updated soil profile in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil, layer1, phys1` | `soil(ihru)%nly, soil(ihru)%phys, soil(ihru)%ly, phys1(ly)%d, soil(ihru)%ly(nly1), soil(ihru)%phys(nly1), soil(ihru)%ly(lyn), soil(ihru)%phys(lyn), soil(ihru)%phys(lyn)%d, soil(ihru)%phys(lyn)%thick, soil(ihru)%phys(lyn-1)%d, soil(ihru)%ly(lyn+1), soil(ihru)%phys(lyn+1), soil(ihru)%phys(lyn+1)%thick, soil(ihru)%phys(lyn+1)%d` |
| [sym:organic_mineral_mass_module] | `layer1, phys1` | `layer1(ly), layer1(nly), layer1(lyn); phys1(ly), phys1(nly), phys1(lyn), phys1(ly)%d` |
| [sym:constituent_mass_module] | `layer1, phys1` | `layer1(ly), layer1(nly), layer1(lyn); phys1(ly), phys1(nly), phys1(lyn), phys1(ly)%d` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `layer1(ly)` | When `phys1(ly)%d > dep_new` for the first layer below the target depth. | `layer1(ly)` itself is not modified; it serves as the preserved source copy that gets written back into `soil(ihru)%ly` before the split layer is reconstructed. |
| `phys1(ly)` | When `phys1(ly)%d > dep_new` and the routine begins rebuilding the profile. | `phys1(ly)` is not changed in place; it is the preserved physical-property source that gets copied into `soil(ihru)%phys` and used to derive the new split-layer thickness and depth. |
| `soil(ihru)%nly` | Immediately before reallocating the soil profile for the split. | The layer count increases by one so the new soil profile can contain both sides of the inserted boundary. |
| `soil(ihru)%ly(lyn)` | During reconstruction of the upper half of the split profile, especially when `lyn == ly`. | The copied layer entry at the split position is rewritten to represent the new upper portion of the split layer. |
| `soil(ihru)%phys(lyn)` | During reconstruction of the profile after the arrays have been reallocated. | The physical-property entry at the split position is copied from the original profile, then the split layer's depth and thickness are adjusted to reflect the new boundary. |
| `soil(ihru)%phys(lyn)%d` | When `lyn == ly` in the first copy loop. | The depth to bottom of the split layer is forced to `dep_new`, replacing the original deeper depth from `phys1(ly)%d`. |
| `soil(ihru)%phys(lyn)%thick` | When `lyn == ly` in the first copy loop. | The split layer thickness is recalculated as the distance from the previous layer bottom depth to `dep_new`. |
| `soil(ihru)%ly(lyn+1)` | When the second copy loop shifts the lower profile and `lyn == ly`. | The lower copy of the split layer is written one slot later in the new arrays so the original layer sequence is preserved below the inserted boundary. |
| `soil(ihru)%phys(lyn+1)` | During the second copy loop for the lower part of the profile. | The shifted physical-property record is copied into the new position and then adjusted so the lower portion of the split is represented separately from the upper portion. |
| `soil(ihru)%phys(lyn+1)%thick` | When `lyn == ly` in the second copy loop. | The thickness of the lower split portion is set to the original layer depth minus `dep_new`, so the two new pieces together match the original layer extent. |

## File I/O

<!-- facts:io -->


## Lineage

`layersplit` was introduced in commit 94b6dec as a new subroutine that copies the current soil profile, deallocates the active arrays, and rebuilds them with a split at `dep_new`. Commit 39fabde initialized the local loop counters `nly`, `nly1`, `lyn`, and `ly` to zero and kept the routine logic the same. Commit 2ee1889 only changed the final statement to `end subroutine layersplit` without altering behavior.

- 94b6dec added the full split-and-rebuild logic for `soil(ihru)%ly` and `soil(ihru)%phys`, including depth and thickness adjustment at the new boundary.
- 39fabde changed only variable initialization and formatting, which does not change the layer-splitting algorithm.
- 2ee1889 changed the subroutine terminator text only; behavior is unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'layersplit' has no extracted documentation comment.
