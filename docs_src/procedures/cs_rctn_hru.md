---
kind: procedure
symbol: cs_rctn_hru
title: cs_rctn_hru
status: filled
source_hash: 4bf78de34cfc7f62
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index. The routine sets `j = ihru` and then uses `j` to read and update the
    active HRU's area, soil profile, constituent masses, nitrate pool, and mass-balance records.
  jj: Soil-layer loop index. It selects the current layer within `soil(j)%nly` so the routine
    can compute layer water volume, concentrations, reaction changes, and updated masses one
    layer at a time.
  n: Loop index over the three reaction species in the Runge-Kutta update. It is used to compute
    the final weighted increment for SeO4, SeO3, and NO3 from the four stored stage slopes
    in `k_rg`.
  conc_old: Vector of starting concentrations for the current layer, one entry each for SeO4,
    SeO3, and NO3 in soil water. It is the base concentration state passed into the reaction-rate
    routine and used to build each Runge-Kutta stage.
  conc_new: Vector of updated layer concentrations after the Runge-Kutta step. The routine
    stores SeO4 and SeO3 back into `cs_soil(j)%ly(jj)%csc`, and uses the NO3 value to update
    `soil1(j)%mn(jj)%no3`.
  conc_rg: Working concentration vector for the current Runge-Kutta stage. Each stage copies
    `conc_old` and then shifts it by the previous slope estimate before calling `se_reactions_soil`.
  k_rg: Array of Runge-Kutta slope results for the four stages and three species. `se_reactions_soil`
    fills it, and this routine combines the four columns to compute `conc_new`.
  phi_value: Weighted Runge-Kutta increment for each species. The routine computes it from
    the four stage slopes and then adds it to `conc_old` to form `conc_new`.
  hru_area_m2: HRU area converted from hectares to square meters. It is used to turn layer
    water depth into layer water volume and to convert between concentration and mass units.
  water_volume: Liquid water volume in the current soil layer, in cubic meters. It is the
    denominator for concentration calculations and the scale factor used when converting updated
    concentrations back to kg/ha.
  mass_seo4_before: Running total of SeO4 mass across all soil layers before reactions, in
    kg/ha. It is used to compute the HRU-level reaction mass balance after the layer loop
    finishes.
  mass_seo3_before: Running total of SeO3 mass across all soil layers before reactions, in
    kg/ha. It is used to compute the HRU-level reaction mass balance after the layer loop
    finishes.
  mass_seo4_after: Running total of updated SeO4 mass across all soil layers after reactions,
    in kg/ha. It is compared with the pre-reaction total to compute the SeO4 reaction balance.
  mass_seo3_after: Running total of updated SeO3 mass across all soil layers after reactions,
    in kg/ha. It is compared with the pre-reaction total to compute the SeO3 reaction balance.
  cs_mass_kg: Temporary mass converter for one constituent in the current layer. The routine
    uses it to translate kg/ha masses into total kilograms before dividing by water volume
    to get concentration.
  seo4_conc: Current SeO4 concentration in soil water for the active layer, expressed as mg/L.
    It becomes `conc_old(1)` and feeds the selenium reaction calculation.
  seo3_conc: Current SeO3 concentration in soil water for the active layer, expressed as mg/L.
    It becomes `conc_old(2)` and feeds the selenium reaction calculation.
  no3_conc: Current NO3 concentration in soil water for the active layer, expressed as mg/L.
    It becomes `conc_old(3)` and is updated by the same reaction step as the selenium species.
