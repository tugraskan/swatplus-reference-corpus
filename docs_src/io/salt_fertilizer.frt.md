---
kind: io
source_symbols:
- salt_fert_read
title: '`salt_fertilizer.frt`'
status: filled
source_hash: 14e59e62928295f8
version_label: SWAT+ 62.0.0
---

**Primary target:** `fert_salt(:)` (array of `type fert_db_salt`)  
**Read by:** [sym:salt_fert_read]

## Bottom Line

salt_fertilizer.frt is an optional input file that provides salt ion fertilizer loading rates in kg/ha for various fertilizer types.

It configures the fertilizer salt ion loading state in the model.

The file is read by the `salt_fert_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the `db_mx` variable which contains `fertparm`, the number of fertilizer parameter records to read and allocate. |
| [sym:input_file_module] | Provides the `fert_salt_flag` logical flag that is set to 1 when the fertilizer salt data is successfully read. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to determine the size of the fertilizer salt array allocation. |
| [sym:salt_module] | Defines the `fert_salt` array of type `fert_db_salt` where the fertilizer salt ion loading data is stored. |

## File Variables

The file consists of multiple records each representing a fertilizer type's salt ion loading rates in kg/ha. Each record is read into an element of the `fert_salt` array of derived type `fert_db_salt`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `fert_salt%fertnm` | character(len=16) |  | Name or identifier of the fertilizer type |
| 3 |  | `fert_salt%so4` | real | kg so4/ha | fertilizer load of so4 (kg/ha) |
| 4 |  | `fert_salt%ca` | real | kg ca/ha | fertilizer load of ca (kg/ha) |
| 5 |  | `fert_salt%mg` | real | kg mg/ha | fertilizer load of mg (kg/ha) |
| 6 |  | `fert_salt%na` | real | kg na/ha | fertilizer load of na (kg/ha) |
| 7 |  | `fert_salt%k` | real | kg k/ha | fertilizer load of k (kg/ha) |
| 8 |  | `fert_salt%cl` | real | kg cl/ha | fertilizer load of cl (kg/ha) |
| 9 |  | `fert_salt%co3` | real | kg co3/ha | fertilizer load of co3 (kg/ha) |
| 10 |  | `fert_salt%hco3` | real | kg hco3/ha | fertilizer load of hco3 (kg/ha) |

## Sample

```text
Example record format from salt_fertilizer.frt:
FERTILIZER1  10.0  5.0  2.0  1.0  3.0  4.0  0.5  0.2  0.1
FERTILIZER2  0.0   0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
```

## Read Pattern

```fortran
open (107,file="salt_fertilizer.frt")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*) fert_salt(isalti)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="salt_fertilizer.frt")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*) fert_salt(isalti)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:salt_fert_read] | close, open, read | Reads the salt ion fertilizer loading rates from salt_fertilizer.frt into the `fert_salt` array, allocating it based on the number of fertilizer parameters. Sets a flag indicating the fertilizer salt data has been loaded. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; the reader checks for existence before reading.
- The fertilizer type name (`fertnm`) has no explicit description in source; assumed to be the fertilizer identifier.
- Sample record format is inferred from the type fields and typical fertilizer data; no explicit example in source.
