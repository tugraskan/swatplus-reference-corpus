---
kind: procedure
symbol: pl_partition
title: pl_partition
status: filled
source_hash: 7203551351d0e7ed
version_label: SWAT+ 62.0.0
args:
  j: Selects the HRU/plant-community slot whose active plant state is partitioned; the routine
    uses j to index pcom(j) and pl_mass(j).
  init: 'Controls whether the routine is doing initial setup or a normal simulation update:
    init = 1 assigns the starting biomass fractions, while init = 0 runs the daily repartitioning
    logic that fills deficient pools from pl_mass_up.'
locals:
  idp: Plant database index for the current plant species; it is taken from pcom(j)%plcur(ipl)%idplt
    and used to look up plant type and yield concentrations in pldb(idp).
  root_frac: Stores the target fraction of total plant mass that should be in roots for the
    current plant, taken from pcom(j)%plg(ipl)%root_frac.
  ab_gr_frac: Stores the target fraction of total mass that should be above ground; it is
    computed from root_frac and harvest index rules, especially for tuber crops.
  leaf_mass_frac: Target fraction of above-ground biomass assigned to leaves when the routine
    is splitting above-ground mass into leaf, stem, and seed pools.
  stem_mass_frac: Target fraction of above-ground biomass assigned to stem/stalk after accounting
    for leaf and seed fractions.
  seed_mass_frac: Target fraction of total or above-ground biomass assigned to the seed/grain
    yield pool, depending on plant type and tuber logic.
  n_left: Intermediate nitrogen mass remaining after the seed pool is assigned its yield concentration;
    the remainder is redistributed to the non-seed pools.
  n_frac: Fallback nitrogen concentration used to spread remaining nitrogen across non-seed
    pools for annuals and grasses when the routine distributes N by mass.
  p_left: Intermediate phosphorus mass remaining after the seed pool is assigned its yield
    concentration; the remainder is redistributed to the non-seed pools.
  p_frac: Fallback phosphorus concentration used to spread remaining phosphorus across non-seed
    pools for annuals and grasses when the routine distributes P by mass.
  mass_left: Working mass pool available for topping up underfilled compartments during the
    daily update; it starts from pl_mass_up%m and is reduced as root, seed, and leaf are brought
    up to target fractions.
  mass_act: Current mass in the compartment being checked against its target fraction before
    any top-up is applied.
  mass_opt: Target or optimal mass for the compartment being checked, computed from total
    plant mass and the compartment fraction.
  mass_add: Amount of biomass added to a compartment during the daily refill logic, limited
    by the available mass_left.
  leaf_frac_veg: Base leaf share of the vegetative above-ground portion, chosen by plant type
    and used to derive leaf and stem fractions.
  leaf_mass_frac_veg: Leaf fraction within vegetative above-ground biomass after adjusting
    the base leaf share by the plant's current LAI relative to potential LAI.
uses:
  plant_data_module: pldb provides the plant-specific type and yield concentration parameters
    that decide which partitioning rules to apply and how much N and P should be placed in
    the seed pool.
  basin_module: basin_module matters because the plant community and population-scaling inputs
    live there and determine the current plant's identity, growth status, LAI scaling, root
    fraction, and adjusted harvest index that drive the partition equations.
  hru_module: hru_module matters because ipl selects the active plant slot within each HRU,
    so every array lookup in pl_partition is scoped to the current plant instance.
  plant_module: plant_module provides the current plant status and growth state, including
    species identity, current and potential LAI, root fraction, harvest-index adjustment,
    and the carbon fractions used to convert biomass into carbon mass.
  carbon_module: carbon_module matters because the routine uses the shared carbon fraction
    parameters to convert each biomass compartment into carbon mass for leaf, stem, seed,
    and root pools.
  organic_mineral_mass_module: organic_mineral_mass_module matters because it defines the
    plant mass pools updated here; pl_partition writes the total, root, leaf, stem, seed,
    above-ground, and nutrient contents back into pl_mass for the current plant.
---

<!-- facts:header -->

Partitions a plant's total biomass, carbon, nitrogen, and phosphorus into root, leaf, stem, and seed pools for one HRU plant.

## Bottom Line

