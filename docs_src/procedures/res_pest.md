---
kind: procedure
symbol: res_pest
title: res_pest
status: filled
source_hash: df6d5269c42f9186
version_label: SWAT+ 62.0.0
args:
  jres: Reservoir index. It selects the reservoir object, its associated inflow connection,
    sediment property record, water-body area, and daily pesticide storage/output arrays that
    this routine updates.
locals:
  tpest1: Working water-column pesticide mass for the current pesticide. It starts as incoming
    load plus stored water mass and is reduced by reaction, volatilization, settling, resuspension
    adjustments, diffusion, and outflow before the final water-store update.
  tpest2: Working benthic pesticide mass for the current pesticide. It begins from the stored
    benthic mass and is modified by settling, resuspension, diffusion, reaction in the benthic
    layer, and burial before the final benthic-store update.
  kd: Partition coefficient used to convert sediment characteristics into dissolved/sorbed
    fractions. It is computed from pesticide Koc and reservoir sediment organic carbon and
    drives the water-column and benthic fraction calculations.
  fd1: Dissolved fraction of pesticide in the reservoir water column. It is derived from kd
    and sediment loading and is used for volatilization and dissolved outflow calculations.
  fd2: Dissolved fraction of pesticide in the benthic active layer. It is derived from kd
    and benthic sediment properties and is used in the sediment-water diffusion calculation.
  fp1: Sorbed fraction of pesticide in the reservoir water column. It is computed as 1 - fd1
    and is used for settling and sorbed outflow.
  fp2: Sorbed fraction of pesticide in the benthic active layer. It is computed as 1 - fd2
    and represents the benthic particulate share paired with fd2.
  depth: Average reservoir water depth used to convert areal transport velocities into mass
    losses. It is the geometric depth of the reservoir and scales volatilization, settling,
    and outflow terms.
  solpesto: Working amount of dissolved pesticide leaving the reservoir with outflow. It is
    computed from flow, dissolved fraction, and water concentration, then subtracted from
    tpest1.
  sorpesto: Working amount of sorbed pesticide leaving the reservoir with outflow. It is computed
    from flow, sorbed fraction, and the remaining water-column mass, then subtracted from
    tpest1.
  sedmass_watervol: Intermediate conversion factor representing sediment mass per water volume.
    It is used to estimate partitioning in the water column and in the benthic layer from
    sediment bulk properties.
  pest_init: Baseline mass before a decay calculation. It is used to measure how much pesticide
    was lost to reaction in the water or benthic layer during the current stage of the update.
  pest_end: Post-decay mass remaining after applying the pesticide decay factor. It is used
    to update the working mass and derive the reaction loss.
  mol_wt_rto: Molecular-weight ratio used when transferring parent decay mass to daughter
    pesticides. It converts parent-loss mass into the daughter pesticide mass basis.
  ipest_db: Lookup index into the pesticide database for the current simulated pesticide.
    It links the reservoir’s sequential pesticide number to the pesticide property tables.
  ipseq: Sequential basin pesticide number for a daughter pesticide. It is used to target
    metabolite accumulation in the reservoir pesticide arrays.
  ipdb: Database index for a daughter pesticide. It is used to obtain the daughter pesticide
    molecular weight for metabolite mass conversion.
  imeta: Counter over a pesticide’s daughter products. It loops through all metabolites declared
    for the current parent pesticide.
  ipst: Loop index over simulated pesticides in the reservoir. It identifies which pesticide
    state and output entries are being updated.
  icmd: Connectivity-object index for the reservoir’s command/routing object. It is used to
    reach the inflow hydrograph and object properties for this reservoir.
  jsed: Index into reservoir sediment data for the current reservoir. It selects the sediment
    organic carbon and bulk density used in partitioning and sediment exchange calculations.
  idb: Reservoir property-data index for the current reservoir. It selects the reservoir’s
    sediment type record used to locate sediment properties.
