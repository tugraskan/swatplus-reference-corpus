---
kind: output_family
source_symbols:
- aquifer_output
- header_aquifer
title: aquifer_*
status: filled
source_hash: 06e07d6a24c93540
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_aquifer`](../procedures/header_aquifer.md)  
**Written by:** [`aquifer_output`](../procedures/aquifer_output.md)  
**Primary data type:** `aquifer_module::aquifer_dynamic`  
**Files covered:** `aquifer_day`, `aquifer_mon`, `aquifer_yr`, `aquifer_aa` text/CSV pairs

## Bottom Line

`aquifer_*` is the aquifer water- and nutrient-balance time-series output family. It uses one shared record layout for daily, monthly, yearly, and average-annual reporting. Each row represents one aquifer object for one reporting period: it starts with time and aquifer-identity fields, then expands an `aquifer_dynamic` state object holding the flow, storage, recharge/seepage/revap, and nitrogen/phosphorus/carbon balance for that period.

This is one documentation page, not four nearly identical pages. The frequency-specific part is only the file name, unit number, print condition, and source state object: `aqu_d(iaq)`, `aqu_m(iaq)`, `aqu_y(iaq)`, or `aqu_a(iaq)`.

> **What each row means:** one aquifer object's water and nitrogen budget for one reporting period — how much water flowed laterally to streams, recharged in, seeped out the bottom, and left as plant uptake/evaporation (revap), together with the nitrate, mineral/organic phosphorus, and carbon it stored and passed downstream. Pick the file whose frequency (day/month/year/average-annual) matches the timestep you want; the columns are identical across all four.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | State Written | Write Lines |
|---|---|---|---:|---:|---|---|
| Daily | `aquifer_day.txt` | `aquifer_day.csv` | 2520 | 2524 | `aqu_d(iaq)` | `aquifer_output.f90:22-24` |
| Monthly | `aquifer_mon.txt` | `aquifer_mon.csv` | 2521 | 2525 | `aqu_m(iaq)` | `aquifer_output.f90:37-39` |
| Yearly | `aquifer_yr.txt` | `aquifer_yr.csv` | 2522 | 2526 | `aqu_y(iaq)` | `aquifer_output.f90:52-54` |
| Average annual | `aquifer_aa.txt` | `aquifer_aa.csv` | 2523 | 2527 | `aqu_a(iaq)` | `aquifer_output.f90:64-66` |

## File Contracts

| Frequency | Open Condition | Open Lines | Header / Units | Catalog Entry |
|---|---|---|---|---|
| Daily | `pco%aqu%d == "y"` (within the daily print interval) | `header_aquifer.f90:13-24` | `aqu_hdr`, `aqu_hdr_units` | `AQUIFER aquifer_day.txt/csv` |
| Monthly | `time%end_mo == 1` and `pco%aqu%m == "y"` | `header_aquifer.f90:30-40` | `aqu_hdr`, `aqu_hdr_units` | `AQUIFER aquifer_mon.txt/csv` |
| Yearly | `time%end_yr == 1` and `pco%aqu%y == "y"` | `header_aquifer.f90:47-57` | `aqu_hdr`, `aqu_hdr_units` | `AQUIFER aquifer_yr.txt/csv` |
| Average annual | `time%end_sim == 1` and `pco%aqu%a == "y"` | `header_aquifer.f90:64-74` | `aqu_hdr`, `aqu_hdr_units` | `AQUIFER aquifer_aa.txt/csv` |

## Writer And Print Controls

| Control | Source Line | Applies To | Meaning |
|---|---:|---|---|
| `pco%aqu%d == "y"` | `header_aquifer.f90:13`, `aquifer_output.f90:20` | Daily | Enables daily aquifer output. |
| `pco%aqu%m == "y"` | `header_aquifer.f90:30`, `aquifer_output.f90:36` | Monthly | Enables monthly aquifer output. |
| `pco%aqu%y == "y"` | `header_aquifer.f90:47`, `aquifer_output.f90:50` | Yearly | Enables yearly aquifer output. |
| `pco%aqu%a == "y"` | `header_aquifer.f90:64`, `aquifer_output.f90:62` | Average annual | Enables average-annual aquifer output. |
| `pco%csvout == "y"` | `header_aquifer.f90:19`, `aquifer_output.f90:23` | CSV companions | Enables the CSV file beside each fixed-width text file. |
| `pco%day_print == "y"` and `pco%int_day_cur == pco%int_day` | `aquifer_output.f90:20` | Daily | Restricts daily rows to the configured print interval. |
| `time%end_mo == 1` | `aquifer_output.f90:30` | Monthly | Builds and writes monthly rows at month end. |
| `time%end_yr == 1` | `aquifer_output.f90:47` | Yearly | Builds and writes yearly rows at year end. |
| `time%end_sim == 1` | `aquifer_output.f90:62` | Average annual | Builds and writes average-annual rows at simulation end. |

## Shared Record Layout

| Row Part | Columns | Source | Meaning |
|---|---|---|---|
| Title row | Basin name and program string | `header_aquifer.f90:14, 31, 48, 65` | Identifies the model run. |
| Header row | `aqu_hdr` | `header_aquifer.f90:15, 32, 49, 66` | Column names for the time, aquifer-identity, and aquifer-balance values. |
| Units row | `aqu_hdr_units` | `header_aquifer.f90:16, 33, 50, 67` | Units for the aquifer-balance columns. |
| Data row | `time`, `iaq`, `ob(iob)`, aquifer state | `aquifer_output.f90:22, 37, 52, 64` | One aquifer record for the active frequency. |

```text
title:    bsn%name, prog
header:   aqu_hdr
units:    aqu_hdr_units
data:     jday mon day yr unit gis_id name aqu_*(iaq)%flo ... flo_ls
```

## Columns Written

| Column | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` |  | `time%day` | Julian day / simulation day of the reporting period. |
| `mon` |  | `time%mo` | Simulation month. |
| `day` |  | `time%day_mo` | Day of month. |
| `yr` |  | `time%yrc` | Simulation year. |
| `unit` |  | `iaq` | Aquifer index (object number of this aquifer). |
| `gis_id` |  | `ob(iob)%gis_id` | GIS / object id of the aquifer object. |
| `name` |  | `ob(iob)%name` | Object name of the aquifer object. |
| `flo` | mm | `aqu_*(iaq)%flo` | lateral flow from aquifer |
| `dep_wt` | m | `aqu_*(iaq)%dep_wt` | average depth from average surface elevation to water table |
| `stor` | mm | `aqu_*(iaq)%stor` | average water storage in aquifer in timestep |
| `rchrg` | mm | `aqu_*(iaq)%rchrg` | recharge entering aquifer from other objects |
| `seep` | mm | `aqu_*(iaq)%seep` | seepage from bottom of aquifer |
| `revap` | mm | `aqu_*(iaq)%revap` | plant water uptake and evaporation |
| `no3_st` | kg/ha N | `aqu_*(iaq)%no3_st` | current total NO3-N mass in aquifer |
| `minp` | kg/ha P | `aqu_*(iaq)%minp` | mineral phosphorus transported in return (lateral) flow |
| `cbn` | percent | `aqu_*(iaq)%cbn` | organic carbon in aquifer - currently static |
| `orgn` | kg/ha P | `aqu_*(iaq)%orgn` | organic nitrogen in aquifer - currently static |
| `no3_rchg` | kg/ha N | `aqu_*(iaq)%no3_rchg` | nitrate NO3-N flowing into aquifer from another object |
| `no3_loss` | kg/ha | `aqu_*(iaq)%no3_loss` | nitrate NO3-N loss |
| `no3_lat` | kg/ha N | `aqu_*(iaq)%no3_lat` | nitrate loading to reach in groundwater |
| `no3_seep` | kg/ha N | `aqu_*(iaq)%no3_seep` | seepage of no3 to next object |
| `flo_cha` | mm H2O | `aqu_*(iaq)%flo_cha` | surface runoff flowing into channels |
| `flo_res` | mm H2O | `aqu_*(iaq)%flo_res` | surface runoff flowing into reservoirs |
| `flo_ls` | mm H2O | `aqu_*(iaq)%flo_ls` | surface runoff flowing into a landscape element (hru or ru) |

