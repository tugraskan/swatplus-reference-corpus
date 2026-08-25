---
kind: io
source_symbols:
- rte_read_nut
title: '`nutrients.rte`'
status: filled
source_hash: 2ef32638ff7eda2c
version_label: SWAT+ 62.0.0
---

**Primary target:** `rte_nut(:)` (array of `type routing_nut_data`)  
**Read by:** [sym:rte_read_nut]

## Bottom Line

The file `nutrients.rte` configures nutrient and sediment reduction parameters for routing through channels or reservoirs in the watershed.

It is an optional input file; if absent, an empty array is allocated for `rte_nut`.

The primary reader for this file is the subroutine `rte_read_nut`.

| Module | Role for this file |
| --- | --- |
| [sym:channel_data_module] | Provides the derived type `routing_nut_data` and the allocatable array `rte_nut` where the file data is stored. |

## File Variables

The file `nutrients.rte` contains tabular data records each corresponding to a routing nutrient data structure (`routing_nut_data`). Each record holds parameters for nutrient and sediment reduction in routing segments, mapped directly into the fields of the `rte_nut` array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rte_nut%name` | character(len=16) |  | Name identifier for the routing segment or channel type. |
| 3 |  | `rte_nut%len_inc` | real | m | Segment length used for nutrient reduction calculations. |
| 4 |  | `rte_nut%no3_slp` | real | (mgN/m2/h)/ppm | Slope of denitrification rate versus inflow nitrate concentration. |
| 5 |  | `rte_nut%no3_int` | real | mgN/m2/h | Intercept of the denitrification rate equation. |
| 6 |  | `rte_nut%no3_slp_ob` | real | (mgN/m2/h)/ppm | Slope of denitrification rate for overbank flow versus inflow nitrate. |
| 7 |  | `rte_nut%no3_int_ob` | real | mgN/m2/h | Intercept of denitrification rate equation for overbank flow. |
| 8 |  | `rte_nut%no3_slp_ub` | real | (mgN/m2/h)/ppm | Slope of denitrification rate for underbank flow versus inflow nitrate. |
| 9 |  | `rte_nut%no3_int_ub` | real | mgN/m2/h | Intercept of denitrification rate equation for underbank flow. |
| 10 |  | `rte_nut%turb_slp` | real | (del ppm/ppm) | Slope of turbidity reduction versus inflow turbidity. |
| 11 |  | `rte_nut%turb_int` | real | ppm | Intercept of turbidity reduction equation. |
| 12 |  | `rte_nut%tss_slp` | real | (del ppm/ppm) | Slope of total suspended solids (TSS) versus inflow turbidity. |
| 13 |  | `rte_nut%tss_int` | real | ppm | Intercept of TSS reduction equation. |
| 14 |  | `rte_nut%tp_slp` | real | (del ppm/ppm) | Slope of total phosphorus (TP) reduction versus turbidity reduction. |
| 15 |  | `rte_nut%tp_int` | real | ppm | Intercept of total phosphorus reduction equation. |
| 16 |  | `rte_nut%srp_slp` | real | (del ppm/ppm) | Slope of soluble reactive phosphorus (SRP) reduction versus total phosphorus reduction. |
| 17 |  | `rte_nut%srp_int` | real | ppm | Intercept of soluble reactive phosphorus reduction equation. |
| 18 |  | `rte_nut%turb_tss_slp` | real | ppm | Slope relating turbidity to total suspended solids, typically between 0.2 and 0.4. |
| 19 |  | `rte_nut%no3_min_conc` | real | ppm | Minimum nitrate concentration allowed in routing calculations. |
| 20 |  | `rte_nut%tp_min_conc` | real | ppm | Minimum total phosphorus concentration allowed. |
| 21 |  | `rte_nut%tss_min_conc` | real | ppm | Minimum total suspended solids concentration allowed. |
| 22 |  | `rte_nut%srp_min_conc` | real | ppm | Minimum soluble reactive phosphorus concentration allowed. |

## Sample

```text
Example record format (fields separated by spaces or commas):
"Drainage_Ditch" 250 0.86 0.17 0.48 1.30 1.50 0.03 -0.0002 0.175 0.457 0.534 0.375 1.312 0.646 0.207 0.35 0.05 0.06 5 0.015
```

## Read Pattern

```fortran
open (105,file="nutrients.rte")
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) rte_nut(ich)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file="nutrients.rte")` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) rte_nut(ich)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:rte_read_nut] | backspace, close, open, read, rewind | Reads the optional input file `nutrients.rte` to populate the array `rte_nut` with nutrient and sediment reduction parameters for routing segments. If the file does not exist, it allocates an empty array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
