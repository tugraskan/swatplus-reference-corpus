---
kind: procedure
symbol: hru_sweep
title: hru_sweep
status: filled
source_hash: 1f5caf5db9740338
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` and used to address the current element of `twash` for the
    active HRU.
  dirt: Temporary storage for the current street solids load in kg/curb km. It is first computed
    from the buildup relation, then reduced by sweeping, and finally used to reset `twash(j)`.
  fr_curb: Sweepable-curb availability factor. In this extracted source it is initialized
    to 0. and never assigned before use, so the implemented reduction becomes a no-op unless
    another source/version provides a value; the lineage diff shows only initialization changes,
    not a new assignment.
uses:
  hru_module: These `hru_module` variables define which HRU is being processed (`ihru`), how
    much sweeping is applied (`sweepeff`), which urban database row to use (`ulu`), and where
    the result is stored (`twash`). Without them, the routine has no HRU context and no place
    to write the updated street-buildup state.
  urban_data_module: '`urban_data_module` supplies the urban database entry for the current
    urban land use. `urbdb(ulu)%dirtmx` and `urbdb(ulu)%thalf` provide the maximum street
    dirt load and buildup half-time used in the buildup/sweeping formulas.'
---

<!-- facts:header -->

Applies the urban street-sweeping operation for one HRU. It reduces the current curb-street dirt load and resets the corresponding buildup time to match the cleaned condition.

## Bottom Line

hru_sweep updates the street-sweeping state for the current HRU. It reads the HRU index and urban parameters from module state, computes the amount of dirt present before sweeping, applies the configured sweeping removal efficiency, and then converts the reduced dirt load back into an updated buildup time.

This matters because the routine is the model’s mechanism for street cleaning in urban areas. The resulting `twash` value affects how much solids are available on impervious streets the next time buildup and wash-off are evaluated.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the urban HRU processing in `hru_urbanhr` after runoff/buildup time has been advanced. `hru_urbanhr` checks sweep timing conditions and then calls `hru_sweep`; the updated `twash` state then controls later urban buildup and wash-off behavior for the same HRU.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. copy the active HRU index | The routine clears `j` to 0 and then sets `j = ihru` so subsequent array access targets the current HRU record. |
| 2. compute pre-sweep dirt load | It initializes `dirt` and calculates the current solids load on the street using the urban database maximum (`dirtmx`) scaled by the current buildup time `twash(j)` relative to `thalf + twash(j)`. |
| 3. apply sweeping reduction | The dirt load is multiplied by `1. - fr_curb * sweepeff` to represent removal by sweeping; if the result is extremely small, it is forced to zero. |
| 4. convert cleaned dirt back to buildup time | The routine resets `twash(j)` and then recomputes it from the reduced dirt load using the inverse of the buildup relation: `thalf * dirt / (dirtmx - dirt)`. |
| 5. exit the routine | The subroutine returns to its caller after leaving the updated HRU street-sweep state in module storage. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `twash, ihru, sweepeff, ulu` |  |
| [sym:urban_data_module] | `urbdb` | `urbdb(ulu)%dirtmx` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `twash(j)` | Executed whenever `hru_urbanhr` calls `hru_sweep` for the current `ihru`/`ulu` context. | `twash(j)` is overwritten with the buildup-time equivalent of the cleaned street dirt load. The routine first sets it to 0. and then replaces it with the recalculated value, so the stored state reflects the post-sweep condition rather than the pre-sweep buildup. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:3.4.4 | Street cleaning solid removal | $SED=SED_0*(1-fr_{av}*reff)$ | Verified against SWAT+ 62.0.0 (hru_sweep.f90). street cleaning removal |

## Lineage

Three resolved commits changed `hru_sweep`: df07e3f added the routine with the street-sweeping buildup/removal logic; 94b6dec introduced the current source version into the tree with the same behavior; and 39fabde only initialized the local variables `j`, `dirt`, and `fr_curb` to zero without changing the algorithm.

- df07e3f introduced the street-sweeping procedure, including the dirt buildup calculation, the sweeping reduction, and the conversion back into `twash(j)`.
- 39fabde changed only local variable initialization (`j = 0`, `dirt = 0.`, `fr_curb = 0.`) and did not alter the computed sweep behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_sweep' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into five steps to match the visible operations and cite actual line ranges.
- Source shows `fr_curb` initialized to 0. and never assigned within this subroutine; the extracted lineage and source packet do not show where a nonzero value would come from.
