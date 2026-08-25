---
kind: procedure
symbol: mgt_harvbiomass
title: mgt_harvbiomass
status: filled
source_hash: dfe7f24ad6b986ed
version_label: SWAT+ 62.0.0
args:
  jj: '`jj` is the HRU index for the plant community being harvested; the routine uses it
    to access the correct `pcom`, `pl_mass`, `cs_pl`, `cs_soil`, `hrc_d`, and `hpc_d` entries.'
  iplant: '`iplant` selects which plant within HRU `jj` is being harvested; it is assigned
    to local `ipl` and used to index the plant-specific mass, growth, and constituent pools.'
  iharvop: '`iharvop` selects the harvest operation record in `harvop_db`; the routine reads
    that record''s harvest index override, efficiency, and minimum biomass threshold to control
    the removal calculation.'
locals:
  j: HRU index copied from `jj`; it keys all HRU-level plant, residue, pesticide, and carbon
    state updates.
  k: Loop counter over pesticide constituents in `cs_db%num_pests` while updating pesticide
    masses removed by harvest.
  idp: Plant identifier read from `pcom(j)%plcur(ipl)%idplt`; it is loaded for the selected
    plant but not used later in the extracted source.
  npl: Loop counter over all plants in the community when rebuilding the community total residue
    pool from each plant's `rsd` entry.
  ipl: Plant index copied from `iplant`; it selects the plant-specific pools and growth state
    within HRU `j`.
  clippst: Temporary pesticide mass left in the harvested clippings and transferred to soil
    surface residue.
  yldpst: Temporary pesticide mass associated with the portion removed in the yield calculation
    for the current pesticide constituent.
  hi_tot: Effective harvest index used for this operation, computed as `hi_ovr * harveff`
    and then applied to seed, leaf, and stem masses.
  hi_ovr: Harvest-index target read from the harvest operation database entry; it sets the
    intended fraction of biomass to remove.
  harveff: Harvest efficiency read from the harvest operation database entry; it controls
    how much of the computed yield is actually removed versus left as residue.
  clip: Complement of harvest efficiency (`1. - harveff`); it is used to compute the biomass
    left behind as residue.
  yld_rto: Fraction of total plant mass that is represented by the harvested aboveground yield;
    it is used to partition plant pesticide masses between removed yield and what remains.
uses:
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the plant mass and
    organic-mass types that this routine reads and updates: seed, leaf, stem, total biomass,
    aboveground biomass, residue, harvested yield, and the temporary harvest masses. Without
    those shared state arrays and `organic_mass` fields, the routine could not compute what
    biomass is removed or store the resulting residue and yield quantities.'
  soil_module: '`soil_module` matters because the routine historically interacted with the
    soil surface residue pool, and the lineage evidence shows that logic was refactored into
    `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot`. The imported module remains relevant to
    the harvest/residue pathway even though no current source line in the extracted span references
    it directly.'
  plant_module: '`plant_module` provides the community and plant-status state that determines
    which plant is harvested and how its growth state is reset afterward. The routine reads
    plant identity, pest stress, number of plants in the community, LAI, accumulated heat
    units, and root fraction from `pcom`.'
  plant_data_module: '`plant_data_module` is imported because harvest behavior depends on
    plant database information, especially the mapped plant type and growth characteristics
    that define how the selected plant should respond after biomass removal. The extracted
    source does not show a direct reference to a symbol from this module, so its use is inferred
    from the shared harvest workflow rather than a visible line in the span.'
  mgt_operations_module: '`mgt_operations_module` supplies the harvest operation database
    entry for `iharvop`, including the target harvest index, harvest efficiency, and minimum
    biomass threshold. Those operation settings directly control whether harvest proceeds
    and how much biomass is removed.'
  constituent_mass_module: '`constituent_mass_module` supplies the pesticide-state arrays
    and the count of pesticide constituents. The routine uses them to reduce pesticide mass
    in the harvested plant, compute pesticide retained in clippings, and add that mass to
    the top soil layer.'
  carbon_module: '`carbon_module` matters because the routine records harvested carbon as
    plant carbon removed and surface-residue carbon gained. Those bookkeeping totals are used
    in the model''s carbon accounting after harvest.'
