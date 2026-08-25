---
kind: procedure
symbol: cb_plc_stat_emit
title: cb_plc_stat_emit
status: filled
source_hash: 82c59b529cc7a469
version_label: SWAT+ 62.0.0
args:
  freq_in: '`freq_in` selects which reporting interval to use: daily, monthly, yearly, or
    average annual. The procedure maps that code to a pair of output units and then suppresses
    output unless the corresponding `pco%cb_plt_hru%*` flag is set to `"y"`.'
  hru_j: '`hru_j` is the HRU index whose plant-carbon totals are written. It is used to pick
    the `pl_mass(hru_j)` record and is also written to the output as the HRU identifier.'
  hru_iob: '`hru_iob` is the object index for the HRU being reported. It is used to fetch
    the GIS id and object name from `ob(hru_iob)` for both text and CSV output rows.'
locals:
  u_txt: Holds the text-file unit number for the selected reporting frequency, so the routine
    can write the formatted `.txt` record to the correct already-open output file.
  u_csv: Holds the CSV-file unit number for the selected reporting frequency, so the routine
    can write the optional comma-separated record to the correct already-open output file.
---

<!-- facts:header -->

Emits HRU plant-carbon statistics for the requested reporting frequency. It writes a fixed-format text record and, if enabled, a CSV record for the same plant-carbon totals.

## Bottom Line

This subroutine is a reporting hook for plant carbon in HRUs. Given a frequency code, it selects the matching output units and checks whether that reporting interval is enabled before writing anything.

When enabled, it writes one record per HRU containing the simulation date, HRU identifier, GIS object metadata, and the plant-carbon totals from `pl_mass(hru_j)`. It also writes the same fields to CSV when `pco%csvout == "y"`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `soil_nutcarb_write` after the caller has determined the current output frequency and HRU/object indices. Its results feed the plant-carbon reporting files for daily, monthly, yearly, or average-annual HRU outputs, so downstream users of SWAT+ carbon diagnostics depend on it for those summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. choose reporting frequency | Examine `freq_in` to decide which output interval is being requested for plant-carbon reporting. |
| 2. daily gate and units | For daily reports, bind the daily text and CSV units and return immediately unless daily plant-carbon output is enabled in `pco%cb_plt_hru%d`. |
| 3. monthly gate and units | For monthly reports, bind the monthly text and CSV units and return immediately unless monthly plant-carbon output is enabled in `pco%cb_plt_hru%m`. |
| 4. yearly gate and units | For yearly reports, bind the yearly text and CSV units and return immediately unless yearly plant-carbon output is enabled in `pco%cb_plt_hru%y`. |
| 5. average-annual gate and units | For average-annual reports, bind the average-annual text and CSV units and return immediately unless average-annual plant-carbon output is enabled in `pco%cb_plt_hru%a`. |
| 6. ignore unsupported codes | Return without output for any frequency code other than the four supported plant-carbon intervals. |
| 7. write text record | Write one fixed-format text record with the current date, HRU index, GIS id, object name, and plant-carbon totals from `pl_mass(hru_j)`. |
| 8. check CSV setting | Test `pco%csvout` to see whether the optional CSV companion record should be written. |
| 9. write CSV record | Write one comma-separated record with the same date, HRU, GIS, name, and plant-carbon totals to the selected CSV unit. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one behavior-changing refactor in bc7755a: this routine was introduced as part of the carbon IO refactor that replaced the older diagnostics-style gating with per-frequency plant-carbon output and added support for average-annual reporting (`case (" a")`).

- bc7755a added the `case (" a")` branch and average-annual plant-carbon gating/output units, expanding the routine beyond daily/monthly/yearly reporting.
- bc7755a removed the old `cbn_diagnostics`-style wrapper logic from related carbon emitters and shifted to per-family gating inside emit subroutines, which is the pattern this routine now follows.
- bc7755a kept the text/CSV emission structure but aligned it with the new frequency labels and unit numbers used by the refactored carbon IO layer.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cb_plc_stat_emit' has no extracted documentation comment.
