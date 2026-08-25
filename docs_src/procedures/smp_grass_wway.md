---
kind: procedure
symbol: smp_grass_wway
title: smp_grass_wway
status: filled
source_hash: 87cbb6ae2dec2add
version_label: SWAT+ 62.0.0
locals:
  chflow_m3: Converted runoff volume in cubic meters per second equivalent, derived from daily
    runoff before peak-flow checks and Manning-based calculations.
  sf_area: Effective sheetflow area along the waterway sides. It is computed from waterway
    geometry, limited to a fraction of HRU area, and used to derive runoff depth and sediment
    loading over the treated side slope.
  surq_remove: Percent of surface runoff removed by the grassed waterway treatment. It is
    computed from sheetflow depth, then capped to the valid 0-95 range and used to leave runoff-related
    pesticide loads unchanged only by the remaining fraction.
  sed_remove: Percent of sediment removed by the grassed waterway. It is computed from sheetflow
    sediment load and runoff removal, capped to 0-95, and used to scale sediment, nutrient,
    and pesticide sediment-phase losses.
  sf_sed: Sheetflow sediment loading in kg/m^2 over the waterway sides. It is derived from
    incoming sediment yield and effective sheetflow area and drives the sediment-removal equation.
  vc: Computed channel flow velocity for the waterway reach. It is estimated from discharge
    and cross-sectional area, with an upper bound at bankfull celerity, and is used to calculate
    sediment transport capacity.
  chflow_day: Daily runoff volume converted to m^3/day. It is the intermediate used to obtain
    peak discharge and later to compute sediment concentration and deposition terms.
  j: Current HRU index copied from ihru so the routine can read and update the active HRU's
    state arrays.
  rchdep: Water depth in the grassed waterway channel for the current day. It is set either
    to bankfull depth or iteratively increased until Manning discharge matches the target
    peak flow.
  p: Wetted perimeter of the assumed trapezoidal channel cross section. It is used with rcharea
    to compute hydraulic radius for the Manning calculation.
  rh: Hydraulic radius of the current waterway section. It is passed to qman to estimate discharge
    or velocity under Manning's equation.
  qman: External Manning-equation helper used to compute discharge or velocity from cross-sectional
    geometry, roughness, and slope.
  sedin: Incoming sediment yield from the HRU, copied before treatment so the routine can
    compute how much sediment enters the waterway system.
  sf_depth: Runoff depth across the effective sheetflow treatment area. It is used to estimate
    runoff removal from the simplified grassed-waterway relation.
  sedint: Sediment remaining after sheetflow removal, before channel deposition. It is the
    sediment mass passed into the in-channel deposition calculation.
  cyin: Incoming sediment concentration derived from sedint and daily runoff volume. It is
    compared with transport capacity to estimate deposition.
  cych: Sediment transport capacity of the waterway flow, computed from waterway-specific
    sediment transport coefficient and flow velocity.
  rcharea: Cross-sectional flow area for the current waterway hydraulic condition. It is either
    the bankfull area or the iteratively solved area used to compute velocity and deposition.
  depnet: Net sediment deposition mass in the waterway channel. It is computed from the difference
    between incoming concentration and transport capacity and then used to derive sediment
    leaving the waterway.
  deg: Placeholder for degradation/re-entrainment-related sediment handling. In this routine
    it is reset to zero and not otherwise used in the shown calculations.
  dep: Placeholder for deposition bookkeeping. In this routine it is reset to zero and not
    otherwise used in the shown calculations.
  sedout: Sediment mass leaving the waterway after deposition losses. It is the remaining
    sediment used to calculate sediment fraction transported downstream.
  sed_frac: Fraction of the original sediment yield that remains after waterway treatment.
    It is used to scale sediment and sediment-attached nutrient state variables.
  surq_frac: Fraction of surface runoff that remains after runoff removal. It is used to scale
    the surface-runoff pesticide load component.
  sedtrap: Sediment trapped by the waterway treatment. It is the amount removed from the HRU
    sediment pool and subtracted from sediment-class yield pools in sequence.
  xrem: Remaining trapped sediment to allocate across sediment size classes after the largest
    class is depleted.
  k: Loop index over simulated pesticide constituents in cs_db%num_pests.
