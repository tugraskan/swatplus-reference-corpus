---
kind: io
source_symbols:
- septic_parm_read
title: '`septic.sep`'
status: filled
source_hash: ca44c7136e77ba26
version_label: SWAT+ 62.0.0
---

**Primary target:** `sepdb(:)` (array of `type septic_db`)  
**Read by:** [sym:septic_parm_read]

## Bottom Line

The `septic.sep` input file configures septic tank effluent parameters for the model, specifying flow rates and concentrations of various pollutants per septic system.

This file is optional; if it does not exist or is set to "null", the septic database array is allocated with zero size.

The file is read by the `septic_parm_read` subroutine, which loads its data into the `sepdb` array of `type septic_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_parmdb` variable that holds the file path for `septic.sep`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable, specifically `db_mx%sep`, which stores the number of septic records read from the file. |
| [sym:septic_data_module] | Defines the `type septic_db` and the `sepdb` array where the file records are stored. |

## File Variables

The `septic.sep` file consists of records each corresponding to a septic tank configuration. Each record is read into an element of the `sepdb` array of derived type `septic_db`. The file columns map directly to the components of `type septic_db`, including a name identifier and various flow and concentration parameters.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sepdb%sepnm` | character(len=20) |  | Septic tank name or identifier |
| 3 |  | `sepdb%qs` | real | m3/d | flow rate of the septic tank effluent per capita (sptq) |
| 4 |  | `sepdb%bodconcs` | real | mg/l | biological oxygen demand of the septic tank effluent |
| 5 |  | `sepdb%tssconcs` | real | mg/l | concentration of total suspended solid in the septic tank effluent |
| 6 |  | `sepdb%nh4concs` | real | mg/l | concentration of total phosphorus in the septic tank effluent |
| 7 |  | `sepdb%no3concs` | real | mg/l | concentration of nitrate in the septic tank effluent |
| 8 |  | `sepdb%no2concs` | real | mg/l | concentration of nitrite in the septic tank effluent |
| 9 |  | `sepdb%orgnconcs` | real | mg/l | concentration of organic nitrogen in the septic tank effluent |
| 10 |  | `sepdb%minps` | real | mg/l | concentration of mineral phosphorus in the septic tank effluent |
| 11 |  | `sepdb%orgps` | real | mg/l | concentration of organic phosphorus in the septic tank effluent |
| 12 |  | `sepdb%fcolis` | real | mg/l | concentration of fecal coliform in the septic tank effluent |

## Sample

```text
Example record lines are not provided in the source code; typical records contain a leading identifier string followed by the columns matching the `septic_db` type fields.
```

## Read Pattern

```fortran
open (171,file=in_parmdb%septic_sep)
read (171,*,iostat=eof) titldum
read (171,*,iostat=eof) header
rewind (171)
backspace (171)
read (171,*,iostat=eof) sepdb(is)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 171 | `open (171,file=in_parmdb%septic_sep)` |
| Input | `read` | 171 | `read (171,*,iostat=eof) titldum` |
| Input | `read` | 171 | `read (171,*,iostat=eof) header` |
| Input | `read` | 171 | `read (171,*,iostat=eof) titldum` |
| File control | `rewind` | 171 | `rewind (171)` |
| Input | `read` | 171 | `read (171,*,iostat=eof) titldum` |
| Input | `read` | 171 | `read (171,*,iostat=eof) header` |
| Input | `read` | 171 | `read (171,*,iostat=eof) titldum` |
| File control | `backspace` | 171 | `backspace (171)` |
| Input | `read` | 171 | `read (171,*,iostat=eof) sepdb(is)` |
| File control | `close` | 171 | `close (171)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:septic_parm_read] | backspace, close, open, read, rewind | Reads the `septic.sep` file if it exists and is not set to "null". It counts the number of records to allocate the `sepdb` array, then reads each septic tank configuration record into `sepdb`. If the file does not exist or is "null", it allocates an empty `sepdb` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample record format is not shown in the source; users should consult example datasets for exact formatting.
- The ammonium concentration field `nh4concs` is documented in source comments as total phosphorus concentration, which appears to be a documentation inconsistency; the field name suggests ammonium concentration.
