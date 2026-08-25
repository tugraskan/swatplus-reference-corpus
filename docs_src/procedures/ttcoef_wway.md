---
kind: procedure
symbol: ttcoef_wway
title: ttcoef_wway
status: filled
source_hash: 86de30cd600351da
version_label: SWAT+ 62.0.0
args:
  k: '`k` selects which HRU and matching grassed-waterway parameter record to read and update;
    all geometry and routing coefficients are computed for `hru(k)` and written to `grwway_vel(k)`.'
locals:
  fps: Temporary side-slope factor for the 1.2-bankfull low-flow geometry; it is set to 4.0
    and used in the widened cross-section calculation.
  b: Working bottom-width value for the trapezoidal waterway cross section. It is derived
    from HRU width and depth, checked for validity, and then copied to `grwway_vel(k)%wid_btm`.
  d: Working flow depth. It is first set to the HRU's bankfull waterway depth, then reused
    for 1.2-bankfull and 0.1-bankfull coefficient calculations.
  p: Working wetted perimeter of the cross section, recomputed for each depth case before
    calculating hydraulic radius.
  a: Working cross-sectional flow area, recomputed for bankfull and low-flow cases and stored
    to `grwway_vel(k)%area` for the bankfull case.
  qq1: Temporary discharge-like value returned by `Qman` for the current low-flow geometry;
    it is used to form travel-time coefficients at 1.2-bankfull and 0.1-bankfull depth.
  rh: Working hydraulic radius, computed as area divided by wetted perimeter and passed to
    `Qman`.
  tt1: Temporary travel-time coefficient for the 1.2-bankfull and 0.1-bankfull cases; it is
    computed locally but not stored in the module state.
  tt2: Temporary bankfull travel-time coefficient; it is computed locally from bankfull area
    and velocity but not written out.
  aa: Unit area factor passed to `Qman` when the routine wants flow velocity rather than discharge;
    it is fixed at 1.0.
  chsslope: Channel side-slope factor for the trapezoidal section. It starts at 8:1 for the
    waterway default, may be reset if the bottom width would be invalid, and is used in perimeter
    and area formulas.
  qman: External Manning-equation helper used to compute either discharge or velocity from
    area, hydraulic radius, roughness, and slope.
uses:
  hru_module: The HRU module holds the waterway design inputs for each `k`—depth, width, length,
    slope, and Manning's n—so this routine can derive the hydraulic geometry and travel-time
    coefficients from the land-management settings attached to that HRU.
  channel_velocity_module: The channel-velocity module owns the `grwway_vel` records that
    persist the computed bottom width, bankfull area, velocities, celerities, and storage-time
    terms for later routing code to use.
---

<!-- facts:header -->

Computes travel-time and velocity coefficients for a grassed waterway cross section tied to one HRU.

## Bottom Line

ttcoef_wway builds the geometric and Manning-based routing coefficients for one grassed waterway identified by `k`. It reads the HRU's waterway width, depth, length, slope, and roughness, then stores derived channel shape and travel-time terms in `grwway_vel(k)`.

