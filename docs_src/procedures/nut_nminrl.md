---
kind: procedure
symbol: nut_nminrl
title: nut_nminrl
status: filled
source_hash: 1ee76375fbe40849
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; used to select the current hydrologic response unit and
    its associated soil, plant, septic, and output records.
  k: Soil-layer loop counter for the current HRU; drives layer-by-layer mineralization and
    denitrification updates.
  kk: Helper layer index used for climate-driven factors; the first soil layer uses layer
    2 conditions, otherwise it uses the current layer.
  idp: Plant database index taken from the current plant community’s `plcur(ipl)%idplt`; used
    to look up the residue decomposition coefficient for that plant.
  rmn1: Temporary residue nitrogen transfer amount, carried as the amount decomposed from
    fresh organic material before it is split into nitrate and active organic pools.
  rmp: Temporary residue phosphorus transfer amount, carried as the amount decomposed from
    fresh organic material before it is split into labile and stable organic pools.
  xx: Scratch value for intermediate calculations, including the soil water/temperature factor
    blend and the humus P partition denominator.
  csf: Combined moisture-temperature stress factor used to scale humus mineralization and
    residue decomposition.
  rwn: Net transfer between active and stable humus nitrogen pools; positive values move N
    from active to stable, negative values move N the other way.
  hmn: Humus mineralized nitrogen from the active pool to nitrate for the current layer.
  hmp: Humus mineralized phosphorus from organic/stable humus to the labile mineral P pool
    for the current layer.
  cnr: Carbon-to-nitrogen ratio of current plant residue, used to evaluate residue quality.
  cnrf: Residue quality factor derived from `cnr`; lower values suppress decomposition when
    residue C:N is high.
  cpr: Carbon-to-phosphorus ratio of current plant residue, used to evaluate residue quality
    for phosphorus cycling.
  cprf: Residue quality factor derived from `cpr`; lower values suppress decomposition when
    residue C:P is high.
  ca: Nutrient cycling factor for residue decomposition, chosen as the minimum of the C:N
    and C:P response factors and capped at 1.
  decr: Daily decomposition fraction for the current plant residue in the current soil layer.
  wdn: Denitrification loss from soil nitrate in the current layer, computed after residue
    and humus transformations.
  cdg: Soil temperature response factor derived from layer temperature and used in the combined
    stress factor.
  sut: Soil water response factor derived from water storage relative to field capacity and
    used in the combined stress factor.
uses:
  septic_data_module: The septic-system array is checked so denitrification is skipped for
    the septic-affected layer when the septic option is active. That prevents the routine
    from removing nitrate in a layer where septic behavior should override the normal denitrification
    calculation.
  basin_module: The basin parameters provide global thresholds and coefficients that control
    residue breakdown and denitrification behavior. `bsn_prm%decr_min` limits how small residue
    decay can be, while `bsn_prm%sdnco` and `bsn_prm%cdn` control when and how strongly nitrate
    is lost to denitrification.
  organic_mineral_mass_module: These soil-profile mass pools are the direct storage locations
    for the organic and mineral material this routine redistributes. The subroutine moves
    nitrogen and phosphorus among active humus, stable humus, mineral nitrate, labile phosphorus,
    residues, and the temporary `decomp` mass.
  hru_module: The HRU structure supplies the current unit’s nutrient parameter `cmn`, the
    active HRU index, the plant-competition indices, and the septic index. Those values determine
    the mineralization rate, which HRU is updated, which plant residue is processed, and whether
    denitrification is suppressed.
  soil_module: The soil profile provides the layer count and the temperature and field-capacity
    values used to compute mineralization stress factors. Those layer properties determine
    whether the layer is warm enough for mineralization and how strongly moisture limits the
    reaction.
  plant_module: The plant community determines how many plant residue pools exist in the HRU
    and which residue entry is active for each plant. The routine loops over `npl` and uses
    `plcur(ipl)%idplt` to match each residue pool to its plant-specific decomposition coefficient.
  plant_data_module: The plant database supplies `rsdco_pl`, the residue decomposition coefficient
    for the current plant type. That coefficient scales the daily residue decay fraction before
    the residue mass is split into nitrate, active organic, labile P, and stable organic P.
  output_landscape_module: The landscape nutrient-balance output records accumulate the layer-by-layer
    transfers computed here. These fields matter because they summarize how much N and P moved
    among pools or left the layer through denitrification during the current day.
