---
kind: procedure
symbol: wallo_control
title: wallo_control
status: filled
source_hash: 719e93c2c3f4d2b5
version_label: SWAT+ 62.0.0
args:
  iwallo: Selects which water-allocation object in `wallo`, `wallod_out`, and `wal_omd` is
    processed.
locals:
  itrn: Current transfer-object index within `wallo(iwallo)%trn`; initialized from `wallo(iwallo)%trn_cur`
    and used to process one transfer record.
  iosrc: Declared but not used in the visible source; likely a leftover or placeholder.
  isrc: Source-object loop index used to walk each source in the current transfer and apply
    demand, withdrawal, and compensation logic.
  j: Receiving-object index taken from `wallo(iwallo)%trn(itrn)%rcv%num` and used to update
    the destination object.
  jj: Temporary integer passed into `salt_irrig` and `cs_irrig` to avoid compiler warnings;
    set equal to `itrn`.
  irec: Declared but not used in the visible source; likely a leftover or placeholder.
  iob: Object index used for channel transfer routing via `sd_ch(j)%obj_no` and `ob(iob)%trans`.
  dum: Declared but not used in the visible source; likely a leftover or placeholder.
  irr_mm: Irrigation depth in millimeters computed from withdrawn volume and HRU area for
    the `hru` receiving case.
  div_total: Declared but not used in the visible source; likely a leftover or placeholder.
  div_daily: Declared but not used in the visible source; likely a leftover or placeholder.
uses:
  water_allocation_module: Provides the transfer definitions, source/receiver metadata, and
    cumulative accounting records that this routine reads and updates.
---

<!-- facts:header -->

Routes one water-allocation transfer through demand, withdrawal, transfer, and receiving-object updates.

## Bottom Line

`wallo_control` processes the current transfer object for one water-allocation record. It computes demand, withdraws water from eligible sources, applies conveyance/transfer bookkeeping, and then updates the receiving object based on its type.

