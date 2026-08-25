---
kind: procedure
symbol: sq_canopyint
title: sq_canopyint
status: filled
source_hash: ef9ab868194554a2
version_label: SWAT+ 62.0.0
locals:
  xx: Temporary holder for the original precipitation value before interception is subtracted,
    so the routine can add that amount back when a subtraction drives a time-step precipitation
    value negative.
  j: The current HRU index, copied from `ihru` and used to access the active HRU's canopy,
    plant, and weather-linked state.
  ii: Loop counter over the subdaily time steps within the day.
  canmxl: The current day's maximum canopy storage capacity, computed from the HRU's maximum
    canopy storage and the plant community's current LAI ratio.
  canstori: The canopy storage amount at the start of the routine, used as the baseline when
    distributing additional interception across subdaily time steps.
  iwst: Index of the weather station connected to the current HRU's object, used to reach
    the station's precipitation time series.
  iob: Index of the connected hydrograph object for the current HRU, used to find the linked
    weather station number.
uses:
  basin_module: The routine imports `basin_module`, so basin-wide model state is available
    in scope even though the extracted lines do not show a direct symbol from that module.
    It matters here because this procedure runs inside the basin/HRU control flow and participates
    in basin-wide precipitation and interception accounting.
  time_module: The `time` object provides `time%step`, which determines whether the routine
    treats precipitation as daily or loops through subdaily slices. That time-step setting
    controls the entire branch structure of the interception calculation.
  climate_module: The `w` and `wst` weather objects provide the precipitation time series
    that this routine reduces by interception. `w%ts(ii)` is the active day’s subdaily precipitation
    series, and `wst(iwst)%weat%ts(ii)` is used when redistributing canopy storage across
    the day's time steps.
  hru_module: The current HRU supplies the object number, the maximum canopy storage parameter,
    and the shared canopy-storage array. Those values determine which HRU is updated and how
    much rainfall the canopy can hold before excess passes through.
  plant_module: The plant community provides the summed current LAI and summed maximum LAI
    used to scale the HRU's maximum canopy storage to the present canopy condition. Without
    those plant-community totals, the routine cannot compute `canmxl`.
  hydrograph_module: The connected object list provides the weather-station index for the
    current HRU. That link is what lets this routine reach the correct station precipitation
    series for interception adjustments.
---

<!-- facts:header -->

Computes canopy interception for the current HRU, reducing subdaily precipitation and updating canopy storage. It handles both multi-step subdaily storms and daily precipitation routing.

## Bottom Line

sq_canopyint computes how much precipitation is intercepted by the plant canopy for the current HRU. It uses the HRU's canopy capacity, plant community LAI, weather-station precipitation, and current time-step structure to shift water from precipitation into canopy storage.

If the simulation is running with subdaily time steps, it adjusts each time-step precipitation amount in `w%ts(ii)` and carries any remaining canopy storage forward through the day's substeps. For a daily time step, it updates `precip_eff` and `canstor(j)` directly so later runoff and routing calculations see the reduced rainfall and the filled canopy storage.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `hru_control` after soil temperature is computed and before snowmelt and downstream runoff routing. `hru_control` has already set the active HRU context (`ihru`) and the object/weather links needed to identify the correct HRU and weather station. Its outputs matter immediately for later snowmelt and overland-flow calculations because they depend on the precipitation remaining after canopy interception.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load active indices | Copies the active HRU index from `ihru`, then follows the HRU's object link to the connected weather-station index. |
| 2. skip sparse canopy | Returns immediately when either summed LAI or summed maximum LAI is too small to support canopy interception. |
| 3. branch on time step | Checks whether the simulation uses more than one precipitation time step per day and saves the starting canopy storage when subdaily processing is needed. |
| 4. compute daily canopy capacity | Scales the HRU's maximum canopy storage by the current LAI fraction to get today's canopy storage limit. |
| 5. intercept first subdaily series | Loops over the day's time steps, subtracts the available canopy space from each precipitation amount, stores the original amount in `xx`, and fills canopy storage until the step precipitation is exhausted or storage reaches the daily maximum. |
| 6. refill from remaining storage | If canopy storage increased above the starting value, loops through the same time steps again and removes the extra intercepted water from the weather-station precipitation series, again guarding against negative precipitation values. |
| 7. daily-step canopy interception | For daily time steps, computes the canopy limit once and either captures all effective precipitation or fills the canopy to capacity while leaving the remainder in `precip_eff`. |
| 8. finish | Returns to the caller after updating precipitation and canopy storage for the active HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state` | `basin-level state imported by use association, but no specific basin_module component is referenced in the extracted source lines` |
| [sym:time_module] | `time` | `time%step` |
| [sym:climate_module] | `w, wst` | `w%ts(ii), wst(iwst)%weat%ts(ii)` |
| [sym:hru_module] | `hru, canstor, ihru, precip_eff` | `hru(j)%obj_no, hru(j)%hyd%canmx` |
| [sym:plant_module] | `pcom` | `pcom(j)%lai_sum, pcom(j)%laimx_sum` |
| [sym:hydrograph_module] | `ob` | `ob(iob)%wst` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `w%ts(ii)` | When subdaily interception causes `w%ts(ii)` to go below zero, or when the daily branch fills from `precip_eff` | `w%ts(ii)` is reduced by intercepted canopy water so the remaining precipitation reaching the soil surface is smaller; if the subtraction would make it negative, the routine restores the excess to canopy storage logic and clips the precipitation to zero. |
| `canstor(j)` | When intercepted water increases canopy storage during subdaily processing, or when the daily branch stores rainfall in the canopy | `canstor(j)` is increased toward the day's canopy maximum so the HRU keeps track of how much water is held in the canopy after interception. |
| `precip_eff` | Only in the daily-time-step branch, after comparing `precip_eff` with the remaining canopy storage space | `precip_eff` is reduced by the amount intercepted by the canopy, or set to zero if all effective precipitation is captured, so later runoff and routing routines see only the rainfall that survives interception. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:2.1.1 | Daily canopy storage | $can_{day}=can_{mx}*\frac{LAI}{LAI_{mx}}$ | Verified against SWAT+ 62.0.0 (sq_canopyint.f90:53). canmxl = canmx*lai_sum/laimx_sum` — canopy storage |
| 2:2.1.2 | Interception when rainfall fits remaining storage | $R'_{day} \le can_{day} - R_{INT(i)}$ | Verified against SWAT+ 62.0.0 (sq_canopyint.f90:56). |
| 2:2.1.3 | Interception when rainfall exceeds remaining storage | $R'_{day}>can_{day}-R_{INT(i)}$ | Verified against SWAT+ 62.0.0 (sq_canopyint.f90:62). |

## Lineage

Three resolved commits changed `sq_canopyint`. df07e3f added the subroutine and its full canopy-interception logic. 94b6dec carried in the same code from the Bitbucket import without changing behavior in the shown snippet. 39fabde initialized the local scalars `xx`, `j`, `ii`, `canmxl`, `canstori`, `iwst`, and `iob` to zero. e18817a only added the inline comment `! time%step > 1` to the closing `end if` and did not alter the algorithm.

- df07e3f introduced the routine and its full subdaily/daily canopy-interception behavior.
- 39fabde changed only local-variable initialization defaults for `xx`, `j`, `ii`, `canmxl`, `canstori`, `iwst`, and `iob`.
- e18817a made a comment-only edit at the `end if` for the `time%step > 1` block.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_canopyint' has no extracted documentation comment.
