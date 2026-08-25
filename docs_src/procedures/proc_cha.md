---
kind: procedure
symbol: proc_cha
title: proc_cha
status: filled
source_hash: b7b9facebac4cb3e
version_label: SWAT+ 62.0.0
locals:
  irch: Loop index for channel reaches when calling ch_initial; starts at 0 and runs from
    1 to sp_ob%chan.
  idat: Holds the selected channel properties index from ob(i)%props before passing it to
    ch_initial.
  i: Temporary object index computed from sp_ob1%chan + irch - 1 to locate the current channel
    connectivity record in ob.
uses:
  hydrograph_module: Provides the shared spatial-object counts and connectivity records needed
    to loop over channels, map each channel reach to its properties record, and size the initialization
    work.
---

<!-- facts:header -->

Initializes channel-related input tables and derived routing state for SWAT+.

## Bottom Line

proc_cha is the channel setup routine. It reads the channel initialization, hydrology, sediment, nutrient, and SWAT-DEG linkage inputs, then builds derived channel routing state before the simulation starts.

It also initializes per-channel travel-time coefficients, channel initial sediment textures, overbank/surface links, and concentration-time values so later routing and water-quality routines can use a fully prepared channel state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel setup before routing begins. It is the place where SWAT+ loads channel tables and prepares derived channel state that later channel routing, sediment, nutrient, floodplain, and concentration-time routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read channel inputs | Read the channel initialization, hydrology, sediment, nutrient, and SWAT-DEG input tables needed for channel setup. |
| 2. Initialize aquifer linkage | Set up aquifer-to-channel linkage state for geomorphic baseflow routing. |
| 3. Compute routing coefficients | Loop over all channel objects and compute travel-time coefficients with ch_ttcoef. |
| 4. Initialize channel reaches | Loop over all channel reaches, map each reach to its properties record, and call ch_initial to set bank and bed sediment defaults. |
| 5. Load overbank links | Read overbank linkage data and build the channel-surface/floodplain links used by SWAT-DEG channel routing. |
| 6. Initialize concentration time | Finalize setup by initializing concentration-time values before returning to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob, ich` | `sp_ob%chan, sp_ob1%chan, ob(i)%props` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `shared channel setup state` | After channel input tables are read | Loads and sizes the channel initialization, hydrology, sediment, nutrient, and SWAT-DEG linkage data used by later channel routines. |
| `routing coefficients and channel reach state` | For each channel object in sp_ob%chan | Computes ch_vel routing coefficients and initializes each reach's sediment texture and critical shear-stress defaults. |
| `floodplain linkage state` | After overbank and surface-link setup | Populates channel-surface and floodplain link lists for later SWAT-DEG routing. |
| `concentration-time state` | Before return | Initializes concentration-time values so downstream runoff and routing calculations can use them. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_cha.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_cha.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_cha' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
