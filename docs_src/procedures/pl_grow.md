---
kind: procedure
symbol: pl_grow
title: pl_grow
status: filled
source_hash: 7ab5de07aa532956
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; selects the current HRU/community entry to process.
  idp: Plant database index for the active plant; derived from `pcom(j)%plcur(ipl)%idplt`
    and used to inspect the plant trigger type.
uses:
  plant_data_module: Provides the plant database trigger that determines whether a growing
    plant should be checked for temperature-based dormancy.
  basin_module: Imported by the procedure, but no specific basin-module symbol was resolved
    in the provided context.
  hru_module: Provides the current HRU index and the plant-loop index used by this routine.
  plant_module: Holds the plant community, plant status flags, and per-plant metadata that
    control the daily growth loop and dormancy gating.
  carbon_module: Imported by the procedure, but no specific carbon-module symbol was resolved
    in the provided context.
  organic_mineral_mass_module: Provides the daily biomass/nutrient increment container and
    the zero-mass template used to reset plant uptake before each plant is processed.
  time_module: Provides the year-end flag that controls whether mortality is applied after
    daily growth.
  output_landscape_module: Stores daily plant biomass and carbon growth summaries for the
    current HRU.
---

<!-- facts:header -->

Daily plant growth driver for one HRU. It updates nutrient demand, dormancy, biomass growth, organ growth, partitioning, and year-end mortality for each plant in the community.

## Bottom Line

`pl_grow` is the daily plant-growth coordinator for the current HRU. It first updates nutrient demand, then loops through each plant in the community to handle dormancy checks, biomass and organ growth, leaf senescence, seed growth, and biomass partitioning.

It matters because it is the routine that advances plant state for the day and records growth summaries in the landscape output arrays. At year end it also applies mortality so perennial biomass does not accumulate unrealistically across years.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pl_grow` is called from `hru_control` after the HRU plant status has been prepared for the day. It performs the daily plant-growth update for every plant in the current HRU, and its results feed the same HRU-level output and end-of-year mortality bookkeeping that follows in `hru_control`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. call | Copies the current HRU index from `ihru` into `j`, calls `pl_nut_demand` to refresh nutrient demand, and zeros the daily HRU growth output accumulators `hpw_d(j)%bm_grow` and `hpw_d(j)%c_gro`. |
| 2. loop | Iterates over each plant in the current community with `do ipl = 1, pcom(j)%npl` and resets `pl_mass_up` to `plt_mass_z` so each plant starts the loop with zero daily biomass and nutrient increment state. |
| 3. if | For plants whose growth flag is on, loads the plant database index `idp` from `pcom(j)%plcur(ipl)%idplt` and calls `pl_dormant` when the plant trigger is `temp_gro`, allowing temperature-based dormancy to be updated before growth. |
| 4. if | Only plants with `idorm == "n"` and `gro == "y"` proceed through the daily growth sequence: biomass growth, root growth, leaf growth, leaf senescence, seed growth, and biomass partitioning. |
| 5. call | Calls `pl_biomass_gro` to calculate the plant’s daily biomass increase under current stress and climate conditions. |
| 6. call | Calls `pl_root_gro(j)` to update rooting depth and root allocation for the current HRU plant. |
| 7. call | Calls `pl_leaf_gro` to update leaf area index and canopy growth for the active plant. |
| 8. call | Calls `pl_leaf_senes` to remove senesced leaf biomass and move it into residue accounting after leaf growth. |
| 9. call | Calls `pl_seed_gro(j)` to update seasonal seed growth and harvest index for the current HRU plant. |
| 10. call | Calls `pl_partition(j, 0)` to distribute the day’s biomass and nutrient gains among root, leaf, stem, and seed pools. |
| 11. if | When `time%end_yr == 1`, calls `pl_mortality` so end-of-year biomass losses are routed to residue pools. |
| 12. return | Ends the plant loop, returns from the subroutine, and leaves the updated plant and output state in module storage. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%trig` |
| [sym:basin_module] | `basin state imported by use association` |  |
| [sym:hru_module] | `ihru, ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%idorm` |
| [sym:carbon_module] | `carbon state imported by use association` |  |
| [sym:organic_mineral_mass_module] | `pl_mass_up, plt_mass_z` |  |
| [sym:time_module] | `time` | `time%end_yr` |
| [sym:output_landscape_module] | `hpw_d` | `hpw_d(j)%bm_grow, hpw_d(j)%c_gro` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpw_d(j)%bm_grow` | At routine start | Reset to zero before daily plant growth is accumulated for the HRU. |
| `hpw_d(j)%c_gro` | At routine start | Reset to zero before daily plant carbon growth is accumulated for the HRU. |
| `pl_mass_up` | At the start of each plant loop iteration | Reset to `plt_mass_z` so the current plant begins with zero daily biomass and nutrient increment state. |

## File I/O

<!-- facts:io -->


## Lineage

`pl_grow.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 9 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_grow.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `2e38acc` (2025-07-25) — Fixed problem with bm_grow so that it is zero in hru_pw when no crop is growing,
- `aef12f3` (2025-05-29) — Add growth check before calling pl_dormant subroutine
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- No source-backed lineage evidence was available; lineage summary reflects that limitation.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
