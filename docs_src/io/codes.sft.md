---
kind: io
source_symbols:
- calsoft_read_codes
title: '`codes.sft`'
status: filled
source_hash: 4befe610f9ebf839
version_label: SWAT+ 62.0.0
---

**Primary target:** `cal_codes(:)` (array of `type soft_calibration_codes`)  
**Read by:** [sym:calsoft_read_codes]

## Bottom Line

The file `codes.sft` is an optional soft calibration input file that configures calibration flags for hydrologic, plant growth, sediment, nutrient, channel, and reservoir processes in the SWAT+ model.

It is read by the `calsoft_read_codes` subroutine, which loads the calibration flags into the `cal_codes` array of `soft_calibration_codes` derived type instances.

If the file does not exist or is set to "null", no calibration flags are applied.

| Module | Role for this file |
| --- | --- |
| [sym:calibration_data_module] | Provides the `soft_calibration_codes` derived type and the `cal_codes` variable where the file data is stored. |
| [sym:plant_data_module] | Used by `calsoft_read_codes` likely for plant-related calibration flags or data structures. |
| [sym:input_file_module] | Provides the `in_chg` variable containing the filename `codes_sft` to open. |
| [sym:soil_module] | Imported for potential soil-related calibration flags or data access during reading. |
| [sym:plant_module] | Imported for plant-related calibration flags or data access during reading. |
| [sym:hydrograph_module] | Imported for hydrologic calibration flags or data access during reading. |
| [sym:hru_lte_module] | Imported for hydrologic calibration flags related to HRU LTE processes. |
| [sym:sd_channel_module] | Imported for channel-related calibration flags. |
| [sym:organic_mineral_mass_module] | Imported for nutrient or sediment calibration flags. |
| [sym:mgt_operations_module] | Imported possibly for management operation calibration flags. |
| [sym:conditional_module] | Imported for conditional logic during reading or calibration flag setting. |

## File Variables

The `codes.sft` file consists of a header block followed by one or more records of soft calibration flags. Each record is read into an element of the `cal_codes` array of type `soft_calibration_codes`. Each record contains single-character flags indicating whether to calibrate specific model processes such as hydrology, plant growth, sediment, nutrients, channels, and reservoirs.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cal_codes%hyd_hru` | character (len=1) |  | if a, calibrate all hydrologic balance processes for hru by land use in each region |
| 3 |  | `cal_codes%hyd_hrul` | character (len=1) |  | if b, calibrate baseflow and total runoff for hru by land use in each region if y, defaults to b for existing NAM simulations if y, calibrate hydrologic balance for hru_lte by land use in each region |
| 4 |  | `cal_codes%plt` | character (len=1) |  | if y, calibrate plant growth by land use (by plant) in each region |
| 5 |  | `cal_codes%sed` | character (len=1) |  | if y, calibrate sediment yield by land use in each region |
| 6 |  | `cal_codes%nut` | character (len=1) |  | if y, calibrate nutrient balance by land use in each region |
| 7 |  | `cal_codes%chsed` | character (len=1) |  | if y, calibrate channel widening and bank accretion by stream order |
| 8 |  | `cal_codes%chnut` | character (len=1) |  | if y, calibrate channel nutrient balance by stream order |
| 9 |  | `cal_codes%res` | character (len=1) |  | if y, calibrate reservoir budgets by reservoir |

## Sample

```text
Example `codes.sft` file content:
Line 1: Title or description (80 characters)
Line 2: Header line (80 characters)
Line 3: a n y n y n n y n
Where each character corresponds to the flags in order: hyd_hru, hyd_hrul, plt, sed, nut, chsed, chnut, res
```

## Read Pattern

```fortran
open (107,file=in_chg%codes_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) cal_codes
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%codes_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cal_codes` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:calsoft_read_codes] | open, read, close | Reads the `codes.sft` file if it exists and is not set to "null", loading calibration flags into the `cal_codes` array. Sets the global `cal_soft` flag to "y" if any calibration flags are enabled. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", no calibration flags are applied.
- The `calsoft_read_codes` subroutine sets a global flag `cal_soft` to "y" if any calibration flags are enabled in the file.
- Sample record format is inferred from the type and reading pattern; no explicit example record was found in the source.
