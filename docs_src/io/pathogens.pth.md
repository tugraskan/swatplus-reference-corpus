---
kind: io
source_symbols:
- path_parm_read
title: '`pathogens.pth`'
status: filled
source_hash: 14546f565f5edb3c
version_label: SWAT+ 62.0.0
---

**Primary target:** `path_db(:)` (array of `type pathogen_db`)  
**Read by:** [sym:path_parm_read]

## Bottom Line

The file `pathogens.pth` configures pathogen properties for the SWAT+ model, including die-off and growth rates in various environmental compartments.

It is optional; if the file does not exist or is set to "null", the pathogen database array is allocated empty.

The reader `path_parm_read` loads this file into the `path_db` array of `type pathogen_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variable `in_parmdb%pathcom_db` used to locate the pathogens.pth file. |
| [sym:pathogen_data_module] | Provides the derived type `pathogen_db` and the `path_db` array where each pathogen record is stored. |
| [sym:maximum_data_module] | Provides the `db_mx%path` integer used to store the number of pathogen records read from the file. |

## File Variables

The file `pathogens.pth` consists of multiple records each describing a pathogen's properties. Each record is read into an element of the `path_db` array of derived type `pathogen_db`. The file contains a header and title lines that are skipped before reading the pathogen records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `path_db%pathnm` | character(len=16) |  | Pathogen name identifier |
| 3 |  | `path_db%do_soln` | real | 1/day | Die-off factor for persisting bacteria in soil solution |
| 4 |  | `path_db%gr_soln` | real | 1/day | Growth factor for persisting bacteria in soil solution |
| 5 |  | `path_db%do_sorb` | real | 1/day | Die-off factor for persisting bacteria adsorbed to soil particles |
| 6 |  | `path_db%gr_sorb` | real | 1/day | Growth factor for persisting bacteria adsorbed to soil particles |
| 7 |  | `path_db%kd` | real | none | Partition coefficient between solution and sorbed phase in surface runoff |
| 8 |  | `path_db%t_adj` | real | none | Temperature adjustment factor for bacterial die-off/growth |
| 9 |  | `path_db%washoff` | real | none | Fraction of persistent bacteria on foliage washed off by rainfall |
| 10 |  | `path_db%do_plnt` | real | 1/day | Die-off factor for persistent bacteria on foliage |
| 11 |  | `path_db%gr_plnt` | real | 1/day | Growth factor for persistent pathogen on foliage |
| 12 |  | `path_db%fr_manure` | real | none | Fraction of manure containing active colony forming units (CFU) |
| 13 |  | `path_db%perco` | real | none | Pathogen percolation coefficient ratio of solution bacteria in surface layer |
| 14 |  | `path_db%det_thrshd` | real | # cfu/m^2 | Threshold detection level for less persistent bacteria when pathogen levels are low |
| 15 |  | `path_db%do_stream` | real |  | Die-off factor for persistent pathogen in streams; below this level bacteria are considered insignificant and set to zero |
| 16 |  | `path_db%gr_stream` | real | 1/day | Growth factor for persistent pathogen in streams |
| 17 |  | `path_db%do_res` | real | 1/day | Die-off factor for less persistent pathogen in reservoirs |
| 18 |  | `path_db%gr_res` | real | 1/day | Growth factor for less persistent pathogen in reservoirs |
| 19 |  | `path_db%conc_min` | real |  | Minimum pathogen concentration |

## Sample

```text
Example record format (fields separated by spaces or commas):
1 PathogenName 0.01 0.005 0.02 0.01 0.5 1.0 0.3 0.01 0.005 0.2 0.1 0.05 100.0 0.001 0.002 0.003 0.004 0.0001
```

## Read Pattern

```fortran
open (107,file=in_parmdb%pathcom_db)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) path_db(ibac)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_parmdb%pathcom_db)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) path_db(ibac)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:path_parm_read] | backspace, close, open, read, rewind | Reads the pathogen properties from the file `pathogens.pth` into the `path_db` array. It first checks if the file exists and is not set to "null". If the file exists, it counts the number of pathogen records, allocates the `path_db` array accordingly, then reads each pathogen record into the array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format is inferred as the source code does not provide explicit example records.
- The file is optional; if missing or set to "null", an empty pathogen database is allocated.
- The reader uses multiple reads of title and header lines to count records before actual reading.
