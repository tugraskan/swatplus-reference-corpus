---
kind: procedure
symbol: lsreg_output
title: lsreg_output
status: filled
source_hash: 1c6c3a24c379f77d
version_label: SWAT+ 62.0.0
locals:
  iarea: Temporary integer work array used to mark which land-use database indices appear
    in a region. It is summed to get the number of unique land uses in that region, and then
    reused to drive the region-specific land-use numbering.
  ireg: Loop index for the current landscape output region. It also selects which `region(ireg)`
    and output arrays are being populated or written.
  ielem: Loop index over the HRU numbers stored in `region(ireg)%num`. It walks the member
    HRUs of each region when collecting land-use membership and when accumulating outputs.
  area_ha: Running area accumulator for a region, initialized to zero before region processing.
    In the shown source it is cleared but not otherwise used in the extracted lines, so its
    role is uncertain from this packet alone.
  i: Lower bound used in the `do ielem = i, region(ireg)%num_tot` loop. The source initializes
    it to zero, but the packet does not show it being set elsewhere, so the starting index
    is uncertain.
  ilum: Loop index for land-use classes. It is used both to scan land-use database entries
    and to index region land-use arrays such as `region(ireg)%lum_num`, `region(ireg)%lum_ha`,
    and the regional output arrays.
  nlum: Count of distinct land uses in the current region, and later a scratch counter while
    filling `lum_num` arrays. It is first set from `sum(iarea)` and stored into `region(ireg)%nlum`.
  const: Per-HRU weighting factor for distributing HRU-based outputs to regional land-use
    outputs when `hru(ihru)%land_use_mgt_c` is blank. It is computed as regional land-use
    area divided by HRU area.
  ilum_db: Land-use database index for the current regional land-use entry. It maps region-relative
    land-use slots to the corresponding `lum(ilum_db)` metadata used in output labels.
  constnb: Normalization factor for nutrient-balance and loss average-annual outputs. It is
    `1. / region(ireg)%lum_ha(ilum)` so the accumulated values can be converted from area-weighted
    totals back to per-hectare values.
  icu: Loop/scratch index name declared in the routine but not shown being assigned or used
    in the extracted lines. From the packet alone its role is uncertain.
  constwb: Normalization factor for water-balance average-annual outputs. It is `1. / (10.
    * region(ireg)%lum_ha(ilum))`, converting mm·ha style totals back to the reported regional
    metric.
  constpw: Normalization factor for plant-weather average-annual outputs. It is `region(ireg)%area_ha
    / region(ireg)%lum_ha(ilum)`, used to area-weight outputs that are not per-hectare quantities.
uses:
  time_module: '`time_module` supplies the simulation calendar and period-end flags that control
    when daily, monthly, yearly, and average-annual records are written. `time%day`, `time%mo`,
    `time%day_mo`, `time%yrc`, `time%end_mo`, and `time%end_yr` are embedded in every output
    row and gate the monthly/yearly branches.'
  basin_module: '`basin_module` provides the print-control object `pco`, which determines
    whether daily/monthly/yearly/average-annual outputs are enabled for water balance, nutrient
    balance, losses, plant-weather, and CSV reporting. Without these flags, the routine would
    still accumulate values but would not know which files to write.'
  maximum_data_module: '`maximum_data_module` provides the size limits that bound the region
    and land-use loops. `db_mx%lsu_out` controls how many regions are processed, and `db_mx%landuse`
    defines the land-use scan range and array sizing for `iarea`.'
  calibration_data_module: '`calibration_data_module` holds the regional cataloging-unit structures
    that this routine fills and reads back. `region(ireg)%num_tot`, `num`, `nlum`, `lum_num`,
    `lum_ha`, `name`, `area_ha`, and `lum_ha_tot` define the region''s HRU membership, land-use
    composition, and accumulated land-use area totals.'
  plant_data_module: '`plant_data_module` is included by the routine, but the provided source
    lines do not show any resolved references to symbols from that module. The packet therefore
    does not show a direct role for it in the visible body of `lsreg_output`.'
  landuse_data_module: '`landuse_data_module` supplies `lum`, which provides the land-use
    metadata used in each printed row. The routine uses `lum(ilum_db)%plant_cov` to label
    outputs with the plant community / cover name associated with the regional land-use database
    entry.'
  hru_module: '`hru_module` supplies the HRU array and the active HRU index used to walk region
    membership. `hru(ihru)%land_use_mgt` identifies the land-use database entry for each HRU,
    `area_ha` gives the HRU area for weighting, and `land_use_mgt_c` is used to decide whether
    HRU-based outputs are converted into regional land-use outputs.'
  plant_module: '`plant_module` is included by the routine, but the source lines shown here
    do not contain any resolved references to symbols from it. The visible logic depends on
    output arrays and land-use metadata, not on a plant-module symbol in the extracted packet.'
  output_landscape_module: '`output_landscape_module` provides the regional output arrays
    that this routine fills and prints. The daily, monthly, yearly, and average-annual water
    balance, nutrient balance, loss, and plant-weather structures are all stored in `rwb_*`,
    `rnb_*`, `rls_*`, and `rpw_*` arrays before being written to output units.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is listed in the uses clause,
    but no resolved references to its symbols appear in the extracted source lines. The packet
    does not show a direct dependency on that module in the visible body.'
