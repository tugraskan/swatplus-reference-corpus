---
kind: procedure
symbol: ru_control
title: ru_control
status: filled
source_hash: 1c31261cbec52e24
version_label: SWAT+ 62.0.0
locals:
  iday: Loop/day index used as a scratch day selector for hydrograph work; it is initialized
    but the visible source uses `day_cur` and `day_next` instead.
  ihdmx: Hard-coded hydrograph dimension marker set to 2 at startup; it appears to define
    the active hydrograph storage depth used by this routine.
  sumfrac: Accumulator for the total fraction of routing-unit elements processed in this call.
  sumarea: Accumulator for the total area of the objects encountered while looping over routing-unit
    elements.
  ielem: Index over routing-unit elements in `ru_def(iru)%num`.
  ise: Routing-unit element number looked up from `ru_def(iru)%num(ielem)` and then used to
    access `ru_elem(ise)`.
  iob: Object index for the current routing element, taken from `ru_elem(ise)%obj`.
  iday_cur: Scratch copy of the current hydrograph day used when writing subdaily flow slots.
  ihtypno: Hydrograph-type index for looping across the `hd` array in each object.
  ef: Expansion factor applied to convert element fractions and, for HRUs, to scale area-based
    fluxes.
  cnv_m3: Conversion factor from millimeters over routing-unit area to cubic meters, based
    on `ru(iru)%da_km2`.
  cnv: Subdaily conversion factor used to translate HRU surface runoff from mm to m3 when
    building subdaily hydrographs.
  ii: Inner loop counter for subdaily time-step loops.
  ts_flo_mm: Subdaily flow contribution in millimeters, derived from the conversion factor
    and HRU surface runoff.
  rto: Declared but not used in the visible source; likely reserved for a routing ratio or
    cloud-cover factor from older code.
  istep: Loop counter used when shifting hydrograph steps between current and next day storage.
  ipest: Loop counter for pesticides in `cs_db%num_pests`.
  isalt: Loop counter for salt ions in `cs_db%num_salts`.
  ics: Loop counter for other constituents in `cs_db%num_cs`.
  hru_num: HRU index obtained from `ob(iob)%num` so the routine can read HRU-specific area
    and balance arrays.
  istep_bak: Backward step index used while shifting the current-day hydrograph by the time
    of concentration.
  day_cur: Current hydrograph day copied from `ob(icmd)%day_cur`.
  day_next: Next hydrograph day, computed as `day_cur + 1` and wrapped to 1 after `day_max`.
  tinc: Number of subdaily time steps corresponding to the routing delay `ru_tc(iru)`.
  inext_step: Index of the source subdaily step when copying current-day flow into the next-day
    hydrograph slot.
uses:
  hru_module: '`hru_module` matters because the routine converts HRU-specific balance fluxes
    to routing-unit totals using `hru(hru_num)%area_ha`, so it needs the HRU area for every
    HRU element it aggregates.'
  ru_module: '`ru_module` matters because `ru(iru)%da_km2` provides the routing-unit drainage
    area used to scale element fractions and convert mm-based flow to routed volume.'
  hydrograph_module: '`hydrograph_module` matters because it supplies the routing-unit definition,
    object connectivity, and hydrograph storage that `ru_control` reads and updates: `ob`,
    `ru_def`, and `ru_elem` determine which objects are routed, which hydrograph type is being
    filled, and how flow is distributed across the unit.'
  time_module: '`time_module` matters because subdaily branching and flow shifting depend
    on the model time step length and the number of substeps per day.'
  constituent_mass_module: '`constituent_mass_module` matters because `ru_control` copies
    pesticide, salt, and other constituent hydrographs from source objects into routing-unit
    hydrographs and uses the constituent counts to drive the loops over `pest`, `salt`, and
    `cs` arrays.'
  output_landscape_module: '`output_landscape_module` is imported by this routine, but the
    extracted source does not show any direct references to its state; it may be included
    for shared output bookkeeping or interface consistency with other landscape-routing code.'
  salt_module: '`salt_module` matters because this routine aggregates HRU salt flux balances
    into routing-unit daily totals, including the area-weighted HRU-to-RU sums for irrigation,
    rainfall, deposition, fertilizer, amendment, uptake, and dissolved salt.'
  cs_module: '`cs_module` matters because the routine similarly aggregates HRU constituent
    balances into routing-unit totals, including sediment-associated and other chemical constituent
    fluxes such as `sedm`, `wtsp`, `irsw`, `irgw`, `irwo`, `rain`, `dryd`, `fert`, `uptk`,
    `rctn`, and `sorb`.'