uses:
  hru_module: The HRU module supplies the current HRU record and its index. `hru(j)%area_ha`
    is needed to convert between areal mass units and total layer mass, and `ihru` tells the
    routine which HRU to process.
  constituent_mass_module: The constituent-mass module holds the soil-layer state that this
    routine reads and writes. `cs_soil(j)%ly(jj)%cs(1)`, `cs_soil(j)%ly(jj)%cs(2)`, `cs_soil(j)%ly(jj)%csc(1)`,
    and `cs_soil(j)%ly(jj)%csc(2)` are the SeO4 and SeO3 mass/concentration fields being updated.
  cs_data_module: The constituent-setup data module provides the switch that determines whether
    this routine is called at all. `cs_db%num_cs` gates the constituent-reaction branch in
    `hru_control`, so it controls whether the selenium reaction update runs for the HRU.
  soil_module: The soil module supplies the number of layers and the layer water storage used
    to compute reaction volume. `soil(j)%nly` controls the layer loop, and `soil(j)%phys(jj)%st`
    gives the water stored in each layer for concentration calculations.
  organic_mineral_mass_module: The organic/mineral nitrogen module holds the nitrate pool
    by soil layer. `soil1(j)%mn(jj)%no3` is converted to concentration, passed through the
    same reaction calculation, and written back after the update.
  cs_module: The CS balance module stores the reaction bookkeeping for the HRU. `hcsb_d(j)%cs(1)%rctn`
    and `hcsb_d(j)%cs(2)%rctn` record the net change in SeO4 and SeO3 mass caused by chemical
    reactions.
---

<!-- facts:header -->

Updates selenium and nitrate concentrations in each HRU soil layer using chemical reaction kinetics and a Runge-Kutta integration step.

## Bottom Line

This subroutine loops through the active soil layers in the current HRU, converts layer masses into water concentrations, and then advances SeO4, SeO3, and NO3 through a four-stage Runge-Kutta reaction calculation. It writes the updated concentrations back to the soil constituent stores and converts them back to kg/ha so the rest of SWAT+ can keep using mass-based soil routines.

