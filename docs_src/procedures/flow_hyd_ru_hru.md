---
kind: procedure
symbol: flow_hyd_ru_hru
title: flow_hyd_ru_hru
status: filled
source_hash: 871abceff3047b1b
version_label: SWAT+ 62.0.0
args:
  iday_start: Starting hydrograph day index for the current runoff event; it seeds the current
    and previous lag-day positions before the routine begins shifting flows through the hydrograph
    array.
  surfq: Daily surface runoff volume to distribute across the unit hydrograph; this is the
    flow component that is multiplied by `uh` and added into `hyd_flo`.
  latq: Daily lateral soil flow volume; it is combined with tile flow to form the subsurface
    flow term `ssq`, which is treated as uniformly distributed over the day.
  tileq: Daily tile drainage volume; it is added to lateral flow when forming the subsurface
    runoff contribution for the current hydrograph day.
  uh: Unit hydrograph weights by lag day and subdaily step; the routine uses these coefficients
    to spread `surfq` across the `hyd_flo` time slots.
  hyd_flo: Accumulating hydrograph storage for lag days and subdaily steps; the routine zeros
    the previous-day slot and adds routed surface runoff into the current-day slot in place.
locals:
  istep: Subdaily step index inside each lag day; it walks through the `time%step` columns
    while applying the unit hydrograph.
  iday: Lag-day loop counter; it advances through the hydrograph window from day 1 to `bsn_prm%day_lag_mx`.
  iday_prev: Tracks the previous lag-day slot so the routine can clear the old day’s hydrograph
    before shifting forward.
  iday_cur: Tracks the current lag-day slot receiving routed runoff during the loop; it is
    wrapped back to 1 when it passes the lag-day maximum.
  ssq: Subsurface flow rate per time step, computed from lateral plus tile runoff divided
    by the number of subdaily steps; the code prepares it as a uniform daily contribution,
    though the extracted loop only resets it after the first lag day.
  sq: Temporary routed surface-runoff increment for one lag day and time step, computed as
    `uh(iday,istep) * surfq` before adding into `hyd_flo`.
  sumflo: Accumulator intended to track total routed flow when hydrograph lagging exceeds
    the maximum days; in the extracted source it is initialized but not used further.
uses:
  hydrograph_module: This module defines the hydrograph-related shared data structures that
    `hyd_flo` and `uh` belong to, so the subroutine depends on its declarations to work with
    the routed flow arrays.
  time_module: '`time%step` sets how many subdaily slots exist in each day, which controls
    the inner loop and the divisor used when spreading lateral/tile flow uniformly over the
    day.'
  basin_module: '`bsn_prm%day_lag_mx` sets the size of the lagged hydrograph window and provides
    the wraparound limit for the day-index shifts.'
---

<!-- facts:header -->

Builds subdaily HRU/RU flow hydrographs from daily surface, lateral, and tile runoff. It shifts hydrograph storage across lag days so each time step gets the right routed flow contribution.

## Bottom Line

This subroutine turns one day’s runoff inputs into a lagged, subdaily hydrograph array. It uses the basin’s maximum lag length and the model time-step count to place surface runoff through the unit hydrograph and to keep the rolling daily storage aligned with the current and previous lag days.

It matters because HRU and RU routing later reads `hyd_flo` to represent how runoff is distributed through the day instead of as a single daily total. The routine also clears the previous-day slot before rebuilding the hydrograph so stale flow does not carry forward.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when HRU or RU routing needs to expand daily runoff into a subdaily hydrograph, after the caller has populated daily surface, lateral, and tile flow values plus the unit hydrograph for the current command. `hru_hyds` and `ru_control` prepare those inputs before calling it, and the resulting `hyd_flo` array feeds later routed-flow behavior that expects subdaily timing rather than a single daily total.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize day pointers | Sets the current lag-day index from `iday_start`, computes the previous lag-day index, and wraps the previous index to the maximum lag day when the start day is the first slot. |
| 2. compute uniform subsurface flow | Forms the lateral-plus-tile subsurface flow term and divides it by the number of subdaily steps, then initializes the running sum accumulator. |
| 3. clear previous lag day | Zeros the previous day’s hydrograph slot so old routed flow does not remain in the rolling storage. |
| 4. loop over lag days | Walks through each lag day in the hydrograph window to distribute runoff across the full lagged response period. |
| 5. drop subsurface flow after first day | Keeps the subsurface term only for the first lag day and resets it to zero on later lag days, matching the one-day uniform contribution assumption. |
| 6. loop over subdaily steps | For each subdaily slot, multiplies the unit hydrograph weight by surface runoff and adds that routed amount into the current hydrograph day. |
| 7. advance rolling day indices | Moves the current and previous day pointers forward one slot and wraps each pointer back to 1 when it passes the basin lag-day maximum. |
| 8. return | Exits after the lagged hydrograph array has been updated in place for the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `hydrograph_module state` | `No candidate outside references were resolved to this module in the extracted context.` |
| [sym:time_module] | `time` | `time%step` |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%day_lag_mx` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three source states: the routine was introduced in df07e3f with the hydrograph-purpose comment, module uses, arguments, and the lag-day/subdaily routing loop; 94b6dec later added the same source into the imported codebase; 39fabde only initialized the local counters and accumulators to zero without changing the routing logic.

- df07e3f introduced `flow_hyd_ru_hru` as a new routine that builds subdaily hydrographs from daily runoff inputs and adds the lag-day wraparound logic.
- 39fabde changed only local variable initialization (`istep`, `iday`, `iday_prev`, `iday_cur`, `ssq`, `sq`, `sumflo`) and did not alter the routing algorithm.
- 94b6dec imported the routine into the current source tree with the same routing behavior present in the new-file version.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'flow_hyd_ru_hru' has no extracted documentation comment.
