---
kind: procedure
symbol: sd_channel_sediment3
title: sd_channel_sediment3
status: filled
source_hash: cbe059b9cbfcf604
version_label: SWAT+ 62.0.0
locals:
  iob: Object index for the SWAT-DEG channel reach in the connectivity arrays; set from `sp_ob1%chandeg
    + jrch - 1`.
  ihru: Loop index over HRUs connected to the channel floodplain.
  iihru: Actual HRU number selected from the floodplain HRU list for the current channel.
  ires: Pointer-like index into the HRU's surface storage database; used to test whether floodplain
    water can be routed into wetland storage.
  rto: A routing fraction used to scale hydrograph volumes or constituents when only part
    of the current inflow is diverted.
  rto1: The complement routing fraction `1 - rto`, used to keep the remainder of inflow in
    the channel after part is routed to wetlands.
  trap_eff: Floodplain trap efficiency; determines what fraction of sediment and nutrients
    are deposited on the floodplain from the current channel inflow.
  cohesion: Computed bank cohesion term derived from channel clay content; used in the critical-velocity
    bank erosion calculation.
  b_exp: Empirical exponent derived from clay content; calculated in the bank-erosion section
    but not used further in this routine.
  ebtm_m: Bed erosion depth increment in meters per year, computed when channel velocity exceeds
    the critical threshold.
  ebank_m: Bank erosion depth/width increment in meters per year, computed when routing velocity
    exceeds the bank critical velocity.
  ebtm_t: Total bed erosion mass in tons, derived from `ebtm_m` and channel geometry.
  ebank_t: Total bank erosion mass in tons, derived from `ebank_m` and channel geometry.
  shear_btm_cr: Stored placeholder for the bed critical shear/shear proxy; assigned from `d50`
    before bed-erosion calculations.
  shear_btm: Computed bed shear proxy from channel depth and slope; used as a diagnostic/placeholder
    in the bed-erosion block.
  flo_time: Estimated total time that floodwater remains overbank during the day; used to
    choose the floodplain volume formula.
  bf_flow: Bankfull flow threshold adjusted by the rating curve; compared with mean daily
    flow to decide whether overbank flooding occurs.
  pk_rto: Adjusted peak-to-mean flow ratio used to convert mean daily channel flow into peak
    daily flow.
  bd_fac: Bulk-density-related factor used in the critical velocity calculation for bank erosion.
  cohes_fac: Combined cohesion and vegetation factor used to compute the bank critical velocity.
  florate: A lower-triangle flow rate used only when overbank flow persists longer than one
    day to estimate flood volume.
  vel: Current channel velocity used for routing, floodplain exchange, and bank/bed erosion
    checks.
  veg: Vegetation resistance term contributing to the bank critical velocity calculation.
  vel_cr: Critical velocity threshold for bank or bed erosion, computed from channel properties
    and later reused in the bed-erosion test.
  rad_curv: Radius of channel curvature used to adjust velocity for meander-bend effects.
  vel_bend: Velocity adjusted for bend effects before computing an effective reach velocity
    for erosion.
  vel_rch: Effective reach velocity blending bend-adjusted and mean velocity; this is the
    main driver for bank erosion and is also compared to the bed critical velocity.
  arc_len: Approximate bank erosion arc length used to convert bank erosion depth into mass.
  prot_len: Protected length along the bank arc; calculated from arc length and the arc-length
    fraction, but not used later in this routine.
  h_rad: Hydraulic radius proxy computed from cross-sectional area and wetted perimeter before
    velocity is overwritten by the flow/area relation.
  fp_m2: Floodplain area estimate in square meters used in the floodplain trap-efficiency
    formula.
  exp_co: Exponential coefficient in the floodplain trap-efficiency equation.
  florate_ob: Overbank flow rate above bankfull used to determine whether floodplain deposition
    and floodplain-to-wetland routing occur.
  precip: Channel precipitation volume added to inflow during the current day.
  flovol_ob: Estimated overbank flood volume available after subtracting wetland filling needs.
  wet_fill: Volume required to fill a connected wetland to emergency spillway storage.
  ave_rate: Mean daily flow rate (`ht1%flo / 86400`) used to compare against bankfull flow
    and derive flood durations.
  v_vc: Intermediate bank-erosion velocity term combining duration scaling, channel width,
    and the logistic excess-velocity response.
  m_exhaust: Exhaustion cap on bank erosion mass rate, used to limit the bank erosion estimate.
  dur_scale: Duration scaling factor for the bank erosion response, based on drainage area.
