---
kind: procedure
symbol: sq_crackflow
title: sq_crackflow
status: filled
source_hash: 61fd056bfd6ea040
version_label: SWAT+ 62.0.0
locals:
  j: HRU index local used to copy `ihru` so the routine can update the active HRU’s runoff
    entries in `surfq(j)` and `hhqday(j,ii)`.
  voli: Remaining crack volume available to subtract from subdaily hourly runoff. It starts
    at `voltot` and is decremented as `hhqday(j,ii)` is reduced.
  ii: Loop counter over the subdaily time steps in the current day when `time%step > 1`.
uses:
  basin_module: The basin crack-flow switch controls whether `surface` calls this routine
    at all, so basin configuration determines whether crack-flow adjustment is applied.
  hru_module: The HRU module holds the active HRU index, daily surface runoff, hourly runoff
    array, and crack volume. `sq_crackflow` uses those shared states to identify which HRU
    to adjust and to update the runoff values in place.
  time_module: The time-step setting determines whether the routine only adjusts daily runoff
    or also loops through hourly runoff values. Without `time%step`, it could not decide how
    to distribute crack-volume removal across subdaily intervals.
---

<!-- facts:header -->

Adjusts surface runoff for crack flow at the HRU scale. It reduces daily runoff and, when the model is running subdaily, distributes the crack-volume deduction across hourly runoff values.

## Bottom Line

sq_crackflow is a runoff post-processing routine. It checks whether the current HRU’s surface runoff is larger than the available crack volume (`voltot`); if so, it subtracts that volume, otherwise it zeroes the daily surface runoff.

When the simulation uses more than one time step per day, the routine also walks through the hourly runoff array and removes the same crack volume from `hhqday` until the volume is exhausted. This keeps the daily and subdaily runoff accounting consistent with the crack-flow adjustment.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the surface-runoff sequence in `surface`, after `sq_volq` has computed runoff and only when runoff is positive and basin crack flow is enabled (`bsn_cc%crk == 1`). Its result feeds later daily runoff routing, including the remaining `surfq(j)` used after irrigation runoff is added and the downstream daily channel runoff accounting in `surface`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select active HRU | Initialize local counters, then copy the current HRU index from `ihru` into `j` so the routine can operate on the correct entries in the shared runoff arrays. |
| 2. reduce daily runoff | Compare daily surface runoff against available crack volume. If runoff exceeds `voltot`, subtract the crack volume from `surfq(j)`; otherwise set the daily runoff to zero because cracks can absorb it all. |
| 3. check subdaily mode | Only proceed to hourly redistribution when the simulation uses more than one time step per day. Set `voli` to the total crack volume so the same volume can be removed from hourly runoff. |
| 4. loop through hourly runoff | For each hourly time step, compare hourly runoff to the remaining crack volume. If the hourly runoff is larger, subtract the remaining volume and set `voli` to zero; otherwise subtract the whole hourly runoff from `voli` and zero that hourly value. |
| 5. exit | Return to the caller after the daily and, if needed, hourly runoff arrays have been updated for crack flow. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%crk` |
| [sym:hru_module] | `surfq, hhqday, ihru, voltot` |  |
| [sym:time_module] | `time` | `time%step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `surfq(j)` | When `surfq(j) > voltot`, `surfq(j)` is reduced by `voltot`; otherwise it is set to `0.` | The active HRU’s daily surface runoff is trimmed by the crack volume so that part of the runoff is diverted into cracks before later routing steps use the daily value. |
| `hhqday(j,ii)` | When `time%step > 1`, the routine enters the hourly loop and updates `hhqday(j,ii)` for each hour based on the remaining crack volume `voli`. | The hourly runoff series is reduced in place so subdaily runoff accounting matches the same crack-flow loss applied to the daily total. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.3.6 | Surface runoff reduced by crack volume when runoff exceeds cracks | $Q_{surf}=Q_{surf,i}-crk$ | Verified against SWAT+ 62.0.0 (sq_crackflow.f90). surface runoff vs crack volume comparison |
| 2:3.3.7 | Zero runoff when cracks absorb all runoff | $Q_{surf}=0$ | surfq is set to zero when runoff is less than available crack volume. |

## Lineage

Two resolved commits changed `sq_crackflow`. The initial addition commit df07e3f introduced the subroutine with its crack-flow runoff adjustment logic and module dependencies. Commit 39fabde only initialized the local variables `j`, `voli`, and `ii` to zero; the crack-flow algorithm itself was unchanged.

- df07e3f added `sq_crackflow` as a new subroutine that reduces `surfq` by crack volume and, for subdaily runs, removes the same volume from `hhqday`.
- 39fabde changed only local variable initialization (`j = 0`, `voli = 0.`, `ii = 0`) without altering the runoff-adjustment behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_crackflow' has no extracted documentation comment.
- algorithm_steps revised: merged the explicit local-initialization and assignment details into a single active-HRU setup step, and condensed the exit to the actual return path at the end of the subroutine.
- The packet’s callee list names `surfq` and `hhqday`, but the source lines show these as module arrays, not procedure calls; callee-purpose text reflects that uncertainty.