## Frequency-Specific Behavior

| Aspect | Daily | Monthly | Yearly | Average annual |
|---|---|---|---|---|
| State object | `aqu_d(iaq)` | `aqu_m(iaq)` | `aqu_y(iaq)` | `aqu_a(iaq)` |
| Text/CSV units | 2520 / 2524 | 2521 / 2525 | 2522 / 2526 | 2523 / 2527 |
| Trigger | daily print interval | `time%end_mo == 1` | `time%end_yr == 1` | `time%end_sim == 1` |
| Print flag | `pco%aqu%d` | `pco%aqu%m` | `pco%aqu%y` | `pco%aqu%a` |

The columns are identical across all four frequencies; only the accumulation window and the source state object differ.

## Data Sources And Calculations

- Daily values are written directly from `aqu_d(iaq)`, the per-timestep aquifer state.
- Monthly values accumulate the daily state (`aqu_m(iaq) = aqu_m(iaq) + aqu_d(iaq)`), and storage-like fields (`stor`, `dep_wt`, `no3_st`) are divided by the number of days to report a monthly average; the accumulator is then zeroed for the next month.
- Yearly values accumulate the monthly state the same way (`aqu_y(iaq) = aqu_y(iaq) + aqu_m(iaq)`).
- Average-annual values accumulate over the run and are divided by the number of years at simulation end.

