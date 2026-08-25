---
kind: procedure
symbol: cbn_rsd_transfer
title: cbn_rsd_transfer
status: filled
source_hash: 69f28cf32acf044f
version_label: SWAT+ 62.0.0
locals:
  j: HRU index used to select the current landscape and soil/plant state; it is set from `ihru`
    and used to address all HRU-specific arrays.
  k: Soil-layer counter for walking through each layer in `soil(j)%nly` and updating layer-specific
    residue and humus pools.
  decr: Scalar transfer multiplier for the residue move; here it is fixed at 1.0, so the routine
    transfers the full residue amount rather than a partial fraction.
  ipl: Plant-community index used to visit each plant in `pcom(j)%npl` and transfer that plant’s
    residue from the matching `soil1` slot.
  idp: Plant-data index taken from `pcom(j)%plcur(ipl)%idplt`; it selects the belowground
    partition fractions for the current plant type.
uses:
  septic_data_module: '`ihru` chooses which HRU is being updated, and `hnb_d` holds the HRU-level
    nutrient-balance fields that this routine clears before the transfer so downstream output
    can report the residue-driven nitrogen and phosphorus fluxes.'
  basin_module: '`soil` provides the number of soil layers and the layer temperature gate
    that determines whether transfer is allowed, while `pcom` provides the number of plants
    in the community and the plant ID needed to pick the correct residue partition fractions.'
  organic_mineral_mass_module: '`soil1` stores the residue and humus pools that are directly
    modified by the transfer, and `transfer` is the temporary organic-mass object used to
    move the full residue amount into the target pools.'
  hru_module: '`organic_mineral_mass_module` defines the residue and organic-mass types used
    by these nested fields, so it matters because the routine subtracts and adds whole `organic_mass`
    records rather than separate scalars.'
  soil_module: '`ihru` is the active HRU pointer supplied by the HRU control flow, so it anchors
    the routine’s index selection for all HRU-specific state updates.'
  plant_module: '`soil` matters because its layer count drives the outer loop and its layer
    temperature decides whether residue transfer is allowed for that layer.'
  plant_data_module: '`pcom` matters because it determines how many plants are processed in
    the HRU and which plant data entry supplies the residue partition fractions for each plant.'
  output_landscape_module: '`plant_data_module` supplies the belowground metabolic, structural,
    and lignin fractions used to split the transferred residue into the soil organic pools
    for the current plant type.'
---

<!-- facts:header -->

Moves all unfrozen subsurface plant residue in the current HRU into the soil metabolic, structural, and lignin pools, using lignin-based partition fractions for belowground material. It also resets several HRU nutrient-balance counters so the transfer can be tracked for output.

## Bottom Line

`cbn_rsd_transfer` runs inside the HRU control sequence to handle subsurface residue carbon transfer when the soil is above freezing. For each soil layer and each plant in the community, it takes the residue mass stored in `soil1(j)%pl(ipl)%rsd(k)`, removes that amount from the residue pools, and adds the transferred mass and carbon to the soil `meta`, `str`, and `lig` pools using belowground partition fractions from `cswat_1_part_fracs(idp)`.

