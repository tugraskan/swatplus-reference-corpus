---
kind: output_family
source_symbols:
- hcsin_output
- header_cs
title: hydin_paths_*
status: filled
source_hash: 1efdbf255015c580
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_cs`](../procedures/header_cs.md)  
**Written by:** [`hcsin_output`](../procedures/hcsin_output.md)  
**Primary data type:** `constituent_mass_module::constituent_mass` (the `%path` array of `obcs(iob)%hcsin_*(iin)`)  
**Files covered:** `hydin_paths_day`, `hydin_paths_mon`, `hydin_paths_yr`, `hydin_paths_aa` text/CSV pairs

## Bottom Line

`hydin_paths_*` reports the pathogen mass carried **into** each spatial object on each of its incoming hydrograph connections. `hcsin_output` walks every spatial object (`iob = 1, sp_ob%objs`) and, for each object, every incoming hydrograph (`iin = 1, ob(iob)%rcv_tot`). It writes one row per object-inflow link: time, the object identity, the descriptors of that inflow link, and then one value per simulated pathogen (an implied-do over `ipath = 1, cs_db%num_paths`).

This is one documentation page, not four. Daily, monthly, yearly, and average-annual files share the same row layout; only the file name, unit number, print condition, and source state object differ: `hcsin_d(iin)` (daily), `hcsin_m(iin)` (monthly), `hcsin_y(iin)` (yearly), `hcsin_a(iin)` (average annual).

> **What each row means:** one incoming hydrograph link feeding one object for one reporting period. The first columns say which object it is and where the inflow comes from (source object type/number, hydrograph type, and the fraction of that source hydrograph delivered on this link); the remaining columns give the mass of each simulated pathogen carried in on that link. If a run simulates N pathogens there are N constituent columns. Pick the file whose frequency matches your timestep — the columns are the same across all four. Whole files only exist when at least one pathogen is simulated (`cs_db%num_paths > 0`).

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | State Written | Write Lines |
|---|---|---|---:|---:|---|---|
| Daily | `hydin_paths_day.txt` | `hydin_paths_day.csv` | 2712 | 2728 | `obcs(iob)%hcsin_d(iin)%path` | `hcsin_output.f90:33, 37` |
| Monthly | `hydin_paths_mon.txt` | `hydin_paths_mon.csv` | 2713 | 2729 | `obcs(iob)%hcsin_m(iin)%path` | `hcsin_output.f90:84, 88` |
| Yearly | `hydin_paths_yr.txt` | `hydin_paths_yr.csv` | 2714 | 2730 | `obcs(iob)%hcsin_y(iin)%path` | `hcsin_output.f90:135, 139` |
| Average annual | `hydin_paths_aa.txt` | `hydin_paths_aa.csv` | 2715 | 2731 | `obcs(iob)%hcsin_a(iin)%path` | `hcsin_output.f90:186, 190` |

## File Contracts

| Frequency | Open Condition | Open Lines | Header Row | Catalog Entry |
|---|---|---|---|---|
| Daily | `pco%hyd%d == "y"` and `cs_db%num_paths > 0` | `header_cs.f90:30` (txt), `:35` (csv) | `csin_hyd_hdr` + one `cs_path_solsor` label group per pathogen (`header_cs.f90:33`) | `HYDIN_PATHS hydin_paths_day.txt/csv` |
| Monthly | `pco%hyd%m == "y"` and `cs_db%num_paths > 0` | `header_cs.f90:86` (txt), `:91` (csv) | same | `HYDIN_PATHS hydin_paths_mon.txt/csv` |
| Yearly | `pco%hyd%y == "y"` and `cs_db%num_paths > 0` | `header_cs.f90:142` (txt), `:147` (csv) | same | `HYDIN_PATHS hydin_paths_yr.txt/csv` |
| Average annual | `pco%hyd%a == "y"` and `cs_db%num_paths > 0` | `header_cs.f90:197` (txt), `:202` (csv) | same | `HYDIN_PATHS hydin_paths_aa.txt/csv` |

## Writer And Print Controls

| Control | Source Line | Applies To | Meaning |
|---|---:|---|---|
| `cs_db%num_paths > 0` | `hcsin_output.f90:32`, `header_cs.f90:29` | All | Nothing is opened or written unless at least one pathogen is simulated. |
| `pco%hyd%d == "y"` | `header_cs.f90:15`, `hcsin_output.f90:20` | Daily | Enables the daily HYDIN constituent files. |
| `pco%day_print == "y"` and `pco%int_day_cur == pco%int_day` | `hcsin_output.f90:19` | Daily | Restricts daily rows to the configured print interval. |
| `pco%hyd%m == "y"` | `header_cs.f90:70`, `hcsin_output.f90:71` | Monthly | Enables monthly HYDIN files. |
| `pco%hyd%y == "y"` | `header_cs.f90:127`, `hcsin_output.f90:122` | Yearly | Enables yearly HYDIN files. |
| `pco%hyd%a == "y"` | `header_cs.f90:182`, `hcsin_output.f90:172` | Average annual | Enables average-annual HYDIN files. |
| `pco%csvout == "y"` | `hcsin_output.f90:36`, `header_cs.f90:34` | CSV companions | Enables the CSV file beside each text file. |
| `time%end_mo == 1` | `hcsin_output.f90:70` | Monthly | Writes monthly rows at month end. |
| `time%end_yr == 1` | `hcsin_output.f90:121` | Yearly | Writes yearly rows at year end. |
| `time%end_sim == 1` | `hcsin_output.f90:172` | Average annual | Writes average-annual rows at simulation end. |

## Shared Record Layout

| Row Part | Columns | Source | Meaning |
|---|---|---|---|
| Title row | Basin name and program string | `header_cs.f90:32` | Identifies the model run. |
| Header row | `csin_hyd_hdr` + per-pathogen labels | `header_cs.f90:33` | Column names; see the note about label/value alignment in Review Notes. |
| Data row | time, object identity, inflow descriptors, per-pathogen mass | `hcsin_output.f90:33` | One incoming hydrograph link for the active frequency. |

```text
title:   bsn%name, prog
header:  csin_hyd_hdr, (cs_path_solsor(ipath), ipath = 1, num_paths)
data:    jday mon day yr iob gis_id type num obtypin obtyp_noin htyp_in frac_in  path(1) ... path(num_paths)
```

## Columns Written

The first twelve columns are fixed. The pathogen columns then repeat once per simulated pathogen (`ipath = 1, cs_db%num_paths`).

| Column | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` |  | `time%day` | Julian day / simulation day of the reporting period. |
| `mon` |  | `time%mo` | Simulation month. |
| `day` |  | `time%day_mo` | Day of month. |
| `yr` |  | `time%yrc` | Calendar year. |
| `iob` |  | `iob` | Spatial object number of the receiving object. |
| `gis_id` |  | `ob(iob)%gis_id` | GIS id of the receiving object. |
| `type` |  | `ob(iob)%typ` | Receiving object type (hru, sd_hru, chan, res, recall, …). |
| `num` |  | `ob(iob)%num` | Spatial object number within its type. |
| `obtypin` |  | `ob(iob)%obtyp_in(iin)` | Inflow (source) object type feeding this incoming hydrograph. |
| `obtyp_noin` |  | `ob(iob)%obtypno_in(iin)` | Inflow object type number (which source object of that type). |
| `htyp_in` |  | `ob(iob)%htyp_in(iin)` | Inflow hydrograph type (tot, rec, surf, …). |
| `frac_in` | frac | `ob(iob)%frac_in(iin)` | Fraction of the source hydrograph delivered on this link. |
| `path(ipath)` | cfu | `obcs(iob)%hcsin_*(iin)%path(ipath)` | Mass of pathogen `ipath` carried in on this incoming hydrograph. One column per simulated pathogen. |

