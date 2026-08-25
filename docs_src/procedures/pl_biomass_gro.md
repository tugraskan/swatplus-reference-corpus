---
kind: procedure
symbol: pl_biomass_gro
title: pl_biomass_gro
status: filled
source_hash: 97147b036222b259
version_label: SWAT+ 62.0.0
locals:
  j: Local HRU index used to point into the current hydrologic response unit and its associated
    plant, climate, output, and connectivity state. It is set from ihru and then reused to
    read and update j-indexed module arrays.
  ruedecl: Temporary vapor-pressure-deficit decline amount. It is set to vpd - 1.0 when vpd
    exceeds the threshold and used to reduce radiation-use efficiency.
  beadj: Adjusted radiation-use efficiency for the active plant on the current day. It starts
    from the plant’s baseline or CO2-adjusted value, is reduced by VPD if needed, and is multiplied
    by intercepted radiation to get bioday.
  rto: Declared as a growth-age ratio for perennial plants, but in this routine it is only
    initialized to 1. and not used in the executed calculations.
  idp: Plant database index for the active plant species or cultivar. It is derived from the
    current plant community status and used to retrieve plant-specific coefficients such as
    ruc2, bio_e, wavp, pltnfr3, and pltpfr3.
  iob: Object-connectivity index used to reach the weather-station assignment for the current
    HRU. It is set from hru(j)%obj_no and then used to look up the HRU-linked weather station.
  iwgn: Weather-generator station index extracted from the selected weather station. It is
    read from wst(iwst)%wco%wgn, but the commented day-length logic shows it is not used in
    the active calculations here.
uses:
  plant_data_module: This module supplies the plant-specific parameters that control biomass
    efficiency and stress response for the active plant. The routine uses plcp(idp)%ruc2 for
    the CO2 response curve and pldb(idp)%bio_e and pldb(idp)%wavp as the baseline efficiency
    and VPD decline rate.
  basin_module: This module provides basin-wide controls that alter how biomass is computed.
    bsn_prm%co2 switches the CO2 response branch, and bsn_cc%nostress and bsn_cc%cswat control
    whether stress factors are forced off and whether plant carbon gain is accumulated.
  hru_module: This module holds the current HRU context and shared plant-growth vectors that
    this routine reads and updates. hru(j)%obj_no links the HRU to its object/weather station,
    while the shared arrays and scalars such as uno3d, uapd, bioday, rto_no3, and rto_solp
    are the daily plant uptake and growth intermediates used by the plant-growth workflow.
  plant_module: This module stores the current plant community, plant status, and plant stress
    factors. pl_biomass_gro reads pcom(j)%plcur(ipl)%idplt and phuacc to identify the active
    plant and growth stage, then updates the plant stress factors and their running sums in
    pcom(j)%plstr(ipl).
  carbon_module: This module stores daily plant carbon gains. When the basin carbon option
    is active, the routine adds the day’s biomass carbon increment to hpc_d(j)%npp_c so the
    carbon accounting stays aligned with biomass growth.
  organic_mineral_mass_module: This module holds the compact daily biomass-and-carbon increment
    summary. The routine writes pl_mass_up%m and pl_mass_up%c so downstream plant growth and
    accounting routines can use the day’s actual biomass production.
  climate_module: This module provides the weather-station table needed to reach the weather
    generator index tied to the current HRU. The routine reads wst(iwst)%wco%wgn when establishing
    the current station context, even though the day-length adjustment is commented out.
  hydrograph_module: This module maps the current HRU or object to its assigned weather station.
    The routine uses ob(j)%wst and ob(iob)%wst to find the weather-station index associated
    with the current HRU/object context.
  constituent_mass_module: This module reports how many salt ions and other constituents are
    simulated. The routine checks cs_db%num_salts and cs_db%num_cs before calling salt_uptake
    and cs_uptake so those paths only run when the relevant constituents exist.
  salt_module: This module contains the switch that turns salt-uptake simulation on or off.
    The routine requires salt_uptake_on to be enabled before it calls salt_uptake.
  salt_data_module: This module contains the control that determines how salinity stress is
    combined with other stresses. The routine uses salt_effect to choose whether salt stress
    is applied after the other stress factors or included with them in the minimum reduction.
  output_landscape_module: This module stores plant-weather output accumulators. The routine
    adds daily biomass and carbon growth to hpw_d(j)%bm_grow and hpw_d(j)%c_gro for later
    reporting.
---

<!-- facts:header -->

Computes daily potential biomass growth for the active plant in the current HRU, then reduces that growth by plant stresses and records biomass/carbon gain totals.

