---
kind: procedure
symbol: zero1
title: zero1
status: filled
source_hash: 932acdba34b0db52
version_label: SWAT+ 62.0.0
locals:
  sep_opt: Local septic option flag used here as a hardcoded initialization value; it is set
    to 1 during setup, but it is not a module state and is not referenced after assignment
    in this routine.
  filt_w: Temporary local placeholder for filter width initialization; set to 0 and not used
    later in this subroutine.
  grwat_veg: Temporary local placeholder for groundwater/vegetation-related initialization;
    set to 0 and not used later in this subroutine.
  plq_rt: Temporary local septic/plaque-related parameter initialized to 0; not used elsewhere
    in this subroutine.
  pr_w: Temporary local parameter for probability of wet day after dry day in a month; initialized
    to 0 and not used further here.
  rchrg: Temporary local recharge value; set to 0 to clear any prior value before the routine
    exits.
  sedst: Temporary local sediment storage value; initialized to 0 as part of the reset sequence.
  sol_wp: Temporary local solids-on-impervious-area water-parameter placeholder; set to 0
    and not used later in this subroutine.
  thalf: Temporary local buildup half-time parameter; initialized to 0 even though the comment
    documents its intended meaning.
  tnconc: Temporary local total nitrogen concentration placeholder for impervious-area wash-off;
    set to 0 and not used later.
  tno3conc: Temporary local nitrate concentration placeholder for impervious-area wash-off;
    set to 0 and not used later.
  tpconc: Temporary local total phosphorus concentration placeholder for impervious-area wash-off;
    set to 0 and not used later.
  urbcoef: Temporary local urban wash-off coefficient placeholder; set to 0 and not used later
    in this routine.
  urbcn2: Temporary local curve-number placeholder for impervious areas; set to 0 and not
    used later in this routine.
  vp: Temporary local placeholder initialized to 0; it has no observable use in this subroutine
    beyond being reset.
uses:
  hru_module: '`hru_module` supplies the allocatable HRU state that `zero1` resets in place.
    These arrays and scalars matter because downstream HRU and septic/urban processes read
    them after `allocate_parms` finishes initialization.'
---

<!-- facts:header -->

Initializes selected HRU and septic/urban-related state variables to zero or default starting values. It is a setup routine called during parameter allocation before simulation begins.

## Bottom Line

`zero1` is a reset routine: it zeroes a set of HRU-module state arrays and a few related flags so the model starts from a clean baseline. The routine is not driven by inputs; instead, it uses `hru_module` state that was already allocated by the caller.

