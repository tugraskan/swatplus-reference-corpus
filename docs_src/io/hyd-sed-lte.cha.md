---
kind: io
source_symbols:
- sd_hydsed_read
title: '`hyd-sed-lte.cha`'
status: filled
source_hash: bfae134041a8db75
version_label: SWAT+ 62.0.0
---

**Primary target:** `sd_chd(:)` (array of `type swatdeg_hydsed_data`)  
**Read by:** [sym:sd_hydsed_read]

## Bottom Line

The file `hyd-sed-lte.cha` is a required input file that configures channel hydraulic and sediment properties for the SWAT+ model.

It is read by the `sd_hydsed_read` subroutine, which loads channel geometry, sediment, and nutrient parameters into the arrays `sd_chd` and `sd_chd1`.

This file controls channel dimensions, sediment characteristics, erosion parameters, and nutrient concentrations used in channel sediment routing.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variable `in_cha%hyd_sed` used to locate the `hyd-sed-lte.cha` file. |
| [sym:sd_channel_module] | Defines the derived types `swatdeg_hydsed_data` and `swatdeg_sednut_data` used for the `sd_chd` and `sd_chd1` arrays where file records are stored. |
| [sym:channel_velocity_module] | Imported but no direct variables or types from this module are used in `sd_hydsed_read`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores the counts `ch_lte` and `ch_sednut` for the number of records read from the file. |
| [sym:hydrograph_module] | Imported but no direct variables or types from this module are used in `sd_hydsed_read`. |
| [sym:time_module] | Provides the `time%step` variable used to determine the sediment routing time step `ts_sed`. |

## File Variables

The file `hyd-sed-lte.cha` contains two record sets representing channel hydraulic and sediment data (`sd_chd`) and channel sediment-nutrient data (`sd_chd1`). Each record corresponds to a channel segment and is read into arrays of derived types defined in `sd_channel_module`. The file is read sequentially with header lines skipped, and the number of records is determined by scanning the file before allocation.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sd_chd%name` | character(len=25) |  | Channel segment name identifier |
| 3 |  | `sd_chd%order` | integer |  | Channel segment order or hierarchy |
| 4 |  | `sd_chd%chw` | real | m | Channel width |
| 5 |  | `sd_chd%chd` | real | m | Channel depth |
| 6 |  | `sd_chd%chs` | real | m/m | Channel slope |
| 7 |  | `sd_chd%chl` | real | km | Channel length |
| 8 |  | `sd_chd%chn` | real |  | Channel Manning's roughness coefficient |
| 9 |  | `sd_chd%chk` | real | mm/h | Channel bottom hydraulic conductivity |
| 10 |  | `sd_chd%bank_exp` | real |  | Bank erosion exponent |
| 11 |  | `sd_chd%cov` | real | 0-1 | Channel cover factor |
| 12 |  | `sd_chd%sinu` | real | none | Channel sinuosity |
| 13 |  | `sd_chd%vcr_coef` | real |  | Critical velocity coefficient |
| 14 |  | `sd_chd%d50` | real | mm | Median sediment particle size |
| 15 |  | `sd_chd%ch_clay` | real | % | Clay content percentage |
| 16 |  | `sd_chd%carbon` | real | % | Carbon content percentage |
| 17 |  | `sd_chd%ch_bd` | real | t/m3 | Dry bulk density |
| 18 |  | `sd_chd%chss` | real |  | Channel side slope |
| 19 |  | `sd_chd%bankfull_flo` | real |  | Bankfull flow rate |
| 20 |  | `sd_chd%fps` | real | m/m | Flood plain slope |
| 21 |  | `sd_chd%fpn` | real |  | Flood plain Manning's n |
| 22 |  | `sd_chd%n_conc` | real | mg/kg | Nitrogen concentration in channel bank |
| 23 |  | `sd_chd%p_conc` | real | mg/kg | Phosphorus concentration in channel bank |
| 24 |  | `sd_chd%p_bio` | real | frac | Fraction of phosphorus bioavailable in bank |
| 2 |  | `sd_chd1%name` | character(len=25) |  | Channel segment name identifier |
| 3 |  | `sd_chd1%order` | character(len=16) |  | Channel segment order or classification |
| 4 |  | `sd_chd1%pk_rto` | real | ratio | Ratio of peak to mean daily flow |
| 5 |  | `sd_chd1%fp_inun_days` | real | days | Flood plain inundation duration |
| 6 |  | `sd_chd1%n_setl` | real | ratio | Ratio of nitrogen settling to sediment settling |
| 7 |  | `sd_chd1%p_setl` | real | ratio | Ratio of phosphorus settling to sediment settling |
| 8 |  | `sd_chd1%n_sol_part` | real |  | Nitrogen soluble to particulate transformation coefficient |
| 9 |  | `sd_chd1%p_sol_part` | real |  | Phosphorus soluble to particulate transformation coefficient |
| 10 |  | `sd_chd1%n_dep_enr` | real |  | Nitrogen enrichment ratio in remaining water |
| 11 |  | `sd_chd1%p_dep_enr` | real |  | Phosphorus enrichment ratio in remaining water |
| 12 |  | `sd_chd1%arc_len_fr` | real | frac | Fraction of arc length with bank erosion |
| 13 |  | `sd_chd1%bed_exp` | real |  | Bed erosion exponential coefficient |
| 14 |  | `sd_chd1%wash_bed_fr` | real | frac | Fraction of bank erosion as washload |

## Sample

```text
Example record block from hyd-sed-lte.cha (fields correspond to `sd_chd` type):
1  Channel1  1  10.0  2.0  0.001  5.0  0.03  0.035  0.1  0.5  1.1  0.8  0.2  15.0  20.0  1.5  0.3  100.0  0.000001  0.1  10.0  5.0  0.3
Example record block from sed_nut.cha (fields correspond to `sd_chd1` type):
1  Channel1  OrderA  1.2  4.0  0.6  0.7  0.02  0.02  0.6  0.7  1.1  1.6  0.15
```

## Read Pattern

```fortran
open (1,file=in_cha%hyd_sed)
read (1,*,iostat=eof) titldum
read (1,*,iostat=eof) header
do while not eof
  read (1,*,iostat=eof) titldum to count records
