---
kind: procedure
symbol: ch_rtday
title: ch_rtday
status: filled
source_hash: a6d0bb7868b240de
version_label: SWAT+ 62.0.0
locals:
  qman: External Manning-equation function used to turn cross-sectional area, hydraulic radius,
    roughness, and slope into discharge. This routine calls it to test whether the current
    channel geometry can carry the inflow at bankfull depth and to iterate depth until the
    computed flow matches the target flow.
  scoef: Variable-storage routing coefficient computed from the day length and travel time.
    It controls how much of the inflow plus prior storage is released as outflow when the
    reach is not storage-limited.
  p: Wetted perimeter of the active flow cross section. It is used to compute hydraulic radius
    and also appears in the transmission-loss calculation as part of the channel seepage loss
    term.
  topw: Top width of flow at the current water level. It is used when estimating evaporation
    loss from the wetted surface of the channel.
  vol: Starting water volume in the reach for this day, initialized from `wtrin`. It is used
    as the volume available for routing and for computing how much storage remains after outflow.
  c: Inverse side-slope parameter for the channel cross section, taken from `ch_hyd(jhyd)%side`.
    It is used to compute perimeter, area, and top width for the main channel geometry.
  rh: Hydraulic radius of the current flow cross section. It is used as the Manning input
    to `qman` while testing channel capacity and iterating depth.
  volrt: Average daily flow rate expressed from the incoming water volume and routing time-step
    length. It is the main target flow used to decide whether bankfull capacity is exceeded
    and to drive the depth iteration.
  maxrt: Bankfull flow capacity of the channel computed with `qman` at bankfull geometry.
    It is the threshold used to decide whether floodplain routing and wetland spillover are
    needed.
  addp: Perimeter of the expanded floodplain cross section during the overbank depth iteration.
    It is recomputed each step to get the hydraulic radius for the larger flooded section.
  addarea: Cross-sectional area of the expanded floodplain section during the overbank iteration.
    It grows in 1 cm depth increments until `qman` reaches the target flow.
  vc: Mean channel flow velocity for the current day. It is derived from discharge divided
    by area and stored in `ch(jrch)%vel_chan` for later use.
  aaa: Evaporation-depth factor derived from basin evaporation adjustment, potential ET, and
    the routing time step. It is used to convert evaporative demand into a water-depth loss
    over the channel surface.
  rttlc1: Portion of transmission-loss volume taken from remaining channel storage first.
    It prevents storage from going negative when seepage losses exceed available storage.
  rttlc2: Remainder of transmission-loss volume taken from the routed outflow after storage
    has been exhausted. It is used when seepage losses are larger than channel storage.
  rtevp1: Portion of evaporation loss taken from routed outflow first after storage contribution
    is accounted for. It is used to keep the final outflow nonnegative while applying evaporation.
  rtevp2: Portion of evaporation loss assigned to reach storage. It is the storage share of
    total evaporation before any remainder is removed from routed outflow.
  det: Simulation time step in hours, set from the daily routing fraction. It scales storage
    routing, transmission loss, and evaporation calculations over the day.
  adddep: Incremental floodplain depth above bankfull used during the overbank iteration.
    It advances in 0.01 m steps until the computed discharge can carry `volrt`.
  itermx: Iteration counter that limits the floodplain-depth search. It stops the 1 cm loop
    if it runs too long.
  ihr: Loop index over HRUs or spatial objects linked to the reach. It is used to find landscape
    units connected to the current channel so floodwater can be passed to wetlands.
  ires: Index of the wetland or reservoir storage unit associated with a connected HRU. It
    selects the wetland storage volumes that receive floodwater and are used in loss calculations.
  ichan: Channel link identifier for an HRU’s flood connection. It is compared with the current
    reach number to determine whether floodwater should be routed to that landscape unit.
  iobhr: Object number for the current HRU’s connectivity record. It is used to reach `ob(iobhr)%flood_ch_lnk`
    and identify the linked channel.
  depst: Available wetland storage depth or floodwater capacity for a connected storage unit
    on this day. It is the amount of flood volume that can actually be accepted from the excess
    channel water.
  depstmax: Maximum wetland storage volume at spillway capacity for the connected storage
    unit. It is read from `wet_ob(ires)%pvol` and used as the cap when computing available
    flood storage.
  rchvol: Channel volume implied by bankfull geometry and channel length. It is used when
    the computed storage coefficient would exceed 1, letting the routine cap outflow to the
    available channel volume.
