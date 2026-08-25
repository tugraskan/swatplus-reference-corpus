---
kind: procedure
symbol: wallo_withdraw
title: wallo_withdraw
status: filled
source_hash: c55245da6c5f8b06
version_label: SWAT+ 62.0.0
args:
  iwallo: '`iwallo` selects which water-allocation object in `wallo` and `wallod_out` is being
    processed, so the routine updates the chosen transfer object''s source accounting and
    hydrograph totals.'
  itrn: '`itrn` selects which transfer object within `wallo(iwallo)` is being processed, so
    the routine applies withdrawal logic to that demand object and its source list.'
  isrc: '`isrc` selects which source entry within `wallo(iwallo)%trn(itrn)%src` is being evaluated,
    so the routine computes withdrawal for that one source and writes its outputs.'
locals:
  j: '`j` is the object index for the specific source being processed; it is taken from `wallo(iwallo)%trn(itrn)%src(isrc)%num`
    and used to index treatment/use/storage/canal/reservoir/aquifer source arrays.'
  iom: '`iom` is the recall or export-coefficient index for outside-basin sources; it is set
    from either `wallo(iwallo)%trn(itrn)%osrc(isrc)%daymoyr` or `wallo(iwallo)%trn(itrn)%osrc(isrc)%aa`
    and used to select the external hydrograph source.'
  res_min: '`res_min` stores the minimum reservoir volume allowed to remain after withdrawal,
    computed from the source-specific withdrawal limit and `res_ob(j)%pvol`.'
  res_vol: '`res_vol` stores the reservoir volume remaining after a candidate withdrawal,
    and is compared with `res_min` to decide whether the withdrawal is allowed.'
  can_min: '`can_min` stores the minimum canal volume allowed to remain after withdrawal,
    computed from the source withdrawal limit and current canal storage.'
  can_vol: '`can_vol` stores the canal volume remaining after a candidate withdrawal, and
    is compared with `can_min` to decide whether the withdrawal is allowed.'
  cha_min: '`cha_min` stores the minimum allowable channel flow left in the stream after diversion,
    computed from the source withdrawal limit and converted from m3/s to m3/d.'
  cha_div: '`cha_div` stores how much flow can be diverted from the channel without violating
    the minimum flow constraint.'
  rto: '`rto` is the proportional take fraction used to scale a hydrograph by the portion
    withdrawn from storage, channel, canal, or reservoir sources.'
  avail: '`avail` is the aquifer water volume available for withdrawal, computed from aquifer
    surface area and current storage.'
  extracted: '`extracted` accumulates the groundwater volume actually allocated by `gwflow_pump_allo`
    when the gwflow module is active.'
  trn_unmet: '`trn_unmet` accumulates the groundwater demand that could not be met by `gwflow_pump_allo`
    when the gwflow module is active.'
  withdraw: '`withdraw` is a local accumulator for withdrawn volume, but in the shown source
    it is never assigned before being added into the output totals.'
  unmet: '`unmet` is a local accumulator for unmet demand, but in the shown source it is never
    assigned before being added into the output totals.'
uses:
  water_allocation_module: The water-allocation module provides the transfer object tree being
    processed, the per-source demand and withdrawal output records being filled, the outside-basin
    source selectors, and the total unmet demand field that this routine reduces after each
    source is handled.
  hydrograph_module: The hydrograph module defines the flow/mass containers that this routine
    copies, scales, and accumulates so each source contributes the correct water, nitrate,
    and soluble phosphorus hydrograph to the transfer object total.
  aquifer_module: The aquifer module supplies aquifer area and dynamic storage/mass states,
    which are needed to calculate available groundwater and to reduce water, nitrate, and
    phosphorus stores when aquifer water is withdrawn.
  reservoir_module: The reservoir module provides the principal-spillway volume used to turn
    a reservoir withdrawal limit into a minimum remaining reservoir volume.
  time_module: The time module supplies the current day, month, and sequential year so outside-basin
    recall hydrographs can be selected at the correct timestep granularity.
  recall_module: The recall module supplies the recall database metadata that tells this routine
    whether an outside-basin source is indexed by day, month, or year.
  basin_module: The basin control codes determine whether the gwflow groundwater module is
    active, which changes the aquifer branch from direct aquifer storage withdrawal to gwflow-based
    pumping allocation.