end do
rewind (1)
read (1,*,iostat=eof) titldum
read (1,*,iostat=eof) header
read (1,*,iostat=eof) sd_chd(idb) for each record
close (1)
open (1,file="sed_nut.cha")
read (1,*,iostat=eof) titldum
read (1,*,iostat=eof) header
do while not eof
  read (1,*,iostat=eof) titldum to count records
end do
rewind (1)
read (1,*,iostat=eof) titldum
read (1,*,iostat=eof) header
read (1,*,iostat=eof) sd_chd1(idb) for each record
close (1)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 1 | `open (1,file=in_cha%hyd_sed)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| Input | `read` | 1 | `read (1,*,iostat=eof) header` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| File control | `rewind` | 1 | `rewind (1)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| Input | `read` | 1 | `read (1,*,iostat=eof) header` |
| Input | `read` | 1 | `read (1,*,iostat=eof) sd_chd(idb)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| Input | `read` | 1 | `read (1,*,iostat=eof) header` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| File control | `rewind` | 1 | `rewind (1)` |
| Input | `read` | 1 | `read (1,*,iostat=eof) titldum` |
| Input | `read` | 1 | `read (1,*,iostat=eof) header` |
| Input | `read` | 1 | `read (1,*,iostat=eof) sd_chd1(idb)` |
| File control | `close` | 1 | `close (1)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:sd_hydsed_read] | close, open, read, rewind | Reads the `hyd-sed-lte.cha` file and the related `sed_nut.cha` file to load channel hydraulic, sediment, and nutrient parameters into the arrays `sd_chd` and `sd_chd1`. It first counts the number of records in each file to allocate arrays, then reads the data records sequentially, storing them in the corresponding derived type arrays for use in channel sediment routing. |

## Review Notes

- The file `hyd-sed-lte.cha` is required for channel sediment routing and is read by `sd_hydsed_read` along with `sed_nut.cha` for sediment-nutrient parameters.
- The reader uses `in_cha%hyd_sed` to locate the file, which must not be 'null' or missing.
- The file format includes header lines that are skipped before reading data records into `sd_chd` and `sd_chd1` arrays.
- No sample data records were found in the source; example records are constructed based on field order and types.
- Modules `channel_velocity_module` and `hydrograph_module` are imported but not directly used in this reader.
- The reader allocates temporary arrays for sediment routing time steps but these are not directly related to file reading.
