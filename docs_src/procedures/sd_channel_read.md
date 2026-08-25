---
kind: procedure
symbol: sd_channel_read
title: sd_channel_read
status: filled
source_hash: be9013a6f2e3c7a4
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the file title line from `channel-lte.cha`
    before processing data rows.
  header: Scratch character buffer used to read and discard the file header line from `channel-lte.cha`
    before processing data rows.
  eof: '`iostat` status flag for each read from `channel-lte.cha`; negative values terminate
    the scan/read loops at end of file.'
  imax: Tracks the largest channel-deg record index found while scanning the file so the routine
    can size `sd_dat` and store the count in `db_mx%sdc_dat`.
  i_exist: Logical inquiry result that tells the routine whether `in_cha%chan_ez` exists;
    if false or set to `null`, the routine skips reading the file.
  ichi: Loop counter over channel-deg records during the second pass through `channel-lte.cha`.
  isp_ini: Loop counter over available channel initial-condition definitions in `ch_init`
    when matching `sd_dat(ichi)%initc`.
  ics: Generic loop counter reused for nested lookups of organic-mineral, pesticide, pathogen,
    salt, and constituent initial-condition names.
  inut: Loop counter over `db_mx%ch_nut` when matching the nutrient input file name `sd_dat(ichi)%nutc`.
  ihydsed: Loop counter over hydraulic/sediment file lists (`db_mx%ch_lte` and `db_mx%ch_sednut`)
    when matching `sd_dat(ichi)%hydc`.
  i: Record index read from the file during the first scan pass; also used as the array index
    for `sd_dat(i)` during the data pass.
  k: First integer field read from each data record in the file; the routine reads it before
    the channel name and file-name fields.
  isalt: Loop counter over salt-ion names when initializing salt-related crosswalks inside
    the nested channel setup.
uses:
  basin_module: This module is imported by the routine, but the provided evidence does not
    resolve a specific `basin_module` symbol used in the shown lines. It likely supplies broader
    basin-wide state needed elsewhere in the subroutine body, but that use is not visible
    in the extracted references.
  input_file_module: '`in_cha%chan_ez` provides the configured filename for the channel-lte
    input table. The routine uses it to decide whether to open `channel-lte.cha` and to form
    the file path for the read pass.'
  maximum_data_module: '`db_mx` holds the record counts that control allocation and crosswalk
    loops. `sdc_dat` stores how many channel-deg data rows were found, `ch_init` bounds the
    search over channel initial-condition definitions, and `om_water_init` bounds the lookup
    for organic-mineral initial names.'
  channel_data_module: '`ch_init` supplies the channel initial-condition catalog that `sd_channel_read`
    matches against each record''s `initc` field. The `name` and `org_min` components are
    used to resolve the record''s initial-condition reference and the organic-mineral initial-state
    crosswalk.'
  channel_velocity_module: The module is imported in the routine, but no specific symbol from
    it appears in the extracted reference list. It matters because channel-deg reading allocates
    velocity-related state, yet the exact referenced component is not visible in the provided
    evidence.
  ch_pesticide_module: This module defines the pesticide hydrograph containers that are allocated
    and initialized when pesticides are simulated. `sd_channel_read` needs them so channel-deg
    setup can create the daily, monthly, yearly, and annual pesticide storage for each channel
    object.
  ch_salt_module: This module provides the salt balance storage that the routine allocates
    per channel and per salt ion. The read/setup pass initializes these arrays so later channel
    routing can accumulate salt inputs, outputs, irrigation losses, water mass, and concentration.
  ch_cs_module: This module is the parallel storage for non-pesticide constituents (`cs`)
    in channels. `sd_channel_read` allocates and zeroes these balances so the routing code
    can later record daily, monthly, yearly, and annual constituent mass and concentration.
  sd_channel_module: This module owns the SWAT-deg channel dynamic state and the channel-deg
    data-file table. `sd_channel_read` fills `sd_dat` with file crosswalks and allocates `sd_ch`
    mixing arrays so downstream channel-deg logic has the metadata and per-channel storage
    it needs.
  hydrograph_module: '`sp_ob%chandeg` sets the number of swat-deg channel objects, which determines
    the bounds for all channel-deg allocations and loops in this routine.'
  constituent_mass_module: This module provides the counts of simulated constituent groups
    and the channel water/benthic storage containers. `sd_channel_read` uses those counts
    to decide which arrays to allocate and zero for pest, pathogen, metal, salt, and general
    constituent tracking.
  pesticide_data_module: The module is imported, but no specific pesticide-database symbol
    from it is resolved in the extracted references. It matters because pesticide-related
    channel arrays are initialized here, but the exact database crosswalk symbol is not visible
    in the evidence.
  pathogen_data_module: The module is imported, but no specific pathogen-database symbol from
    it is resolved in the extracted references. It matters because pathogen-related channel
    arrays are part of the constituent setup, though the exact database symbol is not shown.
  water_body_module: The module is imported, but no specific water-body symbol from it is
    resolved in the extracted references. It likely supports broader channel-water initialization,
    but the exact dependency is not visible in the provided lines.
