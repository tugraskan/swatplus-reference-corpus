---
kind: io
source_symbols:
- aqu2d_read
title: '`aqu_cha.lin`'
status: filled
source_hash: 6fd71490666a1ae0
version_label: SWAT+ 62.0.0
---

**Primary target:** `aq_ch(:)` (array of `type channel_aquifer_elements`)  
**Read by:** [sym:aqu2d_read]

## Bottom Line

The file `aqu_cha.lin` configures 2-D groundwater aquifer elements for the SWAT+ model.

It is optional and only read if the file exists and is not set to "null".

The reader subroutine `aqu2d_read` loads this file, allocating and populating the `aq_ch` array of `channel_aquifer_elements` accordingly.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the derived type `channel_aquifer_elements` and its components such as `hyd_output` and `geomorphic_baseflow_channel_data` used to store aquifer channel data read from the file. |
| [sym:input_file_module] | Supplies the `in_link` variable which contains the filename `aqu_cha` used to open and read the input file. |
| [sym:maximum_data_module] | Provides variables such as `defunit_num` used to initialize the `num` array in `aq_ch` after reading element counts. |

## File Variables

The file `aqu_cha.lin` contains records describing aquifer channel elements for the 2-D groundwater model. Each record corresponds to one aquifer channel element stored in the `aq_ch` array of `channel_aquifer_elements`. The file columns map to the components of this derived type, including name, element counts, channel numbers, total length, and hydrograph data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `aq_ch%name` | character(len=16) |  | Name identifier of the aquifer channel element |
| 3 |  | `aq_ch%num_tot` | integer |  | Total number of elements in the aquifer channel |
| 4 |  | `aq_ch%num` | integer |  | Array of channel element numbers |
| 5 |  | `aq_ch%len_tot` | real | km | Total length of channels in the aquifer (kilometers) |
| 6 |  | `aq_ch%hd` | type (hyd_output) |  | Baseflow hydrograph data for the aquifer |
| 7 |  | `aq_ch%ch` | type (geomorphic_baseflow_channel_data) |  | Geomorphic baseflow channel data associated with the aquifer channel |

## Sample

```text
Example record block from `aqu_cha.lin` (format inferred from reader):
  <integer record id>
  <integer iaq> <character(16) name> <integer nspu>
  <integer numb> <character(16) name> <integer nspu> <elem_cnt(1)> <elem_cnt(2)> ... <elem_cnt(nspu)>
```

## Read Pattern

```fortran
open (107,file=in_link%aqu_cha)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
read (107,*) titldum
read (107,*) header
read (107,*,iostat=eof) iaq, namedum, nspu
backspace (107)
read (107,*,iostat=eof) numb, aq_ch(iaq)%name, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_link%aqu_cha)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*) titldum` |
| Input | `read` | 107 | `read (107,*) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) iaq, namedum, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) numb, aq_ch(iaq)%name, nspu, (elem_cnt(isp), isp = 1, nspu)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:aqu2d_read] | backspace, close, open, read, rewind | Reads the `aqu_cha.lin` file if it exists and is not "null". It determines the maximum record index, allocates the `aq_ch` array accordingly, and reads each aquifer channel element's data into `aq_ch`. It also allocates and initializes element count arrays and channel number arrays for each aquifer channel element. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as the reader checks for existence and skips allocation if missing or set to "null".
- The reader uses `define_unit_elements` and `defunit_num` from `maximum_data_module` to allocate and initialize channel element numbers.
- No explicit sample data block was found in the source; the sample read format is inferred from read statements.
- The meaning of some fields like `aq_ch%ch` is from the type definition but not explicitly documented in the reader source.
