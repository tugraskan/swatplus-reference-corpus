---
kind: procedure
symbol: aqu_1d_control
title: aqu_1d_control
status: filled
source_hash: 2e934ed4c9216fd3
version_label: SWAT+ 62.0.0
locals:
  iaq: Index of the active aquifer record for the current command object, taken from `ob(icmd)%num`
    and used to access aquifer storage, parameters, and database values.
  iaqdb: Index/pointer to the aquifer database record for the active object, taken from `ob(icmd)%props`;
    it identifies the property set behind the current aquifer.
  icha: Loop index over the linked channel elements in the geomorphic baseflow routing setup.
  iob_out: Copies the current command-object index so the routine can walk the object’s outgoing
    routing fractions when tallying destination flows.
  iout: Loop counter over the outgoing route slots in `ob(iob_out)%src_tot`.
  ii: Loop counter used when filling subdaily time-step hydrographs near the end of the routine.
  icontrib: Holds the first contributing channel index found in the aquifer-channel linkage
    loop, or stays zero if no channel qualifies.
  ipest: Loop index over simulated pesticides in the aquifer.
  ipest_db: Database pesticide number mapped from `cs_db%pest_num(ipest)`; used to read reaction
    and sorption parameters from `pestcp` and `pestdb`.
  ipseq: Sequential pesticide number for a daughter/metabolite species during pesticide decay
    processing.
  ipdb: Database index for the daughter pesticide associated with `ipseq`.
  imeta: Loop counter over the metabolite daughter list for a parent pesticide.
  mol_wt_rto: Molecular-weight ratio used to convert parent pesticide decay mass into daughter
    pesticide mass.
  stor_init: Snapshot of aquifer water storage at routine entry, saved before any recharge,
    flow, seepage, or revap updates.
  conc_no3: Working nitrate concentration in aquifer water, computed from nitrate storage
    divided by water storage.
  step: Copy of the time-step count, used when splitting hydrograph output into subdaily pieces.
  contrib_len: Computed contributing length used to decide where aquifer baseflow begins to
    enter the channel network.
  contrib_len_left: Remaining contributing length at the first active channel segment, used
    to assign per-channel flow fractions.
  pest_init: Pesticide mass present in the aquifer at the start of the day, saved for the
    pesticide output summary.
  no3_init: Nitrate mass present in the aquifer before applying the daily nitrate loss factor.
  flow_mm: Total aquifer flow volume expressed in mm, combining lateral groundwater flow and
    seepage for pesticide transport calculations.
  pest_kg: Working pesticide mass moved with aquifer flow during the transport calculation.
  conc: Working pesticide concentration in the aquifer flow, limited by pesticide solubility.
  zdb1: Transport attenuation factor used in the exponential pesticide flow-distribution formula.
  kd: Sorption partition factor derived from pesticide Koc and aquifer organic carbon.
  gw_volume: Groundwater volume in cubic meters, used to convert stored salt/constituent mass
    to concentrations.
  salt_recharge: Salt mass added from incoming recharge water for one salt species.
  gw_discharge: Groundwater discharge volume in cubic meters sent to channels for one salt/constituent
    calculation.
  salt_discharge: Salt mass exported with groundwater discharge to channels.
  gw_seep: Groundwater seepage volume in cubic meters used for seepage export calculations.
  salt_seep: Salt mass exported with seepage out of the aquifer.
  cs_recharge: Generic constituent mass added from incoming recharge water for one non-salt
    constituent.
  cs_discharge: Generic constituent mass exported with groundwater discharge to channels.
  cs_seep: Generic constituent mass exported with seepage out of the aquifer.
  m: Loop counter over salt ions.
  ics: Loop counter over other simulated constituents.
