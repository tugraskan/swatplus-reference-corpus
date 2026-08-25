---
kind: procedure
symbol: soils_test_adjust
title: soils_test_adjust
status: filled
source_hash: 111594304af3aa48
version_label: SWAT+ 62.0.0
args:
  isol: '`isol` selects which soil profile entry in `sol` and `soildb` is being adjusted.
    The routine only touches the profile whose soil series name matches the current soil test
    record.'
  mlyr: '`mlyr` limits how many model soil layers are scanned when the adjusted layer values
    are recomputed. It controls the depth range over which the routine writes updated `sol(isol)%phys(i)`
    values.'
locals:
  soil_layer_thickness: Stores the thickness of the current model layer in millimeters so
    the routine can convert summed millimeter-level values into layer averages.
  prev_depth: Tracks the previous layer bottom depth while walking through soil test intervals
    and model layers so the routine knows the current depth window. It starts at 0 and is
    reset when the first matching test record is found.
  sum_bd: Accumulates bulk-density values across millimeter positions within the current model
    layer so the final layer bulk density can be computed as an average.
  sum_cbn: Accumulates carbon values across millimeter positions within the current model
    layer so the final layer carbon value can be computed as an average.
  sum_sand: Accumulates sand values across millimeter positions within the current model layer
    so the final layer sand fraction can be computed as an average.
  sum_silt: Accumulates silt values across millimeter positions within the current model layer
    so the final layer silt fraction can be computed as an average.
  sum_clay: Accumulates clay values across millimeter positions within the current model layer
    so the final layer clay fraction can be computed as an average.
  tot_soil_depth: Holds the deepest soil depth used to size and fill the temporary millimeter-level
    soil database. It starts at 0 and is set from the last soil-layer depth in `soildb(isol)`
    before the overlay is built.
  test: Indexes through the available soil test records in `sol_test` while matching them
    to the current soil profile.
  i: Indexes individual millimeter positions and model layers when copying, overlaying, and
    averaging soil values.
  j: Indexes source soil database layers while building the temporary millimeter-level copy
    from `soildb`, and also indexes the temporary array during value propagation.
  first_lr: Flags the first matching soil test record so the routine can initialize `prev_depth`
    and allocate/populate the temporary database only once per profile.
  sol_mm_db: Holds the temporary millimeter-by-millimeter soil database used to apply soil-test
    overrides before depth-weighted averaging back to model layers.
uses:
  soil_module: '`soil_module` supplies the active soil-test list, the current HRU soil profile,
    and the layer property components that this routine reads and rewrites. Without `sol_test`,
    `sol`, and `nmbr_soil_test_layers`, there would be no matching test records to apply and
    no profile state to update.'
  soil_data_module: '`soil_data_module` provides the source soil database (`soildb`) that
    the routine expands into millimeter resolution before averaging. Its layer depths and
    default properties define the baseline profile that the soil tests modify.'
---

<!-- facts:header -->

Adjusts soil profile layer properties using matching soil test records, then rebuilds layer values by depth-weighted averaging. It is called during soil initialization so later soil physics calculations use the adjusted profile.

## Bottom Line

`soils_test_adjust` searches the loaded soil test list for records whose soil series name matches the current HRU soil profile. When it finds a match, it overlays any provided test values onto a temporary millimeter-by-millimeter soil layer database and then recomputes each model layer's bulk density, carbon, sand, silt, and clay by averaging those adjusted millimeter values over the layer thickness.

