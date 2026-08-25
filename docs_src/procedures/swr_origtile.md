---
kind: procedure
symbol: swr_origtile
title: swr_origtile
status: filled
source_hash: 2d2f3cc369a08fbd
version_label: SWAT+ 62.0.0
args:
  tile_above_btm: '`tile_above_btm` is the vertical distance from the bottom of the soil profile
    to the tile depth. It limits how much of the profile water above field capacity can contribute
    to drainage by scaling the excess water term against the available saturated thickness
    (`wt_shall`).'
locals:
  j: '`j` is the HRU index used to look up the active soil profile and HRU drainage parameters.
    It is initialized to 0 and then set from `ihru` so the routine works on the current HRU
    only.'
uses:
  hru_module: '`hru_module` provides the current HRU index and the shared drainage outputs/settings
    that this routine reads and writes. `ihru` selects the active HRU, `hru(j)%sdr%time` controls
    the exponential drainage response, `hru(j)%sdr%drain_co` limits the outflow, and `qtile`/`sw_excess`
    are updated here for later water-balance use.'
  soil_module: '`soil_module` supplies the current HRU soil-state values that determine whether
    tile drainage can occur and how large the excess is. The comparison of `soil(j)%sw` against
    `soil(j)%sumfc` decides if the soil is above field capacity, and the difference between
    them is the water available for drainage.'
---

<!-- facts:header -->

Computes tile drainage for the current HRU using soil-water excess, drain depth, and tile-time response.

## Bottom Line

`swr_origtile` is the older tile-drainage routine used when the basin is not using the DrainMOD-based tile equation path. It checks whether the current soil profile water storage is above field capacity, computes a drainage-eligible excess from the water table position relative to the tile depth, then converts that excess to daily tile flow using the HRU drain time and caps the result by the drain capacity.

The routine updates shared HRU state for tile outflow: `sw_excess` holds the excess water available to drain, and `qtile` holds the final tile flow returned to the rest of the water-balance calculation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`swr_percmain` calls this routine after it has determined that tile drainage is active for the current HRU and that the water table is above the tile depth (`wt_shall > d`). If the basin is not using the DrainMOD path, `swr_percmain` passes the tile depth argument to `swr_origtile`; the `qtile` value it produces then feeds the later daily HRU water-balance accounting, where negative values are also guarded against.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select HRU | Set local index `j` from `ihru` so the routine uses the current HRU and matching soil profile. |
| 2. check soil water | Proceed only when the active soil profile water storage exceeds field capacity; otherwise no tile drainage is produced. |
| 3. compute excess | Compute `sw_excess` from the portion of the soil-water surplus that lies above the tile-relevant water-table thickness, using `wt_shall` and `tile_above_btm` to scale the surplus. |
| 4. choose daily drain response | Convert excess water to `qtile` using either the full excess when drain time is under 1 hour, or the exponential drainage fraction `1 - Exp(-24. / hru(j)%sdr%time)` otherwise. |
| 5. cap by drain capacity | Limit the computed tile flow to the HRU drain capacity `hru(j)%sdr%drain_co`. |
| 6. no excess case | Set `qtile` to zero when the soil profile is not above field capacity, indicating no tile drainage from this routine. |
| 7. return | Return the updated shared tile-drainage values to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru, qtile, sw_excess, wt_shall` | `hru(j)%sdr%time` |
| [sym:soil_module] | `soil` | `soil(j)%sw, soil(j)%sumfc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sw_excess` | When `soil(j)%sw > soil(j)%sumfc` and the routine reaches the drainage branch. | `sw_excess` is overwritten with the water available for tile drainage from the current HRU, scaled by the water-table thickness above the tile depth. It represents the drainage-eligible portion of the soil-water surplus that the later flow calculation uses. |
| `qtile` | When the soil is above field capacity; if `hru(j)%sdr%time < 1.` the routine assigns all excess directly, otherwise it applies the exponential daily drainage fraction, then caps the result with `Min`. | `qtile` is overwritten with the final daily tile drainage flow for the current HRU, or set to zero when the soil profile is not wet enough to drain. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:2.2.1 | Tile drainage flow | $tile_{wtr}=\frac{h_{wtbl}-h_{drain}}{h_{wtbl}}*(SW-FC)*(1-exp[\frac{-24}{t_{drain}}])$ | Verified against SWAT+ 62.0.0 (swr_origtile.f90). tile flow active when water table exceeds drain depth (h_wtbl>h_drain) |

## Lineage

Four resolved commits changed `swr_origtile`: df07e3f added the routine with the original tile-drainage calculation, 35b029c commented out the old combined soil-water/water-table condition and kept the soil-water-only test, 39fabde initialized local `j` and normalized the return/end formatting, and 577e852 added a short-drain-time branch that sets `qtile = sw_excess` when `hru(j)%sdr%time < 1.` before applying the drain-cap limit.

- df07e3f introduced `swr_origtile` with soil-water-excess calculation, exponential daily drainage decay, and drain-cap limiting.
- 35b029c changed the activation condition from `soil(j)%sw > soil(j)%sumfc .and. wt_shall > 1.e-6` to only `soil(j)%sw > soil(j)%sumfc`, broadening when tile drainage can be computed.
- 39fabde initialized local variable `j` to 0 and made formatting-only cleanup to the return/end statements; functional behavior stayed the same.
- 577e852 added explicit handling for `hru(j)%sdr%time < 1.` so the routine returns the full excess instead of evaluating the exponential term for very short drain times.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_origtile' has no extracted documentation comment.
