---
kind: procedure
symbol: res_sediment
title: res_sediment
status: filled
source_hash: 878f365dde361ebb
version_label: SWAT+ 62.0.0
locals:
  sed_ppm: Temporary suspended-sediment concentration in parts per million, computed from
    `wbody%sed / wbody%flo`, floored at `1.e-6`, and then adjusted by the settling rule when
    concentration exceeds `wbody_prm%sed%nsed`.
  sil_ppm: Temporary silt concentration in parts per million, computed from `wbody%sil / wbody%flo`
    and floored at `1.e-6`; in this routine it is only initialized and not used in a later
    update.
  cla_ppm: Temporary clay concentration in parts per million, computed from `wbody%cla / wbody%flo`
    and floored at `1.e-6`; in this routine it is only initialized and not used in a later
    update.
uses:
  reservoir_data_module: '`wbody_prm` carries the sediment parameterization for the current
    reservoir or wetland. `wbody_prm%sed%nsed` defines the minimum equilibrium concentration
    threshold used to decide whether settling should occur, and `wbody_prm%sed_stlr_co` controls
    how strongly the concentration is reduced toward that threshold.'
  reservoir_module: '`reservoir_module` matters because this routine is invoked from reservoir
    routing and uses the reservoir-side water-body context to update the current body’s sediment
    condition before the rest of reservoir control continues.'
  conditional_module: '`conditional_module` is listed in the procedure’s `use` set, so it
    is part of the compilation context, but the extracted source for this routine shows no
    direct references to symbols from that module.'
  climate_module: '`climate_module` is part of the routine’s module context, but the extracted
    code fragment does not directly read climate symbols here; it remains relevant because
    the calling routing workflow is climate-driven at the daily timestep.'
  time_module: '`time_module` matters because the surrounding control routines operate on
    the current simulation step, and this sediment update is performed as part of that daily/stepwise
    routing sequence even though no time symbol is referenced directly in the extracted lines.'
  hydrograph_module: '`hydrograph_module` supplies the shared hydrologic output records that
    this routine reads and mutates. `wbody` holds the current water-body volume and sediment
    masses, `ht2` carries the routed outflow sediment mass, and `hz` is the zeroed empty-body
    template used when the reservoir has effectively no water.'
  water_body_module: '`water_body_module` matters because it provides the shared water-body
    object that this routine updates in place for reservoir and wetland sediment bookkeeping.'
---

<!-- facts:header -->

Updates reservoir or wetland sediment after daily flow routing by applying a settling adjustment to sediment concentration and then resetting the suspended sand, silt, clay, aggregated sand, large aggregate, and gravel stores when conditions warrant.

## Bottom Line

`res_sediment` operates on the shared water-body state for reservoirs and wetlands. It converts the current stored sediment mass and water volume into concentration, compares that concentration to the minimum equilibrium sediment concentration `wbody_prm%sed%nsed`, and if needed applies the settling coefficient `wbody_prm%sed_stlr_co` to reduce concentration before updating the water-body sediment mass.