It also updates irrigation, reservoir, aquifer, wastewater, water-use, canal, and outside-receiving storage or hydrograph state, plus cumulative demand/withdrawal/unmet totals for the allocation object. That makes it the central dispatcher for water-allocation effects in this part of SWAT+.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by `command` and `sd_channel_control3` while iterating water-allocation objects. Those callers set up the active allocation index and, in the channel case, the current channel context before invoking this routine.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Reset transfer hydrographs | Clear the current allocation transfer hydrograph totals before processing the selected transfer. |
| 2. Select current transfer | Load the current transfer index from `trn_cur` so the routine works on one transfer object. |
| 3. Clear source outputs | Initialize each source output and source hydrograph record for the current transfer. |
| 4. Compute transfer demand | Call `wallo_demand` to compute the transfer demand, then copy that demand into the transfer object's unmet volume. |
| 5. Initialize source demand | Reset source outputs again and compute each source's share of the total transfer demand from its fraction. |
| 6. Withdraw available water | For each source with positive demand, call `wallo_withdraw` to take available water and reduce unmet demand. |
| 7. Apply compensation withdrawals | Make a second withdrawal pass for sources marked as compensating if unmet demand remains. |
| 8. Sum source withdrawals | Accumulate the total withdrawal across all sources for the current transfer. |
| 9. Transfer routed water | Call `wallo_transfer` to move the withdrawn water into the receiving-object hydrograph. |
| 10. Dispatch by receiver type | Choose the receiving-object branch based on the receiver type stored in the transfer record. |
| 11. Update receiving object | Apply receiver-specific updates for HRU, channel, reservoir, aquifer, wastewater treatment, water use, storage, canal, or outside receiving objects. |
| 12. Accumulate totals and advance | Add demand, withdrawal, and unmet totals to the allocation object, then advance `trn_cur` and wrap it to zero after the last transfer. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wallo, wallod_out, walloz, trn_m3` | `wallo(iwallo)%trn_cur, wallo(iwallo)%trn(itrn)%src_num, wallod_out(iwallo)%trn(itrn)%src(isrc), wallo(iwallo)%trn(itrn)%unmet_m3, wallod_out(iwallo)%trn(itrn)%trn_flo, wallod_out(iwallo)%trn(itrn)%src(:), wallod_out(iwallo)%trn(itrn)%src(isrc)%demand, wallo(iwallo)%trn(itrn)%src(isrc)%frac, wallo(iwallo)%trn(itrn)%src(isrc)%comp, wallo(iwallo)%trn(itrn)%withdr_tot, wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr, wallo(iwallo)%trn(itrn)%rcv%num, wallo(iwallo)%trn(itrn)%rcv%typ, wallo(iwallo)%trn(itrn)%irr_eff, wallo(iwallo)%trn(itrn)%surq, wallo(iwallo)%trn(itrn)%amount, wallo(iwallo)%name, wallo(iwallo)%tot%demand, wallo(iwallo)%tot%withdr, wallo(iwallo)%tot%unmet, wallo(iwallo)%trn_obs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wal_omd(iwallo)%trn(:)%h_tot` | At procedure start | Reset to `hz` for all transfer objects before the current transfer is processed. |
| `wallod_out(iwallo)%trn(itrn)%src(isrc)` | For each source before demand calculation | Reset to `walloz` so source-level demand/withdrawal bookkeeping starts clean. |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` | For each source before demand calculation | Reset to `hz` so source hydrograph output starts from zero before withdrawals are applied. |
| `wallo(iwallo)%trn(itrn)%unmet_m3` | After `wallo_demand` returns | Set equal to the computed transfer demand so later withdrawals can reduce unmet volume. |
| `wallod_out(iwallo)%trn(itrn)%src(:)` | For each source after demand is computed | Source outputs are cleared again before source demand and withdrawal accounting is filled in. |
| `wdraw_om_tot` | Before and during withdrawal processing | Reset to `hz` before withdrawals, then later accumulate organics into the total withdrawal hydrograph. |
| `wallod_out(iwallo)%trn(itrn)%src(isrc)%demand` | For each source after demand is computed | Set to the source fraction times the total transfer demand. |
| `trn_m3` | During withdrawal processing | Holds the current source demand or remaining unmet volume used to decide whether to call `wallo_withdraw`. |
| `wallo(iwallo)%trn(itrn)%withdr_tot` | After source withdrawals | Summed from all source withdrawals to represent total water actually withdrawn for the transfer. |
| `irrig(j)%applied` | When receiver type is `hru` and withdrawal is positive | Set to the applied irrigation depth derived from withdrawn volume, irrigation efficiency, and surface runoff fraction. |
| `irrig(j)%runoff` | When receiver type is `hru` and withdrawal is positive | Set to the runoff portion of the irrigation amount using the transfer's runoff fraction. |
| `irrig(j)%water` | When receiver type is `hru` and withdrawal is positive | Set to the transfer hydrograph for the irrigated HRU. |
| `pcom(j)%days_irr` | When receiver type is `hru` and withdrawal is positive | Reset to 1 to mark irrigation on the current day. |
| `hru(j)%irr_yr` | When receiver type is `hru` and withdrawal is positive | Incremented by the applied irrigation amount for yearly irrigation accounting. |
| `ob(iob)%trans` | When receiver type is `cha` | Set to the transferred hydrograph for the channel object identified by `sd_ch(j)%obj_no`. |
| `res(j)` | When receiver type is `res` | Incremented by the transferred hydrograph before optional reservoir control is called. |
| `res(j)` | When receiver type is `res` and the reservoir has no receiving total | Triggers `res_control` after the reservoir storage update so reservoir routing can be recomputed. |
| `aqu(j)` | When receiver type is `aqu` | Incremented by the transferred hydrograph for aquifer storage accounting. |
| `wtp_om_stor(j)` | When receiver type is `wtp` | Incremented by the transferred hydrograph before wastewater treatment outflow is computed. |
| `wuse_om_stor(j)` | When receiver type is `use` | Incremented by the transferred hydrograph before water-use outflow is computed. |
| `wtow_om_stor(j)` | When receiver type is `stor` | Incremented by the transferred hydrograph for water-tower storage accounting. |
| `canal_om_stor(j)` | When receiver type is `can` | Incremented by the transferred hydrograph before canal losses and outflow are computed. |
| `orcv_om(j)` | When receiver type is `orcv` | Incremented by the transferred hydrograph for outside receiving-object accounting. |
| `wallo(iwallo)%tot%demand` | After receiver processing | Accumulated with the current transfer demand. |
| `wallo(iwallo)%tot%withdr` | After receiver processing | Accumulated with the total withdrawal from all sources. |
| `wallo(iwallo)%tot%unmet` | After receiver processing | Accumulated with the remaining unmet demand. |
| `wallo(iwallo)%trn_cur` | After receiver processing | Advanced to the next transfer object, wrapping to zero after the last transfer. |

## File I/O

<!-- facts:io -->


## Lineage

`wallo_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 13 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wallo_control.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `0d74307` (2026-01-07) — Fixed Warnings, removed unused variable declarations and update external function references
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `815ec79` (2026-01-07) — water allocation updates
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists at unit 2612; the file name is not shown in the source, so its external meaning remains uncertain.
- `iosrc`, `irec`, `dum`, `div_total`, and `div_daily` are declared but not used in the visible source.
- `reservoir_module` is used via `use` but no concrete outside references were resolved from the context packet.
- No Git lineage commits were resolved for this source span.
- warning: missing_doc: Procedure 'wallo_control' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
