---
kind: procedure
symbol: rls_routesoil
title: rls_routesoil
status: filled
source_hash: 68c4f6dbddd3fd22
version_label: SWAT+ 62.0.0
args:
  iob: '`iob` selects which object-connectivity entry in `ob` provides the incoming lateral
    flow for this call, so the routine routes the lateral inflow for that specific object
    into the currently active HRU.'
locals:
  latqlyr: '`latqlyr` holds the amount of lateral water assigned to the current soil layer
    during the distribution loop; it is initialized to zero and recalculated for each layer.'
  j: '`j` is the HRU index used to access the active soil profile in `soil(j)`; it is set
    from `ihru` before routing begins.'
  lyr: '`lyr` is the loop counter over soil layers in the current HRU profile.'
uses:
  hru_module: '`hru_module` supplies `ihru`, which identifies the active HRU, and `latqrunon`,
    which this routine overwrites with the incoming lateral inflow before distributing it
    through the soil profile.'
  soil_module: '`soil_module` holds the HRU soil profile being updated. The routine needs
    `soil(j)%nly` to know how many layers to traverse, `soil(j)%phys(lyr)%thick` and `soil(j)%phys(soil(j)%nly)%d`
    to apportion inflow by layer depth, and `soil(j)%phys(lyr)%st` to store the added water.'
  hydrograph_module: '`hydrograph_module` provides `ob(iob)%hin_lat%flo`, the lateral inflow
    volume for the selected object. That value is the source water this routine routes into
    the soil profile.'
---

<!-- facts:header -->

Routes incoming lateral soil water into the current HRU's soil layers.

## Bottom Line

`rls_routesoil` takes the lateral inflow attached to an object and adds that water to the soil water store for the active HRU. It distributes the inflow across soil layers using layer thickness relative to total profile depth, so deeper profiles receive more of the routed water in deeper layers.

This matters because it updates the HRU soil moisture state before later water-balance and saturation-excess logic runs. The routine does not write files or call other routines; it only transfers lateral inflow from `ob(iob)%hin_lat%flo` into `soil(j)%phys(lyr)%st` when there is meaningful inflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`rls_routesoil` runs during HRU routing inside `hru_control`, immediately after `hru_control` detects positive lateral inflow with `ob(icmd)%hin_lat%flo > 0`. `hru_control` prepares the object index and active HRU context; later soil-water accounting and saturation-excess behavior depend on the updated `latqrunon` and soil-layer storage values produced here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. capture active HRU | Set `j = ihru` so the routine works on the soil profile for the currently active HRU. |
| 2. load lateral inflow | Copy the incoming lateral flow from `ob(iob)%hin_lat%flo` into `latqrunon`, making the routed amount available as the procedure's working inflow value. |
| 3. test for meaningful flow | Only continue when the lateral inflow is greater than the tiny threshold `1.e-9`; otherwise no soil update is needed. |
| 4. route across layers | Loop through every soil layer in the current HRU, compute the layer share of the incoming lateral water using layer thickness and total profile depth, and add that share to `soil(j)%phys(lyr)%st`. |
| 5. end routine | Return to the caller after updating the lateral inflow state and soil-layer water storage. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `ihru, latqrunon` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(lyr)%thick, soil(j)%phys(lyr)%st` |
| [sym:hydrograph_module] | `ob` | `ob(iob)%hin_lat%flo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `latqrunon` | `latqrunon` is always updated when the routine starts, before the inflow threshold test. | `latqrunon` is overwritten with the current object's lateral inflow (`ob(iob)%hin_lat%flo`) so later soil-routing and downstream water-balance logic can use the routed amount. |
| `soil(j)%phys(lyr)%st` | When `latqrunon > 1.e-9`, each layer in `soil(j)%phys` is visited and its storage is increased by the computed layer share. | `soil(j)%phys(lyr)%st` is increased by the portion of lateral inflow assigned to that layer, representing added soil water in the active HRU profile. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved lineage commits changed `rls_routesoil`. The initial addition in `df07e3f` introduced the routine with lateral-flow routing into soil layers, and `39fabde` only initialized local variables (`latqlyr`, `j`, and `lyr`) without changing the routing logic.

- df07e3f added the full `rls_routesoil` routine: it reads `ob(iob)%hin_lat%flo`, checks for positive inflow, loops through `soil(j)%nly`, and adds a depth-weighted share to each layer's storage.
- 39fabde changed only local declarations by giving `latqlyr`, `j`, and `lyr` default initial values; the procedure's water-routing behavior remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rls_routesoil' has no extracted documentation comment.
