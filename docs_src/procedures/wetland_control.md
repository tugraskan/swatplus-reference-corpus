---
kind: procedure
symbol: wetland_control
title: wetland_control
status: filled
source_hash: a799ce56fe0cf556
version_label: SWAT+ 62.0.0
locals:
  bypass: Scale factor that lets downstream runoff, sediment, nutrient, and constituent yields
    be carried forward while adding the current wetland contribution; the routine uses it
    when blending `ht2` loads into HRU yield arrays near the end.
  j: HRU loop index for the current wetland/paddy object; set from `ihru` and then used to
    index the HRU, wetland, soil, hydrograph, and output arrays throughout the routine.
  x1: Temporary discriminant term for the wetland depth/area quadratic solution, computed
    from the wetland hydrology coefficients and current stored volume.
  wet_h: Intermediate wetland depth term derived from the quadratic solve; used to build the
    fractional wetland area factor.
  wet_h1: First quadratic root candidate for wetland depth before the coefficient offset is
    restored into `wet_h`.
  ised: Integer selector for sediment input data from `wet_dat(ires)%sed`, used to identify
    the wetland's sediment setup.
  irel: Decision-table or release-configuration index from `wet_dat(ires)%release`, used when
    evaluating paddy release and wetland hydrograph rules.
  icon: Constituent-parameter index from `wet_dat(ires)%cs`, passed to `wet_cs` to select
    the wetland constituent set.
  ires: Surface-storage reservoir/wetland database index taken from `hru(j)%dbs%surf_stor`;
    it links the HRU to its wetland parameter records.
  j1: Layer counter used in the seepage refinement loops over `soil(j)%nly` layers.
  ii: Sub-daily time-step counter used to split daily runoff into `time%step` pieces for `hhsurfq`.
  ihyd: Hydrology record index from `wet_dat(ires)%hyd`, used to select the wetland hydrology
    input and distinguish paddy handling.
  isched: Management-operation index from `hru(j)%mgt_ops`, retained as a wetland scheduling
    reference.
  wet_fr: Computed fractional wetland surface area relative to the HRU, limited to the 0.01–1.0
    range.
  pvol_m3: Principal spillway or normal wetland target volume read from `wet_ob(j)%pvol` for
    decision-table release calculations.
  evol_m3: Emergency spillway or emergency volume read from `wet_ob(j)%evol` for release calculations.
  dep: Current wetland water depth in meters, derived from stored volume and HRU area before
    outflow is computed.
  weir_hgt: Current weir crest height from `wet_ob(j)%weir_hgt`, used by paddy release logic.
  wsa1: Wetland surface area in square meters, computed as `hru(j)%area_ha * 10.` and reused
    as the volume-to-depth conversion factor.
  sedppm: Sediment concentration in the wetland water column after routing, computed from
    `wet(j)%sed / wet(j)%flo`.
  no3ppm: Nitrate concentration in the wetland water column after routing, computed from `wet(j)%no3
    / wet(j)%flo`.
  seep_rto: Fraction of ponded water mass assigned to seepage, used to partition wetland nutrients
    between seepage and remaining ponded water.
  qp_cms: Peak discharge proxy in cms used by the flushed-wetland sediment yield calculation.
  dep_init: Initial wetland depth before precipitation and irrigation are added; used to detect
    a nearly dry wetland that can generate flushed sediment yield.
  volseep: Seepage depth equivalent in mm derived from `wet_wat_d(j)%seep / wsa1`, then used
    to refine oversaturation limits in the soil layers.
  volex: Temporary excess-water volume tracker used while pushing seepage through soil layers
    and moving excess upward.
  swst: Working array of soil-water storage per layer used to test and adjust oversaturation
    during seepage refinement.
