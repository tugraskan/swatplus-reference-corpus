---
kind: io
source_symbols:
- res_read
title: '`reservoir.res`'
status: filled
source_hash: 63f555c8599417fe
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_dat_c(:)` (array of `type reservoir_data_char_input`)  
**Read by:** [sym:res_read]

## Bottom Line

The file `reservoir.res` configures reservoir characteristics and initial conditions for the SWAT+ model.

It is required if reservoirs are included in the simulation and is read by the `res_read` subroutine.

The file defines reservoir names, initial conditions, hydrology inputs, release methods, sediment inputs, and nutrient inputs.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_res` variable which contains the filename for the reservoir input file. |
| [sym:input_file_module] | Used for general input file handling and possibly for `in_res` definition. |
| [sym:maximum_data_module] | Supplies maximum counts and database sizes such as `db_mx%res_dat`, `db_mx%res_init`, `db_mx%res_hyd`, `db_mx%ctbl_res`, `db_mx%dtbl_res`, `db_mx%res_sed`, `db_mx%res_nut`, `db_mx%pestw_ini`, and `db_mx%pathw_ini`. |
| [sym:reservoir_data_module] | Defines the derived type `reservoir_data_char_input` and the arrays `res_dat_c` and `res_dat` where the file data is stored. |
| [sym:conditional_module] | Used for conditional compilation or logic, exact variables not specified. |
| [sym:hydrograph_module] | Provides hydrology-related data structures such as `res_hyddb` and `res_hyd` used to link hydrology inputs. |
| [sym:constituent_mass_module] | Likely provides constituent mass data structures referenced during initialization, exact variables not specified. |
| [sym:reservoir_module] | Provides reservoir state variables such as `res_ob` and parameters `res_prm` used for sediment and nutrient parameters. |
| [sym:pesticide_data_module] | Provides pesticide initial conditions arrays like `pest_init_name` and related initialization. |
| [sym:res_salt_module] | Likely used for salt initial conditions, referenced but exact variables not specified. |
| [sym:res_cs_module] | Likely used for constituent or chemical species initial conditions, referenced but exact variables not specified. |
| [sym:reservoir_conditions_module] | Likely used for reservoir condition states, referenced but exact variables not specified. |

## File Variables

The file `reservoir.res` consists of records each describing a reservoir's configuration using character fields mapped into the derived type `reservoir_data_char_input`. Each record includes reservoir name, initial condition references, hydrology input references, release method, sediment input, and nutrient input identifiers.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_dat_c%name` | character (len=25) |  | Reservoir name identifier |
| 3 |  | `res_dat_c%init` | character (len=25) |  | Initial data-points reference to initial.res |
| 4 |  | `res_dat_c%hyd` | character (len=25) |  | Points to hydrology.res for hydrology inputs |
| 5 |  | `res_dat_c%release` | character (len=25) |  | 0=simulated; 1=measured outflow |
| 6 |  | `res_dat_c%sed` | character (len=25) |  | Sediment inputs reference to sediment.res |
| 7 |  | `res_dat_c%nut` | character (len=25) |  | Nutrient inputs reference to nutrient.res |

## Sample

```text
1 reservoir1 init1 hyd1 0 sed1 nut1
2 reservoir2 init2 hyd2 1 sed2 nut2
```

## Read Pattern

```fortran
open (105,file=in_res%res)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
read (105,*,iostat=eof) i
rewind (105)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
read (105,*,iostat=eof) ires
backspace (105)
read (105,*,iostat=eof) k, res_dat_c(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%res)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ires` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) k, res_dat_c(ires)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read] | backspace, close, open, read, rewind | Reads the reservoir.res file to populate reservoir configuration data into the arrays `res_dat_c` and `res_dat`. It initializes reservoir initial conditions, hydrology inputs, release methods, sediment and nutrient parameters by linking character references in the input file to internal data structures and indices. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format is a constructed example based on the field order and types; no explicit example was found in the source.
- Module usage is inferred from the `use` statements and variable references in `res_read` but exact variables from some modules (conditional_module, constituent_mass_module, res_salt_module, res_cs_module, reservoir_conditions_module) are not explicitly identified in the source.
