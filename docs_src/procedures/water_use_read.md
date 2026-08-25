---
kind: procedure
symbol: water_use_read
title: water_use_read
status: filled
source_hash: d9d111482ee0f456
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title/header line read from `water_use.wal` before the record count;
    the routine uses it to advance past the file’s first text line.
  header: Scratch string for section labels or separator lines in `water_use.wal`; it is read
    and discarded before pesticide and pathogen data blocks.
  eof: I/O status flag for `read(...,iostat=eof)` calls; negative values end the scan loop
    or skip further processing on end-of-file.
  imax: Number of water-use objects declared in `water_use.wal`; it controls array allocation
    size and sets `db_mx%uses`.
  i_exist: Logical file-existence test from `inquire`; it determines whether the routine reads
    `water_use.wal` or falls back to an empty `wuse(0:0)` allocation.
  i: Record index read from file for each water-use entry; it is a file sequence counter and
    is not the main storage index.
  iwuse: Loop index for populating the `wuse` and companion arrays one water-use object at
    a time.
  iom: Loop index used to search `om_use_name` for a matching organic-mineral name so `wuse(iwuse)%iorg_min`
    can be set.
uses:
  input_file_module: '`input_file_module` matters because this routine only parses the water-use
    database when the requested input file is available; otherwise it allocates a trivial
    placeholder array and skips the read.'
  water_allocation_module: '`water_allocation_module` matters because it owns the `wuse` database,
    the `wal` pointer, and the organic-mineral name table that this routine fills and crosswalks.
    The routine populates the treatment-use records and resolves each record’s `org_min` name
    to an internal index.'
  mgt_operations_module: '`mgt_operations_module` matters because the routine compares each
    water-use record’s `org_min` text value against `om_use_name(iom)` to find the matching
    management-operation index stored in `wuse(iwuse)%iorg_min`.'
  maximum_data_module: '`maximum_data_module` matters because `db_mx` stores file-size metadata;
    this routine writes `db_mx%uses = imax` so later allocation and model setup know how many
    water-use objects were read.'
  hydrograph_module: '`hydrograph_module` matters because this routine allocates the shared
    hydrograph output arrays sized to the number of water-use objects. Those arrays hold water-use
    storage/outflow and organic-mineral addition diagnostics for later reporting.'
  constituent_mass_module: '`constituent_mass_module` matters because the routine sizes and
    fills the water-use constituent concentration arrays from the active pesticide and pathogen
    counts in `cs_db`. Those arrays let treated-water effluent carry constituent concentrations
    forward into later transport calculations.'
  sd_channel_module: '`sd_channel_module` matters as a dependency of the water-allocation
    and routing stack, even though the extracted source does not show a direct symbol reference;
    the imported module keeps this reader linked to channel-routing state used later by the
    model.'
---

<!-- facts:header -->

Reads the `water_use.wal` input file and builds the water-use treatment database used by SWAT+ water allocation routines. It also crosswalks organic-mineral names to indices and loads optional pesticide/pathogen effluent concentrations.

## Bottom Line

`water_use_read` is a file-backed initialization routine for water-treatment use objects. When `water_use.wal` exists, it opens the file, reads the count and each water-use record, allocates the shared arrays sized to that count, and stores the parsed attributes in `wuse` plus related output/state arrays.