---

<!-- facts:header -->

Aggregates and prints regional landscape outputs by land-use class. It tracks daily, monthly, yearly, and average-annual water balance, nutrient balance, loss, and plant-weather summaries for each region and land use.

## Bottom Line

`lsreg_output` builds the land-use structure for each output region, then accumulates and prints regional summaries for water balance, nutrient balance, losses, and plant-weather variables. It writes both formatted text records and optional CSV records, using the region's land-use database mapping to label each output row.

The routine matters because it is the reporting bridge between HRU-level state and region-level landscape output files. It also resets and deallocates period-specific arrays at the right times, and maintains average-annual totals that are normalized by the number of years in the averaging window.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`lsreg_output` runs after the simulation has updated HRU-, land-use-, and regional-output state for the current time step, and it uses `pco` and `time` to decide which summaries to emit. The upstream setup that matters here is the region/HRU mapping and output-array allocation; later model behavior depends on the accumulated regional output totals and on the files this routine writes for postprocessing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Allocate and reset scratch land-use tracking | The routine allocates `iarea` to the number of land-use database entries and zeros it at the start of the yearly-reset branch. This scratch array is used to discover which land uses are present in each region. |
| 2. Count unique land uses in each region | For each output region, the routine walks the HRU list in `region(ireg)%num`, marks each land-use database index seen in `iarea`, counts the unique entries with `sum(iarea)`, and stores the count in `region(ireg)%nlum`. |
| 3. Allocate region-specific output arrays | Using the region's land-use count, the routine allocates the daily, monthly, yearly, and average-annual output arrays for water balance, nutrient balance, losses, and plant-weather summaries. |
| 4. Build the region land-use index list | The routine resets the scratch array and fills `region(ireg)%lum_num` with the land-use database numbers that occur in the region. This produces a compact sequential list of land uses for later printing. |
| 5. Compute land-use area within each region | The routine clears `region(ireg)%lum_ha` and then accumulates HRU areas into the matching land-use slot whenever an HRU's management code matches a regional land-use number. |
| 6. Map HRU outputs to regional land-use outputs | For each HRU and each regional land-use slot, the routine checks whether the HRU has no custom land-use label and, if so, distributes the HRU's water-balance outputs into the regional land-use arrays using an area ratio stored in `const`. |
| 7. Write daily regional output records when enabled | If daily printing is enabled and the daily interval matches, the routine writes the daily water-balance, nutrient-balance, losses, and plant-weather records to their text and optional CSV units for each region-land-use pair. |
| 8. Accumulate monthly outputs | When the month ends, the routine normalizes monthly regional outputs by land-use area and adds them into the monthly summary arrays before any monthly writes occur. The packet shows the monthly branch using the same regional arrays that are later written to output units. |
| 9. Accumulate yearly outputs | At the end of the year, the routine adds the current period values into the yearly output arrays for water balance, nutrient balance, losses, and plant-weather. If yearly printing is enabled, it writes the yearly records to the corresponding units and optional CSV streams. |
| 10. Reset period arrays after yearly output | After yearly output is written, the routine deallocates the daily, monthly, and yearly subarrays for each region so the next cycle can reallocate them with the correct land-use count. |
| 11. Build average-annual land-use coverage | When average-annual printing is due, the routine re-identifies land uses that have non-negligible total area across years, stores the count in the region structure, and records the corresponding land-use database numbers for the average-annual output list. |
| 12. Normalize and write average-annual outputs | For each average-annual land-use slot, the routine divides accumulated totals by the number of years in the print interval, writes the average-annual water-balance, nutrient-balance, losses, and plant-weather records, and then resets the average-annual accumulators to their zero-state sentinels. |
| 13. Release scratch storage and finish | The routine deallocates `iarea`, returns to the caller, and ends after the format labels used by the writes. The final labels are part of the source file but not runtime logic. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%wb_hru%d, pco%csvout, pco%nb_hru%d, pco%ls_hru%d, pco%pw_hru%d, pco%wb_hru%m, pco%nb_hru%m, pco%ls_hru%m, pco%pw_hru%m, pco%wb_hru%y, pco%nb_hru%y, pco%ls_hru%y, pco%pw_hru%y` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%landuse, db_mx%lsu_out` |
| [sym:calibration_data_module] | `region` | `region(ireg)%num_tot, region(ireg)%num(ielem), region(ireg)%nlum, region(ireg)%lum_num(nlum), region(ireg)%lum_ha, region(ireg)%lum_num(ilum), region(ireg)%lum_ha(ilum), region(ireg)%name, region(ireg)%area_ha, region(ireg)%lum_ha_tot(ilum_db)` |
| [sym:plant_data_module] | `No imported state from `plant_data_module` is used in the extracted lines.` | `[]` |
| [sym:landuse_data_module] | `lum` | `lum(ilum_db)%plant_cov` |
| [sym:hru_module] | `hru` | `hru(ihru)%land_use_mgt, hru(ihru)%area_ha, hru(ihru)%land_use_mgt_c` |
| [sym:plant_module] | `No imported state from `plant_module` is used in the extracted lines.` | `[]` |
| [sym:output_landscape_module] | `rwb_d, rwb_m, rwb_y, rnb_d, rnb_m, rnb_y, rls_d, rls_m, rls_y, rpw_d, rpw_m, rpw_y, rwb_a, rnb_a, rls_a, rpw_a` | `rwb_d(ireg)%lum(nlum), rwb_m(ireg)%lum(nlum), rwb_y(ireg)%lum(nlum), rnb_d(ireg)%lum(nlum), rnb_m(ireg)%lum(nlum), rnb_y(ireg)%lum(nlum), rls_d(ireg)%lum(nlum), rls_m(ireg)%lum(nlum), rls_y(ireg)%lum(nlum), rpw_d(ireg)%lum(nlum), rpw_m(ireg)%lum(nlum), rpw_y(ireg)%lum(nlum), rwb_d(ireg)%lum(ilum), rwb_m(ireg)%lum(ilum), rwb_y(ireg)%lum(ilum), rwb_a(ireg)%lum(ilum), rnb_d(ireg)%lum(ilum), rls_d(ireg)%lum(ilum), rpw_d(ireg)%lum(ilum), rpw_m(ireg)%lum(ilum), rwb_m(ireg)%lum(ilum)%cn, rwb_m(ireg)%lum(ilum)%sw, rwb_m(ireg)%lum(ilum)%sw_300, rnb_y(ireg)%lum(ilum), rnb_m(ireg)%lum(ilum), rls_y(ireg)%lum(ilum), rls_m(ireg)%lum(ilum), rpw_y(ireg)%lum(ilum), rwb_y(ireg)%lum(ilum)%cn, rwb_y(ireg)%lum(ilum)%sw, rwb_y(ireg)%lum(ilum)%sw_300, rwb_a(ireg)%lum(ilum_db), rnb_a(ireg)%lum(ilum_db), rls_a(ireg)%lum(ilum_db), rpw_a(ireg)%lum(ilum_db), rwb_d(ireg)%lum, rwb_m(ireg)%lum, rwb_y(ireg)%lum, rnb_d(ireg)%lum, rnb_m(ireg)%lum, rnb_y(ireg)%lum, rls_d(ireg)%lum` |
| [sym:organic_mineral_mass_module] | `No imported state from `organic_mineral_mass_module` is used in the extracted lines.` | `[]` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ihru` | When scanning each region's HRU membership in the region setup branch, the routine assigns `ihru = region(ireg)%num(ielem)` for each member HRU. | `ihru` becomes the current HRU index being processed. It is used immediately to look up land-use management and area information for land-use counting, area accumulation, and output aggregation. |
| `region(ireg)%nlum` | When `time%day == 1`, after counting distinct land uses in a region, the routine stores `nlum = sum(iarea)` into `region(ireg)%nlum`. | `region(ireg)%nlum` holds the number of distinct land-use classes present in the region for the current year. That count controls allocation and looping for all region-specific output arrays. |
| `region(ireg)%lum_num(nlum)` | Still in the yearly reset branch, after resetting `nlum = 1` and scanning `iarea`, the routine fills `region(ireg)%lum_num(nlum) = ilum` for each marked land-use database entry. | `region(ireg)%lum_num(nlum)` becomes the ordered list of land-use database IDs present in the region. Later output rows use this mapping to pull `lum(ilum_db)%plant_cov` and other labels. |
| `region(ireg)%lum_ha` | When `time%day == 1`, before accumulating HRU areas, the routine zeros `region(ireg)%lum_ha` and then adds each matching HRU's `area_ha` to the appropriate land-use slot. | `region(ireg)%lum_ha` becomes the per-land-use area summary for the region. It is used to weight HRU outputs into regional land-use outputs and to print the land-use area columns. |
| `region(ireg)%lum_ha(ilum)` | During the yearly reset branch, for each HRU/land-use match the routine updates `region(ireg)%lum_ha(ilum) = region(ireg)%lum_ha(ilum) + hru(ihru)%area_ha`. | Each `region(ireg)%lum_ha(ilum)` slot accumulates the hectares associated with that land-use class in the region. These values are the basis for the output weighting and the printed area columns. |
| `rwb_d(ireg)%lum(ilum)` | When `hru(ihru)%land_use_mgt_c == '                '` in the regional HRU-to-land-use mapping branch, the routine computes `const = region(ireg)%lum_ha(ilum) / hru(ihru)%area_ha` and divides the HRU water-balance outputs by it. | `rwb_d(ireg)%lum(ilum)` is filled with the daily regional water-balance contribution for the current land-use slot. It represents the HRU value scaled to the regional land-use share. |
| `rwb_m(ireg)%lum(ilum)` | Under the same HRU-mapping condition, the routine sets `rwb_m(ireg)%lum(ilum) = hwb_m(ihru) / const`. | `rwb_m(ireg)%lum(ilum)` becomes the monthly regional water-balance value for the land-use slot, scaled from the HRU-level monthly water balance. |
| `rwb_y(ireg)%lum(ilum)` | Under the same HRU-mapping condition, the routine sets `rwb_y(ireg)%lum(ilum) = hwb_y(ihru) / const`. | `rwb_y(ireg)%lum(ilum)` becomes the yearly regional water-balance value for the land-use slot, scaled from the HRU-level yearly water balance. |
| `rwb_a(ireg)%lum(ilum)` | Under the same HRU-mapping condition, the routine sets `rwb_a(ireg)%lum(ilum) = hwb_a(ihru) / const`. | `rwb_a(ireg)%lum(ilum)` becomes the average-annual regional water-balance value for the land-use slot, scaled from the HRU-level accumulated water balance. |
| `rpw_m(ireg)%lum(ilum)` | In the regional HRU-mapping branch, the routine assigns `rwb_m(ireg)%lum(ilum)` from the HRU monthly water-balance state when the land-use-management label is blank. | `rpw_m(ireg)%lum(ilum)` receives the monthly plant-weather summary for the land-use slot. The packet does not show the exact assignment line in the excerpted lines, but the yearly and average-annual plant-weather accumulation branch uses the same regional output family. |
| `rwb_m(ireg)%lum(ilum)%cn` | After annual values are accumulated for water balance, the routine normalizes `rwb_m(ireg)%lum(ilum)%cn` by the regional land-use area in the annual/period branch. | `rwb_m(ireg)%lum(ilum)%cn` holds the area-weighted curve-number summary for the land-use slot. It is a regional reporting quantity used in water-balance output. |
| `rwb_m(ireg)%lum(ilum)%sw` | After annual values are accumulated for water balance, the routine normalizes `rwb_m(ireg)%lum(ilum)%sw` by the regional land-use area in the annual/period branch. | `rwb_m(ireg)%lum(ilum)%sw` holds the average soil-water content for the land-use slot in regional output form. |
| `rwb_m(ireg)%lum(ilum)%sw_300` | After annual values are accumulated for water balance, the routine normalizes `rwb_m(ireg)%lum(ilum)%sw_300` by the regional land-use area in the annual/period branch. | `rwb_m(ireg)%lum(ilum)%sw_300` holds the average water content in the upper 300 mm for the land-use slot in regional output form. |
| `rnb_y(ireg)%lum(ilum)` | When the yearly branch accumulates nutrient-balance output for a land-use slot, the routine updates `rnb_y(ireg)%lum(ilum)` before writing annual output. | `rnb_y(ireg)%lum(ilum)` becomes the yearly nutrient-balance summary for the region-land-use slot, ready for reporting and later normalization. |
| `rls_y(ireg)%lum(ilum)` | When the yearly branch accumulates losses output for a land-use slot, the routine updates `rls_y(ireg)%lum(ilum)` before writing annual output. | `rls_y(ireg)%lum(ilum)` becomes the yearly losses summary for the region-land-use slot, used for annual reporting. |
| `rpw_y(ireg)%lum(ilum)` | When the yearly branch accumulates plant-weather output for a land-use slot, the routine updates `rpw_y(ireg)%lum(ilum)` before writing annual output. | `rpw_y(ireg)%lum(ilum)` becomes the yearly plant-weather summary for the region-land-use slot, used in yearly reporting. |
| `rnb_m(ireg)%lum(ilum)` | When the yearly branch accumulates nutrient-balance output for a land-use slot, the routine updates `rnb_m(ireg)%lum(ilum)` for the monthly period. | `rnb_m(ireg)%lum(ilum)` stores the monthly nutrient-balance summary for the region-land-use slot. |
| `rls_m(ireg)%lum(ilum)` | When the yearly branch accumulates losses output for a land-use slot, the routine updates `rls_m(ireg)%lum(ilum)` for the monthly period. | `rls_m(ireg)%lum(ilum)` stores the monthly losses summary for the region-land-use slot. |
| `rwb_y(ireg)%lum(ilum)%cn` | During the annual normalization branch for water balance, the routine updates `rwb_y(ireg)%lum(ilum)%cn` from the accumulated regional values. | `rwb_y(ireg)%lum(ilum)%cn` holds the yearly curve-number summary for the land-use slot. |
| `rwb_y(ireg)%lum(ilum)%sw` | During the annual normalization branch for water balance, the routine updates `rwb_y(ireg)%lum(ilum)%sw` from the accumulated regional values. | `rwb_y(ireg)%lum(ilum)%sw` holds the yearly average soil-water content for the land-use slot. |
| `rwb_y(ireg)%lum(ilum)%sw_300` | During the annual normalization branch for water balance, the routine updates `rwb_y(ireg)%lum(ilum)%sw_300` from the accumulated regional values. | `rwb_y(ireg)%lum(ilum)%sw_300` holds the yearly upper-300-mm soil-water summary for the land-use slot. |
| `region(ireg)%lum_ha_tot(ilum_db)` | In the average-annual branch, when `region(ireg)%lum_ha_tot(ilum)` exceeds the non-negligible threshold, the routine marks the land-use database entry in the annual scratch array and later normalizes `region(ireg)%lum_ha_tot(ilum)` by `time%yrs_prt_int`. | `region(ireg)%lum_ha_tot(ilum_db)` becomes the accumulated land-use area for average-annual reporting over the print interval. It is later divided by the number of years in the interval before output. |
| `rwb_a(ireg)%lum(ilum_db)` | When `time%end_aa_prt == 1` and `pco%wb_hru%a == 'y'`, the routine divides `rwb_a(ireg)%lum(ilum)` by `time%yrs_prt_int` before writing average-annual water-balance output. | `rwb_a(ireg)%lum(ilum)` becomes the normalized average-annual water-balance value for the land-use slot. It is then reset to `hwbz` after writing. |
| `rnb_a(ireg)%lum(ilum_db)` | When `time%end_aa_prt == 1` and `pco%nb_hru%a == 'y'`, the routine divides `rnb_a(ireg)%lum(ilum)` by `time%yrs_prt_int` before writing average-annual nutrient-balance output. | `rnb_a(ireg)%lum(ilum)` becomes the normalized average-annual nutrient-balance value for the land-use slot. It is then reset to `hnbz` after writing. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `lsreg_output`: `df07e3f` added the routine with its region/land-use aggregation and output branches; `94b6dec` imported the same initial source body into the SWAT+ tree; `39fabde` initialized local scalars, changed `iarea` allocation to zero-fill, and expanded output allocation layout; `889136d` fixed the `constpw` comment typo; `2fe89fd` changed several CSV `G0.3` formats to `G0.6` for higher-precision CSV output; `dab22e1` only commented out an unused format label and did not change runtime behavior.

- `df07e3f` introduced the full `lsreg_output` routine, including land-use discovery, regional aggregation, and the daily/yearly/average-annual output writes.
- `39fabde` made the routine safer by initializing local scalars and zero-filling `iarea` on allocation, which affects region land-use counting and prevents stale scratch values.
- `889136d` did not change behavior; it only corrected a comment on `constpw`.
- `2fe89fd` changed CSV precision from `G0.3` to `G0.6` on the regional CSV write statements, affecting the textual precision of exported values.
- `dab22e1` did not change runtime behavior; it only marked an unused format label as commented out.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'lsreg_output' has no extracted documentation comment.
- plant_data_module and organic_mineral_mass_module are used in the USE list but no resolved symbol references from those modules appear in the extracted source lines.
- Some monthly/annual branch details are inferred from the visible control flow and output writes; the packet truncates a middle portion of the source body, so the exact month-branch source lines are partially omitted in the provided context.
