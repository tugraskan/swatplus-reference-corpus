---
kind: output_family
source_symbols:
- hcsout_output
- header_cs
title: hydout_pests_*
status: filled
source_hash: b90a64c853492134
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_cs`](../procedures/header_cs.md)  
**Written by:** [`hcsout_output`](../procedures/hcsout_output.md)  
**Primary data type:** `constituent_mass_module::constituent_mass` (the `%pest` array of `hcs1` / `obcs(iob)%hcsout_*(iiout)`)  
**Files covered:** `hydout_pests_day`, `hydout_pests_mon`, `hydout_pests_yr`, `hydout_pests_aa` text/CSV pairs

## Bottom Line

`hydout_pests_*` reports the pesticide mass carried **out of** each spatial object on each of its outgoing hydrograph connections. `hcsout_output` walks every spatial object (`iob = 1, sp_ob%objs`) and, for each object, every outgoing hydrograph (`iiout = 1, ob(iob)%src_tot`). It writes one row per object-outflow link: time, the object identity, the descriptors of that outflow link, and then one value per simulated pesticide (an implied-do over `ipest = 1, cs_db%num_pests`).

This is one documentation page, not four. Daily, monthly, yearly, and average-annual files share the same row layout; only the file name, unit number, print condition, and source state object differ. The daily row is written from `hcs1` (the current outgoing constituent hydrograph); the coarser frequencies use the `hcsout_m`, `hcsout_y`, and `hcsout_a` accumulators.

> **What each row means:** one outgoing hydrograph link leaving one object for one reporting period. The first columns say which object it is and where the outflow goes (destination object type/number, hydrograph type, and the fraction of this object's hydrograph sent on this link); the remaining columns give the mass of each simulated pesticide carried out on that link. If a run simulates N pesticides there are N constituent columns. Pick the file whose frequency matches your timestep — the columns are the same across all four. Whole files only exist when at least one pesticide is simulated (`cs_db%num_pests > 0`).

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | State Written | Write Lines |
|---|---|---|---:|---:|---|---|
| Daily | `hydout_pests_day.txt` | `hydout_pests_day.csv` | 2740 | 2756 | `hcs1%pest` | `hcsout_output.f90:22, 26` |
| Monthly | `hydout_pests_mon.txt` | `hydout_pests_mon.csv` | 2741 | 2757 | `obcs(iob)%hcsout_m(iiout)%pest` | `hcsout_output.f90:73, 77` |
| Yearly | `hydout_pests_yr.txt` | `hydout_pests_yr.csv` | 2742 | 2758 (see note) | `obcs(iob)%hcsout_y(iiout)%pest` | `hcsout_output.f90:124, 128` |
| Average annual | `hydout_pests_aa.txt` | `hydout_pests_aa.csv` | 2743 | 2759 | `obcs(iob)%hcsout_a(iiout)%pest` | `hcsout_output.f90:175, 179` |

## File Contracts

| Frequency | Open Condition | Open Lines | Header Row | Catalog Entry |
|---|---|---|---|---|
| Daily | `pco%hyd%d == "y"` and `cs_db%num_pests > 0` | `header_cs.f90:239` (txt), `:244` (csv) | `csout_hyd_hdr` + one `cs_pest_solsor` label group per pesticide (`header_cs.f90:241`) | `HYDOUT_PESTS hydout_pests_day.txt/csv` |
| Monthly | `pco%hyd%m == "y"` and `cs_db%num_pests > 0` | `header_cs.f90:294` (txt), `:299` (csv) | same | `HYDOUT_PESTS hydout_pests_mon.txt/csv` |
| Yearly | `pco%hyd%y == "y"` and `cs_db%num_pests > 0` | `header_cs.f90:350` (txt), `:355` (csv) | same | `HYDOUT_PESTS hydout_pests_yr.txt/csv` |
| Average annual | `pco%hyd%a == "y"` and `cs_db%num_pests > 0` | `header_cs.f90:405` (txt), `:410` (csv) | same | `HYDOUT_PESTS hydout_pests_aa.txt/csv` |

## Writer And Print Controls

| Control | Source Line | Applies To | Meaning |
|---|---:|---|---|
| `cs_db%num_pests > 0` | `hcsout_output.f90:21`, `header_cs.f90:238` | All | Nothing is opened or written unless at least one pesticide is simulated. |
| `pco%hyd%d == "y"` | `header_cs.f90:237`, `hcsout_output.f90:20` | Daily | Enables the daily HYDOUT constituent files. |
| `pco%day_print == "y"` and `pco%int_day_cur == pco%int_day` | `hcsout_output.f90:19` | Daily | Restricts daily rows to the configured print interval. |
| `pco%hyd%m == "y"` | `header_cs.f90:292`, `hcsout_output.f90:71` | Monthly | Enables monthly HYDOUT files. |
| `pco%hyd%y == "y"` | `header_cs.f90:348`, `hcsout_output.f90:122` | Yearly | Enables yearly HYDOUT files. |
| `pco%hyd%a == "y"` | `header_cs.f90:403`, `hcsout_output.f90:172` | Average annual | Enables average-annual HYDOUT files. |
| `pco%csvout == "y"` | `hcsout_output.f90:25`, `header_cs.f90:243` | CSV companions | Enables the CSV file beside each text file. |
| `time%end_mo == 1` | `hcsout_output.f90:70` | Monthly | Writes monthly rows at month end. |
| `time%end_yr == 1` | `hcsout_output.f90:121` | Yearly | Writes yearly rows at year end. |
| `time%end_sim == 1` | `hcsout_output.f90:172` | Average annual | Writes average-annual rows at simulation end. |

## Shared Record Layout

| Row Part | Columns | Source | Meaning |
|---|---|---|---|
| Title row | Basin name and program string | `header_cs.f90:240` | Identifies the model run. |
| Header row | `csout_hyd_hdr` + per-pesticide labels | `header_cs.f90:241` | Column names; see the note about label/value alignment in Review Notes. |
| Data row | time, object identity, outflow descriptors, per-pesticide mass | `hcsout_output.f90:22` | One outgoing hydrograph link for the active frequency. |

```text
title:   bsn%name, prog
header:  csout_hyd_hdr, (cs_pest_solsor(ipest), ipest = 1, num_pests)
data:    jday mon day yr iob gis_id type num obtypout obtyp_noout htyp_out frac_out  pest(1) ... pest(num_pests)
```

## Columns Written

The first twelve columns are fixed. The pesticide columns then repeat once per simulated pesticide (`ipest = 1, cs_db%num_pests`).

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
| `pest(ipest)` | kg/ha | `hcs1%pest(ipest)` / `hcsout_*(iiout)%pest(ipest)` | Mass of pesticide `ipest` carried out on this outgoing hydrograph. One column per simulated pesticide. |

## Frequency-Specific Behavior

| Aspect | Daily | Monthly | Yearly | Average annual |
|---|---|---|---|---|
| State object | `hcs1` | `hcsout_m(iiout)` | `hcsout_y(iiout)` | `hcsout_a(iiout)` |
| Text/CSV units | 2740 / 2756 | 2741 / 2757 | 2742 / 2758 (see note) | 2743 / 2759 |
| Trigger | daily print interval | `time%end_mo == 1` | `time%end_yr == 1` | `time%end_sim == 1` |
| Print flag | `pco%hyd%d` | `pco%hyd%m` | `pco%hyd%y` | `pco%hyd%a` |

The columns are identical across all four frequencies; only the accumulation window and the source state object differ.

## Data Sources And Calculations

- The daily row is written directly from `hcs1`, the current outgoing constituent hydrograph for that outflow link (there is no separate `hcsout_d` accumulator).
- After the daily block the daily hydrograph is accumulated into the monthly state (`hcsout_m(iiout) = hcsout_m(iiout) + hcs1`, `hcsout_output.f90:67`).
- Monthly is accumulated into yearly (`hcsout_y(iiout) = hcsout_y(iiout) + hcsout_m(iiout)`, `hcsout_output.f90:118`), and yearly into average-annual (`hcsout_a(iiout) = hcsout_a(iiout) + hcsout_y(iiout)`, `hcsout_output.f90:169`).
- These are running sums of pesticide mass; the writer does not divide the constituent columns by the number of days or years, so monthly/yearly/average-annual rows are period totals of the daily outflow.

## Writer Flow

1. Loop over every spatial object `iob = 1, sp_ob%objs`.
2. For each object, loop over every outgoing hydrograph `iiout = 1, ob(iob)%src_tot`.
3. If daily printing is enabled and within the print interval and `cs_db%num_pests > 0`, write the daily row from `hcs1` to unit 2740 (and 2756 for CSV).
4. Accumulate `hcs1` into the monthly state; at month end write the monthly row from `hcsout_m(iiout)`.
5. Accumulate into the yearly state; at year end write the yearly row from `hcsout_y(iiout)`.
6. Accumulate into the average-annual state; at simulation end write the average-annual row from `hcsout_a(iiout)`.

## Line-Based I/O Trace

| Source Line | Operation | Unit | File | Fields |
|---:|---|---|---|---|
| `hcsout_output.f90:22` | `write` | `2740` | `hydout_pests_day.txt` | time, object identity, outflow descriptors, `hcs1%pest(:)` |
| `hcsout_output.f90:26` | `write` | `2756` | `hydout_pests_day.csv` | time, object identity, outflow descriptors, `hcs1%pest(:)` |
| `hcsout_output.f90:73` | `write` | `2741` | `hydout_pests_mon.txt` | time, object identity, outflow descriptors, `hcsout_m(iiout)%pest(:)` |
| `hcsout_output.f90:124` | `write` | `2742` | `hydout_pests_yr.txt` | time, object identity, outflow descriptors, `hcsout_y(iiout)%pest(:)` |
| `hcsout_output.f90:128` | `write` | `2752` | (misdirected — see note) | time, object identity, outflow descriptors, `hcsout_y(iiout)%pest(:)` |
| `hcsout_output.f90:175` | `write` | `2743` | `hydout_pests_aa.txt` | time, object identity, outflow descriptors, `hcsout_a(iiout)%pest(:)` |

## Review Notes

- **Yearly CSV unit anomaly.** The header opens the yearly-pests CSV as unit `2758` (`header_cs.f90:355`), but the writer's yearly CSV write targets unit `2752` (`hcsout_output.f90:128`) — the unit the header assigns to `hydout_salts_day.txt` (`header_cs.f90:278`). As written, `hydout_pests_yr.csv` (2758) receives no data rows and the yearly-pests CSV values land on the salts daily-text unit instead. This is a source-level unit typo; the yearly text file (2742) is unaffected.
- **Header/data column alignment.** The fixed part of the header (`csout_hyd_hdr`, `constituent_mass_module.f90:568-581`) has twelve labels that match the twelve fixed data columns. Each pesticide then contributes a `cs_pest_solsor` group (`sol_out`/`sor_out`, two labels) to the header, while the data row writes a single value per pesticide. Readers aligning constituent columns by position should key off the writer (`hcsout_output.f90:22`), not the per-constituent header labels.
- The pesticide value unit is `kg/ha`, from the `%pest` comment in `type constituent_mass` (`constituent_mass_module.f90:80`).
- Rows are emitted per outgoing hydrograph link, so an object with several outflows contributes several rows per period.

## Source Links

- Writer: [`hcsout_output`](../procedures/hcsout_output.md) (`hcsout_output.f90:1-222`)
- Header/opener: [`header_cs`](../procedures/header_cs.md) (`header_cs.f90:236-455`)
- Data type: `constituent_mass_module::constituent_mass` (`%pest`)

## Evidence Used

- `hcsout_output.f90:1-222`
- `header_cs.f90:236-455`
- `constituent_mass_module.f90:79-90` (`type constituent_mass`), `:154` (`hcs1`), `:159-174` (`all_constituent_hydrograph`, `obcs`), `:568-591` (`csout_hyd_hdr`, `sol_sor`)
- `hydrograph_module.f90:350-355` (`obtyp_out`, `obtypno_out`, `htyp_out`, `frac_out`)
