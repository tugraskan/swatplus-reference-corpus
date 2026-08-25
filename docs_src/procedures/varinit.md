---
kind: procedure
symbol: varinit
title: varinit
status: filled
source_hash: a282b72b6c08fbd1
version_label: SWAT+ 62.0.0
locals:
  j: HRU index used to select the active element in `soil`, `hhqday`, and `wet_seep_day`;
    it is set from `ihru` before resets begin.
  ly: Loop counter over the soil layers of the active HRU profile; it drives the per-layer
    clearing of `prk` and `flat`.
  crk: Temporary crack-flow percolation accumulator for the HRU; initialized to zero as part
    of the daily hydrology reset.
  enratio: Temporary enrichment-ratio accumulator for the HRU; reset so erosion/nutrient calculations
    can recompute it for the new day.
  etday: Temporary daily evapotranspiration amount for the HRU; cleared before the new day's
    water-balance calculations.
  over_flow: Temporary overflow accumulator; reset to remove any carryover from the prior
    day.
  sedprev: Temporary sediment-from-previous-day value used in urban modeling; cleared before
    new sediment routing is computed.
  irmmdt: Urban-modeling temporary integer flag/counter; reset to zero with the other daily
    carryover values.
uses:
  time_module: '`time%step` tells `varinit` whether the simulation is running daily or subdaily.
    That matters because hourly runoff storage `hhqday(j,:)` is only cleared when there is
    more than one step per day, so the routine preserves the expected time-resolution behavior.'
  hru_module: These HRU-module variables are the daily water, sediment, plant, and nutrient
    accumulators that downstream land-phase routines read after initialization. `varinit`
    must zero them so subsequent hydrologic, erosion, and management calculations start from
    a consistent daily baseline for the active HRU.
  soil_module: '`soil(j)%nly` determines how many layers the active HRU has, and the layer
    members `prk` and `flat` are daily soil-flow carryover terms. `varinit` needs the soil
    profile so it can clear each layer''s state before the next day''s percolation and lateral-flow
    calculations.'
  hydrograph_module: '`wet_seep_day(j)` stores daily wetland seepage nutrient outputs for
    the active HRU. `varinit` clears these components so wetland seepage mass-balance values
    do not persist across days.'
---

<!-- facts:header -->

Initializes per-HRU daily state before the land-phase simulation proceeds. It clears soil-layer carryover, runoff/erosion, water balance, crop stress, and wetland seepage accumulators for the active HRU.

## Bottom Line

`varinit` is a reset routine called once per HRU at the start of the daily land-phase workflow. It uses the current HRU index and the simulation time step to clear a wide set of daily accumulators so each HRU starts the next model pass from a clean state.

