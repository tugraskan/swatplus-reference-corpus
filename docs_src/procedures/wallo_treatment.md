---
kind: procedure
symbol: wallo_treatment
title: wallo_treatment
status: filled
source_hash: 180d9b131136afcb
version_label: SWAT+ 62.0.0
args:
  iwallo: '`iwallo` selects which water-allocation object in `wal_omd` is being processed,
    so the routine reads the transfer mass/volume for that allocation entry.'
  itrn: '`itrn` selects the specific transfer within `wal_omd(iwallo)%trn`, which supplies
    the incoming total hydrologic state used to scale and limit treatment output.'
  itrt: '`itrt` selects the water-treatment-plant slot whose treated-concentration template
    and accumulated outflow/removed-mass records are updated.'
locals:
  iom: '`iom` is only a dummy local used to suppress the unused-variable warning; the `if
    (iom < 0) continue` line has no model effect.'
uses:
  water_allocation_module: '`water_allocation_module` matters because `wallo_treatment` does
    not work with local copies alone: it updates the global treatment outflow and removed-mass
    records and reads the selected allocation transfer from the shared water-allocation state
    that the broader allocation controller maintains.'
  hydrograph_module: '`hydrograph_module` matters because this routine manipulates shared
    `hyd_output` states: it copies the treatment template from `wtp_om_treat(itrt)`, scales
    the treated flow from `wal_omd(iwallo)%trn(itrn)%h_tot%flo`, stores the resulting outflow
    in `wtp_om_out(itrt)`, derives removed mass in `wal_tr_omd(itrt)`, and resets `outflo_om`
    to the zeroed `hz` state at the end.'
  constituent_mass_module: '`constituent_mass_module` matters because the routine only performs
    constituent mass conversion when constituents are simulated (`cs_db%num_tot > 0`), and
    that switch controls whether `hydcsout_conc_mass` is called to populate `outflo_cs` from
    the treated flow and `wtp_cs_treat(itrt)`.'
---

<!-- facts:header -->

Computes treated wastewater outflow for a water allocation transfer. It scales the treatment-plant concentration template by transferred flow, converts concentrations to masses, and updates transfer bookkeeping for downstream water-quality accounting.

## Bottom Line

`wallo_treatment` is the wastewater-treatment branch of the water-allocation workflow. For the selected allocation object, transfer, and treatment plant, it builds the treated outflow from the plant's concentration template, scales it by the transferred volume, converts the result from concentrations to masses, and clips the treated masses so they do not exceed the incoming transfer mass.

It also accumulates the treated outflow into `wtp_om_out(itrt)`, computes the removed organic-mineral mass as the difference between the incoming transfer and treated outflow, and, when constituents are enabled, converts the treated volume plus treatment concentrations into constituent mass output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallo_treatment` runs inside `wallo_control` in the wastewater-treatment case after the control routine has already selected the allocation object, transfer index, and treatment-plant index and added the transfer to treatment-plant storage. Its results feed the rest of the allocation bookkeeping by updating treated outflow, removed mass, and optional constituent masses for later reporting and water-quality accounting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. suppress unused local | Declares the unused local `iom` and executes `if (iom < 0) continue` only to silence compiler warnings; this does not change model state. |
| 2. copy treatment template | Copies the stored treatment-plant outflow template `wtp_om_treat(itrt)` into `outflo_om`, giving this transfer a baseline set of treated concentrations and flow fields. |
| 3. scale treated flow | Sets treated outflow volume to a fraction of the withdrawn transfer by multiplying `outflo_om%flo` by the incoming transfer flow `wal_omd(iwallo)%trn(itrn)%h_tot%flo`. |
| 4. convert concentrations to mass | Calls `hyd_convert_conc_to_mass` so the treated output in `outflo_om` is represented as mass rather than concentration, using the computed treated flow. |
| 5. cap treated mass by inflow | Calls `hyd_min` to limit treated mass in `outflo_om` so no mass component exceeds the corresponding incoming transfer mass in `wal_omd(iwallo)%trn(itrn)%h_tot`. |
| 6. accumulate treated outflow | Adds the treated output in `outflo_om` to the cumulative treatment-plant outflow record `wtp_om_out(itrt)`. |
| 7. compute removed mass | Computes the mass removed by treatment as the incoming transfer `wal_omd(iwallo)%trn(itrn)%h_tot` minus the accumulated treated outflow `wtp_om_out(itrt)`, and stores it in `wal_tr_omd(itrt)`. |
| 8. optionally convert constituents | If constituents are enabled (`cs_db%num_tot > 0`), calls `hydcsout_conc_mass` to convert `wtp_cs_treat(itrt)` into constituent mass output `outflo_cs` using the treated volume `outflo_om%flo`. |
| 9. reset temporary output | Resets `outflo_om` to `hz`, clearing the temporary treated-outflow state before returning. |
| 10. return | Returns to the caller after updating treated outflow, removed mass, and any constituent mass output. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `outflo_om, wal_omd, wtp_om_treat, wtp_om_out, wal_tr_omd, hz` | `outflo_om%flo, wal_omd(iwallo)%trn(itrn)%h_tot%flo, wal_omd(iwallo)%trn(itrn)%h_tot, wtp_om_treat(itrt), wtp_om_out(itrt), wal_tr_omd(itrt), hz` |
| [sym:hydrograph_module] | `outflo_om, wal_omd, wal_tr_omd, wtp_om_treat, wtp_om_out, hz` | `outflo_om%flo, wal_omd(iwallo)%trn(itrn)%h_tot%flo, wal_omd(iwallo)%trn(itrn)%h_tot` |
| [sym:constituent_mass_module] | `cs_db, wtp_cs_treat, outflo_cs` | `cs_db%num_tot` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `outflo_om` | After the treatment template is copied and flow is scaled, and before the temporary state is reset. | `outflo_om` is overwritten from `wtp_om_treat(itrt)` and then adjusted to represent the treated outflow for the current allocation transfer; it acts as the routine's working hydrologic output container. |
| `outflo_om%flo` | When the treated-flow fraction is applied in the wastewater-treatment branch. | `outflo_om%flo` becomes the treated volume for this transfer, computed from the treatment template flow scaled by the incoming withdrawal flow. |
| `wtp_om_out(itrt)` | Every time the routine finishes computing the treated outflow for the selected treatment plant. | `wtp_om_out(itrt)` is incremented by the treated output so the model retains the cumulative outflow from that treatment plant across calls. |
| `wal_tr_omd(itrt)` | After treated outflow has been accumulated and compared to the incoming transfer. | `wal_tr_omd(itrt)` stores the net organic-mineral mass removed by treatment as the difference between the incoming transfer and the treated outflow. |

## File I/O

<!-- facts:io -->


## Lineage

`wallo_treatment.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wallo_treatment.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wallo_treatment' has no extracted documentation comment.
- algorithm_steps revised: expanded the original six-step draft into ten source-backed steps to reflect the template copy, scaling, accumulation, removal calculation, optional constituent conversion, and final reset shown in the source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
