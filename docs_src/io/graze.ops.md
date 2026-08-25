---
kind: io
source_symbols:
- mgt_read_grazeops
title: '`graze.ops`'
status: filled
source_hash: 6a1d83e3eea54eb2
version_label: SWAT+ 62.0.0
---

**Primary target:** `grazeop_db(:)` (array of `type grazing_operation`)  
**Read by:** [sym:mgt_read_grazeops]

## Bottom Line

The input file `graze.ops` defines grazing operations parameters for the SWAT+ model, specifying biomass removal and manure deposition rates associated with grazing activities.

This file is optional; if it does not exist or is set to "null", an empty grazing operation database is allocated.

The file is read and parsed by the `mgt_read_grazeops` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_ops` variable which contains the filename for `graze.ops` |
| [sym:maximum_data_module] | provides `db_mx` which stores the maximum counts and the total number of grazing operations read |
| [sym:mgt_operations_module] | provides the `grazing_operation` type and the `grazeop_db` array where the grazing operations are stored |
| [sym:fertilizer_data_module] | provides the `fertdb` array and `db_mx%fertparm` for cross-referencing fertilizer names to fertilizer IDs |

## File Variables

The `graze.ops` file contains records of grazing operations, each record specifying parameters such as the operation name, associated fertilizer name, biomass removal rates by grazing and trampling, manure deposition rate, and minimum plant biomass required for grazing. Each record is read into an element of the `grazeop_db` array of type `grazing_operation`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `grazeop_db%name` | character (len=40) |  | Name of the grazing operation |
| 3 |  | `grazeop_db%fertnm` | character (len=40) |  | Name of the fertilizer associated with the grazing operation |
| 4 |  | `grazeop_db%manure_id` | integer |  | Fertilizer number cross-referenced from fertilizer.frt database |
| 5 |  | `grazeop_db%eat` | real | (kg/ha)/day | Dry weight of biomass removed by grazing daily |
| 6 |  | `grazeop_db%tramp` | real | (kg/ha)/day | Dry weight of biomass removed by trampling daily |
| 7 |  | `grazeop_db%manure` | real | (kg/ha)/day | Dry weight of manure deposited daily |
| 8 |  | `grazeop_db%biomin` | real | kg/ha | Minimum plant biomass required for grazing to occur |

## Sample

```text
Example record lines from a typical `graze.ops` file:
Name_of_Operation Fertilizer_Name 1.5 0.2 0.3 100.0
Another_Operation Fertilizer_X    2.0 0.1 0.4 150.0
```

## Read Pattern

```fortran
open (107,file=in_ops%graze_ops)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) grazeop_db(igrazop)%name, grazeop_db(igrazop)%fertnm, grazeop_db(igrazop)%eat, grazeop_db(igrazop)%tramp, grazeop_db(igrazop)%manure, grazeop_db(igrazop)%biomin
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ops%graze_ops)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) grazeop_db(igrazop)%name, grazeop_db(igrazop)%fertnm, grazeop_db(igrazop)%eat, grazeop_db(igrazop)%tramp, grazeop_db(igrazop)%manure, grazeop_db(igrazop)%biomin` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_grazeops] | open, read, rewind, close | Reads the `graze.ops` file, counts the number of grazing operation records, allocates the `grazeop_db` array accordingly, reads each grazing operation record into `grazeop_db`, and cross-references fertilizer names to fertilizer IDs. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format is a constructed example based on the expected fields and types; no explicit example record was found in the source.
