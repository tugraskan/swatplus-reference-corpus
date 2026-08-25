---
kind: procedure
symbol: mgt_killop
title: mgt_killop
status: filled
source_hash: c3534c870d9a3f9a
version_label: SWAT+ 62.0.0
args:
  jj: Selects the HRU/community entry to operate on; the routine copies it into local `j`
    and uses that index to update the corresponding plant community, soil pools, and residue/carbon
    bookkeeping.
  iplant: Identifies which plant within the HRU plant community is being killed; the routine
    stores it in `ipl` and uses it to move and then zero that plant’s masses and status.
locals:
  j: HRU index used to access the target plant community, soil profile, residue pools, and
    carbon/pest accounting for this kill operation. It is set from `jj` at the start and does
    not otherwise change.
  k: Loop counter over pesticide/constituent slots when the kill operation transfers plant-associated
    pesticide mass to the soil surface pool.
  npl: Loop counter over all plants in the community when rebuilding the total surface residue
    pool from individual plant residue masses.
  ly: Loop counter over soil layers when distributing the killed plant’s root mass into layer-specific
    soil residue pools.
uses:
  basin_module: The module is imported by the subroutine, so it is part of the routine’s execution
    context; however, no specific basin-module symbol was extracted as directly used in the
    source lines provided.
  organic_mineral_mass_module: 'This module defines the organic mass containers that the kill
    logic updates: per-plant mass (`tot`, `ab_gr`, `leaf`, `stem`, `seed`, `root`, `rsd`),
    community totals (`*_com`, `rsd_tot`), and zero-mass templates (`orgz`, `plt_mass_z`).
    Those objects are the actual targets of the biomass and residue transfers.'
  hru_module: The HRU-level plant index `ipl` is imported from this module and is overwritten
    with the `iplant` argument so the rest of the routine can address the correct plant slot
    in the community arrays.
  soil_module: The soil profile object supplies `soil(j)%nly`, which bounds the layer loop
    used to spread the killed plant’s root mass into soil residue across all layers in the
    HRU.
  plant_module: 'This module provides the plant-community containers and state that are reset
    or consulted: the number of plants in the community, the root-fraction array used for
    root redistribution, the per-plant mass and stress objects, and plant-status fields that
    are cleared after the kill.'
  constituent_mass_module: The constituent/pesticide mass arrays are updated during kill so
    pesticide mass on and in the plant is moved into the soil surface pool and then cleared
    from the plant pools.
  carbon_module: These carbon accounting arrays record how much carbon from killed biomass
    is transferred to residue pools for output and diagnostics, so they must be updated consistently
    with the mass moves.
---

<!-- facts:header -->

Kills one plant in an HRU: transfers its biomass, roots, residue, pest, and carbon state into the appropriate pools, then zeros the plant's live-state variables.

## Bottom Line

mgt_killop performs the model’s plant-kill bookkeeping for one HRU (`j`) and one plant (`iplant`). It first updates root fractions, then moves above-ground biomass to surface residue, adds dead roots to soil residue by layer, removes the killed plant’s masses from the community totals, and transfers associated carbon and pest mass into the residue/soil accounting pools.

