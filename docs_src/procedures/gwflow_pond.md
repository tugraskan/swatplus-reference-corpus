---
kind: procedure
symbol: gwflow_pond
title: gwflow_pond
status: filled
source_hash: d831cbe548bfb7a3
version_label: SWAT+ 62.0.0
locals:
  pond_name: Character(len=18) label built by an internal write at line 334 as 'pond_XXXX';
    used only as a string field in out_pond_bal and out_pond_sol writes.
  r: Outer loop index over recharge ponds, 1 to gw_npond; indexes gw_pond_info(r) throughout.
  k: Inner loop index over aquifer cells connected to pond r, 1 to gw_pond_info(r)%ncell;
    used to accumulate per-cell secharge into cell_recharge.
  s: Solute index in the gwsol_ss accumulation loop at lines 316-320, ranging 1 to gw_nsolute.
  year: Calendar year read from in_ponds at line 57 when gw_pond_div_flag == 1; not used after
    the read.
  day: Day-of-year read from in_ponds at line 57 when gw_pond_div_flag == 1; not used after
    the read.
  month: Month read from in_ponds at line 57 when gw_pond_div_flag == 1; not used after the
    read.
  chan_id: Index into ch_stor and ch_water for the source channel linked to pond r; set from
    gw_pond_info(r)%chan at line 87.
  rec_id: Point-source record index for canal diversion; used in omitted lines 131-300 to
    look up div_conc_salt and div_conc_cs.
  cell_id: Aquifer grid cell index for the k-th cell connected to pond r; set from gw_pond_info(r)%cells(k)
    in the per-cell recharge loop.
  iwst: Weather station index for pond r; set from gw_pond_info(r)%wsta to index wst for precip
    and PET.
  dum: Unused diagnostic integer; set to 10 at lines 82 and 330 as guard sentinels with no
    effect on model state.
  sol_index: Sequential solute counter advancing through NO3 (1), P (2), then each salt ion,
    then each constituent; indexes gw_pond_info(r)%sol_mass(sol_index) and output arrays.
  isalt: Loop counter for salt ions, 1 to cs_db%num_salts; advances sol_index by one per ion.
  ics: Loop counter for custom constituents, 1 to cs_db%num_cs; advances sol_index past the
    salt-ion range.
  canal_id: Index into gw_canl_div_info for the irrigation canal linked to pond r; set from
    gw_pond_info(r)%canal in omitted lines 131-300.
  chan_volume: Channel storage (m3) captured from ch_stor(chan_id)%flo at line 88 before diversion;
    denominator for channel solute concentrations at lines 102, 111, 124.
  cell_recharge: Seepage flux (m3) from pond r to one aquifer cell k; computed in the omitted
    per-cell loop and accumulated into pond_recharge.
  pond_recharge: Total seepage (m3) from pond r to the aquifer across all connected cells;
    written to out_pond_bal at line 343.
  div_specified: Requested diversion volume (m3) from gw_pond_info(r)%div, assigned at line
    80; compared against chan_volume at line 91 to derive div_added.
  div_added: Actual volume (m3) added to pond r; capped at chan_volume when div_specified
    exceeds channel storage (line 92); flagged at line 329 if negative.
  pond_evap: Evaporation from pond r surface (m3) computed from wst(iwst)%weat%pet and gw_pond_info(r)%evap_co
    in omitted lines; written to out_pond_bal at line 342.
  pond_rain: Rainfall added to pond r (m3) from wst(iwst)%weat%precip and gw_pond_info(r)%area
    in omitted lines; written to out_pond_bal at line 340.
  pond_volume: Pond storage (m3) after additions and before recharge occurs; set in omitted
    lines; denominator for recharge solute concentrations at line 305.
  sol_conc: Concentration (g/m3) of one solute in the source water; recomputed for each species
    before calculating sol_mass.
  sol_mass: Mass (kg) of one solute transferred in one operation; reused for each species
    per loop iteration.
  div_mass: Array (20 elements, kg) of solute masses added to the pond from today's diversion,
    by sol_index; written to out_pond_sol at line 356.
  rech_mass: Array (20 elements, kg) of total solute masses leaching from pond r to the aquifer
    across all cells today, by sol_index; written to out_pond_sol at line 356.
  rech_mass_cell: Array (20 elements, g) of solute mass leaching from pond r to one cell k;
    assigned to gwsol_ss(cell_id)%solute(s)%pond at line 317.
