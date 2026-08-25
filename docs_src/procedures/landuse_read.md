---
kind: procedure
symbol: landuse_read
title: landuse_read
status: filled
source_hash: 5641b95e0bd94bdb
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and skip title lines from landuse.lum during
    both the counting pass and the data-read pass.
  header: Temporary character buffer used to read and skip the file header line in landuse.lum
    before scanning or loading records.
  eof: IOSTAT status flag for reads from unit 107; it controls end-of-file detection and exits
    from the counting and load loops.
  imax: Running count of landuse data records found in the file; it becomes the allocation
    size and the loop bound for loading and mapping records.
  i_exist: Logical flag set by INQUIRE to tell whether the configured landuse file exists
    before attempting to open it.
  mlu: Reset-to-zero placeholder counter that is not used in the visible routine body after
    initialization.
  ilu: Loop index for each landuse record being read and translated from names to database
    indices.
  ipcom: Loop counter used when searching plant community names in `pcomdb` to match `lum(ilu)%plant_cov`.
  isched: Loop counter used when searching management schedules in `sched` to match `lum(ilu)%mgt_ops`.
  ipr: Generic lookup counter reused for curve number, conservation practice, drainage, septic,
    filter strip, grassed waterway, and BMP user tables.
uses:
  input_file_module: '`input_file_module` provides the configured file name `in_lum%landuse_lum`,
    which determines which landuse.lum file this routine checks, opens, and reads.'
  maximum_data_module: '`maximum_data_module` holds the database-size counters that bound
    each lookup search and receives the final landuse count in `db_mx%landuse` after loading
    completes.'
  septic_data_module: '`septic_data_module` supplies the septic system database `sep`; its
    names are compared against `lum(ilu)%septic` so the routine can convert septic pointers
    to integer indices.'
  plant_data_module: '`plant_data_module` supplies `pcomdb`, the plant community database
    needed to resolve each land-use plant community name into an index for `lum_str(ilu)%plant_cov`.'
  hru_module: '`hru_module` provides the subsurface drainage database `sdr`, which is searched
    to resolve tile-drain references stored in `lum(ilu)%tiledrain`.'
  landuse_data_module: '`landuse_data_module` defines the source records `lum` and the resolved
    integer structure `lum_str` plus the lookup tables `cn` and `cons_prac`; these are the
    main state objects this routine fills and cross-links.'
  mgt_operations_module: '`mgt_operations_module` provides the management lookup tables `sched`,
    `filtstrip_db`, `grwaterway_db`, and `bmpuser_db`, whose names are matched to land-use
    management pointers so the routine can store the correct indices.'
---

<!-- facts:header -->

Reads the landuse.lum database, counts and loads land-use management records, then translates name-based pointers into integer indices for linked plant, management, curve number, conservation practice, drainage, septic, filter strip, grassed waterway, and BMP user tables.

## Bottom Line

`landuse_read` is a database-loader for SWAT+ land use management definitions. It opens the configured landuse.lum file, counts the data rows, allocates `lum` and `lum_str`, reads each land use record, and then resolves each string pointer to an index in the corresponding database array.