## Frequency-Specific Behavior

| Aspect | Daily | Monthly | Yearly | Average annual |
|---|---|---|---|---|
| State object | `hcsin_d(iin)` | `hcsin_m(iin)` | `hcsin_y(iin)` | `hcsin_a(iin)` |
| Text/CSV units | 2712 / 2728 | 2713 / 2729 | 2714 / 2730 | 2715 / 2731 |
| Trigger | daily print interval | `time%end_mo == 1` | `time%end_yr == 1` | `time%end_sim == 1` |
| Print flag | `pco%hyd%d` | `pco%hyd%m` | `pco%hyd%y` | `pco%hyd%a` |

The columns are identical across all four frequencies; only the accumulation window and the source state object differ.

## Data Sources And Calculations

- Daily values are written directly from `obcs(iob)%hcsin_d(iin)`, the per-timestep incoming constituent hydrograph for that inflow link.
- After the daily block the daily state is accumulated into the monthly state (`hcsin_m(iin) = hcsin_m(iin) + hcsin_d(iin)`, `hcsin_output.f90:67`).
- Monthly is accumulated into yearly (`hcsin_y(iin) = hcsin_y(iin) + hcsin_m(iin)`, `hcsin_output.f90:118`), and yearly into average-annual (`hcsin_a(iin) = hcsin_a(iin) + hcsin_y(iin)`, `hcsin_output.f90:169`).
- These are running sums of pathogen mass; the writer does not divide the constituent columns by the number of days or years, so monthly/yearly/average-annual rows are period totals of the daily inflow.

