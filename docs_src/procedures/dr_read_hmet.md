---
kind: procedure
symbol: dr_read_hmet
title: dr_read_hmet
status: filled
source_hash: 48abd95bdb235009
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch text field used to read and discard title or record-name lines from `dr_hmet.del`
    during the counting and data-loading passes.
  header: Scratch text field used to read and discard the file header line from `dr_hmet.del`
    before the data records are counted or loaded.
  eof: I/O status flag for each `read`; values below zero end the scan, and zero means the
    file still has readable records.
  imax: Counts how many heavy-metal delivery-ratio records are present in `dr_hmet.del`; also
    used to size the allocation arrays.
  ob1: Lower bound of the delivery-ratio object range to process when copying heavy-metal
    coefficients into object hydrographs.
  ob2: Upper bound of the delivery-ratio object range to process when copying heavy-metal
    coefficients into object hydrographs.
  i_exist: Logical flag from `inquire` that records whether the configured heavy-metal delivery-ratio
    file is present on disk.
  idr_hmet: Loop index over heavy-metal delivery-ratio records, used both when allocating
    per-record coefficient arrays and when matching names to records.
  ii: Loop index for the second file pass that reads each heavy-metal delivery-ratio record
    into `dr_hmet_name` and `dr_hmet`.
  ihmet: Loop index over individual heavy-metal coefficients within one delivery-ratio record.
  idr: Loop index over delivery-ratio database entries while crosswalking `dr_db(idr)%hmet_file`
    to the heavy-metal table.
  iob: Loop index over object slots in the delivery-ratio object range when copying coefficients
    into `obcs(iob)%hd(1)%hmet`.
uses:
  hydrograph_module: These hydrograph and connectivity objects define which spatial objects
    carry delivery-ratio properties and where the loaded heavy-metal coefficients are stored.
    `sp_ob1%dr` and `sp_ob%dr` define the object range, `ob(iob)%props` selects the delivery-ratio
    record for each object, and `obcs(iob)%hd(1)%hmet` is the destination array that receives
    the coefficients.
  dr_module: The delivery-ratio database stores the configured heavy-metal file name for each
    delivery-ratio entry. `dr_db(idr)%hmet_file` is what this routine crosswalks against the
    names read from `dr_hmet.del` so it can assign the correct numbered heavy-metal record.
  input_file_module: This module supplies the configured path to the heavy-metal delivery-ratio
    input file. `in_delr%hmet` determines which file is opened and whether the routine should
    attempt to read heavy-metal delivery-ratio data at all.
  organic_mineral_mass_module: These constituent-mass arrays hold the heavy-metal delivery-ratio
    coefficients that are read from file, sized by the number of simulated metals, and then
    copied into each object’s constituent hydrograph for later transport calculations.
  constituent_mass_module: This module provides the heavy-metal delivery-ratio table, the
    count of simulated metals, and the object hydrograph destination. `dr_hmet(idr_hmet)%hmet`
    stores the loaded coefficients, `cs_db%num_metals` sets the allocation and read width,
    and `obcs(iob)%hd(1)%hmet` receives the selected coefficient vector for each object.
  maximum_data_module: This module holds the maximum-record counters used to dimension the
    delivery-ratio arrays. `db_mx%dr_hmet` is set from the number of heavy-metal records read,
    and `db_mx%dr` controls how many delivery-ratio database entries are crosswalked afterward.
---

<!-- facts:header -->

Reads the heavy-metal delivery-ratio file for SWAT+ and loads its names and metal transfer coefficients into shared model state.

It also crosswalks those delivery-ratio names to the delivery-ratio database and copies the matching heavy-metal coefficients onto each object’s constituent hydrograph.

## Bottom Line

dr_read_hmet is the heavy-metal counterpart to the other delivery-ratio readers: it opens the configured `dr_hmet.del` file, counts the usable records, allocates storage, then reads each delivery-ratio name and its heavy-metal coefficients into `dr_hmet`, `dr_hmet_name`, and `dr_hmet_num`-related state.

