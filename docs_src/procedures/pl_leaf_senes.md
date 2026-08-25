---
kind: procedure
symbol: pl_leaf_senes
title: pl_leaf_senes
status: filled
source_hash: 2ac6ca52cfc2898a
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects the current hydrologic response unit entry in
    `hru`, `pcom`, and `pl_mass` for the senescence update.
  idp: Plant database index taken from `pcom(j)%plcur(ipl)%idplt`; it points to the current
    plant definition record in `pldb` and controls which senescence rules and parameters are
    used.
  iob: Connectivity/object index resolved from `hru(j)%obj_no`; it is used to reach the weather-station
    linkage in `ob(iob)%wst` for moisture-triggered perennial senescence.
  iwgn: Weather generator index obtained from `wst(iwst)%wco%wgn`; it selects the generator
    statistics used to compute the precipitation-to-PET ratio for moisture-based leaf turnover.
  rto: Intermediate ratio used to scale LAI decline; for annuals it is `(1 - phuacc)/(1 -
    dphu)`, and for temperature-based perennials it is a linear countdown from a 15-day senescence
    window.
  ppet: Running precipitation-to-PET ratio from `wgn_pms(iwgn)%precip_sum / wgn_pms(iwgn)%pet_sum`;
    it drives the moisture-stress leaf turnover calculation.
  leaf_tov_mon: Monthly leaf turnover period computed from `ppet` and plant turnover limits;
    it is then converted to a daily turnover fraction for moisture-based perennials.
  coef: Coefficient in the moisture-response exponential expression for leaf turnover; here
    it is fixed at 1. to shape the transition when `ppet < 0.5`.
  exp_co: Exponent term in the moisture-response exponential expression; it is computed from
    `ppet` as `-10. * ppet + 6.` and then used in `exp(-exp_co)`.
  lai_init: Saved LAI before senescence update; it is used to compute the fractional LAI loss
    (`lai_drop`) before converting that loss into leaf biomass drop.
  lai_drop: Fractional LAI loss computed from the pre-senescence and post-senescence LAI values;
    it is bounded to 0-1 and used to limit the implied leaf biomass reduction in the temperature-triggered
    perennial path.
