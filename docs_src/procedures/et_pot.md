---
kind: procedure
symbol: et_pot
title: et_pot
status: filled
source_hash: 90c515dbffea0c4e
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the current HRU index, set from `ihru` at the start and then used to access HRU-specific
    elevation, snow, object connectivity, and plant community state.'
  idp: '`idp` holds the plant database index for the current plant in the community. It is
    assigned from `pcom(j)%plcur(ipl)%idplt` and used to fetch species stomatal conductance
    and VPD sensitivity from `pldb`.'
  iob: '`iob` stores the HRU''s connected object number so the routine can find the associated
    weather station when PET is read from input.'
  tk: '`tk` is air temperature converted to Kelvin (`w%tave + 273.15`) and is used in the
    longwave radiation term.'
  pb: '`pb` is mean barometric pressure estimated from HRU elevation and used to compute the
    psychrometric constant.'
  gma: '`gma` is the psychrometric constant derived from `pb` and latent heat; it appears
    in the Priestley-Taylor and Penman-Monteith equations.'
  xl: '`xl` is latent heat of vaporization computed from average air temperature and used
    to convert energy flux to evapotranspiration depth.'
  ea: '`ea` is the saturation vapor pressure returned by `ee(w%tave)` and used as the saturation
    term in the vapor-pressure calculations.'
  ed: '`ed` is actual vapor pressure, computed as saturation vapor pressure times relative
    humidity.'
  dlt: '`dlt` is the slope of the saturation vapor pressure curve at the current air temperature
    and is used in all PET equations here.'
  ramm: '`ramm` is extraterrestrial radiation estimated from `w%solradmx` and is used only
    by the Hargreaves PET branch.'
  ralb1: '`ralb1` is the net shortwave radiation for maximum plant ET in Penman-Monteith mode,
    using the day-specific albedo `albday`.'
  ralb: '`ralb` is the net shortwave radiation used for PET and is computed from snow presence
    versus open-surface albedo.'
  xx: '`xx` stores vapor-pressure deficit above the 1 kPa threshold so the code can reduce
    stomatal conductance when the air is dry.'
  rbo: '`rbo` is the net emissivity factor used in the longwave radiation calculation.'
  rto: '`rto` is the cloud-cover factor used to scale longwave radiation.'
  rn: '`rn` is the net radiation used in the Penman-Monteith maximum plant ET calculation.'
  uzz: '`uzz` is wind speed adjusted to the canopy measurement height and used in aerodynamic
    resistance for maximum plant ET.'
  zz: '`zz` is the wind measurement height in centimeters, set from canopy height rules before
    wind adjustment.'
  zom: '`zom` is the roughness length for momentum transfer, derived from canopy height.'
  zov: '`zov` is the roughness length for vapor transfer, set as a fraction of `zom`.'
  rv: '`rv` is aerodynamic resistance; it is first used for the reference-crop Penman-Monteith
    calculation and later recomputed for the plant canopy case.'
  rn_pet: '`rn_pet` is net radiation for the PET calculation and combines PET shortwave and
    longwave components.'
  fvpd: '`fvpd` is the VPD conductance reduction factor applied to plant stomatal conductance;
    it is limited to a minimum of 0.1.'
  rc: '`rc` is canopy resistance. The routine first sets a reference value for Penman-Monteith
    PET and later recomputes it for the active plant community.'
  rho: '`rho` is the combined-term coefficient `1710 - 6.85*Tave` used in the Penman-Monteith
    numerator.'
  rout: '`rout` is outgoing longwave radiation and is added to shortwave radiation to form
    net radiation.'
  d: '`d` is the zero-plane displacement height, computed from canopy height for the aerodynamic
    resistance calculation.'
  chz: '`chz` is canopy height in centimeters, derived from `pcom(j)%cht_mx` and used to size
    roughness and displacement terms.'
  gsi_adj: '`gsi_adj` is the VPD-adjusted stomatal conductance for one plant. It is accumulated
    across the community to build canopy resistance.'
  pet_alpha: '`pet_alpha` is the Priestley-Taylor alpha coefficient; this routine sets it
    to 1.28 before computing `pet_day` in case 0.'
  ee: '`ee` is the saturation vapor pressure function called with air temperature to obtain
    `ea`.'
  gsi_wav: '`gsi_wav` accumulates the VPD-adjusted conductance across the plant community,
    weighted by each plant''s LAI share. The routine computes it but does not use it later
    in this source span.'
  igrocom: '`igrocom` flags whether at least one plant in the community is growing; it controls
    whether maximum plant ET is computed.'
