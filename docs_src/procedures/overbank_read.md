---
kind: procedure
symbol: overbank_read
title: overbank_read
status: filled
source_hash: 727d172c7ec133d0
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the title line read from `chan-surf.lin` during both the scan pass and the
    data load pass.
  header: Holds the header line from `chan-surf.lin`; it is skipped/consumed before the routine
    reads the numbered data records.
  namedum: Temporary string field used when reading each record's object name during the first
    pass over the data records.
  eof: I/O status flag for reads from unit 107; negative means end-of-file, zero means the
    read succeeded and the routine can continue.
  imax: Tracks the larger of the counted record total and the file's stated surface count;
    this becomes the allocation size and the stored maximum surface count.
  nspu: Number of surface/polygon entries on a channel record; used to decide whether per-object
    arrays must be allocated and read.
  i_exist: Logical flag set by `inquire` to show whether the configured channel-surface file
    exists before reading starts.
  max: Intrinsic comparison function used to set `imax` to the larger of the counted records
    and `mcha_sp`; it is not a stored variable.
  mcha_sp: Reads the file's declared maximum channel-surface count from the second line and
    participates in the final allocation size check.
  i: Loop/index variable used both to count records in the file scan and to identify the current
    channel object when loading data.
  isp: Loop counter over the sub-object arrays `obtyp` and `obtypno` while reading a channel's
    floodplain entries.
  numb: Temporary integer read from each full data record before the record's name, object
    total, and type lists are loaded into `sd_ch(i)%fp`.
  ise: Counter for the final data-loading loop; it iterates through the allocated record slots
    from 1 to `imax`.
uses:
  hydrograph_module: The routine allocates `ch_sur(imax)` in `hydrograph_module`; that shared
    array is the destination for channel-surface elements, so its size must be set before
    floodplain linkage data can be populated.
  input_file_module: '`input_file_module` provides `in_link%chan_surf`, the configured file
    name for the channel-surface linkage file that this routine opens and reads.'
  maximum_data_module: '`maximum_data_module` holds `db_mx%ch_surf`, the shared maximum-file-size
    counter that this routine updates after determining how many channel-surface records it
    must manage.'
  sd_channel_module: '`sd_channel_module` supplies the `sd_ch` channel objects whose floodplain
    parameter blocks are filled here; their `fp` fields receive the surface type and number
    arrays that define overbank linkage.'
---

<!-- facts:header -->

Reads the channel-surface linkage file and loads floodplain surface-element settings for channel objects. It sizes the shared channel-surface arrays, stores the maximum surface count, and populates each channel's floodplain parameter lists.

## Bottom Line

overbank_read opens the configured `chan-surf.lin` file, checks that it exists, and scans it to find how many channel-surface records and sub-objects it contains. It uses that count to allocate `ch_sur` and to store the maximum file size in `db_mx%ch_surf`.

After rewinding the file, it rereads the records and fills `sd_ch(i)%fp` floodplain data for each channel object: the floodplain name, total object count, and the per-object type and object-number arrays. That information is what later channel processing uses to connect channels to overbank/floodplain surface elements.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when channel hydrology and channel-process setup need the overbank surface-link file translated into shared model state. `hyd_connect` calls it after channel connection setup, and `proc_cha` calls it before `sd_channel_surf_link`, so the loaded `sd_ch` floodplain parameters are available when channel-to-landscape linkage is established.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check for a usable channel-surface file | The routine calls `inquire` on `in_link%chan_surf` to see whether the configured file exists, and only enters the read logic when the file is present or the name is not the literal `null`. |
| 2. Open the file and read the file header | It opens unit 107 on `in_link%chan_surf`, reads the title, maximum surface count, and header line, and stops the pass early if end-of-file is hit. |
| 3. Count data records to determine allocation size | The routine loops through the remaining records, reading a placeholder integer from each line and incrementing `imax` until end-of-file; it then raises `imax` to at least `mcha_sp` with `max(imax, mcha_sp)`. |
| 4. Allocate the shared channel-surface array | Using the final `imax`, it allocates `ch_sur(imax)` in `hydrograph_module` so the model has storage for the channel-surface elements. |
| 5. Rewind and reread the file header | The file is rewound and the title, maximum surface count, and header are read again so the second pass starts from the top of the file. |
| 6. Store the maximum surface count | It copies `imax` into `db_mx%ch_surf`, recording the maximum channel-surface count for the model's data-size bookkeeping. |
| 7. Read each channel-surface record | For each expected record, the routine reads the record index, name, and `nspu`; when `nspu > 0`, it allocates `sd_ch(i)%fp%obtyp` and `sd_ch(i)%fp%obtypno`, backspaces one record, and rereads the full line into `sd_ch(i)%fp%name`, `sd_ch(i)%fp%obj_tot`, and the per-entry type/number arrays. |
| 8. Close the file and return | After one successful loading pass, the routine exits the open loop, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ch_sur` |  |
| [sym:input_file_module] | `in_link` | `in_link%chan_surf` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_surf` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(i)%fp%obtyp(nspu), sd_ch(i)%fp%obtypno(nspu), sd_ch(i)%fp%name, sd_ch(i)%fp%obj_tot, sd_ch(i)%fp%obtyp(isp), sd_ch(i)%fp%obtypno(isp)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_surf` | When `in_link%chan_surf` exists or is not the literal `null`, after `imax` has been determined from the file scan. | `db_mx%ch_surf` is updated to the final record-count maximum so other routines know how many channel-surface entries were loaded from `chan-surf.lin`. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f with the full channel-surface read-and-load logic. Commit 94b6dec later carried the source forward with no behavioral change in this routine, and commit 39fabde changed the `allocate (sd_ch(i)%fp%obtypno(nspu))` line to initialize the array with `source = 0` so the object-number list starts from zero-filled storage.

- df07e3f added `overbank_read` with file existence checking, two-pass scanning, allocation of `ch_sur`, storage of `db_mx%ch_surf`, and loading of `sd_ch(i)%fp` floodplain linkage records from `chan-surf.lin`.
- 39fabde changed the `obtypno` allocation to `allocate (..., source = 0)`, ensuring newly allocated object-number arrays are initialized to zero before record data are read.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'overbank_read' has no extracted documentation comment.
