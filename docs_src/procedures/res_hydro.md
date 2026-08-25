---
kind: procedure
symbol: res_hydro
title: res_hydro
status: filled
source_hash: d3fbff1f41c69088
version_label: SWAT+ 62.0.0
args:
  jres: Reservoir object index used to read and update the corresponding `res_ob(jres)` operation
    state, including inflow/demand memory and operating parameters for the `nonirr-h06`, `irr-h06`,
    and `hydrop` options.
  id: Object index used with the decision-table set `dtbl_res(id)` to select which reservoir/wetland
    rule set and action settings are evaluated for this call.
  pvol_m3: Principal or normal-season target volume passed in by the caller; several actions
    use it as the target storage reference, such as `rate_pct`, `days`, `natlake`, `nonirr-h06`,
    `irr-h06`, and `hydrop`.
  evol_m3: Emergency or flood-season target volume passed in by the caller; actions such as
    `ab_emer`, `days`, `natlake`, `nonirr-h06`, and `irr-h06` compare against or derive releases
    from this threshold.
locals:
  iweir: Index of the weir outflow parameter entry in `res_weir`; used by the weir-based release
    branch to pick the coefficients for the current structure.
  nstep: Number of subdaily steps in the current day; controls how the daily release is divided
    across loop iterations.
  tstep: Loop counter over the `nstep` subdaily iterations.
  iac: Loop counter over actions in the selected decision table.
  ic: Condition index used when the code evaluates decision-table condition metadata.
  ial: Loop counter over decision-table alternatives when checking whether an action is hit.
  irel: Index of the reservoir recall database / hydrograph input used by measured-release
    options.
  iob: Index of the irrigation or water-right object used by the irrigation transfer branches.
  vol: Working copy of the current water volume in the body at the start of the routine and
    during release calculations.
  vol_above: Working storage above a threshold; reserved for stepwise release computations
    and geometry-based overflow logic.
  b_lo: Lower target or baseline volume used by the `days` and similar target-release branches.
  action: Flag that marks whether the current action's conditions are met (`y`) or not (`n`).
  res_h: Computed water depth used by the weir-release branch to convert volume to head.
  demand: Working demand volume used by irrigation-related calculations.
  wsa1: Water-surface area of the current water body, derived from `wbody_wb%area_ha` and
    used to convert volume to depth.
  qout: Working discharge volume for weir calculations during a short time step.
  hgt: Height of the weir bottom above the impoundment bottom; part of the weir geometry calculations.
  hgt_above: Height of water above the top of the weir; used to compute overflow discharge.
  sto_max: Maximum storage volume at bank top, used as a geometric limit in reservoir calculations.
  sto: Current effective storage used by the Doell natural-lake release formula.
  smax: Maximum lake storage used as the upper reference storage in natural-lake and Hanazaki-style
    formulas.
  so: Dead-storage threshold used by the natural-lake formula.
  kr: Release coefficient used by the natural-lake formula.
  alpha: Exponent or shape parameter used by the Doell, Hanazaki, and HYPE-style formulas.
  er: Release-rate scaling factor computed from starting storage and used in the Hanazaki-style
    rules.
  i_mon: Monthly inflow sample from the rolling memory window used in the Hanazaki and related
    formulas.
  d_mon: Monthly demand sample from the rolling memory window used in the irrigation-reservoir
    Hanazaki formula.
  beta: Demand-to-inflow threshold coefficient used to choose the target-release expression
    in the irrigation Hanazaki branch.
  target_rel: Computed release target for the current action branch before it is converted
    to a discharge volume.
  pi: Mathematical constant used in the HYPE seasonal demand factor calculation.
  a_amp: Amplitude parameter for the HYPE sinusoidal demand factor.
  b_phase: Phase-shift parameter for the HYPE sinusoidal demand factor.
  s_min_hype: Lower storage limit below which the HYPE release factor is suppressed.
  s_lim_hype: Upper storage threshold that defines when HYPE releases become head-limited.
  f_sin: Seasonal multiplier in the HYPE hydropower release formula.
  f_lin: Storage-limiting multiplier in the HYPE hydropower release formula.
  dom: Current day-of-month copied from `time%day_mo` for the Hanazaki-style year-start checks.
  mon: Current month copied from `time%mo` for time-dependent release logic.
  end_of_mo: End-of-month flag copied from `time%end_mo`; available for month-boundary logic.
