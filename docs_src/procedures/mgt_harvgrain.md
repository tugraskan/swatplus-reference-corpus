---
kind: procedure
symbol: mgt_harvgrain
title: mgt_harvgrain
status: filled
source_hash: 5d2b8d4b6bf77173
version_label: SWAT+ 62.0.0
args:
  jj: Selects the HRU that this harvest is applied to; the routine copies it into local `j`
    and uses it to index the community plant mass, carbon, soil, and pesticide state for that
    HRU.
  iplant: Selects which plant slot within the HRU’s plant community is harvested; the routine
    stores it in the module-level `ipl` index and uses it to access the chosen plant’s status
    and mass arrays.
  iharvop: Selects the harvest operation record that supplies the harvest efficiency `harvop_db(iharvop)%eff`
    for this grain harvest.
locals:
  j: Local HRU index used after copying `jj`; it drives all per-HRU lookups into `pcom`, `pl_mass`,
    `hpc_d`, `soil1`, and `cs_pl`.
  k: Loop counter over pesticide constituents in `cs_db%num_pests`; each pass adjusts the
    plant pesticide masses for one pesticide type.
  harveff: Harvest efficiency read from `harvop_db(iharvop)%eff`; it sets the fraction of
    seed mass removed as grain yield.
  idp: Plant database index taken from `pcom(j)%plcur(ipl)%idplt`; it is used to look up the
    crop’s minimum harvest-index threshold in `pldb(idp)%wsyf`.
  harveff1: Complement of harvest efficiency (`1. - harveff`); it is the fraction of seed
    mass left behind and routed to soil active humus.
  yld_rto: Yield-to-total-biomass ratio for the harvested plant, computed from `pl_yield%m`
    and `pl_mass(j)%tot(ipl)%m`; it scales pesticide removal from the plant.
  yldpst: Temporary amount of pesticide associated with the harvested yield for the current
    pesticide loop iteration; it is computed but not assigned to another state in the extracted
    source.
