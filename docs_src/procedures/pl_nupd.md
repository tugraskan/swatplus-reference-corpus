---
kind: procedure
symbol: pl_nupd
title: pl_nupd
status: filled
source_hash: fd7e408a182fc875
version_label: SWAT+ 62.0.0
locals:
  j: HRU-local index copied from `ihru`; it selects which HRU/community entry in `pcom`, `pl_mass`,
    `un2`, and `uno3d` is being updated.
  idp: Plant identifier for the current HRU plant, taken from `pcom(j)%plcur(ipl)%idplt`;
    it indexes the species-specific plant database and plant coefficients used in the nitrogen
    equation.
  matur_frac: Fraction of maturity used in the nitrogen fraction curve. For perennials it
    is computed from current-year maturity over years to maturity; for annuals it comes from
    accumulated heat-unit fraction `phuacc`.
uses:
  plant_data_module: '`plant_data_module` supplies the species-level nitrogen parameters and
    plant type that determine the maturity-dependent nitrogen fraction. `pldb(idp)%typ` decides
    whether the maturity fraction comes from heat units or years, `pldb(idp)%pltnfr1` and
    `pldb(idp)%pltnfr3` bound the fraction at emergence and maturity, and `plcp(idp)%nup2`
    shapes the curve used to compute `pcom(j)%plm(ipl)%n_fr`.'
  hru_module: '`hru_module` holds the HRU and plant-demand work arrays that this routine reads
    and updates. `ihru` and `ipl` locate the active HRU plant, while `un2(ipl)` and `uno3d(ipl)`
    receive the computed nitrogen demand and nitrogen deficiency for that plant.'
  plant_module: '`plant_module` carries the per-plant status and biomass state for the active
    community member. `pcom(j)%plcur(ipl)%idplt` identifies the plant species, `pcom(j)%plcur(ipl)%phuacc`
    supplies the annual maturity fraction, and `pcom(j)%plm(ipl)%n_fr` stores the optimal
    plant nitrogen fraction computed here for later growth and nutrient calculations.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the current plant nitrogen
    mass used as the floor for demand. `pl_mass(j)%tot(ipl)%m` is the total biomass multiplier
    for the optimal fraction, and `pl_mass(j)%tot(ipl)%n` is the actual plant N mass that
    `un2(ipl)` cannot fall below.'
---

<!-- facts:header -->

Computes the current plant nitrogen fraction for the active HRU plant and turns that into plant N demand and deficiency.

## Bottom Line

`pl_nupd` is a small helper routine that updates the active plant’s optimal nitrogen fraction based on its species parameters and how far it is through maturity. It then multiplies that fraction by total plant biomass to estimate optimal plant nitrogen mass.

