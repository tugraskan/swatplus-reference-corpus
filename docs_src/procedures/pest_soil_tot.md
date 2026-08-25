---
kind: procedure
symbol: pest_soil_tot
title: pest_soil_tot
status: filled
source_hash: 4deb4378b7dc0c89
version_label: SWAT+ 62.0.0
locals:
  j: '`j` holds the current HRU index. The routine copies `ihru` into `j` and then uses `j`
    to read plant, soil, constituent-mass, and output-balance arrays for that HRU.'
  k: '`k` is the pesticide index. The routine loops over `1..cs_db%num_pests` so it can compute
    a separate balance record for each simulated pesticide.'
  ly: '`ly` is the soil-layer index. It is used to sum pesticide mass across all soil layers
    in the current HRU.'
  ipl: '`ipl` is the plant-community member index. It is used to accumulate pesticide mass
    associated with each plant in the HRU community.'
uses:
  pesticide_data_module: This module is listed as a dependency, but no specific symbols from
    it were resolved in the extracted references. It still matters because the routine’s pesticide
    calculations depend on pesticide-domain data being available through the module state.
  hru_module: hru_module provides `ihru`, the active HRU number. The routine copies that index
    into `j` so it can look up the correct HRU entries in plant, soil, constituent-mass, and
    output-balance arrays.
  soil_module: soil_module provides the HRU soil profile, especially `soil(j)%nly`. That layer
    count controls how many soil layers are summed when building the total soil pesticide
    balance.
  constituent_mass_module: constituent_mass_module holds the simulated pesticide counts and
    the per-HRU mass arrays. `cs_db%num_pests` sets the pesticide loop bounds, while `cs_pl`
    and `cs_soil` provide the plant- and soil-resident pesticide masses that are aggregated
    here.
  output_ls_pesticide_module: output_ls_pesticide_module defines the destination balance structure
    `hpestb_d`. This routine writes the aggregated pesticide totals into `hpestb_d(j)%pest(k)`
    so other output and reporting code can use daily HRU pesticide balances.
  plant_module: plant_module provides `pcom(j)%npl`, the number of plants in the current HRU
    community. That count determines how many plant entries must be summed when building the
    foliage and in-plant pesticide totals.
---

<!-- facts:header -->

Summarizes pesticide mass for the current HRU by pesticide, separating foliage, in-plant, and soil pools. The results populate the daily pesticide balance output state used by later runoff and transport reporting.

## Bottom Line

pest_soil_tot is a per-HRU aggregation routine. It uses the current HRU index, the number of simulated pesticides, the number of plants in the community, and the number of soil layers to build pesticide totals for the active HRU.

For each pesticide, it stores pesticide on plant foliage, pesticide in plant tissue, and pesticide in soil into hpestb_d(j)%pest(k). These summary balances are then available to downstream pesticide-output routines after hru_control calls this routine during the HRU pesticide sequence.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the HRU pesticide processing sequence after `pest_decay` and `pest_lch`, as shown by `hru_control` calling it at line 521. It prepares summary pesticide balances for the current HRU, and later pesticide output behavior such as runoff and sediment-related reporting depends on those totals being populated before the subsequent calls to `pest_enrsb` and `pest_pesty`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set HRU index | Copies the active HRU number from `ihru` into local index `j` so all subsequent lookups use the current HRU. |
| 2. skip if no pesticides | Returns immediately when `cs_db%num_pests` is zero, because there are no pesticide pools to summarize. |
| 3. loop over pesticides | Iterates through every simulated pesticide type so each pesticide gets its own balance record. |
| 4. sum pesticide on plants | Visits every plant in the HRU community and accumulates pesticide on foliage and in-plant mass into `hpestb_d(j)%pest(k)%plant` and `hpestb_d(j)%pest(k)%in_plant`. |
| 5. initialize soil total | Sets the soil balance accumulator for the current pesticide to zero before adding soil-layer values. |
| 6. sum pesticide in soil layers | Loops over all soil layers in the HRU and adds `cs_soil(j)%ly(ly)%pest(k)` into the soil balance total. |
| 7. finish pesticide loop | After all plant and soil contributions are collected for one pesticide, control returns to the outer pesticide loop for the next type. |
| 8. return | Returns to the caller after all pesticide balance fields have been updated for the current HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:pesticide_data_module] | `pesticide_data_module state` | `pesticide_data_module` |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:constituent_mass_module] | `cs_db, cs_pl, cs_soil` | `cs_db%num_pests, cs_pl(j)%pl_on(ipl)%pest(k), cs_pl(j)%pl_in(ipl)%pest(k), cs_soil(j)%ly(ly)%pest(k)` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(k)%plant, hpestb_d(j)%pest(k)%in_plant, hpestb_d(j)%pest(k)%soil` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpestb_d(j)%pest(k)%plant` | When `cs_db%num_pests > 0`, inside the loop over `k = 1, cs_db%num_pests` and `ipl = 1, pcom(j)%npl`. | `hpestb_d(j)%pest(k)%plant` is overwritten with the summed pesticide-on-plant value for the current HRU and pesticide. It represents the foliage-associated pesticide balance that downstream output routines can report. |
| `hpestb_d(j)%pest(k)%in_plant` | When `cs_db%num_pests > 0`, inside the loop over `k = 1, cs_db%num_pests` and `ipl = 1, pcom(j)%npl`. | `hpestb_d(j)%pest(k)%in_plant` is overwritten with the summed pesticide-in-plant value for the current HRU and pesticide. It represents pesticide held within plant tissue for later balance and output reporting. |
| `hpestb_d(j)%pest(k)%soil` | When `cs_db%num_pests > 0`, after `hpestb_d(j)%pest(k)%soil = 0.` and while looping over `ly = 1, soil(j)%nly`. | `hpestb_d(j)%pest(k)%soil` becomes the total pesticide mass in the HRU soil profile for pesticide `k`, summed across all soil layers. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source states for `pest_soil_tot`. The procedure was added in df07e3f as a new subroutine that summed plant and soil pesticide pools. c639a8c temporarily changed the plant balance logic to assign the last plant’s value rather than a sum. 2405a68 restored accumulation and also zeroed the plant balance fields before summing. 39fabde then initialized the local loop variables `j`, `k`, `ly`, and `ipl` to zero without changing the balance formulas.

- df07e3f introduced the new `pest_soil_tot` routine and its original loop structure for summing pesticide-on-plant and pesticide-in-soil pools into `hpestb_d`.
- c639a8c changed the plant and in-plant assignments from cumulative addition to simple overwrite with each plant entry, altering the meaning of the plant totals until it was reverted.
- 2405a68 restored cumulative summation for `hpestb_d(j)%pest(k)%plant` and `hpestb_d(j)%pest(k)%in_plant`, and added explicit zero initialization for those accumulators before the plant loop.
- 39fabde initialized the local loop/index variables to zero at declaration, a non-behavioral change that affects compiler/runtime safety rather than the balance equations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pest_soil_tot' has no extracted documentation comment.
- algorithm_steps revised: expanded the original five-step sketch into eight source-backed steps and split the combined plant/soil work into explicit summation and return phases.
- source extraction did not resolve any direct callees for this subroutine.