uses:
  reservoir_data_module: '`reservoir_data_module` supplies the weir coefficient table `res_weir(iweir)`
    used when the selected action routes flow through a weir equation; without those geometry
    and coefficient values, the weir branch cannot compute discharge.'
  reservoir_module: '`reservoir_module` provides the reservoir operation state `res_ob(jres)`,
    which stores the rolling inflow and demand histories and the persistent values (`I_mean`,
    `c_ratio`, `S_ini`, `d_mean`) that the Hanazaki-style and hydropower branches update and
    reuse.'
  conditional_module: '`conditional_module` holds the decision-table structure that determines
    which action is active and which parameters to use. `res_hydro` depends on those tables
    to decide whether a particular release rule applies and to read the action constants,
    alternative hits, and condition metadata.'
  climate_module: '`climate_module` is the only imported module in the use list that is not
    backed by a resolved outside reference in the packet; no direct state from it was extracted
    for this routine, so its specific role here is uncertain from the available evidence.'
  time_module: '`time_module` supplies the current simulation calendar and subdaily step count.
    `res_hydro` uses those fields to split daily releases across steps and to pick day-, month-,
    or year-based measured hydrograph values.'
  hydrograph_module: '`hydrograph_module` provides the shared output objects that carry water
    volume through routing. `res_hydro` reads and updates `wbody%flo`, writes releases to
    `ht2%flo`, and uses `ht1%flo`, `irrig(iob)%demand`, and `recall(irel)%hd` in the inflow-
    and demand-driven branches.'
  water_body_module: '`water_body_module` provides the current water-body area `wbody_wb%area_ha`,
    which is converted to square meters and used to compute depth from volume for the weir
    and geometry-based release calculations.'
  soil_module: '`soil_module` is imported by the routine, but no soil-module symbols were
    resolved in the extracted source lines. The module may be included for shared types or
    future branches, but the packet gives no direct evidence of a soil-specific dependency
    here.'
  hru_module: '`hru_module` matters because reservoir and wetland control is embedded in the
    broader HRU/time-step flow routing workflow. The routine is invoked with an HRU-like object
    index context and shares the model-wide month variable `mo`, so it participates in the
    HRU routing sequence managed by the HRU module.'
  recall_module: '`recall_module` provides the metadata that tells `res_hydro` how to interpret
    a measured-release database, especially whether the hydrograph input is daily, monthly,
    or annual. That metadata selects which `recall(irel)%hd(...)` record becomes the outflow
    source.'
  water_allocation_module: '`water_allocation_module` provides the aggregated demand bookkeeping
    used by irrigation-transfer branches. `res_hydro` can use the allocation object''s total
    demand when release rules are tied to water-rights or transfer demand rather than only
    to reservoir storage.'
---

<!-- facts:header -->

Applies decision-table-based reservoir and wetland release rules for the current time step. It computes subdaily outflow, updates several reservoir operation statistics, and feeds later storage routing in the caller.

## Bottom Line

`res_hydro` is the rule engine that turns a reservoir or wetland decision table into an outflow volume for the current time step. It reads the active action table, checks which action conditions are met, and then accumulates the corresponding release into `ht2%flo` using the current water volume, target storages, inflow memory, demand memory, or weir geometry depending on the selected option.

