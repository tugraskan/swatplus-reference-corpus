---
kind: io
source_symbols:
- sdr_read
title: '`tiledrain.str`'
status: filled
source_hash: 815e3f0cfcffb625
version_label: SWAT+ 62.0.0
---

**Primary target:** `sdr(:)` (array of `type subsurface_drainage_parameters`)  
**Read by:** [sym:sdr_read]

## Bottom Line

The file `tiledrain.str` configures subsurface drainage parameters for hydrologic response units (HRUs) in SWAT+.

It is optional; if the file does not exist or is set to "null", no subsurface drainage data is loaded and the `sdr` array is allocated with zero length.

The reader `sdr_read` loads this file and populates the `sdr` array with subsurface drainage parameters.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file name string `in_str%tiledrain_str` used to locate the `tiledrain.str` file. |
| [sym:maximum_data_module] | provides the global data structure `db_mx` where the total number of subsurface drainage records read (`db_mx%sdr`) is stored. |
| [sym:hru_module] | provides the derived type `subsurface_drainage_parameters` and the array `sdr` where each record from the file is stored. |

## File Variables

The file `tiledrain.str` contains tabular records of subsurface drainage parameters, each record corresponding to one subsurface drainage configuration stored in an element of the `sdr` array of type `subsurface_drainage_parameters`. The file format includes a title line, a header line, and then multiple data records matching the fields of the `sdr` type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sdr%name` | character(len=40) |  | name identifier for the subsurface drainage configuration |
| 3 |  | `sdr%depth` | real | mm | depth of drain tube from the soil surface |
| 4 |  | `sdr%time` | real | hrs | time to drain soil to field capacity |
| 5 |  | `sdr%lag` | real | hours | drain tile lag time |
| 6 |  | `sdr%radius` | real | mm | effective radius of drains |
| 7 |  | `sdr%dist` | real | mm | distance between two drain tubes or tiles |
| 8 |  | `sdr%drain_co` | real | mm/day | drainage coefficient |
| 9 |  | `sdr%pumpcap` | real | mm/hr | pump capacity |
| 10 |  | `sdr%latksat` | real | !na | multiplication factor to determine lateral saturated hydraulic conductivity for profile |

## Sample

```text
Example record block from `tiledrain.str` (from typical SWAT+ datasets):
Title line (ignored): "Subsurface Drainage Parameters"
Header line (ignored): "Name Depth Time Lag Radius Dist Drain_Co PumpCap LatKsat"
Data lines (one per subsurface drainage configuration):
Drain1 100.0 24.0 1.5 50.0 200.0 5.0 0.1 1.0
Drain2 120.0 30.0 2.0 60.0 250.0 6.0 0.15 1.2
```

## Read Pattern

```fortran
open (107,file=in_str%tiledrain_str)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) sdr(isdr)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_str%tiledrain_str)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) sdr(isdr)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:sdr_read] | close, open, read, rewind | Reads the `tiledrain.str` file if it exists and is not set to "null", counts the number of subsurface drainage records, allocates the `sdr` array accordingly, then reads all subsurface drainage parameter records into the `sdr` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