The states it touches include septic, vegetation, sediment, and urban wash-off variables such as `bio_bod`, `fcoli`, `biom`, `rbiom`, `bz_perc`, `plqm`, `qstemm`, `i_sep`, `sep_tsincefail`, `sweepeff`, `swtrg`, `t_ov`, `tconc`, `usle_cfac`, `usle_eifac`, and `wfsh`. Those values are then available for later HRU calculations after initialization.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`zero1` runs during global parameter setup after `allocate_parms` has initialized other model parameters and before the HRU module begins simulation use. In the caller workflow, `allocate_parms` calls `zero0`, then `zero1`, then `zero2`, then `zeroini`, so this routine contributes to the initial state that later HRU process calculations depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare local initialization placeholders and import HRU state | The routine brings in the HRU-module variables it will reset and defines local placeholder scalars for septic, urban, sediment, and recharge parameters. These locals are only used to hold default zero values during setup. |
| 2. Begin septic-related state reset | The routine clears septic and related biological state in `hru_module`, setting `bio_bod`, `fcoli`, `biom`, `rbiom`, `bz_perc`, `plqm`, `qstemm`, `i_sep`, and `sep_tsincefail` to their starting values. It also assigns `sep_opt = 1` as the septic option default used for later logic. |
| 3. Reset local filter and groundwater placeholders | It sets local placeholders `filt_w` and `grwat_veg` to zero, then clears `plqm` and `plq_rt` again as part of the septic initialization block. These assignments ensure no prior values carry into the model start. |
| 4. Reset recharge, sediment, and related local parameters | The routine zeros `pr_w`, `rchrg`, `sedst`, and `sol_wp`, clearing month wet-day probability, recharge, sediment storage, and solids buildup state used by related HRU processes. |
| 5. Reset urban runoff and impervious-surface variables | It clears the urban and impervious-surface states `sweepeff`, `swtrg`, `t_ov`, `tconc`, `thalf`, `tnconc`, `tno3conc`, `tpconc`, `urbcoef`, `urbcn2`, `usle_cfac`, and `usle_eifac`. This prepares urban wash-off and erosion-related state for later HRU computations. |
| 6. Finish septic/vegetation placeholder reset and return | The routine zeroes `vp` and `wfsh`, then returns to the caller without invoking any other routines. At this point the HRU module initialization values are ready for subsequent model setup and simulation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `bio_bod, biom, bz_perc, fcoli, i_sep, plqm, qstemm, rbiom, sep_tsincefail, sweepeff, swtrg, t_ov, tconc, usle_cfac, usle_eifac, wfsh` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bio_bod` | Always, during the initialization call from `allocate_parms`. | `bio_bod` is reset to 0 so septic biochemical oxygen demand starts from a clean initial condition instead of carrying over stale state. |
| `fcoli` | Always, during the initialization call from `allocate_parms`. | `fcoli` is reset to 0 so fecal coliform loading begins from no prior stored mass or concentration. |
| `biom` | Always, during the initialization call from `allocate_parms`. | `biom` is reset to 0 so biomass-related septic state starts empty before any HRU processes run. |
| `rbiom` | Always, during the initialization call from `allocate_parms`. | `rbiom` is reset to 0 so residual biomass does not persist into the first simulation step. |
| `bz_perc` | Always, during the initialization call from `allocate_parms`. | `bz_perc` is reset to 0 so the associated zone-percolation state starts from baseline before process updates. |
| `plqm` | Always, during the initialization call from `allocate_parms`. | `plqm` is reset to 0 so the plaque/mass state does not carry over into the initialized HRU state. |
| `qstemm` | Always, during the initialization call from `allocate_parms`. | `qstemm` is reset to 0 so the septic stem flow or related quantity starts from no stored amount. |
| `i_sep` | Always, during the initialization call from `allocate_parms`. | `i_sep` is reset to 0 as the septic system index/flag default for later logic. |
| `sep_tsincefail` | Always, during the initialization call from `allocate_parms`. | `sep_tsincefail` is reset to 0 so failure timing starts fresh with no elapsed time accumulated. |
| `sweepeff` | Always, during the initialization call from `allocate_parms`. | `sweepeff` is reset to 0 so no sweep efficiency is assumed before the HRU sweep process is configured. |
| `swtrg` | Always, during the initialization call from `allocate_parms`. | `swtrg` is reset to 0 so sweep trigger state begins inactive. |
| `t_ov` | Always, during the initialization call from `allocate_parms`. | `t_ov` is reset to 0 so overland travel-time state starts from no prior contribution. |
| `tconc` | Always, during the initialization call from `allocate_parms`. | `tconc` is reset to 0 so time-of-concentration state starts from a blank initial value. |
| `usle_cfac` | Always, during the initialization call from `allocate_parms`. | `usle_cfac` is reset to 0 so the USLE crop-management factor starts from a neutral baseline before erosion calculations. |
| `usle_eifac` | Always, during the initialization call from `allocate_parms`. | `usle_eifac` is reset to 0 so the USLE erosivity-impact factor starts from a blank initial value. |
| `wfsh` | Always, during the initialization call from `allocate_parms`. | `wfsh` is reset to 0 so the associated watershed/HRU state starts without a carried-over value. |

## File I/O

<!-- facts:io -->


## Lineage

`zero1` was added in `df07e3f` as a new initialization subroutine that zeroed a set of HRU-module states and local placeholders. Later `39fabde` changed the declarations so the local placeholders were initialized directly to zero, but did not alter the reset assignments. `889136d` only corrected a comment typo, and `bd18ad4` added an `external` declaration and changed the closing form to `end subroutine zero1` without changing the initialization logic.

- `df07e3f` introduced the routine and its initial zeroing behavior for the HRU septic/urban state variables.
- `39fabde` moved the local scalar initializations into the declarations, reducing reliance on later assignment for those placeholders while leaving the runtime reset behavior unchanged.
- `bd18ad4` updated the subroutine footer to an explicit `end subroutine zero1` and added `external :: soil_nutcarb_write`; the executable zeroing sequence stayed the same.
- `889136d` corrected the `urbcn2` comment text from "moisture condiction" to "moisture conduction" without changing behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'zero1' has no extracted documentation comment.
