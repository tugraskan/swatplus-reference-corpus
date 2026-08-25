---
kind: procedure
symbol: rls_routesurf
title: rls_routesurf
status: filled
source_hash: f47d65355062ad67
version_label: SWAT+ 62.0.0
args:
  iob: '`iob` selects the object-connectivity record in `ob(iob)` whose incoming surface and
    tile hydrographs supply the runon water and sediment for this HRU.'
  tile_fr_surf: '`tile_fr_surf` is the fraction of incoming tile flow that is treated as surface
    runon and added to `ls_overq`.'
locals:
  j: '`j` is the current HRU index, copied from `ihru`, and used to pull HRU-specific area,
    field, and topography values.'
  ifield: '`ifield` stores the field database index from `hru(j)%dbs%field`; it is assigned
    but not used later in this routine.'
  sed: '`sed` holds sediment load normalized by HRU area so it can be compared against the
    transport capacity.'
  trancap: '`trancap` holds the sediment transport capacity computed from deposition coefficient,
    cover factor, runoff, slope, and field width.'
uses:
  hru_module: '`hru_module` provides the active HRU pointer and the HRU properties needed
    to scale routing by area and erosion potential: the current HRU index `ihru`, area `hru(j)%area_ha`,
    deposition coefficient `hru(j)%topo%dep_co`, slope `hru(j)%topo%slope`, field width `hru(j)%field%wid`,
    and the cover factor array `usle_cfac` used in the sediment-capacity formula. It also
    owns the shared outputs `ls_overq` and `precip_eff` that this routine updates.'
  hydrograph_module: '`hydrograph_module` supplies the incoming hydrograph object `ob(iob)`
    and the routing outputs `ht1` and `ht2`. The routine reads surface runoff, tile runoff,
    and surface sediment from `ob(iob)` and writes the split sediment amounts into `ht1%sed`
    and `ht2%sed`.'
  climate_module: '`climate_module` matters because the routine adds surface runon into `w%ts(:)`
    when the model is running with more than one subdaily time step, so the weather time-series
    used for runoff generation reflects the added water.'
---

<!-- facts:header -->

Routes surface runon and tile inflow across the current HRU, updates effective precipitation, and partitions sediment into deposition and outflow.

## Bottom Line

`rls_routesurf` handles surface routing for a downstream HRU/landscape position. It combines incoming surface runoff and a fraction of tile flow into `ls_overq`, adds that water to cumulative effective precipitation, and, when the model is running subdaily, distributes the added water across the weather time-step array `w%ts(:)`.

It also computes how much sediment can be transported across the landscape using HRU topography and field properties. That calculation splits incoming sediment into deposited sediment (`ht1%sed`) and routed sediment (`ht2%sed`) for later deposition/routing bookkeeping.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_control` calls this routine during HRU-to-HRU routing when an incoming surface flow exists and the destination is not a wetland. `hru_control` has already selected the current object (`icmd`/`iob`), determined that surface runon should be routed across the HRU, and passed in `tile_fr_surf`; later runoff and sediment calculations depend on the updated `ls_overq`, `precip_eff`, `w%ts(:)`, `ht1%sed`, and `ht2%sed` values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU context | Copy the active HRU index from `ihru` into `j` and read the field pointer from `hru(j)%dbs%field`. This anchors the routine to the current HRU’s geometry and database links. |
| 2. compute runon depth | Compute `ls_overq` as incoming surface runoff plus the tile-flow contribution scaled by `tile_fr_surf` and HRU area, then add that depth to `precip_eff`. |
| 3. distribute subdaily runon | If the model time step is subdaily (`time%step > 1`), add the runon depth evenly across the weather substeps in `w%ts(:)` by dividing by `time%step`. |
| 4. calculate sediment load | Convert incoming surface sediment to a per-area load by dividing `ob(iob)%hin_sur%sed` by the current HRU area. |
| 5. calculate transport capacity | Compute sediment transport capacity from deposition coefficient, USLE cover factor, runon depth, slope, and field width. |
| 6. split sediment routed vs. deposited | Compare sediment load to transport capacity. If load exceeds capacity, store the excess in `ht1%sed` as deposition and the capacity-limited amount in `ht2%sed`; otherwise route all sediment in `ht2%sed` and set `ht1%sed` to zero. |
| 7. finish | Return to the caller after the runon and sediment bookkeeping updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, usle_cfac, ihru, ls_overq, precip_eff` | `hru(j)%dbs%field, hru(j)%area_ha, hru(j)%topo%dep_co, hru(j)%topo%slope, hru(j)%field%wid` |
| [sym:hydrograph_module] | `ob, ht1, ht2, ts` | `ob(iob)%hin_sur%flo, ob(iob)%hin_til%flo, ob(iob)%hin_sur%sed, ht1%sed, ht2%sed` |
| [sym:climate_module] | `w` | `w%ts(:)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ls_overq` | Always, after `ls_overq` is computed at line 32. | `ls_overq` is overwritten with the current HRU’s routed surface runon depth, combining surface inflow and the tile-flow share; later sediment capacity uses this value, and runoff accounting elsewhere can rely on the updated runon depth. |
| `precip_eff` | Always, immediately after `ls_overq` is computed. | `precip_eff` is increased by the routed surface runon depth so the HRU’s effective precipitation includes incoming water for runoff calculations. |
| `w%ts(:)` | Only when `time%step > 1`. | `w%ts(:)` is incremented by an even share of `ls_overq` across the subdaily precipitation sequence so the weather time series reflects the added runon during multi-step days. |
| `ht1%sed` | When `sed > trancap`. | `ht1%sed` is assigned the excess sediment above transport capacity, representing deposition that will be carried as deposition output. |
| `ht2%sed` | When `sed <= trancap`. | `ht2%sed` is assigned the sediment amount that is actually routed onward; in this branch it equals all incoming sediment, because capacity is sufficient. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved. The initial addition of `rls_routesurf` in `df07e3f` introduced the routine with the runon, precipitation, and sediment-routing logic. Commit `94b6dec` preserved the same algorithm while carrying forward the upstream source import. Commit `39fabde` only changed local variable declarations by initializing `j`, `ifield`, `sed`, and `trancap`; the routing formulas and control flow were unchanged.

- df07e3f added the entire procedure, including runon accumulation into `ls_overq`, the `w%ts(:)` update for subdaily steps, and the sediment split into `ht1%sed` and `ht2%sed`.
- 39fabde changed only local initialization defaults for `j`, `ifield`, `sed`, and `trancap`; it did not change the routing equations or branching behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rls_routesurf' has no extracted documentation comment.
