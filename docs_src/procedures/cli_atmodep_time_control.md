---
kind: procedure
symbol: cli_atmodep_time_control
title: cli_atmodep_time_control
status: filled
source_hash: 1484258f39f9bbf8
version_label: SWAT+ 62.0.0
uses:
  climate_module: The atmospheric deposition control block in `climate_module` holds the persistent
    inputs and outputs that determine whether this routine does anything and how it updates
    the counter. `num_sta`, `timestep`, `yr_init`, and `mo_init` define the activation and
    start condition, while `ts` and `first` are the state variables this routine initializes
    and advances.
  time_module: The `time_module` state provides the current simulation year and month plus
    the end-of-period flags that trigger counter advancement. Without `time%yrc`, `time%mo`,
    `time%end_yr`, and `time%end_mo`, this routine could not tell when the configured start
    point has been reached or when to increment the atmospheric deposition counter.
---

<!-- facts:header -->

Advances the atmospheric deposition station counter at the start of the simulation and at each year or month boundary, depending on the configured timestep.

## Bottom Line

This routine manages the atmospheric deposition time-step counter stored in `climate_module%atmodep_cont`. If atmospheric deposition stations are configured, it initializes `ts` to 1 at the configured start year or start year/month, then increments `ts` at each end-of-year or end-of-month event for the chosen timestep.

The routine also clears the `first` flag after the initial start point is reached so later calls switch from initialization to periodic advancement. `time_control` calls it after `climate_control`, so the current simulation date in `time_module%time` is already available when the counter is updated.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `time_control` immediately after `climate_control` has updated the simulation clock and weather state. It prepares the atmospheric deposition station counter so later atmospheric deposition processing can use the correct `ts` value for the current year or month cycle.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. test station availability | The routine first checks whether any atmospheric deposition stations are configured. If `atmodep_cont%num_sta` is zero or less, it exits without changing the counter. |
| 2. handle first-time initialization | If this is the first call (`atmodep_cont%first == 1`), the routine looks for the configured simulation start point. It uses the selected timestep to decide whether to match only the start year or the start year and month. |
| 3. initialize yearly start | For yearly deposition (`timestep == 'yr'`), the routine sets `ts` to 1 when the current calendar year equals `yr_init`, then clears `first` so later calls move into increment mode. |
| 4. initialize monthly start | For monthly deposition (`timestep == 'mo'`), the routine sets `ts` to 1 when both the current year and month match `yr_init` and `mo_init`, then clears `first` so later calls move into increment mode. |
| 5. switch to periodic advancement | After initialization has happened, the routine uses the `else` branch to advance the counter only on periodic boundaries instead of resetting it again. |
| 6. increment yearly counter at year end | For yearly deposition, the routine increments `ts` by 1 when `time%end_yr` is 1, which marks the end of a simulation year. |
| 7. increment monthly counter at month end | For monthly deposition, the routine increments `ts` by 1 when `time%end_mo` is 1, which marks the end of a simulation month. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `atmodep_cont` | `atmodep_cont%num_sta, atmodep_cont%first, atmodep_cont%timestep, atmodep_cont%yr_init, atmodep_cont%ts, atmodep_cont%mo_init` |
| [sym:time_module] | `time` | `time%yrc, time%mo, time%end_yr, time%end_mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `atmodep_cont%ts` | When `atmodep_cont%num_sta > 0` and either the start year matches for yearly mode or the start year and month match for monthly mode, and on later calls when the selected end-of-period flag is set. | `atmodep_cont%ts` is set to 1 at the configured start point, then increased by 1 at each later year-end or month-end event depending on `atmodep_cont%timestep`. This keeps the atmospheric deposition time-step index aligned with the simulation calendar. |
| `atmodep_cont%first` | When the first valid start point is reached for the configured timestep, specifically after the routine assigns `ts = 1` at the matching start year or start year/month. | `atmodep_cont%first` is cleared from 1 to 0 so the routine knows initialization is complete. On subsequent calls it will no longer reset `ts` and will instead only increment the counter at the appropriate end-of-period boundary. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in commit df07e3f as a new source file containing the full atmospheric deposition time-control logic. Commit c7c8e22 did not change the routine's behavior; its diff only shows the same source content carried forward from the previous version, with no functional edits visible in the resolved snippet.

- df07e3f introduced `cli_atmodep_time_control` with initialization and end-of-period increment logic for yearly and monthly atmospheric deposition timing.
- c7c8e22 preserved the routine content without a visible behavioral change in the resolved diff.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_atmodep_time_control' has no extracted documentation comment.
