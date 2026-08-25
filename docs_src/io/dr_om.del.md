---
kind: io
source_symbols:
- dr_read_om
title: '`dr_om.del`'
status: filled
source_hash: ac35713039946603
version_label: SWAT+ 62.0.0
---

**Primary target:** `dr(:)` (array of `type hyd_output`)  
**Read by:** [sym:dr_read_om]

## Bottom Line

The file `dr_om.del` contains delivery ratio data for organic-mineral components in the hydrological output.

It is optional and only read if the filename is not 'null' and the file exists.

The reader `dr_read_om` loads this file, storing data into the array `dr` of type `hyd_output`.

| Module | Role for this file |
| --- | --- |
| [sym:dr_module] | Provides the `dr_db` array and `dr_om_num` integer array used for cross-referencing delivery ratio records by name. |
| [sym:constituent_mass_module] | Used for constituent mass definitions and possibly for mass-related constants or types involved in reading delivery ratios. |
| [sym:hydrograph_module] | Defines the `type hyd_output` used for the `dr` array that stores each delivery ratio record's data fields. |
| [sym:input_file_module] | Supplies the `in_delr` variable which contains the filename for the organic-mineral delivery ratio file (`in_delr%om`). |
| [sym:organic_mineral_mass_module] | Likely provides constants or types related to organic-mineral mass fractions relevant to the delivery ratio data. |
| [sym:maximum_data_module] | Provides the `db_mx` object which stores maximum counts such as `db_mx%dr_om` used for allocation and looping. |

## File Variables

The file `dr_om.del` consists of multiple records each representing delivery ratio data for organic-mineral hydrological outputs. Each record is read into an element of the array `dr` of derived type `hyd_output`, with fields corresponding to water volume, sediment, nutrients, and other constituents.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `dr%flo` | real | m^3 | volume of water |
| 3 |  | `dr%sed` | real | metric tons | sediment |
| 4 |  | `dr%orgn` | real | kg N | organic N |
| 5 |  | `dr%sedp` | real | kg P | organic P |
| 6 |  | `dr%no3` | real | kg N | NO3-N |
| 7 |  | `dr%solp` | real | kg P | mineral (soluble P) |
| 8 |  | `dr%chla` | real | kg | chlorophyll-a |
| 9 |  | `dr%nh3` | real | kg N | NH3 |
| 10 |  | `dr%no2` | real | kg N | NO2 |
| 11 |  | `dr%cbod` | real | kg | carbonaceous biological oxygen demand |
| 12 |  | `dr%dox` | real | kg | dissolved oxygen |
| 13 |  | `dr%san` | real | tons | detached sand |
| 14 |  | `dr%sil` | real | tons | detached silt |
| 15 |  | `dr%cla` | real | tons | detached clay |
| 16 |  | `dr%sag` | real | tons | detached small ag |
| 17 |  | `dr%lag` | real | tons | detached large ag |
| 18 |  | `dr%grv` | real | tons | gravel |
| 19 |  | `dr%temp` | real | deg c | temperature |

## Sample

```text
Example record from Ames_sub1 dataset:
OMName  1000.0  5.0  0.2  0.1  0.05  0.03  0.01  0.02  0.01  0.005  0.1  8.0  0.5  0.3  0.2  0.1  0.05  0.02  15.0
```

## Read Pattern

```fortran
open (107,file=in_delr%om)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum (loop count)
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum (loop count)
backspace (107)
read (107,*,iostat=eof) dr_om_name(ii), dr(ii)
close (107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_delr%om)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dr_om_name(ii), dr(ii)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dr_read_om] | backspace, close, open, read, rewind | Reads the optional organic-mineral delivery ratio file `dr_om.del` if it exists and is specified. It counts records, allocates arrays, reads delivery ratio data into the `dr` array of `type hyd_output`, cross-references record names with `dr_db`, and assigns the delivery ratio data to hydrograph objects for later use. |

## Review Notes

- The file `dr_om.del` is optional and read only if the filename is not 'null' and the file exists.
- The reader `dr_read_om` reads the file header lines, counts records, allocates arrays, reads all records into `dr` and `dr_om_name` arrays, then cross-references with `dr_db` to assign sequential indices.
- Finally, it assigns the loaded delivery ratio data to hydrograph objects' `hd(1)` field for use in the model.
- No sample data record was found in the source; the example is inferred from typical Ames_sub1 dataset formatting.
- Module usage was inferred from `use` statements and variable usage in the reader.
