---
kind: procedure
symbol: define_unit_elements
title: define_unit_elements
status: filled
source_hash: d4804e6805826004
version_label: SWAT+ 62.0.0
args:
  num_elem: Number of defining-unit entries available in `elem_cnt`; this is the loop bound
    that determines how many groups or ranges the routine scans.
  ielem: Returns the total number of element IDs generated in `defunit_num`, so callers can
    allocate their target `num` array to the correct length.
locals:
  ii: Main scan index through `elem_cnt`; it advances one entry for a single group or skips
    ahead by two entries when a negative endpoint indicates a range.
  ie1: Holds the starting element number for the current defining-unit segment, taken from
    `elem_cnt(ii)` or `elem_cnt(ii-1)` depending on position.
  ie2: Holds the end marker for the current segment; if it is negative, the code uses `abs(ie2)`
    as the inclusive upper bound of a range.
  ie: Loop counter used to expand each inclusive element range and to write each generated
    element ID into `defunit_num`.
uses:
  hydrograph_module: '`hydrograph_module` supplies the temporary input list `elem_cnt` and
    the output buffer `defunit_num`; this routine converts one into the other, so both arrays
    are central to its behavior.'
---

<!-- facts:header -->

Builds the list of defining-unit element numbers for one grouped object and returns its total length.

## Bottom Line

`define_unit_elements` reads the element breakpoints already stored in `hydrograph_module%elem_cnt`, counts how many element IDs belong to the requested group, and allocates `defunit_num` to hold that exact sequence. The routine handles both single-element groups and multi-element ranges, including the special last-group case, so later readers can copy a clean per-object element list.

After the count pass, it fills `defunit_num` with the element numbers in order and then removes the temporary `elem_cnt` array. Callers use the returned `ielem` value to size their own `num` arrays, then copy `defunit_num` into those persistent structures before deallocating the temporary result.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after a reader has parsed a record that includes `nspu` and the raw `elem_cnt` values, and before that reader allocates and fills its persistent `num` array. The length and contents of `defunit_num` determine later per-object element membership used by aquifer, channel, LSU, HRU, reservoir, and calibration-region setup.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counting state and scan the defining-unit list once to determine output length. | The routine resets `ielem` and walks `elem_cnt` from the first entry, using each pair of markers to decide whether the current defining unit is a single element or an inclusive range. For a positive next marker it counts one element; for a negative next marker it counts every element from the start marker through the absolute end marker. The last input entry is handled as a special case so the scan can finish cleanly at the end of the list. |
| 2. Allocate the output array and reset the counters for the fill pass. | After the total length is known, the routine allocates `defunit_num(ielem)` and initializes it to zero, then clears `ielem` and restarts the scan from the first input entry. |
| 3. Fill a single-element final group or expand the final range into explicit element IDs. | When the scan reaches the last defining-unit entry, the routine either writes the single final element directly or loops from the stored start value to the absolute end value, appending each element number to `defunit_num`. |
| 4. Fill each nonfinal group by copying a single element or expanding a range. | For every nonfinal pair in `elem_cnt`, the routine either records the start element as one output value or iterates through an inclusive range and appends each element number in order, advancing `ii` by one or two positions accordingly. |
| 5. Release the temporary input list and return to the caller. | The routine deallocates the temporary `elem_cnt` array once `defunit_num` has been built, then returns with `ielem` holding the final count and `defunit_num` holding the explicit membership list. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `elem_cnt, defunit_num` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `defunit_num(1)` | When the current item is the last defining-unit entry and it represents a single element, or when the last entry starts an inclusive range. | `defunit_num(1)` is set during the special one-item final case to hold the only element ID in the group; this seeds the output list when the whole record contains just one defining unit. |
| `defunit_num(ielem)` | When the routine is filling the last defining-unit entry as a single element or expanding its inclusive range. | `defunit_num(ielem)` receives each explicit element number produced from the final group, so the output array ends with the last expanded member of the defining-unit list. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The initial addition in 94b6dec created `define_unit_elements` with the two-pass expansion logic, the `hydrograph_module` dependency, and the final `deallocate (elem_cnt)`. Commit 39fabde preserved the logic but initialized the local counters (`ii`, `ie1`, `ie2`, `ie`) to zero and changed the allocation of `defunit_num` to `allocate (..., source = 0)`.

- 39fabde: made the local scan variables default to zero on declaration and zero-filled `defunit_num` at allocation time, reducing uninitialized-state risk without changing the expansion algorithm.
- 94b6dec: introduced the procedure and its two-pass conversion from `elem_cnt` markers to an explicit `defunit_num` list, including cleanup of the temporary input array.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'define_unit_elements' has no extracted documentation comment.