uses:
  climate_module: The current-day precipitation record from `wst(iwst)%weat%precip` is added
    directly onto channel inflow, so weather forcing changes the water volume available for
    floodplain exchange and sediment routing.
  sd_channel_module: The SWAT-DEG channel state supplies the channel geometry, sediment properties,
    floodplain links, and erosion parameters that control every calculation in this routine,
    including peak flow, floodplain trapping, bank erosion, and bed erosion.
  channel_module: This module stores the reach velocity and routing time computed here so
    later channel-temperature or transport routines can reuse the updated hydraulic timing
    and flow speed.
  hydrograph_module: The hydrograph state holds the shared inflow/outflow sediment and nutrient
    carriers (`ht1`, `fp_dep`, `ch_dep`, `bank_ero`, `bed_ero`, and `ob(icmd)%tsin`) that
    this routine updates as water is partitioned between the channel, floodplain, and wetland
    pathway.
  time_module: Time state matters because flood routing, daily precipitation addition, and
    erosion/deposition updates are performed on the current simulation day and are intended
    to feed the model's time-stepped routing sequence.
  hru_module: The HRU database pointer `hru(iihru)%dbs%surf_stor` is used to decide whether
    a floodplain-connected HRU can receive overbank water into wetlands, and `hru(iihru)%wet_obank_in`
    records the amount routed in.
  water_body_module: Channel-water-body state is needed to store precipitation added to the
    channel water surface and to compute the channel water surface area used in the precipitation
    volume calculation.
  reservoir_module: Wetland emergency storage `wet_ob(iihru)%evol` is the capacity check for
    routing overbank water from the channel floodplain into connected wetland storage.
  utils: The routine calls `exp_w` from `utils` to evaluate the logistic bank-erosion response
    safely, so the module provides the numerical helper used in the bank-erosion calculation.
  basin_module: Basin control codes determine whether groundwater floodplain exchange is active;
    when `bsn_cc%gwflow` is 1 the routine invokes `gwflow_floodplain` and sets flood-frequency
    tracking.
  gwflow_module: The flood-frequency array is updated when groundwater floodplain exchange
    is triggered so the gwflow subsystem can track which channels experienced a floodplain
    event.
  channel_velocity_module: The channel-velocity state stores the velocity and routing-time
    diagnostics computed here, making them available to later channel temperature and routing
    calculations.
---

<!-- facts:header -->

Routes water, sediment, and associated nutrients through a SWAT+ SWAT-DEG channel reach. It updates floodplain exchange, bank erosion, and bed erosion using the current channel flow conditions.

## Bottom Line

`sd_channel_sediment3` is the reach-scale sediment and nutrient routing step for SWAT-DEG channels. When inflow is present, it computes peak flow, interpolates the channel rating curve, adds local precipitation, and then routes water onto the floodplain and into connected wetlands before any erosion or deposition calculations.

