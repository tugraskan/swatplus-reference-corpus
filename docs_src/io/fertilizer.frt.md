---
kind: io
source_symbols:
- fert_parm_read
title: '`fertilizer.frt`'
status: filled
source_hash: 76916ce36aebf406
version_label: SWAT+ 62.0.0
---

**Primary target:** `fertdb(:)` (array of `type fertilizer_db`)  
**Read by:** [sym:fert_parm_read]

## Bottom Line

fertilizer.frt is an input file that defines fertilizer parameter records used by the model.

It is optional; if the file does not exist or is set to "null", an empty fertilizer database is allocated.

The file configures fertilizer composition fractions such as mineral nitrogen, mineral phosphorus, organic nitrogen, organic phosphorus, and ammonia nitrogen fractions.

The reader subroutine `fert_parm_read` in `fert_parm_read.f90` is responsible for loading this file into the `fertdb` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input parameter database variable `in_parmdb` which contains the filename `fert_frt` for fertilizer.frt |
| [sym:maximum_data_module] | provides the global database max counts variable `db_mx` where `fertparm` is set to the number of fertilizer records read |
| [sym:fertilizer_data_module] | provides the derived type `fertilizer_db` and the array `fertdb` where fertilizer records are stored |

## File Variables

The fertilizer.frt file consists of multiple records each corresponding to a fertilizer type. Each record is read into an element of the `fertdb` array of type `fertilizer_db`. The file schema includes a title line, a header line, and then multiple fertilizer records. Each fertilizer record contains fields for fertilizer name and fractional composition of mineral and organic nitrogen and phosphorus components.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `fertdb%fertnm` | character(len=16) |  | fertilizer name identifier |
| 3 |  | `fertdb%fminn` | real | kg minN/kg frt | fract of fert which is mineral nit (NO3+NH3) |
| 4 |  | `fertdb%fminp` | real | kg minN/kg frt | frac of fert which is mineral phos |
| 5 |  | `fertdb%forgn` | real | kg orgN/kg frt | frac of fert which is org n |
| 6 |  | `fertdb%forgp` | real | kg orgP/kg frt | frac of fert which is org p |
| 7 |  | `fertdb%fnh3n` | real | kg NH3-N/kg N | frac of mineral N content of fert which is NH3 |

## Sample

```text
Example fertilizer.frt record block (from typical dataset):
Title line (ignored): "Fertilizer Parameters"
Header line (ignored): "Name FminN FminP ForgN ForgP Fnh3N"
Records:
Urea           0.46 0.00 0.00 0.00 0.00
DAP            0.18 0.46 0.00 0.00 0.00
Manure         0.10 0.05 0.30 0.20 0.05
```

## Read Pattern

```fortran
open (107,file=in_parmdb%fert_frt)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) fertdb(it)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_parmdb%fert_frt)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) fertdb(it)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:fert_parm_read] | open, read, rewind, close | Reads the fertilizer.frt input file, counting the number of fertilizer records, allocating the `fertdb` array accordingly, and then reading each fertilizer record into `fertdb`. If the file does not exist or is set to "null", it allocates an empty fertilizer database. It sets the global count `db_mx%fertparm` to the number of fertilizer records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format example is inferred from typical fertilizer parameter files but not directly extracted from source; verify with actual datasets.
- The file is optional as per the existence check and null filename test in `fert_parm_read`.
