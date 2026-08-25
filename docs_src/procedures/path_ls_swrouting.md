---
kind: procedure
symbol: path_ls_swrouting
title: path_ls_swrouting
status: filled
source_hash: 379952cb074c8744
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from the global current HRU number `ihru`; it is used to index the soil
    pathogen store, soil profile, and pathogen balance arrays for the HRU being processed.
  ipath: Loop counter over pathogen types. It runs from 1 to `cs_db%num_paths` so the routine
    updates leaching for every simulated pathogen constituent.
  ipath_db: Database pointer to the pathogen definition associated with the current soil-plant
    initialization. It selects the pathogen coefficients (`kd` and `perco`) used in the leaching
    calculation.
  isp_ini: Soil-plant initialization index taken from the current HRU's database pointers.
    It is used to reach `sol_plt_ini(isp_ini)%path` and find which pathogen database entry
    applies.
  path_kd: Temporary copy of the pathogen distribution coefficient `path_db(ipath_db)%kd`
    for the current pathogen. It is used in the leaching formula before the value is discarded.
uses:
  pathogen_data_module: The pathogen database supplies the pathogen-specific coefficients
    that control leaching. `kd` scales how readily the pathogen partitions with soil water,
    and `perco` appears in the denominator to represent the pathogen's percolation-related
    coefficient for the current pathogen type.
  constituent_mass_module: These arrays hold the pathogen mass bookkeeping for the soil compartment.
    `cs_db%num_paths` sets how many pathogen species are processed, and `cs_soil(j)%ly(1)%path(ipath)`
    is the available mass in the first soil layer that this routine removes from after computing
    leaching.
  output_ls_pathogen_module: This module stores the per-pathogen balance outputs. `hpath_bal(j)%path(ipath)%perc1`
    is the leached-pathogen amount this routine computes and records for downstream runoff,
    process, and reporting routines.
  hru_module: The HRU module provides the current HRU context and the database pointers needed
    to identify the active soil-plant initialization. `hru(ihru)%dbs%soil_plant_init` selects
    the initialization record, and `sol_plt_ini(isp_ini)%path` identifies which pathogen database
    entry governs this HRU.
  soil_module: The soil module provides the hydrologic drivers used in the leaching equation.
    `soil(j)%ly(1)%prk` is the current percolation from the top layer, and `soil(j)%phys(1)%conv_wt`
    converts the layer mass basis into the scaling used in the denominator.
---

<!-- facts:header -->

Routes pathogen mass from soil into leached-out balance terms for the current HRU. It updates the first soil layer pathogen store and the corresponding pathogen leaching balance.

## Bottom Line

This routine computes daily pathogen leaching for each simulated pathogen type in the active HRU. It uses the current soil percolation, soil conversion weight, and pathogen-specific coefficients to estimate how much pathogen leaves the first soil layer as percolation loss.

The calculated leached amount is stored in `hpath_bal(j)%path(ipath)%perc1`, capped so it cannot exceed the pathogen mass available in `cs_soil(j)%ly(1)%path(ipath)` and floored at zero. The same amount is then subtracted from the soil pathogen pool, so later pathogen transport and output routines see the reduced soil mass and the leaching balance for the day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in `hru_control` during the daily pathogen transport section, before `path_ls_runoff` and `path_ls_process`. `hru_control` must already have the current HRU index, soil-plant initialization pointers, soil state, and pathogen inventories loaded; the results then feed later pathogen transport accounting and output balances for the same HRU and day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. copy current HRU index | Sets local HRU index `j` to the current global HRU number `ihru`, so all subsequent array access is tied to the active HRU. |
| 2. loop over pathogen types | Iterates through every simulated pathogen constituent from 1 to `cs_db%num_paths`. |
| 3. find HRU soil-plant init | Reads the HRU's soil-plant initialization index from `hru(ihru)%dbs%soil_plant_init`. |
| 4. resolve pathogen database entry | Uses the soil-plant initialization record to select the pathogen database pointer `ipath_db` for this HRU. |
| 5. load pathogen partition coefficient | Copies `path_db(ipath_db)%kd` into local `path_kd` for use in the leaching calculation. |
| 6. compute leached mass | Calculates pathogen leached past the first soil layer using pathogen `kd`, first-layer pathogen mass, soil percolation, soil conversion weight, and pathogen `perco`. |
| 7. cap leached mass at available mass | Forces the computed leached amount to be no larger than the pathogen mass currently present in the first soil layer. |
| 8. floor leached mass at zero | Prevents negative leaching values by taking the maximum with zero. |
| 9. remove leached mass from soil store | Subtracts the leached amount from `cs_soil(j)%ly(1)%path(ipath)`, reducing the first-layer soil pathogen inventory. |
| 10. finish routine | Returns after all pathogen types have been processed for the current HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:pathogen_data_module] | `path_db` | `path_db(ipath_db)%kd, path_db(ipath_db)%perco` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_paths, cs_soil(j)%ly(1)%path(ipath)` |
| [sym:output_ls_pathogen_module] | `hpath_bal` | `hpath_bal(j)%path(ipath)%perc1` |
| [sym:hru_module] | `hru, sol_plt_ini, ihru` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%path` |
| [sym:soil_module] | `soil` | `soil(j)%ly(1)%prk, soil(j)%phys(1)%conv_wt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpath_bal(j)%path(ipath)%perc1` | Within the loop for each `ipath = 1, cs_db%num_paths`, after the raw leaching amount is computed from soil and pathogen coefficients. | This balance term captures how much of the current pathogen type leaves the first soil layer by percolation for the active HRU on the current day. It is later used as the pathogen leaching output reported by the balance module. |
| `cs_soil(j)%ly(1)%path(ipath)` | Within the same pathogen loop, after `hpath_bal(j)%path(ipath)%perc1` has been limited to the range from zero to the available soil mass. | The first-layer soil pathogen store is reduced by the exact amount routed to leaching, so the remaining mass stays consistent with the day's pathogen balance accounting. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:4.3.1 |  | $bact_{lp,perc}=\frac{bact_{lpsol}*w_{perc,surf}}{10*\rho_b*depth_{surf}*k_{bact,perc}}$ | Verified against SWAT+ 62.0.0 (path_ls_swrouting.f90:24). perc1 = kd*path*prk/((conv_wt/1000.)*perco)` — leaching |
| 3:4.3.2 |  | $bact_{p,perc}=\frac{bact_{psol}*w_{perc,surf}}{10*\rho_b*depth_{surf}*k_{bact,perc}}$ | Verified against SWAT+ 62.0.0 (path_ls_swrouting.f90:24). same line, p pool |

## Lineage

Three source-backed commits were resolved. `df07e3f` introduced `path_ls_swrouting.f90` with the leaching loop, the capped `perc1` calculation, and subtraction from the soil pathogen pool. `94b6dec` shows the same routine content carried forward without behavioral change in the extracted lines. `39fabde` only initialized the local scalars `j`, `ipath`, `ipath_db`, `isp_ini`, and `path_kd`; the leaching logic remained the same.

- df07e3f added the routine and its pathogen leaching/balance update logic.
- 39fabde initialized the local loop and pointer variables to zero/default values; no change to the leaching formula itself was shown.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'path_ls_swrouting' has no extracted documentation comment.
- algorithm_steps revised: expanded the two-step draft into a source-faithful 10-step sequence covering the loop, coefficient lookup, capped calculation, and soil inventory update.
- Source is explicit about the leaching formula but does not show any other callees or file operations.
