---
kind: io
source_symbols:
- pest_cha_res_read
title: '`pest_water.ini`'
status: filled
source_hash: c6f85cf30fa75325
version_label: SWAT+ 62.0.0
---

**Primary target:** `pest_water_ini(:)` (array of `type cs_water_init_concentrations`)  
**Read by:** [sym:pest_cha_res_read]

## Bottom Line

`pest_water.ini` is an optional input file that configures the initial concentrations of various constituents (pests) in water and benthic compartments at the start of the simulation. It is read by the `pest_cha_res_read` subroutine, which loads these initial constituent concentrations into the `pest_water_ini` array of `cs_water_init_concentrations` type.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_water_init_concentrations` and the `pest_water_ini` array where the initial constituent concentrations are stored. |
| [sym:input_file_module] | Supplies the `in_init` variable which contains the filename for `pest_water.ini` as `in_init%pest_water`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable whose `pestw_ini` field is set to the number of records read from the file. |
| [sym:channel_data_module] | Used but no specific types or variables from this module are directly referenced in the reader for this file. |
| [sym:hydrograph_module] | Used but no specific types or variables from this module are directly referenced in the reader for this file. |
| [sym:sd_channel_module] | Used but no specific types or variables from this module are directly referenced in the reader for this file. |
| [sym:organic_mineral_mass_module] | Used but no specific types or variables from this module are directly referenced in the reader for this file. |

## File Variables

The file `pest_water.ini` contains initial concentration data for pest constituents in water and benthic compartments. Each record corresponds to one constituent and includes its name and initial concentrations in water, benthic, and reservoir compartments. These records are read into the `pest_water_ini` array of `cs_water_init_concentrations` type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pest_water_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `pest_water_ini%water` | real | ppm,fracitons | amount of constituents (dissolved, salt minerals) in aquifer at start of simulation |
| 4 |  | `pest_water_ini%benthic` | real | ppm or #cfu/m^2 | amount of constituent in benthic at start of simulation |
| 5 |  | `pest_water_ini%reservoir` | real | ppm | amount of constituent in reservoir water at start of simulation |

## Sample

```text
Example record block from `pest_water.ini` (format inferred from reader):
ConstituentName
  <water_concentration_value>  <benthic_concentration_value>
Repeat for each constituent...
```

## Read Pattern

```fortran
open (107,file=in_init%pest_water)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) pest_init_name(ipesti)
read (107,*,iostat=eof) titldum, pest_water_ini(ipesti)%water, pest_water_ini(ipesti)%benthic
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_init%pest_water)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pest_init_name(ipesti)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, pest_water_ini(ipesti)%water, pest_water_ini(ipesti)%benthic` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:pest_cha_res_read] | open, read, rewind, close | Reads the `pest_water.ini` file to load initial pest constituent concentrations into the `pest_water_ini` array. It first counts the number of records, allocates arrays accordingly, then rereads the file to populate the arrays with constituent names and their initial water and benthic concentrations. |

## Review Notes

- The file is optional and only read if it exists or the filename is not 'null'.
- The reader uses `cs_db%num_pests` to allocate arrays for water and benthic concentrations per constituent.
- The reservoir concentration field exists in the type but is not read from the file in the current reader source; this may indicate it is unused or set elsewhere.
- The sample read format is inferred from the reader's read statements but no explicit example data block is present in the source.
