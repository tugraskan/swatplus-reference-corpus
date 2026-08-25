---
kind: io
source_symbols:
- ch_read_sed
title: '`sediment.cha`'
status: filled
source_hash: ac91c1190b158527
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_sed(:)` (array of `type channel_sed_data`)  
**Read by:** [sym:ch_read_sed]

## Bottom Line

The file `sediment.cha` configures channel sediment properties used in sediment routing and erosion modeling within SWAT+. It is an optional input file checked by the reader `ch_read_sed`. When present, `ch_read_sed` reads sediment parameters for each channel segment into the array `ch_sed` of type `channel_sed_data`, setting defaults and bounds for missing or invalid values.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_cha%sed` used to locate the `sediment.cha` file. |
| [sym:maximum_data_module] | provides the integer `db_mx%ch_sed` which stores the number of sediment records read and is used to allocate the `ch_sed` array. |
| [sym:channel_data_module] | provides the derived type `channel_sed_data` and the array `ch_sed` where the sediment data records are stored. |

## File Variables

The `sediment.cha` file contains tabular records of channel sediment properties, each record corresponding to a channel segment. Each record is read into an element of the `ch_sed` array of type `channel_sed_data`. The file columns map directly to the components of this derived type, including sediment routing method, cover factors, bulk densities, erodibility coefficients, particle sizes, critical shear stresses, and monthly erosion rates.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ch_sed%name` | character(len=16) |  | Channel segment name identifier. |
| 3 |  | `ch_sed%eqn` | integer |  | Sediment routing method code: 0=SWAT default, 1=Bagnold, 2=Kodatine, 3=Molinas WU, 4=Yang. |
| 4 |  | `ch_sed%cov1` | real |  | Channel erodibility factor or cover factor 1, range 0.0-1.0 or up to 25.0 depending on method. |
| 5 |  | `ch_sed%cov2` | real | none | Channel cover factor 2, range 0.0-1.0 or up to 25.0 depending on method. |
| 6 |  | `ch_sed%bnk_bd` | real | (g/cc) | Bulk density of channel bank sediment, typical range 1.1-1.9 g/cc, default 1.40 g/cc if missing. |
| 7 |  | `ch_sed%bed_bd` | real | (g/cc) | Bulk density of channel bed sediment, typical range 1.1-1.9 g/cc, default 1.50 g/cc if missing. |
| 8 |  | `ch_sed%bnk_kd` | real |  | Erodibility coefficient of channel bank sediment from jet test (cm^3/N/s), estimated if missing based on critical shear stress. |
| 9 |  | `ch_sed%bed_kd` | real |  | Erodibility coefficient of channel bed sediment from jet test (cm^3/N/s), estimated if missing based on critical shear stress. |
| 10 |  | `ch_sed%bnk_d50` | real |  | Median particle size diameter (D50) of channel bank sediment in micrometers, default 50 if missing. |
| 11 |  | `ch_sed%bed_d50` | real |  | Median particle size diameter (D50) of channel bed sediment in micrometers, default 500 if missing. |
| 12 |  | `ch_sed%tc_bnk` | real | N/m2 | Critical shear stress of channel bank sediment in N/m^2, set to zero if non-positive. |
| 13 |  | `ch_sed%tc_bed` | real | N/m2 | Critical shear stress of channel bed sediment in N/m^2, set to zero if non-positive. |
| 14 |  | `ch_sed%erod` | real |  | Monthly erosion rate factors (12 values), zero indicates non-erosive channel; if all zero, set to cov1 value. |

## Sample

```text
Example record from Ames_sub1 dataset:
ChannelName 0 0.1 0.1 1.40 1.50 0.15 0.10 50 500 0.5 0.6 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
```

## Read Pattern

```fortran
open (105,file=in_cha%sed)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) ch_sed(ich)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%sed)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ch_sed(ich)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_sed] | backspace, close, open, read, rewind | Reads the optional input file `sediment.cha` if it exists, counts the number of sediment records, allocates the `ch_sed` array accordingly, and reads each sediment record into `ch_sed`. It sets default values and bounds for missing or invalid parameters such as critical shear stresses, cover factors, particle sizes, bulk densities, and erodibility coefficients. It also initializes monthly erosion rates if missing. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The reader `ch_read_sed` treats `sediment.cha` as optional, allocating zero-length arrays if missing or set to 'null'.
- Defaults and bounds for sediment parameters are set explicitly in the reader source.
- The sample record is a constructed example based on typical default values and field order; no exact example was found in the source.
