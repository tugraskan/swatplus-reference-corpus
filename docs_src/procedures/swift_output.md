---
kind: procedure
symbol: swift_output
title: swift_output
status: filled
source_hash: 97ee4a7ec1d41e08
version_label: SWAT+ 62.0.0
locals:
  iaqu: Loop index for aquifer delivery-ratio records; it is set from 1 to `sp_ob%aqu` when
    writing `aqu_dr.swf`.
  icha: Loop index for SWAT-deg channel records; it tracks the current channel entry while
    writing channel data and delivery-ratio files.
  ires: Loop index for reservoir or wetland records; it is reused both for wetland HRU lookup
    and for reservoir data/delivery-ratio output loops.
  ihyd: Hydrograph-component index within HRU, channel, aquifer, or object output arrays;
    it selects which averaged hydrograph slot to write or convert.
  idat: Intermediate lookup index for `sd_dat`; it holds the SWAT-deg datafile pointer used
    to reach the channel hydraulic record.
  idb: Intermediate lookup index for `sd_chd`; it resolves the hydraulic channel record selected
    through `sd_dat(idat)%hyd`.
  iobj_out: Loop index over `ob_out` entries when writing object print output files.
  irec: Loop index over recall database entries while writing `recall.swf` and the individual
    recall output files.
  iob: Resolved object number for an object print output entry; it is taken from `ob_out(iobj_out)%objno`
    and used to access `ob(iob)%hd_aa`.
  i: Generic loop counter used to walk the fixed `file_list` of SWAT input files to copy into
    the SWIFT folder.
  ifile: Constant count of SWAT input files to copy; it is 14, matching the entries loaded
    into `file_list`.
  folderpath: Temporary string holding the `SWIFT` directory name before the `mkdir` command
    is assembled.
  command: Shell command string passed to `SYSTEM` to create the `SWIFT` directory if it does
    not already exist.
  file_list: Fixed list of 14 SWAT input filenames that are copied into the SWIFT folder before
    the SWIFT files are written.
  i_exist: Logical flag set by `inquire` to indicate whether `SWIFT/file_cio.swf` already
    exists; it controls whether the directory-creation command is issued.
uses:
  hydrograph_module: 'The hydrograph module supplies the basin and object hydrograph structures
    that `swift_output` reads, converts, and writes: spatial counts (`sp_ob`, `sp_ob1`), hydrograph
    totals (`hd_tot`, `ht5`, `rec_a`), object connectivity (`ob`), and the SWIFT header layouts
    (`hru_swift_hdr`). These values determine how many rows are written, how outputs are labeled,
    and which averaged hydrograph values are exported.'
  hru_module: The HRU module provides the HRU list, land-use code, slope, object mapping,
    annual precipitation accumulation, and surface-storage pointer that appear in the HRU
    and wetland SWIFT files. `swift_output` uses this module to print HRU metadata and to
    decide whether an HRU has wetland storage that should be written to `hru_wet.swf`.
  soil_module: The soil module matters because the HRU data file writes the hydrologic soil
    group for each HRU. That field is part of the SWIFT HRU summary and is read directly from
    `soil(ihru)%hydgrp`.
  output_landscape_module: The output-landscape module matters because it provides the object-output
    list that drives the final `object_prt.swf` loop. Those records tell `swift_output` which
    object file name to use, which object to read from `ob`, and which hydrograph slot to
    average and export.
  reservoir_data_module: The reservoir data module supplies the wetland and reservoir descriptor
    tables that determine which hydrologic pointers and principal/emergency spillway parameters
    are written. `swift_output` uses wetland pointers for HRU wetland rows and reservoir geometry
    fields for `res_dat.swf`.
  maximum_data_module: The maximum-data module provides the counts that bound the weather-station
    and recall loops. Without `db_mx%wst` and `db_mx%recalldb_max`, `swift_output` would not
    know how many weather rows or recall entries to write.
  climate_module: The climate module provides the weather-station list and the annual precipitation
    and PET accumulators that are averaged and exported to `precip.swf`.
  aquifer_module: The aquifer module is imported because `swift_output` writes `aqu_dr.swf`,
    which is part of the SWIFT aquifer output set. The packet does not resolve a concrete
    aquifer symbol use in the visible source, so the module matters here mainly as the declared
    dependency for aquifer-related SWIFT output generation.
  input_file_module: The input-file module supplies the filenames for the SWAT input and connection
    files that are copied into the SWIFT folder and then listed in `file_cio.swf`. Those names
    are the source paths for the copied control and connectivity files.
  sd_channel_module: The SWAT-deg channel module provides the hydraulic-channel file pointers
    and channel definitions used to build `chan_dat.swf`. `swift_output` uses the `sd_dat`
    to reach the correct channel record in `sd_chd` and then writes that record to the SWIFT
    channel file.
  time_module: The time module matters because `yrs_print` is used to normalize accumulated
    annual values before they are written to SWIFT average-annual files. It controls the conversion
    from accumulated totals to per-year averages in `precip.swf`, `hru_exco.swf`, and the
    object-output file.
  recall_module: The recall module supplies the recall database metadata and file names that
    drive both the summary `recall.swf` listing and the per-recall output files. `swift_output`
    uses these records to create a master recall index and then write each annual recall file
    using the configured name and constituent descriptors.
