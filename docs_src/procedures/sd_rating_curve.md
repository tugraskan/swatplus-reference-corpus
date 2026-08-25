---
kind: procedure
symbol: sd_rating_curve
title: sd_rating_curve
status: filled
source_hash: 9fc85ff0d846f508
version_label: SWAT+ 62.0.0
args:
  i: Selects which reach in `sd_ch` and `ch_rcurv` is updated; all geometry, flow, and travel-time
    calculations are done for that one channel element.
locals:
  i_dep: Loop index for the two in-channel points and then the two floodplain points. It also
    determines which `ch_rcurv(i)%elev(...)` slot gets filled.
  ifp_dep: Derived index used to map the floodplain loop’s `i_dep = 1,2` onto `ch_rcurv(i)%elev(3:4)`
    for the above-bankfull rating-curve entries.
  a: Temporary cross-sectional flow area at the current depth, used for Manning discharge,
    storage volume, and floodplain area calculations.
  b: Temporary bottom width of the main channel. It is derived from channel width, depth,
    and side slope, and corrected if it becomes nonpositive.
  p: Temporary wetted perimeter at the current depth, used to compute hydraulic radius and
    store the rating-curve geometry.
  rh: Temporary hydraulic radius (`a / p`) passed to `Qman` for discharge and velocity calculations.
  qman: External Manning-equation function. It is used as a generic calculator for both discharge
    (with area `a`) and velocity (with area `1.`).
  dep: Temporary water depth for the current rating-curve point. It is set to bankfull fractions
    in the first loop and to above-bankfull fractions in the second loop.
  a_bf: Saved bankfull cross-sectional area from the in-channel loop; reused to build the
    floodplain cross section above bankfull.
  p_bf: Saved bankfull wetted perimeter from the in-channel loop; reused as the starting perimeter
    for floodplain points.
  vol_bf: Saved bankfull channel volume; reused as the channel-volume baseline when floodplain
    storage is added.
  vel: Temporary velocity returned by `Qman(1., ...)`, used to compute travel time along the
    reach.
  frac_abov: Fraction of bankfull depth used to define the two floodplain depths, first 0.2
    and then 1.0.
uses:
  sd_channel_module: '`sd_channel_module` provides the reach-geometry state and rating-curve
    containers that this routine reads and fills. `sd_ch(i)` supplies channel width, depth,
    side slopes, roughness, length, and floodplain parameters, while `ch_rcurv(i)` receives
    the computed depth, area, perimeter, volume, flow, and travel-time values.'
  channel_velocity_module: 'This module supplies the Manning-based velocity/discharge calculation
    used to turn geometry and roughness into flow rate and travel time. The routine calls
    `Qman` twice per point: once for discharge and once for unit-area velocity.'
  maximum_data_module: This module is imported because the rating-curve calculation relies
    on shared maximum-data definitions available to the hydrologic setup. The context packet
    does not resolve a specific symbol from it, so its role here is limited to supporting
    the imported calculation environment.
---

<!-- facts:header -->

Builds channel and floodplain rating-curve values for one reach index `i`. It computes geometry, flow, and travel-time points at bankfull and above-bankfull depths.

## Bottom Line

`sd_rating_curve` generates a small rating curve for the selected SWAT+ channel reach. Using the reach geometry stored in `sd_ch(i)`, it first fixes an invalid bottom width if needed, then computes hydraulic properties at two in-channel depths and two floodplain depths. Those results are written into `ch_rcurv(i)%elev(...)` for later use by hydrology and sediment routines.

