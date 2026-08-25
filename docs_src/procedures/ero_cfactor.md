---
kind: procedure
symbol: ero_cfactor
title: ero_cfactor
status: filled
source_hash: cd16ac744756ad6b
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` so the subroutine works on the current HRU's plant, residue,
    and erosion state.
  ipl: Sequential plant counter used conceptually for plant-by-plant cover calculations in
    the older method; it is declared here but not used in the active code path shown.
  idp: Plant database identifier used conceptually to map a plant community member to plant
    data; it is declared here but not used in the active code path shown.
  c: Working value for the final USLE C factor before it is stored in `usle_cfac(ihru)`.
  ab_gr_t: Above-ground biomass converted from kg/ha to tons/ha for the active APEX-style
    biomass cover calculation.
  rsd_covfact: Residue cover factor computed from residue mass and `bsn_prm%rsd_covco`.
  rsd_sumfac: Intermediate residue-mass term used to turn residue mass into an exponential
    cover attenuation factor.
  grcov_frac: Fraction of biomass that contributes to ground cover, based on above-ground
    biomass.
  bio_covfact: Biomass cover factor derived from ground-cover fraction and maximum canopy
    height, then bounded to [1e-10, 1].
  cover: Total cover mass used only in the older branch as the sum of above-ground biomass
    and residue.
uses:
  basin_module: '`basin_module` provides the basin-level control switch `bsn_cc%cfac` that
    selects the cover-factor algorithm, and the basin parameter `bsn_prm%rsd_covco` that controls
    how residue mass is converted into a cover attenuation factor.'
  hru_module: '`hru_module` supplies the current HRU index `ihru` plus the HRU-level arrays
    `cvm_com` and `usle_cfac` that the routine reads for the old method and writes with the
    final C factor for this HRU.'
  plant_module: '`plant_module` provides `pcom`, which gives each HRU''s plant community structure,
    including `pcom(j)%npl` to test whether the older plant-community cover method can be
    used and `pcom(j)%cht_mx` to compute biomass cover in the active method.'
  plant_data_module: '`plant_data_module` matters because the older cover-factor formulation
    depends on plant database information for plant-community members, even though no specific
    imported symbol from this module is resolved in the extracted candidate references.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides `pl_mass`, which holds
    the HRU''s above-ground biomass and residue masses; those masses are the direct inputs
    to both the old and new cover-factor calculations.'
  time_module: '`time_module` matters because this erosion calculation runs in the daily simulation
    flow and depends on the current model time context even though no specific resolved symbol
    from the module appears in the extracted references.'
  erosion_module: '`erosion_module` receives the computed cover-factor terms through `ero_output(j)%ero_d`;
    that makes the intermediate erosion diagnostics available for sediment/erosion reporting
    and later model use.'
  utils: '`utils` matters because `exp_w` is used throughout the formulae to compute exponentials
    safely, preventing underflow in the residue and biomass cover calculations.'
---

<!-- facts:header -->

Computes the daily USLE cover-management factor for the current HRU. It can use either the older plant-community minimum-C approach or the newer residue/biomass APEX-based approach, then stores the result for erosion calculations.

## Bottom Line

`ero_cfactor` determines the USLE C factor for the current HRU using the model's active cover-factor method. In this source, `bsn_cc%cfac` is forced to `1`, so the routine follows the APEX-style path that combines residue cover and growing biomass cover into a single `c` value, then writes that value to `usle_cfac(ihru)`.

When that active path runs, the routine also records the component terms in `ero_output(j)%ero_d` so erosion output can report the residue mass, ground-cover fraction, residue cover factor, and biomass cover factor used to build the final C factor. Those outputs are then available to later erosion computations such as the sediment yield routines called from `surface` and `wetland_control`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU erosion setup, after the calling routine has established the current HRU context (`ihru` or `j`) and the runoff/sediment conditions that warrant an erosion calculation. `surface` calls it before `ero_ysed`, and `wetland_control` calls it before computing wetland sediment yield, so the resulting `usle_cfac` and erosion output terms are available to those downstream sediment calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set current HRU and active cover-mode flag | Copy the current HRU index from `ihru` into `j`, then force `bsn_cc%cfac = 1`, which selects the newer residue-and-biomass cover-factor formulation instead of the older plant-community minimum-C method. |
| 2. enter the legacy path only if the basin switch disables the new method | If `bsn_cc%cfac == 0`, compute total cover as above-ground biomass plus residue and use the older plant-community logic: when the HRU has plants (`pcom(j)%npl > 0`), compute `c` from `cvm_com(j)` and total cover; otherwise use a residue-only formula if cover exists, or fall back to `0.8` for essentially bare soil. |
| 3. compute residue cover attenuation in the active path | Convert residue mass to a scaled residue term with `rsd_sumfac = (pl_mass(j)%rsd_tot%m + 1.) / 1000.`, then apply the basin residue coefficient through `rsd_covfact = exp_w(-bsn_prm%rsd_covco * rsd_sumfac)`. |
| 4. compute biomass cover attenuation in the active path | Convert above-ground biomass to tons per hectare, derive `grcov_frac` from biomass using a nonlinear saturation curve, and turn that fraction plus canopy height into `bio_covfact`. Clamp `bio_covfact` to the range `[1.e-10, 1.]`. |
| 5. combine the active cover terms into the final C factor | Set `c` to the product of residue and biomass cover factors, with a minimum bound of `1.e-10` so the cover factor never collapses to zero. |
| 6. publish the active-path diagnostics to erosion output | Store the computed C factor and its component diagnostics into `ero_output(j)%ero_d`, including residue mass, ground-cover fraction, residue cover factor, and biomass cover factor. |
| 7. store the HRU C factor and return | Copy the final `c` value into `usle_cfac(ihru)` so later erosion routines can use it for this HRU, then return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc, bsn_prm` | `bsn_cc%cfac, bsn_prm%rsd_covco` |
| [sym:hru_module] | `cvm_com, usle_cfac, ihru` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |
| [sym:plant_data_module] | `pldb` | `plant data types and plant-lookup state used to interpret plant-community members when the older per-plant cover method is applied` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%rsd_tot%m` |
| [sym:time_module] | `time state and date-related types` | `time and calendar state used to determine the current simulation day and the active HRU timestep context` |
| [sym:erosion_module] | `ero_output` | `ero_output(j)%ero_d%c, ero_output(j)%ero_d%rsd_m, ero_output(j)%ero_d%grcov_frac, ero_output(j)%ero_d%rsd_covfact, ero_output(j)%ero_d%bio_covfact` |
| [sym:utils] | `safe exponential wrapper `exp_w`` | `exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bsn_cc%cfac` | Always when the subroutine finishes the active-path calculation; `bsn_cc%cfac` is set to 1 at line 51 before the branch. | `bsn_cc%cfac` is used as the basin switch for cover-factor formulation. In this routine it is forced to 1, so the active APEX-style residue/biomass cover method is selected for the rest of the call. |
| `ero_output(j)%ero_d%c` | Only in the active `else` branch where `bsn_cc%cfac /= 0`. | `ero_output(j)%ero_d%c` is written with the final USLE C factor for the current erosion event so erosion diagnostics can report the cover factor actually used in the sediment calculation. |
| `ero_output(j)%ero_d%rsd_m` | Only in the active `else` branch where `bsn_cc%cfac /= 0`. | `ero_output(j)%ero_d%rsd_m` records the current residue mass for the HRU, allowing the erosion output to preserve the residue state that contributed to the cover factor. |
| `ero_output(j)%ero_d%grcov_frac` | Only in the active `else` branch where `bsn_cc%cfac /= 0`. | `ero_output(j)%ero_d%grcov_frac` stores the computed biomass ground-cover fraction so downstream diagnostics can separate biomass cover from residue cover. |
| `ero_output(j)%ero_d%rsd_covfact` | Only in the active `else` branch where `bsn_cc%cfac /= 0`. | `ero_output(j)%ero_d%rsd_covfact` stores the residue-cover attenuation term used to build the final C factor. |
| `ero_output(j)%ero_d%bio_covfact` | Only in the active `else` branch where `bsn_cc%cfac /= 0`. | `ero_output(j)%ero_d%bio_covfact` stores the biomass-cover attenuation term used to build the final C factor. |
| `usle_cfac(ihru)` | Always at the end of the routine after `c` has been determined. | `usle_cfac(ihru)` is updated with the current HRU's final USLE C factor so later erosion routines can use the value when computing sediment yield. |

## File I/O

<!-- facts:io -->


## Lineage

`ero_cfactor.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 12 non-merge commit(s) since, most recently `15ff92f` (2026-04-08, "Refactor erosion and pesticide modules to incorporate biomass and ground cover f…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ero_cfactor.f90` are listed.

- `15ff92f` (2026-04-08) — Refactor erosion and pesticide modules to incorporate biomass and ground cover factors in calculations
- `0b603da` (2026-01-30) — Prevent runtime underflow errors in cbn_rsd_decomp and update residue decomposition call in hru_control based on cswat condition.
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ero_cfactor' has no extracted documentation comment.
- plant_data_module, time_module, and utils had no resolved candidate outside references beyond the safe exponential wrapper; their roles are inferred from the source context and may be partially uncertain.
- algorithm_steps revised: condensed the branch structure into the actual executed control flow and combined the active-path assignments into clearer model steps while preserving cited source lines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
