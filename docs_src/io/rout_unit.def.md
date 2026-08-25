---
kind: io
source_symbols:
- ru_read_elements
title: '`rout_unit.def`'
status: filled
source_hash: 554980807d98967a
version_label: SWAT+ 62.0.0
---

**Primary target:** `ru_def(:)` (array of `type routing_unit_data`)  
**Read by:** [sym:ru_read_elements]

## Bottom Line

The file `rout_unit.def` defines routing units (RUs) in the model, specifying their names and the elements (subbasin elements) they contain.

It is an optional input file, checked for existence before reading.

The reader `ru_read_elements` loads this file and stores its data into the `ru_def` array of `type routing_unit_data`.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the derived type `routing_unit_data` and the arrays `ru_def`, `ru_elem`, and related counters used to store routing unit and element data. |
| [sym:input_file_module] | Supplies the `in_ru` input file paths, including `in_ru%ru_def` for the routing unit definition file. |
| [sym:maximum_data_module] | Provides maximum counts such as `db_mx%ru_elem` and `db_mx%dr_om` used for array sizing and loops. |
| [sym:dr_module] | Provides the delivery ratio database `dr_db` and related arrays used to crosswalk delivery ratio names to delivery ratio objects. |

## File Variables

The file consists of records defining routing units, each with a name, total number of elements, and a list of element indices pointing to subbasin elements. The Fortran reader maps each record into an element of the `ru_def` array of `type routing_unit_data`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ru_def%name` | character(len=16) |  | Name identifier of the routing unit. |
| 3 |  | `ru_def%num_tot` | integer |  | Total number of subbasin elements contained in this routing unit. |
| 4 |  | `ru_def%num` | integer |  | Array of indices pointing to subbasin elements (sub_elem) that compose the routing unit. |

## Sample

```text
1  RU001  3  10 20 30
2  RU002  2  15 25
```

## Read Pattern

```fortran
open (107,file=in_ru%ru_def)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) numb, namedum, nspu
backspace (107)
read (107,*,iostat=eof) numb, ru_def(iru)%name, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ru%ru_def)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) numb, namedum, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) numb, ru_def(iru)%name, nspu, (elem_cnt(isp), isp = 1, nspu)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ru_read_elements] | backspace, close, open, read, rewind | Reads the routing unit definition file `rout_unit.def` if it exists, parses routing unit records, and stores them into the `ru_def` array of `type routing_unit_data`. It reads the routing unit name, total number of elements, and the list of element indices for each routing unit. |

## Review Notes

- The file `rout_unit.def` is optional and only read if it exists or is not set to "null".
- The reader `ru_read_elements` also reads other files such as `ru_ele` but this overlay focuses on `rout_unit.def`.
- The sample read format is inferred from the read statements and variable usage; no explicit example block was found in the source.
- The `num` field in `ru_def` points to subbasin elements, as confirmed by the source line hydrograph_module.f90:477 and usage in ru_read_elements.
