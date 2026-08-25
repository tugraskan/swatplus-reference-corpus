---
kind: procedure
symbol: om_use_read
title: om_use_read
status: filled
source_hash: 4fb289b990cd65e7
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the file title line read from `om_use.wal`; the
    routine discards its content after skipping the first record.
  header: Temporary character buffer for the file header line read from `om_use.wal`; it is
    consumed only to advance past the header section.
  eof: I/O status flag for the reads from unit 107; negative values signal end-of-file and
    stop the scan/record loop.
  imax: Number of water-use records declared in `om_use.wal`; it also sets the allocation
    size for `om_use_name` and `wuse_om_efflu`.
  i_exist: Logical existence test from `inquire`; it decides whether the routine treats `om_use.wal`
    as available or falls back to zero-length allocations.
  iom_use: Loop index used to read each water-use name and effluent output setting into the
    allocated arrays.
uses:
  input_file_module: The routine imports `input_file_module`, but the packet does not resolve
    any concrete symbols from it. That module likely provides shared input-file configuration
    or file-handling state needed by the broader model setup, even though no direct reference
    was extracted here.
  water_allocation_module: '`om_use_name` is the array filled by this routine with the names
    of water-allocation use entries, so the water-allocation module owns the primary shared
    results. `wal` is imported from the same module, but the extracted source does not show
    it being referenced directly in this routine.'
  mgt_operations_module: The routine imports `mgt_operations_module`, but no concrete symbol
    usage was extracted. The module matters because water-use names read here may be linked
    later to management operations elsewhere in the model.
  maximum_data_module: '`db_mx` holds model-wide maxima for data-file-backed collections.
    This routine updates `db_mx%om_use` so later allocation and validation code know how many
    water-use entries were loaded.'
  hydrograph_module: '`wuse_om_efflu` is the shared output-configuration array populated here
    from `om_use.wal`. The hydrograph module matters because these values control water-use
    effluent outputs used by later hydrologic reporting and routing logic.'
  constituent_mass_module: The routine imports `constituent_mass_module`, but no direct symbol
    references were extracted. That module matters because effluent settings can affect constituent-mass
    accounting downstream, even though this subroutine only loads the configuration.
---

<!-- facts:header -->

Reads the `om_use.wal` water-allocation input and loads water-use names and effluent output settings into shared model arrays.

## Bottom Line

`om_use_read` is a simple input loader for the water allocation subsystem. It checks whether `om_use.wal` exists, then reads the file’s title line, record count, header, and one `name / effluent` pair per water-use entry.

Its main effect is to populate `om_use_name` and `wuse_om_efflu`, and to record the number of water-use entries in `db_mx%om_use`. Those values are used later wherever water-use operation names and effluent outputs are referenced.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization when the water-allocation inputs are being loaded. The file-level setup happens before later routines can use the water-use names and effluent settings, and downstream behavior depends on `om_use_name`, `wuse_om_efflu`, and `db_mx%om_use` being populated correctly.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and status flags | Sets the title/header buffers to empty strings, resets `eof` and `imax` to zero, and declares the existence flag and loop counter used during file loading. |
| 2. Check whether the input file exists | Uses `inquire` on `om_use.wal` and checks for the special disabled-file case before deciding whether to read data or fall back to empty allocations. |
| 3. Allocate empty arrays if the file is unavailable | Allocates one-element zero-bounds arrays for `wuse_om_efflu` and `om_use_name` when the file is missing or disabled, giving the rest of the model a defined empty state. |
| 4. Open the water-allocation file and read the prologue | Opens unit 107 on `om_use.wal`, reads the title line, reads `imax`, reads the header line, and stores `imax` in `db_mx%om_use` before continuing. |
| 5. Allocate arrays sized to the declared record count | Creates `wuse_om_efflu(imax)` and `om_use_name(imax)` so the routine can store each water-use record from the file. |
| 6. Load each water-use record | Loops from 1 to `imax`, stops early on end-of-file, and reads each `om_use_name(iom_use)` together with its corresponding `wuse_om_efflu(iom_use)` value. |
| 7. Close the file and return | Closes unit 107 after the read loop finishes, then returns to the caller with the shared arrays populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `No specific symbols were resolved from this module in the extracted source.` | `[]` |
| [sym:water_allocation_module] | `om_use_name, wal` |  |
| [sym:mgt_operations_module] | `No specific symbols were resolved from this module in the extracted source.` | `[]` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%om_use` |
| [sym:hydrograph_module] | `wuse_om_efflu` |  |
| [sym:constituent_mass_module] | `No specific symbols were resolved from this module in the extracted source.` | `[]` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%om_use` | When `om_use.wal` exists and the read of `imax` succeeds | The routine stores the declared number of water-use records into the global database-maximum counter so later code knows how many `om_use_name` and `wuse_om_efflu` elements were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit d70017a (2025-11-24) as a new source file. The diff shows the full initial implementation: existence check for `om_use.wal`, allocation of `wuse_om_efflu` and `om_use_name`, reading `imax`, storing `db_mx%om_use`, looping over records, and closing unit 107.

- d70017a added `om_use_read.f90` as a new subroutine that reads `om_use.wal`, allocates shared arrays, and records the file-defined count in `db_mx%om_use`. This created the water-use input loader used by the model initialization flow.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'om_use_read' has no extracted documentation comment.
