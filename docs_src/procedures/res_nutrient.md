---
kind: procedure
symbol: res_nutrient
title: res_nutrient
status: filled
source_hash: 0c187fe41787f1cb
version_label: SWAT+ 62.0.0
args:
  iob: '`iob` selects the current object connectivity entry in `ob(iob)`, which supplies the
    linked weather-station index `wst`. That weather station drives the temperature used in
    the settling-rate correction.'
locals:
  theta: Temperature-adjustment function used to convert the base settling coefficients (`nsetlr`,
    `psetlr`, `nsolr`, `psolr`) into a rate at the current water temperature.
  nitrok: Fractional loss factor for organic nitrogen settling. It is computed from total
    nitrogen concentration, the minimum concentration threshold, and the temperature-adjusted
    settling coefficient.
  phosk: Fractional loss factor for particulate phosphorus settling. It is computed from total
    phosphorus concentration, the minimum concentration threshold, and the temperature-adjusted
    settling coefficient.
  nitrosolk: Fractional loss factor for soluble nitrogen species (`no3`, `nh3`, `no2`). It
    is computed separately from `nitrok` so soluble nitrogen can use `nsolr` instead of the
    organic-N settling rate.
  phossolk: Fractional loss factor for soluble phosphorus (`solp`). It is computed separately
    from `phosk` so soluble phosphorus can use `psolr` instead of the particulate-P settling
    rate.
  tpco: Temporary total-phosphorus concentration used to decide whether chlorophyll-a should
    be recomputed.
  chlaco: Working chlorophyll-a coefficient/placeholder. It is reset to zero here, and the
    commented empirical TP-to-chlorophyll expression is not active in this source.
  iwst: Weather-station index taken from `ob(iob)%wst`, used to fetch the daily average temperature
    that drives `Theta`.
  nsetlr: 'Selected nitrogen settling rate coefficient for the current month: `nsetlr1` during
    the mid-year settling season, otherwise `nsetlr2`.'
  psetlr: 'Selected phosphorus settling rate coefficient for the current month: `psetlr1`
    during the mid-year settling season, otherwise `psetlr2`.'
  nsolr: Base settling/loss coefficient for soluble nitrogen species, copied from reservoir
    parameters before the soluble-N fractions are calculated.
  psolr: Base settling/loss coefficient for soluble phosphorus, copied from reservoir parameters
    before the soluble-P fraction is calculated.
  conc_n: Total nitrogen concentration in the water body, computed from organic N plus nitrate,
    ammonium, and nitrite divided by water volume and scaled to ppm-like units.
  conc_p: Total phosphorus concentration in the water body, computed from sediment P plus
    soluble P divided by water volume and scaled to ppm-like units.
  conc_soln: Soluble nitrogen concentration used to compute the separate soluble-N loss factor
    from the total-N settling factor.
  conc_solp: Soluble phosphorus concentration used to compute the separate soluble-P loss
    factor from the total-P settling factor.
uses:
  reservoir_data_module: 'This module provides the reservoir nutrient-season parameters and
    thresholds that control the whole calculation: month window, settling coefficients, minimum
    concentrations, temperature factors, and soluble-loss fractions. Without `wbody_prm%nut`
    and the soluble-fraction fields, the routine could not choose the right seasonal rates
    or compute the loss fractions.'
  time_module: The current month determines whether the routine uses the mid-year or default
    settling coefficients. `time%mo` is the switch that selects between `nsetlr1/psetlr1`
    and `nsetlr2/psetlr2`.
  reservoir_module: '`reservoir_module` supplies the shared reservoir/wetland parameter pointer
    used here as `wbody_prm`, and it also provides the zero-state reset target `resz` for
    the empty-volume early return. Those values are what let the routine access the current
    water-body nutrient settings and clear the body when there is essentially no water.'
  hydrograph_module: '`hydrograph_module` holds the shared hydrologic output structures that
    the routine reads and writes. `wbody` is the active reservoir/wetland state, `ht2` carries
    the current outflow volume used to compute exported nutrient mass, and `ob(iob)%wst` links
    the object to the correct weather station.'
  climate_module: '`climate_module` matters because the settling fractions are temperature
    dependent. The routine uses `wst(iwst)%weat%tave` as the temperature argument passed into
    `Theta`.'
