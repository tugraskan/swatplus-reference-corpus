---
kind: procedure
symbol: cbn_zhang2
title: cbn_zhang2
status: filled
source_hash: 216daff006c687b9
version_label: SWAT+ 62.0.0
locals:
  j: HRU index taken from `ihru`; selects the active HRU whose soil profile and residue pools
    are processed.
  k: Current soil-layer index in the main loop over `soil(j)%nly`.
  kk: Auxiliary layer index used when layer 1 needs temperature or depth values from layer
    2 for response calculations.
  lmnta: Actual nitrogen transformed out of the metabolic litter pool after supply-demand
    limits are applied.
  min_n_ppm: Profile mineral nitrogen concentration in ppm, used in lower layers to set nitrogen
    ratios and passive/slow humus allocations.
  min_n: Amount of nitrate moved from the mineral pool to ammonium when excess mineral nitrogen
    is available after demand balancing.
  cf_lyr: 'Selects which carbon coefficient set to use: layer 1 for surface conditions or
    layer 2 for subsurface conditions.'
  soil_lyr_thickness: Temporary soil-layer thickness accumulator; initialized but not used
    in the shown calculations.
  sol_mass: Computed soil mass for the current layer in kg/ha, used to convert mineral nitrogen
    totals to concentration units.
  sol_min_n: Total mineral nitrogen in the layer (`no3 + nh4`), used when computing concentration
    and supply checks.
  fc: Field-capacity water amount for the current layer, used in the soil-water response factor.
  wc: Current layer water content plus wilting water, used to evaluate soil-water stress and
    pore-space terms.
  sat: Potential saturation water amount; declared but not used in the shown code.
  void: Void-space or pore-space-related temporary value; declared for alternative water/oxygen
    calculations but not used in the active branch.
  stemp: Current soil-layer temperature, used to gate decomposition and compute the temperature
    response factor.
  x3: Temporary carbon transfer sum from passive, slow, metabolic, and non-lignin structural
    pools into microbial biomass for the EPIC-style update block.
  lscta: Actual carbon transformed from the structural litter pool after nitrogen supply-demand
    reduction.
  lslcta: Actual carbon transformed from the lignin portion of structural litter after reduction.
  lslncta: Actual carbon transformed from the non-lignin portion of structural litter after
    reduction.
  lsnta: Actual nitrogen transformed from structural litter after reduction.
  lmcta: Actual carbon transformed from metabolic litter after reduction.
  nf: Temporary nitrogen-related scalar noted in comments; initialized but not used in the
    active calculations shown.
  a1: Allocation factor equal to `1 - org_allo(cf_lyr)%a1co2`; used in litter-to-biomass nitrogen
    demand calculations.
  asx: Allocation complement for slow-humus transformations, equal to `1 - asco2 - asp`.
  apx: Allocation complement for passive-humus transformations, equal to `1 - apco2`.
  df1: Difference between structural litter nitrogen supply and its demand in the EPIC-style
    bookkeeping block.
  df2: Difference between metabolic litter nitrogen supply and its demand in the EPIC-style
    bookkeeping block.
  snmn: Temporary nitrogen pool variable that is initialized but not used in the active code
    path shown.
  df3: Difference between microbial biomass nitrogen supply and demand in the EPIC-style bookkeeping
    block.
  df4: Difference between slow humus nitrogen supply and demand in the EPIC-style bookkeeping
    block.
  df5: Difference between passive humus nitrogen supply and demand in the EPIC-style bookkeeping
    block.
  df6: Difference between available mineral nitrogen and nitrate demand in the EPIC-style
    bookkeeping block.
  add: Signed total nitrogen balance across the EPIC-style difference terms.
  adf1: Absolute magnitude of `df1`, used when forming the weighting total `tot`.
  adf2: Absolute magnitude of `df2`, used when forming the weighting total `tot`.
  adf3: Absolute magnitude of `df3`, used when forming the weighting total `tot`.
  adf4: Absolute magnitude of `df4`, used when forming the weighting total `tot`.
  adf5: Absolute magnitude of `df5`, used when forming the weighting total `tot`.
  tot: Sum of absolute EPIC-style nitrogen demand terms, used to scale the correction factor
    `xx`.
  pn1: Potential nitrogen demand from structural litter to biomass transformation.
  pn2: Potential nitrogen demand from structural litter to slow humus transformation.
  pn3: Potential nitrogen demand from metabolic litter to biomass transformation.
  pn4: Placeholder for biomass-to-leaching nitrogen demand; not computed here because that
    process is handled elsewhere.
  pn5: Potential nitrogen demand from microbial biomass to passive humus transformation.
  pn6: Potential nitrogen demand from microbial biomass to slow humus transformation.
  pn7: Potential nitrogen demand from slow humus to biomass transformation.
  pn8: Potential nitrogen demand from slow humus to passive humus transformation.
  pn9: Potential nitrogen demand from passive humus to biomass transformation.
  cpn1: Nitrogen deficit for structural litter transformations after comparing structural
    demand with actual structural N supply.
  cpn2: Nitrogen deficit for metabolic litter transformations after comparing metabolic demand
    with actual metabolic N supply.
  cpn3: Nitrogen deficit for microbial biomass transformations after comparing biomass demand
    with actual biomass N supply.
  cpn4: Nitrogen deficit for slow humus transformations after comparing slow-humus demand
    with actual slow-humus N supply.
  cpn5: Nitrogen deficit for passive humus transformations after comparing passive-humus demand
    with actual passive-humus N supply.
  wmin: Available mineral plus surplus organic nitrogen used to determine whether total N
    supply can satisfy total transformation demand.
  trnn: Total nitrogen demand across the five SOM transformation groups.
  wdn: Denitrification loss of nitrate in the current layer, computed from moisture, temperature,
    and nitrate stock.
  deltawn: Temporary nitrate-loss delta; initialized but not used in the active code shown.
  deltabmc: Temporary biomass-carbon change term; initialized but not used in the active code
    shown.
  snta: Placeholder/temporary storage for structural nitrogen transfer accounting; initialized
    but not used in the active code shown.
  rlr: Fraction of structural litter that is lignin, capped at 0.8 and used to split structural
    carbon flow.
  xbm: Microbial biomass activity multiplier based on surface versus subsurface layer properties.
  bmcta: Actual carbon transformed from microbial biomass after nitrogen limitation is applied.
  bmnta: Actual nitrogen transformed from microbial biomass after nitrogen limitation is applied.
  hscta: Actual carbon transformed from slow humus after nitrogen limitation is applied.
  hsnta: Actual nitrogen transformed from slow humus after nitrogen limitation is applied.
  hpcta: Actual carbon transformed from passive humus after nitrogen limitation is applied.
  hpnta: Actual nitrogen transformed from passive humus after nitrogen limitation is applied.
  fcgd: Temperature-response multiplier for decomposition when `org_con%tmpf == 2`; it is
    stored for the current layer and feeds the combined biological control factor.
  rsdn_pct: Relative residue nitrogen percentage used in the surface layer to determine biomass
    C:N ratios and passive-humus allocation.
  sum: Total surplus nitrogen available from all pools after demand comparison; also reused
    as the organic surplus when forming the mineral-N supply test.
  sum1: Surplus nitrogen from structural litter transformations when structural supply exceeds
    structural demand.
  sum2: Surplus nitrogen from metabolic litter transformations when metabolic supply exceeds
    metabolic demand.
  sum3: Surplus nitrogen from microbial biomass transformations when biomass supply exceeds
    biomass demand.
  sum4: Surplus nitrogen from slow humus transformations when slow-humus supply exceeds slow-humus
    demand.
  sum5: Surplus nitrogen from passive humus transformations when passive-humus supply exceeds
    passive-humus demand.
  reduc: Scaling factor applied to actual carbon and nitrogen transformations when total nitrogen
    supply is insufficient.
  rnmn: Net mineral nitrogen balance (`sum - trnn`); if positive, extra nitrate is moved to
    ammonium.
  hmp_rate: Humus mineralization rate for organic phosphorus, computed from slow and passive
    humus nitrogen fluxes.
  hmp: Actual phosphorus moved from passive humus to the labile mineral P pool.
  decr: Fraction of fresh organic nitrogen/phosphorus that is decomposed from surface and
    litter pools.
  rmp: Fresh organic phosphorus moved from total organic P to the labile and passive mineral
    P pools.
  rto: Actual C:N ratio used to update metabolic litter mass after carbon loss.
  rspc: Per-soil-layer heterotrophic (microbial) respiration carbon released as CO2 for the
    current layer; each layer value is accumulated into hsc_d(j)%rsp_c as the day total soil
    CO2-C emission.
  xx: Composite nitrogen-balance factor used in the EPIC-style bookkeeping block.
  xx1: Intermediate soil-water response factor in the `watf == 2` branch.
  xx2: Intermediate pore-space response factor in the `watf == 2` branch.
  w1: First multiplicative component of the `watf == 2` soil-water control factor.
  w2: Second multiplicative component of the `watf == 2` soil-water control factor.
  svoid: Computed soil void-space fraction used only in the `watf == 2` soil-water response
    branch.