uses:
  gwflow_module: gwflow_module is the primary data repository for all groundwater state. gwflow_pond
    reads pond geometry (gw_pond_info), cell connectivity (cells, conn_area, bed_k), diversion
    amounts (gw_pond_info(r)%div), and control flags (gw_pond_flag, gw_pond_div_flag, gw_solute_flag,
    gwsol_salt, gwsol_cons, gwflag_flux, gw_daycount). It writes daily, monthly, and yearly
    per-cell pond recharge flux into gw_hyd_ss(cell_id)%pond, gw_hyd_ss_mo(cell_id)%pond,
    and gw_hyd_ss_yr(cell_id)%pond for gwflow_simulate's mass-balance pass.
  hydrograph_module: ch_stor holds the current-day storage for each channel reach. gwflow_pond
    reads ch_stor(chan_id)%flo to determine whether the channel can supply the full requested
    diversion, then reduces flo, no3, and solp by the diverted amounts so channel mass balance
    remains consistent after transfer to the pond.
  time_module: Provides the current simulation date. gwflow_pond uses time%day, time%mo, time%day_mo,
    and time%yrc exclusively as header fields in the out_pond_bal, out_pond_sol, out_pond_mass,
    and out_pond_conc write statements; they are read-only within this routine.
  constituent_mass_module: cs_db%num_salts and cs_db%num_cs control loop bounds for salt ions
    and custom constituents. ch_water(chan_id)%salt(isalt) and ch_water(chan_id)%cs(ics) hold
    solute mass in the source channel; gwflow_pond removes a proportion of each when water
    is diverted to the pond.
  water_allocation_module: water_allocation_module is imported at line 13. The source comment
    at line 15 states that div_conc_cs and div_conc_salt were temporarily moved into gwflow_module
    pending full wallo integration. No outside reference in the context packet was resolved
    to this module; its specific contribution is uncertain until the integration is completed.
  climate_module: Provides daily weather data for the weather station assigned to each pond.
    gwflow_pond uses wst(iwst)%weat%precip and wst(iwst)%weat%pet together with gw_pond_info(r)%evap_co
    and gw_pond_info(r)%area to compute pond_rain and pond_evap in the omitted source block
    (lines 131-300).
---

<!-- facts:header -->

Simulates daily water and solute exchange between user-defined recharge ponds and the groundwater grid, then writes pond water-balance and solute-balance output files.

## Bottom Line

gwflow_pond runs once per simulation day (when gw_pond_flag == 1) and manages the full water and solute cycle for all recharge ponds. It reads or zeroes the specified daily diversion volume, diverts water from the linked surface channel or irrigation canal into each pond's storage, computes rainfall additions and evaporative losses using the assigned weather station, and calculates seepage from each pond to the underlying aquifer cells via a hydraulic conductance relationship.

For each active pond, the routine tracks solute mass (NO3, soluble P, salt ions, custom constituents) entering from diverted water and leaving as groundwater recharge; per-cell solute fluxes are stored in gwsol_ss, gwsol_ss_sum, and gwsol_ss_sum_mo for gwflow_simulate's mass-balance pass. When gwflag_flux == 1, it writes daily per-pond water balance to out_pond_bal, per-pond solute mass balance to out_pond_sol, and wide-format all-pond mass and concentration rows to out_pond_mass and out_pond_conc.

## Arguments

<!-- facts:arguments -->

## Where It Fits

