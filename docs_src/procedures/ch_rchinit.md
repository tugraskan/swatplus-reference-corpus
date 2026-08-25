---
kind: procedure
symbol: ch_rchinit
title: ch_rchinit
status: filled
source_hash: dfb7903ac223aa91
version_label: SWAT+ 62.0.0
locals:
  rchwtr: Local working copy of the current reach’s starting-day water storage. It is seeded
    from `ch(jrch)%rchstor` before the routine clears other daily variables.
  bury: Temporary daily pesticide loss from the active sediment layer due to burial; initialized
    to zero so the day’s burial loss can be accumulated later.
  difus: Temporary daily pesticide transfer from sediment to reach by diffusion; initialized
    to zero for later accumulation.
  reactb: Temporary daily pesticide loss from sediment by reactions, including the bank-storage/root-zone
    pathway noted in the source comments; initialized to zero.
  reactw: Temporary daily pesticide loss from water in the reach by reactions; initialized
    to zero.
  resuspst: Temporary daily pesticide mass moving from sediment back to the reach by resuspension;
    initialized to zero.
  setlpst: Temporary daily pesticide mass moving from water to sediment by settling; initialized
    to zero.
  volatpst: Temporary daily pesticide mass lost from the reach by volatilization; initialized
    to zero.
uses:
  channel_module: '`channel_module` provides the shared reach-state variables that this routine
    resets and seeds for the active reach, including `peakr`, `rcharea`, `rchdep`, `rtevp`,
    `rttime`, `rttlc`, `rtwtr`, `sdti`, `sedrch`, the channel object array `ch`, and the sediment-size
    mass pools. The routine reads `ch(jrch)%rchstor` to initialize `rchwtr` and clears `ch(jrch)%vel_chan`
    and the daily channel outputs so later routing code works from the correct per-reach state.'
  hydrograph_module: '`hydrograph_module` supplies `jrch`, the active reach index. That index
    selects which element of `channel_module::ch` is being initialized, so this routine can
    reset the correct reach before the routing loop advances.'
---

<!-- facts:header -->

Initializes per-reach daily channel-routing state before the routing calculations run. It copies the current reach storage into a working variable and clears daily flow, sediment, and pesticide accumulators for the active reach.

## Bottom Line

`ch_rchinit` is a reset-and-seed routine for the daily channel-routing command loop. It takes the current reach number from `hydrograph_module`, copies that reach’s stored water volume into `rchwtr`, and zeroes the day’s computed outputs and mass-balance accumulators so later routing code starts from a clean slate.