uses:
  hru_module: '`hru_module` supplies the HRU-specific tillage depth boundary that the routine
    compares against each layer''s depth to decide whether tillage should increase decomposition
    in that layer.'
  soil_module: '`soil_module` holds the per-HRU soil profile, layer counts, depths, water
    states, and texture properties that drive every layer loop and control the temperature,
    moisture, oxygen, and tillage response factors.'
  basin_module: '`basin_module` provides the basin-level tillage method selector and denitrification
    parameters that determine which tillage formula is used and when nitrate losses are allowed.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` stores the HRU soil-pool state
    that this routine reads, updates, and then writes back into layer-level history arrays
    and daily totals.'
  carbon_module: '`carbon_module` provides the shared carbon-control, allocation, ratio, and
    transformation structures that are populated here and then reused by the rest of the soil
    carbon/nutrient workflow.'
  output_landscape_module: '`output_landscape_module` records the HRU denitrification total
    that this routine increments after computing layer nitrate loss, so later output routines
    can report the daily nitrogen balance.'
  tillage_data_module: '`tillage_data_module` matters because the routine uses its tillage-effect
    timing threshold when applying the DSSAT tillage branch, so the active tillage response
    depends on data imported from this module.'
---

<!-- facts:header -->

Computes layer-by-layer carbon, nitrogen, and phosphorus pool transformations for the SWAT+ CENTURY-based soil organic matter routine, including tillage, temperature, moisture, and oxygen controls.

## Bottom Line

`cbn_zhang2` is the main per-HRU soil organic matter routine used by the SWAT+ carbon/nitrogen pathway. For each soil layer, it builds environmental response factors, computes potential carbon and nutrient transformations among litter, microbial biomass, slow humus, and passive humus, then applies supply-demand limits so the actual carbon and nutrient transfers stay internally consistent.

It also updates denitrification losses, residue decay accounting, soil respiration, and the layer-level output records that later routines use for landscape and nutrient balance reporting. The routine is called from `hru_control` during the carbon/mineralization step after residue transfer has been prepared.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cbn_zhang2` runs inside `hru_control` after surface-residue decomposition and residue transfer have been prepared, and before the nitrogen-volatilization and phosphorus-mineralization routines. Its outputs matter because later daily HRU accounting depends on the updated mineral nitrogen pools, organic pool masses, residue-decay totals, respiration, and layer-level carbon flux records it writes back.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and clear daily residue counters. | Use `ihru` to choose the current HRU, then reset the HRU-level surface and root residue decay accumulators before any layer processing begins. |
| 2. Initialize per-HRU and per-layer working storage. | Set the daily organic-flux total to zero, loop over all soil layers, and initialize the layer copies of `org_con`, `org_ratio`, `org_flux`, `org_tran`, and `org_allo` that hold the intermediate carbon and nitrogen bookkeeping for that layer. |
| 3. Compute layer mass, water, temperature, and tillage response factors. | Derive soil mass from layer thickness, bulk density, and rock content; choose the layer coefficient set; then compute soil-water control, tillage effect, temperature response, oxygen response, and the combined biological control factor `org_con%cs`. |
| 4. Apply denitrification and set layer-specific C:N ratios and allocations. | Use basin denitrification thresholds to remove nitrate and accumulate `hnb_d(j)%denit`, then determine residue and humus C:N ratios and passive-humus allocation fractions from residue N, mineral N concentration, clay, and sand. |
| 5. Compute potential carbon transformations among SOM pools. | Calculate potential carbon flow rates from structural, metabolic, microbial, slow-humus, and passive-humus pools using the coefficient database `carbdb`, the current control factors, and the pool masses. |
| 6. Estimate nitrogen demand and balance supply against demand. | Form the nitrogen demand terms `pn1` through `pn9`, compare them with the corresponding actual nitrogen supplies, accumulate deficits and surpluses, and compute the reduction factor `reduc` when total supply is insufficient. |
| 7. Apply supply-limited actual transformations. | Scale the actual carbon and nitrogen transformations for structural litter, metabolic litter, microbial biomass, slow humus, and passive humus using `reduc` whenever a pool is nitrogen-limited; otherwise keep the potential rates. |
| 8. Recompute N demand after reductions and move excess mineral N. | Recalculate the demand terms from the actual transformations, compare them again with supply, and if the balance is positive move excess nitrate to ammonium in the layer mineral pool. |
| 9. Compute phosphorus transfers tied to humus and residue decay. | Derive humus mineralization and fresh organic P losses from the current carbon turnover rate, then move P between humus, labile mineral P, and passive pools. |
| 10. Call nutrient-flow accounting for each carbon transfer. | For each major carbon flow, call `nut_np_flow` to compute the associated nutrient immobilization or mineralization for passive-to-microbial, slow-to-microbial, metabolic-to-microbial, structural-to-microbial, structural-to-slow, microbial-to-slow, microbial-to-passive, and slow-to-passive transfers. |
| 11. Update pool masses, respiration, and layer diagnostics. | Apply the computed carbon and nitrogen losses and gains to the litter, biomass, slow-humus, passive-humus, nitrate, and ammonium pools; accumulate layer respiration and residue-decay totals; then save the updated control, ratio, allocation, flux, and pool-summary records back to the HRU profile. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `tillage_depth` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(k)%thick, soil(j)%phys(k)%bd, soil(j)%phys(k)%rock, soil(j)%phys(k)%tmp, soil(j)%phys(k)%st, soil(j)%phys(k)%fc, soil(j)%phys(k)%wpmm, soil(j)%phys(kk)%st, soil(j)%phys(k)%por, soil(j)%phys(k)%ul, soil(j)%phys(k)%d, soil(j)%phys(k-1)%d, soil(j)%ly(k)%tillagef, soil(j)%phys(kk)%d, soil(j)%phys(kk-1)%d, soil(j)%phys(k)%clay, soil(j)%phys(k)%sand` |
| [sym:basin_module] | `bsn_cc, bsn_prm` | `bsn_cc%idc_till, bsn_prm%sdnco, bsn_prm%cdn` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass` | `soil1(j)%org_flx_tot, soil1(j)%org_con_lr(k), soil1(j)%org_ratio_lr(k), soil1(j)%org_flx_lr(k), soil1(j)%org_tran_lr(k), soil1(j)%org_allo_lr(k), soil1(j)%mn(k)%no3, soil1(j)%cbn(k), soil1(j)%mn(k)%nh4, soil1(j)%str(k)%m, pl_mass(j)%rsd_tot%n, soil1(j)%meta(1)%n, pl_mass(j)%rsd_tot%c, soil1(j)%str(k)%c, soil1(j)%str(k)%n, soil1(j)%meta(k)%c, soil1(j)%meta(k)%n, soil1(j)%microb(k)%c, soil1(j)%microb(k)%n, soil1(j)%hs(k)%c` |
| [sym:carbon_module] | `org_con, org_frac, org_tran, hrc_d, org_allo, org_ratio, carbdb` | `org_con%x1, org_frac%lmf, org_frac%lsf, org_frac%lslf, org_tran%lsctp, hrc_d(j)%rsd_surfdecay_c, hrc_d(j)%rsd_rootdecay_c, org_con%sut, org_con%cdg, org_con%cs, org_con%ox, org_con%no3, org_con%nh4, org_con%resp, org_con%till_eff, org_allo(cf_lyr)%abp, org_allo(cf_lyr)%asp, org_con%watf, org_con%tmpf, org_ratio%nchp, org_ratio%ncbm, org_ratio%nchs, org_allo(cf_lyr)%abco2, carbdb(cf_lyr)%str_rate, org_tran%lslctp, org_tran%lslnctp, org_tran%lsntp, carbdb(cf_lyr)%meta_rate, org_tran%lmctp, org_tran%lmntp, carbdb(cf_lyr)%microb_top_rate, carbdb(cf_lyr)%microb_rate, org_tran%bmctp, org_tran%bmntp, carbdb(cf_lyr)%hs_rate, org_tran%hsctp, org_tran%hsntp` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%denit` |
| [sym:tillage_data_module] | `tillage_data_module state used for tillage effects` | `till_eff_days` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `org_con%x1` | After the structural-litter potential transformation block has been computed for the current layer. | This variable temporarily holds the structural-litter nitrogen demand threshold (`pn1 + pn2`) so the code can compare it with actual structural nitrogen supply and decide whether the layer has a deficit or surplus. |
| `org_frac%lmf` | When the structural litter carbon flow is initialized from `carbdb(cf_lyr)%str_rate` and `org_con%cs`, and before the demand check resets it to `pn1 + pn2`. | This routine clears the litter-fraction working copy at the start of each layer, so later calculations can rebuild litter partitioning from the current HRU state rather than from stale values. |
| `org_frac%lsf` | When the structural litter carbon flow is initialized from `carbdb(cf_lyr)%str_rate` and `org_con%cs`, and before the demand check resets it to `pn1 + pn2`. | This routine clears the litter-fraction working copy at the start of each layer, so later calculations can rebuild litter partitioning from the current HRU state rather than from stale values. |
| `org_frac%lslf` | When the structural litter carbon flow is initialized from `carbdb(cf_lyr)%str_rate` and `org_con%cs`, and before the demand check resets it to `pn1 + pn2`. | This routine clears the litter-fraction working copy at the start of each layer, so later calculations can rebuild litter partitioning from the current HRU state rather than from stale values. |
| `org_tran%lsctp` | Whenever a potential carbon flow into a pool is calculated from `carbdb(cf_lyr)%str_rate`, `meta_rate`, `microb_rate`, `hs_rate`, or `hp_rate`. | This stores the current layer's potential structural-litter carbon transformation, which is then used in the nitrogen-demand checks and in the later actual-pool updates. |
| `hrc_d(j)%rsd_surfdecay_c` | For the surface layer after `lscta = lmcta + lscta` is assigned and the routine records residue decay for printing. | The surface residue decay total is set to the actual carbon lost from metabolic plus structural litter in layer 1 so the HRU output can report how much surface residue decomposed that day. |
| `hrc_d(j)%rsd_rootdecay_c` | For any subsurface layer after `lscta = lmcta + lscta` is assigned and the routine records residue decay for printing. | The root/subsurface residue decay total is set to the actual carbon lost from metabolic plus structural litter below the surface so the HRU output can report root and incorporated-residue decay. |
| `soil1(j)%org_flx_tot` | After the actual carbon and nitrogen updates have been applied to the layer pools and before the layer total is accumulated. | This daily HRU total is incremented by the current layer's full organic flux record so later reporting can summarize all layer-level organic transfers for the day. |
| `org_con%sut` | After the actual carbon and nitrogen updates have been applied and the layer respiration has been computed. | The soil-water control is not a persistent state change itself, but the routine stores the current layer value in the layer record so later consumers can see the control factor that governed this day's transformations. |
| `org_con%cdg` | After the actual carbon and nitrogen updates have been applied and the layer respiration has been computed. | The temperature control value is saved in the layer record so later consumers can see the control factor that governed this day's transformations. |
| `org_con%cs` | After the actual carbon and nitrogen updates have been applied and the layer respiration has been computed. | The combined biological control factor is saved in the layer record so later consumers can see the overall multiplier that governed this day's transformations. |
| `org_con%ox` | After the actual carbon and nitrogen updates have been applied and the layer respiration has been computed. | The oxygen control factor is saved in the layer record so later consumers can see the depth-dependent aeration limit used in this day's decomposition calculations. |
| `org_con%no3` | After denitrification is computed in the current layer. | The layer nitrate value is copied into the control record so the current day’s post-denitrification nitrate state is preserved alongside the other layer controls. |
| `org_con%nh4` | After denitrification is computed in the current layer. | The layer ammonium value is copied into the control record so the current day’s mineral nitrogen state is preserved alongside the other layer controls. |
| `org_con%resp` | After respiration is computed for the current layer. | The layer CO2 flux is copied into the control record so the current day’s respiration output can be saved with the layer controls and output arrays. |
| `org_con%till_eff` | When the tillage branch is evaluated inside the moisture/temperature-active layer block. | The current tillage efficiency is recomputed from the basin tillage method and HRU tillage state, because it directly scales decomposition rates for this layer on this day. |
| `soil1(j)%org_con_lr(k)` | After the actual transformations are computed and before they are written back to the soil profile record. | The layer copy of the control record is updated so the HRU profile retains the exact environmental factors and denitrification result used for that layer on that day. |
| `org_ratio` | After the residue nitrogen content and mineral nitrogen concentration are evaluated for the current layer. | The shared layer working record is overwritten with the current layer's biomass, slow-humus, and passive-humus N:C ratios so later transformations use the layer-specific values. |
| `soil1(j)%org_ratio_lr(k)` | After the residue nitrogen content and mineral nitrogen concentration are evaluated for the current layer. | The layer ratio record is saved so later diagnostics and output routines can retrieve the exact N:C ratios used for that layer on that day. |
| `org_flux` | After the potential carbon flows are computed and before nitrogen-demand balancing begins. | The flux record is filled with the current layer's transformation, immobilization, mineralization, and CO2 terms so later code can use the complete accounting package for updates and output. |
| `soil1(j)%org_flx_lr(k)` | After the potential carbon flows are computed and before nitrogen-demand balancing begins. | The layer-level flux record is stored so the profile retains all carbon and nutrient exchange terms for that layer on that day. |
| `org_tran` | After the actual carbon and nitrogen pool updates have been computed for the current layer. | The current layer's transformation rates are preserved in the shared working record so the post-update profile snapshot contains the final actual rates rather than only the potentials. |
| `soil1(j)%org_tran_lr(k)` | After the actual carbon and nitrogen pool updates have been computed for the current layer. | The layer-level transformation record is saved for later output and diagnostics, capturing the final actual transformation rates for that layer on that day. |
| `org_allo(cf_lyr)%abp` | When the passive-humus allocation is re-evaluated from clay content. | The passive-humus allocation fraction is updated for the current coefficient layer because it controls how much microbial biomass carbon can move to passive humus in later pool transfers. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:5.1.4 | Maximum slow humus capacity S_CC and alpha=6 | $S_{CC}=S_{BD}Z_l(0.021+0.38clay)$ | S_CC=S_BD*Z_l*(0.021+0.38*clay) and alpha=6 are not computed in cbn_zhang2; code uses fixed CENTURY allocation fractions instead. |
| 3:5.1.5 | Dynamic C:N ratio S_CN of slow humus | $S_{CN}=8.5+2.7(1-\frac{1}{1+(\frac{R_{CN}}{110})^3})(1+\frac{1}{1+(\frac{N_{min}}{8})^3})$ | ncbm/nchs/nchp ratios set from rsdn_pct and min_n_ppm via empirical expressions; differs from theory eq S_CN=8.5+2.7*(...) |
| 3:5.1.7 | Slow humus transformation rate k_S | $k_S=k_xf_{tool}f_E(\frac{S_C}{S_{CC}})^{\beta}.$ | x1=hs_rate*cs; hsctp=hs%c*x1; implements k_S*f_E*S_C without the (S_C/S_CC)^beta concentration-feedback term. |
| 3:5.1.8 | Tillage factor f_tool | $f_{tool}=1+(3+5e^{-5.5clay})(\frac{f_{cm}}{f_{cm}+e^{1-2f_{cm}}})$ | Verified against SWAT+ 62.0.0 (cbn_zhang2.f90:357). theory's clay S-curve f_tool (`3+5e^-5.5clay`) NOT implemented; code uses constant 1.6 + depth interp (:365-370) |
| 3:5.1.2a | Slow humus C flux (dS_C/dt) | $k_R=k_M=1$ | hsctp=hs%c*hs_rate*cs; slow humus loses hscta and gains from litter+biomass pools (x1 at line 878). Full dS_C/dt balance across lines 875-883. |
| 3:5.1.2b | Slow humus N flux (dS_N/dt) | $\frac{dS_N}{dt}=\frac{h_R f_E k_R R_C+h_Mf_Ek_MM_C}{S_{CN}}-k_SS_N,$ | hs%n updated with all N flows to/from slow pool (lines 966-973); implements dS_N/dt. |
| 3:5.1.3a | Humification efficiency h_R (structural litter) | $h_R=h_x(1-(\frac{S_C}{S_{CC}})^{\alpha}),$ | pn1=lslncta*a1*ncbm; pn2=0.7*lslcta*nchs; allocation fractions (a1, 0.7) are CENTURY constants, not the dynamic h_R=(1-(S_C/S_CC)^alpha) formula. |
| 3:5.1.3b | Humification efficiency h_M = 1.6*h_R | $h_M=1.6h_R,$ | Verified against SWAT+ 62.0.0 (cbn_zhang2.f90:365). tillage factor `till_eff = 1.6` (DSSAT case) |
| 3:5.1.6a | N mineralization from structural litter (MIN_RN) | $MIN_{RN}=\frac{dR_C}{dt}(\frac{1}{R_{CN}}-\frac{h_R}{S_{CN}}),$ | rnmn=sum-trnn; sum=N supply from pool decompositions, trnn=N demand. Mineral pool updated at lines 721-724. |
| 3:5.1.6b | N mineralization from metabolic litter (MIN_MN) | $MIN_{MN}=\frac{dM_C}{dt}(\frac{1}{M_{CN}}-\frac{h_M}{S_{CN}}),$ | Same rnmn update covers both MIN_RN and MIN_MN contributions. |
| 3:5.3.1 | Carbon sub-model analytical solution | $\frac{dS_C}{dt}=h_xR_C-\frac{h_xR_C}{S_x}S_C-\frac{k}{S_x}S^2_C$ | Analytical/steady-state solution derived from the ODEs. Not a direct numerical step; serves as reference for parameter interpretation. |
| 3:5.3.2 | Carbon sub-model analytical solution | $S_C(t)=\frac{h_xR_C}{2k}[(\frac{\phi e^{\frac{\gamma_t}{S_x}}-1}{\phi e^{\frac{\gamma _t}{S_x}}+1})\sqrt{1+\frac{4kS_x}{h_xR_C}}-1]$ | Analytical/steady-state solution derived from the ODEs. Not a direct numerical step; serves as reference for parameter interpretation. |
| 3:5.3.3 | Carbon sub-model analytical solution | $S_C=\frac{h_xR_C}{2k}\sqrt{1+\frac{4kS_x}{h_xR_C}}-1]$ | Analytical/steady-state solution derived from the ODEs. Not a direct numerical step; serves as reference for parameter interpretation. |
| 3:5.3.4 | Carbon sub-model analytical solution | $1+\frac{1}{2}\frac{4kS_x}{h_xR_C}$ | Analytical/steady-state solution derived from the ODEs. Not a direct numerical step; serves as reference for parameter interpretation. |

## Lineage

`cbn_zhang2.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 76 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cbn_zhang2.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `d2a214e` (2026-05-18) — Changed the min value of org_con%cs to 15
- `a96057d` (2026-05-15) — Fixed issue of tillagef not being initialized to 0. in cbn_zhang2. Corrected mgt_biomass to correctly reflect the potentional bio mixing for…
- `5fc6ffe` (2026-05-14) — Added comments to define variables in cbn_zhang2
- `5323b15` (2026-05-13) — Initial changes to calculate non-lignin c and output to hru_cpool_stat
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cbn_zhang2' has no extracted documentation comment.
- algorithm_steps revised: merged the original draft's broad work/call/state steps into 11 source-backed steps tied to visible line ranges.
- Source uncertainty: `tillage_data_module` is imported, but the packet did not resolve any explicit symbols from that module beyond the active tillage threshold usage in the code comments/logic.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
