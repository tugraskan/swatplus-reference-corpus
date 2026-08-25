---
kind: procedure
symbol: hcsin_output
title: hcsin_output
status: filled
source_hash: 8d2a1a8a4c2e3808
version_label: SWAT+ 62.0.0
locals:
  iin: Index of the incoming receiving-hydrograph slot within each object; it selects which
    inbound hydrograph entry and constituent-summary arrays are being written.
  ipest: Loop counter over pesticide constituents when writing pesticide mass arrays.
  ipath: Loop counter over pathogen constituents when writing pathogen mass arrays.
  imetal: Loop counter over heavy-metal constituents when writing heavy-metal mass arrays.
  isalt: Loop counter over salt constituents when writing salt mass arrays.
  iob: Index of the current spatial object in `sp_ob%objs`; it selects which object connection
    and output records are processed.
uses:
  hydrograph_module: '`hydrograph_module` provides the object inventory and receiving-hydrograph
    metadata that label every record. `sp_ob%objs` sets the outer loop bound, while `ob(iob)%rcv_tot`
    sets the inner loop bound and fields such as `gis_id`, `typ`, `num`, `obtyp_in`, `obtypno_in`,
    `htyp_in`, `frac_in`, and `hin_a` identify the routed object and the linked hydrograph
    entry whose constituent-output summaries are being reported.'
  time_module: '`time_module` determines when each reporting block is written and supplies
    the date fields attached to every row. The daily, monthly, yearly, and end-of-simulation
    flags gate the respective outputs, and `time%day`, `time%mo`, `time%day_mo`, `time%yrc`,
    and `time%yrs_prt` are written so each record can be tied to the simulation calendar and
    the average-annual normalization.'
  constituent_mass_module: '`constituent_mass_module` supplies the constituent counts and
    the nested hydrograph summary arrays that are actually written. `cs_db%num_pests`, `cs_db%num_paths`,
    `cs_db%num_metals`, and `cs_db%num_salts` control whether each constituent family is emitted,
    and the `obcs(iob)%hcsin_*` arrays provide the daily, monthly, yearly, and average-annual
    values that are accumulated and written for each family.'
---

<!-- facts:header -->

Writes hydrograph constituent-input summary outputs for each receiving object. It reports daily, monthly, yearly, and average-annual masses for pesticides, pathogens, metals, and salts, with optional CSV-formatted copies.

## Bottom Line

hcsin_output walks every spatial object and each of its receiving hydrograph slots, then writes the current constituent-input values for that object to the appropriate output files. It handles four reporting windows: daily, monthly, yearly, and average annual.