gwflow_pond is called from gwflow_simulate at line 206, inside the daily groundwater simulation loop, after gwflow_simulate has initialized canal diversion storage for the day (lines 199-202: gw_canl_div_info(i)%stor = gw_canl_div_info(i)%div and out_pond/out_seep zeroed). It runs before gwflow_canal_div (gwflow_simulate.f90:210) and before gwflow_simulate's per-cell source/sink summation (line 214+). The per-cell recharge flux written into gw_hyd_ss(cell_id)%pond and the solute fluxes in gwsol_ss(cell_id)%solute(s)%pond feed directly into gwflow_simulate's groundwater mass-balance and head-update pass for the same day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Guard on recharge pond flag | Checks gw_pond_flag == 1. If false, the entire routine body is skipped and control returns immediately; no state is modified. |
| 2. Read or zero daily diversion volumes | If gw_pond_div_flag == 1, reads one record from in_ponds containing year, month, day, and one diversion volume (m3) per pond into gw_pond_info(r)%div for all r. Otherwise zeroes gw_pond_info(r)%div for all ponds. |
| 3. Zero per-pond daily accumulators | Opens the outer loop over r=1..gw_npond. Resets pond_rain, div_added, pond_evap, pond_recharge, gw_pond_info(r)%div_uns, div_mass, and rech_mass to zero before any pond-specific computation. |
| 4. Gate on pond start day | Checks gw_daycount >= gw_pond_info(r)%dy_start. All pond-specific water and solute processing for pond r is skipped if the pond has not yet reached its scheduled activation day. |
| 5. Apply channel-source diversion | If gw_pond_info(r)%chan > 0: sets chan_id and captures chan_volume from ch_stor(chan_id)%flo. Computes div_added = min(div_specified, chan_volume); sets gw_pond_info(r)%div_uns = div_specified - div_added; reduces ch_stor(chan_id)%flo by div_added; increases gw_pond_info(r)%stor by div_added. |
| 6. Transfer NO3 and soluble P mass from channel to pond | When gw_solute_flag == 1 and chan_volume > 10: computes sol_conc = ch_stor(chan_id)%no3 * 1000 / chan_volume g/m3, sol_mass = sol_conc * div_added / 1000 kg (capped at available mass), deducts from ch_stor(chan_id)%no3, adds to gw_pond_info(r)%sol_mass(1) and div_mass(1). Repeats for soluble P using ch_stor(chan_id)%solp into index 2. |
| 7. Transfer salt ion mass from channel; process canal diversion, rainfall, evaporation, and per-cell seepage (partial) | When gwsol_salt == 1, loops isalt=1..cs_db%num_salts: advances sol_index, computes concentration from ch_water(chan_id)%salt(isalt), caps and deducts sol_mass, adds to gw_pond_info(r)%sol_mass(sol_index) and div_mass(sol_index). Source lines 131-300 are absent from the context packet; that omitted block likely processes canal-source diversion (gw_pond_info(r)%canal / gw_canl_div_info), custom constituent transfer from ch_water, rainfall addition from wst(iwst)%weat%precip, evaporation via wst(iwst)%weat%pet, and per-cell seepage recharge writing cell_recharge to gw_hyd_ss(cell_id)%pond. |
| 8. Accumulate constituent recharge mass to gwsol_ss arrays | Within the per-cell recharge loop, after computing rech_mass_cell(sol_index) for each constituent (lines 301-314): loops s=1..gw_nsolute and assigns gwsol_ss(cell_id)%solute(s)%pond = rech_mass_cell(s), adds to gwsol_ss_sum(cell_id)%solute(s)%pond, and adds to gwsol_ss_sum_mo(cell_id)%solute(s)%pond. |
| 9. Write per-pond daily water and solute balance output | Constructs pond_name via an internal character write (line 334). When gwflag_flux == 1, writes one record to out_pond_bal (format 8100) with date, pond index, label, area, storage, rain, div_added, evap, recharge, specified div, and unsatisfied div. Then loops s=1..gw_nsolute and writes one record per solute to out_pond_sol (format 8101) with solute name, pond solute mass, div_mass(s), and rech_mass(s). |
| 10. Write all-pond solute mass and concentration summaries | After the pond loop, when gwflag_flux == 1: writes NO3 (index 1) and P (index 2) mass rows to out_pond_mass and concentration rows to out_pond_conc for all ponds, computing gw_pond_info(r)%sol_conc(n) = sol_mass(n)*1000/stor (or 0 if stor <= 0). Then loops isalt=1..cs_db%num_salts and ics=1..cs_db%num_cs, advancing sol_index, and writes one mass row and one concentration row per species. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo` | `gw_hyd_ss(cell_id)%pond, gw_hyd_ss_yr(cell_id)%pond, gw_hyd_ss_mo(cell_id)%pond` |
| [sym:hydrograph_module] | `ch_stor` | `ch_stor(chan_id)%flo, ch_stor(chan_id)%no3, ch_stor(chan_id)%solp` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc` |
| [sym:constituent_mass_module] | `cs_db, ch_water` | `cs_db%num_salts, ch_water(chan_id)%salt(isalt), cs_db%num_cs, ch_water(chan_id)%cs(ics)` |
| [sym:water_allocation_module] | `none resolved` | `none resolved` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%precip, wst(iwst)%weat%pet` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_pond_info(r)%div` | gw_pond_div_flag == 1: read from in_ponds at line 57; else zeroed at line 60 | Holds the user-specified daily diversion volume (m3) for pond r. When gw_pond_div_flag == 1, overwritten each day from the pond_div.gw input record; otherwise zeroed. Serves as div_specified at line 80 and is written to out_pond_bal at line 344. |
| `gw_pond_info(r)%div_uns` | gw_pond_info(r)%chan > 0 and gw_daycount >= gw_pond_info(r)%dy_start | Set to div_specified - div_added at line 94. Represents the portion of the requested diversion that could not be supplied because channel storage was insufficient. Written to out_pond_bal at line 345. |
| `ch_stor(chan_id)%flo` | gw_pond_info(r)%chan > 0 and pond is active | Reduced by div_added at line 96: ch_stor(chan_id)%flo = ch_stor(chan_id)%flo - div_added. Records the water volume removed from the channel reach to fill the recharge pond. |
| `gw_pond_info(r)%stor` | Pond is active (multiple conditions: channel diversion line 97, rainfall/evap/recharge in omitted lines) | Increased by div_added at line 97; further modified in omitted lines 131-300 by rainfall addition, evaporation loss, and seepage loss to aquifer cells. Holds end-of-day storage volume (m3) in the pond. |
| `ch_stor(chan_id)%no3` | gw_solute_flag == 1 and chan_volume > 10 and pond is active | Reduced by sol_mass at line 107: ch_stor(chan_id)%no3 = ch_stor(chan_id)%no3 - sol_mass, where sol_mass = (ch_stor(chan_id)%no3*1000/chan_volume * div_added)/1000 capped at available NO3. |
| `gw_pond_info(r)%sol_mass(1)` | gw_solute_flag == 1 and chan_volume > 10 and pond is active | Accumulated by adding NO3 sol_mass from channel at line 108; reduced in omitted lines by recharge loss. Holds current NO3 mass (kg) stored in pond r. |
| `ch_stor(chan_id)%solp` | gw_solute_flag == 1 and chan_volume > 10 and pond is active | Reduced by sol_mass at line 116 using the same proportional pattern as NO3. Records soluble P mass (kg) removed from the channel. |
| `gw_pond_info(r)%sol_mass(2)` | gw_solute_flag == 1 and chan_volume > 10 and pond is active | Accumulated by adding soluble P sol_mass from channel at line 117; reduced in omitted lines by recharge. Holds current soluble P mass (kg) in pond r. |
| `ch_water(chan_id)%salt(isalt)` | gwsol_salt == 1 and gw_solute_flag == 1 and chan_volume > 10 and pond is active | Reduced by sol_mass at line 129: ch_water(chan_id)%salt(isalt) = ch_water(chan_id)%salt(isalt) - sol_mass. Removes salt ion isalt mass proportional to diverted volume. |
| `gw_pond_info(r)%sol_mass(sol_index)` | gwsol_salt == 1 or gwsol_cons == 1, inside per-solute loops | Accumulated at line 130 (salt) and omitted constituent block from channel transfer; reduced at line 310 by recharge: gw_pond_info(r)%sol_mass(sol_index) = gw_pond_info(r)%sol_mass(sol_index) - sol_mass. Tracks current stored mass (kg) for each salt ion or constituent. |
| `ch_water(chan_id)%cs(ics)` | gwsol_cons == 1 and gw_solute_flag == 1 and chan_volume > 10 and pond is active | Reduced in omitted source lines 131-300 by sol_mass proportional to diverted volume, analogous to the salt pattern at line 129. Specific source line not visible in context packet. |
| `gw_canl_div_info(canal_id)%stor` | Canal diversion is active for pond r (omitted source lines 131-300) | Adjusted in omitted lines when the pond's source is a canal diversion. Specific formula not visible in context packet. |
| `gw_canl_div_info(canal_id)%out_pond` | Canal diversion is active for pond r (omitted source lines 131-300) | Set to the volume delivered from the canal to the pond in omitted lines. Zeroed in gwflow_simulate at line 201 before this call. Specific formula not visible in context packet. |
| `gw_hyd_ss(cell_id)%pond` | Pond is active and has connected cells (omitted source lines 131-300) | Set to cell_recharge (m3) for each connected cell in the omitted per-cell loop. Represents daily pond-to-aquifer seepage for this cell; consumed by gwflow_simulate's mass-balance pass. Specific assignment line not visible in context packet. |
| `gw_hyd_ss_yr(cell_id)%pond` | Pond is active and has connected cells (omitted source lines 131-300) | Running annual accumulation of pond seepage per cell, updated in the omitted per-cell loop. Specific assignment line not visible in context packet. |
| `gw_hyd_ss_mo(cell_id)%pond` | Pond is active and has connected cells (omitted source lines 131-300) | Running monthly accumulation of pond seepage per cell, updated in the omitted per-cell loop. Specific assignment line not visible in context packet. |
| `gwsol_ss(cell_id)%solute(s)%pond` | gw_solute_flag == 1 and pond_volume > 0 and pond has connected cells | Assigned rech_mass_cell(s) (g) at line 317: gwsol_ss(cell_id)%solute(s)%pond = rech_mass_cell(s). Daily solute mass recharged from pond to cell; overwrites previous day; consumed by gwflow_simulate. |
| `gwsol_ss_sum(cell_id)%solute(s)%pond` | gw_solute_flag == 1 and pond_volume > 0 and pond has connected cells | Accumulated at line 318: gwsol_ss_sum(cell_id)%solute(s)%pond = gwsol_ss_sum(cell_id)%solute(s)%pond + rech_mass_cell(s). Running cumulative total of pond solute recharge (g) for annual averaging. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%pond` | gw_solute_flag == 1 and pond_volume > 0 and pond has connected cells | Accumulated at line 319: gwsol_ss_sum_mo(cell_id)%solute(s)%pond = gwsol_ss_sum_mo(cell_id)%solute(s)%pond + rech_mass_cell(s). Running monthly total of pond solute recharge (g). |
| `gw_pond_info(r)%sol_conc(1)` | gwflag_flux == 1 and gw_pond_info(r)%stor > 0, after pond loop | Computed at line 368: gw_pond_info(r)%sol_conc(1) = (gw_pond_info(r)%sol_mass(1)*1000.) / gw_pond_info(r)%stor; set to 0 if stor <= 0. End-of-day NO3 concentration (g/m3) in pond r. |
| `gw_pond_info(r)%sol_conc(2)` | gwflag_flux == 1 and gw_pond_info(r)%stor > 0, after pond loop | Computed at line 378: gw_pond_info(r)%sol_conc(2) = (gw_pond_info(r)%sol_mass(2)*1000.) / gw_pond_info(r)%stor; set to 0 if stor <= 0. End-of-day soluble P concentration (g/m3) in pond r. |
| `gw_pond_info(r)%sol_conc(sol_index)` | gwflag_flux == 1 and gw_pond_info(r)%stor > 0, inside salt/constituent loops | Computed at lines 392 and 407: gw_pond_info(r)%sol_conc(sol_index) = (gw_pond_info(r)%sol_mass(sol_index)*1000.) / gw_pond_info(r)%stor; 0 if stor <= 0. End-of-day concentration (g/m3) for the current salt ion or constituent. |

## File I/O

<!-- facts:io -->


## Lineage

Five commits touch gwflow_pond.f90. Commit 9d9069f (2026-03-31) established the module foundation including the groundwater_ss unified source/sink type with its pond field and file renames. Commit 0ece228 (2026-03-31) introduced or substantially reworked the canal and pond processes including gwflow_pond. Commit 7ff5029 (2026-04-02) redesigned output to long format with print.prt integration, likely changing the write statements for out_pond_bal, out_pond_sol, out_pond_mass, and out_pond_conc. Commit b78c4ea (2026-04-04) applied calibration wiring, canal-wallo unification, gfortran portability fixes, and dynamic array sizing; impact on gwflow_pond specifically is unclear from the commit subject. Commit 3cc92b5 (2026-06-02) reworked gwflow input, likely affecting the read(in_ponds,*) logic and gw_pond_div_flag handling.

- {'commit': '9d9069f', 'date': '2026-03-31', 'subject': 'gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renames, heat/pond/phreatophyte types, stubs', 'impact': 'Introduced groundwater_ss type with the pond field (gwflow_module.f90:127) used by gw_hyd_ss, gw_hyd_ss_yr, and gw_hyd_ss_mo; established file naming that gwflow_pond.f90 now resides in.'}
- {'commit': '0ece228', 'date': '2026-03-31', 'subject': 'gwflow re-merge: canal and pond processes - canal, canal_ext, canal_div, pond', 'impact': 'Introduced or substantially rewrote gwflow_pond, including the per-pond loop, channel diversion logic, and per-cell recharge computation.'}
- {'commit': '7ff5029', 'date': '2026-04-02', 'subject': 'gwflow re-merge: output redesign - long format, print.prt integration, standardized output', 'impact': 'Likely redesigned the out_pond_bal, out_pond_sol, out_pond_mass, and out_pond_conc write statements to the current formats 8100, 8101, and 102.'}
- {'commit': 'b78c4ea', 'date': '2026-04-04', 'subject': 'gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes', 'impact': 'Impact on gwflow_pond specifically is unclear from the commit subject; may have adjusted canal-diversion or water-allocation integration pending the wallo unification noted at source line 15.'}
- {'commit': '3cc92b5', 'date': '2026-06-02', 'subject': 'gwflow input rework', 'impact': 'Likely modified the read(in_ponds,*) record format or the handling of gw_pond_div_flag and the pond_div.gw input file.'}

## Review Notes

- algorithm_steps revised: replaced the parser's 2-step decomposition (scan input, store state) with 10 steps matching the actual control flow. Steps 1-6 and 8-10 cite visible source lines; step 7 notes that 170 source lines (131-300) are absent from the context packet, covering canal diversion, rainfall, evaporation, and per-cell seepage — those steps cannot be cited with real line numbers.
- warning: missing_doc: Procedure 'gwflow_pond' has no extracted documentation comment.
- Direct file I/O exists; unit names (in_ponds, out_pond_bal, out_pond_sol, out_pond_mass, out_pond_conc) should be verified against gwflow_module integer unit declarations before finalizing.
- water_allocation_module is imported at line 13 but no outside reference in the context packet was resolved to it. The source comment at line 15 indicates div_conc_cs and div_conc_salt were moved temporarily to gwflow_module; this module's role should be re-evaluated once wallo integration is complete.
- State changes for gw_hyd_ss(cell_id)%pond, gw_hyd_ss_yr/mo, gw_canl_div_info, canal-diversion solute transfer, rainfall, and evaporation are inferred from candidate outside refs and algorithm logic but cannot be confirmed with visible line numbers due to the 170-line omission.
