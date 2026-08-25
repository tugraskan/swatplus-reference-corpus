---
kind: procedure
symbol: smp_buffer
title: smp_buffer
status: filled
source_hash: 9d78d4b4853d526f
version_label: SWAT+ 62.0.0
locals:
  j: Holds the current HRU index. The routine initializes it to 0, then sets `j = ihru` so
    it can read and update the correct element of the HRU-state arrays.
  reduc: Stores the computed percent nitrate reduction from the buffer strip for the active
    HRU. It is calculated from `filterw(j)`, then forced to zero if the formula produces a
    negative value.
uses:
  hru_module: This routine depends on `hru_module` because the active HRU index (`ihru`) identifies
    which array element to update, `filterw` provides the buffer width used to compute reduction,
    and `latno3` is the nitrate state being modified in place for that HRU.
---

<!-- facts:header -->

Reduces lateral nitrate flow for the current HRU based on riparian buffer width. It looks up the active HRU, computes a percent reduction, and applies that reduction to `latno3`.

## Bottom Line

smp_buffer is a small HRU-level adjustment routine for the riparian buffer strip BMP. For the active HRU, it converts buffer width (`filterw`) into a nitrate reduction percentage, clamps negative reductions to zero, and then lowers the HRU’s lateral nitrate load (`latno3`).

This matters because hru_control calls it during pollutant-reduction processing when a filter strip is present. The updated `latno3` value becomes the nitrate amount passed on in the HRU water-quality workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

smp_buffer runs inside the HRU pollutant-reduction branch in `hru_control`, after `smp_filter` when `hru(j)%lumv%vfsi > 0.` and `filterw(j) > 0.`. `hru_control` has already selected the current HRU and set up its landuse/BMP context, and later nitrate transport and water-quality calculations depend on the reduced `latno3` value produced here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set active HRU index | Initialize `j` to 0, then assign `j = ihru` so the routine works on the current HRU’s state arrays. |
| 2. compute buffer reduction | Compute the nitrate reduction percentage as `2.1661 * filterw(j) - 5.1302`, using the current HRU’s filter-strip width. |
| 3. prevent negative reduction | If the computed reduction is below zero, reset it to zero so the buffer never increases nitrate instead of reducing it. |
| 4. apply reduction to nitrate state | Update `latno3(j)` by multiplying it by the remaining fraction `1. - reduc / 100.`, reducing the current HRU’s lateral nitrate load in place. |
| 5. return to caller | Exit the subroutine after the HRU nitrate state has been adjusted. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `filterw, latno3, ihru` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `latno3(j)` | When the active HRU has a filter width and the computed reduction is positive after clamping. | The routine overwrites `latno3(j)` with a reduced value for the current HRU, representing nitrate removal by the riparian buffer strip. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed smp_buffer. df07e3f added the routine with its riparian-buffer nitrate reduction formula and update to `latno3`; 39fabde then initialized the local variables `j` and `reduc` at declaration and kept the existing reduction logic unchanged.

- df07e3f introduced the new `smp_buffer` subroutine and its in-place reduction of `latno3` based on `filterw`.
- 39fabde only changed local variable initialization (`j = 0`, `reduc = 0.`) without changing the reduction formula or state update.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'smp_buffer' has no extracted documentation comment.