uses:
  basin_module: The basin parameter `bsn_prm%evrch` scales how strongly potential ET is applied
    to channel water. Without this basin-wide adjustment, the evaporation volume removed from
    the reach would not match model configuration.
  channel_data_module: The channel hydraulic data `ch_hyd(jhyd)%side`, `%d`, `%n`, `%s`, `%w`,
    `%l`, and `%k` define the reach cross-section, roughness, slope, length, and hydraulic
    conductivity used to compute capacity, routing time, seepage loss, and evaporation geometry.
  channel_module: The channel state in `ch` and the routing controls in `wtrin`, `rt_delt`,
    `jhyd`, `sdti`, `rchdep`, `rcharea`, `rttime`, `rtwtr`, `rttlc`, `rtevp`, and `pet_ch`
    are the core inputs and outputs of the daily channel-water balance. They determine whether
    the reach overflows, how much storage remains, and what gets passed downstream.
  hydrograph_module: The hydrograph connectivity and wetland output arrays determine which
    HRUs are linked to the current reach for flood spillover and where the transferred water
    is recorded. They matter because excess channel flow can be diverted into wetland storage
    rather than staying in the channel.
  hru_module: HRU connectivity provides the mapping from each spatial object to its flood-linked
    channel and to the associated surface-storage database index. That mapping is how the
    routine finds which wetland storage to fill when the reach is above bankfull.
  channel_velocity_module: The bankfull velocity parameters in `ch_vel` provide the channel
    cross-sectional area and bottom width needed to compute hydraulic radius, mean velocity,
    and routing travel time.
  maximum_data_module: 'Imported at `ch_rtday.f90:60` but not used: the module exposes a single
    module-level variable and this routine references none of it. Note that `maximum_data_module`
    declares a `ch_hyd` component inside the derived type `data_files_max_elements`, which
    is a different symbol from the `ch_hyd` array this routine uses — that one is declared
    in `channel_data_module.f90:84` and is already attributed to `channel_data_module` above.'
  reservoir_module: The wetland/reservoir volume `wet_ob(ires)%pvol` sets the maximum floodwater
    capacity available to a connected storage unit. It is used to determine how much excess
    channel water can be accepted before the spillover is limited.
  reservoir_data_module: 'Imported at `ch_rtday.f90:62` but not used: none of the module''s
    20 module-level variables is referenced anywhere in this routine''s body. The reservoir
    state the routine does touch (`wet_ob`) comes from `reservoir_module`.'
---

<!-- facts:header -->

Routes daily flow through a channel reach with variable-storage routing, then subtracts transmission losses and evaporation. It also spills excess water to connected wetlands when the reach exceeds bankfull capacity.

## Bottom Line

ch_rtday computes one day of reach routing for the current reach using Manning-based geometry, a variable-storage routing coefficient, and reach storage carryover. It first checks whether the daily inflow exceeds bankfull capacity; if so, it computes floodplain overflow and transfers part of that water to linked wetland storage before continuing the routing calculation.

