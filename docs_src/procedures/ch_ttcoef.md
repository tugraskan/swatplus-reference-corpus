---
kind: procedure
symbol: ch_ttcoef
title: ch_ttcoef
status: filled
source_hash: 81498016c1957dc4
version_label: SWAT+ 62.0.0
args:
  k: '`k` selects the channel reach whose hydraulic geometry in `ch_hyd(k)` is evaluated and
    whose derived routing coefficients are stored in `ch_vel(k)`.'
locals:
  fps: Temporary floodplain side-slope factor used only in the 1.2-bankfull-depth calculation;
    it is set to 4. and used in the extra area and perimeter terms for the higher-flow case.
  d: Working flow depth for the current geometry case. It is first set to the bankfull depth,
    then reassigned to 1.2 and 0.1 times bankfull depth for the alternate travel-time calculations.
  b: Working bottom-width estimate of the channel. It is computed from top width, depth, and
    side slope, then adjusted if the estimate becomes nonpositive, and finally stored as the
    bankfull bottom width.
  p: Working wetted perimeter of the channel cross section at the current depth case, used
    with area to compute hydraulic radius.
  a: Working cross-sectional flow area at the current depth case, used to compute discharge,
    velocity, and hydraulic radius.
  qq1: Temporary discharge or flow-rate result from `qman` for the current depth case; it
    is used to form the travel-time coefficient `tt1`.
  rh: Working hydraulic radius, computed as area divided by wetted perimeter and passed to
    `qman`.
  tt1: Temporary travel-time coefficient for the low-flow and 1.2-bankfull cases, computed
    as `l * a / qq1` but not stored in `ch_vel`.
  tt2: Temporary bankfull travel-time coefficient, computed as `l * a / ch_vel(k)%vel_bf`
    but not stored in `ch_vel`.
  aa: Unit-area scaling factor passed to `qman` when the routine wants Manning velocity instead
    of discharge; it is set to 1. so `qman` returns velocity-like values.
  chsslope: Working channel side slope used in the trapezoid geometry formulas. It defaults
    to 2. if no side slope is provided and is adjusted again if the initial bottom-width estimate
    is invalid.
  qman: '`qman` is the Manning-equation calculator used to convert area, hydraulic radius,
    roughness, and slope into discharge or unit-area velocity values.'
uses:
  channel_data_module: 'The `channel_data_module` supplies the channel-geometry inputs that
    control every calculation here: side slope, bankfull depth, top width, slope, roughness,
    and length. Without `ch_hyd(k)`, the routine cannot build the cross section or compute
    routing coefficients.'
  channel_module: The `channel_module` matters because it is the host module for the channel-related
    state this routine is part of. Even though no candidate outside refs were resolved to
    it, `ch_ttcoef` is compiled in the channel-routing workflow alongside the channel state
    it helps initialize.
  channel_velocity_module: The `channel_velocity_module` matters because `ch_ttcoef` writes
    all of its outputs into `ch_vel(k)`. Those stored bankfull and low-flow values are the
    routing coefficients that later channel-flow calculations reuse.
---

<!-- facts:header -->

Computes main-channel travel-time and routing coefficients from channel geometry, slope, Manning roughness, and bankfull/low-flow depths.

## Bottom Line

ch_ttcoef calculates channel cross-section properties and Manning-based flow metrics for a single channel index `k`. It derives bottom width, area, wetted perimeter, hydraulic radius, velocity, celerity, and storage-time coefficients from `ch_hyd(k)` geometry and writes the results into `ch_vel(k)`.

