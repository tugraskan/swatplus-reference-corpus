---
kind: procedure
symbol: mgt_plantop
title: mgt_plantop
status: filled
source_hash: f789aedc8d3b3e7c
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the working HRU index. The routine sets `j = ihru` and then uses `j` as the array
    index for `pcom` and `pl_mass` entries tied to the current HRU.'
  min: '`min` is declared but not used in the extracted body. The only depth comparison uses
    the intrinsic `Min(...)` on `soil(ihru)%zmx` and `plt_zmx`.'
  plt_zmx: '`plt_zmx` holds the plant’s maximum rooting depth expressed in millimeters. The
    routine computes it from the plant database rooting depth (`pldb(... )%rdmx`) and uses
    it to cap `soil(ihru)%zmx`.'
uses:
  hru_module: '`hru_module` provides the current HRU and plant indices (`ihru` and `ipl`).
    Those indices select which community and plant records this operation resets for the active
    management step.'
  soil_module: '`soil_module` matters because the routine updates the active HRU soil profile
    depth (`soil(ihru)%zmx`). That depth limit must reflect the plant’s maximum rooting depth
    so later root-zone-dependent calculations do not assume deeper soil access than the plant
    can use.'
  plant_module: '`plant_module` stores the active plant community state that this routine
    resets: growth status, dormancy, accumulated heat units, growth ET counters, harvest-index
    adjustment fields, and plant stress. The routine edits these values so the current plant
    starts the operation in a consistent growth state.'
  plant_data_module: '`plant_data_module` is needed because the routine reads the plant database
    entry for the current plant (`pldb(pcom(j)%plcur(ipl)%idplt)%rdmx`) to determine the maximum
    rooting depth used in the soil-depth cap.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the organic mass records
    that are zeroed here. The routine assigns `orgz` into the active plant biomass containers
    so total, above-ground, leaf, stem, seed, and root pools start from a zero-mass state.'
---

<!-- facts:header -->

Initializes plant-operation state for the current HRU and plant, then constrains the soil rooting depth to the plant’s maximum rooting depth.

## Bottom Line

`mgt_plantop` is a reset-and-setup routine for a plant operation. It marks the current plant as growing, clears dormancy and accumulated heat units, zeroes several plant growth and biomass bookkeeping variables, and copies the default plant stress state into the active community state.

