---
kind: procedure
symbol: cs_sorb_aqu
title: cs_sorb_aqu
status: filled
source_hash: f771d51fcb260825
version_label: SWAT+ 62.0.0
locals:
  iaq: Aquifer index for the current hydrologic object; taken from `ob(icmd)%num` and used
    to read and update the matching aquifer-state arrays.
  iaqdb: Index of the aquifer database record for the current object; taken from `ob(icmd)%props`
    and used to fetch aquifer depth and specific yield.
  mass_seo4_sol: Current dissolved selenium-4 mass in groundwater, in mg, before and after
    the equilibrium sorption update.
  mass_seo3_sol: Current dissolved selenium-3 mass in groundwater, in mg, before and after
    the equilibrium sorption update.
  mass_born_sol: Current dissolved boron mass in groundwater, in mg, before and after the
    equilibrium sorption update.
  mass_seo4_sorb: Current sorbed selenium-4 mass associated with aquifer material, in mg,
    before and after the equilibrium sorption update.
  mass_seo3_sorb: Current sorbed selenium-3 mass associated with aquifer material, in mg,
    before and after the equilibrium sorption update.
  mass_born_sorb: Current sorbed boron mass associated with aquifer material, in mg, before
    and after the equilibrium sorption update.
  ratio: Diagnostic ratio of sorbed concentration to dissolved concentration; computed after
    each constituent update to check against the corresponding Kd, though it is not stored
    externally.
  mass_total: Conserved total mass for one constituent, formed as dissolved mass plus sorbed
    mass before repartitioning.
  val_num: Numerator term used in the closed-form sorption solution; it combines the constituent
    Kd with aquifer volume and bulk density.
  val_den: Denominator term used in the closed-form sorption solution; it scales by groundwater
    volume in liters.
  val: Intermediate factor equal to `(val_num / val_den) + 1`, used to split conserved total
    mass into dissolved and sorbed parts.
  cseo4_new: Updated dissolved selenium-4 concentration in groundwater, in g/m3, after equilibrium
    partitioning.
  ccseo4_new: Updated sorbed selenium-4 concentration on aquifer material, in mg/kg, after
    equilibrium partitioning.
  cseo3_new: Updated dissolved selenium-3 concentration in groundwater, in g/m3, after equilibrium
    partitioning.
  ccseo3_new: Updated sorbed selenium-3 concentration on aquifer material, in mg/kg, after
    equilibrium partitioning.
  cborn_new: Updated dissolved boron concentration in groundwater, in g/m3, after equilibrium
    partitioning.
  ccborn_new: Updated sorbed boron concentration on aquifer material, in mg/kg, after equilibrium
    partitioning.
  gw_volume: Groundwater volume in the aquifer, in m3, derived from aquifer storage and object
    area; used to convert between concentration and mass.
  aqu_volume: Volume of aquifer material participating in sorption, in m3, computed from area,
    aquifer depth, and specific yield.
  aqu_bd: Aquifer bulk density, fixed at 2000 kg/m3, used to convert aquifer material volume
    to mass and to convert mg/kg sorbed concentrations.
  aqu_mass: Total mass of aquifer material, in kg, used as the basis for sorbed concentration
    calculations.
  sorbed_seo4: Temporary working value holding selenium-4 sorbed mass or concentration depending
    on the conversion stage; it starts from `cs_aqu(iaq)%cs_sorb(1)` and is later overwritten
    with converted mass.
  sorbed_seo3: Temporary working value holding selenium-3 sorbed mass or concentration depending
    on the conversion stage; it starts from `cs_aqu(iaq)%cs_sorb(2)` and is later overwritten
    with converted mass.
  sorbed_born: Temporary working value holding boron sorbed mass or concentration depending
    on the conversion stage; it starts from `cs_aqu(iaq)%cs_sorb(3)` and is later overwritten
    with converted mass.
  mass_seo4_before: Stored dissolved selenium-4 mass before repartitioning; used to compute
    the sorption mass transfer diagnostic.
  mass_seo4_after: Stored dissolved selenium-4 mass after repartitioning; used to compute
    the sorption mass transfer diagnostic.
  mass_seo3_before: Stored dissolved selenium-3 mass before repartitioning; used to compute
    the sorption mass transfer diagnostic.
  mass_seo3_after: Stored dissolved selenium-3 mass after repartitioning; used to compute
    the sorption mass transfer diagnostic.
  mass_born_before: Stored dissolved boron mass before repartitioning; used to compute the
    sorption mass transfer diagnostic.
  mass_born_after: Stored dissolved boron mass after repartitioning; used to compute the sorption
    mass transfer diagnostic.
