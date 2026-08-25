---
kind: procedure
symbol: allocate_parms
title: allocate_parms
status: filled
source_hash: 3d73d8e596e35fb5
version_label: SWAT+ 62.0.0
locals:
  mhru: Local copy of the number of HRUs; set from `sp_ob%hru` and used as the allocation
    size for HRU-indexed arrays.
  mch: Local copy of the number of channels; set from `sp_ob%chan` and available as the channel
    count during allocation setup.
  mpc: Fixed plant-community array length; set to 20 and used to allocate the daily plant
    parameter arrays such as `uno3d`, `uapd`, `un2`, `up2`, `translt`, `par`, `htfac`, and
    `epmax`.
uses:
  hru_module: This module supplies the shared HRU-state arrays that `allocate_parms` creates
    and initializes. The routine sizes them from `mhru` and `mpc`, so the module's allocatable
    state must exist before later HRU, septic, drainage, sediment, and management routines
    can use it.
  time_module: The routine allocates several time-step-dependent arrays using `time%step`,
    including `hhqday`, `hhsurf_bs`, `hhsedy`, `ovrlnd_dt`, and `hhsurfq`. The time-step count
    therefore determines the second dimension of the subdaily storage that later routing and
    erosion code reads.
  hydrograph_module: The object counts in `sp_ob` provide the HRU and channel totals that
    drive allocation sizing. `allocate_parms` copies `sp_ob%hru` into `mhru` and `sp_ob%chan`
    into `mch` before allocating HRU-indexed arrays.
  constituent_mass_module: No candidate outside references were resolved to `constituent_mass_module`
    in the evidence packet, so its specific imported state cannot be identified here. The
    module is still relevant because it is use-associated in the subroutine and may provide
    types or shared state needed by the unseen parts of the procedure or later compilation
    context.
---

<!-- facts:header -->

Allocates and zero-initializes the shared HRU, plant, septic, drainage, salt/constituent, and tillage arrays used by SWAT+ before simulation begins.

## Bottom Line

allocate_parms is an initialization routine, not a calculation routine. It uses the current object counts in `sp_ob` and the time-step setting in `time%step` to allocate many shared arrays in `hru_module`, then fills key states with zero so later HRU, drainage, septic, and routing code starts from a clean baseline.

