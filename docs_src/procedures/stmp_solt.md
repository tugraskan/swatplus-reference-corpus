---
kind: procedure
symbol: stmp_solt
title: stmp_solt
status: filled
source_hash: b3512734adf5e6d4
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects which HRU and associated soil, residue, snow,
    and septic-state data this call updates.
  k: Loop counter over soil layers in the current HRU.
  f: Reusable intermediate factor for exponential/logarithmic damping-depth calculations.
  dp: Maximum damping depth computed from average bulk density; it is the base depth scale
    before moisture adjustment.
  ww: Intermediate soil-water scaling term used to form the daily damping depth denominator.
  b: Intermediate logarithm term used in the daily damping-depth calculation.
  wc: Soil-water scaling factor that adjusts the daily damping depth based on profile water
    content.
  dd: Daily damping depth used to scale the depth factor for each soil layer.
  xx: Running depth accumulator used to compute the center depth of each soil layer; later
    reused as a snow-cover factor in the snow branch.
  st0: Surface radiation term derived from daily solar radiation and albedo; it drives bare-soil
    surface temperature.
  tlag: Lag coefficient for soil temperature, fixed at 0.8, blending yesterday's layer temperature
    with today's forcing.
  df: Depth factor that attenuates the influence of the surface temperature with depth.
  zd: Dimensionless depth ratio for the current layer center relative to the daily damping
    depth.
  bcv: Lagging factor that blends bare-soil and covered-surface temperature effects, taking
    residue cover and snow into account.
  tbare: Bare-soil surface temperature calculated from air temperature and daily radiation
    forcing.
  tcov: Soil-surface temperature corrected for cover, blending bare-soil and the upper soil
    temperature.
  cover: Total surface cover mass used to compute the residue lag factor, formed from above-ground
    biomass and total surface residue.
uses:
  climate_module: '`climate_module` provides the daily weather forcing and annual temperature
    baseline that drive the soil-temperature equations. `w%solrad`, `w%tave`, `w%tmax`, and
    `w%tmin` determine the day’s surface forcing, while `wgn_pms(iwgen)%tmp_an` supplies the
    annual mean air temperature used in the recursive layer update.'
  septic_data_module: '`septic_data_module` matters because this routine checks whether a
    septic system is active for the current HRU and whether the current year is within its
    operational window before adjusting soil temperature in affected layers.'
  hru_module: '`hru_module` supplies the current HRU index, snow amount, septic linkage, and
    snow/land-management attributes that determine which branch of the temperature logic runs.
    `hru(j)%sno_mm` directly affects the cover lag factor, and `iseptic`, `i_sep`, `ihru`,
    `iwgen`, and `albday` are the control values this routine reads.'
  soil_module: '`soil_module` matters because the routine reads profile-average bulk density,
    profile soil water, layer thickness, layer count, and per-layer temperatures, then updates
    the surface temperature and each layer temperature in place.'
  time_module: '`time_module` matters because septic-system temperature corrections only apply
    once the simulation year has reached the septic system’s start year.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the residue and above-ground
    biomass masses that define the surface cover used in the cover lag factor. That cover
    value changes how much the bare-soil surface temperature is moderated before layer temperatures
    are updated.'
---

<!-- facts:header -->

Estimates daily average soil temperature at the bottom of each soil layer for each HRU. It combines weather, snow/cover, soil-water, and septic-system conditions to update layer temperatures and the soil surface temperature state.

## Bottom Line

`stmp_solt` calculates the daily damping depth, surface temperature, and layer-by-layer soil temperature profile for the current HRU. The routine uses average annual air temperature, daily solar radiation, soil bulk density, soil water, snow, and plant residue/biomass cover to drive the recursive temperature update.