It then estimates floodplain trapping, bank erosion, bank-related deposition, and bed erosion, updating the shared hydrograph and morphology state objects that later channel routing and output routines depend on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside channel control after the outgoing hydrograph has been initialized and before Muskingum routing and pesticide routing are performed. `sd_channel_control3` prepares the current channel state and then calls this routine to update floodplain exchange and erosion/deposition, and later channel routing and output calculations depend on the modified hydrograph, morphology, and velocity state it leaves behind.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local state and current channel pointers. | Sets `ich` and `iob`, clears erosion/deposition accumulators, copies zero hydrograph output into `fp_dep`, `ch_dep`, `bank_ero`, `bed_ero`, and `ch_trans`, and resets channel precipitation storage. |
| 2. Skip all sediment work if there is no inflow. | Checks whether `ht1%flo` is greater than `1.e-6`; all routing, erosion, and deposition logic runs only when inflow is present. |
| 3. Compute peak daily flow and interpolate channel hydraulics. | Adjusts the peak-to-mean ratio, computes `peakrate`, calls `rcurv_interp_flo` for the current reach and peak flow, then derives velocity and routing time from the interpolated rating curve and stores them in `sd_ch_vel(ich)`. |
| 4. Add local precipitation to the inflow hydrograph. | Computes channel water-body area, converts station precipitation to a channel precipitation volume, stores it in `ch_wat_d(ich)%precip`, scales the inflow hydrograph, and adds precipitation to `ht1%flo`. |
| 5. Estimate floodplain discharge above bankfull and optionally trigger gwflow exchange. | Computes mean flow, bankfull threshold, and overbank flow; if overbank flow exists and groundwater floodplain routing is active, sets `flood_freq(ich)` and calls `gwflow_floodplain`. |
| 6. Compute floodplain trapping and remove deposited material from channel flow. | Uses flood duration, floodplain area, and an exponential coefficient to estimate trap efficiency, then partitions floodplain deposition into sediment, organic N, particulate P, nitrate, and soluble P before subtracting `fp_dep` from `ht1`. |
| 7. Route remaining flood volume into connected wetlands and HRUs. | Loops over floodplain HRUs, checks wetland emergency volume and HRU surface storage, and moves part of the remaining overbank water into `wet(iihru)`, `wet_in_d(iihru)`, and `hru(iihru)%wet_obank_in` while scaling the channel hydrograph remainder. |
| 8. Add floodplain deposition to morphology output. | Accumulates deposited floodplain sediment into `ch_morph(ich)%fp_mm` for later morphology reporting. |
| 9. Compute bank cohesion, vegetation, and critical velocity. | Derives bank cohesion from channel clay, builds vegetation and bulk-density factors, and computes the critical velocity threshold for bank erosion, capped by `vcr_coef`. |
| 10. Estimate bend-driven bank erosion when effective velocity exceeds the critical threshold. | Computes radius of curvature, bend-adjusted velocity, and effective reach velocity; if `vel_rch > vel_cr`, uses the safe exponential helper to compute a bank erosion mass rate limited by an exhaustion term. |
| 11. Convert bank erosion to mass and associated nutrient loads, then update channel inflow. | Uses an arc-length approximation to convert `ebank_m` into bank erosion mass, fills `bank_ero` sediment and nutrient fields, scales the inflow hydrograph, and adds bank erosion back into `ht1`. |
| 12. Compute channel deposition as a fraction of bank erosion and remove it from the flow. | Sets channel deposition to the wash-bed fraction of bank erosion, computes its nutrient species, and subtracts `ch_dep` from `ht1`. |
| 13. Compute bed erosion when slope and velocity conditions permit. | For non-negligible channel slope, computes bed shear and critical velocity from `d50`, applies a power-law bed erosion depth increment when velocity exceeds the threshold, converts it to mass, and accumulates bed downcutting into `ch_morph(ich)%d_yr`. |
| 14. Populate bed erosion hydrograph output and return. | Sets `bed_ero` sediment and nutrient fields from the computed bed erosion mass and exits the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%precip` |
| [sym:sd_channel_module] | `sd_ch, rcurv, ch_rcurv, ch_morph` | `sd_ch(ich)%pk_rto, rcurv%xsec_area, rcurv%wet_perim, sd_ch(ich)%chn, sd_ch(ich)%chl, sd_ch(ich)%chw, sd_ch(ich)%bankfull_flo, ch_rcurv(ich)%elev(2)%flo_rate, sd_ch(ich)%fp_inun_days, sd_ch(ich)%n_dep_enr, sd_ch(ich)%p_dep_enr, sd_ch(ich)%fp%hru_tot, sd_ch(ich)%fp%hru(ihru), ch_morph(ich)%fp_mm, sd_ch(ich)%ch_clay, sd_ch(ich)%chd, sd_ch(ich)%cov, sd_ch(ich)%ch_bd, sd_ch(ich)%vcr_coef, sd_ch(ich)%sinu, ch_morph(ich)%w_yr, sd_ch(ich)%arc_len_fr, sd_ch(ich)%n_conc, sd_ch(ich)%p_bio, sd_ch(ich)%p_conc, sd_ch(ich)%wash_bed_fr, sd_ch(ich)%chs, sd_ch(ich)%d50, rcurv%dep, sd_ch(ich)%bed_exp, ch_morph(ich)%d_yr` |
| [sym:channel_module] | `sd_ch_vel` | `sd_ch_vel(ich)%vel, sd_ch_vel(ich)%rttime` |
| [sym:hydrograph_module] | `sp_ob1, ht1, ob, fp_dep, wet, bank_ero, ch_dep, bed_ero` | `sp_ob1%chandeg, ht1%flo, ob(icmd)%area_ha, ob(icmd)%tsin(:), fp_dep%sed, ht1%sed, fp_dep%orgn, ht1%orgn, fp_dep%sedp, ht1%sedp, fp_dep%no3, fp_dep%solp, wet(iihru)%flo, bank_ero%sed, bank_ero%orgn, bank_ero%sedp, bank_ero%no3, bank_ero%solp, bank_ero%no2, bank_ero%flo, ch_dep%sed, ch_dep%orgn, ch_dep%sedp, bed_ero%sed, bed_ero%orgn, bed_ero%sedp, bed_ero%no3, bed_ero%solp, bed_ero%no2, bed_ero%flo` |
| [sym:time_module] | `time variables from `time_module` are used through imported model time state, but no specific symbol from that module is explicitly referenced in the extracted lines.` |  |
| [sym:hru_module] | `hru` | `hru(iihru)%dbs%surf_stor, hru(iihru)%wet_obank_in, hru(iihru)%area_ha` |
| [sym:water_body_module] | `ch_wat_d` | `ch_wat_d(ich)%precip, ch_wat_d(ich)%area_ha` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(iihru)%evol` |
| [sym:utils] | `No specific imported symbol from `utils` is referenced in the extracted lines; the module is brought in for its available helper functions.` |  |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:gwflow_module] | `flood_freq` | `flood_freq` |
| [sym:channel_velocity_module] | `sd_ch_vel` | `sd_ch_vel(ich)%vel, sd_ch_vel(ich)%rttime` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ich` | At routine entry (unconditional). | Local channel index set from `isdch`, the current SWAT-deg channel being processed. |
| `fp_dep` | Reset to the zero hydrograph `hz` at entry; populated when overbank flow occurs (`florate_ob > 0`). | Floodplain deposition hydrograph; zeroed then filled with sediment and particulate nutrient masses trapped on the floodplain. |
| `ch_dep` | Reset to the zero hydrograph `hz` at entry. | Channel (bed) deposition hydrograph initialized to zero before its sediment/nutrient components are computed. |
| `bank_ero` | Reset to the zero hydrograph `hz` at entry. | Bank-erosion hydrograph initialized to zero before erosion sediment/nutrient loads are computed. |
| `bed_ero` | Reset to the zero hydrograph `hz` at entry. | Bed-erosion hydrograph initialized to zero before bed-erosion loads are computed. |
| `ch_trans` | Reset to the zero hydrograph `hz` at entry. | Channel transport hydrograph reset to zero; not further modified in this routine. |
| `ch_wat_d(ich)%precip` | Reset to 0 at entry; set when inflow occurs (`ht1%flo > 1.e-6`). | Precipitation volume falling directly on the channel surface this day. |
| `peakrate` | When inflow occurs (`ht1%flo > 1.e-6`). | Peak daily flow rate derived from a peak-to-mean ratio scaled by drainage area. |
| `rttime` | When inflow occurs (`ht1%flo > 1.e-6`). | Reach travel time from channel length and flow velocity. |
| `sd_ch_vel(ich)%vel` | When inflow occurs (`ht1%flo > 1.e-6`). | Stores the computed channel velocity for later use by the temperature routine. |
| `sd_ch_vel(ich)%rttime` | When inflow occurs (`ht1%flo > 1.e-6`). | Stores the reach travel time for later use by the temperature routine. |
| `ch_wat_d(ich)%area_ha` | When inflow occurs (`ht1%flo > 1.e-6`). | Channel water-surface area from reach length and width. |
| `ob(icmd)%tsin(:)` | Whenever the bulk inflow volume is rescaled: precipitation add, wetland overbank fill, and bank-erosion add. | The sub-daily inflow time series is scaled by the same ratio as the bulk volume so the hydrograph shape is preserved. |
| `ht1%flo` | Gate `ht1%flo > 1.e-6`; then augmented when precipitation is added. | Inflow volume gates all sediment/erosion processing, and is increased by direct precipitation onto the channel surface. |
| `flood_freq(ich)` | When overbank flow occurs and gwflow is active (`florate_ob > 0` and `bsn_cc%gwflow == 1`). | Flags the channel as flooded for the groundwater-flow floodplain exchange module. |
| `fp_dep%sed` | When overbank flow occurs (`florate_ob > 0`). | Sediment trapped on the floodplain via the trap-efficiency fraction of inflow sediment. |
| `fp_dep%orgn` | When overbank flow occurs (`florate_ob > 0`). | Particulate organic nitrogen deposited on the floodplain, enriched by `n_dep_enr`. |
| `fp_dep%sedp` | When overbank flow occurs (`florate_ob > 0`). | Particulate phosphorus deposited on the floodplain, enriched by `p_dep_enr`. |
| `fp_dep%no3` | When overbank flow occurs (`florate_ob > 0`). | Floodplain nitrate trapping is set to zero in this version (soluble species not trapped without floodplain interaction). |
| `fp_dep%solp` | When overbank flow occurs (`florate_ob > 0`). | Floodplain soluble-P trapping is set to zero in this version (soluble species not trapped without floodplain interaction). |
| `ht1` | Updated repeatedly when inflow occurs: floodplain deposition, wetland filling, bank-erosion addition, and channel deposition. | The channel routing hydrograph is reduced by floodplain and channel deposition, partitioned to wetlands, and increased by bank erosion as it passes through the reach. |
| `wet(iihru)` | For each floodplain-linked HRU when overbank volume and wetland capacity remain (`ires > 0`, `wet_fill > 0`, `rto > 1.e-6`). | Wetland storage receives a flow-weighted share of the channel hydrograph as overbank water fills it toward emergency volume. |
| `wet_in_d(iihru)` | For each floodplain-linked HRU when overbank water enters the wetland (same guard as `wet(iihru)`). | Accumulates the daily overbank inflow contributed to the wetland. |
| `hru(iihru)%wet_obank_in` | For each floodplain-linked HRU receiving overbank water (same guard as `wet(iihru)`). | Overbank inflow expressed as a depth over the wetland HRU area. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:2.2.1 | Peak channel velocity | $v_{ch,pk}=\frac{q_{ch,pk}}{A_{ch}}$ | peakrate = pk_rto*ht1%flo/86400 and vel = peakrate/rcurv%xsec_area match v_ch,pk = q_ch,pk / A_ch. |
| 7:2.2.2 | Peak flow rate from mean flow | $q_{ch,pk}=prf*q_{ch}$ | pk_rto is adjusted by contributing area before use, so q_ch,pk = pk_rto*Q is implemented with an added watershed-scale correction. |
| 7:2.2.3 | Maximum sediment concentration by Bagnold relation | $conc_{sed,ch,mx}=c_{sp}*v_{ch,pk}^{spexp}$ | The legacy Bagnold coefficients spcon and spexp are declared as 'not used' in this codebase, so conc_sed,ch,mx = c_sp*v^spexp is not evaluated directly. |
| 7:2.2.4 | Sediment deposition from excess concentration | $sed_{dep}=(conc_{sed,ch,i}-conc_{sed,ch,mx})*V_{ch}$ | Channel deposition is not computed from (conc_i - conc_mx)*V_ch; instead ch_dep is set as a wash-bed fraction of bank erosion. |
| 7:2.2.5 | Sediment degradation from transport deficit | $sed_{deg}=(conc_{sed,ch,mx}-conc_{sed,ch,i})*V_{ch}*K_{CH}*C_{CH}$ | Bed erosion is triggered by an empirical critical-velocity power law, not by (conc_mx - conc_i)*V_ch*K_CH*C_CH. |
| 7:2.2.6 | Updated channel sediment mass | $sed_{ch}=sed_{ch,i}-sed_{dep}+sed_{deg}$ | Channel sediment is updated through separate floodplain deposition, bank erosion addition, and channel deposition subtraction steps rather than one explicit sed_ch = sed_in - dep + deg equation. |
| 7:2.2.8 | Bank erosion rate from excess shear | $\xi_{bank}=k_{d,bank}*(\tau_{e,bank}-\tau_{c,bank})*10^{-6}$ | Bank erosion is driven by a logistic excess-velocity relation and an exhaustion cap, not by kd_bank*(tau_e,bank - tau_c,bank)*1e-6. |
| 7:2.2.9 | Bed erosion rate from excess shear | $\xi_{bed}=k_{d,bed}*(\tau_{e,bed}-\tau_{c,bed})*10^{-6}$ | Bed erosion uses ebtm_m = 0.0001*(vel_rch/vel_cr)^bed_exp when velocity exceeds critical velocity, not the printed kd_bed excess-shear formula. |
| 7:2.2.10 | Effective bank shear stress relation | $\frac{\tau_{e,bank}}{\gamma*depth*slp_{ch}}=\frac{SF_{bank}}{100}(\frac{(W+P_{bed})*sin\theta}{4*depth})$ | The detailed bank shear-stress partition formula is not evaluated explicitly; bend velocity is instead estimated from curvature and mean channel velocity. |
| 7:2.2.11 | Effective bed shear stress relation | $\frac{\tau_{e,bed}}{\gamma_{W}*depth*slp_{ch}}=(1-\frac{SF_{bank}}{100})(\frac{W}{2*P_{bed}}+0.5)$ | Verified against SWAT+ 62.0.0 (sd_channel_sediment3.f90:180). (critical velocity/shear) |
| 7:2.2.12 | Bank shear fraction from bank and bed perimeters | $logSF_{bank}=-1.4026*log(\frac{P_{bed}}{P_{bank}}+1.5)+2.247$ | The logarithmic SF_bank perimeter relation is not present; curvature-adjusted velocity is used instead. |
| 7:2.2.13 | Erodibility coefficient from critical shear | $k_d=0.2*\tau_c^{-0.5}$ | The code does not compute kd = 0.2*tau_c^-0.5; bank and bed erosion are controlled by clay/cohesion/critical-velocity relationships. |
| 7:2.2.14 | Bank erosion mass rate | $Bnkrte=\xi_{bnk}*(L_{ch}*1000*depth*\sqrt{1+Z_{ch}^2})*\rho_{b,bank}*86400$ | Bank erosion mass is computed as ebank_t = 1000*ebank_m*depth*arc_len*bulk_density, using an arc-length approximation rather than the printed exact bank-face geometry. |
| 7:2.2.15 | Bed erosion mass rate | $Bedrte=\xi_{bed}*(L_{ch}*1000*W_{btm})*\rho_{b,bed}*86400$ | Bed erosion mass is computed as ebtm_t = 1000*ebtm_m*width*length*bulk_density, matching the same concept with a velocity-threshold erosion law. |
| 7:2.2.16 | Bank erosion fraction of total degradation | $Bnk_{rp}=\frac{Bnkrte}{Bnkrte+Bedrte}$ | SWAT+ computes bank and bed erosion masses independently and does not form an explicit bank fraction Bnk_rp = Bnkrte/(Bnkrte+Bedrte). |
| 7:2.2.17 | Bed erosion fraction of total degradation | $Bed_{rp}=1-Bnk_{rp}$ | No explicit Bed_rp = 1 - Bnk_rp term is stored; bank and bed erosion are computed as separate empirical components. |
| 7:2.2.18 | Maximum sediment concentration as a peak-velocity function | $conc_{sed,ch.mx}=f(peak$ | Peak velocity is computed, but the theory page's conc_sed,ch,mx = f(peak velocity) relation is not evaluated because the legacy spcon/spexp pathway is inactive. |
| 7:2.2.19 | Critical shear or legacy max-concentration relation | $\tau_c=(0.1+0.1779*SC+0.0028*SC^2-2.34*10^{-5}*SC^3)*C_{CH}$ | The GitBook reuses 7:2.2.19 for alternate formulas; this code uses neither the printed tau_c polynomial nor the legacy spcon*spexp concentration equation directly. |
| 7:2.2.20 | Alternative maximum sediment concentration relation | $conc_{sed,ch,mx}=(\frac{a.v_{ch}^b*y^c*S^d}{Q_{in}})*(\frac{W+W_{btm}}{2})$ | The alternate a*v^b*y^c*S^d/Q-based concentration formula is not evaluated in the current channel sediment routine. |
| 7:2.2.21 | Concentration coefficient power law | $C_W=M\Psi^N$ | No C_W = M*Psi^N relation is computed in the current reach sediment implementation. |
| 7:2.2.22 | Yang transport concentration relation | $C_W=\frac{1430*(0.86+\sqrt \Psi)*\Psi^{1.5}}{0.016+\Psi}*10^{-6}$ | The explicit Yang-style concentration equation is not evaluated in the active channel sediment code. |
| 7:2.2.23 | Dimensionless stream power parameter | $\Psi=\frac{\Psi^3}{(S_g-1)*g*depth*\omega_{50}*[log_{10}(\frac{depth}{D_{50}})]^2}$ | The Psi transport parameter is not formed explicitly in this routine. |
| 7:2.2.24 | Settling velocity from median grain size | $\omega_{50}=\frac{411*D_{50}^2}{3600}$ | The routine uses d50 to derive a critical velocity threshold, but it does not compute omega_50 = 411*D50^2/3600. |
| 7:2.2.25 | Sediment concentration from C_W and specific gravity | $conc_{sed,ch,mx}=\frac{C_W}{C_W+(1-C_W)*S_g}*S_g$ | No explicit conversion from C_W to sediment concentration is evaluated in the active routine. |
| 7:2.2.26 | Fine-sediment transport concentration relation | $logC_W=5.435-0.286log\frac{\omega_{50}D_{50}}{\upsilon}-0.457log\frac{V_*}{\omega_{50}}\\+(1.799-0.409log\frac{\omega_{50}D_{50}}{\upsilon}-0.3141log\frac{V_*}{\omega_{50}})log(\frac{v_{ch}S}{\omega_{50}}-\frac{V_{cr}S}{\omega_{50}})$ | The logarithmic transport relation involving omega_50, viscosity, and shear velocity is not present in the current implementation. |
| 7:2.2.27 | Coarse-sediment transport concentration relation | $logC_W=6.681-0.6331log\frac{\omega_{50}D_{50}}{\upsilon}-4.816log\frac{V_*}{\omega_{50}}+\\(2.784-0.305log\frac{\omega_{50}D_{50}}{\upsilon}-0.282log\frac{V_*}{\omega_{50}})log(\frac{v_{ch}S}{\omega_{50}}-\frac{V_{cr}S}{\omega_{50}})$ | The alternative logarithmic transport relation for coarse material is not evaluated explicitly. |
| 7:2.2.28 | Sediment exchange from transport deficit | $SedEx=V_{ch}*(conc_{sed,ch,mx}-conc_{sed,ch,i})$ | The code does not compute SedEx = V_ch*(conc_mx - conc_i); erosion is driven by empirical bank and bed excess-velocity relations instead. |
| 7:2.2.29 | Bank degradation limited by bank erosion rate | $Bnk_{deg}=SedEX* Bnk_{rp}, SedEX*Bnk_{rp} \le Bnkrte \\ Bnk_{deg}=Bnkrte, SedEX*Bnk_{rp}>Bnkrte$ | Bank degradation is computed directly as ebank_m/ebank_t and is not limited through a SedEx*Bnk_rp comparison. |
| 7:2.2.30 | Bed degradation limited by bed erosion rate | $Bed_{deg}=SedEX*Bed_{rp},SedEX*Bed_{rp}\le Bedrte \\ Bed_{deg}=Bedrte , SedEX*Bed_{rp}>Bedrte$ | Bed degradation is computed directly as ebtm_m/ebtm_t and is not limited through a SedEx*Bed_rp comparison. |
| 7:2.2.31 | Total channel degradation | $sed_{deg}=Bank_{deg}+Bed_{deg}$ | Total degradation is the sum of separately computed bank and bed erosion masses, but the code does not form one explicit sed_deg assignment. |
| 7:2.2.32 | Bank degradation split by particle classes | $Bnksan=Bnk_{deg}*Bnksanfr_i \\ Bnksil=Bnk_{deg}*Bnksilfr_i \\ Bnkcla=Bnk_{deg}*Bnkclafr_i \\ Bnkgra=Bnk_{deg}*Bnkgrafr_i$ | Bank erosion is partitioned only into total sediment, org N, and P species; the sand/silt/clay/gravel class breakdown is not computed here. |
| 7:2.2.33 | Settling or travel-length parameter x | $x=\frac{1.055*L_{ch}*1000*\omega}{v_{ch}*depth}$ | The theory page's x = 1.055*L*omega/(v*depth) relation is not evaluated in the active channel sediment routine. |
| 7:2.2.34 | Total bed degradation from particle classes | $Bed_{deg}=Bedsan+Bedsil+Bedcla+Bedgra$ | Bed erosion is stored only as total sediment plus nutrient-associated masses; no sand/silt/clay/gravel summation is formed. |
| 7:2.3.1 | Channel erodibility factor | $K_{d,bank\|bed}=0.003*exp[385*J_i]$ | The routine does not compute Kd = 0.003*exp(385*J_i); erodibility is represented indirectly through clay-dependent cohesion, vegetation, bulk density, and critical velocity terms. |
| 7:2.5.1 | Channel downcutting increment | $depth_{dcut}=358.6*depth*slp_{ch}*K_{CH}$ | Downcutting is represented by the empirical bed-erosion depth increment ebtm_m, not by the printed 358.6*depth*slope*K_CH expression. |
| 7:2.5.4 |  | $slp_{ch}=slp_{ch,i}-\frac{depth_{dcut}}{1000*L_{ch}}$ | Verified against SWAT+ 62.0.0 (sd_channel_sediment3.f90). (channel downcutting) |

## Lineage

`sd_channel_sediment3.f90` was introduced in `94b6dec` (2024-05-30, "Added latest source code from bitbucket") and has been changed in 19 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `sd_channel_sediment3.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `90fa54f` (2025-10-29) — Channel deposition and erosion adjusment. Water allocation modeule related adjustemnts
- `3d7fcfb` (2025-10-08) — Updates to utils.f90 to have a flag to print out stack trace or not. Multple changes to get NAM data set to run using gfortran compiled exec…
- `29fdf38` (2025-09-09) — updates 0909
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_channel_sediment3' has no extracted documentation comment.
- lineage: no commits resolved for this source span.
- algorithm_steps revised: condensed the draft into 14 source-backed steps and aligned each step to real line ranges from the source listing.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
