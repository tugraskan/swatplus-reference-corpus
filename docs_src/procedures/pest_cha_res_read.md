---
kind: procedure
symbol: pest_cha_res_read
title: pest_cha_res_read
status: filled
source_hash: 0ea53417d908b242
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to consume label or data fields while scanning and rereading
    `pest_water.ini`; in the first pass it advances past record labels and in the second pass
    it is also the dummy field preceding the concentration arrays.
  header: Scratch string used to read and skip the file header line(s) after the title line
    on both passes through `pest_water.ini`.
  eof: I/O status flag from each `read`; zero means keep reading, negative indicates end-of-file
    and stops the scan or load loop.
  imax: Counts how many initial-condition records are present in `pest_water.ini`; it becomes
    the allocation size and is copied to `db_mx%pestw_ini`.
  i_exist: Logical flag from `inquire` that tells whether the configured pesticide-water initial
    file exists on disk.
  ipest: Loop counter over pesticide entries within one initial-condition block during the
    counting pass; it runs from 1 to `cs_db%num_pests`.
  ipesti: Loop counter over the initial-condition blocks themselves; it indexes `pest_water_ini`
    and `pest_init_name` during allocation and loading.
uses:
  constituent_mass_module: '`cs_db%num_pests` sets how many pesticide concentration rows each
    block must contain, so the routine uses it to count records and to size the `water` and
    `benthic` arrays. The loaded values go into `pest_water_ini(ipesti)` and the block name
    goes into `pest_init_name(ipesti)`, which are the shared initial-condition containers
    other routines will reference later.'
  input_file_module: '`in_init%pest_water` supplies the file name that this reader opens;
    without that configured path there is no source file to scan or load.'
  maximum_data_module: '`db_mx%pestw_ini` stores the number of pesticide-water initial-condition
    blocks found in the file, which becomes a database-size limit for later use and other
    code can consult it to know how many entries were loaded.'
  channel_data_module: The module is imported because the pesticide initial conditions loaded
    here are part of channel/reservoir constituent setup, even though this subroutine does
    not reference a specific channel-data symbol directly in the extracted lines.
  hydrograph_module: This reader is part of a broader routing/init workflow; the module is
    available so downstream hydrograph calculations can later consume the loaded initial pesticide
    state, even though no hydrograph symbol is referenced in the routine body.
  sd_channel_module: The import keeps the routine in the same shared initialization context
    as stream/deep-channel state that can depend on pesticide initial conditions later, even
    though no sd-channel symbol is touched here.
  organic_mineral_mass_module: The routine participates in constituent initialization, so
    this mass module is part of the shared state environment that later uses the loaded pesticide
    concentrations, although no direct symbol from it is read or written here.
---

<!-- facts:header -->

Reads the channel/reservoir pesticide initial-condition file and loads per-pesticide water and benthic starting concentrations into shared module arrays.

## Bottom Line

`pest_cha_res_read` opens the file named by `in_init%pest_water`, scans it once to count how many initial-condition blocks it contains, allocates `pest_water_ini` and `pest_init_name` to that size, then rewinds the file and reads each block into shared state. The data it loads are the pesticide names plus water and benthic initial concentrations for each pesticide listed in `cs_db%num_pests`.

This matters because later channel, reservoir, and related constituent routines need those initialized pesticide concentrations and the file-count limit stored in `db_mx%pestw_ini`. If the configured file is missing or set to `'null'`, the routine does nothing and leaves the shared arrays unchanged.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization, when the configured pesticide-water initial-condition file needs to be parsed into shared memory. The upstream setup is the input-file configuration in `in_init%pest_water` together with the pesticide count in `cs_db%num_pests`; the results are then available to later channel/reservoir constituent initialization and simulation code that uses `pest_water_ini`, `pest_init_name`, and `db_mx%pestw_ini`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local state and check whether to process the file | Sets scratch variables and uses `inquire` on `in_init%pest_water` to decide whether the configured file exists or the configured path is not the literal `'null'`. |
| 2. Open the pesticide initial-condition file and skip title/header records | Opens unit 107 on `in_init%pest_water`, reads the title line into `titldum`, then reads the header line into `header` before starting the scan. |
| 3. Count how many initial-condition blocks are present | Loops through the file, reading each block name and then `cs_db%num_pests` pairs of pesticide records, incrementing `imax` once per block until end-of-file is reached. |
| 4. Store the block count and allocate shared arrays | Copies the block count into `db_mx%pestw_ini`, allocates `pest_water_ini(imax)` and `pest_init_name(imax)`, and allocates each block's `water` and `benthic` arrays with zero initialization. |
| 5. Rewind the file and skip the title/header again | Repositions unit 107 to the start of `pest_water.ini` and rereads the title and header so the second pass begins at the first block. |
| 6. Load each block name and concentration arrays | Reads each block name into `pest_init_name(ipesti)` and then reads the block's water and benthic concentration arrays into `pest_water_ini(ipesti)`. |
| 7. Close the input file and exit | Closes unit 107, leaves the gate loop, and returns to the caller with the initialized pesticide state in shared modules. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_db, pest_water_ini, pest_init_name` | `cs_db%num_pests, pest_water_ini(ipesti)%water, pest_water_ini(ipesti)%benthic` |
| [sym:input_file_module] | `in_init` | `in_init%pest_water` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pestw_ini` |
| [sym:channel_data_module] | `channel data types and state imported by `use channel_data_module`` | `none used directly in this routine` |
| [sym:hydrograph_module] | `hydrograph state and types imported by `use hydrograph_module`` | `none used directly in this routine` |
| [sym:sd_channel_module] | `sd-channel state and types imported by `use sd_channel_module`` | `none used directly in this routine` |
| [sym:organic_mineral_mass_module] | `organic/mineral mass state and types imported by `use organic_mineral_mass_module`` | `none used directly in this routine` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%pestw_ini` | After the scan loop finishes and before allocation, when the file contains one or more initial-condition blocks | The routine records the number of pesticide-water initial-condition blocks found in `pest_water.ini`. This size is used to define how many `pest_water_ini` and `pest_init_name` entries are allocated and loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-changing updates after the file was introduced in `df07e3f`: `16e54aa` collapsed two separate reads into one combined read for `titldum`, `pest_water_ini(ipesti)%water`, and `pest_water_ini(ipesti)%benthic`; `f8bb6ec` added zero-initialization to `pest_water_ini(ipesti)%water`; and `39fabde` initialized local scalars and also zero-initialized `pest_water_ini(ipesti)%benthic`. The original `df07e3f` commit created the routine with the two-pass count-and-load design, file rewind, array allocation, and `db_mx%pestw_ini` assignment.

- `df07e3f` introduced the routine, including the file scan/count pass, `db_mx%pestw_ini = imax`, allocation of `pest_water_ini` and `pest_init_name`, and the second pass that loads the data from `pest_water.ini`.
- `16e54aa` changed the load phase to read `titldum`, `pest_water_ini(ipesti)%water`, and `pest_water_ini(ipesti)%benthic` in a single record read instead of two separate reads.
- `f8bb6ec` zero-initialized `pest_water_ini(ipesti)%water` at allocation time.
- `39fabde` initialized `titldum`, `header`, `eof`, `imax`, `ipest`, and `ipesti` to default values and also zero-initialized `pest_water_ini(ipesti)%benthic` at allocation time.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pest_cha_res_read' has no extracted documentation comment.
- algorithm_steps revised: merged the original scan/allocation split into clearer count, allocate, and load phases to match the source flow.
