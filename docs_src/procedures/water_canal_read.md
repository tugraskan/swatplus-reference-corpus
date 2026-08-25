---
kind: procedure
symbol: water_canal_read
title: water_canal_read
status: filled
source_hash: 6708ccc366b985e9
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from the start of `water_canal.wal` and discarded after
    the file header is parsed.
  header: Temporary header line read from `water_canal.wal` before the canal records are processed.
  eof: I/O status flag used on reads from unit 107; negative values signal end-of-file and
    stop the scan.
  imax: Holds the canal record count read from `water_canal.wal`; it controls allocation sizes
    for `canal`, `canal_om_stor`, `canal_om_out`, and `canal_cs_stor`.
  i_exist: Logical flag from `inquire` that reports whether `water_canal.wal` exists before
    the routine tries to read it.
  i: Input record index read from each canal line and used as the sequence/check value for
    the current canal entry.
  ic: Loop index over canal records; identifies which element of `canal` is being filled.
  num_aqu: Temporary count of aquifers associated with the current canal record; used to allocate
    `canal(ic)%aqu_loss` before the second read.
  iaq: Loop index for the per-aquifer loss values inside `canal(ic)%aqu_loss`.
uses:
  input_file_module: The routine uses `inquire` on `i_exist` to decide whether `water_canal.wal`
    can be read or whether it should fall back to an empty canal allocation.
  water_allocation_module: This module owns the `canal` array and the `wal` pointer. `water_canal_read`
    fills `canal(ic)%...` fields from the file and uses the canal type definition, including
    `aqu_loss`, to allocate and store each canal's configuration and aquifer-loss data.
  mgt_operations_module: The import is present in the source, but no resolved symbols from
    `mgt_operations_module` are used in the visible lines of this routine.
  maximum_data_module: '`db_mx%canal` stores the maximum number of canal records discovered
    in the input file. That count is needed elsewhere to size database-style arrays and to
    know how many canal entries exist.'
  hydrograph_module: These arrays hold canal storage and outflow hydrograph data. They must
    be allocated to `imax` so later canal-routing and output routines can write time-series
    results for each canal entry.
  constituent_mass_module: This array holds canal constituent-mass storage state. It is allocated
    alongside the canal list so later water-quality or tracer accounting can track canal mass
    storage for each canal entry.
---

<!-- facts:header -->

Reads canal configuration records from `water_canal.wal` and populates the shared canal allocation data structures. It also sizes related storage arrays and records the number of canal entries for later water-allocation, hydrograph, and constituent-mass handling.

## Bottom Line

`water_canal_read` is the file-reader for canal setup data. It checks whether `water_canal.wal` is present, opens it, reads the header and entry count, then loads each canal definition into the shared `canal` array.

The routine also allocates companion storage arrays for canal hydrograph and constituent-mass outputs, and it records the maximum canal count in `db_mx%canal` so later model code can size and reference canal-related state consistently.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during water-allocation input initialization, after the model has established whether `water_canal.wal` exists and before canal routing or water-quality calculations begin. Its results feed later canal allocation, hydrograph storage/outflow, and constituent-mass accounting that depend on `canal`, `db_mx%canal`, `canal_om_stor`, `canal_om_out`, and `canal_cs_stor`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Reset counters and test whether the canal input file exists | The routine initializes `eof` and `imax`, checks for `water_canal.wal` with `inquire`, and allocates a zero-length `canal` array if the file is missing or the filename is disabled by the string comparison. |
| 2. Open and read the file header | If the file is present, the routine opens unit 107 on `water_canal.wal`, reads a title line, reads the canal count into `imax`, reads the next header line, and stores `imax` in `db_mx%canal`. |
| 3. Allocate canal-related shared arrays | Using the canal count from the file, the routine allocates the main `canal` array plus the companion `canal_om_stor`, `canal_om_out`, and `canal_cs_stor` arrays to the same size. |
| 4. Scan each canal record to learn its aquifer count | For each canal entry, the routine reads the base canal fields and the temporary `num_aqu` count, exits on end-of-file, and uses `backspace` so the full record can be reread after allocating the aquifer-loss array. |
| 5. Allocate per-canal aquifer-loss storage | After `num_aqu` is known, the routine allocates `canal(ic)%aqu_loss(num_aqu)` for the current canal entry. |
| 6. Read the full canal definition including aquifer-loss values | The routine rereads the same record with `canal(ic)%num_aqu` and the full `canal(ic)%aqu_loss(iaq)` list, leaving placeholders for weather-station, initial-concentration, and decision-table crosswalks. |
| 7. Close the input file and return | After the loop finishes, the routine closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `i_exist` | `i_exist` |
| [sym:water_allocation_module] | `canal, wal` | `canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, canal(ic)%aqu_loss(num_aqu), canal(ic)%num_aqu, canal(ic)%aqu_loss(iaq)` |
| [sym:mgt_operations_module] | `none resolved` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%canal` |
| [sym:hydrograph_module] | `canal_om_stor, canal_om_out` |  |
| [sym:constituent_mass_module] | `canal_cs_stor` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%canal` | When `water_canal.wal` exists and its canal count line is read successfully. | `db_mx%canal` is set to the number of canal records found in the file, making the canal database size available to later routines that need to know how many canal entries exist. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two source-backed commits affecting `water_canal_read`: 080211e introduced the routine and its file-reading/allocation logic, and b78c4ea expanded the canal record layout by adding `bed_thick`, `div_id`, `day_beg`, and `day_end` to both the scan and full-read statements.

- 080211e added `water_canal_read.f90` with the file existence check, header reads, canal allocation, and aquifer-loss loading workflow.
- b78c4ea changed the canal record parsing so the routine now reads and stores `bed_thick`, `div_id`, `day_beg`, and `day_end` before `num_aqu`, and it mirrors those fields in the reread with `aqu_loss` values.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_canal_read' has no extracted documentation comment.
