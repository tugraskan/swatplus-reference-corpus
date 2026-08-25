---
kind: procedure
symbol: cli_bounds_check
title: cli_bounds_check
status: filled
source_hash: 2ef7e1cff7d46ac2
version_label: SWAT+ 62.0.0
args:
  st_day: '`st_day` is the first day-of-year available in the climate record. If the simulation
    is in the same start year and the current simulation day is earlier than `st_day`, the
    routine marks the record as out of bounds.'
  st_yr: '`st_yr` is the first calendar year available in the climate record. If `st_yr` is
    later than the current simulation year, the record starts after the simulation and is
    marked out of bounds.'
  end_day: '`end_day` is the last day-of-year available in the climate record. If the simulation
    is in the same end year and the current simulation day is later than `end_day`, the record
    is marked out of bounds.'
  end_yr: '`end_yr` is the last calendar year available in the climate record. If `end_yr`
    is earlier than the current simulation year, the record ends before the simulation and
    is marked out of bounds.'
  out_bounds: '`out_bounds` is the one-character status flag this routine sets to "y" when
    the current simulation day falls outside the climate record limits; callers initialize
    it to "n" before the check.'
uses:
  time_module: '`time_module` provides the current simulation year and day (`time%yrc`, `time%day`)
    that define the comparison point. Without that shared state, the routine would have no
    way to decide whether the climate record brackets the active model date.'
  climate_module: '`climate_module` is the source of the climate-record metadata structures
    that the callers pull from before invoking this check. The routine itself does not reference
    named members from that module in the extracted source, but the module matters because
    the caller passes climate dataset start/end bounds from climate-control state.'
---

<!-- facts:header -->

`cli_bounds_check` tests whether a climate record's date range covers the current simulation day. It flags `out_bounds` when the simulation starts before the record begins or continues after the record ends.

## Bottom Line

This subroutine compares the current simulation date in `time_module` against a climate dataset's start and end year/day. If the simulation day falls before the dataset starts or after it ends, it sets `out_bounds` to "y"; otherwise the caller can treat the data as usable for the current step.

It does not read files or update climate values itself. Instead, `cli_precip_control` and `climate_control` call it to decide whether precipitation or temperature/other climate time series can be indexed safely, and to trigger their fallback behavior when the requested weather data are outside the available range.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the climate-control path after a caller has selected a climate dataset and before that caller indexes weather time series. `cli_precip_control` prepares precipitation record bounds from `pcp(ipg)%...`, and `climate_control` prepares temperature/tgage record bounds from `tmp(ig)%...`. The result determines whether later code uses the climate arrays normally or switches to the caller's out-of-bounds handling, such as setting weather outputs to the sentinel value `-98.`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compare start year | The routine first checks whether the climate record starts after the current simulation year. If `st_yr` is greater than `time%yrc`, the simulation is already before the available data, so `out_bounds` is set to "y". |
| 2. Check matching start year | If the start year matches the current simulation year, the routine compares day-of-year values. A start day later than `time%day` means the simulation has not yet reached the first available climate day, so `out_bounds` is set to "y". |
| 3. Compare end year | The routine next checks whether the climate record ends before the current simulation year. If `end_yr` is less than `time%yrc`, the available data end too early and `out_bounds` is set to "y". |
| 4. Check matching end year | If the end year matches the current simulation year, the routine compares day-of-year values. An end day earlier than `time%day` means the simulation has moved past the last available climate day, so `out_bounds` is set to "y". |
| 5. Return to caller | After the comparisons, the subroutine returns control to the caller, leaving `out_bounds` set to indicate whether the climate record covers the current model date. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%yrc, time%day` |
| [sym:climate_module] | `time` | `time%yrc, time%day` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. `df07e3f` introduced `cli_bounds_check` with the current logic and documentation comment. `c7c8e22` re-added the same subroutine in a later import/update and the diff shows no behavioral change to the checks themselves in the visible hunk.

- df07e3f added the new `cli_bounds_check` subroutine, including the `time_module`/`climate_module` uses, argument declarations, and the year/day boundary checks that set `out_bounds`.
- c7c8e22 preserved the same boundary-check logic in the imported source snapshot; the visible diff shows the routine carried forward without changing the comparison behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_bounds_check' has no extracted documentation comment.