The routine compares that optimal nitrogen mass with the plant’s actual nitrogen mass, stores the larger value as the day’s demand in `un2(ipl)`, and stores the shortfall in `uno3d(ipl)`. Those results feed later plant-nutrient demand and uptake logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after `pl_nut_demand` has updated the plant’s heat-unit accumulation for the current HRU and before `pl_pupd` and the HRU-level nitrogen deficit totals are updated. Its outputs, `pcom(j)%plm(ipl)%n_fr`, `un2(ipl)`, and `uno3d(ipl)`, are then used by later plant nutrient and growth behavior to track nitrogen demand and deficiency.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load the active HRU plant context. | Copy the current HRU index from `ihru` into local `j`, then use `pcom(j)%plcur(ipl)%idplt` to identify which plant species is active. |
| 2. Choose maturity basis by plant type. | If the plant is perennial, compute `matur_frac` as current-year maturity divided by years to maturity; otherwise use the accumulated heat-unit fraction `pcom(j)%plcur(ipl)%phuacc` for annuals. |
| 3. Compute optimal plant N fraction. | Evaluate the maturity-dependent nitrogen-fraction curve using `pldb(idp)%pltnfr1`, `pldb(idp)%pltnfr3`, `plcp(idp)%nup1`, and `plcp(idp)%nup2`, then store the result in `pcom(j)%plm(ipl)%n_fr`. |
| 4. Convert fraction to optimal N mass. | Multiply the computed fraction by total plant biomass from `pl_mass(j)%tot(ipl)%m` to get the optimal daily nitrogen amount and store it in `un2(ipl)`. |
| 5. Enforce minimum at actual plant N mass. | If the computed optimal N mass is below the plant’s actual N mass `pl_mass(j)%tot(ipl)%n`, replace it with that actual mass so demand does not drop below existing N. |
| 6. Compute nitrogen deficiency. | Subtract the plant’s actual N mass from `un2(ipl)` and save the difference in `uno3d(ipl)` as the HRU plant nitrogen deficiency. |
| 7. Return to the caller. | Exit after updating the plant fraction, demand, and deficiency state for the current HRU plant. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb, plcp` | `pldb(idp)%typ, pldb(idp)%pltnfr1, pldb(idp)%pltnfr3, plcp(idp)%nup2` |
| [sym:hru_module] | `un2, uno3d, ihru, ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plm(ipl)%n_fr` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%tot(ipl)%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plm(ipl)%n_fr` | When the maturity fraction and species parameters have been read for the current active plant. | `pcom(j)%plm(ipl)%n_fr` is overwritten with the maturity-dependent optimal nitrogen fraction for the current plant, replacing the previous value so later routines can use the updated nitrogen target. |
| `un2(ipl)` | When the optimal nitrogen fraction has been multiplied by total biomass. | `un2(ipl)` is set to the plant’s optimal nitrogen mass demand, but it is raised to at least the plant’s actual nitrogen mass if the computed optimum is lower than the current N content. |
| `uno3d(ipl)` | When `un2(ipl)` has been finalized against actual plant nitrogen mass. | `uno3d(ipl)` is set to the excess of optimal nitrogen demand over actual plant nitrogen mass, representing the day’s nitrogen deficiency used by later HRU plant-demand logic. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.3.1 | Optimal nitrogen fraction in biomass | $fr_N=(fr_{N,1}-fr_{N,3})*[1-\frac{fr_{PHU}}{fr_{PHU}+exp(n_1-n_2*fr_{PHU})}]+fr_{N,3}$ | Verified against SWAT+ 62.0.0 (pl_nupd.f90:52). N-fraction maturity curve `(nfr1-nfr3)*(1-mf/(mf+Exp(nup1-nup2*mf)))+nfr3 |
| 5:2.3.4 | Optimal plant nitrogen mass | $bio_{N,opt}=fr_N*bio$ | un2 = n_fr * total plant biomass. |
| 5:2.3.5 | Nitrogen demand | $N_{up}=Min \begin{cases} bio_{N,opt}-bio_N \\ 4*fr_{N,3}* \Delta bio \end {cases}$ | Demand is first computed as un2 - plant N, then capped in pl_biomass_gro by 4*pltnfr3*bioday. The printed min() form is therefore distributed across two routines. |
| 5:2.4.7 | Nitrogen fraction used for optimal growth and yield state | $yld_N=fr_N*yld$ | SWAT+ tracks the maturity-varying whole-plant N fraction through n_fr and un2. It does not separately compute yld_N = fr_N*yld inside the growth routine. |

## Lineage

Two source-backed commits were resolved. `df07e3f` added the new `pl_nupd.f90` subroutine with the nitrogen-demand calculation and accompanying documentation comments. `39fabde` did not change the algorithm; it only initialized the local variables `j`, `idp`, and `matur_frac` with default values.

- `df07e3f` introduced `pl_nupd` as a new routine that computes plant nitrogen demand from maturity fraction, plant parameters, and biomass, and stores the result in `pcom(j)%plm(ipl)%n_fr`, `un2(ipl)`, and `uno3d(ipl)`.
- `39fabde` changed only local variable initialization (`j = 0`, `idp = 0`, `matur_frac = 0.`) without changing the nitrogen-demand equations or state updates.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_nupd' has no extracted documentation comment.