uses:
  aquifer_module: '`aquifer_module` provides the aquifer database, parameters, and dynamic
    state that this controller updates. The routine reads and writes water storage, water-table
    depth, recharge, flow, seepage, revap, nitrate, and mineral phosphorus values there, so
    the module is the core state reservoir for all aquifer calculations.'
  time_module: '`time_module` matters because the routine assigns `iwst = ob(icmd)%wst` and
    then uses `wst(iwst)%weat%pet` to compute aquifer revap. The weather-station index ties
    the aquifer object to the correct daily climate forcing.'
  hydrograph_module: '`hydrograph_module` matters because it holds the routing object `ob`
    and the aquifer-channel linkage `aq_ch`. The routine uses `ob(icmd)%num`, `ob(icmd)%props`,
    `ob(icmd)%wst`, `ob(icmd)%hin`, `ob(icmd)%hd`, and `aq_ch(iaq)` to route water and constituent
    loads to downstream objects and to build subdaily channel fractions when geomorphic baseflow
    routing is active.'
  climate_module: '`climate_module` matters because the aquifer revap calculation uses daily
    potential evapotranspiration from `wst(iwst)%weat%pet`. Without the climate state, the
    controller cannot compute evaporative loss from the aquifer.'
  maximum_data_module: '`maximum_data_module` matters because `db_mx%aqu2d` controls whether
    the routine also prepares 2-D aquifer/channel distribution outputs. When it is positive,
    the routine saves hydrographs for later distribution through `aq_ch` and constituent-loading
    arrays.'
  constituent_mass_module: '`constituent_mass_module` matters because it supplies the aquifer
    salt, constituent, and pesticide storage arrays plus the hydrograph containers used to
    move those masses through the model. The routine updates `cs_aqu`, `obcs`, and `aq_chcs`
    so recharge, discharge, seepage, and pesticide transport are preserved in the shared constituent
    state.'
  pesticide_data_module: '`pesticide_data_module` matters because the controller needs pesticide-specific
    decay and metabolite mapping to update aquifer pesticide masses. It reads the parent decay
    factor and daughter relationships from `pestcp` before splitting parent decay into metabolite
    storage.'
  aqu_pesticide_module: '`aqu_pesticide_module` matters because it stores the daily aquifer
    pesticide process diagnostics. The routine writes reaction, metabolite, storage, and flow
    terms into `aqupst_d` so pesticide mass balance can be reported after the aquifer update.'
  salt_module: 'Imported but not used: none of the module''s 18 module-level variables is
    referenced anywhere in this routine''s body. Salt state reaches the aquifer through the
    routines this controller calls rather than through direct access here.'
  salt_aquifer: '`salt_aquifer` matters because it provides the per-aquifer salt balance output
    structure that records recharge, seepage, mass, concentration, and stream loading for
    each salt ion. The controller fills `asaltb_d` as it moves salt mass through the aquifer.'
  cs_aquifer: '`cs_aquifer` matters because it provides the analogous balance structure for
    generic constituents. The routine stores recharge, groundwater discharge, seepage, mass,
    and concentration into `acsb_d` for each simulated constituent.'
  ch_pesticide_module: 'Imported but not used: none of the module''s 20 module-level variables
    is referenced anywhere in this routine''s body. Channel-side pesticide state is handled
    by the called routines, not by this controller directly.'
---

<!-- facts:header -->

Routes one-day aquifer water, nitrate, salt, constituent, and pesticide balances for a 1-D aquifer object. It updates shared aquifer state and exports flow and chemistry hydrographs to connected objects.

## Bottom Line

`aqu_1d_control` is the daily controller for the old 1-D aquifer path. It pulls the current aquifer and weather pointers from the routing object, adds recharge to storage, computes return flow, seepage, revap, nitrate movement, salt and constituent balances, and pesticide decay/transport, then writes the resulting hydrographs back to the shared object state.

