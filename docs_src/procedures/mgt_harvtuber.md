---
kind: procedure
symbol: mgt_harvtuber
title: mgt_harvtuber
status: filled
source_hash: 5b58397a41b189e6
version_label: SWAT+ 62.0.0
args:
  jj: Selects which HRU entry to operate on; the routine copies `jj` into local `j` and then
    reads and updates the plant, soil, and residue state for that HRU.
  iplant: Selects which plant-community slot within the HRU to harvest; the routine copies
    `iplant` into `ipl` and then uses that plant index for all biomass, residue, and pesticide
    updates.
  iharvop: Selects the harvest-operation record whose `eff` value controls how much root biomass
    is removed and how the tuber harvest is applied.
locals:
  j: HRU index used to access and update `pcom`, `pl_mass`, `soil`, `soil1`, and `cs_pl` for
    the chosen landscape unit.
  k: Loop index over pesticide constituents; it steps through each pesticide mass tracked
    in `cs_pl` so all pesticide pools are adjusted with the harvest.
  ly: Loop index over soil layers; it is used to place the remaining root mass into the corresponding
    layer residue pool.
  harveff: Harvest-efficiency factor read from `harvop_db(iharvop)%eff`; it determines the
    fraction of root biomass removed as harvested yield.
  idp: Plant database identifier copied from `pcom(j)%plcur(ipl)%idplt`; it identifies which
    plant definition the community slot refers to, even though this routine does not use it
    later.
  yld_rto: Fraction of total plant biomass represented by the harvested yield; it is used
    to apportion pesticide mass removed with the yield.
  yldpst: Temporary calculation of pesticide mass removed with the harvested yield; the routine
    computes it for each pesticide but does not store it back to a state variable.
uses:
  basin_module: The basin plant-community array provides the current plant status and growth
    state for the selected HRU, including the plant database id, pest stress, and layer root
    fractions needed to route harvested root mass into residue.
  hru_module: The HRU plant index `ipl` is the local alias for the selected plant-community
    slot, and every plant-state read/write in this routine is keyed by that index.
  plant_module: The plant community growth and status fields supply the root distribution,
    plant identity, and pest-stress factor that control how harvested biomass is distributed
    and how much of it is retained as effective yield.
  plant_data_module: The zero-valued plant-mass object is the reset value used to clear all
    plant biomass pools after tuber harvest kills the plant.
  mgt_operations_module: The harvest-operation database provides the per-operation efficiency
    value that determines how much root biomass is removed for this tuber harvest type.
  carbon_module: This module provides the organic-mass container used for harvested yield
    and residue bookkeeping, including the yield mass field and the plant community mass pools
    that are updated by this routine.
  organic_mineral_mass_module: These plant-community and soil-profile mass containers are
    the reservoirs that receive the remaining roots and aboveground residue, and then are
    reset so the harvested plant contributes no further biomass.
  soil_module: The soil profile supplies the number of layers to iterate over when distributing
    remaining root mass into layer-specific residue pools.
  constituent_mass_module: The constituent-mass module tracks pesticide mass in and on the
    plant, and this routine reduces those pools in proportion to the harvested yield fraction.
---

<!-- facts:header -->

Removes tuber harvest from a plant community, applies harvest efficiency and pest stress, and shifts the surviving root and aboveground material into soil residue and zeroed plant pools.

## Bottom Line

mgt_harvtuber handles the special harvest case for tuber crops and peanuts. It uses the selected HRU, plant-community plant, and harvest operation to compute how much root biomass is taken, how much residue is left behind, and how much pesticide mass is removed with the harvested yield.

