---
kind: procedure
symbol: pl_graze
title: pl_graze
status: filled
source_hash: 8c30f9e5289463b8
version_label: SWAT+ 62.0.0
locals:
  j: HRU index assigned from `ihru`; it selects which row of `pl_mass`, `pcom`, and `soil1`
    the grazing operation updates.
  l: Soil layer index for manure placement; this routine always sets it to the surface layer
    (`1`) before adding manure-derived nutrients.
  it: Fertilizer/manure database index copied from `graze%manure_id`; it chooses the manure
    composition record in `fertdb`.
  xx: Intermediate amount of metabolic-litter carbon added from manure; computed as `X8 *
    X10` before updating `soil1(j)%meta(l)%c`.
  dmi: Current above-ground biomass of the plant being processed (`pl_mass(j)%ab_gr(ipl)%m`);
    used to decide whether to exit the plant loop and whether to reset LAI/PHU accumulation.
  zz: Intermediate organic nitrogen added to metabolic litter; computed from manure amount,
    fertilizer organic-N fraction, and `X10` before updating `soil1(j)%meta(l)%n`.
  yz: Intermediate manure mass assigned to structural and lignin pool mass updates after metabolic
    allocation has been removed; used to add the remaining mass to structural/lignin pools.
  yy: Intermediate total manure mass assigned to the metabolic pool (`manure_kg * X10`); used
    to update `soil1(j)%meta(l)%m`.
  xz: Intermediate carbon allocated to the structural litter carbon pool; computed as `manure_kg
    * orgc_f - XX` before updating structural and lignin carbon pools.
  x8: Organic carbon mass applied from manure (`X1 * orgc_f`); it is the total carbon basis
    used to split manure carbon into metabolic and structural fractions.
  x10: Fraction of manure carbon routed to the metabolic litter pool; it is derived from the
    manure carbon-to-nutrient ratio and clipped to the range 0.01 to 0.7.
  x1: Manure mass applied to the layer; set equal to `manure_kg` and used as the base mass
    for carbon partitioning.
  rln: Carbon-to-nutrient ratio term used to estimate the metabolic fraction of manure carbon;
    calculated from organic carbon fraction and fertilizer N/P composition.
  orgc_f: Fixed organic-carbon fraction of manure used in the C/N cycling block; this sets
    the carbon mass basis for the litter partitioning calculation.
  ipl: Plant index in the community loop; iterates from 1 to `pcom(j)%npl` to process each
    plant in the HRU.
  manure_kg: Daily manure deposited by grazing animals; copied from `graze%manure` and used
    to update soil nutrient pools and grazing outputs.
  eat_plant: Fraction of each plant's above-ground biomass removed by grazing; derived from
    `graze%eat` relative to total community biomass and capped at 1.
  tramp_plant: Fraction of each plant's above-ground biomass removed by trampling; derived
    from `graze%tramp` relative to total community biomass, though the current source forces
    it to zero.
uses:
  mgt_operations_module: '`mgt_operations_module` provides the `graze` operation record that
    supplies the grazing intensity, trampling intensity, manure amount, manure database id,
    and biomass threshold that control every major branch in this routine.'
  fertilizer_data_module: '`fertilizer_data_module` provides `fertdb(it)`, which defines the
    manure''s mineral N, mineral P, organic N, organic P, and ammonium-N fractions used to
    split deposited manure into soil pools.'
  basin_module: '`basin_module` supplies `bsn_cc%cswat`, the carbon-code switch that determines
    whether manure is handled with the simple nutrient bookkeeping path or the C/N cycling
    path.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the plant and soil
    mass structures this routine mutates; the grazing fractions are applied to `pl_mass`,
    and manure is added into `soil1` pools across mineral and organic carbon/nitrogen/phosphorus
    compartments.'
  hru_module: '`hru_module` provides the current HRU index and the cumulative grazing outputs.
    `ihru` tells the routine which HRU to update, while `grazn` and `grazp` record nutrient
    loads returned by grazing manure in the CSWAT=0 pathway.'
  soil_module: The soil profile mass object is where manure-derived mineral and organic nutrients
    are deposited. These layer-resolved pools are the direct sinks for the manure additions
    computed in the grazing logic.
  plant_module: '`plant_module` provides the plant community structure and the growth-state
    variables that are adjusted after biomass removal. The routine needs `npl` to loop over
    plants, and it reduces `lai` and `phuacc` after grazing so later growth calculations reflect
    the disturbance.'
  carbon_module: The carbon module is imported because the broader grazing procedure is tied
    to carbon cycling, and this routine explicitly partitions manure into organic carbon-related
    soil pools in the C/N cycling branch.
