---
kind: output_family
source_symbols:
- hcsout_output
- header_cs
title: hydout_salts_*
status: filled
source_hash: b90a64c853492134
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_cs`](../procedures/header_cs.md)  
**Written by:** [`hcsout_output`](../procedures/hcsout_output.md)  
**Primary data type:** `constituent_mass_module::constituent_mass` (the `%salt` array of `hcs1` / `obcs(iob)%hcsout_*(iiout)`)  
**Files covered:** `hydout_salts_day`, `hydout_salts_mon`, `hydout_salts_yr`, `hydout_salts_aa` text/CSV pairs

## Bottom Line

`hydout_salts_*` reports the salt-ion mass carried **out of** each spatial object on each of its outgoing hydrograph connections. `hcsout_output` walks every spatial object (`iob = 1, sp_ob%objs`) and, for each object, every outgoing hydrograph (`iiout = 1, ob(iob)%src_tot`). It writes one row per object-outflow link: time, the object identity, the descriptors of that outflow link, and then one value per simulated salt ion (an implied-do over `isalt = 1, cs_db%num_salts`).

This is one documentation page, not four. Daily, monthly, yearly, and average-annual files share the same row layout; only the file name, unit number, print condition, and source state object differ. The daily row is written from `hcs1` (the current outgoing constituent hydrograph); the coarser frequencies use the `hcsout_m`, `hcsout_y`, and `hcsout_a` accumulators.

> **What each row means:** one outgoing hydrograph link leaving one object for one reporting period. The first columns say which object it is and where the outflow goes (destination object type/number, hydrograph type, and the fraction of this object's hydrograph sent on this link); the remaining columns give the mass of each simulated salt ion carried out on that link. If a run simulates N salt ions there are N constituent columns. Pick the file whose frequency matches your timestep — the columns are the same across all four. Whole files only exist when at least one salt ion is simulated (`cs_db%num_salts > 0`).

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | State Written | Write Lines |
|---|---|---|---:|---:|---|---|
| Daily | `hydout_salts_day.txt` | `hydout_salts_day.csv` | 2752 | 2768 | `hcs1%salt` | `hcsout_output.f90:55, 59` |
| Monthly | `hydout_salts_mon.txt` | `hydout_salts_mon.csv` | 2753 | 2769 | `obcs(iob)%hcsout_m(iiout)%salt` | `hcsout_output.f90:106, 110` |
| Yearly | `hydout_salts_yr.txt` | `hydout_salts_yr.csv` | 2754 | 2770 | `obcs(iob)%hcsout_y(iiout)%salt` | `hcsout_output.f90:157, 161` |
| Average annual | `hydout_salts_aa.txt` | `hydout_salts_aa.csv` | 2755 | 2771 | `obcs(iob)%hcsout_a(iiout)%salt` | `hcsout_output.f90:208, 212` |

## File Contracts

| Frequency | Open Condition | Open Lines | Header Row | Catalog Entry |
|---|---|---|---|---|
| Daily | `pco%hyd%d == "y"` and `cs_db%num_salts > 0` | `header_cs.f90:278` (txt), `:283` (csv) | `csout_hyd_hdr` + one `cs_salt_solsor` label group per salt ion (`header_cs.f90:281`) | `HYDOUT_SALTS hydout_salts_day.txt/csv` |
| Monthly | `pco%hyd%m == "y"` and `cs_db%num_salts > 0` | `header_cs.f90:333` (txt), `:338` (csv) | same | `HYDOUT_SALTS hydout_salts_mon.txt/csv` |
| Yearly | `pco%hyd%y == "y"` and `cs_db%num_salts > 0` | `header_cs.f90:389` (txt), `:394` (csv) | same | `HYDOUT_SALTS hydout_salts_yr.txt/csv` |
| Average annual | `pco%hyd%a == "y"` and `cs_db%num_salts > 0` | `header_cs.f90:444` (txt), `:449` (csv) | same | `HYDOUT_SALTS hydout_salts_aa.txt/csv` |

## Writer And Print Controls

| Control | Source Line | Applies To | Meaning |
|---|---:|---|---|
| `cs_db%num_salts > 0` | `hcsout_output.f90:54`, `header_cs.f90:277` | All | Nothing is opened or written unless at least one salt ion is simulated. |
| `pco%hyd%d == "y"` | `header_cs.f90:237`, `hcsout_output.f90:20` | Daily | Enables the daily HYDOUT constituent files. |
| `pco%day_print == "y"` and `pco%int_day_cur == pco%int_day` | `hcsout_output.f90:19` | Daily | Restricts daily rows to the configured print interval. |
| `pco%hyd%m == "y"` | `header_cs.f90:292`, `hcsout_output.f90:71` | Monthly | Enables monthly HYDOUT files. |
| `pco%hyd%y == "y"` | `header_cs.f90:348`, `hcsout_output.f90:122` | Yearly | Enables yearly HYDOUT files. |
| `pco%hyd%a == "y"` | `header_cs.f90:403`, `hcsout_output.f90:172` | Average annual | Enables average-annual HYDOUT files. |
| `pco%csvout == "y"` | `hcsout_output.f90:58`, `header_cs.f90:282` | CSV companions | Enables the CSV file beside each text file. |
| `time%end_mo == 1` | `hcsout_output.f90:70` | Monthly | Writes monthly rows at month end. |
| `time%end_yr == 1` | `hcsout_output.f90:121` | Yearly | Writes yearly rows at year end. |
| `time%end_sim == 1` | `hcsout_output.f90:172` | Average annual | Writes average-annual rows at simulation end. |

## Shared Record Layout

| Row Part | Columns | Source | Meaning |
|---|---|---|---|
| Title row | Basin name and program string | `header_cs.f90:280` | Identifies the model run. |
| Header row | `csout_hyd_hdr` + per-salt-ion labels | `header_cs.f90:281` | Column names; see the note about label/value alignment in Review Notes. |
| Data row | time, object identity, outflow descriptors, per-salt-ion mass | `hcsout_output.f90:55` | One outgoing hydrograph link for the active frequency. |

```text
title:   bsn%name, prog
header:  csout_hyd_hdr, (cs_salt_solsor(isalt), isalt = 1, num_salts)
data:    jday mon day yr iob gis_id type num obtypout obtyp_noout htyp_out frac_out  salt(1) ... salt(num_salts)
```

## Columns Written

The first twelve columns are fixed. The salt-ion columns then repeat once per simulated salt ion (`isalt = 1, cs_db%num_salts`).

| Column | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` |  | `time%day` | Julian day / simulation day of the reporting period. |
| `mon` |  | `time%mo` | Simulation month. |
| `day` |  | `time%day_mo` | Day of month. |
| `yr` |  | `time%yrc` | Calendar year. |
| `iob` |  | `iob` | Spatial object number of the source object. |
| `gis_id` |  | `ob(iob)%gis_id` | GIS id of the source object. |
| `type` |  | `ob(iob)%typ` | Source object type (hru, sd_hru, chan, res, recall, …). |
| `num` |  | `ob(iob)%num` | Spatial object number within its type. |
| `obtypout` |  | `ob(iob)%obtyp_out(iiout)` | Outflow (destination) object type of this outgoing hydrograph. |
| `obtyp_noout` |  | `ob(iob)%obtypno_out(iiout)` | Outflow object type number (which destination object of that type). |
| `htyp_out` |  | `ob(iob)%htyp_out(iiout)` | Outflow hydrograph type (tot, rec, surf, …). |
| `frac_out` | frac | `ob(iob)%frac_out(iiout)` | Fraction of this object's hydrograph sent on this outgoing link. |
| `salt(isalt)` | kg/ha | `hcs1%salt(isalt)` / `hcsout_*(iiout)%salt(isalt)` | Mass of salt ion `isalt` carried out on this outgoing hydrograph. One column per simulated salt ion. |

