---
kind: procedure
symbol: mgt_read_mgtops
title: mgt_read_mgtops
status: filled
source_hash: b4d3eb86623b77f8
version_label: SWAT+ 62.0.0
locals:
  nops: '`nops` holds the number of scheduled operation records declared for the current management
    schedule while the file is being scanned and then read. In the first pass it is used to
    skip over the scheduled-operation lines so `imax` can count schedules correctly; in the
    second pass it drives allocation and reading of the `mgt_ops` array through `read_mgtops`.'
  titldum: '`titldum` is a throwaway character buffer for title and record-name fields read
    from `management.sch`. It absorbs the file''s title line and the leading string on schedule
    and operation records when the routine only needs the numeric counts or wants to skip
    a record.'
  header: '`header` stores the header line read near the top of `management.sch` in both passes.
    The routine reads it but does not interpret it further here; it is used as part of advancing
    past the file''s introductory lines before the schedule records are processed.'
  eof: '`eof` captures the IOSTAT status from reads so the routine can detect end-of-file
    and stop scanning or reading cleanly. A negative value is treated as EOF and exits the
    current loop or pass.'
  imax: '`imax` accumulates the number of management schedule records found in the file. After
    the scan pass completes, it is used to allocate `sched(0:imax)` and later copied to `db_mx%mgt_ops`.'
  i_exist: '`i_exist` records whether the configured management schedule file exists. The
    routine uses it, together with the filename string being non-''null'', to decide whether
    to allocate an empty schedule array or read the file.'
  iops: '`iops` is a loop counter used while scanning past the scheduled-operation records
    belonging to one management schedule. It advances through `nops` lines so the first-pass
    count reaches the next schedule header.'
  nauto: '`nauto` holds the number of automated operation records declared for the current
    schedule. The scan pass uses it to skip over the corresponding auto-operation lines, and
    the read pass uses it to size and fill the `auto_name` and `num_db` arrays.'
  iauto: '`iauto` is the loop index for automated operations within a schedule. It is used
    first to skip each auto record during the counting pass and then to read and possibly
    rewrite each `auto_name` entry during the load pass.'
  isched: '`isched` indexes the current schedule in the `sched` array during the second pass.
    Each iteration of the load pass fills one `sched(isched)` entry and then calls `read_mgtops`
    for that schedule.'
  m_autos: '`m_autos` caches `sched(isched)%num_autos` for the current schedule so the code
    can test for any automated operations and allocate the matching per-schedule arrays. It
    also serves as the loop bound when reading the automated-operation records.'
uses:
  input_file_module: '`in_lum%management_sch` supplies the path to the management schedule
    file that this routine opens and parses. Without the input-file module''s configured filename,
    the routine would not know which `management.sch`-style file to read.'
  maximum_data_module: '`db_mx%mgt_ops` is the shared counter that receives the final schedule
    count. The maximum-data module matters here because this routine determines the size of
    the management-schedule database and publishes that size for other code to use.'
  mgt_operations_module: '`sched` is the shared management-schedule array that this routine
    allocates and fills. Its members hold the schedule names, counts, automated-operation
    names, crop lists, and the `mgt_ops` array that later management code depends on.'
---

<!-- facts:header -->

Reads the management schedule file, counts management schedules, and loads each schedule's automated and scheduled operations into shared database state. It also records the total number of management schedules for later use by the model.

## Bottom Line

mgt_read_mgtops opens the management schedule file named by `in_lum%management_sch`, scans it once to count how many schedule records are present, allocates `sched` to that size, then rewinds and reads each schedule into `mgt_operations_module` state. While doing that, it also expands each schedule's automated-operation lists and hands the scheduled-operation records to `read_mgtops` for detailed decoding.

