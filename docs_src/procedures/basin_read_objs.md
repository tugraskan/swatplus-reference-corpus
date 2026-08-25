---
kind: procedure
symbol: basin_read_objs
title: basin_read_objs
status: filled
source_hash: 2fda470f019f83c2
version_label: SWAT+ 62.0.0
locals:
  titldum: Title string read from `object.cnt`; it is used as the first record and then discarded,
    serving as a header/title placeholder during file scanning.
  header: Generic 80-character line buffer used to skip or capture header records in `object.cnt`
    and `chancell.gw` before the routine reads structured data.
  eof: I/O status flag for sequential reads; `0` means keep reading, negative values end the
    scan, and it is reset before counting gwflow records.
  nriv: Counter for the number of gwflow river-cell records found in `chancell.gw`; it becomes
    the value assigned to `sp_ob%gwflow`.
  riv_id: Temporary integer read from each gwflow channel-cell record while counting rows
    in `chancell.gw`; its value is not otherwise used.
  i_exist: Logical file-existence flag set by `inquire`; it determines whether the configured
    input file or `chancell.gw` is available before reading continues.
uses:
  hydrograph_module: '`hydrograph_module` supplies `sp_ob`, the shared spatial-object counter
    record that this routine reads and updates. The routine uses its components to determine
    how many basin objects exist and to rewrite the gwflow and aquifer counts that downstream
    object allocation depends on.'
  input_file_module: '`input_file_module` supplies the configured filenames `in_sim%object_cnt`,
    `in_con%gwflow_con`, and `in_con%aqu_con`. The routine uses these names to open the object-count
    file and to switch connection-file references when gwflow is activated or aquifers are
    disabled.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` matters because this routine
    allocates `obom(sp_ob%objs)`, the per-object organic/mineral mass storage used later by
    mass-balance and routing code.'
  constituent_mass_module: '`constituent_mass_module` matters because it defines `obcs_alloc`,
    the allocation-tracking array that is sized here alongside the object count so later constituent-loading
    code can tell which objects have basin constituent storage initialized.'
  basin_module: '`basin_module` provides basin-wide inputs and control flags, especially `bsn_cc%gwflow`,
    which gates whether the gwflow-specific record scan and file reassignment logic runs at
    all.'
  gwflow_module: '`gwflow_module` matters because it provides `out_gw`, the output unit used
    to create the gwflow record file when gwflow is active.'
---

<!-- facts:header -->

Reads basin object connectivity from object.cnt, adjusts object counts for gwflow when needed, and allocates the basin object arrays. It also writes a gwflow record file when gwflow is active.

## Bottom Line

`basin_read_objs` is an initialization routine called by `proc_bsn` after basin control codes are read. It loads the object-count/connectivity information from `object.cnt`, checks whether gwflow should add river-cell objects from `chancell.gw`, and then allocates the basin object arrays sized to the final object count.

If gwflow is active and a channel-cell file is present, the routine derives `sp_ob%gwflow` by counting records in `chancell.gw`, updates `sp_ob%objs`, and switches connection-file state so later code uses `gwflow.con` and disables aquifer connectivity. It also creates `gwflow_record` through `out_gw` for gwflow tracing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin setup, immediately after `basin_read_cc` in `proc_bsn` and before time and parameter readers. Its results determine the final object count, connection-file selection, and allocation sizes used by later basin, routing, constituent, and gwflow processing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine asks whether the configured `object.cnt` file exists and is not set to the sentinel name `null`; if not, it prints an error message and stops execution. |
| 2. Read object definitions | It opens `object.cnt` on unit 107, reads title and header lines, then reads `bsn` and `sp_ob` records until end-of-file is reached, and finally closes the file. |
| 3. Apply gwflow-specific adjustments | If `bsn_cc%gwflow` is active, the routine looks for `chancell.gw`; when present it may count gwflow river cells, set `sp_ob%gwflow`, grow `sp_ob%objs`, switch `in_con%gwflow_con`, and disable aquifer connectivity, then it writes the gwflow record file on `out_gw`. |
| 4. Allocate basin object storage | Using the final `sp_ob%objs` value, the routine allocates `ob`, `obcs`, `obcs_alloc`, and `obom`, and initializes `obcs_alloc` to zero. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%gwflow, sp_ob%objs, sp_ob%aqu` |
| [sym:input_file_module] | `in_sim, in_con` | `in_sim%object_cnt, in_con%gwflow_con, in_con%aqu_con` |
| [sym:organic_mineral_mass_module] | `ob` | `ob, obom` |
| [sym:constituent_mass_module] | `obcs_alloc` |  |
| [sym:basin_module] | `bsn_cc, bsn` | `bsn_cc%gwflow` |
| [sym:gwflow_module] | `out_gw` | `out_gw` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sp_ob%gwflow` | When `chancell.gw` exists, `bsn_cc%gwflow == 1`, and `sp_ob%gwflow == 0` before the gwflow scan | It is set to the counted number of gwflow river cells (`nriv`) so the shared spatial-object totals include gwflow objects. |
| `sp_ob%objs` | After gwflow cell counting completes and `sp_ob%gwflow` is known | It is increased by `nriv - sp_ob%aqu` so the total object count reflects the added gwflow objects while removing the aquifer objects they replace. |
| `in_con%gwflow_con` | When gwflow is activated from the channel-cell file | It is reassigned to `gwflow.con` so downstream code reads gwflow connectivity from the gwflow-specific connection file. |
| `sp_ob%aqu` | When `chancell.gw` exists and `sp_ob%gwflow == 0` | It is reset to `0` because the gwflow objects are being used instead of aquifer objects in the spatial-object layout. |
| `in_con%aqu_con` | When `chancell.gw` exists and `sp_ob%gwflow == 0` | It is set to `null` so the aquifer connection file is suppressed after gwflow objects are substituted in. |
| `bsn_cc%gwflow` | When `chancell.gw` is missing or its header read fails while gwflow is expected | It is forced to `0` to deactivate gwflow for the run, preventing later code from using missing gwflow input. |
| `obcs_alloc` | At the end of the routine after the final object count is known | It is allocated to the size of `sp_ob%objs` and filled with zeros so constituent/object bookkeeping starts from a known unallocated state per object. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `basin_read_objs`: df07e3f added the routine with file scanning, gwflow handling, and allocations; 39fabde initialized local scalars and changed `obcs_alloc` to allocate with `source = 0`; 3cc92b5 renamed the gwflow channel-cell file from `gwflow.chancells` to `chancell.gw`; and 2ee1889 only reformatted the end of the subroutine without changing behavior.

- df07e3f introduced the full routine logic for reading `object.cnt`, conditionally processing gwflow channel-cell input, writing `gwflow_record`, and allocating basin object storage.
- 39fabde added default initial values for `titldum`, `header`, `eof`, `nriv`, and `riv_id`, and changed `obcs_alloc` to allocate with `source = 0` before the explicit zero assignment.
- 3cc92b5 changed the gwflow file name used by the routine from `gwflow.chancells` to `chancell.gw` in both the `inquire` and `open` statements.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_read_objs' has no extracted documentation comment.
- algorithm_steps revised: split the original scan step into object-definition reading and gwflow adjustment so each step matches a distinct source region.