## Frequency-Specific Behavior

| Aspect | Daily | Monthly | Yearly | Average annual |
|---|---|---|---|---|
| State object | `hcs1` | `hcsout_m(iiout)` | `hcsout_y(iiout)` | `hcsout_a(iiout)` |
| Text/CSV units | 2752 / 2768 | 2753 / 2769 | 2754 / 2770 | 2755 / 2771 |
| Trigger | daily print interval | `time%end_mo == 1` | `time%end_yr == 1` | `time%end_sim == 1` |
| Print flag | `pco%hyd%d` | `pco%hyd%m` | `pco%hyd%y` | `pco%hyd%a` |

The columns are identical across all four frequencies; only the accumulation window and the source state object differ.

## Data Sources And Calculations

- The daily row is written directly from `hcs1`, the current outgoing constituent hydrograph for that outflow link (there is no separate `hcsout_d` accumulator).
- After the daily block the daily hydrograph is accumulated into the monthly state (`hcsout_m(iiout) = hcsout_m(iiout) + hcs1`, `hcsout_output.f90:67`).
- Monthly is accumulated into yearly (`hcsout_y(iiout) = hcsout_y(iiout) + hcsout_m(iiout)`, `hcsout_output.f90:118`), and yearly into average-annual (`hcsout_a(iiout) = hcsout_a(iiout) + hcsout_y(iiout)`, `hcsout_output.f90:169`).
- These are running sums of salt-ion mass; the writer does not divide the constituent columns by the number of days or years, so monthly/yearly/average-annual rows are period totals of the daily outflow.