---

<!-- facts:header -->

Reads and initializes the channel-lte input table for SWAT+ channel-deg/stream-deg processing. It sizes the channel dynamic state arrays, crosswalks initial-condition and hydrology file names, and loads per-channel metadata used later in routing and constituent accounting.

## Bottom Line

`sd_channel_read` is a setup routine, not a simulation step. It allocates the channel-deg state containers, checks whether `in_cha%chan_ez` points to a real `channel-lte.cha` file, counts how many channel-deg records it contains, and then reads those records into `sd_dat` and related module arrays.

It matters because later channel-deg behavior depends on the file-name crosswalks and the per-channel flags established here: initial conditions (`initc`/`init`), hydraulic and sediment inputs (`hydc`, `sedc`, `nutc`), and the optional constituent arrays for pesticides, salts, and other constituents.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`sd_channel_read` runs during channel initialization, after the channel input readers (`ch_read_init`, `ch_read_init_cs`, `sd_hydsed_read`, `ch_read_hyd`, `ch_read_sed`, `ch_read_nut`, `ch_read`) have prepared the broader channel data environment. `proc_cha` calls it before `sd_hydsed_init` and before aquifer-to-channel initialization, so its results feed the later hydraulic setup and the channel constituent/routing behavior that depends on `sd_dat`, `sd_ch`, and the allocated balance arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Allocate channel-deg state containers | Allocates the major channel, storage, flow, pesticide, salt, and constituent arrays to the size implied by `sp_ob%chandeg` before any file reading begins. |
| 2. Allocate hydrograph-separation storage | Creates `ch_stor_hdsep` and initializes `hyd_sep_array` so hydrograph-separation tracking starts from zero. |
| 3. Allocate constituent-specific arrays when simulated | Uses `cs_db` counts to conditionally allocate pesticide, salt, and general-constituent buffers, then zeros the per-ion/per-constituent balance fields for each channel object. |
| 4. Check whether the channel-lte file exists | Queries `in_cha%chan_ez`; if the file is missing or set to `null`, the routine allocates a minimal `sd_dat` table and skips the file read path. |
| 5. Scan the file to find the maximum record index | Opens `channel-lte.cha`, skips the title and header lines, reads record indices, and tracks the maximum index in `imax` so the `sd_dat` array can be sized correctly. |
| 6. Save the record count and allocate `sd_dat` | Copies the maximum index into `db_mx%sdc_dat` and allocates `sd_dat(0:imax)` for the second pass through the file. |
| 7. Rewind and restart the file pass | Rewinds unit 105 and rereads the title and header lines so the routine can parse the data rows from the start of the file. |
| 8. Read each channel-lte record into `sd_dat` | Reads the record index, backs up one line, then reads the channel name and input-file crosswalks (`name`, `initc`, `hydc`, `sedc`, `nutc`) into the corresponding `sd_dat(i)` entry. |
| 9. Resolve initial-condition and input-file crosswalks | Matches each record's `initc`, `hydc`, and `nutc` values against the appropriate module tables and stores the resolved indices in `sd_dat`, `sd_init`, and related lookup arrays. |
| 10. Close the input file and return | Closes unit 105 and exits the subroutine after all channel-lte records have been read and linked. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:input_file_module] | `in_cha` | `in_cha%chan_ez` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%sdc_dat, db_mx%ch_init, db_mx%om_water_init` |
| [sym:channel_data_module] | `ch_init` | `ch_init(isp_ini)%name, ch_init(isp_ini)%org_min` |
| [sym:channel_velocity_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:ch_pesticide_module] | `chpst, chpstz, bchpst_d, bchpst_m, bchpst_y, bchpst_a, chpst_d, chpst_m, chpst_y, chpst_a` | `chpst%pest, chpstz%pest, bchpst_d%pest, bchpst_m%pest, bchpst_y%pest, bchpst_a%pest, chpst_d(ich)%pest, chpst_m(ich)%pest, chpst_y(ich)%pest, chpst_a(ich)%pest` |
| [sym:ch_salt_module] | `chsalt_d, chsalt_m, chsalt_y, chsalt_a` | `chsalt_d(ich)%salt, chsalt_m(ich)%salt, chsalt_y(ich)%salt, chsalt_a(ich)%salt, chsalt_m(ich)%salt(isalt)%tot_in, chsalt_m(ich)%salt(isalt)%tot_out, chsalt_m(ich)%salt(isalt)%irr, chsalt_m(ich)%salt(isalt)%water, chsalt_m(ich)%salt(isalt)%conc, chsalt_y(ich)%salt(isalt)%tot_in, chsalt_y(ich)%salt(isalt)%tot_out, chsalt_y(ich)%salt(isalt)%irr, chsalt_y(ich)%salt(isalt)%water, chsalt_y(ich)%salt(isalt)%conc, chsalt_a(ich)%salt(isalt)%tot_in, chsalt_a(ich)%salt(isalt)%tot_out, chsalt_a(ich)%salt(isalt)%irr, chsalt_a(ich)%salt(isalt)%water, chsalt_a(ich)%salt(isalt)%conc` |
| [sym:ch_cs_module] | `chcs_d, chcs_m, chcs_y, chcs_a` | `chcs_d(ich)%cs, chcs_m(ich)%cs, chcs_y(ich)%cs, chcs_a(ich)%cs, chcs_m(ich)%cs(ics)%tot_in, chcs_m(ich)%cs(ics)%tot_out, chcs_m(ich)%cs(ics)%irr, chcs_m(ich)%cs(ics)%water, chcs_m(ich)%cs(ics)%conc, chcs_y(ich)%cs(ics)%tot_in, chcs_y(ich)%cs(ics)%tot_out, chcs_y(ich)%cs(ics)%irr, chcs_y(ich)%cs(ics)%water, chcs_y(ich)%cs(ics)%conc, chcs_a(ich)%cs(ics)%tot_in, chcs_a(ich)%cs(ics)%tot_out, chcs_a(ich)%cs(ics)%irr, chcs_a(ich)%cs(ics)%water, chcs_a(ich)%cs(ics)%conc` |
| [sym:sd_channel_module] | `sd_ch, sd_dat` | `sd_ch(ich)%aq_mix, sd_dat(i)%name, sd_dat(i)%initc, sd_dat(i)%hydc, sd_dat(i)%sedc, sd_dat(i)%nutc, sd_dat(ichi)%initc, sd_dat(ichi)%init` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%chandeg` |
| [sym:constituent_mass_module] | `cs_db, ch_water, ch_benthic` | `cs_db%num_pests, ch_water(ich)%pest, ch_benthic(ich)%pest, cs_db%num_paths, ch_water(ich)%path, ch_benthic(ich)%path, cs_db%num_metals, ch_water(ich)%hmet, ch_benthic(ich)%hmet, cs_db%num_salts, ch_water(ich)%salt, ch_water(ich)%saltc, ch_benthic(ich)%salt, cs_db%num_cs, ch_water(ich)%cs, ch_water(ich)%csc, ch_benthic(ich)%cs` |
| [sym:pesticide_data_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:pathogen_data_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:water_body_module] | `No candidate outside references were resolved to this module.` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hyd_sep_array` | When the routine starts, before any file data are read | `hyd_sep_array` is allocated with zeros and explicitly reset so later hydrograph-separation calculations begin from a clean zero state. |
| `chsalt_m(ich)%salt(isalt)%tot_in` | When `cs_db%num_salts > 0` and the per-channel salt arrays are allocated | `chsalt_m(ich)%salt(isalt)%tot_in` is initialized to zero so monthly salt inflow accounting starts from no accumulated mass. |
| `chsalt_m(ich)%salt(isalt)%tot_out` | When `cs_db%num_salts > 0` and the per-channel salt arrays are allocated | `chsalt_m(ich)%salt(isalt)%tot_out` is initialized to zero so monthly salt outflow accounting starts from no accumulated mass. |
| `chsalt_m(ich)%salt(isalt)%irr` | When `cs_db%num_salts > 0` and the per-channel salt arrays are allocated | `chsalt_m(ich)%salt(isalt)%irr` is initialized to zero so monthly irrigation salt loss accounting starts from no accumulated mass. |
| `chsalt_m(ich)%salt(isalt)%water` | When `cs_db%num_salts > 0` and the per-channel salt arrays are allocated | `chsalt_m(ich)%salt(isalt)%water` is initialized to zero so monthly salt storage in channel water starts from no residue. |
| `chsalt_m(ich)%salt(isalt)%conc` | When `cs_db%num_salts > 0` and the per-channel salt arrays are allocated | `chsalt_m(ich)%salt(isalt)%conc` is initialized to zero so monthly salt concentration starts from no prior value. |
| `chsalt_y(ich)%salt(isalt)%tot_in` | When `cs_db%num_salts > 0` and the yearly salt arrays are allocated | `chsalt_y(ich)%salt(isalt)%tot_in` is initialized to zero so yearly salt inflow accounting starts cleanly. |
| `chsalt_y(ich)%salt(isalt)%tot_out` | When `cs_db%num_salts > 0` and the yearly salt arrays are allocated | `chsalt_y(ich)%salt(isalt)%tot_out` is initialized to zero so yearly salt outflow accounting starts cleanly. |
| `chsalt_y(ich)%salt(isalt)%irr` | When `cs_db%num_salts > 0` and the yearly salt arrays are allocated | `chsalt_y(ich)%salt(isalt)%irr` is initialized to zero so yearly irrigation salt loss accounting starts cleanly. |
| `chsalt_y(ich)%salt(isalt)%water` | When `cs_db%num_salts > 0` and the yearly salt arrays are allocated | `chsalt_y(ich)%salt(isalt)%water` is initialized to zero so yearly salt water storage starts cleanly. |
| `chsalt_y(ich)%salt(isalt)%conc` | When `cs_db%num_salts > 0` and the yearly salt arrays are allocated | `chsalt_y(ich)%salt(isalt)%conc` is initialized to zero so yearly salt concentration starts cleanly. |
| `chsalt_a(ich)%salt(isalt)%tot_in` | When `cs_db%num_salts > 0` and the annual salt arrays are allocated | `chsalt_a(ich)%salt(isalt)%tot_in` is initialized to zero so annual salt inflow accounting starts cleanly. |
| `chsalt_a(ich)%salt(isalt)%tot_out` | When `cs_db%num_salts > 0` and the annual salt arrays are allocated | `chsalt_a(ich)%salt(isalt)%tot_out` is initialized to zero so annual salt outflow accounting starts cleanly. |
| `chsalt_a(ich)%salt(isalt)%irr` | When `cs_db%num_salts > 0` and the annual salt arrays are allocated | `chsalt_a(ich)%salt(isalt)%irr` is initialized to zero so annual irrigation salt loss accounting starts cleanly. |
| `chsalt_a(ich)%salt(isalt)%water` | When `cs_db%num_salts > 0` and the annual salt arrays are allocated | `chsalt_a(ich)%salt(isalt)%water` is initialized to zero so annual salt water storage starts cleanly. |
| `chsalt_a(ich)%salt(isalt)%conc` | When `cs_db%num_salts > 0` and the annual salt arrays are allocated | `chsalt_a(ich)%salt(isalt)%conc` is initialized to zero so annual salt concentration starts cleanly. |
| `ch_water(ich)%salt` | When `cs_db%num_salts > 0` and the per-channel water constituent arrays are allocated | `ch_water(ich)%salt` is zeroed so the channel-water salt-mass container begins with no salt mass stored. |
| `ch_water(ich)%saltc` | When `cs_db%num_salts > 0` and the per-channel water constituent arrays are allocated | `ch_water(ich)%saltc` is zeroed so the channel-water salt concentration container begins with no concentration stored. |
| `chcs_m(ich)%cs(ics)%tot_in` | When `cs_db%num_cs > 0` and the monthly constituent arrays are allocated | `chcs_m(ich)%cs(ics)%tot_in` is initialized to zero so monthly constituent inflow accounting starts cleanly. |
| `chcs_m(ich)%cs(ics)%tot_out` | When `cs_db%num_cs > 0` and the monthly constituent arrays are allocated | `chcs_m(ich)%cs(ics)%tot_out` is initialized to zero so monthly constituent outflow accounting starts cleanly. |
| `chcs_m(ich)%cs(ics)%irr` | When `cs_db%num_cs > 0` and the monthly constituent arrays are allocated | `chcs_m(ich)%cs(ics)%irr` is initialized to zero so monthly constituent irrigation-loss accounting starts cleanly. |
| `chcs_m(ich)%cs(ics)%water` | When `cs_db%num_cs > 0` and the monthly constituent arrays are allocated | `chcs_m(ich)%cs(ics)%water` is initialized to zero so monthly constituent water storage starts cleanly. |
| `chcs_m(ich)%cs(ics)%conc` | When `cs_db%num_cs > 0` and the monthly constituent arrays are allocated | `chcs_m(ich)%cs(ics)%conc` is initialized to zero so monthly constituent concentration starts cleanly. |
| `chcs_y(ich)%cs(ics)%tot_in` | When `cs_db%num_cs > 0` and the yearly constituent arrays are allocated | `chcs_y(ich)%cs(ics)%tot_in` is initialized to zero so yearly constituent inflow accounting starts cleanly. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `sd_channel_read`. The initial addition in `df07e3f` introduced the subroutine with channel-deg allocations, file scanning, and crosswalk logic. Commit `94b6dec` carried that source into the repository and the later `f8bb6ec` change added zero-initialization for several `ch_water` salt and constituent allocations while `39fabde` initialized local scalars and `hyd_sep_array` more explicitly, also converting some allocations to use `source = 0.`.

- `df07e3f` added the full `sd_channel_read` implementation, including the channel-lte file scan/read workflow, array allocations, and the initial-condition/hydrology crosswalks into `sd_dat` and related module state.
- `94b6dec` shows the routine already performing the same two-pass file scan and record loading; it documents the original integration of the channel-deg reader into the source tree.
- `f8bb6ec` changed the allocation pattern for `ch_water(ich)%path`, `ch_water(ich)%salt`, `ch_benthic(ich)%salt`, `ch_water(ich)%cs`, and `ch_benthic(ich)%cs` to use `source = 0.`, ensuring those arrays start zeroed when the simulated constituent dimensions are present.
- `39fabde` initialized `titldum`, `header`, `eof`, `imax`, `ichi`, `isp_ini`, `ics`, `inut`, `ihydsed`, `i`, `k`, and `isalt` at declaration and changed `hyd_sep_array` allocation to include `source = 0.` before setting it to zero again.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sd_channel_read' has no extracted documentation comment.
- algorithm_steps revised: compressed the earlier scan/allocation/read sequence into 10 source-backed steps aligned to the visible line ranges.
- Source evidence does not resolve specific imported symbols for `basin_module`, `channel_velocity_module`, `pesticide_data_module`, `pathogen_data_module`, or `water_body_module`; their why-fields are therefore limited to the visible allocation/setup context.
- The `basin_module` dependency is uncertain in the extracted references; avoid claiming a concrete symbol use beyond the imported-module role.