---

<!-- facts:header -->

Routes a requested transfer demand to the correct source type and computes how much water, flow, and constituent mass can actually be withdrawn. It also records unmet demand and updates the transfer hydrology for downstream reporting.

## Bottom Line

`wallo_withdraw` is the source-allocation worker for one transfer source within one water-allocation object. Given `iwallo`, `itrn`, and `isrc`, it looks up the source type, computes the source-specific withdrawal available under current conditions, and stores the resulting withdrawal, unmet demand, and hydrograph mass/flow updates in the allocation output structures.

It matters because later water-allocation accounting depends on its results: it updates source-level withdrawal/unmet totals, subtracts the withdrawn amount from the transfer object's remaining unmet volume, and accumulates source hydrographs for outside-basin recalls, treatment/use/storage/canal/reservoir/aquifer sources, and unlimited sources. For aquifer sources it also branches on whether the gwflow module is active and, if so, delegates pumping allocation to `gwflow_pump_allo`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallo_withdraw` runs inside `wallo_control` after that routine has identified a transfer object with positive demand and set `trn_m3` to the current source demand. `wallo_control` loops over every source for the transfer object and calls this routine once per source; the results then feed later compensation logic and the transfer object's remaining unmet-demand accounting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the source hydrograph state. | The routine starts by copying `hz` into `wdraw_om`, giving the source a zeroed hydrologic contribution before any case-specific withdrawal is computed. |
| 2. Dispatch on the source type. | A `select case` chooses the withdrawal algorithm based on `wallo(iwallo)%trn(itrn)%src(isrc)%typ`. |
| 3. Process outside-basin recall sources. | For `osrc`, the routine selects the correct recall timestep (`day`, `mo`, or `yr`) using `recall_db(iom)%org_min%tstep`, pulls the hydrograph from `recall(iom)%hd`, and either withdraws the full source or only the requested transfer demand while scaling the hydrograph accordingly. |
| 4. Process annual outside sources. | For `osrc_a`, the routine uses the export-coefficient hydrograph `exco(iom)`, then applies the same full-versus-partial withdrawal logic and scales the source hydrograph to the demand actually met. |
| 5. Process water treatment plant sources. | For `wtp`, the routine takes the treatment plant outflow hydrograph from `wtp_om_out(j)` and records it as a fully met withdrawal with no unmet demand. |
| 6. Process water use effluent sources. | For `use`, the routine takes the effluent outflow hydrograph from `wuse_om_out(j)` and records it as a fully met withdrawal with no unmet demand. |
| 7. Process water tower storage sources. | For `stor`, the routine compares storage against the requested transfer, withdraws either the full demand or all available storage, scales the source hydrograph by the withdrawal ratio `rto`, updates remaining storage, and records any unmet demand if storage is insufficient. |
| 8. Process channel diversion sources. | For `cha`, the routine computes the minimum allowed channel flow from `wdraw_lim`, determines the divertible flow above that minimum, withdraws only what is available, scales `ht2`, reduces the remaining channel hydrograph, and caps unmet demand at the source demand. |
| 9. Process canal sources. | For `can`, the routine computes a minimum remaining canal volume from `wdraw_lim`, withdraws only if storage stays above that minimum, scales and reduces `canal_om_stor(j)`, and otherwise adds the request to unmet demand. |
| 10. Process reservoir sources. | For `res`, the routine computes the minimum remaining reservoir volume from `res_ob(j)%pvol`, withdraws only if the reservoir stays above that threshold, scales and reduces `res(j)`, and otherwise adds the request to unmet demand. |
| 11. Process aquifer sources. | For `aqu`, the routine either applies the legacy aquifer-storage withdrawal path when `bsn_cc%gwflow == 0` or calls `gwflow_pump_allo` to allocate pumping when gwflow is active, then records the extracted and unmet volumes in the output totals. |
| 12. Process unlimited sources. | For `unl`, the routine assigns the full requested transfer volume to the source hydrograph and adds the same amount to the withdrawn total. |
| 13. Accumulate totals and reduce unmet demand. | After the source-specific branch, the routine adds the source hydrograph to the transfer-object total hydrograph and subtracts the source withdrawal from the transfer object's remaining unmet demand. |
| 14. Return to the caller. | The subroutine exits after updating the per-source, per-transfer, and per-allocation output states. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wallo, wallod_out, osrc, trn_m3, wtp` | `wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallo(iwallo)%trn(itrn)%osrc(isrc)%daymoyr, wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr, wallod_out(iwallo)%trn(itrn)%src(isrc)%unmet, wallo(iwallo)%trn(itrn)%osrc(isrc)%aa, wallo(iwallo)%trn(itrn)%src(isrc)%wdraw_lim, wallod_out(iwallo)%trn(itrn)%src(isrc)%demand, wallo(iwallo)%trn(itrn)%unmet_m3` |
| [sym:hydrograph_module] | `recall, wdraw_om, wal_omd, exco, wtp_om_out, wuse_om_out, wtow_om_stor, wtow_om_out, ht2, canal_om_stor, res, hz, aqu` | `recall(iom)%hd, wdraw_om%flo, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, exco(iom)%flo, wtp_om_out(j)%flo, wuse_om_out(j)%flo, wtow_om_stor(j)%flo, wtow_om_out(j)%flo, ht2%flo, canal_om_stor(j)%flo, res(j)%flo, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd%flo, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd%no3, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd%solp, wal_omd(iwallo)%trn(itrn)%h_tot` |
| [sym:aquifer_module] | `aqu_prm, aqu_d` | `aqu_prm(j)%area_ha, aqu_d(j)%stor, aqu_d(j)%no3_st, aqu_d(j)%minp` |
| [sym:reservoir_module] | `res_ob` | `res_ob(j)%pvol` |
| [sym:time_module] | `time` | `time%day, time%yrs, time%mo` |
| [sym:recall_module] | `recall_db` | `recall_db(iom)%org_min%tstep` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wdraw_om` | At the start of every call, before the source-type branch. | `wdraw_om` is reset to `hz` so the routine can build a fresh source hydrograph for the current source without carrying over any prior flow or constituent values. |
| `wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr` | After each source branch computes the amount actually taken from the selected source. | The source's withdrawn volume is stored in `wallod_out` so the transfer-object output records how much water this source supplied to the demand object. |
| `wallod_out(iwallo)%trn(itrn)%src(isrc)%unmet` | When the source cannot fully meet `trn_m3`, or when the aquifer branch records gwflow unmet volume. | The unmet field is increased to record the part of the transfer demand not supplied by this source, and it is capped at the source demand so the output remains bounded by the request. |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` | When a source contributes a scaled hydrograph: outside-basin recall, export coefficient, storage, channel, reservoir, aquifer, or unlimited source branches. | `wal_omd(... )%hd` is set to the hydrograph that represents the water actually withdrawn from the current source, including flow and, where available, constituent mass. |
| `wtow_om_out(j)%flo` | When the storage, channel, or reservoir source branch computes a proportional take fraction `rto`. | `wtow_om_out(j)%flo` is set to the withdrawn water volume from the water tower source for the current source request. |
| `wtow_om_out(j)` | When the water tower branch computes an actual outflow from storage. | `wtow_om_out(j)` stores the full hydrograph for the amount withdrawn from the water tower, not just the flow component, so the transfer object hydrograph can be updated consistently. |
| `wtow_om_stor(j)` | When the water tower branch removes water from stored volume. | `wtow_om_stor(j)` is reduced by the withdrawn fraction so the remaining water tower storage reflects the amount that is still available after this source withdrawal. |
| `ht2` | When the channel source branch determines a valid diversion ratio. | `ht2` is reduced by the diverted fraction so the remaining channel flow after withdrawal is preserved for downstream routing and later source accounting. |
| `canal_om_stor(j)` | When the canal source branch accepts a withdrawal from canal storage. | `canal_om_stor(j)` is reduced by the withdrawal fraction so the canal's remaining storage matches what was actually left after supplying demand. |
| `res(j)` | When the reservoir source branch accepts a withdrawal from reservoir volume. | `res(j)` is reduced by the withdrawal fraction so the reservoir hydrograph reflects the remaining storage after supplying demand. |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd%flo` | When the source branch accepts a withdrawal and stores the withdrawn hydrograph. | `wal_omd(... )%hd%flo` stores the water volume associated with the withdrawn source hydrograph, which is then added into the transfer-object total hydrograph. |
| `aqu_d(j)%stor` | When the legacy aquifer path is active and the requested withdrawal is available. | `aqu_d(j)%stor` is reduced by the amount of water removed from the aquifer, expressed back into aquifer depth units from the withdrawn volume. |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd%no3` | When the legacy aquifer path is active and the withdrawal is available. | `wal_omd(... )%hd%no3` stores the nitrate mass associated with the withdrawn aquifer water so the allocation hydrograph carries solute mass with the extracted flow. |
| `aqu_d(j)%no3_st` | When the legacy aquifer path is active and the withdrawal is available. | `aqu_d(j)%no3_st` is reduced by the nitrate fraction removed with the pumped groundwater. |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd%solp` | When the legacy aquifer path is active and the withdrawal is available. | `wal_omd(... )%hd%solp` stores the soluble phosphorus mass associated with the withdrawn aquifer water. |
| `aqu_d(j)%minp` | When the legacy aquifer path is active and the withdrawal is available. | `aqu_d(j)%minp` is reduced by the phosphorus fraction removed with the pumped groundwater. |
| `wal_omd(iwallo)%trn(itrn)%h_tot` | After the source-specific branch completes for any source type. | `wal_omd(iwallo)%trn(itrn)%h_tot` accumulates the current source hydrograph into the transfer object's total withdrawn hydrograph. |
| `wallo(iwallo)%trn(itrn)%unmet_m3` | After the source-specific withdrawal amount has been determined for the current source. | `wallo(iwallo)%trn(itrn)%unmet_m3` is reduced by the amount taken from this source so the transfer object retains the remaining unmet demand for subsequent sources or compensation logic. |

## File I/O

<!-- facts:io -->


## Lineage

`wallo_withdraw.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 13 non-merge commit(s) since, most recently `f7e26d7` (2026-05-01, "Incremental improvements to pl_fert and pl_manure"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wallo_withdraw.f90` are listed.

- `f7e26d7` (2026-05-01) — Incremental improvements to pl_fert and pl_manure
- `1f59e9b` (2026-04-17) — Revise aquifer water withdrawal logic in wallo_withdraw.f90
- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `9d9069f` (2026-03-31) — gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renames, heat/pond/phreatophyte types, stubs
- `080211e` (2026-03-09) — water allocation operating properly
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wallo_withdraw' has no extracted documentation comment.
- algorithm_steps revised: merged the source-type branches into 14 source-level steps and cited exact visible line ranges from the provided source block.
- review_note: the aquifer branch contains a post-call block that updates `withdraw` and `unmet`, but those locals are never assigned in the visible source; this appears suspicious and may be a latent bug or incomplete snippet.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
