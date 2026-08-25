---
kind: procedure
symbol: sep_biozone
title: sep_biozone
status: filled
source_hash: fd336059a9e766b1
version_label: SWAT+ 62.0.0
locals:
  bz_lyr: Index of the soil layer where the biozone sits for the current HRU; used to read
    and update the biozone layer in both the soil physics arrays and the soil mass pools.
  isp: Septic system type for the current HRU, taken from `sep(isep)%typ` and used to look
    up septic effluent composition and process coefficients from `sepdb`.
  j: Current HRU index, copied from `ihru`, so the routine can read and write the per-HRU
    arrays for soil, septic, and pathogen state.
  nly: Number of layers in the current HRU soil profile, copied from `soil(j)%nly`; used when
    computing the lower boundary depth for sorption-related calculations.
uses:
  septic_data_module: '`septic_data_module` supplies the septic-system definition for the
    current HRU. `sep(isep)` provides the operation flag, timing limit, geometry, and process
    coefficients that control whether the routine does nothing, resets a failed system, or
    updates active biozone chemistry and biomass.'
  basin_module: '`hru_module` holds the per-HRU indices and septic output state that this
    routine reads and writes. It provides the current HRU id, the septic system assignment,
    flow-perc values, failure counters, and the biomass/pathogen/plaque arrays that are updated
    here and later reused by other HRU processes.'
  pathogen_data_module: '`pathogen_data_module` supplies the septic effluent concentration
    database used to convert septic water volume into added nutrients, BOD, total suspended
    solids, and fecal coliform loading for the biozone.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` contains the soil-layer mineral
    and organic mass pools that receive septic loading and then lose mass through nitrification,
    denitrification, percolation, and phosphorus sorption. These are the core biozone chemistry
    states this routine updates.'
  hru_module: '`hru_module` matters because the biozone calculations are done per HRU and
    use the HRU area to convert between layer water volumes, septic inflow/outflow, and areal
    mass units. The routine also writes back HRU-level septic outputs such as biomass, plaque,
    BOD, and fecal coliform.'
  soil_module: '`soil_module` provides the soil profile geometry and physical properties for
    the biozone layer. The routine needs layer count, storage, porosity, field capacity, wilting
    point, saturation, thickness, and bottom depth to decide when the biozone saturates, when
    the system fails, and how much sorption space remains.'
  time_module: '`time_module` matters because the caller only invokes `sep_biozone` when the
    current simulation year is at or beyond the septic system’s start year, so this routine’s
    effects are gated by simulation time.'
---

<!-- facts:header -->

Updates septic biozone state for a septic HRU: it handles failing systems, then for active systems it adds septic tank effluent to soil pools, updates biozone water and chemistry, and adjusts biomass, plaque, and pathogen indicators.

## Bottom Line

`sep_biozone` is the septic biozone process routine. It runs for septic HRUs when the septic system is active enough to process and the soil temperature gate in the caller allows it, then applies the day’s septic tank effluent to the biozone layer and updates water storage, mineral N and P pools, BOD, fecal coliform, plaque, and live bacteria biomass.

It also handles the special failing-system case: if the septic system is marked failing, it counts failure days and, once the failure duration is reached, restores the system to active operation and resets the biozone soil and mass states. The results feed later septic and HRU behavior through the shared `hru_module`, `soil_module`, `organic_mineral_mass_module`, and `septic_data_module` state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

The caller `hru_control` sets `isep = iseptic(j)` and checks that the septic system is operational for the current year and that the biozone soil temperature is above zero before calling this routine. `sep_biozone` then performs the day’s septic biozone updates; later HRU and septic routines depend on the updated shared biomass, plaque, BOD, fecal coliform, and soil nutrient states.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load HRU and septic context | Copy the current HRU index and its septic-system, soil-layer, and geometry state into local variables; compute biozone area, volume, initial water, inflow, outflow, and starting nutrient concentrations. |
| 2. handle failing system | If the septic system is marked failing, increment the failure-duration counter, and once the failure period reaches the configured limit, restore the system to active status and reset the biozone soil and mass pools before returning immediately. |
| 3. add septic effluent to soil pools | Convert septic tank effluent volume to areal mass and add nitrate, ammonium, organic N, organic P, labile P, and BOD to the biozone soil pools using the septic effluent database for the current septic type. |
| 4. update biozone field capacity and saturation | Adjust the biozone field capacity from the septic coefficients and biomass, recompute saturated water content from thickness and plaque, and force saturation up to field capacity; if saturation falls to or below field capacity, mark the septic system as failing. |
| 5. compute bacterial losses and plaque buildup | Compute respiration, mortality, and slough-off rates from the septic coefficients and current biomass, then accumulate plaque from biomass losses and incoming suspended solids. |
| 6. mix fecal coliform with biozone water | Blend septic fecal coliform concentration into the biozone using a volumetric averaging step based on the current soil water and septic inflow volumes. |
| 7. compute reaction rate scaling | Form the biomass-based reaction-rate factor and use it to compute BOD and fecal coliform decay rates, capping the BOD reaction rate to avoid unrealistically large daily losses. |
| 8. nitrify ammonium and move ammonium downward | Use the nitrification rate to convert part of biozone ammonium to nitrate, then move some ammonium to the layer below by percolation. |
| 9. denitrify nitrate | Use the denitrification rate to remove part of the biozone nitrate pool. |
| 10. compute phosphorus sorption capacity | Compute the soil volume below the biozone and the maximum phosphorus sorption potential, then cap labile phosphorus at the sorption limit and shift any excess into the active phosphorus pool. |
| 11. percolate soluble phosphorus | Recalculate soluble phosphorus concentration after sorption, then move a portion of labile phosphorus downward to the next soil layer by percolation. |
| 12. finalize nutrient and biomass outputs | Store the end-of-day ammonium, nitrate, and labile phosphorus values and update live biozone biomass by adding the computed daily biomass change. |
| 13. return to caller | Exit after all septic biozone updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `sep` | `sep(isep)%typ, sep(isep)%thk, sep(isep)%opt, sep(isep)%fc1, sep(isep)%fc2, sep(isep)%rsp, sep(isep)%mrt, sep(isep)%slg1, sep(isep)%plq, sep(isep)%z, sep(isep)%psorpmax, sep(isep)%solpslp, sep(isep)%solpintc` |
| [sym:basin_module] | `hru, ihru, i_sep, iseptic, qstemm, bz_perc, isep, sep_tsincefail, biom, plqm, bio_bod, fcoli, rbiom` | `hru(j)%area_ha; i_sep(j); iseptic(j); qstemm(j); bz_perc(j); sep_tsincefail(j); biom(j); plqm(j); bio_bod(j); fcoli(j); rbiom(j); ihru; isep` |
| [sym:pathogen_data_module] | `sepdb` | `sepdb(sep(isep)%typ)%no3concs, sepdb(sep(isep)%typ)%no2concs, sepdb(sep(isep)%typ)%nh4concs, sepdb(sep(isep)%typ)%orgnconcs, sepdb(sep(isep)%typ)%orgps, sepdb(sep(isep)%typ)%minps, sepdb(sep(isep)%typ)%bodconcs, sepdb(sep(isep)%typ)%tssconcs, sepdb(sep(isep)%typ)%fcolis` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(bz_lyr)%nh4, soil1(j)%mn(bz_lyr)%no3, soil1(j)%mp(bz_lyr)%lab, soil1(j)%hsta(bz_lyr)%n, soil1(j)%hsta(bz_lyr)%p, soil1(j)%tot(bz_lyr)%p, soil1(j)%mp(bz_lyr)%act, soil1(j)%tot(bz_lyr)%n, soil1(j)%mn(bz_lyr+1)%nh4, soil1(j)%mp(bz_lyr+1)%lab` |
| [sym:hru_module] | `hru, sep_tsincefail, bz_perc, rbiom, iseptic, i_sep, qstemm, biom, plqm, bio_bod, fcoli, ihru, isep` | `hru(j)%area_ha` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(bz_lyr)%st, soil(j)%ly(bz_lyr-1)%prk, soil(j)%phys(bz_lyr)%ul, soil(j)%phys(bz_lyr)%por, soil(j)%phys(bz_lyr)%wp, soil(j)%phys(bz_lyr)%fc, soil(j)%phys(bz_lyr)%up, soil(j)%phys(nly)%d` |
| [sym:time_module] | `time%yrc` | `time%yrc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `isep` | When `sep(isep)%opt == 2` and `sep_tsincefail(j) >= sep(isep)%tfail`. | The routine clears the failure state by resetting the septic system to active operation after the configured failure duration ends. |
| `bza` | When the routine computes `bza = hru(j)%area_ha` near the start of the subroutine. | `bza` is the biozone area for the current HRU, used as the conversion basis between layer volumes, loads, and areal mass units. |
| `bz_vol` | When the routine computes `bz_vol = sep(isep)%thk * bza * 10.`. | `bz_vol` is the biozone volume derived from septic thickness and HRU area, and it is used to scale the biomass reaction-rate factor. |
| `qlyr` | When the routine assigns `qlyr = qstemm(j)` and later uses percolation volume from `bz_perc(j)` in the active-system branch. | `qlyr` captures the septic water entering the biozone layer for this HRU; it is part of the water-balance context for subsequent loading and reaction calculations. |
| `qsrf` | When the routine initializes `qsrf = 0` and uses the active-system water balance rather than surface runoff. | `qsrf` is set to zero here because this routine is concerned with septic biozone exchange rather than direct surface runoff routing. |
| `ctmp` | When the routine sets `ctmp = 1.`. | `ctmp` is the temperature correction factor for bacteria and decay processes; here it is fixed at 1, so no temperature scaling is applied. |
| `qi` | When the routine computes `qi = (soil(j)%phys(bz_lyr)%st + soil(j)%ly(bz_lyr-1)%prk + qstemm(j)) * bza * 10.`. | `qi` is the initial biozone water volume used to convert between concentration units and areal mass for septic loading and reaction calculations. |
| `qin` | When the routine computes `qin = qstemm(j) * bza * 10.`. | `qin` is the septic tank effluent inflow volume applied to the biozone for the current day. |
| `qout` | When the routine computes `qout = bz_perc(j) * bza * 10.`. | `qout` is the leaching or percolation volume leaving the biozone and is used in pathogen, nutrient, and phosphorus loss calculations. |
| `hvol` | When the routine computes `hvol = soil(j)%phys(bz_lyr)%st * bza * 10.`. | `hvol` is the ending water volume stored in the biozone layer after the day’s setup, used as a summary of current biozone storage. |
| `rtof` | When the routine assigns `rtof = 0.5`. | `rtof` is the fixed partition factor that splits septic organic N and P additions between fresh/stable organic pools in the biozone. |
| `nh3_init` | When the routine sets `nh3_init = soil1(j)%mn(bz_lyr)%nh4` before loading septic effluent. | `nh3_init` captures the starting ammonium pool in the biozone so later calculations can measure how septic loading and nitrification changed it. |
| `no3_init` | When the routine sets `no3_init = soil1(j)%mn(bz_lyr)%no3` before loading septic effluent. | `no3_init` captures the starting nitrate pool in the biozone for the same before/after comparison. |
| `solp_init` | When the routine sets `solp_init = soil1(j)%mp(bz_lyr)%lab` before loading septic effluent. | `solp_init` records the starting labile phosphorus in the biozone so the routine can track sorption and percolation changes. |
| `if(sep_tsincefail(j)>0)sep_tsincefail(j)` | When `sep_tsincefail(j) > 0` during a failing-system step. | The failure counter is incremented to track how long the septic system has been in failure mode. |
| `sep(isep)%opt` | When the routine detects a failing system and later when saturation forces `sep(isep)%opt = 2` in the active-system path. | `sep(isep)%opt` switches between active and failing operation, controlling whether the routine processes effluent or exits after failure handling. |
| `soil(j)%phys(bz_lyr)%ul` | When the routine resets the failing system back to active operation. | `soil(j)%phys(bz_lyr)%ul` is recomputed from septic biozone thickness and soil porosity/wilting point so the restored biozone has the correct saturated storage limit. |
| `soil(j)%phys(bz_lyr)%fc` | When the routine resets the failing system back to active operation. | `soil(j)%phys(bz_lyr)%fc` is recomputed from septic biozone thickness and the updated field-capacity relationship so the restored system has a valid water-content threshold. |
| `soil1(j)%mn(bz_lyr)%nh4` | When septic effluent is added and later when nitrification and failure reset occur. | `soil1(j)%mn(bz_lyr)%nh4` increases from septic ammonium loading and then decreases through nitrification, percolation, or failure reset. |
| `soil1(j)%mn(bz_lyr)%no3` | When septic effluent is added and later when nitrification and denitrification occur. | `soil1(j)%mn(bz_lyr)%no3` increases from septic nitrate loading and nitrification, then decreases through denitrification or failure reset. |
| `soil1(j)%hsta(bz_lyr)%n` | When septic effluent is partitioned into organic nitrogen and the system is reset on failure. | `soil1(j)%hsta(bz_lyr)%n` receives the stable/stored portion of septic organic nitrogen and is cleared if the septic system is restored after failure. |
| `soil1(j)%hsta(bz_lyr)%p` | When septic effluent is partitioned into organic phosphorus and the system is reset on failure. | `soil1(j)%hsta(bz_lyr)%p` receives the stable/stored portion of septic organic phosphorus and is cleared if the septic system is restored after failure. |
| `soil1(j)%tot(bz_lyr)%p` | When septic effluent is partitioned into organic phosphorus and the system is reset on failure. | `soil1(j)%tot(bz_lyr)%p` captures the total organic phosphorus pool in the biozone and is cleared if the system is returned from failure to active operation. |
| `soil1(j)%mp(bz_lyr)%lab` | When soluble phosphorus loading and sorption calculations run, and when the failing system is reset. | `soil1(j)%mp(bz_lyr)%lab` increases from septic labile phosphorus input, is reduced by sorption and percolation, and is zeroed on failure reset to restore the biozone state. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved. `df07e3f` introduced `sep_biozone.f90` with the full septic biozone algorithm. `94b6dec` imported the same source from Bitbucket without changing the algorithm. `39fabde` initialized the local variables with explicit `:: = 0` defaults, which changed declarations but not the process logic. `889136d` corrected a typo in the purpose comment from "occuring" to "occurring". `dab22e1` commented out the unused `1000` format label at the end of the file.

- `df07e3f`: added the septic biozone subroutine and its active/failing-system processing, including nutrient, BOD, fecal-coliform, plaque, and biomass updates.
- `39fabde`: changed local declarations to initialized forms such as `integer :: bz_lyr = 0` and `real*8 :: ... = 0.d0`, making the routine’s locals explicitly initialized before use.
- `889136d`: updated the header documentation comment spelling from "occuring" to "occurring" without changing runtime behavior.
- `dab22e1`: removed the active Fortran format label by commenting it out, leaving the executable septic biozone logic unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sep_biozone' has no extracted documentation comment.
- algorithm_steps revised: condensed the initial setup into one step and separated the active-system calculations into distinct process steps to match the visible control flow.
- Source shows `basin_module` and `pathogen_data_module` are used but no candidate outside references were resolved for them in the packet, so their module-level components are not enumerated beyond the extracted septic database and caller-visible state.
- The caller snippet shows the `time%yrc` gate in `hru_control`; the routine itself does not read time values in the visible source, so the `time_module` dependency is documented as caller-gated rather than direct internal use.
