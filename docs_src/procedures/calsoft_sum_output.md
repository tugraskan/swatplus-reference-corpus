---
kind: procedure
symbol: calsoft_sum_output
title: calsoft_sum_output
status: filled
source_hash: 406e65156604bd16
version_label: SWAT+ 62.0.0
locals:
  ireg: Region index used to loop over landscape calibration regions (`db_mx%lsu_reg`) and
    channel calibration regions (`db_mx%ch_reg`).
  ilu: Index of the land-use / management class within each region (`region(ireg)%nlum`).
  iord: Index of the stream-order calibration group within a channel region (`chcal(ireg)%ord_num`).
  ihru_s: Loop counter over HRUs listed in a region (`region(ireg)%num_tot`); used to map
    region membership to the current HRU index.
  ich: Actual channel index pulled from a region's channel list (`chcal(ireg)%num(ich_s)`)
    before its output is read.
  ich_s: Loop counter over the channels assigned to a channel calibration region (`chcal(ireg)%num_tot`).
  ha_hru: Area weight for the current HRU, taken from `region(ireg)%hru_ha(ihru)` for HRU
    calibration and scaled by 10 in the HRU_LTE branch; it is the factor used to convert per-area
    outputs into summed volumes or loads.
uses:
  sd_channel_module: '`sd_channel_module` provides the channel geometry (`sd_ch`) and yearly
    channel-degradation outputs (`chsd_y`) that the channel-calibration branch converts into
    length-weighted summary statistics. Without `sd_ch(ich)%chl` and `sd_ch(ich)%chw`, the
    routine could not accumulate channel length or normalize bank widening against channel
    width.'
  hru_lte_module: '`hru_lte_module` matters because the HRU_LTE branch summarizes yearly water-balance
    and sediment outputs from the LTE landscape tables. `hltwb_y` supplies precipitation,
    runoff, lateral flow, percolation, ET, and tile flow; `hltls_y` supplies sediment yield.'
  hru_module: '`hru_module` supplies the active HRU list and HRU attributes needed to decide
    which units contribute to a given calibration land-use group. `hru(ihru)%lum_group_c`
    is the matching label, and `hru(ihru)%irr` excludes irrigated HRUs from the HRU soft-calibration
    sums.'
  output_landscape_module: '`output_landscape_module` supplies the yearly landscape output
    structures whose fields are being accumulated. The routine reads these containers to build
    annual sums of water balance and sediment terms for both standard HRUs and HRU_LTE units.'
  maximum_data_module: '`maximum_data_module` provides the region-count limits that bound
    the outer loops. `db_mx%lsu_reg` controls how many landscape regions are processed, and
    `db_mx%ch_reg` controls how many channel calibration regions are processed.'
  calibration_data_module: '`calibration_data_module` holds the calibration flags, region
    membership tables, and the target summary containers that this routine updates. `cal_codes`
    turns each branch on or off, `region` maps HRUs to landscape calibration regions, `lscal`
    and `lscalt` store landscape summaries, and `chcal` stores channel summaries for later
    soft-calibration comparisons.'
---

<!-- facts:header -->

Aggregates yearly HRU, HRU_LTE, and channel outputs into soft-calibration summary totals by region and land-use group. The results are converted to average-annual values for later calibration comparisons.

## Bottom Line

`calsoft_sum_output` is an end-of-year summarizer for soft calibration. It walks the configured landscape regions and, when the corresponding calibration flags are enabled, accumulates simulated water-balance and sediment outputs from HRUs or HRU_LTE units into the landscape calibration containers `lscal` and `lscalt`. It also has a separate branch that summarizes channel widening/bank-change outputs into `chcal` when channel-sediment calibration is the only active mode.

