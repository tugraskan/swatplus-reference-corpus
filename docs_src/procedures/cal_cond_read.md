---
kind: procedure
symbol: cal_cond_read
title: cal_cond_read
status: filled
source_hash: c68d4a8a91418252
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary holder for the first record in `scen_dtl.upd`, used to read and discard
    the file title line before the numeric content starts.
  header: Temporary holder for the header record in `scen_dtl.upd`, used to skip the descriptive
    header line before reading the conditional update rows.
  eof: IOSTAT status flag for `read` statements; negative values trigger `exit` when the file
    ends or a read fails.
  i_exist: Logical flag set by `inquire` to indicate whether `scen_dtl.upd` is present before
    the routine tries to read it.
  num_dtls: Stores the number of conditional update definitions declared in `scen_dtl.upd`
    and drives allocation and the main read loop.
  i: Loop counter over the conditional update definitions being loaded from the file.
  icond: Loop counter used to search the decision-table list for a name match to the current
    update entry.
uses:
  input_file_module: This module is imported by the routine and typically provides file-path
    or input-file control state. Even though no specific symbol was resolved here, it matters
    because the routine’s file-open decision depends on the broader input-file configuration
    and file-handling conventions established by that module.
  maximum_data_module: The routine writes `db_mx%cond_up` from the file’s declared count and
    uses `db_mx%dtbl_scen` as the upper bound when searching for a matching decision table
    name. That module supplies the shared maxima used to size and interpret the conditional-update
    database.
  calibration_data_module: The allocatable `upd_cond` array stores the conditional-update
    records read from `scen_dtl.upd`. Its components hold the maximum execution count, update
    type, decision-table name, and matched decision-table index that this routine populates.
  conditional_module: The routine compares each update entry’s `dtbl` name against `dtbl_scen(icond)%name`
    to resolve the decision-table pointer. This module matters because it contains the scenario
    decision-table catalog that `cal_cond_read` crosswalks into `upd_cond(i)%cond_num`.
---

<!-- facts:header -->

Reads the conditional update scenario file `scen_dtl.upd` and loads the conditional-update definitions into shared calibration state. It also crosswalks each update table name to the matching decision-table index in `dtbl_scen`.

## Bottom Line

`cal_cond_read` is a file reader for conditional calibration/update settings. It checks whether `scen_dtl.upd` exists, opens it, reads the file title, number of conditional update entries, and a header row, then loads each entry into `upd_cond`.

For each conditional update entry, the routine stores the maximum hit count, update type, and decision-table name. It then matches that name against `conditional_module%dtbl_scen(icond)%name` and saves the corresponding index in `upd_cond(i)%cond_num`, so later update logic can find the referenced decision table quickly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during setup of calibration/conditional-update inputs, after the scenario update file name has been established and before any conditional updates are executed. Its results are later used by the conditional calibration machinery to schedule updates and resolve each update entry to the correct decision table in the scenario decision-table list.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the update file is usable | Resets the record counter, checks whether `scen_dtl.upd` exists, and if the file is missing or disabled (`'null'`), allocates a one-element placeholder `upd_cond(0:0)` and stops reading real content. |
| 2. Open the conditional-update file and read title/count records | Opens unit 107 on `scen_dtl.upd`, reads the title line into `titldum`, and reads the declared number of update definitions into `num_dtls`, exiting early if input ends unexpectedly. |
| 3. Size the shared conditional-update array and publish the count | Allocates `upd_cond(0:num_dtls)` so the shared update array has one slot per file entry and stores the count in `db_mx%cond_up` for later model use. |
| 4. Skip the descriptive header line | Reads the header record into `header` and exits if the file ends before the data section begins. |
| 5. Load each conditional-update definition | Loops from 1 to `num_dtls` and reads each row’s `max_hits`, `typ`, and `dtbl` fields into `upd_cond(i)`, stopping if a read fails. |
| 6. Crosswalk each update table name to a scenario decision table | For each update entry, searches the `dtbl_scen` list until `upd_cond(i)%dtbl` matches `dtbl_scen(icond)%name`, then stores the matching index in `upd_cond(i)%cond_num` and exits the search loop. |
| 7. Exit the file-processing loop and return | Leaves the open-ended `do` after one successful pass through the file and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module state for file-path/availability context` | `No resolved component reference from this module was extracted in the packet.` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cond_up, db_mx%dtbl_scen` |
| [sym:calibration_data_module] | `upd_cond` | `upd_cond(i)%max_hits, upd_cond(i)%typ, upd_cond(i)%dtbl, upd_cond(i)%cond_num` |
| [sym:conditional_module] | `dtbl_scen` | `dtbl_scen(icond)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cond_up` | When `scen_dtl.upd` is present and the routine successfully reads `num_dtls`. | `db_mx%cond_up` is set to the number of conditional update definitions declared in the file so later code knows how many conditional updates are available. |
| `upd_cond(i)%cond_num` | For each `i` whose `upd_cond(i)%dtbl` matches some `dtbl_scen(icond)%name` during the search loop. | `upd_cond(i)%cond_num` is assigned the matched decision-table index, linking the file entry to the scenario decision-table catalog. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed revisions were resolved. The initial `df07e3f` add introduced `cal_cond_read` with file checking, file reads, allocation of `upd_cond`, and the decision-table crosswalk. The `39fabde` revision changed the local scalar initializations to `""` or `0` and left the reading logic unchanged. The `889136d` revision corrected a typo in the documentation comment from "paramter" to "parameter" without changing executable behavior.

- df07e3f established the full routine behavior: detect `scen_dtl.upd`, read the title/count/header, allocate `upd_cond`, store `db_mx%cond_up`, and map each `upd_cond(i)%dtbl` to `upd_cond(i)%cond_num` via `dtbl_scen`.
- 39fabde only initialized `titldum`, `header`, `eof`, `num_dtls`, `i`, and `icond` at declaration time; the file-processing algorithm remained the same.
- 889136d changed only a comment typo in the purpose text and did not alter runtime logic.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cal_cond_read' has no extracted documentation comment.
