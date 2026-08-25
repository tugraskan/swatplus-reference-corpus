---
kind: procedure
symbol: res_weir_release
title: res_weir_release
status: filled
source_hash: fcc4473c1e7086e6
version_label: SWAT+ 62.0.0
args:
  jres: '`jres` selects which wetland or HRU entry is being processed. The routine uses it
    to read `wet_ob(jres)%iweir` and `hru(jres)%area_ha`, so it controls the active weir configuration
    and, for paddy cases, the surface area used to convert depth to volume.'
  id: '`id` is an unused reservoir decision-table identifier in this routine. It is only present
    to match the caller signature; the code does not use it to control release behavior.'
  ihyd: '`ihyd` selects the wetland hydrology record used to decide whether the current case
    is a paddy or a wetland. That choice changes which surface area is used in the discharge
    calculation.'
  evol_m3: '`evol_m3` is the emergency storage limit in cubic meters. If the current volume
    exceeds this threshold, the excess is treated as emergency spillway release before the
    weir discharge loop continues.'
  dep: '`dep` is the current ponding depth above the reservoir bottom. It is compared with
    `weir_hgt` to compute `hgt_above`, the water height available to drive weir flow.'
  weir_hgt: '`weir_hgt` is the crest elevation of the weir above the reservoir bottom. Together
    with `dep`, it determines whether any water is above the crest and how much discharge
    head is available.'
locals:
  iweir: '`iweir` holds the weir index used to look up the discharge coefficients in `res_weir(iweir)`.
    It is initialized to 1 and then overwritten from `wet_ob(jres)%iweir` before discharge
    is computed.'
  nstep: '`nstep` controls how many release substeps are used in the day. It is set to 1 here,
    so the routine follows the single-day/24-hour branch rather than a multi-step loop.'
  tstep: '`tstep` is the outer loop counter over release substeps. With `nstep = 1`, it still
    provides the one-pass control structure that surrounds the release calculation.'
  ic: '`ic` is the inner hourly counter used only in the `nstep <= 1` branch. It steps through
    up to 24 hourly discharge calculations until the storage above the weir is depleted or
    nearly depleted.'
  vol: '`vol` stores the current remaining water volume in the reservoir/wetland body. The
    routine subtracts released volume from it and writes the final value back to `wbody%flo`.'
  res_h: '`res_h` is the computed water depth from volume divided by surface area. It is used
    to recompute how far the water surface stands above the weir crest after each release
    subtraction.'
  wsa1: '`wsa1` is the active water surface area in square meters. It is set from `hru(jres)%area_ha`
    for paddy cases or `wbody_wb%area_ha` for wetlands, and it converts between depth and
    volume.'
  qout: '`qout` holds the amount of water discharged during the current substep. It is computed
    from the weir equation and then capped so it cannot exceed the volume available above
    the crest.'
  hgt_above: '`hgt_above` is the water height above the weir crest. It is the head term in
    the weir equation, and the routine recomputes it after each release so discharge can decay
    as storage is drained.'
  vol_above: '`vol_above` tracks how much volume is currently stored above the weir crest.
    It is used to prevent the routine from releasing more than the above-crest water actually
    available.'
