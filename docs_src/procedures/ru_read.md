---
kind: procedure
symbol: ru_read
title: ru_read
status: filled
source_hash: cb18f618746d93df
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from the top of `rout_unit.rtu` during both the count
    pass and the data load pass.
  header: Temporary header line read after `titldum`; used to skip the file header before
    reading routing unit records.
  eof: IO status flag for reads from unit 107. A negative value ends the scan/load loops at
    end-of-file, while zero indicates a successful read.
  imax: Tracks the largest routing-unit index seen while scanning the file. It is used as
    the maximum database index encountered in `rout_unit.rtu`.
  i_exist: Logical flag returned by `inquire` that tells whether the configured routing-unit
    input file exists.
  i: Routing-unit index read from the file during the scan and load passes. It is used to
    size the database and to select `ru(i)` for loading.
  max: Unused local declaration in the extracted source; no assignment or reference was visible
    in the provided lines.
  k: First field read from each routing-unit record on the second pass. It is read along with
    `ru(i)%name` and `ru(i)%dbsc` and is part of the record format.
  ith: Loop counter used to search the topography and field databases for a name match.
  isalt: Loop counter over salt ions when zero-initializing `ru_hru_saltb_*` entries for each
    routing unit.
  ics: Loop counter over constituents when zero-initializing `ru_hru_csb_*` entries for each
    routing unit.
  ihyd: Loop counter over the five hydrograph slots used to allocate and initialize `rusaltb_*`
    and `rucsb_*` loading arrays.
uses:
  basin_module: The routine imports `basin_module`, so basin-level shared state may participate
    in routing-unit setup; however, the extracted evidence did not resolve any specific basin
    symbol used inside this procedure.
  input_file_module: The `input_file_module` provides `in_ru%ru`, the configured path to `rout_unit.rtu`.
    That value controls whether the file is opened at all and which file is read.
  time_module: The routine imports `time_module`, but the extracted source lines do not show
    a specific time variable being used. The module still matters because routing-unit setup
    runs in the model initialization phase where shared timing state is commonly available.
  ru_module: The routine populates routing-unit state into `ru_module` storage (`ru`, `mru_db`,
    and related arrays). That module is the shared home for the routing-unit database after
    the file is read.
  hydrograph_module: The `hydrograph_module` supplies `sp_ob%ru`, which is the routing-unit
    object count used to size the `ru` arrays and all per-routing-unit balance arrays.
  maximum_data_module: The module is imported even though no specific symbol was resolved
    in the extracted references. It matters because the procedure is part of the data-loading
    phase where model maxima and database sizes are typically established.
  topography_data_module: The routine matches `ru(i)%dbsc%toposub_db` against `topo_db(ith)%name`,
    so topography database contents determine how each routing unit is linked to its topographic
    record.
  constituent_mass_module: The `constituent_mass_module` supplies `cs_db%num_salts` and `cs_db%num_cs`,
    which gate whether salt/constituent arrays are allocated. It also defines the `rusaltb_*`
    and `rucsb_*` hydrograph structures that this routine initializes for routing-unit loading
    bookkeeping.
  salt_module: The `salt_module` provides the routing-unit salt balance arrays `ru_hru_saltb_*`.
    This routine allocates them and zeroes each salt-flux component so later salt routing
    has a clean baseline.
  cs_module: The `cs_module` provides the routing-unit constituent balance arrays `ru_hru_csb_*`.
    This routine allocates them and zeroes each constituent-flux component so later constituent
    routing has a clean baseline.
---

<!-- facts:header -->

Reads and initializes routing-unit data from the `rout_unit.rtu` input file. It also builds the routing-unit salt and constituent balance arrays needed by downstream hydrology and transport routines.

## Bottom Line

ru_read loads the routing unit database: it checks whether the configured `rout_unit.rtu` file exists, scans it to count routing units, then allocates and fills `ru` plus related per-unit state. It also resolves each routing unit's topography and field database links from the names stored in the file.