---

<!-- facts:header -->

Adjusts reservoir or wetland nutrient stores for settling, temperature effects, and outlet export during the current time step.

## Bottom Line

res_nutrient updates the nutrient state held in `wbody` for a reservoir or wetland object. It first skips empty water bodies, then computes temperature-adjusted settling and soluble losses, estimates chlorophyll-a, and finally removes the nutrient mass that leaves through the outlet flow.

The routine matters because it is the reservoir/wetland nutrient balance step called from control logic after hydrology has already set the body volume and outflow. Its results feed the next model state through the shared `wbody` and `ht2` hyd output structures.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after `res_control` or `wetland_control` has already assembled the current reservoir/wetland hydrologic state in `wbody` and set the outlet flow in `ht2`. Those upstream routines call it to perform the constituent balance, and later model behavior depends on the updated `wbody` and `ht2` values when the outflow constituent loads are carried forward.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check empty water body | If reservoir volume is below the tiny threshold, copy the zero-state template `resz` into `wbody` and stop. This bypasses all nutrient calculations when the water body is effectively dry. |
| 2. select seasonal settling rates | Use the current month to choose the nitrogen and phosphorus settling coefficients for either the mid-year period or the rest of the year, and copy the soluble-rate coefficients into local variables. |
| 3. compute nutrient concentrations | Compute total nitrogen, total phosphorus, soluble nitrogen, and soluble phosphorus concentrations from the current `wbody` masses and volume, scaling them to concentration units used by the settling equations. |
| 4. get weather station and temperature-correct rates | Look up the linked weather station from `ob(iob)`, then compute and clamp the organic-N, particulate-P, soluble-N, and soluble-P loss fractions using concentration above minimum thresholds and the temperature-adjusted `Theta` rates. |
| 5. apply settling losses | Reduce the reservoir/wetland nutrient masses by the computed fractions, with separate handling for soluble and particulate pools. This is the main settling update for the current time step. |
| 6. compute chlorophyll-a proxy | Reset chlorophyll-a work variables, compute total phosphorus concentration, and if the threshold is exceeded assign a simple volume-based chlorophyll-a value. The empirical TP-to-chlorophyll formula remains commented out. |
| 7. enforce nonnegative masses | Clip all nutrient and chlorophyll-a masses to zero or greater so numerical subtraction does not leave small negative values. |
| 8. compute exported nutrient loads | Partition each nutrient mass in proportion to outlet flow `ht2%flo` over total water volume plus outlet flow, creating the amount leaving the reservoir or wetland in this step. |
| 9. subtract exported masses | Remove the exported nutrient masses from `wbody`, again protecting against negatives. These are the remaining in-body masses after outflow has been accounted for. |
| 10. return | Exit after the shared water-body state has been updated for the current reservoir or wetland object. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `wbody_prm` | `wbody_prm%nut%ires1, wbody_prm%nut%ires2, wbody_prm%nut%nsetlr1, wbody_prm%nut%psetlr1, wbody_prm%nut%nsetlr2, wbody_prm%nut%psetlr2, wbody_prm%nut%nsolr, wbody_prm%nut%psolr, wbody_prm%nut%conc_nmin, wbody_prm%nut%theta_n, wbody_prm%nut%conc_pmin, wbody_prm%nut%theta_p, wbody_prm%solp_stl_fr, wbody_prm%soln_stl_fr` |
| [sym:time_module] | `time` | `time%mo` |
| [sym:reservoir_module] | `wbody_prm, resz` | `wbody_prm%nut%ires1, wbody_prm%nut%ires2, wbody_prm%nut%nsetlr1, wbody_prm%nut%psetlr1, wbody_prm%nut%nsetlr2, wbody_prm%nut%psetlr2, wbody_prm%nut%nsolr, wbody_prm%nut%psolr, wbody_prm%nut%conc_nmin, wbody_prm%nut%theta_n, wbody_prm%nut%conc_pmin, wbody_prm%nut%theta_p, wbody_prm%solp_stl_fr, wbody_prm%soln_stl_fr, resz` |
| [sym:hydrograph_module] | `wbody, ob, ht2, resz` | `wbody%flo, wbody%orgn, wbody%sedp, wbody%no3, wbody%nh3, wbody%no2, wbody%solp, ob(iob)%wst, wbody%chla, ht2%flo, ht2%no3, ht2%orgn, ht2%sedp, ht2%solp, ht2%chla, ht2%nh3, ht2%no2` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%tave` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wbody` | When `wbody%flo >= 1.e-6`, and after settling, chlorophyll, and outflow export are applied. | `wbody` is updated in place to hold the post-settling, post-export reservoir or wetland masses for nutrients and chlorophyll-a. That updated state is what later routing and balance routines see for the same object. |
| `wbody%solp` | After total phosphorus is checked and `tpco > 1.e-4`. | `wbody%solp` is first reduced by soluble phosphorus settling and then further reduced by the portion leaving in `ht2%solp`. The value represents the remaining soluble phosphorus in the body after all losses for the step. |
| `wbody%sedp` | After particulate phosphorus settling and outflow export are applied. | `wbody%sedp` is reduced by the settling fraction and then by exported sediment phosphorus. It becomes the remaining particulate phosphorus stored in the water body. |
| `wbody%orgn` | After the nitrogen settling fractions are computed and after export loads are removed. | `wbody%orgn` is reduced by settling and by the outgoing organic-N load, leaving the stored organic nitrogen for the next time step. |
| `wbody%no3` | After soluble-N settling, clamping, and outflow subtraction. | `wbody%no3` is reduced by the soluble nitrogen loss fraction and by the nitrate exported through `ht2%no3`, then clipped at zero. |
| `wbody%nh3` | After soluble-N settling, clamping, and outflow subtraction. | `wbody%nh3` is reduced by the same soluble nitrogen loss logic as nitrate and then by the ammonium exported in the outlet flow. |
| `wbody%no2` | After soluble-N settling, clamping, and outflow subtraction. | `wbody%no2` is reduced by the same soluble nitrogen loss logic as nitrate and then by the nitrite exported in the outlet flow. |
| `wbody%chla` | When phosphorus is high enough to enter the chlorophyll calculation branch, and then after export subtraction. | `wbody%chla` is reset, assigned a simple volume-based proxy if TP exceeds the threshold, and then reduced by the chlorophyll mass leaving with the outflow. |
| `ht2%no3` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%no3` stores the nitrate mass that leaves the body in proportion to outlet flow, so downstream routing can carry that exported load. |
| `ht2%orgn` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%orgn` stores the exported organic nitrogen mass for the current time step. |
| `ht2%sedp` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%sedp` stores the exported particulate phosphorus mass for the current time step. |
| `ht2%solp` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%solp` stores the exported soluble phosphorus mass for the current time step. |
| `ht2%chla` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%chla` stores the chlorophyll-a mass leaving the body with the outlet flow. |
| `ht2%nh3` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%nh3` stores the exported ammonium mass for the current time step. |
| `ht2%no2` | After `ht2%flo` is known and before subtracting the exported load from the reservoir or wetland. | `ht2%no2` stores the exported nitrite mass for the current time step. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:3.1.1 | Initial nutrient mass M_initial | $M_{initial}=M_{stored}+M_{flowin}$ | M_initial=M_stored+M_flowin: nutrients accumulated via res+=ht1 in res_control before res_nutrient called; wbody holds combined mass. |
| 8:3.1.2 | Initial volume V_initial | $V_{initial}=V_{stored}+V_{flowin}$ | V_initial=V_stored+V_flowin: same mechanism as 8:3.1.1; wbody%flo holds combined volume. |
| 8:3.1.3 | Nutrient settling M_settling=v*c*A_s*dt | $M_{settling}=v*c*A_s*dt$ | Theory: M_settling=v*c*A_s*dt. Code: nitrok=(conc_n-conc_nmin)*Theta(nsetlr,theta_n,T); wbody%orgn*=(1-nitrok). Temperature-corrected fractional removal, not explicit v*c*A_s*dt formula. |
| 8:3.2.1 | Nutrient mass balance ODE | $V*\frac{dc}{dt}=W(t)-Q*c-v*c*A_s$ | V*dc/dt=W(t)-Q*c-v*c*A_s solved as implicit daily-step: fractional settling (lines 73-78) then proportional outflow (lines 100-115). Not an explicit ODE solver. |
| 8:3.3.1 | Chla from TP: Chla = 0.551*p^0.76 | $Chla=0.551*p^{0.76}$ | FLAG: line 86 !chlaco = wbody_prm%nut%chlar * 0.551 * (tpco**0.76) is COMMENTED OUT. Line 87 uses trivial volume-proportional assignment instead. |
| 8:3.3.2 | Chla with correction: Chla_co*0.551*p^0.76 | $Chla=Chla_{co}*0.551*p^{0.76}$ | Commented out â€” same as 8:3.3.1. chlar coefficient exists in parameter structure but formula inactive. |
| 8:5.1.1 | Less-persistent bacteria decay in reservoir | $bact_{lpres,i}=bact_{lpre s,i-1}*exp(\mu _{lpres,die})$ | bact_lpres_i=bact_lpres_i-1*exp(mu_lpres_die) not found in res_nutrient.f90 or any other reservoir/wetland routine. Bacteria tracking in reservoirs not implemented. |
| 8:5.1.2 | Persistent bacteria decay in reservoir | $bact_{pres,i}=bact_{pres,i-1}*exp(\mu _{pres,die})$ | bact_pres_i not found in reservoir routines; see 8:5.1.1. |
| 8:5.1.3 | Less-persistent bacteria die-off rate | $\mu_{lpres,die} =\mu_{lpres,die,20} * \theta _{bact}^{(T_{water}-20)}$ | mu_lpres_die=mu_lpres_die_20*theta_bact^(T-20) not found in reservoir routines. |
| 8:5.1.4 | Persistent bacteria die-off rate | $\mu_{pres,die} =\mu_{pres,die,20} * \theta _{bact}^{(T_{water}-20)}$ | mu_pres_die=mu_pres_die_20*theta_bact^(T-20) not found in reservoir routines. |