The routine matters because it turns sparse test depths into layer values the rest of the soil model can use. It runs after `soils_init` has loaded `sol_test`, `sol`, and `soildb`, and before later soil-physics setup (`soil_phys_init`) uses the corrected profile state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `soils_init` after the soil test records have been loaded and `sol_test` is allocated for the current soil series. It prepares adjusted layer properties for the current `isol`, and the later `soil_phys_init` call depends on those updated values when it initializes soil physical behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over soil test records | Initialize the first-layer flag, then scan every loaded soil test record and process only records whose soil series name matches the current soil profile. |
| 2. Allocate and fill a temporary millimeter profile | On the first matching record, determine total soil depth from `soildb`, allocate `sol_mm_db(1)%ly`, and copy each source layer's properties into millimeter positions up to its depth. |
| 3. Overlay soil test values into the temporary profile | For each millimeter between the previous test depth and the current test depth, replace any provided test fields (`bd`, `cbn`, `sand`, `silt`, `clay`) in `sol_mm_db(1)%ly`. Unspecified values remain from the source profile. |
| 4. Recompute layer averages from millimeter values | Walk the model layers in `sol`, sum millimeter values over each layer thickness, and write the averaged `bd`, `cbn`, `sand`, `silt`, and `clay` back to `sol(isol)%phys(i)`. |
| 5. Release temporary storage | If the temporary soil database was allocated, deallocate its layer array and then the container to clean up before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `sol_test, sol, nmbr_soil_test_layers` | `sol_test(test)%snam, sol(isol)%s%snam, sol_test(test-1)%d, sol_test(test)%d, sol_test(test)%bd, sol_test(test)%cbn, sol_test(test)%sand, sol_test(test)%silt, sol_test(test)%clay, sol(isol)%phys(i)%d, sol(isol)%phys(i)%bd, sol(isol)%phys(i)%cbn, sol(isol)%phys(i)%sand, sol(isol)%phys(i)%silt, sol(isol)%phys(i)%clay` |
| [sym:soil_data_module] | `soildb` | `soildb(isol)%s%nly, soildb(isol)%ly(j)%z, soildb(isol)%ly(j)%bd, soildb(isol)%ly(j)%awc, soildb(isol)%ly(j)%k, soildb(isol)%ly(j)%cbn, soildb(isol)%ly(j)%clay, soildb(isol)%ly(j)%silt, soildb(isol)%ly(j)%sand, soildb(isol)%ly(j)%rock, soildb(isol)%ly(j)%alb, soildb(isol)%ly(j)%usle_k, soildb(isol)%ly(j)%ec, soildb(isol)%ly(j)%cal, soildb(isol)%ly(j)%ph` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sol(isol)%phys(i)%bd` | When a matching soil test record provides a bulk-density value other than -1.0, after the temporary millimeter database is filled and before the layer-averaging pass writes the final profile values. | `sol(isol)%phys(i)%bd` is replaced with the depth-averaged bulk density computed from the millimeter-level temporary profile, so the active soil profile reflects the soil-test-adjusted bulk density. |
| `sol(isol)%phys(i)%cbn` | When a matching soil test record provides a carbon value other than -1.0, during the layer-averaging pass over the temporary millimeter profile. | `sol(isol)%phys(i)%cbn` is replaced with the depth-averaged carbon value from the temporary profile, so the active soil profile reflects the soil-test-adjusted carbon content. |
| `sol(isol)%phys(i)%sand` | When a matching soil test record provides a sand value other than -1.0, during the layer-averaging pass over the temporary millimeter profile. | `sol(isol)%phys(i)%sand` is replaced with the depth-averaged sand value from the temporary profile, so the active soil profile reflects the soil-test-adjusted sand fraction. |
| `sol(isol)%phys(i)%silt` | When a matching soil test record provides a silt value other than -1.0, during the layer-averaging pass over the temporary millimeter profile. | `sol(isol)%phys(i)%silt` is replaced with the depth-averaged silt value from the temporary profile, so the active soil profile reflects the soil-test-adjusted silt fraction. |
| `sol(isol)%phys(i)%clay` | When a matching soil test record provides a clay value other than -1.0, during the layer-averaging pass over the temporary millimeter profile. | `sol(isol)%phys(i)%clay` is replaced with the depth-averaged clay value from the temporary profile, so the active soil profile reflects the soil-test-adjusted clay fraction. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-changing edits to `soils_test_adjust`. In 2025-08-12, the routine was extracted from `soils_init` and rewritten to use a temporary soil-test-adjustment subroutine file, while preserving the purpose of modifying soils from soil test values. In 2026-01-28, the logic was refactored to track previous depths correctly and to adjust bulk density and the other soil-test properties with a depth-aware averaging approach, including a fix that changed the clay assignment to write `%clay` instead of `%silt`. In 2026-01-29, the routine was extended to use `soil_data_module`, allocate a temporary millimeter-level soil database from `soildb`, overlay soil-test values into that structure, and then average back into `sol(isol)%phys(i)` while also introducing cleanup of the temporary allocation.

- 2025-08-12: extracted the soil-test adjustment logic into its own routine so soil updates happen during initialization from soil test values rather than inline in `soils_init`.
- 2026-01-28: corrected depth handling and made clay updates write to `sol(isol)%phys(i)%clay`; the routine now uses layer depths to compute weighted averages for the adjusted soil properties.
- 2026-01-29: added `soil_data_module`, built a temporary millimeter-resolution soil database from `soildb`, overlaid test values into that structure, and deallocated the temporary storage after recomputing the layer averages.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'soils_test_adjust' has no extracted documentation comment.
