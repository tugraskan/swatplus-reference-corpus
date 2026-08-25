---
kind: procedure
symbol: swr_percmain
title: swr_percmain
status: filled
source_hash: 9c2cb703663d2554
version_label: SWAT+ 62.0.0
locals:
  j: Loop index for the active HRU's soil layers and for the HRU selection itself once set
    to `ihru`.
  j1: Layer counter used to walk downward through soil layers during percolation, saturation,
    water-table, and tile-drain updates.
  ires: Stores `hru(j)%dbs%surf_stor`, a surface-storage flag used to decide whether irrigated
    water is included in the day’s seepage entering the soil profile.
  slug: Upper bound for the slug-routing loop; the routine chunks total seepage into a maximum
    increment before routing through layers.
  sep_left: Remaining seepage water still to be routed through the soil after each slug-sized
    increment has been processed.
  por_air: Temporary air-porosity factor used in the original water-table-depth calculation
    when `wtdn == 0`.
  d: Tile-depth reference above the profile bottom, computed from soil depth and septic/drain
    depth; used to decide whether tile drainage is allowed and in the water-table calculation.
  yy: Intermediate water-storage threshold used in the original shallow-water-table equation
    when `wtdn == 0`.
  xx: Normalized saturation ratio used to scale `wt_shall` in the original water-table-depth
    calculation.
  wat: Temporary water-table depth below the soil surface to the impervious layer, computed
    from the original drainmod-style equation.
  sw_del: Temporary soil-water deficit between current profile water and the previous water-table-based
    profile water in the modified `wtdn == 1` branch.
  wt_del: Incremental change in water-table depth derived from `sw_del` and layer water-table
    factor `vwt` in the modified `wtdn == 1` branch.
  sumqtile: Accumulator for tile flow removed from layer storages after `qtile` is computed,
    so the routine can subtract the flow from the correct layers.
uses:
  hru_module: '`hru_module` supplies the active HRU selection and the daily HRU water-balance
    state that this routine updates. The listed members provide the current HRU (`hru`, `ihru`),
    infiltration and septic inputs (`inflpcp`, `qstemm`, `i_sep`, `isep`), routing outputs
    (`sepday`, `sepbtm`, `latq`, `lyrtile`, `qtile`, `latlyr`, `sw_excess`, `wt_shall`, `sepcrktot`),
    and HRU properties that control routing choices such as surface storage, area, septic-layer
    index, and tile-drain enablement.'
  soil_module: '`soil_module` holds the per-layer storage and hydraulic properties that determine
    whether water is routed downward, sideways, or to tile drainage. `swr_percmain` reads
    layer count, field capacity, saturation, depth, temperature, and profile totals from `soil`
    and writes updated layer storage, layer percolation, lateral-flow storage, total soil
    water, and water-table state back into that same profile.'
  septic_data_module: '`septic_data_module` provides the septic-system operation flag that
    decides whether septic effluent is added to the biozone layer. Without `sep(isep)%opt`,
    the routine could not tell whether `qstemm` should be injected into the current layer.'
  hydrograph_module: '`hydrograph_module` contributes the daily irrigation applied to the
    HRU and the overland-flow hydrograph volume that becomes infiltration into the soil profile.
    `irrig(j)%applied` and `ht1%flo` are therefore part of the water entering this routine
    at the start of soil routing.'
  basin_module: '`basin_module` control codes switch major branches in the algorithm. `bsn_cc%gwflow`,
    `crk`, `wtdn`, and `tdrn` decide whether groundwater is added to soil, whether crack flow
    is routed, whether the original or modified water-table algorithm is used, and whether
    tile flow uses Drainmod equations or the older tile equation.'
---

<!-- facts:header -->

Master soil-percolation routing for the active HRU. It moves infiltrating water through soil layers, updates lateral flow, percolation, septic and tile-drain contributions, and recalculates soil-water storage and water-table depth.

## Bottom Line

`swr_percmain` is the HRU-level soil-water routing driver. It starts with infiltration and any groundwater or crack-flow contributions, then sends water through each soil layer in sequence, splitting excess storage into percolation, lateral flow, tile drainage, and bottom seepage according to basin control codes and soil/HRU settings.

