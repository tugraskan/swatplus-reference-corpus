---
kind: procedure
symbol: ero_ovrsed
title: ero_ovrsed
status: filled
source_hash: f6bc6b9f484f1722
version_label: SWAT+ 62.0.0
locals:
  k: Loop index for the subdaily time-step within the current day; it selects the rainfall
    and runoff values for each step and the `hhsedy(j,k)` output slot.
  j: Current HRU index copied from `ihru` so the routine can read the active HRU’s soil, plant,
    landuse, and runoff state and write sediment back to that HRU.
  ulu: Urban land-use code from `hru(j)%luse%urb_lu`; used to look up the impervious fraction
    in `urbdb(ulu)` when the HRU is urban.
  percent_clay: Clay percentage of the top soil layer; used with silt to classify the soil
    texture class and choose `erod_k`.
  percent_silt: Silt percentage of the top soil layer; used with clay to classify the soil
    texture class and choose `erod_k`.
  percent_sand: Sand percentage computed as the remainder after clay and silt; used in the
    texture-class rules that determine `erod_k`.
  erod_k: Soil detachability coefficient selected from EUROSEM texture rules; it scales rainfall
    splash erosion for the current HRU.
  ke_direct: Kinetic energy per unit rainfall depth from direct throughfall; computed from
    rainfall intensity and used in total rainfall energy.
  ke_leaf: Kinetic energy of leaf drainage; computed from effective canopy height and used
    in total rainfall energy.
  ke_total: Total rainfall kinetic energy for the time step, combining direct throughfall
    and leaf drainage contributions; this drives splash erosion.
  pheff: Effective plant height derived from canopy height; used to estimate leaf-drainage
    kinetic energy.
  c: Cover-management factor used in the overland-flow sediment equation; computed from vegetation/residue
    cover and `cvm_com(j)`.
  rdepth_direct: Depth of direct throughfall rainfall reaching the soil surface; used with
    `ke_direct` to compute total rainfall energy.
  rdepth_leaf: Depth of rainfall intercepted by the canopy and routed as leaf drainage; used
    with `ke_leaf` to compute total rainfall energy.
  rdepth_tot: Total rainfall depth for the current time step; it is partitioned into direct
    and leaf-drainage components.
  canopy_cover: Fractional canopy cover derived from LAI; it controls how much rainfall is
    assigned to leaf drainage versus direct throughfall.
  bed_shear: Shear stress exerted by overland flow on the soil surface; used to compute rill/interrill
    erosion (`sedov`).
  sedspl: Splash-erosion sediment yield for the current time step; computed from rainfall
    energy, soil detachability, runoff suppression, and HRU area.
  sedov: Overland-flow sediment yield for the current time step; computed from bed shear,
    soil K, cover factor, and basin scaling terms.
  rain_d50: Median raindrop diameter implied by rainfall intensity; used to limit splash erosion
    when surface water depth is too large.
  rintnsty: Rainfall intensity for the current subdaily step, derived from precipitation depth
    and time-step length; it drives raindrop energy calculations.
  cover: Combined surface cover mass from above-ground biomass and total residue; used to
    compute the overland-flow cover factor `c`.