uses:
  hru_module: The grassed-waterway logic reads HRU geometry, runoff, sediment, nutrient, and
    pesticide state from hru_module and writes reduced values back to those same HRU arrays.
    It also needs the active HRU index, hydraulic time-of-concentration, and the grass-waterway
    management parameters stored on hru(j)%lumv to decide whether the treatment runs and how
    strong the removal should be.
  constituent_mass_module: The routine needs cs_db%num_pests to know how many pesticide records
    exist for the current object. That count controls the loop that scales each pesticide's
    surface-runoff and sediment-phase balances after the grassed-waterway removal is computed.
  channel_velocity_module: The grassed-waterway calculation depends on precomputed channel-geometry
    and bankfull hydraulic properties for the waterway reach. grwway_vel(j)%vel_bf, area,
    wid_btm, and celerity_bf are used to decide whether the flow is bankfull, to solve the
    flowing section, and to limit the computed velocity.
  output_ls_pesticide_module: The routine directly rescales pesticide balances for the current
    HRU and each pesticide constituent. hpestb_d stores the per-object pesticide load components
    that must be reduced according to runoff and sediment removal fractions.
---

<!-- facts:header -->

Computes daily pollutant and sediment reductions for a grassed waterway on the current HRU. It estimates flow hydraulics, sediment trapping, and then scales nutrients and pesticide loads by the resulting removal fractions.

## Bottom Line

This subroutine runs only when the current HRU has a grass waterway and surface runoff is present. It uses the HRU's grass-waterway settings, the current runoff depth, and channel-velocity parameters to estimate peak flow, waterway hydraulics, runoff removal, and sediment removal.

