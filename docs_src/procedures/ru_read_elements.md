---
kind: procedure
symbol: ru_read_elements
title: ru_read_elements
status: filled
source_hash: fd03971654d44af7
version_label: SWAT+ 62.0.0
locals:
  iobtyp: Three-character object-type code read from each routing-unit element record and
    used in the `select case` to decide which spatial object family the element belongs to.
  titldum: Temporary title-line buffer used to skip or re-read file headings in both routing-unit
    input files.
  header: Temporary header-line buffer used to read and discard the second header line before
    scanning file contents.
  namedum: Temporary name buffer for the routing-unit definition scan; it captures the subbasin
    name field before the detailed membership list is reread.
  eof: I/O status flag returned by each `read(...,iostat=eof)` call; negative values end the
    scan and zero means continue.
  imax: Tracks the maximum element number seen in `rout_unit.ele` and later the count of records
    scanned in `rout_unit.def`.
  nspu: Number of defining-unit entries read for a routing-unit definition line; it controls
    whether the line is expanded and how many element IDs are read.
  i_exist: Logical flag from `inquire` that tells the routine whether the routing-unit file
    physically exists before attempting to open it.
  i: Loop index or record number read from `rout_unit.ele`; it identifies which `ru_elem(i)`
    slot is being populated.
  max: Temporary integer used with `Max(i,imax)` while scanning `rout_unit.ele` to find the
    largest element index.
  isp: Loop counter for scanning and later reading element records; in the definition file
    it also indexes `elem_cnt` values.
  k: Record index or object index read from the files; after object mapping it is reused as
    the destination object number in `ob(k)`.
  iob: Current spatial-object index derived from `sp_ob1%ru + iru - 1` and later from each
    element's mapped object number.
  iob1: Stores the first routing-unit object index in the current block of spatial objects.
  iob2: Stores the last routing-unit object index in the current block of spatial objects.
  iru: Loop counter over routing units/definition records in the current subbasin range.
  idr: Loop counter used to search the loaded delivery-ratio database for a matching `dr_name`.
  numb: Record identifier read from `rout_unit.def` before the line is expanded into explicit
    element numbers.
  ielem1: Loop counter over the explicit members of a routing unit; also receives the total
    expanded count from `define_unit_elements`.
  ii: Temporary element number taken from `ru_def(iru)%num(ielem1)` while assigning object
    membership and counting routing-unit participation.
  ie: Temporary element number used in the final pass that fills each object's routing-unit
    list.
  iru_tot: Temporary accumulator for the number of routing units attached to an object; it
    is loaded from `ob(iob)%ru_tot` before allocation.
uses:
  hydrograph_module: The hydrograph module owns the routing-unit, object-connectivity, spatial-object,
    and delivery-ratio arrays that this routine populates. `ru_elem`, `ru_def`, `ielem_ru`,
    `ob`, `sp_ob1`, `sp_ob`, `res`, `dr`, and related components provide the persistent state
    that stores element metadata, maps element type codes to object-number ranges, counts
    memberships per object, and records the per-object routing-unit links used later by hydrologic
    connectivity.
  input_file_module: The input-file module provides the configured file names `in_ru%ru_ele`
    and `in_ru%ru_def`, so this routine can open the correct routing-unit element and definition
    files without hard-coding paths. Those filenames determine which project inputs are scanned
    here.
  maximum_data_module: The maximum-data module holds `db_mx%ru_elem` and `db_mx%dr_om`, which
    this routine updates or uses as upper bounds while sizing routing-unit arrays and searching
    the delivery-ratio database. That shared maximum-data state matters because later allocation
    and crosswalk loops depend on the recorded element and delivery-ratio counts.
  dr_module: The delivery-ratio module provides `dr_db(idr)%name`, the lookup key used to
    match each routing-unit element's `dr_name` against the loaded delivery-ratio definitions.
    Without that shared database, the routine could not assign `ru_elem(i)%dr` to the correct
    delivery-ratio object.
---

<!-- facts:header -->

Reads routing-unit element and definition files, builds routing-unit membership arrays, and crosswalks element delivery ratios and object links for later hydrologic connectivity setup.

## Bottom Line

ru_read_elements ingests the routing-unit element list from `rout_unit.ele` and the routing-unit definition list from `rout_unit.def`. It expands the definition lists into explicit element memberships, assigns each element to its owning object number, and counts how many routing units and defining units touch each object.

