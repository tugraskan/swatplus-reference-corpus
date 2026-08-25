---
kind: io
source_symbols:
- water_orcv_read
title: '`outside_rcv.wal`'
status: filled
source_hash: 5889e59c2cc9fc67
version_label: SWAT+ 62.0.0
---

**Primary target:** `orcv(:)` (array of `type outside_basin_receive`)  
**Read by:** [sym:water_orcv_read]

## Bottom Line

The file `outside_rcv.wal` configures outside basin receiving objects, specifying their names and associated filenames.

It is optional; if the file does not exist or is named "null", the model allocates an empty array for these objects.

The reader `water_orcv_read` loads this file and populates the `orcv` array of type `outside_basin_receive`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides general input file handling utilities used by `water_orcv_read`. |
| [sym:water_allocation_module] | Defines the `outside_basin_receive` type and the `orcv` array where the file data is stored. |
| [sym:recall_module] | Imported but no direct evidence of usage in `water_orcv_read` for this file. |
| [sym:mgt_operations_module] | Imported but no direct evidence of usage in `water_orcv_read` for this file. |
| [sym:maximum_data_module] | Provides `db_mx%out_rcv` which stores the maximum number of outside basin receiving objects read from the file. |
| [sym:hydrograph_module] | Imported but no direct evidence of usage in `water_orcv_read` for this file. |
| [sym:constituent_mass_module] | Imported but no direct evidence of usage in `water_orcv_read` for this file. |
| [sym:sd_channel_module] | Imported but no direct evidence of usage in `water_orcv_read` for this file. |

## File Variables

The file `outside_rcv.wal` contains a header block followed by a list of outside basin receiving objects. Each object record includes an index, a name, and a filename, which are read into the `orcv` array of type `outside_basin_receive`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `orcv%name` | character (len=25) |  | name of outside basin receiving object |
| 3 |  | `orcv%filename` | character (len=25) |  | name of outside basin receiving object |

## Sample

```text
Example snippet from `outside_rcv.wal`:
Title of file line
3
Header line
1 OutsideBasin1 File1.wal
2 OutsideBasin2 File2.wal
3 OutsideBasin3 File3.wal
```

## Read Pattern

```fortran
open (107,file='outside_rcv.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, orcv(ircv)%name, orcv(ircv)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='outside_rcv.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, orcv(ircv)%name, orcv(ircv)%filename` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_orcv_read] | close, open, read | Reads the `outside_rcv.wal` file to load outside basin receiving objects into the `orcv` array. It first checks if the file exists; if not, it allocates an empty array. If the file exists, it reads a title line, the number of objects, a header line, and then reads each object's index, name, and filename, storing them in `orcv`. |

## Review Notes

- The file `outside_rcv.wal` is optional; if missing or named "null", the model initializes an empty outside basin receiving object array.
- The `water_orcv_read` subroutine reads this file and populates the `orcv` array of type `outside_basin_receive`.
- Several imported modules are not directly referenced in this reader but may be used elsewhere in the model.
- Sample record format is inferred from the read pattern and typical file structure; no exact sample from source is available.