uses:
  reservoir_data_module: This module supplies the reservoir sediment property records that
    determine the partitioning and mass-conversion terms used by res_pest. The procedure needs
    the current reservoir’s sediment type to read organic carbon and bulk density, which drive
    the dissolved/sorbed fractions in water and benthic sediment.
  reservoir_module: This module holds the reservoir object map and shared pesticide process
    variables that res_pest both reads and writes. It provides the reservoir-to-object link,
    the water-body-specific mixing velocity array, and the shared process outputs for volatilization,
    settling, resuspension, diffusion, and burial.
  res_pesticide_module: This module stores the per-reservoir pesticide process output arrays
    that res_pest populates. Those fields record how much pesticide entered, reacted, metabolized,
    volatilized, settled, resuspended, diffused, buried, and remained in water or benthic
    storage for later reporting and routing.
  hydrograph_module: This module provides the reservoir hydrology and connectivity fields
    that control pesticide transport. The reservoir flow gives the water volume used for concentration
    and outflow terms, the command-object properties select the matching reservoir record,
    and the temporary hydrograph flow ht2%flo supplies the outgoing discharge used in pesticide
    export.
  constituent_mass_module: This module supplies the constituent bookkeeping arrays that map
    simulation pesticide numbers to sequential indices and store reservoir hydrograph masses.
    res_pest uses the pesticide count to loop, the mapping arrays to resolve parent and daughter
    pesticide numbers, and the reservoir water/benthic mass arrays to read and update stored
    pesticide amounts.
  pesticide_data_module: This module provides the pesticide-specific properties that govern
    every transformation and exchange rate in res_pest. The routine reads decay factors, metabolite
    definitions, molecular weights, and transfer velocities from these tables to compute reaction,
    metabolite transfer, volatilization, settling, resuspension, diffusion, and burial.
  water_body_module: This module supplies the reservoir surface area used to convert reservoir
    volume into average depth. That depth is required to turn areal transport coefficients
    into mass losses for volatilization, settling, and outflow.
---

<!-- facts:header -->

Computes the daily pesticide mass balance for a reservoir, splitting pesticide between water and benthic sediment and tracking transformations, exchanges, and routing losses.

## Bottom Line

res_pest updates reservoir pesticide state for each simulated pesticide when a reservoir has water volume. It starts from incoming water pesticide mass plus stored water and benthic mass, then applies water-column decay, metabolite transfer, volatilization, settling, resuspension, sediment-water diffusion, benthic decay, burial, and outflow routing.

The routine writes process-level diagnostics to respst_d and updates the reservoir storage states in res_water and res_benthic, with the routed pesticide leaving the reservoir summed into hcs2%pest for downstream transport by the command/connection flow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