pl_partition updates the current plant's total mass by adding the daily biomass increment, then divides that total into root, leaf, stem, and seed compartments using plant type, harvest index, LAI, and configured yield concentrations. It keeps the mass pools and their C/N/P contents consistent so later growth, harvest, and residue routines can use compartment-level plant state.

For tuber crops it allocates total biomass differently from other annuals, solving above-ground and seed fractions from root fraction and adjusted harvest index. During initialization it can also seed the plant pools from their initial fractions instead of doing the daily refill logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after upstream plant growth setup has populated pl_mass_up, plant identity, LAI, root fraction, and harvest-index state; it is called by mgt_transplant and plant_init with init = 1 for initialization, and by pl_grow with init = 0 during the simulation. Its results feed later growth, harvest, residue, and mass-balance behavior because those routines read the compartment masses and nutrient contents stored in pl_mass.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the current plant identity and add the daily biomass/carbon increment to the total plant pool. | The routine picks the active plant species from pcom(j)%plcur(ipl)%idplt and updates pl_mass(j)%tot(ipl)%m and pl_mass(j)%tot(ipl)%c by adding pl_mass_up%m and pl_mass_up%c. |
| 2. Choose the base vegetative leaf fraction and scale it by current LAI relative to potential LAI. | Perennial plants use a smaller leaf fraction than other plants, and that fraction is converted into leaf_mass_frac_veg using current LAI and lai_pot. |
| 3. Compute root, above-ground, leaf, stem, and seed fractions for tuber crops. | For warm_annual_tuber and cold_annual_tuber, the code solves above-ground biomass from root fraction and adjusted harvest index, then derives seed, leaf, and stem fractions from that solution. |
| 4. Compute root, above-ground, leaf, stem, and seed fractions for non-tuber plants. | For all other plants, root_frac comes from plant growth state, above-ground biomass is the remainder, seed mass follows hi_adj, and the remaining above-ground biomass is split into leaf and stem fractions. |
| 5. During simulation updates, top up underfilled root, seed, and leaf pools from the available new biomass. | When init = 0, the routine compares current root, seed, and leaf masses to target fractions of total mass and adds mass_add to each pool until mass_left is exhausted. |
| 6. Assign the remaining biomass to stem and recompute above-ground mass. | Any leftover mass is added to stem, then ab_gr is recomputed as leaf + stem + seed. |
| 7. During initialization, assign all compartment masses directly from the target fractions. | When init is not 0, the routine fills ab_gr, root, leaf, seed, and stem directly from the computed fractions of total mass. |
| 8. Convert biomass compartments to carbon using fixed carbon fractions. | Leaf, stem, seed, and root carbon are computed from c_frac, and the carbon totals for ab_gr and tot are summed from the compartment carbon pools. |
| 9. Partition nitrogen for perennial plants by assigning yield N to seed and distributing the remainder by mass. | If the plant is perennial and has nontrivial biomass, seed N is computed from cnyld, any negative remainder is clamped, and leaf, stem, and root N are spread in proportion to their masses. |
| 10. Partition phosphorus for perennial plants using the same yield-first and mass-proportional pattern. | Seed P comes from cpyld, negative remainder is clamped, and the remaining P is distributed across leaf, stem, and root by mass. |
| 11. Partition nitrogen for annuals and grasses using yield concentration and a fallback concentration across the remaining biomass. | For non-perennials, seed N is set from cnyld, negative remainder is corrected, n_frac is computed from the non-seed biomass, and leaf, stem, and root N are assigned from that concentration. |
| 12. Partition phosphorus for annuals and grasses using yield concentration and a fallback concentration across the remaining biomass. | For non-perennials, seed P is set from cpyld, negative remainder is corrected, p_frac is computed from the non-seed biomass, and leaf, stem, and root P are assigned from that concentration. |
| 13. Return the updated plant mass state to the caller. | The subroutine ends after writing the updated compartment masses and nutrient contents into pl_mass. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%typ, pldb(idp)%cnyld, pldb(idp)%cpyld` |
| [sym:basin_module] | `pcom, plcp` | `pcom(j)%plcur(ipl)%lai_pot, pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%lai, pcom(j)%plg(ipl)%root_frac, pcom(j)%plg(ipl)%hi_adj, plcp(idp)%popsc1, plcp(idp)%popsc2` |
| [sym:hru_module] | `ipl` |  |
| [sym:plant_module] | `pcom, c_frac` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%lai, pcom(j)%plcur(ipl)%lai_pot, pcom(j)%plg(ipl)%root_frac, pcom(j)%plg(ipl)%hi_adj, c_frac%leaf, c_frac%stem, c_frac%seed, c_frac%root` |
| [sym:carbon_module] | `c_frac` | `c_frac%leaf, c_frac%stem, c_frac%seed, c_frac%root` |
| [sym:organic_mineral_mass_module] | `pl_mass, pl_mass_up` | `pl_mass(j)%tot(ipl)%m, pl_mass_up%m, pl_mass(j)%tot(ipl)%c, pl_mass_up%c, pl_mass(j)%root(ipl)%m, pl_mass(j)%seed(ipl)%m, pl_mass(j)%leaf(ipl)%m, pl_mass(j)%stem(ipl)%m, pl_mass(j)%ab_gr(ipl)%m, pl_mass(j)%leaf(ipl)%c, pl_mass(j)%stem(ipl)%c, pl_mass(j)%seed(ipl)%c, pl_mass(j)%root(ipl)%c, pl_mass(j)%ab_gr(ipl)%c, pl_mass(j)%seed(ipl)%n, pl_mass(j)%tot(ipl)%n, pl_mass(j)%leaf(ipl)%n, pl_mass(j)%stem(ipl)%n, pl_mass(j)%root(ipl)%n, pl_mass(j)%ab_gr(ipl)%n, pl_mass(j)%seed(ipl)%p, pl_mass(j)%tot(ipl)%p, pl_mass(j)%leaf(ipl)%p, pl_mass(j)%stem(ipl)%p, pl_mass(j)%root(ipl)%p, pl_mass(j)%ab_gr(ipl)%p` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pl_mass(j)%tot(ipl)%m` | Whenever pl_partition runs, after pl_mass_up%m has been added to total mass. | Stores the current plant's cumulative biomass after adding the daily biomass increment; later compartment fractions and yield computations depend on this total mass. |
| `pl_mass(j)%tot(ipl)%c` | Whenever pl_partition runs, after pl_mass_up%c has been added to total carbon. | Stores the current plant's cumulative carbon mass; later carbon accounting uses the compartment values summed from this total pool. |
| `pl_mass(j)%root(ipl)%m` | If init = 0 and the current root mass is below the target root fraction, or if init /= 0 during direct initialization. | Root biomass is increased or assigned so the root pool matches the target fraction of total plant mass. |
| `pl_mass(j)%seed(ipl)%m` | If init = 0 and the current seed mass is below the target seed fraction, or if init /= 0 during direct initialization. | Seed biomass is increased or assigned to match the harvest-index-based target fraction of total plant mass. |
| `pl_mass(j)%leaf(ipl)%m` | If init = 0 and the current leaf mass is below the target leaf fraction, or if init /= 0 during direct initialization. | Leaf biomass is increased or assigned so the leaf pool follows the LAI-scaled vegetative fraction. |
| `pl_mass(j)%stem(ipl)%m` | If init = 0 after root, seed, and leaf replenishment, or if init /= 0 during direct initialization. | Stem biomass receives any leftover biomass and then becomes part of the initialized above-ground split. |
| `pl_mass(j)%ab_gr(ipl)%m` | After stem, leaf, and seed masses have been set in either update mode or initialization mode. | Above-ground biomass is recalculated as the sum of leaf, stem, and seed compartments. |
| `pl_mass(j)%leaf(ipl)%c` | After biomass partitioning, using c_frac%leaf and the leaf biomass. | Leaf carbon is set from leaf biomass and the fixed leaf carbon fraction. |
| `pl_mass(j)%stem(ipl)%c` | After biomass partitioning, using c_frac%stem and the stem biomass. | Stem carbon is set from stem biomass and the fixed stem carbon fraction. |
| `pl_mass(j)%seed(ipl)%c` | After biomass partitioning, using c_frac%seed and the seed biomass. | Seed carbon is set from seed biomass and the fixed seed carbon fraction. |
| `pl_mass(j)%root(ipl)%c` | After biomass partitioning, using c_frac%root and the root biomass. | Root carbon is set from root biomass and the fixed root carbon fraction. |
| `pl_mass(j)%ab_gr(ipl)%c` | After all compartment carbon values are computed. | Above-ground carbon is updated as the sum of leaf, stem, and seed carbon pools. |
| `pl_mass(j)%seed(ipl)%n` | For perennial plants when total non-root biomass is nontrivial. | Seed nitrogen is computed from the plant database yield-N concentration, with fallback handling if that would exceed total plant N. |
| `pl_mass(j)%leaf(ipl)%n` | For perennial plants after seed N is removed and the remainder is nonnegative. | Leaf nitrogen is allocated from the leftover N in proportion to leaf biomass. |
| `pl_mass(j)%stem(ipl)%n` | For perennial plants after seed N is removed and the remainder is nonnegative. | Stem nitrogen is allocated from the leftover N in proportion to stem biomass. |
| `pl_mass(j)%root(ipl)%n` | For perennial plants after seed N is removed and the remainder is nonnegative. | Root nitrogen is allocated from the leftover N in proportion to root biomass. |
| `pl_mass(j)%ab_gr(ipl)%n` | For perennial plants after the leaf, stem, and root N allocations are made. | Above-ground nitrogen is updated as seed N plus leaf and stem N. |
| `pl_mass(j)%seed(ipl)%p` | For perennial plants when total non-root biomass is nontrivial. | Seed phosphorus is computed from the plant database yield-P concentration, with fallback handling if that would exceed total plant P. |
| `pl_mass(j)%leaf(ipl)%p` | For perennial plants after seed P is removed and the remainder is nonnegative. | Leaf phosphorus is allocated from the leftover P in proportion to leaf biomass. |
| `pl_mass(j)%stem(ipl)%p` | For perennial plants after seed P is removed and the remainder is nonnegative. | Stem phosphorus is allocated from the leftover P in proportion to stem biomass. |
| `pl_mass(j)%root(ipl)%p` | For perennial plants after seed P is removed and the remainder is nonnegative. | Root phosphorus is allocated from the leftover P in proportion to root biomass. |
| `pl_mass(j)%ab_gr(ipl)%p` | For perennial plants after the leaf, stem, and root P allocations are made. | Above-ground phosphorus is updated as seed P plus leaf and stem P. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.1.3 | Accumulated biomass | $bio=\sum_{i=1}^{d}\Delta bio_i$ | Total plant mass is updated by adding the daily biomass increment pl_mass_up to cumulative plant biomass. |
| 5:2.4.4 | Above-ground biomass from root fraction | $bio_{ag}=(1-fr_{root})*bio$ | Verified against SWAT+ 62.0.0 (pl_partition.f90:50). ab_gr_frac = (1.-root_frac)/(1.+hi_adj) |
| 5:2.4.5 | Nitrogen in yield using yield concentration | $yld_N=fr_{N,yld}*yld$ | Yield nitrogen is computed from seed mass using cnyld rather than an explicit frN,yld * yld variable. |
| 5:2.4.6 | Phosphorus in yield using yield concentration | $yld_P=fr_{P,yld}*yld$ | Yield phosphorus is computed from seed mass using cpyld rather than an explicit frP,yld * yld variable. |

## Lineage

Resolved lineage shows four changes to pl_partition. The original file was added in df07e3f with the initial mass partitioning, carbon conversion, and N/P distribution logic. 94b6dec changed the subroutine to accept the init argument and keep initial vs simulation behavior separate. e18817a introduced the daily refilling logic for root/seed/leaf pools, added mass_left and related control variables, and changed the perennial leaf fraction constant. eb22103 refactored the refill logic to use mass_add and Min() so the daily biomass increment is allocated incrementally to underfilled compartments. 889136d only corrected a comment typo in the init argument description.

- df07e3f established the routine's full partitioning workflow: total biomass update, type-based biomass fractions, carbon conversion, and N/P redistribution.
- 94b6dec added the init argument so initialization and simulation partitioning could follow different paths.
- e18817a added the init-controlled daily refill path with mass_left/mass_act/mass_opt, and changed the perennial leaf fraction from 0.30 to 0.02.
- eb22103 revised the simulation path so underfilled root, seed, and leaf pools are topped up by mass_add limited by the remaining daily biomass increment.
- 889136d made no behavior change; it only fixed the init comment spelling.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_partition' has no extracted documentation comment.
