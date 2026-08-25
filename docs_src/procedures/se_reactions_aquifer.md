---
kind: procedure
symbol: se_reactions_aquifer
title: se_reactions_aquifer
status: filled
source_hash: 4bdb99fcc7627ac0
version_label: SWAT+ 62.0.0
args:
  iaq: '`iaq` selects which aquifer''s reaction-parameter record in `cs_rct_aqu` supplies
    the oxygen, inhibition, and shale-reaction coefficients used for this calculation.'
  conc_rg: '`conc_rg` provides the current trial concentrations for this Runge-Kutta slope:
    selenate in element 1, selenite in element 2, and nitrate in element 3.'
  k_rg: '`k_rg` is the Runge-Kutta slope array that this routine fills for the selected slope
    index with computed concentration changes for SeO4, SeO3, and NO3.'
  k_slope: '`k_slope` tells the routine which Runge-Kutta pass it is computing, so the resulting
    reaction rates are stored in the correct row of `k_rg`.'
locals:
  kk: Loop index over geologic shale units inside the aquifer reaction calculation.
  cseo4: Working copy of the trial selenate concentration taken from `conc_rg(1)`.
  cseo3: Working copy of the trial selenite concentration taken from `conc_rg(2)`; it is read
    from input but not used later in the shown source.
  no3inhib: Nitrate-inhibition factor applied to selenate reduction, reducing the selenate
    reduction rate when nitrate is present.
  seo4red: Computed rate of selenate reduction to selenite for the current aquifer and slope.
  dseo4: Net change in selenate after adding selenium produced from shale oxidation and subtracting
    selenate reduced to selenite.
  dseo3: Net change in selenite; here it is set equal to the amount of reduced selenate that
    becomes selenite.
  dno3: Net change in nitrate concentration; it is the negative of the total nitrate reduction
    rate.
  cno3: Working copy of the trial nitrate concentration taken from `conc_rg(3)`.
  o2: Groundwater dissolved oxygen concentration for the selected aquifer, used as the oxidant
    in shale reaction rates.
  o2red: Per-shale-unit oxygen reduction rate contribution computed from oxygen, a kinetic
    constant, and shale fraction.
  no3red: Accumulated nitrate reduction rate across all shale-bearing geologic units.
  yseo4_o2: Stoichiometric conversion factor from oxygen oxidation of shale sulfur to selenium
    production.
  yseo4_no3: Stoichiometric conversion factor from nitrate-driven oxidation of shale sulfur
    to selenium production.
  se_prod_o2: Accumulated selenium production attributed to oxygen-driven shale oxidation.
  se_prod_no3: Accumulated selenium production attributed to nitrate-driven shale oxidation.
  ko2a: Temporary storage for the oxygen-reduction rate constant of the current shale unit.
  kno3: Temporary storage for the nitrate-reduction rate constant of the current shale unit.
  sseratio: Temporary storage for the sulfur-to-selenium ratio of the current shale unit,
    used to convert shale oxidation into selenium release.
uses:
  cs_data_module: The routine depends on `cs_data_module` because it reads all aquifer-specific
    reaction settings and the number of shale-bearing geologic formations from module state
    rather than from its argument list. `cs_rct_aqu(iaq)` provides the kinetic constants,
    oxygen level, nitrate inhibition, and shale properties that control the rate calculations,
    and `num_geol_shale` sets the loop over shale units.
---

<!-- facts:header -->

Simulates selenium redox reactions in one aquifer for a single Runge-Kutta slope. It computes changes in selenate, selenite, and nitrate from groundwater chemistry and shale-mediated oxidation/reduction.

## Bottom Line

This subroutine takes the current aquifer-state concentrations for one reaction evaluation and turns them into reaction-rate changes for selenium and nitrate. It uses aquifer-specific reaction parameters from `cs_rct_aqu(iaq)` and the current groundwater concentrations to compute how much selenate is reduced to selenite, how much selenium is produced from shale oxidation, and how much nitrate is consumed.

The results are written into `k_rg(k_slope,1:3)` so the caller can use them as one slope of the Runge-Kutta integration. In practice, `cs_rctn_aqu` calls this routine repeatedly with different trial concentrations to build the full aquifer chemistry update.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the aquifer reaction step when `cs_rctn_aqu` is building the Runge-Kutta slopes for groundwater chemistry. `cs_rctn_aqu` prepares the trial concentration vector `conc_rg` from the current slope estimate before calling this routine, and the returned values in `k_rg` feed the later Runge-Kutta concentration update for aquifer selenium and nitrate reactions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load the trial species concentrations from `conc_rg`. | The routine copies the current Runge-Kutta trial concentrations for selenate, selenite, and nitrate into local working variables so the rate equations use the slope-specific state. |
| 2. Read aquifer dissolved oxygen from module state. | It pulls the groundwater oxygen concentration for aquifer `iaq` from `cs_rct_aqu`, because oxygen controls shale oxidation in the aquifer reaction rates. |
| 3. Compute nitrate inhibition and selenate reduction. | The code forms a nitrate-inhibition factor from the aquifer's inhibition parameter and current nitrate concentration, then computes the selenate-to-selenite reduction rate. |
| 4. Initialize shale-driven production factors. | It sets stoichiometric conversion factors and clears the accumulated shale-driven nitrate reduction and selenium-production totals before processing shale formations. |
| 5. Loop over each shale-bearing geologic formation. | For each shale unit, the routine pulls that unit's oxygen and nitrate reaction constants and sulfur-to-selenium ratio, computes oxygen and nitrate reduction on shale, and accumulates selenium released by those redox processes. |
| 6. Form the net concentration changes. | It combines selenium produced from shale oxidation with selenium lost to reduction to get the net selenate change, sets selenite gain equal to the reduced selenate, and makes nitrate change the negative of the total nitrate reduction rate. |
| 7. Store the slope results and return. | The routine writes the computed changes into the requested row of `k_rg` for the current Runge-Kutta slope and then exits. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:cs_data_module] | `cs_rct_aqu, num_geol_shale` | `cs_rct_aqu(iaq)%oxy_aqu, cs_rct_aqu(iaq)%se_ino3, cs_rct_aqu(iaq)%kseo4, cs_rct_aqu(iaq)%ko2a(kk), cs_rct_aqu(iaq)%shale(kk), cs_rct_aqu(iaq)%kno3a(kk), cs_rct_aqu(iaq)%sseratio(kk)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one commit affecting this routine: d70017a added `se_reactions_aquifer.f90` with the full subroutine implementation, including the aquifer oxygen read, nitrate-inhibition selenate reduction, shale-driven oxygen and nitrate reduction loop, and storing the three reaction deltas into `k_rg`.

- d70017a introduced the procedure and its behavior: aquifer-specific selenium reduction chemistry, shale-mediated selenium production, nitrate consumption, and Runge-Kutta slope storage in `k_rg`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- algorithm_steps revised: expanded the two-step draft into seven source-backed steps to reflect the actual computation flow in the routine.
