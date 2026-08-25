---
kind: procedure
symbol: cs_fert
title: cs_fert
status: filled
source_hash: 547e7d7593dc93c5
version_label: SWAT+ 62.0.0
args:
  jj: HRU index selecting which soil and balance records to update.
  ifrt: Fertilizer constituent database index; if it is not positive, no constituent mass
    is added.
  frt_kg: Applied fertilizer mass in kg/ha, which is scaled by the fertilizer composition
    to determine added constituent mass.
  fertop: Chemical-application operation index used to look up the surface fraction that splits
    the application between the top two layers.
locals:
  xx: 'Holds the fraction of the fertilizer application assigned to the current split portion:
    first the surface fraction, then its complement for the remaining portion.'
  l: Loop counter used to process the two split portions of the top-layer application.
uses:
  mgt_operations_module: '`mgt_operations_module` provides `chemapp_db(fertop)%surf_frac`,
    which tells `cs_fert` how much of the fertilizer is treated as surface-applied versus
    the remainder in the near-surface portion.'
  cs_module: '`cs_module` provides the fertilizer constituent database and the HRU balance
    arrays. `fert_cs(ifrt)` supplies the seo4, seo3, and boron loads per fertilizer type,
    while `hcsb_d(jj)%cs(*)%fert` records how much fertilizer-derived constituent mass has
    been added for accounting.'
  constituent_mass_module: '`constituent_mass_module` supplies the global constituent switch
    and the HRU soil constituent storage. `cs_db%num_cs` gates whether constituent simulation
    is active, and `cs_soil(jj)%ly(1)%cs(*)` is the soil pool that receives the fertilizer-applied
    masses.'
  fertilizer_data_module: '`fertilizer_data_module` is needed because this routine reads the
    fertilizer constituent composition and the flag that enables constituent fertilizer handling.'
---

<!-- facts:header -->

Adds fertilizer-borne chemical constituents to the top soil layer and updates the constituent fertilizer balance for an HRU.

## Bottom Line

`cs_fert` applies constituent fertilizer mass for one HRU when constituent simulation is active and the fertilizer type is valid. It uses the fertilizer composition database and the surface-application fraction to split the applied fertilizer between the surface and subsurface portions of the top layer, then adds the resulting masses to the soil constituent pool and the HRU fertilizer balance arrays.