uses:
  urban_data_module: '`urban_data_module` supplies `urbdb(ulu)%fimp`, the impervious fraction
    for urban land uses. That factor reduces both splash and overland-flow sediment when the
    current HRU is urban.'
  basin_module: '`basin_module` provides basin-wide erosion controls and coefficients. `bsn_cc%gampt`
    determines whether the subdaily Green-Ampt erosion loop runs, and `bsn_prm%eros_spl`,
    `bsn_prm%rill_mult`, `bsn_prm%c_factor`, and `bsn_prm%eros_expo` scale the splash and
    overland-flow formulas.'
  climate_module: '`climate_module` provides the subdaily precipitation series `wst(iwst)%weat%ts(k)`
    for the active weather station. Those values are converted into rainfall intensity and
    depth for each erosion time step.'
  time_module: '`time_module` provides the number of subdaily steps (`time%step`) and the
    step length in minutes (`time%dtm`). The routine uses both to convert precipitation depth
    into intensity and to convert sediment rates into per-step totals.'
  hydrograph_module: '`hydrograph_module` supplies the current weather-station index `iwst`
    and the time-step storage `ts`, which link the active HRU to the precipitation time series
    used in the erosion calculation.'
  hru_module: '`hru_module` provides the active HRU, its urban land-use code and area (`hru(j)%luse%urb_lu`,
    `hru(j)%km`), the current runoff depth `hhqday(j,k)`, the cover-management baseline `cvm_com(j)`,
    and the output array `hhsedy(j,k)` that receives the sediment load.'
  soil_module: '`soil_module` provides the soil texture and erodibility inputs for the current
    HRU. The routine reads clay and silt from the top soil physical layer and `usle_k` from
    the first soil layer to select texture class and compute overland-flow erosion.'
  plant_module: '`plant_module` provides the current community canopy height and LAI. `pcom(j)%lai_sum`
    sets fractional canopy cover and `pcom(j)%cht_mx` sets effective plant height for rainfall
    interception energy.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides biomass and residue
    masses. `pl_mass(j)%ab_gr_com%m` and `pl_mass(j)%rsd_tot%m` are added to form the cover
    mass used in the overland-flow cover factor.'
---

<!-- facts:header -->

Computes subdaily sediment yield from an HRU by combining raindrop splash erosion and overland-flow erosion.

## Bottom Line

`ero_ovrsed` loops through the day’s rainfall time steps for the current HRU and estimates sediment produced at each step. It first computes splash erosion from rainfall energy, soil texture, canopy interception, runoff depth, and urban imperviousness, then computes overland-flow erosion from runoff shear stress, soil erodibility, cover, and basin erosion coefficients.

