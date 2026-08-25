---
kind: procedure
symbol: basin_print_codes_read
title: basin_print_codes_read
status: filled
source_hash: 238ea9d046672b20
version_label: SWAT+ 62.0.0
locals:
  header: Scratch text buffer for section headers and other non-data lines read from `print.prt`;
    the routine uses it to step through the file structure and discard or inspect headings
    before reading the next settings record.
  titldum: Temporary title string for the first line of `print.prt`; it is read and then ignored
    as part of the file prologue handling.
  name: Holds the current print-object label read from `print.prt` in label-driven mode so
    the routine can dispatch to the matching `select case` branch.
  eof: I/O status flag for every `read` from unit 107; negative values terminate the current
    loop or abort the current pass when end-of-file is reached.
  i_exist: Stores the result of `inquire(file=in_sim%prt, exist=i_exist)` so the routine can
    decide whether the configured print file is available before attempting to read it.
  ii: Loop counter used when filling the allocatable annual-year list `pco%aa_yrs` from the
    print file.
  result: Holds the return value from `print_prt_error(name)` when a print object is duplicated;
    it is assigned for the side effect of invoking the error routine.
uses:
  input_file_module: The routine needs `in_sim%prt` to know which file to open for print-code
    input; without the configured filename it cannot load any of the basin output controls.
  basin_module: 'The `pco` state is the target of nearly every read in this routine: it stores
    the simulation-wide timing fields, the label-mode switch, and all per-object print intervals
    that control later output generation.'
  time_module: Current simulation year and run length are used to fill default start and end
    years when `pco%yrc_start` or `pco%yrc_end` is left unset in `print.prt`.
---

<!-- facts:header -->

Reads `print.prt` and populates basin print-code settings, including interval flags, start/end timing, and per-object output schedules.

## Bottom Line

This subroutine opens the simulation print-code file named by `in_sim%prt`, reads the basin print-control settings into `pco`, and then closes the file. It can parse either the older fixed-order `print.prt` layout or the newer label-driven layout selected by `pco%use_obj_labels`, and it fills the daily/annual timing controls plus the basin, region, LSU, HRU, routing-unit, salt, carbon, and gwflow print intervals.