uses:
  hydrograph_module: '`ob(icmd)` identifies which aquifer object is being processed and supplies
    the object area and database pointer. `cs_sorb_aqu` needs that connectivity information
    to map from the current routed command to the correct aquifer state and geometry.'
  aquifer_module: '`aqu_d(iaq)%stor`, `aqudb(iaqdb)%dep_bot`, and `aqu_dat(iaq)%spyld` define
    the groundwater volume and the aquifer-material volume available for sorption. Those values
    control the mass-to-concentration conversions in this routine.'
  organic_mineral_mass_module: The source imports `organic_mineral_mass_module`, but no resolved
    references from this routine were extracted from it. It matters here only if shared mass-state
    definitions from that module are expected by the broader aquifer constituent bookkeeping;
    the extracted evidence does not show a direct symbol use.
  constituent_mass_module: '`cs_aqu(iaq)` holds the aquifer constituent state that this routine
    reads and overwrites: dissolved concentrations, sorbed concentrations, and constituent
    masses for selenium-4, selenium-3, and boron. Without this module’s state, the equilibrium
    update has nowhere to store its results.'
  cs_aquifer: '`acsb_d(iaq)` captures aquifer constituent mass-balance diagnostics. `cs_sorb_aqu`
    writes the sorption transfer and sorbed-phase mass there so later reporting and balance
    checks can distinguish sorption from other groundwater processes.'
  cs_data_module: '`cs_rct_aqu(iaq)%kd_seo4`, `%kd_seo3`, and `%kd_born` supply the partition
    coefficients that define the equilibrium split between dissolved and sorbed phases. The
    whole calculation is driven by those Kd values.'
---

<!-- facts:header -->

Updates aquifer constituent concentrations and sorbed masses for selenium-4, selenium-3, and boron using equilibrium sorption relationships. It keeps dissolved and sorbed phases consistent with aquifer geometry, groundwater storage, and constituent Kd values.

## Bottom Line

`cs_sorb_aqu` recalculates how much selenium-4, selenium-3, and boron is dissolved in aquifer groundwater versus sorbed to aquifer material. It starts from the current aquifer object, groundwater storage, aquifer thickness, and sorption coefficients, then recomputes phase masses so total mass is conserved while the dissolved/sorbed split matches the Kd values.