The results matter because other processes use the updated soil-layer temperatures and the stored surface temperature. In particular, the routine also applies a special correction for septic-system HRUs when the septic option is active and a layer is warmer than the septic threshold.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`stmp_solt` is called from `hru_control` immediately after the code finishes HRU-level reaction and sorption processing and before canopy interception and snowmelt are computed. `hru_control` has already established the current HRU context (`ihru`, `iwgen`, `albday`, `iseptic`, `i_sep`) and the daily weather state, so this routine can update soil temperatures for the rest of the daily process sequence.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU context and lag constant | Copy the current HRU index from `ihru` into `j` and fix the soil-temperature lag coefficient at 0.8 for the recursive update. |
| 2. compute maximum damping depth | Use current soil average bulk density to calculate the maximum damping depth `dp` with the exponential SWAT soil-temperature relationship. |
| 3. compute soil-water scaling | Derive the soil-water scaling factor `wc` from profile water storage, average bulk density, and total profile depth. |
| 4. compute daily damping depth | Convert the maximum damping depth into the daily damping depth `dd` using the moisture scaling factor and a logarithmic adjustment. |
| 5. compute cover lag factor | Form surface cover from above-ground biomass and total residue, then combine residue cover with any snow cover to obtain the larger lag factor `bcv`. |
| 6. compute surface forcing terms | Reset surface-temperature intermediates, compute the radiation forcing term `st0`, calculate bare-soil temperature `tbare`, compute covered-surface temperature `tcov`, and store the surface temperature state in `soil(j)%tmp_srf` as the average of bare and covered values. |
| 7. update each soil layer temperature | Loop through all soil layers, compute each layer center depth and depth factor, then update `soil(j)%phys(k)%tmp` by blending yesterday’s layer temperature with today’s forcing driven by annual air temperature and the stored surface temperature. |
| 8. apply septic correction when active | Look up the HRU’s septic-system index, test whether the septic system is active in the current year and layer range, and if a qualifying layer is colder than 10 C, raise it toward 10 C with a partial correction. |
| 9. finish the routine | Exit after all layers have been processed and any septic adjustment has been applied. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `w, wgn_pms` | `w%solrad, w%tave, w%tmax, w%tmin, wgn_pms(iwgen)%tmp_an` |
| [sym:septic_data_module] | `sep` | `sep(isep)%opt, sep(isep)%yr` |
| [sym:hru_module] | `hru, iseptic, i_sep, ihru, iwgen, albday, isep` | `hru(j)%sno_mm` |
| [sym:soil_module] | `soil` | `soil(j)%avbd, soil(j)%sw, soil(j)%tmp_srf, soil(j)%phys(2)%tmp, soil(j)%nly, soil(j)%phys(k)%d, soil(j)%phys(k)%tmp` |
| [sym:time_module] | `time` | `time%yrc` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%rsd_tot%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(j)%tmp_srf` | After computing `tbare` and `tcov` for the current HRU, before the layer loop. | Stores the daily soil-surface temperature used as the forcing term for all layer-temperature updates in this HRU. |
| `soil(j)%phys(k)%tmp` | For each layer `k` during the soil-layer loop, after the depth factor is computed. | Updates the layer’s daily average temperature by blending the previous value with the annual-air/surface-temperature forcing. If the septic correction condition is met later in the same loop, the value is further nudged upward toward 10 C for affected layers. |
| `isep` | When the current HRU has a septic mapping and the septic system is active, the simulation year has reached the septic start year, and the loop is at or below the septic-affected layer index. | Holds the septic-system index for the current HRU so the routine can test the proper septic record before adjusting soil temperatures. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:1.3.1.9 | Bare-soil surface temperature | $T_{bare}=\overline T_{av}+\varepsilon_{sr} \frac{(T_{mx}-T_{mn})}{2}$ | Verified against SWAT+ 62.0.0 (stmp_solt.f90:106). tbare = tave + 0.5*(tmax-tmin)*st0` (eq 2.3.9); ε_sr = st0 |
| 1:1.3.2 | Soil temperature (analytical form) | $T_{soil}(z,d_n)=\overline T_{AA} +A_{surf}exp(-z/dd)sin(\omega_{tmp}d_n-z/dd)$ | Verified against SWAT+ 62.0.0 (stmp_solt.f90:126). code uses empirical depth-lag `df=zd/(zd+Exp(-.8669-2.0775*zd))`, NOT the analytical sine-wave solution shown in theory |
| 1:1.3.3 | Soil temperature (recursive form) | $T_{soil}(z,d_n)=\ell T_{soil}(z,d_n1)+[1.0-\ell] [df [\overline T_{AAair}-T_{ssurf}]+T_{ssurf}]$ | Verified against SWAT+ 62.0.0 (stmp_solt.f90:126). empirical-lag soil temp `tlag*tmp+(1-tlag)*(df*(tmp_an-tmp_srf)+tmp_srf)` — the form the code ACTUALLY uses (cf. 1:1.3.2 sine = outdated) |
| 1:1.3.4 | Depth factor df | $df=\frac{zd}{zd+exp(-0.867-2.078 zd)}$ | Verified against SWAT+ 62.0.0 (stmp_solt.f90). |
| 1:1.3.5 | Depth ratio zd | $zd=\frac{z}{dd}$ | Verified against SWAT+ 62.0.0 (stmp_solt.f90:122). zd = zd/dd` (eq 2.3.5) |
| 1:1.3.6 | Maximum damping depth | $dd_{max} = 1000+\frac{2500\rho_b}{\rho_b+686exp(-5.63\rho_b)}$ | dp = 1000 + 2500*avbd/(avbd+686*exp(-5.63*avbd)). |
| 1:1.3.7 | Soil-water scaling phi | $\varphi=\frac{SW}{(0.356-0.144\rho_b) z_{tot}}$ | wc = sw/((0.356-0.144*avbd)*z_tot). |
| 1:1.3.8 | Daily damping depth | $dd=dd_{max} exp[ln(\frac{500}{dd_{max}}) (\frac{1-\varphi}{1+\varphi})^2]$ | dd = exp(log(500/dp)*((1-wc)/(1+wc))^2)*dp. |
| 1:1.3.10 | Surface radiation term | $\varepsilon_{sr}=\frac{H_{day} (1-\alpha)-14}{20}$ | st0 = (solrad*(1-albday) - 14)/20. |
| 1:1.3.11 | Cover lag factor bcv | $bcv=max \{{{\frac{CV}{CV+exp(7.563-1.297X10^-4*CV)}}}, \frac{SNO}{SNO+exp(6.055-0.3002*SNO)}\}$ | bcv = cover/(cover+exp(7.563-1.297e-4*cover)), max with snow term. |
| 1:1.3.12 | Soil-surface temperature | $T_{ssurf}=bcv T_{soil}(1,d_n-1)+(1-bcv) T_{bare}$ | Verified against SWAT+ 62.0.0 (stmp_solt.f90:108). tcov = bcv*phys(2)%tmp + (1-bcv)*tbare` (eq 2.3.12) |

## Lineage

Resolved lineage evidence shows five behavior changes to `stmp_solt`: a 2024 refactor tied the routine to the new `soil1`/residue structure, a 2024 fix corrected a typo in the soil-temperature comments, a 2024 tab cleanup preserved the septic correction logic, a 2025 change renamed the surface-temperature local to `soil(j)%tmp_srf`, and a 2026 change switched the cover calculation from a single residue field to total residue mass in `pl_mass(j)%rsd_tot%m`.

- Switched the cover term from `soil1(j)%rsd(1)%m`/`rsd1(j)%tot_com%m` to `pl_mass(j)%rsd_tot%m`, changing how residue cover contributes to the lag factor.
- Stored surface temperature in `soil(j)%tmp_srf` instead of a local variable, so the HRU soil profile now retains the computed surface temperature for downstream use.
- Kept the septic-system temperature adjustment intact while cleaning formatting, preserving the active-year and layer-threshold gate on the correction.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'stmp_solt' has no extracted documentation comment.