After the mass transfers, it clears the killed plant’s live plant-growth, plant-mass, and plant-stress state so the community no longer treats that plant as growing. The routine is called from management workflows when a kill action is triggered for a matching plant.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a management action requests a plant kill for a specific HRU/plant pair. `actions` and `mgt_sched` prepare the HRU index and plant selection, then call `mgt_killop`; later output and carbon/residue accounting depend on the updated `pl_mass`, `soil1`, `cs_soil`, `cs_pl`, `hrc_d`, `hpc_d`, and `pcom` state produced here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set indices | Copies the caller’s HRU and plant selections into local indices so the rest of the routine works on the chosen community entry and plant slot. |
| 2. update roots | Recomputes the plant’s layer root fractions before mass transfer so the root residue can be distributed by the current rooting profile. |
| 3. move above-ground biomass | Adds the killed plant’s above-ground mass to its surface-residue pool, converting standing biomass into residue. |
| 4. rebuild total residue pool | Initializes the community surface-residue total and sums all plant residue pools to refresh the HRU-wide residue total. |
| 5. distribute root residue | Loops over all soil layers and adds the killed plant’s root mass to each layer’s plant residue pool in proportion to the layer root fraction. |
| 6. remove community mass | Subtracts the killed plant’s biomass components from the community totals for total biomass, above-ground mass, leaf, stem, seed, and root pools. |
| 7. record carbon transfers | Adds the killed plant’s surface and root carbon to the HRU residue-carbon and plant-carbon loss trackers, including root carbon in the plant drop total. |
| 8. zero plant mass | Resets all of the killed plant’s live mass containers to the zero-mass template so no biomass remains assigned to that plant slot. |
| 9. move pesticides | For each pesticide constituent, moves plant-associated pesticide mass from plant pools into the top soil-layer pool and clears the plant pools. |
| 10. reset plant state | Clears the plant-growth structure, resets plant mass and stress objects, and marks the plant as not growing with heat accumulation reset. |
| 11. return | Exits after all mass, residue, pest, carbon, and status bookkeeping for the killed plant has been completed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state referenced by the routine is not resolved to a specific symbol in the extracted context.` |  |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1, orgz, plt_mass_z` | `pl_mass(j)%rsd(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%rsd_tot, pl_mass(j)%rsd(npl), soil1(j)%pl(ipl)%rsd(ly), pl_mass(j)%root(ipl), pl_mass(j)%tot_com, pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr_com, pl_mass(j)%leaf_com, pl_mass(j)%leaf(ipl), pl_mass(j)%stem_com, pl_mass(j)%stem(ipl), pl_mass(j)%seed_com, pl_mass(j)%seed(ipl), pl_mass(j)%root_com, pl_mass(j)%ab_gr(ipl)%c, pl_mass(j)%root(ipl)%c` |
| [sym:hru_module] | `ipl` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:plant_module] | `pcom, plmz, plstrz` | `pcom(j)%npl, pcom(j)%plg(ipl)%rtfr(ly), pcom(j)%plg(ipl), pcom(j)%plm(ipl), pcom(j)%plstr(ipl), pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plcur(ipl)%curyr_mat` |
| [sym:constituent_mass_module] | `cs_db, cs_soil, cs_pl` | `cs_db%num_pests, cs_soil(j)%ly(1)%pest(k), cs_pl(j)%pl_in(ipl)%pest(k), cs_pl(j)%pl_on(ipl)%pest(k)` |
| [sym:carbon_module] | `hrc_d, hpc_d` | `hrc_d(j)%plant_surf_c, hrc_d(j)%plant_root_c, hpc_d(j)%drop_c` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ipl` | Always, after assigning `ipl = iplant` | `ipl` is set to the plant slot being killed so all subsequent array references target the selected plant entry in the HRU. |
| `pl_mass(j)%rsd(ipl)` | After root fractions are refreshed and before the plant mass is zeroed | The killed plant’s above-ground residue pool receives its above-ground biomass, converting live biomass into surface residue for that plant slot. |
| `pl_mass(j)%rsd_tot` | During the residue-sum pass over `npl = 1, pcom(j)%npl` | The HRU total surface residue pool is rebuilt from the sum of all plant residue pools so it reflects the kill transfer. |
| `soil1(j)%pl(ipl)%rsd(ly)` | For each soil layer `ly = 1, soil(j)%nly` while the plant is being killed | Each layer’s plant residue pool receives a share of the killed plant’s root mass based on the layer root fraction, so dead roots are stored in the soil profile. |
| `pl_mass(j)%tot_com` | After the mass transfer, when community totals are updated for the killed plant | The community total biomass is reduced by the killed plant’s total mass so the remaining community totals exclude the removed plant. |
| `pl_mass(j)%ab_gr_com` | After the mass transfer, when community totals are updated for the killed plant | The community above-ground mass total is reduced by the killed plant’s above-ground biomass. |
| `pl_mass(j)%leaf_com` | After the mass transfer, when community totals are updated for the killed plant | The community leaf-mass total is reduced by the killed plant’s leaf mass. |
| `pl_mass(j)%stem_com` | After the mass transfer, when community totals are updated for the killed plant | The community stem-mass total is reduced by the killed plant’s stem mass. |
| `pl_mass(j)%seed_com` | After the mass transfer, when community totals are updated for the killed plant | The community seed-mass total is reduced by the killed plant’s seed mass. |
| `pl_mass(j)%root_com` | After the mass transfer, when community totals are updated for the killed plant | The community root-mass total is reduced by the killed plant’s root mass. |
| `hrc_d(j)%plant_surf_c` | When carbon accounting is updated for the killed plant | Surface residue carbon gain is increased by the killed plant’s above-ground carbon so print/output carbon accounting matches the residue transfer. |
| `hrc_d(j)%plant_root_c` | When carbon accounting is updated for the killed plant | Soil/root residue carbon gain is increased by the killed plant’s root carbon to match the dead-root transfer into soil residue. |
| `hpc_d(j)%drop_c` | When carbon accounting is updated for the killed plant | The plant-carbon drop total is increased by the killed plant’s above-ground and root carbon so the plant-loss accounting matches the kill event. |
| `pl_mass(j)%tot(ipl)` | When the killed plant’s mass is cleared | The killed plant’s total biomass object is reset to the zero-mass template so no live total mass remains in that plant slot. |
| `pl_mass(j)%ab_gr(ipl)` | When the killed plant’s mass is cleared | The killed plant’s above-ground mass object is reset to the zero-mass template after the biomass has been moved to residue. |
| `pl_mass(j)%leaf(ipl)` | When the killed plant’s mass is cleared | The killed plant’s leaf mass object is reset to zero after being removed from the community totals. |
| `pl_mass(j)%stem(ipl)` | When the killed plant’s mass is cleared | The killed plant’s stem mass object is reset to zero after being removed from the community totals. |
| `pl_mass(j)%seed(ipl)` | When the killed plant’s mass is cleared | The killed plant’s seed mass object is reset to zero after being removed from the community totals. |
| `pl_mass(j)%root(ipl)` | When the killed plant’s mass is cleared | The killed plant’s root mass object is reset to zero after its mass has been distributed to soil residue. |
| `cs_soil(j)%ly(1)%pest(k)` | For each pesticide constituent during the transfer loop | The top soil-layer pesticide pool receives the pesticide mass that was on and in the killed plant, representing deposition to the soil surface. |
| `cs_pl(j)%pl_in(ipl)%pest(k)` | For each pesticide constituent during the transfer loop | Pesticide mass in the plant-internal pool is cleared after being moved to the soil pool. |
| `cs_pl(j)%pl_on(ipl)%pest(k)` | For each pesticide constituent during the transfer loop | Pesticide mass on the plant surface is cleared after being moved to the soil pool. |
| `pcom(j)%plm(ipl)` | After plant mass and growth are reset | The plant-mass status object is reset to the zero-valued template so the plant slot has no remaining active biomass state. |
| `pcom(j)%plstr(ipl)` | After plant mass and growth are reset | The plant-stress object is reset to the zero-valued template so no prior stress state persists for the killed plant. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_killop.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 13 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_killop.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `3e18acf` (2026-02-17) — Integrate CENTURY residue/N updates and root-fraction tracking changes
- `febcf0c` (2026-01-27) — corrections to root distribution and tracking features to soil and plant modules
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_killop' has no extracted documentation comment.
- algorithm_steps revised: expanded the core sequence to include index setup, carbon and pest transfers, and final plant-state reset based on the visible source lines.
- basin_module is imported but no specific basin_module symbol was resolved in the extracted source lines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
