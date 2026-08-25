---
kind: procedure
symbol: rsd_decomp
title: rsd_decomp
status: filled
source_hash: e8636d4a56857600
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index copied from `ihru` and used to access the HRU's plant, soil, residue,
    and output state.
  idp: Plant database identifier for the current plant (`pcom(j)%plcur(ipl)%idplt`), used
    to look up `pldb(idp)%rsdco_pl`.
  xx: Temporary scratch value for the combined factor calculation and temperature-factor equation.
  csf: Combined residue decay factor from soil temperature and soil water; multiplied into
    the residue decay rate.
  cnr: Current residue carbon-to-nitrogen ratio computed from `pl_mass(j)%rsd(ipl)%c / pl_mass(j)%rsd(ipl)%n`.
  cnrf: Reduction factor derived from C:N ratio; limits decomposition when residue is N-poor.
  cpr: Current residue carbon-to-phosphorus ratio computed from `pl_mass(j)%rsd(ipl)%c / pl_mass(j)%rsd(ipl)%p`.
  cprf: Reduction factor derived from C:P ratio; limits decomposition when residue is P-poor.
  ca: Chemical limitation factor chosen as the minimum of `cnrf`, `cprf`, and 1.0.
  decr: Daily decay fraction for the current plant residue after applying chemical and environmental
    limits.
  cdg: Soil temperature factor computed from the surface-layer temperature response curve.
  sut: Soil water factor computed from surface-layer storage relative to field capacity.
uses:
  plant_data_module: '`pldb` supplies the plant-specific residue decomposition coefficient
    that scales the daily decay fraction for each plant''s surface residue.'
  basin_module: '`bsn_prm%decr_min` sets the minimum allowed daily residue decay so decomposition
    does not drop below the basin-wide floor.'
  organic_mineral_mass_module: This module owns the residue and soil organic/mineral mass
    pools that `rsd_decomp` reads, updates, and summarizes while transferring decomposed residue
    into soil nitrogen, phosphorus, and carbon pools.
  hru_module: '`ihru` selects the active HRU and `ipl` is the loop index over plants in that
    HRU, so both are needed to address the current community member.'
  soil_module: Surface soil temperature and water status control whether decomposition happens
    and how strongly it proceeds through the temperature and water response factors.
  plant_module: '`pcom` provides the number of plants in the HRU community and the plant-status
    record used to map each plant to its database residue coefficient.'
  output_landscape_module: '`hnb_d` stores the HRU-scale residue nutrient transfer totals
    that this routine accumulates for reporting and balance tracking.'
  carbon_module: '`hrc_d` records the carbon loss from surface residue decay so the HRU carbon
    budget reflects the amount of residue carbon mineralized here.'
---

<!-- facts:header -->

Computes daily surface residue decomposition and associated N and P mineralization for each plant in an HRU. It uses soil temperature, soil water, residue chemistry, and plant-specific decay coefficients to update residue pools and residue-balance outputs.

## Bottom Line

`rsd_decomp` steps through each plant in the current HRU and, when the surface soil is above freezing, computes a decay fraction for that plant's surface residue from temperature, water, C:N ratio, C:P ratio, and the plant database residue decomposition coefficient. It then removes that fraction from the plant residue pool and transfers the mineralized nitrogen and phosphorus to soil nitrate, active humus, and labile P pools.