uses:
  plant_data_module: The plant database provides species parameters, especially maximum stomatal
    conductance (`gsi`) and VPD response (`vpd2`), that the Penman-Monteith branch needs to
    reduce conductance and form canopy resistance for the active plants.
  basin_module: The basin control code selects which PET method runs in this subroutine, so
    it determines the entire control flow and which output variable is produced.
  hydrograph_module: The connected object table maps the current HRU to its weather station,
    which is needed when PET is read from input instead of being computed.
  climate_module: 'Daily weather supplies the meteorological drivers for all PET branches:
    temperature, humidity, solar radiation, wind, and the read-in station PET value.'
  hru_module: The current HRU state supplies elevation, snow depth, connected object number,
    and a PET coefficient that all affect the calculation or final scaling.
  plant_module: The plant community provides canopy height, total LAI, plant count, growth
    flags, and current plant IDs, which are required to decide whether plant ET is computed
    and to build canopy resistance.
---

<!-- facts:header -->

Computes daily potential evapotranspiration for an HRU using Priestley-Taylor, Penman-Monteith, Hargreaves, or read-in PET. In Penman-Monteith mode it also estimates maximum plant transpiration from current plant and climate state.

## Bottom Line

The routine calculates the HRU's daily potential evapotranspiration and stores the result in `pet_day`. Which formula is used is controlled by `bsn_cc%pet`: Priestley-Taylor, Penman-Monteith, Hargreaves, or a read-in weather-station PET value.