The routine first trims root biomass by the harvest efficiency, recomputes root fractions, then routes the remaining root mass into layer residue using the plant root distribution. It also reduces the harvested yield by pest stress, scales pesticide masses off the harvested fraction, and finally kills the plant by moving aboveground biomass into residue and zeroing all plant mass pools.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during management execution when the action dispatcher or management scheduler encounters a harvest operation whose type is tuber or peanuts. The caller must already have selected the HRU, plant-community index, and harvest-operation record; `mgt_harvtuber` then updates plant, residue, and pesticide state that later soil-residue accounting and plant-state bookkeeping depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU and plant indices, plant id, and harvest efficiency | Copies the incoming HRU and plant indices into local variables, reads the plant database id from the selected plant community, and loads the harvest efficiency from the chosen harvest-operation record. |
| 2. compute harvested root yield | Multiplies the current root mass by harvest efficiency to get the harvested tuber yield mass. |
| 3. subtract harvested root mass from the plant | Removes the harvested amount from the plant's root mass so only the unharvested root fraction remains. |
| 4. recompute plant root fractions | Calls `pl_rootfr` to update the layerwise root fraction distribution after the root mass change. |
| 5. distribute remaining roots to soil residue by layer | Loops over all soil layers and adds the remaining root mass to each layer's plant residue pool using the updated root fraction for that layer. |
| 6. reduce harvested yield for pest stress | Applies the plant's pest-stress factor to the harvested yield so the effective yield reflects pest losses. |
| 7. scale pesticide mass removed with harvested yield | Loops over each pesticide constituent, computes the harvested-fraction ratio from yield mass and total plant biomass, and reduces both internal and surface pesticide masses with a lower bound of zero. |
| 8. move aboveground biomass to residue | Adds all aboveground plant mass to the plant residue totals so the non-harvested top growth becomes residue. |
| 9. zero the plant biomass pools | Resets total, aboveground, leaf, stem, seed, and root biomass to the zero-mass object because this tuber harvest is treated as killing the plant. |
| 10. return to caller | Exits after the plant, residue, and pesticide state updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pcom` | `pcom(j)` |
| [sym:hru_module] | `ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%rtfr(ly), pcom(j)%plcur(ipl)%pest_stress` |
| [sym:plant_data_module] | `plt_mass_z` | `plt_mass_z` |
| [sym:mgt_operations_module] | `harvop_db` | `harvop_db(iharvop)%eff` |
| [sym:carbon_module] | `pl_yield` | `pl_yield%m` |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1, pl_yield, plt_mass_z` | `pl_mass(j)%root(ipl), soil1(j)%pl(ipl)%rsd(ly), pl_yield%m, pl_mass(j)%tot(ipl)%m, pl_mass(j)%rsd_tot, pl_mass(j)%ab_gr(ipl), pl_mass(j)%rsd(ipl), pl_mass(j)%tot(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%seed(ipl)` |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:constituent_mass_module] | `cs_db, cs_pl` | `cs_db%num_pests, cs_pl(j)%pl_in(ipl)%pest(k), cs_pl(j)%pl_on(ipl)%pest(k)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ipl` | When the routine starts, after copying `jj` into `j` and `iplant` into `ipl`. | `ipl` becomes the active plant-community index used for all subsequent reads and writes in the selected HRU. |
| `pl_yield` | After root biomass is harvested and pest stress is applied to the yield. | `pl_yield` holds the effective harvested root yield mass that is later used to scale pesticide removal. |
| `pl_mass(j)%root(ipl)` | Immediately after `pl_yield = harveff * pl_mass(j)%root(ipl)` and before the plant is reset. | `pl_mass(j)%root(ipl)` is reduced by the harvested fraction, leaving only the root mass that remains in the field. |
| `soil1(j)%pl(ipl)%rsd(ly)` | During the soil-layer loop after root fractions are recomputed. | Each layer's plant residue pool receives the remaining root mass apportioned by that layer's root fraction. |
| `cs_pl(j)%pl_in(ipl)%pest(k)` | During the pesticide loop for each pesticide constituent. | The internal pesticide mass on the harvested plant is reduced in proportion to the harvested yield fraction and constrained to nonnegative values. |
| `cs_pl(j)%pl_on(ipl)%pest(k)` | During the same pesticide loop for each pesticide constituent. | The surface pesticide mass on the harvested plant is reduced in proportion to the harvested yield fraction and constrained to nonnegative values. |
| `pl_mass(j)%rsd_tot` | After the harvest residue is added to the plant residue pool. | `pl_mass(j)%rsd_tot` accumulates the aboveground residue created by the harvest. |
| `pl_mass(j)%rsd(ipl)` | After the harvest residue is added to the plant-specific residue pool. | `pl_mass(j)%rsd(ipl)` accumulates the aboveground residue associated with the harvested plant. |
| `pl_mass(j)%tot(ipl)` | At the end of the routine when the plant is treated as killed by tuber harvest. | `pl_mass(j)%tot(ipl)` is reset to zero so the plant no longer carries total biomass. |
| `pl_mass(j)%ab_gr(ipl)` | At the end of the routine when the plant is treated as killed by tuber harvest. | `pl_mass(j)%ab_gr(ipl)` is reset to zero because all aboveground biomass has been moved to residue. |
| `pl_mass(j)%leaf(ipl)` | At the end of the routine when the plant is treated as killed by tuber harvest. | `pl_mass(j)%leaf(ipl)` is reset to zero so leaf biomass is removed from the living plant state. |
| `pl_mass(j)%stem(ipl)` | At the end of the routine when the plant is treated as killed by tuber harvest. | `pl_mass(j)%stem(ipl)` is reset to zero so stem biomass is removed from the living plant state. |
| `pl_mass(j)%seed(ipl)` | At the end of the routine when the plant is treated as killed by tuber harvest. | `pl_mass(j)%seed(ipl)` is reset to zero so seed biomass is removed from the living plant state. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_harvtuber.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `3e18acf` (2026-02-17, "Integrate CENTURY residue/N updates and root-fraction tracking changes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_harvtuber.f90` are listed.

- `3e18acf` (2026-02-17) — Integrate CENTURY residue/N updates and root-fraction tracking changes
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `eb22103` (2024-12-05) — Refactor residue management to use new soil1 structure
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_harvtuber' has no extracted documentation comment.
- The source shows `idp` is assigned from `pcom(j)%plcur(ipl)%idplt` but not used afterward in this routine.
- The source computes `yldpst` inside the pesticide loop but does not store or use it after the assignment.
- The source section provided no resolved lineage commits for `mgt_harvtuber`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