---

<!-- facts:header -->

Applies grazing and trampling losses to plant biomass in the current HRU, then routes any deposited manure into soil and grazing output pools. It also resets plant growth state such as leaf area and heat-unit accumulation when grazing is intense enough.

## Bottom Line

pl_graze acts on the current HRU selected by `ihru`. It first checks whether total above-ground biomass is large enough to allow grazing, then loops through the plant community and removes fractions of seed, leaf, stem, total biomass, and above-ground biomass based on the configured grazing amounts `graze%eat` and `graze%tramp`.

If manure is deposited, the routine uses the manure fertilizer record `fertdb(it)` to split that manure into mineral and organic N/P forms and add them to the surface soil layer. Depending on `bsn_cc%cswat`, it updates either the simpler CSWAT=0 bookkeeping or the C/N cycling pathway for CSWAT=2, and it stores grazing losses in `grazn` and `grazp`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a grazing management action is triggered for the current HRU. The `actions` and `hru_control` callers set `ihru` and load `graze` from the management database before calling it. Its results feed later plant-growth and soil-pool behavior because it lowers plant biomass and leaf area, updates accumulated heat-unit state, and deposits manure nutrients into the surface soil layer.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check biomass threshold | The routine first checks whether total above-ground community biomass is below `graze%biomin`. If so, it returns immediately and skips grazing because the HRU does not have enough biomass to support the operation. |
| 2. loop over plants | It iterates through each plant in the community, reads the current above-ground biomass into `dmi`, and exits the loop once a plant has negligible biomass. This prevents further biomass updates for plants that are effectively absent. |
| 3. compute grazing fraction | The routine converts daily eaten biomass into a per-plant fraction using `graze%eat / pl_mass(j)%ab_gr_com%m` and caps that fraction at 1.0. That fraction controls the amount removed from seed, leaf, stem, total, and above-ground biomass pools. |
| 4. remove eaten biomass | It subtracts the eaten fraction from the plant's seed, leaf, stem, total biomass, and above-ground biomass pools. The update reduces the mass remaining on the plant after grazing. |
| 5. compute trampling fraction | The routine computes a trampling fraction from `graze%tramp` and total above-ground biomass, but the current source forces `tramp_plant` to zero. That means trampling does not actually remove biomass in this version of the code. |
| 6. apply trampling update | It applies the trampling fraction to the same plant biomass pools that were reduced by grazing. Because the fraction is currently zero, these assignments leave the plant masses unchanged in practice. |
| 7. reset growth state | The routine adjusts leaf area index and accumulated heat units after grazing. If biomass is above 1 kg/ha and still below 2500 kg/ha, it reduces LAI and PHU accumulation slightly; if biomass is extremely low, it resets LAI to 0.05 and PHU accumulation to zero. |
| 8. load manure settings | After finishing the plant loop, the routine reads the manure fertilizer id and manure mass from `graze`. These values determine whether manure is added to soil and how it is partitioned. |
| 9. add manure for CSWAT=0 | If manure is present and `bsn_cc%cswat == 0`, the routine adds mineral and organic N and P to the surface soil layer using fertilizer fractions. It also records total grazing N and P losses in `grazn` and `grazp`. |
| 10. enter C/N cycling path | For `bsn_cc%cswat == 2`, the routine begins the C/N cycling branch and again adds nitrate nitrogen from manure mineral-N fractions. This branch then partitions the manure into metabolic, structural, and lignin pools. |
| 11. compute manure carbon split | It sets the organic carbon fraction, computes the carbon mass, forms the carbon-to-nutrient ratio term `RLN`, and derives the metabolic fraction `X10`. `X10` is then clamped to the range 0.01 to 0.7 before being used in pool partitioning. |
| 12. update soil organic pools | The routine distributes manure carbon, mass, and organic N into the soil's metabolic, structural, and lignin pools. It updates litter carbon, litter mass, organic nitrogen, and lignin partitioning terms with the computed fractions. |
| 13. finalize mineral and total pools | It recomputes total organic nitrogen for the surface layer from metabolic and structural pools, then adds ammonium-N, labile P, and total P from the manure fractions. This completes the manure deposition for the active carbon code branch. |
| 14. return | The subroutine exits after finishing all grazing, trampling, and manure updates for the current HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `graze` | `graze%biomin, graze%eat, graze%tramp, graze%manure_id, graze%manure` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(it)%fnh3n, fertdb(it)%fminn, fertdb(it)%forgn, fertdb(it)%fminp, fertdb(it)%forgp` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%ab_gr(ipl)%m, pl_mass(j)%seed(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl), soil1(j)%mn(l)%no3, soil1(j)%tot(l)%n, soil1(j)%mn(l)%nh4, soil1(j)%mp(l)%lab, soil1(j)%tot(l)%p, soil1(j)%meta(l)%c, soil1(j)%meta(l)%m, soil1(j)%meta(l)%n, soil1(j)%str(l)%n, soil1(j)%str(l)%c, soil1(j)%lig(l)%c, soil1(j)%lig(l)%n, soil1(j)%str(l)%m, soil1(j)%lig(l)%m` |
| [sym:hru_module] | `ihru, grazn, grazp` |  |
| [sym:soil_module] | `soil1` | `soil1(j)%mn(l)%no3, soil1(j)%tot(l)%n, soil1(j)%mn(l)%nh4, soil1(j)%mp(l)%lab, soil1(j)%tot(l)%p, soil1(j)%meta(l)%c, soil1(j)%meta(l)%m, soil1(j)%meta(l)%n, soil1(j)%str(l)%n, soil1(j)%str(l)%c, soil1(j)%lig(l)%c, soil1(j)%lig(l)%n, soil1(j)%str(l)%m, soil1(j)%lig(l)%m` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plg(ipl)%lai, pcom(j)%plcur(ipl)%phuacc` |
| [sym:carbon_module] | `pl_mass` | `pl_mass(j)%ab_gr_com%m, pl_mass(j)%ab_gr(ipl)%m, pl_mass(j)%seed(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pl_mass(j)%seed(ipl)` | When the HRU has enough biomass to graze and the current plant receives the eating update in the plant loop. | `pl_mass(j)%seed(ipl)` is reduced in proportion to the eaten fraction and, in this version, also receives the trampling fraction update. The routine leaves the remaining seed biomass in the plant community object for later growth and harvest logic. |
| `pl_mass(j)%leaf(ipl)` | When the HRU has enough biomass to graze and the current plant receives the eating update in the plant loop. | `pl_mass(j)%leaf(ipl)` is reduced by the same eaten fraction and then by the trampling fraction. This tracks leaf biomass remaining after grazing disturbance. |
| `pl_mass(j)%stem(ipl)` | When the HRU has enough biomass to graze and the current plant receives the eating update in the plant loop. | `pl_mass(j)%stem(ipl)` is reduced by the eaten and trampled fractions. The remaining stem biomass is what survives the grazing event. |
| `pl_mass(j)%tot(ipl)` | When the HRU has enough biomass to graze and the current plant receives the biomass removal updates. | `pl_mass(j)%tot(ipl)` is decreased using the removed above-ground biomass fraction. This keeps the plant's total biomass consistent with the post-grazing state. |
| `pl_mass(j)%ab_gr(ipl)` | When grazing is applied to a plant in the community loop. | `pl_mass(j)%ab_gr(ipl)` is reduced by the eaten and trampled fractions, representing the remaining above-ground biomass on that individual plant after the event. |
| `pcom(j)%plg(ipl)%lai` | When `dmi > 1.` and `dmi < 2500.` after biomass removal. | `pcom(j)%plg(ipl)%lai` is reduced slightly to reflect canopy removal by grazing. If biomass is extremely low, it is reset to a small residual value of 0.05 instead of being reduced incrementally. |
| `pcom(j)%plcur(ipl)%phuacc` | When `dmi > 1.` and `dmi < 2500.` after biomass removal, or when `dmi <= 1.`. | `pcom(j)%plcur(ipl)%phuacc` is reduced in proportion to grazing when biomass is still present, or reset to zero when the plant is essentially gone. This modifies the plant's phenological progress after disturbance. |
| `soil1(j)%mn(l)%no3` | When manure is deposited and the routine enters the manure application blocks. | `soil1(j)%mn(l)%no3` is increased by the manure's mineral-N fraction that is not ammonia. It represents nitrate added to the surface soil from grazing manure. |
| `soil1(j)%tot(l)%n` | When manure is deposited and the routine enters the manure application blocks. | `soil1(j)%tot(l)%n` is increased first by the simple CSWAT=0 manure addition and then recomputed in the C/N cycling branch as the sum of metabolic and structural organic nitrogen. It holds the layer's total organic nitrogen after manure deposition. |
| `soil1(j)%mn(l)%nh4` | When manure is deposited and the routine enters the manure application blocks. | `soil1(j)%mn(l)%nh4` is increased by the manure's ammonium-N fraction. It stores the ammonium pool contribution from the manure application. |
| `soil1(j)%mp(l)%lab` | When manure is deposited and the routine enters the manure application blocks. | `soil1(j)%mp(l)%lab` is increased by the manure's mineral phosphorus fraction. This adds labile phosphorus to the surface soil layer. |
| `soil1(j)%tot(l)%p` | When manure is deposited and the routine enters the manure application blocks. | `soil1(j)%tot(l)%p` is increased by the manure's organic phosphorus fraction in the simple path and again in the C/N cycling path. It represents the layer's total phosphorus pool after manure input. |
| `grazn` | When `manure_kg > 0.` and `bsn_cc%cswat == 0`. | `grazn` stores the total nitrogen returned to the HRU from manure, combining organic-N and mineral-N fractions. It is a grazing nutrient bookkeeping output for the non-C/N pathway. |
| `grazp` | When `manure_kg > 0.` and `bsn_cc%cswat == 0`. | `grazp` stores the total phosphorus returned to the HRU from manure, combining organic-P and mineral-P fractions. It is the matching grazing phosphorus bookkeeping output. |
| `soil1(j)%meta(l)%c` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%meta(l)%c` receives manure carbon allocated to the metabolic litter pool. This is the carbon input used by the C/N cycling model for decomposition. |
| `soil1(j)%meta(l)%m` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%meta(l)%m` is increased by the manure mass routed to the metabolic pool. This records how much manure becomes metabolic litter mass. |
| `soil1(j)%meta(l)%n` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%meta(l)%n` is increased by the organic nitrogen portion assigned to metabolic litter. It is part of the soil organic N bookkeeping for the manure. |
| `soil1(j)%str(l)%n` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%str(l)%n` receives the remainder of manure organic nitrogen after the metabolic allocation is removed. This places the remaining N into the structural litter pool. |
| `soil1(j)%str(l)%c` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%str(l)%c` is increased by the carbon assigned to structural litter. This carbon then supports further splitting into lignin-related pools. |
| `soil1(j)%lig(l)%c` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%lig(l)%c` is increased by the lignin-share of structural carbon. It tracks carbon entering the lignin pool from manure. |
| `soil1(j)%lig(l)%n` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%lig(l)%n` is increased by the nitrogen share associated with lignin carbon. This keeps lignin C and N partitioning consistent with the structural carbon update. |
| `soil1(j)%str(l)%m` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%str(l)%m` is increased by the manure mass remaining after the metabolic portion is removed. It records the structural litter mass added to the soil layer. |
| `soil1(j)%lig(l)%m` | When `bsn_cc%cswat == 2` in the C/N cycling branch. | `soil1(j)%lig(l)%m` is increased by the lignin fraction of the structural manure mass. It stores the lignin mass contribution from grazing manure. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `pl_graze`. The earliest resolved update added the source file with the grazing/manure logic. A later 2024 initialization commit mainly set local variables to zero. In 2025, one commit replaced the explicit eat/trample temporary-variable workflow with direct proportional biomass subtraction and another commit disabled trampling by forcing `tramp_plant` to zero. In 2026, one commit removed the `bsn_cc%cswat == 1` manure update block and another expanded the C/N cycling branch to also run for `bsn_cc%cswat == 3`.

- Added the original grazing routine with plant biomass removal, manure deposition, and C/N cycling logic in the initial source import.
- Initialized local scalars to zero to avoid undefined values before grazing and manure calculations.
- Simplified grazing biomass removal by deleting intermediate eat/trample component variables and subtracting fractions directly from plant pools.
- Disabled trampling loss by setting `tramp_plant` to zero instead of capping it with `amin1`.
- Removed the CSWAT=1 manure-to-soil update block, leaving the simple CSWAT=0 path and the C/N cycling path.
- Changed the C/N cycling manure branch to run for `bsn_cc%cswat == 2 .or. bsn_cc%cswat == 3`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_graze' has no extracted documentation comment.
