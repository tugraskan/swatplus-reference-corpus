---
kind: output_family
source_symbols:
- header_salt
- salt_balance
title: basin_salt_*
status: filled
source_hash: 7ce26797ab9d880a
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`salt_balance`](../procedures/salt_balance.md)  
**Primary data type:** `salt_module::output_saltbal_header` / the `salt_basin(28)` flux array in `salt_balance`  
**Files covered:** `basin_salt_day`, `basin_salt_mon`, `basin_salt_yr`, `basin_salt_aa` (text only — no CSV)

## Bottom Line

`basin_salt_*` is the basin-wide salt mass-balance time series. Each row is one reporting period for the whole basin: the date, then 28 flux and state values in kilograms. Every value is the **sum over all simulated salt ions** (so4, ca, mg, na, k, cl, co3, hco3) — there is one column per mass-balance category, not per ion. This is the key structural difference from `basin_cs_*`, which reports each category separately for three fixed constituents.

This is one documentation page, not four. Daily, monthly, yearly, and average-annual files share the same 31-column layout (3 date columns + 28 balance columns); only the file name, unit number, print flag, and accumulation window differ. Like `basin_cs_*`, this family has **no CSV companion** — the files are fixed-width text only.

> **What each row means:** a whole-basin salt budget for one reporting period, in kg, totalled across all salt ions. Reading across the 28 columns you see where salt came from and went — lateral, groundwater, surface, urban, wetland, and tile flows to streams; percolation to the aquifer; groundwater transfer and wetland seepage back to soil; three irrigation sources; rainfall, dry deposition, road salt, fertilizer, and soil-amendment inputs; plant uptake; watershed and outside point sources; groundwater recharge and seepage; salt dissolved from soil and aquifer minerals; and the total dissolved and mineral salt mass stored in the soil profile and aquifer. Pick the file whose frequency matches your timestep — the columns are identical across all four.

## Output Family

| Frequency | Text File | Text Unit | State Written | Write Line |
|---|---|---:|---|---|
| Daily | `basin_salt_day.txt` | 5080 | `salt_basin(1:28)` | `salt_balance.f90:370` |
| Monthly | `basin_salt_mon.txt` | 5082 | `salt_basin_mo(1:28)` | `salt_balance.f90:386` |
| Yearly | `basin_salt_yr.txt` | 5084 | `salt_basin_yr(1:28)` | `salt_balance.f90:397` |
| Average annual | `basin_salt_aa.txt` | 5086 | `salt_basin_aa(1:28)` | `salt_balance.f90:411` |

## File Contracts

| Frequency | Open Condition | Open Line | Header Row | Catalog Entry |
|---|---|---|---|---|
| Daily | `pco%salt_basin%d == "y"` and `cs_db%num_salts > 0` | `header_salt.f90:18` | definitions block + `saltb_hdr` (`header_salt.f90:26-55`) | `basin_salt_day.txt` |
| Monthly | `pco%salt_basin%m == "y"` and `cs_db%num_salts > 0` | `header_salt.f90:60` | definitions block + `saltb_hdr` (`header_salt.f90:97`) | `basin_salt_mon.txt` |
| Yearly | `pco%salt_basin%y == "y"` and `cs_db%num_salts > 0` | `header_salt.f90:102` | definitions block + `saltb_hdr` (`header_salt.f90:139`) | `basin_salt_yr.txt` |
| Average annual | `pco%salt_basin%a == "y"` and `cs_db%num_salts > 0` | `header_salt.f90:144` | definitions block + `saltb_hdr` (`header_salt.f90:181`) | `basin_salt_aa.txt` |

## Writer And Print Controls

| Control | Source Line | Applies To | Meaning |
|---|---:|---|---|
| `cs_db%num_salts > 0` | `header_salt.f90:17` | All | Files are only opened when salt ions are simulated. |
| `pco%salt_basin%d == "y"` | `header_salt.f90:17` | Daily | Opens `basin_salt_day.txt`. See the note about the daily write guard in Review Notes. |
| `pco%salt_basin%m == "y"` | `header_salt.f90:59` | Monthly | Opens `basin_salt_mon.txt`. |
| `pco%salt_basin%y == "y"` | `header_salt.f90:101` | Yearly | Opens `basin_salt_yr.txt`. |
| `pco%salt_basin%a == "y"` | `header_salt.f90:143` | Average annual | Opens `basin_salt_aa.txt`. |
| `time%end_mo == 1` | `salt_balance.f90:380` | Monthly | Averages state columns, writes the monthly row, then zeroes the monthly accumulator. |
| `time%end_yr == 1` | `salt_balance.f90:391` | Yearly | Averages state columns, writes the yearly row, then zeroes the yearly accumulator. |
| `time%end_sim == 1` | `salt_balance.f90:402` | Average annual | Divides accumulated fluxes by the number of years, writes the average-annual row. |

