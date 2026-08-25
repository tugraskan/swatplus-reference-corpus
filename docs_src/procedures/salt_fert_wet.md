---
kind: procedure
symbol: salt_fert_wet
title: salt_fert_wet
status: filled
source_hash: 6636527c88cf9eb7
version_label: SWAT+ 62.0.0
args:
  jj: HRU index for the wetland receiving the fertilizer application; it selects which wetland
    storage and balance records are updated.
  ifrt: Fertilizer database index; if it is not positive, the routine skips the fertilizer
    mass addition entirely.
  frt_kg: Applied fertilizer rate in kg/ha; this rate is multiplied by fertilizer salt fractions
    and HRU area to compute added salt mass.
uses:
  mgt_operations_module: The routine only runs its salt-fertilizer updates when `cs_db%num_salts
    > 0`, and it writes the computed salt masses into the wetland salt storage array `wet_water(jj)%salt(:)`.
  salt_module: The fertilizer composition stored in `fert_salt(ifrt)` provides the eight ion
    fractions used to compute how much SO4, Ca, Mg, Na, K, Cl, CO3, and HCO3 are added.
  constituent_mass_module: This module owns the `cs_db` flag that enables salt simulation
    and the `wet_water` storage that receives the added salt masses, so both are required
    for the wetland fertilizer update.
  fertilizer_data_module: The fertilizer salt database stores the per-unit fertilizer masses
    for each salt ion, which are multiplied by `frt_kg` and HRU area to produce the wetland
    additions.
  hru_module: The HRU area converts the fertilizer rate from kg/ha into total kilograms applied
    to this wetland HRU.
  res_salt_module: This module stores the wetland salt balance output arrays, and the routine
    records the fertilizer contribution in `wetsalt_d(jj)%salt(:)%fert` for later reporting.
---

<!-- facts:header -->

Adds fertilizer-derived salt ions to a wetland HRU’s salt storages and wetland salt balance outputs.

## Bottom Line

This subroutine is the wetland-side salt bookkeeping for fertilizer operations. When salt ions are enabled and a fertilizer type is valid, it converts the applied fertilizer rate into added masses of eight salt ions using the fertilizer composition database and the HRU area.

