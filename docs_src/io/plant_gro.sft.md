---
kind: io
source_symbols:
- pl_read_regions_cal
title: '`plant_gro.sft`'
status: filled
source_hash: 56e435200f646c49
version_label: SWAT+ 62.0.0
---

**Primary target:** `plcal(:)` (array of `type soft_data_calib_plant`)  
**Read by:** [sym:pl_read_regions_cal]

## Bottom Line

The file `plant_gro.sft` contains soft calibration data for plant growth regions, defining regions, their land uses, and associated HRUs.

It is optional; if the file does not exist or is set to "null", the calibration array is allocated empty.

The reader `pl_read_regions_cal` loads this file, parsing region names, land use counts, HRU assignments, and calibration measurements.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_chg%plant_gro_sft` used to locate the file |
| [sym:maximum_data_module] | provides global maximums and constants such as `sp_ob%hru` used for HRU counts |
| [sym:calibration_data_module] | provides the derived type `soft_data_calib_plant` and its components `plcal` where the data is stored |
| [sym:hydrograph_module] | used indirectly for HRU and calibration data linkage (no direct variables identified) |
| [sym:hru_module] | provides the `hru` type array used to assign HRUs to crop regions (`hru(iihru)%crop_reg`) |

## File Variables

The file `plant_gro.sft` is structured as a sequence of region calibration records. Each record defines a region name, the number of land uses, the number of HRUs, and calibration data arrays for land uses. The Fortran reader maps these records into an array `plcal` of type `soft_data_calib_plant`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `plcal%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_reg) |
| 3 |  | `plcal%lum_num` | integer |  | number of land uses in each region |
| 4 |  | `plcal%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `plcal%num` | integer |  | hru"s that are included in the region |
| 6 |  | `plcal%lum` | type (pl_calib_regions) |  | dimension for land uses within a region |

## Sample

```text
Example record block from plant_gro.sft:
RegionName1 3 5 10 20 30
Header line for land uses
0.1 0.2 0.3 0.4 0.5
0.6 0.7 0.8 0.9 1.0
0.11 0.12 0.13 0.14 0.15
```

## Read Pattern

```fortran
open (107,file=in_chg%plant_gro_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) plcal(i)%name, plcal(i)%lum_num, nspu
backspace (107)
read (107,*,iostat=eof) plcal(i)%name, plcal(i)%lum_num,  nspu, (elem_cnt(isp), isp = 1, nspu)
read (107,*,iostat=eof) plcal(i)%lum(ilum)%meas
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%plant_gro_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) plcal(i)%name, plcal(i)%lum_num, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) plcal(i)%name, plcal(i)%lum_num,  nspu, (elem_cnt(isp), isp = 1, nspu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) plcal(i)%lum(ilum)%meas` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:pl_read_regions_cal] | backspace, close, open, read | Reads the plant_gro.sft file to load soft calibration data for plant growth regions. It opens the file, reads region counts and headers, then iteratively reads each region's name, land use count, and HRU counts. It assigns HRUs to regions and reads calibration measurement arrays for each land use within regions. |

## Review Notes

- The file is optional; if missing or set to "null", the calibration array is allocated empty.
- The reader assigns HRUs to crop regions via the hru array's crop_reg field.
- The sample read format is inferred from the read statements and typical file structure; no exact example block was found in source.
- No direct variables from hydrograph_module are identified in the reader, but it is used by the module.