---

<!-- facts:header -->

Builds the SWIFT file index and writes SWIFT-format basin, HRU, channel, reservoir, aquifer, recall, and object-output files from model state.

## Bottom Line

`swift_output` prepares a SWIFT output folder and writes the control file `file_cio.swf` plus the SWIFT input/output files that describe basin metadata, weather summaries, HRU properties, export coefficients, wetlands, channels, aquifers, reservoirs, recall files, and object print files.

It also converts selected hydrograph totals from mass to concentration form before writing them, and it normalizes annual weather and output values by `yrs_print` so the SWIFT files contain average-annual summaries.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`swift_output` runs after model state has been accumulated into annual summary arrays and file-name metadata are available from the input-file modules. It prepares the SWIFT folder, copies the required SWAT input files into it, and writes the SWIFT summary/output files that later SWIFT workflows and postprocessing expect to find.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Ensure the SWIFT folder exists and write the SWIFT control index. | The routine checks whether `SWIFT/file_cio.swf` exists and, if not, creates the `SWIFT` directory with `SYSTEM('mkdir SWIFT')`. It then opens `SWIFT/file_cio.swf` and writes the basin, climate, connection, channel, reservoir, routing-unit, HRU, recall, aquifer, and LS-unit file-name entries before closing the control file. |
| 2. Copy the listed SWAT input files into the SWIFT folder. | It builds `file_list` from the configured input-file names and loops over the 14 entries, calling `copy_file` to create `SWIFT/` copies of each source file. |
| 3. Write annual weather-station precipitation and PET summaries. | It opens `SWIFT/precip.swf`, writes the basin name and station count, prints a header, divides each station's accumulated annual precipitation and PET by `yrs_print`, and writes one summary row per weather station before closing the file. |
| 4. Write HRU metadata for SWIFT. | It opens `SWIFT/hru_dat.swf`, writes the basin name and HRU count, prints the HRU table headings, and then writes one row per HRU with the object name, land-use/management code, slope, hydrologic soil group, and placeholder null fields. |
| 5. Write HRU export-coefficient summaries. | It opens `SWIFT/hru_exco.swf`, writes the basin name and HRU count, prints SWIFT hydrograph labels and units, then loops over HRUs. For each HRU it resolves the command-object index, allocates `wyld_rto`, converts hydrograph masses to concentrations when flow exists, computes runoff-to-precipitation ratios, writes the average-annual export-coefficient row, and deallocates `wyld_rto`. |
| 6. Write HRU wetland inputs where surface storage exists. | It opens `SWIFT/hru_wet.swf`, writes the basin name and HRU count, prints wetland labels and units, and then writes one record for each HRU whose `dbs%surf_stor` pointer is positive by looking up the wetland hydrology record through `wet_dat(ires)%hyd` and writing the corresponding spillway fractions and depths from `wet_hyd`. |
| 7. Write SWAT-deg channel hydraulic data. | It opens `SWIFT/chan_dat.swf`, writes the basin name and SWAT-deg channel header, then loops over `sp_ob%chandeg` to resolve each channel's data record through `ob(icmd)%props` and `sd_dat(idat)%hyd`, and writes the selected `sd_chd` entry before closing the file. |
| 8. Write channel delivery ratios and hydrograph totals. | It opens `SWIFT/chan_dr.swf`, writes the basin name, channel count, headers, and units, then loops over channels. For each channel it combines the outgoing and incoming hydrograph totals into `ht5`, forces the flow and transport ratios used by SWIFT, and writes the averaged flow and constituent values to the channel-delivery file. |
| 9. Write aquifer delivery ratios. | It opens `SWIFT/aqu_dr.swf`, writes the basin name and aquifer count, prints the aquifer headers and units, then loops over aquifers, combines the aquifer hydrograph totals into `ht5`, and writes the averaged flow and constituent values for each aquifer record before closing the file. |
| 10. Write reservoir geometry and reservoir delivery ratios. | It writes `SWIFT/res_dat.swf` with basin name, reservoir count, and reservoir geometry table rows from `res_hyd`, then writes `SWIFT/res_dr.swf` with basin name, reservoir count, headers, and one averaged reservoir delivery-ratio row per reservoir using the combined hydrograph totals from `ob(icmd)`. |
| 11. Write the recall index and each recall file. | It opens `SWIFT/recall.swf`, writes a header, and loops over the recall database entries. For each entry it writes the recall metadata row to the index file, opens the corresponding per-recall file named by `recall_db(irec)%name`, writes the annual recall header and averaged constituent row from `rec_a`, closes the per-file output, and then closes the recall index when all entries are finished. |
| 12. Write average-annual object output files. | It loops over the object-output list, opens `SWIFT/object_prt.swf`, writes the file header, resolves the object number and hydrograph slot from `ob_out`, divides the selected hydrograph totals by `yrs_print`, and writes one annual object-output row before closing the file. After the loop it closes unit 107. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, ob, hru_swift_hdr, hd_tot, wyld_rto, sp_ob1, ht5, rec_a` | `sp_ob%hru, ob(ihru)%name, hru_swift_hdr%hd_type(ihyd), hru_swift_hdr%exco, hd_tot%hru, hru_swift_hdr%exco_unit, ob(icmd)%hd_aa(ihyd)%flo, ob(icmd)%hd_aa(ihyd), ob(icmd)%hd_aa(ihyd)%orgn, ob(icmd)%hd_aa(ihyd)%sedp, ob(icmd)%hd_aa(ihyd)%no3, ob(icmd)%hd_aa(ihyd)%solp, ob(icmd)%hd_aa(ihyd)%nh3, ob(icmd)%hd_aa(ihyd)%no2, sp_ob%chandeg, sp_ob1%chandeg, ob(icmd)%props, hru_swift_hdr%dr, hru_swift_hdr%dr_unit, ob(icmd)%hout_tot, ob(icmd)%hin_tot, ht5%flo, ht5%sed, ht5%orgn, ht5%sedp, ht5%nh3, ht5%no2, ht5%no3, ht5%solp, sp_ob%aqu, sp_ob1%aqu, sp_ob%res, sp_ob1%res, ob(icmd)%name, rec_a(irec)%flo, rec_a(irec)%sed` |
| [sym:hru_module] | `hru` | `hru(ihru)%land_use_mgt_c, hru(ihru)%topo%slope, hru(ihru)%obj_no, hru(ihru)%precip_aa, hru(ihru)%dbs%surf_stor` |
| [sym:soil_module] | `soil` | `soil(ihru)%hydgrp` |
| [sym:output_landscape_module] | `ob_out` | `ob_out(iobj_out)%filename, ob_out(iobj_out)%name, ob_out(iobj_out)%objno, ob_out(iobj_out)%hydno` |
| [sym:reservoir_data_module] | `wet_dat, wet_hyd, res_hyd` | `wet_dat(ires)%hyd, wet_hyd(ihyd)%psa, wet_hyd(ihyd)%pdep, wet_hyd(ihyd)%esa, wet_hyd(ihyd)%edep, res_hyd(ires)%name, res_hyd(ires)%psa, res_hyd(ires)%pvol, res_hyd(ires)%esa, res_hyd(ires)%evol` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wst, db_mx%recalldb_max` |
| [sym:climate_module] | `wst` | `wst(iwst)%precip_aa, wst(iwst)%pet_aa, wst(iwst)%name` |
| [sym:aquifer_module] | `gwflow_aquifer, gwflow_aquifer_state` | `No aquifer-module candidate reference was resolved in the packet for this routine.` |
| [sym:input_file_module] | `in_sim, in_con, in_ru, in_regs` | `in_sim%object_cnt, in_sim%object_prt, in_sim%cs_db, in_con%hru_con, in_con%ru_con, in_con%aqu_con, in_con%chandeg_con, in_con%res_con, in_con%rec_con, in_con%out_con, in_ru%ru_def, in_ru%ru_ele, in_regs%def_lsu, in_regs%ele_lsu` |
| [sym:sd_channel_module] | `sd_dat, sd_chd` | `sd_dat(idat)%hyd, sd_chd(idb)%name` |
| [sym:time_module] | `time-based summary state, yrs_print` | `yrs_print` |
| [sym:recall_module] | `recall_db` | `recall_db(irec)%org_min%name, recall_db(irec)%org_min%units, recall_db(irec)%org_min%tstep, recall_db(irec)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%precip_aa` | When `SWIFT/precip.swf` is written for each weather station in the `do iwst = 1, db_mx%wst` loop. | `wst(iwst)%precip_aa` is replaced with the average annual precipitation by dividing the accumulated value by `yrs_print`, so the value written to the SWIFT precipitation file is annualized rather than cumulative. |
| `wst(iwst)%pet_aa` | When `SWIFT/precip.swf` is written for each weather station in the `do iwst = 1, db_mx%wst` loop. | `wst(iwst)%pet_aa` is replaced with the average annual potential evapotranspiration by dividing the accumulated value by `yrs_print`, so the value written to the SWIFT precipitation file is annualized rather than cumulative. |
| `icmd` | When processing each HRU in the `do ihru = 1, sp_ob%hru` loops that write HRU export coefficients and wetland data. | `icmd` is set from the current HRU's object number or the current HRU's surface-storage-linked record so the routine can locate the associated object-connectivity hydrographs and wetland metadata before writing SWIFT outputs. |
| `ob(icmd)%hd_aa(ihyd)` | When writing HRU export coefficients for each hydrograph component in the `do ihyd = 1, hd_tot%hru` loop. | `ob(icmd)%hd_aa(ihyd)` is converted to concentration form in place when flow is present, so the exported hydrograph values match SWIFT's concentration-based file format. |
| `wyld_rto(ihyd)` | When writing HRU export coefficients for each hydrograph component in the `do ihyd = 1, hd_tot%hru` loop. | `wyld_rto(ihyd)` is assigned the runoff-to-precipitation ratio for the current HRU and hydrograph component, so SWIFT receives the average annual yield ratio alongside constituent concentrations. |
| `ht5` | When writing channel, aquifer, and reservoir delivery-ratio files in the loops over `icha` and `ires`. | `ht5` is set to the combined outgoing plus incoming hydrograph total for the current object, so the file records are based on net average-annual transport through each object. |
| `ht5%flo` | After `ht5 = ob(icmd)%hout_tot // ob(icmd)%hin_tot` in the channel-delivery loop. | `ht5%flo` is forced to 1.0 to represent the SWIFT delivery-ratio convention for flow in the channel-delivery file. |
| `ht5%sed` | After `ht5 = ob(icmd)%hout_tot // ob(icmd)%hin_tot` in the channel-delivery loop. | `ht5%sed` is forced to 1.0 so sediment delivery is written as a normalized SWIFT delivery ratio rather than the raw combined hydrograph value. |
| `ht5%orgn` | After `ht5 = ob(icmd)%hout_tot // ob(icmd)%hin_tot` in the channel-delivery loop. | `ht5%orgn` is forced to 1.0 so organic nitrogen delivery is written as a normalized SWIFT delivery ratio. |
| `ht5%sedp` | After `ht5 = ob(icmd)%hout_tot // ob(icmd)%hin_tot` in the channel-delivery loop. | `ht5%sedp` is forced to 1.0 so organic phosphorus delivery is written as a normalized SWIFT delivery ratio. |
| `ht5%nh3` | After `ht5 = ob(icmd)%hout_tot // ob(icmd)%hin_tot` in the channel-delivery loop. | `ht5%nh3` is forced to 1.0 so ammonia delivery is written as a normalized SWIFT delivery ratio. |
| `ht5%no2` | After `ht5 = ob(icmd)%hout_tot // ob(icmd)%hin_tot` in the channel-delivery loop. | `ht5%no2` is forced to 1.0 so nitrite delivery is written as a normalized SWIFT delivery ratio. |
| `ob(iob)%hd_aa(ihyd)` | When writing annual object output files in the `do iobj_out = 1, mobj_out` loop. | `ob(iob)%hd_aa(ihyd)` is divided by `yrs_print` in place so the object print file contains average annual hydrograph values instead of cumulative totals. |

## File I/O

<!-- facts:io -->


## Lineage

`swift_output.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 15 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `swift_output.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `3d7fcfb` (2025-10-08) — Updates to utils.f90 to have a flag to print out stack trace or not. Multple changes to get NAM data set to run using gfortran compiled exec…
- `ee1b472` (2024-10-10) — Refactor and enhance residue decomposition and output
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'swift_output' has no extracted documentation comment.
- output_landscape_module is imported, but the provided packet resolves no concrete outside references to it for this routine.
- aquifer_module is imported, but the provided packet resolves no concrete outside references to it for this routine.
- time_module is imported, but the provided packet resolves no concrete outside references to it for this routine.
- algorithm_steps revised: merged and expanded the draft into 12 source-backed steps tied to visible line ranges.
- `swift_output` writes `SWIFT/res_dat.swf` and `SWIFT/res_dr.swf`; the draft text calling both reservoir outputs "reservoir delivery ratios" is only partly accurate because `res_dat.swf` carries reservoir geometry/metadata from `res_hyd`.
- `output_landscape_module` and `aquifer_module` appear only as imports in the provided evidence packet; no concrete symbols were resolved from them for this routine.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