The routine matters because it prepares the channel response relationships that downstream model code can use to relate depth, area, discharge, storage volume, and travel time. `sd_hydsed_init` calls it during initialization after it has set the reach geometry and derived the floodplain side slope inputs.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`sd_rating_curve` runs during hydrologic/sediment initialization after `sd_hydsed_init` has prepared the reach geometry, including bottom width, depth, side slope, and floodplain slope inputs. Its outputs seed the stored rating-curve tables that later channel routing and floodplain calculations depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute channel bottom width and correct invalid values | Derive the main-channel bottom width from channel width, depth, and side slope. If the result is nonpositive, replace it with half the channel width, clamp it to zero or above, and back-calculate a usable side slope into `sd_ch(i)%chss`. |
| 2. loop over in-channel rating points | Evaluate two depths within the main channel: a shallow point at 10% of bankfull depth and a bankfull point at 100% of bankfull depth. |
| 3. set in-channel depth | Select the current depth for the loop: `0.1 * sd_ch(i)%chd` for the first point and `sd_ch(i)%chd` for the second. |
| 4. compute in-channel geometry | Compute wetted perimeter, cross-sectional area, and hydraulic radius for the current in-channel depth using the stored bottom width and side slope. |
| 5. store in-channel rating-curve values | Write depth, perimeter, area, width, surface area, volume, channel volume, floodplain volume, discharge, and travel time into `ch_rcurv(i)%elev(i_dep)` for the current in-channel point. |
| 6. save bankfull reference values | When the loop reaches the bankfull point, cache bankfull perimeter, area, and channel volume for use in the floodplain calculations. |
| 7. loop over floodplain rating points | Evaluate two above-bankfull points corresponding to 20% and 100% of bankfull depth above the bankfull line. |
| 8. set above-bankfull fraction | Choose the above-bankfull depth fraction (`0.2` or `1.0`) and convert it to a depth above bankfull. |
| 9. compute floodplain geometry | Build the floodplain wetted perimeter, cross-sectional area, and hydraulic radius from the saved bankfull geometry and the above-bankfull depth. |
| 10. map floodplain index and store values | Map the loop index to the floodplain rating-curve slots, then store depth, perimeter, area, width, surface area, channel volume baseline, floodplain volume, total volume, discharge, and travel time. |
| 11. return to caller | Finish the subroutine after both rating-curve loops have populated the channel and floodplain tables. |
| 12. end subroutine | Terminate the procedure definition. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sd_ch, ch_rcurv` | `sd_ch(i)%chw, sd_ch(i)%chd, sd_ch(i)%chss, ch_rcurv(i)%elev(i_dep)%dep, ch_rcurv(i)%elev(i_dep)%wet_perim, ch_rcurv(i)%elev(i_dep)%xsec_area, ch_rcurv(i)%elev(i_dep)%top_wid, ch_rcurv(i)%elev(i_dep)%surf_area, sd_ch(i)%chl, ch_rcurv(i)%elev(i_dep)%vol, ch_rcurv(i)%elev(i_dep)%vol_ch, ch_rcurv(i)%elev(i_dep)%vol_fp, ch_rcurv(i)%elev(i_dep)%flo_rate, sd_ch(i)%chs, ch_rcurv(i)%elev(i_dep)%ttime, sd_ch(i)%fps, ch_rcurv(i)%elev(ifp_dep)%dep, ch_rcurv(i)%elev(ifp_dep)%wet_perim, ch_rcurv(i)%elev(ifp_dep)%xsec_area, ch_rcurv(i)%elev(ifp_dep)%top_wid, ch_rcurv(i)%elev(ifp_dep)%surf_area, ch_rcurv(i)%elev(ifp_dep)%vol_ch, ch_rcurv(i)%elev(ifp_dep)%vol_fp, ch_rcurv(i)%elev(ifp_dep)%vol, ch_rcurv(i)%elev(ifp_dep)%flo_rate, ch_rcurv(i)%elev(ifp_dep)%ttime` |
| [sym:channel_velocity_module] | `channel_velocity_module` | `Qman` |
| [sym:maximum_data_module] | `maximum_data_module` | `maximum_data_module state or parameters used by Qman` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sd_ch(i)%chss` | When the computed bottom width `b` is less than or equal to zero. | `sd_ch(i)%chss` is recomputed from the corrected width so later geometry calculations have a usable side slope. |
| `ch_rcurv(i)%elev(i_dep)%dep` | During the first loop when `i_dep` is 1 or 2. | The current in-channel depth is stored for the rating-curve entry before geometry is derived. |
| `ch_rcurv(i)%elev(i_dep)%wet_perim` | During the first loop when `i_dep` is 1 or 2. | The computed in-channel wetted perimeter is stored for the current rating-curve point. |
| `ch_rcurv(i)%elev(i_dep)%xsec_area` | During the first loop when `i_dep` is 1 or 2. | The computed in-channel cross-sectional area is stored for the current rating-curve point. |
| `ch_rcurv(i)%elev(i_dep)%top_wid` | During the first loop when `i_dep` is 1 or 2. | The top width of the in-channel water surface is stored for the current rating-curve point. |
| `ch_rcurv(i)%elev(i_dep)%surf_area` | During the first loop when `i_dep` is 1 or 2. | The in-channel surface area is stored as top width times channel length. |
| `ch_rcurv(i)%elev(i_dep)%vol` | During the first loop when `i_dep` is 1 or 2. | The in-channel total volume is stored from area times reach length. |
| `ch_rcurv(i)%elev(i_dep)%vol_ch` | During the first loop when `i_dep` is 1 or 2. | The channel-volume component is set equal to the computed in-channel volume. |
| `ch_rcurv(i)%elev(i_dep)%vol_fp` | During the first loop when `i_dep` is 1 or 2. | The floodplain-volume component is set to zero because these points are still within the main channel. |
| `ch_rcurv(i)%elev(i_dep)%flo_rate` | During the first loop when `i_dep` is 1 or 2. | The discharge at the in-channel depth is stored from `Qman(a, rh, sd_ch(i)%chn, sd_ch(i)%chs)`. |
| `ch_rcurv(i)%elev(i_dep)%ttime` | During the first loop when `i_dep` is 1 or 2. | The travel time across the reach is stored from the `Qman(1., ...)` velocity estimate. |
| `ch_rcurv(i)%elev(ifp_dep)%dep` | Only when the first loop reaches bankfull (`i_dep == 2`). | The bankfull depth entry is set to `(1. + frac_abov) * sd_ch(i)%chd`, which evaluates to the bankfull depth for the floodplain baseline point stored at slot 3. |
| `ch_rcurv(i)%elev(ifp_dep)%wet_perim` | Only when the first loop reaches bankfull (`i_dep == 2`). | The bankfull wetted perimeter is reused for the floodplain baseline reference. |
| `ch_rcurv(i)%elev(ifp_dep)%xsec_area` | Only when the first loop reaches bankfull (`i_dep == 2`). | The bankfull cross-sectional area is reused for the floodplain baseline reference. |
| `ch_rcurv(i)%elev(ifp_dep)%top_wid` | Only when the first loop reaches bankfull (`i_dep == 2`). | The bankfull top width is used as the starting width for the floodplain rating point. |
| `ch_rcurv(i)%elev(ifp_dep)%surf_area` | Only when the first loop reaches bankfull (`i_dep == 2`). | The bankfull surface area is stored using the bankfull top width and channel length. |
| `ch_rcurv(i)%elev(ifp_dep)%vol_ch` | Only when the first loop reaches bankfull (`i_dep == 2`). | The stored channel-volume baseline is set to the bankfull channel volume saved in `vol_bf`. |
| `ch_rcurv(i)%elev(ifp_dep)%vol_fp` | Only when the first loop reaches bankfull (`i_dep == 2`). | The floodplain volume is set from floodplain width, above-bankfull depth, and channel length. |
| `ch_rcurv(i)%elev(ifp_dep)%vol` | Only when the first loop reaches bankfull (`i_dep == 2`). | Total volume is set to the channel baseline plus floodplain volume for the above-bankfull point. |
| `ch_rcurv(i)%elev(ifp_dep)%flo_rate` | Only when the first loop reaches bankfull (`i_dep == 2`). | The floodplain discharge is stored from `Qman(a, rh, sd_ch(i)%fpn, sd_ch(i)%chs)` using floodplain roughness. |
| `ch_rcurv(i)%elev(ifp_dep)%ttime` | Only when the first loop reaches bankfull (`i_dep == 2`). | The floodplain travel time is stored from the velocity estimate for the floodplain roughness. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits changed `sd_rating_curve`. Commit `df07e3f` added the subroutine with the full in-channel and floodplain rating-curve logic, and `94b6dec` carried that implementation forward unchanged except for bringing in the latest source snapshot. Commit `39fabde` then initialized the local scalars (`i_dep`, `ifp_dep`, `a`, `b`, `p`, `rh`, `dep`, `a_bf`, `p_bf`, `vol_bf`, `vel`, `frac_abov`) and later `bd18ad4` refined `qman` to an explicit external procedure declaration.

- df07e3f introduced the full geometry/discharge/travel-time rating-curve computation for in-channel and floodplain depths.
- 39fabde reduced uninitialized-variable risk by giving the local counters and temporaries default zero values.
- bd18ad4 clarified that `qman` is an external routine, preserving the same call behavior while making the interface explicit.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_rating_curve' has no extracted documentation comment.
- algorithm_steps revised: merged the final `return` and `end subroutine` into separate terminal steps while keeping all source-line citations from the extracted source.
- channel_velocity_module and maximum_data_module did not resolve specific imported symbols in the candidate references; their roles are inferred only from the imported procedure context and the available callee contract for Qman.
- The source defines `qman` as an external procedure in later lineage, but the current source span still shows only the call sites; the callee contract describes the intended Manning-equation behavior.
