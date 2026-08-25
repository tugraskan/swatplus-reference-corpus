---
kind: procedure
symbol: res_objects
title: res_objects
status: filled
source_hash: ad6402c1731f5f63
version_label: SWAT+ 62.0.0
locals:
  iob1: First object number that is a reservoir (start of loop).
  iob2: Last object number that is a reservoir (end of loop).
  ires: Running counter into res_ob array; equals the number of reservoir objects processed
    so far.
  i: Loop variable that iterates over object numbers from iob1 to iob2.
uses:
  reservoir_module: The routine fills the res_ob array so that reservoir-specific routines
    can access each reservoir’s global object number and database property record.
  hydrograph_module: Provides the location and count of reservoir objects and the property
    pointer that must be copied into res_ob.
---

<!-- facts:header -->

Initialises the res_ob array with object numbers and property indices for every reservoir object in the project.

## Bottom Line

res_objects maps each reservoir object appearing in the global object-connectivity list (ob) to a compact reservoir array (res_ob).

Using counters stored in hydrograph_module, it determines the first and last object numbers that belong to reservoirs, then walks through that range while counting up a local reservoir index (ires).  For every reservoir encountered it copies:

• the global object number (ob index) into res_ob(ires)%ob, and

• the pointer to that object’s properties record (ob(i)%props) into res_ob(ires)%props.

The routine performs no calculations beyond these assignments and makes no external calls; it simply prepares look-up information that later reservoir routines (reading parameters, initialisation, daily routing, etc.) rely on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

proc_res allocates memory for reservoirs (res_allo) and then immediately calls res_objects to populate the res_ob array before any reservoir data are read (res_read, res_initial) or simulated.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. find first index | Set iob1 to the first object number that represents a reservoir. |
| 2. find last index | Compute iob2 as the last reservoir object number using the count stored in sp_ob%res. |
| 3. reset counter | Initialise ires so that the res_ob array is filled from position 1 upward. |
| 4. loop over reservoirs | For each object number i between iob1 and iob2 increment ires, copy i to res_ob(ires)%ob, and copy ob(i)%props to res_ob(ires)%props. |
| 5. return | Exit the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_module] | `res_ob` | `res_ob(ires)%ob, res_ob(ires)%props` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob` | `sp_ob1%res, sp_ob%res, ob(i)%props` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `res_ob(ires)%ob` | Inside loop for each reservoir object | Assigned the global object number so downstream code can relate res_ob entries back to the connectivity list. |
| `res_ob(ires)%props` | Inside loop for each reservoir object | Stores the property record index for this reservoir so parameter reading routines know which res.dat row to use. |

## File I/O

<!-- facts:io -->


## Lineage

Git history shows three commits (39fabde, 94b6dec, df07e3f) touching the source tree after initial import; their subjects mention general variable initialisation and source code updates, but none explicitly reference res_objects.f90, so the precise impact on this routine is unclear.

## Review Notes

- algorithm_steps revised: expanded from 2 to 5 steps to reflect every distinct operation present in the source code.
- No direct file I/O occurs in this subroutine.
- Procedure has no inline documentation comments.