The routine also zeroes the HRU-level residue transfer counters in `hnb_d(j)` before accumulating results. Those values are what later landscape/output accounting uses to report residue-derived nitrogen and phosphorus movement, while the updated `soil1` pools become the starting point for later soil carbon transformations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cbn_rsd_transfer` is called from `hru_control` after surface residue decomposition and before later soil carbon/nitrogen transformations. In the `bsn_cc%cswat == 2` branch, `hru_control` has already established the active HRU (`ihru`) and the community state, and the results from this routine feed the subsequent carbon-pool and nutrient-balance behavior that uses `soil1` and `hnb_d`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU counters | The routine selects the current HRU with `j = ihru` and clears the HRU nutrient-balance accumulators in `hnb_d(j)` so residue-driven fluxes start from zero for this time step. |
| 2. loop over soil layers | It visits each soil layer in the current HRU, because residue transfer is tracked separately by layer. |
| 3. loop over plants | For each soil layer, it visits every plant in the HRU plant community so each plant’s residue can be transferred using its own plant type fractions. |
| 4. gate on frozen soil | Residue transfer only proceeds when the layer temperature is above freezing; if the soil is frozen, the plant residue in that layer is left unchanged. |
| 5. choose plant data fractions | The current plant type ID is copied from `pcom(j)%plcur(ipl)%idplt` into `idp` so the routine can look up the correct belowground partition fractions. |
| 6. move full residue mass | The transfer factor is set to 1.0, the whole residue mass is copied into `transfer`, and that amount is removed from both `soil1(j)%pl(ipl)%rsd(k)` and the layer total `soil1(j)%rsd_tot(k)`. |
| 7. zero tiny residue remnants | After subtraction, any residue `m`, `c`, `n`, or `p` component that falls below the underflow threshold is forced to zero to avoid runtime underflow issues. |
| 8. add transferred mass to humus pools | The transferred residue is split into metabolic, structural, and lignin pools using `cswat_1_part_fracs(idp)` belowground fractions, and the corresponding `meta`, `str`, and `lig` pools in `soil1(j)` are incremented by that amount. |
| 9. return to caller | The subroutine ends after updating all eligible layers and plants; later carbon and nutrient accounting routines use the modified `soil1` and `hnb_d` state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `hnb_d, ihru` | `hnb_d(j)%act_nit_n, hnb_d(j)%org_lab_p, hnb_d(j)%act_sta_n, hnb_d(j)%denit, hnb_d(j)%rsd_nitorg_n, hnb_d(j)%rsd_laborg_p; ihru` |
| [sym:basin_module] | `soil, pcom` | `soil(j)%nly, soil(j)%phys(k)%tmp; pcom(j)%npl, pcom(j)%plcur(ipl)%idplt` |
| [sym:organic_mineral_mass_module] | `soil1, transfer` | `soil1(j)%pl(ipl)%rsd(k), soil1(j)%rsd_tot(k), soil1(j)%pl(ipl)%rsd(k)%m, soil1(j)%pl(ipl)%rsd(k)%c, soil1(j)%pl(ipl)%rsd(k)%n, soil1(j)%pl(ipl)%rsd(k)%p, soil1(j)%meta(k), soil1(j)%str(k), soil1(j)%lig(k)` |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(k)%tmp` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt` |
| [sym:plant_data_module] | `cswat_1_part_fracs` | `cswat_1_part_fracs(idp)%meta_frac_blg, cswat_1_part_fracs(idp)%str_frac_blg, cswat_1_part_fracs(idp)%lig_frac_blg` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%act_nit_n, hnb_d(j)%org_lab_p, hnb_d(j)%act_sta_n, hnb_d(j)%denit, hnb_d(j)%rsd_nitorg_n, hnb_d(j)%rsd_laborg_p` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%act_nit_n` | At the start of the routine for the active HRU `j = ihru`. | `hnb_d(j)%act_nit_n` is reset to zero so later accumulation of active-organic-to-nitrate nitrogen starts cleanly for this HRU and time step. |
| `hnb_d(j)%org_lab_p` | At the start of the routine for the active HRU `j = ihru`. | `hnb_d(j)%org_lab_p` is reset to zero so later accounting of organic-to-labile phosphorus begins from a clean slate. |
| `hnb_d(j)%act_sta_n` | At the start of the routine for the active HRU `j = ihru`. | `hnb_d(j)%act_sta_n` is reset to zero before any later active-to-stable nitrogen movement is summed. |
| `hnb_d(j)%denit` | At the start of the routine for the active HRU `j = ihru`. | `hnb_d(j)%denit` is reset to zero so denitrification accounting for this HRU is not contaminated by earlier values. |
| `hnb_d(j)%rsd_nitorg_n` | At the start of the routine for the active HRU `j = ihru`. | `hnb_d(j)%rsd_nitorg_n` is reset to zero before residue-derived nitrogen movement is recorded. |
| `hnb_d(j)%rsd_laborg_p` | At the start of the routine for the active HRU `j = ihru`. | `hnb_d(j)%rsd_laborg_p` is reset to zero before residue-derived phosphorus movement is recorded. |
| `transfer` | When a soil layer is above freezing (`soil(j)%phys(k)%tmp > 0.`). | `transfer` is set to the full current residue mass for the current plant-layer combination, and it is then used as the quantity moved from residue into the soil organic pools. |
| `soil1(j)%pl(ipl)%rsd(k)` | When a soil layer is above freezing (`soil(j)%phys(k)%tmp > 0.`). | `soil1(j)%pl(ipl)%rsd(k)` loses the transferred residue mass, leaving only any residue not moved by the routine; its components are then clamped to zero if they become tiny. |
| `soil1(j)%rsd_tot(k)` | When a soil layer is above freezing (`soil(j)%phys(k)%tmp > 0.`). | `soil1(j)%rsd_tot(k)` is reduced by the same transferred residue amount so the layer total residue pool stays consistent with the plant-level residue removal. |
| `soil1(j)%meta(k)` | When a soil layer is above freezing and a plant type has been selected. | `soil1(j)%meta(k)` gains the belowground metabolic fraction of the transferred residue mass and carbon. |
| `soil1(j)%str(k)` | When a soil layer is above freezing and a plant type has been selected. | `soil1(j)%str(k)` gains the belowground structural fraction of the transferred residue mass and carbon. |
| `soil1(j)%lig(k)` | When a soil layer is above freezing and a plant type has been selected. | `soil1(j)%lig(k)` gains the belowground lignin fraction of the transferred residue mass and carbon. |

## File I/O

<!-- facts:io -->


## Lineage

Five resolved commits changed `cbn_rsd_transfer`. The initial addition in 69e06ad created the routine to move subsurface residue into soil organic pools and hook it into `hru_control`. 053ed0d then removed unused variables and dropped the `isep` import. a3ae724 changed the transfer so `soil1(j)%rsd_tot(k)` is reduced when residue is moved into `meta`, `str`, and `lig`. f40b513 fixed the `ipl` declaration and introduced run-away total N/P guard variables, but the diff shown here only exposes the type correction and new locals. bc7755a removed the local `nactfr` variable and its initialization.

- 69e06ad established `cbn_rsd_transfer` as a new HRU routine that transfers residue into soil organic pools and added its call from `hru_control`.
- 053ed0d trimmed unused local state and simplified the `hru_module` dependency to `ihru` only.
- a3ae724 made the residue transfer also subtract from `soil1(j)%rsd_tot(k)`, keeping the layer total residue pool consistent with the per-plant residue removal.
- f40b513 corrected `ipl` to an integer and added local tracking variables for start/end nutrient totals, though the shown diff does not reveal any further logic changes.
- bc7755a removed the unused local active-fraction variable `nactfr` and its constant assignment.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cbn_rsd_transfer' has no extracted documentation comment.
- algorithm_steps revised: condensed the source walk into 9 model steps that match the visible line-numbered logic and include the residue-total update and final return.
- Source evidence for `septic_data_module` and `basin_module` showed imports only; no specific resolved component references were available in the packet.
- The lineage summary is based only on resolved diffs in the provided Git Lineage Evidence section.
