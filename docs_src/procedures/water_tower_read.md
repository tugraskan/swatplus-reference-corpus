---
kind: procedure
symbol: water_tower_read
title: water_tower_read
status: filled
source_hash: d6e02d9ee5521ed5
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from the top of `water_tower.wal` and discarded after
    the file header is consumed.
  header: Temporary header marker read before the record count and before each data row, used
    to step through the file structure rather than stored as model state.
  eof: I/O status flag from each `read`; negative values signal end-of-file or failed record
    reads and cause the routine to exit its scan loop.
  imax: Number of water-tower entries declared in the file; used to size `wtow`, `wtow_om_stor`,
    `wtow_om_out`, and `wtow_cs_stor`.
  i_exist: Logical flag set by `inquire` to indicate whether `water_tower.wal` is present
    before the routine tries to read it.
  i: Input record index read from each data row; it is consumed as a file value while the
    loop stores the corresponding row into `wtow(iwtow)`.
  iwtow: Loop counter that walks through the allocated water-tower array and selects which
    `wtow` element to populate.
uses:
  input_file_module: This module supplies the shared file-input context used to decide whether
    the named input file should be treated as available and read; the routine's file-existence
    check and file-name gating depend on that global input setup.
  water_allocation_module: This module owns the water-transfer data that `water_tower_read`
    populates. The routine fills `wtow(iwtow)%name`, `wtow(iwtow)%stor_mx`, `wtow(iwtow)%ddown_days`,
    and `wtow(iwtow)%loss_fr`, so the allocation-state module must be present for the read
    data to persist and be used later.
  mgt_operations_module: This module is imported because water-tower definitions participate
    in management-operation logic elsewhere in the model. Even though no specific symbol from
    it is referenced in the visible lines, the read routine is part of preparing management-related
    water-allocation inputs for later use.
  maximum_data_module: This module is imported for shared model sizing/limit state. The routine
    uses `imax` to determine how much water-tower storage it must allocate, so maximum-data
    support matters to keep the allocation consistent with the model's data limits.
  hydrograph_module: This module provides `wtow_om_stor` and `wtow_om_out`, the water-tower
    storage and outflow output arrays. `water_tower_read` allocates them to the same length
    as `wtow` so downstream hydrograph bookkeeping can record tower storage and release behavior.
  constituent_mass_module: This module provides `wtow_cs_stor`, the constituent-mass storage
    array for water towers. The routine allocates it alongside the water-tower definitions
    so later water-quality or mass-balance code has a place to store tower constituent mass
    state.
---

<!-- facts:header -->

Reads the water tower allocation definition file and loads water-tower metadata into shared model arrays. It also allocates related storage/output arrays used by the water allocation, hydrograph, and constituent-mass subsystems.

## Bottom Line

This routine loads `water_tower.wal`, first checking whether the file exists. If the file is missing or disabled, it ensures `wtow` exists as a zero-sized placeholder; otherwise it reads the record count, allocates the water-tower data arrays, and fills each `wtow(iwtow)` entry from the file.

The data it reads are not local to this routine: they populate shared allocation state and companion arrays for water-tower storage/outflow and constituent mass tracking. Later model code can use those arrays to simulate water-tower operation and associated routing or mass bookkeeping.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input initialization, after the water-tower allocation file name has been made available through the shared input-file setup. Its results feed later water-allocation, hydrograph, and constituent-mass behavior because it creates and fills the shared `wtow` array and the matching storage/output arrays those subsystems expect.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check for a usable water-tower input file | The routine tests whether `water_tower.wal` exists and is not disabled by the literal string `null`. If the file is missing or disabled, it leaves the routine with a placeholder `wtow(0:0)` allocation when `wtow` has not already been created. |
| 2. Open the input file for reading | The routine enters a loop, opens unit 107 on `water_tower.wal`, and reads the first record into `titldum` to advance past the file title line. |
| 3. Read record count and header | It reads `imax` as the declared number of water-tower entries, then reads a header line. If either read reports end-of-file or failure, the scan stops. |
| 4. Allocate shared water-tower state arrays | Using `imax`, the routine allocates `wtow` and the companion water-tower storage arrays `wtow_om_stor`, `wtow_om_out`, and `wtow_cs_stor` so later model components can store tower state and outputs. |
| 5. Scan each tower definition record | For each expected tower entry, the routine reads and discards a header line, then reads the tower index and the fields `name`, `stor_mx`, `ddown_days`, and `loss_fr` into `wtow(iwtow)`. Any end-of-file or failed read breaks out of the loop. |
| 6. Close the file and return | After the input scan finishes, the routine closes unit 107 and returns to its caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:water_allocation_module] | `wtow, wal` | `wtow(iwtow)%name, wtow(iwtow)%stor_mx, wtow(iwtow)%ddown_days, wtow(iwtow)%loss_fr` |
| [sym:mgt_operations_module] | `mgt_operations_module` |  |
| [sym:maximum_data_module] | `maximum_data_module` |  |
| [sym:hydrograph_module] | `wtow_om_stor, wtow_om_out` |  |
| [sym:constituent_mass_module] | `wtow_cs_stor` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavior changes. The initial addition in d70017a created `water_tower_read` as a new input routine that reads `water_tower.wal`, allocates `wtow`, and fills each record. The later commit 080211e changed the allocation behavior to always allocate `wtow`, `wtow_om_stor`, `wtow_om_out`, and `wtow_cs_stor`. Commit e24da22 then renamed the per-record field read from `lag_days` to `ddown_days`, matching the updated water-transfer data type.

- d70017a introduced the routine and its file-driven population of water-tower definitions from `water_tower.wal`.
- 080211e expanded the setup so the routine allocates the companion hydrograph and constituent-mass arrays, not just `wtow`.
- e24da22 updated the record read to store `ddown_days` instead of the older `lag_days` field.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_tower_read' has no extracted documentation comment.