After computing those removals, it reduces sediment-associated constituents and pesticide loads for the HRU. It does not change the runoff water balance itself; instead it adjusts sediment, nutrient, and pesticide state variables so later routing and output reflect the waterway treatment.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls this routine during HRU pollutant-processing, after checking hru(j)%lumv%grwat_i == 1. The HRU state it uses is already populated by runoff and sediment generation, and the results feed the later HRU pollutant outputs and downstream routing because the routine reduces sediment, nutrient, and pesticide loads before the model continues.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and check for runoff | The routine copies ihru into j and exits immediately unless surfq(j) exceeds the runoff threshold of 0.001. |
| 2. Compute peak runoff rate | It converts daily runoff into a volumetric flow rate and uses tc_gwat(j) to estimate qp_cms as the day's peak runoff rate. |
| 3. Choose bankfull flow or solve for flow depth | If qp_cms exceeds the bankfull flow rate grwway_vel(j)%vel_bf, it uses bankfull area and depth; otherwise it increments rchdep in 1 cm steps, recomputes rcharea and hydraulic radius, and calls Qman until the discharge reaches qp_cms. |
| 4. Load incoming sediment | It copies the current HRU sediment yield into sedin so later calculations can treat the incoming load separately from the modified output state. |
| 5. Derive sheetflow treatment area and depth | It estimates the effective waterway side area from waterway depth and length, caps that area at 10 percent of HRU area, reduces it to 20 percent for nonuniform flow, then computes sf_depth and sf_sed. |
| 6. Compute runoff and sediment removal fractions | Using sf_depth and sf_sed, it computes surq_remove and sed_remove, clips both to 0-95, and falls back to zero removal if the effective area is zero. |
| 7. Compute sediment entering the channel | It converts the trapped-removal result to sedint, computes flow velocity vc from discharge and area, limits vc by grwway_vel(j)%celerity_bf, and if chflow_m3 is large enough calculates sediment concentration, transport capacity, and net deposition depnet. |
| 8. Derive sediment leaving the waterway | It subtracts deposition from the incoming sediment to get sedout, then converts that to a remaining sediment fraction sed_frac with bounds applied. |
| 9. Compute runoff fraction for non-sediment solutes | It turns the surface-runoff removal percentage into surq_frac, which is used for runoff-linked pesticide components. |
| 10. Scale sediment, nutrient, and solute pools | It computes sedtrap and scales sediment yield plus sediment-associated nutrient pools by sed_frac, while scaling surface-water phosphorus and nitrate pools by surq_frac. |
| 11. Remove trapped sediment from sediment classes | It subtracts sedtrap from lagyld first, then spills the remaining amount through sanyld, sagyld, silyld, and clayld, and clamps each pool to a nonnegative value. |
| 12. Scale pesticide loads | For each pesticide constituent in cs_db%num_pests, it reduces the surface-runoff balance by surq_frac and the sediment-phase balance by the sediment-removal fraction. |
| 13. Return to caller | If runoff existed, the routine finishes after updating the shared HRU and pesticide state variables; otherwise it returns without changes. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `surfq, hru, tc_gwat, sedyld, sedminpa, sedminps, sedorgp, surqsolp, sedorgn, surqno3, lagyld, sanyld, sagyld, silyld, clayld, ihru, qp_cms, sdti` | `hru(j)%lumv%grwat_d, hru(j)%lumv%grwat_s, hru(j)%lumv%grwat_l, hru(j)%lumv%grwat_spcon` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests` |
| [sym:channel_velocity_module] | `grwway_vel` | `grwway_vel(j)%vel_bf, grwway_vel(j)%area, grwway_vel(j)%wid_btm, grwway_vel(j)%celerity_bf` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(k)%surq, hpestb_d(j)%pest(k)%sed` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `qp_cms` | When surfq(j) > 0.001 and the routine enters the runoff-processing block, qp_cms is computed from chflow_m3 and tc_gwat(j). | qp_cms stores the day's estimated peak runoff rate for the active HRU. The routine uses it to decide whether the waterway is at bankfull flow or whether it must solve the hydraulic depth iteratively. |
| `sdti` | When surfq(j) > 0.001 and the code enters the iterative hydraulics branch, sdti is initialized to 0. and updated inside the Do While loop until it reaches qp_cms. | sdti holds the discharge returned by Qman for the current trial section. It tracks whether the trial waterway depth is sufficient to pass the target peak flow. |
| `sedyld(j)` | When surfq(j) > 0.001, sedyld(j) is reassigned after the runoff and sediment removal fractions are computed. | sedyld(j) is reduced to the sediment mass remaining after grassed-waterway trapping. That remaining load is what later routing and output stages see as the post-treatment sediment yield. |
| `sedminpa(j)` | When sedtrap is computed and then applied in the sediment-class depletion sequence, sedminpa(j) is multiplied by sed_frac. | sedminpa(j) is scaled down in proportion to the sediment that remains after treatment, so the mineral phosphorus attached to sediment follows the treated sediment load. |
| `sedminps(j)` | When sedtrap is computed and then applied in the sediment-class depletion sequence, sedminps(j) is multiplied by sed_frac. | sedminps(j) is scaled down with the remaining sediment fraction so that sediment-associated phosphorus pools are reduced consistently with sediment removal. |
| `sedorgp(j)` | When sedtrap is computed and then applied in the sediment-class depletion sequence, sedorgp(j) is multiplied by sed_frac. | sedorgp(j) is reduced along with the treated sediment load because this organic phosphorus pool is carried on sediment rather than remaining in surface runoff. |
| `surqsolp(j)` | When the runoff-removal fraction surq_frac has been computed, surqsolp(j) is multiplied by surq_frac. | surqsolp(j) is reduced only by the fraction of surface runoff that remains after the waterway removal step, preserving the runoff-linked solute balance. |
| `sedorgn(j)` | When sedtrap is computed and then applied in the sediment-class depletion sequence, sedorgn(j) is multiplied by sed_frac. | sedorgn(j) is reduced with the treated sediment fraction because the organic nitrogen pool is associated with sediment transport. |
| `surqno3(j)` | When surq_frac has been computed, surqno3(j) is multiplied by surq_frac. | surqno3(j) is reduced according to the runoff fraction that survives treatment, reflecting that nitrate in surface runoff is attenuated by the waterway's runoff removal. |
| `lagyld(j)` | When sedtrap is larger than the lagyld pool, the routine subtracts lagyld(j) to zero and carries the remainder into the next sediment class. | lagyld(j) is the first sediment class to be depleted by trapped sediment, so it is reduced before finer classes are adjusted. |
| `sanyld(j)` | When residual trapped sediment remains after lagyld(j) is exhausted, the remainder is applied to sanyld(j). | sanyld(j) is reduced by any trapped sediment that could not be removed from the lag sediment class. |
| `sagyld(j)` | When residual trapped sediment remains after sanyld(j) is exhausted, the remainder is applied to sagyld(j). | sagyld(j) is reduced by the leftover trapped sediment after the previous coarser classes have been depleted. |
| `silyld(j)` | When residual trapped sediment remains after sagyld(j) is exhausted, the remainder is applied to silyld(j). | silyld(j) is reduced by any trapped sediment still remaining after sand and aggregated sediment pools have been depleted. |
| `clayld(j)` | When residual trapped sediment remains after silyld(j) is exhausted, the remainder is applied to clayld(j). | clayld(j) is the final sediment class used to absorb any leftover trapped sediment, and it is then clamped to a nonnegative value. |
| `hpestb_d(j)%pest(k)%surq` | When surfq(j) > 0.001 and the do-loop over cs_db%num_pests runs, hpestb_d(j)%pest(k)%surq is rescaled by surq_frac. | hpestb_d(j)%pest(k)%surq stores the pesticide amount carried in surface runoff for constituent k, and it is reduced to match the runoff fraction that remains after the grassed-waterway treatment. |
| `hpestb_d(j)%pest(k)%sed` | When surfq(j) > 0.001 and the do-loop over cs_db%num_pests runs, hpestb_d(j)%pest(k)%sed is rescaled by 1. - sed_remove / 100. | hpestb_d(j)%pest(k)%sed stores the pesticide amount attached to sediment for constituent k, and it is reduced according to the sediment-removal percentage. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:5.2.1 | Sediment transport capacity in waterway | $Scap=Spcon*v^{1.5}$ | Verified against SWAT+ 62.0.0 (smp_grass_wway.f90). (Scap = Spcon*v^1.5) |
| 6:5.2.2 | Waterway runoff removal SolR | $SolR=75.8-10.8log(SD)+25.9log(SolK)$ | FLAG: theory uses 75.8-10.8*log(SD)+25.9*log(SolK) (two-term with soil K). Code uses simplified 95.6-10.79*Log(sf_depth) (single term, soil K dropped). Comment at line 122 explicitly notes this is a simpler form from vfsmod simulations (White and Arnold 2008 pending). |
| 6:5.2.3 | Waterway sediment removal SedR | $SedR=79.0-1.04(SedL)+0.213*(SolR)$ | sed_remove=79.0-1.04*sf_sed+0.213*surq_remove; structurally matches SedR=79.0-1.04*SedL+0.213*SolR, but surq_remove inherits the simplified formula from 6:5.2.2 (no soil K term). |

## Lineage

Resolved lineage shows four source changes. The 2024-05-30 import added the procedure from upstream Bitbucket with the current grass-waterway control logic. The 2024-08-08 and 2024-10-08 changes mainly initialized local variables to zero and cleaned spacing/tabs in the specification comments and declarations. The 2024-12-31 change declared qman as external, and the 2025-02-03 change only corrected a typo in a comment.

- 94b6dec added the initial smp_grass_wway implementation, including the runoff threshold, hydraulic iteration, removal equations, and pollutant scaling logic.
- 39fabde initialized the local working variables to zero, changing the routine's default startup state from uninitialized locals to deterministic values.
- f1e61a3 and 889136d were non-behavioral cleanup changes to comments and formatting, with no algorithmic effect.
- bd18ad4 changed qman from a plain local real to an external procedure declaration, making the Manning helper callable as a function.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'smp_grass_wway' has no extracted documentation comment.