The routine also accumulates residue-derived N and P in the landscape nutrient-balance outputs and carbon loss in the HRU carbon-loss output, then rebuilds the total surface residue amount for the HRU. Its results feed the rest of the daily residue/nutrient bookkeeping used by HRU control.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`rsd_decomp` runs during HRU control after the day’s plant/soil state has been prepared and before later nutrient-mineralization steps. In `hru_control`, it is called in the CSWAT residue-decomposition branch (`bsn_cc%cswat == 0`) before `nut_nminrl`, and its residue, nutrient, and carbon updates are then available to downstream daily HRU accounting and output variables.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU outputs | Copies the active HRU index from `ihru` into `j`, then clears the residue-derived N and P output totals for this HRU before any plant-by-plant updates. |
| 2. loop over plants | Iterates over each plant in the HRU community using `pcom(j)%npl`, because decomposition is computed separately for each plant's surface residue pool. |
| 3. require thawed surface soil | Skips decomposition unless the surface soil temperature is above 0 C, so residue mineralization only proceeds in unfrozen conditions. |
| 4. compute C:N limitation | Calculates the residue C:N ratio from `pl_mass(j)%rsd(ipl)` and converts it to `cnrf`; if residue N is too small, the factor is set to 1.0, and the ratio is capped at 500 to avoid extreme suppression. |
| 5. compute C:P limitation | Calculates the residue C:P ratio and converts it to `cprf`; if residue P is too small, the factor is set to 1.0, and the ratio is capped at 5000 to avoid extreme suppression. |
| 6. compute soil water factor | Ensures soil storage is nonnegative, then computes a moisture response from surface water relative to field capacity and bounds it to a minimum of 0.05. |
| 7. compute soil temperature factor | Applies the temperature response curve to surface soil temperature and enforces a minimum factor of 0.1. |
| 8. combine environmental factors | Multiplies temperature and water factors, constrains the result to a valid range, takes its square root as `csf`, and selects the most limiting chemical factor in `ca`. |
| 9. derive daily decay rate | Looks up the plant's residue coefficient from `pldb(idp)%rsdco_pl`, multiplies it by the chemical and environmental factors, then bounds the daily decay fraction between `bsn_prm%decr_min` and 1.0. |
| 10. transfer decomposed residue | Computes the decomposed residue mass in `decomp`, subtracts it from the plant residue pool, and sends 80% of the released N and P to mineral/labile pools and 20% to active humus pools. |
| 11. record carbon loss and residue nutrients | Adds decomposed carbon to `hrc_d(j)%rsd_surfdecay_c` and accumulates the residue-derived N and P transfers in `hnb_d(j)`. |
| 12. finish plant loop | Ends the thaw check and advances to the next plant, repeating the residue-decomposition calculation for every plant in the community. |
| 13. rebuild total surface residue | Resets `pl_mass(j)%rsd_tot` to `plt_mass_z` and sums all plant residue pools into the HRU total surface residue mass. |
| 14. return | Returns to the caller after updating residue pools, soil pools, carbon loss, and residue-balance outputs for the HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%rsdco_pl` |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%decr_min` |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1, decomp, plt_mass_z` | `pl_mass(j)%rsd(ipl)%n, pl_mass(j)%rsd(ipl)%c, pl_mass(j)%rsd(ipl)%p, pl_mass(j)%rsd(ipl), soil1(j)%mn(1)%no3, decomp%n, soil1(j)%hact(1)%n, soil1(j)%mp(1)%lab, decomp%p, soil1(j)%hact(1)%p, decomp%c, pl_mass(j)%rsd_tot` |
| [sym:hru_module] | `ihru, ipl` |  |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%tmp, soil(j)%phys(1)%st, soil(j)%phys(1)%fc` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%rsdco_pl` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%rsd_nitorg_n, hnb_d(j)%rsd_laborg_p` |
| [sym:carbon_module] | `hrc_d` | `hrc_d(j)%rsd_surfdecay_c` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%rsd_nitorg_n` | When surface soil temperature is above freezing for the active HRU and plant-specific residue is present. | Accumulates the daily amount of nitrogen released from decomposing surface residue and routed to nitrate plus active organic pools, for HRU nutrient-balance reporting. |
| `hnb_d(j)%rsd_laborg_p` | When surface soil temperature is above freezing for the active HRU and plant-specific residue is present. | Accumulates the daily amount of phosphorus released from decomposing surface residue and routed to labile plus active organic pools, for HRU nutrient-balance reporting. |
| `decomp` | When the current plant's surface residue meets the freezing, chemistry, and decay-rate checks. | Holds the mass of residue carbon, nitrogen, and phosphorus decomposed for the current plant before those components are distributed to soil pools. |
| `pl_mass(j)%rsd(ipl)` | When the current plant's residue decays under warm-soil conditions. | Loses the computed decomposed fraction, reducing the plant's remaining surface residue mass and nutrient content. |
| `soil1(j)%mn(1)%no3` | When decomposed residue nitrogen is transferred in the warm-soil branch. | Gains 80% of the decomposed residue nitrogen as nitrate in the surface soil mineral pool. |
| `soil1(j)%hact(1)%n` | When decomposed residue nitrogen is transferred in the warm-soil branch. | Gains 20% of the decomposed residue nitrogen as active humus nitrogen in the surface soil pool. |
| `soil1(j)%mp(1)%lab` | When decomposed residue phosphorus is transferred in the warm-soil branch. | Gains 80% of the decomposed residue phosphorus as labile mineral phosphorus in the surface soil pool. |
| `soil1(j)%hact(1)%p` | When decomposed residue phosphorus is transferred in the warm-soil branch. | Gains 20% of the decomposed residue phosphorus as active humus phosphorus in the surface soil pool. |
| `hrc_d(j)%rsd_surfdecay_c` | When residue carbon is decomposed for a plant. | Increases by 42% of decomposed residue carbon to record the carbon lost from surface residue decay in the HRU carbon budget. |
| `pl_mass(j)%rsd_tot` | After all plant residues in the HRU have been updated. | Is rebuilt as the sum of the zero baseline `plt_mass_z` plus all current plant residue pools, so the HRU has an updated total surface residue mass. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `rsd_decomp`. The initial addition in `ee1b472` introduced the procedure and its residue-decomposition logic. Commit `914687a` changed the residue redistribution from a multiplicative decay on litter pools to explicit `decomp` transfers into soil pools and output accumulators. Commit `72206bc` then refocused the routine from layered soil residue processing to surface residue processing by switching the loop to `pcom(j)%npl`, using `pl_mass(j)%rsd(ipl)`, and tightening the soil-temperature/moisture logic around the surface layer.

- `ee1b472` added the new subroutine with daily residue decomposition, environmental response factors, nutrient mineralization, and HRU output accumulation.
- `914687a` changed the implementation to move decomposed mass explicitly into soil nitrogen, phosphorus, and carbon pools while recording residue carbon loss and residue nutrient transfers.
- `72206bc` reworked the routine to operate on surface residue by plant in the community rather than layered soil residue, and updated the module imports and local indices accordingly.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rsd_decomp' has no extracted documentation comment.
- algorithm_steps revised: aligned steps to the visible source lines and the resolved lineage, including the final surface-residue total rebuild.
