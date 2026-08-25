---
kind: procedure
symbol: sq_volq
title: sq_volq
status: filled
source_hash: 93a0830c3624819d
version_label: SWAT+ 62.0.0
uses:
  basin_module: The basin control flag `bsn_cc%gampt` tells `sq_volq` which runoff method
    the basin is configured to use. Without `basin_module`, this procedure would not know
    whether to route execution to the curve-number or Green-Ampt calculation.
---

<!-- facts:header -->

Chooses the daily runoff calculation for the current HRU. It dispatches to either curve-number runoff or Green-Ampt runoff based on the basin control flag `bsn_cc%gampt`.

## Bottom Line

`sq_volq` is a small dispatcher for surface runoff computation. It checks the basin control code `bsn_cc%gampt` and then calls either `sq_daycn` for the curve-number method or `sq_greenampt` for the Green-Ampt method.

This routine matters because `surface` uses it after precipitation has been screened for a runoff event. The routine’s choice determines how the HRU’s runoff depth is computed for the day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the surface-runoff portion of `surface`, after `sq_dailycn` has already been called and only when `precip_eff > 0.1`. Its inputs are therefore already prepared by the caller and by prior runoff setup, and its output is the runoff calculation path that downstream water-balance and routing code relies on through the HRU runoff state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Check the basin runoff-method control flag `bsn_cc%gampt` to decide whether the basin is using curve-number runoff or Green-Ampt runoff. |
| 2. call | If `bsn_cc%gampt == 0`, call `sq_daycn` to compute daily surface runoff using the curve-number approach for the current HRU. |
| 3. else | Otherwise, follow the Green-Ampt branch so the basin uses infiltration-based runoff computation instead of curve-number runoff. |
| 4. call | Call `sq_greenampt` to compute the HRU’s runoff with the Green-Ampt method, including the infiltration/runoff partitioning required by that option. |
| 5. return | Return to the caller after the appropriate runoff routine has finished, leaving the selected runoff state updated for later surface-flow processing. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gampt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`sq_volq.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `sq_volq.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_volq' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