## Writer Flow

1. Loop over every spatial object `iob = 1, sp_ob%objs`.
2. For each object, loop over every outgoing hydrograph `iiout = 1, ob(iob)%src_tot`.
3. If daily printing is enabled and within the print interval and `cs_db%num_salts > 0`, write the daily row from `hcs1` to unit 2752 (and 2768 for CSV).
4. Accumulate `hcs1` into the monthly state; at month end write the monthly row from `hcsout_m(iiout)`.
5. Accumulate into the yearly state; at year end write the yearly row from `hcsout_y(iiout)`.
6. Accumulate into the average-annual state; at simulation end write the average-annual row from `hcsout_a(iiout)`.

## Line-Based I/O Trace

| Source Line | Operation | Unit | File | Fields |
|---:|---|---|---|---|
| `hcsout_output.f90:55` | `write` | `2752` | `hydout_salts_day.txt` | time, object identity, outflow descriptors, `hcs1%salt(:)` |
| `hcsout_output.f90:59` | `write` | `2768` | `hydout_salts_day.csv` | time, object identity, outflow descriptors, `hcs1%salt(:)` |
| `hcsout_output.f90:106` | `write` | `2753` | `hydout_salts_mon.txt` | time, object identity, outflow descriptors, `hcsout_m(iiout)%salt(:)` |
| `hcsout_output.f90:157` | `write` | `2754` | `hydout_salts_yr.txt` | time, object identity, outflow descriptors, `hcsout_y(iiout)%salt(:)` |
| `hcsout_output.f90:208` | `write` | `2755` | `hydout_salts_aa.txt` | time, object identity, outflow descriptors, `hcsout_a(iiout)%salt(:)` |

## Review Notes

- **Shared unit number 2752.** The daily HYDOUT_SALTS text file is opened as unit `2752` (`header_cs.f90:278`). The HYDOUT_PESTS yearly-CSV write also targets `2752` by mistake (`hcsout_output.f90:128`; see `hydout_pests`). During a run with both pesticides and salts enabled, the yearly-pests CSV rows are appended to whatever file 2752 is bound to. The salts daily rows themselves come from `hcsout_output.f90:55` and are correct.
- **Header/data column alignment.** The fixed part of the header (`csout_hyd_hdr`, `constituent_mass_module.f90:568-581`) has twelve labels that match the twelve fixed data columns. Each salt ion then contributes a `cs_salt_solsor` group (`sol_out`/`sor_out`, two labels) to the header, while the data row writes a single value per salt ion. Readers aligning constituent columns by position should key off the writer (`hcsout_output.f90:55`), not the per-constituent header labels.
- The salt-ion value unit is `kg/ha`, from the `%salt` comment in `type constituent_mass` (`constituent_mass_module.f90:83`).
- Rows are emitted per outgoing hydrograph link, so an object with several outflows contributes several rows per period.

## Source Links

- Writer: [`hcsout_output`](../procedures/hcsout_output.md) (`hcsout_output.f90:1-222`)
- Header/opener: [`header_cs`](../procedures/header_cs.md) (`header_cs.f90:236-455`)
- Data type: `constituent_mass_module::constituent_mass` (`%salt`)

## Evidence Used

- `hcsout_output.f90:1-222`
- `header_cs.f90:236-455`
- `constituent_mass_module.f90:79-90` (`type constituent_mass`), `:154` (`hcs1`), `:159-174` (`all_constituent_hydrograph`, `obcs`), `:568-591` (`csout_hyd_hdr`, `sol_sor`)
- `hydrograph_module.f90:350-355` (`obtyp_out`, `obtypno_out`, `htyp_out`, `frac_out`)