It also accumulates before-and-after mass totals for SeO4 and SeO3 and stores the resulting reaction balance in `hcsb_d(j)%cs(1)%rctn` and `hcsb_d(j)%cs(2)%rctn`. Those balance terms let later constituent accounting report how much mass moved because of chemical reactions in the soil profile.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` after the model has confirmed there are constituent species to process (`cs_db%num_cs > 0`). `hru_control` supplies the active HRU context through `ihru`, and this routine uses that context to update layer-by-layer reaction concentrations before `cs_sorb_hru` performs sorption and the rest of the HRU water/soil calculations continue.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select HRU and scale area | Uses the current HRU index `ihru`, assigns it to `j`, and converts the HRU area from hectares to square meters for later water-volume and mass conversions. |
| 2. reset mass totals | Initializes the before/after running totals for SeO4 and SeO3 so the routine can compute HRU-level reaction mass balances after processing all layers. |
| 3. loop over soil layers | Processes each soil layer in the active HRU one at a time. |
| 4. compute layer water volume | Uses the layer water storage `soil(j)%phys(jj)%st` and HRU area to calculate the liquid water volume in the current soil layer. |
| 5. derive current concentrations | If the layer contains water, converts SeO4, SeO3, and NO3 masses into soil-water concentrations; otherwise sets all three concentrations to zero. |
| 6. load starting concentrations | Copies the current layer concentrations into `conc_old` so they can serve as the base state for the Runge-Kutta reaction step. |
| 7. accumulate pre-reaction mass | Adds the layer masses for SeO4 and SeO3 to the running before-reaction totals. |
| 8. run K1 reaction slope | Initializes `conc_rg` with the starting concentrations and calls `se_reactions_soil` to compute the first Runge-Kutta slope. |
| 9. run K2 reaction slope | Forms the midpoint concentrations from K1 and calls `se_reactions_soil` again to compute the second slope. |
| 10. run K3 reaction slope | Forms the next midpoint concentrations from K2 and calls `se_reactions_soil` to compute the third slope. |
| 11. run K4 reaction slope | Forms the endpoint concentrations from K3 and calls `se_reactions_soil` to compute the fourth slope. |
| 12. combine Runge-Kutta increments | For SeO4, SeO3, and NO3, computes the weighted Runge-Kutta increment in `phi_value` and adds it to `conc_old` to produce `conc_new`. |
| 13. store updated layer state | Writes the new SeO4 and SeO3 concentrations back to `cs_soil(... )%csc`, converts the updated concentrations to kg/ha for `cs_soil(... )%cs`, and updates `soil1(... )%mn(... )%no3` from the new nitrate concentration. |
| 14. accumulate post-reaction mass and finish | Adds the updated SeO4 and SeO3 layer masses to the after-reaction totals, stores the HRU reaction balances in `hcsb_d(j)%cs(1)%rctn` and `hcsb_d(j)%cs(2)%rctn`, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru` | `hru(j)%area_ha` |
| [sym:constituent_mass_module] | `cs_soil` | `cs_soil(j)%ly(jj)%cs(1), cs_soil(j)%ly(jj)%cs(2), cs_soil(j)%ly(jj)%csc(1), cs_soil(j)%ly(jj)%csc(2)` |
| [sym:cs_data_module] | `cs_db` | `cs_db%num_cs` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(jj)%st` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(jj)%no3` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(j)%cs(1)%rctn, hcsb_d(j)%cs(2)%rctn` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(j)%ly(jj)%csc(1)` | After the Runge-Kutta update for a layer with nonzero water volume, when the new SeO4 concentration is written back from `conc_new(1)`. | `cs_soil(j)%ly(jj)%csc(1)` becomes the updated SeO4 concentration in the layer water, replacing the pre-reaction concentration so later constituent routines see the reaction-adjusted value. |
| `cs_soil(j)%ly(jj)%csc(2)` | After the Runge-Kutta update for a layer with nonzero water volume, when the new SeO3 concentration is written back from `conc_new(2)`. | `cs_soil(j)%ly(jj)%csc(2)` becomes the updated SeO3 concentration in the layer water, replacing the pre-reaction concentration for later constituent accounting. |
| `cs_soil(j)%ly(jj)%cs(1)` | After the new SeO4 concentration has been stored and the routine converts it back to mass using the current layer water volume. | `cs_soil(j)%ly(jj)%cs(1)` is reset to the updated SeO4 mass per hectare corresponding to the new concentration, so the soil constituent mass state stays consistent with the concentration state. |
| `cs_soil(j)%ly(jj)%cs(2)` | After the new SeO3 concentration has been stored and the routine converts it back to mass using the current layer water volume. | `cs_soil(j)%ly(jj)%cs(2)` is reset to the updated SeO3 mass per hectare corresponding to the new concentration, keeping the mass state aligned with the reaction-updated concentration. |
| `soil1(j)%mn(jj)%no3` | After `conc_new(3)` is computed from the Runge-Kutta reaction update for the current soil layer. | `soil1(j)%mn(jj)%no3` is updated to the new nitrate mass per hectare implied by the reaction-adjusted concentration, so the mineral nitrogen pool reflects the same chemistry used for selenium. |
| `hcsb_d(j)%cs(1)%rctn` | After all soil layers have been processed and the routine has accumulated the before/after SeO4 totals. | `hcsb_d(j)%cs(1)%rctn` stores the net SeO4 mass change caused by chemical reactions in the HRU soil profile, which is used for CS mass-balance reporting. |
| `hcsb_d(j)%cs(2)%rctn` | After all soil layers have been processed and the routine has accumulated the before/after SeO3 totals. | `hcsb_d(j)%cs(2)%rctn` stores the net SeO3 mass change caused by chemical reactions in the HRU soil profile, which is used for CS mass-balance reporting. |

## File I/O

<!-- facts:io -->


## Lineage

`cs_rctn_hru.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cs_rctn_hru.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_rctn_hru' has no extracted documentation comment.
- algorithm_steps revised: merged the raw source flow into 14 explicit model steps while keeping only line-number citations visible in the source block.
- cs_data_module ownership is uncertain from the extracted references; the routine uses `cs_db%num_cs` through the broader constituent setup, but no direct candidate reference to `cs_db` was separately resolved in the packet.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