It then computes the plant’s maximum rooting depth from the plant database and limits the HRU soil profile depth to that value. This keeps later plant and soil calculations aligned with the root zone available for the current plant.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during planting/plant-operation scheduling after `mgt_sched` has selected the current HRU/plant operation and set the active plant as growing. Its results prepare the plant community and soil-root-depth state for subsequent growth, stress, and harvest-related calculations that depend on the active plant status, biomass pools, and root-zone limit.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Copy the current HRU index into the local working index. | The routine sets `j = ihru` so later updates use the active HRU’s plant-community and biomass arrays. |
| 2. Mark the current plant as actively growing and not dormant. | It sets `gro` to `"y"`, `idorm` to `"n"`, and clears accumulated heat units (`phuacc = 0.`) for the active plant. |
| 3. Clear the active plant’s biomass mass records. | The routine assigns the zero organic mass record `orgz` to total, above-ground, leaf, stem, seed, and root mass containers for the current plant. |
| 4. Clear plant growth bookkeeping counters. | It resets plant ET counters and growth transition flags (`plet`, `plpet`, `laimxfr`, `hi_adj`, `olai`, `dphu`) to zero. |
| 5. Reset the root mass scalar and stress state. | The routine zeroes `pl_mass(j)%root(ipl)%m` and copies the default plant stress template `plstrz` into the active plant’s stress state. |
| 6. Read the plant’s maximum rooting depth from the plant database. | It converts the plant database rooting depth from meters to millimeters by multiplying `pldb(pcom(j)%plcur(ipl)%idplt)%rdmx` by 1000. |
| 7. Limit the HRU soil rooting depth to the plant maximum. | The routine replaces `soil(ihru)%zmx` with the smaller of the current soil depth and the plant’s maximum rooting depth. |
| 8. Return to the caller. | The subroutine ends after updating the active plant and soil state for the management operation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `ihru, ipl` |  |
| [sym:soil_module] | `soil` | `soil(ihru)%zmx` |
| [sym:plant_module] | `pcom, plstrz` | `pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%plet, pcom(j)%plg(ipl)%plpet, pcom(j)%plg(ipl)%laimxfr, pcom(j)%plg(ipl)%hi_adj, pcom(j)%plg(ipl)%olai, pcom(j)%plg(ipl)%dphu, pcom(j)%plstr(ipl)` |
| [sym:plant_data_module] | `plant_data_module` | `pldb` |
| [sym:organic_mineral_mass_module] | `pl_mass, orgz` | `pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%seed(ipl), pl_mass(j)%root(ipl), pl_mass(j)%root(ipl)%m` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plcur(ipl)%gro` | When the routine runs for the active HRU/plant, after `j = ihru`. | `pcom(j)%plcur(ipl)%gro` is forced to `"y"` so the current plant is treated as growing for the rest of the management sequence. |
| `pcom(j)%plcur(ipl)%idorm` | When the routine runs for the active HRU/plant. | `pcom(j)%plcur(ipl)%idorm` is forced to `"n"` to clear dormancy and keep the plant in an active-growth state. |
| `pcom(j)%plcur(ipl)%phuacc` | When the routine runs for the active HRU/plant. | `pcom(j)%plcur(ipl)%phuacc` is reset to zero so the accumulated plant heat-unit fraction restarts at the planting/operation point. |
| `pl_mass(j)%tot(ipl)` | Unconditionally during the reset block. | `pl_mass(j)%tot(ipl)` is overwritten with `orgz`, clearing the plant’s total organic mass inventory for the active plant record. |
| `pl_mass(j)%ab_gr(ipl)` | Unconditionally during the reset block. | `pl_mass(j)%ab_gr(ipl)` is overwritten with `orgz` to clear above-ground biomass mass. |
| `pl_mass(j)%leaf(ipl)` | Unconditionally during the reset block. | `pl_mass(j)%leaf(ipl)` is overwritten with `orgz` to clear leaf biomass mass. |
| `pl_mass(j)%stem(ipl)` | Unconditionally during the reset block. | `pl_mass(j)%stem(ipl)` is overwritten with `orgz` to clear stem biomass mass. |
| `pl_mass(j)%seed(ipl)` | Unconditionally during the reset block. | `pl_mass(j)%seed(ipl)` is overwritten with `orgz` to clear seed biomass mass. |
| `pl_mass(j)%root(ipl)` | Unconditionally during the reset block. | `pl_mass(j)%root(ipl)` is overwritten with `orgz` to clear the root mass container before the root scalar is set separately. |
| `pcom(j)%plg(ipl)%plet` | Unconditionally during the reset block. | `pcom(j)%plg(ipl)%plet` is set to zero so plant-life actual ET accumulation restarts. |
| `pcom(j)%plg(ipl)%plpet` | Unconditionally during the reset block. | `pcom(j)%plg(ipl)%plpet` is set to zero so plant-life potential ET accumulation restarts. |
| `pcom(j)%plg(ipl)%laimxfr` | Unconditionally during the reset block. | `pcom(j)%plg(ipl)%laimxfr` is set to zero as part of clearing plant growth transfer bookkeeping for the current operation. |
| `pcom(j)%plg(ipl)%hi_adj` | Unconditionally during the reset block. | `pcom(j)%plg(ipl)%hi_adj` is set to zero so no prior harvest-index adjustment carries into the new plant state. |
| `pcom(j)%plg(ipl)%olai` | Unconditionally during the reset block. | `pcom(j)%plg(ipl)%olai` is set to zero to clear the onset-of-decline leaf-area marker. |
| `pcom(j)%plg(ipl)%dphu` | Unconditionally during the reset block. | `pcom(j)%plg(ipl)%dphu` is set to zero to clear the heat-unit threshold marker for leaf-area decline. |
| `pl_mass(j)%root(ipl)%m` | Unconditionally during the reset block. | `pl_mass(j)%root(ipl)%m` is set to zero so the scalar root mass is explicitly cleared after the root mass record is reset. |
| `pcom(j)%plstr(ipl)` | Unconditionally during the reset block. | `pcom(j)%plstr(ipl)` is replaced with `plstrz`, restoring the default plant stress state for the current plant. |
| `soil(ihru)%zmx` | Always after the rooting-depth calculation. | `soil(ihru)%zmx` is reduced, if necessary, to the plant’s maximum rooting depth so the soil root-zone limit cannot exceed the crop’s rooting capability. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `mgt_plantop`. The initial addition commit introduced the subroutine, its module uses, documentation header, and the full reset-and-root-depth logic. A later commit only initialized the local variables `j` and `plt_zmx` to zero without changing the routine’s behavior.

- df07e3f added `mgt_plantop` with the plant-operation reset logic, biomass zeroing, stress reset, and soil root-depth capping.
- 39fabde only initialized `j` and `plt_zmx` in the declaration block; it did not alter the subroutine’s algorithm.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_plantop' has no extracted documentation comment.
- plant_data_module is used through `pldb` in the source body, but the context packet did not provide a resolved outside-reference table for that module; the outside_state entry names `pldb` from the source use.
