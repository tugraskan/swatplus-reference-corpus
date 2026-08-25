---
kind: io
source_symbols:
- mgt_read_harvops
title: '`harv.ops`'
status: filled
source_hash: 9ccc98130ef93a8f
version_label: SWAT+ 62.0.0
---

**Primary target:** `harvop_db(:)` (array of `type harvest_operation`)  
**Read by:** [sym:mgt_read_harvops]

## Bottom Line

The `harv.ops` file configures harvest-only operations in the model, specifying parameters like harvest index target, efficiency, and minimum biomass for harvest.

This file is optional; if it does not exist or is set to "null", an empty harvest operation database is allocated.

The reader `mgt_read_harvops` loads this file and populates the `harvop_db` array with its records.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_ops` variable which contains the filename for `harv.ops`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store the count of harvest operations read (`db_mx%harvop_db`). |
| [sym:mgt_operations_module] | Defines the `type harvest_operation` and the `harvop_db` array where the file records are stored. |

## File Variables

The `harv.ops` file consists of records describing harvest operations, each mapped to an element of the `harvop_db` array of type `harvest_operation`. Each record includes fields such as the operation name, type, harvest index override, efficiency, and minimum biomass for harvest.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `harvop_db%name` | character (len=40) |  | Name of the harvest operation |
| 3 |  | `harvop_db%typ` | character (len=40) | none | grain;biomass;residue;tree;tuber |
| 4 |  | `harvop_db%hi_ovr` | real | (kg/ha)/(kg/ha) | harvest index target specified at harvest |
| 5 |  | `harvop_db%eff` | real | none | harvest efficiency: fraction of harvested yield that is removed |
| 6 |  | `harvop_db%bm_min` | real |  | the remainder becomes residue on the soil surface minimum biomass to allow harvest |

## Sample

```text
Example record lines are not present in the source; typical records include fields matching the `harvest_operation` type such as name, type, hi_ovr, eff, and bm_min.
```

## Read Pattern

```fortran
open (107,file=in_ops%harv_ops)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) harvop_db(iharvop)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ops%harv_ops)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) harvop_db(iharvop)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_harvops] | open, read, rewind, close | Reads the `harv.ops` file if it exists and is not "null", counts the number of harvest operation records, allocates the `harvop_db` array accordingly, and reads all harvest operation records into `harvop_db`. If the file does not exist or is "null", allocates an empty `harvop_db` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- No example record lines were found in the source; sample read format is inferred from the type definition.
- The file is optional and may be set to "null" to disable harvest operations.