---

<!-- facts:header -->

Routes daily and subdaily water, salt, and constituent hydrographs for one routing unit. It aggregates HRU contributions into routing-unit totals and, when needed, builds subdaily hydrographs from daily flow data.

## Bottom Line

`ru_control` is the routing-unit control subroutine. It loops through the elements assigned to the current routing unit, pulls each element's flow and constituent hydrographs from `hydrograph_module`, `constituent_mass_module`, `salt_module`, and `cs_module`, and adds the contributions into routing-unit totals such as `ru_d(iru)`, `ob(icmd)%hd(*)`, `obcs(icmd)%hd(*)`, `rusaltb_d`, `rucsb_d`, `ru_hru_saltb_d`, and `ru_hru_csb_d`.

It also handles special cases for export coefficients and HRU objects, applies delivery ratios, and, for subdaily simulations, shifts or reconstructs hydrographs so the current command object has the runoff timing needed by later routing and output steps.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ru_control` runs when `command` processes a routing-unit command (`case ('ru')`), after `command` has set `iru = ob(icmd)%num`. It prepares and accumulates the current routing-unit hydrographs for water, salts, and other constituents, and later routing/output behavior depends on these totals being available in `ob(icmd)%hd(*)`, `obcs(icmd)%hd(*)`, `ru_d(iru)`, and the RU/HRU balance arrays before `hyddep_output` or subsequent command processing uses them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize working indices and scaling factors | Declare scratch variables, set `iday = 1` and `ihdmx = 2`, and compute `cnv_m3 = 1000. * ru(iru)%da_km2` to provide the routing-unit area conversion used later. |
| 2. Seed routing-unit hydrographs to zero or empty states | Copy zero hydrographs into `ru_d(iru)` and `ob(icmd)%hd(1:5)`, and, when any constituents are simulated (`cs_db%num_tot > 0`), initialize the constituent hydrographs `obcs(icmd)%hd(1:5)` to the empty constituent hydrograph `hin_csz`. |
| 3. Clear element accumulators and set current/next day indices | Reset `sumfrac` and `sumarea`, then copy `ob(icmd)%day_cur` into `day_cur`, compute `day_next`, and wrap `day_next` to 1 when it passes `day_max`. |
| 4. Loop over routing-unit elements | For each element listed in `ru_def(iru)%num_tot`, fetch the element record, object index, HRU number, and routing parameters, then accumulate element fraction and object area into `sumfrac` and `sumarea`. |
| 5. Apply the element delivery ratio and handle export-coefficient objects | Read `ru_elem(ise)%dr` into `delrto`. If the element is an export coefficient object (`obtyp == 'exc'`), compute `ht1` from `exco(ob(iob)%props) ** delrto`, set `ht2` to zero, and scale by area-based expansion when the object area exceeds 0.01 ha. |
| 6. Build routed hydrographs for non-export elements | For normal routing elements, set `ef` from the element fraction and expand it for HRU objects when needed. Then loop over all hydrograph types in `ob(iob)%nhyds`, apply the delivery ratio to non-recharge hydrographs, copy constituent loads into `hcs1`, and multiply the selected hydrograph by `ef`. |
| 7. Add water and constituent contributions to routing-unit totals | Accumulate the scaled hydrograph into `ob(icmd)%hd(ihtypno)` and `ru_d(iru)`, then add pesticide, salt, and other constituent loads from `hcs1` into the routing-unit hydrograph arrays. For HRU source objects, also retain salt fluxes in `rusaltb_d(iru)`. |
| 8. Accumulate HRU salt balance contributions | For the first hydrograph type only, and only when the source object is an HRU, multiply HRU salt balance terms by `hru(hru_num)%area_ha` and add them to `ru_hru_saltb_d`, including the dissolved-salt term in `salt(1)%diss`. |
| 9. Accumulate HRU constituent balance contributions | For the first hydrograph type only, and only when the source object is an HRU, multiply HRU constituent balance terms by HRU area and add them to `ru_hru_csb_d`, including sediment, uptake, reaction, and sorbed-constituent terms. |
| 10. Add object hydrograph separation contributions | Add the current object's separated surface runoff and lateral flow volumes into the routing-unit separation totals in `ob(icmd)%hdsep`. |
| 11. Subdaily branch: build HRU hydrographs when Green-Ampt routing is active | When `time%step > 1` and `bsn_cc%gampt == 1`, loop through subdaily steps for HRU sources, convert mm to m3 with `cnv`, write the current hydrograph slot, and shift the hydrograph to the next day according to `ru_tc(iru)`. |
| 12. Subdaily branch: call the helper hydrograph shifter for non-Green-Ampt routing | When `time%step > 1` and `bsn_cc%gampt == 0`, call `flow_hyd_ru_hru` with the current day index and the daily surface, lateral, and tile hydrographs so the subdaily hydrograph storage is populated. |
| 13. Single-step branch: store daily runoff for command-level summation | When `time%step == 1`, copy the daily total runoff `ob(icmd)%hd(1)%flo` into `ob(icmd)%hyd_flo(day_cur,1)` so `command` can sum incoming runoff later. |
| 14. Return to caller | Exit the subroutine after all routing, constituent accumulation, and hydrograph preparation are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(hru_num)%area_ha` |
| [sym:ru_module] | `ru` | `ru(iru)%da_km2` |
| [sym:hydrograph_module] | `ob, ru_def, ru_elem` | `ob(icmd)%hd(1), ob(icmd)%hd(2), ob(icmd)%hd(3), ob(icmd)%hd(4), ob(icmd)%hd(5), ob(icmd)%day_cur, ob(icmd)%day_max, ru_def(iru)%num_tot, ru_def(iru)%num(ielem), ru_elem(ise)%obj, ru_elem(ise)%obtypno, ru_elem(ise)%frac, ob(iob)%area_ha, ru_elem(ise)%dr, ru_elem(ise)%obtyp, ob(iob)%typ, ob(iob)%nhyds, ob(iob)%hd(ihtypno), ob(icmd)%hd(ihtypno), ob(iob)%num` |
| [sym:time_module] | `time` | `time%step, time%dtm` |
| [sym:constituent_mass_module] | `cs_db, obcs, hcs1, rusaltb_d, rucsb_d` | `cs_db%num_tot, obcs(icmd)%hd(1), obcs(icmd)%hd(2), obcs(icmd)%hd(3), obcs(icmd)%hd(4), obcs(icmd)%hd(5), cs_db%num_pests, hcs1%pest(ipest), obcs(iob)%hd(ihtypno)%pest(ipest), cs_db%num_salts, hcs1%salt(isalt), obcs(iob)%hd(ihtypno)%salt(isalt), cs_db%num_cs, hcs1%cs(ics), obcs(iob)%hd(ihtypno)%cs(ics), obcs(icmd)%hd(ihtypno)%pest(ipest), obcs(icmd)%hd(ihtypno)%salt(isalt), rusaltb_d(iru)%hd(ihtypno)%salt(isalt), obcs(icmd)%hd(ihtypno)%cs(ics), rucsb_d(iru)%hd(ihtypno)%cs(ics)` |
| [sym:output_landscape_module] | `ob_io, ob_out, output_landscape state not resolved from candidate references` | `No candidate outside references were resolved to `output_landscape_module` in the context packet.` |
| [sym:salt_module] | `ru_hru_saltb_d, hsaltb_d` | `ru_hru_saltb_d(iru)%salt(isalt)%wtsp, hsaltb_d(hru_num)%salt(isalt)%wtsp, ru_hru_saltb_d(iru)%salt(isalt)%irsw, hsaltb_d(hru_num)%salt(isalt)%irsw, ru_hru_saltb_d(iru)%salt(isalt)%irgw, hsaltb_d(hru_num)%salt(isalt)%irgw, ru_hru_saltb_d(iru)%salt(isalt)%irwo, hsaltb_d(hru_num)%salt(isalt)%irwo, ru_hru_saltb_d(iru)%salt(isalt)%rain, hsaltb_d(hru_num)%salt(isalt)%rain, ru_hru_saltb_d(iru)%salt(isalt)%dryd, hsaltb_d(hru_num)%salt(isalt)%dryd, ru_hru_saltb_d(iru)%salt(isalt)%road, hsaltb_d(hru_num)%salt(isalt)%road, ru_hru_saltb_d(iru)%salt(isalt)%fert, hsaltb_d(hru_num)%salt(isalt)%fert, ru_hru_saltb_d(iru)%salt(isalt)%amnd, hsaltb_d(hru_num)%salt(isalt)%amnd, ru_hru_saltb_d(iru)%salt(isalt)%uptk, hsaltb_d(hru_num)%salt(isalt)%uptk, ru_hru_saltb_d(iru)%salt(1)%diss, hsaltb_d(hru_num)%salt(1)%diss` |
| [sym:cs_module] | `ru_hru_csb_d, hcsb_d` | `ru_hru_csb_d(iru)%cs(ics)%sedm, hcsb_d(hru_num)%cs(ics)%sedm, ru_hru_csb_d(iru)%cs(ics)%wtsp, hcsb_d(hru_num)%cs(ics)%wtsp, ru_hru_csb_d(iru)%cs(ics)%irsw, hcsb_d(hru_num)%cs(ics)%irsw, ru_hru_csb_d(iru)%cs(ics)%irgw, hcsb_d(hru_num)%cs(ics)%irgw, ru_hru_csb_d(iru)%cs(ics)%irwo, hcsb_d(hru_num)%cs(ics)%irwo, ru_hru_csb_d(iru)%cs(ics)%rain, hcsb_d(hru_num)%cs(ics)%rain, ru_hru_csb_d(iru)%cs(ics)%dryd, hcsb_d(hru_num)%cs(ics)%dryd, ru_hru_csb_d(iru)%cs(ics)%fert, hcsb_d(hru_num)%cs(ics)%fert` |
| [sym:hru_module] | `hru` | `hru(hru_num)%area_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ru_d(iru)` | After `ru_d(iru) = hz` at routine start and during each non-export routing-element update at `ru_control.f90:148-149` | `ru_d(iru)` is reset to zero-equivalent before the loop, then incremented by each element's scaled hydrograph contribution so it ends as the routing-unit total hydrograph for the current command. |
| `ob(icmd)%hd(1)` | For every hydrograph type processed in the element loop at `ru_control.f90:148` | `ob(icmd)%hd(1)` is initialized to zero and then accumulated with routed total flow contributions, so it holds the command object's total water hydrograph. |
| `ob(icmd)%hd(2)` | For every hydrograph type processed in the element loop at `ru_control.f90:148` | `ob(icmd)%hd(2)` is initialized to zero and then accumulated with the routed recharge hydrograph when the source hydrograph type corresponds to recharge or when `ht2` is used in the selected branch. |
| `ob(icmd)%hd(3)` | For every hydrograph type processed in the element loop at `ru_control.f90:148` and during the subdaily branch | `ob(icmd)%hd(3)` is initialized to zero and then filled with the routed surface-flow hydrograph, including subdaily updates when Green-Ampt routing is off or on. |
| `ob(icmd)%hd(4)` | For every hydrograph type processed in the element loop at `ru_control.f90:148` | `ob(icmd)%hd(4)` is initialized to zero and then accumulated with the routed lateral-flow hydrograph contribution. |
| `ob(icmd)%hd(5)` | For every hydrograph type processed in the element loop at `ru_control.f90:148` | `ob(icmd)%hd(5)` is initialized to zero and then accumulated with the routed tile-flow hydrograph contribution. |
| `obcs(icmd)%hd(1)` | When constituent counts are positive and each hydrograph type is processed at `ru_control.f90:151-153` | `obcs(icmd)%hd(1)` is zeroed at routine start and then filled with routed pesticide masses copied from source-object hydrographs. |
| `obcs(icmd)%hd(2)` | When salt simulation is active and each hydrograph type is processed at `ru_control.f90:155-158` | `obcs(icmd)%hd(2)` is zeroed at routine start and then filled with routed salt-ion masses copied from source-object hydrographs. |
| `obcs(icmd)%hd(3)` | When other-constituent simulation is active and each hydrograph type is processed at `ru_control.f90:191-193` | `obcs(icmd)%hd(3)` is zeroed at routine start and then filled with routed constituent masses copied from source-object hydrographs. |
| `obcs(icmd)%hd(4)` | When the corresponding routed hydrograph slots are updated in the loop at `ru_control.f90:148-156` | `obcs(icmd)%hd(4)` is initialized to zero and is available as the next hydrograph slot in the command object, but the visible source does not show a separate distinct assignment for it beyond the initial reset. |
| `obcs(icmd)%hd(5)` | When the corresponding routed hydrograph slots are updated in the loop at `ru_control.f90:148-156` | `obcs(icmd)%hd(5)` is initialized to zero and is available as the next hydrograph slot in the command object, but the visible source does not show a separate distinct assignment for it beyond the initial reset. |
| `ihru` | During each element iteration at `ru_control.f90:83-84` and `ru_control.f90:112-117` | `ihru` is updated to the HRU number associated with the current routing element so later subdaily and HRU-specific logic can index the correct HRU record. |
| `ht1` | At the start of each element iteration at `ru_control.f90:84-88` | `ht1` is reset to zero-state and then becomes the working hydrograph value for the current element's total/surface routing path before scaling and accumulation. |
| `ht2` | At the start of each element iteration at `ru_control.f90:84-88` | `ht2` is reset to zero-state and serves as the working hydrograph slot for recharge/secondary flow handling in the element branch. |
| `ht3` | At the start of each element iteration at `ru_control.f90:84-88` | `ht3` is reset to zero-state so the routine can reuse the variable for other hydrograph slot calculations if needed, although the visible source does not assign it later in this routine. |
| `ht4` | At the start of each element iteration at `ru_control.f90:84-88` | `ht4` is reset to zero-state so the routine can reuse the variable for other hydrograph slot calculations if needed, although the visible source does not assign it later in this routine. |
| `ht5` | At the start of each element iteration at `ru_control.f90:84-88` | `ht5` is reset to zero-state so the routine can reuse the variable for other hydrograph slot calculations if needed, although the visible source does not assign it later in this routine. |
| `hcs1` | At the start of each element iteration at `ru_control.f90:89` and during HRU-area-weighted sums at `ru_control.f90:160-225` | `hcs1` is initialized to the empty constituent hydrograph and then reused as a scratch container for pesticide, salt, and other constituent loads copied from the source object. |
| `delrto` | No explicit assignment to `delrto` outside the element loop is shown; it is set from `ru_elem(ise)%dr` at `ru_control.f90:96` | `delrto` holds the delivery-ratio hydrograph for the current element and is used to exponentiate or scale the routed hydrographs before accumulation. |
| `hcs1%pest(ipest)` | Within the pesticide loop at `ru_control.f90:124-126` | `hcs1%pest(ipest)` is copied from the current source object's pesticide hydrograph so the routed pesticide mass can be added to the command object. |
| `hcs1%salt(isalt)` | Within the salt loop at `ru_control.f90:127-129` and area-weighted aggregation at `ru_control.f90:163-185` | `hcs1%salt(isalt)` is copied from the current source object's salt hydrograph so the routed salt mass can be added to the command object and, for HRU sources, to RU-level salt balance outputs. |
| `hcs1%cs(ics)` | Within the constituent loop at `ru_control.f90:130-132` and area-weighted aggregation at `ru_control.f90:200-221` | `hcs1%cs(ics)` is copied from the current source object's other-constituent hydrograph so the routed constituent mass can be added to the command object and to RU-level constituent balance outputs. |
| `ob(icmd)%hd(ihtypno)` | For each hydrograph type selected in the element loop at `ru_control.f90:148` | `ob(icmd)%hd(ihtypno)` is incremented by the scaled flow contribution for that hydrograph type, so the command object's hydrograph array stores the accumulated routed flow by hydrograph category. |
| `obcs(icmd)%hd(ihtypno)%pest(ipest)` | For each pesticide index in the element loop at `ru_control.f90:151-153` | `obcs(icmd)%hd(ihtypno)%pest(ipest)` is incremented by the routed pesticide load so the command object's constituent hydrograph mirrors the water hydrograph updates. |

## File I/O

<!-- facts:io -->


## Lineage

`ru_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `78b295f` (2026-02-05, "Updated hydrological calculations to include time step adjustments for flow conv…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ru_control.f90` are listed.

- `78b295f` (2026-02-05) — Updated hydrological calculations to include time step adjustments for flow conversions in hru_hyds and ru_control subroutines.
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `c8fadcd` (2025-05-13) — Update ru_control.f90
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ru_control' has no extracted documentation comment.
- time_module candidate refs were not resolved in the packet; outside_state[3] is filled from visible source usage only.
- output_landscape_module had no resolved candidate outside references in the packet; its import appears unused in the extracted lines.
- state_changes for `ob(icmd)%hd(4)` and `ob(icmd)%hd(5)` are inferred from initialization and the hydrograph array role, but the visible source does not show distinct per-slot assignments beyond the zeroing and accumulation structure.
- algorithm_steps revised: merged the original draft's broad state-update and routine-call steps into a line-ordered 14-step sequence that matches the visible source blocks and cites only real line ranges.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