---

<!-- facts:header -->

Computes daily soil nitrogen and phosphorus mineralization, immobilization, and denitrification for an HRU. It updates humus, mineral, and residue pools while accumulating nutrient-balance outputs.

## Bottom Line

This routine runs once per HRU during HRU control to translate temperature, soil water, residue quality, and plant-specific residue decomposition rates into daily nutrient transfers. It handles both humus turnover and fresh residue decomposition, with separate accounting for nitrogen and phosphorus.

It matters because the updated soil and residue pools feed the rest of the day’s nutrient cycling, including nitrate availability, labile phosphorus, denitrification loss, and the nutrient-balance diagnostics stored in `hnb_d`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `hru_control` after surface residue decomposition has been handled, within the daily HRU update when `bsn_cc%cswat == 0`. Its results feed the day’s soil nutrient state, especially mineral nitrate, labile phosphorus, humus pools, and the HRU nutrient-balance outputs used later in reporting and downstream nutrient processes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize per-HRU output accumulators and select the current HRU. | Copies `ihru` into `j` and zeros the HRU-level nutrient-balance totals so the routine can accumulate daily layer contributions for active-to-stable N transfer, humus mineralization, residue mineralization, and denitrification. |
| 2. Loop through each soil layer in the HRU and choose the climate reference layer. | Iterates over `soil(j)%nly` layers and uses layer 2 for temperature/water factors when processing the top layer, otherwise it uses the current layer’s physical properties. |
| 3. Compute moisture, temperature, and combined stress factors when the layer is warm enough. | If layer temperature is above freezing, the routine calculates a soil-water factor from storage relative to field capacity, a temperature factor from the logistic response, and a combined factor `csf` as the square root of their product after bounding it. |
| 4. Move nitrogen between active and stable humus pools. | Computes the daily active-to-stable humus transfer `rwn`, caps it so it cannot exceed available pool mass, updates `soil1(j)%hsta(k)%n` and `soil1(j)%hact(k)%n`, and records the signed transfer in `hnb_d(j)%act_sta_n`. |
| 5. Mineralize active humus nitrogen and partition associated phosphorus. | Uses `hru(j)%nut%cmn`, `csf`, and active humus N to compute `hmn`, limits it to the active pool, then derives `hmp` from the stable-plus-active humus N ratio. It transfers `hmn` to `soil1(j)%mn(k)%no3`, transfers `hmp` to `soil1(j)%mp(k)%lab`, and accumulates both in `hnb_d`. |
| 6. Process fresh residue decomposition separately for each plant in the community. | Loops over `pcom(j)%npl`, computes residue quality ratios from the plant residue pools, looks up the plant-specific residue coefficient from `pldb(idp)%rsdco_pl`, forms the daily decay fraction `decr`, and subtracts the resulting `decomp` mass from `soil1(j)%pl(ipl)%rsd(k)`. |
| 7. Partition decomposed residue into mineral and organic end products. | After subtracting residue mass, sends 80% of residue N to `soil1(j)%mn(k)%no3`, 20% to `soil1(j)%hact(k)%n`, 80% of residue P to `soil1(j)%mp(k)%lab`, and 20% to `soil1(j)%hsta(k)%p`. |
| 8. Compute denitrification when the layer is not septic-controlled. | If the current layer is not the active septic layer or the septic option is off, the routine applies a water-threshold test and, when satisfied, removes a fraction of nitrate using temperature, water, and carbon-based controls. The loss is stored in `hnb_d(j)%denit`. |
| 9. Finish the layer and HRU update. | Ends the warm-layer block, completes the layer loop, and returns with the soil and output-state arrays updated for the day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `sep` |  |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%decr_min, bsn_prm%sdnco, bsn_prm%cdn` |
| [sym:organic_mineral_mass_module] | `soil1, decomp` | `soil1(j)%hact(k)%n, soil1(j)%hsta(k)%n, soil1(j)%hsta(k)%p, soil1(j)%mn(k)%no3, soil1(j)%mp(k)%lab, soil1(j)%pl(ipl)%rsd(k)%n, soil1(j)%pl(ipl)%rsd(k)%c, soil1(j)%pl(ipl)%rsd(k)%p, soil1(j)%pl(ipl)%rsd(k), soil1(j)%pl(ipl)%rsd(k)%m, decomp%n, decomp%p, soil1(j)%cbn(k)` |
| [sym:hru_module] | `hru, i_sep, ihru, isep, ipl` | `hru(j)%nut%cmn` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(kk)%tmp, soil(j)%phys(kk)%fc` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%rsdco_pl` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%act_nit_n, hnb_d(j)%org_lab_p, hnb_d(j)%act_sta_n, hnb_d(j)%denit, hnb_d(j)%rsd_nitorg_n, hnb_d(j)%rsd_laborg_p` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%act_nit_n` | On every layer where `soil(j)%phys(kk)%tmp > 0.` | Accumulates the amount of nitrogen mineralized from active humus into nitrate for the current HRU and day. |
| `hnb_d(j)%org_lab_p` | On every layer where `soil(j)%phys(kk)%tmp > 0.` | Accumulates the phosphorus mineralized from organic humus into the labile phosphorus pool. |
| `hnb_d(j)%act_sta_n` | When the active-to-stable humus transfer `rwn` is computed in a warm layer | Records the net daily nitrogen moved between active and stable humus pools, including the direction of transfer. |
| `hnb_d(j)%denit` | When denitrification is allowed by the septic check and the soil-water threshold test passes | Accumulates nitrate lost to denitrification from the current HRU layer. |
| `hnb_d(j)%rsd_nitorg_n` | For each plant residue pool processed in a warm layer | Summarizes the nitrogen transfer from fresh residue into nitrate and active organic pools after residue decomposition. |
| `hnb_d(j)%rsd_laborg_p` | For each plant residue pool processed in a warm layer | Summarizes the phosphorus transfer from fresh residue into labile and stable organic pools after residue decomposition. |
| `soil1(j)%hsta(k)%n` | When humus N is redistributed in a warm layer | Receives nitrogen from or gives nitrogen to the active humus pool as the routine maintains the target active fraction. |
| `soil1(j)%hact(k)%n` | When humus N is redistributed in a warm layer | Loses nitrogen to stable humus and to nitrate during humus mineralization, then gains nitrogen from decomposed residue. |
| `soil1(j)%mn(k)%no3` | When humus and residue mineralization affect mineral N | Increases by humus mineralized N and by 80% of decomposed residue N, then decreases by denitrification when that process is active. |
| `soil1(j)%hsta(k)%p` | When humus mineralization partitions P | Loses P to the labile mineral pool during humus mineralization and then gains 20% of decomposed residue P. |
| `soil1(j)%mp(k)%lab` | When decomposed residue P is partitioned | Gains labile phosphorus from humus mineralization and from 80% of decomposed residue P. |
| `decomp` | For each warm soil layer | Stores the temporary residue mass removed from the current plant residue pool so the N and P portions can be distributed to mineral and organic pools. |
| `soil1(j)%pl(ipl)%rsd(k)` | For each plant residue pool in a warm layer before and after the decay subtraction | Loses residue mass according to the decomposition fraction `decr`, with tiny remaining masses forced to zero to avoid underflow. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:1.2.1 | Soil temperature factor gamma_tmp | $\gamma_{tmp,ly}=0.9*\frac{T_{soil,ly}}{T_{soil,ly}+exp[9.93-0.312*T_{soil,ly}]}+0.1$ | cdg=0.9*T/(T+exp(9.93-0.312*T))+0.1; exact match. cbn_rsd_decomp:87 is the CENTURY-path duplicate. |
| 3:1.2.2 | Soil water factor gamma_sw | $\gamma_{sw,ly}=\frac{SW_{ly}}{FC_{ly}}$ | sut=0.1+0.9*sqrt(SW/FC); theory gives SW/FC directly; code uses scaled sqrt form. Combined csf=sqrt(cdg*sut). |
| 3:1.2.3 | Active-to-stable N transfer rate | $N_{trns,ly}=\beta_{trns}*orgN_{act,ly}*(\frac{1}{fr_{actN}}-1)-orgN_{sta,ly}$ | rwn=1e-4*(hact_n*(1/nactfr-1)-hsta_n); exact match for N_trns=beta_trns*orgN_act*(1/fr_actN-1)-orgN_sta with beta_trns=1e-4, nactfr=0.02. |
| 3:1.2.4 | Humus N mineralization (active pool) | $N_{mina,ly}=\beta_{min}*(\gamma_{tmp,ly}*\gamma_{sw,ly})^{1/2}*orgN_{act,ly}$ | hmn=hru%nut%cmn*csf*hact_n; exact match for N_mina=beta_min*(gamma_tmp*gamma_sw)^0.5*orgN_act (cmn=beta_min, csf=combined factor). |
| 3:1.2.5 | C:N ratio of fresh organic material | $\varepsilon _{C:N}=\frac{0.58*rsd_{ly}}{orgN_{frsh,ly}+NO3_{ly}}$ | cnr=rsd%c/rsd%n; implements epsilon_CN=0.58*rsd/(orgN_frsh+NO3) in simplified form (C stored as 0.58*OM). |
| 3:1.2.6 | C:P ratio of fresh organic material | $\varepsilon_{C:P}=\frac{0.58*rsd_{ly}}{orgP_{frsh,ly}+P_{solution,ly}}$ | cpr=rsd%c/rsd%p; analogous to epsilon_CP. |
| 3:1.2.7 | Residue decomposition rate delta_ntr | $\delta_{ntr,ly}=\beta_{rsd}*\gamma_{ntr,ly}*(\gamma_{tmp,ly}*\gamma_{sw,ly})^{1/2}$ | decr=rsdco_pl*ca*csf; matches delta_ntr=beta_rsd*gamma_ntr*(gamma_tmp*gamma_sw)^0.5. |
| 3:1.2.8 | Nutrient cycling factor gamma_ntr | $\gamma_{ntr,ly}=min[{exp[-0.693*\frac{(\varepsilon_{C:N}-25)}{25}] ,exp[-0.693*\frac{(\varepsilon_{C:P}-200)}{200}] , 1.0}]$ | cnrf=exp(-0.693*(cnr-25)/25); cprf=exp(-0.693*(cpr-200)/200); ca=min(cnrf,cprf,1). Exact match. |
| 3:1.2.9 | N mineralized from fresh organic (80% to NO3) | $N_{minf,ly}=0.8*\delta_{ntr,ly}*orgN_{frsh,ly}$ | mn(k)%no3+=0.8*decomp%n; exact match for N_minf=0.8*delta_ntr*orgN_frsh. |
| 3:1.2.10 | N moving to active organic pool (20%) | $N_{dec,ly}=0.2*\delta_{ntr,ly}*orgN_{frsh,ly}$ | hact(k)%n+=0.2*decomp%n; exact match for N_dec=0.2*delta_ntr*orgN_frsh. |
| 3:2.2.1 | Soil temperature factor gamma_tmp (P path) | $\gamma_{tmp,ly}=0.9*\frac{T_{soil,ly}}{T_{soil,ly}+exp[9.93-0.312*T_{soil,ly}]}+0.1$ | Same temperature factor as 3:1.2.1; shared code path. |
| 3:2.2.2 | Soil water factor gamma_sw (P path) | $\gamma_{sw,ly}=\frac{SW_{ly}}{FC_{ly}}$ | Same as 3:1.2.2; shared code path. |
| 3:2.2.3 | Active organic P proportional to active organic N | $orgP_{act,ly}=orgP_{hum,ly}*\frac{orgN_{act,ly}}{orgN_{act,ly}+orgN_{sta,ly}}$ | hmp=1.4*hmn*hsta_p/(hact_n+hsta_n); orgP_act/orgP_hum ratio implicit via N pool ratio. |
| 3:2.2.4 | Stable organic P proportional to stable organic N | $orgP_{sta,ly}=orgP_{hum,ly}*\frac{orgN_{sta,ly}}{orgN_{act,ly}+orgN_{sta,ly}}$ | Same denominator as 3:2.2.3; orgP_sta is implicit complement. |
| 3:2.2.5 | Humus P mineralization | $P_{mina,ly}=1.4*\beta_{min}*(\gamma_{tmp,ly}*\gamma_{sw,ly})^{1/2}*orgP_{act,ly}$ | Verified against SWAT+ 62.0.0 (nut_nminrl.f90:123). (1.4 humus-P mineralization) |
| 3:2.2.6 | C:N ratio for P-path residue decomp | $\varepsilon_{C:N}=\frac{0.58*rsd_{ly}}{orgN_{frsh,ly}+NO3_{ly}}$ | Verified against SWAT+ 62.0.0 (nut_nminrl.f90:142). cnr = rsd%c/rsd%n` — code tracks residue C directly, not 0.58·mass |
| 3:2.2.7 | C:P ratio for P-path residue decomp | $\varepsilon_{C:P}=\frac{0.58*rsd_{ly}}{orgP_{frsh,ly}+P_{solution,ly}}$ | Verified against SWAT+ 62.0.0 (nut_nminrl.f90:150). cpr = rsd%c/rsd%p |
| 3:2.2.8 | Decomposition rate delta_ntr (P path) | $\delta_{ntr,ly}=\beta_{rsd}*\gamma_{ntr,ly}*(\gamma_{tmp,ly}*\gamma_{sw,ly})^{1/2}$ | Same decr as 3:1.2.7; shared code path. |
| 3:2.2.9 | Nutrient cycling factor gamma_ntr (P path) | $\gamma_{ntr,ly}=min[exp[0.693*\frac{\varepsilon_{C:N}-25}{25}],exp[-0.693*\frac{(\varepsilon_{C:P}-200}{200}],1.0]$ | Same ca as 3:1.2.8; both N and P use same nutrient cycling factor. |

## Lineage

Four resolved commits changed `nut_nminrl`. The 2024-12-05 refactor switched the routine from the older `rsd` residue structure to `soil1`-based plant residues, removed the direct use of `rsdco_plcom` from `hru_module`, and added the residue decomposition and denitrification bookkeeping fields in `hnb_d`. The 2025-02-06 change moved the humus mineralization coefficient from `bsn_prm%cmn` to `hru(j)%nut%cmn`. The 2026-01-07 update made residue decomposition plant-specific by looping over `pcom(j)%npl`, using `pcom(j)%plcur(ipl)%idplt` with `pldb(idp)%rsdco_pl`, and it also retained the new `decomp` temporary and residue-zeroing logic. The 2026-05-27 refactor removed the local `nactfr` variable and replaced it with `n_act_frac` in the active-to-stable humus transfer calculation.

- 2024-12-05 refactor: migrated residue decomposition to the `soil1(j)%pl(ipl)%rsd(k)` structure, added `hnb_d(j)%rsd_nitorg_n` and `hnb_d(j)%rsd_laborg_p` initialization, and changed residue decay from the older layer-level residue pools to per-plant residue mass updates.
- 2025-02-06 update: changed humus mineralization to use the HRU-level nutrient parameter `hru(j)%nut%cmn` instead of the basin-level `bsn_prm%cmn`.
- 2026-01-07 update: made residue decomposition plant-specific by looping over `pcom(j)%npl`, selecting the plant database entry via `pcom(j)%plcur(ipl)%idplt`, and applying `pldb(idp)%rsdco_pl` to each plant residue pool.
- 2026-05-27 refactor: removed the local `nactfr` constant and used `n_act_frac` in the active-to-stable N transfer formula, keeping the same transfer logic but changing the source of the active-fraction parameter.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_nminrl' has no extracted documentation comment.
- algorithm_steps revised: merged the source into 9 higher-level steps to reflect the actual control flow and the per-plant residue loop.
- The extracted source initializes `hnb_d(j)%rsd_nitorg_n` and `hnb_d(j)%rsd_laborg_p`, but the visible lines in this packet do not show explicit accumulation assignments for those two fields; their summary is therefore based on the documented intent and zero-initialization only.
- The lineage evidence shows the active-fraction change as `n_act_frac`; the extracted source block still shows `n_act_frac` in the diff context, so the historical note reflects that variable name rather than the older local `nactfr`.
