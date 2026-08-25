---
kind: io
source_symbols:
- landuse_read
title: '`landuse.lum`'
status: filled
source_hash: be733cd999e08180
version_label: SWAT+ 62.0.0
---

**Primary target:** `lum(:)` (array of `type land_use_management`)  
**Read by:** [sym:landuse_read]

## Bottom Line

The file `landuse.lum` configures land use and management types for the SWAT+ model, defining attributes such as plant cover, management operations, curve number land use, conservation practices, urban land use types, and various best management practices.

This file is optional; if it does not exist or is set to "null", the model allocates empty land use arrays.

The primary reader for this file is the `landuse_read` subroutine, which reads and parses the file into the `lum` array of `type land_use_management`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_lum%landuse_lum` used to locate the `landuse.lum` file. |
| [sym:maximum_data_module] | provides the `db_mx` object which contains maximum counts for various databases such as plant communities, management operations, curve number land uses, conservation practices, septic tanks, filter strips, grass waterways, and BMP user options used for indexing and validation. |
| [sym:septic_data_module] | provides the `sep` array and related data for septic tank definitions referenced by `lum%septic`. |
| [sym:plant_data_module] | provides the `pcomdb` array of plant community definitions referenced by `lum%plant_cov`. |
| [sym:hru_module] | provides the `sdr` array of subsurface drainage definitions referenced by `lum%tiledrain`. |
| [sym:landuse_data_module] | provides the `type land_use_management` definition and the `lum` and `lum_str` arrays where the file data is stored. |
| [sym:mgt_operations_module] | provides the `sched` array of management operation schedules referenced by `lum%mgt_ops`. |

## File Variables

The `landuse.lum` file contains records of land use and management types, each record mapping to an element of the `lum` array of `type land_use_management`. Each record includes multiple character fields representing names or pointers to other input files or tables defining plant cover, management schedules, curve number land uses, conservation practices, urban land use types, and best management practices.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `lum%name` | character (len=40) |  | name of the land use and management (from hru-data.hru pointer) |
| 3 |  | `lum%cal_group` | character (len=40) |  | calibration group (not currently used) |
| 4 |  | `lum%plant_cov` | character (len=40) |  | plant community initialization (pointer to plants.ini) |
| 5 |  | `lum%mgt_ops` | character (len=40) |  | management operations (pointer to management.sch) |
| 6 |  | `lum%cn_lu` | character (len=40) |  | land use for curve number table (pointer to cntable.lum) |
| 7 |  | `lum%cons_prac` | character (len=40) |  | conservation practice from table (cons_practice.lum) |
| 8 |  | `lum%urb_lu` | character (len=40) |  | type of urban land use- ie. residential, industrial, etc (urban.urb) |
| 9 |  | `lum%urb_ro` | character (len=40) |  | urban runoff model |
| 10 |  | `lum%ovn` | character (len=40) |  | "usgs_reg", simulate using USGS regression eqs "buildup_washoff", simulate using build up/wash off alg Manning"s "n" land use type for overland flow (ovn_table.lum) |
| 11 |  | `lum%tiledrain` | character (len=40) |  | tile drainage (pointer to tiledrain.str |
| 12 |  | `lum%septic` | character (len=40) |  | septic tanks (pointer to septic.str) |
| 13 |  | `lum%fstrip` | character (len=40) |  | filter strips (pointer to filterstrip.str) |
| 14 |  | `lum%grassww` | character (len=40) |  | grass waterways (pointer to grassedww.str) |
| 15 |  | `lum%bmpuser` | character (len=40) |  | user specified removal efficiency (pointer to bmpuser.str) |

## Sample

```text
Example record from Ames_sub1 dataset (formatted as free format):
Corn_Continuous_30  ""  Corn_plantcov  Corn_mgtops  Corn_cnlu  NoCons  Residential  UrbanRO  usgs_reg  TileDrain1  SepticA  FilterStrip1  GrassWW1  BMPUser1
```

## Read Pattern

```fortran
open (107,file=in_lum%landuse_lum)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do while (eof == 0)
  read (107,*,iostat=eof) titldum
  imax = imax + 1
end do
allocate (lum(0:imax))
allocate (lum_str(0:imax))
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do ilu = 1, imax
  read (107,*,iostat=eof) lum(ilu)
end do
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_lum%landuse_lum)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) lum(ilu)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:landuse_read] | open, read, rewind, close | Reads the `landuse.lum` file, counts records, allocates the `lum` array, reads each land use record into `lum`, and resolves string pointers to indices in related databases such as plant communities, management operations, curve number land uses, conservation practices, tile drainage, septic tanks, filter strips, grass waterways, and BMP user options. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format is inferred from typical usage and naming conventions; no explicit example record is present in the source.
- The file is optional; if missing or set to "null", empty land use arrays are allocated.
- The reader resolves string fields to indices in various related databases and logs warnings if names are not found.
