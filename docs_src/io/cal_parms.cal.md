---
kind: io
source_symbols:
- cal_parm_read
title: '`cal_parms.cal`'
status: filled
source_hash: ec1a117986f8d8a4
version_label: SWAT+ 62.0.0
---

**Primary target:** `cal_parms(:)` (array of `type calibration_parameters`)  
**Read by:** [sym:cal_parm_read]

## Bottom Line

The file `cal_parms.cal` contains calibration parameter change definitions used to adjust model parameters during calibration.

It is optional; if the file does not exist or is set to "null", no calibration parameters are loaded.

The reader `cal_parm_read` loads this file and populates the `cal_parms` array with these parameter definitions.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_chg` variable which contains the filename `cal_parms` used to open the calibration parameter file. |
| [sym:maximum_data_module] | provides the `db_mx` variable where the number of calibration parameters read (`cal_parms`) is stored in `db_mx%cal_parms`. |
| [sym:calibration_data_module] | provides the derived type `calibration_parameters` which defines the structure of each calibration parameter record stored in `cal_parms`. |

## File Variables

The file consists of a header block followed by a count of calibration parameters and then a list of calibration parameter records. Each record maps to an element of the `cal_parms` array of type `calibration_parameters`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cal_parms%name` | character(len=25) |  | cn2, esco, awc, etc. |
| 3 |  | `cal_parms%ob_typ` | character(len=25) |  | object type the parameter is associated with (hru, chan, res, basin, etc) |
| 4 |  | `cal_parms%absmin` | real |  | minimum range for variable |
| 5 |  | `cal_parms%absmax` | real |  | maximum change for variable |
| 6 |  | `cal_parms%units` | character(len=25) |  | units used for each parameter |

## Sample

```text
Example calibration parameter file snippet:
Title line (ignored)
Number of parameters to change (integer)
Header line (ignored)
Parameter records, one per line, e.g.:
cn2       hru    0.0    1.0    null
esco      hru    0.0    1.0    null
```

## Read Pattern

```fortran
open (107,file=in_chg%cal_parms)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mchg_par
read (107,*,iostat=eof) header
read (107,*,iostat=eof) cal_parms(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%cal_parms)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mchg_par` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cal_parms(i)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cal_parm_read] | open, read | Reads the calibration parameter file `cal_parms.cal` if it exists and is not set to "null". It reads a title line, the number of parameters to change, a header line, and then reads each calibration parameter record into the `cal_parms` array. If the file does not exist or is "null", it allocates an empty `cal_parms` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as per the existence check and null string test in `cal_parm_read`.
- The reader `cal_parm_read` uses `in_chg%cal_parms` from `input_file_module` as the filename.
- The number of parameters read is stored in `db_mx%cal_parms` from `maximum_data_module`.
- The parameter records are stored as elements of `cal_parms` of type `calibration_parameters` from `calibration_data_module`.
