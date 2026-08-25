---
kind: procedure
symbol: gwflow_canal_div
title: gwflow_canal_div
status: filled
source_hash: 40c82f3605c933bd
version_label: SWAT+ 62.0.0
locals:
  i: Outer loop counter over canal-cell diversion links, and later over canals when writing
    balance output.
  j: Reserved loop counter in the routine; present in declarations but not used in the extracted
    source lines.
  canal_name: Formatted canal label such as `canal_0001`, built from the canal index for output
    records.
  s: Loop counter over groundwater solutes when transferring solute mass and updating solute
    summaries.
  cell_id: Groundwater grid cell connected to the current canal link.
  irec: Recall/diversion record identifier used to look up diversion concentrations for salts
    and constituents.
  sol_index: Running index into the combined groundwater solute list when selecting the output
    solute name and concentration slot.
  ics: Loop counter over non-salt constituents in the canal solute transfer logic.
  isalt: Loop counter over salt ions in the canal solute transfer logic.
  hru_id: Present in the declarations, but the extracted source does not use it after the
    irrigation block was removed.
  canal_id: Index of the current canal object in `gw_canl_div_info`.
  wetland: Declared flag for wetland-related logic, but not used in the extracted source lines.
  dum: Declared scratch integer, but not used in the extracted source lines.
  width: Canal width used to compute seepage area across the canal bed.
  depth: Canal water depth used to derive the canal stage above the bed.
  thick: Canal bed thickness used in the Darcy-style seepage calculation.
  length: Length of canal in the connected cell, used with width to form seepage area.
  stage: Water surface elevation in the canal cell, computed from bed elevation plus depth.
  bed_k: Hydraulic conductivity of the canal bed used to compute exchange rate.
  reduc: Declared numeric scratch variable, but not used in the extracted source lines.
  daycount_real: Declared numeric scratch variable, but not used in the extracted source lines.
  flow_area: Seepage area for the canal-cell exchange, computed as canal length times width.
  canal_bed: Canal bed elevation in the cell, taken from the canal-cell geometry.
  head_diff: Head difference driving the canal-groundwater exchange rate.
  q: Calculated water exchange flux between canal and groundwater cell; positive means canal
    to aquifer, negative means aquifer to canal.
  solmass: Temporary array holding transferred solute mass for each groundwater solute component.
  heat_flux: Temporary heat transfer amount associated with water exchange between canal and
    groundwater.
  canal_area: Declared irrigation-area accumulator from the removed irrigation section; not
    used in the extracted source lines.
  irrig_depth: Declared irrigation-depth variable from the removed irrigation section; not
    used in the extracted source lines.
  irrig_volm: Declared irrigation-volume variable from the removed irrigation section; not
    used in the extracted source lines.
  irrig_conc: Declared irrigation concentration variable from the removed irrigation section;
    not used in the extracted source lines.
  irrig_mass: Declared irrigation mass variable from the removed irrigation section; not used
    in the extracted source lines.
  canal_conc: Concentration value used to convert canal water fluxes into solute mass fluxes
    for output.
  mass_div: Mass associated with the diverted canal inflow for a given solute.
  mass_stor: Mass associated with canal water remaining in storage for a given solute.
  mass_pond: Mass associated with ponded canal water for a given solute.
  mass_seep: Mass associated with seepage water lost from the canal for a given solute.
  mass_irrg: Declared mass variable from the removed irrigation section; not used in the extracted
    source lines.
  mass_ret: Declared return-flow mass variable from the removed irrigation section; not used
    in the extracted source lines.