## Writer Flow

1. For each aquifer `iaq`, resolve its spatial object `iob = sp_ob1%aqu + iaq - 1`.
2. If daily printing is enabled and within the print interval, write `aqu_d(iaq)` to the daily text (and CSV) file.
3. Accumulate the daily state into the monthly state; at month end, average the storage fields, write the monthly row, then zero the monthly accumulator.
4. Accumulate the monthly state into the yearly state; at year end, write the yearly row.
5. Accumulate into the average-annual state; at simulation end, average over the years and write the average-annual row.

## Line-Based I/O Trace

| Source Line | Operation | Unit | File | Fields |
|---:|---|---|---|---|
| `aquifer_output.f90:22` | `write` | `2520` | `aquifer_day.txt` | time, `iaq`, `ob(iob)`, `aqu_d(iaq)` |
| `aquifer_output.f90:24` | `write` | `2524` | `aquifer_day.csv` | time, `iaq`, `ob(iob)`, `aqu_d(iaq)` |
| `aquifer_output.f90:37` | `write` | `2521` | `aquifer_mon.txt` | time, `iaq`, `ob(iob)`, `aqu_m(iaq)` |
| `aquifer_output.f90:52` | `write` | `2522` | `aquifer_yr.txt` | time, `iaq`, `ob(iob)`, `aqu_y(iaq)` |
| `aquifer_output.f90:64` | `write` | `2523` | `aquifer_aa.txt` | time, `iaq`, `ob(iob)`, `aqu_a(iaq)` |

## Review Notes

- All four frequencies share the `aquifer_dynamic` layout; the columns table above applies to every file in the family.
- `cbn` and `orgn` are marked in the source as currently static (`organic carbon/nitrogen in aquifer - currently static`).
- `orgn` carries a `kg/ha P` unit comment in the source although it is organic nitrogen; likely a copy/paste unit typo.
- Monthly/yearly/average-annual rows report averages for storage-like fields and sums for flux fields; see Data Sources And Calculations.

## Source Links

- Writer: [`aquifer_output`](../procedures/aquifer_output.md) (`aquifer_output.f90:1-75`)
- Header/opener: [`header_aquifer`](../procedures/header_aquifer.md) (`header_aquifer.f90:1-80`)
- Data type: `aquifer_module::aquifer_dynamic`

## Evidence Used

- `aquifer_output.f90:1-75`
- `header_aquifer.f90:1-80`
- `aquifer_module.f90` (`type aquifer_dynamic`)