After each record is read, it resolves the `org_min` text name to an `iorg_min` index using `om_use_name` and, when constituent databases are active, allocates and loads pesticide and pathogen effluent concentration arrays. Those results feed later water allocation, hydrograph, and constituent-mass handling.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization when water-use treatment data must be loaded from `water_use.wal`. The extracted source shows no resolved caller, so the upstream setup is not identified in the packet; downstream water allocation, hydrograph reporting, and constituent-mass routines depend on the arrays and indices it populates.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize status and test for input availability | The routine clears the local end-of-file and record-count variables, checks whether `water_use.wal` exists, and if not allocates `wuse(0:0)` as an empty placeholder. |
| 2. Open the water-use file and skip the title line | The routine opens unit 107 on `water_use.wal`, reads the title line into `titldum`, and stops the scan if the file is already exhausted. |
| 3. Read the record count and header | It reads the declared number of water-use objects into `imax`, skips the next header line into `header`, stores the count in `db_mx%uses`, and exits early if the file ended unexpectedly. |
| 4. Allocate shared arrays for all water-use objects | Using `imax`, the routine allocates the main `wuse` database and the companion hydrograph and constituent-mass arrays that must match the number of water-use records. |
| 5. Read each water-use record | For each record, it reads the file index and the water-use fields into `wuse(iwuse)`, including name, storage, lag, loss fraction, organic-mineral label, and other constituent labels. |
| 6. Crosswalk organic-mineral names to indices | The routine loops through `om_use_name` to match `wuse(iwuse)%org_min`; when it finds a match, it stores the corresponding index in `wuse(iwuse)%iorg_min`. |
| 7. Read pesticide effluent concentrations when pesticides are active | If `cs_db%num_pests` is positive, the routine allocates `wuse_cs_efflu(iwuse)%pest`, reads a separator line, and then reads the pesticide concentrations for the current water-use object. |
| 8. Read pathogen effluent concentrations when pathogens are active | If `cs_db%num_paths` is positive, the routine allocates `wuse_cs_efflu(iwuse)%path`, reads a separator line, and then reads the pathogen concentrations for the current water-use object. |
| 9. Finish the file scan and close the input | After the loop completes or exits early, the routine leaves the scanning block, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module state that reports whether configured input files are present or disabled, including the file-name string checked by `inquire`.` | `i_exist, the `water_use.wal` name test in `if (.not. i_exist .or. 'water_use.wal' == "null")`` |
| [sym:water_allocation_module] | `wuse, om_use_name, wal` | `wuse(iwuse)%name, wuse(iwuse)%stor_mx, wuse(iwuse)%lag_days, wuse(iwuse)%loss_fr, wuse(iwuse)%org_min, wuse(iwuse)%pests, wuse(iwuse)%paths, wuse(iwuse)%salts, wuse(iwuse)%constit, wuse(iwuse)%descrip, wuse(iwuse)%iorg_min` |
| [sym:mgt_operations_module] | `mgt_operations_module state providing management-operation name lookup tables used for crosswalks.` | `om_use_name` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%uses, db_mx%om_use` |
| [sym:hydrograph_module] | `wuse_om_stor, wuse_om_out, wal_use_omd, wal_use_omm, wal_use_omy, wal_use_oma` |  |
| [sym:constituent_mass_module] | `cs_db, wuse_cs_efflu, wuse_cs_stor` | `cs_db%num_pests, wuse_cs_efflu(iwuse)%pest, cs_db%num_paths, wuse_cs_efflu(iwuse)%path` |
| [sym:sd_channel_module] | `sd_channel_module state and types used to support downstream routing/channel interactions tied to water-use outputs.` | `the module is imported but no specific symbol from `sd_channel_module` is referenced in the extracted source` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%uses` | When `water_use.wal` is read successfully and `imax` has been parsed from the file. | `db_mx%uses` is set to the number of water-use records declared in the input file so later code can size and reference the water-use database consistently. |
| `wuse(iwuse)%iorg_min` | When a water-use record’s `org_min` text matches one entry in `om_use_name` during the per-record crosswalk loop. | `wuse(iwuse)%iorg_min` is set to the matching management-operation index, replacing the text label with an internal pointer used later by water-use and management logic. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The initial addition `d70017a` created `water_use_read.f90` and implemented the file read, record allocation, organic-mineral crosswalk, and optional pesticide/pathogen section reads. Commit `080211e` changed the stored count from `db_mx%water_use` to `db_mx%uses` and added allocations for `wuse_om_stor`, `wuse_om_out`, `wuse_cs_stor`, `wal_use_omd`, `wal_use_omm`, `wal_use_omy`, and `wal_use_oma`.

- `d70017a` introduced the reader and its core behavior: file existence check, `water_use.wal` scan, `wuse` allocation, per-record field parsing, `org_min` crosswalk, and optional constituent effluent reads.
- `080211e` corrected the stored record count field to `db_mx%uses` and expanded initialization to allocate the hydrograph and constituent-mass arrays needed for water-use storage and output tracking.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_use_read' has no extracted documentation comment.
