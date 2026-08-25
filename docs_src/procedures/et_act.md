---
kind: procedure
symbol: et_act
title: et_act
status: filled
source_hash: 8fb623ad088ad07f
version_label: SWAT+ 62.0.0
locals:
  j: HRU index used to access the current row of `hru`, `pcom`, `pl_mass`, `soil`, `soil1`,
    `wet`, and related module arrays; it is set from `ihru` at the start of the routine.
  esd: Maximum soil depth from which evaporation is allowed to occur. The routine sets it
    to 500 mm and uses it as a cutoff when iterating through soil layers.
  etco: Soil evaporation coefficient used to cap layer evaporation by the amount of water
    stored in the layer. The routine sets it to 0.80.
  effnup: Efficiency factor for moving nitrate upward with evaporation. It scales the nitrate
    flux from layer 2 to layer 1 based on the amount of evaporation taken from the upper soil.
  no3up: Computed nitrate amount moved upward from layer 2 into layer 1 during evaporation-driven
    redistribution.
  es_max: Maximum potential soil evaporation available for the day after canopy, plant, and
    water-body effects are accounted for.
  eos1: Intermediate value used during soil-evaporation calculations; in this routine it is
    initialized but not shown taking a final role in the extracted source.
  xx: Intermediate exponent argument used when reducing layer evaporation under dry soil conditions.
  cej: Unused in the extracted source beyond initialization; it appears to be a coefficient
    placeholder related to cover adjustment.
  eaj: Soil-cover attenuation factor applied when computing potential soil evaporation from
    plant and residue cover.
  pet: Working copy of daily PET after canopy interception demand is removed. The routine
    uses it to compute remaining atmospheric demand for transpiration and soil evaporation.
  esleft: Remaining soil-evaporation demand after canopy interception, snow sublimation, and
    wetland/ponded-water evaporation have been taken out.
  evzp: Tracks cumulative evaporation from depth as the routine steps through soil layers,
    so each deeper layer can be computed as a difference from the previous depth.
  eosl: Residual soil-evaporation demand passed into the layer loop. It starts as `esleft`
    and represents the total soil evaporation still available to allocate by depth.
  dep: Depth to the bottom of the current layer or the layer above it, used to stop evaporation
    extraction below the configured maximum depth `esd`.
  evz: Cumulative evaporation available at the current layer depth before subtracting the
    previous cumulative amount.
  sev: Actual evaporation removed from the current soil layer after all reductions and limits
    are applied.
  sev_st: Ratio of evaporation taken from layer 2 to the water stored in that layer; it is
    used to scale nitrate movement upward.
  cover: Total soil/vegetation cover mass used to attenuate potential soil evaporation.
  wetvol_mm: Ponded-water or wetland volume expressed as an average depth over the HRU area;
    it is used to convert between depth and volume when evaporation is taken from water bodies.
  ly: Loop counter over soil layers.
  ires: Index of the surface-storage/wetland reservoir data record associated with the current
    HRU.
  ihyd: Index into wetland/reservoir hydrology data used to obtain the wetland evaporation
    coefficient.
uses:
  basin_module: '`basin_module` is included because the routine relies on basin-wide control
    state to interpret the daily ET method and HRU processing context; even though no specific
    basin symbol was extracted here, the module is part of the routine''s operating state
    set.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the plant residue and
    soil nitrate pools that this routine uses to define cover and to move nitrate upward when
    evaporation draws water from the upper soil layers.'
  hru_module: '`hru_module` holds the HRU-specific working state that this routine updates
    directly: canopy storage, snow water, water-body evaporation, PET-derived ET terms, and
    the HRU''s soil-evaporation compensation factor.'
  soil_module: '`soil_module` matters because the routine pulls layer depths and water-storage
    values from the HRU soil profile, uses them to compute evaporation by layer, and then
    writes the updated layer water back.'
  plant_module: '`plant_module` supplies the community LAI used to split PET between plant
    transpiration and soil evaporation, so it directly controls how much demand remains for
    the soil.'
  climate_module: '`climate_module` provides daily average temperature, which gates the snow
    sublimation branch; the routine only takes sublimation from snow when the day is warm
    enough in the extracted logic.'
  hydrograph_module: '`hydrograph_module` supplies the wetland flow volume for the current
    HRU, letting the routine estimate how much evaporation can be taken from ponded or wetland
    water before the remaining demand reaches the soil.'
  water_body_module: '`water_body_module` stores the daily wetland evaporation volume for
    each HRU, which this routine updates after converting between depth over area and water-body
    volume.'
  reservoir_data_module: '`reservoir_data_module` matters because the wetland evaporation
    coefficient comes from the hydrology record referenced by the HRU surface-storage index,
    so the routine can scale ponded-water evaporation appropriately.'
