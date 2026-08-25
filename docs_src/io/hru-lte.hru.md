---
kind: io
source_symbols:
- hru_lte_read
title: '`hru-lte.hru`'
status: filled
source_hash: d1bcb4ce94ff67fa
version_label: SWAT+ 62.0.0
---

**Primary target:** `hlt_db(:)` (array of `type swatdeg_hru_data`)  
**Read by:** [sym:hru_lte_read]

## Bottom Line

The `hru-lte.hru` input file configures hydrologic response unit (HRU) parameters for the SWAT+ model, including soil, plant, and hydrologic properties.

This file is optional; if absent or set to "null", the HRU data array is allocated empty.

The file is read and parsed by the `hru_lte_read` subroutine, which loads the data into the `hlt_db` array of `swatdeg_hru_data` records.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides `db_mx` and `pldb` arrays used for crosswalking plant and growing season data. |
| [sym:plant_data_module] | Provides `pldb` plant parameter data used for plant type crosswalk and heat unit calculations. |
| [sym:hru_lte_module] | Defines the `swatdeg_hru_data` type and the `hlt_db` array where the file data is stored. |
| [sym:hydrograph_module] | Provides `ob` and `sp_ob` objects used to link HRU properties and allocate output variables. |
| [sym:input_file_module] | Provides the `in_hru` object containing the filename `hru_ez` for this input file. |
| [sym:output_landscape_module] | Provides `sp_ob` and `sp_ob1` for HRU counts and indexing used in allocation and data mapping. |
| [sym:climate_module] | Provides weather generator data `wgn` and weather station info `wst` used in heat unit calculations. |
| [sym:time_module] | Provides `ndays` array for days per month used in growing season heat unit calculations. |
| [sym:soil_data_module] | Provides `soil_lte` array for soil texture parameters used to compute available water capacity and related properties. |
| [sym:conditional_module] | No specific variables or types are directly referenced from this module in the reader. |

## File Variables

The `hru-lte.hru` file contains tabular records of hydrologic response unit parameters, each record corresponding to one HRU. Each record is read into an element of the `hlt_db` array of type `swatdeg_hru_data`. The file format includes a leading record ID followed by the fields listed below, matching the order and types declared in `hru_lte_module`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `hlt_db%name` | character(len=16) |  | HRU name identifier |
| 3 |  | `hlt_db%dakm2` | real | km^2 | drainage area |
| 4 |  | `hlt_db%cn2` | real | none | condition II curve number |
| 5 |  | `hlt_db%cn3_swf` | real | none | soil water factor for cn3 (used in calibration) 0 = fc; 1 = saturation (porosity) |
| 6 |  | `hlt_db%tc` | real | min | time of concentration |
| 7 |  | `hlt_db%soildep` | real | mm | soil profile depth |
| 8 |  | `hlt_db%perco` | real |  | soil percolation coefficient |
| 9 |  | `hlt_db%slope` | real | m/m | land surface slope |
| 10 |  | `hlt_db%slopelen` | real | m | land surface slope length |
| 11 |  | `hlt_db%etco` | real |  | et coefficient - use with pet and aet |
| 12 |  | `hlt_db%sy` | real | mm | specific yld of the shallow aquifer |
| 13 |  | `hlt_db%abf` | real |  | alpha factor groundwater |
| 14 |  | `hlt_db%revapc` | real |  | revap coefficient amt of et from shallow aquifer |
| 15 |  | `hlt_db%percc` | real |  | percolation coeff from shallow to deep |
| 16 |  | `hlt_db%sw` | real | frac | initial soil water (frac of awc) |
| 17 |  | `hlt_db%gw` | real | mm | initial shallow aquifer storage |
| 18 |  | `hlt_db%gwflow` | real | mm | initial shallow aquifer flow |
| 19 |  | `hlt_db%gwdeep` | real | mm | initial deep aquifer flow |
| 20 |  | `hlt_db%snow` | real | mm | initial snow water equivalent |
| 21 |  | `hlt_db%xlat` | real |  | latitude |
| 22 |  | `hlt_db%text` | character(len=16) |  | soil texture 1=sand 2=loamy_sand 3=sandy_loam 4=loam 5=silt_loam 6=silt 7=silty_clay 8=clay_loam 9=sandy_clay_loam 10=sandy_clay 11=silty_clay 12=clay |
| 23 |  | `hlt_db%tropical` | character(len=16) |  | (0)="non_trop" (1)="trop" |
| 24 |  | `hlt_db%igrow1` | character(len=16) |  | start of growing season for non-tropical (pl_grow_sum) start of monsoon initialization period for tropical |
| 25 |  | `hlt_db%igrow2` | character(len=16) |  | end of growing season for non-tropical (pl_end_sum) end of monsoon initialization period for tropical |
| 26 |  | `hlt_db%plant` | character(len=16) |  | plant type (as listed in plants.plt) |
| 27 |  | `hlt_db%stress` | real | frac | plant stress - pest, root restriction, soil quality, nutrient, (non water, temp) |
| 28 |  | `hlt_db%ipet` | character(len=16) |  | potential ET method (0="harg"; 1="p_t") |
| 29 |  | `hlt_db%irr` | character(len=16) |  | irrigation code 0="no_irr"; 1="irr" |
| 30 |  | `hlt_db%irrsrc` | character(len=16) |  | irrigation source 0="outside_bsn"; 1="shal_aqu" 2="deep_aqu" |
| 31 |  | `hlt_db%tdrain` | real | hr | design subsurface tile drain time |
| 32 |  | `hlt_db%uslek` | real |  | usle soil erodibility factor |
| 33 |  | `hlt_db%uslec` | real |  | usle cover factor |
| 34 |  | `hlt_db%uslep` | real | none | USLE equation support practice (P) factor |
| 35 |  | `hlt_db%uslels` | real | none | USLE equation length slope (LS) factor |

## Sample

```text
1 HRU1 12.5 75.0 0.3 15.0 1500.0 0.05 0.12 100.0 0.8 0.1 0.3 0.05 0.02 0.4 50.0 5.0 10.0 0.0 35.0 45.0 sand 0 pl_grow_sum pl_end_sum corn 0.1 harg no_irr outside_bsn 24.0 0.2 0.3 0.1 0.5
```

## Read Pattern

```fortran
open (1,file=in_hru%hru_ez)
read (1,*,iostat=eof) titldum
read (1,*,iostat=eof) header
read (1,*,iostat=eof) i
rewind (1)
backspace (1)
read (1,*,iostat=eof) k, hlt_db(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 1 | `open (1,file=in_hru%hru_ez)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| Input | `read` | 1 | `read (1,*,iostat=eof) header` |
| Input | `read` | 1 | `read (1,*,iostat=eof) i` |
| File control | `rewind` | 1 | `rewind (1)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| Input | `read` | 1 | `read (1,*,iostat=eof) header` |
| Input | `read` | 1 | `read (1,*,iostat=eof) i` |
| File control | `backspace` | 1 | `backspace (1)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) k, hlt_db(i)` |
| File control | `close` | 1 | `close (1)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:hru_lte_read] | backspace, close, open, read, rewind | Reads the `hru-lte.hru` file and loads hydrologic response unit parameters into the `hlt_db` array of `swatdeg_hru_data`. It handles file existence checks, determines the maximum HRU index, allocates arrays, reads all records, and performs crosswalks to plant and soil data modules for further initialization. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", an empty HRU data array is allocated.
- The reader performs crosswalks to plant and soil parameter data for initialization beyond file contents.
- Sample record format is inferred from the data type and read pattern; no explicit example found in source.
