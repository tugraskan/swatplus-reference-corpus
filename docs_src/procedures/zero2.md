---
kind: procedure
symbol: zero2
title: zero2
status: filled
source_hash: 7d0c7aed5351ddb3
version_label: SWAT+ 62.0.0
locals:
  cklsp: Local scalar initialized to zero and then immediately set to zero again; it appears
    to be a leftover placeholder with no effect on the routine's behavior.
  zdb: Local scalar initialized to zero and then immediately set to zero again; the comment
    identifies it as a division term from the net pesticide equation, but `zero2` does not
    otherwise use it.
uses:
  hru_module: '`hru_module` owns the allocatable HRU state arrays that this routine clears.
    Zeroing them here resets shared per-HRU storage used by later sediment, overland, and
    groundwater calculations, so the rest of the model does not see uninitialized or stale
    values.'
---

<!-- facts:header -->

Resets a set of HRU sediment, wash, and related arrays to zero. It is a parameter-initialization helper called from `allocate_parms` before model calculations begin.

## Bottom Line

`zero2` is a short setup routine that clears several allocatable HRU state arrays in `hru_module` by assigning zero to each of them. The arrays include sediment yield fractions, overland/wash variables, and a few groundwater-related buffers such as `bss_ex`.

It matters because `allocate_parms` calls it during model initialization, so downstream routines start from a clean, known baseline rather than carrying stale values from a prior run or allocation cycle.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`zero2` runs during parameter allocation, after `allocate_parms` has already set several initialization values and before the model returns from that setup phase. `allocate_parms` prepares the shared HRU arrays and then calls `zero2` to clear them, so later HRU sediment, wash, and groundwater behavior starts from zeroed state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare the routine and import the HRU state arrays from `hru_module`. | The subroutine header establishes `zero2` as a no-argument initialization helper. The `use hru_module, only : ...` line brings in the shared arrays that will be reset. |
| 2. Select implicit typing rules and define two local scalars. | `implicit none` forces explicit declarations. `cklsp` and `zdb` are local reals initialized to zero, but they are not used in any later calculation in this routine. |
| 3. Set `cklsp` to zero. | The routine explicitly assigns `0.` to `cklsp`, reinforcing its initial zero value. |
| 4. Zero the overland yield state. | `ovrlnd` is reset so the HRU overland-flow/yield storage starts from a clean baseline. |
| 5. Zero the sediment yield component arrays. | `sedyld`, `sanyld`, `silyld`, `clayld`, `sagyld`, and `lagyld` are all set to zero so the sediment source fractions and sediment yield storage do not carry prior values into the next phase. |
| 6. Zero the `smx`, `surf_bs`, and `twash` states. | These shared HRU arrays are cleared to remove any prior values used by later wash/sediment-related calculations. |
| 7. Zero the `wrt` matrix. | `wrt` is reset to zero across all elements, clearing the shared two-dimensional state. |
| 8. Set `zdb` to zero. | The local scalar `zdb` is assigned zero even though it is not used further in this procedure. |
| 9. Zero the groundwater-linked `bss_ex` array. | `bss_ex` is cleared as part of initialization; the inline comment marks it as related to gwflow. |
| 10. Return to the caller and end the subroutine. | After all shared states are cleared, control returns to `allocate_parms` and the subroutine ends. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `clayld, lagyld, ovrlnd, sagyld, sanyld, sedyld, silyld, smx, surf_bs, twash, wrt, bss_ex` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ovrlnd` | Always, during the initialization pass in `allocate_parms`. | `ovrlnd` is cleared before HRU runoff-related calculations begin, so no previous overland state leaks into the new model setup. |
| `sedyld` | Always, during the initialization pass in `allocate_parms`. | `sedyld` is reset so sediment yield storage starts from zero before later HRU sediment routines populate it. |
| `sanyld` | Always, during the initialization pass in `allocate_parms`. | `sanyld` is cleared to remove any previous sand-yield fraction or mass before new calculations. |
| `silyld` | Always, during the initialization pass in `allocate_parms`. | `silyld` is zeroed so silt-yield state begins from a clean baseline for the next HRU cycle. |
| `clayld` | Always, during the initialization pass in `allocate_parms`. | `clayld` is zeroed so clay-yield state is not contaminated by prior run data. |
| `sagyld` | Always, during the initialization pass in `allocate_parms`. | `sagyld` is cleared because it is part of the sediment yield storage that must be reset before use. |
| `lagyld` | Always, during the initialization pass in `allocate_parms`. | `lagyld` is reset so lag sediment yield state starts at zero for the next model computations. |
| `smx` | Always, during the initialization pass in `allocate_parms`. | `smx` is cleared to zero as part of resetting shared HRU state used by later calculations. |
| `surf_bs` | Always, during the initialization pass in `allocate_parms`. | `surf_bs` is zeroed so the surface base-state matrix does not retain values from earlier allocations or runs. |
| `twash` | Always, during the initialization pass in `allocate_parms`. | `twash` is reset because wash-related shared state must begin from zero before downstream routines update it. |
| `wrt` | Always, during the initialization pass in `allocate_parms`. | `wrt` is cleared across both dimensions so the shared matrix starts empty for later HRU work. |
| `bss_ex` | Always, during the initialization pass in `allocate_parms`. | `bss_ex` is zeroed as part of groundwater-related initialization so later gwflow-linked code sees a clean starting value. |

## File I/O

<!-- facts:io -->


## Lineage

`zero2` was introduced in 94b6dec as a new routine that zeroes shared HRU arrays in `hru_module`. In 39fabde, `cklsp` and `zdb` were changed to be initialized at declaration and the routine still explicitly zeroed the same shared arrays. In 2ee1889, only the final procedure terminator changed from `end` to `end subroutine zero2`; the runtime behavior did not change.

- 94b6dec added the initialization routine and its zero assignments for the HRU arrays used by downstream model setup.
- 39fabde made the local scalars `cklsp` and `zdb` explicitly initialized at declaration while preserving the same zeroing behavior for the shared arrays.
- 2ee1889 updated the end statement syntax only; the procedure logic stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'zero2' has no extracted documentation comment.