uses:
  gwflow_module: The groundwater module provides the per-cell groundwater state and summary
    arrays that this routine reads and updates. `gw_state(cell_id)%head` and `%stor` determine
    the seepage direction and limit groundwater withdrawal, while `gw_hyd_ss`, `gw_hyd_ss_yr`,
    `gw_hyd_ss_mo`, `gw_heat_ss`, and `gw_heat_ss_yr` accumulate canal exchange totals that
    later groundwater reporting depends on; `gwflag_flux` controls whether the diagnostic
    output rows are written.
  hydrograph_module: The irrigation transfer array is the destination for the now-removed
    HRU irrigation logic in the source history, and it still marks the water-transfer pathway
    tied to canal diversions. Its presence matters because the routine was reworked away from
    applying canal water to HRUs directly, so the current code’s behavior is best understood
    against that former irrigation linkage.
  time_module: The routine stamps every diagnostic output row with the current simulation
    date. `time%day`, `time%mo`, `time%day_mo`, and `time%yrc` identify when the canal-water
    and solute balance records were produced.
  constituent_mass_module: The constituent database tells the routine how many salt ions and
    other constituents must be handled when building the solute-transfer loops. `cs_db%num_salts`
    and `cs_db%num_cs` control the number of iterations and the mapping into `gwsol_nm(sol_index)`
    for the diagnostic solute output.
  hru_module: The HRU array is the linked land-unit structure that the removed irrigation
    branch used to populate with applied water and runoff. It matters here because the subroutine’s
    historical purpose included routing canal diversions to HRUs, even though that part is
    no longer active in the extracted version.
  res_salt_module: The wetland salt balance output array is part of the broader surface-water/soil
    constituent accounting system that this routine interacts with through solute transfer
    bookkeeping. It matters because the canal exchange routine sits in the same mass-balance
    framework that tracks salt outputs for wetland-related processes.
  res_cs_module: The wetland constituent-balance array serves the same mass-balance role for
    non-salt constituents that `wetsalt_d` does for salts. It matters because this routine’s
    solute handling is integrated with the model-wide constituent accounting structure, even
    though the extracted source only shows canal-specific balance updates.
  salt_module: The salt balance array is the model’s soil-system salt accounting target, and
    this routine updates related solute transfers when canal water exchanges with groundwater.
    It matters because the transferred canal solute mass feeds the salt bookkeeping used elsewhere
    in the model.
  cs_module: The constituent balance array is the counterpart to the salt balance array for
    other constituents. It matters because this routine computes and stores canal-groundwater
    solute exchange for both salt and non-salt constituents.
---

<!-- facts:header -->

Moves water between canal diversions and connected groundwater cells, then writes canal water and solute balance output. Positive seepage is removed from the diverted canal water volume before canal balance records are written.

## Bottom Line

This routine loops over all canal-cell diversion links and computes seepage exchange between each canal and its connected groundwater cell using canal geometry, groundwater head, and canal-bed properties. If the exchange is from canal to groundwater, it reduces the canal diversion storage and records that seepage in the canal water balance; if the exchange is from groundwater to canal, it adds that water to the groundwater store and records the exchange in groundwater source/sink summaries.