uses:
  reservoir_data_module: '`reservoir_data_module` provides the hydrology name and the configured
    weir geometry used to decide both the release regime and the magnitude of the discharge.
    `wet_hyd(ihyd)%name` determines whether the routine treats the water body as paddy or
    wetland, and `res_weir(iweir)%c`, `%w`, and `%k` supply the coefficients for the weir-flow
    formula.'
  reservoir_module: '`reservoir_module` provides the per-wetland management metadata needed
    to pick the correct weir definition. `wet_ob(jres)%iweir` selects which `res_weir` parameter
    set to use for this specific reservoir or wetland instance.'
  conditional_module: This module is imported by the subroutine, but the extracted source
    does not show any concrete references to its state or types. It may support management
    logic in related code paths, but no direct dependency was resolved here.
  climate_module: This module is imported but no climate variable or type is referenced in
    the visible routine body. It matters only as a potential shared dependency in the broader
    reservoir/wetland management code, not in the extracted calculations here.
  time_module: This module is imported, but the extracted routine does not directly reference
    any time-state symbol from it. The release calculation itself is purely arithmetic once
    the caller has entered the routine.
  hydrograph_module: '`hydrograph_module` matters because it owns the flow accumulators that
    receive the released volume. `wbody%flo` is the current storage being reduced, and `ht2%flo`
    is where the routine records the water discharged out of the reservoir/wetland.'
  water_body_module: '`water_body_module` matters because the routine uses `wbody_wb%area_ha`
    as the water-surface area for wetlands. That area controls the head-to-volume conversion
    for non-paddy cases and scales the weir discharge formula.'
  soil_module: The module is imported, but the extracted procedure body does not reference
    a soil field directly. It is likely included because this wetland release routine sits
    in a larger hydrologic context where soil states are handled nearby, but no direct dependency
    is visible here.
  hru_module: '`hru_module` matters because paddy release uses the HRU area instead of the
    wetland body area. `hru(jres)%area_ha` provides the surface area needed to compute the
    volume represented by a given water depth.'
  water_allocation_module: This module is imported but no allocation-specific symbol appears
    in the visible code. It may be part of the broader wetland management environment, but
    it does not directly control the extracted release computation.
  basin_module: The module is imported, but the routine body does not reference a basin-state
    symbol in the extracted lines. It does not directly affect the release arithmetic shown
    here.
---

<!-- facts:header -->

Computes weir outflow for a wetland or paddy reservoir and updates reservoir storage after that release. It uses the configured weir geometry and current ponding depth to move water from the reservoir body into the outflow accumulator.

## Bottom Line

res_weir_release computes scheduled/manual weir discharge for a wetland or paddy storage unit. It starts from the current water volume in `wbody%flo`, picks the active weir ID from `wet_ob(jres)%iweir`, determines the wetted surface area from either the HRU or the water body, and then applies the weir equation using `res_weir(iweir)%c`, `%w`, and `%k` to move water out of storage.

