---
kind: procedure
symbol: wallo_canal
title: wallo_canal
status: filled
source_hash: 26f05d20227541d0
version_label: SWAT+ 62.0.0
args:
  iwallo: Identifier for the active water-allocation object whose transfer record is being
    updated; it selects which `wallod_out(iwallo)` entry receives the computed canal outflow.
  itrn: Identifier for the transfer index within the chosen allocation object; it selects
    which `trn(itrn)` subrecord gets the canal outflow amount.
  ican: Identifier for the canal object being routed; it selects the canal storage, loss fraction,
    drawdown timing, and aquifer-loss connections used by this call.
locals:
  iaq: Loop index over the canal’s configured aquifer-loss destinations when seepage is being
    assigned to 1-D aquifers.
  iaqu_ob: Holds the aquifer object number taken from `canal(ican)%aqu_loss(iaq)%aqu_num`
    so the routine can update the matching aquifer state record.
  ic: Loop index over gwflow canal-to-cell division records to find the entries that belong
    to the current canal.
  cell_id: The gwflow cell number associated with a matched canal division record; used to
    update that cell’s groundwater state and hydrograph summaries.
  canal_loss_vol: Total canal seepage/loss volume computed from the canal loss fraction and
    canal outflow volume.
  aqu_loss_vol: The portion of canal loss assigned to one specific aquifer destination before
    converting to aquifer storage units.
  aqu_loss_mm: The aquifer loss expressed in millimeters over the target aquifer area, so
    it can be added to `aqu_d` storage and recharge terms.
  total_length: Accumulator for the total canal length across gwflow-connected division cells,
    used to split canal loss proportionally by length.
  cell_frac: The fraction of total canal loss assigned to one gwflow-connected cell based
    on its canal length share.
  cell_seep: The seepage volume assigned to a particular gwflow cell before updating that
    cell’s groundwater storage and summaries.
uses:
  water_allocation_module: '`water_allocation_module` holds the canal configuration, loss
    routing, and transfer-output records that this routine reads and writes. `canal(ican)`
    provides drawdown timing, loss fraction, and aquifer-loss destinations, while `wallod_out(iwallo)%trn(itrn)%trn_flo`
    receives the computed withdrawal/outflow amount.'
  hydrograph_module: '`hydrograph_module` provides the canal storage/outflow hydrographs and
    the receiving-object hydrograph accumulator that this routine updates. `canal_om_stor(ican)%flo`
    is the available canal water, `canal_om_out(ican)%flo` records how much leaves the canal,
    and `outflo_om` carries the post-loss flow onward.'
  constituent_mass_module: '`constituent_mass_module` matters because the canal transfer is
    not just a flow balance; the outflow object and remaining storage are the structures that
    carry routed water and any attached constituent mass bookkeeping through this procedure.'
  basin_module: '`basin_module` supplies the basin control flag `bsn_cc%gwflow`, which determines
    whether canal loss is handled through gwflow cell routing or through the 1-D aquifer fallback
    path.'
  aquifer_module: '`aquifer_module` provides the aquifer dynamic storage and recharge records
    that receive canal seepage when the routine falls back to 1-D aquifer accounting instead
    of gwflow cell updates.'
  gwflow_module: '`gwflow_module` matters because it supplies the gwflow activation flag,
    the canal-to-cell division table, and the per-cell groundwater state and summary arrays
    that receive canal seepage when gwflow routing is enabled.'
---

<!-- facts:header -->

Transfers water through a canal routing object, computing canal outflow, losses, and seepage/recharge to connected aquifer or gwflow cell states.

## Bottom Line

`wallo_canal` takes a canal storage object and a water-allocation transfer record, computes how much canal water is withdrawn, subtracts canal losses, and sends the remaining flow to the receiving object. It also routes the lost volume to groundwater accounting: either distributed across gwflow-connected cells or added to 1-D aquifer storage and recharge.

