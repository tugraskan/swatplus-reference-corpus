---
kind: procedure
symbol: cb_cflux_stat_emit
title: cb_cflux_stat_emit
status: filled
source_hash: 0bf9dde2524e9365
version_label: SWAT+ 62.0.0
args:
  freq_in: 'Selects which carbon-flux output family to emit: daily (`" d"`), monthly (`" m"`),
    yearly (`" y"`), or annual-average (`" a"`). Any other value causes the routine to return
    without writing anything.'
  hru_j: Identifies the HRU whose soil-layer depths and carbon-flux arrays are written. It
    is also passed to the row-ID helpers so the emitted record is tied to the correct HRU.
  hru_iob: Selects the HRU object metadata used in the row identifier output, including the
    GIS ID and name. It lets the routine write a row prefix that matches the HRU index in
    the emitted data.
locals:
  u_txt: Text output unit chosen from the requested frequency; the routine writes the fixed-width
    carbon-flux row to this unit.
  u_csv: CSV output unit chosen from the requested frequency; used only when `pco%csvout ==
    "y"` to write the same row in CSV format.
  k: Loop index used to copy active soil layer depths from `soil(hru_j)%phys(k)%d` into the
    scratch buffer.
  n_use: The number of active soil layers in the HRU (`soil(hru_j)%nly`), used to limit how
    many layer values are copied and written.
  buf: Scratch vector holding layer depths before they are written by `cb_write_depth_row`
    and passed onward to flux emission.
  use_aa: Flags whether the annual-average flux path should be used. It is set true only for
    `freq_in = " a"` and false for the daily, monthly, and yearly cases.
---

<!-- facts:header -->

Writes HRU carbon-flux summary rows for day, month, year, or annual-average output. It emits both fixed-width text and optional CSV rows using the current HRU’s soil layer depths and carbon-flux arrays.

## Bottom Line

`cb_cflux_stat_emit` formats one HRU’s carbon-flux summary record in wide, per-layer form. The `freq_in` argument selects the output family: daily, monthly, yearly, or annual-average. For each supported frequency, the routine chooses the matching text and CSV unit numbers, checks the corresponding `pco%cb_flux_hru%*` switch, and stops immediately if that output family is disabled.

When output is enabled, it writes a row identifier, a layer-depth row built from `soil(hru_j)%phys(k)%d`, and then all 37 organic-flux fields through `cb_cflux_emit_blocks`. If CSV output is enabled in `pco%csvout`, it repeats the same data to the CSV unit. The annual-average case sets `use_aa=.true.` so downstream flux emission uses annual-average cumulative values instead of instantaneous layer fluxes.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `soil_nutcarb_write` during HRU output generation, after the caller has selected the current HRU and its object index (`hru_j`, `hru_iob`). It prepares the per-HRU carbon-flux summary record for whichever frequency is active, and later model reporting depends on its output files for the carbon-flux diagnostics used by the HRU-level carbon output family.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select frequency | Branch on `freq_in` to choose which carbon-flux output family to write and which file units to target. |
| 2. daily case | For daily output, set the text and CSV units, mark annual-average mode off, and return unless daily HRU carbon-flux output is enabled in `pco%cb_flux_hru%d`. |
| 3. monthly case | For monthly output, set the monthly text and CSV units, keep annual-average mode off, and return unless monthly HRU carbon-flux output is enabled in `pco%cb_flux_hru%m`. |
| 4. yearly case | For yearly output, set the yearly text and CSV units, keep annual-average mode off, and return unless yearly HRU carbon-flux output is enabled in `pco%cb_flux_hru%y`. |
| 5. annual-average case | For annual-average output, set the annual-average text and CSV units, enable annual-average flux handling, and return unless annual-average HRU carbon-flux output is enabled in `pco%cb_flux_hru%a`. |
| 6. unsupported frequency | Reject any unrecognized `freq_in` value by returning without writing output. |
| 7. count active layers | Set `n_use` to the current HRU soil-layer count so later writes know how many layer values are active. |
| 8. write text row id | Write the text-row identifier for the current HRU before any numeric columns are emitted. |
| 9. stage depths | Clear `buf`, copy each active layer depth from `soil(hru_j)%phys(k)%d`, and emit the depth row to the text unit as non-CSV fields. |
| 10. write text flux blocks | Append all 37 carbon-flux variable blocks to the text row, using `use_aa` to decide between instantaneous and annual-average values. |
| 11. gate CSV output | Only enter the CSV branch when global CSV output is enabled. |
| 12. write CSV row id | Write the CSV row identifier for the same HRU so the CSV record can be matched to the text record. |
| 13. stage depths for CSV | Rebuild the depth buffer and write the depth row in CSV format. |
| 14. write CSV flux blocks | Append the same carbon-flux blocks to the CSV row, again honoring `use_aa` for annual-average mode. |

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

Two resolved commits changed `cb_cflux_stat_emit`. Commit bc7755a refactored the surrounding carbon output system and added the annual-average `" a"` path alongside the existing daily, monthly, and yearly cases. Commit de210d6 (merged from the carbon IO and bug-fix work) preserved this procedure in its current form in the extracted span; no additional behavior change is visible in the provided diff for this routine.

- bc7755a added support for the annual-average carbon-flux output case by mapping `freq_in = " a"` to its own text/CSV units and setting `use_aa = .true.`, so downstream flux emission can use annual-average cumulative values.
- bc7755a kept the per-frequency gating on `pco%cb_flux_hru%*` and the dual text/CSV emission path intact while extending the output family choices to include annual-average records.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cb_cflux_stat_emit' has no extracted documentation comment.
