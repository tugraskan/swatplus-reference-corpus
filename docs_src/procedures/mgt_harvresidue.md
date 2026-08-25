---
kind: procedure
symbol: mgt_harvresidue
title: mgt_harvresidue
status: filled
source_hash: eb2b58e207a827c8
version_label: SWAT+ 62.0.0
args:
  jj: Selects the HRU whose plant community residue pools are updated.
  harveff: Sets the residue harvest efficiency to use directly when it is nonzero; if it is
    effectively zero, the routine falls back to the harvest operation's default efficiency.
  iharvop: Chooses the harvest operation record whose `eff`, `hi_ovr`, and `bm_min` values
    control the residue removal and minimum remaining biomass check.
locals:
  rsd_removed: Temporary organic mass holding the amount of residue removed from the current
    plant during the loop; it is used to update the plant residue pool, the community residue
    total, and the harvested carbon diagnostic.
  eff: The effective residue harvest efficiency used for calculations in this call, taken
    from `harveff` unless that value is almost zero, in which case the operation default is
    used.
  harv_idx: The harvest index override from `harvop_db(iharvop)%hi_ovr`; it scales the effective
    harvest efficiency into the net fraction applied to residue.
  net_eff: The combined residue removal fraction computed as `eff * harv_idx`; it is the factor
    multiplied by each plant residue pool to get the removed residue mass.
  reduction_frac: A corrective fraction used only when the initial removal would push remaining
    residue below `bm_min`; it rescales `rsd_removed` so the post-harvest residue stays at
    the minimum allowed mass.
  bm_min: The minimum biomass that must remain after residue removal, read from the selected
    harvest operation and used to cap the removal.
  ipl: Loops over each plant in the community so residue removal can be applied one plant
    at a time.
  j: Local HRU index copied from `jj` so the routine can use a mutable working index while
    updating module state.
uses:
  plant_module: The plant module provides `pcom(j)%npl`, which tells the routine how many
    plants are in the HRU community and therefore how many residue pools must be processed.
  carbon_module: The carbon module provides `hrc_d(j)%harv_stov_c`, the carbon harvest/loss
    diagnostic that this routine resets and then fills with the carbon mass removed from residue.
  mgt_operations_module: The management operations module stores the selected harvest-operation
    parameters that define the default efficiency, the harvest-index override, and the minimum
    biomass safeguard used by this routine.
  organic_mineral_mass_module: The organic mass module defines the residue and total-residue
    state objects and the `orgz` zero-mass value, which are needed to subtract removed residue
    and to reset totals when the residue pool becomes negligible.
---

<!-- facts:header -->

Removes a fraction of plant surface residue for an HRU harvest residue operation. It also records the carbon mass taken off the surface and preserves a minimum residue mass when required by the harvest operation.

## Bottom Line

This routine applies a residue harvest to the plant residue pools for one HRU. It uses the passed harvest efficiency together with the selected harvest operation database entry to decide how much residue to remove from each plant, while enforcing the operation's minimum remaining biomass limit.

