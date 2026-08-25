---
kind: procedure
symbol: calsoft_ave_output
title: calsoft_ave_output
status: filled
source_hash: 4d877620765c34e3
version_label: SWAT+ 62.0.0
locals:
  ireg: Loop index for the calibration region being processed. It runs across the configured
    landscape, plant, or channel calibration regions depending on which calibration mode is
    active.
  ilu: Loop index for the land-use or management unit within the current region. It selects
    the specific `lum` entry whose accumulated calibration totals are being averaged.
  ich: Loop index for the channel stream-order entry within the current region. It selects
    the specific channel calibration record to normalize.
uses:
  sd_channel_module: The routine includes `sd_channel_module` because the channel calibration
    branch works with channel soft-calibration state (`chcal`) and must be compiled with the
    channel-output definitions that support that workflow, even though no direct component
    from this module was isolated in the packet.
  hru_lte_module: The routine includes `hru_lte_module` because the `hyd_hrul` branch averages
    landscape calibration values for the hru_lte calibration path, and that path depends on
    module state defined with the hru_lte implementation.
  maximum_data_module: '`maximum_data_module` supplies `db_mx`, which provides the region-count
    limits used to size the loops over landscape calibration regions, plant-calibration regions,
    and channel-calibration regions. Without those maxima the routine would not know how many
    region records to traverse.'
  calibration_data_module: '`calibration_data_module` is the core state source for this routine.
    It provides the calibration-mode flags that decide which branch runs, the region and land-use
    arrays that are looped over, the accumulated soft-calibration totals that are divided
    by `time%yrs_prt`, and the zero-value plant calibration template used to clear `plcal(ireg)%lum(ilu)%sim`
    after yield is computed.'
  time_module: '`time_module` matters because `time%yrs_prt` is the divisor that converts
    accumulated sums into average annual values. The routine only performs normalization when
    that printing interval is positive, so this state controls both the calculation and the
    guard against division by zero.'
---

<!-- facts:header -->

Averaging and normalizing soft-calibration accumulators at the end of a printing period. It converts summed landscape, plant, and channel calibration totals into annualized values and resets plant calibration state for the next run.

## Bottom Line

`calsoft_ave_output` is the end-of-period cleanup routine for soft calibration output. When hydrologic, sediment, plant, or channel calibration modes are active, it converts accumulated sums into average annual values by dividing the stored calibration totals by `time%yrs_prt`, and it preserves selected averages such as precipitation in the `*_precip_aa_sav` fields for later reporting.

