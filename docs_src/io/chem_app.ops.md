---
kind: io
source_symbols:
- mgt_read_chemapp
title: '`chem_app.ops`'
status: filled
source_hash: 785bfeff94c8bba9
version_label: SWAT+ 62.0.0
---

**Primary target:** `chemapp_db(:)` (array of `type chemical_application_operation`)  
**Read by:** [sym:mgt_read_chemapp]

## Bottom Line

The file `chem_app.ops` configures chemical application operations used in the management simulation.

It is optional; if the file does not exist or is set to "null", an empty array is allocated.

The reader `mgt_read_chemapp` loads this file and populates the `chemapp_db` array with operation records.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_ops` variable which contains the filename for `chem_ops` used to open the input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable where the total number of chemical application operations read (`chemapp_db` size) is stored. |
| [sym:mgt_operations_module] | Defines the derived type `chemical_application_operation` and the array `chemapp_db` where the file records are stored. |

## File Variables

The file consists of multiple records each representing a chemical application operation. Each record is read into an element of the `chemapp_db` array of type `chemical_application_operation`. The file includes header lines that are read and discarded before reading the actual data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `chemapp_db%name` | character (len=40) |  | Name of the chemical application operation |
| 3 |  | `chemapp_db%form` | character (len=40) |  | solid; liquid |
| 4 |  | `chemapp_db%op_typ` | character (len=40) |  | operation type-spread; spray; inject; direct |
| 5 |  | `chemapp_db%app_eff` | real |  | application efficiency |
| 6 |  | `chemapp_db%foliar_eff` | real |  | foliar efficiency |
| 7 |  | `chemapp_db%inject_dep` | real | mm | injection depth |
| 8 |  | `chemapp_db%surf_frac` | real |  | surface fraction-amount in upper 10 mm |
| 9 |  | `chemapp_db%drift_pot` | real |  | drift potential |
| 10 |  | `chemapp_db%aerial_unif` | real |  | aerial uniformity |

## Sample

```text
Example record block from a typical `chem_app.ops` file is not present in the source; user should consult a reference dataset such as Ames_sub1 for format examples.
```

## Read Pattern

```fortran
open (107,file=in_ops%chem_ops)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) chemapp_db(ichemapp)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ops%chem_ops)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) chemapp_db(ichemapp)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_chemapp] | close, open, read, rewind | Reads the chemical application operations file `chem_app.ops` if it exists and is not set to "null". It counts the number of records to allocate the `chemapp_db` array, then reads each chemical application operation record into this array. If the file does not exist or is set to "null", an empty array is allocated. The total number of operations read is stored in `db_mx%chemapp_db`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- No sample record block is present in the source; users should refer to example datasets for format details.
