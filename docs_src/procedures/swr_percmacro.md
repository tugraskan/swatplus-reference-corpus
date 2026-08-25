---
kind: procedure
symbol: swr_percmacro
title: swr_percmacro
status: filled
source_hash: 23a389b759c56c3d
version_label: SWAT+ 62.0.0
locals:
  j: HRU index used to select the active soil profile and update the corresponding `sepbtm(j)`
    and soil-profile state for the current hydrologic response unit.
  ly: Loop counter for soil layers, running from the deepest layer to the top so the routine
    can route crack flow upward through the profile.
  crklch: Fixed scaling factor applied to the deepest-layer crack contribution calculation
    before any remaining crack flow is distributed upward.
  xx: Temporary water-deficit variable for the current layer, computed as field capacity minus
    current stored water; it limits how much crack flow that layer can still absorb.
  crk: Temporary crack-flow amount assigned in the current step, either for the deepest-layer
    crack contribution or for filling remaining storage in the current layer.
uses:
  hru_module: 'This module holds the HRU-level inputs and outputs that control and record
    the routing: `ihru` selects the active HRU, `voltot` and `inflpcp` limit how much crack
    water is available, `volcrmin` sets the minimum crack volume threshold, and `sepcrk`,
    `sepcrktot`, and `sepbtm` are updated to report how much crack flow remains or exits the
    profile.'
  soil_module: The soil profile data provide the per-layer geometry and water status needed
    to convert crack volume into seepage and to store the routed water. `soil(j)%nly` sets
    the traversal range, `soil(j)%ly(ly)%volcr` and the depth fields define the deepest-layer
    crack contribution, `soil(j)%phys(ly)%fc` and `soil(j)%phys(ly)%st` define how much water
    each layer can still take, and `soil(j)%ly(ly)%prk` records per-layer percolation gains.
---

<!-- facts:header -->

Moves today’s crack-flow seepage through the active soil profile, filling soil-layer crack storage and passing any remainder to the bottom of the HRU.

## Bottom Line

swr_percmacro computes percolation by crack flow for the current HRU. It starts from the available crack-flow water, then works from the deepest soil layer upward, using crack volume and layer storage to decide how much water can be retained in each layer versus passed downward.