For plant calibration, it computes yield per hectare from accumulated simulated yield and area, increments the year counter when a land-use area is present, and then resets the per-land-use simulated plant-calibration state to `plcal_z`. The routine does not perform file I/O; it prepares shared module state for later reporting or calibration steps.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs near the end of `time_control`, after the simulation period has accumulated soft-calibration sums and just before `time_control` stores `yrs_print` and resets `time` back to `time_init`. Its results are the annualized calibration values that downstream soft-calibration reporting or comparison logic uses after the print interval ends.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Enter the hydrologic/sediment landscape branch when HRU hydrologic or sediment calibration is enabled. | The routine tests `cal_codes%hyd_hru` and `cal_codes%sed`. If either indicates an active HRU hydrologic or sediment calibration, it proceeds to average landscape calibration output for HRU-based calibration. |
| 2. Loop over all HRU calibration regions and land-use entries. | For each region index `ireg` up to `db_mx%lsu_reg`, the routine iterates through the land uses recorded in `region(ireg)%nlum`. |
| 3. Convert accumulated landscape calibration totals to annual averages when the print interval is positive. | If `time%yrs_prt > 0`, the routine divides precipitation, PET, and the landscape process totals (`srr`, `lfr`, `pcr`, `etr`, `tfr`, `bfr`, `wyr`) by `time%yrs_prt`. It also copies the averaged precipitation into `lscal(ireg)%lum(ilu)%precip_aa_sav` for later output use. |
| 4. Enter the HRU LTE landscape branch when that calibration mode is enabled. | The routine tests `cal_codes%hyd_hrul` and, when it is `"y"`, averages the corresponding HRU LTE landscape calibration state. |
| 5. Loop over all HRU LTE calibration regions and land-use entries. | For each region index `ireg` up to `db_mx%lsu_reg`, the routine iterates through the land uses recorded in `lscalt(ireg)%lum_num`. |
| 6. Convert accumulated HRU LTE landscape totals to annual averages when the print interval is positive. | If `time%yrs_prt > 0`, the routine divides precipitation and the HRU LTE process totals (`srr`, `lfr`, `pcr`, `etr`, `tfr`) by `time%yrs_prt`. It then stores the averaged precipitation in `lscalt(ireg)%lum(ilu)%precip_aa_sav`. |
| 7. Enter the plant-calibration branch when plant calibration is enabled. | The routine tests `cal_codes%plt` and only processes plant calibration output when the plant soft-calibration mode is active. |
| 8. Loop over plant-calibration regions and land-use entries. | For each plant-calibration region index `ireg` up to `db_mx%plcal_reg`, the routine iterates through the plant calibration land uses in `plcal(ireg)%lum_num`. |
| 9. Update plant-calibration year count, compute yield per area, and reset simulated plant state for each active land use. | When `plcal(ireg)%lum(ilu)%ha > 1.e-6`, the routine increments `nbyr`, sets `aa%yield` to `sim%yield / ha`, and assigns `sim = plcal_z` to zero the simulated plant-calibration accumulators. |
| 10. Enter the channel-calibration branch only when channel sediment calibration is the only active mode. | The routine requires `cal_codes%chsed == "y"` and simultaneously requires `sed`, `plt`, `hyd_hru`, and `hyd_hrul` to all be `"n"` before it averages channel calibration output. |
| 11. Loop over channel calibration regions and stream-order entries. | For each channel calibration region index `ireg` up to `db_mx%ch_reg`, the routine iterates through the stream-order entries recorded in `chcal(ireg)%ord_num`. |
| 12. Convert accumulated channel calibration totals to annual averages when the print interval is positive. | If `time%yrs_prt > 0`, the routine divides channel depth, width, headcut advance, and flood-plain deposition totals (`chd`, `chw`, `hc`, `fpd`) by `time%yrs_prt` so they become average annual values. |
| 13. Return to the caller after shared calibration state is updated. | The subroutine exits after all enabled calibration outputs have been normalized in shared module state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sd_channel_module state/types are not individually resolved in the extracted snippets, but the module is used as a dependency for channel-calibration output data structures.` | `None resolved in the extracted snippets.` |
| [sym:hru_lte_module] | `hru_lte_module state/types are not individually resolved in the extracted snippets, but the module is used as a dependency for the hru_lte calibration branch.` | `None resolved in the extracted snippets.` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg, db_mx%plcal_reg, db_mx%ch_reg` |
| [sym:calibration_data_module] | `cal_codes, region, lscal, lscalt, plcal, chcal, plcal_z` | `cal_codes%hyd_hru, cal_codes%sed, region(ireg)%nlum, lscal(ireg)%lum(ilu)%precip_aa, lscal(ireg)%lum(ilu)%precip_aa_sav, lscal(ireg)%lum(ilu)%pet_aa, lscal(ireg)%lum(ilu)%aa%srr, lscal(ireg)%lum(ilu)%aa%lfr, lscal(ireg)%lum(ilu)%aa%pcr, lscal(ireg)%lum(ilu)%aa%etr, lscal(ireg)%lum(ilu)%aa%tfr, lscal(ireg)%lum(ilu)%aa%bfr, lscal(ireg)%lum(ilu)%aa%wyr, cal_codes%hyd_hrul, lscalt(ireg)%lum_num, lscalt(ireg)%lum(ilu)%precip_aa, lscalt(ireg)%lum(ilu)%precip_aa_sav, lscalt(ireg)%lum(ilu)%aa%srr, lscalt(ireg)%lum(ilu)%aa%lfr, lscalt(ireg)%lum(ilu)%aa%pcr, lscalt(ireg)%lum(ilu)%aa%etr, lscalt(ireg)%lum(ilu)%aa%tfr, cal_codes%plt, plcal(ireg)%lum_num, plcal(ireg)%lum(ilu)%ha, plcal(ireg)%lum(ilu)%nbyr, plcal(ireg)%lum(ilu)%aa%yield, plcal(ireg)%lum(ilu)%sim%yield, plcal(ireg)%lum(ilu)%sim, cal_codes%chsed, chcal(ireg)%ord_num, chcal(ireg)%ord(ich)%aa%chd, chcal(ireg)%ord(ich)%aa%chw, chcal(ireg)%ord(ich)%aa%hc, chcal(ireg)%ord(ich)%aa%fpd` |
| [sym:time_module] | `time` | `time%yrs_prt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lscal(ireg)%lum(ilu)%precip_aa` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Stores the average annual precipitation for each landscape calibration land-use entry by dividing the accumulated precipitation by the print interval. |
| `lscal(ireg)%lum(ilu)%precip_aa_sav` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`, immediately after `precip_aa` is averaged. | Preserves the averaged precipitation value for later reporting or reuse after the routine finishes normalizing the HRU landscape calibration state. |
| `lscal(ireg)%lum(ilu)%pet_aa` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Converts accumulated potential evapotranspiration to an average annual value for the current landscape calibration land-use entry. |
| `lscal(ireg)%lum(ilu)%aa%srr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated surface runoff ratio total into an average annual calibration value. |
| `lscal(ireg)%lum(ilu)%aa%lfr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated lateral-flow ratio total into an average annual calibration value. |
| `lscal(ireg)%lum(ilu)%aa%pcr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated percolation ratio total into an average annual calibration value. |
| `lscal(ireg)%lum(ilu)%aa%etr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated evapotranspiration ratio total into an average annual calibration value. |
| `lscal(ireg)%lum(ilu)%aa%tfr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated tile-flow ratio total into an average annual calibration value. |
| `lscal(ireg)%lum(ilu)%aa%bfr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated baseflow ratio total into an average annual calibration value. |
| `lscal(ireg)%lum(ilu)%aa%wyr` | When HRU hydrologic or sediment soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated water-yield ratio total into an average annual calibration value. |
| `lscalt(ireg)%lum(ilu)%precip_aa` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`. | Stores the average annual precipitation for each HRU LTE landscape calibration land-use entry by dividing the accumulated precipitation by the print interval. |
| `lscalt(ireg)%lum(ilu)%precip_aa_sav` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`, immediately after `precip_aa` is averaged. | Preserves the averaged precipitation value for later reporting or reuse after the routine finishes normalizing the HRU LTE landscape calibration state. |
| `lscalt(ireg)%lum(ilu)%aa%srr` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated surface runoff ratio total into an average annual calibration value for HRU LTE landscape calibration. |
| `lscalt(ireg)%lum(ilu)%aa%lfr` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated lateral-flow ratio total into an average annual calibration value for HRU LTE landscape calibration. |
| `lscalt(ireg)%lum(ilu)%aa%pcr` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated percolation ratio total into an average annual calibration value for HRU LTE landscape calibration. |
| `lscalt(ireg)%lum(ilu)%aa%etr` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated evapotranspiration ratio total into an average annual calibration value for HRU LTE landscape calibration. |
| `lscalt(ireg)%lum(ilu)%aa%tfr` | When HRU LTE soft calibration is active and `time%yrs_prt > 0`. | Turns the accumulated tile-flow ratio total into an average annual calibration value for HRU LTE landscape calibration. |
| `plcal(ireg)%lum(ilu)%nbyr` | When plant soft calibration is active and the land-use area for the current plant entry is greater than `1.e-6`. | Counts one more year of valid plant-calibration data for that land-use entry. |
| `plcal(ireg)%lum(ilu)%aa%yield` | When plant soft calibration is active and `plcal(ireg)%lum(ilu)%ha > 1.e-6`. | Computes annual plant yield as simulated yield divided by planted area, giving a per-hectare calibration output. |
| `plcal(ireg)%lum(ilu)%sim` | When plant soft calibration is active and `plcal(ireg)%lum(ilu)%ha > 1.e-6`. | Resets the accumulated plant calibration simulation state to zero by copying `plcal_z`, so the next run starts from a clean accumulator. |
| `cal_codes%hyd_hrul` | When channel sediment soft calibration is active and no other soft-calibration branches are enabled, and `time%yrs_prt > 0`. | Normalizes channel calibration totals into average annual rates for the channel sediment calibration workflow. |
| `chcal(ireg)%ord(ich)%aa%chd` | When channel sediment soft calibration is active and no other soft-calibration branches are enabled, and `time%yrs_prt > 0`. | Converts accumulated channel downcutting/accretion to an annual average value. |
| `chcal(ireg)%ord(ich)%aa%chw` | When channel sediment soft calibration is active and no other soft-calibration branches are enabled, and `time%yrs_prt > 0`. | Converts accumulated channel widening to an annual average value. |
| `chcal(ireg)%ord(ich)%aa%hc` | When channel sediment soft calibration is active and no other soft-calibration branches are enabled, and `time%yrs_prt > 0`. | Converts accumulated headcut advance to an annual average value. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolves three commits for `calsoft_ave_output`. The original file was introduced in `df07e3f`; `c7c8e22` kept the procedure logic and includes the same averaging branches and assignments visible in the diff context; `39fabde` only initialized the local loop counters `ireg`, `ilu`, and `ich` to zero without changing the algorithm.

- df07e3f introduced the new `calsoft_ave_output` subroutine with the landscape, plant, and channel averaging branches that divide accumulated calibration totals by `time%yrs_prt` and reset plant simulation state.
- c7c8e22 preserved the procedure structure and averaging behavior already present in the initial addition; the diff context shows the same branch logic and assignments for landscape, HRU LTE, plant, and channel calibration output.
- 39fabde changed only the local integer declarations for `ireg`, `ilu`, and `ich` by adding explicit zero initializers; it did not alter the calibration calculations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_ave_output' has no extracted documentation comment.
