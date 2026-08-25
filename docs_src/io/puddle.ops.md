---
kind: io
source_symbols:
- mgt_read_puddle
title: '`puddle.ops`'
status: filled
source_hash: cad9b36890e706b4
version_label: SWAT+ 62.0.0
---

**Primary target:** `pudl_db(:)` (array of `type puddle_operation`)  
**Read by:** [sym:mgt_read_puddle]

## Bottom Line

The file `puddle.ops` configures puddling-related soil hydraulic and nutrient properties after puddling operations.

It is optional and only read if the file exists and is not named " null".

The reader subroutine `mgt_read_puddle` loads this file into the array `pudl_db` of type `puddle_operation`.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | provides the global variable `db_mx` used to store the count of puddle records read (`db_mx%pudl_db`) |
| [sym:mgt_operations_module] | provides the derived type `puddle_operation` and the array `pudl_db` where the puddling data records are stored |

## File Variables

The file `puddle.ops` consists of multiple records each representing puddling operations with soil hydraulic and nutrient parameters after puddling. Each record is read into an element of the array `pudl_db` of derived type `puddle_operation`. The file includes two header lines before the data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pudl_db%name` | character (len=40) |  | name identifier for the puddling operation |
| 3 |  | `pudl_db%wet_hc` | real | mm/h | hydraulic conductivity of upper layer of soil after puddling |
| 4 |  | `pudl_db%sed` | real | ppm | sediment concentration after puddling |
| 5 |  | `pudl_db%orgn` | real | ppm | organic N concentration after puddling |
| 6 |  | `pudl_db%sedp` | real | ppm | organic P concentration after puddling |
| 7 |  | `pudl_db%no3` | real | ppm | NO3-N concentration after puddling |
| 8 |  | `pudl_db%solp` | real | ppm | mineral (soluble P) concentration after puddling |
| 9 |  | `pudl_db%nh3` | real | ppm | NH3 concentration after puddling |
| 10 |  | `pudl_db%no2` | real | ppm | NO2 concentration after puddling |

## Sample

```text
Example record format (after two header lines):
  "OperationName" 12.5 0.3 1.2 0.05 0.02 0.1 0.03 0.01 0.005
```

## Read Pattern

```fortran
open (104,file="puddle.ops")
read (104,*,iostat=eof) titldum
read (104,*,iostat=eof) header
rewind (104)
read (104,*,iostat=eof) pudl_db(ic)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 104 | `open (104,file="puddle.ops")` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| Input | `read` | 104 | `read (104,*,iostat=eof) header` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| File control | `rewind` | 104 | `rewind (104)` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| Input | `read` | 104 | `read (104,*,iostat=eof) header` |
| Input | `read` | 104 | `read (104,*,iostat=eof) pudl_db(ic)` |
| File control | `close` | 104 | `close (104)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_puddle] | open, read, rewind, close | Reads the puddling operations data from `puddle.ops` into the array `pudl_db`. It first checks if the file exists, counts the number of records, allocates the array, then reads all records into `pudl_db`. It also updates the global count `db_mx%pudl_db`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not named " null".
- The sample record format is inferred from the type fields and typical SWAT+ input style; no explicit example data lines were found in the source.