## Shared Record Layout

| Row Part | Columns | Source | Meaning |
|---|---|---|---|
| Title row | Basin name and program string | `header_salt.f90:19` | Identifies the model run. |
| Definitions block | One line per category | `header_salt.f90:26-53` | Human-readable units and source→sink description for each stem. |
| Header row | `saltb_hdr` | `header_salt.f90:55` | Column names `yr mo jday` then the 28 `*_kg` balance columns. |
| Data row | `time%yrc`, `time%mo`, `time%day`, `salt_basin(1:28)` | `salt_balance.f90:370` | One whole-basin salt budget for the active frequency. |

```text
title:   bsn%name, prog
header:  yr mo jday  lat_kg gw_kg sur_kg ... aquds_kg aqumn_kg
data:    time%yrc time%mo time%day  salt_basin(1) ... salt_basin(28)
format:  (i8,i8,i8,35e16.8)   (salt_balance.f90:501)
```

## Columns Written

The row begins with three date columns, then 28 balance columns. Each balance value is a total in kg summed over all simulated salt ions. All values are kg.

| # | Column | Source | Meaning (from `header_salt`) |
|---:|---|---|---|
| 1 | `yr` | `time%yrc` | Calendar year. |
| 2 | `mo` | `time%mo` | Simulation month. |
| 3 | `jday` | `time%day` | Julian day / simulation day. |
| 4 | `lat_kg` | `salt_basin(1)` | Salt mass in soil lateral flow (soil → stream). |
| 5 | `gw_kg` | `salt_basin(2)` | Salt mass in groundwater flow (aquifer → stream). |
| 6 | `sur_kg` | `salt_basin(3)` | Salt mass in surface runoff (soil → stream). |
| 7 | `urb_kg` | `salt_basin(4)` | Salt mass in urban runoff (soil → stream). |
| 8 | `wet_kg` | `salt_basin(5)` | Salt mass in wetland runoff (wetland → stream). |
| 9 | `tile_kg` | `salt_basin(6)` | Salt mass in tile drain flow (soil → stream). |
| 10 | `perc_kg` | `salt_basin(7)` | Salt mass in deep percolation (soil → aquifer). |
| 11 | `gwup_kg` | `salt_basin(8)` | Salt mass from groundwater transfer (aquifer → soil). |
| 12 | `wtsp_kg` | `salt_basin(9)` | Salt mass in wetland seepage (wetland → soil). |
| 13 | `irsw_kg` | `salt_basin(10)` | Salt mass in surface-water irrigation (channel → soil). |
| 14 | `irgw_kg` | `salt_basin(11)` | Salt mass in groundwater irrigation (aquifer → soil). |
| 15 | `irwo_kg` | `salt_basin(12)` | Salt mass in outside-source irrigation (outside → soil). |
| 16 | `rain_kg` | `salt_basin(13)` | Salt mass in rainfall (outside → soil). |
| 17 | `dryd_kg` | `salt_basin(14)` | Salt mass in dry deposition (outside → soil). |
| 18 | `road_kg` | `salt_basin(15)` | Salt mass in applied road salt (outside → soil). |
| 19 | `fert_kg` | `salt_basin(16)` | Salt mass in applied fertilizer (outside → soil). |
| 20 | `amnd_kg` | `salt_basin(17)` | Salt mass in soil amendments (outside → soil). |
| 21 | `uptk_kg` | `salt_basin(18)` | Salt mass in plant uptake (soil → outside). |
| 22 | `ptso_kg` | `salt_basin(19)` | Salt mass in watershed point sources (outside → channel). |
| 23 | `ptout_kg` | `salt_basin(20)` | Salt mass in outside point sources (outside → channel). |
| 24 | `rchg_kg` | `salt_basin(21)` | Salt mass in groundwater recharge (soil → aquifer). |
| 25 | `seep_kg` | `salt_basin(22)` | Salt mass in groundwater seepage (aquifer → deep). |
| 26 | `dssl_kg` | `salt_basin(23)` | Salt mass dissolved from soil minerals (mineral → soil). |
| 27 | `dsaq_kg` | `salt_basin(24)` | Salt mass dissolved from aquifer minerals (mineral → aquifer). |
| 28 | `soilds_kg` | `salt_basin(25)` | Total dissolved salt mass in soil water (state; averaged over the period). |
| 29 | `soilmn_kg` | `salt_basin(26)` | Total salt mineral mass in soil profile (state; averaged over the period). |
| 30 | `aquds_kg` | `salt_basin(27)` | Total dissolved salt mass in groundwater (state; averaged over the period). |
| 31 | `aqumn_kg` | `salt_basin(28)` | Total salt mineral mass in aquifer (state; averaged over the period). |

## Frequency-Specific Behavior

