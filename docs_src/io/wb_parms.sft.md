---
kind: io
source_symbols:
- ls_read_lsparms_cal
title: '`wb_parms.sft`'
status: filled
source_hash: 0b3527cf277e1e2b
version_label: SWAT+ 62.0.0
---

**Primary target:** `ls_prms(:)` (array of `type soft_calib_parms`)  
**Read by:** [sym:ls_read_lsparms_cal]

## Bottom Line

The file `wb_parms.sft` is an optional soft calibration parameter file that configures calibration adjustments for parameters such as curve numbers (cn2), terraces, land use, and management practices within the SWAT+ model.

It is read by the subroutine `ls_read_lsparms_cal`, which loads the file contents into the array `ls_prms` of type `soft_calib_parms`.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides the variable `db_mx` used to store the number of soft calibration parameters read (`db_mx%lscal_prms`). |
| [sym:calibration_data_module] | Defines the derived type `soft_calib_parms` and the array `ls_prms` where the file records are stored. |
| [sym:input_file_module] | Supplies the input file path variable `in_chg%wb_parms_sft` that specifies the location of the `wb_parms.sft` file. |

## File Variables

The file consists of a header block followed by multiple records, each corresponding to a soft calibration parameter stored as an element of the `ls_prms` array of type `soft_calib_parms`. Each record contains fields describing the parameter name, database crosswalk number, type of change, and numeric limits for calibration adjustments.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ls_prms%name` | character(len=16) |  | cn2, terrace, land use, mgt, etc. |
| 3 |  | `ls_prms%num_db` | integer |  | crosswalk number of parameter, structure or land use to get database array number |
| 4 |  | `ls_prms%chg_typ` | character(len=16) |  | type of change (absval,abschg,pctchg) |
| 5 |  | `ls_prms%neg` | real |  | negative limit of change |
| 6 |  | `ls_prms%pos` | real |  | positive limit of change |
| 7 |  | `ls_prms%lo` | real |  | lower limit of parameter |
| 8 |  | `ls_prms%up` | real |  | upper limit of parameter |

## Sample

```text
Example record block from `wb_parms.sft` (not from source, illustrative only):
Title line (ignored): "Soft Calibration Parameters"
Number of parameters: 3
Header line (ignored): "Name ChgTyp Neg Pos Lo Up"
Records:
cn2           absval  -0.1  0.1  0.0  1.0
terrace       pctchg  -5.0  5.0  0.0  100.0
landuse       abschg  -0.2  0.2  0.0  1.0
```

## Read Pattern

```fortran
open (107,file = in_chg%wb_parms_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mlsp
read (107,*,iostat=eof) header
read (107,*,iostat=eof) ls_prms(i)%name, ls_prms(i)%chg_typ, ls_prms(i)%neg, ls_prms(i)%pos, ls_prms(i)%lo, ls_prms(i)%up
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file = in_chg%wb_parms_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mlsp` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) ls_prms(i)%name, ls_prms(i)%chg_typ, ls_prms(i)%neg, ls_prms(i)%pos, ls_prms(i)%lo, ls_prms(i)%up` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ls_read_lsparms_cal] | close, open, read | Reads the optional soft calibration parameter file `wb_parms.sft` if it exists and is not set to "null". It opens the file, reads header lines and the number of parameters, allocates the `ls_prms` array accordingly, and reads each parameter record into `ls_prms`. It also updates `db_mx%lscal_prms` with the number of parameters read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional: if the file does not exist or is set to "null", the parameter array is allocated with zero size.
- The `num_db` field is read from the file but not assigned in the reader; it is part of the `soft_calib_parms` type but not populated by this reader, possibly set elsewhere or defaulted.
- Sample read format is illustrative; no actual example records were found in the source.
