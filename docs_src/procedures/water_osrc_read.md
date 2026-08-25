---
kind: procedure
symbol: water_osrc_read
title: water_osrc_read
status: filled
source_hash: 4dab8749efd842fd
version_label: SWAT+ 62.0.0
locals:
  titldum: Title-line buffer read from out_src.wal before the source count and headers are
    processed.
  header: Reusable header buffer used to skip or capture section labels in out_src.wal before
    reading constituent data blocks.
  eof: I/O status flag for each read; negative values indicate end-of-file and stop the parsing
    loop.
  imax: The number of outside basin sources declared in the file; used to allocate osrc and
    drive the source-read loop.
  i_exist: Logical flag set by INQUIRE to tell whether the expected input file is present
    before reading begins.
  i: Loop-local integer that reads the record index field from each source record.
  isrc: Loop index over outside basin source objects, used to fill osrc and osrc_cs entries.
  iom: Declared counter for recall crosswalk logic, but that logic is not present in the resolved
    source slice.
  irec: Declared counter for recall crosswalk logic, but that logic is not present in the
    resolved source slice.
uses:
  input_file_module: This module matters because the routine first checks file availability
    before attempting to open and parse out_src.wal; that control state determines whether
    the reader allocates a placeholder osrc array or proceeds with file I/O.
  water_allocation_module: water_allocation_module matters because osrc and wal hold the outside
    basin source database that this routine populates; the routine fills osrc(isrc)%name,
    osrc(isrc)%stor_mx, osrc(isrc)%lag_days, and osrc(isrc)%loss_fr for later water-allocation
    calculations.
  recall_module: recall_module matters because the lineage diff shows a removed crosswalk
    section that matched outside source names against recall database entries; even though
    that block is absent in the resolved source slice, the module is part of the routine's
    documented dependency set.
  mgt_operations_module: mgt_operations_module matters because the routine's dependency list
    includes it and the outside-source data it reads is used by management operations that
    route treated water and its associated constituents.
  maximum_data_module: maximum_data_module matters because db_mx%out_src is updated with the
    number of outside sources read from the file, making that count available to later allocation
    and array-sizing logic.
  hydrograph_module: hydrograph_module matters because the outside-source water objects are
    part of the broader routed water system; their stored capacity, lag, and loss parameters
    ultimately feed hydrograph/water-transfer calculations elsewhere in SWAT+.
  constituent_mass_module: constituent_mass_module matters because it supplies cs_db counts
    for pesticide and pathogen arrays and the osrc_cs storage that this routine allocates
    and fills from out_src.wal.
  sd_channel_module: sd_channel_module matters because the treated outside-source water and
    its constituent loads must ultimately interact with channel-routing storage and transport
    behavior in the receiving model domain.
---

<!-- facts:header -->

Reads the outside source water-treatment definition file and loads outside basin source objects plus optional pesticide and pathogen concentrations. It also records how many outside sources were found for later water-allocation logic.

## Bottom Line

water_osrc_read is the file-reader for outside basin source definitions. It opens out_src.wal, checks whether the file exists, reads the declared number of sources, and populates the shared osrc array with each source's name, maximum storage, lag time, and loss fraction.

If pesticide or pathogen constituents are active, it also allocates osrc_cs entries and reads those concentration arrays from the same file. The routine finishes by closing the file and storing the source count in db_mx%out_src so downstream water-allocation code can size and use the outside-source database.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input-data setup, after the outside-source file path has been established and before water allocation and constituent routing begin. It prepares the shared osrc and osrc_cs data that later water-allocation, pesticide, and pathogen handling depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check for the outside-source input file | The routine uses INQUIRE to test whether outside_src.wal exists and, if it does not, allocates a minimal osrc(0:0) placeholder so the shared array remains defined. |
| 2. Open the file and read the file header | The routine opens unit 107 on out_src.wal, reads the title line, reads the maximum source count into imax, reads a section header, and stores the count in db_mx%out_src. |
| 3. Allocate storage for all outside sources | After confirming the header read succeeded, the routine allocates osrc(imax) so the outside-source database has one entry per source record. |
| 4. Read each outside-source property record | The routine loops over isrc from 1 to imax and reads the source index, source name, maximum storage, lag days, and loss fraction into osrc(isrc). |
| 5. Read pesticide concentrations when enabled | If cs_db%num_pests is greater than zero, the routine allocates osrc_cs(isrc)%pest, consumes a header line, and reads the pesticide concentration vector for the current outside source. |
| 6. Read pathogen concentrations when enabled | If cs_db%num_paths is greater than zero, the routine allocates osrc_cs(isrc)%path, consumes a header line, and reads the pathogen concentration vector for the current outside source. |
| 7. Finish the read and close the file | The routine exits the file-processing block, closes unit 107, and returns with osrc, osrc_cs, and db_mx%out_src populated for later model use. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module provides the file-existence/input-control state used to decide whether the read should proceed.` | `input-file control state used by the routine's INQUIRE/open logic` |
| [sym:water_allocation_module] | `osrc, wal` | `osrc(isrc)%name, osrc(isrc)%stor_mx, osrc(isrc)%lag_days, osrc(isrc)%loss_fr` |
| [sym:recall_module] | `recall_module provides recall database/state used for outside-source crosswalking in the full routine lineage.` | `recall_db(irec)%name, recall(iom)%filename` |
| [sym:mgt_operations_module] | `mgt_operations_module provides management-operation state used for outside-source routing in the full routine lineage.` | `management-operation state for outside-source handling` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%out_src` |
| [sym:hydrograph_module] | `hydrograph_module provides hydrograph-related state/types used by the outside-source water workflow.` | `hydrograph-related state used by outside-source allocation` |
| [sym:constituent_mass_module] | `cs_db, osrc_cs` | `cs_db%num_pests, osrc_cs(isrc)%pest, cs_db%num_paths, osrc_cs(isrc)%path` |
| [sym:sd_channel_module] | `sd_channel_module provides channel-routing state/types referenced by the outside-source water-transfer workflow.` | `channel-routing state used by outside-source water allocation` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%out_src` | When outside_src.wal exists and is successfully read, db_mx%out_src is set to the imax value parsed from the file. | This records how many outside basin source objects were loaded, so later routines know the database size and can iterate over the allocated osrc array. |

## File I/O

<!-- facts:io -->


## Lineage

The resolved lineage shows two commits affecting this routine. The initial addition in 72206bc introduced water_osrc_read and its outside-source reading logic. Commit 080211e changed the file name from outside_src.wal to out_src.wal, renamed the stored maximum from db_mx%outside_src to db_mx%out_src, and removed the recall crosswalk loop that matched outside sources to recall records.

- 72206bc added the routine and its baseline behavior: file existence check, osrc allocation, source record reads, and optional pesticide/pathogen constituent reads.
- 080211e changed the external file name and database counter to out_src.wal and db_mx%out_src, and it removed the recall_db/recall-based crosswalk block from the source-processing loop.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_osrc_read' has no extracted documentation comment.
- algorithm_steps revised: collapsed the placeholder allocate/store steps into source-faithful file-read steps with line-specific evidence.
- Source slice shows a mismatch between inquire(file='outside_src.wal') and open/read on out_src.wal; this may be intentional in the lineage or may warrant manual verification.