The routine matters because it is the actual release step used by `wetland_control` for paddy management. It updates `wbody%flo` and records the released volume in `ht2%flo`, so later wetland/reservoir accounting sees the reduced storage and the corresponding outflow volume.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside wetland control when the model is handling a paddy-style wetland release. `wetland_control` prepares the current depth, crest height, hydrology type, and reservoir identifiers before calling it, and the result feeds back into `wet(j)%flo` and the shared hydrograph storage so later wetland/reservoir accounting uses the updated volume and discharge.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize storage, step counters, and the active weir ID. | The routine starts with the current storage in `wbody%flo`, chooses `wet_ob(jres)%iweir` as the active weir, and zeroes `vol_above` before any discharge is computed. This sets up the state needed to calculate how much water lies above the crest. |
| 2. Choose the operating surface area from hydrology type. | If `wet_hyd(ihyd)%name` is `paddy`, the routine uses `hru(jres)%area_ha`; otherwise it uses `wbody_wb%area_ha`. The selected area becomes `wsa1`, which converts depth to volume for the rest of the release calculation. |
| 3. Compute water height above the weir crest. | The routine computes `hgt_above = max(0., dep - weir_hgt)`, so no release head exists unless the ponded depth exceeds the crest height. This establishes the initial driving head for the weir equation. |
| 4. Skip the unused decision-table logic and enter the release loop. | The decision-table block is commented out, so the routine proceeds directly to the loop over `tstep = 1, nstep`. With `nstep` initialized to 1, this is effectively a single-day release pass. |
| 5. Apply the release logic only when water is above the crest and a weir is active. | Inside the loop, the routine first checks that `hgt_above > 0` and `iweir > 0`. If the current volume exceeds `evol_m3`, it sends the excess to `ht2%flo`, clamps the stored volume to the emergency threshold, and recomputes `res_h` and `hgt_above`; it then computes `vol_above = hgt_above * wsa1` as the volume sitting above the crest. |
| 6. Compute multi-step weir discharge when `nstep > 1`. | For the multi-step branch, the routine evaluates the weir equation using the configured coefficient, width, and exponent, scales it by the daily time fraction, and limits the release to the volume available above the crest. It subtracts the released amount from `vol`, updates `ht2%flo`, recomputes depth/head, and exits early when the above-crest water is nearly gone. |
| 7. Compute hourly weir discharge when `nstep <= 1`. | For the single-step branch, the routine loops over 24 hourly increments, using the same weir equation and scaling by one hour. Each pass subtracts either the full above-crest storage or the hourly discharge from `vol`, updates `ht2%flo`, recomputes the remaining head, and stops once the remaining above-crest volume is negligible. |
| 8. Write back the remaining reservoir storage and return. | If no release is possible, `ht2%flo` is reset to zero; otherwise the routine still writes the reduced storage back to `wbody%flo` at the end of the loop. The updated storage and accumulated discharge are then returned to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `wet_hyd, res_weir` | `wet_hyd(ihyd)%name, res_weir(iweir)%c, res_weir(iweir)%w, res_weir(iweir)%k` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(jres)%iweir` |
| [sym:conditional_module] | `conditional_module state/types were not resolved to specific component references in the extracted source` |  |
| [sym:climate_module] | `climate_module state/types were not resolved to specific component references in the extracted source` |  |
| [sym:time_module] | `time_module state/types were not resolved to specific component references in the extracted source` |  |
| [sym:hydrograph_module] | `wbody, ht2` | `wbody%flo, ht2%flo` |
| [sym:water_body_module] | `wbody_wb` | `wbody_wb%area_ha` |
| [sym:soil_module] | `soil_module state/types were not resolved to specific component references in the extracted source` |  |
| [sym:hru_module] | `hru` | `hru(jres)%area_ha` |
| [sym:water_allocation_module] | `water_allocation_module state/types were not resolved to specific component references in the extracted source` |  |
| [sym:basin_module] | `basin_module state/types were not resolved to specific component references in the extracted source` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ht2%flo` | When `hgt_above > 0` and `iweir > 0`, and after any emergency spill above `evol_m3` has been accounted for. | `ht2%flo` accumulates the water volume released from the wetland/reservoir. It increases by either the emergency spill amount, the capped weir discharge, or the full remaining above-crest volume when that is smaller than the computed outflow. |
| `wbody%flo` | At the end of each loop pass, after the routine has subtracted any spill or weir discharge from `vol`; if no discharge is allowed, it is set to zero in the else branch. | `wbody%flo` is overwritten with the remaining stored water volume after release. This is the primary storage state that later wetland and hydrograph routines will read. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f with the initial release algorithm and imports. Later commits changed behavior: 39fabde initialized several locals and made `id` explicitly unused, bd18ad4 removed the decision-table counter logic and `weir_flg` check, e18817a added `vol_above` and changed the release logic to cap discharge by above-crest volume instead of total volume, and 645ac00 changed the active weir default and scaled the discharge formula by `wbody_wb%area_ha*0.45` with explanatory comments.

- df07e3f added `res_weir_release` with the basic paddy/wetland area selection, crest-head computation, and release loop.
- 39fabde initialized local variables and marked `id` as unused without changing the release math.
- bd18ad4 removed the decision-table branch from active use and left a no-op `id` check to suppress warnings.
- e18817a introduced `vol_above` and changed the routine to limit discharge by water above the weir crest rather than by total reservoir volume.
- 645ac00 set the default weir index to 1 and scaled the weir equation by `wbody_wb%area_ha*0.45`, changing the magnitude of computed outflow.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_weir_release' has no extracted documentation comment.
- conditional_module, climate_module, time_module, soil_module, water_allocation_module, and basin_module were imported but no concrete symbol references were resolved in the extracted routine body.
- algorithm_steps revised: compressed the source into 8 behavior-focused steps and cited only line ranges visible in the provided source block.