If the water body is effectively empty, it zeroes the water-body state and leaves a tiny concentration floor for the local ppm variables. The routine matters because later control logic uses the updated `wbody`/`ht2` sediment quantities as the sediment result for the current routing step.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after upstream control has assembled the current water-body flow and sediment state for the step. `res_control` calls it after routing the reservoir outflow flow, and `wetland_control` calls it before copying `wbody%sed` back into `wet(j)%sed`; downstream reservoir and wetland balances depend on the updated sediment masses and zeroed suspended fractions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check for an effectively empty water body | If `wbody%flo` is smaller than `1.e-6`, treat the reservoir or wetland as empty: copy the zero-state template `hz` into `wbody`, force `wbody%sed` and `ht2%sed` to zero, and initialize the local concentration variables to a tiny floor value. |
| 2. compute current concentrations | When water is present, convert stored sediment masses to ppm concentrations using `1000000. * mass / wbody%flo` for total sediment, silt, and clay, and clamp each to at least `1.e-6`. |
| 3. apply settling only above equilibrium | If total sediment concentration exceeds `wbody_prm%sed%nsed`, reduce it toward equilibrium with the settling coefficient `wbody_prm%sed_stlr_co`, then clamp the result so it does not fall below the equilibrium concentration. |
| 4. update stored sediment mass | Convert the adjusted concentration back to mass for `wbody%sed`, compute sediment exported in `ht2%sed`, and subtract that outflow sediment from the remaining stored sediment while preventing a negative result. |
| 5. clear settled coarse fractions | After the settling calculation, set suspended silt, clay, sand, small aggregate, large aggregate, and gravel masses to zero, reflecting the routine’s assumption that these coarse fractions settle out here. |
| 6. return to caller | Exit after leaving the shared water-body state updated for the current routing step. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `wbody_prm` | `wbody_prm%sed%nsed, wbody_prm%sed_stlr_co` |
| [sym:reservoir_module] | `wbody, ht2, hz` | `wbody%flo, wbody%sed, ht2%sed, wbody%sil, wbody%cla, ht2%flo, wbody%san, wbody%sag, wbody%lag, wbody%grv, wbody, hz` |
| [sym:conditional_module] | `no resolved imported state or types were extracted from `conditional_module`` | `none resolved` |
| [sym:climate_module] | `no resolved imported state or types were extracted from `climate_module`` | `none resolved` |
| [sym:time_module] | `no resolved imported state or types were extracted from `time_module`` | `none resolved` |
| [sym:hydrograph_module] | `wbody, ht2, hz` | `wbody%flo, wbody%sed, ht2%sed, wbody%sil, wbody%cla, ht2%flo, wbody%san, wbody%sag, wbody%lag, wbody%grv` |
| [sym:water_body_module] | `wbody` | `wbody` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wbody` | `wbody%flo < 1.e-6` | The shared water-body record is reset to the empty template so later routing logic sees no active reservoir or wetland storage for this step. |
| `wbody%sed` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Stored sediment mass is recalculated from the adjusted concentration, so the water body retains the settled amount after the concentration reduction. |
| `ht2%sed` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Outflow sediment is computed from the updated concentration and routed volume, so the current step’s exported sediment mass is available to the caller. |
| `wbody%sil` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Silt is forced to zero after settling, representing complete removal of that suspended fraction in this routine. |
| `wbody%cla` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Clay is forced to zero after settling, representing complete removal of that suspended fraction in this routine. |
| `wbody%san` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Sand is forced to zero after settling, so no suspended sand remains in the shared water-body record. |
| `wbody%sag` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Small aggregate sediment is forced to zero as part of the coarse-fraction settling assumption. |
| `wbody%lag` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Large aggregate sediment is forced to zero as part of the coarse-fraction settling assumption. |
| `wbody%grv` | `wbody%flo >= 1.e-6` and `sed_ppm > wbody_prm%sed%nsed` | Gravel is forced to zero as part of the coarse-fraction settling assumption. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:2.1.1 | Sediment mass balance in water body | $sed_{wb}=sed_{wb,i}+sed_{flowin}-sed_{stl}-sed_{flowout}$ | sed_wb=sed_wb_i+sed_flowin-sed_stl-sed_flowout: wbody%sed includes incoming (added via res+=ht1 in res_control); line 40 updates after settling; line 43 subtracts outflow. |
| 8:2.2.1 | Detention time t_D | $t_D=\frac{(C_t(1-DS)Vol)}{Q_o}$ | t_D=C_t*(1-DS)*Vol/Q_o not computed. Code uses coefficient-based settling (sed_stlr_co), not the Brune/trapping-efficiency approach. |
| 8:2.2.2 | Trap efficiency trappeff | $trappeff=V_{setl}/V_{ovfl}$ | trappeff=V_setl/V_ovfl not computed; code uses sed_stlr_co concentration-decay. |
| 8:2.2.3 | Overflow velocity V_ovfl | $V_{ovfl}=\frac{(Q_o/SA_{res})}{(10,000)}$ | V_ovfl=Q_o/(SA_res*10000) not computed. |
| 8:2.2.4 | Initial sediment concentration | $conc_{sed,i}=\frac{(sed_{wb,i}+sed_{flowin})}{(V_{stored}+V_{flowin})}$ | sed_ppm=1e6*wbody%sed/wbody%flo; wbody aggregates stored+flowin. Exact match conc_sed_i=(sed_wb_i+sed_flowin)/(V_stored+V_flowin). |
| 8:2.2.5 | Final concentration when conc > equilibrium | $conc_{sed,i}>conc_{sed,eq}$ | FLAG: code uses sed_ppm=(sed_ppm-nsed)*sed_stlr_co+nsed (linear decay toward equilibrium nsed), not conc_f=conc_i*(1-trappeff). Functionally similar purpose, mechanistically different. |
| 8:2.2.6 | Final concentration unchanged when conc <= equilibrium | $conc_{sed,f}=conc_{sed,i}$ | if(sed_ppm>nsed) branch at line 36; no adjustment when sed_ppm<=nsed. Matches conc_sed_f=conc_sed_i. |
| 8:2.2.7 | Median particle size d_50 | $d_{50}=exp(0.41*\frac{m_c}{100}+2.71*\frac{m_{silt}}{100}+5.7*\frac{m_s}{100})$ | d_50=exp(0.41*m_c/100+2.71*m_silt/100+5.7*m_s/100) not computed; code does not use d_50-based settling velocity. |
| 8:2.2.8 | Settled sediment sed_stl | $sed_{stl}=(conc_{sed,i}-conc_{sed,f})*V$ | Implicit: settled=(sed_ppm_before-sed_ppm_after)*flo/1e6 from line 37 update then line 40 wbody%sed=sed_ppm*flo/1e6. Matches sed_stl=(conc_i-conc_f)*V conceptually via coefficient mechanism. |
| 8:2.3.1 | Sediment in reservoir outflow | $sed_{flowout}=conc_{sed,f}*V_{flowout}$ | ht2%sed=sed_ppm*ht2%flo/1e6; exact match sed_flowout=conc_sed_f*V_flowout. |

## Lineage

Resolved lineage shows four source-backed changes to `res_sediment`: the original bitbucket import, later replacement of an older trapping-efficiency style sediment update with the current concentration-decay approach, a cleanup that removed extra indentation, and a 2025 change that zeroed the empty-body sediment fields and simplified the concentration calculation by removing a nested `if (wbody%flo > 0.)` check. The most recent resolved diff also commented out the final outflow subtraction lines in favor of the current explicit storage update earlier in the routine.

- 94b6dec introduced the routine in its earlier form, including a trapping-style sediment reduction and direct subtraction of outflow sediment from `wbody%sed`.
- e18817a replaced the older trap-based logic with the current `wbody_prm%sed_stlr_co` concentration adjustment, updated `wbody%sed` before computing `ht2%sed`, and zeroed `wbody%sil`, `wbody%cla`, `wbody%san`, `wbody%sag`, `wbody%lag`, and `wbody%grv`.
- f1e61a3 made formatting-only tab cleanup with no behavioral change.
- 0c9f7bd added explicit zeroing for empty-body sediment fields, simplified concentration calculation by removing a redundant nested flow check, and commented out the old final outflow subtraction lines.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_sediment' has no extracted documentation comment.
- algorithm_steps revised: merged the empty-body branch and subsequent return into a six-step outline aligned to the visible source lines.
- Source uncertainty note: `conditional_module`, `climate_module`, `time_module`, and `water_body_module` are listed in the `use` statements, but no direct symbol references from those modules were resolved in the extracted source for this routine.