uses:
  reservoir_data_module: '`reservoir_data_module` supplies the wetland''s configuration records:
    which hydrology, sediment, release, and constituent datasets belong to the HRU, plus the
    wetland hydraulic coefficients and constituent-input selectors that govern the branch
    choices and parameter values in this routine.'
  reservoir_module: '`reservoir_module` defines the wetland object storage that holds volume,
    depth, spillway geometry, and area state. `wetland_control` reads and updates that shared
    wetland record to compute release, depth, and remaining storage.'
  hru_module: '`hru_module` matters because the routine is organized around the current HRU:
    it uses the HRU''s area, wetland storage pointer, management-operation index, upper-layer
    wetness conductivity, and surface-storage pointer to route the wetland balance.'
  conditional_module: '`conditional_module` matters because paddy and reservoir-style wetland
    releases use decision-table logic; the routine selects `d_tbl => dtbl_res(irel)` and calls
    `conditions` before `res_hydro` to evaluate those rules.'
  climate_module: '`climate_module` provides daily precipitation through `w%precip`, which
    is converted into wetland precipitation volume and added directly to ponded storage.'
  hydrograph_module: '`hydrograph_module` provides the routed hydrograph records for the wetland,
    irrigation inflow, outflow hydrograph, and constituent masses. Those shared `wet`, `irrig`,
    `wet_seep_day`, `wbody`, `ht2`, and `ob` states are updated and then copied back to the
    wetland outputs.'
  time_module: '`time_module` controls whether the routine splits daily runoff into sub-daily
    pieces and whether daily wetland records are written after the model''s skip-year window.'
  basin_module: '`basin_module` matters because `bsn_cc%gwflow` switches between the gwflow-based
    seepage path and the older hydraulic-conductivity seepage formula, while `bsn_prm%prf`
    and `pco%nyskip` affect sediment-yield scaling and output timing.'
  channel_module: '`channel_module` matters because wetland release and constituent routing
    are tied to the command/object connectivity index `icmd` and the `ob` connectivity record
    used for temperature-linked nutrient calculations and routed hydrograph bookkeeping.'
  water_body_module: '`water_body_module` provides `wet_wat_d`, the daily wetland water-body
    record that stores area, precipitation, and seepage. That record is the bridge between
    the hydrologic balance and later wetland output summaries.'
  soil_module: '`soil_module` supplies the number of soil layers, which the seepage refinement
    loop needs in order to step through the profile and limit excess water by layer capacity.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the soil mineral and
    organic pools that receive seepage-associated nitrate, ammonium, phosphorus, organic nitrogen,
    and sediment-associated phosphorus from the wetland.'
  mgt_operations_module: '`mgt_operations_module` matters because the wetland links to HRU
    management scheduling through `hru(j)%mgt_ops`, and that index is retained here as `isched`
    for operation-dependent behavior.'
  constituent_mass_module: '`constituent_mass_module` matters because `wet_cs` updates the
    wetland''s generic constituent pools, and `wetland_control` passes the constituent selector
    `icon` before calling it.'
  aquifer_module: '`aquifer_module` matters because the wetland can exchange water with groundwater
    through gwflow-related seepage paths, so aquifer-linked state is part of the broader wetland
    water balance context.'
  gwflow_module: '`gwflow_module` matters because when basin gwflow is active the routine
    delegates wetland seepage to `gwflow_wetland`, which exchanges water and solutes with
    the groundwater flow system.'
---

<!-- facts:header -->

Routes daily wetland/paddy water and constituent balances for an HRU-linked surface storage. It updates wetland area, seepage, outflow, sediment, nutrients, salt, and generic constituents before passing results to routing outputs.

## Bottom Line

`wetland_control` is the daily control routine for HRU-linked wetlands and paddies. It starts from the HRU's surface-storage mapping, computes current wetland area/depth and precipitation/irrigation gains, applies seepage or gwflow exchange, then releases water through either a paddy weir path or a decision-table reservoir path.

