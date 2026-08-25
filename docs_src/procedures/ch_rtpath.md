---
kind: procedure
symbol: ch_rtpath
title: ch_rtpath
status: filled
source_hash: 1d5f034cf1ada3a0
version_label: SWAT+ 62.0.0
locals:
  theta: External temperature-response function used to convert each pathogen's 20°C die-off
    rate and temperature adjustment factor into a rate at the current water temperature.
  path_tot: Temporary accumulator for total pathogen mass in the reach before and after die-off.
    It starts at zero, is built from inflow mass plus stored in-reach mass, is decayed, clipped
    at zero, and then divided by water volume to form the new concentration.
  netwtr: Temporary total water volume in the reach for the current routing step. It combines
    inflow water and stored reach water, and it is used as the denominator when computing
    the updated concentration.
  tday: Routing duration in days for the current reach pass. It is computed from reach travel
    time in hours and capped at 1.0 so the die-off exponent does not use a longer-than-day
    interval.
  wtmp: Estimated channel water temperature used for pathogen die-off. It is derived from
    the station weather average temperature and forced to a small positive value if the estimate
    would be nonpositive.
  rchwtr: Stored reach water volume carried into the concentration calculation. It represents
    the preexisting channel water that receives routed pathogen mass and helps determine the
    final dilution volume.
  iwst: Index of the weather station whose mean air temperature is used to estimate channel
    water temperature.
  ipath: Loop counter over the simulated pathogen definitions in the constituent database.
  jrch: Current reach index used to read and write channel state for this routing step.
  iob: Index of the object-hydrograph entry supplying the incoming pathogen concentration
    for the current routing path.
  icmd: Index of the channel command/object whose inflow hydrograph provides the water volume
    used in the routing calculation.
uses:
  basin_module: The routine imports basin_module even though no resolved symbol from it appears
    in the extracted lines; it is part of the shared model state scope that makes basin-level
    settings available to channel routing code.
  time_module: The routine imports time_module even though no resolved symbol from it appears
    in the extracted lines; it is part of the shared simulation-time context that governs
    when channel routing executes.
  pathogen_data_module: pathogen_data_module supplies path_db(ipath)%do_stream and path_db(ipath)%t_adj,
    which define the pathogen-specific die-off rate and temperature adjustment used inside
    Theta. Without these pathogen parameters, the routine could not compute the per-pathogen
    decay factor.
  channel_module: channel_module provides the reach-state variables rtwtr, rchdep, rttime,
    and ch(jrch)%bactp. Those values determine whether routing runs, how long decay acts,
    how much water is available, and how much pathogen mass is already stored in the channel.
  hydrograph_module: hydrograph_module supplies ob(icmd)%hin%flo, the inflow water volume
    used to compute total pathogen mass carried into the reach. That inflow volume is part
    of the mass balance before dilution and die-off.
  climate_module: climate_module supplies wst(iwst)%weat%tave, which is used to estimate water
    temperature for temperature-dependent pathogen decay. The decay rate changes with that
    temperature estimate.
  constituent_mass_module: constituent_mass_module provides cs_db%num_paths, obcs(iob)%hd(1)%path(ipath),
    and ch_water(jrch)%path(ipath). These define how many pathogen paths are routed, the incoming
    pathogen concentration for each path, and the destination concentration array that this
    routine updates.
---

<!-- facts:header -->

Routes pathogen mass through a channel reach and converts it to a new water-column concentration. It applies temperature-adjusted die-off before storing the updated pathogen concentration for each path.

## Bottom Line

ch_rtpath routes pathogen mass through a channel reach for each simulated pathogen path. It combines inflow-borne mass with mass already stored in the reach, applies a temperature-adjusted first-order die-off over the reach travel time, and then stores the resulting channel-water concentration in ch_water(jrch)%path(ipath).

