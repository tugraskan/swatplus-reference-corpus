---
kind: procedure
symbol: pest_decay
title: pest_decay
status: filled
source_hash: f601ea09cb364cbb
version_label: SWAT+ 62.0.0
locals:
  j: Loop index for the plant count within the current HRU when processing foliar pesticide
    decay and metabolite redistribution.
  k: Sequential pesticide index in the HRU constituent-mass arrays; identifies the parent
    pesticide being updated.
  ipl: Index of the plant in the HRU plant community being checked for pesticide on foliage.
  ipest_db: Database index for the current parent pesticide, taken from `cs_db%pest_num(k)`
    and used to read decay factors and metabolite definitions.
  l: Soil layer index within the current HRU profile while updating pesticide in soil.
  ipseq: Sequential basin-pesticide index for a daughter or metabolite pesticide being credited
    with decayed mass.
  ipdb: Database index for the daughter pesticide associated with `ipseq`; used to fetch the
    daughter molecular weight.
  imeta: Metabolite counter that walks through the configured daughter list for the current
    parent pesticide.
  mol_wt_rto: Molecular-weight ratio used to convert parent mass loss into equivalent daughter
    pesticide mass.
  pest_init: Pesticide mass at the start of the current layer or plant update; the amount
    subject to decay.
  pest_end: Remaining pesticide mass after applying the daily decay factor.
  pst_decay: Mass lost from one soil layer after applying soil decay; used as the parent contribution
    to metabolites.
  pst_decay_s: Accumulated soil decay across all layers for the current parent pesticide;
    stored in the output balance.
  metab_decay: Mass assigned to a specific daughter pesticide from one decay event after applying
    the daughter fraction and molecular-weight ratio.
uses:
  pesticide_data_module: This module supplies the parent pesticide decay multipliers and the
    daughter-metabolite routing data. `decay_s` and `decay_f` scale the parent mass, `num_metab`
    and `daughter(imeta)%num` determine which metabolites receive mass, `soil_fr` provides
    the fraction sent to each daughter, and the molecular weights are needed to convert parent
    mass loss to equivalent daughter mass.
  hru_module: '`ihru` selects the active HRU whose soil layers and plant communities are being
    updated. The routine copies it into `j` so the decay calculations and balance outputs
    are written to the correct HRU slot.'
  constituent_mass_module: This module holds the simulated pesticide inventory and the storage
    locations that are modified by decay. `cs_db` maps sequential pesticide IDs to database
    IDs, while `cs_soil` and `cs_pl` contain the soil-layer and plant-foliage masses that
    are reduced and augmented during metabolite formation.
  soil_module: '`soil(j)%nly` controls how many soil layers must be traversed for the current
    HRU. The decay update is layer-by-layer, so the soil profile definition determines the
    extent of the soil loop.'
  plant_module: '`pcom(j)%npl` determines how many plants exist in the current HRU community
    and therefore how many foliage masses must be checked for decay and metabolite creation.'
  output_ls_pesticide_module: This module stores the HRU-level pesticide balance diagnostics
    updated by the routine. The decay and metabolite accumulators it holds are the bookkeeping
    outputs that report how much parent pesticide was lost and how much daughter mass was
    produced on soil and foliage.
---

<!-- facts:header -->

Calculates daily pesticide degradation in HRU soil layers and on plant foliage, including transfer of degraded mass to daughter metabolites.

## Bottom Line

`pest_decay` updates pesticide mass after one day of decay for the current HRU. It loops over each simulated pesticide, reduces its soil and foliar mass by the precomputed daily decay factors, and routes the lost mass into daughter pesticide pools using the configured metabolite fractions and molecular-weight ratios.

