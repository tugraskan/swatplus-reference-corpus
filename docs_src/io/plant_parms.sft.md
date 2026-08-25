---
kind: io
source_symbols:
- pl_read_parms_cal
title: '`plant_parms.sft`'
status: filled
source_hash: 549b2e06d839a941
version_label: SWAT+ 62.0.0
---

**Primary target:** `pl_prms(:)` (array of `type pl_parm_region`)  
**Read by:** [sym:pl_read_parms_cal]

## Bottom Line

The file `plant_parms.sft` contains landscape soft calibration parameters for plant growth regions.

It is optional and only read if the file exists and is not set to "null".

The reader `pl_read_parms_cal` loads this file and populates the `pl_prms` array of `type pl_parm_region` with calibration data.

This file configures plant parameter initial values such as epco, pest_stress, lai_pot, and harv_idx for each plant in each HRU region.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | provides the global variable db_mx and defunit_num used for region and HRU counts and default unit numbering |
| [sym:calibration_data_module] | provides the type pl_parm_region and the pl_prms array where the file data is stored |
| [sym:hydrograph_module] | used but no specific variables identified from source |
| [sym:hru_module] | provides the hru derived type array hru, which is updated with crop_reg indices |
| [sym:input_file_module] | provides the in_chg derived type with the plant_parms_sft filename string |
| [sym:plant_module] | provides pcom array used to assign plant parameter initial values per HRU |

## File Variables

The file consists of multiple plant parameter calibration regions, each with a name, number of land uses, number of parameters, and associated HRUs. For each region, the file lists counts of elements per land use and calibration parameter values. These map to the Fortran derived type `pl_parm_region` and its components.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pl_prms%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_reg) |
| 3 |  | `pl_prms%lum_num` | integer |  | number of land uses in each region |
| 4 |  | `pl_prms%parms` | integer |  | number of plant parameters used in calibration |
| 5 |  | `pl_prms%num_tot` | integer |  | number of hru"s in each region |
| 6 |  | `pl_prms%num` | integer |  | hru"s that are included in the region |
| 7 |  | `pl_prms%prm` | type (pl_parms_cal) |  | dimension for land uses within a region |

## Sample

```text
Example record block from plant_parms.sft:
Title line (character*80)
Number of regions (integer)
Header line (character*80)
For each region:
  region name (character*16), number of land uses (integer), number of parameters (integer), number of subunits (integer)
  region name (character*16), number of land uses (integer), number of subunits (integer), element counts per subunit (integer array)
  header line (character*80)
  for each land use and parameter combination:
    parameter calibration record (type pl_parms_cal)
```

## Read Pattern

```fortran
open (107,file=in_chg%plant_parms_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) pl_prms(i)%name, pl_prms(i)%lum_num, pl_prms(i)%parms, nspu
backspace (107)
read (107,*,iostat=eof) pl_prms(i)%name, pl_prms(i)%lum_num,  nspu, (elem_cnt(isp), isp = 1, nspu)
read (107,*,iostat=eof) header
read (107,*,iostat=eof) pl_prms(i)%prm(ilum)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%plant_parms_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pl_prms(i)%name, pl_prms(i)%lum_num, pl_prms(i)%parms, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pl_prms(i)%name, pl_prms(i)%lum_num,  nspu, (elem_cnt(isp), isp = 1, nspu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pl_prms(i)%prm(ilum)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:pl_read_parms_cal] | backspace, close, open, read | Reads the optional plant_parms.sft file if it exists and is not "null". It loads plant parameter calibration regions into the pl_prms array, allocating arrays for HRUs and parameters, and sets initial plant parameter values (epco, pest_stress, lai_pot, harv_idx) for each plant in each HRU region. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not set to "null".
- The reader sets crop_reg indices in the hru array to link HRUs to calibration regions.
- The reader assigns initial values to plant parameters for each plant in each HRU using the loaded calibration data.
- No sample data block was found in the source; the sample_read_format is inferred from read statements.
