---
kind: io
source_symbols:
- ru_read_elements
title: '`rout_unit.ele`'
status: filled
source_hash: 554980807d98967a
version_label: SWAT+ 62.0.0
---

**Primary target:** `ru_elem(:)` (array of `type routing_unit_elements`)  
**Read by:** [sym:ru_read_elements]

## Bottom Line

`rout_unit.ele` lists the spatial elements that make up each routing unit: each record names the element, its object type and number, its area fraction, and the delivery ratio applied to it.

The reader `ru_read_elements` reads a title and header line, sizes `ru_elem` from the maximum element id, then reads each element into `ru_elem(i)` and crosswalks `dr_name` against the delivery-ratio database from `delratio.del`.

The reader processes the file when `in_ru%ru_ele` exists (and is not `"null"`).

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Defines `ru_elem` and `type routing_unit_elements`; each record is read into `ru_elem(i)`. |
| [sym:input_file_module] | Supplies `in_ru`; `in_ru%ru_ele` holds the `rout_unit.ele` filename opened on unit 107. |
| [sym:maximum_data_module] | Supplies `db_mx`; the reader stores the element count in `db_mx%ru_elem`. |
| [sym:dr_module] | Supplies `dr_db`/`dr`; each element's `dr_name` is crosswalked to a delivery-ratio record. |

## File Variables

`rout_unit.ele` has a title line and a column-header line followed by one record per routing-unit element. Each record gives the element id, name, object type and number, area fraction, and the delivery-ratio name to apply. The reader stores these in `ru_elem` and resolves `dr_name` against the delivery-ratio database read from `delratio.del`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `id` | `i` | integer |  | routing-unit element id; index into `ru_elem` |
| 2 | `name` | `ru_elem%name` | character(len=16) |  | element name |
| 3 | `obtyp` | `ru_elem%obtyp` | character(len=3) |  | object type (1=hru, 2=hru_lte, 11=export coef, ...) |
| 4 | `obtypno` | `ru_elem%obtypno` | integer |  | object number for the given object type |
| 5 | `frac` | `ru_elem%frac` | real |  | fraction of the element in the routing unit (expansion factor) |
| 6 | `dr_name` | `ru_elem%dr_name` | character(len=16) |  | delivery-ratio name; crosswalks to `dr_db(...)%name` in delratio.del |

## Sample

```text
Schematic of the record layout (field names in read order, not a specific dataset):

<title line>
id  name       obtyp  obtypno  frac    dr_name
1   elem_1     1      5        1.000   null
2   elem_2     1      6        0.500   dr_om1
```

## Read Pattern

```fortran
open (107,file=in_ru%ru_ele)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, ru_elem(i)%name, ru_elem(i)%obtyp, ru_elem(i)%obtypno, ru_elem(i)%frac, ru_elem(i)%dr_name
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ru%ru_ele)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ru_elem(i)%name, ru_elem(i)%obtyp, ru_elem(i)%obtypno, ru_elem(i)%frac, ru_elem(i)%dr_name` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ru_read_elements] | backspace, open, read | Opens `rout_unit.ele` on unit 107, reads the title and header, sizes `ru_elem` from the maximum element id, then reads each element record into `ru_elem(i)` and crosswalks its `dr_name` with the delivery-ratio database. |

## Review Notes

- Each record is read twice: a first read gets the element id `i`; the reader backspaces and re-reads the full line into `ru_elem(i)` (ru_read_elements.f90:68-72).
- The array is sized by the maximum element id, so ids may be sparse.
- `dr_name` crosswalks to `dr_db(...)%name` from `delratio.del`; `null` applies no delivery ratio.
- Object-type codes follow `obtyp` (1=hru, 2=hru_lte, 11=export coefficient, ...).
