---
kind: procedure
symbol: pl_waterup
title: pl_waterup
status: filled
source_hash: 97b11445c8025865
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` so the routine works on the active HRU in `hru`, `soil`,
    and `pcom`.
  k: Soil-layer loop counter used to walk through `soil(j)%nly` layers and update each layer’s
    uptake and water storage.
  ir: Flag marking that the bottom of the rooted zone has been reached; when set, it exits
    the layer loop early.
  idp: Plant identifier pulled from `pcom(j)%plcur(ipl)%idplt` so the routine can look up
    plant-specific salinity and aeration parameters.
  ulu: Urban land-use code from `hru(j)%luse%urb_lu`, read before the impervious-area adjustment
    step.
  isalt: Salt-ion counter used to loop over `cs_db%num_salts` ions in a rooted layer.
  sum: Cumulative potential uptake at the current rooting depth, computed from `epmax`, `uptake%water_dis`,
    and `uptake%water_norm`.
  sum_wuse: Running total of actual water uptake across all soil layers for the current plant.
  sum_wusep: Previous value of `sum_wuse`, used to back-calculate the layer’s capped uptake
    when total demand exceeds `epmax(ipl)`.
  sump: Stores the prior layer’s cumulative potential uptake so compensation with `epco` can
    be applied to the next layer.
  gx: Effective depth used in the exponential uptake distribution; it is the smaller of rooting
    depth and the current layer bottom depth.
  wuse: Actual water uptake assigned to the current soil layer after compensation and availability
    limits are applied.
  satco: Computed saturation coefficient used in the aeration-stress calculation when soil
    water exceeds field capacity.
  scparm: Intermediate aeration-stress parameter derived from saturation excess and the plant’s
    aeration tolerance.
  reduc_salt: Current salinity reduction factor for the active layer, initialized to 1 and
    reduced when soil EC exceeds the crop threshold.
  reduc_salt_min: Minimum salinity reduction encountered across rooted layers; this becomes
    the plant’s daily salt stress factor.
  sw_decrease: Declared salt-stress helper variable, but it is not updated in the visible
    source.
  salt_decrease: Declared salt-stress helper variable, but it is not updated in the visible
    source.
  theta_w: Layer water-content ratio used to convert dissolved salt concentration to a saturated-paste
    basis before chemistry adjustment.
  soil_tds_sat: Total dissolved solids concentration for the current layer after summing ion
    concentrations.
  soil_ece: Electrical conductivity equivalent derived from `soil_TDS_sat` and `salt_tds_ec`.
  a_val: Crop salinity threshold read from `salt_stress_a(idp)` and possibly adjusted for
    gypsiferous soil.
  b_val: Crop salinity slope read from `salt_stress_b(idp)` and used to scale the reduction
    factor above threshold.
  depth: Cumulative soil depth below land surface used to stop salinity processing below the
    root zone.
uses:
  plant_data_module: The plant database supplies the species-specific aeration tolerance.
    `pl_waterup` uses `pldb(idp)%aeration` to convert profile saturation excess into the air-stress
    factor `pcom(j)%plstr(ipl)%strsa`.
  basin_module: The basin-level state exposes the HRU soil water profile and salinity control
    settings used to decide whether stress is computed at all and how salinity is translated
    into uptake reduction.
  hru_module: The HRU module provides the active HRU index, plant index, potential transpiration
    demand, uptake-distribution parameters, and urban land-use flag that shape the water-uptake
    calculation.
  soil_module: The soil module supplies per-HRU profile storage, field-capacity and saturation
    totals, layer geometry, and layer water storage. `pl_waterup` needs those values to distribute
    demand by depth, cap uptake by availability, and write the remaining water back to the
    profile.
  plant_module: The plant module holds the current plant’s status, growth, and stress records.
    `pl_waterup` reads root depth, compensation factor, and plant identifiers from `pcom`,
    then writes layer uptake and stress factors back into `pcom(j)%plcur` and `pcom(j)%plstr`
    for later growth routines.
  urban_data_module: The packet shows `use urban_data_module`, but no direct urban-state reference
    was extracted. If the source is authoritative, this module is likely present for urban
    land-use support around `hru(j)%luse%urb_lu`, but that linkage is not visible in the extracted
    refs.
  constituent_mass_module: The constituent-mass module gates the salinity pathway. `cs_db%num_salts`
    determines whether salt ions are simulated and whether the routine loops over `cs_soil(j)%ly(k)%saltc(isalt)`
    and computes salinity stress.
  salt_data_module: The salt-data module holds the global salinity controls and ion concentration
    scratch array. `pl_waterup` uses these values to convert layer salt concentrations into
    plant stress through `soil_salt_conc`, `salt_stress_a/b`, `salt_tds_ec`, and `salt_soil_type`.
---

<!-- facts:header -->

Distributes each plant’s potential water uptake through rooted soil layers, limits it by available layer water, updates actual transpiration, and applies optional salinity stress.

## Bottom Line

`pl_waterup` runs for the current HRU/plant combination and converts potential transpiration demand into layer-by-layer water uptake. It first computes aeration stress when the profile is wetter than field capacity, then builds a rooted uptake distribution, caps uptake by each layer’s stored water, writes the per-layer uptake back to `pcom(j)%plcur(ipl)%uptake`, and accumulates the day’s actual transpiration in `ep_day`.

When salinity simulation is enabled, the routine also derives soil-solution salt concentration for each rooted layer, calls `salt_chem_soil_single` to adjust chemistry, computes salinity-based uptake reduction, and stores the minimum salinity stress in `pcom(j)%plstr(ipl)%strss`. The resulting `strsw`, `strsa`, and `strss` values are then available to downstream plant growth routines as the day’s stress factors.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pl_waterup` runs during plant community processing, once per growing plant in `pl_community` after the current HRU, plant, soil profile, and plant status records are already selected. Its outputs feed later daily plant-growth calculations by supplying `pcom(j)%plstr(ipl)%strsa`, `pcom(j)%plstr(ipl)%strsw`, `pcom(j)%plstr(ipl)%strss`, per-layer uptake, and `ep_day`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and plant record | Copies `ihru` into `j` and reads the current plant ID from `pcom(j)%plcur(ipl)%idplt` so all subsequent calculations operate on the active HRU and plant. |
| 2. Compute aeration stress when the profile is wetter than field capacity | Checks whether `soil(j)%sw` exceeds `soil(j)%sumfc`; if so, computes `satco`, `scparm`, and sets `pcom(j)%plstr(ipl)%strsa` from the plant’s aeration tolerance `pldb(idp)%aeration`. |
| 3. Initialize water-uptake accumulation and salinity state | If potential transpiration is nonzero, resets the rooted-profile bookkeeping variables, clears `pcom(j)%plcur(ipl)%uptake(:)`, and initializes salinity reduction tracking before the layer loop starts. |
| 4. Walk each soil layer in the profile | Loops over `k = 1, soil(j)%nly`, stops early after the rooted zone is passed, and sets `gx` to the smaller of the root depth and the current layer bottom depth. |
| 5. Compute cumulative potential uptake with depth | Uses `epmax(ipl)`, `uptake%water_dis`, and `uptake%water_norm` to calculate cumulative potential uptake `sum` at the current depth; shallow roots fall back to a simple normalization when root depth is near zero. |
| 6. Convert cumulative uptake to a layer demand with compensation | Derives `wuse` from the current cumulative uptake and the previous layer’s `sump`; the second soil layer is special-cased so compensation is disabled there. |
| 7. Limit uptake by available layer water and by total demand | Reads urban land use, caps `wuse` by the current layer storage `soil(j)%phys(k)%st`, accumulates `sum_wuse`, and trims the layer uptake if total uptake would exceed `epmax(ipl)`. |
| 8. Apply salinity stress when salt simulation is enabled | If `salt_tol_sim` is on and salts are present within the rooted zone, converts dissolved salts to concentration, calls `salt_chem_soil_single` after setting `soil_salt_conc`, computes layer EC, and updates the minimum reduction factor `reduc_salt_min`. |
| 9. Remove taken water from the layer and store layer uptake | Subtracts the actual layer uptake from `soil(j)%phys(k)%st`, keeping a small positive floor, and writes the final layer uptake to `pcom(j)%plcur(ipl)%uptake(k)`. |
| 10. Recompute profile water storage | Rebuilds `soil(j)%sw` by summing the updated layer storages after the layer loop finishes. |
| 11. Save plant salinity stress and actual transpiration | Sets `pcom(j)%plstr(ipl)%strss` to the minimum salinity reduction when salt simulation is active, stores the actual water-use fraction in `pcom(j)%plstr(ipl)%strsw`, and adds actual uptake to `ep_day`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%aeration` |
| [sym:basin_module] | `soil, pldb, cs_db, cs_soil, soil_salt_conc, salt_stress_a, salt_stress_b, salt_tol_sim, salt_tds_ec, salt_soil_type` | `soil(j)%sw, soil(j)%sumfc, soil(j)%sumul, soil(j)%nly, soil(j)%phys(k)%d, soil(j)%phys(k)%st, soil(j)%phys(k)%thick, soil(j)%phys(k)%ul, pldb(idp)%aeration, cs_db%num_salts, cs_soil(j)%ly(k)%saltc(isalt), soil_salt_conc(isalt), salt_stress_a(idp), salt_stress_b(idp), salt_tol_sim, salt_tds_ec, salt_soil_type` |
| [sym:hru_module] | `uptake, hru, epmax, ihru, ipl, ep_day` | `uptake%water_norm, uptake%water_dis, hru(j)%luse%urb_lu` |
| [sym:soil_module] | `soil` | `soil(j)%sw, soil(j)%sumfc, soil(j)%sumul, soil(j)%nly, soil(j)%phys(k)%d, soil(j)%phys(k)%st, soil(j)%phys(k)%thick, soil(j)%phys(k)%ul` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plstr(ipl)%strsa, pcom(j)%plstr(ipl)%strsw, pcom(j)%plcur(ipl)%uptake(:), pcom(j)%plg(ipl)%root_dep, pcom(j)%plcur(ipl)%epco, pcom(j)%plcur(ipl)%uptake(k), pcom(j)%plstr(ipl)%strss` |
| [sym:urban_data_module] | `situation unclear; no candidate outside references were resolved to this module in the packet` |  |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts` |
| [sym:salt_data_module] | `soil_salt_conc, salt_stress_a, salt_stress_b, salt_tol_sim, salt_tds_ec, salt_soil_type` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plstr(ipl)%strsa` | When `soil(j)%sw > soil(j)%sumfc` | The routine writes the plant’s aeration stress factor from the soil saturation excess and the species aeration tolerance. This only changes on wet profiles where the layer water exceeds field capacity. |
| `pcom(j)%plstr(ipl)%strsw` | When `epmax(ipl) > 1.e-6` and the layer loop runs | At the end of the uptake calculation, this becomes `sum_wuse / epmax(ipl)`, the fraction of potential transpiration actually met by soil water. It changes only for active plants with non-negligible potential demand. |
| `pcom(j)%plcur(ipl)%uptake(:)` | When `epmax(ipl) > 1.e-6` before the soil-layer loop | The routine clears the per-layer uptake array to zero before refilling it with the day’s actual uptake distribution. |
| `soil_salt_conc(isalt)` | When `salt_tol_sim.eq.1` and `cs_db%num_salts > 0` for a rooted layer | The routine sets each ion’s concentration for the current layer from `cs_soil(j)%ly(k)%saltc(isalt)` scaled by `theta_w`, then may let `salt_chem_soil_single` adjust those concentrations before salinity stress is computed. |
| `soil(j)%phys(k)%st` | After `wuse` is finalized for the current layer | The routine subtracts actual water uptake from the layer’s stored water, leaving at least `1.e-6`. This updates the layer water balance for later processes. |
| `pcom(j)%plcur(ipl)%uptake(k)` | After the current layer’s actual uptake is determined | The routine stores the layer’s actual water uptake so downstream plant routines can see how much water came from each soil layer. |
| `soil(j)%sw` | When the layer loop completes | The routine recomputes total profile soil water as the sum of updated layer storage, so the HRU-wide soil water state matches the modified layers. |
| `pcom(j)%plstr(ipl)%strss` | When salinity simulation is active at the end of the layer loop | The routine stores the minimum layer salinity reduction as the plant’s salt-stress factor. If salinity is off or no salts are simulated, it remains 1. |
| `ep_day` | When `epmax(ipl) > 1.e-6` | The routine adds the day’s actual plant water uptake to the HRU evapotranspiration total. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.2.1 | Cumulative potential water uptake by depth | $w_{up,z}=\frac{E_t}{[1-exp(-\beta_w)]}*[1-exp(-\beta_w*\frac{z}{z_{root}})]$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:125). sum = epmax*(1-Exp(-water_dis*gx/root_dep))/water_norm` — water uptake depth dist |
| 5:2.2.2 | Layer potential water uptake | $w_{up,ly}=w_{up,zl}-w_{up,zu}$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:133). wuse = sum - sump*(1.-epco)` — layer difference |
| 5:2.2.3 | Compensated layer water uptake | $w'_{up,ly}=w_{up,ly}+w_{demand}*epco$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:133). epco demand compensation (same line) |
| 5:2.2.4 | Low-water exponential reduction branch | $w''_{up,ly}=w'_{up,ly}*exp[5*(\frac{SW_{ly}}{(.25*AWC_{ly})}-1)]$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:133). theory's SW<0.25·AWC exponential water-stress reduction removed; SWAT+ uses epco layer compensation |
| 5:2.2.5 | No-reduction branch above 25% AWC | $w''_{up,ly}=w'_{up,ly}$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:133). complementary branch (SW≥0.25·AWC) |
| 5:2.2.7 | Actual layer water uptake | $w_{actualup,ly}=min\lfloor w''_{up,ly},(SW_{ly}-WP_{ly})\rfloor$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:139). wuse = amin1(wuse, st) |
| 5:2.2.8 | Total actual water uptake | $w_{actualup}=\sum^n_{ly=1} w_{actualup,ly}$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:141). sum_wuse = sum_wuse + wuse |
| 5:2.2.9 | Actual transpiration equals actual uptake | $E_{t,act}=w_{actualup}$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:144). capped at `epmax` = E_t,act |
| 5:3.1.1 | Water stress factor | $wstrs=1-\frac{E_{t,act}}{E_t}=1-\frac{w_{actualup}}{E_t}$ | Verified against SWAT+ 62.0.0 (pl_waterup.f90:230). strsw = wuse_sum/epmax` complement |

## Lineage

`pl_waterup.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_waterup.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `889136d` (2025-02-03) — Fix typos
- `452ba2b` (2024-12-13) — commited out hardcoded pcom(j)plcur(ipl)%epco
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_waterup' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