After routing the main channel flow, it updates reach storage, transmission losses, evaporation, velocity, travel time, and the final outflow volume. Those results feed later channel state, sediment/water routing, and connected landscape or wetland water balances.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the daily channel-routing stage after upstream code has already set the current reach index, inflow volume `wtrin`, routing fraction `rt_delt`, geometry pointers, and connectivity state. Its outputs then drive the rest of the channel water balance for the day, including reach storage, outflow, seepage, evaporation, and any wetland flood transfer.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize daily volume and target average flow. | The routine copies the incoming water volume into `vol` and converts it to an average daily flow rate `volrt` using the daily routing fraction. |
| 2. Compute bankfull hydraulic capacity. | Using channel side slope, bankfull width/depth, area, roughness, and slope, it derives the bankfull wetted perimeter, hydraulic radius, and maximum bankfull discharge `maxrt` with `qman`. |
| 3. Reset day-state accumulators. | It clears depth, perimeter, velocity, and flood-volume state so the day starts from a neutral channel state. |
| 4. Divert overflow to linked wetlands when inflow exceeds bankfull. | If average flow exceeds bankfull capacity, it computes excess flood volume, loops over HRUs, finds those linked to the current channel, and transfers as much floodwater as possible into the connected wetland storage arrays. |
| 5. Iterate channel depth above bankfull when still over capacity. | If the flow still exceeds bankfull after spillover, the routine holds bankfull geometry fixed and increases overbank depth in 0.01 m increments until `qman` reaches the target flow, then stores the resulting floodplain area and depth. |
| 6. Otherwise iterate in-bank depth to match the daily flow. | For sub-bankfull flow, it increments depth in 0.01 m steps, recomputes area, perimeter, radius, and discharge, and stops when the simulated discharge reaches the target daily flow. |
| 7. Derive flow top width and routing time step. | It computes the current top width from either the main-channel or floodplain geometry and sets the effective routing time step in hours. |
| 8. Compute velocity, travel time, and routed outflow. | When discharge is positive, it computes mean velocity and travel time, builds the storage coefficient, then calculates outflow either from stored channel volume limits or from the variable-storage routing formula before updating reach storage. |
| 9. Remove transmission losses from storage and outflow. | It computes seepage loss from conductivity, length, and wetted perimeter, subtracts that loss first from channel storage and then from routed outflow, and preserves the remaining transmission-loss total in `rttlc`. |
| 10. Remove evaporation losses from storage and outflow. | It scales potential ET by basin evaporation adjustment, converts it to a channel evaporation volume using the current wetted geometry, splits the loss between storage and outflow, and updates `rtevp` accordingly. |
| 11. Zero out state when no flow is available and clamp negatives. | If no positive discharge remains, it clears outflow, storage, velocity, and previous flow variables; then it clamps negative outflow and storage to zero before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%evrch` |
| [sym:channel_data_module] | `ch_hyd` | `ch_hyd(jhyd)%side, ch_hyd(jhyd)%d, ch_hyd(jhyd)%n, ch_hyd(jhyd)%s, ch_hyd(jhyd)%w, ch_hyd(jhyd)%l, ch_hyd(jhyd)%k` |
| [sym:channel_module] | `ch, wtrin, rt_delt, jhyd, sdti, rchdep, rcharea, rttime, rtwtr, rttlc, rtevp, pet_ch` | `ch(jrch)%chfloodvol, ch(jrch)%vel_chan, ch(jrch)%rchstor, ch(jrch)%flwin, ch(jrch)%flwout` |
| [sym:hydrograph_module] | `sp_ob, ob, wet, wet_in_d, jrch` | `sp_ob%hru, ob(iobhr)%flood_ch_lnk, wet(ires)%flo, wet_in_d(ires)%flo` |
| [sym:hru_module] | `hru` | `hru(ihr)%obj_no, hru(ihr)%dbs%surf_stor` |
| [sym:channel_velocity_module] | `ch_vel` | `ch_vel(jrch)%wid_btm, ch_vel(jrch)%area` |
| [sym:maximum_data_module] | `no direct reference in this procedure` |  |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(ires)%pvol` |
| [sym:reservoir_data_module] | `no direct reference in this procedure` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sdti` | When `volrt > maxrt` is true. | `sdti` is first set to `maxrt` and then raised through the depth-iteration branch until it matches the overflow-adjusted daily flow; it represents the simulated discharge rate used to size the reach cross section. |
| `rchdep` | When the routine enters the depth-iteration paths and again after the outflow calculation. | `rchdep` is set to bankfull depth for the overflow case or incremented from zero for the in-bank case, then finalized as the daily flow depth in the reach. |
| `ch(jrch)%chfloodvol` | When `volrt > maxrt` at the start of the floodplain branch. | The channel flood-volume accumulator stores the amount of water above bankfull that must be handled by floodplain routing or wetland transfer. |
| `wet(ires)%flo` | When a linked wetland has available spill capacity and `depst > 0.`. | `wet(ires)%flo` is increased by the accepted flood volume to record that the wetland received floodwater from the channel. |
| `wet_in_d(ires)%flo` | When floodwater is transferred to a wetland and the daily wetland inflow record is updated. | `wet_in_d(ires)%flo` records the same flood transfer in depth-equivalent units so daily wetland inflow bookkeeping stays consistent. |
| `rcharea` | When the routine computes flow area from the daily discharge, both in the overbank and in-bank branches. | `rcharea` is updated to the cross-sectional area needed to carry the target flow for the current geometry, and later it is used to compute velocity. |
| `ch(jrch)%vel_chan` | When `sdti > 0.` and the routine computes velocity. | `ch(jrch)%vel_chan` stores the average channel velocity for the day, which is needed for routing diagnostics and later reach-state logic. |
| `rttime` | When `sdti > 0.` and velocity is known. | `rttime` is updated to the travel time through the reach in hours; it drives the storage coefficient used for variable-storage routing. |
| `rtwtr` | When `sdti > 0.` and the routine computes routed outflow. | `rtwtr` becomes the day’s water leaving the reach before the final clamping step, reduced later by transmission and evaporation losses. |
| `ch(jrch)%rchstor` | When `sdti > 0.` and the routine updates storage after routing. | `ch(jrch)%rchstor` is increased by inflow volume and reduced by routed outflow and losses; it holds the remaining water stored in the reach at day end. |
| `rttlc` | When `rtwtr > 0.` and seepage losses are computed. | `rttlc` stores the total transmission-loss volume removed from the channel during the day. |
| `rtevp` | When `rtwtr > 0.` and evaporation is computed. | `rtevp` stores the total evaporation volume removed from the channel during the day, split between storage and outgoing flow. |
| `ch(jrch)%flwin` | When the routine completes routing and reaches the final cleanup path. | `ch(jrch)%flwin` is cleared to zero in the no-flow case so the reach does not carry stale inflow state into the next day. |
| `ch(jrch)%flwout` | When the routine completes routing and reaches the final cleanup path. | `ch(jrch)%flwout` is cleared to zero in the no-flow case so the previous day’s outflow is not reused after routing ends with no water. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.5.1 | Transmission-loss adjusted final runoff volume | $vol_{Qsurf,f}=\begin {cases} 0 & vol{Qsurf,i} \le vol_{thr} \\ a_x+b_x*vol_{Qsurf,i} & vol_{Qsurf,i} > vol_{thr} \end{cases}$ | Current channel transmission losses use a seepage-loss volume rttlc = det*k*l*p rather than the piecewise ax + bx*vol runoff-transmission formula on the theory page. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 2:1.5.2 | Transmission-loss threshold volume | $vol_{thr}=-\frac{a_x}{b_x}$ | No direct vol_thr = -ax/bx threshold formula is coded in this checkout. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 2:1.5.5 | Transmission-loss kr parameter | $k_r=-2.22*ln[1-2.6466*\frac{K_{ch}*dur_{flw}}{vol_{Qsurf,i}}]$ | No kr logarithmic coefficient is computed in the active code path. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 2:1.5.6 | Transmission-loss ar parameter | $a_r=-0.2258*K_{ch}*dur_{flw}$ | No ar coefficient is computed in the active code path. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 2:1.5.7 | Transmission-loss br parameter | $b_r=exp[-0.4905*k_r]$ | No br coefficient is computed in the active code path. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 2:1.5.8 | Transmission-loss bx parameter | $b_x=exp[-k_r*L*W]$ | No bx exponential attenuation coefficient is computed in the active code path. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 2:1.5.9 | Transmission-loss ax parameter | $a_x=\frac{a_r}{(1-b_r)}*(1-b_x)$ | No ax coefficient is computed in the active code path. NOTE (v62 verify): mapped routine ch_rtday is uncalled legacy code (no 'call ch_rtday' in the source); the live channel-abstraction path is channel seepage in sd_channel_control3.f90, still a seepage-volume form, not the Lane ax+bx*vol regression. |
| 7:1.1.8 | Flooded depth above bankfull | $depth=depth_{bnkfull}+depth_{fld}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:163). |
| 7:1.2.3 | Channel area from volume and length | $A_{ch}=\frac{V_{ch}}{1000*L_{ch}}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:197). (A_ch = V/(1000*L)) |
| 7:1.2.4 | Depth from channel area below bankfull | $depth=\sqrt{\frac{A_{ch}}{z_{ch}}+(\frac{W_{btm}}{2*z_{ch}})^2}-\frac{W_{btm}}{2*z_{ch}}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:105). (depth from area) |
| 7:1.2.5 | Depth from area above bankfull | $depth=depth_{bnkfull}+\sqrt{\frac{(A_{ch}-A_{ch,bnkfull})}{z_{fld}}+(\frac{W_{btm,fld}}{2*z_{fld}})^2}-\frac{W_{btm,fld}}{2*z_{fld}}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90). (overbank depth) |
| 7:1.3.8 | Variable-storage routing coefficient | $SC=\frac{2*\Delta t}{2*TT+ \Delta t}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:202). scoef = 2.*det/(2.*rttime+det)` — SC exactly |
| 7:1.3.10 | Variable-storage outflow from inflow plus prior storage | $q_{out,2}=SC*(q_{in,ave}+\frac{V_{stored,1}}{\Delta t })$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:207). rate form of outflow |
| 7:1.3.11 | Variable-storage outflow volume | $V_{out,2}=SC*(V_{in}+V_{stored,1})$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:207). volume form of the same line |
| 7:1.3.1 |  | $V_{in}-V_{out}=\Delta V_{stored}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:210). rchstor = rchstor + vol - rtwtr` — continuity |
| 7:1.3.2 |  | $\Delta t*(\frac{q_{in,1}+q_{in,2}}{2})-\Delta t*(\frac{q_{out,1}+q_{out,2}}{2})=V_{stored,2}-V_{stored,1}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:210). discrete continuity over Δt |
| 7:1.3.3 |  | $q_{in,ave}+\frac{V_{stored,1}}{\Delta t}-\frac{q_{out,1}}{2}=\frac{V_{stored,2}}{\Delta t}+\frac{q_{out,2}}{2}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:202). rearranged continuity → SC derivation |
| 7:1.3.4 |  | $TT=\frac{V_{stored}}{q_{out}}=\frac{V_{stored,1}}{q_{out,1}}=\frac{V_{stored,2}}{q_{out,2}}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:199). rttime = l*1000./(3600.*vc)` — TT=V/q |
| 7:1.3.5 |  | $q_{in,ave}+\frac{V_{stored,1}}{(\frac{\Delta t}{TT})*(\frac{V_{stored,1}}{q_{out,1}})}-\frac{q_{out,1}}{2}=\frac{V_{stored,2}}{(\frac{\Delta t}{TT})*(\frac{V_{stored,2}}{q_{out,2}})}+\frac{q_{out,2}}{2}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:202). TT-substituted form |
| 7:1.3.6 |  | $q_{out,2}=(\frac{2*\Delta t}{2*TT+\Delta t})*q_{in,ave}+(1-\frac{2*\Delta t}{2*TT+ \Delta t})*q_{out,1}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:202). expanded SC form |
| 7:1.3.7 |  | $q_{out,2}=SC*q_{in,ave}+(1-SC)*q_{out,1}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:207). rtwtr = scoef*(wtrin+rchstor) |
| 7:1.3.9 |  | $(1-SC)*q_{out}=SC*\frac{V_{stored}}{\Delta t}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:202). algebraic identity of SC |
| 7:1.5.1 |  | $tloss=K_{ch}*TT*P_{ch}*L_{ch}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:226). rttlc = det*k*l*p` — K_ch·TT·P·L |
| 7:1.7.2 |  | $V_{bnk}=bnk*(1-exp[-\alpha_{bnk}])$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90). (bank storage 1-exp) |
| 7:1.8.1 |  | $V_{stored,2}=V_{stored,1}+V_{in}-V_{out}-tloss-E_{ch}+div+V_{bnk}$ | Verified against SWAT+ 62.0.0 (ch_rtday.f90:210). channel water balance |

## Lineage

The procedure was introduced in df07e3f as a new daily channel-routing subroutine with the full water-balance logic, documentation block, and core flow algorithm. In c7c8e22 the source was imported from Bitbucket without altering the algorithm shown in the diff. In 39fabde the local variable declarations were initialized to zero, and in f1e61a3 the patch only fixed indentation. In bd18ad4 the routine changed `qman` from a local real variable to an external function declaration.

- df07e3f added the routine and its full daily-routing behavior, including flood spillover, depth iteration, variable-storage routing, seepage, and evaporation.
- 39fabde only initialized local scalars and loop indices to zero; the routing algorithm itself did not change.
- f1e61a3 applied whitespace-only tab fixes and did not change behavior.
- bd18ad4 changed the `qman` declaration to `real, external :: qman`, making the Manning calculation an external function call rather than a local variable.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_rtday' has no extracted documentation comment.
- maximum_data_module and reservoir_data_module had no resolved candidate outside references in the provided evidence.
- algorithm_steps revised: expanded to 11 steps to reflect the actual control flow and state updates visible in the source.
- Modules imported without contributing state were verified rather than left unresolved: each module's own source was checked from its context packet, counting only module-level variables, and none of the modules marked "no direct reference in this procedure" is referenced in this routine's body.
