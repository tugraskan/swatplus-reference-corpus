---
kind: procedure
symbol: water_pipe_read
title: water_pipe_read
status: filled
source_hash: 4a368a266aa6602e
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard the first title line from `water_pipe.wal`
    before parsing the actual data records.
  header: Temporary string used to read and discard section header lines in `water_pipe.wal`
    while stepping through the file structure.
  eof: I/O status flag from each `read`; negative values signal end-of-file and stop the scan/parse
    loop.
  imax: Holds the pipe-record count read from the file header; it is used to size the `pipe`
    allocation and copied to `db_mx%pipe`.
  i_exist: Logical flag from `inquire` that tells the routine whether `water_pipe.wal` is
    present before attempting to read it.
  i: Record index read from the file for each pipe entry; it appears to be a sequential identifier
    or echoed row number from the input.
  ipipe: Loop counter over pipe definitions; it selects which element of the shared `pipe`
    array is being populated.
  num_aqu: Temporary count of aquifers associated with the current pipe; it is used to allocate
    `pipe(ipipe)%aqu_loss`.
  iaq: Inner-loop counter used in the array-directed read of `pipe(ipipe)%aqu_loss(iaq)` values.
uses:
  input_file_module: This module supplies the file-existence state needed by `inquire(file='water_pipe.wal',
    exist=i_exist)` so the routine can safely decide whether to allocate an empty `pipe(0:0)`
    placeholder or parse the input file.
  water_allocation_module: '`water_allocation_module` owns the `pipe` derived-type array and
    the `wal` pointer target, so this routine relies on it to create and populate the shared
    water-transfer records that other allocation code will later consume.'
  mgt_operations_module: The routine imports this module because the pipe input format includes
    a leading record identifier read into `i`; the module is part of the shared model state
    used by management and allocation input handling, even though no specific symbol from
    it is resolved in the extracted snippet.
  maximum_data_module: '`maximum_data_module` provides `db_mx`, and `db_mx%pipe` is updated
    with the pipe count read from the file so the model''s maximum-data bookkeeping matches
    the loaded pipe database.'
  hydrograph_module: This module is imported by the routine, indicating pipe input loading
    participates in the broader hydrologic state setup; no specific hydrograph symbol was
    resolved in the extracted source, so its exact usage here is uncertain.
  constituent_mass_module: This module is imported because water-transfer inputs can affect
    constituent-loss calculations downstream; no specific constituent-mass symbol was resolved
    in the extracted source, so the exact dependency is not visible in this snippet.
---

<!-- facts:header -->

Reads the `water_pipe.wal` water-allocation input and loads pipe definitions into shared model storage. It also records the number of pipe entries so later water-allocation routines can use the parsed configuration.

## Bottom Line

`water_pipe_read` is a file-driven initialization routine for SWAT+ water allocation pipes. It checks whether `water_pipe.wal` exists, opens it, reads the file header and pipe count, then allocates and fills the shared `pipe` array with each pipe's name, storage capacity, drawdown days, loss fraction, and aquifer-loss data.

The routine matters because it establishes the in-memory pipe database used by later water-allocation behavior. It also updates `db_mx%pipe` so the model knows how many pipe records were loaded from the input file.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization when the water-allocation pipe input file needs to be loaded. The upstream setup is the presence of `water_pipe.wal` and the shared module state it populates; later water-allocation behavior depends on the filled `pipe` array and the updated `db_mx%pipe` count.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize status variables and check for input file presence | The routine zeroes the EOF and maximum-count variables, checks whether `water_pipe.wal` exists with `inquire`, and if the file is missing or disabled (`'water_pipe.wal' == "null"`) allocates a minimal `pipe(0:0)` placeholder instead of reading real data. |
| 2. Open the pipe input file and read the file title and count | When the file is present, the routine opens unit 107 on `water_pipe.wal`, reads the title line and the pipe-count header, then stores the count in `db_mx%pipe` so downstream code knows how many pipe records exist. |
| 3. Allocate storage for the pipe records | After confirming the header read succeeded, the routine allocates the shared `pipe(imax)` array using the count read from the file. |
| 4. Loop over each pipe entry and skip per-record header lines | For each expected pipe record, the routine reads and discards a section header line before parsing the actual pipe data. |
| 5. Read the basic pipe fields and temporary aquifer count | The routine reads the pipe index, name, maximum storage, drawdown days, loss fraction, and a temporary aquifer count into `num_aqu`, using the count to size the per-pipe aquifer-loss storage. |
| 6. Allocate the per-pipe aquifer-loss array | Using `num_aqu`, the routine allocates `pipe(ipipe)%aqu_loss` so the pipe can hold one aquifer-loss record per linked aquifer. |
| 7. Read the full pipe record including aquifer-loss values | The routine rereads the pipe line, this time capturing `pipe(ipipe)%num_aqu` and filling the `aqu_loss` array with the per-aquifer loss values from the record. |
| 8. Finish the file scan and close the input unit | After all pipe records are processed, the routine exits the loop, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` | `i_exist` |
| [sym:water_allocation_module] | `pipe, wal` | `pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, pipe(ipipe)%aqu_loss(num_aqu), pipe(ipipe)%num_aqu, pipe(ipipe)%aqu_loss(iaq)` |
| [sym:mgt_operations_module] | `mgt_operations_module` | `i` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pipe` |
| [sym:hydrograph_module] | `hydrograph_module` | `none resolved` |
| [sym:constituent_mass_module] | `constituent_mass_module` | `none resolved` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%pipe` | When `water_pipe.wal` exists and the header read succeeds, `db_mx%pipe` is assigned the file's pipe count (`imax`). | This updates the model's maximum-data bookkeeping to match the number of pipe records loaded from the input file, which downstream allocation and transfer routines can use to size or iterate over pipe data. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was added in d70017a with the initial file-reading implementation: it checks for `water_pipe.wal`, reads the title/header/count, allocates `pipe`, reads pipe fields, allocates `aqu_loss`, and closes the file. Commit 080211e changed the shared count assignment from a commented placeholder to `db_mx%pipe = imax` and renamed the stored pipe timing field from `lag_days` to `ddown_days` in both pipe reads.

- d70017a introduced `water_pipe_read.f90` and implemented the initial `water_pipe.wal` parsing workflow, including allocation of `pipe` and `pipe(ipipe)%aqu_loss` and reading each pipe record from unit 107.
- 080211e made the routine update `db_mx%pipe` with the parsed pipe count and changed the parsed pipe timing field to `ddown_days`, so the loaded water-allocation records match the current water-transfer data type.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_pipe_read' has no extracted documentation comment.
- algorithm_steps revised: split the original coarse steps into eight source-faithful steps so each major read/allocate action is represented with explicit line citations.
- Source uses `pipe(ipipe)%ddown_days` in the final version; earlier lineage diff showed `lag_days`, so the documentation should follow the current source, not the older commit.
- `mgt_operations_module`, `hydrograph_module`, and `constituent_mass_module` are imported but no specific resolved symbols from them appear in the extracted snippet; their roles here are therefore partially uncertain.
