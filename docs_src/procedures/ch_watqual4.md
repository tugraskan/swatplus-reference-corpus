---
kind: procedure
symbol: ch_watqual4
title: ch_watqual4
status: filled
source_hash: 7d6cfd562927a98e
version_label: SWAT+ 62.0.0
locals:
  theta: Temperature-correction function used to scale reaction and exchange rates from 20°C
    to the current water temperature.
  wq_k2m: Helper that converts a k-term reaction rate into the matching m-term for the semi-analytic
    update.
  wq_semianalyt: Semi-analytic QUAL2E concentration updater used to advance concentrations
    over the timestep.
  tday: Effective timestep in days, derived from reach travel time and capped at 1 day.
  wtmp: Estimated stream water temperature used in temperature-dependent reaction calculations.
  fll: Light-limitation factor for algal growth.
  gra: Local algal growth rate selected from the growth-option logic.
  lambda: Light extinction coefficient including algal self-shading.
  fnn: Nitrogen limitation factor for algal growth.
  fpp: Phosphorus limitation factor for algal growth.
  algi: Daylight-averaged photosynthetically active light intensity.
  fl_1: Intermediate term in the light-attenuation calculation.
  xx: Intermediate term used in the dissolved oxygen saturation formula and later phosphorus
    update.
  yy: Intermediate term used in the dissolved oxygen saturation formula and later phosphorus
    update.
  zz: Intermediate term used in the dissolved oxygen saturation formula and later phosphorus
    update.
  ww: Intermediate term used in the dissolved oxygen saturation formula.
  cordo: Low-oxygen correction factor for nitrification-related oxygen demand.
  f1: Fraction of algal nitrogen uptake assigned to ammonia rather than nitrate.
  algcon: Current algal biomass concentration expressed from chlorophyll-a.
  thgra: Temperature factor for algal growth rate correction.
  thrho: Temperature factor for algal respiration rate correction.
  thrs1: Temperature factor for algal settling rate correction.
  thrs2: Temperature factor for benthic dissolved phosphorus source correction.
  thrs3: Temperature factor for benthic ammonia source correction.
  thrs4: Temperature factor for organic nitrogen settling correction.
  thrs5: Temperature factor for organic phosphorus settling correction.
  thbc1: Temperature factor for ammonia-to-nitrite oxidation.
  thbc2: Temperature factor for nitrite-to-nitrate oxidation.
  thbc3: Temperature factor for organic nitrogen hydrolysis.
  thbc4: Temperature factor for organic phosphorus decay.
  thrk1: Temperature factor for CBOD deoxygenation.
  thrk2: Temperature factor for reaeration.
  thrk3: Temperature factor for CBOD settling loss.
  thrk4: Temperature factor for sediment oxygen demand.
  soxy: Dissolved oxygen saturation concentration at the current water temperature.
  rs2_s: Temperature-corrected benthic dissolved phosphorus source term scaled by benthic
    area.
  rs3_s: Temperature-corrected benthic ammonia source term scaled by benthic area.
  rk4_s: Temperature-corrected sediment oxygen demand term scaled by benthic area.
  disoxin: Incoming dissolved oxygen concentration after benthic oxygen demand adjustment.
  dispin: Incoming soluble phosphorus concentration after benthic source adjustment.
  ammoin: Incoming ammonia concentration after benthic source adjustment.
  cinn: Effective available nitrogen pool used for algal growth limitation.
  algin: Incoming algal biomass concentration used as the starting concentration for the semi-analytic
    update.
  factk: Kinetic coefficient passed into the semi-analytic solver for the current process.
  alg_m1: Semi-analytic helper value for algal biomass change used in oxygen accounting.
  alg_m: Semi-analytic helper value for algal biomass change used in nutrient and oxygen accounting.
  alg_m2: Difference between the two algal semi-analytic helper values, used for oxygen production/uptake.
  alg_no3_m: Algal nitrate uptake term.
  alg_nh4_m: Algal ammonia uptake term.
  alg_p_m: Algal phosphorus uptake term.
  alg_set: Algal settling loss term.
  algcon_out: End-of-day algal biomass concentration after growth and settling.
  cbodo: Limited carbonaceous oxygen demand used as a mass cap.
  cbodoin: Limited carbonaceous oxygen demand used as a mass cap.
  rk1_k: Temperature-corrected CBOD deoxygenation rate in k-form.
  rk1_m: CBOD deoxygenation m-term used in the semi-analytic update.
  rk3_k: Temperature-corrected CBOD settling loss rate in k-form.
  factm: Source/sink term passed into the semi-analytic solver for the current process.
  bc1_k: Temperature-corrected ammonia oxidation rate.
  bc3_k: Temperature-corrected organic nitrogen hydrolysis rate.
  rs4_k: Temperature-corrected organic nitrogen settling rate scaled by depth.
  bc3_m: Semi-analytic m-term for organic nitrogen hydrolysis.
  rk2_m: Temperature-corrected reaeration m-term.
  rk2_k: Temperature-corrected reaeration k-term.
  alg_m_o2: Oxygen demand or production contribution from algal biomass change.
  bc2_k: Temperature-corrected nitrite oxidation rate with sign convention for the solver.
  bc1_m: Semi-analytic m-term for ammonia oxidation.
  bc2_m: Semi-analytic m-term for nitrite oxidation.
  bc4_k: Temperature-corrected organic phosphorus decay rate.
  bc4_m: Semi-analytic m-term for organic phosphorus decay.
  rs5_k: Temperature-corrected organic phosphorus settling rate scaled by depth.
  flo_rate: Flow rate in cubic meters per second used to interpolate the rating curve.
  iwgn: Weather-generator index selected from the current weather station.
