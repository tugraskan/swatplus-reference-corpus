---
kind: procedure
symbol: sim_initday
title: sim_initday
status: filled
source_hash: 70818b7dcc24e003
version_label: SWAT+ 62.0.0
locals:
  drift: Temporary daily pesticide drift mass to the main channel; it is initialized to zero
    so any drift added later in the day starts from no prior carryover.
  hrupstd: Temporary HRU pesticide output accumulator; it is zeroed at day start so the daily
    HRU pesticide standard/output value does not carry across days.
  j: HRU index for the outer loop over all HRUs when rebuilding soil summary totals.
  ly: Soil-layer index for the inner loop over layers within each HRU.
uses:
  hru_module: This module owns the HRU-level daily state arrays that `sim_initday` clears
    and recomputes. The routine's main job is to reset these shared outputs at the start of
    each day so downstream HRU, routing, sediment, nutrient, salt, carbon, and groundwater
    calculations accumulate into fresh daily totals.
  soil_module: '`soil(j)%nly` gives the number of soil layers in each HRU, which sets the
    bounds of the inner loop used to sum layer nutrients. Without the soil profile layer count,
    `sim_initday` could not traverse the full profile to rebuild `sol_sumno3` and `sol_sumsolp`.'
  organic_mineral_mass_module: '`soil1` holds the layered mineral mass pools for each HRU.
    `sim_initday` reads those layer pools to build the HRU-wide nutrient sums, including ammonium
    via `mn(ly)%nh4` and phosphorus via `mp(ly)%lab`.'
  carbon_module: This module is imported because the routine's soil-pool bookkeeping depends
    on the mass-state structures that also support carbon/mineral accounting. Even though
    the visible computation here uses mineral N and P totals, the shared soil-mass state is
    part of the coupled pool system used by carbon-related processes.
  hydrograph_module: '`sp_ob%hru` gives the number of HRU objects in the simulation. `sim_initday`
    uses it to decide whether daily initialization is needed and to size the HRU loop that
    rebuilds per-HRU totals.'
  reservoir_module: This routine is initialized alongside reservoir-linked daily bookkeeping
    so reservoir-related daily state can start clean when the new day begins, even though
    no reservoir field is directly assigned in the visible lines.
  maximum_data_module: This module matters because `sim_initday` participates in the model's
    daily reset sequence for shared maximum/summary data structures; its placement ensures
    daily maxima or counters from prior days do not leak into the next day.
  res_cs_module: This module is included so reservoir carbon/salt daily bookkeeping can be
    reset with the other coupled routing states at day start, keeping reservoir-related carbon/salt
    summaries synchronized with the rest of the model day initialization.
---

<!-- facts:header -->

Initializes daily HRU and reach-level summary arrays at the start of each model day. It also rebuilds per-HRU soil nitrogen and phosphorus totals from layer pools.

## Bottom Line

`sim_initday` is a daily reset routine. When `time_control` starts a new day and there are HRUs in the simulation, this subroutine zeros a large set of HRU output/state arrays so the new day's fluxes accumulate from a clean slate.