It matters because later model code relies on the integer lookups stored in `lum_str` rather than the raw names in `lum`. The routine also records the total landuse count in `db_mx%landuse` and reports unresolved references to unit 9001.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after soil/plant/management-related databases have been read and before later model routines use land-use pointers. Its output populates the `lum` and `lum_str` arrays and the landuse count used by downstream HRU and management setup.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the landuse file is available | The routine inquires on `in_lum%landuse_lum` and, if the file is missing or set to `"null"`, allocates one-element placeholder arrays for `lum` and `lum_str` instead of reading data. |
| 2. Count data records in landuse.lum | It opens unit 107, skips the title and header records, then reads through the remaining lines with `titldum` to count how many landuse records exist in the file. |
| 3. Allocate storage for all landuse records | Using the counted record total `imax`, it allocates `lum(0:imax)` and `lum_str(0:imax)` so the arrays can hold every landuse entry and its resolved indices. |
| 4. Rewind and reread the file from the start | The routine rewinds unit 107 and rereads the title and header lines so the file position is reset before actual record loading begins. |
| 5. Load each landuse record | It reads each record into `lum(ilu)` for `ilu = 1, imax`, populating the string-based land-use management fields from landuse.lum. |
| 6. Resolve plant community references | For non-`"null"` `plant_cov` values, it searches `pcomdb` by name and stores the matching index in `lum_str(ilu)%plant_cov`. |
| 7. Resolve management schedule references | For non-`"null"` `mgt_ops` values, it searches `sched` by name and stores the matching schedule index in `lum_str(ilu)%mgt_ops`. |
| 8. Resolve curve-number references | For non-`"null"` `cn_lu` values, it searches `cn` by name and stores the matched curve-number table index in `lum_str(ilu)%cn_lu`. |
| 9. Resolve conservation-practice references | For non-`"null"` `cons_prac` values, it searches `cons_prac` by name and stores the matching conservation-practice index in `lum_str(ilu)%cons_prac`. |
| 10. Resolve tile-drain references | For non-`"null"` `tiledrain` values, it searches `sdr` by name and stores the matching subsurface-drainage index in `lum_str(ilu)%tiledrain`. |
| 11. Resolve septic references | For non-`"null"` `septic` values, it searches `sep` by name and stores the matching septic-system index in `lum_str(ilu)%septic`. |
| 12. Resolve filter-strip, grassed-waterway, and BMP-user references | It resolves `fstrip`, `grassww`, and `bmpuser` by searching `filtstrip_db`, `grwaterway_db`, and `bmpuser_db`, storing matched indices in the corresponding `lum_str` fields. |
| 13. Report unresolved references to unit 9001 | When a non-`"null"` lookup field still has resolved value 0, the routine writes a message to unit 9001 naming the landuse and the missing database entry. |
| 14. Close the file and save the count | Finally, it closes unit 107 and stores the total landuse count in `db_mx%landuse` for use by later model setup. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_lum` | `in_lum%landuse_lum` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantcom, db_mx%mgt_ops, db_mx%cn_lu, db_mx%cons_prac, db_mx%sdr, db_mx%septic, db_mx%filtop_db, db_mx%grassop_db, db_mx%bmpuserop_db, db_mx%landuse` |
| [sym:septic_data_module] | `sep` | `sep(ipr)%name` |
| [sym:plant_data_module] | `pcomdb` | `pcomdb(ipcom)%name` |
| [sym:hru_module] | `sdr` | `sdr(ipr)%name` |
| [sym:landuse_data_module] | `lum, lum_str, cn, cons_prac` | `lum(ilu)%plant_cov, lum_str(ilu)%plant_cov, lum(ilu)%mgt_ops, lum_str(ilu)%mgt_ops, lum(ilu)%cn_lu, cn(ipr)%name, lum_str(ilu)%cn_lu, lum(ilu)%cons_prac, cons_prac(ipr)%name, lum_str(ilu)%cons_prac, lum(ilu)%tiledrain, lum_str(ilu)%tiledrain, lum(ilu)%septic, lum_str(ilu)%septic, lum(ilu)%fstrip, lum_str(ilu)%fstrip, lum(ilu)%grassww, lum_str(ilu)%grassww, lum(ilu)%bmpuser, lum_str(ilu)%bmpuser, lum(ilu)%name` |
| [sym:mgt_operations_module] | `sched, filtstrip_db, grwaterway_db, bmpuser_db` | `sched(isched)%name, filtstrip_db(ipr)%name, grwaterway_db(ipr)%name, bmpuser_db(ipr)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lum_str(ilu)%plant_cov` | When `lum(ilu)%plant_cov` is not `"null"` and matches `pcomdb(ipcom)%name` during the lookup loop. | Stores the plant community index in `lum_str(ilu)%plant_cov` so the landuse record points to the loaded plant community database entry. |
| `lum_str(ilu)%mgt_ops` | When `lum(ilu)%mgt_ops` is not `"null"` and matches `sched(isched)%name` during the lookup loop. | Stores the management schedule index in `lum_str(ilu)%mgt_ops` so later routines can apply the correct management schedule. |
| `lum_str(ilu)%cn_lu` | When `lum(ilu)%cn_lu` is not `"null"` and matches `cn(ipr)%name` during the lookup loop. | Stores the curve-number table index in `lum_str(ilu)%cn_lu` so runoff calculations can use the correct curve-number set. |
| `lum_str(ilu)%cons_prac` | When `lum(ilu)%cons_prac` is not `"null"` and matches `cons_prac(ipr)%name` during the lookup loop. | Stores the conservation-practice table index in `lum_str(ilu)%cons_prac` so erosion and practice settings can reference the correct table entry. |
| `lum_str(ilu)%tiledrain` | When `lum(ilu)%tiledrain` is not `"null"` and matches `sdr(ipr)%name` during the lookup loop. | Stores the subsurface-drainage index in `lum_str(ilu)%tiledrain` so tile-drain behavior can refer to the correct drainage parameters. |
| `lum_str(ilu)%septic` | When `lum(ilu)%septic` is not `"null"` and matches `sep(ipr)%name` during the lookup loop. | Stores the septic-system index in `lum_str(ilu)%septic` so septic-related landuse behavior can use the correct system definition. |
| `lum_str(ilu)%fstrip` | When `lum(ilu)%fstrip` is not `"null"` and matches `filtstrip_db(ipr)%name` during the lookup loop. | Stores the filter-strip operation index in `lum_str(ilu)%fstrip` so filter-strip behavior can use the correct operation parameters. |
| `lum_str(ilu)%grassww` | When `lum(ilu)%grassww` is not `"null"` and matches `grwaterway_db(ipr)%name` during the lookup loop. | Stores the grassed-waterway operation index in `lum_str(ilu)%grassww` so grassed-waterway behavior can use the correct operation parameters. |
| `lum_str(ilu)%bmpuser` | When `lum(ilu)%bmpuser` is not `"null"` and matches `bmpuser_db(ipr)%name` during the lookup loop. | Stores the BMP-user operation index in `lum_str(ilu)%bmpuser` so user-defined BMP removal settings can use the correct operation entry. |
| `db_mx%landuse` | After the routine finishes loading and counting the file, just before return. | Records the total number of landuse entries read from landuse.lum so other initialization code knows the size of the landuse database. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved for `landuse_read`. The initial addition in `df07e3f` created the routine that reads landuse.lum, builds `lum` and `lum_str`, resolves lookups, and stores `db_mx%landuse`. Commit `94b6dec` preserved that behavior as part of a source import, and `39fabde` only initialized local scalars (`titldum`, `header`, `eof`, `imax`, `mlu`, `ilu`, `ipcom`, `isched`, `ipr`) without changing the algorithm.

- df07e3f introduced the full landuse database reader: file existence check, count pass, allocation, record load, pointer resolution, diagnostics, close, and final `db_mx%landuse` assignment.
- 39fabde changed only local variable initialization for `titldum`, `header`, `eof`, `imax`, `mlu`, `ilu`, `ipcom`, `isched`, and `ipr`; the file I/O and lookup behavior remained the same.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'landuse_read' has no extracted documentation comment.