## Bottom Line

pl_biomass_gro calculates the day’s potential biomass gain for the current HRU plant from intercepted radiation, then adjusts that gain for CO2, vapor-pressure deficit, temperature, nutrient, water, air, and salt effects. It updates the plant stress summary state and the landscape output accumulators for biomass and carbon growth.

The routine only runs while the plant is still in the growth phase before full heat-unit maturity. It also invokes the separate temperature, nitrogen, phosphorus, salt, and constituent-uptake routines so the stress factors and uptake state used by later growth routines are current for the day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

pl_biomass_gro runs inside the daily plant-growth sequence after pl_grow has established that the plant is growing and not dormant. pl_grow sets the current HRU/plant context before calling it, and the results feed the later growth routines and daily output accounting that depend on updated biomass, stress, and carbon-growth state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve the current HRU, plant, and weather-station context. | The routine copies ihru into j, gets the current plant ID from pcom(j)%plcur(ipl)%idplt, resolves the object-linked weather station through ob(j)%wst, and reads the weather-generator index from wst(iwst)%wco%wgn. |
| 2. Exit early for plants that have reached maturity. | All biomass-growth work is skipped unless the current plant has phuacc <= 1.0; otherwise the routine returns immediately. |
| 3. Compute the baseline radiation-use efficiency. | The routine sets beadj from either the basin CO2 response curve using co2y(time%yrs), plcp(idp)%ruc1, and plcp(idp)%ruc2, or the plant’s baseline bio_e when basin CO2 is not above 350 ppm. |
| 4. Reduce radiation-use efficiency for vapor-pressure deficit when needed. | If vpd exceeds 1.0, the routine computes ruedecl, subtracts pldb(idp)%wavp * ruedecl from beadj, and floors the result at 0.27 * pldb(idp)%bio_e. |
| 5. Compute daily potential biomass production. | The routine resets iob from hru(j)%obj_no, reloads iwst from ob(iob)%wst, multiplies beadj by par(ipl) to get bioday, and forces bioday to zero if the product is negative. |
| 6. Update temperature stress and plant nutrient-demand ratios. | The routine calls pl_tstr, computes rto_no3 and rto_solp from the current uptake totals when the totals exceed the summed demand, caps uno3d(ipl) and uapd(ipl) by plant-specific daily limits based on bioday, then calls pl_nup and pl_pup. |
| 7. Trigger salt and other constituent uptake when simulated. | If salts are simulated and salt uptake is enabled, the routine calls salt_uptake; if other constituents are simulated, it calls cs_uptake. |
| 8. Optionally disable selected plant stresses. | When bsn_cc%nostress equals 1, the routine sets the water, temperature, nitrogen, phosphorus, air, and salt stress factors to 1.0. When bsn_cc%nostress equals 2, it sets only nitrogen and phosphorus stress to 1.0. |
| 9. Combine the active stress factors into the growth regulator. | The routine computes pcom(j)%plstr(ipl)%reg as the minimum of the active stress factors, either with salt stress applied after the other stresses when salt_effect == 1 or with salt stress included directly in the minimum otherwise, then constrains reg to the 0..1 range. |
| 10. Convert potential biomass to actual biomass and carbon growth. | The routine multiplies bioday by reg to get pl_mass_up%m, converts it to carbon as 0.42 * pl_mass_up%m, adds both amounts to the HRU-level biomass/carbon output accumulators, and adds carbon growth to hpc_d(j)%npp_c when basin carbon simulation is active. |
| 11. Accumulate daily stress summaries. | The routine adds one minus each stress factor into the running sums for water, temperature, nitrogen, phosphorus, and air stress. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `plcp, pldb` | `plcp(idp)%ruc2, pldb(idp)%bio_e, pldb(idp)%wavp` |
| [sym:basin_module] | `bsn_prm, bsn_cc` | `bsn_prm%co2, bsn_cc%nostress, bsn_cc%cswat` |
| [sym:hru_module] | `hru, par, uno3d, uapd, bioday, ihru, ipl, rto_no3, rto_solp, sum_no3, sum_solp, uapd_tot, uno3d_tot, vpd` | `hru(j)%obj_no` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plstr(ipl)%strsw, pcom(j)%plstr(ipl)%strst, pcom(j)%plstr(ipl)%strsn, pcom(j)%plstr(ipl)%strsp, pcom(j)%plstr(ipl)%strsa, pcom(j)%plstr(ipl)%strss, pcom(j)%plstr(ipl)%reg, pcom(j)%plstr(ipl)%sum_w, pcom(j)%plstr(ipl)%sum_tmp, pcom(j)%plstr(ipl)%sum_n, pcom(j)%plstr(ipl)%sum_p, pcom(j)%plstr(ipl)%sum_a` |
| [sym:carbon_module] | `hpc_d` | `hpc_d(j)%npp_c` |
| [sym:organic_mineral_mass_module] | `pl_mass_up` | `pl_mass_up%m, pl_mass_up%c` |
| [sym:climate_module] | `wst` | `wst(iwst)%wco%wgn` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(j)%wst, ob(iob)%wst` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts, cs_db%num_cs` |
| [sym:salt_module] | `salt_uptake_on` |  |
| [sym:salt_data_module] | `salt_effect` |  |
| [sym:output_landscape_module] | `hpw_d` | `hpw_d(j)%bm_grow, hpw_d(j)%c_gro` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | After the routine enters the maturity gate, iwst is first set from ob(j)%wst and then reset again from ob(iob)%wst after iob = hru(j)%obj_no. | iwst carries the weather-station index for the current HRU/object context so later calculations can reference the correct station mapping; the second assignment rebinds it through the HRU’s object connectivity. |
| `bioday` | Only when pcom(j)%plcur(ipl)%phuacc <= 1.0. | bioday is computed as the day’s potential biomass production from adjusted radiation-use efficiency times intercepted radiation, and it is zeroed if the raw product is negative. |
| `rto_no3` | Only while the plant is still in the growth branch and after the daily uptake totals are compared to sum_no3. | rto_no3 is set to the active plant’s share of total daily nitrate uptake demand when demand totals are positive enough to compare; otherwise it is set to 1.0 as a neutral ratio. |
| `rto_solp` | Only while the plant is still in the growth branch and after the daily uptake totals are compared to sum_solp. | rto_solp is set to the active plant’s share of total daily soluble phosphorus uptake demand when demand totals are positive enough to compare; otherwise it is set to 1.0 as a neutral ratio. |
| `uno3d(ipl)` | Before pl_nup is called, after the routine limits daily nitrate demand with 4. * pldb(idp)%pltnfr3 * bioday. | uno3d(ipl) is reduced to the smaller of the plant-specific nitrate demand limit and its current value, so the nitrogen-uptake routine works with a capped daily demand. |
| `uapd(ipl)` | Before pl_pup is called, but only when uapd(ipl) is greater than 10. | uapd(ipl) is reduced to the smaller of the plant-specific phosphorus demand limit and its current value, so the phosphorus-uptake routine works with a capped daily demand. |
| `pcom(j)%plstr(ipl)%strsw` | When bsn_cc%nostress == 1. | The water-stress factor is forced to 1.0, removing water limitation from the growth calculation for this day. |
| `pcom(j)%plstr(ipl)%strst` | When bsn_cc%nostress == 1. | The temperature-stress factor is forced to 1.0, removing temperature limitation from the growth calculation for this day. |
| `pcom(j)%plstr(ipl)%strsn` | When bsn_cc%nostress == 1 or bsn_cc%nostress == 2. | The nitrogen-stress factor is forced to 1.0 so nitrogen limitation does not reduce growth on that day. |
| `pcom(j)%plstr(ipl)%strsp` | When bsn_cc%nostress == 1 or bsn_cc%nostress == 2. | The phosphorus-stress factor is forced to 1.0 so phosphorus limitation does not reduce growth on that day. |
| `pcom(j)%plstr(ipl)%strsa` | When bsn_cc%nostress == 1. | The air-stress factor is forced to 1.0, removing air-stress limitation from the growth calculation for this day. |
| `pcom(j)%plstr(ipl)%strss` | When bsn_cc%nostress == 1. | The salt-stress factor is forced to 1.0, removing salt limitation from the growth calculation for this day. |
| `pcom(j)%plstr(ipl)%reg` | After the active stress factors are combined and, if needed, after salt stress is applied separately. | reg is set to the limiting growth factor for the current day and then constrained to the 0..1 range so it can scale potential biomass into actual biomass. |
| `pl_mass_up%m` | After reg has been computed and bioday is available. | pl_mass_up%m stores the day’s actual biomass increment, equal to bioday multiplied by the combined growth regulator. |
| `pl_mass_up%c` | Immediately after pl_mass_up%m is computed. | pl_mass_up%c stores the corresponding carbon increment as 0.42 times the biomass increment. |
| `hpw_d(j)%bm_grow` | After actual biomass is computed for the day. | hpw_d(j)%bm_grow accumulates the HRU’s daily plant biomass growth for output reporting. |
| `hpw_d(j)%c_gro` | After actual biomass is computed for the day. | hpw_d(j)%c_gro accumulates the HRU’s daily plant carbon growth for output reporting. |
| `hpc_d(j)%npp_c` | When bsn_cc%cswat == 2. | hpc_d(j)%npp_c is incremented by the day’s plant carbon growth so the carbon-balance output reflects biomass production under the dynamic carbon option. |
| `pcom(j)%plstr(ipl)%sum_w` | After the growth regulator has been set and the routine reaches the stress summary block. | sum_w accumulates the day-by-day water-stress complement, tracking cumulative water limitation over time. |
| `pcom(j)%plstr(ipl)%sum_tmp` | After the growth regulator has been set and the routine reaches the stress summary block. | sum_tmp accumulates the day-by-day temperature-stress complement, tracking cumulative temperature limitation over time. |
| `pcom(j)%plstr(ipl)%sum_n` | After the growth regulator has been set and the routine reaches the stress summary block. | sum_n accumulates the day-by-day nitrogen-stress complement, tracking cumulative nitrogen limitation over time. |
| `pcom(j)%plstr(ipl)%sum_p` | After the growth regulator has been set and the routine reaches the stress summary block. | sum_p accumulates the day-by-day phosphorus-stress complement, tracking cumulative phosphorus limitation over time. |
| `pcom(j)%plstr(ipl)%sum_a` | After the growth regulator has been set and the routine reaches the stress summary block. | sum_a accumulates the day-by-day air-stress complement, tracking cumulative air limitation over time. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.1.2 | Daily biomass increment | $\Delta bio=RUE*H_{phosyn}$ | Daily biomass is bioday = beadj*par after CO2 and VPD adjustments to radiation-use efficiency. |
| 5:2.1.4 | Radiation-use efficiency response to CO2 | $RUE=\frac{100*CO_2}{CO_2+exp(r_1-r_2*CO_2)}$ | Verified against SWAT+ 62.0.0 (pl_biomass_gro.f90:44). beadj = 100.*co2/(co2+Exp(ruc1-co2*ruc2))` — RUE·CO2 |
| 5:2.1.7 | RUE reduction above vapor-pressure threshold | $RUE=RUE_{vpd=1}-\Delta rue_{dcl}*(vpd-vpd_{thr})$ | For vpd > 1.0, beadj is reduced by wavp*(vpd-1.0) and floored at 0.27*bio_e. The threshold form matches, but the floor is an extra code constraint. |
| 5:2.1.8 | RUE at or below vapor-pressure threshold | $RUE=RUE_{vpd=1}$ | When vpd <= 1.0, no decline term is applied and beadj remains at the CO2-adjusted RUE value. |
| 5:3.2.1 | Actual biomass growth | $\Delta bio_{act}=\Delta bio*\gamma_{reg}$ | Actual daily biomass is pl_mass_up = bioday*reg, where reg is the minimum of the stored growth factors rather than the printed 1-max(stress) form. |
| 5:3.2.3 | Combined growth-regulating factor | $\gamma_{reg}=1-max(wstrs,tstrs,nstrs,pstrs)$ | reg = min(strsw, strst, strsn, strsp, strsa[, strss]). Because these stored variables are growth factors, this is the code-side counterpart to the printed stress-complement formulation. |
| 5:3.2.4 | Biomass override toward target biomass | $\Delta bio_{act} = \Delta bio_i*\frac{(bio_{trg}-bio_{i-1})}{bio_{trg}}$ | No explicit bio_trg override term is applied in the biomass-growth routine. |

## Lineage

`pl_biomass_gro.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 11 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_biomass_gro.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `3389f29` (2026-04-22) — Numerous changes to account for the removal of the old cswat ==1 and moving cswat == 3 to cswat =1. Also some code formatting changes to get…
- `cb5de88` (2026-02-25) — changes made to run a cswat == 3 option and added a new subroutine named mgt_newtill_mix_3.f90
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_biomass_gro' has no extracted documentation comment.
- source uncertainty: the routine reads iwst from ob(j)%wst and later resets iwst from ob(iob)%wst after iob = hru(j)%obj_no; the first assignment is immediately overwritten in the active branch.
- source uncertainty: rto is declared and set to 1. but is not used in the executed logic shown in this source span.
- algorithm_steps revised: split the draft into 11 source-backed steps and anchored each step to visible line ranges from pl_biomass_gro.f90.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
