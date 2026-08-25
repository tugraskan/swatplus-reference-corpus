---
kind: procedure
symbol: swr_depstor
title: swr_depstor
status: filled
source_hash: 757dc18ff4ea654e
version_label: SWAT+ 62.0.0
locals:
  j: Loop/index variable for the current HRU. It is set from `ihru` and then used to read
    and update the HRU-specific state arrays such as `itill`, `cumeira`, `cumei`, `cumrt`,
    `cumrai`, `ranrns_hru`, and `stmaxd`.
  df: Decay factor used in the roughness attenuation equation. It is derived from soil clay
    and organic matter, limited to 1.0 when the intermediate expression exceeds 1.0, and then
    applied in the exponential decay for random roughness.
  hru_slpp: Current HRU slope steepness expressed as percent. It is computed from `hru(j)%topo%slope
    * 100` and used in the depressional-storage formula.
  sol_orgm: Estimated percent organic matter in the soil material for the current HRU. It
    is computed from the soil organic carbon pool `soil1(j)%tot(1)%c / 0.58` and used in the
    decay-factor expression.
  sol_rrr: Current random roughness for the HRU after decay from rainfall and erosivity. It
    is computed from the initial random roughness `ranrns_hru(j)` and used to calculate `stmaxd(j)`.
  ei: Current erosivity increment for the day. It is computed from `usle_ei * 18.7633` and
    added to the cumulative erosivity state when the HRU is under tillage.
  xx: Intermediate value for the decay-factor exponent. It combines clay and organic matter
    terms before being converted to `df` with the `exp` function or capped at 1.0.
uses:
  hru_module: This module supplies the current HRU context and the shared HRU-state arrays
    that swr_depstor reads and updates. The routine needs `ihru` to select the active HRU,
    `itill` to know whether tillage-based accumulation is active, `usle_ei` and `precip_eff`
    to build the cumulative rainfall/erosivity terms, `ranrns_hru` to seed random roughness,
    and `stmaxd` plus the cumulative arrays to store the updated depressional-storage state
    for that HRU.
  soil_module: This module provides the soil texture data used to compute the decay factor
    that reduces roughness with changing soil conditions. The clay fraction in `soil(j)%phys(1)%clay`
    is part of the exponent that determines `df`, so it directly influences the roughness
    decay and therefore the final storage depth.
  organic_mineral_mass_module: This module provides the soil organic carbon pool used to estimate
    organic matter content for the decay-factor calculation. `soil1(j)%tot(1)%c` is converted
    to organic matter and included in the exponent that controls how quickly roughness decays,
    which in turn changes `stmaxd(j)`.
---

<!-- facts:header -->

Computes the current maximum surface depressional storage depth for an HRU. It updates tillage-linked rainfall/erosivity accumulators and then uses soil and slope properties to estimate how much surface storage remains available.

## Bottom Line

swr_depstor is a daily HRU-level support routine for the tile/drainage workflow. It takes the current HRU index from `ihru`, updates cumulative rainfall and USLE erosivity totals when the HRU is under tillage (`itill(j) == 1`), and then converts soil texture, organic carbon, and slope into a current depressional-storage depth estimate `stmaxd(j)`.

The routine matters because `swr_drains` calls it immediately before computing surface storage (`storro = 0.2 * stmaxd(j)`), so its result directly affects how ponded water is partitioned into drainage-related surface storage for that HRU.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the surface-water/drainage workflow after `swr_drains` has selected the HRU and computed the day’s drainage-related geometry. `swr_drains` sets up the call, and `swr_depstor` then updates cumulative erosivity/rainfall state and recalculates `stmaxd(j)` so later drainage logic can use the current surface storage threshold.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and update cumulative event totals if the HRU is under tillage. | The routine copies `ihru` into `j`, computes the current erosivity increment `ei = usle_ei * 18.7633`, and, only when `itill(j) == 1`, adds that increment to the tillage-interval erosivity total and adds current effective precipitation to the rainfall total while also keeping carry-forward values without the current event. |
| 2. Build the soil-based decay factor from clay and organic matter. | The routine converts surface-layer carbon to organic matter with `soil1(j)%tot(1)%c / 0.58`, computes the exponent `xx` from clay and organic matter terms, caps the factor at 1.0 when `xx > 1.0`, and otherwise evaluates `df = exp(xx)`. |
| 3. Reduce random roughness using the decay factor and cumulative rainfall/erosivity. | The routine derives the current random roughness `sol_rrr` from the HRU's initial random roughness `ranrns_hru(j)` and exponentially decays it using `df` together with cumulative erosivity `cumei(j)` and cumulative rainfall `cumrt(j)`. |
| 4. Compute slope percent and convert roughness to maximum depressional storage. | The routine gets slope percent from `hru(j)%topo%slope * 100` and calculates `stmaxd(j)` from random roughness and slope using the storage equation `0.112*sol_rrr + 0.031*sol_rrr**2 - 0.012*sol_rrr*hru_slpp`. |
| 5. Return to the caller. | The routine finishes after updating the HRU-specific storage state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, itill, cumeira, cumei, cumrai, cumrt, ranrns_hru, stmaxd, ihru, precip_eff, usle_ei` | `hru(j)%topo%slope` |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%clay` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%tot(1)%c` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cumeira(j)` | When `itill(j) == 1`. | `cumeira(j)` is increased by the current day’s erosivity increment `ei`, so it holds the cumulative erosivity since the last tillage interval while tillage is active. |
| `cumei(j)` | When `itill(j) == 1`. | `cumei(j)` is reset to the carry-forward erosivity total by subtracting the current increment back out, so it represents cumulative erosivity excluding the present event for the decay calculation. |
| `cumrai(j)` | When `itill(j) == 1`. | `cumrai(j)` is increased by `precip_eff`, so it accumulates effective rainfall over the current tillage interval for the roughness-decay computation. |
| `cumrt(j)` | When `itill(j) == 1`. | `cumrt(j)` is reset to the rainfall carry-forward total by subtracting the current `precip_eff`, so it represents rainfall since the last tillage event for the decay calculation. |
| `stmaxd(j)` | Always, after `sol_rrr` and `hru_slpp` are computed. | `stmaxd(j)` is overwritten with the current maximum depressional storage estimate for the active HRU, based on slope and decayed random roughness. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits resolved. The routine was added in `df07e3f` with its full initial implementation. `94b6dec` mainly preserved the same code while adding the source file to the imported snapshot. `39fabde` initialized local variables to zero in the declaration block. `f1e61a3` fixed formatting/tab indentation without changing the calculations. `889136d` corrected a comment typo from 'cummulative' to 'cumulative'. `bd18ad4` added `external :: theta`, but that declaration is visible in the current source even though it does not participate in the shown calculations.

- df07e3f introduced the complete `swr_depstor` routine: cumulative tillage-linked rainfall/erosivity tracking, soil-based decay-factor computation, roughness decay, and the final `stmaxd` formula.
- 39fabde changed the routine by initializing `j`, `df`, `hru_slpp`, `sol_orgm`, `sol_rrr`, `ei`, and `xx` to zero at declaration time.
- f1e61a3 made formatting-only edits in the source snapshot and did not alter the algorithm.
- 889136d changed only a comment in the erosivity update section and did not change behavior.
- bd18ad4 added `external :: theta` to the declarations, but the visible routine body does not call `theta` in the extracted source.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_depstor' has no extracted documentation comment.
- algorithm_steps revised: expanded the original 4-step draft into 5 source-backed steps to separate HRU selection, decay-factor computation, roughness decay, storage calculation, and return.