It also sets the model-wide `mhyd` flag to 1, sizes the plant-community arrays at `mpc = 20`, and calls `zero0`, `zero1`, `zero2`, and `zeroini` to reset additional shared state that other model components depend on after parameter loading.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at the start of HRU data reading, immediately after `hru_read` resets its counters and before any HRU input files are opened. `hru_read` prepares the spatial-object counts that `allocate_parms` uses, and the arrays initialized here are then consumed by the rest of the model setup and by later HRU, drainage, septic, tillage, and routing calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Capture shared dimensions and set the hydrograph count flag. | Declares local counters, then copies `sp_ob%hru` into `mhru`, `sp_ob%chan` into `mch`, and sets `mhyd = 1` as a model-wide hydrograph count baseline. |
| 2. Allocate drain and plant-community arrays. | Allocates the shared drainage scratch arrays and the plant-community arrays sized by `mhru` and `mpc`, then explicitly clears `epmax`. |
| 3. Allocate septic, management-output, and HRU bookkeeping arrays. | Allocates septic-system flags and storages, daily HQ output storage indexed by `time%step`, management summary arrays, and grazing counters. |
| 4. Allocate HRU process, drainage, and runoff arrays. | Allocates HRU state arrays for canopy, curve number, tile drainage accumulators, crop/soil timing, groundwater-linked fields, and related runoff variables. |
| 5. Allocate sediment, salt/constituent, and storage matrices. | Allocates sediment-yield arrays, tillage-related storage, salt and conservative-solute matrices, and multiple shared 2-D storage arrays used by gwflow, salt, and CS tracking. |
| 6. Allocate subdaily erosion and overland-flow arrays. | Allocates the subdaily storage arrays that depend on `mhru` and `time%step`, including subdaily surface-base, erosion, and runoff accumulators. |
| 7. Allocate and clear tillage-factor arrays. | Allocates the tillage-factor arrays, then sets their values to zero so decomposition-related logic starts from a neutral state. |
| 8. Reset additional shared module state through helper routines. | Calls `zero0`, `zero1`, `zero2`, and `zeroini` to finish initializing shared HRU state beyond the allocations handled directly in this routine. |
| 9. Return to the caller. | Leaves the subroutine after completing the allocation and initialization pass. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `wnan, ranrns_hru, uno3d, uapd, un2, up2, translt, par, htfac, epmax, cvm_com, percn, i_sep, sep_tsincefail, qstemm, bio_bod, biom, rbiom, fcoli, bz_perc, plqm, itb, sol_sumno3, sol_sumsolp, iseptic, grz_days, brt, canstor, cbodu, chl_a, cklsp, cn2, cnday, cumei, cumeira, cumrt, cumrai, dormhr, doxq, filterw, igrz, yr_skip, isweep, phusw, latno3, latq, ndeat, nplnt, orgn_con, orgp_con, ovrlnd, phubase, pplnt, qdr, gwsoilq, satexq, gwsoiln, gwsoilp, satexn, sstmaxd, sedminpa, sedminps, sedorgn, sedorgp, sedyld, sanyld, silyld, clayld, sagyld, lagyld, grayld, sed_con, sepbtm, smx, soln_con, solp_con, stmaxd` |  |
| [sym:time_module] | `time` | `time%step` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%chan` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mhyd` | `mhyd = 1` unconditionally near the start of the routine. | `mhyd` is forced to a one-based hydrograph count before other setup continues, providing a default model-wide hydrograph dimension used by later initialization and allocation logic. |
| `epmax` | `epmax` is allocated and then explicitly set to zero after `mpc = 20` and `allocate (epmax(mpc), source = 0.)`. | `epmax` becomes a zeroed daily plant-community parameter array, ensuring later plant-process calculations do not inherit stale values. |
| `tillage_switch` | `tillage_switch`, `tillage_depth`, `tillage_days`, and `tillage_factor` are allocated after the comment `!Tillage factor on SOM decomposition`. | These tillage-control arrays are created during initialization so decomposition and tillage logic have dedicated per-HRU storage before simulation begins. |
| `tillage_depth` | Immediately after the tillage arrays are allocated, `tillage_depth` is set to `0.` for all HRUs. | `tillage_depth` starts from a neutral zero depth, preventing any carry-over tillage effect until later management code assigns a real value. |
| `tillage_days` | Immediately after the tillage arrays are allocated, `tillage_days` is set to `0` for all HRUs. | `tillage_days` begins at zero elapsed days, which lets later tillage scheduling count from a clean initialization point. |
| `tillage_factor` | Immediately after the tillage arrays are allocated, `tillage_factor` is set to `0.` for all HRUs. | `tillage_factor` is cleared to a neutral value so soil organic matter decomposition adjustments can be computed later from initialized inputs. |

## File I/O

<!-- facts:io -->


## Lineage

`allocate_parms.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `72206bc` (2026-01-07, "Enhance water allocation with recall support and update soil cover calculations"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `allocate_parms.f90` are listed.

- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `d70017a` (2025-11-24) — code cleanup of stacked routines, unused routines, added 'end subroutine/function' to some codes to be consistent., remove warnings in code…
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `889136d` (2025-02-03) — Fix typos
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'allocate_parms' has no extracted documentation comment.
- algorithm_steps revised: expanded the original two coarse steps into nine source-backed steps to match the allocation and initialization sequence in the routine.
- outside_state[3] uncertain: the evidence packet shows `constituent_mass_module` is used, but no specific imported symbols from that module were resolved.
- lineage: no commits resolved for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
