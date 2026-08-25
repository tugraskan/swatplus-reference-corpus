---
kind: io
source_symbols:
- hydrol_read
title: '`hydrology.hyd`'
status: filled
source_hash: 5b3d4a48675e3dda
version_label: SWAT+ 62.0.0
---

**Primary target:** `hyd_db(:)` (array of `type hydrology_db`)  
**Read by:** [sym:hydrol_read]

## Bottom Line

The file `hydrology.hyd` configures hydrology parameters for the SWAT+ model, defining properties such as lateral flow travel time, sediment concentrations, canopy storage, and various soil and plant water factors.

This file is optional; if it does not exist or is set to "null", an empty hydrology database array is allocated.

The primary reader for this file is the `hydrol_read` subroutine, which reads the file into the `hyd_db` array of `type hydrology_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the file path variable `in_hyd%hydrol_hyd` used to locate the hydrology input file. |
| [sym:maximum_data_module] | provides the global maximum data structure `db_mx` whose `hyd` field is set to the number of hydrology records read. |
| [sym:hydrology_data_module] | provides the derived type `type hydrology_db` and the `hyd_db` array where the file records are stored. |

## File Variables

The file `hydrology.hyd` consists of multiple records each corresponding to an instance of `type hydrology_db`. Each record contains hydrology-related parameters such as names, coefficients, and concentrations that configure the hydrology state in the model.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `hyd_db%name` | character(len=16) | none | name |
| 3 |  | `hyd_db%lat_ttime` | real | days | Exponential of the lateral flow travel time |
| 4 |  | `hyd_db%lat_sed` | real | g/L | sediment concentration in lateral flow |
| 5 |  | `hyd_db%canmx` | real | mm H2O | maximum canopy storage |
| 6 |  | `hyd_db%esco` | real | none | soil evaporation compensation factor (0-1) |
| 7 |  | `hyd_db%epco` | real | none | plant water uptake compensation factor (0-1) |
| 8 |  | `hyd_db%erorgn` | real | none | organic N enrichment ratio, if left blank |
| 9 |  | `hyd_db%erorgp` | real | % | the model will calculate for every event organic P enrichment ratio, if left blank |
| 10 |  | `hyd_db%cn3_swf` | real | % | the model will calculate for every event soil water at cn3 - 0=fc; .99=near saturation |
| 11 |  | `hyd_db%biomix` | real | none | biological mixing efficiency. |
| 12 |  | `hyd_db%perco` | real | % | Mixing of soil due to activity of earthworms and other soil biota. Mixing is performed at the end of every calendar year. percolation coefficient - linear adjustment to daily perc |
| 13 |  | `hyd_db%lat_orgn` | real | ppm | organic N concentration in lateral flow |
| 14 |  | `hyd_db%lat_orgp` | real | ppm | organic P concentration in lateral flow |
| 15 |  | `hyd_db%pet_co` | real | none | coefficient related to radiation used in Hargreaves equation |
| 16 |  | `hyd_db%latq_co` | real | none | lateral soil flow coefficient - linear adjustment to daily lat flow |

## Sample

```text
Example record block from Ames_sub1 dataset (not shown in source):
  "ExampleName" 0.5 10.0 2.0 0.8 0.9 1.1 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.3
```

## Read Pattern

```fortran
open (107,file=in_hyd%hydrol_hyd)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) hyd_db(ithyd)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_hyd%hydrol_hyd)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) hyd_db(ithyd)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:hydrol_read] | close, open, read, rewind | Reads the hydrology parameters from the `hydrology.hyd` file into the `hyd_db` array. It first checks if the file exists or is set to "null"; if not, it counts the number of records, allocates the array, rewinds the file, and reads all hydrology records. It updates the global maximum hydrology count `db_mx%hyd` accordingly. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format example is illustrative only; no actual example record was present in the source.