---

<!-- facts:header -->

Harvests aboveground biomass from a plant without killing it, then updates residue, pesticide, carbon, and plant-state bookkeeping for the selected HRU and plant.

## Bottom Line

`mgt_harvbiomass` removes a harvest fraction from seed, leaf, and stem pools for one plant in one HRU, using the harvest operation's target harvest index (`hi_ovr`) and efficiency (`eff`). It then applies pest stress, records harvested carbon, and subtracts the harvested mass from the plant's live biomass pools.

It also moves the unremoved fraction into surface residue, updates total residue for the plant community, adjusts pesticide masses associated with the plant and soil surface, and resets canopy/phenology state after harvest when the plant still has biomass left.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a biomass harvest action is executed for a specific HRU and plant, after the caller has identified the target plant and checked that biomass exceeds the harvest-operation minimum. `actions` and `mgt_sched` both gate the call with `harvop_db(iharvop)%bm_min`, then dispatch `mgt_harvbiomass` for harvest types such as `biomass` and `tree`. Its results feed the plant-residue, pesticide, and carbon balances that later parts of the daily simulation rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. copy indices and harvest settings | Copies the HRU and plant indices into local variables, reads the plant ID, and loads the harvest-operation harvest index override and efficiency for the selected operation. |
| 2. compute target removed biomass | Computes the effective harvest index (`hi_tot`) and uses it to calculate harvested seed, leaf, stem, and total yield mass for the plant. |
| 3. check minimum biomass | Skips the harvest update unless the plant's aboveground biomass remaining after the computed yield is greater than the operation minimum biomass threshold. |
| 4. apply pest stress and carbon bookkeeping | Reduces the harvested yield by pest stress, then adds the harvested carbon to the HRU residue and harvested-plant carbon totals. |
| 5. remove pesticide from plant pools | Loops over each pesticide constituent, estimates the fraction removed with yield, reduces pesticide remaining on and in the plant, caps values at zero, and moves pesticide in clippings to the top soil layer. |
| 6. subtract harvested biomass from plant pools | Subtracts the harvested seed, leaf, stem, total, and aboveground biomass from the plant's live biomass pools. |
| 7. add clippings to residue and rebuild totals | Computes leftover clipping mass as `1 - harveff`, adds it to the plant's surface residue pool, and rebuilds the community total residue by summing each plant's residue pool. |
| 8. reset growth state or zero out the plant | If total plant mass remains above a small threshold, reduces LAI and accumulated heat units and recomputes root fraction; otherwise it zeros total biomass, LAI, and accumulated heat units. |
| 9. close the harvest threshold branch and return | Ends the biomass-threshold conditional and returns to the caller after all plant, residue, pesticide, and carbon bookkeeping is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `pl_mass, pl_yield, harv_seed, harv_leaf, harv_stem, harv_left, orgz` | `pl_mass(j)%seed(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%ab_gr(ipl)%m, pl_yield%m, pl_yield%c, pl_mass(j)%tot(ipl)%m, pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%rsd(ipl), pl_mass(j)%rsd_tot, pl_mass(j)%rsd(npl), pl_mass(j)%root(ipl)%m` |
| [sym:soil_module] | `soil_module` | `soil1(j)%rsd(1)` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%pest_stress, pcom(j)%npl, pcom(j)%plg(ipl)%lai, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%root_frac` |
| [sym:plant_data_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%pest_stress, pcom(j)%npl, pcom(j)%plg(ipl)%lai, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%root_frac` |
| [sym:mgt_operations_module] | `harvop_db` | `harvop_db(iharvop)%hi_ovr, harvop_db(iharvop)%eff, harvop_db(iharvop)%bm_min` |
| [sym:constituent_mass_module] | `cs_db, cs_pl, cs_soil` | `cs_db%num_pests, cs_pl(j)%pl_in(ipl)%pest(k), cs_pl(j)%pl_on(ipl)%pest(k), cs_soil(j)%ly(1)%pest(k)` |
| [sym:carbon_module] | `hrc_d, hpc_d` | `hrc_d(j)%plant_surf_c, hpc_d(j)%harv_abgr_c` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `harv_seed` | When the biomass-harvest branch runs and the plant still has biomass above the minimum threshold. | `harv_seed` stores the seed mass removed by the harvest operation so the routine can subtract it from the plant's seed pool and include it in the harvested yield bookkeeping. |
| `harv_leaf` | When the biomass-harvest branch runs and the plant still has biomass above the minimum threshold. | `harv_leaf` stores the leaf mass removed by the harvest operation so it can be removed from the plant and counted in the harvested yield. |
| `harv_stem` | When the biomass-harvest branch runs and the plant still has biomass above the minimum threshold. | `harv_stem` stores the stem mass removed by the harvest operation so it can be subtracted from the live stem pool and included in yield. |
| `pl_yield` | When the biomass-harvest branch runs and pest stress is applied to the computed harvest mass. | `pl_yield` is the harvested aboveground biomass after operation settings and pest stress; it is what gets removed from the plant and partly left behind as residue. |
| `hrc_d(j)%plant_surf_c` | When harvest succeeds and harvested carbon is accounted for. | `hrc_d(j)%plant_surf_c` is incremented by the carbon contained in the harvested biomass so surface-residue carbon bookkeeping reflects the harvest event. |
| `hpc_d(j)%harv_abgr_c` | When harvest succeeds and harvested carbon is accounted for. | `hpc_d(j)%harv_abgr_c` is incremented by the carbon removed in aboveground harvest so plant carbon-loss totals track the event. |
| `cs_pl(j)%pl_in(ipl)%pest(k)` | For each pesticide constituent during a successful harvest. | `cs_pl(j)%pl_in(ipl)%pest(k)` is reduced to remove the portion of internal plant pesticide that leaves with the harvested biomass. |
| `cs_pl(j)%pl_on(ipl)%pest(k)` | For each pesticide constituent during a successful harvest. | `cs_pl(j)%pl_on(ipl)%pest(k)` is reduced to remove the portion of pesticide on the plant surface that leaves with the harvested biomass. |
| `cs_soil(j)%ly(1)%pest(k)` | For each pesticide constituent during a successful harvest. | `cs_soil(j)%ly(1)%pest(k)` gains the pesticide mass that remains in clippings and is deposited on the soil surface layer. |
| `pl_mass(j)%seed(ipl)` | When harvest succeeds. | `pl_mass(j)%seed(ipl)` is decreased by the harvested seed mass so the plant's seed pool reflects the removed yield. |
| `pl_mass(j)%leaf(ipl)` | When harvest succeeds. | `pl_mass(j)%leaf(ipl)` is decreased by the harvested leaf mass so the live leaf pool reflects the removed yield. |
| `pl_mass(j)%stem(ipl)` | When harvest succeeds. | `pl_mass(j)%stem(ipl)` is decreased by the harvested stem mass so the live stem pool reflects the removed yield. |
| `pl_mass(j)%tot(ipl)` | When harvest succeeds. | `pl_mass(j)%tot(ipl)` is decreased by the harvested total biomass so the plant's total biomass matches the postharvest state. |
| `pl_mass(j)%ab_gr(ipl)` | When harvest succeeds. | `pl_mass(j)%ab_gr(ipl)` is decreased by the harvested aboveground biomass so the aboveground pool matches the postharvest state. |
| `harv_left` | When harvest succeeds; it is computed from the unremoved fraction of `pl_yield`. | `harv_left` is the biomass left behind by incomplete harvest and is added to the plant's surface residue pool. |
| `pl_mass(j)%rsd(ipl)` | When harvest succeeds. | `pl_mass(j)%rsd(ipl)` increases by `harv_left`, representing the residue deposited on the soil surface for this plant. |
| `pl_mass(j)%rsd_tot` | When harvest succeeds. | `pl_mass(j)%rsd_tot` is rebuilt as the sum of all plant residue pools in the community, updating the community-level surface residue total. |
| `pcom(j)%plg(ipl)%lai` | When postharvest total biomass remains above `0.001`. | `pcom(j)%plg(ipl)%lai` is reduced in proportion to harvest intensity to represent canopy loss after biomass removal. |
| `pcom(j)%plcur(ipl)%phuacc` | When postharvest total biomass remains above `0.001`. | `pcom(j)%plcur(ipl)%phuacc` is reduced in proportion to harvest intensity so phenological progress reflects the partial harvest. |
| `pcom(j)%plg(ipl)%root_frac` | When postharvest total biomass remains above `0.001`. | `pcom(j)%plg(ipl)%root_frac` is recomputed from root mass divided by total biomass, keeping the plant's root allocation consistent after harvest. |
| `pl_mass(j)%tot(ipl)%m` | When postharvest total biomass is not above `0.001`. | `pl_mass(j)%tot(ipl)%m` is forced to zero to represent a plant effectively reduced to no remaining biomass after harvest. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:3.3.3 | Harvest-index override at harvest | $HI_{act}=HI_{trg}$ | The harvest operation can impose hi_ovr directly at harvest; the effective removed fraction is hi_tot = hi_ovr*harveff. |
| 5:3.3.5 | Residue left by incomplete harvest | $\Delta rsd=yld*(1-harv_{eff})$ | Unharvested clippings are harv_left = (1-harveff)*pl_yield and are added to the residue pool. |
| 5:3.3.6 | Surface residue update after harvest | $rsd_{surf,i}=rsd_{surf,i-1}+\Delta rsd$ | The leftover harvested biomass is added to pl_mass%rsd and rolled into the total surface residue pool rsd_tot. |