After the zeroing pass, it loops over every HRU and soil layer to recompute `sol_sumno3` and `sol_sumsolp` from the layered mineral N and P pools in `soil1`. Those totals are then available for later HRU output and process routines that need profile-wide nutrient sums.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`time_control` calls `sim_initday` once per day after the model's day counter and daily timing state have been advanced. The routine prepares HRU-wide daily summary arrays before process and routing calculations run, so later water, nutrient, sediment, salt, and carbon outputs can accumulate correctly for the new day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. clear daily HRU state | Set a broad set of HRU-level daily output and transport arrays to zero, including water, nutrient, sediment, salt, carbon, groundwater, and urban runoff summaries. |
| 2. reset soil summary accumulators | Initialize the HRU soil summary totals `sol_sumno3` and `sol_sumsolp` to zero before recomputing them from layer pools. |
| 3. loop over HRUs | Iterate across every HRU object in the simulation so each HRU's soil profile totals can be rebuilt. |
| 4. loop over soil layers | Within each HRU, iterate through all soil layers defined by `soil(j)%nly`. |
| 5. sum mineral nitrogen | Add each layer's nitrate and ammonium from `soil1(j)%mn(ly)` into the HRU nitrate summary `sol_sumno3(j)`. |
| 6. sum soluble phosphorus | Add each layer's labile mineral phosphorus from `soil1(j)%mp(ly)` into the HRU soluble phosphorus summary `sol_sumsolp(j)`. |
| 7. close loops and return | Finish the HRU and layer loops, then return to the caller with all daily arrays reinitialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sol_sumno3, sol_sumsolp, cbodu, chl_a, clayld, cnday, doxq, grayld, hhsurfq, lagyld, latno3, latq, nplnt, percn, pplnt, qdr, sagyld, sanyld, sedminpa, sedminps, sedorgn, sedorgp, sedyld, sepbtm, silyld, surfq, surqno3, surqsolp, tileno3, ubnrunoff, ubntss, gwsoilq, satexq, gwsoiln, gwsoilp, satexn, surqsalt, latqsalt, tilesalt, percsalt, urbqsalt, wetqsalt, wtspsalt, gwupsalt, surqcs, latqcs, tilecs, perccs, gwupcs, urbqcs, sedmcs, irswcs, irgwcs, wetqcs, wtspcs` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(ly)%nh4` |
| [sym:carbon_module] | `soil1` | `soil1(j)%mn(ly)%no3, soil1(j)%mn(ly)%nh4, soil1(j)%mp(ly)%lab` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:reservoir_module] | `reservoir state` |  |
| [sym:maximum_data_module] | `maximum-data state` |  |
| [sym:res_cs_module] | `reservoir carbon/salt state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cbodu` | At the start of every day when `sim_initday` is called. | `cbodu` is cleared to zero so the day's biochemical oxygen demand accumulation starts fresh and does not retain the prior day's value. |
| `chl_a` | At the start of every day when `sim_initday` is called. | `chl_a` is cleared to zero so algae/chlorophyll loading is rebuilt only from the current day onward. |
| `cnday` | At the start of every day when `sim_initday` is called. | `cnday` is cleared to zero so the daily curve-number or related CN summary does not carry over from yesterday. |
| `doxq` | At the start of every day when `sim_initday` is called. | `doxq` is cleared to zero so dissolved oxygen flux accumulation restarts for the new day. |
| `latno3` | At the start of every day when `sim_initday` is called. | `latno3` is cleared to zero so lateral nitrate load begins a new daily total. |
| `latq` | At the start of every day when `sim_initday` is called. | `latq` is cleared to zero so lateral flow quantity accumulation begins from zero for the current day. |
| `nplnt` | At the start of every day when `sim_initday` is called. | `nplnt` is cleared to zero so plant nitrogen-related daily bookkeeping is reset. |
| `percn` | At the start of every day when `sim_initday` is called. | `percn` is cleared to zero so percolation nitrogen-related daily accumulation starts fresh. |
| `pplnt` | At the start of every day when `sim_initday` is called. | `pplnt` is cleared to zero so plant phosphorus-related daily bookkeeping is reset. |
| `qdr` | At the start of every day when `sim_initday` is called. | `qdr` is cleared to zero so drainage flow accumulation starts from no prior daily flow. |
| `sedminpa` | At the start of every day when `sim_initday` is called. | `sedminpa` is cleared to zero so mineral phosphorus in sediment is recomputed from current-day processes only. |
| `sedminps` | At the start of every day when `sim_initday` is called. | `sedminps` is cleared to zero so soluble phosphorus in sediment is recomputed from current-day processes only. |
| `sedorgn` | At the start of every day when `sim_initday` is called. | `sedorgn` is cleared to zero so organic nitrogen in sediment is accumulated only for the current day. |
| `sedorgp` | At the start of every day when `sim_initday` is called. | `sedorgp` is cleared to zero so organic phosphorus in sediment is accumulated only for the current day. |
| `sedyld` | At the start of every day when `sim_initday` is called. | `sedyld` is cleared to zero so total sediment yield starts a fresh daily total. |
| `sanyld` | At the start of every day when `sim_initday` is called. | `sanyld` is cleared to zero so sand yield does not include prior-day mass. |
| `silyld` | At the start of every day when `sim_initday` is called. | `silyld` is cleared to zero so silt yield starts from zero for the day. |
| `clayld` | At the start of every day when `sim_initday` is called. | `clayld` is cleared to zero so clay yield starts from zero for the day. |
| `sagyld` | At the start of every day when `sim_initday` is called. | `sagyld` is cleared to zero so aggregate-sized sediment yield starts fresh. |
| `lagyld` | At the start of every day when `sim_initday` is called. | `lagyld` is cleared to zero so large aggregate yield starts fresh. |
| `grayld` | At the start of every day when `sim_initday` is called. | `grayld` is cleared to zero so gravel yield starts fresh. |
| `sepbtm` | At the start of every day when `sim_initday` is called. | `sepbtm` is cleared to zero so septic-bottom related daily mass starts from no carryover. |
| `surfq` | At the start of every day when `sim_initday` is called. | `surfq` is cleared to zero so surface runoff quantity starts a new daily accumulation. |
| `surqno3` | At the start of every day when `sim_initday` is called. | `surqno3` is cleared to zero so surface runoff nitrate load is rebuilt for the new day. |

## File I/O

<!-- facts:io -->


## Lineage

`sim_initday` was introduced in commit df07e3f as a new daily initialization routine that zeroes HRU state arrays and computes `sol_sumno3`/`sol_sumsolp` from soil layer pools. Commit 09d23f0 removed an old in-source comment above the soil-sum block. Commit 39fabde initialized local scalars `drift`, `hrupstd`, `j`, `ly`, and `ires`, and commit 2ee1889 later removed `ires` and changed the final `end` to `end subroutine sim_initday`. Commit 889136d only fixed a typo in the documentation comment.

- df07e3f added the full daily reset behavior and the soil-layer nutrient summation loop.
- 09d23f0 removed a stale explanatory comment before the soil summary block; behavior unchanged.
- 39fabde gave the local working variables explicit zero initial values, which changed initial state safety but not the overall algorithm.
- 2ee1889 removed the unused `ires` local and made the subroutine terminator explicit as `end subroutine sim_initday`.
- 889136d corrected a documentation typo from "occuring" to "occurring" without affecting code behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sim_initday' has no extracted documentation comment.