This routine matters because it builds the management schedule database used by later management execution. It also stores the total schedule count in `db_mx%mgt_ops`, which downstream code can use as the upper bound for management-schedule storage and iteration.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database/input initialization in `proc_db`, after other management-related readers and before structural-operation readers. It depends on `input_file_module` for the filename and on `mgt_operations_module` for the shared `sched` array; once it completes, later management execution can use the loaded schedules and `read_mgtops` can fill each schedule's detailed operation records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the management schedule file is available. | The routine uses `inquire` to test whether `in_lum%management_sch` exists and whether the filename is not the literal string `null`. If the file is missing or disabled, it allocates a minimal `sched(0:0)` array and skips reading. |
| 2. Open the file and scan its title and header. | The routine opens unit 107 on `management.sch`, reads and discards the title line, then reads the header line. EOF status is checked after each read so the scan stops cleanly if the file ends early. |
| 3. Count management schedules by walking the file. | Inside a loop, the routine reads each schedule summary line to get `nops` and `nauto`, skips that schedule's automated-operation lines and scheduled-operation lines, and increments `imax` once per schedule. This first pass determines how many schedules must be allocated. |
| 4. Allocate the schedule database. | After the scan completes, the routine allocates `sched(0:imax)` so there is one entry for each management schedule plus the zero index used by the type's storage convention. |
| 5. Rewind the file to begin the load pass. | The routine rewinds unit 107 and rereads the title and header lines to reset the file pointer before loading the actual schedule records. |
| 6. Read each schedule header into `sched`. | For each schedule index from 1 to `imax`, the routine reads the schedule name, scheduled-operation count, and automated-operation count into `sched(isched)`. These values initialize the per-schedule data structure. |
| 7. Allocate and read automated-operation names. | If a schedule has automated operations, the routine allocates `auto_name` and `num_db`, then reads each auto-operation name. For special generic records such as `pl_hv_summer1`, `pl_hv_winter1`, and `pl_hv_summer2`, it backspaces and rereads the line to capture crop names in `auto_crop` and sets `auto_crop_num`. |
| 8. Allocate scheduled-operation storage and delegate detailed reading. | The routine allocates the `mgt_ops` array for the current schedule using `num_ops`, then calls `read_mgtops(isched)` to fill the detailed management-operation records. |
| 9. Publish the total schedule count and close the file. | After loading is complete, the routine stores `imax` in `db_mx%mgt_ops` and closes unit 107 on `management.sch`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_lum` | `in_lum%management_sch` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%mgt_ops` |
| [sym:mgt_operations_module] | `sched` | `sched(isched)%name, sched(isched)%num_ops, sched(isched)%num_autos, sched(isched)%auto_name(m_autos), sched(isched)%num_db(m_autos), sched(isched)%auto_name(iauto), sched(isched)%auto_crop(1), sched(isched)%auto_crop_num, sched(isched)%auto_crop, sched(isched)%auto_crop(2)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sched(isched)%auto_name(iauto)` | When an automated-operation name is one of the generic plant/harvest table names and the record is reread after a backspace. | `sched(isched)%auto_name(iauto)` is replaced by the reread value from the same file line when the routine expands a generic auto-operation record to include crop information. This happens for the `pl_hv_summer1`, `pl_hv_winter1`, and `pl_hv_summer2` cases. |
| `sched(isched)%auto_crop_num` | When a generic auto-operation record is detected and the code allocates crop-name storage for it. | `sched(isched)%auto_crop_num` is set to 1 in the generic plant/harvest cases so the schedule knows a crop list is present. The value marks the number of crop entries associated with that auto-operation in this routine. |
| `db_mx%mgt_ops` | After the file scan finishes and `imax` holds the number of schedules found, including the empty-file case. | `db_mx%mgt_ops` receives the total number of management schedules loaded from the file. Other code can use this as the maximum count of management-operation database entries available from the management schedule input. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_read_mgtops.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_read_mgtops.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_mgtops' has no extracted documentation comment.
- algorithm_steps revised: condensed the original draft steps into the actual scan/load sequence visible in the source and added the explicit close/finalize step.
- The source allocates `sched(0:0)` when the file is missing or disabled, which leaves an empty placeholder schedule entry.
- The code sets `sched(isched)%auto_crop_num = 1` even after allocating `auto_crop(2)` for `pl_hv_summer2`; that value appears inconsistent with the array length, so the source should be treated as written without correction.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