This routine matters because it is the point where a management fertilizer application becomes simulated constituent loading in the soil profile. Downstream constituent transport, reaction, and accounting routines rely on the updated `cs_soil` and `hcsb_d` values.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cs_fert` runs from management workflows after a fertilizer/manure application has been selected and its fertilizer type, applied amount, and application operation have been set up by the caller. `actions` and `mgt_sched` both prepare `ifrt`, `frt_kg`, and the application operation index before calling it. Its results feed later constituent mass balance and transport behavior because it increases the soil constituent pools and the fertilizer flux accounting for the HRU.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. gate on constituent simulation | The subroutine does nothing unless other constituent simulation is enabled (`cs_db%num_cs > 0`) and constituent fertilizer tracking is active (`fert_cs_flag == 1`). |
| 2. require a valid fertilizer type | It only continues when the fertilizer database index is positive, preventing updates for invalid or missing fertilizer IDs. |
| 3. split the application into two passes | The loop runs twice to represent the two portions of the application split by the surface fraction. |
| 4. assign the surface fraction on the first pass | On the first pass, `xx` is set to `chemapp_db(fertop)%surf_frac`, the fraction treated as surface-applied. |
| 5. assign the remainder on the second pass | On the second pass, `xx` becomes `1. - chemapp_db(fertop)%surf_frac`, the part not assigned to the surface fraction. |
| 6. add seo4 mass to the top soil constituent pool | The routine increases `cs_soil(jj)%ly(1)%cs(1)` by `xx * frt_kg * fert_cs(ifrt)%seo4`, adding fertilizer-derived seo4 to the top soil layer. |
| 7. add seo3 mass to the top soil constituent pool | The routine increases `cs_soil(jj)%ly(1)%cs(2)` by `xx * frt_kg * fert_cs(ifrt)%seo3`, adding fertilizer-derived seo3 to the top soil layer. |
| 8. add boron mass to the top soil constituent pool | The routine increases `cs_soil(jj)%ly(1)%cs(3)` by `xx * frt_kg * fert_cs(ifrt)%boron`, adding fertilizer-derived boron to the top soil layer. |
| 9. record seo4 fertilizer loading in the balance array | It adds the same seo4 mass to `hcsb_d(jj)%cs(1)%fert` so the HRU fertilizer balance tracks this input. |
| 10. record seo3 fertilizer loading in the balance array | It adds the same seo3 mass to `hcsb_d(jj)%cs(2)%fert` for fertilizer balance accounting. |
| 11. record boron fertilizer loading in the balance array | It adds the same boron mass to `hcsb_d(jj)%cs(3)%fert` for fertilizer balance accounting. |
| 12. finish after both split portions are processed | After both passes are complete, the routine returns to the caller with the updated soil and balance states in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `chemapp_db` | `chemapp_db(fertop)%surf_frac` |
| [sym:cs_module] | `fert_cs, hcsb_d, fert_cs_flag` | `fert_cs(ifrt)%seo4, fert_cs(ifrt)%seo3, fert_cs(ifrt)%boron, hcsb_d(jj)%cs(1)%fert, hcsb_d(jj)%cs(2)%fert, hcsb_d(jj)%cs(3)%fert` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_cs, cs_soil(jj)%ly(1)%cs(1), cs_soil(jj)%ly(1)%cs(2), cs_soil(jj)%ly(1)%cs(3)` |
| [sym:fertilizer_data_module] | `fert_cs, fert_cs_flag` | `fert_cs(ifrt)%seo4, fert_cs(ifrt)%seo3, fert_cs(ifrt)%boron, fert_cs_flag` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(jj)%ly(1)%cs(1)` | When constituent simulation is active, the fertilizer ID is valid, and the routine is processing either split portion of the application. | `cs_soil(jj)%ly(1)%cs(1)` gains fertilizer-derived seo4 mass in the top soil layer, with the added amount proportional to the split fraction, application rate, and fertilizer composition. |
| `cs_soil(jj)%ly(1)%cs(2)` | When constituent simulation is active, the fertilizer ID is valid, and the routine is processing either split portion of the application. | `cs_soil(jj)%ly(1)%cs(2)` gains fertilizer-derived seo3 mass in the top soil layer, scaled by the split fraction, applied mass, and fertilizer composition. |
| `cs_soil(jj)%ly(1)%cs(3)` | When constituent simulation is active, the fertilizer ID is valid, and the routine is processing either split portion of the application. | `cs_soil(jj)%ly(1)%cs(3)` gains fertilizer-derived boron mass in the top soil layer, scaled by the split fraction, applied mass, and fertilizer composition. |
| `hcsb_d(jj)%cs(1)%fert` | When constituent simulation is active, the fertilizer ID is valid, and the routine is processing either split portion of the application. | `hcsb_d(jj)%cs(1)%fert` is incremented by the seo4 mass added from fertilizer so the HRU fertilizer balance reflects this source. |
| `hcsb_d(jj)%cs(2)%fert` | When constituent simulation is active, the fertilizer ID is valid, and the routine is processing either split portion of the application. | `hcsb_d(jj)%cs(2)%fert` is incremented by the seo3 mass added from fertilizer so the HRU fertilizer balance reflects this source. |
| `hcsb_d(jj)%cs(3)%fert` | When constituent simulation is active, the fertilizer ID is valid, and the routine is processing either split portion of the application. | `hcsb_d(jj)%cs(3)%fert` is incremented by the boron mass added from fertilizer so the HRU fertilizer balance reflects this source. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits touched `cs_fert`. The initial addition in `df07e3f` introduced the subroutine, its purpose comment, inputs, module uses, conditional gating, split-application loop, and the soil/balance updates. `16e54aa` changed the constituent-simulation test from `.eq.1` to `== 1`. `39fabde` initialized local variables `xx`, `ics`, and `l` at declaration time. `bd18ad4` commented out the unused `ics` declaration, leaving the active logic unchanged.

- df07e3f added the routine and its fertilizer-to-soil constituent transfer logic for seo4, seo3, and boron.
- 16e54aa only modernized the `fert_cs_flag` comparison syntax in the activation test.
- 39fabde initialized local variables to default values at declaration to prevent uninitialized use.
- bd18ad4 removed the active `ics` local by commenting it out, indicating it was no longer needed in the routine.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_fert' has no extracted documentation comment.
- algorithm_steps revised: expanded the core algorithm from 6 draft steps to 12 source-backed steps and cited only visible line ranges from cs_fert.f90.