---

<!-- facts:header -->

Computes daily actual evapotranspiration for an HRU. It removes interception and ponded-water losses first, then allocates the remaining demand to snow sublimation and layer-by-layer soil evaporation while updating soil water and nitrate in the profile.

## Bottom Line

This routine is the HRU-level evapotranspiration allocator. Starting from daily PET, it subtracts canopy interception, limits plant transpiration and soil evaporation by vegetation and soil-cover conditions, and then distributes the remaining evaporation demand across snow, wetland/ponded water, and soil layers.

It also updates related HRU state: canopy storage, snowpack, wetland water volume, per-layer soil water, profile water content, and nitrate movement between the upper soil layers. Those updates feed later HRU management and surface-runoff processing in the same daily control sequence.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the daily HRU evapotranspiration phase, immediately after `et_pot` in `hru_control`. `et_pot` prepares the potential-demand state, and `et_act` then turns that demand into actual canopy, snow, ponded-water, and soil losses that later management and runoff calculations depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the working HRU index and ET controls. | The routine declares and initializes its local controls, copies `ihru` into `j`, reads the day's PET from `pet_day`, sets fixed coefficients such as `esd`, `etco`, and `effnup`, and fetches the current surface-storage index from `hru(j)%dbs%surf_stor`. |
| 2. Remove canopy interception from daily PET. | It first satisfies canopy evaporation from stored canopy water. If interception storage exceeds remaining PET, all PET is consumed, canopy storage is reduced by the leftover amount, and plant/soil evaporation demand is zeroed. Otherwise the canopy storage is emptied and the remaining PET continues. |
| 3. Compute potential transpiration from LAI. | When PET remains, the routine sets potential plant transpiration from `pcom(j)%lai_sum`: LAI up to 3 scales transpiration linearly with PET, while LAI above 3 allows transpiration to equal the remaining PET. Negative results are clipped to zero. |
| 4. Build the soil-cover attenuation term for potential soil evaporation. | The routine resets soil-evaporation intermediates, forms total cover from aboveground biomass and total residue mass, and converts that cover into an attenuation factor. Snow cover forces a fixed reduction, while otherwise the factor depends exponentially on the cover amount. The resulting potential soil evaporation is then limited so that plant and soil ET together do not exceed available PET. |
| 5. Add ponded-water or wetland evaporation when surface storage exists. | If the HRU has ponded surface water, the routine uses the wetland hydrology coefficient and LAI to compute evaporation from water before soil evaporation. When no surface water is present, the code instead reconciles soil and plant demand so their combined total does not exceed PET. |
| 6. Initialize remaining soil-evaporation demand and remove snow sublimation first. | The remaining soil-evaporation demand is copied into `esleft`. If air temperature is above freezing, the routine takes as much of that demand as possible from snowpack, decreasing `hru(j)%sno_mm` and accumulating the amount in `snoev`. |
| 7. Remove evaporation from ponded water and update wetland volume. | The routine converts wetland flow volume to an average depth over the HRU, subtracts as much remaining demand as possible from that water, converts the evaporation back to a volume stored in `wet_wat_d(j)%evap`, and writes the reduced volume back to `wet(j)%flo` and `hru(j)%water_evap`. |
| 8. Distribute the remaining evaporation down the soil profile. | For each soil layer above the maximum evaporation depth, the routine computes cumulative evaporation with depth, subtracts the portion already taken from shallower layers using `hru(j)%hyd%esco`, and reduces the layer rate when water storage is below field capacity. Layer evaporation is then capped by available water, subtracted from the layer storage, and the remaining demand is updated. |
| 9. Move nitrate upward when the second layer is depleted by evaporation. | On layer 2, the routine converts the evaporation fraction into an upward nitrate transfer from `soil1(j)%mn(2)%no3` to `soil1(j)%mn(1)%no3`, limiting the transfer to the available nitrate pool. |
| 10. Recompute total soil water and daily soil evaporation. | After the layer loop, the routine recomputes profile soil water as the sum of layer storages and sets daily actual soil evaporation to the portion of potential soil evaporation that was actually removed. |
| 11. Return to the daily HRU control sequence. | The subroutine exits after leaving the updated HRU, water-body, soil-water, nitrate, and ET state in the shared modules for later daily model processing. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `hru, canstor, ihru, canev, ep_max, es_day, pet_day, snoev` | `hru(j)%dbs%surf_stor, hru(j)%sno_mm, hru(j)%area_ha, hru(j)%water_evap, hru(j)%hyd%esco` |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%rsd_tot%m, soil1(j)%mn(2)%no3, soil1(j)%mn(1)%no3` |
| [sym:hru_module] | `hru, canstor, ihru, canev, ep_max, es_day, pet_day, snoev` | `hru(j)%dbs%surf_stor, hru(j)%sno_mm, hru(j)%area_ha, hru(j)%water_evap, hru(j)%hyd%esco` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(1)%d, soil(j)%phys(ly-1)%d, soil(j)%phys(ly)%d, soil(j)%phys(ly)%st, soil(j)%phys(ly)%fc, soil(j)%phys(2)%st, soil(j)%sw` |
| [sym:plant_module] | `pcom` | `pcom(j)%lai_sum` |
| [sym:climate_module] | `w` | `w%tave` |
| [sym:hydrograph_module] | `wet` | `wet(j)%flo` |
| [sym:water_body_module] | `wet_wat_d` | `wet_wat_d(j)%evap` |
| [sym:reservoir_data_module] | `wet_dat, wet_hyd` | `wet_dat(ires)%hyd, wet_hyd(ihyd)%evrsv` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `canev` | When PET remains after canopy storage is checked. | `canev` is set to the amount evaporated from canopy storage for the day, either the full `pet_day` if interception demand exceeds available PET or the entire canopy storage amount when storage is emptied. |
| `canstor(j)` | After canopy interception is processed for the current HRU. | `canstor(j)` is reduced by the amount of canopy evaporation. It becomes the leftover interception storage when PET is exhausted or zero when all canopy water evaporates. |
| `ep_max` | When remaining PET is positive and LAI is evaluated. | `ep_max` becomes the day's potential plant transpiration limit, scaled by LAI for sparse canopies and equal to remaining PET for dense canopies. |
| `hru(j)%sno_mm` | When the snow-sublimation branch takes water from snowpack. | `hru(j)%sno_mm` is reduced by the amount of soil-evaporation demand removed from snow, and it can be driven to zero when the demand exceeds the available snowpack. |
| `snoev` | During the warm-temperature snow branch. | `snoev` accumulates the amount of snow water lost to sublimation on the current day. |
| `wet_wat_d(j)%evap` | When wetland or ponded water exists on the HRU. | `wet_wat_d(j)%evap` is set to the evaporation volume removed from the water body, converted from the remaining demand depth back into volume. |
| `wet(j)%flo` | When `wet(j)%flo` is positive. | `wet(j)%flo` is reduced to reflect the water volume consumed by evaporation from ponded water or wetland storage. |
| `hru(j)%water_evap` | After evaporation is taken from surface water. | `hru(j)%water_evap` records the equivalent depth of water evaporated from the HRU's surface water storage. |
| `soil(j)%phys(ly)%st` | For each soil layer that lies above the evaporation depth and has enough storage to lose water. | `soil(j)%phys(ly)%st` is reduced by the layer evaporation amount, but not below the routine's minimum storage safeguard. |
| `soil1(j)%mn(2)%no3` | When the loop reaches soil layer 2 and evaporation has occurred. | `soil1(j)%mn(2)%no3` loses nitrate in proportion to the evaporation fraction moving water upward out of layer 2. |
| `soil1(j)%mn(1)%no3` | When nitrate is shifted upward from layer 2. | `soil1(j)%mn(1)%no3` gains the nitrate transferred from layer 2, preserving the pool within the upper soil layer. |
| `soil(j)%sw` | After all soil-layer evaporation is applied. | `soil(j)%sw` is recomputed as the sum of all layer storages so the profile water content stays consistent with the updated layer states. |
| `es_day` | At the end of the routine after soil evaporation has been allocated. | `es_day` stores the actual soil evaporation realized during the day, calculated as the potential soil evaporation minus the remaining unmet demand. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:2.3.1 | Canopy evaporation equals PET | $E_a=E_{can}=E_o$ | If intercepted water exceeds PET, all PET is used for canopy evaporation. |
| 2:2.3.2 | Interception storage after canopy evaporation | $R_{INT(f)}=R_{INT(i)}-E_{can}$ | Canopy storage is reduced by the evaporated amount. |
| 2:2.3.3 | Canopy evaporation limited by interception storage | $E_{can}=R_{INT(i)}$ | When interception storage is less than PET, all intercepted water evaporates and storage is reset to zero. |
| 2:2.3.4 | Zero interception storage after complete evaporation | $R_{INT(f)}=0$ | Stored intercepted water is zeroed after the canopy is emptied. |
| 2:2.3.5 | Transpiration for LAI <= 3 | $E_t=\frac{E'_o*LAI}{3.0}$ | Verified against SWAT+ 62.0.0 (et_act.f90:115). if (lai_sum<=3.0) ep_max = lai_sum*pet/3. |
| 2:2.3.6 | Transpiration for LAI > 3 | $E_t=E'_o$ | Verified against SWAT+ 62.0.0 (et_act.f90:117). else ep_max = pet` — LAI>3.0 branch |
| 2:2.3.7 | Potential soil evaporation after cover reduction | $E_s=E'_o*cov_{sol}$ | Verified against SWAT+ 62.0.0 (et_act.f90:115). transpiration-vs-LAI relation implied by the same two-branch split |
| 2:2.3.8 | Soil cover attenuation factor | $cov_{sol}=exp(-5.0*10^{-5}*CV)$ | Verified against SWAT+ 62.0.0 (et_act.f90:131). eaj = Exp(-5.e-5*(cover+0.1))` — soil cover index |
| 2:2.3.9 | Soil evaporation limited by remaining energy | $E'_s=min[E_s,\frac{E_s*E'_o}{E_s+E_t}]$ | es_max is limited to es*pet/(es+ep) before layer extraction. |
| 2:2.3.10 | Sublimation equals remaining soil-evaporation demand | $E_{sub}=E'_s$ | The routine subtracts snow from the residual soil-evaporation demand, but the branch is entered under the routine's current snow/temperature logic rather than as a standalone published sequence. |
| 2:2.3.11 | Snowpack after sublimation | $SNO_{(f)}=SNO_{(i)}-E'_s$ | Snow storage is reduced by the sublimated amount when sufficient snow is present. |
| 2:2.3.12 | Zero residual soil evaporation after full sublimation demand is met | $E''_s=0.$ | Residual soil-evaporation demand is set to zero after sublimation consumes it. |
| 2:2.3.13 | Sublimation limited by available snow | $E_{sub}=SNO_{(i)}$ | When snow is insufficient, the whole snowpack sublimates. |
| 2:2.3.14 | Snowpack emptied by sublimation | $SNO_{(f)}=0.$ | Snow storage is reset to zero when sublimation exceeds the snowpack. |
| 2:2.3.15 | Residual soil evaporation after partial sublimation | $E''_s=E'_s-E_{sub}$ | Remaining soil-evaporation demand is reduced by the sublimated snow amount. |
| 2:2.3.16 | Cumulative soil evaporation with depth | $E_{soil,z}=E''_s*\frac{z}{z+exp(2.374-0.00713*z)}$ | sev = eosl*z/(z + exp(2.374 - 0.00713*z)). |
| 2:2.3.17 | Layer soil evaporation from cumulative-depth difference | $E_{soil,ly}=E_{soil,zl}-E_{soil,zu}$ | Verified against SWAT+ 62.0.0 (et_act.f90:217). |
| 2:2.3.18 | Layer evaporation reduced by esco | $E_{soil,ly}=E_{soil,zl}-E_{soil,zu}*esco$ | Verified against SWAT+ 62.0.0 (et_act.f90:217). |
| 2:2.3.19 | Moisture-limited layer evaporation when SW < FC | $E'_{soil,ly}=E_{soil,ly}*exp(\frac{2.5*(SW_{ly}-FC_{ly})}{FC_{ly}-WP_{ly}})$ | Code at et_act.f90:219-223 reduces layer evaporation by `exp(2.5 * (st - fc) / fc)` when storage is below field capacity, using an FC denominator; theory equation 2:2.3.19 uses an FC - WP (field capacity minus wilting point) denominator. Confirm whether this is an intentional SWAT+ simplification or a genuine divergence. Independent 2.2 traceability trace flags this as 'Difference'; prior status was 'implemented'. |
| 2:2.3.20 | No moisture reduction when SW >= FC | $E'_{soil,ly}=E_{soil,ly}$ | Verified against SWAT+ 62.0.0 (et_act.f90:219). |
| 2:2.3.21 | Layer evaporation limited by available water | $E''_{soil,ly}=min(E'_{soil,ly} 0.8*(SW_{ly}-WP_{ly}))$ | Verified against SWAT+ 62.0.0 (et_act.f90:224). sev = Min(sev, st*etco)` etco=0.80; theory limits to 0.8·(SW−WP), code to 0.8·SW |
| 2:2.3.22 | Ponded-water evaporation under partial LAI cover | $EVP_t=0.6*(1-\frac {LAI}{4.0})*PET \; when \; LAI≤4.0$ | Verified against SWAT+ 62.0.0 (et_act.f90:143). ponded/wetland evap; theory's 0.6 is param `evrsv`, LAI≤4 branch |
| 2:2.3.23 | Zero ponded-water evaporation at high LAI | $EVP_t = 0, \; when \; LAI>4.0$ | Verified against SWAT+ 62.0.0 (et_act.f90:145). else es_max = 0.` — LAI>4.0 ponded-evap branch |
| 3:1.7.1 |  | $N_{evap}=0.1*NO3_{ly}*\frac{E''_{soil,ly}}{SW_{ly}}$ | Verified against SWAT+ 62.0.0 (et_act.f90:248). no3up = effnup*sev_st*no3` with sev_st=sev/st (E″/SW); effnup=0.05 in code vs theory's 0.1 |

## Lineage

Four resolved commits changed `et_act`: df07e3f added the subroutine; 94b6dec introduced the initial documented implementation; 39fabde initialized local variables and set fixed `esd`, `etco`, and `effnup` values; eb22103 and 72206bc updated the cover calculation to use `soil1(j)%rsd(1)%m` and then `pl_mass(j)%rsd_tot%m`.

- df07e3f created the routine and established the original ET allocation flow from canopy evaporation through soil evaporation and nitrate redistribution.
- 94b6dec introduced the extracted implementation and documentation comments that define the daily PET, snow, wetland, and soil-layer processing.
- 39fabde changed local variable initialization from uninitialized declarations to explicit zero initialization and set the working constants used by the routine.
- eb22103 switched the cover term from `rsd1(j)%tot_com%m` to `soil1(j)%rsd(1)%m`, changing which residue structure contributed to soil-cover attenuation.
- 72206bc changed the cover term again, replacing `soil1(j)%rsd(1)%m` with `pl_mass(j)%rsd_tot%m` so total residue mass now drives the soil-cover calculation.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'et_act' has no extracted documentation comment.