uses:
  basin_module: '`basin_module` is the source of basin-wide plant community state, and this
    routine needs the current plant status for the chosen HRU/plant pair to enforce the minimum
    harvest index and apply pest stress to harvested yield.'
  hru_module: '`hru_module` provides the shared plant-competition index `ipl`, which this
    routine overwrites with the incoming plant slot so the harvest acts on the correct plant
    within the current HRU.'
  plant_module: '`plant_module` holds the selected plant’s identity, harvest index, and pest
    stress. Those fields determine which crop database record to use and how much of the calculated
    grain yield is actually harvested.'
  plant_data_module: '`plant_data_module` supplies the crop-specific lower bound `wsyf` for
    harvest index. The routine uses it to prevent the plant’s harvest index from dropping
    below the minimum allowed value.'
  mgt_operations_module: '`mgt_operations_module` supplies the harvest operation database
    and its efficiency value. Without `harvop_db(iharvop)%eff`, the routine could not compute
    how much seed becomes harvested grain versus leftover residue.'
  carbon_module: '`carbon_module` provides the HRU carbon accounting record that tracks carbon
    removed in grain or biomass harvest. The routine increments `hpc_d(j)%harv_abgr_c` with
    the carbon contained in the harvested yield.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` contains the plant mass pools,
    soil active humus pool, and yield object that this routine updates. These masses are the
    primary bookkeeping targets for subtracting seed, creating yield, and preserving carbon/mass
    balance.'
  constituent_mass_module: '`constituent_mass_module` holds the pesticide pools on and in
    the plant plus the number of pesticide constituents to process. The harvest routine loops
    over those pests to reduce plant-borne pesticide masses in proportion to the harvested
    fraction.'
---

<!-- facts:header -->

Removes grain from a plant’s biomass after a harvest operation, using the operation’s efficiency and the plant’s minimum harvest index. It updates harvested carbon, residue/humus balance, and pesticide masses tied to the removed grain.

## Bottom Line

`mgt_harvgrain` executes the grain-harvest branch used by management actions. It identifies the active HRU and plant, reads the harvest efficiency and minimum harvest-index threshold, then subtracts seed mass from plant totals and computes the grain yield that leaves the plant system.

The routine also applies pest stress to the harvested yield, accumulates harvested plant carbon for reporting, returns the unharvested fraction of seed mass to the soil active humus pool, zeros the seed pool, and reduces plant pesticide masses in proportion to the harvested fraction. Those updates keep plant, soil, carbon, and pesticide balances consistent after grain removal.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during a management harvest step after the caller has already selected a harvestable HRU, plant slot, and harvest operation type. The upstream caller supplies `jj`, `iplant`, and `iharvop` from the active action or schedule, and later model behavior depends on the updated plant mass pools, soil active humus, carbon harvest totals, and pesticide masses remaining on the plant.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU and plant indices | Copy the incoming HRU index into local `j`, copy the incoming plant-community slot into module-level `ipl`, look up the crop database index `idp` from the current plant status, and read the harvest efficiency from the chosen harvest operation. |
| 2. enforce minimum harvest index | Raise the plant’s harvest index to at least the crop-specific minimum `pldb(idp)%wsyf` so grain harvest cannot reduce it below the allowed floor. |
| 3. remove seed from plant biomass and compute yield | Subtract the seed pool from total and above-ground plant mass, then compute harvested yield as the harvest efficiency times the seed mass. |
| 4. apply pest stress and record harvested carbon | Reduce the harvested yield by plant pest stress and add the carbon in that yield to the HRU harvest-carbon accumulator for reporting. |
| 5. route unharvested seed to soil | Compute the fraction not removed by harvest efficiency and add that leftover seed mass to the soil active humus pool `soil1(j)%hact(1)` to preserve mass balance. |
| 6. clear the seed pool | Reset the plant’s seed mass pool to the zero organic-mass object after harvest. |
| 7. adjust pesticide masses for each constituent | Loop over all simulated pesticides, compute the yield fraction of total biomass, estimate pesticide removed with the harvested fraction, then reduce both internal and surface plant pesticide masses and clip them at zero. |
| 8. return to caller | Finish the harvest update and return control to the management routine that requested the grain harvest. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%harv_idx, pcom(j)%plcur(ipl)%pest_stress` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%harv_idx, pcom(j)%plcur(ipl)%pest_stress` |
| [sym:hru_module] | `ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%harv_idx, pcom(j)%plcur(ipl)%pest_stress` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%wsyf` |
| [sym:mgt_operations_module] | `harvop_db` | `harvop_db(iharvop)%eff` |
| [sym:carbon_module] | `hpc_d` | `hpc_d(j)%harv_abgr_c` |
| [sym:organic_mineral_mass_module] | `pl_mass, pl_yield, soil1, plt_mass_z` | `pl_mass(j)%tot(ipl), pl_mass(j)%seed(ipl), pl_mass(j)%ab_gr(ipl), pl_yield%c, soil1(j)%hact(1), pl_yield%m, pl_mass(j)%tot(ipl)%m` |
| [sym:constituent_mass_module] | `cs_db, cs_pl` | `cs_db%num_pests, cs_pl(j)%pl_in(ipl)%pest(k), cs_pl(j)%pl_on(ipl)%pest(k)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ipl` | On every grain-harvest call after `j = jj` and `ipl = iplant` | The routine stores the current HRU’s plant-community slot in the shared `ipl` index so subsequent plant-mass and pesticide lookups target the selected plant. |
| `pcom(j)%plcur(ipl)%harv_idx` | After loading `idp` and before yield/mass updates | The selected plant’s harvest index is clamped upward to the database minimum `wsyf`, which prevents a harvest from using a lower-than-allowed grain fraction. |
| `pl_mass(j)%tot(ipl)` | When a grain harvest is executed | The total plant mass is reduced by the seed pool so the harvested grain no longer counts as standing biomass. |
| `pl_mass(j)%ab_gr(ipl)` | When a grain harvest is executed | The above-ground mass is reduced by the seed pool so the removed grain is no longer part of the plant’s standing aerial biomass. |
| `pl_yield` | After seed subtraction and pest-stress adjustment | `pl_yield` becomes the actual harvested grain mass object, scaled by harvest efficiency and pest stress; it is then used for carbon accounting and pesticide scaling. |
| `hpc_d(j)%harv_abgr_c` | After yield is computed | The HRU harvest-carbon tally increases by the carbon content of the harvested yield so output summaries reflect grain carbon removal. |
| `soil1(j)%hact(1)` | When the unharvested fraction of seed is routed to soil | The active humus pool gains the leftover seed mass that was not removed by harvest efficiency, preserving the plant-to-soil mass balance. |
| `pl_mass(j)%seed(ipl)` | Immediately after routing residue to soil | The seed pool is cleared because the grain has been harvested out of the plant. |
| `cs_pl(j)%pl_in(ipl)%pest(k)` | For each pesticide `k` from 1 to `cs_db%num_pests` | The internal plant pesticide pool is reduced in proportion to the harvested fraction, then clipped at zero so harvested grain no longer carries the removed amount. |
| `cs_pl(j)%pl_on(ipl)%pest(k)` | For each pesticide `k` from 1 to `cs_db%num_pests` | The surface/on-plant pesticide pool is reduced in proportion to the harvested fraction, then clipped at zero to keep the remaining plant-borne pesticide nonnegative. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:3.3.4 | Actual yield with harvest efficiency | $yld_{act}=yld*harv_{eff}$ | Harvested yield is pl_yield = harveff*seed_mass, then reduced by pest stress if present. |

## Lineage

Resolved lineage commits show three behavior-changing updates to `mgt_harvgrain`: the file was introduced in `df07e3f`, `39fabde` initialized local variables and kept the existing harvest logic, and `eb22103` changed the harvested-carbon accumulator from `hpc_d(j)%harv_c` to `hpc_d(j)%harv_abgr_c`. `35b029c` only adjusted the subroutine end statement formatting.

- `df07e3f` added the full `mgt_harvgrain` routine, including grain yield calculation, seed removal, soil routing, and pesticide adjustment.
- `39fabde` did not change the algorithm; it only initialized local variables and preserved the grain-harvest logic in the source.
- `eb22103` changed harvested-carbon accounting to accumulate grain/above-ground harvest carbon in `hpc_d(j)%harv_abgr_c` instead of the older `hpc_d(j)%harv_c` field.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_harvgrain' has no extracted documentation comment.