When salt or constituent transport is enabled, the routine also allocates and zero-initializes the routing-unit loading arrays (`rusaltb_*`, `ru_hru_saltb_*`, `rucsb_*`, and `ru_hru_csb_*`). Those arrays provide the per-routing-unit bookkeeping used later by routing and balance calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during hydrologic connectivity setup, immediately after `hyd_connect` reads the routing-unit connection file and before `ru_read_elements`. `hyd_connect` prepares the routing-unit object counts and connection context; `ru_read` then loads the routing-unit database entries that later routing, topography linking, and salt/constituent bookkeeping depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test the configured file | The routine clears `mru_db`, `eof`, and `imax`, then checks whether `in_ru%ru` exists. If the file is missing or set to `"null"`, it allocates a minimal `ru(0:0)` array and skips file loading. |
| 2. Scan the file to count routing units | The routine opens unit 107 on `in_ru%ru`, reads the title and header, then loops through record indices until end-of-file or a zero index. Each valid record increments `mru_db` and updates `imax` with the largest index seen. |
| 3. Allocate routing-unit and helper arrays | Using `sp_ob%ru`, the routine allocates the routing-unit database arrays `ru`, `ru_d`, `ru_m`, `ru_y`, and `ru_a`, plus `ru_tc`, `ru_n`, and `itsb`, with zero initialization where needed. |
| 4. Allocate salt transport bookkeeping when enabled | If `cs_db%num_salts > 0`, the routine allocates the salt hydrograph arrays `rusaltb_*` and the routing-unit salt balance arrays `ru_hru_saltb_*`. It then allocates per-hydrograph and per-salt slots and zeroes all salt flux fields, including `diss` for the monthly, yearly, and average balance arrays. |
| 5. Allocate constituent transport bookkeeping when enabled | If `cs_db%num_cs > 0`, the routine allocates the constituent hydrograph arrays `rucsb_*` and the routing-unit constituent balance arrays `ru_hru_csb_*`. It then allocates per-hydrograph and per-constituent slots and zeroes all constituent flux fields. |
| 6. Rewind and reread the routing-unit file | The routine rewinds unit 107 and rereads the title and header so it can make a second pass over the file for the actual data load. |
| 7. Load each routing-unit record | For each routing unit, the routine reads the index, backs up one record, then rereads the full line into `k`, `ru(i)%name`, and `ru(i)%dbsc`. |
| 8. Resolve topography and field database references | For each loaded routing unit, the routine searches `topo_db` for `ru(i)%dbsc%toposub_db` and `field_db` for `ru(i)%dbsc%field_db`. On a field match it also copies the field length, width, and angle into `ru(i)%field`. |
| 9. Close the input file and finish | After all routing units are processed, the routine closes unit 107, exits the file-processing loop, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state used by this routine is not explicitly identified in the extracted references.` | `No candidate outside references were resolved to basin_module.` |
| [sym:input_file_module] | `in_ru` | `in_ru%ru` |
| [sym:time_module] | `time_module state used by this routine is not explicitly identified in the extracted references.` | `No candidate outside references were resolved to time_module.` |
| [sym:ru_module] | `ru_module state used by this routine is not explicitly identified in the extracted references.` | `No candidate outside references were resolved to ru_module.` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%ru` |
| [sym:maximum_data_module] | `maximum_data_module state used by this routine is not explicitly identified in the extracted references.` | `No candidate outside references were resolved to maximum_data_module.` |
| [sym:topography_data_module] | `topography_data_module state used by this routine is not explicitly identified in the extracted references.` | `No candidate outside references were resolved to topography_data_module.` |
| [sym:constituent_mass_module] | `cs_db, rusaltb_d, rusaltb_m, rusaltb_y, rusaltb_a, rucsb_d, rucsb_m, rucsb_y, rucsb_a` | `cs_db%num_salts, rusaltb_d(iru)%hd(5), rusaltb_m(iru)%hd(5), rusaltb_y(iru)%hd(5), rusaltb_a(iru)%hd(5), rusaltb_d(iru)%hd(ihyd)%salt, rusaltb_m(iru)%hd(ihyd)%salt, rusaltb_y(iru)%hd(ihyd)%salt, rusaltb_a(iru)%hd(ihyd)%salt, cs_db%num_cs, rucsb_d(iru)%hd(5), rucsb_m(iru)%hd(5), rucsb_y(iru)%hd(5), rucsb_a(iru)%hd(5), rucsb_d(iru)%hd(ihyd)%cs, rucsb_m(iru)%hd(ihyd)%cs, rucsb_y(iru)%hd(ihyd)%cs, rucsb_a(iru)%hd(ihyd)%cs` |
| [sym:salt_module] | `ru_hru_saltb_d, ru_hru_saltb_m, ru_hru_saltb_y, ru_hru_saltb_a` | `ru_hru_saltb_d(iru)%salt, ru_hru_saltb_m(iru)%salt, ru_hru_saltb_y(iru)%salt, ru_hru_saltb_a(iru)%salt, ru_hru_saltb_d(iru)%salt(isalt)%wtsp, ru_hru_saltb_d(iru)%salt(isalt)%irsw, ru_hru_saltb_d(iru)%salt(isalt)%irgw, ru_hru_saltb_d(iru)%salt(isalt)%irwo, ru_hru_saltb_d(iru)%salt(isalt)%rain, ru_hru_saltb_d(iru)%salt(isalt)%dryd, ru_hru_saltb_d(iru)%salt(isalt)%road, ru_hru_saltb_d(iru)%salt(isalt)%fert, ru_hru_saltb_d(iru)%salt(isalt)%amnd, ru_hru_saltb_d(iru)%salt(isalt)%uptk, ru_hru_saltb_m(iru)%salt(isalt)%wtsp, ru_hru_saltb_m(iru)%salt(isalt)%irsw, ru_hru_saltb_m(iru)%salt(isalt)%irgw, ru_hru_saltb_m(iru)%salt(isalt)%irwo, ru_hru_saltb_m(iru)%salt(isalt)%rain, ru_hru_saltb_m(iru)%salt(isalt)%dryd, ru_hru_saltb_m(iru)%salt(isalt)%road, ru_hru_saltb_m(iru)%salt(isalt)%fert, ru_hru_saltb_m(iru)%salt(isalt)%amnd, ru_hru_saltb_m(iru)%salt(isalt)%uptk, ru_hru_saltb_y(iru)%salt(isalt)%wtsp, ru_hru_saltb_y(iru)%salt(isalt)%irsw, ru_hru_saltb_y(iru)%salt(isalt)%irgw, ru_hru_saltb_y(iru)%salt(isalt)%irwo, ru_hru_saltb_y(iru)%salt(isalt)%rain, ru_hru_saltb_y(iru)%salt(isalt)%dryd, ru_hru_saltb_y(iru)%salt(isalt)%road, ru_hru_saltb_y(iru)%salt(isalt)%fert, ru_hru_saltb_y(iru)%salt(isalt)%amnd, ru_hru_saltb_y(iru)%salt(isalt)%uptk, ru_hru_saltb_a(iru)%salt(isalt)%wtsp, ru_hru_saltb_a(iru)%salt(isalt)%irsw, ru_hru_saltb_a(iru)%salt(isalt)%irgw, ru_hru_saltb_a(iru)%salt(isalt)%irwo, ru_hru_saltb_a(iru)%salt(isalt)%rain, ru_hru_saltb_a(iru)%salt(isalt)%dryd, ru_hru_saltb_a(iru)%salt(isalt)%road, ru_hru_saltb_a(iru)%salt(isalt)%fert, ru_hru_saltb_a(iru)%salt(isalt)%amnd, ru_hru_saltb_a(iru)%salt(isalt)%uptk, ru_hru_saltb_m(iru)%salt(1)%diss, ru_hru_saltb_y(iru)%salt(1)%diss, ru_hru_saltb_a(iru)%salt(1)%diss` |
| [sym:cs_module] | `ru_hru_csb_d, ru_hru_csb_m, ru_hru_csb_y, ru_hru_csb_a` | `ru_hru_csb_d(iru)%cs, ru_hru_csb_m(iru)%cs, ru_hru_csb_y(iru)%cs, ru_hru_csb_a(iru)%cs, ru_hru_csb_d(iru)%cs(ics)%sedm, ru_hru_csb_d(iru)%cs(ics)%wtsp, ru_hru_csb_d(iru)%cs(ics)%irsw, ru_hru_csb_d(iru)%cs(ics)%irgw, ru_hru_csb_d(iru)%cs(ics)%irwo, ru_hru_csb_d(iru)%cs(ics)%rain, ru_hru_csb_d(iru)%cs(ics)%dryd, ru_hru_csb_d(iru)%cs(ics)%fert, ru_hru_csb_d(iru)%cs(ics)%uptk` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mru_db` | When `in_ru%ru` exists and is not `"null"`, the scan pass counts at least one valid routing-unit record. | `mru_db` becomes the number of routing-unit records found in `rout_unit.rtu`. That count drives the second pass over the file and determines how many routing-unit records are loaded. |
| `rusaltb_d(iru)%hd(ihyd)%salt` | When `cs_db%num_salts > 0`, during the salt-bookkeeping initialization loop for each routing unit and hydrograph slot. | `rusaltb_d(iru)%hd(ihyd)%salt` is allocated to hold the daily salt hydrograph values for routing unit `iru` and hydrograph slot `ihyd`, then initialized to zero so later salt routing can accumulate values into it. |
| `rusaltb_m(iru)%hd(ihyd)%salt` | When `cs_db%num_salts > 0`, during the salt-bookkeeping initialization loop for each routing unit and hydrograph slot. | `rusaltb_m(iru)%hd(ihyd)%salt` is allocated to hold the monthly salt hydrograph values for routing unit `iru` and hydrograph slot `ihyd`, then initialized to zero for later accumulation. |
| `rusaltb_y(iru)%hd(ihyd)%salt` | When `cs_db%num_salts > 0`, during the salt-bookkeeping initialization loop for each routing unit and hydrograph slot. | `rusaltb_y(iru)%hd(ihyd)%salt` is allocated to hold the yearly salt hydrograph values for routing unit `iru` and hydrograph slot `ihyd`, then initialized to zero for later accumulation. |
| `rusaltb_a(iru)%hd(ihyd)%salt` | When `cs_db%num_salts > 0`, during the salt-bookkeeping initialization loop for each routing unit and hydrograph slot. | `rusaltb_a(iru)%hd(ihyd)%salt` is allocated to hold the average/annual salt hydrograph values for routing unit `iru` and hydrograph slot `ihyd`, then initialized to zero for later accumulation. |
| `ru_hru_saltb_d(iru)%salt(isalt)%wtsp` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%wtsp` is set to zero as the daily wetland-seepage salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%irsw` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%irsw` is set to zero as the daily surface-water irrigation salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%irgw` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%irgw` is set to zero as the daily groundwater irrigation salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%irwo` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%irwo` is set to zero as the daily irrigation-from-outside-the-watershed salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%rain` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%rain` is set to zero as the daily rainfall salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%dryd` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%dryd` is set to zero as the daily dry deposition salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%road` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%road` is set to zero as the daily road-salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%fert` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%fert` is set to zero as the daily fertilizer salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%amnd` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%amnd` is set to zero as the daily amendment salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_d(iru)%salt(isalt)%uptk` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_d(iru)%salt(isalt)%uptk` is set to zero as the daily crop-uptake salt sink term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%wtsp` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%wtsp` is set to zero as the monthly wetland-seepage salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%irsw` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%irsw` is set to zero as the monthly surface-water irrigation salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%irgw` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%irgw` is set to zero as the monthly groundwater irrigation salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%irwo` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%irwo` is set to zero as the monthly irrigation-from-outside-the-watershed salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%rain` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%rain` is set to zero as the monthly rainfall salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%dryd` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%dryd` is set to zero as the monthly dry deposition salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%road` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%road` is set to zero as the monthly road-salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%fert` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%fert` is set to zero as the monthly fertilizer salt input term for salt ion `isalt` in routing unit `iru`. |
| `ru_hru_saltb_m(iru)%salt(isalt)%amnd` | When `cs_db%num_salts > 0`, during the per-salt initialization loop for each routing unit. | `ru_hru_saltb_m(iru)%salt(isalt)%amnd` is set to zero as the monthly amendment salt input term for salt ion `isalt` in routing unit `iru`. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `ru_read`: df07e3f added the routine and its full file-reading/allocation logic; 94b6dec brought the source into the current repository history with the same routing-unit count/load structure; f8bb6ec changed salt and constituent allocations to use `source = 0.` and explicitly zeroed the hydrograph arrays; 39fabde initialized the scalar locals and also added `source = 0.` to `ru_tc`, `ru_n`, and `itsb` plus the salt/constituent hydrograph allocations.

- df07e3f introduced `ru_read` with the scan pass, allocation pass, rewind, record load, and database-name resolution steps that populate routing-unit state from `rout_unit.rtu`.
- 94b6dec shows the imported source retained the same behavior: count valid routing-unit records, allocate arrays sized by `sp_ob%ru`, initialize salt and constituent bookkeeping, then read each routing-unit record and link it to topography and field databases.
- f8bb6ec changed the salt and constituent allocation sections so the per-hydrograph arrays are initialized with `source = 0.` at allocation time before the explicit zero assignments.
- 39fabde initialized local scalars (`titldum`, `header`, `eof`, `imax`, `i`, `k`, `ith`, `isalt`, `ics`, `ihyd`) and added `source = 0.` to the `ru_tc`, `ru_n`, `itsb`, and hydrograph allocation statements.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ru_read' has no extracted documentation comment.
- The extracted source shows `max` declared but not used in the visible lines.
- algorithm_steps revised: collapsed the original overlapping scan/allocation steps into a sequential 9-step flow that matches the visible source order.
