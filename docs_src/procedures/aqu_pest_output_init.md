---
kind: procedure
symbol: aqu_pest_output_init
title: aqu_pest_output_init
status: filled
source_hash: 1df94399d65527b8
version_label: SWAT+ 62.0.0
locals:
  ipest: Loop index for the pesticide being initialized within each aquifer and basin-wide
    output array. It runs from 1 to `cs_db%num_pests`.
  iaq: Loop index for the aquifer being initialized. It runs from 1 to `sp_ob%aqu`.
uses:
  aqu_pesticide_module: This module owns the aquifer pesticide output containers whose `stor_init`
    fields are written here. The routine clears the basin-level output records and loads each
    aquifer-level record so later pesticide reporting can start from the correct initial mass
    values.
  constituent_mass_module: This module supplies the number of pesticide constituents to loop
    over and the aquifer constituent-mass array that provides the source values copied into
    output initialization. Without it, the routine would not know how many pesticide slots
    exist or what mass to place into each aquifer record.
  hydrograph_module: This module provides the spatial object counts used to size the aquifer
    loop. `sp_ob%aqu` tells the routine how many aquifer objects exist in the current simulation,
    so each one can have its output state initialized.
---

<!-- facts:header -->

Initializes aquifer pesticide output storage for daily, monthly, yearly, and average-annual reporting. It zeroes basin-wide pesticide accumulators and copies each aquifer's current pesticide mass into the corresponding output structures.

## Bottom Line

This routine prepares pesticide output state before the model starts printing aquifer reports. For every aquifer and every simulated pesticide, it resets the basin-wide start values to zero, then fills the aquifer output structures from `cs_aqu(iaq)%pest(ipest)` and accumulates those same masses into the basin-wide totals.

The result is a consistent set of `stor_init` values for daily, monthly, yearly, and average-annual aquifer pesticide output. Those values are used later by the output/reporting code as the starting point for tracking and printing pesticide mass in aquifers and at the basin scale.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during time-control setup, after the model has already decided whether initial water/output state needs to be prepared and before the daily simulation loop begins. `time_control` calls it once when `pco%sw_init` is still "n" and the simulation has advanced past skipped years; its outputs then feed the aquifer pesticide print/checking state used by later output routines throughout the run.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop aquifers | Iterate over each aquifer object from 1 to `sp_ob%aqu` so the routine can initialize pesticide output for every aquifer in the simulation. |
| 2. zero basin outputs | For the current pass through the aquifer loop, iterate over every simulated pesticide and reset the basin-wide daily, monthly, yearly, and average-annual `stor_init` fields to 0.0 before adding aquifer contributions. |
| 3. load aquifer outputs and accumulate basin totals | For each pesticide, copy the current aquifer pesticide mass from `cs_aqu(iaq)%pest(ipest)` into the daily, monthly, yearly, and average-annual aquifer output records, then add that same mass into the basin-wide accumulators. |
| 4. return | Exit after all aquifers and pesticides have been initialized, leaving the output state ready for later reporting. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:aqu_pesticide_module] | `baqupst_d, baqupst_m, baqupst_y, baqupst_a, aqupst_d, aqupst_m, aqupst_y, aqupst_a` | `baqupst_d%pest(ipest)%stor_init, baqupst_m%pest(ipest)%stor_init, baqupst_y%pest(ipest)%stor_init, baqupst_a%pest(ipest)%stor_init, aqupst_d(iaq)%pest(ipest)%stor_init, aqupst_m(iaq)%pest(ipest)%stor_init, aqupst_y(iaq)%pest(ipest)%stor_init, aqupst_a(iaq)%pest(ipest)%stor_init` |
| [sym:constituent_mass_module] | `cs_db, cs_aqu` | `cs_db%num_pests, cs_aqu(iaq)%pest(ipest)` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%aqu` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `baqupst_d%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Resets the basin daily pesticide start value to zero before the current aquifer's mass is added, so basin output can be accumulated cleanly across aquifers. |
| `baqupst_m%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Resets the basin monthly pesticide start value to zero before the current aquifer's mass is added, so monthly reporting starts from a clean accumulator. |
| `baqupst_y%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Resets the basin yearly pesticide start value to zero before the current aquifer's mass is added, so yearly reporting starts from a clean accumulator. |
| `baqupst_a%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Resets the basin average-annual pesticide start value to zero before the current aquifer's mass is added, so long-term reporting starts from a clean accumulator. |
| `aqupst_d(iaq)%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Stores the current aquifer pesticide mass as the initial daily output value for aquifer `iaq`, making the daily aquifer report start from the current constituent mass. |
| `aqupst_m(iaq)%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Stores the current aquifer pesticide mass as the initial monthly output value for aquifer `iaq`, making the monthly aquifer report start from the current constituent mass. |
| `aqupst_y(iaq)%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Stores the current aquifer pesticide mass as the initial yearly output value for aquifer `iaq`, making the yearly aquifer report start from the current constituent mass. |
| `aqupst_a(iaq)%pest(ipest)%stor_init` | Inside the aquifer loop, for every `ipest = 1, cs_db%num_pests`. | Stores the current aquifer pesticide mass as the initial average-annual output value for aquifer `iaq`, making the long-term aquifer report start from the current constituent mass. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in commit `df07e3f` as a new initializer for aquifer pesticide output. Commit `39fabde` changed only the local loop variable declarations to initialize `ipest` and `iaq` to 0. Commit `889136d` corrected comments from "beggining"/"inital" to "beginning"/"initial" without changing logic.

- df07e3f introduced the full `aqu_pest_output_init` routine with the two nested loops that zero basin pesticide output, copy aquifer pesticide masses into the output arrays, and accumulate basin totals.
- 39fabde changed the local integer declarations to initialize `ipest` and `iaq` at declaration time; this is a code-style/defensive initialization change with no change to the routine's loop behavior.
- 889136d corrected comment text only and did not alter executable behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aqu_pest_output_init' has no extracted documentation comment.
