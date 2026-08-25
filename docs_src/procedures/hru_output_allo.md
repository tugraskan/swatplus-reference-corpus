---
kind: procedure
symbol: hru_output_allo
title: hru_output_allo
status: filled
source_hash: 063b8c05f1832576
version_label: SWAT+ 62.0.0
locals:
  ihru: Loop index over HRUs when allocating nested per-HRU balance arrays and initializing
    their component records.
  mhru: Holds the total number of HRUs from `sp_ob%hru` and is used as the first-dimension
    size for the HRU output arrays.
  isalt: Loop index over salt ions when allocating and zeroing the salt balance arrays.
  ics: Loop index over constituent species when allocating and zeroing the general constituent
    balance arrays.
uses:
  output_landscape_module: '`sp_ob%hru` supplies the number of HRUs to allocate against; without
    it, the routine cannot size the HRU output arrays or loop over each HRU''s nested balance
    records.'
  maximum_data_module: '`db_mx%lsu_out` sets the number of LSU-level output objects for the
    carbon accumulators, so this routine allocates the LSU carbon arrays only when that output
    space exists.'
  hydrograph_module: '`sp_ob%hru` is the HRU-count driver for the HRU pesticide balance arrays,
    so it determines both the outer array size and the nested per-HRU pesticide component
    allocation.'
  constituent_mass_module: '`cs_db%num_pests`, `cs_db%num_paths`, `cs_db%num_salts`, and `cs_db%num_cs`
    determine which constituent output families are active and how many component slots each
    family needs for allocation and initialization.'
  output_ls_pesticide_module: These pesticide balance records hold the HRU-level and basin-level
    pesticide output state that this routine allocates; their component arrays must exist
    before later pesticide output accumulation can store mass balances.
  output_ls_pathogen_module: These pathogen balance records provide the HRU-level and basin-level
    pathogen output state that this routine allocates so later accumulation routines can record
    pathogen fluxes by HRU and by simulation period.
  salt_module: The salt balance records define the HRU salt output state that this routine
    allocates and zeros; the named fields are the flux and storage components the model later
    accumulates for daily, monthly, yearly, and average annual reporting.
  cs_module: These constituent-balance records are the HRU-level general constituent output
    state that this routine allocates so later routines can accumulate the per-constituent
    mass fluxes and storage terms.
  carbon_module: '`carbon_module` is imported because this procedure also allocates carbon-related
    output arrays; the module defines the carbon balance types and storage used by those arrays,
    even though no resolved outside references were listed in the packet.'
---

<!-- facts:header -->

Allocates and initializes HRU-level output balance arrays for water, pesticides, pathogens, salts, constituents, and carbon. It sizes those arrays from the current HRU and LSU counts so later output routines can accumulate daily, monthly, yearly, and average annual summaries.

## Bottom Line

`hru_output_allo` is the one-time setup routine for HRU output accounting. It uses the current object counts to allocate the output-balance arrays that other routines fill during the simulation.