It updates both the wetland water salt storage (`wet_water(jj)%salt`) and the wetland daily salt fertilizer balance (`wetsalt_d(jj)%salt(:)%fert`) so later wetland salt accounting can report the fertilizer contribution.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`salt_fert_wet` runs during the management schedule when a fertilizer operation is applied to a wetland with standing water. `mgt_sched` prepares the fertilizer type, application rate, and wetland condition before calling it. Its results feed wetland salt bookkeeping and downstream salt output accounting, including the wetland salt balance arrays used for diagnostics and reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check salt simulation | The routine first verifies that salt ions are being simulated by testing `cs_db%num_salts > 0`. If salts are not enabled, it skips all fertilizer-salt bookkeeping. |
| 2. Validate fertilizer ID | If salt simulation is active, it checks that the fertilizer ID is positive. A nonpositive `ifrt` means no fertilizer database entry is available, so no salt masses are added. |
| 3. Add SO4 to wetland storage | It adds the fertilizer-derived sulfate mass to `wet_water(jj)%salt(1)` using the applied rate, sulfate fraction from `fert_salt(ifrt)%so4`, and `hru(jj)%area_ha`. |
| 4. Add Ca to wetland storage | It adds the fertilizer-derived calcium mass to `wet_water(jj)%salt(2)` using `fert_salt(ifrt)%ca` and the HRU area. |
| 5. Add Mg to wetland storage | It adds magnesium mass to `wet_water(jj)%salt(3)` from the fertilizer composition and applied area. |
| 6. Add Na to wetland storage | It adds sodium mass to `wet_water(jj)%salt(4)` using the sodium fraction of the fertilizer and the applied rate. |
| 7. Add K to wetland storage | It adds potassium mass to `wet_water(jj)%salt(5)`. |
| 8. Add Cl to wetland storage | It adds chloride mass to `wet_water(jj)%salt(6)`. |
| 9. Add CO3 to wetland storage | It adds carbonate mass to `wet_water(jj)%salt(7)`. |
| 10. Add HCO3 to wetland storage | It adds bicarbonate mass to `wet_water(jj)%salt(8)`. |
| 11. Record SO4 fertilizer balance | It writes the sulfate fertilizer mass to the wetland daily salt balance array `wetsalt_d(jj)%salt(1)%fert`. |
| 12. Record remaining ion balances | It stores the fertilizer contribution for Ca, Mg, Na, K, Cl, CO3, and HCO3 in `wetsalt_d(jj)%salt(2:8)%fert` using the same fertilizer composition and area calculation. |
| 13. Exit routine | After the conditional updates, the subroutine returns without any additional computation or external calls. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `cs_db, wet_water` | `cs_db%num_salts, wet_water(jj)%salt(1), wet_water(jj)%salt(2), wet_water(jj)%salt(3), wet_water(jj)%salt(4), wet_water(jj)%salt(5), wet_water(jj)%salt(6), wet_water(jj)%salt(7), wet_water(jj)%salt(8)` |
| [sym:salt_module] | `fert_salt` | `fert_salt(ifrt)%so4, fert_salt(ifrt)%ca, fert_salt(ifrt)%mg, fert_salt(ifrt)%na, fert_salt(ifrt)%k, fert_salt(ifrt)%cl, fert_salt(ifrt)%co3, fert_salt(ifrt)%hco3` |
| [sym:constituent_mass_module] | `cs_db, wet_water` | `cs_db%num_salts, wet_water(jj)%salt(1), wet_water(jj)%salt(2), wet_water(jj)%salt(3), wet_water(jj)%salt(4), wet_water(jj)%salt(5), wet_water(jj)%salt(6), wet_water(jj)%salt(7), wet_water(jj)%salt(8)` |
| [sym:fertilizer_data_module] | `fert_salt` | `fert_salt(ifrt)%so4, fert_salt(ifrt)%ca, fert_salt(ifrt)%mg, fert_salt(ifrt)%na, fert_salt(ifrt)%k, fert_salt(ifrt)%cl, fert_salt(ifrt)%co3, fert_salt(ifrt)%hco3` |
| [sym:hru_module] | `hru` | `hru(jj)%area_ha` |
| [sym:res_salt_module] | `wetsalt_d` | `wetsalt_d(jj)%salt(1)%fert, wetsalt_d(jj)%salt(2)%fert, wetsalt_d(jj)%salt(3)%fert, wetsalt_d(jj)%salt(4)%fert, wetsalt_d(jj)%salt(5)%fert, wetsalt_d(jj)%salt(6)%fert, wetsalt_d(jj)%salt(7)%fert, wetsalt_d(jj)%salt(8)%fert` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_water(jj)%salt(1)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Sulfate salt mass in the wetland is increased by the fertilizer-derived SO4 load for HRU `jj`. |
| `wet_water(jj)%salt(2)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Calcium salt mass in the wetland is increased by the fertilizer-derived Ca load. |
| `wet_water(jj)%salt(3)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Magnesium salt mass in the wetland is increased by the fertilizer-derived Mg load. |
| `wet_water(jj)%salt(4)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Sodium salt mass in the wetland is increased by the fertilizer-derived Na load. |
| `wet_water(jj)%salt(5)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Potassium salt mass in the wetland is increased by the fertilizer-derived K load. |
| `wet_water(jj)%salt(6)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Chloride salt mass in the wetland is increased by the fertilizer-derived Cl load. |
| `wet_water(jj)%salt(7)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Carbonate salt mass in the wetland is increased by the fertilizer-derived CO3 load. |
| `wet_water(jj)%salt(8)` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | Bicarbonate salt mass in the wetland is increased by the fertilizer-derived HCO3 load. |
| `wetsalt_d(jj)%salt(1)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The sulfate fertilizer contribution is recorded in the wetland salt balance output for later reporting. |
| `wetsalt_d(jj)%salt(2)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The calcium fertilizer contribution is recorded in the wetland salt balance output. |
| `wetsalt_d(jj)%salt(3)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The magnesium fertilizer contribution is recorded in the wetland salt balance output. |
| `wetsalt_d(jj)%salt(4)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The sodium fertilizer contribution is recorded in the wetland salt balance output. |
| `wetsalt_d(jj)%salt(5)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The potassium fertilizer contribution is recorded in the wetland salt balance output. |
| `wetsalt_d(jj)%salt(6)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The chloride fertilizer contribution is recorded in the wetland salt balance output. |
| `wetsalt_d(jj)%salt(7)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The carbonate fertilizer contribution is recorded in the wetland salt balance output. |
| `wetsalt_d(jj)%salt(8)%fert` | Only when `cs_db%num_salts > 0` and `ifrt > 0`. | The bicarbonate fertilizer contribution is recorded in the wetland salt balance output. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the routine was introduced in df07e3f with the wetland salt-fertilizer logic already present. 39fabde initialized the local `isalt` variable to zero, and 2ee1889 later removed that unused variable; 35b029c only adjusted the subroutine end-line formatting without changing behavior.

- df07e3f added the full `salt_fert_wet` implementation that gates on `cs_db%num_salts`, validates `ifrt`, and updates `wet_water(jj)%salt(1:8)` plus `wetsalt_d(jj)%salt(1:8)%fert` from `fert_salt(ifrt)` and `hru(jj)%area_ha`.
- 39fabde changed the local declaration of `isalt` from an uninitialized integer to `integer :: isalt = 0`, but the variable is not used in the routine body.
- 2ee1889 removed the unused `isalt = 0` declaration, leaving the routine behavior unchanged.
- 35b029c changed only the trailing `end subroutine` line formatting and did not alter logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_fert_wet' has no extracted documentation comment.