For each plant in the community, it subtracts the removed residue from both the per-plant residue pool and the community residue total. It also sets the harvested stover carbon diagnostic in `hrc_d(j)%harv_stov_c`, which keeps later carbon accounting consistent with the residue removal.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when the management workflow reaches a harvest-residue operation. `actions` prepares `harveff` from the action table, and `mgt_sched` prepares it from `mgt%op3`; both pass the HRU index and harvest-operation index so this subroutine can update residue and carbon state. Its results feed later residue, carbon, and surface-condition calculations because the plant residue pools and `hrc_d(j)%harv_stov_c` are modified in place.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. choose effective efficiency | If the incoming harvest efficiency is effectively zero, use the harvest-operation default efficiency from `harvop_db(iharvop)%eff`; otherwise use the passed-in `harveff` value. |
| 2. load operation controls | Read the harvest index override and minimum biomass limit from the selected harvest operation, then combine the effective efficiency and harvest index into `net_eff`. |
| 3. clear carbon diagnostic | Reset the harvested stover carbon diagnostic for the target HRU before processing any plant residue. |
| 4. initialize residue accumulator | Start the temporary removed-residue mass at zero mass so each plant's removal can be computed cleanly inside the loop. |
| 5. loop over plants | For each plant in the community, compute the residue mass removed as `net_eff * pl_mass(j)%rsd(ipl)`. |
| 6. enforce minimum residue | If the planned removal would leave less than `bm_min` mass in the plant residue pool, shrink the removal using `reduction_frac` so the remaining residue stays at the allowed minimum. |
| 7. update residue pools | Subtract the removed residue from both the individual plant residue pool and the community residue total. |
| 8. guard against empty total | If the community residue total becomes negligible, reset it to the zero organic-mass object `orgz`. |
| 9. record harvested carbon | Store the carbon mass removed in the harvested stover carbon diagnostic for the HRU. |
| 10. finish loop and return | After all plants are processed, return to the caller with the residue and carbon state updated in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |
| [sym:carbon_module] | `hrc_d` | `hrc_d(j)%harv_stov_c` |
| [sym:mgt_operations_module] | `harvop_db` | `harvop_db(iharvop)%eff, harvop_db(iharvop)%hi_ovr, harvop_db(iharvop)%bm_min` |
| [sym:organic_mineral_mass_module] | `pl_mass, orgz` | `pl_mass(j)%rsd(ipl), pl_mass(j)%rsd(ipl)%m, pl_mass(j)%rsd_tot, pl_mass(j)%rsd_tot%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hrc_d(j)%harv_stov_c` | For each plant processed in `do ipl = 1, pcom(j)%npl`, after residue removal is computed. | `hrc_d(j)%harv_stov_c` is overwritten with the carbon mass removed from the current plant's residue, so the HRU-level carbon harvest diagnostic reflects the latest residue removal. |
| `pl_mass(j)%rsd(ipl)` | When `pl_mass(j)%rsd(ipl)` is updated after computing `rsd_removed`, with a possible reduction applied if the minimum biomass check would be violated. | The plant's surface residue pool is reduced by the harvested amount, leaving the post-harvest residue mass in place for later residue and carbon accounting. |
| `pl_mass(j)%rsd_tot` | After the plant residue total is reduced by `rsd_removed`, and only if the total residue mass falls below `1.e-6`. | The community residue total is refreshed to reflect the removal across plants, and it is reset to the zero mass object when effectively exhausted. |

## File I/O

<!-- facts:io -->


## Lineage

Five resolved commits changed `mgt_harvresidue`. The earliest resolved change replaced the old `soil1`-based residue handling with the current `pl_mass`/`hrc_d` structure. Later changes initialized local loop variables, then switched the routine to use `pcom(j)%npl` and moved the residue carbon tally to the new community residue structure. A subsequent change added operation-level controls (`harvop_db(iharvop)%hi_ovr`, `bm_min`) and the minimum-residue safeguard, and the latest resolved commit corrected the residue removal logic so it removes `net_eff * pl_mass(j)%rsd(ipl)` while preserving at least `bm_min` and resetting empty totals to `orgz`.

- 94b6dec introduced the routine in the older residue storage format, harvesting residue from `rsd1` arrays and accumulating total residue there.
- eb22103 refactored the routine to the new soil/residue structure and rewired carbon tracking to `soil1` and `hrc_d(j)%harv_stov_c`.
- 39fabde only initialized `j` and `ipl`, changing no harvest behavior.
- f8feed6 added the guard against tiny harvest efficiency and switched the residue/carbon bookkeeping to the current `soil1` form before the later refactor.
- 72206bc moved the residue operation to the `pl_mass` community structure, introduced `ipl` as the plant loop, and added the `pcom(j)%npl` loop over plants.
- 99e9b55 added the operation-derived harvest index and minimum biomass limit, changed residue removal to use `net_eff`, and enforced the `bm_min` floor plus zero-total reset.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_harvresidue' has no extracted documentation comment.
