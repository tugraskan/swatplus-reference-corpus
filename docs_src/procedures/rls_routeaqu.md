---
kind: procedure
symbol: rls_routeaqu
title: rls_routeaqu
status: filled
source_hash: a86bc6945c337e4d
version_label: SWAT+ 62.0.0
args:
  iob: Selects which routing object in `ob` provides the aquifer inflow. The procedure reads
    `ob(iob)%hin_til%flo` and `ob(iob)%hin_til%no3` from that object and adds them to the
    current HRU's bottom soil layer.
locals:
  j: Temporary HRU index. It is set from `ihru` and then used to locate the current HRU's
    soil and mineral-nitrogen profiles.
  lyr: Temporary soil-layer index. It is set to the last layer in the current HRU (`soil(j)%nly`)
    so the routine can update the bottom soil layer.
uses:
  hru_module: '`ihru` identifies which HRU is currently being processed. `rls_routeaqu` copies
    that global HRU pointer into `j` so it can update the correct `soil` and `soil1` profile
    for the active HRU.'
  soil_module: '`soil_module` provides the active HRU soil profile and its layer structure.
    The routine uses `soil(j)%nly` to find the bottom layer and then adds incoming water to
    `soil(j)%phys(lyr)%st` there.'
  hydrograph_module: '`hydrograph_module` holds the routed inflow object for this subroutine.
    `ob(iob)%hin_til%flo` supplies the water volume and `ob(iob)%hin_til%no3` supplies the
    nitrate mass that are transferred into the soil profile.'
  organic_mineral_mass_module: '`soil1` is the HRU mineral-nitrogen profile used by the organic/mineral
    mass accounting. The routine adds incoming nitrate to `soil1(j)%mn(lyr)%no3` so the layer''s
    mineral N pool stays consistent with routed inflow.'
---

<!-- facts:header -->

Adds aquifer inflow water and nitrate to the bottom soil layer for the current HRU.

## Bottom Line

This routine takes the incoming aquifer tile-flow object for the current routing object and deposits its water volume and nitrate into the bottom layer of the active HRU's soil profile. It is the handoff point that converts routed aquifer inflow into updates to soil storage and mineral nitrogen state.

If the added water makes the layer too wet, later saturation-excess handling is expected to redistribute the surplus. The nitrate addition similarly becomes part of the layer's mineral nitrogen pool and can be used by later soil and routing calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU control when an aquifer inflow has been detected for the current routing object. `hru_control` prepares the current object index and only calls `rls_routeaqu` when `ob(icmd)%hin_aqu%flo > 0`, so the routine acts on routed aquifer inflow before later steps such as crack-volume and evapotranspiration calculations. Its result affects the soil water and nitrate states that later saturation-excess redistribution and soil-process routines use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set the active HRU index from `ihru`. | Copies the globally selected HRU number into the local index `j` so the subroutine works on the current HRU's soil and mineral-state arrays. |
| 2. Identify the bottom soil layer. | Uses the number of layers in the current HRU soil profile to point `lyr` at the deepest layer, which is where aquifer inflow is deposited. |
| 3. Add aquifer water to the bottom layer water storage. | Increases `soil(j)%phys(lyr)%st` by the inflow water volume stored in `ob(iob)%hin_til%flo`. |
| 4. Add aquifer nitrate to the bottom layer mineral N pool. | Increases `soil1(j)%mn(lyr)%no3` by the nitrate carried in `ob(iob)%hin_til%no3`. |
| 5. Return to the caller. | Ends the subroutine after the soil-water and nitrate state updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(lyr)%st` |
| [sym:hydrograph_module] | `ob` | `ob(iob)%hin_til%flo, ob(iob)%hin_til%no3` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(lyr)%no3` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(j)%phys(lyr)%st` | When `ob(iob)%hin_til%flo` is positive and the routine is called from `hru_control` for the current object. | `soil(j)%phys(lyr)%st` is increased by the routed aquifer water volume at the bottom layer of the active HRU. This records the added water in soil storage before any later saturation-excess redistribution step. |
| `soil1(j)%mn(lyr)%no3` | When `ob(iob)%hin_til%no3` is present in the routed aquifer inflow for the current object. | `soil1(j)%mn(lyr)%no3` is increased by the nitrate mass delivered with aquifer inflow. This appends routed nitrate to the bottom layer's mineral nitrogen pool for later soil and transport accounting. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved for `rls_routeaqu`. The original addition in 94b6dec introduced the routine with the aquifer-to-bottom-layer updates and the comment about redistribution in `swr_satexcess`. Later, 39fabde changed only the local declarations by initializing `j` and `lyr` to zero; the water and nitrate update logic stayed the same.

- 94b6dec introduced `rls_routeaqu` as a new subroutine that copies `ihru` to `j`, selects the bottom layer, and adds `ob(iob)%hin_til%flo` and `ob(iob)%hin_til%no3` to the soil and mineral-nitrogen states.
- 39fabde added default initialization for the local integers `j` and `lyr` (`= 0`) without changing the routing or state-update behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rls_routeaqu' has no extracted documentation comment.