It zeroes layer-level soil storage terms, daily hydrology and plant-water variables, and several sediment/nutrient tracking outputs used by downstream runoff, erosion, and wetland seepage calculations. The routine matters because later daily computations assume these fields begin each cycle at zero rather than carrying stale values forward.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_control` prepares the active HRU state and then calls `varinit` after prior daily balance variables have been handled. This routine runs at the start of the HRU daily loop, and its zeroed state is then consumed by later land-phase calculations that compute runoff, soil water movement, erosion, and wetland seepage for that HRU.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select active HRU | Copies `ihru` into local `j` so all resets operate on the current HRU element. |
| 2. clear soil layers | Loops over every soil layer in `soil(j)` and resets the layer percolation and lateral-flow storage terms `prk` and `flat` to zero. |
| 3. reset daily water and crop state | Zeros the HRU's daily albedo, biomass, runoff lag, canopy evaporation, crack flow, enrichment ratio, evapotranspiration, fertilizer, grazing, infiltration, tile flow, runoff, snow, soil water excess, nitrogen deficiency, erosion, vapor pressure deficit, and total crack volume accumulators. |
| 4. clear subdaily runoff conditionally | If the simulation uses more than one time step per day, clears `hhqday(j,:)` so the active HRU's subdaily runoff history does not carry into the next day. |
| 5. reset urban and sediment outputs | Zeros urban-model sediment carryover (`sedprev`, `ubnrunoff`, `irmmdt`, `hhsedy`, `ubntss`) and clears the active HRU's wetland seepage nutrient outputs (`no3`, `nh3`, `orgn`, `solp`, `sedp`). |
| 6. return to caller | Returns to `hru_control` after the active HRU's daily state has been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%step` |
| [sym:hru_module] | `hhqday, ihru, albday, bioday, bsprev, canev, ep_day, ep_max, es_day, fertn, fertp, grazn, grazp, hhsedy, inflpcp, latqrunon, ls_overq, lyrtile, qp_cms, pet_day, qday, qtile, sepday, snoev, snofall, snomlt, sw_excess, ubnrunoff, ubntss, uno3d, usle, usle_ei, voltot, vpd, fixn` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%ly(ly)%prk, soil(j)%ly(ly)%flat` |
| [sym:hydrograph_module] | `wet_seep_day` | `wet_seep_day(j)%no3, wet_seep_day(j)%nh3, wet_seep_day(j)%orgn, wet_seep_day(j)%solp, wet_seep_day(j)%sedp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(j)%ly(ly)%prk` | For every `ly` from 1 to `soil(j)%nly`. | `soil(j)%ly(ly)%prk` is reset to zero so the layer does not retain prior-day percolation before the next day's soil-water movement is computed. |
| `soil(j)%ly(ly)%flat` | For every `ly` from 1 to `soil(j)%nly`. | `soil(j)%ly(ly)%flat` is reset to zero so the layer starts the day without leftover lateral-flow storage. |
| `albday` | Always, once the active HRU is selected. | `albday` is cleared to start the new day with no stored albedo value from the previous HRU/day pass. |
| `bioday` | Always, once the active HRU is selected. | `bioday` is cleared so daily biomass generation can be recomputed from zero carryover. |
| `bsprev` | Always, once the active HRU is selected. | `bsprev` is reset to remove lagged surface-runoff storage from the previous day. |
| `canev` | Always, once the active HRU is selected. | `canev` is reset so canopy evaporation starts from zero for the new day. |
| `ep_day` | Always, once the active HRU is selected. | `ep_day` is cleared so daily transpiration can accumulate fresh for the current day. |
| `ep_max` | Always, once the active HRU is selected. | `ep_max` is cleared so the day's maximum transpiration allowance can be recomputed. |
| `es_day` | Always, once the active HRU is selected. | `es_day` is reset so soil evaporation accumulates only the current day's amount. |
| `fertn` | Always, once the active HRU is selected. | `fertn` is cleared so daily fertilizer nitrogen inputs do not carry across days. |
| `fertp` | Always, once the active HRU is selected. | `fertp` is cleared so daily fertilizer phosphorus inputs do not carry across days. |
| `fixn` | Always, once the active HRU is selected. | `fixn` is reset so nitrogen fixation starts fresh for the current day. |
| `grazn` | Always, once the active HRU is selected. | `grazn` is cleared so grazing nitrogen removal is accumulated only for the current day. |
| `grazp` | Always, once the active HRU is selected. | `grazp` is cleared so grazing phosphorus removal is accumulated only for the current day. |
| `inflpcp` | Always, once the active HRU is selected. | `inflpcp` is reset so infiltration from precipitation is recomputed for the new day. |
| `lyrtile` | Always, once the active HRU is selected. | `lyrtile` is reset so tile-drain flow by layer begins the day at zero. |
| `qp_cms` | Always, once the active HRU is selected. | `qp_cms` is reset so the day's peak runoff rate can be recomputed from new runoff conditions. |
| `pet_day` | Always, once the active HRU is selected. | `pet_day` is cleared so potential evapotranspiration accumulates only for the current day. |
| `qday` | Always, once the active HRU is selected. | `qday` is reset so daily surface runoff starts from zero. |
| `qtile` | Always, once the active HRU is selected. | `qtile` is reset so daily drainage-tile flow starts from zero. |
| `ls_overq` | Always, once the active HRU is selected. | `ls_overq` is cleared so lateral-subsurface overland flow does not persist into the new day. |
| `latqrunon` | Always, once the active HRU is selected. | `latqrunon` is cleared so lateral runon is recomputed for the current day only. |
| `sepday` | Always, once the active HRU is selected. | `sepday` is reset so percolation from the bottom soil layer accumulates only for the current day. |
| `snoev` | Always, once the active HRU is selected. | `snoev` is reset so snow sublimation starts from zero each day. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was introduced in `df07e3f` with the full daily HRU initialization block. Commit `94b6dec` later imported the same source and preserved the routine structure. Commit `39fabde` changed local variable declarations in `varinit` by giving `j`, `ly`, `crk`, `enratio`, `etday`, `over_flow`, `sedprev`, and `irmmdt` explicit zero initial values, and `f1e61a3` only adjusted indentation in the urban-modeling block without changing behavior.

- `df07e3f` added `varinit` as the HRU daily-state initialization routine, including zeroing of soil-layer state, daily HRU balances, subdaily runoff, and wetland seepage outputs.
- `39fabde` changed initialization semantics at declaration time by assigning default zero values to the local control and temporary variables used in the routine.
- `f1e61a3` made formatting-only tab-to-space changes in the urban-modeling comment and assignments; no functional behavior changed.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'varinit' has no extracted documentation comment.