The routine matters because it turns daily output arrays like `hwb_y`, `hls_y`, `hltwb_y`, `hltls_y`, `chsd_y`, and structural metadata from `hru`, `region`, `sd_ch`, and `chcal` into annualized calibration sums and averages. Those values are then used by the soft-calibration workflow to compare model behavior against measured targets and to update calibration summaries year by year.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`time_control` calls this routine at the end of the yearly loop, after daily model processes and outputs have been completed for the year. The routine depends on those prepared yearly outputs to accumulate annual soft-calibration summaries, and later calibration logic uses the updated `lscal`, `lscalt`, and `chcal` averages to compare simulated behavior against measured targets.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether landscape calibration should run. | The routine first tests `cal_codes%hyd_hru` and `cal_codes%hyd_hrul` to decide whether to process HRU-based or HRU_LTE-based soft calibration summaries. |
| 2. Loop through landscape calibration regions and land-use groups for HRU outputs. | For each landscape region (`ireg`) and land-use class (`ilu`), it clears the yearly accumulation fields in `lscal(ireg)%lum(ilu)` and then prepares to scan all HRUs assigned to that region. |
| 3. Map each region member to the active HRU and test whether it belongs to the current calibration group. | The routine sets `ihru` from `region(ireg)%num(ihru_s)` and includes the HRU only when its land-use group matches `lscal(ireg)%lum(ilu)%meas%name` or when the calibration target is basin-wide; irrigated HRUs are skipped in this branch. |
| 4. Accumulate HRU water-balance and sediment totals with area weighting. | For each selected non-irrigated HRU, the routine computes `ha_hru` from `region(ireg)%hru_ha(ihru)` and adds area-weighted precipitation, PET, runoff, lateral flow, percolation, ET, tile flow, baseflow, water yield, and sediment into `lscal(ireg)%lum(ilu)%sim` and related totals. |
| 5. Convert HRU sums to average-annual values when the land-use total area is nonzero. | If `lscal(ireg)%lum(ilu)%ha` exceeds the tiny threshold, the routine increments `nbyr` and converts the accumulated sums back to average-annual precipitation, PET, runoff, flow ratios, and sediment metrics in `lscal(ireg)%lum(ilu)%aa` and `precip_aa`/`pet_aa`. |
| 6. Check whether HRU_LTE calibration should run. | A second branch executes only when `cal_codes%hyd_hrul` is enabled, indicating that HRU_LTE-based water-balance calibration should be summarized instead of or in addition to standard HRUs. |
| 7. Loop through landscape calibration regions and land-use groups for HRU_LTE outputs. | For each region and land-use class, the routine resets `lscalt(ireg)%lum(ilu)` accumulation fields before scanning the region's member HRUs. |
| 8. Accumulate HRU_LTE water-balance and sediment totals with area weighting. | The routine maps each region member into `ihru`, computes an area weight from `region(ireg)%hru_ha(ihru)`, and sums HRU_LTE precipitation, runoff, lateral flow, percolation, ET, tile flow, and sediment from `hltwb_y` and `hltls_y` into `lscalt(ireg)%lum(ilu)%sim`. |
| 9. Convert HRU_LTE sums to average-annual values when the land-use total area is nonzero. | When `lscalt(ireg)%lum(ilu)%ha` is positive, the routine increments `nbyr` and converts the summed quantities into average-annual precipitation and process ratios in `lscalt(ireg)%lum(ilu)%aa`. |
| 10. Check whether channel sediment calibration should run. | The channel branch runs only when channel-sediment calibration is enabled and landscape calibration modes are disabled, matching the routine's use as a dedicated channel soft-calibration summarizer. |
| 11. Loop through channel regions and stream-order groups. | For each channel region and order group, the routine clears `chcal(ireg)%ord(iord)` so it can accumulate new yearly channel statistics. |
| 12. Accumulate length-weighted channel widening and related measures. | For every channel assigned to the region, the routine looks up `ich`, checks for the basin measurement target, and adds channel length plus length-weighted widening, downcutting, headcut retreat, and floodplain depth terms into `chcal(ireg)%ord(iord)%sim`. |
| 13. Convert channel sums to average-annual values by channel length. | If the total channel length is nonzero, the routine increments `nbyr` and divides the simulated channel sums by total length to update the annual average fields in `chcal(ireg)%ord(iord)%aa`. |
| 14. Return to the caller after all selected summaries are updated. | The routine ends without direct file I/O or further calls; its effect is the updated calibration summary state stored in the module arrays. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sd_ch, chsd_y` | `sd_ch(ich)%chl, chsd_y(ich)%deg_bank_m, sd_ch(ich)%chw` |
| [sym:hru_lte_module] | `hru_lte_module` | `hltwb_y, hltls_y` |
| [sym:hru_module] | `hru` | `hru(ihru)%lum_group_c, hru(ihru)%irr` |
| [sym:output_landscape_module] | `hwb_y, hls_y, hltwb_y, hltls_y` | `hwb_y(ihru)%precip, hwb_y(ihru)%irr, hwb_y(ihru)%pet, hwb_y(ihru)%surq_gen, hwb_y(ihru)%latq, hwb_y(ihru)%perc, hwb_y(ihru)%et, hwb_y(ihru)%qtile, hls_y(ihru)%sedyld, hltwb_y(ihru)%precip, hltwb_y(ihru)%surq_gen, hltwb_y(ihru)%latq, hltwb_y(ihru)%perc, hltwb_y(ihru)%et, hltwb_y(ihru)%qtile, hltls_y(ihru)%sedyld` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg, db_mx%ch_reg` |
| [sym:calibration_data_module] | `cal_codes, region, lscal, lscalt, chcal` | `cal_codes%hyd_hru, cal_codes%hyd_hrul, region(ireg)%nlum, lscal(ireg)%lum(ilu)%ha, lscal(ireg)%lum(ilu)%precip, lscal(ireg)%lum(ilu)%pet, lscal(ireg)%lum(ilu)%sim, region(ireg)%num_tot, region(ireg)%num(ihru_s), lscal(ireg)%lum(ilu)%meas%name, region(ireg)%hru_ha(ihru), lscal(ireg)%lum(ilu)%sim%srr, lscal(ireg)%lum(ilu)%sim%lfr, lscal(ireg)%lum(ilu)%sim%pcr, lscal(ireg)%lum(ilu)%sim%etr, lscal(ireg)%lum(ilu)%sim%tfr, lscal(ireg)%lum(ilu)%sim%bfr, lscal(ireg)%lum(ilu)%sim%wyr, lscal(ireg)%lum(ilu)%sim%sed, lscal(ireg)%lum(ilu)%nbyr, lscal(ireg)%lum(ilu)%precip_aa, lscal(ireg)%lum(ilu)%pet_aa, lscal(ireg)%lum(ilu)%aa%srr, lscal(ireg)%lum(ilu)%aa%lfr, lscal(ireg)%lum(ilu)%aa%pcr, lscal(ireg)%lum(ilu)%aa%etr, lscal(ireg)%lum(ilu)%aa%tfr, lscal(ireg)%lum(ilu)%aa%bfr, lscal(ireg)%lum(ilu)%aa%wyr, lscal(ireg)%lum(ilu)%aa%sed, lscalt(ireg)%lum(ilu)%ha, lscalt(ireg)%lum(ilu)%precip, lscalt(ireg)%lum(ilu)%sim, lscalt(ireg)%lum(ilu)%sim%srr, lscalt(ireg)%lum(ilu)%sim%lfr, lscalt(ireg)%lum(ilu)%sim%pcr, lscalt(ireg)%lum(ilu)%sim%etr, lscalt(ireg)%lum(ilu)%sim%tfr, lscalt(ireg)%lum(ilu)%sim%sed, lscalt(ireg)%lum(ilu)%nbyr, lscalt(ireg)%lum(ilu)%precip_aa, lscalt(ireg)%lum(ilu)%aa%srr, lscalt(ireg)%lum(ilu)%aa%lfr, lscalt(ireg)%lum(ilu)%aa%pcr, lscalt(ireg)%lum(ilu)%aa%etr, lscalt(ireg)%lum(ilu)%aa%tfr, lscalt(ireg)%lum(ilu)%aa%sed, cal_codes%chsed, cal_codes%sed, cal_codes%plt, chcal(ireg)%ord_num, chcal(ireg)%ord(iord)%length, chcal(ireg)%ord(iord)%sim, chcal(ireg)%num_tot, chcal(ireg)%num(ich_s), chcal(ireg)%ord(iord)%meas%name, chcal(ireg)%ord(iord)%sim%chw` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lscal(ireg)%lum(ilu)%ha` | When `cal_codes%hyd_hru /= 'n' .or. cal_codes%hyd_hrul == 'y'` and the code is inside the HRU branch, before scanning HRUs in a region. | Resets each landscape land-use summary's accumulated area to zero so the yearly HRU sums can be rebuilt from the current year's outputs. |
| `lscal(ireg)%lum(ilu)%precip` | When `cal_codes%hyd_hru /= 'n' .or. cal_codes%hyd_hrul == 'y'` and the code is inside the HRU branch, before scanning HRUs in a region. | Clears the accumulated precipitation sum so yearly HRU precipitation can be re-added from `hwb_y(ihru)%precip` plus irrigation input. |
| `lscal(ireg)%lum(ilu)%pet` | When `cal_codes%hyd_hru /= 'n' .or. cal_codes%hyd_hrul == 'y'` and the code is inside the HRU branch, before scanning HRUs in a region. | Clears the accumulated PET sum so yearly HRU PET can be re-summed from `hwb_y(ihru)%pet`. |
| `lscal(ireg)%lum(ilu)%sim` | When `cal_codes%hyd_hru /= 'n' .or. cal_codes%hyd_hrul == 'y'` and the code is inside the HRU branch, before scanning HRUs in a region. | Resets the full simulated-process summary record so the year’s runoff, flow, ET, and sediment totals are written from scratch into `lscal(ireg)%lum(ilu)%sim`. |
| `ihru` | For each HRU member processed in the HRU branch, after `ihru = region(ireg)%num(ihru_s)`. | `ihru` is reassigned to the current region member so the routine can read the correct HRU outputs and metadata. |
| `lscal(ireg)%lum(ilu)%sim%srr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's area-weighted surface runoff to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%lfr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's area-weighted lateral flow to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%pcr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's area-weighted percolation to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%etr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's area-weighted actual evapotranspiration to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%tfr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's area-weighted tile flow to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%bfr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's combined baseflow-like term, computed from lateral flow, percolation, and tile flow, to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%wyr` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's total water yield term, computed from surface runoff, lateral flow, percolation, and tile flow, to the simulated annual sum used for calibration. |
| `lscal(ireg)%lum(ilu)%sim%sed` | When a selected non-irrigated HRU contributes to the HRU branch. | Adds the current HRU's sediment yield, weighted by HRU area, to the simulated annual sediment sum. |
| `lscal(ireg)%lum(ilu)%nbyr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Increments the number of simulated years contributing to the HRU calibration average. |
| `lscal(ireg)%lum(ilu)%precip_aa` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized precipitation total to the average-annual precipitation accumulator so later calibration can compare mm-equivalent values. |
| `lscal(ireg)%lum(ilu)%pet_aa` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized PET total to the average-annual PET accumulator. |
| `lscal(ireg)%lum(ilu)%aa%srr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized surface-runoff ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%lfr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized lateral-flow ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%pcr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized percolation ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%etr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized ET ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%tfr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized tile-flow ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%bfr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized baseflow ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%wyr` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized water-yield ratio to the average-annual simulated-process record. |
| `lscal(ireg)%lum(ilu)%aa%sed` | When the HRU branch has accumulated a positive area total for the current land-use class. | Adds the area-normalized sediment yield to the average-annual simulated-process record. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved for `calsoft_sum_output`. The routine was added in `df07e3f` with the full HRU, HRU_LTE, and channel soft-calibration summation logic; `39fabde` only initialized the local counters and area scalar; `10e5ddc` narrowed the channel branch so order summaries now run only when the measurement name is `basin`.

- `df07e3f` introduced the routine and its three accumulation branches: HRU landscape summaries, HRU_LTE summaries, and channel-order summaries, including the annual normalization into `aa` fields.
- `39fabde` changed only local variable initialization, setting `ireg`, `ilu`, `iord`, `ihru_s`, `ich`, `ich_s`, and `ha_hru` to zero at declaration; the summation behavior stayed the same.
- `10e5ddc` removed the `meas%name == sd_ch(ich)%order` condition from the channel branch so channel-order aggregation now occurs only when `chcal(ireg)%ord(iord)%meas%name == 'basin'`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_sum_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps to cover the HRU, HRU_LTE, and channel branches separately.
- Source evidence shows `hru_lte_module` is imported but no specific symbols were isolated by the candidate reference extractor; the only visible uses are the `hltwb_y` and `hltls_y` arrays in the source.
