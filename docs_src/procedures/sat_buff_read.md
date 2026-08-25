---
kind: procedure
symbol: sat_buff_read
title: sat_buff_read
status: filled
source_hash: 86522ec60ac90eae
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard title/label lines from `satbuffer.str`
    during the initial scan and the rewind/read pass.
  header: Scratch character buffer used to read and discard the header line from `satbuffer.str`
    before the actual buffer records are processed.
  eof: I/O status flag from `read(..., iostat=eof)`; it is used both to detect end-of-file
    and to stop reading when the file is exhausted.
  imax: Counts how many saturated buffer records are present in `satbuffer.str`; it later
    sets the allocation size for `satbuff_db` and the stored database count.
  i_exist: Logical file-existence flag from `inquire(file=..., exist=i_exist)` that controls
    whether the routine processes `satbuffer.str` at all.
  msno: Initialized local integer that is not used in the extracted source body.
  ibuff: Loop counter over saturated buffer database records and the index used to access
    `satbuff_db` entries.
  idb: Loop counter over flow-control decision tables; used to search `dtbl_flo` for a matching
    table name.
  hru_src: Holds the source-HRU index read from each saturated buffer record so the routine
    can copy the record into that HRU's saturated-buffer state.
  hru_rcv: Holds the receiving-HRU index read from each saturated buffer record so the routine
    can copy the record into that HRU's saturated-buffer state.
uses:
  input_file_module: This module supplies the file-access control used by `inquire(file=...,
    exist=i_exist)` so the routine can skip all reading work when `satbuffer.str` is not present.
  maximum_data_module: '`maximum_data_module` provides `db_mx`, which holds the global database-size
    counters for SWAT+ input tables. `sat_buff_read` uses `db_mx%dtbl_flo` to bound the decision-table
    search and writes `db_mx%sat_buff` so later code knows how many saturated buffer records
    were loaded.'
  hru_module: '`hru_module` defines both the `satbuff_db` array being populated and the `hru`
    array that receives copied saturated-buffer settings. The routine needs these structures
    to move each record from file storage into the source and receiving HRU records and to
    store the resolved decision-table index on the source HRU.'
  conditional_module: '`conditional_module` provides `dtbl_flo`, the flow-control decision-table
    database. `sat_buff_read` compares each buffer record''s `flocon_dtbl` name against `dtbl_flo(idb)%name`
    so it can translate a table name into the numeric index stored on the source HRU.'
---

<!-- facts:header -->

Reads the saturated buffer database from `satbuffer.str` and loads the records into SWAT+ HRU state. It also crosswalks each buffer record to the corresponding flow-control decision table and stores the total record count.

## Bottom Line

`sat_buff_read` is a database loader for saturated buffer definitions. It checks whether `satbuffer.str` exists, scans the file to count buffer records, allocates `satbuff_db`, then reads each record into memory.

After loading the records, it copies each saturated buffer definition into the source HRU and receiving HRU state (`hru(... )%sb%sb_db`) and resolves the flow-control decision table name to an index in `hru(hru_src)%sb%dtbl`. The routine finishes by storing the total number of saturated buffer records in `db_mx%sat_buff`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after other structural-operation files are read and before plant-community and later management databases are loaded. Its results matter later because HRU saturated-buffer settings and the stored count in `db_mx%sat_buff` are used by the model after database setup is complete.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the buffer file exists | The routine tests for `satbuffer.str` with `inquire(file="satbuffer.str", exist=i_exist)` and only enters the reading logic if the file is present. |
| 2. Open the file and scan its records | It opens unit 107 on `satbuffer.str`, reads and discards the title/header records, then loops through the remaining records to count how many saturated-buffer entries exist by incrementing `imax`. |
| 3. Rewind and prepare for the load pass | After counting, it rewinds unit 107, rereads the title and header records, and allocates `satbuff_db(0:imax)` so there is storage for every buffer record. |
| 4. Read each saturated-buffer record | The routine loops from `ibuff = 1` to `imax` and reads each saturated-buffer database record directly into `satbuff_db(ibuff)`. |
| 5. Copy database records into HRU state and resolve decision tables | For each buffer record, it copies the record into the source and receiving HRU saturated-buffer state, then searches `dtbl_flo` for a matching `flocon_dtbl` name and stores the matching index in `hru(hru_src)%sb%dtbl`. |
| 6. Close the file and store the total count | After the loop finishes, it closes unit 107 and saves the number of loaded saturated-buffer records in `db_mx%sat_buff` before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module state` | `if(i_exist)` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dtbl_flo, db_mx%sat_buff` |
| [sym:hru_module] | `satbuff_db, hru` | `satbuff_db(ibuff)%hru_src, hru(hru_src)%sb%sb_db, satbuff_db(ibuff)%hru_rcv, hru(hru_rcv)%sb%sb_db, satbuff_db(ibuff)%flocon_dtbl, hru(hru_src)%sb%dtbl` |
| [sym:conditional_module] | `dtbl_flo` | `dtbl_flo(idb)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(hru_src)%sb%sb_db` | When `satbuff_db(ibuff)` has been read and its `hru_src` index is available inside the `do ibuff = 1, imax` loop. | The source HRU's saturated-buffer database copy is overwritten with the record just read from `satbuffer.str`, so that HRU carries the loaded buffer definition in its local `sb%sb_db` state. |
| `hru(hru_rcv)%sb%sb_db` | When `satbuff_db(ibuff)` has been read and its `hru_rcv` index is available inside the `do ibuff = 1, imax` loop. | The receiving HRU's saturated-buffer database copy is overwritten with the same loaded record, giving the buffer HRU access to the shared saturated-buffer parameters. |
| `hru(hru_src)%sb%dtbl` | When the record's `flocon_dtbl` name matches `dtbl_flo(idb)%name` during the decision-table search loop. | The source HRU's saturated-buffer decision-table index is set to the matching `dtbl_flo` entry so later model logic can use a numeric table reference instead of a character name. |
| `db_mx%sat_buff` | After the file has been processed, just before the subroutine returns. | The global saturated-buffer database count is stored in `db_mx%sat_buff`, making the loaded record total available to later initialization and model code. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `sat_buff_read`. Commit 1807dbb added the subroutine as a new file and implemented the full read-count-allocate-load-copy workflow for `satbuffer.str`. Commit bd18ad4 later inserted the `external :: smp_buffer` declaration near the top of the routine without changing the file-reading logic.

- 1807dbb introduced `sat_buff_read` and its core behavior: file existence check, two-pass scan of `satbuffer.str`, allocation of `satbuff_db`, transfer of each record into HRU state, decision-table name-to-index lookup, and storing the final record count in `db_mx%sat_buff`.
- bd18ad4 added `external :: smp_buffer` to the routine's declarations; the diff shows no other behavioral change in the file.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sat_buff_read' has no extracted documentation comment.
- The source declares `external :: smp_buffer`, but no call or use of `smp_buffer` is visible in the extracted body; its purpose is uncertain from this snippet.
