---
kind: procedure
symbol: se_reactions_soil
title: se_reactions_soil
status: filled
source_hash: 8ca563d7e2c1c238
version_label: SWAT+ 62.0.0
args:
  j: Selects which soil reaction-parameter record in `cs_rct_soil` supplies the oxygen level,
    inhibition factor, and shale-linked rate constants for this call.
  jj: Unused control argument; it only exists so the caller can match the shared reaction
    interface, and the routine uses `if (jj < 0) continue` to suppress an unused-variable
    warning.
  conc_rg: 'Carries the current Runge-Kutta stage concentrations for the three modeled species:
    SeO4, SeO3, and NO3. The routine reads these values to compute reaction rates and concentration
    changes.'
  k_rg: Provides the Runge-Kutta slope array where this stage’s changes are written. The routine
    stores the computed deltas in column `k_slope` for SeO4, SeO3, and NO3.
  k_slope: Selects which Runge-Kutta stage column of `k_rg` this call updates, so each stage
    can keep its own set of concentration changes.
locals:
  kk: Loop index over shale formations in `cs_rct_soil(j)`; it steps through each geologic
    shale source when accumulating oxygen and nitrate reduction terms.
  cseo4: Holds the current SeO4 concentration copied from `conc_rg(1)` for use in reduction-rate
    calculations.
  cseo3: Holds the current SeO3 concentration copied from `conc_rg(2)` for use in reduction-rate
    calculations.
  no3inhib: Computes the nitrate-inhibition multiplier that reduces selenium reduction rates
    when NO3 is present.
  seo4red: Stores the instantaneous selenate reduction rate, based on `kseo4`, SeO4 concentration,
    and nitrate inhibition.
  seo3red: Stores the instantaneous selenite reduction rate, based on `kseo3`, SeO3 concentration,
    and nitrate inhibition.
  dseo4: Holds the net change in SeO4 after subtracting selenate reduction and adding shale-driven
    selenium release terms.
  dseo3: Holds the net change in SeO3, treated as the SeO4 reduction gain minus SeO3 reduction
    loss.
  dno3: Holds the NO3 concentration change; it is the negative of the accumulated nitrate
    reduction rate.
  cno3: Holds the current NO3 concentration copied from `conc_rg(3)` for use in inhibition
    and reduction-rate calculations.
  o2: Stores dissolved oxygen concentration for the HRU soil reaction object, taken from `cs_rct_soil(j)%oxy_soil`.
  o2red: Holds the oxygen-reduction rate for the current shale layer; it is used to estimate
    selenium release from shale.
  no3red: Accumulates nitrate reduction across all shale layers, then drives NO3 loss and
    selenium production from shale.
  yseo4_o2: Conversion factor linking oxygen reduction to selenium release on the SeO4 scale.
  yseo4_no3: Conversion factor linking nitrate reduction to selenium release on the SeO4 scale.
  se_prod_o2: Accumulates selenium produced from shale due to oxygen reduction across all
    shale formations.
  se_prod_no3: Accumulates selenium produced from shale due to nitrate reduction across all
    shale formations.
  ko2a: Temporary copy of the shale-specific oxygen-reduction rate constant for the current
    `kk` layer.
  kno3: Temporary copy of the shale-specific nitrate-reduction rate constant for the current
    `kk` layer.
  sseratio: Temporary copy of the shale sulfur/selenium ratio used to convert shale oxidation/reduction
    effects into selenium-release terms.
uses:
  cs_data_module: '`cs_data_module` supplies the reaction-parameter store that makes the routine
    stateful across HRUs and geologic layers. The procedure reads `cs_rct_soil(j)%oxy_soil`,
    `se_ino3`, `kseo4`, `kseo3`, and the shale-layer arrays `ko2a`, `shale`, `kno3a`, and
    `sseratio`, plus `num_geol_shale` to know how many shale layers to traverse.'
---

<!-- facts:header -->

Computes selenium reaction-rate changes for one soil HRU and one Runge-Kutta slope.

## Bottom Line

`se_reactions_soil` evaluates selenium redox reactions for a single soil reaction object `j` at one Runge-Kutta stage `k_slope`. It reads the current stage concentrations from `conc_rg`, applies inhibition and shale-driven release terms from `cs_rct_soil`, and stores the resulting concentration changes in `k_rg` for the RK integrator.

The routine combines selenate reduction to selenite, selenite reduction to elemental selenium, nitrate inhibition, and shale-associated oxygen/nitrate reduction contributions. Its outputs feed the `cs_rctn_hru` Runge-Kutta update that advances selenium species concentrations in the HRU soil system.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the HRU selenium reaction workflow after `cs_rctn_hru` has assembled the stage concentration vector `conc_rg` for a Runge-Kutta step. `cs_rctn_hru` calls it repeatedly for slopes 1 through 4, and the resulting `k_rg` entries are then used by the surrounding Runge-Kutta update to advance soil SeO4, SeO3, and NO3 concentrations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. ignore unused jj | The routine executes a no-op conditional on `jj` so the shared interface argument is referenced, but the value does not affect the reaction calculations. |
| 2. load species concentrations | Copies SeO4, SeO3, and NO3 from `conc_rg`, then loads dissolved oxygen from the soil reaction parameters for HRU `j`. These are the concentration inputs used to evaluate the rate laws. |
| 3. compute nitrate inhibition and Se reduction | Builds the nitrate-inhibition factor and uses it to calculate selenate and selenite reduction rates from the HRU-specific rate constants and current concentrations. |
| 4. initialize shale-driven totals | Sets fixed conversion factors and zeros the accumulated nitrate-reduction and selenium-production totals before traversing the shale layers. |
| 5. loop over shale layers | For each shale formation, reads the layer-specific oxygen and nitrate reduction constants, applies them to the current dissolved oxygen and nitrate concentrations, and accumulates shale-driven selenium release terms. |
| 6. form net concentration changes | Combines shale-driven selenium production with SeO4/SeO3 reduction losses to compute the net changes for SeO4, SeO3, and NO3. |
| 7. write RK slope outputs | Stores the three net concentration changes into the `k_rg` column selected by `k_slope`, making the results available to the Runge-Kutta integrator. |
| 8. return | Ends the procedure after the slope vector has been filled for the current Runge-Kutta stage. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:cs_data_module] | `cs_rct_soil, num_geol_shale` | `cs_rct_soil(j)%oxy_soil, cs_rct_soil(j)%se_ino3, cs_rct_soil(j)%kseo4, cs_rct_soil(j)%kseo3, cs_rct_soil(j)%ko2a(kk), cs_rct_soil(j)%shale(kk), cs_rct_soil(j)%kno3a(kk), cs_rct_soil(j)%sseratio(kk)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one commit that introduced `se_reactions_soil`: bd18ad4 added the entire subroutine in `src/se_reactions_soil.f90` along with its selenium reaction logic and Runge-Kutta slope storage. No later resolved diff in the provided lineage evidence changed this procedure.

- bd18ad4 introduced the complete `se_reactions_soil` implementation, including nitrate-inhibited SeO4/SeO3 reduction, shale-layer accumulation, and writing the resulting deltas into `k_rg`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- `jj` is explicitly marked unused in the source; the routine keeps it only to satisfy the shared reaction-call interface.