The routine also guards against an impossible trapezoidal section when the computed bottom width would be nonpositive. In that case it resets the geometry to a narrower bottom and recomputes the side slope so later routing calculations have a usable cross section.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after `structure_set_parms` has prepared the grassed-waterway dimensions for the selected HRU and before routing uses the resulting velocity/storage coefficients. `structure_set_parms` calls it once the waterway depth has been adjusted to a feasible value, and the values it writes into `grwway_vel(k)` support later waterway routing behavior in the model.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local working values and defaults. | Sets `aa` to 1.0, clears `b`, and clears `d` so the geometry calculations start from a known state. |
| 2. Apply the default side slope for a grassed waterway. | Uses an 8:1 side slope default and sets `fps` to 4.0 for the later widened low-flow cross-section calculation. |
| 3. Read the HRU's bankfull depth and compute the initial bottom width. | Copies `grwat_d` into `d` and computes `b` from the HRU waterway width minus the two sloping sides. |
| 4. Repair impossible trapezoid geometry when bottom width is nonpositive. | If the computed bottom width is zero or negative, the routine resets the bottom width to half the total width and recomputes the side slope so the section remains physically valid. |
| 5. Store the bankfull geometry in the velocity-parameter record. | Writes the final bottom width and bankfull depth to `grwway_vel(k)`. |
| 6. Compute bankfull perimeter, area, hydraulic radius, velocity, celerity, storage distance, and travel time. | Builds the bankfull trapezoid geometry, calls `Qman` for discharge and unit-area velocity, derives celerity and storage distance, and forms the bankfull travel-time coefficient. |
| 7. Form the widened 1.2-bankfull low-flow geometry and compute its travel-time terms. | Resets the working values, sets depth to 1.2 times bankfull depth, expands the area and perimeter with the floodplain-side term, and computes low-flow discharge and travel time. |
| 8. Form the 0.1-bankfull low-flow geometry and store the low-flow routing coefficients. | Recomputes the trapezoid at 0.1 bankfull depth, derives discharge and velocity, and stores the low-flow velocity, celerity, and storage distance in `grwway_vel(k)`. |
| 9. Return to the caller. | Ends the subroutine after populating the persistent routing coefficients. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(k)%lumv%grwat_d, hru(k)%lumv%grwat_w, hru(k)%lumv%grwat_s, hru(k)%lumv%grwat_l` |
| [sym:channel_velocity_module] | `grwway_vel` | `grwway_vel(k)%wid_btm, grwway_vel(k)%dep_bf, grwway_vel(k)%area, grwway_vel(k)%vel_bf, grwway_vel(k)%velav_bf, grwway_vel(k)%celerity_bf, grwway_vel(k)%st_dis, grwway_vel(k)%vel_1bf, grwway_vel(k)%celerity_1bf, grwway_vel(k)%stor_dis_1bf` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `grwway_vel(k)%wid_btm` | When the bankfull geometry has been checked and a valid bottom width is available. | `grwway_vel(k)%wid_btm` is updated to the final trapezoidal bottom width used for the grassed waterway cross section. |
| `grwway_vel(k)%dep_bf` | When the HRU's grassed-waterway depth has been read for this `k`. | `grwway_vel(k)%dep_bf` records the bankfull water depth for later routing and geometry calculations. |
| `grwway_vel(k)%area` | After bankfull area is computed from the final geometry. | `grwway_vel(k)%area` stores the bankfull cross-sectional flow area used in Manning-based travel calculations. |
| `grwway_vel(k)%vel_bf` | After bankfull discharge is computed from `Qman`. | `grwway_vel(k)%vel_bf` stores the bankfull flow rate returned by `Qman` for the waterway section. |
| `grwway_vel(k)%velav_bf` | After bankfull velocity is computed with unit area passed to `Qman`. | `grwway_vel(k)%velav_bf` stores the bankfull average velocity used to derive wave celerity. |
| `grwway_vel(k)%celerity_bf` | After bankfull average velocity has been computed. | `grwway_vel(k)%celerity_bf` stores the bankfull wave celerity derived from average velocity. |
| `grwway_vel(k)%st_dis` | After bankfull celerity has been computed. | `grwway_vel(k)%st_dis` stores the bankfull storage-distance time constant in hours. |
| `grwway_vel(k)%vel_1bf` | After the 0.1-bankfull low-flow geometry is computed. | `grwway_vel(k)%vel_1bf` stores the low-flow average velocity for the 0.1-bankfull case. |
| `grwway_vel(k)%celerity_1bf` | After the 0.1-bankfull low-flow average velocity is computed. | `grwway_vel(k)%celerity_1bf` stores the low-flow wave celerity used in routing stability calculations. |
| `grwway_vel(k)%stor_dis_1bf` | After the 0.1-bankfull low-flow celerity is computed. | `grwway_vel(k)%stor_dis_1bf` stores the low-flow storage-distance time constant for the grassed waterway. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `ttcoef_wway`: df07e3f added the subroutine with the full grassed-waterway travel-time calculation; 94b6dec introduced the current source version in the repository; 39fabde initialized the local working variables and later bd18ad4 made `qman` an explicit external and changed the file end marker to `end subroutine ttcoef_wway`.

- df07e3f introduced the routine and its bankfull/low-flow Manning-based calculations for grassed waterways.
- 94b6dec added the source file content used as the baseline for this routine in the repository history.
- 39fabde set local scratch variables to zero at declaration time, removing reliance on implicit initialization.
- bd18ad4 clarified `qman` as an external procedure and updated the ending statement to a named subroutine end.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ttcoef_wway' has no extracted documentation comment.