The routine stores the combined sediment yield in `hhsedy(j,k)` so later surface and routing calculations can use the subdaily erosion load for the active HRU and time step. If the Green-Ampt option is disabled (`bsn_cc%gampt <= 0`), the routine skips the time-step loop and leaves no updated sediment values for this call.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`surface` calls this routine after it has established positive daily runoff and peak flow conditions and after `ero_eiusle` in the same surface-erosion sequence. `ero_ovrsed` then fills `hhsedy(j,k)` for the active HRU and each subdaily step, and those sediment values feed later surface erosion and routing behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local indices and erosion helper variables, then bind the active HRU and its urban land-use code from `ihru` and `hru(j)%luse%urb_lu`. | Sets up the current HRU context and zero-initialized working variables used in the rainfall and flow erosion calculations. |
| 2. Read the top-soil clay and silt fractions, compute sand as the remainder, and classify the soil texture to choose `erod_k`. | Uses soil texture rules from the EUROSEM user guide to assign a detachability coefficient that controls splash erosion strength. |
| 3. Convert LAI to a canopy-cover fraction, capping cover at 100% when `pcom(j)%lai_sum` is at least 1.0. | Derives the vegetation interception fraction that splits rainfall into leaf drainage and direct throughfall. |
| 4. Enter subdaily erosion processing only when Green-Ampt routing is enabled (`bsn_cc%gampt > 0`). | Skips the detailed time-step loop unless the basin control flag requests this erosion calculation path. |
| 5. For each subdaily step, convert precipitation depth to rainfall intensity, estimate median drop size, and branch on whether rainfall intensity is positive. | Builds the rainfall inputs used for kinetic-energy calculations and handles the no-rain case by zeroing rainfall-energy and depth terms. |
| 6. Compute direct-throughfall kinetic energy, leaf-drainage kinetic energy, and rainfall depths when rain is present; otherwise keep them zero. | Splits rainfall into surface-reaching and canopy-intercepted components and calculates their separate energy contributions. |
| 7. Combine the rainfall-energy terms into total kinetic energy and compute splash erosion with soil detachability, runoff suppression, HRU area, and urban imperviousness corrections. | Produces the time-step splash sediment yield from raindrop impact and reduces it for impervious urban area when applicable. |
| 8. Suppress splash erosion when runoff depth is too large relative to drop size or when runoff is essentially zero. | Applies the model’s splash-erosion cutoff so unrealistic splash does not occur under deep ponding or no-flow conditions. |
| 9. Form the overland-flow cover mass from above-ground biomass and total residue, then compute the cover factor `c`. | Calculates the management/cover term used in the sediment transport equation from the current vegetation and residue mass. |
| 10. Compute bed shear from runoff depth and slope, then calculate overland-flow sediment yield using basin and soil erosion coefficients. | Estimates rill/interrill erosion rate from hydraulic stress and parameterized erosion response. |
| 11. Convert the overland-flow rate to a per-step sediment total using the model time-step length, or to a daily total when the day is represented as a single step. | Scales the rate into the same temporal units used by the current simulation configuration. |
| 12. Apply the same urban imperviousness reduction to overland-flow sediment when the HRU is urban. | Reduces the flow-erosion yield for impervious area in urban HRUs just as splash erosion is reduced. |
| 13. Store the combined sediment yield in `hhsedy(j,k)` and zero out negligible values. | Writes the final subdaily sediment load for the current HRU/time step and removes near-zero numerical noise. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:urban_data_module] | `urbdb` | `urbdb(ulu)%fimp` |
| [sym:basin_module] | `bsn_cc, bsn_prm` | `bsn_cc%gampt, bsn_prm%eros_spl, bsn_prm%rill_mult, bsn_prm%c_factor, bsn_prm%eros_expo` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%ts(k)` |
| [sym:time_module] | `time` | `time%step, time%dtm` |
| [sym:hydrograph_module] | `ts, iwst` |  |
| [sym:hru_module] | `hru, hhqday, cvm_com, hhsedy, ihru` | `hru(j)%luse%urb_lu, hru(j)%km` |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%clay, soil(j)%phys(1)%silt, soil(j)%ly(1)%usle_k` |
| [sym:plant_module] | `pcom` | `pcom(j)%lai_sum, pcom(j)%cht_mx` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%rsd_tot%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hhsedy(j,k)` | Inside the `bsn_cc%gampt > 0` loop for each `k`, after splash and overland-flow yields are computed | Stores the combined sediment yield for the current HRU and subdaily time step as `sedspl + sedov`, then forces tiny values to zero so downstream code sees a clean sediment load. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four relevant changes. In 2026-01-07 (`72206bc`), the overland-flow cover mass was updated from `soil1(j)%rsd(1)%m` to `pl_mass(j)%rsd_tot%m`, so the cover factor now uses total residue mass from the plant mass module. In 2025-02-03 (`889136d`), only a documentation typo was fixed (`varing` to `varying`) with no behavior change. In 2024-12-05 (`eb22103`), the cover mass source changed from `rsd1(j)%tot_com%m` to `soil1(j)%rsd(1)%m`, reflecting the refactor to the new soil structure. In 2024-08-08 (`39fabde`), local variables were initialized with defaults and the routine’s return statement remained unchanged.

- `72206bc` changed the overland-flow cover term to use `pl_mass(j)%rsd_tot%m`, altering the residue input to the `c` factor and therefore changing `sedov` whenever residue mass differs from the previous source.
- `889136d` made no algorithmic change; it only corrected a documentation typo in the header comments.
- `eb22103` changed the cover mass source to `soil1(j)%rsd(1)%m`, which changed the overland-flow cover factor input before later refactoring moved that logic to `pl_mass(j)%rsd_tot%m`.
- `39fabde` initialized local scalars at declaration time, reducing uninitialized-variable risk but not changing the erosion equations themselves.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ero_ovrsed' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft’s block-level placeholders into 13 source-backed model steps to match the visible control flow and keep each step tied to real line numbers.
- Source evidence shows the routine uses `bsn_cc%gampt` as a gate; if it is not positive, the subdaily loop is skipped entirely.
- The callee list contains no resolved outgoing calls; only intrinsic functions (`log10`, `Exp`, `Real`) are mentioned in the source comments.
- Lineage evidence indicates the residue source for the cover term changed twice across resolved commits; the current code uses `pl_mass(j)%rsd_tot%m`.
