---
kind: procedure
symbol: swr_satexcess
title: swr_satexcess
status: filled
source_hash: 2417832f73260a99
version_label: SWAT+ 62.0.0
locals:
  j: HRU index for the current call. It is set from `ihru` and used to look up the active
    HRU, soil profile, wetland storage, and hydrograph state for that HRU.
  ul_excess: Temporary amount of water above a layer's saturation limit. The routine recomputes
    it as it moves excess water upward through the soil profile and then uses the leftover
    amount to route runoff or ponding flow.
  rto: Fraction of the standing-water seepage mass that should be reassigned to the wetland
    after saturation excess is removed. It is computed from excess water divided by the available
    seepage volume and capped at 1.0.
  nn: Number of soil layers in the current HRU profile. It controls the layer loop from bottom
    to top.
  ly: Main soil-layer loop counter. The routine walks from the deepest layer up to layer 1
    while checking and redistributing saturation excess.
  ly1: Inner loop counter used when excess from the top layer is propagated upward through
    the rest of the soil profile. It identifies each higher layer that may absorb the overflow.
  ires: Surface-storage flag copied from `hru(j)%dbs%surf_stor`. A value of 0 means excess
    goes to runoff; a nonzero value means the HRU has depressional storage and excess is handled
    as wetland/ponded water.
uses:
  hru_module: The HRU module supplies the active HRU identifier, surface-storage setting,
    area, seepage volume, and the runoff/saturation-excess accumulators that this routine
    updates. Without `hru_module`, `swr_satexcess` would have no way to know which HRU to
    process or where to store the runoff and seepage adjustments.
  soil_module: The soil module holds the layer count plus the per-layer water stored (`st`)
    and saturation capacity (`ul`) values that define whether a layer is overloaded. This
    routine's whole job is to compare `st` against `ul` and move the extra water between these
    layer states.
  hydrograph_module: The hydrograph module provides the water and constituent output objects
    used to record where the excess water and redistributed nutrients go. `ht2`, `wet`, and
    `wet_seep_day` carry the volumes and loads that are updated when excess is routed to runoff
    or wetland storage.
  basin_module: The basin module is listed as a dependency in the source, but the extracted
    lines in this procedure do not reference a specific basin state symbol directly. In this
    routine's workflow, basin-level context matters only insofar as routing decisions must
    remain consistent with the broader HRU-to-basin water balance.
  organic_mineral_mass_module: The organic/mineral mass module holds the soil nutrient and
    water-soluble organic pools that are reduced when a portion of standing-water seepage
    is reallocated to wetland storage. Those pools must be adjusted so the water transfer
    does not leave the soil nutrient balances inconsistent.
  gwflow_module: The groundwater-flow flag determines whether saturation excess leaving the
    soil profile also needs to be tracked in the groundwater runoff accumulator. That module
    matters because it changes whether `satexq` is updated along with `surfq`.
  reservoir_module: The reservoir module provides wetland geometry, especially weir height
    and water depth, which control whether excess is treated as direct runoff to `ht2` or
    stored in `wet`. It also supplies `wet_ob(j)%depth`, which is recomputed after ponded
    water changes.
---

<!-- facts:header -->

Redistributes excess soil water upward through a saturated profile and routes any remaining excess to runoff or wetland storage. It also reallocates associated nutrients from the top soil layer into ponded water when wetlands are present.

## Bottom Line

swr_satexcess checks each HRU soil profile for water stored above the saturation limit (`ul`) and pushes that excess upward layer by layer until the profile is back at or below saturation. This is the saturation-excess redistribution step that keeps the soil-water balance consistent before the rest of the daily water accounting continues.

