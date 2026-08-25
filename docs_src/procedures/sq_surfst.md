---
kind: procedure
symbol: sq_surfst
title: sq_surfst
status: filled
source_hash: 22bb6d461ea89345
version_label: SWAT+ 62.0.0
locals:
  j: Loop index for the subdaily time-step loop; it iterates through `time%step` when Green-Ampt
    routing is active.
  k: Counter for each subdaily interval within the day; used to index `hhsurf_bs(1,j,k)` and
    `hhsurfq(j,k)` during lagged routing.
uses:
  basin_module: '`bsn_cc%gampt` is the basin-level switch that selects the routing branch.
    When it is zero, the routine uses daily surface runoff lag storage; when it is nonzero,
    it uses the subdaily Green-Ampt path with `hhsurf_bs` and `hhsurfq`.'
  time_module: '`time%step` tells the routine how many subdaily intervals are in the current
    day, so it controls the length of the lag-routing loop and which element of `hhsurf_bs(1,j,time%step)`
    holds the prior-day lag.'
  hru_module: These HRU-state arrays and scalars hold the runoff input, lag storage, routing
    fraction, and daily output for the current HRU. `sq_surfst` reads and updates them to
    compute how much runoff reaches the main channel and what remains stored for the next
    interval or day.
---

<!-- facts:header -->

Computes the HRU surface-runoff water that reaches the main channel for the current day, including lagged storage. It handles both daily runoff routing and subdaily (time-step) routing depending on the basin Green-Ampt control flag.

## Bottom Line

`sq_surfst` updates the surface-runoff lag store for the current HRU and computes the amount that reaches the main channel during the day. If basin Green-Ampt routing is off (`bsn_cc%gampt == 0`), it uses the daily HRU runoff state; if Green-Ampt routing is on, it steps through `time%step` subdaily intervals and carries runoff forward through `hhsurf_bs` and `hhsurfq`.

The routine matters because `hru_control` calls it after daily water additions have been accumulated, so its output becomes the finalized `qday` value for the HRU and the updated lagged runoff state (`bsprev`, `surf_bs`, or `hhsurf_bs`) that later routing and diagnostics depend on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the HRU daily water-balance workflow after `hru_control` has added any current-day runoff contributions to `qday`/related HRU state. It then converts the current HRU's stored surface runoff into the final daily amount reaching the main channel and leaves behind the lagged remainder that later HRU water-routing logic depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select routing branch | Check basin control `bsn_cc%gampt` to choose daily curve-number routing (`0`) or subdaily Green-Ampt routing (nonzero). |
| 2. daily branch setup | In the daily branch, save the previous lagged runoff in `bsprev`, add current-day `surfq(j)` to `surf_bs(1,j)`, route a fraction with `brt(j)` into `qday`, and keep the remainder in `surf_bs(1,j)`. |
| 3. subdaily branch setup | In the Green-Ampt branch, take the last subdaily lag value from `hhsurf_bs(1,j,time%step)` into `bsprev` and reset `qday` before processing time steps. |
| 4. loop through time steps | For each subdaily interval `k=1,time%step`, combine the prior carryover with the current interval inflow to determine the runoff available for routing. |
| 5. compute available subdaily runoff | Set `hhsurf_bs(1,j,k)` to the nonnegative available amount using `Max(1.e-9, bsprev + hhsurfq(j,k))`, then convert the sentinel value `1.e-9` to zero when the amount is effectively absent. |
| 6. route subdaily runoff | Multiply the available subdaily runoff by `brt(j)` to obtain routed runoff in `hhsurfq(j,k)`, then subtract that routed portion from `hhsurf_bs(1,j,k)` so the remainder stays in storage. |
| 7. carry lag and accumulate day total | Store the remaining subdaily runoff back into `bsprev` for the next interval and add the routed runoff to `qday`, which becomes the daily HRU total. |
| 8. finish | Return to the caller after updating the relevant HRU runoff states. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gampt` |
| [sym:time_module] | `time` | `time%step` |
| [sym:hru_module] | `surf_bs, surfq, brt, hhsurf_bs, hhsurfq, ihru, bsprev, qday` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bsprev` | When Green-Ampt routing is disabled, `bsprev` is set to the pre-update daily lag in `surf_bs(1,j)`; when Green-Ampt routing is enabled, it is set to the last subdaily lag stored in `hhsurf_bs(1,j,time%step)` and then refreshed each interval from `hhsurf_bs(1,j,k)`. | `bsprev` tracks the carryover runoff that must be combined with the next inflow before routing. It changes so the routine can preserve the remaining runoff between days or subdaily intervals. |
| `surf_bs(1,j)` | When `bsn_cc%gampt == 0`, `surf_bs(1,j)` is updated by adding `surfq(j)`, routing `qday = surf_bs(1,j) * brt(j)`, and subtracting `qday` from the store. | `surf_bs(1,j)` becomes the leftover daily surface runoff that did not reach the main channel on this call. |
| `qday` | When `bsn_cc%gampt == 0`, `qday` is set to the routed fraction of daily stored runoff; when `bsn_cc%gampt != 0`, it is reset to zero and then accumulated across subdaily intervals with `qday = qday + hhsurfq(j,k)`. | `qday` holds the total amount of surface runoff from the current HRU that reaches the main channel during the day. |
| `hhsurf_bs(1,j,k)` | Inside the `do k=1,time%step` loop, `hhsurf_bs(1,j,k)` is set from the previous carryover plus current interval inflow, bounded by `Max(1.e-9, ...)`, and then reduced by the routed amount. | `hhsurf_bs(1,j,k)` stores the subdaily leftover runoff after each interval's routing calculation so the next interval can use it as carryover. |
| `hhsurfq(j,k)` | Inside the same subdaily loop, `hhsurfq(j,k)` is overwritten with `hhsurf_bs(1,j,k) * brt(j)`. | `hhsurfq(j,k)` becomes the amount of runoff from interval `k` that actually reaches the main channel for the current HRU. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved for `sq_surfst`. The initial addition (`df07e3f`) introduced the subroutine and its daily/subdaily runoff-lag logic. `94b6dec` imported the same routine into the current source tree without changing the algorithm. `39fabde` initialized local loop variables `j` and `k` to zero and adjusted the final indentation/return formatting. `f1e61a3` kept the algorithm intact while fixing tabs and preserving the daily vs. subdaily branching structure. `20c879b` changed the subdaily storage calculation from `Max(0., bsprev + hhsurfq(j,k))` to an underflow-safe `Max(1.e-9, ...)` followed by a zero-reset sentinel check, which altered how tiny values are handled in the Green-Ampt branch.

- Added the daily and subdaily runoff-lag routing algorithm, including use of `bsn_cc%gampt`, `surf_bs`, `hhsurf_bs`, `hhsurfq`, `bsprev`, and `qday`.
- Initialized local loop counters `j` and `k` to zero and made only formatting changes to the subroutine footer.
- Cleaned whitespace/tabs without changing the runoff computation or state updates.
- Replaced the subdaily zero-floor with a `1.e-9` sentinel and explicit reset to `0.0` to avoid gfortran underflow errors while preserving the routing logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_surfst' has no extracted documentation comment.