For each window it emits one record per constituent group that is active in `cs_db`: pesticides, pathogens, metals, and salts. The routine also maintains cumulative summaries by adding daily into monthly, monthly into yearly, and yearly into average annual state, so later model reporting can use the aggregated totals.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the hydrology/output workflow after routing and constituent hydrograph values have been populated for each object. The upstream state that matters most is the object connectivity and constituent-hydrograph storage in `hydrograph_module` and `constituent_mass_module`; the outputs here feed the model's daily reporting and the month-end, year-end, and average-annual summaries used later in post-processing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over spatial objects and their receiving hydrographs. | The routine iterates through every object in `sp_ob%objs`, then through each receiving hydrograph slot in `ob(iob)%rcv_tot`, so each inbound hydrograph can be reported separately. |
| 2. Emit daily summaries when daily printing is active. | If `pco%day_print` is enabled and the current day matches the print interval, the routine checks `pco%hyd%d` and writes daily pesticide, pathogen, metal, and salt records for the current object-receiver pair. Each constituent family is written only when its database count is greater than zero, and optional CSV copies are written when `pco%csvout == "y"`. |
| 3. Accumulate daily values into monthly totals. | The daily constituent-input summary `obcs(iob)%hcsin_d(iin)` is added into `obcs(iob)%hcsin_m(iin)` so month-to-date totals can be tracked. |
| 4. Emit monthly summaries at month end. | When `time%end_mo == 1` and monthly hydrograph output is enabled, the routine writes the month-end pesticide, pathogen, metal, and salt records from `obcs(iob)%hcsin_m(iin)`, with optional CSV copies beside each plain-text record. |
| 5. Accumulate monthly values into yearly totals. | The monthly constituent-input summary `obcs(iob)%hcsin_m(iin)` is added into `obcs(iob)%hcsin_y(iin)` so year-to-date totals can be tracked. |
| 6. Emit yearly summaries at year end. | When `time%end_yr == 1` and yearly hydrograph output is enabled, the routine writes the year-end pesticide, pathogen, metal, and salt records from `obcs(iob)%hcsin_y(iin)`, again with optional CSV-formatted duplicates. |
| 7. Accumulate yearly values into average-annual totals. | The yearly constituent-input summary `obcs(iob)%hcsin_y(iin)` is added into `obcs(iob)%hcsin_a(iin)` so the simulation-long accumulator is maintained. |
| 8. Normalize and emit average-annual summaries at simulation end. | When `time%end_sim == 1` and average-annual hydrograph output is enabled, the routine divides `ob(iob)%hin_a(iin)` by `time%yrs_prt` and writes the average-annual pesticide, pathogen, metal, and salt records from `obcs(iob)%hcsin_a(iin)`, with optional CSV copies for each family. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, ob` | `sp_ob%objs, ob(iob)%rcv_tot, ob(iob)%typ, ob(iob)%num, ob(iob)%obtyp_in(iin), ob(iob)%obtypno_in(iin), ob(iob)%htyp_in(iin), ob(iob)%frac_in(iin), ob(iob)%hin_a(iin)` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:constituent_mass_module] | `cs_db, obcs` | `cs_db%num_pests, obcs(iob)%hcsin_d(iin)%pest(ipest), cs_db%num_paths, obcs(iob)%hcsin_d(iin)%path(ipath), cs_db%num_metals, obcs(iob)%hcsin_d(iin)%hmet(imetal), cs_db%num_salts, obcs(iob)%hcsin_d(iin)%salt(isalt), obcs(iob)%hcsin_m(iin), obcs(iob)%hcsin_d(iin), obcs(iob)%hcsin_m(iin)%pest(ipest), obcs(iob)%hcsin_m(iin)%path(ipath), obcs(iob)%hcsin_m(iin)%hmet(imetal), obcs(iob)%hcsin_m(iin)%salt(isalt), obcs(iob)%hcsin_y(iin), obcs(iob)%hcsin_y(iin)%pest(ipest), obcs(iob)%hcsin_y(iin)%path(ipath), obcs(iob)%hcsin_y(iin)%hmet(imetal), obcs(iob)%hcsin_y(iin)%salt(isalt), obcs(iob)%hcsin_a(iin), obcs(iob)%hcsin_a(iin)%pest(ipest), obcs(iob)%hcsin_a(iin)%path(ipath), obcs(iob)%hcsin_a(iin)%hmet(imetal), obcs(iob)%hcsin_a(iin)%salt(isalt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `obcs(iob)%hcsin_m(iin)` | After each daily block, before monthly output; unconditional on print flags once the daily section executes. | `obcs(iob)%hcsin_m(iin)` is incremented by the current day's constituent-input summary, turning month-to-date totals into the sum of all daily values seen so far in the month. |
| `obcs(iob)%hcsin_y(iin)` | After the monthly section, before yearly output; executed whenever the routine reaches the yearly-accumulation line. | `obcs(iob)%hcsin_y(iin)` is incremented by the current month's accumulated summary, so it stores the running year-to-date total used for year-end reporting. |
| `obcs(iob)%hcsin_a(iin)` | After the yearly section, before average-annual output; executed whenever the routine reaches the annual-accumulation line. | `obcs(iob)%hcsin_a(iin)` is incremented by the current year's accumulated summary, so it preserves the simulation-long total used for the final average-annual report. |
| `ob(iob)%hin_a(iin)` | At simulation end when `time%end_sim == 1` and `pco%hyd%a == "y"`. | `ob(iob)%hin_a(iin)` is divided by `time%yrs_prt` to convert the stored total into an average annual hydrograph value before the final average-annual constituent records are written. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f as a new `hcsin_output` subroutine that loops over objects and receiving hydrographs and writes daily, monthly, yearly, and average-annual constituent-input summaries. The later 39fabde commit initialized the loop counters to zero in the source file, and 2fe89fd changed the CSV-format writes from `G0.3` to `G0.6` across the output families. The 94b6dec snapshot records the same structure as the initial addition.

- df07e3f added the full `hcsin_output` routine with its object/receiver loops, time-gated output branches, and accumulation of daily values into monthly, yearly, and annual summary states.
- 39fabde changed only the local counter declarations by initializing `iin`, `ipest`, `ipath`, `imetal`, `isalt`, and `iob` to zero; the reporting logic remained the same.
- 2fe89fd increased CSV output precision for the `write` statements from `G0.3` to `G0.6` so comma-separated exports preserve more numeric detail.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hcsin_output' has no extracted documentation comment.
