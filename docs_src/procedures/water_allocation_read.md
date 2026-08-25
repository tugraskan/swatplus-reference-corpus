---
kind: procedure
symbol: water_allocation_read
title: water_allocation_read
status: filled
source_hash: 7270edde04df1715
version_label: SWAT+ 62.0.0
locals:
  titldum: Title line read from the top of the water-allocation input file before the object
    count; used to advance past the file header.
  header: Generic line-buffer for skipping section headers and record labels between blocks
    of object data.
  eof: IOSTAT status flag for reads; controls exit when the end of the file or an input error
    is reached.
  imax: Number of water-allocation objects declared in the file; used to size the main allocation
    and output arrays and stored in `db_mx%wallo_db`.
  i_exist: Logical file-existence test used to decide whether the configured transfer file
    can be read.
  i: Current transfer-object number or loop index read from file and assigned to `wallo(iwro)%trn(i)%num`.
  k: Record leading index/value read alongside transfer-object data; used to preserve the
    sequence number from the file.
  isrc: Loop counter over source objects within a transfer object.
  iwro: Loop counter for the current water-allocation object being read.
  num_objs: Scratch count for how many transfer objects or source objects to allocate in the
    current allocation block.
  num_src: Scratch count for how many source entries belong to the current transfer object.
  itrn: Loop counter for the current transfer object within one water-allocation object.
  idb: Decision-table index used to search `dtbl_lum` or `dtbl_flo` by name.
  idb_irr: Irrigation-operation index used to search `irrop_db` by name when applying irrigation
    parameters.
  ihru: Receiver object number captured from the transfer record when linking irrigation-related
    transfer data to an HRU.
  iexco: Export-coefficient database index taken from an outside-source reference before cross-walking
    to OM-file names.
  iexco_om: Index into the export-coefficient OM-file list used to store the resolved annual
    constant source identifier.
  irec: Recall database index derived from an outside-source number before looking up `recall_db(irec)%iorg_min`.
  iom: Declared counter used by the routine's broader allocation logic; in this source span
    it is not actively referenced after declaration.
uses:
  input_file_module: This module provides the configured path to the water-allocation input
    file. The routine uses `in_watrts%transfer_wro` to decide which file to `open` and whether
    the file is effectively disabled by the string value `"null"`.
  water_allocation_module: This module owns the transfer-object and output types that this
    reader fills. The routine allocates the `wallo` hierarchy, stores file values into the
    transfer-object fields, resolves transfer metadata like `dtbl_lum` and `dtbl_num`, and
    initializes the output accumulators in `wallod_out`, `wallom_out`, `walloy_out`, and `walloa_out`
    for later flow accounting.
  mgt_operations_module: The routine maps irrigation decision-table actions to irrigation-operation
    parameters. It searches `irrop_db` by operation name so it can copy the matching field
    efficiency and surface-runoff ratio into the current transfer object.
  maximum_data_module: This module provides the maximum counts used to bound the lookup loops.
    The routine uses these maxima when scanning decision tables, irrigation operations, and
    export-coefficient metadata, and it stores the parsed water-allocation object count in
    `db_mx%wallo_db`.
  hydrograph_module: The routine allocates month/day/year/annual water-allocation object containers
    from this module and resets their source arrays alongside the main `wallo` data. These
    parallel structures are needed because later hydrograph output and aggregation logic expect
    the same object and source dimensions across time scales.
  sd_channel_module: The source imports this module even though no candidate outside reference
    from it is resolved in the packet. It likely matters because channel-linked transfer sources
    are identified while reading `wallo(iwro)%trn(i)%src(isrc)%typ == "cha"`, so channel state
    from this module may be needed by the broader allocation workflow.
  conditional_module: This module stores the decision tables that the file names refer to.
    The routine matches transfer types against these tables so it can convert a table name
    into a numeric decision-table index and then use the table's first action option to find
    the irrigation operation.
  constituent_mass_module: The routine allocates output and storage structures from the constituent-mass
    workflow earlier in the file's history, and the imported module remains relevant because
    transfer allocation and output initialization are tied to mass-tracking state for later
    constituent accounting.
  recall_module: This module provides the recall-file database used to resolve outside-basin
    sources. The routine reads a source number, treats it as a recall-file index when the
    source type is `osrc`, and copies `iorg_min` into the transfer object's day/month/year
    selector.
  exco_module: This module maps export-coefficient records to OM-file names. The routine uses
    that mapping to turn an `osrc_a` source reference into the resolved annual-constant source
    index stored in `osrc(isrc)%aa`.
  hru_module: This module provides HRU state needed when a transfer object targets an HRU-based
    irrigation rule. The routine captures the receiver number and uses it in the irrigation
    decision-table branch, so HRU-linked allocation must be available here.