It also transfers the corresponding heat and solute mass across the canal-cell boundary, accumulating daily, monthly, and yearly groundwater balance terms. After the flux calculations, it writes diagnostic canal water-balance and solute-balance rows when `gwflag_flux == 1`, using the current date from `time_module` and canal names built from the canal index.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the groundwater simulation step after groundwater and canal-link arrays have been initialized for the day and after `gwflow_pond` has already handled pond seepage. `gwflow_simulate` calls it before the model sums the per-cell groundwater source/sink terms, so its flux updates directly affect the daily groundwater water, heat, and solute balances and the canal diagnostic output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether canal-cell exchange is active | The routine exits immediately unless `gw_canal_flag == 1`, so all canal seepage and output work is conditional on the canal exchange feature being enabled. |
| 2. Loop through each canal-cell diversion link | For each linked canal cell, it identifies the canal and the connected groundwater cell, then skips the cell unless the canal has positive storage and the groundwater cell is active. |
| 3. Load canal and cell geometry | The routine copies canal width, depth, bed thickness, and conductivity plus cell length and bed elevation, then derives the canal stage and seepage area used in the exchange calculation. |
| 4. Compute seepage flux Q | It applies a Darcy-style calculation that uses head position relative to the canal bed and water surface to decide whether flux is from canal to aquifer or aquifer to canal, and it sets the sign of `Q` accordingly. |
| 5. Limit groundwater withdrawal and reduce canal storage when seepage is positive | If `Q < 0`, groundwater water is leaving the cell and the amount is capped by available groundwater storage; if `Q > 0`, canal water is seeping into groundwater, so the routine caps the flux by canal storage, subtracts it from `gw_canl_div_info(canal_id)%stor`, and accumulates it in `gw_canl_div_info(canal_id)%out_seep`. |
| 6. Update groundwater and groundwater-summary water terms | The exchange flux is added to the cell groundwater storage and to the daily, monthly, and yearly canal-related groundwater hydrology summaries. |
| 7. Add heat exchange when groundwater heat is active | If `gw_heat_flag == 1`, negative `Q` is converted into a heat-flux term using groundwater temperature, density, and heat capacity, capped by available heat storage, and added to the daily and yearly canal heat summaries. |
| 8. Compute solute transfer from canal-groundwater exchange | When solute accounting is active, the routine computes per-solute mass transfer for water leaving the cell or entering it from canal concentrations or diversion-record concentrations, then accumulates the result in daily, monthly, and yearly groundwater solute summaries. |
| 9. Loop over canals to write water-balance output | For every canal, it builds `canal_name` and, if `gwflag_flux == 1`, writes a canal water-balance row containing date fields, canal identifiers, and the diversion, storage, pond, and seepage terms. |
| 10. Write salt-constituent mass balance rows | If solute accounting is active, the routine loops through salt ions, computes their mass terms from diversion concentration and the canal fluxes, and writes one solute balance row per salt when flux diagnostics are enabled. |
| 11. Write other-constituent mass balance rows | If non-salt constituents are active, it repeats the concentration-to-mass conversion for each constituent and writes the matching diagnostic rows when `gwflag_flux == 1`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, gwflag_flux` | `gw_state(cell_id)%stat, gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%canl, gw_hyd_ss_yr(cell_id)%canl, gw_hyd_ss_mo(cell_id)%canl, gw_heat_ss(cell_id)%canl, gw_heat_ss_yr(cell_id)%canl` |
| [sym:hydrograph_module] | `irrig` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts, cs_db%num_cs` |
| [sym:hru_module] | `hru` |  |
| [sym:res_salt_module] | `wetsalt_d` |  |
| [sym:res_cs_module] | `wetcs_d` |  |
| [sym:salt_module] | `hsaltb_d` |  |
| [sym:cs_module] | `hcsb_d` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_canl_div_info(canal_id)%stor` | When a canal-cell link has positive seepage flux from the canal into groundwater (`Q > 0`), capped by the canal’s available storage. | The canal’s remaining diversion storage is reduced by the seepage amount so that seepage water is removed from the diverted canal volume before later balances are written. |
| `gw_canl_div_info(canal_id)%out_seep` | When `Q > 0` and the canal has water to lose to seepage. | The routine accumulates the seepage volume in the canal’s seepage-out diagnostic total so the later canal water-balance output reports how much diverted water leaked to groundwater. |
| `gw_state(cell_id)%stor` | For every active canal-cell exchange link after `Q` has been limited. | The cell’s groundwater storage is adjusted by the exchange flux, increasing for canal recharge and decreasing for groundwater discharge to the canal. |
| `gw_hyd_ss(cell_id)%canl` | For every active canal-cell exchange link after `Q` has been limited. | The daily groundwater hydrology summary receives the canal exchange flux so the model can report canal-linked groundwater water fluxes. |
| `gw_hyd_ss_yr(cell_id)%canl` | For every active canal-cell exchange link after `Q` has been limited. | The yearly groundwater hydrology summary accumulates the same canal exchange flux for annual reporting. |
| `gw_hyd_ss_mo(cell_id)%canl` | For every active canal-cell exchange link after `Q` has been limited. | The monthly groundwater hydrology summary accumulates the same canal exchange flux for monthly reporting. |
| `gw_heat_ss(cell_id)%canl` | When `gw_heat_flag == 1` and the flux is from groundwater to canal (`Q < 0`). | The daily groundwater heat summary is updated with the heat carried by water leaving the cell through the canal exchange. |
| `gw_heat_ss_yr(cell_id)%canl` | When `gw_heat_flag == 1` and the flux is from groundwater to canal (`Q < 0`). | The yearly groundwater heat summary is updated with the same canal-exchange heat term for annual reporting. |
| `gwsol_ss(cell_id)%solute(s)%canl` | When `gw_solute_flag == 1` for an active canal-cell exchange link. | The daily groundwater solute summary accumulates the mass transferred between the canal and the groundwater cell for each solute. |
| `gwsol_ss_sum(cell_id)%solute(s)%canl` | When `gw_solute_flag == 1` for an active canal-cell exchange link. | The yearly solute summary accumulates the same canal-transfer mass so annual solute reports include canal exchange. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%canl` | When `gw_solute_flag == 1` for an active canal-cell exchange link. | The monthly solute summary accumulates the same canal-transfer mass so monthly solute reports include canal exchange. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced as a stub in 72aa70a, then 0ece228 expanded it into the canal-seepage and solute-transfer routine with groundwater, heat, and solute bookkeeping. b78c4ea removed the irrigation-to-HRU branch and left only seepage accounting plus canal balance writing, and 7ff5029 added the formatted canal name and switched the diagnostic output to the current long-format records guarded by `gwflag_flux`.

- 72aa70a created the subroutine skeleton but no working behavior.
- 0ece228 implemented canal-groundwater seepage calculations, groundwater/heat/solute summary updates, and diagnostic balance output.
- b78c4ea removed the irrigation application branch and narrowed the routine to seepage and balance reporting.
- 7ff5029 added canal-name formatting and modernized the water and solute output writes to the current record layout.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_canal_div' has no extracted documentation comment.
- algorithm_steps revised: split the original broad output/update steps into explicit seepage, heat, solute, and output-writing phases to match the source lines.
- The extracted source shows `j`, `wetland`, `dum`, `reduc`, `daycount_real`, and the irrigation-related variables declared but unused in the final routine body.
- The optional irrigation branch is absent from the current source lines, but it is visible in lineage history and helps explain some declared locals and dependencies.
