---
kind: procedure
symbol: pest_pl_up
title: pest_pl_up
status: filled
source_hash: 335e56eddd6cdfa3
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects the current land unit whose soil, plant, and
    pesticide state will be updated.
  k: Loop index for the pesticide list in `cs_db`; it identifies which pesticide is being
    processed and which database entry to use.
  ly: Soil-layer loop index; it selects the layer whose pesticide mass and plant water uptake
    are used in the transfer calculation.
  ipl: Plant index within the HRU's plant community; it selects the active plant receiving
    pesticide uptake.
  ipest_db: Cross-reference from the sequential pesticide index `k` to the pesticide database
    entry in `pestdb`; it is used to read the plant-uptake fraction for that pesticide.
  pest_up: Temporary mass variable holding the computed pesticide amount transferred from
    one soil layer into plant uptake before capping and state updates.
uses:
  pesticide_data_module: This module provides the pesticide database entry for the current
    pesticide, and `pl_uptake` is the coefficient that controls how much pesticide can move
    from soil into plants in each layer.
  output_ls_pesticide_module: This module holds the daily HRU pesticide balance array, and
    `hpestb_d(j)%pest(k)%pl_uptake` is the reporting/accounting sink that records total plant
    uptake for each pesticide.
  hru_module: This module supplies `ihru`, which tells the subroutine which HRU's plant, soil,
    and pesticide arrays to update.
  soil_module: This module provides the soil profile size and layer water storage used to
    iterate over layers and normalize uptake by layer water content.
  constituent_mass_module: This module stores the pesticide inventory being tracked in soil
    and plant compartments, plus the pesticide count and database crosswalk that determine
    which indices to loop over and which masses to modify.
  plant_module: This module provides the plant community structure and each plant's layer-by-layer
    water uptake, which is used to apportion pesticide transfer among the active plants and
    soil layers.
---

<!-- facts:header -->

Updates pesticide mass from soil into plants for the current HRU. It moves a fraction of pesticide from each soil layer into each active plant, and records the uptake in the daily pesticide balance.

## Bottom Line

pest_pl_up runs once for the current HRU after pesticide washoff is handled. It loops over every simulated pesticide, then over every plant in the HRU, and for plants that actually carry that pesticide it transfers a small amount from the soil layers into plant tissue using the pesticide's plant-uptake fraction and the plant's layer-by-layer water uptake pattern.

The routine also caps the transfer so it cannot remove more pesticide than is present in a soil layer. It writes the removed mass into `cs_pl(j)%pl_in(ipl)%pest(k)` and accumulates the amount in `hpestb_d(j)%pest(k)%pl_uptake`, so later pesticide accounting and reporting reflect plant uptake.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the HRU daily pesticide sequence after pesticide washoff and before degradation and leaching. `hru_control` prepares the current HRU context via `ihru` and the already-populated plant, soil, and pesticide state arrays; the results then feed later pesticide accounting, especially the subsequent decay and movement routines and the daily balance output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select current HRU | Copies `ihru` into `j` and exits immediately if no pesticides are being simulated. This prevents any plant-uptake work when the pesticide database is empty. |
| 2. loop over pesticides | Walks through each simulated pesticide, maps the sequential pesticide index to the pesticide database number, and clears the daily plant-uptake balance for that pesticide in the current HRU. |
| 3. loop over plants | Checks each plant in the HRU and only continues for plants that actually contain a measurable amount of the current pesticide. It also requires a valid pesticide database entry before any transfer is computed. |
| 4. loop over soil layers | For each soil layer, computes a provisional pesticide transfer using the pesticide's plant-uptake fraction, the plant's water uptake from that layer, the layer water storage, and the pesticide mass already present in that layer. |
| 5. cap transfer to available mass | Limits the provisional transfer so it cannot exceed the pesticide mass present in the source soil layer. |
| 6. move mass from soil to plant | Subtracts the accepted transfer from the soil layer, adds it to plant internal pesticide mass, and accumulates it in the daily HRU pesticide uptake total. |
| 7. finish loops and return | Closes the nested loops and returns to the caller after all pesticides, plants, and layers have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:pesticide_data_module] | `pestdb` | `pestdb(ipest_db)%pl_uptake` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(k)%pl_uptake` |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(ly)%st` |
| [sym:constituent_mass_module] | `cs_db, cs_pl, cs_soil` | `cs_db%num_pests, cs_db%pest_num(k), cs_pl(j)%pl_on(ipl)%pest(k), cs_soil(j)%ly(ly)%pest(k), cs_pl(j)%pl_in(ipl)%pest(k)` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%uptake(ly)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpestb_d(j)%pest(k)%pl_uptake` | When `cs_pl(j)%pl_on(ipl)%pest(k) >= 0.0001`, `ipest_db > 0`, and a soil-layer transfer is computed for the current layer. | `hpestb_d(j)%pest(k)%pl_uptake` is reset for the current pesticide and then incremented by each accepted layer transfer, so it stores the total plant uptake of that pesticide for the HRU on this day. |
| `cs_soil(j)%ly(ly)%pest(k)` | When the routine processes a layer and the computed `pest_up` is accepted for that layer. | `cs_soil(j)%ly(ly)%pest(k)` is reduced by the amount moved into plants, so the soil reservoir reflects pesticide removed by plant uptake. |
| `cs_pl(j)%pl_in(ipl)%pest(k)` | When the routine processes a layer and the computed `pest_up` is accepted for that plant and pesticide. | `cs_pl(j)%pl_in(ipl)%pest(k)` is increased by the transferred mass, so the plant internal pesticide pool reflects uptake from the soil. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved for `pest_pl_up`. The earliest resolved change in 94b6dec added the routine to the imported source snapshot and included the initial plant-uptake logic. 0913193 corrected the soil-layer lookup in the uptake formula from `soil(j)%phys(k)%st` to `soil(j)%phys(ly)%st`. 39fabde initialized the local loop and working variables and cleaned indentation. 1c812c1 kept the uptake formula structure but updated the same denominator to the layer-indexed form in the current history line, confirming the finalized layer-based calculation.

- 94b6dec introduced `pest_pl_up` with daily plant-uptake accumulation from soil into plant tissue.
- 0913193 fixed the uptake formula to use the current layer's soil water storage (`phys(ly)%st`) instead of indexing by pesticide number.
- 39fabde initialized the local indices and working variable (`j`, `k`, `ly`, `ipl`, `ipest_db`, `pest_up`) to zero/0.0 and preserved the pesticide washoff comment cleanup.
- 1c812c1 retained the layer-based uptake computation with `soil(j)%phys(ly)%st`, matching the corrected soil-layer indexing in the current routine.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pest_pl_up' has no extracted documentation comment.