It matters because it writes the wetland's routed outflow and residual water quality state back into shared arrays used by later runoff, sediment, nutrient, salt, and constituent accounting, and it also feeds daily wetland output records once the nyskip print window has passed.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wetland_control` runs during HRU water routing, after `hru_control` has set the current HRU (`ihru`), initialized `ht2`, and confirmed that the HRU has a nonzero surface-storage index (`ires > 0`). Its results feed the rest of HRU routing: the routine sets surface runoff (`surfq`), seepage (`hru(j)%water_seep`), sediment and nutrient yields, and the daily wetland in/out records used by later output and downstream transport logic.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Bind the current HRU and wetland records | Use `ihru` to select the current HRU, fetch the linked wetland storage and data indices, compute the wetland surface-area factor `wsa1`, and alias the shared wetland bodies through `wbody`, `wbody_wb`, and `wbody_prm`. |
| 2. Initialize daily wetland state | Clear HRU seepage, derive the initial wetland depth from stored volume, and save that starting depth as `dep_init` for later flush/yield logic. |
| 3. Add precipitation and irrigation to storage | Convert daily precipitation to wetland water volume, add it to the wetland storage and depth, then add irrigation water and irrigation nitrate mass to the wetland. |
| 4. Compute wetland surface fraction and seepage | If the wetland still has water, solve the quadratic depth relation to update `wet_fr`, optionally reduce the wetland area for non-paddy systems, and compute seepage either through `gwflow_wetland` or the conductivity-limited formula. |
| 5. Refine seepage against soil storage limits | Convert seepage to a depth equivalent, compare it with each soil layer's storage and upper limit, adjust excess water through the profile, and reduce seepage by the amount that cannot enter the soil. |
| 6. Remove seepage and partition dissolved loads | Subtract seepage from wetland water volume, store seepage depth on the HRU, compute the seepage fraction, pass dissolved nitrate, ammonium, soluble phosphorus, organic nitrogen, and sediment phosphorus into the soil and seepage-day records, and remove those masses from the wetland. |
| 7. Compute wetland depth for outflow routing | Recompute depth from the updated volume and wetland area, then capture the current weir height and write the depth back to the wetland object. |
| 8. Route wetland outflow | For paddies, call the manual weir-release routine and copy its volume back to the wetland; otherwise attach the decision table, call `conditions` and `res_hydro`, and subtract the routed hydrograph outflow from wetland storage. |
| 9. Convert outflow to runoff depth | Express routed outflow as `surfq`, split it across sub-daily steps when needed, and refresh wetland depth after the release. |
| 10. Update sediment and nutrient water-body state | Call `res_sediment` and `res_nutrient`, then copy the resulting sediment, nitrate, ammonium, organic nitrogen, particulate phosphorus, and soluble phosphorus masses back into `wet(j)`. |
| 11. Update salt and generic constituent balances | Call `wet_salt` and `wet_cs` so salt ions and generic constituents are updated using the final wetland water volume and the configured constituent index. |
| 12. Estimate flushed sediment yield when the wetland starts nearly dry | If the wetland was nearly dry and still produced outflow, call `ero_cfactor`, compute peak flow and cover factor, estimate sediment yield, subtract the portion carried with the outflow, and assign that sediment to `ht2%sed`. |
| 13. Compute final concentrations and routing outputs | Convert remaining wetland sediment and nitrate to concentrations, zero the connected temperature field, add wetland inflow/outflow records after the skip-year window, and return the updated routing state to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `wet_dat, wet_hyd, wet_dat_c, wet_prm` | `wet_dat(ires)%hyd, wet_dat(ires)%sed, wet_dat(ires)%release, wet_hyd(j)%bcoef, wet_hyd(j)%ccoef, wet_hyd(j)%acoef, wet_dat_c(ires)%hyd, wet_dat(ires)%cs` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(j)%depth, wet_ob(j)%pvol, wet_ob(j)%weir_hgt, wet_ob(j)%evol` |
| [sym:hru_module] | `hru, cklsp, surfq, sedyld` | `hru(j)%dbs%surf_stor, hru(j)%area_ha, hru(j)%mgt_ops, hru(j)%water_seep, hru(j)%wet_hc` |
| [sym:conditional_module] | `conditional_module state and types used by decision tables` | `d_tbl, dtbl_res` |
| [sym:climate_module] | `w` | `w%precip` |
| [sym:hydrograph_module] | `wet, irrig, wet_seep_day, wbody, ht2, ob` | `wet(j)%flo, irrig(j)%applied, wet(j)%no3, irrig(j)%no3, wet(j)%nh3, wet(j)%solp, wet(j)%orgn, wet(j)%sedp, wet_seep_day(j)%no3, wet_seep_day(j)%nh3, wet_seep_day(j)%orgn, wet_seep_day(j)%solp, wet_seep_day(j)%sedp, wbody%flo, ht2%flo, wet(j)%sed, wbody%sed, wbody%no3, wbody%nh3, wbody%orgn, wbody%sedp, wbody%solp, ht2%sed, ob(icmd)%hd(1)%temp, ht2%san, ht2%sil, ht2%cla, ht2%sag, ht2%lag, ht2%grv, ht2%orgn, ht2%sedp, ht2%no3, ht2%solp` |
| [sym:time_module] | `time` | `time%step, time%yrs` |
| [sym:basin_module] | `bsn_cc, bsn_prm, pco` | `bsn_cc%gwflow, bsn_prm%prf, pco%nyskip` |
| [sym:channel_module] | `channel_module state and types used by wetland routing` | `icmd, ob` |
| [sym:water_body_module] | `wet_wat_d` | `wet_wat_d(j)%area_ha, wet_wat_d(j)%precip, wet_wat_d(j)%seep` |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(1)%no3, soil1(j)%mn(1)%nh4, soil1(j)%mp(1)%act, soil1(j)%water(1)%n, soil1(j)%water(1)%p` |
| [sym:mgt_operations_module] | `management operation state and types used by wetland routing` | `mgt_ops` |
| [sym:constituent_mass_module] | `constituent mass state and types used by wetland routing` | `cs, wetcs_d, wet_water, wetqcs, wtspcs` |
| [sym:aquifer_module] | `aquifer state and types used by wetland routing` | `aquifer` |
| [sym:gwflow_module] | `gwflow state and types used by wetland routing` | `gwflow` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_wat_d(j)%area_ha` | After the HRU and wetland are bound at the start of the routine | The daily wetland water-body record is initialized to the HRU area so later precipitation, seepage, and output records can use the correct base surface area before any wetland fraction adjustment is applied. |
| `ht2` | After outflow routing and before final output records are written | `ht2` carries the routed outflow hydrograph for the wetland step, including discharge volume and any sediment or constituent loads assigned by the release, sediment, and nutrient routines. |
| `wbody` | During paddy or decision-table release processing when outflow is computed | `wbody` is the shared wetland water-body state that gets updated by release, sediment, nutrient, salt, and constituent routines; the caller later copies its masses back into `wet(j)`. |
| `wbody_wb` | When routed outflow is computed and the wetland is later stored in daily output records | `wbody_wb` points to the daily wetland water-body record so the current area, precipitation, and seepage bookkeeping can be written back for output and mass-balance tracking. |
| `wbody_prm` | At routine entry when the wetland parameter pointer is assigned | `wbody_prm` points to the wetland's parameter record, allowing the routine and any callee to use the wetland-specific parameter set for this HRU. |
| `hru(j)%water_seep` | After seepage is calculated or gwflow exchange returns | `hru(j)%water_seep` is set to the daily seepage depth equivalent so the HRU water balance can account for wetland leakage into the soil or groundwater system. |
| `wet_ob(j)%depth` | After the final wetland depth is recomputed from stored volume | `wet_ob(j)%depth` is refreshed to the current ponded depth so subsequent release logic, output records, and any later wetland bookkeeping use the post-routing water level. |
| `wet_wat_d(j)%precip` | Immediately after precipitation is added to wetland storage | `wet_wat_d(j)%precip` stores the wetland precipitation volume for the day, which is then available for the daily wetland water-body balance and output summaries. |
| `wet(j)%flo` | After precipitation, irrigation, seepage, and release adjustments | `wet(j)%flo` holds the updated wetland storage volume used to compute depth, runoff, and later concentration calculations. |
| `wet(j)%no3` | After the nutrient-water balance is updated and seepage has been removed from wetland storage | `wet(j)%no3` becomes the remaining wetland nitrate mass after seepage and nutrient routing, so later concentration and output calculations use the post-loss value. |
| `wet_wat_d(j)%seep` | When seepage is limited by soil storage and a nonzero seepage volume remains | `wet_wat_d(j)%seep` is reduced to the effective seepage volume that can actually enter the soil profile, after excess water is pushed through the layer-limited storage test. |
| `soil1(j)%mn(1)%no3` | During seepage partitioning into the soil profile | Top-layer soil nitrate increases by the fraction of wetland nitrate carried with seepage, representing nutrient infiltration from ponded water into the soil profile. |
| `soil1(j)%mn(1)%nh4` | During seepage partitioning into the soil profile | Top-layer soil ammonium increases by the fraction of wetland ammonium carried with seepage, representing nutrient infiltration from ponded water into the soil profile. |
| `soil1(j)%mp(1)%act` | During seepage partitioning into the soil profile | Top-layer active phosphorus increases by the fraction of wetland soluble phosphorus carried with seepage, representing phosphorus infiltration into the soil profile. |
| `soil1(j)%water(1)%n` | During seepage partitioning into the soil profile | Top-layer organic nitrogen increases by the fraction of wetland organic nitrogen carried with seepage, moving dissolved/organic N into the soil-water pool. |
| `soil1(j)%water(1)%p` | During seepage partitioning into the soil profile | Top-layer organic phosphorus increases by the fraction of wetland sediment phosphorus carried with seepage, moving phosphorus into the soil-water pool. |
| `wet_seep_day(j)%no3` | After seepage mass is calculated from the wetland load fraction | `wet_seep_day(j)%no3` records the daily nitrate mass lost from the wetland by seepage so the seepage export can be tracked separately from runoff export. |
| `wet_seep_day(j)%nh3` | After seepage mass is calculated from the wetland load fraction | `wet_seep_day(j)%nh3` records the daily ammonium mass lost from the wetland by seepage so the seepage export can be tracked separately from runoff export. |
| `wet_seep_day(j)%orgn` | After seepage mass is calculated from the wetland load fraction | `wet_seep_day(j)%orgn` records the daily organic nitrogen mass lost from the wetland by seepage for downstream bookkeeping. |
| `wet_seep_day(j)%solp` | After seepage mass is calculated from the wetland load fraction | `wet_seep_day(j)%solp` records the daily soluble phosphorus mass lost from the wetland by seepage for downstream bookkeeping. |
| `wet_seep_day(j)%sedp` | After seepage mass is calculated from the wetland load fraction | `wet_seep_day(j)%sedp` records the daily particulate phosphorus mass lost from the wetland by seepage for downstream bookkeeping. |
| `wet(j)%nh3` | After seepage partitioning and nutrient routing | `wet(j)%nh3` is reduced to the ammonium mass remaining in the wetland water after seepage has removed its share of the load. |
| `wet(j)%orgn` | After seepage partitioning and nutrient routing | `wet(j)%orgn` is reduced to the organic nitrogen mass remaining in the wetland water after seepage has removed its share of the load. |
| `wet(j)%solp` | After seepage partitioning and nutrient routing | `wet(j)%solp` is reduced to the soluble phosphorus mass remaining in the wetland water after seepage has removed its share of the load. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:1.2.1 | Pond/wetland daily water balance | $V=V_{stored}+V_{flowin}-V_{flowout}+V_{pcp}-V_{evap}-V_{seep}$ | V=V_stored+V_flowin-V_flowout+V_pcp-V_evap-V_seep: precip added line 77; seep subtracted 137; outflow 192. Inflow via routing network (ht1). |
| 8:1.2.2 | Pond SA = beta_sa*V^expsa | $SA=\beta_{sa}*V^{expsa}$ | Theory: power-law SA=beta_sa*V^expsa. Code: quadratic depth-fraction: x1=bcoef^2+4*ccoef*(1-flo/pvol); wet_h from quadratic; wet_fr=1+acoef*wet_h; area_ha=hru%area_ha*wet_fr. Different functional form. |
| 8:1.2.3 | Pond SA-V exponent expsa | $expsa=\frac{log_{10}(SA_{em})-log_{10}(SA_{pr})}{log_{10}(V_{em})-log_{10}(V_{pr})}$ | expsa=(log10(SA_em)-log10(SA_pr))/(log10(V_em)-log10(V_pr)) not computed. Code uses parametric quadratic shape coefficients (acoef, bcoef, ccoef) instead. |
| 8:1.2.4 | Pond SA-V coefficient beta_sa | $\beta_{sa}=(\frac{SA_{em}}{V_{em}})^{expsa}$ | beta_sa=(SA_em/V_em)^expsa not computed; see 8:1.2.3. |
| 8:1.2.5 | Wetland expsa from normal/max volumes | $expsa=\frac{log_{10}(SA_{mx})-log_{10}(SA_{nor})}{log_{10}(V_{mx})-log_{10}(V_{nor})}$ | expsa=(log10(SA_mx)-log10(SA_nor))/(log10(V_mx)-log10(V_nor)) not computed; code uses quadratic depth-area approach. |
| 8:1.2.6 | Wetland beta_sa from max volumes | $\beta_{sa}=(\frac{SA_{mx}}{V_{mx}})^{expsa}$ | beta_sa=(SA_mx/V_mx)^expsa not computed; see 8:1.2.5. |
| 8:1.2.7 | Wetland precipitation volume | $V_{pcp}=10*R_{day}*SA$ | precip=w%precip*wsa1; wsa1=area_ha*10; =10*R_day*SA. Exact match V_pcp=10*R_day*SA. |
| 8:1.2.8 | Wetland inflow from HRU runoff | $V_{flowin}=fr_{imp}*10*(Q_{surf}+Q_{gw}+Q_{lat})*(Area-SA)$ | V_flowin=fr_imp*10*(Q_surf+Q_gw+Q_lat)*(Area-SA) formed upstream in routing network; wetland receives total inflow as ht1. |
| 8:1.2.9 | Wetland evaporation volume | $V_{evap}=10*\eta*E_o*SA$ | V_evap=10*eta*E_o*SA not found in wetland_control.f90. No explicit open-water evaporation calculation visible; may be handled via HRU ET pathway or absent. |
| 8:1.2.10 | Wetland seepage volume | $V_{seep}=240*K_{sat}*SA$ | seep=min(flo,wet_hc*24.*area_ha*10.); wet_hc*240*area_ha=240*K_sat*SA. Exact match V_seep=240*K_sat*SA (non-gwflow path). |
| 8:1.3.1 | Depression/pothole water balance | $V=V_{stored}+V_{flowin}-V_{flowout}+V_{pcp}-V_{evap}-V_{seep}$ | Same code path as ponds/wetlands. Pothole-specific SA, evaporation, and seepage formulas are not implemented â€” code uses generalized wetland logic. |
| 8:1.3.2 | Depression SA from volume (cone formula) | $SA=\frac{\pi}{10^4}*(\frac{3*V}{\pi *slp})^{2/3}$ | SA=pi/10^4*(3V/(pi*slp))^(2/3) not found in codebase. Code uses quadratic depth-area for all water body types. |
| 8:1.3.3 | Depression precipitation volume | $V_{pcp}=10*R_{day}*SA$ | Same as 8:1.2.7: precip=w%precip*wsa1=10*R_day*SA. |
| 8:1.3.5 | Depression evaporation when LAI < LAI_evap | $V_{evap}=5*(1-\frac{LAI}{LAI_{evap}})*E_o*SA$ | V_evap=5*(1-LAI/LAI_evap)*E_o*SA not found in wetland_control.f90. |
| 8:1.3.6 | Depression evaporation zero when LAI >= LAI_evap | $V_{evap}=0$ | Not implemented; see 8:1.3.5. |
| 8:1.3.7 | Depression seepage when SW < 0.5*FC | $V_{seep}=240*K_{sat}*SA$ | V_seep=240*K_sat*SA (unrestricted) when SW<0.5*FC not coded; code uses wet_hc*240*SA without SW/FC conditioning. |
| 8:1.3.8 | Depression seepage when 0.5*FC <= SW < FC | $V_{seep}=240*(1-\frac{SW}{FC})*K_{sat}*SA$ | V_seep=240*(1-SW/FC)*K_sat*SA not implemented. |
| 8:1.3.9 | Depression seepage zero when SW >= FC | $V_{seep}=0$ | min(flo, wet_hc*240*SA) does not check SW>=FC explicitly. Soil percolation logic (swr_substor) limits percolation when saturated, but SW/FC threshold is not directly coded here. |

## Lineage

`wetland_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 14 non-merge commit(s) since, most recently `f8d2c4a` (2026-04-07, "fix: correct outflow subtraction from storage in reservoir and wetland"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wetland_control.f90` are listed.

- `f8d2c4a` (2026-04-07) — fix: correct outflow subtraction from storage in reservoir and wetland
- `9d9069f` (2026-03-31) — gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renames, heat/pond/phreatophyte types, stubs
- `3e18acf` (2026-02-17) — Integrate CENTURY residue/N updates and root-fraction tracking changes
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `645ac00` (2025-12-11) — merge rice paddy management code
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wetland_control' has no extracted documentation comment.
- conditional_module and channel_module outside-state details were not resolved from candidate refs in the evidence packet, so their outside/components values are summarized from usage in the source and caller contracts.
- algorithm_steps revised: merged the draft's broad call/state buckets into 13 source-backed steps that follow the actual control flow from initialization through final output.
- The source has no direct file I/O in the extracted span.
- The `state_changes[3]` and `summary_variables[3]` fields refer to `wbody_wb`, which is documented in the overlay skeleton but not shown as a separate declaration in the source packet; it is treated here as the wetland-water-body pointer alias established at lines 65-67.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
