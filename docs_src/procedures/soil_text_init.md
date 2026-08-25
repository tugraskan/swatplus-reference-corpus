---
kind: procedure
symbol: soil_text_init
title: soil_text_init
status: filled
source_hash: 4a24f5794fac678c
version_label: SWAT+ 62.0.0
args:
  isol: '`isol` selects which `soil_module%soil` profile to initialize; the routine uses `soil(isol)`
    as the target profile and updates only that profile''s detached texture fractions.'
locals:
  sa: Holds the sand fraction converted from `soil(isol)%phys(1)%sand / 100.` so it can be
    reused in the detached sand formula.
  cl: Holds the clay fraction converted from `soil(isol)%phys(1)%clay / 100.` and controls
    the small-aggregate branch and the detached clay formula.
  si: Holds the silt fraction converted from `soil(isol)%phys(1)%silt / 100.` so it can be
    reused in the detached silt formula.
uses:
  soil_module: '`soil_module` owns the `soil` array and the `soil_profile` fields that this
    routine reads and overwrites. Without that shared profile state, the routine could not
    translate the current sand, clay, and silt contents into the stored detached sediment
    fractions used later by the model.'
---

<!-- facts:header -->

Initializes the detached sediment texture fractions for one soil profile from its sand, clay, and silt content. It also rescales those fractions if the computed large-aggregate fraction would be negative.

## Bottom Line

`soil_text_init` reads the current soil texture percentages for one profile, converts them to fractions, and computes detached sediment fractions for sand, silt, clay, small aggregates, and large aggregates. Those values are stored back in `soil_module` so later erosion and sediment-related routines can use a consistent texture breakdown.

The routine also checks for an invalid negative large-aggregate fraction, which can happen for very sandy soils, and renormalizes the detached fractions so they sum to 1.0 before setting `det_lag` to zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after a soil profile's texture inputs have been set or updated, as shown by `cal_parm_select` calling it after changing `soil(ielem)%phys(ly)%clay` or `soil(ielem)%phys(ly)%silt`. Its output feeds later erosion/sediment behavior that depends on `soil(isol)%det_san`, `det_sil`, `det_cla`, `det_sag`, and `det_lag` being current and normalized.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load texture fractions | Convert the selected soil profile's sand, clay, and silt percentages from `phys(1)` into fraction values stored in `sa`, `cl`, and `si`. |
| 2. compute detached sand | Set detached sand fraction to `sa * (1. - cl)**2.49`, so the sand contribution declines as clay content increases. |
| 3. compute detached silt | Set detached silt fraction to `0.13 * si`. |
| 4. compute detached clay | Set detached clay fraction to `0.20 * cl`. |
| 5. choose small aggregates | Assign detached small-aggregate fraction from clay content: use `2.0 * cl` when `cl < .25`, `.57` when `cl > .5`, and a linear interpolation `.28 * (cl - .25) + .5` between those bounds. |
| 6. compute large aggregates | Calculate detached large-aggregate fraction as the remaining share after subtracting sand, silt, clay, and small aggregates from 1.0. |
| 7. normalize if needed | If the computed large-aggregate fraction is negative, rescale sand, silt, clay, and small-aggregate fractions by dividing them by `1 - det_lag`, then set `det_lag` to zero. |
| 8. return | Return after the selected soil profile's detached texture fractions have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `soil` | `soil(isol)%phys(1)%sand, soil(isol)%phys(1)%clay, soil(isol)%phys(1)%silt, soil(isol)%det_san, soil(isol)%det_sil, soil(isol)%det_cla, soil(isol)%det_sag, soil(isol)%det_lag` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(isol)%det_san` | After `sa`, `cl`, and `si` are loaded from `soil(isol)%phys(1)`. | `soil(isol)%det_san` is overwritten with the detached sand fraction for the selected soil profile, based on the profile's sand content and clay-dependent reduction; if the negative `det_lag` check fails, it is further rescaled to preserve a unit sum. |
| `soil(isol)%det_sil` | After `sa`, `cl`, and `si` are loaded from `soil(isol)%phys(1)`. | `soil(isol)%det_sil` is overwritten with the detached silt fraction for the selected soil profile, and it is also rescaled if the routine has to correct a negative `det_lag`. |
| `soil(isol)%det_cla` | After `sa`, `cl`, and `si` are loaded from `soil(isol)%phys(1)`. | `soil(isol)%det_cla` is overwritten with the detached clay fraction for the selected soil profile, and it is also rescaled if the routine has to correct a negative `det_lag`. |
| `soil(isol)%det_sag` | The value of `cl` determines which branch of the clay/aggregate rule is used. | `soil(isol)%det_sag` is set from clay content using a low-clay, mid-clay, or high-clay rule, and it is rescaled if the negative `det_lag` correction is needed. |
| `soil(isol)%det_lag` | After the sand, silt, clay, and small-aggregate fractions are computed; then the routine checks whether the remainder is negative. | `soil(isol)%det_lag` stores the leftover large-aggregate fraction. If it is negative, the routine treats the soil texture as non-typical and forces the other detached fractions to renormalize before setting `det_lag` to zero. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one behavior change and two non-behavior edits. The procedure was added in commit df07e3f, later commit 39fabde initialized the local reals `sa`, `cl`, and `si` to `0.` while leaving the formulas unchanged, commit f1e61a3 only converted tab indentation to spaces in the negative-`det_lag` block, and commit 889136d only corrected a comment typo from "wont" to "won't".

- df07e3f introduced `soil_text_init` and its detached texture initialization logic for sand, silt, clay, small aggregates, and large aggregates.
- 39fabde changed local-variable initialization by assigning `0.` to `sa`, `cl`, and `si`; this was a code change but did not alter the formulas or branching behavior.
- f1e61a3 only reformatted indentation in the `det_lag < 0.` correction block; behavior remained the same.
- 889136d only corrected a comment in the error-check note; behavior remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'soil_text_init' has no extracted documentation comment.
