---
kind: procedure
symbol: pl_burnop
title: pl_burnop
status: filled
source_hash: 9a9ab20caf4cceb8
version_label: SWAT+ 62.0.0
args:
  jj: '`jj` selects the HRU/community index to burn; the routine copies it into the local
    `j` and uses that index for all state updates.'
  iburn: '`iburn` selects the fire operation database entry in `fire_db`; its `cn2_upd` and
    `fr_burn` values control the curve-number adjustment and burn fraction.'
locals:
  j: Local HRU index used throughout the routine after copying `jj` into `j`. It lets the
    subroutine reference the selected HRU and its plant community state consistently.
  cnop: Temporary updated curve number. It is computed from the current HRU curve number plus
    the fire-operation adjustment, capped at 98.0 before `curno` is called.
uses:
  basin_module: '`basin_module` is the source of the HRU curve-number array here; the routine
    reads `cn2(j)` to compute the post-burn curve number before passing it to `curno`.'
  mgt_operations_module: '`mgt_operations_module` provides the fire-operation database. `fire_db(iburn)%fr_burn`
    supplies the fraction burned, and `fire_db(iburn)%cn2_upd` supplies the curve-number change
    used by this burn event.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` defines the plant, residue,
    soil, and temporary organic-mass types that `pl_burnop` modifies. The routine updates
    plant-community totals, individual-plant biomass, burned organic mass, and soil humus/residue
    pools using these derived types.'
  hru_module: '`hru_module` matters because it supplies `ipl`, the plant-loop index used here,
    and `cn2`, which is adjusted before the curve-number update call.'
  soil_module: '`soil_module` is used as the host for soil profile state referenced during
    burning. The routine burns layer-1 slow humus, passive humus, and fresh residue, then
    adds burned phosphorus to the stable humus pool through these soil-profile objects.'
  plant_module: '`plant_module` matters because `pcom(j)%npl` gives the number of plants in
    the community, which sets the loop bounds for burning each plant in the HRU.'
  carbon_module: '`carbon_module` matters because the routine records carbon emitted by burning.
    It adds the burned carbon to `hrc_d(j)%emit_c` and `hpc_d(j)%emit_c` so later carbon accounting
    reflects fire losses.'
---

<!-- facts:header -->

Applies a prescribed burn to one HRU’s plant community. It updates curve number, reduces plant/residue pools, and moves burned carbon into the HRU carbon loss trackers.

## Bottom Line

`pl_burnop` is the burn-management routine for a single HRU. Given an HRU index and a fire-operation record, it adjusts the HRU curve number, burns a fraction of plant residue and above-ground biomass for every plant in the community, and updates the community-level mass summaries.

It also transfers burned carbon to the residue and plant CO2 emission counters and moves burned plant phosphorus into the stable humus phosphorus pool. The result is the post-burn state that later runoff, growth, residue, and carbon accounting routines use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when management selects a burn action, either from `actions` or `mgt_sched`. Those callers provide the HRU index and burn type, and `pl_burnop` uses the fire database and current HRU state to apply the burn; later output and carbon/water accounting depend on the updated `cn2`, plant mass pools, residue pools, and emission counters.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set HRU index | Copy the incoming HRU index `jj` into local `j` so the rest of the routine can work on one selected HRU. |
| 2. compute burn curve number | Add the fire-operation curve-number update to the current HRU `cn2`, cap the result at 98.0, and store it in `cnop`. |
| 3. update runoff state | Call `curno(cnop, j)` to write the new curve-number state back into the HRU and refresh runoff-related parameters. |
| 4. reset community totals | Zero the plant-community total, above-ground, leaf, stem, and seed mass accumulators before recomputing them after burning. |
| 5. loop over plants | Iterate across every plant in the community using `pcom(j)%npl` as the loop bound. |
| 6. burn residue and biomass | Reduce each plant’s surface residue and above-ground biomass pools by the burned fraction, then add the burned carbon to `hrc_d(j)%emit_c` and `hpc_d(j)%emit_c`. |
| 7. burn surface soil pools | Reduce layer-1 slow humus, passive humus, and plant residue by the burned fraction, then move burned plant phosphorus into `soil1(j)%hp(1)%p`. |
| 8. rebuild community sums | Accumulate the remaining per-plant total, above-ground, leaf, stem, and seed mass into the community summary pools. |
| 9. return | Exit after the burn updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `cn2` | `cn2(j)` |
| [sym:mgt_operations_module] | `fire_db` | `fire_db(iburn)%fr_burn` |
| [sym:organic_mineral_mass_module] | `pl_mass, pl_burn, soil1, plt_mass_z` | `pl_mass(j)%tot_com, pl_mass(j)%ab_gr_com, pl_mass(j)%leaf_com, pl_mass(j)%stem_com, pl_mass(j)%seed_com, pl_mass(j)%rsd(ipl), pl_mass(j)%rsd_tot, pl_mass(j)%ab_gr(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%seed(ipl), pl_burn%c, soil1(j)%hs(1), soil1(j)%hp(1), soil1(j)%pl(ipl)%rsd(ipl), soil1(j)%hp(1)%p, pl_burn%p, pl_mass(j)%tot(ipl)` |
| [sym:hru_module] | `cn2, ipl` |  |
| [sym:soil_module] | `soil1, plt_mass_z` | `soil1(j)%hs(1), soil1(j)%hp(1), soil1(j)%pl(ipl)%rsd(ipl), soil1(j)%hp(1)%p, plt_mass_z` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |
| [sym:carbon_module] | `hrc_d, hpc_d` | `hrc_d(j)%emit_c, hpc_d(j)%emit_c` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pl_mass(j)%tot_com` | Inside the plant loop after each plant’s burn reduction is applied. | `pl_mass(j)%tot_com` is cleared first and then rebuilt by summing the remaining total biomass of all plants in the community after the burn. |
| `pl_mass(j)%ab_gr_com` | Inside the plant loop after each plant’s burn reduction is applied. | `pl_mass(j)%ab_gr_com` is cleared first and then rebuilt from the remaining above-ground biomass of all plants after the burn. |
| `pl_mass(j)%leaf_com` | Inside the plant loop after each plant’s burn reduction is applied. | `pl_mass(j)%leaf_com` is cleared first and then rebuilt from the remaining leaf biomass of all plants after the burn. |
| `pl_mass(j)%stem_com` | Inside the plant loop after each plant’s burn reduction is applied. | `pl_mass(j)%stem_com` is cleared first and then rebuilt from the remaining stem biomass of all plants after the burn. |
| `pl_mass(j)%seed_com` | Inside the plant loop after each plant’s burn reduction is applied. | `pl_mass(j)%seed_com` is cleared first and then rebuilt from the remaining seed biomass of all plants after the burn. |
| `pl_mass(j)%rsd(ipl)` | For each plant in the community when the burn fraction is applied. | `pl_mass(j)%rsd(ipl)` is multiplied by the unburned fraction so that surface residue for that plant is reduced by fire. |
| `pl_mass(j)%rsd_tot` | For each plant in the community when the burn fraction is applied. | `pl_mass(j)%rsd_tot` is updated from the burned-down surface residue state to represent the post-burn residue total used in outputs. |
| `pl_burn` | For each plant in the community when fire mass is computed. | `pl_burn` is reused as temporary storage for the mass burned from biomass and soil organic pools, first for plant biomass carbon and then for surface soil pools. |
| `pl_mass(j)%ab_gr(ipl)` | For each plant in the community when the burn fraction is applied. | `pl_mass(j)%ab_gr(ipl)` is reduced to the unburned fraction, leaving the remaining above-ground biomass after fire. |
| `pl_mass(j)%stem(ipl)` | For each plant in the community when the burn fraction is applied. | `pl_mass(j)%stem(ipl)` is reduced to the unburned fraction so the surviving stem mass remains after fire. |
| `pl_mass(j)%leaf(ipl)` | For each plant in the community when the burn fraction is applied. | `pl_mass(j)%leaf(ipl)` is reduced to the unburned fraction so the surviving leaf mass remains after fire. |
| `pl_mass(j)%seed(ipl)` | For each plant in the community when the burn fraction is applied. | `pl_mass(j)%seed(ipl)` is reduced to the unburned fraction so the surviving seed mass remains after fire. |
| `hrc_d(j)%emit_c` | When burned plant carbon is computed for a plant. | `hrc_d(j)%emit_c` accumulates the carbon emitted from burning surface residue and above-ground plant material. |
| `hpc_d(j)%emit_c` | When burned plant carbon is computed for a plant. | `hpc_d(j)%emit_c` accumulates the same burned plant carbon as a plant-carbon emission loss for the HRU. |
| `soil1(j)%hs(1)` | When the soil surface burn mass is computed for a plant. | `soil1(j)%hs(1)` is reduced by the burned fraction, representing loss from the slow humus pool in the top soil layer. |
| `soil1(j)%hp(1)` | When the soil surface burn mass is computed for a plant. | `soil1(j)%hp(1)` is reduced by the burned fraction, representing loss from the passive humus pool in the top soil layer. |
| `soil1(j)%hp(1)%p` | After burned plant phosphorus is computed for the top soil layer. | `soil1(j)%hp(1)%p` increases by the burned plant phosphorus so that the burned P is retained in the stable humus pool. |

## File I/O

<!-- facts:io -->


## Lineage

`pl_burnop.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 11 non-merge commit(s) since, most recently `b04fe39` (2026-04-30, "removed commented out code that was legacy cswat = 1 cfarm code."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_burnop.f90` are listed.

- `b04fe39` (2026-04-30) — removed commented out code that was legacy cswat = 1 cfarm code.
- `3f99111` (2026-04-22) — Fixed a few cswat >= 0 errors and reverted and commented out some code that needs to be discussed with jeff.
- `3389f29` (2026-04-22) — Numerous changes to account for the removal of the old cswat ==1 and moving cswat == 3 to cswat =1. Also some code formatting changes to get…
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_burnop' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