It matters because it keeps the constituent-mass state and the pesticide-balance output state synchronized before later routines move pesticides through the soil profile. The routine runs after pesticide uptake and before pesticide leaching, so downstream transport and summary accounting see the already-decayed amounts.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the HRU control sequence after pesticide washoff and pesticide uptake, and before pesticide leaching and soil-total accounting. `hru_control` prepares the active HRU context by setting `ihru` and then calls `pest_decay`; later behavior in `pest_lch` and `pest_soil_tot` depends on the updated parent and daughter masses produced here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. return if no pesticides are simulated | If the constituent database says no pesticides are active, the routine exits immediately because there is nothing to decay or redistribute. |
| 2. loop over each simulated pesticide | For each sequential pesticide in the current HRU, the routine clears the parent decay totals and resolves the matching pesticide database index used to fetch decay factors and daughter definitions. |
| 3. gate on a valid database pesticide | Only pesticides that map to a valid database entry are processed; invalid sequence mappings are ignored. |
| 4. loop through soil layers | Walk each soil layer in the current HRU and read the parent pesticide mass stored in that layer. |
| 5. apply soil decay and record loss | When layer mass is positive, reduce it by the daily soil decay factor, store the remaining mass back into the soil layer, and accumulate the lost amount into the HRU soil-decay balance. |
| 6. distribute soil decay to daughters | For each configured metabolite, use the daughter sequence number, daughter soil fraction, and molecular-weight ratio to convert the parent loss into metabolite mass and add it to both the metabolite balance and the daughter's soil mass pool. |
| 7. store total soil decay for the parent | After all layers are processed, write the accumulated soil decay total into the pesticide-balance output for the parent pesticide. |
| 8. loop through plants on the HRU | Visit each plant in the current HRU community and read the parent pesticide mass on foliage. |
| 9. apply foliar decay and record loss | When foliar mass is positive, reduce it by the daily foliar decay factor, store the remaining mass back on the plant, and record the parent foliar loss in the balance output. |
| 10. distribute foliar decay to daughters | For each metabolite, convert the foliar parent loss into daughter mass using the configured metabolite fraction and molecular-weight ratio, then add that mass to the daughter's foliar balance and foliar mass pool. |
| 11. finish the routine | Return to the caller once all pesticide, soil, and plant updates have been completed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:pesticide_data_module] | `pestcp, pestdb` | `pestcp(ipest_db)%decay_s, pestcp(ipest_db)%num_metab, pestcp(ipest_db)%daughter(imeta)%num, pestdb(ipdb)%mol_wt, pestdb(ipest_db)%mol_wt, pestcp(ipest_db)%daughter(imeta)%soil_fr, pestcp(ipest_db)%decay_f` |
| [sym:hru_module] | `ihru` |  |
| [sym:constituent_mass_module] | `cs_db, cs_soil, cs_pl` | `cs_db%num_pests, cs_db%pest_num(k), cs_soil(j)%ly(l)%pest(k), cs_db%pest_num(ipseq), cs_soil(j)%ly(l)%pest(ipseq), cs_pl(j)%pl_on(ipl)%pest(k), cs_pl(j)%pl_on(ipl)%pest(ipseq)` |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(k)%decay_s, hpestb_d(j)%pest(k)%decay_f, hpestb_d(j)%pest(ipseq)%metab_s, hpestb_d(j)%pest(ipseq)%metab_f` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpestb_d(j)%pest(k)%decay_s` | For each simulated pesticide with a valid database mapping, after all soil layers are processed. | Stores the total mass removed from that parent pesticide across all soil layers during the current day so the HRU pesticide balance can report soil decay. |
| `hpestb_d(j)%pest(k)%decay_f` | For each simulated pesticide with a valid database mapping, when a soil layer has positive parent mass. | Stores the total mass removed from that parent pesticide on foliage across all plants during the current day so the HRU pesticide balance can report foliar decay. |
| `cs_soil(j)%ly(l)%pest(k)` | For each soil layer with positive parent mass and a valid pesticide mapping. | Replaces the parent pesticide mass in that soil layer with the decayed end-of-day mass after applying the soil decay factor. |
| `hpestb_d(j)%pest(ipseq)%metab_s` | For each soil layer with positive parent mass, inside the metabolite loop. | Accumulates metabolite mass produced from soil decay of the parent pesticide and credits it to the daughter pesticide's soil-balance output. |
| `cs_soil(j)%ly(l)%pest(ipseq)` | For each soil layer with positive parent mass, inside the metabolite loop. | Adds the metabolite mass generated from soil decay into the daughter pesticide's soil-layer mass pool. |
| `cs_pl(j)%pl_on(ipl)%pest(k)` | For each plant with positive parent foliage mass and a valid pesticide mapping. | Replaces the parent pesticide mass on foliage with the decayed end-of-day mass after applying the foliar decay factor. |
| `hpestb_d(j)%pest(ipseq)%metab_f` | For each plant with positive parent foliage mass, inside the metabolite loop. | Accumulates metabolite mass produced from foliar decay of the parent pesticide and credits it to the daughter pesticide's foliar-balance output. |
| `cs_pl(j)%pl_on(ipl)%pest(ipseq)` | For each plant with positive parent foliage mass, inside the metabolite loop. | Adds the metabolite mass generated from foliar decay into the daughter pesticide's foliage mass pool. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:3.2.1 | Pesticide degradation in soil (exponential decay) | $pst_{s,ly,t}=pst_{s,ly,o}*exp\lfloor-k_{p,soil}*t\rfloor$ | Verified against SWAT+ 62.0.0 (pest_decay.f90:45). pest_end = pest_init*decay_s` — soil pesticide degradation |
| 3:3.2.3 | Pesticide degradation on plant foliage | $pst_{f,t}=pst_{f,o}*exp\lfloor-k_{p,foliar}*t\rfloor$ | Verified against SWAT+ 62.0.0 (pest_decay.f90:67). pest_end = pest_init*decay_f` — foliar degradation |

## Lineage

Source-backed lineage resolved for four commits. The initial Bitbucket import (`94b6dec`) brought in the full `pest_decay` routine and its soil/foliar degradation logic. `2405a68` added the `pst_decay_f` accumulator, changed foliar metabolite handling to use the incremental `metab_decay` amount, and wrote the foliar total back to `hpestb_d(j)%pest(k)%decay_f`. `39fabde` initialized local variables, corrected comments, and changed the zero-mass thresholds from `1.e-12` to `0.`. `889136d` and the later comment-only change `d81f796` corrected typo-only variable comments without changing behavior.

- 94b6dec established the core daily pesticide decay workflow for soil and foliage, including parent mass reduction and daughter mass redistribution.
- 2405a68 changed foliar bookkeeping so daughter transfers use the incremental decay amount and the parent foliar decay total is accumulated explicitly before being stored.
- 39fabde made the routine initialize all locals and treat any positive mass as eligible for decay by replacing the previous nonzero threshold with `0.` checks.
- 889136d and d81f796 only corrected variable-comment typos; they did not change runtime behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pest_decay' has no extracted documentation comment.
- algorithm_steps revised: consolidated the nested soil and foliar metabolite handling into 11 steps to match the visible control flow and cited only line numbers present in the source block.
- Source evidence shows the foliar daughter fraction field is `soil_fr` in the current routine, even though the commit diff in `2405a68` mentions `foliar_fr`; the source block is the authoritative basis used here.
