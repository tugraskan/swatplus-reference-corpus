---
kind: procedure
symbol: manure_allocation_read
title: manure_allocation_read
status: filled
source_hash: 0268ebd2ff9bd736
version_label: SWAT+ 62.0.0
locals:
  titldum: Title line read from `manure_allo.mnu` before the file's object data begins.
  header: Section header or separator line in `manure_allo.mnu`; used to skip over labeled
    blocks before reading the next data record.
  eof: I/O status flag for reads from unit 107; negative values end the file-processing loop
    and stop parsing.
  imax: Number of manure allocation objects declared in the file header; used to allocate
    `mallo(imax)` and stored in `db_mx%mallo_db`.
  i_exist: Logical file-existence flag from `inquire`; controls whether the routine reads
    `manure_allo.mnu` or creates a dummy zero-sized allocation array.
  i: Record counter read from the file for source and demand object blocks; used to assign
    the current object's `num` field before rereading the full record.
  k: Leading record field read and discarded as part of source/demand object lines; it appears
    to be an object index or sequence marker in the file format.
  isrc: Loop counter for source objects and also the source-count dimension used when allocating
    each demand object's withdrawal arrays.
  imro: Loop counter for manure allocation objects in `mallo`; identifies the current allocation
    object being populated.
  num_objs: Temporary count of how many source objects or demand objects to allocate for the
    current manure allocation object.
  itrn: Loop counter for demand objects within a manure allocation object; replaces the older
    `idmd` name in this routine.
  idb: Database index used for cross-walking manure names to fertilizer records and decision-table
    names to `dtbl_lum` entries.
  ihru: HRU index recovered from a demand object's `ob_num` when the demand object type is
    `hru`.
  idb_man: Database index used to cross-walk a decision-table action option to a chemical
    application operation in `chemapp_db`.
uses:
  input_file_module: This module provides the file-presence check that decides whether the
    routine should build a real manure allocation database or fall back to an empty placeholder
    array.
  manure_allocation_module: The `mallo` array is the central in-memory database being populated
    here. Its allocation sizes, object metadata, nested source/demand records, and cross-linked
    indices are all filled from the file contents.
  mgt_operations_module: '`chemapp_db` supplies the chemical application operation names used
    to translate a manure decision-table action option into the integer `app_method` code
    stored on each demand object.'
  maximum_data_module: '`db_mx` holds the maximum counts needed to size shared database arrays.
    This routine updates `mallo_db` from the file header and uses `fertparm`, `dtbl_lum`,
    and `chemapp_db` as loop bounds for name-to-index crosswalks.'
  hydrograph_module: The source uses `use hydrograph_module`, but no resolved symbols from
    that module are referenced in the extracted routine body, so its specific role here is
    uncertain.
  sd_channel_module: The source uses `use sd_channel_module`, but no resolved symbols from
    that module are referenced in the extracted routine body, so its specific role here is
    uncertain.
  conditional_module: The routine compares each demand object's decision-table name against
    `dtbl_lum(idb)%name`, then reads `dtbl_lum(idb)%act(1)%option` to identify the chemical
    application option tied to that decision table.
  hru_module: When a demand object targets an HRU, the routine writes the matched decision-table
    index into `hru(ihru)%man_trn_dtbl` so the HRU can later use the correct manure-transfer
    decision table during management operations.
---

<!-- facts:header -->

Reads the manure allocation configuration file and builds the in-memory manure allocation database. It also cross-walks manure sources, demand objects, decision tables, and HRU/application metadata to model database indices.

## Bottom Line

manure_allocation_read loads `manure_allo.mnu` into the shared `mallo` allocation array. It first sizes the allocation database from the file header, then reads each manure allocation object, its source objects, and its demand objects.

