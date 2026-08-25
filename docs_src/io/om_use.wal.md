---
kind: io
source_symbols:
- om_use_read
title: '`om_use.wal`'
status: filled
source_hash: baaca50f26a2d6e2
version_label: SWAT+ 62.0.0
---

**Primary target:** `wuse_om_efflu(:)` (array of `type hyd_output`)  
**Read by:** [sym:om_use_read]

## Bottom Line

The file `om_use.wal` contains water allocation input data for the SWAT+ model, specifying water and constituent volumes for operational management units.

It is optional; if the file does not exist or is set to "null", the model allocates zero-length arrays for these data.

The reader subroutine `om_use_read` loads this file, reading water allocation names and associated hydrological output data into the arrays `om_use_name` and `wuse_om_efflu`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the array `om_use_name` which stores the names of water allocation units read from the file. |
| [sym:water_allocation_module] | not directly referenced for variables in this reader; no specific variables identified as used from this module in the reader. |
| [sym:mgt_operations_module] | no specific types or variables from this module are used in the reader. |
| [sym:maximum_data_module] | provides the variable `db_mx%om_use` which stores the maximum number of water allocation units read from the file. |
| [sym:hydrograph_module] | provides the derived type `hyd_output` and the array `wuse_om_efflu` of this type, which stores the hydrological output data read from the file. |
| [sym:constituent_mass_module] | no specific types or variables from this module are used in the reader. |

## File Variables

The file `om_use.wal` contains a header section followed by multiple records, each representing a water allocation unit with a name and associated hydrological output data. Each record is read into the array `wuse_om_efflu` of derived type `hyd_output`, with corresponding names stored in `om_use_name`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wuse_om_efflu%flo` | real | m^3 | volume of water |
| 3 |  | `wuse_om_efflu%sed` | real | metric tons | sediment |
| 4 |  | `wuse_om_efflu%orgn` | real | kg N | organic N |
| 5 |  | `wuse_om_efflu%sedp` | real | kg P | organic P |
| 6 |  | `wuse_om_efflu%no3` | real | kg N | NO3-N |
| 7 |  | `wuse_om_efflu%solp` | real | kg P | mineral (soluble P) |
| 8 |  | `wuse_om_efflu%chla` | real | kg | chlorophyll-a |
| 9 |  | `wuse_om_efflu%nh3` | real | kg N | NH3 |
| 10 |  | `wuse_om_efflu%no2` | real | kg N | NO2 |
| 11 |  | `wuse_om_efflu%cbod` | real | kg | carbonaceous biological oxygen demand |
| 12 |  | `wuse_om_efflu%dox` | real | kg | dissolved oxygen |
| 13 |  | `wuse_om_efflu%san` | real | tons | detached sand |
| 14 |  | `wuse_om_efflu%sil` | real | tons | detached silt |
| 15 |  | `wuse_om_efflu%cla` | real | tons | detached clay |
| 16 |  | `wuse_om_efflu%sag` | real | tons | detached small ag |
| 17 |  | `wuse_om_efflu%lag` | real | tons | detached large ag |
| 18 |  | `wuse_om_efflu%grv` | real | tons | gravel |
| 19 |  | `wuse_om_efflu%temp` | real | deg c | temperature |

## Sample

```text
Example record format from `om_use.wal` (not from source, illustrative):
Water Allocation Name (string), flo (real), sed (real), orgn (real), sedp (real), no3 (real), solp (real), chla (real), nh3 (real), no2 (real), cbod (real), dox (real), san (real), sil (real), cla (real), sag (real), lag (real), grv (real), temp (real)
```

## Read Pattern

```fortran
open (107,file='om_use.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) om_use_name(iom_use), wuse_om_efflu(iom_use)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='om_use.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) om_use_name(iom_use), wuse_om_efflu(iom_use)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:om_use_read] | close, open, read | Reads the water allocation file `om_use.wal` if it exists, loading water allocation unit names into `om_use_name` and their associated hydrological output data into the array `wuse_om_efflu` of type `hyd_output`. If the file is missing or set to "null", it allocates zero-length arrays for these variables. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and allocation of zero-length arrays if missing.
- No sample data records were found in the source; the sample format is illustrative based on the read statement and type definition.