## Lineage

Five resolved commits changed `res_nutrient`. The earliest available version in 94b6dec introduced the subroutine with the empty-body reset, seasonal settling choices, concentration calculations, temperature correction, chlorophyll handling, and outlet subtraction. 39fabde added initial zero values to the local variables. fcf3891 changed the settling comment and temporarily commented out the soluble nutrient reductions. 1b4a94c restored soluble phosphorus and soluble nitrogen loss formulas into the combined terms. 72206bc renamed the local soluble-rate variables (`nitrosolk`, `phossolk`) and switched the formulas to use them. e18817a wrapped all outlet subtraction steps in `max(0., ...)` to prevent negative masses.

- 94b6dec introduced the full reservoir/wetland nutrient-balance subroutine, including temperature-dependent settling and export through `ht2`.
- 39fabde only initialized the local scalars and weather-station index to zero; it did not change the algorithm.
- fcf3891 removed active soluble-N and soluble-P settling from the code path by commenting those updates out.
- 1b4a94c reintroduced soluble phosphorus and soluble nitrogen reductions using the combined product form `1. - rate * stl_fr`.
- 72206bc refactored the soluble settling calculations to use separate `nitrosolk` and `phossolk` variables instead of reusing the particulate factors.
- e18817a added lower-bound protection with `max(0., ...)` around every nutrient export subtraction.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_nutrient' has no extracted documentation comment.