After loading the file, it matches each delivery-ratio database entry (`dr_db(idr)%hmet_file`) to the numbered heavy-metal table, then copies the selected heavy-metal coefficient vector into each affected object’s constituent hydrograph (`obcs(iob)%hd(1)%hmet`). That makes the heavy-metal delivery ratios available to later routing and constituent-mass calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `dr_db_read` after the model has determined that heavy metals are being simulated (`cs_db%num_metals > 0`). It depends on the configured delivery-ratio file name from `in_delr%hmet` and the delivery-ratio database entries in `dr_db`, and its results are used later when object hydrographs are assigned heavy-metal delivery ratios.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Test whether the heavy-metal file should be read | The routine checks `in_delr%hmet` with `inquire` and only proceeds if the file exists or the configured name is not `null`. |
| 2. Open and scan the file to count records | It opens unit 107 on the configured file, skips the title and header lines, then counts each remaining data line to determine `imax`. |
| 3. Store the record count and allocate arrays | The routine records the number of heavy-metal delivery-ratio records in `db_mx%dr_hmet` and allocates `dr_hmet`, `dr_hmet_num`, and `dr_hmet_name`; each `dr_hmet(idr_hmet)%hmet` vector is sized to `cs_db%num_metals`. |
| 4. Rewind and skip file labels again | It rewinds the file so the data can be read from the start again, then rereads the title and header lines to position the file at the first record. |
| 5. Read each heavy-metal delivery-ratio record | For each record, the routine reads a line, backs up one record, then reads the delivery-ratio name and the full heavy-metal coefficient vector into the allocated arrays. |
| 6. Close the file after loading | The input file is closed once all records have been loaded. |
| 7. Crosswalk delivery-ratio database entries to heavy-metal records | The routine loops through each delivery-ratio database entry and finds the matching heavy-metal record name; it stores the matched heavy-metal index in `dr_hmet_num(idr)`. |
| 8. Assign heavy-metal coefficients to object hydrographs | Using the spatial-object delivery-ratio range from `sp_ob1%dr` to `sp_ob1%dr + sp_ob%dr - 1`, the routine looks up each object’s delivery-ratio property and copies the matched heavy-metal coefficient vector into `obcs(iob)%hd(1)%hmet`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%dr, sp_ob%dr, ob(iob)%props` |
| [sym:dr_module] | `dr_db, dr_hmet_num, dr_hmet_name` | `dr_db(idr)%hmet_file` |
| [sym:input_file_module] | `in_delr` | `in_delr%hmet` |
| [sym:organic_mineral_mass_module] | `dr_hmet, cs_db, obcs` | `dr_hmet(idr_hmet)%hmet, cs_db%num_metals, obcs(iob)%hd(1)%hmet` |
| [sym:constituent_mass_module] | `dr_hmet, cs_db, obcs` | `dr_hmet(idr_hmet)%hmet, cs_db%num_metals, obcs(iob)%hd(1)%hmet` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dr_hmet, db_mx%dr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dr_hmet` | When the configured heavy-metal delivery-ratio file is present or the file name is not `null`, and the file scan completes. | `db_mx%dr_hmet` is set to the number of heavy-metal delivery-ratio records found in `dr_hmet.del`, which sizes later allocations and loops. |
| `dr_hmet_num(idr)` | When a delivery-ratio database entry `dr_db(idr)%hmet_file` matches one of the names read from `dr_hmet.del`. | `dr_hmet_num(idr)` stores the index of the matching heavy-metal delivery-ratio record so the model can retrieve the correct coefficient vector for that delivery-ratio entry. |
| `obcs(iob)%hd(1)%hmet` | When an object index `iob` falls in the delivery-ratio object range and its properties entry `ob(iob)%props` maps to a valid heavy-metal record. | `obcs(iob)%hd(1)%hmet` is filled with the selected heavy-metal delivery-ratio coefficients for that object, making the data available to the object’s constituent hydrograph. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `dr_read_hmet`. The initial addition commit `df07e3f` created the routine with file reading, allocation, name crosswalk, and object assignment logic. Commit `94b6dec` kept the same algorithm but did not change behavior in the visible diff. Commit `39fabde` changed initialization and allocation details by giving local scalars default zero values and using `source = 0.` / `source = 0` in the allocations.

- df07e3f introduced `dr_read_hmet` with the full heavy-metal delivery-ratio load/crosswalk/population workflow.
- 39fabde tightened initialization by setting local scalars to zero and allocating `dr_hmet(idr_hmet)%hmet` and `dr_hmet_num` with zero source values.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dr_read_hmet' has no extracted documentation comment.