For salts, constituents, pesticides, pathogens, and carbon-related outputs, it also initializes many per-HRU and per-component balance fields to zero so later accumulation starts from a clean state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU initialization inside `proc_hru`, after HRU objects are allocated/read and before later initialization steps that depend on output storage being ready. Its results are used by the model's output accumulation path so daily, monthly, yearly, and average annual balances can be written later without allocating arrays at runtime.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the current HRU count and size the base HRU output arrays. | The routine copies `sp_ob%hru` into `mhru`, then allocates the core HRU output arrays for water balance, nitrogen balance, landscape output, carbon output, and related summaries with one slot per HRU. |
| 2. Allocate LSU-level carbon arrays when LSU output is enabled. | If `db_mx%lsu_out` is positive, the routine allocates the LSU carbon accumulator arrays (`lsc_*`, `lrc_*`, `lpc_*`, `lscf_*`) using that LSU output count. |
| 3. Allocate pesticide output balances when pesticides are simulated. | When `cs_db%num_pests > 0`, the routine allocates basin and HRU pesticide-balance containers and then allocates each HRU's `pest` array to the number of pesticide species. |
| 4. Allocate pathogen output balances when pathogens are simulated. | When `cs_db%num_paths > 0`, the routine allocates the HRU pathogen balance containers and then allocates each HRU's `path` array to the number of pathogen species. |
| 5. Allocate salt output balances and zero monthly, yearly, and annual salt fields. | When `cs_db%num_salts > 0`, the routine allocates the HRU salt containers and then, for each HRU and salt species, sets the monthly, yearly, and average annual salt flux/storage fields to zero, including the dissolved-mass term for the first salt entry. |
| 6. Allocate general constituent output balances and zero their fields. | When `cs_db%num_cs > 0`, the routine allocates the HRU constituent containers and then zeroes the monthly, yearly, and average annual fields for each constituent species, including soil, runoff, sediment, lateral flow, irrigation, rainfall, deposition, fertilizer, uptake, reaction, sorption, concentration, and sorbed-borne terms. |
| 7. Return after output storage is ready. | The subroutine exits once all needed output arrays have been allocated and initialized for later output accumulation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_landscape_module] | `sp_ob` | `sp_ob%hru` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%num_paths, cs_db%num_salts, cs_db%num_cs` |
| [sym:output_ls_pesticide_module] | `bpestb_d, bpestb_m, bpestb_y, bpestb_a, hpestb_d, hpestb_m, hpestb_y, hpestb_a` | `bpestb_d%pest, bpestb_m%pest, bpestb_y%pest, bpestb_a%pest, hpestb_d(ihru)%pest, hpestb_m(ihru)%pest, hpestb_y(ihru)%pest, hpestb_a(ihru)%pest` |
| [sym:output_ls_pathogen_module] | `hpath_bal, hpathb_m, hpathb_y, hpathb_a` | `hpath_bal(ihru)%path, hpathb_m(ihru)%path, hpathb_y(ihru)%path, hpathb_a(ihru)%path` |
| [sym:salt_module] | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a` | `hsaltb_d(ihru)%salt, hsaltb_m(ihru)%salt, hsaltb_y(ihru)%salt, hsaltb_a(ihru)%salt, hsaltb_m(ihru)%salt(isalt)%soil, hsaltb_m(ihru)%salt(isalt)%surq, hsaltb_m(ihru)%salt(isalt)%latq, hsaltb_m(ihru)%salt(isalt)%urbq, hsaltb_m(ihru)%salt(isalt)%wetq, hsaltb_m(ihru)%salt(isalt)%tile, hsaltb_m(ihru)%salt(isalt)%perc, hsaltb_m(ihru)%salt(isalt)%wtsp, hsaltb_m(ihru)%salt(isalt)%irsw, hsaltb_m(ihru)%salt(isalt)%irgw, hsaltb_m(ihru)%salt(isalt)%irwo, hsaltb_m(ihru)%salt(isalt)%rain, hsaltb_m(ihru)%salt(isalt)%dryd, hsaltb_m(ihru)%salt(isalt)%road, hsaltb_m(ihru)%salt(isalt)%fert, hsaltb_m(ihru)%salt(isalt)%amnd, hsaltb_m(ihru)%salt(isalt)%uptk, hsaltb_y(ihru)%salt(isalt)%soil, hsaltb_y(ihru)%salt(isalt)%surq, hsaltb_y(ihru)%salt(isalt)%latq, hsaltb_y(ihru)%salt(isalt)%urbq, hsaltb_y(ihru)%salt(isalt)%wetq, hsaltb_y(ihru)%salt(isalt)%tile, hsaltb_y(ihru)%salt(isalt)%perc, hsaltb_y(ihru)%salt(isalt)%wtsp, hsaltb_y(ihru)%salt(isalt)%irsw, hsaltb_y(ihru)%salt(isalt)%irgw, hsaltb_y(ihru)%salt(isalt)%irwo, hsaltb_y(ihru)%salt(isalt)%rain, hsaltb_y(ihru)%salt(isalt)%dryd, hsaltb_y(ihru)%salt(isalt)%road, hsaltb_y(ihru)%salt(isalt)%fert, hsaltb_y(ihru)%salt(isalt)%amnd, hsaltb_y(ihru)%salt(isalt)%uptk, hsaltb_a(ihru)%salt(isalt)%soil, hsaltb_a(ihru)%salt(isalt)%surq, hsaltb_a(ihru)%salt(isalt)%latq, hsaltb_a(ihru)%salt(isalt)%urbq, hsaltb_a(ihru)%salt(isalt)%wetq, hsaltb_a(ihru)%salt(isalt)%tile, hsaltb_a(ihru)%salt(isalt)%perc, hsaltb_a(ihru)%salt(isalt)%wtsp, hsaltb_a(ihru)%salt(isalt)%irsw, hsaltb_a(ihru)%salt(isalt)%irgw, hsaltb_a(ihru)%salt(isalt)%irwo, hsaltb_a(ihru)%salt(isalt)%rain, hsaltb_a(ihru)%salt(isalt)%dryd, hsaltb_a(ihru)%salt(isalt)%road, hsaltb_a(ihru)%salt(isalt)%fert, hsaltb_a(ihru)%salt(isalt)%amnd, hsaltb_a(ihru)%salt(isalt)%uptk, hsaltb_m(ihru)%salt(1)%diss, hsaltb_y(ihru)%salt(1)%diss, hsaltb_a(ihru)%salt(1)%diss` |
| [sym:cs_module] | `hcsb_d, hcsb_m, hcsb_y, hcsb_a` | `hcsb_d(ihru)%cs, hcsb_m(ihru)%cs, hcsb_y(ihru)%cs, hcsb_a(ihru)%cs` |
| [sym:carbon_module] | `No candidate outside references were resolved to `carbon_module` in the provided context.` | `No resolved carbon-module components were provided in the context packet.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hsaltb_m(ihru)%salt(isalt)%soil` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly salt soil-store field is explicitly reset to zero so later salt-output accumulation can start from a clean monthly total for each HRU and salt ion. |
| `hsaltb_m(ihru)%salt(isalt)%surq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly surface-runoff salt flux field is reset to zero so monthly salt runoff totals can be accumulated later for each HRU and salt ion. |
| `hsaltb_m(ihru)%salt(isalt)%latq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly lateral-flow salt flux field is reset to zero so later monthly reporting can accumulate HRU salt export through lateral flow. |
| `hsaltb_m(ihru)%salt(isalt)%urbq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly urban-runoff salt flux field is reset to zero so later HRU urban salt runoff can be accumulated separately. |
| `hsaltb_m(ihru)%salt(isalt)%wetq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly wetland-runoff salt flux field is reset to zero so later wetland-related salt export can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%tile` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly tile-flow salt flux field is reset to zero so later tile drainage salt export can be accumulated for each HRU and salt ion. |
| `hsaltb_m(ihru)%salt(isalt)%perc` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly percolation salt flux field is reset to zero so later deep-leaching salt losses can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%wtsp` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly wetland-seepage salt flux field is reset to zero so later seepage contributions to the soil profile can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%irsw` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly surface-water irrigation salt input field is reset to zero so later irrigation additions can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%irgw` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly groundwater irrigation salt input field is reset to zero so later irrigation additions from groundwater can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%irwo` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly outside-watershed irrigation salt input field is reset to zero so later imported irrigation salt can be accumulated separately. |
| `hsaltb_m(ihru)%salt(isalt)%rain` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly rainfall salt input field is reset to zero so later wet-deposition via rainfall can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%dryd` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly dry-deposition salt input field is reset to zero so later atmospheric dry deposition can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%road` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly road-salt input field is reset to zero so later road-salt additions can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%fert` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly fertilizer salt input field is reset to zero so later fertilizer-based salt additions can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%amnd` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly amendment salt input field is reset to zero so later amendment-based salt additions can be accumulated. |
| `hsaltb_m(ihru)%salt(isalt)%uptk` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This monthly crop-uptake salt flux field is reset to zero so later root uptake losses can be accumulated. |
| `hsaltb_y(ihru)%salt(isalt)%soil` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly salt soil-store field is reset to zero so annual salt output can be accumulated independently from the monthly totals. |
| `hsaltb_y(ihru)%salt(isalt)%surq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly surface-runoff salt flux field is reset to zero so annual runoff totals can be accumulated separately. |
| `hsaltb_y(ihru)%salt(isalt)%latq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly lateral-flow salt flux field is reset to zero so annual lateral export can be accumulated separately. |
| `hsaltb_y(ihru)%salt(isalt)%urbq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly urban-runoff salt flux field is reset to zero so annual urban-salt export can be accumulated separately. |
| `hsaltb_y(ihru)%salt(isalt)%wetq` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly wetland-runoff salt flux field is reset to zero so annual wetland-salt export can be accumulated separately. |
| `hsaltb_y(ihru)%salt(isalt)%tile` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly tile-flow salt flux field is reset to zero so annual tile-drainage export can be accumulated separately. |
| `hsaltb_y(ihru)%salt(isalt)%perc` | When `cs_db%num_salts > 0`, during the per-HRU/per-salt initialization loop. | This yearly percolation salt flux field is reset to zero so annual deep-leaching loss can be accumulated separately. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `hru_output_allo`. The original file was introduced in `df07e3f` with HRU output allocations for water, nutrient, pesticide, pathogen, salt, CS, and carbon balances. `39fabde` initialized the loop counters `ihru`, `mhru`, `isalt`, and `ics` to zero but did not change the allocation logic. `bc7755a` added `use maximum_data_module`, removed the obsolete `hgl_*` allocations, added LSU-level carbon allocations sized by `db_mx%lsu_out`, and kept the salt and constituent zero-initialization logic intact.

- `df07e3f` created the subroutine and established the full allocation/zeroing workflow for HRU output balances across salts and other constituents.
- `39fabde` changed only local variable initialization, setting `ihru`, `mhru`, `isalt`, and `ics` to zero at declaration; the routine behavior otherwise remained the same.
- `bc7755a` expanded the routine to depend on `maximum_data_module`, removed unused `hgl_*` arrays, and added LSU-level carbon output allocations (`lsc_*`, `lrc_*`, `lpc_*`, `lscf_*`) controlled by `db_mx%lsu_out`.
- `bc7755a` did not alter the salt/CS initialization loops, so the existing zeroing of `hsaltb_*` and `hcsb_*` fields remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_output_allo' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into seven initialization phases to match the visible control flow and keep each step tied to real line ranges.
- No resolved outside references were provided for `output_landscape_module` or `carbon_module` in the packet; their roles are inferred only from the import list and the allocation logic shown in the source.