The routine updates the HRU’s bottom seepage total and the soil-layer percolation counters, while also increasing layer water storage where crack flow is absorbed. `swr_percmain` calls it during crack-flow routing and then subtracts the returned total crack seepage from the day’s infiltration-driven seepage before continuing with soil-water routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the daily seepage/percolation workflow when crack flow is enabled. `swr_percmain` prepares the day’s infiltration-based seepage, calls `swr_percmacro` to route the crack-flow portion, and then subtracts `sepcrktot` from `sepday` before continuing with the regular soil routing. Its results affect bottom seepage and per-layer percolation totals used later in the HRU water balance.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize crack seepage | Set the crack-flow amount to the lesser of total crack volume and infiltrating precipitation, then copy that amount to the running total `sepcrktot`. |
| 2. start deep-to-shallow routing | Only route crack flow if the initial amount is large enough, then loop from the deepest soil layer upward so lower layers are handled before upper layers. |
| 3. clear per-layer temporaries | Reset the temporary crack-flow and deficit variables for the current layer before any layer-specific allocation is computed. |
| 4. assign deepest-layer crack contribution | For the deepest layer, compute a crack-flow contribution from layer crack volume, layer thickness, total crack depth, and `volcrmin`; then either subtract that amount from remaining crack seepage or consume all remaining seepage if the computed contribution is larger. |
| 5. fill available water storage | Compute the current layer’s storage deficit as field capacity minus stored water, add as much remaining crack seepage as that deficit allows, store it in the layer, and pass the same amount to the overlying layer’s percolation counter when one exists. |
| 6. stop when crack seepage is exhausted | Exit the layer loop once the remaining crack seepage becomes negligibly small, because there is nothing left to distribute upward. |
| 7. send leftover crack flow out the bottom | After all layers are processed, if crack seepage is still above the threshold, add it to bottom seepage and to the deepest layer’s percolation counter as flow leaving the profile. |
| 8. return | Finish the subroutine after the HRU seepage and soil-profile state have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sepbtm, voltot, inflpcp, ihru, sepcrk, sepcrktot, volcrmin` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%ly(ly)%volcr, soil(j)%phys(ly)%d, soil(j)%phys(ly-1)%d, soil(j)%ly(ly)%prk, soil(j)%phys(ly)%fc, soil(j)%phys(ly)%st, soil(j)%ly(ly-1)%prk` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sepcrk` | When `sepcrk` is initialized at line 42 and may be reduced inside the deep-to-shallow routing loop, and when residual crack seepage is checked again at line 73. | `sepcrk` is the remaining crack-flow seepage still to be routed within the profile. It is reduced as water is assigned to the deepest layer, filled into layer storage, or passed downward, so later steps know how much crack water is left. |
| `sepcrktot` | Set immediately after `sepcrk` is initialized, before any routing begins. | `sepcrktot` records the full crack-flow amount available for this routine call. It preserves the original value of `sepcrk` so the caller can subtract the total crack seepage from the day’s seepage budget after this routine returns. |
| `sepbtm(j)` | Updated when crack flow is assigned to the deepest layer or when leftover crack flow exits the bottom of the soil profile. | `sepbtm(j)` accumulates the HRU’s bottom-of-profile seepage from crack flow. It increases by the amount routed into the deepest layer and by any residual crack seepage that cannot be stored in the profile. |
| `soil(j)%ly(ly)%prk` | Updated in the deepest-layer branch and in the layer-storage fill branch whenever crack flow is added to a layer’s percolation total. | `soil(j)%ly(ly)%prk` records the percolation credited to the current soil layer from crack flow. The deepest layer gets the initial crack contribution, and each layer receives additional credited flow when remaining crack seepage is absorbed there. |
| `soil(j)%phys(ly)%st` | Updated inside the `if (xx > 0.) then` branch when the current layer still has room to take crack flow. | `soil(j)%phys(ly)%st` increases by the amount of crack flow that fits within the layer’s remaining storage to field capacity. This represents water entering the soil matrix from the crack pathway. |
| `soil(j)%ly(soil(j)%nly)%prk` | Updated when leftover crack seepage is routed out of the bottom of the profile after the layer loop, if any remains above the threshold. | The deepest layer’s percolation total receives any crack flow that could not be absorbed in the profile, so the bottom layer reflects the final outflow credited to the HRU. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.3.9 | Bottom crack-flow contribution | $w_{crk,btm}=0.5*crk*(\frac{crk_{ly=nn}}{depth_{ly=nn}})$ | Verified against SWAT+ 62.0.0 (swr_percmacro.f90:49). bottom-layer crack flow `crklch*(volcr/dz*voltot - volcrmin) |
| 2:3.3.2 | Lagged crack opening under dry conditions | $SW<0.90*FC$ | Verified against SWAT+ 62.0.0 (swr_percmacro.f90:48). bottom-layer crack condition (ly == nly branch) |

## Lineage

Two resolved commits changed `swr_percmacro`. Commit df07e3f introduced the subroutine with its crack-flow routing logic, module dependencies, and bottom seepage update. Commit 39fabde did not change the algorithm; it only initialized the local scalar variables `j`, `ly`, `xx`, and `crk` to explicit starting values.

- df07e3f added the full crack-flow percolation routine, including the `sepcrk`/`sepcrktot` bookkeeping, deepest-layer crack allocation, storage fill loop, and bottom seepage updates.
- 39fabde changed only local variable initialization by setting `j`, `ly`, `xx`, and `crk` to zero at declaration; the routing behavior stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_percmacro' has no extracted documentation comment.
- algorithm_steps revised: condensed the original 10-step draft into 8 source-backed steps while preserving the routing order and using only visible line numbers.
- Source shows an unresolved `external :: layersplit` declaration at line 33, but no call to `layersplit` appears in the extracted body.
