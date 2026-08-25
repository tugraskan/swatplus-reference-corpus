---
kind: io
source_symbols:
- plant_transplant_read
title: '`transplant.plt`'
status: filled
source_hash: 51253f2614d11d60
version_label: SWAT+ 62.0.0
---

**Primary target:** `transpl(:)` (array of `type plant_transplant_db`)  
**Read by:** [sym:plant_transplant_read]

## Bottom Line

The file `transplant.plt` provides plant transplant data configuring initial plant characteristics such as leaf area index, biomass, and population for the SWAT+ model.

It is optional; if the file does not exist or is named " null", an empty transplant array is allocated.

The reader `plant_transplant_read` loads this file and populates the `transpl` array of type `plant_transplant_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides file handling utilities and possibly the `db_mx` variable used to store the count of transplant records read. |
| [sym:maximum_data_module] | provides the `db_mx` variable, specifically `db_mx%transplant`, which stores the number of transplant records read from the file. |
| [sym:plant_data_module] | provides the derived type `plant_transplant_db` and the allocatable array `transpl` where the transplant records are stored. |

## File Variables

The file `transplant.plt` contains records of plant transplant data, each record mapped to an element of the `transpl` array of type `plant_transplant_db`. The file includes a title line, a header line, and multiple data lines corresponding to plant transplant parameters.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `transpl%name` | character(len=40) |  | plant species or variety name |
| 3 |  | `transpl%lai` | real | m**2/m**2 | leaf area index |
| 4 |  | `transpl%bioms` | real | kg/ha | land cover/crop biomass |
| 5 |  | `transpl%phuacc` | real | frac | fraction of plant heat unit accumulation |
| 6 |  | `transpl%fr_yrmat` | real | years | fraction of current year of growth to years to maturity |
| 7 |  | `transpl%pop` | real | plants/m^2 | plant population |

## Sample

```text
Example record lines are not present in the source; typical records include a leading identifier followed by fields matching the `plant_transplant_db` type columns.
```

## Read Pattern

```fortran
open (104,file="transplant.plt")
read (104,*,iostat=eof) titldum
read (104,*,iostat=eof) header
rewind (104)
read (104,*,iostat=eof) transpl(ic)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 104 | `open (104,file="transplant.plt")` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| Input | `read` | 104 | `read (104,*,iostat=eof) header` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| File control | `rewind` | 104 | `rewind (104)` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| Input | `read` | 104 | `read (104,*,iostat=eof) header` |
| Input | `read` | 104 | `read (104,*,iostat=eof) transpl(ic)` |
| File control | `close` | 104 | `close (104)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:plant_transplant_read] | open, read, rewind, close | Reads the `transplant.plt` file to populate the `transpl` array of `plant_transplant_db` records, including reading header lines and counting records to allocate the array properly. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or named " null", an empty transplant array is allocated.
- No example record lines were found in the source; sample data should be added from reference datasets if available.