## Lineage

Resolved lineage commits show three behavior changes in this routine: 94b6dec initially added the procedure with harvest of seed, leaf, and stem, pest-stress adjustment, and carbon bookkeeping; eb22103 changed the carbon state targets to `hrc_d(j)%plant_surf_c` and `hpc_d(j)%harv_abgr_c` and moved clipping residue from the older soil residue structure to `soil1(j)%rsd(1)`; 3bb22ed simplified the yield calculation to one summed expression and removed `harveff` from the pest-stress multiplication; 59786e0 added the minimum biomass guard around the harvest logic; 72206bc changed the clipping destination from soil residue to `pl_mass(j)%rsd(ipl)` and added a loop to rebuild `pl_mass(j)%rsd_tot` from all plant residue pools.

- Initial procedure introduction established aboveground biomass harvest without plant kill, with seed/leaf/stem removal, pest-stress adjustment, and carbon tracking.
- Carbon accounting was retargeted to the current residue and harvest carbon fields, and clipping residue handling moved away from the older soil residue structure.
- Yield computation was consolidated and the pest-stress scaling was decoupled from harvest efficiency.
- A minimum biomass threshold was added so harvest only proceeds when enough aboveground mass remains.
- Clipping residue now accumulates in the plant residue pool and the community residue total is explicitly rebuilt from all plant residue pools.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_harvbiomass' has no extracted documentation comment.
- algorithm_steps revised: merged the original harvest-threshold branch into a nine-step source-ordered sequence to reflect the visible control flow and include the final return path.
- `plant_data_module` is imported but no direct symbol from it appears in the extracted source span; its relevance is inferred from the shared harvest workflow and may be uncertain.
- `soil_module` is imported but no current extracted line references a soil symbol from it; lineage evidence shows earlier residue handling through the soil residue structure, so the module remains contextually relevant.
