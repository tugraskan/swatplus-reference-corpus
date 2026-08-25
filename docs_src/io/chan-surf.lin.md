---
kind: io
source_symbols:
- overbank_read
title: '`chan-surf.lin`'
status: filled
source_hash: 37ceae370cb2a1b4
version_label: SWAT+ 62.0.0
---

**Primary target:** `sd_ch(:)%fp` (the `floodplain_parameters` block of each degradation channel)  
**Read by:** [sym:overbank_read]

## Bottom Line

`chan-surf.lin` links each SWAT+ degradation channel to the surface (floodplain) objects that receive its overbank flooding. Each record names the floodplain, gives the number of surface objects, and lists each object's type and number.

The reader `overbank_read` reads a title line, the record count, and a header, then for each record reads the channel id, floodplain name, object count, and the (object type, object number) pairs into `sd_ch(i)%fp`.

The reader only processes the file when `in_link%chan_surf` exists (and is not `"null"`); otherwise no floodplain surface links are configured.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides `ch_sur`, allocated to the number of surface-link records. |
| [sym:input_file_module] | Supplies `in_link`; `in_link%chan_surf` holds the `chan-surf.lin` filename opened on unit 107. |
| [sym:maximum_data_module] | Supplies `db_mx`; the reader stores the surface-link count in `db_mx%ch_surf`. |
| [sym:sd_channel_module] | Defines `sd_ch` and `type floodplain_parameters`; each record fills `sd_ch(i)%fp` (name, obj_tot, obtyp, obtypno). |

## File Variables

`chan-surf.lin` has a title line, an integer record count, and a column-header line, followed by one record per channel surface link. Each record gives the channel id, the floodplain name, the number of surface objects `obj_tot`, and then that many (object type, object number) pairs. The reader stores these in the `fp` (floodplain) block of the matching `sd_ch` channel.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| - | `record count` | `mcha_sp` | integer |  | number of channel surface-link records in the file |
| 1 | `id` | `i` | integer |  | channel id; index into `sd_ch` for this surface link |
| 2 | `name` | `sd_ch%fp%name` | character(len=25) |  | name of the floodplain |
| 3 | `obj_tot` | `sd_ch%fp%obj_tot` | integer |  | number of surface (floodplain) objects listed on this record |
| 4.. | `obtyp` | `sd_ch%fp%obtyp(1:nspu)` | character(len=3) |  | object type for each surface object (1=hru, 2=hru_lte, 11=export coef, ...); repeats obj_tot times |
| 5.. | `obtypno` | `sd_ch%fp%obtypno(1:nspu)` | integer |  | object number for each surface object; paired with obtyp, repeats obj_tot times |

## Sample

```text
Schematic of the record layout (field names in read order, not a specific dataset):

<title line>
2                                  ! number of surface-link records
id  name        obj_tot  obtyp obtypno  obtyp obtypno ...
1   fldpln_1    2        1     5         1     6
3   fldpln_3    1        1     12
```

## Read Pattern

```fortran
open (107,file=in_link%chan_surf)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mcha_sp
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
read (107,*,iostat=eof) i, namedum, nspu
backspace (107)
read (107,*,iostat=eof) numb, sd_ch(i)%fp%name, sd_ch(i)%fp%obj_tot, (sd_ch(i)%fp%obtyp(isp), sd_ch(i)%fp%obtypno(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_link%chan_surf)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mcha_sp` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mcha_sp` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, namedum, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) numb, sd_ch(i)%fp%name, sd_ch(i)%fp%obj_tot, (sd_ch(i)%fp%obtyp(isp), sd_ch(i)%fp%obtypno(isp), isp = 1, nspu)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:overbank_read] | backspace, open, read | Opens `chan-surf.lin` on unit 107, reads the title, record count, and header, counts records to size `db_mx%ch_surf`, then reads each record; when a record lists surface objects it backspaces and re-reads the full line into `sd_ch(i)%fp` (name, obj_tot, and the obtyp/obtypno pairs). |

## Review Notes

- Each record is read twice: a first read gets the object count `nspu`; when `nspu > 0` the reader backspaces and re-reads the full line with the (type, number) pairs (overbank_read.f90:57-67).
- `obtyp` and `obtypno` repeat `obj_tot` times on the record, one pair per surface object.
- The file-exists guard uses `.or.` (`i_exist .or. name /= "null"`), so the read block is entered whenever the file exists.
- Object-type codes follow `floodplain_parameters%obtyp` (1=hru, 2=hru_lte, 11=export coefficient, ...).