## Writer Flow

1. Loop over every spatial object `iob = 1, sp_ob%objs`.
2. For each object, loop over every incoming hydrograph `iin = 1, ob(iob)%rcv_tot`.
3. If daily printing is enabled and within the print interval and `cs_db%num_paths > 0`, write the daily row from `hcsin_d(iin)` to unit 2712 (and 2728 for CSV).
4. Accumulate the daily state into the monthly state; at month end write the monthly row from `hcsin_m(iin)`.
5. Accumulate into the yearly state; at year end write the yearly row from `hcsin_y(iin)`.
6. Accumulate into the average-annual state; at simulation end write the average-annual row from `hcsin_a(iin)`.

## Line-Based I/O Trace

| Source Line | Operation | Unit | File | Fields |
|---:|---|---|---|---|
| `hcsin_output.f90:33` | `write` | `2712` | `hydin_paths_day.txt` | time, object identity, inflow descriptors, `hcsin_d(iin)%path(:)` |
| `hcsin_output.f90:37` | `write` | `2728` | `hydin_paths_day.csv` | time, object identity, inflow descriptors, `hcsin_d(iin)%path(:)` |
| `hcsin_output.f90:84` | `write` | `2713` | `hydin_paths_mon.txt` | time, object identity, inflow descriptors, `hcsin_m(iin)%path(:)` |
| `hcsin_output.f90:135` | `write` | `2714` | `hydin_paths_yr.txt` | time, object identity, inflow descriptors, `hcsin_y(iin)%path(:)` |
| `hcsin_output.f90:186` | `write` | `2715` | `hydin_paths_aa.txt` | time, object identity, inflow descriptors, `hcsin_a(iin)%path(:)` |

## Review Notes

- **Header/data column alignment.** The header row (`csin_hyd_hdr`, `constituent_mass_module.f90:550-565`) carries fourteen fixed labels — the twelve data columns plus a trailing `sol_in`/`sor_in` pair — and then a `cs_path_solsor` group (`sol_out`/`sor_out`, two labels) for each pathogen. The data row, however, writes twelve fixed values and a single value per pathogen. Readers aligning columns by position should key off the writer (`hcsin_output.f90:33`), not the fixed header labels.
- The pathogen value unit is `cfu`, from the `%path` comment in `type constituent_mass` (`constituent_mass_module.f90:81`).
- The number of constituent columns is dynamic (`cs_db%num_paths`); the pathogen names appended to the header come from `cs_path_solsor`.
- Rows are emitted per incoming hydrograph link, so an object with several inflows contributes several rows per period.

## Source Links

- Writer: [`hcsin_output`](../procedures/hcsin_output.md) (`hcsin_output.f90:1-222`)
- Header/opener: [`header_cs`](../procedures/header_cs.md) (`header_cs.f90:14-234`)
- Data type: `constituent_mass_module::constituent_mass` (`%path`)

## Evidence Used

- `hcsin_output.f90:1-222`
- `header_cs.f90:14-234`
- `constituent_mass_module.f90:79-90` (`type constituent_mass`), `:159-174` (`all_constituent_hydrograph`, `obcs`), `:550-591` (`csin_hyd_hdr`, `sol_sor`)
- `hydrograph_module.f90:356-361` (`obtyp_in`, `obtypno_in`, `htyp_in`, `frac_in`)