If excess water still remains after the profile is fully saturated, the routine sends it to surface runoff (`surfq`) or, when the HRU has depressional storage, to wetland/ponded storage (`wet` or `ht2`). In wetland cases it also scales seepage-related nutrient pools in `soil1` and adds matching loads to the wetland hydrograph outputs so the water and mass balances stay aligned.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the percolation workflow after `swr_percmain` has finished moving soil water and before the model recomputes soil-profile totals and later routing quantities. Its outputs are consumed immediately by downstream daily water accounting, including updated soil water storage, runoff/saturation-excess bookkeeping, and wetland ponding depth/constituent balances.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Bind the current HRU and storage flag | Copies the active HRU index from `ihru` into `j` and reads the HRU's depressional-storage flag into `ires`. |
| 2. Traverse the soil profile from bottom to top | Loads the number of layers from `soil(j)%nly` and loops upward through the profile so excess water can be pushed toward the surface. |
| 3. Move excess from lower layers to the layer above | For each layer below the top, compares stored water to saturation and transfers any excess to the next higher layer while resetting the current layer to its saturation limit. |
| 4. Test the top layer and propagate overflow upward | Checks whether the top layer is above saturation, clamps it to its upper limit, and if needed pushes the overflow through the remaining layers until either the excess is absorbed or all layers are saturated. |
| 5. Route any remaining soil excess to runoff or ponding | If excess still remains after the profile is saturated, sends it to surface runoff and, when groundwater soil routing is active, also accumulates it in `satexq`. |
| 6. Handle wetland or depressional storage cases | When the HRU has storage, routes the excess into wetland/ponded water, chooses between `ht2` and `wet` using `wet_ob(j)%weir_hgt`, reduces standing seepage, and recomputes wetland depth. |
| 7. Reallocate seepage-associated nutrient and organic mass | If seepage remains, computes a transfer ratio, scales it to 1.0 or less, removes the corresponding mineral N, mineral P, and water-soluble organic pools from `soil1`, and adds matching loads to the wetland hydrograph state. |
| 8. Finish the HRU loop | Ends the soil-layer redistribution loop and returns to the caller after the soil, runoff, and wetland states have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, surfq, satexq, ihru` | `hru(j)%dbs%surf_stor, hru(ihru)%area_ha, hru(j)%water_seep, hru(j)%area_ha` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(ly)%st, soil(j)%phys(ly)%ul, soil(j)%phys(ly-1)%st, soil(j)%phys(1)%st, soil(j)%phys(1)%ul, soil(j)%phys(ly1)%st, soil(j)%phys(ly1)%ul` |
| [sym:hydrograph_module] | `ht2, wet, wet_seep_day` | `ht2%flo, wet(j)%flo, wet_seep_day(j)%no3, wet_seep_day(j)%nh3, wet_seep_day(j)%solp, wet_seep_day(j)%orgn, wet_seep_day(j)%sedp, wet(j)%no3, wet(ihru)%no3, wet(j)%nh3, wet(ihru)%nh3, wet(j)%orgn, wet(ihru)%orgn, wet(j)%solp, wet(ihru)%solp, wet(j)%sedp, wet(ihru)%sedp` |
| [sym:basin_module] | `wet` | `wet_ob(j)%weir_hgt, wet_ob(j)%depth` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(1)%no3, soil1(j)%mn(1)%nh4, soil1(j)%mp(1)%act, soil1(j)%water(1)%n, soil1(j)%water(1)%p` |
| [sym:gwflow_module] | `gw_soil_flag` | `gw_soil_flag` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(j)%weir_hgt, wet_ob(j)%depth` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(j)%phys(ly)%st` | When `ly > 1` and `soil(j)%phys(ly)%st > soil(j)%phys(ly)%ul`. | The current layer is above saturation, so its storage is reduced to the saturation limit and the excess is moved to the layer above. |
| `soil(j)%phys(ly-1)%st` | When `ly > 1` and the current layer is above saturation. | The layer immediately above receives the excess water that was removed from the current lower layer. |
| `soil(j)%phys(1)%st` | When the top layer is above saturation and excess is being propagated upward through the profile. | The surface layer is clamped to its saturation limit before any overflow is passed to deeper bookkeeping in the profile loop. |
| `soil(j)%phys(ly1)%st` | When overflow from the top layer is pushed into a higher layer and that higher layer also exceeds saturation. | That higher layer is clipped to its saturation limit and the remaining overflow is carried upward again. |
| `surfq(j)` | When the profile is still saturated after redistribution and `ires == 0`. | Remaining excess leaves the HRU as surface runoff by increasing `surfq(j)`. |
| `satexq(j)` | When the profile is still saturated after redistribution and `ires == 0` with groundwater soil routing enabled. | The same leftover excess is also tracked as saturation-excess runoff in `satexq(j)`. |
| `ht2%flo` | When the HRU has depressional storage and `wet_ob(j)%weir_hgt < 0.001`. | Excess water is diverted to the outlet/reservoir hydrograph volume `ht2%flo` instead of being held in the wetland pool. |
| `wet(j)%flo` | When the HRU has depressional storage and `wet_ob(j)%weir_hgt >= 0.001`. | Excess water is added to the wetland ponded-water volume `wet(j)%flo`. |
| `hru(j)%water_seep` | When excess water is being removed from a wetland HRU. | Standing seepage is reduced but never allowed to go below zero, preserving a physically valid seepage volume. |
| `wet_ob(j)%depth` | After wetland volume is updated in a storage HRU. | Wetland depth is recomputed from ponded volume and HRU area so later routing sees the updated water level. |
| `soil1(j)%mn(1)%no3` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | The soil nitrate pool in `soil1` is reduced in proportion to the fraction of seepage transferred to wetland storage. |
| `soil1(j)%mn(1)%nh4` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | The soil ammonium pool in `soil1` is reduced by the same seepage transfer fraction. |
| `soil1(j)%mp(1)%act` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | The active mineral phosphorus pool is reduced to match the mass moved with ponded seepage. |
| `soil1(j)%water(1)%n` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | The water-soluble organic nitrogen pool is reduced in proportion to seepage transfer. |
| `soil1(j)%water(1)%p` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | The water-soluble organic phosphorus pool is reduced in proportion to seepage transfer. |
| `wet(j)%no3` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | Wetland nitrate storage is increased by the seepage-associated nitrate load. |
| `wet(j)%nh3` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | Wetland ammonium storage is increased by the seepage-associated ammonium load. |
| `wet(j)%orgn` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | Wetland organic nitrogen storage is increased by the seepage-associated organic N load. |
| `wet(j)%solp` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | Wetland soluble phosphorus storage is increased by the seepage-associated soluble P load. |
| `wet(j)%sedp` | When `hru(j)%water_seep > 1.e-6` in a wetland HRU. | Wetland sediment-associated phosphorus storage is increased by the seepage-associated sediment P load. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `swr_satexcess`. The original addition in df07e3f introduced the subroutine to move excess soil water upward, route leftover saturation excess to runoff or wetland storage, and redistribute associated wetland seepage nutrients. Commit 39fabde only initialized the local scalars (`j`, `ul_excess`, `rto`, `nn`, `ly`, `ly1`, `ires`) without changing the algorithm. Commit 889136d fixed a comment typo. Commit 645ac00 changed the wetland branch so, when the weir height is below 0.001 m, excess is added to `ht2%flo` and `surfq` instead of only to `wet(j)%flo`, and it also clamps `hru(j)%water_seep` with `max(0., ...)` after removing excess water.

- df07e3f established the full saturation-excess redistribution workflow: upward soil-water shifting, runoff routing, wetland ponding, and nutrient reallocation tied to seepage.
- 39fabde made the temporary locals explicitly initialized, reducing dependence on undefined initial values but not altering the flow logic.
- 889136d corrected an inline comment only; no runtime behavior changed.
- 645ac00 introduced the weir-height branch for wetland routing and added a nonnegative floor to `hru(j)%water_seep`, changing how excess water is split between `ht2`, `surfq`, and `wet`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_satexcess' has no extracted documentation comment.
- external symbol `cli_lapse` appears in the source but is not used in the extracted body.
- basin_module is imported in the source, but no specific basin state symbol was resolved from the extracted lines.