The routine matters because its result is the discharge that `res_control` and `wetland_control` use immediately after the call. The lineage evidence also shows that later fixes moved the actual storage subtraction out of `res_hydro` to avoid double subtraction in the callers, while the newer `nonirr-h06`, `irr-h06`, and `hydrop` branches added reservoir-operation formulas and state tracking in `res_ob(jres)`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after the caller has selected the active decision table and assigned the current water-body pointers. `res_control` prepares the reservoir context and `wetland_control` prepares the wetland context, then both call `conditions(...)` before `res_hydro` evaluates the actions. Its result is the computed outflow in `ht2%flo`, which later routing code uses to subtract storage and to report surface outflow; lineage evidence shows that the subtraction itself was moved into the caller to prevent double subtraction.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize state and subdaily stepping | Copies the current water volume and water-surface area into working variables, derives the number of subdaily steps from `time%step`, and prepares to process releases one step at a time. |
| 2. Loop over each subdaily slice | Iterates `tstep` from 1 to `nstep` so the daily release can be distributed across each routing slice. |
| 3. Evaluate each decision-table action | Scans the reservoir decision table, checks whether the current action is hit by the condition alternatives, and only processes actions whose rules are satisfied. |
| 4. Dispatch the active release rule | Uses `select case (d_tbl%act(iac)%option)` to route the current action into the corresponding reservoir, wetland, irrigation, recall, or hydropower release formula. |
| 5. Apply direct constant or percentage releases | Implements fixed daily release and percentage-of-principal-volume releases by adding a volume increment to `ht2%flo`. |
| 6. Apply inflow-based release rules | Uses the current inflow hydrograph or a bounded inflow rate to set release proportional to inflow or to a minimum daily rate. |
| 7. Release emergency excess above flood storage | If the current body volume exceeds the emergency target, releases the excess volume above `evol_m3`. |
| 8. Build drawdown-days release targets | Selects a baseline target volume from the action metadata (`null`, `pvol`, or `evol`), converts the available surplus into a daily drawdown release, and floors the result at zero. |
| 9. Use yearly target-demand rules | Implements the year-scale release branches that vary target release using inflow and demand memory, including the `dyrt` and `dyrt1` schemes. |
| 10. Route irrigation-transfer demand | Calculates release for irrigation-transfer actions using the irrigation or water-allocation demand fields selected by the action metadata. |
| 11. Compute weir-based discharge | Evaluates weir geometry, computes head above the weir, and converts that head into a subdaily overflow discharge using the `res_weir` coefficients. |
| 12. Read measured hydrograph outflow | Pulls the release directly from a measured daily, monthly, or annual hydrograph record in `recall` using the timestep defined in `recall_db`. |
| 13. Apply natural-lake and Hanazaki-style reservoir formulas | Computes releases using the Doell natural-lake relation, the Hanazaki non-irrigation and irrigation reservoir schemes, and updates reservoir memory variables such as `I_mean`, `c_ratio`, `S_ini`, and `d_mean`. |
| 14. Apply hydropower release logic and finish | Calculates HYPE-style hydropower release from storage, seasonality, and mean inflow, then returns the accumulated outflow volume in `ht2%flo`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `res_weir` | `res_weir(iweir)%c, res_weir(iweir)%w, res_weir(iweir)%k` |
| [sym:reservoir_module] | `res_ob` | `res_ob(jres)%I_mean, res_ob(jres)%c_ratio, res_ob(jres)%S_ini, res_ob(jres)%d_mean` |
| [sym:conditional_module] | `d_tbl, dtbl_res` | `d_tbl%acts, d_tbl%alts, dtbl_res(id)%alts, d_tbl%act_hit(ial), d_tbl%act_outcomes(iac,ial), d_tbl%act(iac)%option, d_tbl%act(iac)%const, dtbl_res(id)%act(iac)%const2, dtbl_res(id)%act(iac)%const, dtbl_res(id)%act(iac)%file_pointer, d_tbl%act(iac)%const2, d_tbl%act(iac)%file_pointer, d_tbl%cond(ic)%lim_op, d_tbl%cond(ic)%lim_const, d_tbl%act_typ(iac)` |
| [sym:climate_module] | `time` | `time%day_mo, time%mo, time%end_mo, time%step, time%day, time%yrs` |
| [sym:time_module] | `time` | `time%day_mo, time%mo, time%end_mo, time%step, time%day, time%yrs` |
| [sym:hydrograph_module] | `wbody, ht2, ht1, irrig, recall` | `wbody%flo, ht2%flo, ht1%flo, irrig(iob)%demand, recall(irel)%hd` |
| [sym:water_body_module] | `wbody_wb` | `wbody_wb%area_ha` |
| [sym:soil_module] | `null` | `null` |
| [sym:hru_module] | `hru, mo` |  |
| [sym:recall_module] | `recall_db` | `recall_db(irel)%org_min%tstep` |
| [sym:water_allocation_module] | `wallo` | `wallo(iob)%tot%demand` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ht2%flo` | When an action branch adds a release amount, especially the `rate`, `rate_pct`, `inflo_rate`, `inflo_frac`, `ab_emer`, `days`, `meas`, `natlake`, `nonirr-h06`, `irr-h06`, or `hydrop` cases. | `ht2%flo` accumulates the subdaily outflow volume that the active rule produces. It is the main result of the routine and is later used by the caller to update the reservoir or wetland water balance. |
| `res_ob(jres)%I_mean` | Only in the `nonirr-h06`, `irr-h06`, and `hydrop` branches, where the code recomputes mean inflow from `res_ob(jres)%I_mon_past`. | `res_ob(jres)%I_mean` is refreshed as the rolling average inflow used to set the operating target for Hanazaki-style and hydropower reservoir releases. |
| `res_ob(jres)%c_ratio` | Only in the `nonirr-h06` and `irr-h06` branches after `smax` and `I_mean` are known. | `res_ob(jres)%c_ratio` is updated as the reservoir capacity ratio, which controls whether the release uses the simple `er*target_rel` form or the blended low-storage form. |
| `res_ob(jres)%S_ini` | Only in the `nonirr-h06` and `irr-h06` branches at the start of an operational year, when `dom == 1` and the current inflow is below the mean or storage exceeds `pvol_m3`. | `res_ob(jres)%S_ini` stores the starting storage for the current operating year. The routine refreshes it when the year begins or when storage rises above the principal volume threshold. |
| `res_ob(jres)%d_mean` | Only in the `irr-h06` branch, where the code computes the long-term mean irrigation demand from `d_mon_past`. | `res_ob(jres)%d_mean` tracks the rolling average irrigation demand used to decide whether the irrigation reservoir should follow the environmental-flow-dominant target or the demand-adjusted target. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:1.1.8 | Measured daily reservoir outflow | $V_{flowout}=86400*q_{out}$ | ht2%flo+=recall%hd(day,yr)%flo/nstep; recall stores daily volumes (m3). V=86400*q_out conversion applied when reading the recall input file. |
| 8:1.1.13 | Target storage V_targ = starg | $V_{targ}=starg$ | pvol_m3=res_ob(jres)%pvol is the normal-season target (starg); used as b_lo in case('days'). |
| 8:1.1.14 | Flood-season target V_targ = V_em | $V_{targ}=V_{em}$ | b_lo=evol_m3 when file_pointer='evol'; evol_m3=V_em. Season switching via decision-table conditions() before res_hydro. |
| 8:1.1.15 | Non-flood season target selection | $mon \le mon_{fld,beg}$ | b_lo=pvol_m3 when file_pointer='pvol'; season logic encoded in decision table. |
| 8:1.1.16 | Controlled release V_flowout = (V-V_targ)/ND_targ | $V_{flowout}=\frac{V-V_{targ}}{ND_{targ}}$ | ht2%flo+=(wbody%flo-b_lo)/const/nstep; const=ND_targ, b_lo=V_targ. Exact match. |
| 8:1.1.17 | Outflow within release bounds [q_rel_mn, q_rel_mx] | $V_{flowout}=V'_{flowout}$ | No explicit [q_rel_mn*86400, q_rel_mx*86400] clipping in res_hydro.f90. Bounds may be encoded in decision-table conditions or handled by caller. Line 135 only clamps to >=0. |
| 8:1.1.18 | Release floored to q_rel_mn*86400 | $V_{flowout}=q_{rel,mn}*86400$ | Minimum release floor not found as explicit formula in res_hydro.f90. |
| 8:1.1.19 | Release capped to q_rel_mx*86400 | $V_{flowout}=q_{rel,mx}*86400$ | Maximum release cap not found as explicit formula in res_hydro.f90. |
| 8:1.2.11 | Pond flood-season target V_targ=V_em | $V_{targ}=V_{em}$ | evol_m3 used as b_lo in case('days') or ab_emer case. Season switching via decision table. |
| 8:1.2.12 | Pond non-flood season target V_targ=V_nor | $mon \le mon_{fld,beg}$ | b_lo=pvol_m3 (=V_nor) in case('days'); non-flood season logic in decision table. |
| 8:1.2.13 | Pond outflow V_flowout=(V-V_targ)/ND | $V_{flowout}=\frac{V-V_{targ}}{ND_{targ}}$ | ht2%flo+=(wbody%flo-b_lo)/const/nstep; exact match V_flowout=(V-V_targ)/ND_targ. |
| 8:1.2.14 | Wetland outflow zero when V < V_nor | $V_{flowout}=0$ | ht2%flo clamped to 0 at line 135 when wbody%flo<=b_lo. Decision table ensures path only activates when V>=V_nor. |
| 8:1.2.15 | Wetland outflow (V-V_nor)/10 when V_nor<=V<=V_mx | $V_{flowout}=\frac{V-V_{nor}}{10}$ | case('days') with b_lo=pvol(=V_nor) and const=10: ht2%flo=(wbody%flo-pvol)/10. Exact match. |
| 8:1.2.16 | Wetland outflow V-V_mx when V > V_mx | $V_{flowout}=V-V_{mx}$ | case('ab_emer'): if(wbody%flo>evol_m3) ht2%flo+=(wbody%flo-evol_m3); evol_m3=V_mx. Exact match. |
| 8:1.3.10 | Depression overflow V_flowout=V-V_pot_mx | $V_{flowout}=V-V_{pot,mx}$ | case('ab_emer'): if(wbody%flo>evol_m3) ht2%flo+=(wbody%flo-evol_m3); evol_m3=V_pot_mx. Exact match. |
| 8:1.3.11 | Depression release all V_flowout=V | $V_{flowout}=V$ | case('days') with const=1 and b_lo=0 gives ht2%flo=wbody%flo. |
| 8:1.3.12 | Tile flow V_flowout=q_tile*86400 when V > q_tile*86400 | $V_{flowout}=q_{tile}*86400$ | case('rate'): ht2%flo+=const*86400 (constant daily tile rate); V>daily capacity condition in decision table. |
| 8:1.3.13 | Tile flow V_flowout=V when V <= q_tile*86400 | $V_{flowout}=V$ | When V<daily release capacity, clamp at line 135 and storage update in res_control ensures outflow<=V. |

## Lineage

Four resolved commits changed `res_hydro` behavior in the evidence. `f1e61a3` only fixed tabs and did not alter algorithmic behavior. `0c9f7bd` changed the weir branch to use `if (nstep>1)` instead of the older hourly-only condition and left the weir-release accumulation commented out. `29e2d36` renamed the irrigation action from `irrig_dmd` to `irrig_trn`. `a03cc8b` re-enabled the storage subtraction in the release branch, while `f8d2c4a` later commented that subtraction back out in `res_hydro` because `res_control` already performs it; the same commit also commented out the direct `wbody%flo = vol` assignment in the weir branch to avoid double subtraction.

- `0c9f7bd` broadened the weir branch trigger to any subdaily timestep (`nstep>1`) and changed how the weir discharge path is exercised during routing.
- `29e2d36` changed the irrigation-related action name recognized by the decision table from `irrig_dmd` to `irrig_trn`.
- `a03cc8b` restored direct subtraction of `ht2%flo` from `wbody%flo` inside `res_hydro`, affecting how release volumes were applied at that time.
- `f8d2c4a` reversed the in-routine storage subtraction and `vol` reassignment because the callers already subtract release, preventing double subtraction in reservoir and wetland routing.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_hydro' has no extracted documentation comment.
- climate_module is imported but no resolved outside references from that module were extracted in the packet; its specific use here is uncertain.
- algorithm_steps revised: merged the original draft's overly fine-grained case labels into source-backed phases that match the visible control flow and line ranges.