When Penman-Monteith is selected, the routine also computes `ep_max` for actively growing plant communities by using HRU weather, canopy structure, plant conductance, and CO2 adjustment. The results feed the later evapotranspiration step called by `hru_control`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU processing in `hru_control`, right after crack volume is computed and before `et_act`. `hru_control` has already set the active HRU context (`ihru`) and current daily climate state, and the PET results from `et_pot` are then used by the later evapotranspiration logic.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Bind the active HRU and basic thermodynamic state. | The routine sets `j = ihru`, converts air temperature to Kelvin, computes pressure from HRU elevation, latent heat, psychrometric constant, saturation vapor pressure, actual vapor pressure, vapor pressure deficit, and the slope of the saturation vapor pressure curve. |
| 2. Choose the PET method. | The routine branches on `bsn_cc%pet` to select Priestley-Taylor, Penman-Monteith, Hargreaves, or read-in PET. |
| 3. Compute Priestley-Taylor PET. | For method 0, it computes PET shortwave radiation with snow/no-snow albedo, longwave radiation using emissivity and cloud factor, combines them into `rn_pet`, applies `pet_alpha = 1.28`, and stores nonnegative `pet_day`. |
| 4. Compute Penman-Monteith PET radiation terms and reference resistances. | For method 1, it computes PET and maximum-plant shortwave radiation, longwave radiation, net radiation, the combined-term coefficient `rho`, a minimum wind speed, reference aerodynamic resistance, reference canopy resistance, and nonnegative `pet_day`. |
| 5. Detect whether any plant is growing. | The routine scans the plant community flags and sets `igrocom` to 1 if at least one plant has `gro == 'y'`; otherwise it sets `ep_max = 0.0` and skips the canopy ET work. |
| 6. Build canopy geometry and aerodynamic resistance. | When plants are growing, it sets wind measurement height from canopy height, adjusts wind speed, derives canopy height in centimeters, computes roughness lengths and displacement height, and calculates aerodynamic resistance. |
| 7. Adjust stomatal conductance for VPD. | The routine loops over plants, finds each plant ID, computes its LAI share, measures VPD excess above 1 kPa, reduces conductance with the plant's `vpd2` parameter when needed, and accumulates adjusted conductance. |
| 8. Compute canopy resistance and maximum plant ET. | It converts the adjusted conductance to canopy resistance with LAI and CO2 scaling, computes `ep_max` from the Penman-Monteith equation, clips it at zero, and limits it to `pet_day`. |
| 9. Compute Hargreaves PET. | For method 2, it estimates extraterrestrial radiation from `w%solradmx`, then computes `pet_day` from temperature range and average temperature when `tmax > tmin`, otherwise sets it to zero. |
| 10. Read PET from the connected weather station. | For method 3, it uses the HRU's connected object to locate the weather station and copies the station's daily PET value into `pet_day`. |
| 11. Apply the HRU PET coefficient and return. | The routine multiplies `pet_day` by `hru(j)%hyd%pet_co` and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%gsi` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%pet` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:climate_module] | `w, wst` | `w%tave, w%rhum, w%solrad, w%solradmx, w%windsp, w%tmax, w%tmin, wst(iwst)%weat%pet` |
| [sym:hru_module] | `hru, ihru, albday, ipl, pet_day, vpd, ep_max` | `hru(j)%topo%elev, hru(j)%sno_mm, hru(j)%obj_no, hru(j)%hyd%pet_co` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%gro, pcom(j)%cht_mx, pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%lai, pcom(j)%lai_sum` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `vpd` | Always, after `ea = Ee(w%tave)` and `ed = ea * w%rhum` are computed. | `vpd` is updated to the current day's vapor pressure deficit for the active HRU. That value drives the Penman-Monteith aerodynamic term and the VPD-limited stomatal conductance adjustment. |
| `pet_day` | Set in method 0 and method 1 after the radiation and temperature terms are assembled, and in method 2 only when `w%tmax > w%tmin`. | `pet_day` becomes the day's potential evapotranspiration for the selected method. It is the routine's main output and is later scaled by the HRU PET coefficient. |
| `ep_max` | Only in Penman-Monteith mode, and only when at least one plant in the community has `gro == 'y'`. | `ep_max` stores the maximum potential transpiration for the active plant community. It is capped by `pet_day` so plant transpiration cannot exceed the HRU-level PET estimate. |
| `iwst` | Only in read-in PET mode (`bsn_cc%pet == 3`), after the HRU's connected object and weather station are resolved. | `iwst` is assigned the weather-station index for the current HRU so the routine can copy `wst(iwst)%weat%pet` into `pet_day`. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:1.2.11 | Net radiation (full balance) | $H_{net}=H_{day}\downarrow-\alpha*H_{day}\uparrow+H_L\downarrow-H_L\uparrow$ | rn_pet = ralb + rout combines net shortwave and net longwave. |
| 1:1.2.12 | Net radiation = (1-alpha)Hday + Hb | $H_{net} = (1-\alpha) H_{day} + H_b$ | ralb=(1-alpha)*solrad shortwave; rout = Hb longwave. |
| 1:1.2.13 | Snow albedo = 0.8 | $\alpha=0.8$ | ralb = solrad*(1-0.8) when snow present; vegetated uses 0.23 (line 122). |
| 1:1.2.17 | Longwave radiation eps*sigma*T^4 | $H_R=\varepsilon \sigma T_K^{4}$ | sigma = 4.9e-9 MJ/m2/K4/day; T in Kelvin (tk). |
| 1:1.2.18 | Cloud-adjusted net longwave Hb | $H_b=f_{cld} (\varepsilon_a -\varepsilon_{vs}) \sigma T_K^{4}$ | rout = rbo*rto*sigma*tk^4 combines net emissivity and cloud factor. |
| 1:1.2.19 | Cloud factor f_cld | $f_{cld}=a \frac{H_{day}}{H_{MX}}-b$ | rto = 0.9*(solrad/solradmx)+0.1. |
| 1:1.2.20 | Net emissivity eps' | $\varepsilon'=\varepsilon_a-\varepsilon_{vs}=-(a_1+b_1 \sqrt{(e)})$ | rbo = -(0.34 - 0.139*Sqrt(ed)). |
| 1:1.2.21 | Net longwave (combined form) | $H_b=-[a \frac{H_{day}}{H_{MX}}-b] [a_1+b_1 \sqrt{(e)}] \sigma T_k^4$ | rout = rbo*rto*4.9e-9*tk^4. |
| 1:1.2.22 | Net longwave (numeric coefficients) | $H_b=-[0.9 \frac{H_{day}}{H_{MX}}+0.1] [0.34-0.139\sqrt{(e)}] \sigma T_k^4$ | Constants 0.34/0.139 (emissivity) and 0.9/0.1 (cloud) match the published coefficients. |
| 1:1.4.1 | Wind measurement height above canopy | $z_w=h_c+100$ | Penman-Monteith plant ET sets zz = canopy height*100 + 100 cm when canopy height exceeds 1 m; otherwise zz defaults to 170 cm. |
| 1:1.4.2 | Wind speed adjusted to canopy measurement height | $u_{z2}=u_{z1}[\frac{z_2}{z_1}]^{aa}$ | uzz = windsp*(zz/1000.)**0.2 applies the documented power-law wind-profile adjustment. |
| 1:2.3.2 | Saturation vapor pressure e^o | $e^o=exp[\frac{16.78*\overline T_{av}-116.9}{\overline T_{av}+237.3}]$ | ea = Ee(w%tave); computed in ee.f90. |
| 1:2.3.4 | Slope of sat vapor pressure curve | $\Delta=\frac{4098*e^o}{(\overline T_{av}+237.3)^2}$ | dlt = 4098*ea/(tave+237.3)^2. |
| 1:2.3.5 | Vapor pressure deficit | $vpd=e^o-e$ | Verified against SWAT+ 62.0.0 (et_pot.f90). |
| 1:2.3.6 | Latent heat of vaporization | $\lambda=2.501-2.361*10^{-3}*\overline T_{av}$ | xl = 2.501 - 2.361e-3*tave. |
| 1:2.3.7 | Psychrometric constant | $\gamma=\frac{c_p*P}{0.622*\lambda}$ | Verified against SWAT+ 62.0.0 (et_pot.f90). |
| 1:2.3.8 | Mean barometric pressure | $P=101.3-0.01152*EL+0.544*10^{-6}*EL^2$ | pb = 101.3 - elev*(0.01152 - 0.544e-6*elev). |
| 2:2.2.1 | Penman-Monteith potential ET | $\lambda E=\frac{\Delta*(H_{net}-G)+\rho_{air}*c_p*[e^o_z-e_z]/r_a}{\Delta+\gamma*(1+r_c/r_a)}$ | Verified against SWAT+ 62.0.0 (et_pot.f90:188). pet_day = (dlt*rn_pet+gma*rho*vpd/rv)/(xl*(dlt+gma*(1.+rc/rv)))` — Penman-Monteith |
| 2:2.2.2 | Penman-Monteith transpiration form | $\lambda E_t=\frac{\Delta*(H_{net}-G)+\gamma*K_1*(0.622*\gamma*\rho_{air}/P)*(e^o_z-e_z)/r_a}{\Delta+\gamma*(1+r_c/r_a)}$ | Verified against SWAT+ 62.0.0 (et_pot.f90:188). expanded PM; `rho` (:181) is the grouped `K1·0.622·ρ/P` psychrometric term |
| 2:2.2.3 | Aerodynamic resistance | $r_a=\frac{ln[(z_w-d)/z_{om}]ln\lfloor(z_p-d)/z_{ov}\rfloor}{k^2u_z}$ | Verified against SWAT+ 62.0.0 (et_pot.f90:229). rv = Log((zz-d)/zom)*Log((zz-d)/zov)` / (0.41^2·uzz) |
| 2:2.2.4 | Low-canopy roughness length | $z_{om} = h_c/8.15 =0.123*h_c$ | Verified against SWAT+ 62.0.0 (et_pot.f90:216). if (chz <= 200.)` roughness-length branch (h_c≤200cm) |
| 2:2.2.5 | Tall-canopy roughness length | $z_{om}= 0.058*(h_c)^{1.19}$ | For canopy height > 200 cm, zom = 0.058*h_c^1.19. |
| 2:2.2.6 | Vapor roughness length | $z_{ov} =0.1*z_{om}$ | Verified against SWAT+ 62.0.0 (et_pot.f90:223). zov = 0.1 * zom` — exact |
| 2:2.2.7 | Zero-plane displacement | $d=2/3*h_c$ | Verified against SWAT+ 62.0.0 (et_pot.f90:225). d = 0.667 * chz` — zero-plane displacement (2/3·h_c) |
| 2:2.2.8 | Canopy resistance from leaf conductance and LAI | $r_c=r_l/(0.5*LAI)$ | Code computes rc from stomatal conductance and LAI, including the CO2 factor, rather than first computing rl then rc as separate stored variables. |
| 2:2.2.9 | Leaf resistance from adaxial/abaxial terms | $r_{l}=\frac{r_{l -ad}*r_{l-ab}}{r_{l-ab}+r_{l-ad}}$ | The code works in conductance space using plant parameters and does not explicitly form rl from separate adaxial and abaxial resistances. |
| 2:2.2.10 | Leaf resistance equal halves | $r_{l}=\frac{r_{l-ad}}{2}=\frac{r_{l-ab}}{2}$ | Equal adaxial/abaxial resistances are not expressed explicitly in the active code. |
| 2:2.2.11 | Single-sided leaf resistance | $r_{l}=r_{l-ad}=r_{l-ab}$ | The active code does not store rl_ad and rl_ab explicitly. |
| 2:2.2.12 | Leaf conductance | $g_{l}=\frac{1}{r_{l}}$ | gsi_adj is the adjusted stomatal conductance used in the canopy-resistance calculation. |
| 2:2.2.13 | Canopy resistance inverse-conductance form | $r_c=(0.5*g_l*LAI)^{-1}$ | rc is computed as the inverse of adjusted conductance scaled by LAI and CO2 rather than via a separate gl variable. |
| 2:2.2.14 | CO2-adjusted leaf conductance | $g_{l,CO_2}=g_{l}*[1.4-0.4*(CO_2/330)]$ | The denominator contains (1.4 - 0.4*CO2/330), reducing conductance as CO2 rises. |
| 2:2.2.15 | CO2-adjusted canopy resistance | $r_c=r_l*[(0.5*LAI)*(1.4-0.4*\frac{CO_2}{330})]^{-1}$ | rc is divided by 0.5*LAI*(1.4 - 0.4*CO2/330). |
| 2:2.2.16 | VPD-limited conductance branch | $g_{l}=g_{l,mx}*\lfloor1-\Delta g_{l,dcl}(vpd-vpd_{thr})\rfloor$ | When vpd exceeds the hard-coded 1 kPa threshold, conductance is reduced by fvpd = max(0.1, 1 - vpd2*(vpd - 1)). |
| 2:2.2.17 | No VPD reduction branch | $g_{l}=g_{l,mx}$ | When vpd <= 1 kPa, fvpd = 1 and conductance remains at the plant parameter value. |
| 2:2.2.18 | VPD decline coefficient | $\Delta g_{l,dcl}=\frac{(1-fr_{g,mx})}{(vpd_{fr}-vpd_{thr})}$ | The printed decline coefficient is represented by plant parameter vpd2 multiplied by the excess vapor pressure deficit. |
| 2:2.2.19 | Combined term coefficient | $K_1 *0.622*\lambda*\rho/P=1710-6.85*\overline T_{av}$ | rho = 1710 - 6.85*Tave. |
| 2:2.2.20 | Reference aerodynamic resistance | $r_a=\frac{114.}{u_z}$ | Verified against SWAT+ 62.0.0 (et_pot.f90:186). rv = 114./(windsp*(170/1000)**0.2)` — r_a=114/u_z |
| 2:2.2.21 | LAI-height relationship | $LAI=1.5*ln(h_c)-1.4$ | The printed LAI = 1.5*ln(hc) - 1.4 relationship is not used; the model reads LAI and canopy height independently from plant state/parameters. |
| 2:2.2.22 | Reference canopy resistance | $r_c=49/(1.4-0.4*\frac{CO_2}{330})$ | rc = 49/(1.4 - 0.4*CO2/330). |
| 2:2.2.23 | Priestley-Taylor PET | $\lambda E_o=\alpha_{pet}*\frac{\Delta}{\Delta+\gamma}*(H_{net}-G)$ | pet_day = alpha*(dlt/(dlt+gma))*rn_pet/xl with alpha = 1.28. |
| 2:2.2.24 | Hargreaves PET | $\lambda E_o=0.0023*H_0*(T_{mx}-T_{mn})^{0.5}*(\overline T_{av}+17.8)$ | pet_day = 0.0023*(ramm/xl)*(tave+17.8)*(tmax-tmin)^0.5. |

## Lineage

`et_pot.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `et_pot.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'et_pot' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
