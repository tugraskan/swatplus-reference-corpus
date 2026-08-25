---
kind: procedure
symbol: path_cha_res_read
title: path_cha_res_read
status: filled
source_hash: f6d10b173caafba9
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to consume title/label lines and unused text fields
    while scanning and rereading `path_water.ini`.
  header: Scratch character buffer for the record that carries each initialization block's
    header/name line before the actual data values are read.
  ipathi: Loop index over the allocated initial-condition blocks in `path_water_ini` and `path_init_name`.
  eof: I/O status flag returned by `read(...,iostat=eof)`; the routine uses negative values
    to stop at end-of-file and zero to continue scanning.
  imax: Count of how many path-water initial-condition blocks are found in the file; later
    used to size `path_water_ini`, `path_init_name`, and `db_mx%pathw_ini`.
  i_exist: Logical existence flag from `inquire`; it gates whether the configured file path
    should be processed at all.
  ipath: Inner loop index over `cs_db%num_paths` while scanning each block's water and benthic
    records to count complete entries.
uses:
  constituent_mass_module: This module defines how many pathogen/constituent paths must be
    read (`cs_db%num_paths`) and owns the allocatable arrays that receive the loaded initial
    concentrations and record names. The routine sizes and fills those arrays, so it must
    use this shared constituent-mass state.
  input_file_module: '`in_init%path_water` supplies the file name to open. Without the input-file
    configuration, the routine would not know which `path_water.ini` file to read.'
  maximum_data_module: '`db_mx%pathw_ini` stores the number of path-water initialization records
    found during the scan. Other routines can use that maximum-data count to size or iterate
    over the loaded initial-condition database.'
  channel_data_module: This module is imported by the routine, but the provided source span
    shows no direct references to its symbols. It may be present because the path-water initialization
    data are part of the broader channel-state setup, even though no specific symbol from
    this module is used here.
  hydrograph_module: This module is imported by the routine, but no symbols from it appear
    in the extracted source lines. It likely matters to downstream channel/hydrologic state
    initialization, even though this reader itself does not reference a visible hydrograph
    object.
  sd_channel_module: This module is imported by the routine, but the extracted lines do not
    reference any of its symbols. It is still relevant because the loaded channel-path initial
    conditions may feed stream/landscape channel state managed elsewhere.
  organic_mineral_mass_module: This module is imported by the routine, but no visible symbols
    from it are used in the shown source. It likely belongs to the larger constituent-mass
    initialization context that this reader supports.
---

<!-- facts:header -->

Reads the channel/reservoir path water initial-condition file and loads the per-pathogen water and benthic starting concentrations into shared model arrays. It first counts how many records are present, then allocates storage and rereads the file to populate names and values.

## Bottom Line

`path_cha_res_read` is an input-reader for `path_water.ini`. It opens the file named by `in_init%path_water`, scans past the title/header records, counts how many initial-condition blocks are present, and stores that count in `db_mx%pathw_ini` so the model knows how many path-water initialization records exist.

After sizing the arrays, it rewinds the same file and rereads each block into `path_init_name(ipathi)` plus the per-pathogen concentration arrays `path_water_ini(ipathi)%water` and `path_water_ini(ipathi)%benthic`. Those values become the shared starting concentrations used by the rest of the SWAT+ constituent-mass setup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization, when the path-water initial-condition file named in `in_init%path_water` must be sized and loaded. It depends on the configured file path and on `cs_db%num_paths` being available so it can allocate the correct per-pathogen arrays. Its results, especially `db_mx%pathw_ini` and the populated `path_water_ini` records, feed later constituent-mass initialization and any downstream routine that needs starting pathogen concentrations for channels/reservoir paths.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | Uses `inquire` on `in_init%path_water` and only proceeds when the file exists or the configured path is not the sentinel string `null`. |
| 2. Open and read file prologue | Opens unit 107 on the configured file, reads the title and header records, and resets the block counter `imax` before scanning data blocks. |
| 3. Count complete initialization blocks | Loops through the file, reading each block name plus `cs_db%num_paths` water and benthic records, and increments `imax` once per complete block found. |
| 4. Save the discovered block count | Copies the scanned count into `db_mx%pathw_ini` so the maximum-data state records how many path-water initial-condition blocks are present. |
| 5. Allocate storage for loaded data | Allocates `path_water_ini(imax)` and `path_init_name(imax)`, then allocates each block's `water` and `benthic` arrays to length `cs_db%num_paths` with zero initialization. |
| 6. Rewind and skip the file title again | Rewinds unit 107 to the beginning and rereads the title record so the second pass starts from a clean file position. |
| 7. Load each initialization block | For each block, reads the header, the block name, and the water/benthic concentration line into `path_init_name(ipathi)`, `path_water_ini(ipathi)%water`, and `path_water_ini(ipathi)%benthic`. |
| 8. Close the input file | Closes unit 107 after all initialization records are read and stored. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_db, path_water_ini, path_init_name` | `cs_db%num_paths, path_water_ini(ipathi)%water, path_water_ini(ipathi)%benthic` |
| [sym:input_file_module] | `in_init` | `in_init%path_water` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pathw_ini` |
| [sym:channel_data_module] | `not resolved` | `none resolved` |
| [sym:hydrograph_module] | `not resolved` | `none resolved` |
| [sym:sd_channel_module] | `not resolved` | `none resolved` |
| [sym:organic_mineral_mass_module] | `not resolved` | `none resolved` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%pathw_ini` | After scanning `path_water.ini` and finding `imax` complete initialization blocks | Records the number of path-water initial-condition entries available in the input file so later initialization code can use the correct count. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `path_cha_res_read`. The initial add (`df07e3f`) created the reader, including the file scan, allocation, rewind, and data-loading logic. Commit `16e54aa` merged the two separate reads for water and benthic values into one read statement. Commit `f8bb6ec` added `source = 0.` when allocating `path_water_ini(ipathi)%water`, and `39fabde` extended that zero-initialization to `titldum`, `header`, `ipathi`, `eof`, `imax`, `ipath`, and `path_water_ini(ipathi)%benthic`.

- `df07e3f` introduced the subroutine and its file-driven two-pass loading pattern, including the `db_mx%pathw_ini` count and allocation of `path_water_ini`/`path_init_name`.
- `16e54aa` changed the data load so water and benthic arrays are read together from a single record instead of two separate reads.
- `f8bb6ec` made the water array allocation explicitly zero-initialized.
- `39fabde` zero-initialized the local scratch variables and the benthic array allocation, reducing uninitialized-state risk during file parsing.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'path_cha_res_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the original five draft steps into eight source-backed steps to reflect the actual two-pass read pattern and the explicit rewind/load sequence.
- The source span imports `channel_data_module`, `hydrograph_module`, `sd_channel_module`, and `organic_mineral_mass_module`, but no direct symbol usage from those modules was visible in the extracted lines; their roles are therefore marked unresolved rather than guessed.
