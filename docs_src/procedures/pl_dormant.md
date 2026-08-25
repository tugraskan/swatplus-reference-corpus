---
kind: procedure
symbol: pl_dormant
title: pl_dormant
status: filled
source_hash: f4761a3ffd067762
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` so the routine can work with the current hydrologic response
    unit’s plant and weather state.
  idp: Plant database index taken from `pcom(j)%plcur(ipl)%idplt`; it selects the species
    record that determines plant type and dormancy behavior.
  iob: Object-connectivity index from `hru(j)%obj_no`; it is used to reach the weather-station
    linkage for this HRU.
  iwgn: Weather-generator parameter index from the selected weather station; it provides the
    minimum daylength threshold `wgn_pms(iwgn)%daylmn`.
  rto: Dormancy die-off ratio used to scale how much stem and leaf biomass is converted to
    dormant-season losses; in this source it is set to zero, so the biomass-drop calculations
    become zeroed.
  lai_init: Temporary storage for the plant’s LAI before dormancy changes it, used to compute
    the updated LAI value.
uses:
  climate_module: This module supplies the weather station assignment and the daylength values
    that drive dormancy timing. `pl_dormant` compares the current station daylength against
    the weather-generator minimum daylength threshold to decide whether the plant should switch
    dormancy state.
  hydrograph_module: This module links the current HRU/object to its weather station. `pl_dormant`
    needs that mapping to find the correct `iwst` before it can read the daylength for this
    HRU.
  plant_data_module: This module provides the plant database record that classifies the plant
    as `perennial` or `cold_annual`. The routine branches on that type because the dormancy
    transition and state reset differ by plant category.
  organic_mineral_mass_module: This module holds the biomass and residue pools that are reassigned
    during dormancy. `pl_dormant` removes biomass from active plant pools and adds the dropped
    material to residue pools so later decomposition and surface residue accounting can use
    the updated masses.
  hru_module: This module supplies the current HRU index, the plant-index context, and the
    HRU-level dormancy threshold adjustment `dormhr(j)`. Those values determine which plant
    instance is being evaluated and how the daylength threshold is adjusted for that HRU.
  plant_module: This module contains the current plant-community status and growth variables
    that are read and updated here. The routine changes dormancy status, heat-unit accumulation,
    LAI, stress state, and senescence tracking so later growth logic sees the correct plant
    condition.
---

<!-- facts:header -->

Checks whether a plant should enter or leave dormancy based on daylength and plant type, then updates dormancy flags and biomass pools for that HRU plant.

## Bottom Line

`pl_dormant` is the dormancy gatekeeper for the current HRU plant (`ihru`, `ipl`). It uses the linked weather station daylength and the plant’s dormancy threshold to decide whether the plant is entering dormancy or coming back out of it, with separate handling for perennial plants and cool-season annuals.

When dormancy starts for a perennial, the routine moves above-ground material into residue, zeroes the plant’s seed mass, lowers LAI, resets heat-unit accumulation, and marks the plant dormant. When dormancy ends, it restores the dormancy flag and clears the counters that should restart growth or senescence tracking.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pl_dormant` runs inside the plant-growth workflow when `pl_grow` is processing a plant whose growth trigger is `temp_gro`; `pl_grow` prepares the current HRU/plant context and then calls this routine to test dormancy entry or exit. Its results matter immediately after the call because `pl_grow` only continues biomass growth when `pcom(j)%plcur(ipl)%idorm == "n"`, so this routine controls whether later plant growth and stress calculations are skipped or resumed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check dormancy onset threshold | The routine first tests whether the current plant is not yet dormant and whether the adjusted daylength at the HRU is below the weather-generator minimum daylength. Only if both conditions are true does it proceed to dormancy-entry logic. |
| 2. Handle perennial dormancy entry | If the plant database says the plant is perennial, the routine marks it dormant, computes above-ground dieoff using the dormant-season ratio, and stores the pre-dormancy LAI so it can be reduced consistently. |
| 3. Reduce perennial leaf and stem pools | The code computes stem, leaf, nitrogen, and phosphorus losses for dormancy using `rto` and the plant mass fractions, then clamps the nutrient losses to nonnegative values. |
| 4. Move dormant biomass to residue pools | The routine adds stem, leaf, and seed losses into `abgr_drop`, subtracts that amount from total and above-ground biomass, clears seed mass, and adds the lost mass to residue storage in `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot`. |
| 5. Reset perennial dormancy state variables | For perennial plants entering dormancy, the routine sets `pcom(j)%plcur(ipl)%idorm` to `"y"`, resets `phuacc` to zero, and restores `strsw` to 1 so the plant is treated as dormant and growth stress is cleared. |
| 6. Handle cool-season annual dormancy entry | If the plant is a cold annual and it has not yet accumulated enough heat units (`phuacc < 0.75`), the routine marks it dormant and resets the water-stress growth factor. |
| 7. Check dormancy exit threshold | The routine then tests the opposite condition: the plant must currently be dormant and the adjusted daylength must be at least the minimum daylength threshold before dormancy can end. |
| 8. Restore perennial active state | For perennials, the routine clears the dormant flag, resets heat-unit accumulation to zero, and zeroes `d_senes` so growth and senescence tracking restart when dormancy ends. |
| 9. Restore cool-season annual active state | For cold annuals, the routine clears the dormant flag and resets heat-unit accumulation so the plant can re-enter active growth. |
| 10. Return to caller | The routine exits after updating the dormancy state and biomass pools; downstream growth logic in `pl_grow` then uses the updated dormancy flag to decide whether to continue plant growth. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wst, wgn_pms` | `wst(iwst)%wco%wgn, wst(iwst)%weat%daylength, wgn_pms(iwgn)%daylmn` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%typ` |
| [sym:organic_mineral_mass_module] | `pl_mass, leaf_drop, stem_drop, seed_drop, abgr_drop, plt_mass_z` | `pl_mass(j)%stem(ipl), leaf_drop%m, pl_mass(j)%leaf(ipl)%m, leaf_drop%n, leaf_drop%p, pl_mass(j)%seed(ipl), pl_mass(j)%tot(ipl), pl_mass(j)%tot_com%m, pl_mass(j)%ab_gr(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%rsd(ipl), pl_mass(j)%rsd_tot` |
| [sym:hru_module] | `hru, dormhr, ipl, ihru` | `hru(j)%obj_no` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%idorm, pcom(j)%plg(ipl)%lai, pcom(j)%plm(ipl)%n_fr, pcom(j)%plm(ipl)%p_fr, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plstr(ipl)%strsw, pcom(j)%plg(ipl)%d_senes` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | When `pcom(j)%plcur(ipl)%idorm == "n"` and `wst(iwst)%weat%daylength - dormhr(j) < wgn_pms(iwgn)%daylmn` evaluates true, then again when the plant comes out of dormancy and the exit test is met. | `iwst` is set from the HRU-to-weather-station link so the routine reads the correct station’s daily daylength; it does not change after assignment, but it determines which climate record controls dormancy decisions. |
| `pcom(j)%plcur(ipl)%idorm` | When dormancy begins for a perennial or a cold annual, and when dormancy ends for either type. | `pcom(j)%plcur(ipl)%idorm` flips between `"n"` and `"y"` to record whether the current plant is actively growing or dormant. Later plant-growth code uses this flag to skip growth while dormant. |
| `stem_drop` | When the perennial-dormancy branch runs and `rto` is used to compute stem loss. | `stem_drop` becomes the portion of stem biomass removed during dormancy onset. That mass is then added to residue and subtracted from the active stem pool. |
| `pcom(j)%plg(ipl)%lai` | When the perennial-dormancy branch runs. | `pcom(j)%plg(ipl)%lai` is reduced to the dormant-season value computed from the pre-dormancy LAI, so canopy area reflects senescence during dormancy. |
| `leaf_drop%m` | When the perennial-dormancy branch runs. | `leaf_drop%m` stores the mass of leaves lost at dormancy onset so that leaf biomass can be removed from the plant and transferred to residue accounting. |
| `leaf_drop%n` | When the perennial-dormancy branch runs. | `leaf_drop%n` stores the nitrogen associated with dropped leaves, based on the leaf mass loss and the plant’s nitrogen fraction, so nutrient mass is conserved in residue accounting. |
| `leaf_drop%p` | When the perennial-dormancy branch runs. | `leaf_drop%p` stores the phosphorus associated with dropped leaves, based on the leaf mass loss and the plant’s phosphorus fraction, so nutrient mass is conserved in residue accounting. |
| `seed_drop` | When the perennial-dormancy branch runs. | `seed_drop` captures the current seed mass so it can be removed from the active plant pool and included in above-ground dormant losses. |
| `abgr_drop` | When the perennial-dormancy branch runs. | `abgr_drop` is the total above-ground dormant-season loss assembled from stem, leaf, and seed drops; it becomes the amount added to residue and removed from the plant’s active biomass. |
| `pl_mass(j)%tot(ipl)` | When `abgr_drop` has been computed during perennial dormancy onset. | `pl_mass(j)%tot(ipl)` is reduced by the above-ground loss so the plant’s total biomass matches the biomass that remains after dormancy starts. |
| `pl_mass(j)%tot_com%m` | When `abgr_drop` has been computed during perennial dormancy onset; if the subtraction would drive the value below zero it is clamped to zero. | `pl_mass(j)%tot_com%m` is kept nonnegative so the community-total biomass does not go negative after the dormancy transfer. |
| `pl_mass(j)%ab_gr(ipl)` | When `abgr_drop` has been computed during perennial dormancy onset. | `pl_mass(j)%ab_gr(ipl)` is reduced by the above-ground dormant loss so the active above-ground biomass pool matches the plant’s remaining biomass. |
| `pl_mass(j)%stem(ipl)` | When the perennial-dormancy branch runs. | `pl_mass(j)%stem(ipl)` is reduced by the dormant-season stem loss so the standing stem pool matches the plant after senescence. |
| `pl_mass(j)%leaf(ipl)` | When the perennial-dormancy branch runs. | `pl_mass(j)%leaf(ipl)` is reduced by the dormant-season leaf loss so the live leaf pool reflects leaf senescence at dormancy onset. |
| `pl_mass(j)%seed(ipl)` | When the perennial-dormancy branch runs. | `pl_mass(j)%seed(ipl)` is reset to `plt_mass_z`, clearing seed mass from the active plant pool after seed transfer to dormant-season losses. |
| `pl_mass(j)%rsd(ipl)` | When the perennial-dormancy branch runs. | `pl_mass(j)%rsd(ipl)` increases by the above-ground loss so the residue pool for this plant records the material shed at dormancy onset. |
| `pl_mass(j)%rsd_tot` | When the perennial-dormancy branch runs. | `pl_mass(j)%rsd_tot` increases by the same above-ground loss so total fresh surface residue reflects the new dormant-season litter. |
| `pcom(j)%plcur(ipl)%phuacc` | When the perennial or cold-annual dormancy-entry branch sets dormancy, and when the corresponding dormancy-exit branch resets it. | `pcom(j)%plcur(ipl)%phuacc` is reset to zero so heat-unit accumulation restarts when the plant becomes dormant or returns to growth. |
| `pcom(j)%plstr(ipl)%strsw` | When the perennial dormancy-entry branch runs and when the cold-annual dormancy-entry branch runs. | `pcom(j)%plstr(ipl)%strsw` is set to 1 to restore the stress multiplier to an unstressed value at dormancy onset. |
| `pcom(j)%plg(ipl)%d_senes` | When perennial dormancy ends. | `pcom(j)%plg(ipl)%d_senes` is reset to zero so the senescence-day counter restarts when the perennial exits dormancy. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:1.2.1 | Dormancy daylength threshold | $T_{DL,thr}=T_{DL,mn}+t_{dorm}$ | Dormancy is triggered when current daylength minus parameter dormhr falls below the site's minimum daylength daylmn; the threshold is evaluated directly rather than stored as T_DL,thr. |
| 5:1.2.2 | Dormancy factor at high latitude | $t_{dorm}=1.0$ | Code uses the input threshold dormhr together with precomputed minimum daylength daylmn; it does not compute t_dorm = 1.0 from latitude phi explicitly. |
| 5:1.2.3 | Dormancy factor in the transition latitude band | $t_{dorm}=\frac{\phi - 20}{20}$ | The printed linear t_dorm = (phi - 20)/20 relationship is not evaluated explicitly; dormancy uses daylength threshold parameters instead. |
| 5:1.2.4 | Dormancy factor at low latitude | $t_{dorm}=0.0$ | The code does not compute the phi < 20 branch explicitly; dormancy onset is controlled by daylength minus dormhr relative to daylmn. |

## Lineage

Four resolved commits changed `pl_dormant`. The earliest resolved change in 2025-07-09 altered perennial dormancy handling by changing LAI reduction to `Max(pldb(idp)%alai_min, rto * lai_init)`, simplifying leaf-loss logic, and later code in the same patch shows dormant biomass and residue updates still being maintained. A 2025-07-17 update then added `ly`, switched dormant residue additions to `soil1(j)%meta`, `soil1(j)%str`, and `soil1(j)%lig` when `bsn_cc%cswat == 2`, and explicitly reset `pcom(j)%plcur(ipl)%idorm`, `phuacc`, and `pcom(j)%plstr(ipl)%strsw` during perennial dormancy onset. The 2025-09-23 change removed those soil-fraction additions from this routine and left only the surface residue update. The 2026-01-07 change moved the dormant-season above-ground loss into `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot` instead of only `soil1(j)%rsd(1)`.

- 2025-07-09: perennial dormancy logic was revised to change LAI reduction behavior and simplify leaf-loss computation while preserving the dormant biomass transfer workflow.
- 2025-07-17: dormant-season onset for perennials began resetting dormancy and stress flags inside `pl_dormant`, and the routine also started adding dormant litter to soil fraction pools when `bsn_cc%cswat == 2`.
- 2025-09-23: the temporary soil-fraction litter additions were removed from `pl_dormant`, leaving the residue transfer to be handled elsewhere.
- 2026-01-07: dormant above-ground losses were additionally accumulated in `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot`, strengthening residue accounting within the plant mass module.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_dormant' has no extracted documentation comment.
- algorithm_steps revised: merged the source into 10 model steps to keep each step aligned with visible control-flow regions and line-number evidence.
- Source lineage was resolved from the provided Git Lineage Evidence; no unresolved commits were reported.
