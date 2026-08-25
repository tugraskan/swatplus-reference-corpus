---
kind: procedure
symbol: dr_ru
title: dr_ru
status: filled
source_hash: e117ee1e27ee145e
version_label: SWAT+ 62.0.0
locals:
  ii: Loop counter over the elements listed in `ru_def(iru)%num`; it selects which routing-unit
    element is being processed within the current routing unit.
  ielem: Holds the actual routing-unit element index looked up from `ru_def(iru)%num(ii)`,
    so the routine can read and write that element's delivery-ratio state in `ru_elem(ielem)`.
  rto: Temporary delivery-ratio factor computed from the selected object's travel-time source;
    it is later square-rooted, capped at 1.0, and stored in `ru_elem(ielem)%dr`.
uses:
  hydrograph_module: This module provides the routing-unit structure and the per-element hydrograph
    state that dr_ru reads and writes. `sp_ob%ru` controls how many routing units are visited,
    `ru_def(iru)%num_tot` and `ru_def(iru)%num(ii)` define the element list for each unit,
    `ru_elem(ielem)%obtypno`, `%obtyp`, and `%dr_name` determine which element is being processed
    and whether it uses calculated or full delivery ratio, and `%dr` / `%dr%flo` are the outputs
    this routine updates.
  hru_lte_module: This module holds the HRU-LTE travel-time database used for the `hlt` object
    type. When a routing-unit element represents an `hlt`, dr_ru uses `hlt_db(ihru)%tc` as
    the timing basis for the calculated delivery ratio.
  ru_module: This module supplies the routing-unit travel-time array `ru_tc` and the routing-unit
    index `iru` used in the ratio calculation. The calculated delivery ratio divides by `ru_tc(iru)`,
    so this state determines the normalization for every eligible element in the routing unit.
  hru_module: This module provides the HRU index `ihru` and the HRU travel-time array `tconc`
    used when a routing-unit element is of type `hru`. dr_ru loads `ihru` from each element
    so it can read the matching HRU concentration time from `tconc(ihru)`.
---

<!-- facts:header -->

Computes routing-element delivery ratios within each routing unit. It assigns either a calculated fraction based on travel time or a full delivery ratio, depending on each element's delivery-ratio setting.

## Bottom Line

dr_ru walks every routing unit and every element inside it, then fills the element-level delivery-ratio output in `ru_elem(ielem)%dr`. For elements marked `calc` or `0`, it derives a ratio from the element type and upstream timing state, bounds it to 1 after taking the square root, and stores the result with unit flow volume. For elements marked `full` or `1`, it assigns a full delivery ratio of 1.0.

This matters because downstream routing and hydrograph handling use the per-element `dr` state that this routine prepares. The routine combines routing-unit topology from `hydrograph_module` with HRU timing information from `hru_module` and `hru_lte_module` to decide how much of each element's load is delivered.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after routing-unit and HRU timing state has been populated in the global modules. Its inputs are prepared by the routing-unit setup that fills `sp_ob`, `ru_def`, `ru_elem`, and the travel-time arrays in `ru_module`, `hru_module`, and `hru_lte_module`. The results are then consumed by later routing and hydrograph behavior that relies on each `ru_elem(ielem)%dr` value.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Iterate over every routing unit configured in `sp_ob%ru`. |
| 2. loop | Within the current routing unit, iterate over every listed element using `ru_def(iru)%num_tot`. |
| 3. assign | Map the element index from `ru_def(iru)%num(ii)` into `ielem`, then load the associated HRU/object number into `ihru` from `ru_elem(ielem)%obtypno`. |
| 4. if | Only calculate a delivery ratio when the element's delivery-ratio name is `calc` or `0`; otherwise leave the element for the later full-ratio branch. |
| 5. select | Choose the travel-time source by object type: use `tconc(ihru)` for `hru`, `hlt_db(ihru)%tc / 3600.` for `hlt`, and force `rto = 1.` for `sdc` and `ru` elements. |
| 6. scale | Convert the raw ratio into a bounded delivery fraction by taking the square root and capping it at 1.0 with `amin1(1.0, rto ** .5)`. |
| 7. assign | Store the calculated delivery ratio in `ru_elem(ielem)%dr` using `rto .add. hz`, then set `ru_elem(ielem)%dr%flo = 1.`. |
| 8. if | If the element is marked `full` or `1`, assign a full delivery ratio by setting `ru_elem(ielem)%dr = 1. .add. hz`. |
| 9. loop | Finish the inner and outer loops after every routing-unit element has been processed. |
| 10. return | Return to the caller after the delivery-ratio state for all routing elements has been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, ru_def, ru_elem, hz` | `sp_ob%ru, ru_def(iru)%num_tot, ru_def(iru)%num(ii), ru_elem(ielem)%obtypno, ru_elem(ielem)%dr_name, ru_elem(ielem)%obtyp, ru_elem(ielem)%dr, ru_elem(ielem)%dr%flo` |
| [sym:hru_lte_module] | `hlt_db, hlt` | `hlt_db(ihru)%tc` |
| [sym:ru_module] | `ru_tc, iru, ru` |  |
| [sym:hru_module] | `tconc, ihru` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ihru` | When a routing-unit element has `ru_elem(ielem)%dr_name == "calc" .or. ru_elem(ielem)%dr_name == "0"` and `ru_elem(ielem)%obtyp == "hru"`, the routine loads `ihru` from `ru_elem(ielem)%obtypno`. | `ihru` is updated so the routine can reference the correct HRU or HRU-LTE timing record for the current routing element. It is overwritten for each processed element and is used immediately in the ratio calculation branches. |
| `ru_elem(ielem)%dr` | When `ru_elem(ielem)%dr_name` is `calc` or `0`, the routine assigns `ru_elem(ielem)%dr = rto .add. hz` after computing and bounding `rto`; when `dr_name` is `full` or `1`, it assigns `ru_elem(ielem)%dr = 1. .add. hz`. | `ru_elem(ielem)%dr` becomes the per-element delivery-ratio hydrograph output. It stores either a calculated fraction or a full unit ratio, depending on the routing element's delivery-ratio setting. |
| `ru_elem(ielem)%dr%flo` | Only in the calculated branch (`dr_name` is `calc` or `0`), immediately after `ru_elem(ielem)%dr` is set. | `ru_elem(ielem)%dr%flo` is forced to 1.0 so the resulting hydrograph output represents a unit flow magnitude alongside the calculated delivery ratio. The full-ratio branch does not assign `flo` here. |

## File I/O

<!-- facts:io -->


## Lineage

dr_ru was added in commit df07e3f with the initial delivery-ratio logic for routing-unit elements. Commit 39fabde only initialized the local counters `ii` and `ielem` and the temporary `rto`, and commit 2ee1889 made a trailing end-of-file formatting cleanup without changing behavior.

- df07e3f introduced the full nested-loop computation, the `calc`/`full` delivery-ratio branches, the object-type cases (`hru`, `hlt`, `sdc`, `ru`), and the writes to `ru_elem(ielem)%dr` and `ru_elem(ielem)%dr%flo`.
- 39fabde changed the local declarations of `ii`, `ielem`, and `rto` from uninitialized locals to explicitly initialized values.
- 2ee1889 made no behavioral change; it only adjusted the subroutine end line formatting.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'dr_ru' has no extracted documentation comment.
