---
kind: output_family
source_symbols:
- cs_balance
- header_const
title: basin_cs_*
status: filled
source_hash: 4b021c986961cc6c
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_const`](../procedures/header_const.md)  
**Written by:** [`cs_balance`](../procedures/cs_balance.md)  
**Primary data type:** `output_csbal_header` / the `cs_basin(87)` flux array in `cs_balance`  
**Files covered:** `basin_cs_day`, `basin_cs_mon`, `basin_cs_yr`, `basin_cs_aa` (text only — no CSV)

## Bottom Line

`basin_cs_*` is the basin-wide constituent (trace-element) mass-balance time series. Each row is one reporting period for the whole basin: the date, then 87 flux and state values. The 87 values are 29 mass-balance categories reported for each of three fixed constituents — **seo4** (selenate), **seo3** (selenite), and **boron** — in that order (`seo4` = columns 1–29, `seo3` = 30–58, `boron` = 59–87). Every value is a mass in kilograms (kg/yr for the average-annual file).

This is one documentation page, not four. Daily, monthly, yearly, and average-annual files share the same 90-column layout (3 date columns + 87 balance columns); only the file name, unit number, print flag, and accumulation window differ. Unlike most constituent families, `basin_cs_*` has **no CSV companion** — the files are fixed-width text only.

> **What each row means:** a whole-basin selenium/boron budget for one reporting period. Reading across each 29-column constituent block you see where the element came from and went — lateral, surface, sediment, urban, wetland, tile, and tile/percolation flows to streams and aquifers; groundwater transfer, wetland seepage, and three irrigation sources into soil; rainfall, dry deposition, and fertilizer inputs; plant uptake, soil and aquifer reaction/sorption transfers; watershed and outside point sources; groundwater discharge, recharge, and seepage; and the total dissolved and sorbed mass stored in the soil profile and aquifer. Pick the file whose frequency matches your timestep — the columns are identical across all four.

## Output Family

| Frequency | Text File | Text Unit | State Written | Write Line |
|---|---|---:|---|---|
| Daily | `basin_cs_day.txt` | 6080 | `cs_basin(1:87)` | `cs_balance.f90:504` |
| Monthly | `basin_cs_mon.txt` | 6082 | `cs_basin_mo(1:87)` | `cs_balance.f90:529` |
| Yearly | `basin_cs_yr.txt` | 6084 | `cs_basin_yr(1:87)` | `cs_balance.f90:549` |
| Average annual | `basin_cs_aa.txt` | 6086 | `cs_basin_aa(1:87)` | `cs_balance.f90:586` |

## File Contracts

| Frequency | Open Condition | Open Line | Header Row | Catalog Entry |
|---|---|---|---|---|
| Daily | `pco%cs_basin%d == "y"` and `cs_db%num_cs > 0` | `header_const.f90:18` | definitions block + `csb_hdr` (`header_const.f90:26-56`) | `basin_cs_day.txt` |
| Monthly | `pco%cs_basin%m == "y"` and `cs_db%num_cs > 0` | `header_const.f90:61` | definitions block + `csb_hdr` (`header_const.f90:69-99`) | `basin_cs_mon.txt` |
| Yearly | `pco%cs_basin%y == "y"` and `cs_db%num_cs > 0` | `header_const.f90:104` | definitions block + `csb_hdr` (`header_const.f90:112-142`) | `basin_cs_yr.txt` |
| Average annual | `pco%cs_basin%a == "y"` and `cs_db%num_cs > 0` | `header_const.f90:147` | definitions block + `csb_hdr` (`header_const.f90:155-185`) | `basin_cs_aa.txt` |

## Writer And Print Controls

| Control | Source Line | Applies To | Meaning |
|---|---:|---|---|
| `cs_db%num_cs > 0` | `header_const.f90:17` | All | Files are only opened when constituents (cs) are simulated. |
| `pco%cs_basin%d == "y"` | `header_const.f90:17` | Daily | Opens `basin_cs_day.txt`. See the note about the daily write guard in Review Notes. |
| `pco%cs_basin%m == "y"` | `header_const.f90:60` | Monthly | Opens `basin_cs_mon.txt`. |
| `pco%cs_basin%y == "y"` | `header_const.f90:103` | Yearly | Opens `basin_cs_yr.txt`. |
| `pco%cs_basin%a == "y"` | `header_const.f90:146` | Average annual | Opens `basin_cs_aa.txt`. |
| `time%end_mo == 1` | `cs_balance.f90:514` | Monthly | Averages state columns, writes the monthly row, then zeroes the monthly accumulator. |
| `time%end_yr == 1` | `cs_balance.f90:534` | Yearly | Averages state columns, writes the yearly row, then zeroes the yearly accumulator. |
| `time%end_sim == 1` | `cs_balance.f90:554` | Average annual | Divides accumulated fluxes by the number of years, writes the average-annual row. |

## Shared Record Layout

| Row Part | Columns | Source | Meaning |
|---|---|---|---|
| Title row | Basin name and program string | `header_const.f90:19` | Identifies the model run. |
| Definitions block | One line per category | `header_const.f90:26-54` | Human-readable units and source→sink description for each stem. |
| Header row | `csb_hdr` | `header_const.f90:56` | Column names `yr mo jday` then `<stem>_<constituent>` for all 87 balance columns. |
| Data row | `time%yrc`, `time%mo`, `time%day`, `cs_basin(1:87)` | `cs_balance.f90:504` | One whole-basin constituent budget for the active frequency. |

```text
title:   bsn%name, prog
header:  yr mo jday  latq_seo4 ... sbd_aq_seo4  latq_seo3 ... sbd_aq_seo3  latq_born ... sbd_aq_born
data:    time%yrc time%mo time%day  cs_basin(1) ... cs_basin(87)
format:  (i8,i8,i8,100e16.8)   (cs_balance.f90:682)
```

## Columns Written

The row begins with three date columns, then repeats the 29 mass-balance categories below for `seo4`, `seo3`, and `boron` (columns 1–29, 30–58, 59–87). Column names are `<stem>_seo4`, `<stem>_seo3`, `<stem>_born`. All values are kg (kg/yr in the average-annual file).

| # | Date Column | Source Field |
|---|---|---|
| 1 | `yr` | `time%yrc` |
| 2 | `mo` | `time%mo` |
| 3 | `jday` | `time%day` |

| Block # | Stem | Category Meaning (from `header_const`) |
|---:|---|---|
| 1 | `latq` | Mass in soil lateral flow (soil → stream). |
| 2 | `surq` | Mass in surface runoff (soil → stream). |
| 3 | `sedm` | Mass in sediment runoff (soil → stream). |
| 4 | `urbq` | Mass in urban runoff (soil → stream). |
| 5 | `wetq` | Mass in wetland runoff (wetland → stream). |
| 6 | `tile` | Mass in tile drain flow (soil → stream). |
| 7 | `perc` | Mass in deep percolation (soil → aquifer). |
| 8 | `gwup` | Mass from groundwater transfer (aquifer → soil). |
| 9 | `wtsp` | Mass in wetland seepage (wetland → soil). |
| 10 | `irsw` | Mass in surface-water irrigation (channel → soil). |
| 11 | `irgw` | Mass in groundwater irrigation (aquifer → soil). |
| 12 | `irwo` | Mass in outside-source irrigation (outside → soil). |
| 13 | `rain` | Mass in rainfall (outside → soil). |
| 14 | `dryd` | Mass in dry deposition (outside → soil). |
| 15 | `fert` | Mass in applied fertilizer (outside → soil). |
| 16 | `uptk` | Mass in plant uptake (soil → outside). |
| 17 | `rct_sl` | Mass transferred via reaction — soil. |
| 18 | `srb_sl` | Mass transferred via sorption — soil. |
| 19 | `ptso` | Mass in watershed point sources (outside → channel). |
| 20 | `ptout` | Mass in outside point sources (outside → channel). |
| 21 | `dis_sl` | Total dissolved mass in soil water (state; averaged over the period). |
| 22 | `sbd_sl` | Total sorbed mass in soil profile (state; averaged over the period). |
| 23 | `gw` | Mass in groundwater discharge (aquifer → channel). |
| 24 | `rchg` | Mass in groundwater recharge (soil → aquifer). |
| 25 | `seep` | Mass in groundwater seepage (aquifer → deep). |
| 26 | `rct_aq` | Mass transferred via reaction — aquifer. |
| 27 | `srb_aq` | Mass transferred via sorption — aquifer. |
| 28 | `dis_aq` | Total dissolved mass in groundwater (state; averaged over the period). |
| 29 | `sbd_aq` | Total sorbed mass in aquifer (state; averaged over the period). |

## Frequency-Specific Behavior

| Aspect | Daily | Monthly | Yearly | Average annual |
|---|---|---|---|---|
| Array written | `cs_basin` | `cs_basin_mo` | `cs_basin_yr` | `cs_basin_aa` |
| Unit | 6080 | 6082 | 6084 | 6086 |
| Trigger | every simulation day | `time%end_mo == 1` | `time%end_yr == 1` | `time%end_sim == 1` |
| Flux value unit | kg | kg | kg | kg/yr |
| State columns (21,22,28,29 in each block) | instantaneous | ÷ days in month | ÷ days in year | ÷ days |

The columns are identical across all four frequencies; only the accumulation window and the state-column averaging differ.

## Data Sources And Calculations

- Each daily category is summed across the relevant objects and converted to kg. HRU-based terms multiply the per-hectare loading by `hru(i)%area_ha` (`cs_balance.f90:43-336`); point-source terms come from `reccsb_d`/`recoutcsb_d`; aquifer terms come from `acsb_d` and `cs_aqu` (or, when `gwflow` is active, from `gwsol_ss`/`gwsol_state` cell arrays, converted from g to kg by `/1000`).
- After the daily write, each of the 87 values is added into the monthly, yearly, and average-annual accumulators (`cs_balance.f90:507-511`).
- Monthly and yearly rows divide the four state columns in each constituent block (indices 21, 22, 28, 29 → array indices 21/22/28/29, 50/51/57/58, 79/80/86/87) by the number of days to report a period average, then zero the accumulator (`cs_balance.f90:514-531`, `:534-551`).
- The average-annual row divides the flux categories by `time%nbyr` and the state columns by `time%days_prt` (`cs_balance.f90:554-587`).

## Writer Flow

1. Build `cs_basin(1:87)` by summing each mass-balance category over HRUs, recall objects, and aquifers (with the gwflow-cell path substituted when groundwater flow is active).
2. Write the daily row (`time`, `cs_basin(1:87)`) to unit 6080 with format `7000` (`cs_balance.f90:504`).
3. Add `cs_basin` into the monthly, yearly, and average-annual accumulators.
4. At month end, average the state columns, write the monthly row to 6082, and zero the monthly accumulator.
5. At year end, average the state columns, write the yearly row to 6084, and zero the yearly accumulator.
6. At simulation end, divide fluxes by years and state columns by days, and write the average-annual row to 6086.
7. Zero the daily balance arrays for the next day (`cs_balance.f90:590-679`).

## Line-Based I/O Trace

| Source Line | Operation | Unit | File | Fields |
|---:|---|---|---|---|
| `cs_balance.f90:504` | `write` | `6080` | `basin_cs_day.txt` | `time%yrc`, `time%mo`, `time%day`, `cs_basin(1:87)` |
| `cs_balance.f90:529` | `write` | `6082` | `basin_cs_mon.txt` | `time%yrc`, `time%mo`, `time%day`, `cs_basin_mo(1:87)` |
| `cs_balance.f90:549` | `write` | `6084` | `basin_cs_yr.txt` | `time%yrc`, `time%mo`, `time%day`, `cs_basin_yr(1:87)` |
| `cs_balance.f90:586` | `write` | `6086` | `basin_cs_aa.txt` | `time%yrc`, `time%mo`, `time%day`, `cs_basin_aa(1:87)` |

## Review Notes

- **Fixed three constituents.** `basin_cs_*` is hard-coded to selenate (`seo4`), selenite (`seo3`), and boron (`born`) — the balance is built from `hcsb_d(i)%cs(1..3)` and the `csb_hdr` labels end in those three suffixes. This is unlike the dynamic per-constituent HRU/channel `*_cs` families.
- **Daily write is not print-flag-guarded in the writer.** `cs_balance` writes unit 6080 every time it runs (`cs_balance.f90:504`), with no `pco%cs_basin%d` guard; the monthly/yearly/average-annual writes are guarded only by the `time%end_*` flags. The `pco%cs_basin%{d,m,y,a}` flags gate file *opening* in `header_const`. Enabling a coarser frequency without the daily flag therefore still emits daily writes to unit 6080.
- **No CSV.** `cs_balance` and `header_const` produce only the fixed-width text files for the basin balance; there is no `basin_cs_*.csv`.
- The write format is `(i8,i8,i8,100e16.8)` (`cs_balance.f90:682`), which allows up to 100 value fields for the 87 balance columns.

## Source Links

- Writer: [`cs_balance`](../procedures/cs_balance.md) (`cs_balance.f90:1-687`)
- Header/opener: [`header_const`](../procedures/header_const.md) (`header_const.f90:16-186`)
- Column-name type: `cs_module::output_csbal_header` (`csb_hdr`)

## Evidence Used

- `cs_balance.f90:1-687`
- `header_const.f90:16-186`
- `cs_module.f90:79-177` (`type output_csbal_header`, `csb_hdr`)
