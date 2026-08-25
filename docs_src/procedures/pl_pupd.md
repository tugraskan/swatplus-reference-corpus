---
kind: procedure
symbol: pl_pupd
title: pl_pupd
status: filled
source_hash: 59fab221a96d93ac
version_label: SWAT+ 62.0.0
locals:
  idp: Plant database index for the currently active plant in the HRU; it is taken from `pcom(j)%plcur(ipl)%idplt`
    and then used to look up species parameters in `pldb` and `plcp`.
  j: HRU index copied from `ihru`; it selects the current hydrologic response unit community
    and mass records that the routine updates.
  matur_frac: Fraction of maturity used in the phosphorus-fraction curve. For perennials it
    is computed from current-year maturity relative to years to maturity; for annuals it uses
    accumulated heat-unit fraction `phuacc`.
uses:
  plant_data_module: '`plant_data_module` provides the plant lookup tables that define which
    plant is active and how its phosphorus fraction should evolve. `pldb(idp)%typ` decides
    whether maturity is based on perennial year fraction or annual heat-unit accumulation,
    `pldb(idp)%pltpfr1` and `pldb(idp)%pltpfr3` set the upper and lower phosphorus-fraction
    limits, and `plcp(idp)%pup2` supplies the curve shape parameter used in the exponential
    term.'
  hru_module: '`hru_module` holds the shared HRU-level working arrays that this routine writes
    for the current plant slot. `ihru` and `ipl` identify the active HRU and plant within
    that HRU, while `up2` and `uapd` receive the computed optimal phosphorus amount and demand
    so later HRU nutrient routines can use them.'
  plant_module: '`plant_module` contains the plant-community state being updated here. `pcom(j)%plcur(ipl)%idplt`
    identifies the plant species, `pcom(j)%plcur(ipl)%phuacc` supplies annual maturity progress,
    and `pcom(j)%plm(ipl)%p_fr` is the phosphorus fraction field that this routine recalculates
    for the active plant biomass.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the above-ground biomass
    and existing above-ground phosphorus mass used to compute demand. `pl_mass(j)%ab_gr(ipl)%m`
    scales the optimal phosphorus content by current above-ground biomass, and `pl_mass(j)%ab_gr(ipl)%p`
    is the current above-ground phosphorus amount used both as a minimum floor and in the
    final demand difference.'
---

<!-- facts:header -->

Computes the plant phosphorus demand state for the current HRU plant using maturity-dependent P fraction and above-ground biomass.

## Bottom Line

`pl_pupd` updates the active plant’s phosphorus fraction at maturity progression, then converts that fraction into an optimal above-ground phosphorus amount and a demand term. It is part of the plant nutrient-demand workflow, so its results feed the HRU-level P uptake accounting used later in plant growth and soil nutrient routines.