It matters because `proc_bsn` calls it during basin setup, after time and basin parameters are read, so downstream output behavior depends on `pco` being populated correctly before simulation continues. The routine also enforces unique labeled objects with `print_prt_error`, and it supplies fallback timing defaults from the current simulation time when those fields are left unset.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin initialization inside `proc_bsn`, after basin parameters are read and defaults are applied but before carbon-related basin and layer readers. Its results determine which outputs are active, their print intervals, and the time window used by later output generation throughout the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the print-control file should be read | The routine inquires about `in_sim%prt` and enters the read loop when the file exists or the configured name is not the null placeholder. |
| 2. Open the print-control file and read the timing preamble | It opens unit 107 on `in_sim%prt`, reads the file title, section header, start/end timing fields, and average-annual count, and stops on end-of-file conditions. |
| 3. Allocate average-annual years and reread them if needed | When `pco%aa_numint` is positive, the routine allocates `pco%aa_yrs`, backs up one record, and rereads the count plus the year list; otherwise it allocates a one-element placeholder array. |
| 4. Read database and other basin-level output switches | The routine reads the database-output section, including `pco%csvout`, `pco%use_obj_labels`, and `pco%cdfout`, then reads the other basin output controls `pco%crop_yld`, `pco%mgtout`, `pco%hydcon`, and `pco%fdcout`. |
| 5. Enter the object-output section | It reads the object-output header and branches on `pco%use_obj_labels` to choose between fixed-order parsing and label-driven dispatch. |
| 6. Read fixed-order object intervals when labels are disabled | When labels are disabled, the routine reads the object records in a fixed sequence and fills basin, region, LSU, HRU, hru-lte, channel, aquifer, reservoir, recall, hydrologic, routing-unit, pesticide, salt, and constituent print intervals. |
| 7. Switch to label-driven parsing when labels are enabled | With label mode enabled, the routine reads object names one at a time, skips blank labels, and dispatches each nonblank name through `select case(name)`. |
| 8. Reject duplicates, reread the full record, and mark basin/region/water-allocation objects | Each basin, region, and water-allocation branch checks the corresponding `already_read_in` flag, calls `print_prt_error` on duplicates, backs up one record, rereads the interval fields, and sets the flag to true after successful consumption. |
| 9. Read LSU objects, including LSU carbon families | The LSU branches use the same duplicate-check, backspace, reread, and mark-read pattern for water, nutrient, loss, plant-weather, and carbon LSU print families. |
| 10. Read HRU objects and HRU carbon families | The routine dispatches the HRU branches for water, nutrient, loss, plant-weather, carbon, carbon-variable, carbon-global, carbon-transfer, carbon-layer, carbon-pool, carbon-npool, carbon-plant, carbon-flux, carbon-driver, carbon-dynamic, carbon-snapshot, and salt/constituent-related outputs, marking each family as read once consumed. |
| 11. Read hru-lte, channel, aquifer, reservoir, recall, hydrologic, routing-unit, pesticide, salt, constituent, and gwflow objects | The remaining labeled branches reread the full record for hru-lte, channel, aquifer, reservoir, recall, hydrologic, routing-unit, pesticide, salt, constituent, and gwflow families, then mark each corresponding `already_read_in` flag. |
| 12. Stop on invalid or duplicate labels, then close and finalize defaults | If a label is unknown the routine writes an error and stops; after processing it closes unit 107, fills unset timing defaults from `time`, and copies `pco%int_day` into `pco%int_day_cur`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_sim` | `in_sim%prt` |
| [sym:basin_module] | `pco` | `pco%nyskip, pco%day_start, pco%yrc_start, pco%day_end, pco%yrc_end, pco%int_day, pco%aa_numint, pco%aa_yrs, pco%aa_yrs(ii), pco%aa_yrs(1), pco%csvout, pco%use_obj_labels, pco%cdfout, pco%crop_yld, pco%mgtout, pco%hydcon, pco%fdcout, pco%wb_bsn%d, pco%wb_bsn%m, pco%wb_bsn%y, pco%wb_bsn%a, pco%nb_bsn%d, pco%nb_bsn%m, pco%nb_bsn%y, pco%nb_bsn%a, pco%ls_bsn%d, pco%ls_bsn%m, pco%ls_bsn%y, pco%ls_bsn%a, pco%pw_bsn%d, pco%pw_bsn%m, pco%pw_bsn%y, pco%pw_bsn%a, pco%aqu_bsn%d, pco%aqu_bsn%m, pco%aqu_bsn%y, pco%aqu_bsn%a, pco%res_bsn%d, pco%res_bsn%m, pco%res_bsn%y, pco%res_bsn%a, pco%chan_bsn%d, pco%chan_bsn%m, pco%chan_bsn%y, pco%chan_bsn%a, pco%sd_chan_bsn%d, pco%sd_chan_bsn%m, pco%sd_chan_bsn%y, pco%sd_chan_bsn%a, pco%recall_bsn%d, pco%recall_bsn%m, pco%recall_bsn%y, pco%recall_bsn%a, pco%wb_reg%d, pco%wb_reg%m, pco%wb_reg%y, pco%wb_reg%a, pco%nb_reg%d, pco%nb_reg%m, pco%nb_reg%y, pco%nb_reg%a, pco%ls_reg%d, pco%ls_reg%m, pco%ls_reg%y, pco%ls_reg%a, pco%pw_reg%d, pco%pw_reg%m, pco%pw_reg%y, pco%pw_reg%a, pco%aqu_reg%d, pco%aqu_reg%m, pco%aqu_reg%y, pco%aqu_reg%a, pco%res_reg%d, pco%res_reg%m, pco%res_reg%y, pco%res_reg%a, pco%sd_chan_reg%d, pco%sd_chan_reg%m` |
| [sym:time_module] | `time` | `time%yrc, time%nbyr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pco%wb_bsn%already_read_in` | When the label `basin_wb` is read in label-driven mode and `pco%wb_bsn%already_read_in` was false, the routine rereads the record and sets `pco%wb_bsn%already_read_in = .true.`. | This records that the basin water-balance print interval has been consumed from `print.prt`, so later duplicate labels can be rejected by `print_prt_error`. |
| `pco%nb_bsn%already_read_in` | When the label `basin_nb` is read in label-driven mode and `pco%nb_bsn%already_read_in` was false, the routine rereads the record and sets `pco%nb_bsn%already_read_in = .true.`. | This records that the basin nutrient-balance print interval has been consumed from `print.prt`, preventing a second `basin_nb` entry from being accepted. |
| `pco%ls_bsn%already_read_in` | When the label `basin_ls` is read in label-driven mode and `pco%ls_bsn%already_read_in` was false, the routine rereads the record and sets `pco%ls_bsn%already_read_in = .true.`. | This records that the basin losses print interval has been consumed from `print.prt`, so the same basin losses label cannot be processed twice. |
| `pco%pw_bsn%already_read_in` | When the label `basin_pw` is read in label-driven mode and `pco%pw_bsn%already_read_in` was false, the routine rereads the record and sets `pco%pw_bsn%already_read_in = .true.`. | This records that the basin plant-weather print interval has been consumed from `print.prt`, making the basin plant-weather branch idempotent across the file. |
| `pco%aqu_bsn%already_read_in` | When the label `basin_aqu` is read in label-driven mode and `pco%aqu_bsn%already_read_in` was false, the routine rereads the record and sets `pco%aqu_bsn%already_read_in = .true.`. | This records that the basin aquifer print interval has been consumed from `print.prt`, so a duplicate aquifer basin label is rejected later. |
| `pco%res_bsn%already_read_in` | When the label `basin_res` is read in label-driven mode and `pco%res_bsn%already_read_in` was false, the routine rereads the record and sets `pco%res_bsn%already_read_in = .true.`. | This records that the basin reservoir print interval has been consumed from `print.prt`, which the duplicate-check logic uses to prevent repeated reservoir labels. |
| `pco%chan_bsn%already_read_in` | When the label `basin_cha` is read in label-driven mode and `pco%chan_bsn%already_read_in` was false, the routine rereads the record and sets `pco%chan_bsn%already_read_in = .true.`. | This records that the basin channel print interval has been consumed from `print.prt`, so a second channel basin label cannot be accepted. |
| `pco%sd_chan_bsn%already_read_in` | When the label `basin_sd_cha` is read in label-driven mode and `pco%sd_chan_bsn%already_read_in` was false, the routine rereads the record and sets `pco%sd_chan_bsn%already_read_in = .true.`. | This records that the basin channel-lte print interval has been consumed from `print.prt`, which lets the routine detect duplicate sd-channel basin entries. |
| `pco%recall_bsn%already_read_in` | When the label `basin_psc` is read in label-driven mode and `pco%recall_bsn%already_read_in` was false, the routine rereads the record and sets `pco%recall_bsn%already_read_in = .true.`. | This records that the basin recall print interval has been consumed from `print.prt`, preventing repeated recall basin entries. |
| `pco%wb_reg%already_read_in` | When the label `region_wb` is read in label-driven mode and `pco%wb_reg%already_read_in` was false, the routine rereads the record and sets `pco%wb_reg%already_read_in = .true.`. | This records that the region water-balance print interval has been consumed from `print.prt`, so the reader can reject a duplicate region water-balance label. |
| `pco%nb_reg%already_read_in` | When the label `region_nb` is read in label-driven mode and `pco%nb_reg%already_read_in` was false, the routine rereads the record and sets `pco%nb_reg%already_read_in = .true.`. | This records that the region nutrient-balance print interval has been consumed from `print.prt`, which blocks a second region nutrient label. |
| `pco%ls_reg%already_read_in` | When the label `region_ls` is read in label-driven mode and `pco%ls_reg%already_read_in` was false, the routine rereads the record and sets `pco%ls_reg%already_read_in = .true.`. | This records that the region losses print interval has been consumed from `print.prt`, so duplicate region losses labels are detected. |
| `pco%pw_reg%already_read_in` | When the label `region_pw` is read in label-driven mode and `pco%pw_reg%already_read_in` was false, the routine rereads the record and sets `pco%pw_reg%already_read_in = .true.`. | This records that the region plant-weather print interval has been consumed from `print.prt`, allowing duplicate region plant-weather labels to be rejected. |
| `pco%aqu_reg%already_read_in` | When the label `region_aqu` is read in label-driven mode and `pco%aqu_reg%already_read_in` was false, the routine rereads the record and sets `pco%aqu_reg%already_read_in = .true.`. | This records that the region aquifer print interval has been consumed from `print.prt`, so the aquifer region label cannot be processed twice. |
| `pco%res_reg%already_read_in` | When the label `region_res` is read in label-driven mode and `pco%res_reg%already_read_in` was false, the routine rereads the record and sets `pco%res_reg%already_read_in = .true.`. | This records that the region reservoir print interval has been consumed from `print.prt`, which is used to reject duplicate reservoir region labels. |
| `pco%sd_chan_reg%already_read_in` | When the label `region_sd_cha` is read in label-driven mode and `pco%sd_chan_reg%already_read_in` was false, the routine rereads the record and sets `pco%sd_chan_reg%already_read_in = .true.`. | This records that the region channel-lte print interval has been consumed from `print.prt`, ensuring only one region sd-channel record is accepted. |
| `pco%recall_reg%already_read_in` | When the label `region_psc` is read in label-driven mode and `pco%recall_reg%already_read_in` was false, the routine rereads the record and sets `pco%recall_reg%already_read_in = .true.`. | This records that the region recall print interval has been consumed from `print.prt`, so repeated recall region entries are caught. |
| `pco%water_allo%already_read_in` | When the label `water_allo` is read in label-driven mode and `pco%water_allo%already_read_in` was false, the routine rereads the record and sets `pco%water_allo%already_read_in = .true.`. | This records that the water-allocation print interval has been consumed from `print.prt`, preventing a second water-allocation record from being processed. |
| `pco%wb_lsu%already_read_in` | When the label `lsunit_wb` is read in label-driven mode and `pco%wb_lsu%already_read_in` was false, the routine rereads the record and sets `pco%wb_lsu%already_read_in = .true.`. | This records that the LSU water-balance print interval has been consumed from `print.prt`, allowing later duplicate LSU water-balance labels to be rejected. |
| `pco%nb_lsu%already_read_in` | When the label `lsunit_nb` is read in label-driven mode and `pco%nb_lsu%already_read_in` was false, the routine rereads the record and sets `pco%nb_lsu%already_read_in = .true.`. | This records that the LSU nutrient-balance print interval has been consumed from `print.prt`, so a second LSU nutrient label is treated as a duplicate. |
| `pco%ls_lsu%already_read_in` | When the label `lsunit_ls` is read in label-driven mode and `pco%ls_lsu%already_read_in` was false, the routine rereads the record and sets `pco%ls_lsu%already_read_in = .true.`. | This records that the LSU losses print interval has been consumed from `print.prt`, which protects against duplicate LSU losses labels. |
| `pco%pw_lsu%already_read_in` | When the label `lsunit_pw` is read in label-driven mode and `pco%pw_lsu%already_read_in` was false, the routine rereads the record and sets `pco%pw_lsu%already_read_in = .true.`. | This records that the LSU plant-weather print interval has been consumed from `print.prt`, so a repeated LSU plant-weather label can be flagged. |
| `pco%cb_gl_lsu%already_read_in` | When the label `lsu_cb_gl` is read in label-driven mode and `pco%cb_gl_lsu%already_read_in` was false, the routine rereads the record and sets `pco%cb_gl_lsu%already_read_in = .true.`. | This records that the LSU carbon-global print interval has been consumed from `print.prt`, which is used to reject duplicates for that carbon family. |
| `pco%cb_trf_lsu%already_read_in` | When the label `lsu_cb_trf` is read in label-driven mode and `pco%cb_trf_lsu%already_read_in` was false, the routine rereads the record and sets `pco%cb_trf_lsu%already_read_in = .true.`. | This records that the LSU carbon-transfer print interval has been consumed from `print.prt`, so the same carbon-transfer LSU label is not processed twice. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The history shows an initial addition of the print-code reader and later changes that switched the routine to read individual interval fields instead of whole derived-type records, added `pco%use_obj_labels` to control label-driven parsing, fixed an annual-year reread bug with `backspace`, added LSU and HRU carbon-family print objects, corrected a misassigned `already_read_in` flag for `hru_cb_vars`, and changed duplicate-object handling from warning prints to an error stop.

- 5054b1f introduced label-driven parsing by reading `pco%use_obj_labels` and expanding the object section from fixed-order reads to `select case(name)` dispatch.
- d2e03ac changed every fixed-order and labeled object read to populate `d/m/y/a` fields explicitly, which fixed the skipped-lines bug caused by reading whole derived types.
- f66c8e6 added the `hru_cb_vars` label branch, but it incorrectly marked `pco%cb_hru%already_read_in` instead of the new carbon-variable flag.
- bc7755a added LSU carbon-family labels (`lsu_cb_gl`, `lsu_cb_trf`, `lsu_cb_plt`) and corrected the `hru_cb_vars` branch to set `pco%cb_vars_hru%already_read_in`.
- 74b595c made duplicate and invalid print-object labels fatal by replacing warning text with error output and `error stop`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_print_codes_read' has no extracted documentation comment.