res_control calls res_pest during the reservoir pesticide transformation phase, after reservoir hydrology has been updated and after res_nutrient has run. res_control has already set up the current reservoir object, command connectivity, incoming constituent hydrographs, and reservoir storage states so res_pest can update pesticide masses and place the routed export in hcs2 for the next routing step.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Enter the reservoir-only pesticide update when the reservoir has positive water volume. | The routine skips all pesticide processing if the reservoir is effectively dry; otherwise it iterates over every simulated pesticide in cs_db%num_pests. |
| 2. Resolve reservoir, sediment, and pesticide lookup indices and load the current pesticide mass state. | It maps the reservoir to its connectivity object, reservoir properties, sediment data, and pesticide database index, then captures incoming water pesticide mass and current benthic storage into working variables. |
| 3. Compute water-column geometry and dissolved/sorbed fractions for the water and benthic compartments. | The routine derives average depth, estimates sediment loading per water volume, computes kd from pesticide Koc and sediment carbon, then calculates dissolved and sorbed fractions for the water column and benthic layer. |
| 4. Apply first-order decay in the water column and transfer the lost mass to daughter pesticides. | If there is enough pesticide mass to matter, the routine decays the water-column mass with decay_a, stores the reaction loss, then distributes daughter metabolite mass using each daughter’s soil fraction and molecular-weight ratio. |
| 5. Compute volatilization loss from the water column and subtract it from the working water mass. | Volatilization is calculated from the pesticide aquatic volatilization coefficient, dissolved fraction, current mass, and depth; the routine caps the loss at the available mass and records it in respst_d. |
| 6. Compute settling from water to benthic sediment and move that mass into the benthic store. | Settling uses the aquatic settling coefficient and sorbed fraction; the routine limits the transfer to the remaining water mass, adds it to benthic mass, and records the settled amount. |
| 7. Compute resuspension from benthic sediment back to the water column and update both working stores. | Resuspension is based on the aquatic resuspension coefficient and active benthic depth; the routine caps the transfer by available benthic mass, adds it back to water, and stores the diagnostic output. |
| 8. Compute sediment-water diffusion and apply it with sign-aware limiting. | The routine evaluates diffusion from the concentration difference between benthic and water compartments, then moves mass in the correct direction while ensuring neither compartment goes negative; the signed result is saved as the diffusion diagnostic. |
| 9. Apply benthic decay and distribute benthic reaction loss to daughter pesticides. | The benthic store is decayed with decay_b when sufficient mass exists, the loss is recorded as react_bot, and daughter metabolite mass is added to the sequential pesticide’s benthic storage. |
| 10. Compute burial loss from the benthic active layer and subtract it from the benthic store. | Burial uses the pesticide burial velocity and active benthic depth; the routine caps the burial loss at available benthic mass and stores the result. |
| 11. Compute dissolved and sorbed pesticide outflow using the current reservoir discharge. | The routine calculates dissolved outflow from ht2%flo, fd1, and the remaining water mass, then computes sorbed outflow from the remaining water mass and fp1; each loss is limited to the available mass and written to respst_d. |
| 12. Store the end-of-day reservoir pesticide masses and the routed pesticide export. | Very small residual masses are zeroed, the final water and benthic stores are written back to res_water and res_benthic, the same values are copied to respst_d water/benthic outputs, and the routed export is placed in hcs2%pest. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `res_dat, res_sed` | `res_dat(idb)%sed, res_sed(jsed)%carbon, res_sed(jsed)%bd` |
| [sym:reservoir_module] | `res_ob, volatpst, setlpst, resuspst, difus, bury` | `res_ob(jres)%ob, res_ob(jres)%aq_mix(ipst)` |
| [sym:res_pesticide_module] | `respst_d` | `respst_d(jres)%pest(ipst)%tot_in, respst_d(jres)%pest(ipst)%react, respst_d(jres)%pest(ipseq)%metab, respst_d(jres)%pest(ipst)%volat, respst_d(jres)%pest(ipst)%settle, respst_d(jres)%pest(ipst)%resus, respst_d(jres)%pest(ipst)%difus, respst_d(jres)%pest(ipst)%react_bot, respst_d(jres)%pest(ipst)%bury, respst_d(jres)%pest(ipst)%sol_out, respst_d(jres)%pest(ipst)%sor_out, respst_d(jres)%pest(ipst)%water, respst_d(jres)%pest(ipst)%benthic` |
| [sym:hydrograph_module] | `res, ob, ht2` | `res(jres)%flo, ob(icmd)%props, res(jres)%sed, ht2%flo` |
| [sym:constituent_mass_module] | `cs_db, obcs, res_water, res_benthic, hcs2` | `cs_db%num_pests, cs_db%pest_num(ipst), obcs(icmd)%hin(1)%pest(ipst), res_water(jres)%pest(ipst), res_benthic(jres)%pest(ipst), cs_db%pest_num(ipseq), res_water(jres)%pest(ipseq), res_benthic(jres)%pest(ipseq), hcs2%pest(ipst)` |
| [sym:pesticide_data_module] | `pestdb, pestcp` | `pestdb(ipest_db)%koc, pestcp(ipest_db)%decay_a, pestcp(ipest_db)%num_metab, pestcp(ipest_db)%daughter(imeta)%num, pestdb(ipdb)%mol_wt, pestdb(ipest_db)%mol_wt, pestcp(ipest_db)%daughter(imeta)%soil_fr, pestdb(ipest_db)%aq_volat, pestdb(ipest_db)%aq_settle, pestdb(ipest_db)%aq_resus, pestdb(ipest_db)%ben_act_dep, pestcp(ipest_db)%decay_b, pestdb(ipest_db)%ben_bury` |
| [sym:water_body_module] | `res_wat_d` | `res_wat_d(jres)%area_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `respst_d(jres)%pest(ipst)%tot_in` | Within the reservoir loop, after loading the current inflow mass for each pesticide. | This records the incoming pesticide mass for the current reservoir and pesticide before any losses or transfers. It is used as the starting point for the process accounting and for downstream diagnostics of total input. |
| `respst_d(jres)%pest(ipst)%react` | When the water-column working mass after inflow is greater than 1.e-12, so water decay is applied. | This stores the mass lost to reaction in the water layer during the current update. It measures the decay removed from the water-column working mass before metabolites and transport processes are applied. |
| `respst_d(jres)%pest(ipseq)%metab` | Inside the water-column reaction block, once parent decay is distributed to daughter pesticides. | This accumulates metabolite mass for each sequential daughter pesticide derived from the current parent’s water-column decay. The accumulated value is then added to the daughter pesticide’s reservoir water storage. |
| `res_water(jres)%pest(ipseq)` | After daughter metabolite mass has been added and the water-column working mass is still being updated. | This updates the reservoir water storage for a daughter pesticide so the metabolite contribution from the parent pesticide is retained in the reservoir water constituent state. |
| `volatpst` | Before and during the volatilization calculation for the current pesticide. | This is the shared volatilization amount computed from pesticide properties, dissolved fraction, current water mass, and reservoir depth. It represents the water-layer loss attributed to air exchange. |
| `respst_d(jres)%pest(ipst)%volat` | Immediately after volatilization is computed and capped by the remaining water mass. | This records the volatilization loss for the current pesticide in the diagnostic output structure. It is the amount removed from the water store by volatilization during this step. |
| `setlpst` | After volatilization and before sediment resuspension, using the current water mass. | This is the settling flux from water to benthic sediment, based on the remaining sorbed water mass and aquatic settling coefficient. It becomes part of the benthic working mass. |
| `respst_d(jres)%pest(ipst)%settle` | Once settling has been computed and limited. | This records the settled mass for the pesticide in the diagnostic output structure. It reflects the water-to-benthic transfer caused by settling. |
| `resuspst` | After settling has updated the benthic working mass and before diffusion. | This is the resuspension flux from benthic sediment back into water. It represents the mass removed from the benthic working store and returned to the water column. |
| `respst_d(jres)%pest(ipst)%resus` | Immediately after resuspension is computed and capped by available benthic mass. | This records the resuspended mass in the diagnostic output structure. It is the amount transferred from benthic storage back into water during the current update. |
| `difus` | When sediment-water concentration difference is evaluated for the current pesticide. | This is the signed diffusion amount before sign-aware capping. Positive values indicate benthic-to-water movement; negative values indicate water-to-benthic movement. |
| `respst_d(jres)%pest(ipst)%difus` | After the sign-aware diffusion limits are applied. | This records the final signed diffusion exchange in the diagnostic output structure. It captures both magnitude and direction of sediment-water diffusion for the current pesticide. |
| `respst_d(jres)%pest(ipst)%react_bot` | When benthic pesticide mass is sufficient for the decay calculation. | This stores the mass lost to reaction in the benthic layer during the current update. It measures benthic decay before burial and the final output bookkeeping. |
| `res_benthic(jres)%pest(ipseq)` | Inside the benthic reaction block, after benthic decay is distributed to daughter pesticides. | This adds metabolite mass derived from benthic parent decay to the daughter pesticide’s benthic reservoir storage. |
| `bury` | After benthic decay and before final storage, using the remaining benthic mass. | This is the burial flux from the benthic active layer to deeper sediment. It removes mass from the active benthic store and is capped by the remaining benthic pesticide mass. |
| `respst_d(jres)%pest(ipst)%bury` | Immediately after burial is computed and limited. | This records the burial loss for the current pesticide in the diagnostic output structure. It reflects the amount removed from active benthic storage by burial. |
| `respst_d(jres)%pest(ipst)%sol_out` | After routing calculations for the remaining water-column mass. | This records the dissolved portion of pesticide exported with reservoir outflow. It is limited to the available water-column mass before the final water store is updated. |
| `respst_d(jres)%pest(ipst)%sor_out` | After the dissolved outflow is removed and the sorbed outflow is computed. | This records the sorbed portion of pesticide exported with reservoir outflow. It is limited to the remaining water-column mass after dissolved export. |
| `res_water(jres)%pest(ipst)` | At the end of the update, after all losses and transfers have been applied. | This stores the final end-of-day water-column pesticide mass for the reservoir. It is the remaining water-phase storage after all transformations and routing losses. |
| `res_benthic(jres)%pest(ipst)` | At the end of the update, after all benthic processes have been applied. | This stores the final end-of-day benthic pesticide mass for the reservoir. It is the remaining active-layer benthic storage after settling, resuspension, diffusion, reaction, burial, and routing effects. |
| `respst_d(jres)%pest(ipst)%water` | After final water and benthic storage values have been determined. | This records the final water-column pesticide storage for the day in the process-output structure, so the daily output can report the state remaining in the reservoir. |
| `respst_d(jres)%pest(ipst)%benthic` | After final water and benthic storage values have been determined. | This records the final benthic pesticide storage for the day in the process-output structure, so the daily output can report the state remaining in the reservoir sediment. |
| `hcs2%pest(ipst)` | After dissolved and sorbed outflow have been computed for the current pesticide. | This stores the total pesticide mass routed out of the reservoir in the current time step. It is the sum of dissolved and sorbed export and feeds downstream hydrograph routing. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:4.1.1 | Water column dissolved fraction F_d | $F_ d=\frac{1}{1+K_d*conc_{sed}}$ | fd1=1./(1.+kd*sedmass_watervol); sedmass_watervol=sed(t)/water_vol(m3)=conc_sed (kg/L). Exact match F_d=1/(1+K_d*conc_sed). |
| 8:4.1.2 | Water column sorbed fraction F_p | $F_p=\frac{K_d*conc_{sed}}{1+K_d*conc_{sed}}=1-F_d$ | fp1=1.-fd1. Exact match F_p=1-F_d. |
| 8:4.1.3 | Partition coefficient K_d from K_ow | $K_d=3.085*10^{-8}*K_{ow}$ | kd=pestdb%koc*res_sed%carbon/100 uses K_oc*f_oc (more accurate). Theory: K_d=3.085e-8*K_ow; equivalent for typical organic carbon fractions but more physically correct approach. |
| 8:4.1.4 | K_ow from solubility regression | $log(K_{ow})=5.00-0.670*log(pst'_{sol})$ | log(K_ow)=5.00-0.670*log(pst'_sol) is a database/setup regression, not in res_pest.f90. |
| 8:4.1.5 | Molar solubility pst'_sol | $pst'_{sol}=\frac{pst_{sol}}{MW}*10^3$ | pst'_sol=pst_sol/MW*10^3 is database/setup, not in res_pest.f90. |
| 8:4.1.6 | Pesticide degradation in water column | $pst_{deg,wtr}=k_{p,aq}*pst_{lkwtr}$ | pest_end=tpest1*pestcp%decay_a; decay_a=exp(-k_p_aq). Discrete first-order decay implementing pst_deg_wtr=k_p_aq*pst_lkwtr. |
| 8:4.1.7 | Aqueous degradation rate k_p_aq | $k_{p,aq}=\frac{0.693}{t_{1/2,aq}}$ | k_p_aq=0.693/t_1/2_aq precomputed as decay_a=exp(-0.693/t_half) during pesticide data loading. |
| 8:4.1.8 | Pesticide volatilization from water | $pst_{vol,wtr}=v_v*SA*\frac{F_d*pst_{lkwtr}}{V}$ | volatpst=pestdb%aq_volat*fd1*tpest1/depth; aq_volat=v_v (m/day), 1/depth=SA/V. Exact match pst_vol=v_v*SA*F_d*pst_lkwtr/V. |
| 8:4.1.9 | Overall volatilization velocity v_v | $v_v=K_l*\frac{H_e}{H_e+R*T_K*(K_l/K_g)}$ | v_v=K_l*H_e/(H_e+R*T_K*(K_l/K_g)) is a pesticide database property, not computed in res_pest.f90. |
| 8:4.1.10 | Gas/liquid-phase transfer coefficients K_g, K_l | $K_l=\frac{D_l}{z_l}$ | K_g=D_g/z_g and K_l=D_l/z_l are setup/database parameters. |
| 8:4.1.11 | Liquid-phase transfer from O2 analogy | $K_l=K_{l,O_2}*(\frac{32}{MW})^{0.25}$ | K_l=K_l_O2*(32/MW)^0.25 is a database/setup calculation. |
| 8:4.1.12 | Gas-phase transfer coefficient from wind | $K_g =168*\mu_w*(\frac{18}{MW})^{0.25}$ | K_g=168*mu_w*(18/MW)^0.25 is a database/setup calculation. |
| 8:4.1.13 | Pesticide settling from water to sediment | $pst_{stl,wtr}=v_s*SA*\frac{F_p*pst_{lkwtr}}{V}$ | setlpst=pestdb%aq_settle*fp1*tpest1/depth; aq_settle=v_s, 1/depth=SA/V. Exact match pst_stl=v_s*SA*F_p*pst_lkwtr/V. |
| 8:4.1.14 | Dissolved pesticide outflow | $pst_{sol,o}=Q*\frac{F_d*pst_{lkwtr}}{V}$ | solpesto=ht2%flo*fd1*tpest1/res%flo; exact match pst_sol_o=Q*F_d*pst_lkwtr/V. |
| 8:4.1.15 | Sorbed pesticide outflow | $pst_{sorb,o}=Q*\frac{F_p*pst_{lkwtr}}{V}$ | sorpesto=ht2%flo*fp1*tpest1/res%flo; exact match pst_sorb_o=Q*F_p*pst_lkwtr/V. |
| 8:4.2.1 | Benthic sediment concentration conc_sed* | $conc_{sed}^*=\frac{M_{sed}}{V_{tot}}$ | sedmass_watervol=bd/(1-bd/2.65) used as proxy for M_sed/V_tot via bulk density and particle density 2.65 t/m3. |
| 8:4.2.2 | Pore water fraction phi=V_wtr/V_tot | $\phi=\frac{V_{wtr}}{V_{tot}}$ | phi not explicitly computed; hard-coded as 0.8 in simplified fd2 formula at line 68. |
| 8:4.2.3 | Solids fraction 1-phi=V_sed/V_tot | $1-\phi=\frac{V_{sed}}{V_{tot}}$ | 1-phi=0.2 implied by phi=0.8 at line 68. |
| 8:4.2.4 | Bulk density rho_s | $\rho_s=\frac{M_{sed}}{V_{sed}}$ | res_sed(jsed)%bd is the bulk density (t/m3) used at line 63. |
| 8:4.2.5 | conc*_sed = (1-phi)*rho_s | $conc^*_{sed}= (1-\phi)*\rho_s$ | sedmass_watervol=bd/(1-bd/2.65) approximates (1-phi)*rho_s; then fd2 (line 64) is overwritten by simplified form at line 68. |
| 8:4.2.6 | Benthic dissolved fraction F_d,sed | $F_{d,sed}=\frac{1}{\phi+(1-\phi)*\rho_s*K_d}$ | FLAG: line 64 fd2=1./(1.+kd*sedmass_watervol) matches theory. But line 68 OVERWRITES with simplified fd2=1./(.8+.026*kd) using hard-coded phi=0.8, (1-phi)*rho_s=0.026. Theoretically correct line 64 value is discarded. |
| 8:4.2.7 | Benthic sorbed fraction F_p,sed | $F_{p,sed}=1-F_{d,sed}$ | fp2=1.-fd2. Exact match F_p,sed=1-F_d,sed. |
| 8:4.2.8 | Pesticide degradation in benthic sediment | $pst_{deg,sed}=k_{p,sed}* pst_{lksed}$ | pest_end=tpest2*pestcp%decay_b; decay_b=exp(-k_p_sed). Implements pst_deg_sed=k_p_sed*pst_lksed. |
| 8:4.2.9 | Sediment degradation rate k_p_sed | $k_{p,sed}=\frac{0.693}{t_{1/2,sed}}$ | k_p_sed=0.693/t_1/2_sed precomputed as decay_b=exp(-0.693/t_half_sed) during pesticide data loading. |
| 8:4.2.10 | Pesticide resuspension from sediment | $pst_{rsp,wtr}=v_r*SA*\frac{pst_{lksed}}{V_{tot}}$ | resuspst=pestdb%aq_resus*tpest2/pestdb%ben_act_dep; aq_resus=v_r, 1/ben_act_dep=SA/V_tot. Exact match pst_rsp=v_r*SA*pst_lksed/V_tot. |
| 8:4.2.11 | Benthic active-zone volume V_tot=SA*D_sed | $V_{tot}=SA*D_{sed}$ | ben_act_dep=D_sed parameter; SA/V_tot=1/D_sed used implicitly in lines 112, 124-125, 163. |
| 8:4.2.12 | Pesticide diffusion between sediment and water | $pst_{dif}=\|v_d*SA*( \frac{F_{d ,sed} *pst_{lksed}}{V_{tot}}- \frac{F_d*pst_{lkwtr}}{V} )\|$ | difus=aq_mix(ipst)*(fd2*tpest2/ben_act_dep-fd1*tpest1/depth); aq_mix=v_d. Absolute value enforced at lines 126-142. Exact match \|v_d*SA*(F_d,sed*pst_lksed/V_tot-F_d*pst_lkwtr/V)\|. |
| 8:4.2.13 | Diffusion coefficient v_d | $v_d=\frac{69.35}{365}*\phi*MW^{-2/3}$ | v_d=69.35/365*phi*MW^(-2/3) is a database/setup calculation; stored as aq_mix per pesticide. |
| 8:4.2.14 | Pesticide burial from benthic zone | $pst_{bur}=v_b*SA*\frac{pst_{lksed}}{V_{tot}}$ | bury=pestdb%ben_bury*tpest2/pestdb%ben_act_dep; ben_bury=v_b. Exact match pst_bur=v_b*SA*pst_lksed/V_tot. |
| 8:4.3.2 | Benthic pesticide mass balance | $\Delta pst_{lksed}=pst_{deg,sed}+pst_{stl,wtr}-pst_{rsp,wtr }-pst_{bur}\pm pst_{dif}$ | Delta_pst_lksed=pst_deg_sed+pst_stl_wtr-pst_rsp_wtr-pst_bur+/-pst_dif distributed: +setlpst(107), -resuspst(119), +/-difus(131-141), *decay_b(148), -bury(168). |
| 7:4.2.4 | Sediment particle density relationship | $\rho_s=\frac{M_{sed}}{V_{sed}}$ | Verified against SWAT+ 62.0.0 (res_pest.f90:56). ρ_s hardcoded 2.65 (sed volume = sed/2.65) |

## Lineage

Resolved lineage shows four historical changes to res_pest. The original df07e3f addition introduced the full reservoir pesticide balance. 39fabde initialized the working scalars and loop counters to zero, and 889136d corrected the ipdb comment typo. 1c812c1 removed the bedvol intermediate by assigning tpest2 directly from res_benthic(jres)%pest(ipst) and added end-of-day storage writes for respst_d(jres)%pest(ipst)%water and %benthic. 2ee1889 later deleted the unused bedvol declaration after that refactor.

- df07e3f established the reservoir pesticide balance algorithm and all tracked outputs.
- 39fabde changed the local declarations to explicit zero initialization, making the working state safe by default.
- 1c812c1 changed benthic mass handling by removing the bedvol scaling step, and it added persisted end-of-day water and benthic output fields.
- 2ee1889 completed the refactor by removing the now-unused bedvol local.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_pest' has no extracted documentation comment.
- algorithm_steps revised: merged the source into 12 model-level steps to cover the full routine while preserving real source line citations.
- The source contains a benthic diffusion fraction overwrite at lines 68-70 after a more theory-based calculation at lines 64-66; documentation should note that the hard-coded approximation is the effective value used.
