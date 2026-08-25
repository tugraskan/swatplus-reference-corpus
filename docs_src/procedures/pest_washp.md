---
kind: procedure
symbol: pest_washp
title: pest_washp
status: filled
source_hash: f8ad7838f5d72c81
version_label: SWAT+ 62.0.0
locals:
  j: HRU index for the current call. It is set from `ihru` and used to select the active HRU’s
    plant, soil, and balance arrays.
  k: Loop index over pesticide entries in `cs_db`. Each `k` identifies one simulated pesticide
    whose mass on plants may be washed off.
  ipl: Loop index over plants in the current HRU’s plant community. It steps through each
    plant that can hold foliar pesticide mass.
  ipest_db: Database index for the current pesticide, taken from `cs_db%pest_num(k)`. It is
    used to look up the pesticide’s wash-off fraction in `pestdb`.
  pest_soil: Temporary amount of pesticide moved from foliage to soil for the current plant
    and pesticide. It is computed from the wash-off fraction and then capped so it cannot
    exceed the pesticide mass available on the plant.
uses:
  pesticide_data_module: The pesticide database provides the wash-off fraction `pestdb(ipest_db)%washoff`,
    which is the key parameter that converts foliage pesticide mass into the amount washed
    to soil.
  output_ls_pesticide_module: This balance structure stores the amount washed off as `hpestb_d(j)%pest(k)%wash`,
    so the routine can report pesticide wash-off in the HRU pesticide budget.
  hru_module: '`ihru` identifies which HRU’s plant, soil, and balance arrays should be updated
    during this call.'
  soil_module: The soil constituent-mass arrays hold the receiving pool for washed-off pesticide.
    `cs_soil(j)%ly(1)%pest(k)` is increased because wash-off deposits pesticide into the top
    soil layer.
  constituent_mass_module: 'The constituent-mass module supplies the simulated pesticide inventory
    and the plant/soil storage locations that this routine reads and updates: the number of
    pesticides, the pesticide database index mapping, the plant-on-foliage mass, and the soil-layer
    mass.'
  plant_module: The plant community defines how many plants exist in the current HRU through
    `pcom(j)%npl`, which controls the inner loop over foliage pesticide masses.
---

<!-- facts:header -->

Moves pesticide wash-off from plant foliage to the soil pool for the current HRU.

The routine loops over simulated pesticides and plants, computes the washed-off fraction from pesticide-specific database data, updates plant and soil pesticide mass, and records the wash-off balance for output.

## Bottom Line

This routine runs during HRU daily processing when rainfall is large enough to trigger pesticide wash-off. It transfers a fraction of pesticide mass from each plant’s on-foliage pool to the top soil layer, using the pesticide-specific wash-off coefficient from the pesticide database.

It also writes the washed-off amount into the pesticide balance output structure so SWAT+ can report how much pesticide left foliage by wash-off. The routine does not read or write files directly; it updates in-memory state used by later pesticide transport and output routines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `hru_control` after rainfall is checked for a wash-off event (`w%precip >= 2.54`). `hru_control` prepares the active HRU context through `ihru` and the plant/soil constituent state, then `pest_washp` updates the pesticide pools before later pesticide routines such as uptake, decay, and soil movement use the revised masses.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. guard | If no pesticides are being simulated (`cs_db%num_pests == 0`), the routine exits immediately because there is nothing to wash off. |
| 2. pesticide loop | Loop over each simulated pesticide and map the simulation index `k` to the pesticide database index `ipest_db`. |
| 3. plant loop | For each pesticide, loop over every plant in the current HRU’s plant community so wash-off can be applied to each foliage pool. |
| 4. foliage presence test | Only process plants whose on-foliage pesticide mass is nonnegative; this avoids acting on missing or inactive pesticide state. |
| 5. database lookup test | Only continue when the pesticide has a valid database entry, because the wash-off fraction must come from `pestdb(ipest_db)%washoff`. |
| 6. compute and limit wash-off | Compute wash-off as the database fraction times the foliage mass, then cap it so the removed amount cannot exceed the pesticide currently on the plant. |
| 7. transfer mass | Add the washed-off pesticide to the top soil layer, subtract the same amount from the plant’s on-foliage pool, and record the amount in the wash-off balance output. |
| 8. return | Exit after all pesticide and plant pools have been updated for this HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:pesticide_data_module] | `pestdb` | `pestdb(ipest_db)%washoff` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(k)%wash` |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `cs_soil` | `cs_soil(j)%ly(1)%pest(k)` |
| [sym:constituent_mass_module] | `cs_db, cs_pl, cs_soil` | `cs_db%num_pests, cs_db%pest_num(k), cs_pl(j)%pl_on(ipl)%pest(k), cs_soil(j)%ly(1)%pest(k)` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(j)%ly(1)%pest(k)` | When a pesticide is active on a plant and the computed wash-off amount is positive (`ipest_db > 0` and `cs_pl(j)%pl_on(ipl)%pest(k) >= 0.`). | `cs_soil(j)%ly(1)%pest(k)` increases by the washed-off mass, representing pesticide deposited from foliage into the surface soil layer. |
| `cs_pl(j)%pl_on(ipl)%pest(k)` | When a pesticide is active on a plant and wash-off is computed for that plant-pesticide combination. | `cs_pl(j)%pl_on(ipl)%pest(k)` is reduced by the amount washed off so the foliage pool no longer contains the transferred pesticide mass. |
| `hpestb_d(j)%pest(k)%wash` | When a valid pesticide database entry exists and wash-off is computed for the current plant and pesticide. | `hpestb_d(j)%pest(k)%wash` records the washed-off mass for pesticide balance reporting in the current HRU. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:3.1.1 | Pesticide wash-off from plant foliage | $pst_{f,wsh}=fr_{wsh}*pst_f$ | pest_soil=washoff*pl_pest; exact match for pst_f_wsh=fr_wsh*pst_f with washoff=fr_wsh. |

## Lineage

Resolved lineage shows the routine was added in df07e3f with the full initial implementation. Later 2405a68 initialized `hpestb_d(j)%pest(k)%wash` to zero before the plant loop and changed the accumulator so wash-off could be summed. c639a8c reverted that accumulation change, restoring a single assignment. 4d173cc then changed the foliage threshold from 0.0001 to 0.0, and 39fabde initialized the local loop/index variables and `pest_soil` to zero.

- df07e3f introduced the wash-off transfer: it reads the pesticide wash-off fraction, moves mass from foliage to top soil, and records the wash-off balance.
- 2405a68 added a per-pesticide balance reset and changed `hpestb_d(j)%pest(k)%wash` to accumulate wash-off across plants.
- c639a8c removed the balance reset and reverted `hpestb_d(j)%pest(k)%wash` back to a single assignment of the current wash-off amount.
- 4d173cc broadened processing by lowering the foliage-mass threshold from 0.0001 to 0.0.
- 39fabde changed local variable initialization so `j`, `k`, `ipl`, `ipest_db`, and `pest_soil` start at zero.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pest_washp' has no extracted documentation comment.
