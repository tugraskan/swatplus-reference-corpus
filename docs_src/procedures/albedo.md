---
kind: procedure
symbol: albedo
title: albedo
status: filled
source_hash: 71da2c2e2af2162b
version_label: SWAT+ 62.0.0
locals:
  cej: '`cej` is the fixed exponential coefficient used to build the soil cover index. It
    is set to `-5.e-5` and multiplied by the cover mass term before the exponential is taken.'
  eaj: '`eaj` is the computed soil-cover weighting factor for albedo. It is `Exp(cej * (cover
    + .1))`, so it converts biomass/residue cover into a 0-to-1 style blend factor between
    plant and soil reflectance.'
  j: '`j` stores the current HRU index. The routine copies `ihru` into `j` and then uses `j`
    to read the current HRU, soil, plant, and mass state for that one HRU.'
  cover: '`cover` holds the surface cover mass used to compute `eaj`. In the current code
    it is the sum of above-ground community mass and total fresh surface residue mass for
    the selected HRU.'
uses:
  hru_module: '`hru_module` provides the current HRU list, the active HRU index, and the output
    variable `albday`. The snow-water amount in `hru(j)%sno_mm` decides whether the routine
    uses bare soil/vegetation albedo or the snow albedo branch, and `albday` is the value
    this routine updates for later model use.'
  soil_module: '`soil_module` supplies the soil surface albedo used as the bare-ground reflectance
    baseline. The routine reads `soil(j)%ly(1)%alb` because the top soil layer controls the
    exposed soil albedo when snow is absent or when the vegetation blend is computed.'
  plant_module: '`plant_module` supplies the canopy density indicator `pcom(j)%lai_sum`. That
    value determines whether the routine applies the plant/soil mixing formula; without leaf
    area, the code leaves `albday` at the bare-soil value.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the biomass and residue
    masses used to estimate cover. The routine combines `pl_mass(j)%ab_gr_com%m` and `pl_mass(j)%rsd_tot%m`
    to form `cover`, which controls the exponential cover factor `eaj` and therefore how strongly
    vegetation masks soil albedo.'
---

<!-- facts:header -->

Computes the daily HRU albedo used by the radiation balance. It blends bare-soil reflectance with a plant/residue cover term, and raises albedo to a snow value when snowpack is present.

## Bottom Line

`albedo` updates the daily HRU surface albedo (`albday`) from the current snow depth, soil surface albedo, and a vegetation/residue cover index. It is a small climate-surface routine: if snow is shallow or absent, it uses soil albedo alone or a soil/plant blend; if snow exceeds the threshold, it forces a high snow albedo.

The routine matters because `albday` feeds the HRU energy balance and short-wave radiation response for the day. `hru_control` calls it after daily HRU state setup so the rest of the model can use the updated reflectance for that HRU.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the HRU daily control flow after `hru_control` has selected the active HRU and prepared the day’s HRU state. Its output, `albday`, is then available to later daily HRU calculations that depend on the surface short-wave reflectance used in the climate/energy balance.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select current HRU | Copy the active HRU index from `ihru` into the local index `j` so the routine works on the current HRU’s state. |
| 2. set cover coefficient | Assign the fixed negative coefficient `-5.e-5` to `cej`; this coefficient scales the exponential cover response. |
| 3. compute surface cover mass | Form `cover` as above-ground community mass plus total fresh surface residue mass for the current HRU. This is the mass basis for the albedo cover index. |
| 4. compute cover weighting | Calculate `eaj = Exp(cej * (cover + .1))`, turning cover mass into an exponential weighting factor used to blend plant and soil albedo. |
| 5. test snow threshold | Check whether snow water on the HRU is at or below the shallow-snow threshold of 0.5 mm. If so, use soil/vegetation albedo logic; otherwise, use snow albedo. |
| 6. assign bare-soil albedo | Set `albday` to the top-soil layer albedo `soil(j)%ly(1)%alb`, establishing the baseline exposed-soil reflectance for snow-free conditions. |
| 7. blend plant and soil albedo when LAI exists | If `pcom(j)%lai_sum > 0.`, replace the bare-soil value with a weighted mix: `0.23 * (1. - eaj) + soil(j)%ly(1)%alb * eaj`. This shifts albedo toward the plant value when cover is low and toward soil albedo as cover increases. |
| 8. assign snow albedo | When snow is above the threshold, force `albday` to 0.8, representing a high-reflectance snow surface. |
| 9. return | Return to the caller after `albday` has been updated for the current HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru, albday` | `hru(j)%sno_mm` |
| [sym:soil_module] | `soil` | `soil(j)%ly(1)%alb` |
| [sym:plant_module] | `pcom` | `pcom(j)%lai_sum` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%rsd_tot%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `albday` | If `hru(j)%sno_mm <= .5`, `albday` is first set to `soil(j)%ly(1)%alb` and may be overwritten by the plant/soil blend when `pcom(j)%lai_sum > 0.`; otherwise `albday` is set to `0.8`. | `albday` is the daily HRU surface albedo, so this routine changes it to match the day’s snow cover and surface cover conditions before later energy-balance calculations use it. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:1.2.14 | Bare-soil albedo | $\alpha=\alpha_{soil}$ | When snow is absent, albday = soil(j)%ly(1)%alb. |
| 1:1.2.15 | Plant/soil albedo | $\alpha=\alpha_{plant} (1-cov_{sol})+\alpha_{soil} cov_{sol}$ | If LAI is present, albday = 0.23*(1-eaj) + soil albedo*eaj. |
| 1:1.2.16 | Soil cover index for albedo | $cov_{sol}=exp(-5.0X10^{-5}*CV)$ | eaj = Exp(-5e-5*(cover + 0.1)), with cover from above-ground biomass and residue. |

## Lineage

Four resolved commits changed `albedo`. The original addition in `df07e3f` introduced the routine and its three-way albedo logic. `39fabde` initialized the local variables `cej`, `eaj`, `j`, and `cover` to zero. `eb22103` changed the cover term from `rsd1(j)%tot_com%m` to `soil1(j)%rsd(1)%m`. `72206bc` changed that cover term again from `soil1(j)%rsd(1)%m` to `pl_mass(j)%rsd_tot%m`.

- df07e3f added `albedo` as a new HRU daily albedo routine with snow, bare-soil, and plant/soil blend branches.
- 39fabde initialized `cej`, `eaj`, `j`, and `cover` at declaration, replacing uninitialized local declarations.
- eb22103 updated the cover calculation to use `soil1(j)%rsd(1)%m` instead of `rsd1(j)%tot_com%m`.
- 72206bc updated the cover calculation to use `pl_mass(j)%rsd_tot%m` instead of `soil1(j)%rsd(1)%m`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'albedo' has no extracted documentation comment.
