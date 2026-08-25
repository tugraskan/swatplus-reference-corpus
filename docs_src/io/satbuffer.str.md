---
kind: io
source_symbols:
- sat_buff_read
title: '`satbuffer.str`'
status: filled
source_hash: 9750cc23942b0273
version_label: SWAT+ 62.0.0
---

**Primary target:** `satbuff_db(:)` (array of `type saturated_buffer_parameters`)  
**Read by:** [sym:sat_buff_read]

## Bottom Line

The file `satbuffer.str` configures saturated buffer parameters that define tile inflow sources and receiving HRUs for saturated buffer flow routing.

It is optional and only read if the file exists.

The reader subroutine `sat_buff_read` loads this file and populates the `satbuff_db` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the external procedure `smp_buffer` referenced in the reader but not directly used in reading. |
| [sym:maximum_data_module] | Provides the global database object `db_mx` used to store the count of saturated buffer entries (`db_mx%sat_buff`) and access to decision tables (`db_mx%dtbl_flo`). |
| [sym:hru_module] | Provides the derived type `saturated_buffer_parameters` for `satbuff_db` and the `hru` array whose elements are assigned saturated buffer data read from the file. |
| [sym:conditional_module] | Provides the decision table array `dtbl_flo` used to crosswalk flow control decision table names to indices. |

## File Variables

The file `satbuffer.str` contains records of saturated buffer parameters, each record corresponding to one saturated buffer configuration entry. Each record is read into an element of the `satbuff_db` array of type `saturated_buffer_parameters`. The file format includes a title line, a header line, and then multiple data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `satbuff_db%name` | character(len=40) |  | Name identifier for the saturated buffer entry |
| 3 |  | `satbuff_db%hru_src` | integer |  | Source HRU providing tile inflow to the saturated buffer |
| 4 |  | `satbuff_db%frac_src` | real |  | Fraction of the source HRU contributing to tile flow |
| 5 |  | `satbuff_db%flocon_dtbl` | character(len=40) |  | Name of the flow control decision table governing flow into the buffer HRU |
| 6 |  | `satbuff_db%hru_rcv` | integer |  | Receiving (buffer) HRU that receives tile flow |
| 7 |  | `satbuff_db%lyr` | integer |  | Soil layer index for incoming tile flow (0 indicates surface layer) |

## Sample

```text
Example record block from satbuffer.str:
  Saturated Buffer Title Line
  Name               HRU_SRC  FRAC_SRC  FLOCON_DTB  HRU_RCV  LYR
  Buffer1            101      1.0       FlowCtrl1   201      0
  Buffer2            102      0.5       FlowCtrl2   202      1
```

## Read Pattern

```fortran
open (107,file="satbuffer.str")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) satbuff_db(ibuff)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="satbuffer.str")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) satbuff_db(ibuff)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:sat_buff_read] | close, open, read, rewind | Reads the saturated buffer parameter file `satbuffer.str` if it exists, counts the number of records, allocates the `satbuff_db` array, reads all saturated buffer records into `satbuff_db`, and then initializes the `hru` array elements' saturated buffer data and flow control decision table indices accordingly. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists, as checked by inquire in the reader.
- The reader crosswalks the flow control decision table name to its index by comparing with `dtbl_flo` names.
- The example record block is a constructed example based on field types and typical usage; no exact example was found in the source.