| Aspect | Daily | Monthly | Yearly | Average annual |
|---|---|---|---|---|
| Array written | `salt_basin` | `salt_basin_mo` | `salt_basin_yr` | `salt_basin_aa` |
| Unit | 5080 | 5082 | 5084 | 5086 |
| Trigger | every simulation day | `time%end_mo == 1` | `time%end_yr == 1` | `time%end_sim == 1` |
| State columns (25–28) | instantaneous | ÷ days in month | ÷ days in year | ÷ days |

The columns are identical across all four frequencies; only the accumulation window and the state-column averaging differ.

## Data Sources And Calculations

- Each daily category is summed across the relevant objects and over all salt ions (`do m = 1, cs_db%num_salts`), converted to kg. HRU-based terms multiply the per-hectare loading by `hru(i)%area_ha` (`salt_balance.f90:42-329`); point-source terms come from `recsaltb_d`/`recoutsaltb_d`; aquifer terms come from `asaltb_d` and `cs_aqu` (or, when `gwflow` is active, from `gwsol_ss`/`gwsol_state` cell arrays, converted from g to kg by `/1000`).
- After the daily write, each of the 28 values is added into the monthly, yearly, and average-annual accumulators (`salt_balance.f90:373-377`).
- Monthly and yearly rows divide the four state columns (25–28) by the number of days to report a period average, then zero the accumulator (`salt_balance.f90:380-388`, `:391-399`).
- The average-annual row divides the flux categories (1–23) by `time%nbyr` and the state columns (25–28) by `time%days_prt` (`salt_balance.f90:402-412`).

## Writer Flow

1. Build `salt_basin(1:28)` by summing each mass-balance category over HRUs, recall objects, and aquifers, and over all salt ions (with the gwflow-cell path substituted when groundwater flow is active).
2. Write the daily row (`time`, `salt_basin(1:28)`) to unit 5080 with format `7000` (`salt_balance.f90:370`).
3. Add `salt_basin` into the monthly, yearly, and average-annual accumulators.
4. At month end, average the state columns, write the monthly row to 5082, and zero the monthly accumulator.
5. At year end, average the state columns, write the yearly row to 5084, and zero the yearly accumulator.
6. At simulation end, divide fluxes by years and state columns by days, and write the average-annual row to 5086.
7. Zero the daily balance arrays for the next day (`salt_balance.f90:415-498`).

## Line-Based I/O Trace

| Source Line | Operation | Unit | File | Fields |
|---:|---|---|---|---|
| `salt_balance.f90:370` | `write` | `5080` | `basin_salt_day.txt` | `time%yrc`, `time%mo`, `time%day`, `salt_basin(1:28)` |
| `salt_balance.f90:386` | `write` | `5082` | `basin_salt_mon.txt` | `time%yrc`, `time%mo`, `time%day`, `salt_basin_mo(1:28)` |
| `salt_balance.f90:397` | `write` | `5084` | `basin_salt_yr.txt` | `time%yrc`, `time%mo`, `time%day`, `salt_basin_yr(1:28)` |
| `salt_balance.f90:411` | `write` | `5086` | `basin_salt_aa.txt` | `time%yrc`, `time%mo`, `time%day`, `salt_basin_aa(1:28)` |

## Review Notes

- **Totals across salt ions.** Every balance column is a sum over all simulated salt ions (so4, ca, mg, na, k, cl, co3, hco3), so the file does not resolve individual ions — one column per category. This is the structural opposite of `basin_cs_*`, which reports 29 categories for each of three fixed constituents.
- **Daily write is not print-flag-guarded in the writer.** `salt_balance` writes unit 5080 every time it runs (`salt_balance.f90:370`), with no `pco%salt_basin%d` guard; the monthly/yearly/average-annual writes are guarded only by the `time%end_*` flags. The `pco%salt_basin%{d,m,y,a}` flags gate file *opening* in `header_salt`.
- **Small-value flooring.** Several input categories (road, fert, amnd, uptk) are floored to zero when their basin total is below `1.e-6` kg (`salt_balance.f90:196, 206, 216, 226`).
- **No CSV.** `salt_balance` and `header_salt` produce only the fixed-width text files for the basin balance; there is no `basin_salt_*.csv`.
- The write format is `(i8,i8,i8,35e16.8)` (`salt_balance.f90:501`), which allows up to 35 value fields for the 28 balance columns.

## Source Links

- Writer: [`salt_balance`](../procedures/salt_balance.md) (`salt_balance.f90:1-505`)
- Header/opener: [`header_salt`](../procedures/header_salt.md) (`header_salt.f90:16-182`)
- Column-name type: `salt_module::output_saltbal_header` (`saltb_hdr`)

## Evidence Used

- `salt_balance.f90:1-505`
- `header_salt.f90:16-182`
- `salt_module.f90:75-108` (`type output_saltbal_header`, `saltb_hdr`)