The routine is used during channel initialization so later routing can use precomputed bankfull and low-flow travel-time parameters rather than recomputing them repeatedly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel initialization in `proc_cha`, inside the loop over `sp_ob%chan` and before `ch_initial` is called. `proc_cha` prepares the channel object count and then `ch_ttcoef` fills the per-reach routing coefficients that downstream channel routing and storage-time behavior depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize working scalars | Sets `aa` to 1. and clears `b` and `d` so the later geometry and Manning calculations start from known values. |
| 2. choose side slope | Uses `ch_hyd(k)%side` when it is provided; otherwise defaults `chsslope` to 2. as the main-channel side slope. |
| 3. compute bankfull bottom width | Sets the working depth to the bankfull depth and computes the bottom width as top width minus the two side-slope wedges. |
| 4. repair invalid width | If the computed bottom width is nonpositive, resets it to half the top width, zeros the side slope temporarily, and recomputes `chsslope` from the adjusted width and depth. |
| 5. store bankfull geometry inputs | Writes the bankfull bottom width and bankfull depth into `ch_vel(k)` for later routing use. |
| 6. compute bankfull cross-section properties | Builds wetted perimeter, area, and hydraulic radius for the bankfull cross section using trapezoid geometry. |
| 7. compute bankfull velocity and travel time | Uses `qman` to compute bankfull discharge and unit-area velocity, converts velocity to celerity, and derives storage distance and travel-time coefficient. |
| 8. compute 1.2-bankfull case | Raises depth to 1.2 times bankfull, adds floodplain area and perimeter terms, then recomputes hydraulic radius, discharge, and travel time for the higher-flow case. |
| 9. compute 0.1-bankfull case | Resets the working geometry to 0.1 times bankfull depth, recomputes area and hydraulic radius, derives low-flow discharge and velocity, then stores low-flow velocity, celerity, and storage distance in `ch_vel(k)`. |
| 10. return | Exits after all geometry-derived routing coefficients have been calculated and stored. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_data_module] | `ch_hyd` | `ch_hyd(k)%side, ch_hyd(k)%d, ch_hyd(k)%w, ch_hyd(k)%s, ch_hyd(k)%l` |
| [sym:channel_module] | `ch_hyd, ch_vel` | `ch_hyd(k)%side, ch_hyd(k)%d, ch_hyd(k)%w, ch_hyd(k)%s, ch_hyd(k)%l, ch_vel(k)%wid_btm, ch_vel(k)%dep_bf, ch_vel(k)%area, ch_vel(k)%vel_bf, ch_vel(k)%velav_bf, ch_vel(k)%celerity_bf, ch_vel(k)%st_dis, ch_vel(k)%vel_1bf, ch_vel(k)%celerity_1bf, ch_vel(k)%stor_dis_1bf` |
| [sym:channel_velocity_module] | `ch_vel` | `ch_vel(k)%wid_btm, ch_vel(k)%dep_bf, ch_vel(k)%area, ch_vel(k)%vel_bf, ch_vel(k)%velav_bf, ch_vel(k)%celerity_bf, ch_vel(k)%st_dis, ch_vel(k)%vel_1bf, ch_vel(k)%celerity_1bf, ch_vel(k)%stor_dis_1bf` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch_vel(k)%wid_btm` | When the routine computes bankfull geometry after the bottom-width check. | `ch_vel(k)%wid_btm` receives the derived bankfull bottom width so later channel routing can use a stored cross-section shape instead of recomputing it. |
| `ch_vel(k)%dep_bf` | Immediately after bankfull geometry is established. | `ch_vel(k)%dep_bf` records the bankfull flow depth used as the reference depth for channel routing coefficients. |
| `ch_vel(k)%area` | After bankfull area is computed from width, depth, and side slope. | `ch_vel(k)%area` stores the bankfull cross-sectional area, which later routing calculations use to derive discharge and travel-time terms. |
| `ch_vel(k)%vel_bf` | After the bankfull discharge is computed with `Qman(a, rh, ch_hyd(k)%n, ch_hyd(k)%s)`. | `ch_vel(k)%vel_bf` stores the bankfull Manning discharge used in the bankfull travel-time coefficient. |
| `ch_vel(k)%velav_bf` | After the unit-area Manning call at bankfull depth. | `ch_vel(k)%velav_bf` stores the average bankfull velocity term that is later converted to wave celerity. |
| `ch_vel(k)%celerity_bf` | Immediately after `velav_bf` is computed. | `ch_vel(k)%celerity_bf` stores the bankfull wave celerity, which controls routing/storage response at bankfull flow. |
| `ch_vel(k)%st_dis` | Immediately after bankfull celerity is computed. | `ch_vel(k)%st_dis` stores the bankfull storage-distance time constant derived from reach length and celerity. |
| `ch_vel(k)%vel_1bf` | After the 0.1-bankfull low-flow cross section is recomputed and passed to `Qman(aa, ...)`. | `ch_vel(k)%vel_1bf` stores the low-flow unit-area Manning velocity used to characterize shallow-flow routing. |
| `ch_vel(k)%celerity_1bf` | Immediately after `vel_1bf` is computed. | `ch_vel(k)%celerity_1bf` stores the low-flow wave celerity used for the 0.1-bankfull routing case. |
| `ch_vel(k)%stor_dis_1bf` | Immediately after low-flow celerity is computed. | `ch_vel(k)%stor_dis_1bf` stores the low-flow storage-distance coefficient for use in later routing behavior. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:1.1.1 | Channel bottom width | $W_{btm}=W_{bnkfull}-2*z_{ch}*depth_{bnkfull}$ | b = ch_hyd(k)%w - 2.*d*chsslope matches W_btm = W_bnkfull - 2*z_ch*depth_bnkfull. |
| 7:1.1.2 | Channel side slope from bankfull geometry | $z_{ch}=\frac{(W_{bnkfull}-W_{btm})}{2*depth_{bnkfull}}$ | b = w - 2*d*chsslope is the rearranged bankfull geometry relation; solving gives z_ch = (W_bnkfull - W_btm)/(2*depth_bnkfull). |
| 7:1.1.3 | Channel top width at flow depth | $W=W_{btm}+2*z_{ch}*depth$ | W = W_btm + 2*z_ch*depth derived from b=ch_hyd%w - 2*d*chsslope (line 87); ch_hyd%w is the bankfull top width and b is the bottom width, so W=b+2*z*d is implicit. ch_vel%wid_btm=b stored at line 98. |
| 7:1.1.4 | Channel cross-sectional area | $A_{ch}=(W_{btm}+z_{ch}*depth)*depth$ | a = b*d + chsslope*d*d is the trapezoid area formula A_ch = (W_btm + z_ch*depth)*depth. |
| 7:1.1.5 | Wetted perimeter | $P_{ch}=W_{btm}+2*depth*\sqrt{1+z_{ch}^2}$ | Verified against SWAT+ 62.0.0 (ch_ttcoef.f90:106). (wetted perimeter b+2d*sqrt(z^2+1)) |
| 7:1.1.6 | Hydraulic radius | $R_{ch}=\frac{A_{ch}}{P_{ch}}$ | rh = a / p directly matches R_ch = A_ch / P_ch. |
| 7:1.2.1 | Channel discharge by Manning equation | $q_{ch}=\frac{A_{ch}*R_{ch}^{2/3}*slp_{ch}^{1/2}}{n}$ | Qman(a, rh, n, s) computes discharge from cross-sectional area, hydraulic radius, Manning n, and slope. |
| 7:1.2.2 | Channel velocity by Manning equation | $v_c=\frac{R_{ch}^{2/3}*slp_{ch}^{1/2}}{n}$ | Qman(1., rh, n, s) stores the unit-area Manning velocity term used as v_c. |
| 7:1.4.11 | Wave celerity as derivative of discharge with respect to area | $c_k=\frac{d}{dA_{ch}}(q_{ch})$ | Verified against SWAT+ 62.0.0 (ch_ttcoef.f90:112). c_k=dq/dA realized as the 5/3 kinematic ratio |
| 7:1.4.12 | Wave celerity from mean velocity | $c_k=\frac{5}{3}*(\frac{R_{ch}^{2/3}*slp_{ch}^{1/2}}{n})=\frac{5}{3}*v_c$ | Verified against SWAT+ 62.0.0 (ch_ttcoef.f90:112). celerity = velav*5./3.` — c_k=5/3·v_c |

## Lineage

The procedure was added in df07e3f as a new channel travel-time coefficient initializer with documented geometry and Manning-based calculations. c7c8e22 later carried the same logic forward as updated source import, and 39fabde only initialized local working scalars to 0. and added explicit initial values. bd18ad4 changed the `qman` declaration to `real, external` and made minor whitespace/end-of-file adjustments without altering the computation.

- df07e3f introduced the subroutine and its full geometry-to-routing calculation sequence, including the bankfull and low-flow coefficient computations.
- 39fabde initialized the local working variables (`fps`, `d`, `b`, `p`, `a`, `qq1`, `rh`, `tt1`, `tt2`, `aa`, `chsslope`) to zero, reducing dependence on implicit initial state.
- bd18ad4 declared `qman` as an external procedure and made nonbehavioral formatting changes.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_ttcoef' has no extracted documentation comment.
