---
kind: io
source_symbols:
- sd_channel_read
title: '`channel-lte.cha`'
status: filled
source_hash: 2f80b3930a9da749
version_label: SWAT+ 62.0.0
---

**Primary target:** `sd_dat(:)` (array of `type swatdeg_datafiles`)  
**Read by:** [sym:sd_channel_read]

## Bottom Line

The file `channel-lte.cha` is a legacy channel data input file that configures channel-related initial conditions and parameter mappings for the SWAT+ model.

It is optional and only read if the file exists and is specified in the input configuration (`in_cha%chan_ez`).

The primary reader for this file is the `sd_channel_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `sp_ob` object which contains the number of channel segments (`chandeg`) used to allocate arrays for channel state variables. |
| [sym:input_file_module] | Supplies the `in_cha` object which contains the file path for `channel-lte.cha` in `in_cha%chan_ez`. |
| [sym:maximum_data_module] | Provides the `db_mx` object which holds maximum counts and indices such as `sdc_dat`, `ch_init`, `ch_lte`, `ch_sednut`, `ch_nut`, and others used for allocation and indexing. |
| [sym:channel_data_module] | Defines the `sd_chd`, `sd_chd1`, and `ch_nut` arrays used to map channel hydraulic, sediment, and nutrient input data by name. |
| [sym:channel_velocity_module] | Not directly referenced in the reading logic but used for channel velocity data structures allocated at runtime. |
| [sym:ch_pesticide_module] | Provides `cs_db` which contains pesticide counts (`num_pests`) used for allocating pesticide-related arrays. |
| [sym:ch_salt_module] | Provides salt ion counts (`num_salts`) and related data structures allocated and initialized for salt constituents. |
| [sym:ch_cs_module] | Provides constituent mass data (`num_metals`, `num_salts`, `num_pests`) and related arrays for channel constituents. |
| [sym:sd_channel_module] | Defines the `sd_dat` array of type `swatdeg_datafiles` which stores the parsed records from the file. |
| [sym:hydrograph_module] | Used for hydrograph separation arrays allocated during initialization. |
| [sym:constituent_mass_module] | Provides constituent mass data used for allocation and initialization of channel constituent arrays. |
| [sym:pesticide_data_module] | Provides pesticide initialization names and counts used to map initial pesticide conditions. |
| [sym:pathogen_data_module] | Provides pathogen initialization names and counts used to map initial pathogen conditions. |
| [sym:water_body_module] | Not directly referenced in the reading logic but used for water body related data structures. |

## File Variables

The file `channel-lte.cha` contains records describing channel segments with their associated initial conditions and parameter names for hydraulics, sediment, and nutrients. Each record is read into an element of the `sd_dat` array of type `swatdeg_datafiles`, with fields corresponding to channel segment identifiers and initial condition names.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sd_dat%name` | character(len=16) |  | The name identifier of the channel segment. |
| 3 |  | `sd_dat%initc` | character(len=16) |  | The name of the initial condition set associated with this channel segment. |
| 4 |  | `sd_dat%hydc` | character(len=16) |  | The name of the hydraulic input data set for this channel segment. |
| 5 |  | `sd_dat%sedc` | character(len=16) |  | The name of the sediment input data set for this channel segment. |
| 6 |  | `sd_dat%nutc` | character(len=16) |  | The name of the nutrient input data set for this channel segment. |
| 7 |  | `sd_dat%init` | integer |  | Index referencing the initial condition set in internal data structures. |
| 8 |  | `sd_dat%hyd` | integer |  | Index referencing the hydraulic input data set. |
| 9 |  | `sd_dat%sed` | integer |  | Index referencing the sediment input data set. |
| 10 |  | `sd_dat%nut` | integer |  | Index referencing the nutrient input data set. |
| 11 |  | `sd_dat%sednut` | integer |  | Index referencing combined sediment-nutrient input data set. |

## Sample

```text
1 CHANNEL1 INITSET1 HYDSET1 SEDSET1 NUTSET1
2 CHANNEL2 INITSET2 HYDSET2 SEDSET2 NUTSET2
```

## Read Pattern

```fortran
open (105,file=in_cha%chan_ez)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
read (105,*,iostat=eof) i
rewind (105)
backspace (105)
read (105,*,iostat=eof) k, sd_dat(i)%name, sd_dat(i)%initc, sd_dat(i)%hydc, sd_dat(i)%sedc, sd_dat(i)%nutc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%chan_ez)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) k, sd_dat(i)%name, sd_dat(i)%initc, sd_dat(i)%hydc, sd_dat(i)%sedc, sd_dat(i)%nutc` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:sd_channel_read] | backspace, close, open, read, rewind | Reads the `channel-lte.cha` file to load channel segment data into the `sd_dat` array. It parses channel segment names and their associated initial condition, hydraulic, sediment, and nutrient input set names, then maps these names to internal indices for use in the model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `channel-lte.cha` is legacy and optional; it is only read if the file exists and is specified in the input configuration.
- The mapping of initial condition names to indices involves matching names against arrays like `ch_init`, `ch_init_cs`, and others, which are defined elsewhere.
- No sample record was found in the source; the sample read format is inferred from the read statement and typical naming conventions.