The routine then writes the updated dissolved concentrations, sorbed concentrations, sorbed masses, and mass-balance diagnostics back into `cs_aqu` and `acsb_d`. Those outputs are used by the groundwater constituent bookkeeping that follows `cs_rctn_aqu` in `aqu_1d_control`, so later aquifer routing and mass-balance reporting see the sorption-adjusted state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the aquifer-chemistry branch of `aqu_1d_control`, after `cs_rctn_aqu` and whenever `cs_db%num_cs > 0`. It depends on the current aquifer object setup, groundwater storage, and constituent reaction parameters prepared earlier in the aquifer step, and its updated `cs_aqu` and `acsb_d` values feed later groundwater constituent balance and routing behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the current routed aquifer object to its aquifer indices. | The routine reads `ob(icmd)%num` into `iaq` and `ob(icmd)%props` into `iaqdb`, so all later calculations use the correct aquifer state and database record for the current command object. |
| 2. Compute groundwater and aquifer-material volumes. | It derives groundwater volume from aquifer storage and object area, then computes aquifer material volume and mass from object area, aquifer depth, specific yield, and bulk density. These volumes define the conversion basis for concentration and mass. |
| 3. Load current sorbed masses and convert them to aquifer-material concentrations. | The routine reads current sorbed constituent mass from `cs_aqu(iaq)%cs_sorb`, converts kg/ha to total mg, and then stores sorbed concentration in `cs_aqu(iaq)%csc_sorb` as mg/kg. |
| 4. Capture the pre-update dissolved masses from groundwater. | It initializes before/after tracking variables to zero and computes dissolved masses for selenium-4, selenium-3, and boron from current groundwater concentrations and groundwater volume. |
| 5. Compute the pre-update sorbed masses from aquifer-material concentrations. | Using the aquifer mass, it converts the current sorbed concentrations back to total sorbed mass for each constituent, so total mass can be conserved during repartitioning. |
| 6. Repartition selenium-4 with the Kd equation and mass conservation. | For selenium-4, it keeps total mass fixed, solves the one-constituent equilibrium split using `kd_seo4`, updates dissolved and sorbed masses, converts them to new concentration forms, and stores the updated groundwater mass in `cs_aqu(iaq)%cs(1)`. |
| 7. Repartition selenium-3 with the Kd equation and mass conservation. | It repeats the same equilibrium calculation for selenium-3 using `kd_seo3`, then writes the new dissolved concentration, sorbed concentration, and groundwater mass back into `cs_aqu(iaq)`. |
| 8. Repartition boron with the Kd equation and mass conservation. | It performs the same closed-form sorption solve for boron using `kd_born`, handling zero groundwater volume safely, and stores the new dissolved and sorbed states in `cs_aqu(iaq)`. |
| 9. Record sorption transfer diagnostics. | The routine stores the net loss of dissolved mass as `sorb` in `acsb_d(iaq)%cs`, which reports how much mass moved between groundwater and sorbed phases during this call. |
| 10. Convert sorbed concentrations back to kg/ha for global state. | It converts the updated sorbed mg/kg values back to kg/ha using aquifer mass and area, then writes them into `cs_aqu(iaq)%cs_sorb` so the global aquifer constituent state stays in its standard unit system. |
| 11. Store sorbed-mass balance outputs. | The routine copies the updated sorbed masses into `acsb_d(iaq)%cs(:)%srbd` so the aquifer mass-balance records can report the final sorbed inventory for each constituent. |
| 12. Return to the caller. | After all aquifer constituent states and balance diagnostics are updated, the subroutine exits and leaves the revised values for downstream aquifer processing. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ob, icmd` | `ob(icmd)%num, ob(icmd)%area_ha, ob(icmd)%props` |
| [sym:aquifer_module] | `aqu_d, aqudb, aqu_dat` | `aqu_d(iaq)%stor, aqudb(iaqdb)%dep_bot, aqu_dat(iaq)%spyld` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `none resolved` |
| [sym:constituent_mass_module] | `cs_aqu` | `cs_aqu(iaq)%cs_sorb(1), cs_aqu(iaq)%cs_sorb(2), cs_aqu(iaq)%cs_sorb(3), cs_aqu(iaq)%csc_sorb(1), cs_aqu(iaq)%csc_sorb(2), cs_aqu(iaq)%csc_sorb(3), cs_aqu(iaq)%csc(1), cs_aqu(iaq)%csc(2), cs_aqu(iaq)%csc(3), cs_aqu(iaq)%cs(1), cs_aqu(iaq)%cs(2), cs_aqu(iaq)%cs(3)` |
| [sym:cs_aquifer] | `acsb_d` | `acsb_d(iaq)%cs(1)%sorb, acsb_d(iaq)%cs(2)%sorb, acsb_d(iaq)%cs(3)%sorb, acsb_d(iaq)%cs(1)%srbd, acsb_d(iaq)%cs(2)%srbd, acsb_d(iaq)%cs(3)%srbd` |
| [sym:cs_data_module] | `cs_rct_aqu` | `cs_rct_aqu(iaq)%kd_seo4, cs_rct_aqu(iaq)%kd_seo3, cs_rct_aqu(iaq)%kd_born` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_aqu(iaq)%csc_sorb(1)` | When selenium-4 sorption is recalculated, regardless of groundwater volume, after the Kd-based equilibrium solve. | `cs_aqu(iaq)%csc_sorb(1)` is overwritten with the updated selenium-4 sorbed concentration in mg/kg so the aquifer’s sorbed-phase state matches the new equilibrium split. |
| `cs_aqu(iaq)%csc_sorb(2)` | When selenium-3 sorption is recalculated, regardless of groundwater volume, after the Kd-based equilibrium solve. | `cs_aqu(iaq)%csc_sorb(2)` is overwritten with the updated selenium-3 sorbed concentration in mg/kg so the aquifer’s sorbed-phase state matches the new equilibrium split. |
| `cs_aqu(iaq)%csc_sorb(3)` | When boron sorption is recalculated, regardless of groundwater volume, after the Kd-based equilibrium solve. | `cs_aqu(iaq)%csc_sorb(3)` is overwritten with the updated boron sorbed concentration in mg/kg so the aquifer’s sorbed-phase state matches the new equilibrium split. |
| `cs_aqu(iaq)%csc(1)` | When selenium-4 dissolved concentration is recomputed from the equilibrium mass split. | `cs_aqu(iaq)%csc(1)` is updated to the new dissolved selenium-4 concentration in g/m3, which represents the groundwater phase concentration after sorption equilibrium is enforced. |
| `cs_aqu(iaq)%cs(1)` | When selenium-4 dissolved concentration is recomputed from the equilibrium mass split. | `cs_aqu(iaq)%cs(1)` is updated to the new dissolved selenium-4 mass in kg/ha-equivalent groundwater mass form used by the aquifer constituent state. |
| `cs_aqu(iaq)%csc(2)` | When selenium-3 dissolved concentration is recomputed from the equilibrium mass split. | `cs_aqu(iaq)%csc(2)` is updated to the new dissolved selenium-3 concentration in g/m3 after sorption equilibrium is enforced. |
| `cs_aqu(iaq)%cs(2)` | When selenium-3 dissolved concentration is recomputed from the equilibrium mass split. | `cs_aqu(iaq)%cs(2)` is updated to the new dissolved selenium-3 mass in kg/ha-equivalent groundwater mass form used by the aquifer constituent state. |
| `cs_aqu(iaq)%csc(3)` | When boron dissolved concentration is recomputed from the equilibrium mass split. | `cs_aqu(iaq)%csc(3)` is updated to the new dissolved boron concentration in g/m3 after sorption equilibrium is enforced. |
| `cs_aqu(iaq)%cs(3)` | When boron dissolved concentration is recomputed from the equilibrium mass split. | `cs_aqu(iaq)%cs(3)` is updated to the new dissolved boron mass in kg/ha-equivalent groundwater mass form used by the aquifer constituent state. |
| `acsb_d(iaq)%cs(1)%sorb` | After selenium-4 mass is repartitioned and before the routine converts sorbed concentrations back to kg/ha. | `acsb_d(iaq)%cs(1)%sorb` stores the selenium-4 mass transferred by sorption, as the difference between the pre- and post-update dissolved masses converted to kg. |
| `acsb_d(iaq)%cs(2)%sorb` | After selenium-3 mass is repartitioned and before the routine converts sorbed concentrations back to kg/ha. | `acsb_d(iaq)%cs(2)%sorb` stores the selenium-3 mass transferred by sorption, as the difference between the pre- and post-update dissolved masses converted to kg. |
| `acsb_d(iaq)%cs(3)%sorb` | After boron mass is repartitioned and before the routine converts sorbed concentrations back to kg/ha. | `acsb_d(iaq)%cs(3)%sorb` stores the boron mass transferred by sorption, as the difference between the pre- and post-update dissolved masses converted to kg. |
| `cs_aqu(iaq)%cs_sorb(1)` | After the selenium-4 sorbed concentration is converted back from mg/kg to kg/ha. | `cs_aqu(iaq)%cs_sorb(1)` is refreshed to the aquifer-scale sorbed mass density for selenium-4 so later routines see the updated sorbed inventory in the standard aquifer unit system. |
| `cs_aqu(iaq)%cs_sorb(2)` | After the selenium-3 sorbed concentration is converted back from mg/kg to kg/ha. | `cs_aqu(iaq)%cs_sorb(2)` is refreshed to the aquifer-scale sorbed mass density for selenium-3 so later routines see the updated sorbed inventory in the standard aquifer unit system. |
| `cs_aqu(iaq)%cs_sorb(3)` | After the boron sorbed concentration is converted back from mg/kg to kg/ha. | `cs_aqu(iaq)%cs_sorb(3)` is refreshed to the aquifer-scale sorbed mass density for boron so later routines see the updated sorbed inventory in the standard aquifer unit system. |
| `acsb_d(iaq)%cs(1)%srbd` | After selenium-4 mass is converted to sorbed kg for balance reporting. | `acsb_d(iaq)%cs(1)%srbd` records the final selenium-4 mass sorbed to aquifer material, providing the mass-balance output counterpart to the `sorb` transfer. |
| `acsb_d(iaq)%cs(2)%srbd` | After selenium-3 mass is converted to sorbed kg for balance reporting. | `acsb_d(iaq)%cs(2)%srbd` records the final selenium-3 mass sorbed to aquifer material, providing the mass-balance output counterpart to the `sorb` transfer. |
| `acsb_d(iaq)%cs(3)%srbd` | After boron mass is converted to sorbed kg for balance reporting. | `acsb_d(iaq)%cs(3)%srbd` records the final boron mass sorbed to aquifer material, providing the mass-balance output counterpart to the `sorb` transfer. |

## File I/O

<!-- facts:io -->


## Lineage

The source history shows the routine was added in commit `df07e3f` with the full sorption-equilibrium implementation already present. `c639a8c` and `2405a68` only changed the imported module name between `cs_aquifer` and `cs_aquifer_module` for compilation compatibility, `39fabde` initialized all local scalars to zero, and `2ee1889` changed only the final program unit terminator from a comment-style `end` to `end subroutine cs_sorb_aqu`.

- df07e3f added the aquifer sorption routine and implemented the dissolved/sorbed equilibrium solve for selenium-4, selenium-3, and boron, including mass-balance outputs.
- 2405a68 and c639a8c only swapped the module import name between `cs_aquifer` and `cs_aquifer_module`; the routine logic did not change.
- 39fabde initialized all local integers and reals to zero, which affects default starting values but not the sorption algorithm itself.
- 2ee1889 changed the closing statement to `end subroutine cs_sorb_aqu`, a cosmetic cleanup with no algorithmic effect.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_sorb_aqu' has no extracted documentation comment.