The routine only does work when there is water leaving the reach and the reach still has positive depth. If those conditions are met, it uses the current weather-station air temperature, pathogen database die-off settings, reach travel time, inflow hydrograph volume, and stored reach water to update the per-pathogen channel concentration for the current routing step.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from sd_channel_control3 after pathogen routing has been enabled by a positive cs_db%num_paths count. sd_channel_control3 sets up the channel-object and hydrograph state that ch_rtpath reads, and later channel-concentration behavior depends on the updated ch_water(jrch)%path(ipath) values produced here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check active routing | The routine only proceeds when both outflow water and channel depth are positive, which prevents pathogen routing from running for dry or inactive reaches. |
| 2. estimate water temperature | It estimates reach water temperature from the weather station daily average air temperature and forces a minimum value of 0.1 if the estimate is nonpositive. |
| 3. loop over pathogen definitions | It iterates through every simulated pathogen so each pathogen path is routed separately. |
| 4. assemble total pathogen mass | For the current pathogen, it adds inflow mass from obcs(iob)%hd(1)%path(ipath) scaled by inflow volume to the mass already stored in the reach, ch(jrch)%bactp, scaled by the stored reach water volume. |
| 5. compute and bound travel time fraction | It converts reach travel time from hours to days and caps the fraction at 1.0 so the decay period does not exceed one day. |
| 6. apply temperature-adjusted die-off | It reduces pathogen mass with an exponential decay term based on the pathogen-specific stream die-off rate, its temperature adjustment factor, and the current water temperature, then clamps the mass at zero or above. |
| 7. compute total water volume | It forms the routing volume by adding inflow water to the water already stored in the reach. |
| 8. remove tiny residual mass | It zeroes very small remaining pathogen mass values so numerical underflow noise is not carried into the concentration update. |
| 9. write routed concentration | If total water volume is at least 1, it writes the routed concentration as mass divided by volume; otherwise it stores zero for that pathogen path. |
| 10. finish the subroutine | The routine returns after updating all pathogen paths for the current reach. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state` | `No candidate outside references were resolved to this module.` |
| [sym:time_module] | `time_module state` | `No candidate outside references were resolved to this module.` |
| [sym:pathogen_data_module] | `path_db` | `path_db(ipath)%t_adj` |
| [sym:channel_module] | `ch, rtwtr, rchdep, rttime` | `ch(jrch)%bactp` |
| [sym:hydrograph_module] | `ob` | `ob(icmd)%hin%flo` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%tave` |
| [sym:constituent_mass_module] | `cs_db, obcs, ch_water` | `cs_db%num_paths, obcs(iob)%hd(1)%path(ipath), ch_water(jrch)%path(ipath)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch_water(jrch)%path(ipath)` | When rtwtr > 0. and rchdep > 0., and for each ipath from 1 to cs_db%num_paths, ch_water(jrch)%path(ipath) is assigned from the routed pathogen mass; otherwise it is not updated by this routine. | This state holds the routed pathogen concentration in channel water for the current reach and pathogen path. The routine updates it to reflect inflow, in-reach storage, decay, and dilution at the end of the routing step. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:5.1.1 | Less-persistent bacteria decay in channel | $bact_{lprch,i}=bact_{lprch,i-1}*exp(-\mu_{lprch,die})$ | Verified against SWAT+ 62.0.0 (ch_rtpath.f90:90). path_tot = path_tot*Exp(-Theta(do_stream,t_adj,wtmp)*tday)` — in-stream bacteria decay (lp) |
| 7:5.1.2 | Persistent bacteria decay in channel | $bact_{prch,i}=bact_{prch,i-1}*exp(-\mu_{prch,die})$ | Verified against SWAT+ 62.0.0 (ch_rtpath.f90:90). same (p pool; lp/p consolidated to one path) |
| 7:5.1.3 | Temperature-adjusted die-off rate for less-persistent bacteria | $\mu_{lprch,die}=\mu_{lprch,die,20}*\theta_{bact}^{(T_{water}-20)}$ | Verified against SWAT+ 62.0.0 (ch_rtpath.f90:90). Theta(...)` = μ_die,20·θ^(T−20) temp correction (lp) |
| 7:5.1.4 | Temperature-adjusted die-off rate for persistent bacteria | $\mu_{prch,die}=\mu_{prch,die,20}*\theta_{bact}^{(T_{water}-20)}$ | Verified against SWAT+ 62.0.0 (ch_rtpath.f90:90). same Theta temp correction (p) |
| 7:5.2.1 | Sediment erosion contribution to bacteria routing | $sed_{deg}=(conc_{sed,ch,mx}-conc_{sed,ch,i})*V_{ch}*K_{ch}*C_{ch}$ | This routine only applies water-column pathogen die-off and concentration updates; it does not compute sediment erosion/degradation terms for bacteria. |
| 7:5.2.2 | Bacteria entrained by channel sediment erosion | $bact_{deg}=sed_{deg} *conc_{bact,sed}$ | No sediment-associated bacteria mass term is formed in ch_rtpath; only total pathogen mass in water is updated. |
| 7:5.2.3 | Seasonal bacteria concentration on sediment | $log(conc_{bact,sed})=bsc_1*sin(bsc_2*\frac{day-bsc_3}{366}*\pi)+bsc_4$ | The sinusoidal sediment-bacteria concentration function from the theory page is not present in the channel pathogen routing routine. |
| 7:5.2.4 | Channel sediment deposition term for bacteria routing | $sed_{dep}=(conc_{sed,ch,i}-conc_{sed,ch,mx})*V_{ch}$ | No sediment deposition calculation is applied to pathogen mass in this routine. |
| 7:5.2.5 | Bacteria deposited with settling sediment | $bact_{dep}=bact_{ch,i}*\frac{K_p*sed_{dep}}{V_{ch}+K_p*(conc_{sed,ch,i}*V_{ch})}$ | The routine does not partition bacteria to deposited sediment using a Kp-style expression. |
| 7:5.2.6 | Sediment partition coefficient for bacteria | $K_p=10^{-1.6}*clay^{1.98}$ | No clay-based bacteria partition coefficient is evaluated in the stream pathogen routine. |
| 7:5.2.7 | Bacteria mass balance with erosion and deposition | $bact_{ch}=bact_{ch,i}+bact_{deg}-bact_{dep}$ | The code updates pathogen mass only through inflow, die-off, and dilution; it does not add separate bact_deg or bact_dep channel terms. |
| 7:5.2.8 | Bacteria concentration in channel water | $conc_{bact,ch}=\frac{bact_{ch}}{V_{ch}}*10^{-4}$ | ch_water(jrch)%path(ipath) = path_tot / netwtr stores water-column concentration, but the 10^-4 reporting conversion from the theory page is not explicit in this routine. |

## Lineage

Resolved lineage shows the routine was introduced in df07e3f as the channel bacteria routing subroutine. Later, 39fabde initialized the local working variables with zero values, f1e61a3 only fixed whitespace around the tiny-mass guard line, and bd18ad4 added blank lines without changing behavior.

- df07e3f added the full ch_rtpath subroutine that routes pathogen mass through the channel network and writes channel-water concentrations.
- 39fabde changed the local working variables to explicit zero-initialized declarations, which affects starting values for the mass and volume calculations but not the routing algorithm itself.
- f1e61a3 made a formatting-only change around the path_tot underflow guard; the executable logic stayed the same.
- bd18ad4 added blank lines near the declaration block; no behavioral change was introduced.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_rtpath' has no extracted documentation comment.
