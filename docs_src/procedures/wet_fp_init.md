---
kind: procedure
symbol: wet_fp_init
title: wet_fp_init
status: filled
source_hash: b1a92c152a62801a
version_label: SWAT+ 62.0.0
locals:
  ihru: Loop index for HRUs within a reach floodplain. It starts at 0, then is reused to walk
    from 1 to `sd_ch(jrch)%fp%hru_tot` while accumulating each `wet(ihru)` contribution into
    `wet_stor(jrch)`.
uses:
  sd_channel_module: '`sd_channel_module` holds the per-reach floodplain metadata needed to
    know whether a reach has any HRUs in its floodplain and how many to sum. `sd_ch(jrch)%fp%hru_tot`
    is the gate and upper bound for the inner accumulation loop.'
  hydrograph_module: '`hydrograph_module` provides the channel-count driver `sp_ob%chandeg`
    plus the wetland storage variables `wet_stor`, `wet`, and `hz` that this routine initializes.
    Those shared hydrograph states are the outputs being seeded for later routing and storage
    calculations.'
---

<!-- facts:header -->

Initializes floodplain wetland storage for each swat-deg channel reach. It seeds each reach with the base wetland storage and adds HRU wetland volumes where the floodplain contains HRUs.

## Bottom Line

`wet_fp_init` prepares the starting floodplain wetland storage state for the simulation. It loops over all swat-deg channel reaches, sets each reach's `wet_stor` from the base wetland output `hz`, and, when a reach's floodplain contains HRUs, adds each HRU wetland contribution from `wet(ihru)` into that reach total.

This matters because `wet_stor` becomes the initialized wetland storage used by the hydrograph/wetland routing state for later channel and floodplain behavior. The routine does not read or write files; it only assembles in-memory storage totals from module state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at initialization, before routing begins, to build floodplain wetland storage totals for every swat-deg channel reach. The upstream setup that makes its inputs meaningful is the model initialization that populates `sp_ob%chandeg`, `sd_ch(jrch)%fp%hru_tot`, `hz`, and `wet(ihru)` in the shared modules. Later floodplain/wetland routing behavior depends on the resulting `wet_stor(jrch)` values as the starting wetland storage state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over reaches | Iterate through every swat-deg channel reach from 1 to `sp_ob%chandeg` so each reach gets its own initial wetland storage total. |
| 2. seed base storage | Set `wet_stor(jrch)` to `hz`, establishing the base wetland storage for the current reach before any HRU-specific additions. |
| 3. test floodplain HRUs | Check whether the reach floodplain contains any HRUs by testing `sd_ch(jrch)%fp%hru_tot > 0`; only nonempty floodplains need accumulation. |
| 4. sum HRU wetland volumes | For each HRU in the reach floodplain, add `wet(ihru)` into `wet_stor(jrch)` to build the reach's total initial wetland storage. |
| 5. continue or finish | Close the conditional and reach loop, then return after all reaches have been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(jrch)%fp%hru_tot` |
| [sym:hydrograph_module] | `sp_ob, wet_stor, wet, jrch, hz` | `sp_ob%chandeg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_stor(jrch)` | For every reach `jrch = 1, sp_ob%chandeg`, with additional HRU accumulation only when `sd_ch(jrch)%fp%hru_tot > 0`. | `wet_stor(jrch)` is initialized from the base wetland storage `hz` and, if the reach floodplain has HRUs, increased by each `wet(ihru)` contribution so the reach starts with total floodplain wetland storage. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three commits affecting `wet_fp_init`. df07e3f added the new subroutine with its initialization loop and accumulation logic. 94b6dec preserved the same logic but appears in the import history as the source was brought in verbatim. 39fabde only initialized local variable `ihru` to 0, and 889136d corrected the purpose comment typo from "intial" to "initial" without changing behavior.

- df07e3f introduced `wet_fp_init` and its loop that seeds `wet_stor(jrch)` from `hz` and adds `wet(ihru)` for each floodplain HRU.
- 39fabde changed the declaration of `ihru` from an uninitialized local integer to `integer :: ihru = 0`, affecting only its starting value before the loop.
- 889136d updated the subroutine purpose comment text only; runtime behavior was unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wet_fp_init' has no extracted documentation comment.
