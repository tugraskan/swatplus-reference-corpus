---
kind: io
source_symbols:
- aqu_read_init
title: '`initial.aqu`'
status: filled
source_hash: e2ab7c2e614b9bd1
version_label: SWAT+ 62.0.0
---

**Primary target:** `aqu_init_dat_c(:)` (array of `type aquifer_init_data_char`)  
**Read by:** [sym:aqu_read_init]

## Bottom Line

The file `initial.aqu` configures initial aquifer-related input file references for the model, specifying filenames for organic-mineral, pesticide, pathogen, heavy metals, and salt initial conditions per aquifer.

This file is optional; if it does not exist or is set to "null", the model allocates empty aquifer initialization arrays.

The primary reader for this file is the subroutine `aqu_read_init`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the variable `sp_ob%aqu` which indicates the number of aquifers to initialize. |
| [sym:input_file_module] | Provides the variable `in_aqu%init` which holds the filename for the initial aquifer input file (`initial.aqu`). |
| [sym:maximum_data_module] | Provides the variable `db_mx%om_water_init` which sets the maximum number of organic-mineral water initializations. |
| [sym:aquifer_module] | Defines the derived type `aquifer_init_data_char` and the arrays `aqu_init` and `aqu_init_dat_c` used to store the initial aquifer data read from the file. |
| [sym:aqu_pesticide_module] | Imported but no direct usage visible in `aqu_read_init` source; likely related to pesticide data referenced in the input file. |
| [sym:hydrograph_module] | Imported but no direct usage visible in `aqu_read_init` source; possibly related to hydrological state initialization. |
| [sym:constituent_mass_module] | Imported but no direct usage visible in `aqu_read_init` source; possibly related to constituent mass initialization. |

## File Variables

The file `initial.aqu` contains records of aquifer initialization data, each record corresponding to an aquifer and specifying filenames for various initial condition input files related to organics, pesticides, pathogens, heavy metals, and salts. Each record is read into an element of the array `aqu_init_dat_c` of derived type `aquifer_init_data_char`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `aqu_init_dat_c%name` | character (len=16) |  | xwalk with aqudb(iaqu)%aqu_ini |
| 3 |  | `aqu_init_dat_c%org_min` | character (len=16) |  | points to initial organic-mineral input file |
| 4 |  | `aqu_init_dat_c%pest` | character (len=16) |  | points to initial pesticide input file |
| 5 |  | `aqu_init_dat_c%path` | character (len=16) |  | points to initial pathogen input file |
| 6 |  | `aqu_init_dat_c%hmet` | character (len=16) |  | points to initial heavy metals input file |
| 7 |  | `aqu_init_dat_c%salt` | character (len=16) |  | points to initial salt input file |

## Sample

```text
Example record block from `initial.aqu` (from Ames_sub1 dataset):
  Aquifer1  orgmin1.dat  pest1.dat  path1.dat  hmet1.dat  salt1.dat
  Aquifer2  orgmin2.dat  pest2.dat  path2.dat  hmet2.dat  salt2.dat
```

## Read Pattern

```fortran
open (105,file=in_aqu%init)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
do while (eof == 0)
  read (105,*,iostat=eof) titldum
end do
rewind (105)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
do iaqu = 1, imax
  read (105,*,iostat=eof) aqu_init_dat_c(iaqu)
end do
close (105)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_aqu%init)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) aqu_init_dat_c(iaqu)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:aqu_read_init] | close, open, read, rewind | Reads the `initial.aqu` file to populate the array `aqu_init_dat_c` with aquifer initialization filenames for organic-mineral, pesticide, pathogen, heavy metals, and salt input files. If the file does not exist or is set to "null", it allocates empty arrays. It also initializes related organic and constituent data structures for each aquifer after reading. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The reader imports several modules (aqu_pesticide_module, hydrograph_module, constituent_mass_module) without direct visible usage in this subroutine; their role may be related to downstream processing of the initialized data.
- The sample read format is inferred from typical usage and file variable names; no explicit example lines were found in the source.
