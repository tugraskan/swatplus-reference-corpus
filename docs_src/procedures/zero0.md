---
kind: procedure
symbol: zero0
title: zero0
status: filled
source_hash: eb180465fd4db5b6
version_label: SWAT+ 62.0.0
locals:
  iop: Loop/counter-style integer used only as a local reset variable; it is initialized to
    0 and then assigned 0 again during the routine.
  pltnfr: Local nitrogen fraction parameter for crop biomass at emergence; it is initialized
    to 0. and then reset again before the subroutine returns.
  pltpfr: Local phosphorus fraction parameter for crop biomass at emergence; it is initialized
    to 0. and then reset again before the subroutine returns.
  ranrns: Local random roughness value for a tillage operation; it is initialized to 0. and
    then reset again before return.
uses:
  hru_module: hru_module holds the shared HRU initialization state that zero0 is responsible
    for clearing. These arrays and scalars represent conditions used across runoff, drainage,
    nutrient, septic, grazing, and residue calculations, so resetting them here establishes
    the starting baseline for later HRU processes.
---

<!-- facts:header -->

Initializes selected HRU and management state values to their zero or default starting values.

## Bottom Line

zero0 is a reset routine called during parameter allocation to clear a wide set of HRU-state arrays and scalars before simulation setup continues. It does not take arguments; instead it writes default values directly into shared state from hru_module.

The routine sets many water, nutrient, grazing, septic, canopy, and drainage-related fields back to baseline values so later routines start from a consistent initial condition. A few variables are not simply zeroed: for example ranrns_hru is set to 20, and the crop nutrient fraction locals are initialized and then reset before return.

## Arguments

<!-- facts:arguments -->

## Where It Fits

