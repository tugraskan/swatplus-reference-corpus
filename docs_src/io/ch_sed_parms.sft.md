---
kind: io
source_symbols:
- ch_read_parms_cal
title: '`ch_sed_parms.sft`'
status: filled
source_hash: 7e410bdc4bfe58ce
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_prms(:)` (array of `type soft_calib_parms`)  
**Read by:** [sym:ch_read_parms_cal]

## Bottom Line

`ch_sed_parms.sft` lists the channel-sediment parameters that soft calibration is allowed to adjust, with the change type and the negative/positive change limits and lower/upper value bounds for each.

The reader `ch_read_parms_cal` reads a title line, the record count `mchp`, and a header, then reads each record (name, change type, and the four limits) into `ch_prms(i)`.

The file is optional; if `in_chg%ch_sed_parms_sft` is missing or `null`, `ch_prms` is allocated with zero size.

| Module | Role for this file |
| --- | --- |
| [sym:calibration_data_module] | Defines `type soft_calib_parms` and the `ch_prms` array each record is read into. |
| [sym:input_file_module] | Supplies `in_chg`; `in_chg%ch_sed_parms_sft` holds the `ch_sed_parms.sft` filename opened on unit 107. |

## File Variables

`ch_sed_parms.sft` has a title line, an integer record count `mchp`, and a column-header line, followed by one record per adjustable channel-sediment parameter. Each record gives the parameter name, the change type, and the negative/positive change limits and lower/upper value bounds.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| - | `record count` | `mchp` | integer |  | number of channel-sediment soft-calibration parameter records |
| 1 | `name` | `ch_prms%name` | character(len=16) |  | parameter name (e.g. cover, erod, etc.) crosswalked to the parameter database |
| 2 | `chg_typ` | `ch_prms%chg_typ` | character(len=16) |  | type of change: absval, abschg, or pctchg |
| 3 | `neg` | `ch_prms%neg` | real |  | negative limit of the allowed change during soft calibration |
| 4 | `pos` | `ch_prms%pos` | real |  | positive limit of the allowed change during soft calibration |
| 5 | `lo` | `ch_prms%lo` | real |  | lower limit of the parameter value |
| 6 | `up` | `ch_prms%up` | real |  | upper limit of the parameter value |

## Sample

```text
Schematic of the record layout (field names in read order, not a specific dataset):

<title line>
2                          ! mchp: number of parameter records
name    chg_typ  neg     pos     lo      up
cover   pctchg  -20.0    20.0    0.0     1.0
erod    pctchg  -50.0    50.0    0.0     10.0
```

## Read Pattern

```fortran
open (107,file=in_chg%ch_sed_parms_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mchp
read (107,*,iostat=eof) header
read (107,*,iostat=eof) ch_prms(i)%name, ch_prms(i)%chg_typ, ch_prms(i)%neg, ch_prms(i)%pos, ch_prms(i)%lo, ch_prms(i)%up
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%ch_sed_parms_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mchp` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) ch_prms(i)%name, ch_prms(i)%chg_typ, ch_prms(i)%neg, ch_prms(i)%pos, ch_prms(i)%lo, ch_prms(i)%up` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_parms_cal] | open, read | Opens `ch_sed_parms.sft` on unit 107, reads the title, record count, and header, allocates `ch_prms(mchp)`, then reads each parameter record (name, change type, and four limits). |

## Review Notes

- `chg_typ` accepts `absval`, `abschg`, or `pctchg`.
- `neg`/`pos` bound the change applied; `lo`/`up` bound the resulting parameter value.
- If `ch_sed_parms.sft` is missing or `null`, `ch_prms` is allocated with zero size.