While loading demand objects, it resolves manure and decision-table names to database indices using `fertdb`, `dtbl_lum`, and `chemapp_db`. Those links let later manure allocation and HRU management routines refer to compact integer IDs instead of raw text names.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization, after the manure allocation input file has been prepared and before any management simulation that depends on manure allocation indices. Its outputs feed later allocation and HRU decision-table behavior, especially the manure application method and HRU transfer-table links.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and inspect the input file | Initialize local status variables, then check whether `manure_allo.mnu` exists. If the file is missing or disabled, allocate a placeholder `mallo(0:0)` array and skip parsing. |
| 2. Open the manure allocation file and read the file title and allocation count | Open unit 107 on `manure_allo.mnu`, read the title line, read the number of manure allocation objects, copy that count into `db_mx%mallo_db`, and allocate `mallo(imax)`. |
| 3. Loop over each manure allocation object | For each allocation object, skip a header line, read the object name, rule type, and source/demand counts, then allocate the `src` and `trn` arrays to match those counts. |
| 4. Read and index source objects | For each source object, read its sequence number, backspace the file, reread the full record, store moisture/manure/location/storage fields, and cross-walk the manure name to `fertdb(idb)` to set `fertdb`. |
| 5. Read and index demand objects | Read the demand-section header, then for each demand object allocate withdrawal arrays sized by the number of sources, read and store the demand object fields, and if the object type is `hru`, map its decision table and manure application metadata to database indices. |
| 6. Finish and close the file | Exit the allocation-object loop, close unit 107, and return to the caller with `mallo` and related database indices populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module state` | `inquire file existence on `manure_allo.mnu`` |
| [sym:manure_allocation_module] | `mallo` | `mallo(imro)%name, mallo(imro)%rule_typ, mallo(imro)%src_obs, mallo(imro)%trn_obs, mallo(imro)%src(num_objs), mallo(imro)%trn(num_objs), mallo(imro)%src(i)%num, mallo(imro)%src(i)%mois_typ, mallo(imro)%src(i)%manure_typ, mallo(imro)%src(i)%lat, mallo(imro)%src(i)%long, mallo(imro)%src(i)%stor_init, mallo(imro)%src(i)%stor_max, mallo(imro)%src(i)%prod_mon, mallo(imro)%src(i)%fertdb, mallo(imro)%trn(itrn)%withdr(isrc), mallo(imro)%trn(itrn)%withdr_m(isrc), mallo(imro)%trn(itrn)%withdr_y(isrc), mallo(imro)%trn(itrn)%withdr_a(isrc), mallo(imro)%trn(i)%num, mallo(imro)%trn(i)%ob_typ, mallo(imro)%trn(i)%ob_num, mallo(imro)%trn(i)%dtbl, mallo(imro)%trn(i)%right, mallo(imro)%trn(i)%dtbl_num, mallo(imro)%trn(itrn)%manure_amt%app_method` |
| [sym:mgt_operations_module] | `chemapp_db` | `chemapp_db(idb_man)%name` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%mallo_db, db_mx%fertparm, db_mx%dtbl_lum, db_mx%chemapp_db` |
| [sym:hydrograph_module] | `not resolved from the extracted source for this routine` |  |
| [sym:sd_channel_module] | `not resolved from the extracted source for this routine` |  |
| [sym:conditional_module] | `dtbl_lum` | `dtbl_lum(idb)%name, dtbl_lum(idb)%act(1)%option` |
| [sym:hru_module] | `hru` | `hru(ihru)%man_trn_dtbl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%mallo_db` | When the file is read and the first header count `imax` is accepted. | `db_mx%mallo_db` stores the number of manure allocation objects available in `manure_allo.mnu`, which later code can use as the maximum size of the manure allocation database. |
| `mallo(imro)%src(i)%num` | For each source-object record that is read successfully inside the `do isrc = 1, mallo(imro)%src_obs` loop. | `mallo(imro)%src(i)%num` is set to the source object's sequence number so later code can refer to the source record by its file order/index. |
| `mallo(imro)%src(i)%fertdb` | After reading a source object's manure type and finding a matching fertilizer-name entry in `fertdb`. | `mallo(imro)%src(i)%fertdb` stores the fertilizer database index corresponding to the source object's manure name, allowing later routines to use a numeric fertilizer reference. |
| `mallo(imro)%trn(i)%num` | For each demand-object record read in the `do itrn = 1, num_objs` loop. | `mallo(imro)%trn(i)%num` is set to the demand object's sequence number so the demand record can be addressed consistently by index. |
| `mallo(imro)%trn(i)%dtbl_num` | When a demand object's decision-table name matches an entry in `dtbl_lum`. | `mallo(imro)%trn(i)%dtbl_num` stores the matched decision-table index for later use in manure transfer logic. |
| `hru(ihru)%man_trn_dtbl` | When the demand object type is `hru` and its decision-table name matches `dtbl_lum(idb)%name`. | `hru(ihru)%man_trn_dtbl` is updated with the matching decision-table index so the target HRU knows which manure transfer decision table to use. |
| `mallo(imro)%trn(itrn)%manure_amt%app_method` | When the demand object type is `hru` and the decision-table action option matches a `chemapp_db` record. | `mallo(imro)%trn(itrn)%manure_amt%app_method` stores the chemical application operation index corresponding to the decision-table option, which later controls how manure is applied. |

## File I/O

<!-- facts:io -->


## Lineage

Three lineage commits were resolved for `manure_allocation_read`. The initial commit `df07e3f` added the routine and its file-reading/crosswalk logic. Commit `94b6dec` updated the implementation to use the then-current manure allocation structure names (`dmd` and `dmd_obs`) and kept the same overall parsing flow. Commit `39fabde` initialized local variables and added `source=0.` when allocating demand withdrawal arrays. Commit `914f365` renamed demand-object fields from `dmd`/`dmd_obs` to `trn`/`trn_obs`, changed the loop variable from `idmd` to `itrn`, and updated the read/assignment statements accordingly.

- df07e3f introduced the routine and established the file-driven allocation workflow: open `manure_allo.mnu`, read allocation headers, allocate source/demand arrays, cross-walk fertilizer and decision-table names, and close the file.
- 94b6dec preserved the same workflow while aligning the routine to the earlier manure-allocation type layout that used `dmd` and `dmd_obs`.
- 39fabde kept behavior the same but changed local initialization and zero-filled the allocated demand withdrawal arrays with `source = 0.`.
- 914f365 renamed the demand side of the manure allocation model from `dmd` to `trn`, including object count fields, loop variables, allocations, and field assignments.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'manure_allocation_read' has no extracted documentation comment.
- hydrograph_module and sd_channel_module are imported but no resolved symbols from those modules are used in the extracted routine body.
- lineage analysis resolved four commits affecting this routine: df07e3f, 94b6dec, 39fabde, and 914f365.