zero0 runs during parameter allocation after allocate_parms has set up the model's parameter and state storage. Its reset values are then available to later HRU and management routines that assume initialized baseline state, including runoff, drainage, nutrient, septic, grazing, and soil-water behaviors.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare zero0 as a subroutine that uses hru_module state and no formal arguments. | The routine is defined as an initialization helper that operates entirely through shared HRU variables rather than input arguments. |
| 2. Initialize local scratch variables iop, pltnfr, pltpfr, and ranrns to zero. | These local variables are given starting values immediately on declaration, establishing clean defaults for any later use in the routine. |
| 3. Reset urban runoff Green-Ampt storage trackers. | urb_abstinit and rateinf_prev are set to zero so urban abstraction and prior infiltration state start from a clean baseline. |
| 4. Clear Drainmod tile and HRU runoff accumulation fields and set ranrns_hru to 20. | The cumulative tile/runoff storages are zeroed, while ranrns_hru is assigned its nonzero default roughness value. |
| 5. Zero canopy and runoff-related HRU storage fields. | brt, bss, and canstor are cleared so biomass/residue and canopy storage begin from zero. |
| 6. Reset curve number, dormancy, and filter width state. | cn2, dormhr, and filterw are set to zero, removing any prior HRU condition from those controls. |
| 7. Zero grazing, septic, and tile-related integer flags and counters. | igrz, iop, iseptic, isep_ly, itb, and grz_days are reset so management and drainage counters start over. |
| 8. Zero nutrient and phosphorus state variables and the local crop fraction variables. | latno3, orgn_con, orgp_con, and phubase are cleared, and the local pltnfr, pltpfr, and ranrns values are reset. |
| 9. Reset sediment, septic crack, and soil temperature-related fields. | sstmaxd, sed_con, sepcrk, and stmaxd are set to zero to clear soil, sediment, and septic drainage state. |
| 10. Clear remaining nutrient and water-table tracking arrays. | sol_sumsolp, soln_con, solp_con, wt_shall, and yr_skip are set to zero so later routines see baseline solute and water-table conditions. |
| 11. Return to the caller after the shared state has been initialized. | The subroutine ends immediately after completing the state reset sequence. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `brt, bss, canstor, cn2, cumei, urb_abstinit, rateinf_prev, cumeira, cumrai, cumrt, dormhr, filterw, grz_days, igrz, isep_ly, iseptic, itb, latno3, orgn_con, orgp_con, phubase, ranrns_hru, sed_con, sepcrk, sol_sumsolp, soln_con, solp_con, sstmaxd, stmaxd, wt_shall, yr_skip` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `urb_abstinit` | During the initialization pass of zero0, unconditionally. | urb_abstinit is reset to 0. so urban abstraction storage starts from a clean initial value before later infiltration/runoff calculations. |
| `rateinf_prev` | During the initialization pass of zero0, unconditionally. | rateinf_prev is reset to 0. to clear the previously stored infiltration rate used by later urban runoff calculations. |
| `cumeira` | During the initialization pass of zero0, unconditionally. | cumeira is reset to 0. as part of clearing cumulative Drainmod/irrigation-related infiltration accounting. |
| `cumei` | During the initialization pass of zero0, unconditionally. | cumei is reset to 0. so cumulative infiltration storage begins at zero for the next model period. |
| `cumrai` | During the initialization pass of zero0, unconditionally. | cumrai is reset to 0. to clear cumulative rainfall infiltration accounting. |
| `cumrt` | During the initialization pass of zero0, unconditionally. | cumrt is reset to 0. so the cumulative runoff/inflow total used by the drainage logic starts from zero. |
| `ranrns_hru` | During the initialization pass of zero0, unconditionally. | ranrns_hru is assigned 20., providing its default HRU roughness value rather than a zero baseline. |
| `brt` | During the initialization pass of zero0, unconditionally. | brt is reset to 0. to clear the biomass or residue-related HRU state before later growth and routing calculations. |
| `bss` | During the initialization pass of zero0, unconditionally. | bss is reset to 0. to clear the soil/biomass storage array before subsequent HRU processes use it. |
| `canstor` | During the initialization pass of zero0, unconditionally. | canstor is reset to 0. so canopy storage begins at a clean baseline before interception calculations. |
| `cn2` | During the initialization pass of zero0, unconditionally. | cn2 is reset to 0. to clear the HRU curve-number state before later runoff-related routines apply their own values. |
| `dormhr` | During the initialization pass of zero0, unconditionally. | dormhr is reset to 0. so dormancy-hour accumulation does not carry over from a previous setup or run. |
| `filterw` | During the initialization pass of zero0, unconditionally. | filterw is reset to 0. to clear any stored filter strip width before management calculations reuse it. |
| `igrz` | During the initialization pass of zero0, unconditionally. | igrz is reset to 0 to clear the grazing management flag/counter before the simulation uses it. |
| `iseptic` | During the initialization pass of zero0, unconditionally. | iseptic is reset to 0 so septic-system state is marked uninitialized before septic routines act on it. |
| `isep_ly` | During the initialization pass of zero0, unconditionally. | isep_ly is reset to 0 so the septic layer indicator returns to its default starting value. |
| `itb` | During the initialization pass of zero0, unconditionally. | itb is reset to 0 to clear the tiling-related integer state before drainage calculations. |
| `grz_days` | During the initialization pass of zero0, unconditionally. | grz_days is reset to 0 so grazing-day accumulation begins anew for the HRU. |
| `latno3` | During the initialization pass of zero0, unconditionally. | latno3 is reset to 0. to clear lateral nitrate concentration/state before later transport calculations. |
| `orgn_con` | During the initialization pass of zero0, unconditionally. | orgn_con is reset to 0. so organic nitrogen concentration starts from zero in the initialized HRU state. |
| `orgp_con` | During the initialization pass of zero0, unconditionally. | orgp_con is reset to 0. so organic phosphorus concentration starts from zero in the initialized HRU state. |
| `phubase` | During the initialization pass of zero0, unconditionally. | phubase is reset to 0. to clear the base heat unit accumulation state before crop development routines use it. |
| `sstmaxd` | During the initialization pass of zero0, unconditionally. | sstmaxd is reset to 0. so the maximum soil temperature depth state starts from zero. |
| `sed_con` | During the initialization pass of zero0, unconditionally. | sed_con is reset to 0. to clear sediment concentration state before erosion and routing routines compute new values. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source changes to zero0: df07e3f created the subroutine and its initialization block; 09d23f0 removed two explanatory comments without changing assignments; 39fabde changed local declarations to initialize iop, pltnfr, pltpfr, and ranrns at declaration time and cleaned spacing on phubase; 2ee1889 only changed the closing statement to an explicit `end subroutine zero0`.

- df07e3f introduced the zero0 initialization routine and the full set of shared HRU reset assignments.
- 09d23f0 only deleted comments and did not alter runtime behavior.
- 39fabde changed the local variable declarations so iop, pltnfr, pltpfr, and ranrns start with explicit default values at declaration time, while leaving the later reset assignments in place.
- 2ee1889 made a cosmetic source-end change from `end` to `end subroutine zero0` without changing the procedure's logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'zero0' has no extracted documentation comment.
