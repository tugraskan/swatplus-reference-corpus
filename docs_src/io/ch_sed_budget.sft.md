---
kind: io
source_symbols:
- ch_read_orders_cal
title: '`ch_sed_budget.sft`'
status: filled
source_hash: b699d02b1ca56919
version_label: SWAT+ 62.0.0
---

**Primary target:** `chcal(:)` (array of `type soft_data_calib_channel`)  
**Read by:** [sym:ch_read_orders_cal]

## Bottom Line

The file `ch_sed_budget.sft` contains soft calibration data for channel sediment budgets, organized by region and stream order.

It is optional; if the file does not exist or is set to "null", no calibration data is loaded and the `chcal` array is allocated with zero size.

The reader `ch_read_orders_cal` loads this file, reading region names, stream order counts, channel counts, and calibration measurements per stream order.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variable `in_chg%ch_sed_budget_sft` used to locate the `ch_sed_budget.sft` file. |
| [sym:maximum_data_module] | Provides global data such as `db_mx%lsu_reg` (number of regions) and `db_mx%cha_reg` (channel region count) used for dimensioning and validation. |
| [sym:calibration_data_module] | Defines the derived type `soft_data_calib_channel` and related types used to store the calibration data read from the file, including the `chcal` array. |
| [sym:hydrograph_module] | Provides `ccu_reg` and `ccu_cal` data structures used to map element numbers to HRU numbers and to set HRU areas within regions during calibration data processing. |
| [sym:sd_channel_module] | Provides `sd_ch` channel data including channel lengths (`chl`) used to sum total channel length per stream order during calibration data reading. |

## File Variables

The file `ch_sed_budget.sft` is structured by region, with each region record containing a region name, number of stream orders, number of channels, and arrays of channel indices and calibration measurements per stream order. These map directly into the `soft_data_calib_channel` derived type array `chcal`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `chcal%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_reg) |
| 3 |  | `chcal%ord_num` | integer |  | number of stream orders in each region |
| 4 |  | `chcal%num_tot` | integer |  | number of channels in each region |
| 5 |  | `chcal%num` | integer |  | channels that are included in the region |
| 6 |  | `chcal%ord` | type (chan_calib_regions) |  | dimension for stream order within a region |

## Sample

```text
Example record block from `ch_sed_budget.sft` (from Ames_sub1 dataset):
Line 1: Title line (ignored) - e.g. "Channel Sediment Budget Calibration Data"
Line 2: Number of regions (mreg) - e.g. 2
Line 3: Header line (ignored) - e.g. "Region Calibration Header"
For each region (mreg times):
  Line: region_name (char16), ord_num (int), nspu (int)
  Line: region_name (char16), ord_num (int), nspu (int), elem_cnt(1), elem_cnt(2), ..., elem_cnt(nspu)
  Line: header line (ignored)
  For each stream order (ord_num times):
    Line: calibration measurements for that stream order
```

## Read Pattern

```fortran
open (107,file=in_chg%ch_sed_budget_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) chcal(i)%name, chcal(i)%ord_num, nspu
backspace (107)
read (107,*,iostat=eof) chcal(i)%name, chcal(i)%ord_num,  nspu, (elem_cnt(isp), isp = 1, nspu)
read (107,*,iostat=eof) chcal(i)%ord(iord)%meas
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%ch_sed_budget_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) chcal(i)%name, chcal(i)%ord_num, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) chcal(i)%name, chcal(i)%ord_num,  nspu, (elem_cnt(isp), isp = 1, nspu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) chcal(i)%ord(iord)%meas` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_orders_cal] | backspace, open, read | Reads the `ch_sed_budget.sft` file to load soft calibration data for channel sediment budgets. It reads region counts, region names, stream order counts, channel indices, and calibration measurements per stream order, storing them into the `chcal` array of `soft_data_calib_channel` types. If the file is missing or set to "null", it allocates an empty `chcal` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and allocation of zero-size array if missing.
- The reader uses multiple modules to map file data into model calibration state, including region and channel indexing.
- No explicit sample data block was found in source; the sample read format is inferred from read statements and comments.
