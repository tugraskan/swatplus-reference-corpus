---
kind: procedure
symbol: search
title: search
status: filled
source_hash: 598a153f66e8e9bd
version_label: SWAT+ 62.0.0
args:
  sch: Character array of candidate names to search through; the array is expected to be sorted
    so the routine can narrow the search interval by lexicographic comparison.
  max: Upper bound on the search list and the initial right-hand end of the search interval;
    it sets `nl = max` before the loop starts.
  cfind: The 50-character name to find in `sch`; every comparison in the routine is made against
    this key.
  iseq: Output index that receives the position of the matching entry in `sch` when a comparison
    succeeds.
locals:
  nf: Left-hand search bound. It starts at 1 and moves right when the midpoint is lower than
    `cfind`.
  int: Loop counter that limits the binary-search refinement to 25 passes.
  nn: Current midpoint index computed from `nf` and `nl` on each pass; it is the candidate
    position tested against `cfind`.
  nl: Right-hand search bound. It starts from `max` and moves left when the midpoint is greater
    than `cfind`.
---

<!-- facts:header -->

Binary-searches a sorted character array for a matching 50-character key and returns its index.

## Bottom Line

`search` looks up `cfind` in the sorted character array `sch` and stores the matching position in `iseq`. It is used as a fast crosswalk helper when the model needs to convert external names such as weather-gage or station identifiers into internal numeric indices.

The routine checks the middle of the current range, then narrows the search bounds toward the target. If the target is found, it returns immediately; otherwise it stops after a fixed number of iterations without assigning a new index.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`search` runs wherever SWAT+ needs to translate a string name into a numbered array position. `cli_staread` prepares the weather-station crosswalks and calls it to resolve weather-generator, precipitation, and temperature gage names; `hyd_read_connect` prepares station-name lists and calls it to resolve station crosswalks. The resulting indices feed later object setup and file associations, so downstream model behavior depends on the returned `iseq` value being correct.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize search bounds | Set the left bound to the first element and the right bound to the last valid element in the array, establishing the initial interval to search. |
| 2. iterate with a fixed limit | Repeat up to 25 times, recomputing the midpoint of the current interval on each pass. |
| 3. check for a two-item interval | If only two entries remain between the bounds, test the right entry and then the left entry directly; if either matches the key, store that index in `iseq` and return immediately. |
| 4. test the midpoint for an exact match | Compare the midpoint entry to the key and return the midpoint index when they are equal. |
| 5. move the right bound leftward | If the midpoint entry sorts after the key, move the right bound down to the midpoint so the next pass searches the lower half. |
| 6. move the left bound rightward | If the midpoint entry sorts before the key, move the left bound up to the midpoint so the next pass searches the upper half. |
| 7. exit without a match | After the loop finishes, return to the caller even if no match was found; in that case `iseq` is left unchanged by this routine. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The procedure was introduced in 94b6dec as a new `search` subroutine implementing a bounded binary search over a sorted character array. Commit 39fabde did not change the search logic, but it initialized the local bounds variables `nf`, `nn`, and `nl` at declaration time while keeping the same comparisons, midpoint calculation, and return behavior.

- 94b6dec added the full `search` routine: initial bounds setup, midpoint comparison loop, boundary checks for two remaining entries, and early return on a match.
- 39fabde only changed variable initialization for `nf`, `nn`, and `nl`; it did not alter the search algorithm or its returned index behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'search' has no extracted documentation comment.