The routine matters because downstream channel-routing calculations update the shared `channel_module` state in place. By clearing variables such as `peakr`, `rcharea`, `rchdep`, `rtevp`, `rttime`, `rttlc`, `rtwtr`, `sdti`, `sedrch`, `ch(jrch)%vel_chan`, and the sediment-size and pesticide pools, it prevents carryover from the previous reach or previous day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at the start of the daily channel-routing command loop, before the reach’s routing calculations for the current day. The active reach index is prepared in `hydrograph_module`, and the downstream routing and channel-process code depend on these cleared and seeded shared variables to compute travel time, flow, sediment transport, and pesticide fate without inheriting stale values from the previous reach.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the active reach storage into the working water-storage variable. | Copies `ch(jrch)%rchstor` into `rchwtr` so the routine starts the day with the reach’s current stored water volume. |
| 2. Reset daily pesticide-loss variables. | Sets `bury`, `difus`, `reactb`, `reactw`, `resuspst`, `setlpst`, and `volatpst` to zero so pesticide fluxes for the day can be accumulated from a clean initial state. |
| 3. Reset daily hydrologic and sediment summary variables. | Clears `peakr`, `rcharea`, `rchdep`, `rtevp`, `rttime`, `rttlc`, `rtwtr`, `sdti`, `sedrch`, and the sediment-size pools `rch_san`, `rch_sil`, `rch_cla`, `rch_sag`, `rch_lag`, and `rch_gra` to zero. |
| 4. Clear the current channel velocity. | Sets `ch(jrch)%vel_chan` to zero so the current reach’s velocity will be recomputed by later routing calculations. |
| 5. End the initialization routine. | Returns to the caller after the shared daily channel-routing state has been initialized for the active reach. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_module] | `ch, peakr, rcharea, rchdep, rtevp, rttime, rttlc, rtwtr, sdti, sedrch, rch_san, rch_sil, rch_cla, rch_sag, rch_lag, rch_gra` | `ch(jrch)%rchstor, ch(jrch)%vel_chan` |
| [sym:hydrograph_module] | `jrch` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `peakr` | When the routine initializes the active reach at the start of the daily routing loop. | `peakr` is reset to zero because the routine is clearing the reach’s daily peak-flow summary before routing calculations compute the day’s peak discharge. |
| `rcharea` | When the routine initializes the active reach at the start of the daily routing loop. | `rcharea` is reset to zero because the cross-sectional area for the day will be recomputed from the current reach hydraulics. |
| `rchdep` | When the routine initializes the active reach at the start of the daily routing loop. | `rchdep` is reset to zero because the reach depth for the day is a derived routing result, not a carried-over value. |
| `rtevp` | When the routine initializes the active reach at the start of the daily routing loop. | `rtevp` is reset to zero so daily evaporation from the reach can be accumulated from scratch. |
| `rttime` | When the routine initializes the active reach at the start of the daily routing loop. | `rttime` is reset to zero because the reach travel time will be recomputed for the current day’s flow conditions. |
| `rttlc` | When the routine initializes the active reach at the start of the daily routing loop. | `rttlc` is reset to zero so daily transmission losses can be recalculated for the current reach and day. |
| `rtwtr` | When the routine initializes the active reach at the start of the daily routing loop. | `rtwtr` is reset to zero because the water leaving the reach on the day will be computed later in routing. |
| `sdti` | When the routine initializes the active reach at the start of the daily routing loop. | `sdti` is reset to zero so the day’s flow rate in the reach can be recomputed from current conditions. |
| `sedrch` | When the routine initializes the active reach at the start of the daily routing loop. | `sedrch` is reset to zero because sediment leaving the reach is a daily output that should not carry over from the previous day or reach. |
| `ch(jrch)%vel_chan` | When the routine initializes the active reach at the start of the daily routing loop. | `ch(jrch)%vel_chan` is reset to zero so the reach’s average channel velocity can be recalculated for the current routing step. |
| `rch_san` | When the routine initializes the active reach at the start of the daily routing loop. | `rch_san` is reset to zero because sand-sized sediment outflow is a daily mass-balance result. |
| `rch_sil` | When the routine initializes the active reach at the start of the daily routing loop. | `rch_sil` is reset to zero because silt-sized sediment outflow is a daily mass-balance result. |
| `rch_cla` | When the routine initializes the active reach at the start of the daily routing loop. | `rch_cla` is reset to zero because clay-sized sediment outflow is a daily mass-balance result. |
| `rch_sag` | When the routine initializes the active reach at the start of the daily routing loop. | `rch_sag` is reset to zero because small aggregate sediment outflow is a daily mass-balance result. |
| `rch_lag` | When the routine initializes the active reach at the start of the daily routing loop. | `rch_lag` is reset to zero because large aggregate sediment outflow is a daily mass-balance result. |
| `rch_gra` | When the routine initializes the active reach at the start of the daily routing loop. | `rch_gra` is reset to zero because gravel sediment outflow is a daily mass-balance result. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits affect `ch_rchinit.f90`: df07e3f added the routine with its documentation and zeroing logic; c7c8e22 carried that source forward unchanged in this file span; and 39fabde initialized the local daily pesticide variables (`rchwtr`, `bury`, `difus`, `reactb`, `reactw`, `resuspst`, `setlpst`, `volatpst`) with inline `= 0.` declarations.

- df07e3f introduced the new subroutine and its initial state resets for daily channel routing.
- 39fabde changed the local declarations to initialize the temporary daily variables at declaration time, avoiding uninitialized values before the explicit reset block.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_rchinit' has no extracted documentation comment.