uses:
  plant_data_module: '`plant_data_module` provides the plant database records that define
    which senescence branch applies and the thresholds and limits for LAI decline and leaf
    turnover. Without `pldb`, the routine would not know the plant type, trigger mode, or
    the parameter values that shape the senescence equations.'
  basin_module: '`basin_module` matters because `bsn_cc%cswat` is the switch that historically
    controlled whether additional residue-pool partitioning was applied to falling leaf material.
    The lineage shows that this branch was later removed, so the basin setting remains relevant
    as an inherited dependency even though the current source no longer uses it in the active
    path.'
  hru_module: '`hru_module` supplies the current HRU index (`ihru`), the HRU table (`hru`),
    and the plant slot index (`ipl`) that locate the exact plant instance being updated. The
    routine cannot compute senescence or mass transfers without those indices because all
    plant and weather-linked state is stored per HRU and per plant within that HRU.'
  plant_module: '`plant_module` holds the per-plant status, growth, and mass pools that senescence
    updates. The routine reads current LAI and PHU accumulation to decide when senescence
    starts, adjusts `d_senes` and `leaf_tov` to model progression, and updates the plant nitrogen/phosphorus
    fractions used to compute falling leaf nutrient mass.'
  carbon_module: '`carbon_module` tracks how much carbon leaves the plant and enters residue
    during leaf senescence. `hrc_d(j)%plant_surf_c` records carbon added to surface residue,
    while `hpc_d(j)%drop_c` records the corresponding plant carbon loss from falling leaves.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` defines the `leaf_drop` mass
    object and the per-plant/community biomass pools that are reduced or increased by senescence.
    The routine uses those structures to move mass from living leaf, total, and above-ground
    pools into residue pools while preserving nitrogen, phosphorus, and carbon components.'
  climate_module: '`climate_module` provides the weather generator statistics used to estimate
    moisture stress for moisture-triggered perennials. The routine combines `wst(iwst)%wco%wgn`
    with `wgn_pms(iwgn)%precip_sum` and `wgn_pms(iwgn)%pet_sum` to compute `ppet`, which controls
    the turnover response.'
  hydrograph_module: '`hydrograph_module` connects the current HRU to its weather station
    through `ob(iob)%wst`. That mapping is required to find the correct station-specific weather
    generator inputs for the moisture-based senescence branch.'
---

<!-- facts:header -->

Computes leaf senescence and the resulting leaf biomass, residue, and carbon transfers for the current plant in an HRU. It handles annuals, temperature-triggered perennials, and moisture-triggered perennials with different senescence rules.

## Bottom Line

`pl_leaf_senes` updates plant leaf area index when senescence begins and converts the associated lost leaf tissue into falling leaf mass. It treats annuals, temperature-based perennials, and moisture-based perennials separately, using plant definition parameters and current weather-linked state to determine how much LAI declines.

When leaf drop is positive, the routine subtracts that mass from plant leaf, total, above-ground, and community biomass pools, adds it to fresh surface residue pools, and records the carbon gained by residue and plant-drop carbon trackers. Those updated masses are used later by residue and carbon accounting in the same simulation step and in subsequent process routines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during plant growth in `pl_grow`, immediately after `pl_leaf_gro` and before `pl_seed_gro` and `pl_partition`. `pl_grow` supplies the current HRU/plant context and has already advanced growth state for the day, so `pl_leaf_senes` can apply senescence using the updated PHU, LAI, and weather-linked conditions. Its results feed later residue and carbon bookkeeping, including plant mass pools, surface residue pools, and carbon gain/loss trackers used by downstream model accounting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize current HRU and plant IDs | Copies the active HRU index from `ihru`, resolves the plant database index from the current plant status record, and clears `leaf_drop%m` so each call starts with no accumulated falling leaf mass. |
| 2. handle annual plant senescence | If the plant type is a warm or cold annual, and PHU accumulation has passed the LAI-decline threshold but is still below maturity, the routine computes a decline ratio from PHU progress and resets LAI from the original LAI through the annual senescence curve. |
| 3. preserve pre-senescence LAI for annuals | Stores the current LAI in `lai_init`, computes `rto` from PHU progression, and applies the plant-specific decline exponent to `olai` to get the new annual LAI. |
| 4. handle temperature-based perennial senescence | For perennials triggered by temperature growth, the routine starts weather-linked senescence once PHU exceeds the threshold and the 15-day senescence counter is still active, then reduces LAI linearly toward `alai_min` while advancing `d_senes`. |
| 5. link perennial senescence to weather station | Uses the current HRU connectivity to find the weather station, stores the pre-senescence LAI, increments the day-since-senescence counter, and computes the remaining fraction of the 15-day decline period. |
| 6. convert temperature-based LAI loss to leaf drop | When the pre-senescence LAI is meaningful, it computes the fractional LAI drop, bounds it to 0-1, and turns that fraction into falling leaf mass using the current leaf biomass and plant nutrient fractions. |
| 7. handle moisture-based perennial senescence | For perennials triggered by moisture growth, it calculates precipitation-to-PET stress from the station weather generator, converts that to a monthly leaf turnover period, clamps it to the plant-specific bounds, and then turns it into a daily leaf turnover fraction that reduces LAI and generates leaf drop. |
| 8. update daily leaf turnover from moisture stress | When `ppet` is below the stress threshold, the routine uses an exponential response to interpolate between minimum and maximum turnover periods; otherwise it uses the minimum turnover period. It then updates `pcom(j)%plcur(ipl)%leaf_tov`, reduces LAI, and prevents LAI from falling below `alai_min`. |
| 9. compute nutrient-bearing leaf drop for moisture case | Uses the updated daily leaf turnover fraction to compute falling leaf biomass and its associated nitrogen and phosphorus masses, applying the same 0.68 nutrient scaling factor used for tree leaf drop. |
| 10. transfer leaf drop into residue and carbon pools | If any leaf mass dropped, the routine subtracts it from plant leaf, total, and above-ground pools, adds it to plant residue pools and community residue totals, and records the carbon transferred to residue and plant-drop accounting. |
| 11. exit | Returns to the caller after senescence-driven LAI and mass bookkeeping are complete for the current plant. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%typ, pldb(idp)%dlai, pldb(idp)%dlai_rate, pldb(idp)%trig, pldb(idp)%alai_min, pldb(idp)%leaf_tov_min, pldb(idp)%leaf_tov_max` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:hru_module] | `hru, ihru, ipl` | `hru(j)%obj_no` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%lai, pcom(j)%plg(ipl)%dphu, pcom(j)%plg(ipl)%olai, pcom(j)%plg(ipl)%d_senes, pcom(j)%plcur(ipl)%leaf_tov, pcom(j)%plm(ipl)%n_fr, pcom(j)%plm(ipl)%p_fr` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%alai_min, pldb(idp)%leaf_tov_min, pldb(idp)%leaf_tov_max, pldb(idp)%dlai, pldb(idp)%dlai_rate, pldb(idp)%typ, pldb(idp)%trig` |
| [sym:carbon_module] | `hrc_d, hpc_d` | `hrc_d(j)%plant_surf_c, hpc_d(j)%drop_c` |
| [sym:organic_mineral_mass_module] | `leaf_drop, pl_mass` | `leaf_drop%m, pl_mass(j)%leaf(ipl)%m, leaf_drop%n, leaf_drop%p, pl_mass(j)%leaf(ipl), pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%rsd(ipl), pl_mass(j)%rsd_tot, pl_mass(j)%tot_com, pl_mass(j)%ab_gr_com, pl_mass(j)%leaf_com, leaf_drop%c` |
| [sym:climate_module] | `wst, wgn_pms` | `wst(iwst)%wco%wgn, wgn_pms(iwgn)%precip_sum, wgn_pms(iwgn)%pet_sum` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `leaf_drop%m` | When `leaf_drop%m > 0.` after senescence calculations. | `leaf_drop%m` becomes the mass of leaf material that senesced and fell during this call, based on either the temperature-triggered or moisture-triggered pathway. It is then used to remove mass from the live plant pools and add it to residue and carbon accounting. |
| `pldb(idp)%typ` | It is read at the start of the routine to choose the current plant type branch; this routine does not change it. | `pldb(idp)%typ` identifies whether the current plant is an annual or perennial and therefore which senescence logic applies. It remains a database control value, not a computed state output. |
| `pcom(j)%plg(ipl)%lai` | When annual or perennial senescence reduces current LAI, especially in the temperature-based and moisture-based perennial branches. | `pcom(j)%plg(ipl)%lai` is reduced to represent the loss of leaf area as senescence progresses. This updated LAI affects later growth, canopy, and stress calculations for the same plant. |
| `iwst` | When the routine needs the weather-station mapping for a temperature- or moisture-based perennial; it is assigned from `hru(j)%obj_no` and then used to find `ob(iob)%wst`. | `iwst` is the weather-station index tied to the current HRU through `ob(iob)`. It matters because moisture-triggered senescence uses station-based weather generator statistics for precipitation and PET. |
| `pcom(j)%plg(ipl)%d_senes` | When the current plant is a temperature-based perennial and PHU exceeds the senescence threshold while the 15-day window is active. | `pcom(j)%plg(ipl)%d_senes` increments the number of days since senescence began. It governs how far through the fixed 15-day LAI decline the perennial has progressed. |
| `leaf_drop%n` | Whenever `leaf_drop%m` is computed from LAI decline and plant leaf mass in the senescence branches. | `leaf_drop%n` stores the nitrogen mass associated with the senesced leaf material. It is derived from leaf drop mass and plant nitrogen fraction so nutrient accounting can follow residue transfer. |
| `leaf_drop%p` | Whenever `leaf_drop%m` is computed from LAI decline and plant leaf mass in the senescence branches. | `leaf_drop%p` stores the phosphorus mass associated with the senesced leaf material. It is derived from leaf drop mass and plant phosphorus fraction for residue nutrient accounting. |
| `pcom(j)%plcur(ipl)%leaf_tov` | When the temperature-based perennial branch is active and the routine computes a fractional LAI loss from the pre- and post-senescence LAI values. | `pcom(j)%plcur(ipl)%leaf_tov` is used as a leaf-turnover fraction in the temperature-based path. It scales leaf biomass loss so the biomass drop matches the modeled LAI decline. |
| `pl_mass(j)%leaf(ipl)` | When `leaf_drop%m > 0.` and the routine subtracts falling leaf mass from the live leaf pool. | `pl_mass(j)%leaf(ipl)` is reduced by the senesced leaf mass so the live leaf biomass matches the updated canopy state. |
| `pl_mass(j)%tot(ipl)` | When `leaf_drop%m > 0.` and live biomass is reduced. | `pl_mass(j)%tot(ipl)` is reduced by the same falling leaf mass so the individual plant’s total biomass remains consistent with the loss of leaves. |
| `pl_mass(j)%ab_gr(ipl)` | When `leaf_drop%m > 0.` and the lost leaf mass is removed from above-ground live biomass. | `pl_mass(j)%ab_gr(ipl)` is reduced because fallen leaves are no longer part of above-ground living biomass. |
| `pl_mass(j)%rsd(ipl)` | When `leaf_drop%m > 0.` and the fallen leaf mass is routed into surface residue accounting. | `pl_mass(j)%rsd(ipl)` increases by the senesced leaf mass, representing fresh surface residue associated with that plant. |
| `pl_mass(j)%rsd_tot` | When `leaf_drop%m > 0.` and residue is accumulated. | `pl_mass(j)%rsd_tot` increases to keep the total fresh surface residue for the plant community consistent with the leaf material that fell. |
| `pl_mass(j)%tot_com` | When `leaf_drop%m > 0.` and community biomass is updated. | `pl_mass(j)%tot_com` is reduced so the community-wide biomass total reflects the transferred leaf mass. |
| `pl_mass(j)%ab_gr_com` | When `leaf_drop%m > 0.` and above-ground community biomass is updated. | `pl_mass(j)%ab_gr_com` is reduced to remove the senesced leaf mass from the community above-ground live biomass total. |
| `pl_mass(j)%leaf_com` | When `leaf_drop%m > 0.` and the community leaf pool is updated. | `pl_mass(j)%leaf_com` is reduced because the plant community has less living leaf biomass after senescence. |
| `hrc_d(j)%plant_surf_c` | When `leaf_drop%m > 0.` and carbon from the lost leaves is credited to residue. | `hrc_d(j)%plant_surf_c` increases by the carbon contained in the fallen leaves, tracking carbon transferred to surface residue. |
| `hpc_d(j)%drop_c` | When `leaf_drop%m > 0.` and plant carbon loss from leaf drop is recorded. | `hpc_d(j)%drop_c` increases by the same carbon amount to record carbon leaving the plant through leaf senescence and drop. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.1.19 | Annual LAI senescence after onset fraction | $LAI=LAI_{mx}*\frac{(1-fr_{PHU})}{(1-fr_{PHU,sen})}$ | After phuacc exceeds dlai, annual LAI declines from olai as olai*((1-phuacc)/(1-dphu))^dlai_rate. This is a generalized senescence curve rather than the simple linear ratio printed on the theory page. |
| 5:2.1.20 | Tree LAI senescence | $LAI=(\frac{yr_{cur}}{yr_{fulldev}})*LAI_{mx}*\frac{(1-fr_{PHU})}{(1-fr_{PHU,sen})}$ | Temperature-based perennials use a 15-day linear decline toward alai_min after senescence starts, not the printed year-scaled LAImax expression. |