uses:
  channel_module: Provides the shared reach timestep, nutrient-parameter index, benthic area,
    and reach depth used to scale reaction rates and gate the water-quality update.
  hydrograph_module: Supplies the current reach identifiers and the hydrograph input/output
    records that this routine reads, updates, and returns to routing.
  climate_module: Provides the weather inputs used to estimate stream temperature, daylight
    length, and light intensity for the reaction-rate calculations.
  channel_data_module: Provides the QUAL2E channel nutrient and reaction parameters that control
    growth, settling, oxidation, and benthic exchange.
  sd_channel_module: Provides the interpolated rating-curve depth and the channel depth parameter
    used to gate the update and scale phosphorus exchange.
  water_body_module: Imported by the procedure, but no source-backed outside references from
    this module were resolved in the context packet.
---

<!-- facts:header -->

Computes in-stream water-quality transformations for a channel reach.

## Bottom Line

ch_watqual4 updates channel water-quality concentrations for a single reach using the current flow, temperature, benthic exchange, algal growth, oxygen balance, and nutrient reaction rates. It converts the incoming mass hydrograph to concentrations, applies QUAL2E-style semi-analytic updates, and then converts the updated concentrations back to masses for routing.

The routine matters because it is the channel water-quality step that produces the updated outflow state used later in channel routing and downstream channel control. If there is no flow or no positive depth, it zeros the water-quality outputs and channel storage for the reach.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `sd_channel_control3` after the channel object, nutrient index, benthic area, and flow rate have been prepared. It performs the channel water-quality step for the current reach and returns updated hydrograph masses that later routing and channel-control logic can use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set reach context | Copies the current swat-deg channel index into the reach index, derives the channel object index, computes the effective timestep in days from rating-curve travel time, and initializes the routing timestep. |
| 2. Convert inflow to concentrations | Converts incoming hydrograph masses in `ht1` to concentrations in `ht3` so the water-quality reactions can be applied in concentration space. |
| 3. Estimate stream temperature | Estimates stream temperature from air temperature and stores it in `ht2%temp` for later temperature-dependent reaction calculations. |
| 4. Compute benthic exchanges | Applies temperature correction to benthic dissolved phosphorus, ammonia, and sediment oxygen demand terms and scales them by benthic area. |
| 5. Interpolate channel depth | Converts flow to cubic meters per second, interpolates the rating curve, and reads the resulting channel depth for depth-dependent reactions. |
| 6. Guard on flow and depth | Skips the water-quality update when flow or depth is nonpositive; otherwise initializes dissolved oxygen saturation and the incoming concentration terms used by later reactions. |
| 7. Compute oxygen limits | Constrains dissolved oxygen and computes the low-oxygen correction factor used in nitrification-related oxygen demand. |
| 8. Evaluate algal growth | Computes algal biomass, light limitation, nutrient limitation, growth option, settling, and the end-of-day chlorophyll-a concentration. |
| 9. Update oxygen demand | Computes CBOD decay, reaeration, sediment oxygen demand, and oxygen uptake from nitrogen transformations, then updates dissolved oxygen. |
| 10. Update nitrogen pools | Advances ammonia, nitrite, and nitrate concentrations with the semi-analytic solver and clamps small negative values to zero. |
| 11. Update phosphorus pools | Advances organic phosphorus and soluble phosphorus using benthic exchange, settling, and algal uptake terms. |
| 12. Convert back to masses | Converts the updated concentrations back to hydrograph masses for routing, or zeros the outputs and storage when no flow is present. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_module] | `rt_delt, jnut, ben_area, rchdep` |  |
| [sym:hydrograph_module] | `sp_ob1, ht3, ht1, ht2, ch_stor, jrch, isdch, icmd, iwst, ich` | `sp_ob1%chandeg, ht3%orgn, ht1%orgn, ht1%flo, ht3%sedp, ht1%sedp, ht3%no3, ht1%no3, ht3%solp, ht1%solp, ht3%chla, ht1%chla, ht3%nh3, ht1%nh3, ht3%no2, ht1%no2, ht3%cbod, ht1%cbod, ht3%dox, ht1%dox, ht2%temp, ch_stor(jrch)%nh3, ch_stor(jrch)%no3, ht2%orgn, ht2%sedp, ht2%no3, ht2%solp, ht2%chla, ht2%nh3, ht2%no2, ht2%cbod, ht2%dox` |
| [sym:climate_module] | `wst, wgn_pms` | `wst(iwst)%weat%tave, wst(iwst)%wco%wgn, wgn_pms(iwgn)%daylth, wst(iwst)%weat%solrad` |
| [sym:channel_data_module] | `ch_nut` | `ch_nut(jnut)%ai0, ch_nut(jnut)%lambda0, ch_nut(jnut)%lambda1, ch_nut(jnut)%lambda2, ch_nut(jnut)%k_n, ch_nut(jnut)%k_p, ch_nut(jnut)%tfact, ch_nut(jnut)%k_l, ch_nut(jnut)%igropt, ch_nut(jnut)%mumax, ch_nut(jnut)%p_n, ch_nut(jnut)%ai1, ch_nut(jnut)%ai2, ch_nut(jnut)%rs1, ch_nut(jnut)%rk1, ch_nut(jnut)%rk3, ch_nut(jnut)%rs4, ch_nut(jnut)%rk2, ch_nut(jnut)%ai4, ch_nut(jnut)%ai3, ch_nut(jnut)%bc2, ch_nut(jnut)%ai5, ch_nut(jnut)%ai6, ch_nut(jnut)%bc4, ch_nut(jnut)%rs5` |
| [sym:sd_channel_module] | `rcurv, sd_chd` | `rcurv%ttime, rcurv%dep, sd_chd(jrch)%chd` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `jrch` | Always at entry | Set to the current swat-deg channel index (`isdch`) so the routine works on the active reach. |
| `icmd` | Always at entry | Set to the current channel object index derived from `sp_ob1%chandeg + jrch - 1`. |
| `rt_delt` | Always at entry | Reset to 1.0 as the routing calculation timestep used by the semi-analytic updates. |
| `ht2%temp` | After temperature estimation | Stores the estimated stream temperature for use in temperature-dependent reaction-rate corrections. |
| `ht3%orgn` | When flow and depth are positive | Updated from incoming concentration to end-of-day concentration after organic nitrogen reactions. |
| `ht3%sedp` | When flow and depth are positive | Updated from incoming concentration to end-of-day concentration after organic phosphorus reactions. |
| `ht3%no3` | When flow and depth are positive | Updated from incoming concentration to end-of-day nitrate concentration. |
| `ht3%solp` | When flow and depth are positive | Updated from incoming concentration to end-of-day soluble phosphorus concentration. |
| `ht3%chla` | When flow and depth are positive | Updated to the end-of-day chlorophyll-a concentration after algal growth and settling. |
| `ht3%nh3` | When flow and depth are positive | Updated from incoming concentration to end-of-day ammonia concentration. |
| `ht3%no2` | When flow and depth are positive | Updated from incoming concentration to end-of-day nitrite concentration. |
| `ht3%cbod` | When flow and depth are positive | Updated from incoming concentration to end-of-day carbonaceous BOD concentration. |
| `ht3%dox` | When flow and depth are positive | Updated from incoming concentration to end-of-day dissolved oxygen concentration. |
| `ht2%orgn` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%sedp` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%no3` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%solp` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%chla` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%nh3` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%no2` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%cbod` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2%dox` | When flow and depth are positive | Converted from the updated concentration back to mass for routing. |
| `ht2` | When no flow or no depth | Set to zeroed hydrograph output state (`hz`) so downstream routing sees no water-quality mass. |
| `ch_stor(jrch)` | When no flow or no depth | Reset channel storage for the active reach to zeroed hydrograph state (`hz`). |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:3.1.11 |  | $fr_{DL}=\frac{T_{DL}}{24}$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90). (daylight fraction) |
| 7:3.1.3 |  | $\mu_{a,20}=\mu_{max}*FL*FN*FP$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90:289). (algal growth mu*FL*FN*FP) |
| 7:3.1.4 |  | $\mu_{a,20}=\mu_{max}*FL*min(FN,FP)$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90). (min limiting nutrient) |
| 7:3.1.5 |  | $\mu_{a,20}=\mu_{max}*FL*\frac{2}{(\frac{1}{FN}+\frac{1}{FP})}$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90). (harmonic mean option) |
| 7:3.1.7 |  | $I_{phosyn,z}=I_{phosyn,hr} exp(-k_{\Box}*z)$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90:158). Beer's-law k = `lambda` light-extinction coeff (QUAL2E III-12); exp(-k·z) in the FL integral |
| 7:3.1.8 |  | $FL=(\frac{1}{k_{\Box}*depth})*ln[\frac{K_L+I_{phosyn,hr}}{K_L+I_{phosyn,hr}exp(-k_{Box}*depth)}]$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90:181). |
| 7:3.3.4 |  | $\Delta solP_{str}=(\beta_{P,4}*orgP_{str}+\frac{\sigma_2}{(1000*depth)}-\alpha_2*\mu _a*algae)*TT$ | Verified against SWAT+ 62.0.0 (ch_watqual4.f90:322). (in-stream soluble P balance) |

## Lineage

`ch_watqual4.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_watqual4.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `889136d` (2025-02-03) — Fix typos
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `54a9d44` (2024-08-12) — NP_flow.f90 - Subroutine NP_FLOW REMOVED
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_watqual4' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