The routine matters because it is the place where aquifer storage is turned into routed flow and constituent loads. Later model behavior depends on the updated aquifer storage, the hydrograph outputs in `ob(icmd)%hd(1:2)`, the constituent outputs in `obcs(icmd)%hd(1:2)`, and the saved per-aquifer diagnostics in `aqu_d`, `asaltb_d`, `acsb_d`, and `aqupst_d`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when `command` reaches an aquifer object and `ob(icmd)%dfn_tot == 0`, meaning the old 1-D aquifer control path is selected instead of the 2-D groundwater flow routine. `command` has already set `icmd` to the current object and the object connectivity state (`ob`, `obcs`, weather station link, and aquifer pointers) is in place. The results feed later routing and output behavior through `ob(icmd)%hd(1:2)`, `obcs(icmd)%hd(1:2)`, `aq_ch(iaq)%hd`, and the aquifer state arrays used by subsequent daily and summary reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Bind the current aquifer, database, and weather station to the routing object | The routine copies the active aquifer index and weather-station index from `ob(icmd)` into local variables, then snapshots the current aquifer storage before any update. This sets up all later reads and writes against the correct aquifer record. |
| 2. Initialize daily hydrograph outputs and constituent hydrographs | It clears the two aquifer hydrograph outputs to zero hydrographs and, if any constituents are simulated, also clears the constituent hydrograph outputs. This ensures the day starts with empty flow/load records. |
| 3. Convert incoming object runoff to aquifer recharge | Recharge is computed from incoming object inflow by converting `ob(icmd)%hin%flo` from cubic meters to mm over the object area. That recharge becomes the day’s aquifer input. |
| 4. Optionally run salt and constituent chemistry updates | If salts are enabled, the routine calls `salt_chem_aqu`; if other constituents are enabled, it calls `cs_rctn_aqu` and `cs_sorb_aqu`. These calls update groundwater chemistry before transport and balance calculations use the masses. |
| 5. Store current recharge as the previous recharge and add recharge to storage | The routine keeps recharge lagging state in `aqu_prm(iaq)%rchrg_prev` and adds the current recharge to aquifer storage. This makes the new water available for the rest of the day’s balance. |
| 6. Recompute water-table depth from storage and specific yield | Using bottom depth and specific yield, the routine derives `dep_wt` from the updated storage and clamps it to zero or greater. That depth controls whether baseflow and revap are allowed. |
| 7. Compute groundwater return flow when the water table is shallow enough | If `dep_wt` is at or above the flow threshold, the routine updates groundwater flow with an exponential recession blend, caps it at storage, subtracts it from storage, and otherwise sets flow to zero. This is the daily lateral baseflow from the aquifer. |
| 8. Convert groundwater flow to object hydrograph output | The return-flow depth is converted back to cubic meters and stored in `ob(icmd)%hd(1)%flo`. This is the aquifer’s routed baseflow output to the connected downstream object. |
| 9. Compute seepage out of the aquifer and export it | The routine computes deep seepage as a fraction of recharge, limits it by remaining storage, stores it in `aqu_d(iaq)%seep`, converts it to `ob(icmd)%hd(2)%flo`, and subtracts it from storage. This is the aquifer’s second routed water export. |
| 10. Compute revap loss from the aquifer when the water table is shallow | If the water table is shallower than the revap threshold, the routine estimates evaporative uptake from PET times `revap_co`, caps it by storage, and subtracts it from storage; otherwise revap is zero. This removes plant-water uptake from the aquifer balance. |
| 11. Update nitrate recharge, storage, loss, and export | The routine adds nitrate recharge from incoming flow, computes nitrate concentration from current storage, exports nitrate with groundwater return flow and seepage, applies the nitrate loss factor, and stores the results in both aquifer and hydrograph state. This keeps the aquifer nitrogen balance synchronized with the water balance. |
| 12. Update salt recharge, discharge, seepage, and output masses | For each salt ion, the routine adds recharge mass, computes groundwater concentration, subtracts discharge to channels, subtracts seepage, and stores the resulting mass and concentration diagnostics. If 2-D aquifer routing is enabled, it also preserves the channel load for next-day distribution. |
| 13. Update generic constituent recharge, discharge, seepage, and output masses | For each simulated constituent, the routine repeats the same mass-balance pattern used for salts: recharge, concentration, discharge, seepage, and diagnostic storage. The results are written to the constituent hydrograph and aquifer-balance arrays. |
| 14. Route mineral phosphorus, geomorphic baseflow fractions, pesticide transport, outflow bookkeeping, and subdaily hydrographs | The routine computes aquifer mineral P output, optionally distributes baseflow across linked channels when 2-D routing is active, updates pesticide reaction and flow partitions for each pesticide, totals incoming/outgoing hydrographs, and fills subdaily time-step outputs. These final steps prepare the aquifer’s routed results for later model components and reporting. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:aquifer_module] | `aqu_d, aqu_prm, aqu_dat` | `aqu_d(iaq)%stor, aqu_d(iaq)%rchrg, aqu_prm(iaq)%rchrg_prev, aqu_d(iaq)%dep_wt, aqu_dat(iaq)%dep_bot, aqu_dat(iaq)%spyld, aqu_dat(iaq)%flo_min, aqu_d(iaq)%flo, aqu_prm(iaq)%alpha_e, aqu_d(iaq)%seep, aqu_dat(iaq)%seep, aqu_dat(iaq)%revap_min, aqu_d(iaq)%revap, aqu_dat(iaq)%revap_co, aqu_d(iaq)%no3_rchg, aqu_d(iaq)%no3_st, aqu_prm(iaq)%rchrgn_prev, aqu_d(iaq)%no3_lat, aqu_prm(iaq)%nloss, aqu_d(iaq)%no3_loss, aqu_d(iaq)%no3_seep, aqu_d(iaq)%minp, aqu_dat(iaq)%minp, aqu_dat(iaq)%bf_max` |
| [sym:time_module] | `iwst` | `iwst` |
| [sym:hydrograph_module] | `ob, aq_ch` | `ob(icmd)%num, ob(icmd)%props, ob(icmd)%wst, ob(icmd)%hd(1), ob(icmd)%hd(2), ob(icmd)%hin%flo, ob(icmd)%area_ha, ob(icmd)%hd(1)%flo, ob(icmd)%hd(2)%flo, ob(icmd)%hin%no3, ob(icmd)%hd(1)%no3, ob(icmd)%hd(2)%no3, ob(icmd)%hd(1)%solp, aq_ch(iaq)%len_tot, aq_ch(iaq)%num_tot, aq_ch(iaq)%ch(icha)%len_left, aq_ch(iaq)%ch(icha)%len, aq_ch(iaq)%ch(icha)%flo_fr, aq_ch(iaq)%hd` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%pet` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%aqu2d` |
| [sym:constituent_mass_module] | `cs_db, obcs, cs_aqu, aq_chcs` | `cs_db%num_tot, obcs(icmd)%hd(1), obcs(icmd)%hd(2), cs_db%num_salts, cs_db%num_cs, obcs(icmd)%hin(1)%salt(m), cs_aqu(iaq)%salt(m), cs_aqu(iaq)%saltc(m), obcs(icmd)%hd(1)%salt(m), aq_chcs(iaq)%hd(1)%salt(m), obcs(icmd)%hd(2)%salt(m), obcs(icmd)%hin(1)%cs(ics), cs_aqu(iaq)%cs(ics), cs_aqu(iaq)%csc(ics), obcs(icmd)%hd(1)%cs(ics), aq_chcs(iaq)%hd(1)%cs(ics), obcs(icmd)%hd(2)%cs(ics), cs_db%num_pests, cs_db%pest_num(ipest), cs_aqu(iaq)%pest(ipest), obcs(icmd)%hin(1)%pest(ipest)` |
| [sym:pesticide_data_module] | `pestcp` | `pestcp(ipest_db)%decay_s, pestcp(ipest_db)%num_metab, pestcp(ipest_db)%daughter(imeta)%num` |
| [sym:aqu_pesticide_module] | `aqupst_d` | `aqupst_d(iaq)%pest(ipest)%react` |
| [sym:salt_module] | `no direct reference in this procedure` |  |
| [sym:salt_aquifer] | `asaltb_d` | `asaltb_d(iaq)%salt(m)%rchrg, asaltb_d(iaq)%salt(m)%saltgw, asaltb_d(iaq)%salt(m)%seep, asaltb_d(iaq)%salt(m)%mass, asaltb_d(iaq)%salt(m)%conc` |
| [sym:cs_aquifer] | `acsb_d` | `acsb_d(iaq)%cs(ics)%rchrg, acsb_d(iaq)%cs(ics)%csgw, acsb_d(iaq)%cs(ics)%seep, acsb_d(iaq)%cs(ics)%mass, acsb_d(iaq)%cs(ics)%conc` |
| [sym:ch_pesticide_module] | `no direct reference in this procedure` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | When the routine starts for the current object | `iwst` is set to the weather-station index linked to the active object so the aquifer can read daily PET from the correct station. |
| `ob(icmd)%hd(1)` | Always at routine entry | The return-flow hydrograph is reset to zero before the day’s aquifer flow is computed, so the output contains only this call’s flow contribution. |
| `ob(icmd)%hd(2)` | Always at routine entry | The seepage hydrograph is reset to zero before the day’s aquifer seepage is computed. |
| `obcs(icmd)%hd(1)` | Only when `cs_db%num_tot > 0` | The first constituent hydrograph is cleared so any simulated constituent loads written later in the routine start from zero. |
| `obcs(icmd)%hd(2)` | Only when `cs_db%num_tot > 0` | The second constituent hydrograph is cleared so seepage loads can be recorded cleanly for the current day. |
| `aqu_d(iaq)%rchrg` | After recharge is computed from `ob(icmd)%hin%flo` | Recharge is stored in mm as the current day’s aquifer inflow and then used by storage, flow, seepage, and chemistry calculations. |
| `aqu_prm(iaq)%rchrg_prev` | After recharge is computed | The previous-recharge tracker is refreshed with the current recharge so lagged recharge behavior can be reproduced or inspected later. |
| `aqu_d(iaq)%stor` | After recharge is added and before flow/seepage/revap are removed | Storage increases by the recharge amount and is then reduced by flow, seepage, and revap; it is the central water-balance state for the aquifer. |
| `aqu_d(iaq)%dep_wt` | After storage is updated | Water-table depth is recomputed from storage and specific yield so the threshold checks for flow and revap use the new aquifer state. |
| `aqu_d(iaq)%flo` | When `dep_wt <= aqu_dat(iaq)%flo_min` | Groundwater return flow is computed from the recession blend, limited by available storage, and stored as the aquifer’s baseflow to channels. |
| `ob(icmd)%hd(1)%flo` | When `dep_wt <= aqu_dat(iaq)%flo_min` | The routed return-flow hydrograph is written in cubic meters for the downstream object once groundwater flow has been computed. |
| `aqu_d(iaq)%seep` | After recharge is known | Seepage is computed as the deep-aquifer fraction of recharge, capped by storage, and then removed from aquifer storage. |
| `ob(icmd)%hd(2)%flo` | After seepage is computed | The seepage hydrograph is written in cubic meters so the deep-aquifer seepage can be routed or reported downstream. |
| `aqu_d(iaq)%revap` | When `dep_wt < aqu_dat(iaq)%revap_min` | Revap is set from PET times `revap_co` and limited by storage; otherwise it is set to zero. |
| `aqu_d(iaq)%no3_rchg` | After constituent recharge is read from incoming hydrograph | Nitrate recharge is accumulated in the aquifer as the input nitrate mass per hectare for the day. |
| `aqu_d(iaq)%no3_st` | After nitrate recharge is added | Nitrate storage is increased by recharge and then reduced by lateral loss, seepage, and the daily decay factor. |
| `aqu_prm(iaq)%rchrgn_prev` | After nitrate recharge is added | The previous nitrate recharge tracker is updated with the current nitrate recharge so the last-day nitrate input is retained in the parameter state. |
| `ob(icmd)%hd(1)%no3` | When nitrate export to return flow is computed | The nitrate load in groundwater return flow is written to the routed hydrograph so downstream objects receive the aquifer NO3 load. |
| `aqu_d(iaq)%no3_lat` | After nitrate return flow is computed | This stores the per-hectare nitrate load exported with lateral groundwater flow. |
| `aqu_d(iaq)%no3_loss` | After nitrate decay is applied | This records how much nitrate mass was removed by the daily nitrate loss factor. |
| `aqu_d(iaq)%no3_seep` | After nitrate seepage is computed | This stores the per-hectare nitrate load leaving the aquifer with seepage. |
| `ob(icmd)%hd(2)%no3` | When nitrate seepage is computed | The nitrate load in seepage is written to the second hydrograph output for downstream routing or reporting. |
| `cs_aqu(iaq)%salt(m)` | During the salt loop, for each salt species after recharge is applied | Salt mass in the aquifer is increased by recharge, then decreased by discharge and seepage, leaving the updated stored mass for that salt ion. |
| `asaltb_d(iaq)%salt(m)%rchrg` | During the salt loop, for each salt species after recharge mass is read | This records the daily salt recharge mass for output and salt-balance reporting. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:4.2.1 | Shallow aquifer water balance | $aq_{sh,i}=aq_{sh,i-1}+w_{rchrg,sh}-Q_{gw}-w_{revap}-w_{seep}-w_{pump,sh}$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:92). storage balance: +rchrg (:92), −flo (:103), −seep (:113), −revap (:122) |
| 2:4.2.3 | Recharge equals deep percolation plus crack-flow seepage | $w_{seep}=w_{perc,ly=n}+w_{crk,btm}$ | Recharge enters the aquifer from ob(icmd)%hin%flo, which is the accumulated soil-profile outflow reaching the aquifer controller. |
| 2:4.2.4 | Recharge partitioned to deep aquifer | $w_{deep}=\beta_{deep}*w_{rchrg}$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:112). seep = rchrg * seep_frac` — β_deep·w_rchrg |
| 2:4.2.5 | Recharge remaining in shallow aquifer | $w_{rchrg,sh}=.w_{rchrg}-w_{deep}$ | Recharge is first added in full to shallow storage, then the deep-aquifer seepage fraction is subtracted, leaving the shallow-aquifer share. |
| 2:4.2.6 | Groundwater/baseflow relation | $Q_{gw}=\frac{8000*K_{sat}}{L_{gw}^2}*h_{wtbl}$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:100). recession store, not `8000·K_sat/L²·h` Hooghoudt discharge |
| 2:4.2.7 | Groundwater-height ODE concept | $\frac{dh_{wtbl}}{dt}=\frac{w_{rchrg,sh}-Q_{gw}}{800*\mu}$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:95). tracks storage→dep_wt, not `dh/dt=(rchrg−Q_gw)/800μ |
| 2:4.2.8 | Baseflow recession ODE | $\frac{dQ_{gw}}{dt}=10*\frac{K_{sat}}{\mu *L^2_{gw}}*(w_{rchrg,sh}-Q_{gw})=\alpha_{gw}*(w_{rchrg,sh}-Q_{gw})$ | flo = flo*alpha_e + rchrg*(1-alpha_e) is the discrete exponential-recession update used in place of the continuous ODE form. |
| 2:4.2.9 | Groundwater flow threshold branch | $aq_{sh}>aq_{shthr,q}$ | Baseflow is computed only when water-table depth is shallower than the flow threshold flo_min. |
| 2:4.2.10 | Zero groundwater flow below threshold | $Q_{gw,i}=0$ | Flow is set to zero when dep_wt exceeds flo_min. |
| 2:4.2.11 | Exponential groundwater recession | $Q_{gw}=Q_{gw,0}*exp\lfloor-\alpha_{gw}*t\rfloor$ | The recession equation is updated daily with concurrent recharge forcing; it is not a pure free-recession Q0*exp(-alpha*t) trajectory unless recharge is zero. |
| 2:4.2.12 | Zero groundwater flow below threshold (recession view) | $Q_{gw,i}=0$ | The recession update is bypassed entirely when the water table is deeper than flo_min. |
| 2:4.2.15 | Maximum revap from PET | $w_{revap,mx}=\beta_{rev} *E_o$ | revap = PET*revap_co when the water table is within the revap depth threshold. |
| 2:4.2.16 | Zero revap below threshold | $w_{revap}=0$ | revap is set to zero when dep_wt >= revap_min. |
| 2:4.2.17 | Partial revap branch | $w_{revap}=w_{revap,mx} - aq_{shthr,rvp}$ | The theory page's intermediate-storage revap branch is not present; code uses only a threshold check plus storage cap. |
| 2:4.2.18 | Full revap branch | $w_{revap}=w_{revap,mx}$ | When the threshold is met, revap is PET*revap_co capped by available storage, not by a separate aqshthr+revapmx branch expression. |
| 2:4.2.19 | Groundwater height relation | $Q_{gw}=\frac{8000*K_{sat}}{L^2_{gw}}*h_{wtbl}=\frac{8000*\mu}{10}*\frac{10*K_{sat}}{\mu * L^2_{gw}}*h_{wtbl}=800*\mu*\alpha_{gw}*h_{wtbl}$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:100). code uses recession-store baseflow `flo*alpha_e+rchrg*(1-alpha_e)`, NOT the 800·μ·α·h water-table form |
| 2:4.2.20 | Discrete groundwater-height update | $h_{wtbl,i}=h_{wtbl,i-1}*exp[-\alpha_{gw}*\Delta t]+\frac{w_{rchrg}*(1-exp\lfloor-\alpha_{gw} *\Delta t\rfloor)}{800*\mu*\alpha_{gw}}$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:100). storage recession `flo*alpha_e+rchrg*(1-alpha_e)`, not the water-table-height analytical form |
| 2:4.3.1 | Deep aquifer storage balance | $aq_{dp,i}=aq_{dp,i-1}+w_{deep}-Q_{gw}-w_{pump,dp}$ | Classic aquifer routing exports deep recharge as aqu_d%seep to the second hydrograph outlet, but deep-aquifer storage itself is handled outside this routine and is not represented as a local aqdp state variable here. |
| 3:1.9.2 | NO3 remaining in shallow aquifer storage | $NO3_{sh,i}=(NO3_{sh,i-1}+NO3_{rchrg,i})*aq_{sh,i}/(aq_{sh,i}+Q_{gw}+w_{revap}+w_{rchrg,dp})$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:135). code uses conc×flow (`conc_no3 = no3_st/stor`), NOT theory's mass-partition fraction |
| 3:1.9.3 | NO3 in groundwater return flow | $NO3_{gw}=(NO3_{sh,i-1}+NO3_{rchrg,i})*Q_{gw}/(aq_{sh,i}+Q_{gw}+w_{revap}+w_{rchrg,dp})$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:140). hd(1)%no3 = conc_no3*flo*area` — same conc-based approach |
| 3:1.9.4 | NO3 lost via revap (deep root uptake) | $NO3_{revap}=(NO3_{sh,i-1}+NO3_{rchrg,i})*w_{revap}/(aq_{sh,i}+Q_{gw}+w_{revap}+w_{rchrg,dp})$ | Comment at line 145: 'revapno3=conc*revap -- dont include nitrate uptake by plant'; intentionally omitted. |
| 3:1.9.5 | NO3 in deep seepage out of aquifer | $NO3_{dp}=(NO3_{sh,i-1}+NO3_{rchrg,i})*w_{rchrg,dp}/(aq_{sh,i}+Q_{gw}+w_{revap}+w_{rchrg,dp})$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90:154). no3_seep = conc_no3*seep` — conc-based, not partition |
| 3:1.9.6 | Exponential decay of NO3 in shallow aquifer | $NO3_{sh,t}=NO3_{sh,o}*exp\lfloor-k_{NO3,sh}*t\rfloor$ | Verified against SWAT+ 62.0.0 (aqu_1d_control.f90). (aquifer NO3 exp decay) |

## Lineage

`aqu_1d_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `aqu_1d_control.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `d81f796` (2025-04-18) — various comment fixes
- `4d173cc` (2025-04-17) — merge
- `889136d` (2025-02-03) — Fix typos
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aqu_1d_control' has no extracted documentation comment.
- algorithm_steps revised: merged the draft into 14 source-backed steps aligned to the visible control flow and line ranges.
- Source evidence did not resolve any `time_module`-specific component beyond the imported `iwst` state used through `wst(iwst)%weat%pet`.
- Source evidence did not resolve any `salt_module` or `ch_pesticide_module` component names beyond the module imports, so those outside-state fields remain uncertain.
- salt_module and ch_pesticide_module are use-imported but no specific imported state was resolved to the body; they appear to be vestigial imports (salt/pesticide state is drawn from salt_aquifer and constituent modules).
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Modules imported without contributing state were verified rather than left unresolved: each module's own source was checked from its context packet, counting only module-level variables, and none of the modules marked "no direct reference in this procedure" is referenced in this routine's body.