## Lineage

Resolved lineage shows five behavior-changing commits for `pl_leaf_senes`. In 2024-05-30, the source was added with annual, temperature-based perennial, and moisture-based perennial senescence branches. In 2024-08-08, the routine was initialized with explicit zero values for its local scalars, and the leaf-drop nutrient formulas were changed to use a 0.68 scaling factor for N and P. In 2024-10-08, the annual senescence branch was left structurally the same but the code comment-and-formula context shows the leaf-drop calculation was still commented out there, while temperature-based perennial leaf-drop calculations remained active. In 2024-12-05, residue handling was refactored from `rsd1` to `soil1` and the routine started updating `pl_mass(j)%tot_com`, `ab_gr_com`, and `leaf_com` after leaf drop. In 2026-01-07, the active residue transfer changed from `soil1(j)%rsd(1)` to `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot`, removing the direct `soil1` update from this routine.

- Added the initial `pl_leaf_senes` implementation with annual, temperature-triggered perennial, and moisture-triggered perennial senescence logic, including LAI decline and falling-leaf mass generation.
- Initialized all local working variables to zero and changed the nutrient formulas for falling leaves to apply the 0.68 nitrogen/phosphorus scaling factor.
- Refactored residue handling to update `soil1` and community biomass totals when leaf drop occurs, adding `tot_com`, `ab_gr_com`, and `leaf_com` updates.
- Removed direct `soil1` residue partitioning from this routine so residue carbon partitioning is handled elsewhere, while keeping the community biomass removals and carbon trackers.
- Switched leaf-drop residue accumulation from `soil1(j)%rsd(1)` to the plant-community residue pools `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_leaf_senes' has no extracted documentation comment.