---

<!-- facts:header -->

Reads the `water_allocation.wro` transfer-allocation file and populates the water allocation database and related output structures. It also cross-walks decision tables, irrigation operations, recall files, and export-coefficient metadata so later allocation and output logic can use resolved indices instead of names.

## Bottom Line

`water_allocation_read` is the input routine for water allocation rules. It opens the configured `water_allocation.wro` file, reads the top-level object count, allocates the `wallo` database plus monthly/daily/annual output containers, and then parses each water-allocation object and its transfer objects.

As it reads each transfer object, the routine resolves named references into internal IDs: land-use decision tables (`dtbl_lum`), flow-control decision tables (`dtbl_flo`), irrigation-operation parameters (`irrop_db`), recall-file sequencing (`recall_db`), and export-coefficient file links (`exco_db`/`exco_om_name`). It also records channel sources and initializes per-source output accumulators to zero so later simulation steps can sum withdrawals and outputs.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization after the configured transfer-water-rights filename has been established in `input_file_module%in_watrts`. It prepares the `wallo` database and related output containers before later water-allocation and hydrograph logic uses those structures to simulate withdrawals, source routing, and output aggregation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the transfer-file input is usable. | The routine tests `in_watrts%transfer_wro` for existence and for the sentinel value `"null"`. If the file is unavailable or disabled, it allocates a one-element placeholder `wallo(0:0)` and skips file parsing. |
| 2. Open the transfer file and read the top-level object count. | The routine opens unit 107 on the configured file, reads the title line and then reads `imax`, storing that count in `db_mx%wallo_db`. That count becomes the basis for all subsequent allocation sizing. |
| 3. Allocate the top-level allocation and output containers. | Using `imax`, the routine allocates `wallo` and the daily, monthly, yearly, and annual hydrograph/output arrays so every water-allocation object has parallel storage for later accounting. |
| 4. Loop over each water-allocation object record. | For each object index, the routine skips a header line, reads the object name, rule type, and transfer-object count, then allocates per-object transfer storage in `wallo` and the matching hydrograph/output containers. |
| 5. Read each transfer object's first pass and record its sequence number. | Inside the transfer loop, the routine reads the record index into `i`, stores it in `wallo(iwro)%trn(i)%num`, backs up one record, and rereads the line with the full transfer metadata fields. |
| 6. Allocate source arrays for the current transfer object. | The routine uses `src_num` to allocate the source list, outside-basin metadata, and corresponding daily/monthly/yearly/annual output arrays for each transfer object. |
| 7. Resolve irrigation decision-table and irrigation-operation references. | When the transfer type is `dtbl_lum`, the routine finds the matching land-use decision table by name, stores its index in `dtbl_lum`, and then searches `irrop_db` using the table's first action option to copy irrigation efficiency and surface runoff values. |
| 8. Resolve flow-control decision-table references. | When the transfer type is `dtbl_con`, the routine finds the matching flow-control decision table by name and stores its numeric table index in `dtbl_num`. |
| 9. Reread the full transfer record with sources and receiver. | After the source arrays are allocated, the routine backs up again and rereads the transfer record including the source list, source-allocation table name, and receiving object. |
| 10. Identify channel sources. | The routine scans the source list for a source of type `cha` and, when found, records the channel number in `ch_src` for later channel-based routing. |
| 11. Resolve outside-basin recall sources. | The routine scans for `osrc` sources and maps their source number to `recall_db(irec)%iorg_min`, storing the resolved sequential file index in `osrc(isrc)%daymoyr`. |
| 12. Resolve annual-constant outside sources from export-coefficient files. | For `osrc_a` sources, the routine compares `exco_db(iexco)%om_file` to the names returned by `exco_om_name` and stores the matching index in `osrc(isrc)%aa`. |
| 13. Zero the per-source output accumulators. | The routine initializes every per-source daily, monthly, yearly, and annual output slot to `walloz` so later simulation steps can accumulate withdrawals and source contributions from a known zero baseline. |
| 14. Close the file and return. | After all objects and transfer records have been read, the routine exits the object loop, closes unit 107, and returns to the caller with the allocation database populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_watrts` | `in_watrts%transfer_wro` |
| [sym:water_allocation_module] | `wallo, wallod_out, wallom_out, walloy_out, walloa_out` | `wallo(iwro)%name, wallo(iwro)%rule_typ, wallo(iwro)%trn_obs, wallo(iwro)%trn(num_objs), wallod_out(iwro)%trn(num_objs), wallom_out(iwro)%trn(num_objs), walloy_out(iwro)%trn(num_objs), walloa_out(iwro)%trn(num_objs), wallo(iwro)%trn(i)%num, wallo(iwro)%trn(i)%trn_typ, wallo(iwro)%trn(i)%trn_typ_name, wallo(iwro)%trn(i)%amount, wallo(iwro)%trn(i)%right, wallo(iwro)%trn(i)%src_num, wallo(iwro)%trn(i)%src(num_src), wallo(iwro)%trn(i)%osrc(num_src), wallod_out(iwro)%trn(i)%src(num_src), wallom_out(iwro)%trn(i)%src(num_src), walloy_out(iwro)%trn(i)%src(num_src), walloa_out(iwro)%trn(i)%src(num_src), wallo(iwro)%trn(i)%rcv%num, wallo(iwro)%trn(itrn)%dtbl_lum, wallo(iwro)%trn(itrn)%irr_eff, wallo(iwro)%trn(itrn)%surq, wallo(iwro)%trn(itrn)%dtbl_num, wallo(iwro)%trn(i)%dtbl_src, wallo(iwro)%trn(i)%src(isrc), wallo(iwro)%trn(i)%rcv, wallo(iwro)%trn(i)%src(isrc)%typ, wallo(iwro)%trn(i)%ch_src, wallo(iwro)%trn(i)%src(isrc)%num, wallo(iwro)%trn(i)%osrc(isrc)%daymoyr, wallo(iwro)%trn(i)%osrc(isrc)%aa, wallod_out(iwro)%trn(i)%src(isrc), wallom_out(iwro)%trn(i)%src(isrc), walloy_out(iwro)%trn(i)%src(isrc), walloa_out(iwro)%trn(i)%src(isrc)` |
| [sym:mgt_operations_module] | `irrop_db` | `irrop_db(idb_irr)%name, irrop_db(idb_irr)%eff, irrop_db(idb_irr)%surq` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wallo_db, db_mx%dtbl_lum, db_mx%irrop_db, db_mx%dtbl_flo, db_mx%exco_om` |
| [sym:hydrograph_module] | `wal_omd, wal_omm, wal_omy, wal_oma` | `wal_omd(iwro)%trn(num_objs), wal_omm(iwro)%trn(num_objs), wal_omy(iwro)%trn(num_objs), wal_oma(iwro)%trn(num_objs), wal_omd(iwro)%trn(i)%src(num_src), wal_omm(iwro)%trn(i)%src(num_src), wal_omy(iwro)%trn(i)%src(num_src), wal_oma(iwro)%trn(i)%src(num_src)` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch` |
| [sym:conditional_module] | `dtbl_lum, dtbl_flo` | `dtbl_lum(idb)%name, dtbl_lum(idb)%act(1)%option, dtbl_flo(idb)%name` |
| [sym:constituent_mass_module] | `cs_stor` | `cs_stor` |
| [sym:recall_module] | `recall_db` | `recall_db(irec)%iorg_min` |
| [sym:exco_module] | `exco_db` | `exco_db(iexco)%om_file` |
| [sym:hru_module] | `hru` | `hru` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%wallo_db` | When the file is usable and `imax` has been read from the top of `water_allocation.wro`. | Stores the declared number of water-allocation objects so other initialization code knows how many objects were parsed from the file. |
| `wallo(iwro)%trn(i)%num` | For each transfer object after its sequence number is read from the file. | Stores the transfer object's file sequence number in the `num` field so the object keeps its original position from the input record. |
| `wallo(iwro)%trn(itrn)%dtbl_lum` | When a transfer object has `trn_typ == "dtbl_lum"` and its `trn_typ_name` matches a land-use decision table. | Records which land-use decision table controls this transfer object so later logic can use an internal table index instead of a name. |
| `wallo(iwro)%trn(itrn)%irr_eff` | When the matched land-use decision table's first action maps to an irrigation operation. | Copies the irrigation operation's field efficiency so irrigation transfer behavior uses the parameters attached to the matched decision table. |
| `wallo(iwro)%trn(itrn)%surq` | When the matched irrigation operation is found for the decision-table action. | Copies the irrigation operation's surface-runoff ratio so the transfer object carries the runoff split associated with that irrigation rule. |
| `wallo(iwro)%trn(itrn)%dtbl_num` | When a transfer object has `trn_typ == "dtbl_con"` and its `trn_typ_name` matches a flow-control decision table. | Records the numeric flow-control decision-table index used to allocate sources for that transfer object. |
| `wallo(iwro)%trn(i)%ch_src` | When a source in the transfer list has type `cha`. | Stores the channel number for the transfer object so later routing can identify the channel source explicitly. |
| `wallo(iwro)%trn(i)%osrc(isrc)%daymoyr` | When a source entry is of type `osrc` and the routine resolves it through `recall_db`. | Stores the recall-file sequential identifier in the outside-source metadata so the source can later be linked to a recall time series. |
| `wallo(iwro)%trn(i)%osrc(isrc)%aa` | When a source entry is of type `osrc_a` and its OM file name matches the export-coefficient list. | Stores the annual-constant source identifier in the outside-source metadata so the source can be matched to the correct export-coefficient datafile. |
| `wallod_out(iwro)%trn(i)%src(isrc)` | After the transfer object's source list has been allocated. | Initializes daily source-output storage to zero for that transfer object so subsequent accumulation starts from a clean baseline. |
| `wallom_out(iwro)%trn(i)%src(isrc)` | After the transfer object's source list has been allocated. | Initializes monthly source-output storage to zero for that transfer object so later monthly accumulation starts from a clean baseline. |
| `walloy_out(iwro)%trn(i)%src(isrc)` | After the transfer object's source list has been allocated. | Initializes yearly source-output storage to zero for that transfer object so later yearly accumulation starts from a clean baseline. |
| `walloa_out(iwro)%trn(i)%src(isrc)` | After the transfer object's source list has been allocated. | Initializes annual source-output storage to zero for that transfer object so later annual accumulation starts from a clean baseline. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows four commits changed `water_allocation_read`. The earliest resolved change, `94b6dec`, imported the current file structure and established the initial read/allocate/close workflow. `39fabde` converted local scalars such as `titldum`, `header`, `eof`, `imax`, `i`, `k`, `isrc`, `iwro`, and related counters to initialized values and also changed some allocation calls elsewhere in the file. `e18817a` made a small source-comment fix but did not materially change the algorithm. `815ec79` changed the allocation line for `osrc_om` and added a recall-related placeholder comment. `72206bc` then added `recall_module`, introduced `iom`, `isrc_wallo`, and `div_found`, and implemented the actual recall cross-walk for `trn_typ == "recall"` while also commenting out an `osrc_om` allocation line.

- 94b6dec established the main file-reading structure: opening the configured transfer file, reading `imax`, allocating `wallo` and the output containers, looping over water-allocation objects, reading transfer records, and closing the file.
- 39fabde initialized the local scalars and counters at declaration time, reducing uninitialized-state risk before file parsing begins.
- 815ec79 changed the allocation target from `osrc_om_out` to `osrc_om` in the water-allocation setup block and added a placeholder recall comment in the source-loop area.
- 72206bc added `use recall_module`, introduced the `iom`/`isrc_wallo`/`div_found` locals, commented out an `osrc_om` allocation line, and implemented the recall-name cross-walk that sets `wallo(iwro)%trn(i)%rec_num` when a transfer type is `recall`.
- e18817a only corrected a comment typo in this routine's source and did not alter runtime behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_allocation_read' has no extracted documentation comment.
- sd_channel_module is imported but no resolved outside references were provided in the packet; its exact role here is uncertain beyond channel-source handling.
- constituent_mass_module is imported but no resolved outside references were provided in the packet; its role here is inferred from the water-allocation/output initialization context.
- Lineage reviewed from resolved commits only; no unresolved-history guesswork used.
