---
kind: procedure
symbol: rls_routetile
title: rls_routetile
status: filled
source_hash: b98bb7b17df9247b
version_label: SWAT+ 62.0.0
args:
  iob: Unused object identifier passed in by the caller; the routine suppresses the compiler
    warning with `if (iob < 0) continue`, but the actual routing uses `ihru` and the HRU saturated-buffer
    fields instead.
  tile_fr_surf: Fraction of tile inflow treated as overland surface flow rather than delivered
    to the soil. The routine multiplies the buffer inflow and nitrate by `(1. - tile_fr_surf)`
    so only the subsurface fraction is added to the receiving layer.
locals:
  j: Loop-free HRU index copied from the module state `ihru`; it identifies which HRU's saturated
    buffer and soil profile are updated.
  lyr: Receiving soil-layer index for the tile inflow. It is set from `hru(j)%sb%sb_db%lyr`
    so the added water and nitrate go to the buffer's configured layer.
uses:
  hru_module: The saturated-buffer fields live on the current HRU object, so this module provides
    the HRU being routed and the buffer storage that supplies the inflow and nitrate. It also
    provides `ihru`, which selects the active HRU whose soil and buffer states are updated.
  soil_module: The soil profile state is where the routed tile water is stored after delivery.
    Updating `soil(j)%phys(lyr)%st` changes the receiving layer's water storage so later soil-water
    balance and excess-water handling can operate on the added inflow.
  hydrograph_module: The module is imported by the routine, but no specific symbol from it
    is referenced in the extracted source lines. Its presence matters only insofar as the
    routine compiles within the routing/state-update context, but the visible logic does not
    use a hydrograph-module variable here.
  organic_mineral_mass_module: The nitrate pool for each soil layer is stored in `soil1`,
    so this module provides the mineral-N state that receives the routed tile nitrate. Updating
    `soil1(j)%mn(lyr)%no3` makes the added nitrate available to later nutrient cycling and
    transport routines.
---

<!-- facts:header -->

Routes tile-drain inflow and nitrate into the receiving HRU's saturated buffer soil layer. It then clears the buffer flow stores so the water and nitrate are not counted twice.

## Bottom Line

This routine transfers the saturated-buffer tile inflow for the current HRU into the receiving soil layer. It uses the HRU's buffer settings to find the layer, adds the buffer water to soil water storage and the buffer nitrate to the mineral N pool, then zeroes the buffer inflow fields.

The routine matters because it is the handoff point between routed tile flow and the soil-state pools that later redistribution routines use. The added water can be redistributed if the layer becomes over-saturated, and the added nitrate becomes part of the layer mineral N state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU control after lateral flow routing and before aquifer flow routing, when the model is handling incoming tile flow for the active HRU. `hru_control` prepares `ihru`, the current `hru(j)` state, and the routed tile fraction `tile_fr_surf`; the result is then used by later soil-water and nutrient redistribution behavior, especially when the added water pushes the layer toward saturation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. suppress unused iob warning | If `iob` is negative, the routine executes a no-op `continue` so the argument is referenced and the compiler does not flag it as unused. This does not alter model state. |
| 2. select active HRU | Copies the current HRU index from `ihru` into local `j` so the routine updates the receiving HRU's states. |
| 3. choose receiving layer | Uses the saturated-buffer definition on the active HRU to find the soil layer that receives tile inflow, storing that layer number in `lyr`. |
| 4. add tile water to soil storage | Adds the subsurface fraction of the buffered tile inflow, `hru(j)%sb%inflo * (1. - tile_fr_surf)`, to the receiving soil layer water storage. |
| 5. add tile nitrate to mineral pool | Adds the subsurface fraction of buffered tile nitrate, `hru(j)%sb%no3 * (1. - tile_fr_surf)`, to the corresponding soil-layer nitrate pool. |
| 6. clear routed buffer water | Resets the saturated-buffer inflow water store to zero after it has been transferred to the soil layer so the same water is not routed again. |
| 7. clear routed buffer nitrate | Resets the saturated-buffer nitrate store to zero after transfer so the mineral N is only counted in the soil pool. |
| 8. return to caller | Ends the subroutine after updating the HRU and soil states, leaving the caller to continue with the rest of the HRU water-routing sequence. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru` | `hru(j)%sb%sb_db%lyr, hru(j)%sb%inflo, hru(j)%sb%no3` |
| [sym:soil_module] | `soil` | `soil(j)%phys(lyr)%st` |
| [sym:hydrograph_module] | `hydrograph_module` |  |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(lyr)%no3` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(j)%phys(lyr)%st` | When the active HRU has tile inflow routed to its saturated-buffer layer, the routine adds the subsurface portion of `hru(j)%sb%inflo` to the chosen soil layer. | `soil(j)%phys(lyr)%st` increases by the routed tile-water amount that is actually delivered to the subsurface layer. This represents water entering the receiving soil layer and makes that layer eligible for later saturation handling. |
| `soil1(j)%mn(lyr)%no3` | When the active HRU has buffered tile nitrate, the routine adds the subsurface portion of `hru(j)%sb%no3` to the same soil layer's mineral-N pool. | `soil1(j)%mn(lyr)%no3` increases by the nitrate mass delivered with the tile water. This moves nitrate from the saturated-buffer routing store into the receiving soil profile's mineral nitrogen state. |
| `hru(j)%sb%inflo` | After the routed tile inflow has been added to the soil layer. | `hru(j)%sb%inflo` is cleared to zero so the same tile water is not routed again in later steps. |
| `hru(j)%sb%no3` | After the routed tile nitrate has been added to the soil layer. | `hru(j)%sb%no3` is cleared to zero so the same nitrate mass is not double-counted in later routing or mass-balance calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits show the routine's evolution. It was introduced in df07e3f with tile inflow routed from `ob(iob)%hin_til` into `hru(j)%lumv%ldrain` using the tile flow fraction. 1807dbb changed the implementation to use the saturated-buffer fields `hru(j)%sb%inflo` and `hru(j)%sb%no3`, the receiving layer `hru(j)%sb%sb_db%lyr`, and then zeroed those buffer stores after transfer. bd18ad4 marked `iob` as unused and added a no-op guard `if (iob < 0) continue` to suppress warnings. 39fabde initialized `j` and `lyr` to zero.

- df07e3f added the subroutine and initially routed tile water and nitrate from `ob(iob)%hin_til` into the HRU soil profile.
- 1807dbb redirected routing to the HRU saturated-buffer state (`hru(j)%sb`) and cleared the buffer water and nitrate after transfer.
- bd18ad4 documented `iob` as unused and added the conditional no-op to silence compiler warnings.
- 39fabde initialized the local indices `j` and `lyr`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rls_routetile' has no extracted documentation comment.
- hydrograph_module is imported in the source, but no extracted symbol from it is used in the visible procedure body.
- The source uses a no-op `if (iob < 0) continue` solely to reference the unused argument.
