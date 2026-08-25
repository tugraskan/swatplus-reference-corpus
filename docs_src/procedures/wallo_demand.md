---
kind: procedure
symbol: wallo_demand
title: wallo_demand
status: filled
source_hash: ac54805405f664ab
version_label: SWAT+ 62.0.0
args:
  iwallo: Selects which water-allocation object in `wallo` and `wallod_out` is being processed.
  itrn: Selects which transfer object within `wallo(iwallo)%trn` is being processed.
locals:
  j: HRU or object index passed to decision-table routines; initialized to 0 and set to the
    receiving HRU for irrigation decision tables or left as 0 for flo decision tables.
  id: Decision-table index used to select `dtbl_flo(id)` or `dtbl_lum(id)` and pass into `conditions`/`actions`.
  iom: Index into recall or export-coefficient data used to fetch outside-basin or recall
    flow values.
  isrc: Source-object index used to select the source-specific output arrays such as `wtp_om_out`,
    `wuse_om_out`, and `canal_om_out`.
uses:
  water_allocation_module: Provides the transfer object metadata and output storage that `wallo_demand`
    reads to decide how demand is computed and where the resulting flow is written.
  hru_module: Provides the HRU index used for irrigation decision-table evaluation and for
    selecting the receiving HRU in `dtbl_lum` transfers.
  hydrograph_module: Supplies the time-series and object-output flow values that are copied
    into the transfer demand, plus the irrigation demand field updated by decision-table actions.
  conditional_module: Provides the decision-table objects and pointer that `wallo_demand`
    selects before calling `conditions` and `actions`.
  recall_module: Maps a source object to its recall database entry and time step so the routine
    can pick the correct daily, monthly, or yearly flow record.
  exco_module: Imported by the procedure, but no resolved outside references were extracted
    for this module in the context packet.
---

<!-- facts:header -->

Computes the demand/transfer flow for one water-allocation transfer object.

## Bottom Line

`wallo_demand` determines the transfer volume for a single water-allocation demand object (`iwallo`, `itrn`) by branching on the transfer type and source type. It pulls flow from recall, export-coefficient, treatment-plant, water-use, channel, canal, or decision-table state, then stores the resulting demand in `wallod_out(iwallo)%trn(itrn)%trn_flo`.

It matters because `wallo_control` uses this computed demand as the starting unmet demand for later withdrawal allocation. For irrigation decision-table transfers, it also runs the conditional logic and uses the resulting irrigation demand when positive.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallo_demand` is called from `wallo_control` after the transfer object outputs are zeroed. It computes the demand for the current water-allocation transfer object, and `wallo_control` then uses `wallod_out(iwallo)%trn(itrn)%trn_flo` as the initial unmet demand before subtracting withdrawals from sources.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select transfer type | Branch on the transfer object type to choose the demand calculation path. |
| 2. Resolve source object | For outflow transfers, read the source object type and number to determine which upstream flow source to use. |
| 3. Read recall flow | For recall-based outflow sources, map the source to a recall database entry and pick the daily, monthly, or yearly flow record from `recall(iom)%hd`. |
| 4. Read outside-basin flow | For annual outside-basin sources, use the export coefficient flow stored in `exco(iom)%flo`. |
| 5. Read object outflow | Copy the current outflow from the matching object output array for treatment plants, water uses, channels, or canals; channel transfers use `trn_m3` directly. |
| 6. Convert average daily amount | Convert an average daily transfer amount from m3/s to m3/day by multiplying by 86400. |
| 7. Compute channel diversion | Compute remaining channel flow for minimum-flow diversions or a fractional diversion from `trn_m3`. |
| 8. Run flo decision table | Select the flo decision table, point `d_tbl` at it, run `conditions` and `actions`, and then take the resulting transfer flow from `trn_m3`. |
| 9. Run irrigation decision table | Select the irrigation decision table for the receiving HRU, run `conditions` and `actions`, and set demand to the computed irrigation demand when it is positive. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wallo, wallod_out, osrc, wtp, trn_m3` | `wallo(iwallo)%trn(itrn)%trn_typ, wallo(iwallo)%trn(itrn)%src(1)%num, wallo(iwallo)%trn(itrn)%src(1)%typ, wallod_out(iwallo)%trn(itrn)%trn_flo, wallo(iwallo)%trn(itrn)%osrc(1)%aa, wallo(iwallo)%trn(itrn)%amount, wallo(iwallo)%trn(itrn)%dtbl_num, wallo(iwallo)%trn(itrn)%rcv%num, wallo(iwallo)%trn(itrn)%dtbl_lum` |
| [sym:hru_module] | `mo` |  |
| [sym:hydrograph_module] | `recall, exco, wtp_om_out, wuse_om_out, canal_om_out, irrig, icmd` | `recall(iom)%hd, exco(iom)%flo, wtp_om_out(isrc)%flo, wuse_om_out(isrc)%flo, canal_om_out(isrc)%flo, irrig(j)%demand` |
| [sym:conditional_module] | `dtbl_flo, dtbl_lum, d_tbl` |  |
| [sym:recall_module] | `recall_db` | `recall_db(isrc)%iorg_min, recall_db(iom)%org_min%tstep` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wallod_out(iwallo)%trn(itrn)%trn_flo` | When `trn_typ` is `outflo`, `ave_day`, `div_min`, `div_frac`, `dtbl_con`, or `dtbl_lum` | Stores the computed transfer demand for the current transfer object so `wallo_control` can treat it as the initial unmet demand and allocate withdrawals from sources. |
| `d_tbl` | When `trn_typ` is `dtbl_con` or `dtbl_lum` | Points the decision-table pointer at the selected flo or lum decision table before `conditions` and `actions` evaluate and execute the table. |

## File I/O

<!-- facts:io -->


## Lineage

`wallo_demand.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wallo_demand.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `815ec79` (2026-01-07) — water allocation updates
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- No Git lineage commits were resolved for the requested source span.
- warning: missing_doc: Procedure 'wallo_demand' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