It also crosswalks each element's delivery-ratio name to the loaded delivery-ratio database so `ru_elem(i)%dr` points at the correct `dr` entry. The resulting `ru_def`, `ru_elem`, `ielem_ru`, and `ob` connectivity fields are then available to the rest of routing and hydrograph setup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during hydrologic connectivity setup in `hyd_connect`, immediately after `ru_read` has loaded the routing-unit metadata. Its results feed later routing and hydrograph behavior by filling `ru_def`, `ru_elem`, `ielem_ru`, and `ob` so the model knows which elements belong to each routing unit and which objects each element maps to.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether routing-unit element data should be read | The routine inquires on `in_ru%ru_ele` and proceeds only if the file exists or the configured filename is not `null`. |
| 2. Scan `rout_unit.ele` to find the largest element index | It opens the element file, skips the title and header, reads element numbers in a loop, and stores the maximum value in `imax`. |
| 3. Size routing-unit arrays from the element count | The routine saves the count in `db_mx%ru_elem` and allocates `ru_def`, `ru_elem`, and `ielem_ru` to hold that many routing-unit entries. |
| 4. Rewind and reread the routing-unit element file | It rewinds the file, rereads the title and header, and clears `ielem_ru` before the second pass. |
| 5. Read each routing-unit element record and crosswalk its delivery ratio | For each record it backspaces to reread the full line, stores the element metadata in `ru_elem(i)`, then searches `dr_db` for a matching `dr_name` and assigns the corresponding `dr` entry. |
| 6. Close the routing-unit element file | After the element pass completes, the routine closes unit 107 for `rout_unit.ele`. |
| 7. Check whether routing-unit definition data should be read | It repeats the existence check for `in_ru%ru_def` and enters the definition branch when the file is available or configured. |
| 8. Count definition records and rewind the file | The routine opens `rout_unit.def`, reads past the headers, counts how many data lines are present, then rewinds and rereads the headers for the expansion pass. |
| 9. Loop over routing units in the current spatial-object block | For each routing unit it computes the object index, clears `ob(iob)%ru_tot`, and reads the compact definition line with `numb`, `namedum`, and `nspu`. |
| 10. Expand the compact definition into explicit element numbers | When `nspu > 0`, it backspaces, reads the full membership list, calls `define_unit_elements` to build `defunit_num`, stores that list in `ru_def(iru)%num`, records its length in `ru_def(iru)%num_tot`, and deallocates the temporary buffer. |
| 11. Map each element to its owning spatial object family | The routine loads the element's object type, uses a `select case` on `hru`, `hlt`, `ru`, `cha`, `res`, `exc`, `dr`, `out`, or `sdc` to compute `ru_elem(ii)%obj`, and increments the destination object's `ru_tot` counter. |
| 12. Build each object's routing-unit membership list | In a second pass it allocates each object's `ru` array, increments `ielem_ru` for each element, stores the current routing-unit number into `ob(iob)%ru(...)`, and records the element position in `ob(iob)%elem`. |
| 13. Close the routing-unit definition file and return | After the definition memberships are built, the routine closes unit 107 for `rout_unit.def` and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ru_elem, sp_ob1, sp_ob, ob, ru_def, ielem_ru, elem_cnt, defunit_num, res, dr` | `ru_elem(i)%name, ru_elem(i)%obtyp, ru_elem(i)%obtypno, ru_elem(i)%frac, ru_elem(i)%dr_name, ru_elem(i)%dr, sp_ob1%ru, sp_ob%ru, ob(iob)%ru_tot, ru_def(iru)%num_tot, ru_def(iru)%name, ru_def(iru)%num(ielem1), ru_def(iru)%num, ob(iob)%dfn_tot, ru_elem(ii)%obtyp, ru_elem(ii)%obj, sp_ob1%hru, ru_elem(ii)%obtypno, sp_ob1%hru_lte, sp_ob1%chan, sp_ob1%res, sp_ob1%exco, sp_ob1%dr, sp_ob1%outlet, sp_ob1%chandeg, ob(k)%ru_tot, ru_elem(ie)%obj, ob(iob)%ru(1), ob(iob)%elem` |
| [sym:input_file_module] | `in_ru` | `in_ru%ru_ele, in_ru%ru_def` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ru_elem, db_mx%dr_om` |
| [sym:dr_module] | `dr_db` | `dr_db(idr)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ru_elem` | After scanning `rout_unit.ele`, before allocating the routing-unit arrays. | `db_mx%ru_elem` stores the maximum routing-unit element index found in the element file so later allocations know how many routing-unit slots to reserve. |
| `ielem_ru` | Whenever an element is assigned to a routing-unit definition in the final membership pass. | `ielem_ru(ie)` counts how many routing units include each element so the code can place the current routing-unit number into the correct slot of `ob(iob)%ru`. |
| `ru_elem(i)%dr` | When a routing-unit element's `dr_name` matches a delivery-ratio record name in `dr_db`. | `ru_elem(i)%dr` is set to the corresponding delivery-ratio output/state object from `dr`, linking the element to its delivery-ratio data. |
| `ob(iob)%ru_tot` | For each element assigned to an object during the object-mapping loop. | `ob(iob)%ru_tot` is incremented to count how many routing units contain that object. |
| `ru_def(iru)%num_tot` | When a routing-unit definition record is expanded from the compact `elem_cnt` form. | `ru_def(iru)%num_tot` is set to the number of explicit element IDs produced by `define_unit_elements`. |
| `ru_def(iru)%num` | After `define_unit_elements` returns for a routing-unit definition with `nspu > 0`. | `ru_def(iru)%num` receives the explicit element-number list copied from `defunit_num`. |
| `ob(iob)%dfn_tot` | For each routing-unit definition's element list before the per-object `ru` arrays are allocated. | `ob(iob)%dfn_tot` records how many defining elements belong to the routing unit mapped to that object block. |
| `ru_elem(ii)%obj` | During the object-mapping loop for every element in each routing-unit definition. | `ru_elem(ii)%obj` is assigned the absolute object number of the element within its spatial-object family. |
| `ob(k)%ru_tot` | When the routine counts each element's membership in an object during the definition pass. | `ob(k)%ru_tot` accumulates the number of routing units that reference object `k`. |
| `ielem_ru(ie)` | During the final membership fill pass over every routing-unit element. | `ielem_ru(ie)` increments for each routing unit that contains element `ie`, providing the write index into that object's routing-unit list. |
| `ob(iob)%ru(ielem_ru(ie))` | When the final pass stores the current routing-unit number for an element's object. | `ob(iob)%ru(ielem_ru(ie))` receives the current routing-unit index so the object knows which routing units include it. |
| `ob(iob)%elem` | During the same final pass after the routing-unit number is stored. | `ob(iob)%elem` stores the element position within the routing unit, which later code can use to identify the object's placement in that unit. |

## File I/O

<!-- facts:io -->


## Lineage

`ru_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ru_read_elements.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `f8bb6ec` (2024-07-25) — Manually coded init changes
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ru_read_elements' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
