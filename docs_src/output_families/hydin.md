---
kind: output_family
source_symbols:
- header_hyd
- hydin_output
title: hydin_*
status: filled
source_hash: 285145b3c85976b3
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_hyd`](../procedures/header_hyd.md)  
**Written by:** [`hydin_output`](../procedures/hydin_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `hydin_day`, `hydin_mon`, `hydin_yr`, `hydin_aa` text/CSV pairs

## Bottom Line

`hydin_*` is the `hydin` time-series output family: the incoming hydrographs of each spatial object. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. `hydin_output` writes **one row per (object x incoming hydrograph)**: the row is time and object identity, a few incoming-connection descriptors, then a `hyd_output` hydrograph record (flow, sediment, nutrients, and constituents).

Only the file name, unit number, print condition, and source state differ between frequencies; the columns are identical.

> **What each row means:** one incoming hydrograph feeding (or leaving) one object for one reporting period (daily, monthly, yearly, average annual). An object with several incoming connections appears once per connection. The `hyd_output` columns are the transported flow, sediment, and nutrient loads.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hydin_day.txt` | `hydin_day.csv` | 2560 | 2564 | `header_hyd.f90:82` |
| Monthly | `hydin_mon.txt` | `hydin_mon.csv` | 2561 | 2565 | `header_hyd.f90:97` |
| Yearly | `hydin_yr.txt` | `hydin_yr.csv` | 2562 | 2566 | `header_hyd.f90:112` |
| Average annual | `hydin_aa.txt` | `hydin_aa.csv` | 2563 | 2567 | `header_hyd.f90:127` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%hyd%d == "y") then` | `header_hyd.f90:82` |
| Monthly | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then` | `header_hyd.f90:97` |
| Yearly | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then  →  if (pco%hyd%y == "` | `header_hyd.f90:112` |
| Average annual | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then  →  if (pco%hyd%y == "` | `header_hyd.f90:127` |

The header and units rows for every file are written by `header_hyd`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%hyd%a == "y"` | aa | Enables output for this frequency. |
| `pco%hyd%d == "y"` | All files | Enables output for this frequency. |
| `pco%hyd%m == "y"` | aa, mon, yr | Enables output for this frequency. |
| `pco%hyd%y == "y"` | aa, yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_hyd` | Basin name and program string. |
| Header row | `header_hyd` | Column names for time, identity, connection descriptors, and `hyd_output` values. |
| Units row | `header_hyd` | Units for the value columns. |
| Data row | `hydin_output` | One incoming hydrograph (`hyd_output`) for one object. |

## Columns Written

| Column | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` | | `time%day` | Julian day / simulation day. |
| `mon` | | `time%mo` | Simulation month. |
| `day` | | `time%day_mo` | Day of month. |
| `yr` | | `time%yrc` | Simulation year. |
| `name` | | `ob(icmd)%name` | Object name. |
| `typ` | | `ob(icmd)%typ` | Object type. |
| `obtyp_in` |  | `ob(icmd)%obtyp_in(i)` | inflow object type (ie 1=hru, 2=sd_hru, 3=sub, 4=chan, etc) |
| `obtypno_in` |  | `ob(icmd)%obtypno_in(i)` | inflow object type number |
| `htyp_in` |  | `ob(icmd)%htyp_in(i)` | inflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc) |
| `frac_in` |  | `ob(icmd)%frac_in(i)` | incoming hydrograph descriptor |
| `flo` | m^3 | `ob(icmd)%hin_d(i)%flo` | volume of water |
| `sed` | metric tons | `ob(icmd)%hin_d(i)%sed` | sediment |
| `orgn` | kg N | `ob(icmd)%hin_d(i)%orgn` | organic N |
| `sedp` | kg P | `ob(icmd)%hin_d(i)%sedp` | organic P |
| `no3` | kg N | `ob(icmd)%hin_d(i)%no3` | NO3-N |
| `solp` | kg P | `ob(icmd)%hin_d(i)%solp` | mineral (soluble P) |
| `chla` | kg | `ob(icmd)%hin_d(i)%chla` | chlorophyll-a |
| `nh3` | kg N | `ob(icmd)%hin_d(i)%nh3` | NH3 |
| `no2` | kg N | `ob(icmd)%hin_d(i)%no2` | NO2 |
| `cbod` | kg | `ob(icmd)%hin_d(i)%cbod` | carbonaceous biological oxygen demand |
| `dox` | kg | `ob(icmd)%hin_d(i)%dox` | dissolved oxygen |
| `san` | tons | `ob(icmd)%hin_d(i)%san` | detached sand |
| `sil` | tons | `ob(icmd)%hin_d(i)%sil` | detached silt |
| `cla` | tons | `ob(icmd)%hin_d(i)%cla` | detached clay |
| `sag` | tons | `ob(icmd)%hin_d(i)%sag` | detached small ag |
| `lag` | tons | `ob(icmd)%hin_d(i)%lag` | detached large ag |
| `grv` | tons | `ob(icmd)%hin_d(i)%grv` | gravel |
| `temp` | deg c | `ob(icmd)%hin_d(i)%temp` | temperature |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual); only the file name, unit number, print flag, and source state differ. See the Output Family and Writer And Print Controls tables for per-frequency detail.

## Data Sources And Calculations

Each value is the matching field of the `hyd_output` hydrograph record for one incoming connection (`ob(icmd)%hin_d(i)`). Daily rows are per-timestep; coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each object, loop over its incoming hydrograph connections.
2. If the frequency's print flag is on, write the connection descriptors and the `hyd_output` record to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hydin_output.f90:20` | `2560` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:25` | `2564` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:38` | `2561` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:41` | `2565` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:53` | `2562` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:56` | `2566` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:67` | `2563` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |
| `hydin_output.f90:70` | `2567` | time, identity, incoming-hydrograph descriptors, one `hyd_output` record |

Header and file-open statements are in `header_hyd`.

## Review Notes

- Rows repeat per incoming hydrograph connection: an object with N incoming connections produces N rows per period.
- The `hyd_output` value columns and their meanings come from the type definition in `hydrograph_module`.
- Auto-derived from source; prose sections may benefit from human review.

## Source Links

- Writer: [`hydin_output`](../procedures/hydin_output.md)
- Header / opener: [`header_hyd`](../procedures/header_hyd.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `hydin_output.f90`
- `header_hyd.f90`
- `hydrograph_module.f90` (`type hyd_output`)
