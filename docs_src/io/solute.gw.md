---
kind: io
source_symbols:
- gwflow_read
title: '`solute.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module.gw_solute(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file solute.gw configures groundwater solute transport parameters for the SWAT+ groundwater flow model.

It is optional and read by the gwflow_read procedure.

It sets parameters such as the number of solute transport species, longitudinal dispersion, sorption, reaction rates, and canal output concentrations for each solute.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the derived type gw_solute and the array gw_solute(:) where solute.gw data are stored. |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:maximum_data_module] |  |
| [sym:hru_module] |  |
| [sym:reservoir_data_module] |  |
| [sym:cs_data_module] |  |
| [sym:constituent_mass_module] |  |
| [sym:water_allocation_module] |  |
| [sym:utils] |  |

## File Variables

The solute.gw file contains groundwater solute transport configuration parameters. The file is read sequentially by gwflow_read and mapped into the gw_solute derived type array in gwflow_module.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Header line 1` | `header` |  |  | First header line read from solute.gw, typically a descriptive or metadata line. |
| 1 | `Header line 2` | `header` |  |  | Second header line read from solute.gw, often column headers or additional metadata. |
| 1 | `Number of solute transport species` | `num_ts_transport` |  |  | Number of solute transport species to be modeled in groundwater flow. |
| 1 | `Groundwater longitudinal dispersion` | `gw_long_disp` |  |  | Longitudinal dispersion coefficient for groundwater solute transport. |
| 1 | `Solute parameters per species` | `name, gwsol_sorb(s), gwsol_rctn(s), canal_out_conc(s)` |  |  | For each solute species s, reads the name, sorption coefficient, reaction rate, and canal output concentration. |

## Sample

```text
Example solute.gw file snippet:
Groundwater solute transport parameters
Name Sorption Reaction CanalConc
3
0.1
Nitrate 0.05 0.001 0.0
Phosphate 0.10 0.002 0.0
Chloride 0.00 0.000 0.0
```

## Read Pattern

```fortran
open(in_gw,file='solute.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,*) num_ts_transport
read(in_gw,*) gw_long_disp
read(in_gw,*) header
read(in_gw,*) name,gwsol_sorb(s),gwsol_rctn(s),canal_out_conc(s)
close(in_gw)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='solute.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) num_ts_transport` |
| Input | `read` | in_gw | `read(in_gw,*) gw_long_disp` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) name,gwsol_sorb(s),gwsol_rctn(s),canal_out_conc(s)` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read | Reads the solute.gw file to configure groundwater solute transport parameters including solute species count, longitudinal dispersion, and per-species sorption, reaction, and canal output concentrations. Stores data in gw_solute array in gwflow_module. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file solute.gw is optional and configures groundwater solute transport parameters used by gwflow_read.
- The primary target is the gw_solute array in gwflow_module, which holds solute species properties.
- No explicit units are given in the source for sorption, reaction, or canal concentration; users should consult model documentation for units.