The routine matters because it links canal operation to both delivery accounting and subsurface water balance tracking. Its updates feed later hydrograph totals, groundwater storage summaries, and aquifer recharge bookkeeping.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallo_control` calls this routine after it has identified a canal-type water-allocation target and added the incoming transfer volume to `canal_om_stor(j)`. `wallo_canal` then computes canal withdrawal, losses, and groundwater recharge; later model behavior depends on the updated transfer output, remaining canal storage, and groundwater/aquifer summaries used by hydrology and balance reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute canal withdrawal | If the canal has no decision table (`dtbl == 'null'`), set the transfer outflow from the stored canal volume divided by the canal drawdown days; otherwise leave the decision-table branch as the alternate control path. |
| 2. Derive canal outflow and reduce storage | Convert the transfer withdrawal into canal outflow, store it in `canal_om_out(ican)`, and subtract that volume from `canal_om_stor(ican)` so canal storage reflects the removal. |
| 3. Compute canal loss and post-loss delivery | Calculate canal loss volume from the canal loss fraction and outflow, then compute `outflo_om` as the remaining flow after loss. |
| 4. Route loss only when positive | Proceed with groundwater or aquifer routing only if canal loss volume is greater than zero; if there is no loss, the routine returns after updating canal flow accounting. |
| 5. Use gwflow cell routing when active | When basin gwflow is enabled and canal gwflow routing is active, sum the lengths of all canal division cells for the current canal, then distribute loss across matching cells in proportion to length and update each active cell’s groundwater storage and hydrology summaries. |
| 6. Fall back to 1-D aquifer routing for canal loss | If there are no matching gwflow division cells, loop over the canal’s aquifer-loss list, convert each assigned loss volume to millimeters using the aquifer area, and add it to the target aquifer storage and recharge. |
| 7. Use 1-D aquifer routing when gwflow is inactive | When gwflow is not active, apply the same aquifer-loss loop directly to `aqu_d`, updating storage and recharge for each configured aquifer destination. |
| 8. Return to caller | Exit after canal flow, loss, and groundwater/aquifer accounting are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `canal, wallod_out` | `canal(ican)%dtbl, wallod_out(iwallo)%trn(itrn)%trn_flo, canal(ican)%ddown_days, canal(ican)%loss_fr, canal(ican)%num_aqu, canal(ican)%aqu_loss(iaq)%aqu_num, canal(ican)%aqu_loss(iaq)%frac` |
| [sym:hydrograph_module] | `canal_om_stor, canal_om_out, sp_ob, sp_ob1, outflo_om` | `canal_om_stor(ican)%flo, canal_om_out(ican)%flo, sp_ob%aqu, sp_ob1%aqu` |
| [sym:constituent_mass_module] | `constituent_mass_module symbols used for mass/quality routing through the canal outflow` | `outflo_om, canal_om_out(ican), canal_om_stor(ican)` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(iaqu_ob)%stor, aqu_d(iaqu_ob)%rchrg` |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_mo, gw_hyd_ss_yr` | `gw_state(cell_id)%stat, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%canl, gw_hyd_ss_mo(cell_id)%canl, gw_hyd_ss_yr(cell_id)%canl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wallod_out(iwallo)%trn(itrn)%trn_flo` | When `canal(ican)%dtbl == 'null'`, the transfer outflow is computed from canal storage and drawdown days. | `wallod_out(iwallo)%trn(itrn)%trn_flo` is set to the canal withdrawal rate for this transfer, providing the amount of water removed from the canal for routing and loss calculations. |
| `canal_om_out(ican)` | After the withdrawal is computed, regardless of whether the canal uses a decision table branch or the simple drawdown branch. | `canal_om_out(ican)` becomes the canal outflow hydrograph for this canal object, representing the amount leaving storage before loss is removed. |
| `canal_om_stor(ican)` | Immediately after `canal_om_out(ican)` is computed. | `canal_om_stor(ican)` is reduced by the outflow so the canal storage record reflects the remaining water after transfer. |
| `outflo_om` | Always after canal outflow is computed; it is the post-loss portion of `canal_om_out(ican)`. | `outflo_om` becomes the water delivered onward after subtracting the canal loss fraction, which is the flow available to the receiving object. |
| `gw_state(cell_id)%stor` | When canal loss is positive, gwflow is active, and a matched canal division cell has `gw_state(cell_id)%stat == 1`. | `gw_state(cell_id)%stor` increases by the share of canal seepage assigned to that active cell, adding canal seepage to groundwater storage. |
| `gw_hyd_ss(cell_id)%canl` | Under the same gwflow-active and active-cell condition used for `gw_state(cell_id)%stor`. | `gw_hyd_ss(cell_id)%canl` accumulates the canal seepage assigned to that cell for daily groundwater source/sink reporting. |
| `gw_hyd_ss_mo(cell_id)%canl` | Under the same gwflow-active and active-cell condition used for `gw_state(cell_id)%stor`. | `gw_hyd_ss_mo(cell_id)%canl` accumulates the same canal seepage in the monthly groundwater summary. |
| `gw_hyd_ss_yr(cell_id)%canl` | Under the same gwflow-active and active-cell condition used for `gw_state(cell_id)%stor`. | `gw_hyd_ss_yr(cell_id)%canl` accumulates the same canal seepage in the yearly groundwater summary. |
| `aqu_d(iaqu_ob)%stor` | When canal loss is positive and the selected aquifer number is valid, either in the gwflow fallback branch or when gwflow is inactive. | `aqu_d(iaqu_ob)%stor` increases by the seepage depth equivalent of the canal loss assigned to that aquifer, updating aquifer water storage. |
| `aqu_d(iaqu_ob)%rchrg` | When canal loss is positive and the selected aquifer number is valid, either in the gwflow fallback branch or when gwflow is inactive. | `aqu_d(iaqu_ob)%rchrg` increases by the same seepage depth equivalent so aquifer recharge accounting records canal loss as recharge. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The original 080211e commit added `wallo_canal` as a new routine that computed canal outflow from storage, applied loss, and routed the lost portion to aquifers. The later b78c4ea rework kept that basic purpose but expanded the routine substantially by adding gwflow integration, basin control gating, canal-to-cell distribution logic, groundwater state/summary updates, and a fallback path for 1-D aquifer recharge.

- 080211e introduced `wallo_canal` with canal outflow, loss, and simple aquifer-loss handling.
- b78c4ea added gwflow-aware canal seepage routing, including cell-length weighting, active-cell storage updates, and daily/monthly/yearly groundwater summaries, while retaining a 1-D aquifer fallback.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wallo_canal' has no extracted documentation comment.
- algorithm_steps revised: split the routing logic into explicit gwflow-active and 1-D aquifer fallback steps to match the source branches.
- Source is partly ambiguous because `constituent_mass_module` is used but no specific imported symbols were resolved from the packet; documentation therefore describes its role at the hydrograph/mass-routing level without naming extra members.