The routine has no explicit arguments; it relies on current HRU/plant state, plant parameter tables, and biomass mass storage. It distinguishes perennial from annual plants when computing maturity fraction, applies the SWAT+ phosphorus uptake curve, and enforces a floor so the optimal P content is never below existing above-ground plant P.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `pl_nut_demand` after that routine has advanced `pcom(j)%plcur(ipl)%phuacc` and `phuacc_p` and called `pl_nupd`. Its outputs populate the current plant’s phosphorus-fraction state and the HRU P demand arrays, which downstream nutrient uptake and growth logic use to total demand and allocate soil phosphorus.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select maturity basis | The routine gets the active plant id from the current HRU plant record, then chooses the maturity fraction source based on plant type. Perennials use current-year maturity divided by years to maturity; annuals use accumulated heat-unit fraction. |
| 2. compute plant P fraction | It evaluates the SWAT+ phosphorus-fraction curve for the active plant, using species limits from `pldb` and shape parameters from `plcp`, and stores the result in the plant mass phosphorus fraction field `pcom(j)%plm(ipl)%p_fr`. |
| 3. compute optimal P mass | The routine multiplies the updated phosphorus fraction by above-ground biomass to get optimal above-ground phosphorus content, then raises that value to at least the current above-ground phosphorus mass if the curve estimate is lower. |
| 4. compute P demand | It subtracts current above-ground phosphorus from the optimal amount to get plant phosphorus demand, then applies the 1.5 multiplier used for luxury uptake demand. |
| 5. return | The routine exits after updating the plant phosphorus fraction and HRU demand state for the active plant. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb, plcp` | `pldb(idp)%typ, pldb(idp)%pltpfr1, pldb(idp)%pltpfr3, plcp(idp)%pup2` |
| [sym:hru_module] | `up2, uapd, ihru, ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plm(ipl)%p_fr` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%ab_gr(ipl)%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plm(ipl)%p_fr` | When the active plant record is processed for the current HRU, after maturity fraction is determined. | `pcom(j)%plm(ipl)%p_fr` is overwritten with the maturity-dependent phosphorus fraction computed from the plant’s species parameters. This gives the current plant a P fraction that varies over growth stage instead of staying at a fixed value. |
| `up2(ipl)` | After `pcom(j)%plm(ipl)%p_fr` is computed, for the active HRU plant slot. | `up2(ipl)` is set to the optimal above-ground phosphorus mass implied by the current P fraction and above-ground biomass. If that estimate is smaller than existing above-ground P, it is raised to the current P mass so demand cannot go negative. |
| `uapd(ipl)` | Immediately after `up2(ipl)` is finalized for the active plant. | `uapd(ipl)` becomes the plant phosphorus demand above current content, then is scaled by 1.5 to represent luxury uptake demand used by later nutrient allocation logic. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.3.19 | Optimal phosphorus fraction in biomass | $fr_P=(fr_{P,1}-fr_{P,3})*[1-\frac{fr_{PHU}}{fr_{PHU}+exp(p_1-p_2*fr_{PHU})}]+fr_{P,3}$ | Verified against SWAT+ 62.0.0 (pl_pupd.f90:57). P-fraction maturity curve (pltpfr1/3, pup1/pup2) |
| 5:2.3.22 | Optimal plant phosphorus mass | $bio_{P,opt}=fr_P*bio$ | up2 = p_fr * above-ground biomass. The printed theory page uses total biomass, while SWAT+ uses above-ground biomass here. |
| 5:2.3.23 | Phosphorus demand | $P_{up}=1.5*Min \begin{cases} bio_{P,opt}-bio_P \\ 4*fr_{P,3}* \Delta bio \end {cases}$ | Verified against SWAT+ 62.0.0 (pl_pupd.f90:64). uapd = 1.5*uapd` luxury P uptake; Min at :61-63 |
| 5:2.4.8 | Phosphorus fraction used for optimal growth and yield state | $yld_P=fr_P*yld$ | SWAT+ tracks the maturity-varying plant P fraction through p_fr and up2, with above-ground biomass and luxury uptake handling rather than a separate yld_P = fr_P*yld expression. |

## Lineage

Source-backed lineage commits were resolved for `pl_pupd`. The initial addition in `df07e3f` created the subroutine and its phosphorus-demand logic. `39fabde` only initialized local variables `idp`, `j`, and `matur_frac` to zero/0.0. `889136d` corrected a documentation typo in the inline comment for the second shape parameter. `bed51b1` changed the phosphorus-demand calculation from total biomass/total P to above-ground biomass/above-ground P and removed the older total-biomass `uapd` calculation block.

- `df07e3f` introduced `pl_pupd` as the plant phosphorus-demand routine, including the maturity-based P-fraction equation and the initial above-ground demand calculation path.
- `39fabde` made the local variables safely initialized at declaration, but did not change the model equations or state updates.
- `889136d` updated only a comment spelling issue and did not affect behavior.
- `bed51b1` changed behavior by replacing total-biomass/total-P demand calculations with above-ground biomass and above-ground phosphorus mass, altering both `up2` and `uapd` results used by downstream uptake logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_pupd' has no extracted documentation comment.