It matters because it updates the daily water balance for the HRU: layer storage, total soil water, lateral flow, bottom seepage, tile flow, septic seepage, and water-table state are all recalculated here and then used by later runoff, groundwater, and drainage accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_control` calls this routine after it has assembled the day’s infiltration and irrigation inputs, including the overland-flow contribution in `ht1%flo` and `irrig(j)%applied` for subdaily steps. Its results feed later HRU and basin behavior such as saturation-excess accounting, tile drainage, lateral flow, bottom seepage, and groundwater coupling in the rest of the HRU control workflow.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and read control flags | The routine sets `j = ihru`, reads the current surface-storage flag from `hru(j)%dbs%surf_stor`, and, when groundwater flow is enabled, calls `gwflow_soil(j)` before any soil routing begins. |
| 2. Build the day’s seepage entering the profile | It initializes `sepday` from infiltration, irrigation, and routed overland flow, then subtracts crack-flow totals after calling `swr_percmacro` when crack flow is enabled. |
| 3. Route seepage in slug-sized chunks through all soil layers | The routine limits routing to a large `slug`, loops until all seepage is consumed, adds each slug to every soil layer, injects septic flow into the configured biozone layer when active, computes layer excess above field capacity, and if excess exists calls `swr_percmicro` to split it into downward percolation, lateral flow, and tile flow. It then subtracts those fluxes from layer storage and records summary totals in `sepbtm`, `latq`, `qtile`, `soil(j)%ly(j1)%flat`, and `soil(j)%ly(j1)%prk`. |
| 4. Correct saturation excess and recompute profile storage | After the layer loop, it calls `swr_satexcess` to redistribute any saturated-profile water, then rebuilds `soil(j)%sw` as the sum of all layer storages. |
| 5. Estimate water-table depth and shallow storage | The routine resets `qtile` and `wt_shall`, then computes the shallow water table using either the original drainmod-style equation when `bsn_cc%wtdn == 0` or the modified water-table update when `bsn_cc%wtdn == 1`, updating `soil(j)%wat_tbl`, `wt_shall`, and `soil(j)%swpwt` as needed. |
| 6. Compute tile drainage if tiles are active | When the HRU has tile drainage and a positive tile depth, the routine either calls `swr_drains` for Drainmod tile flow or calls `swr_origtile(d)` for the original tile equation, clipping negative `qtile` to zero in the original path. |
| 7. Remove tile water from layer storages | If tile flow was produced, the routine walks the soil layers again, subtracting `qtile` from water above field capacity until the tile flux is exhausted, then reduces `qtile` by any unmet remainder and prevents it from going negative. |
| 8. Refresh total soil-water storage and return | Finally, it recomputes `soil(j)%sw` from the updated layer storages and returns to the caller with all daily soil-water routing outputs updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, i_sep, qstemm, sepbtm, latq, ihru, inflpcp, isep, latlyr, lyrtile, sepcrktot, sepday, sw_excess, wt_shall, qtile` | `hru(j)%dbs%surf_stor, hru(j)%area_ha, hru(j)%lumv%sdr_dep, hru(j)%tiledrain` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(j1)%st, soil(j)%phys(j1)%fc, soil(j)%ly(j1)%flat, soil(j)%ly(j1)%prk, soil(j)%sw, soil(j)%zmx, soil(j)%phys(2)%tmp, soil(j)%sumfc, soil(j)%sumul, soil(j)%wat_tbl, soil(j)%phys(j1)%d, soil(j)%swpwt, soil(j)%ly(j1)%vwt` |
| [sym:septic_data_module] | `sep` | `sep(isep)%opt` |
| [sym:hydrograph_module] | `irrig, ht1` | `irrig(j)%applied, ht1%flo` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow, bsn_cc%crk, bsn_cc%wtdn, bsn_cc%tdrn` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sepday` | When `hru(j)%dbs%surf_stor` is zero, `sepday` includes irrigation (`irrig(j)%applied`) as well as infiltration and overland flow; otherwise irrigation is omitted. | `sepday` is the day’s incoming water routed into the soil profile. It changes here so the profile starts with the correct total water input before crack flow and layer routing are applied. |
| `soil(j)%phys(j1)%st` | Inside the layer loop, after adding `sepday` to `soil(j)%phys(j1)%st`, and again after `swr_percmicro` when excess water exists. | `soil(j)%phys(j1)%st` is the current stored water in each layer. It increases when incoming seepage enters the layer and decreases when percolation, lateral flow, and tile drainage are removed; this keeps layer storage consistent with the routed fluxes. |
| `sw_excess` | For any layer where `soil(j)%phys(j1)%st - soil(j)%phys(j1)%fc` is positive. | `sw_excess` captures the water above field capacity in the current layer. It is the trigger for micro-scale routing, so the routine computes it before deciding whether to call `swr_percmicro`. |
| `latlyr` | After the soil-layer routing loop, before water-table and tile calculations. | `latlyr` is reset to zero at the start of each layer and then updated by `swr_percmicro` when lateral subsurface flow is produced. The value matters because the caller subtracts it from layer storage and accumulates it into `latq(j)`. |
| `lyrtile` | After `swr_percmicro` sets tile drainage for the current layer, and before the next layer is processed. | `lyrtile` is the layer-scale tile-drain component. It is reset each layer, filled by the micro-routing routine when tile drainage is available, and accumulated into the HRU total `qtile`. |
| `sepbtm(j)` | When the current layer is the bottom soil layer and the micro-routing routine returns bottom percolation. | `sepbtm(j)` accumulates percolation exiting the bottom of the soil profile. This changes only for the deepest layer because bottom seepage is counted once at the profile outlet. |
| `latq(j)` | Whenever a layer produces lateral flow through `swr_percmicro`. | `latq(j)` is the HRU total of lateral subsurface flow. It is incremented by each layer’s `latlyr`, then clipped to zero if the accumulated total is numerically tiny. |
| `qtile` | Whenever a layer produces tile drainage through `swr_percmicro` or the tile-routing branch. | `qtile` accumulates the HRU’s daily tile-drain outflow. It is first built during layer routing, then possibly reduced after tile water is removed from layer storages, and finally clipped so small negative values do not persist. |
| `soil(j)%ly(j1)%flat` | When a layer receives any lateral flow or tile flow contribution from `swr_percmicro`. | `soil(j)%ly(j1)%flat` stores the layer’s combined lateral-flow storage for the day. It is updated to the sum of `latlyr` and `lyrtile` so the layer summary reflects the routed subsurface outflow. |
| `soil(j)%ly(j1)%prk` | When a layer receives downward percolation from `swr_percmicro`. | `soil(j)%ly(j1)%prk` accumulates the day’s percolation from that layer. It is increased by `sepday` each time water leaves the layer downward. |
| `soil(j)%sw` | After all layer routing has been completed and again after tile removal is applied. | `soil(j)%sw` is the total soil-profile water storage. It changes because the routine recomputes it from the updated layer storages so the profile total matches the routed fluxes. |
| `wt_shall` | When the original shallow-water-table branch (`bsn_cc%wtdn == 0`) finds `soil(j)%sw > soil(j)%sumfc`. | `wt_shall` is the shallow water table height above the bottom of the soil profile. In the original branch it is scaled from the profile’s excess water content, so it changes only when profile water exceeds field capacity and the water table is being estimated. |
| `soil(j)%wat_tbl` | When the modified water-table branch (`bsn_cc%wtdn == 1`) finds the current water table is above the current layer depth. | `soil(j)%wat_tbl` is updated by the modified drainmod water-table algorithm. It moves upward or downward according to the water-storage difference `sw_del` and layer factor `vwt`, then is capped at `soil(j)%zmx` if needed. |
| `if(soil(j)%wat_tbl>soil(j)%zmx)soil(j)%wat_tbl` | In the modified water-table branch, after `soil(j)%wat_tbl` is updated and compared with `soil(j)%zmx`. | The capped `soil(j)%wat_tbl` value prevents the water table from extending beyond the soil profile depth. This assignment keeps the stored water-table depth physically bounded by the profile bottom. |
| `soil(j)%swpwt` | After the modified water-table update when `soil(j)%swpwt` is refreshed from the current profile water. | `soil(j)%swpwt` stores the profile-water reference used by the next modified water-table update. It changes here so the next call can compare current soil water with the previous water-table-based reference. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.2.1 | Excess soil water above field capacity | $SW_{ly,excess}=SW_{ly}-FC_{ly}$ | sw_excess = st - fc when the layer exceeds field capacity. |
| 2:3.2.2 | Zero excess water below field capacity | $SW_{ly,excess}=0$ | The percolation branch is skipped when excess water is not positive. |
| 2:3.4.1 | Percolation reduction near impermeable depth | $w_{perc,btm}=w_{perc,btm,orig}*\frac{depth_{diff}}{depth_{diff}+exp[8.833-2.598*depth_{diff}]}$ | The routine uses a revised water-table and variable-water-table-factor formulation rather than the printed depth-difference sigmoid for bottom-layer percolation. |
| 2:3.4.2 | Perched water-table height | $h_{wtbl}=\frac{SW-FC}{(POR-FC)*(1-\phi_{air})}*depth_{imp}$ | Perched water table is estimated from storage above field capacity and layer porosity through a revised variable-water-table calculation rather than the exact printed formula. |
| 2:3.5.4 | Lateral flow only when SW > FC | $SW_{ly,excess}=SW_{ly}-FC_{ly}$ | Positive lateral-flow source water exists only when storage exceeds field capacity. |
| 2:3.5.5 | Zero lateral-flow source water when SW <= FC | $SW_{ly,excess}=0$ | No lateral-flow source water is created when excess water is not positive. |

## Lineage

`swr_percmain.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `swr_percmain.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_percmain' has no extracted documentation comment.
- source uncertainty: the identifier `ires` is assigned from `hru(j)%dbs%surf_stor`, which is documented as a surface-storage pointer in `hru_module`; its use here is limited to deciding whether irrigation is included in `sepday`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
