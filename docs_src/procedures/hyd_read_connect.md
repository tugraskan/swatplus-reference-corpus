---
kind: procedure
symbol: hyd_read_connect
title: hyd_read_connect
status: filled
source_hash: 5d6a4482342d4e98
version_label: SWAT+ 62.0.0
args:
  con_file: Name of the connectivity file to open and read; this file provides the object
    records that drive all allocation and initialization in this routine.
  obtyp: Sets the object type assigned to every object in the processed spatial block, such
    as hru or hru_lte, before the record fields are read back from the file.
  nspu1: Defines the first object index in the spatial block that this routine will initialize
    and read from the connection file.
  nspu: Defines how many spatial objects are processed in this call; together with nspu1 it
    sets the inclusive object index range.
  nhyds: Sets the number of hydrograph slots to allocate and read for each object, which controls
    the size of ob(i)%hd and related constituent hydrograph arrays.
  ndsave: Sets the number of days of hydrograph history to keep for subdaily storage, which
    determines the size of the per-object time-series arrays.
locals:
  titldum: Holds the first title line read from the connection file so the routine can advance
    past file header text before reading object data.
  header: Holds the second header line from the connection file, again serving as skipped
    file metadata rather than model state.
  eof: I/O status flag used on reads from unit 107 to detect end-of-file or read failure while
    scanning and rereading the connection file.
  imax: Tracks the maximum record count encountered during the file scan phase; it is reset
    here before the file is processed.
  i_exist: Logical flag returned by inquire to decide whether the configured connection file
    can be opened and processed.
  isp: Loop index for per-outlet arrays such as obtyp_out, obtypno_out, htyp_out, and frac_out
    when reading object outflow links.
  cmd_prev: Stores the previously seen command or object identifier during file scanning;
    it is reset before file processing begins.
  ob1: Lower bound of the object index range to process for this spatial-unit block.
  ob2: Upper bound of the object index range to process for this spatial-unit block.
  i: Primary loop counter over spatial objects in the requested block.
  isp_ob: Counts spatial objects within the current block so each object can receive a sequential
    sp_ob_no value.
  nout: Number of outflow links for the current object, taken from src_tot and then used to
    size outflow arrays.
  iout: Loop counter used while allocating or reading each outflow link for an object.
  k: Temporary counter used to scan outflow links when checking for aquifer routing under
    GWFLOW.
  ihyd: Loop counter over hydrograph slots when allocating and initializing constituent hydrograph
    storage.
  npests: Caches cs_db%num_pests so the routine can allocate pesticide arrays only when pesticides
    are active.
  npaths: Caches cs_db%num_paths so the routine can allocate pathogen arrays only when pathogens
    are active.
  nmetals: Caches cs_db%num_metals so the routine can allocate heavy-metal arrays only when
    metals are active.
  nsalts: Caches cs_db%num_salts so the routine can allocate salt arrays only when salts are
    active.
  ncs: Caches cs_db%num_cs so the routine can allocate generic constituent arrays only when
    those constituents are active.
  aqu_found: Flag set when an outflow link to an aquifer is found; it is later used with bsn_cc%gwflow
    to reduce src_tot.
uses:
  hydrograph_module: The hydrograph module provides the shared ob array and the object_connectivity
    type that this routine fills. hyd_read_connect writes core routing metadata into ob(i)%typ,
    ob(i)%nhyds, ob(i)%sp_ob_no, hydrograph containers, and the transfer/inflow/outflow summaries
    that later hydrologic routines depend on.
  constituent_mass_module: The constituent_mass_module supplies the cs_db counters that determine
    whether constituent structures should be allocated, and the obcs array that stores those
    per-object constituent hydrographs. hyd_read_connect uses those counts to size salt and
    generic constituent arrays, initialize them to zero, and prepare the per-outlet mass bookkeeping
    that later water-quality routines expect.
  time_module: The routine allocates subdaily and flow-duration-curve arrays using the current
    timestep count and number of modeled years, so the time module determines those array
    dimensions.
  climate_module: The routine checks whether groundwater flow routing is enabled before deciding
    whether to treat aquifer outflows specially, so climate-module state influences that GWFLOW
    branch here.
  maximum_data_module: The search call uses the maximum weather-station database size when
    crosswalking each object's weather station code to a station index.
  basin_module: The basin module provides bsn_cc%gwflow, which is combined with the GWFLOW
    aquifer check to decide whether an aquifer outflow should be removed from src_tot.
---

<!-- facts:header -->

Reads a connectivity file for a block of spatial objects and initializes hydrograph and constituent tracking for each object. It also crosswalks weather station codes after the object records are loaded.

## Bottom Line

hyd_read_connect opens the configured connection file, checks that it exists, and then walks the file to initialize each spatial object in the requested block. For every object it sets the object type, hydrograph counts, subdaily storage, and, when constituents are active, allocates the matching constituent hydrograph containers and zeros them out.

After the object records are read, the routine reads any declared outflow links, adjusts GWFLOW-related aquifer routing when needed, allocates flow-duration-curve arrays, and finally crosswalks each object's weather station code to the weather database via search. The results feed later hyd_connect logic that uses the populated ob array and constituent structures.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hyd_read_connect runs inside hyd_connect after the spatial object counts and starting indices for a particular object class have been prepared. Its allocations and record reads populate the shared connectivity state that later hydrologic routing, constituent transport, and weather-station crosswalking depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the connection file exists | The routine uses inquire to test whether con_file is present before doing any file I/O. |
| 2. Open and skip the file header | It opens unit 107 on con_file, reads the title and header records, and exits the scan if end-of-file is reached. |
| 3. Determine the object block to process | If nspu is positive, it computes the first and last object indices for this spatial-unit block and resets the per-block object counter. |
| 4. Initialize each object's basic hydrograph state | For every object in the block, it assigns the object type and hydrograph count, numbers the object within the block, allocates daily and average-annual hydrograph arrays, and zeros the basic transfer and total flow fields. |
| 5. Allocate constituent containers when constituents are enabled | If cs_db%num_tot is greater than zero, it marks the object for constituent allocation, allocates obcs storage, allocates constituent arrays by the active database counts, and initializes salt and generic constituent masses and concentrations to zero. |
| 6. Allocate per-hydrograph constituent output arrays | For each hydrograph slot, it allocates the matching pesticide, pathogen, metal, salt, and constituent fields in obcs(i)%hd and zeros the scalar arrays where needed. |
| 7. Allocate subdaily and flow-duration storage | It sets the save-window length from ndsave and allocates the time-series, inflow, unit-hydrograph, and hydrograph-volume arrays used later for subdaily and duration-curve tracking. |
| 8. Read the main object record | The routine reads the object number, name, GIS id, area, coordinates, property references, weather code, constituent code, and source total from con_file. |
| 9. Set area bookkeeping for routing calculations | It copies area_ha into area_ha_calc for HRU, RU, and recall objects and otherwise leaves the calculated area at zero. |
| 10. Re-read any object with outflow links | When src_tot is positive, it sizes the outflow arrays, backspaces the file, and rereads the record including the per-outflow type, number, hydrograph type, and fraction fields. |
| 11. Apply GWFLOW aquifer-link adjustment | If groundwater flow routing is active, it scans the outflow types for aquifer links and, when both aquifer routing and basin GWFLOW are enabled, reduces src_tot by one. |
| 12. Provide defaults when no outflows exist | For objects with no source links, it allocates a single obtypno_out slot and sets it to zero so later loops can rely on a defined outflow-number array. |
| 13. Allocate flow-duration curve arrays | It allocates the per-object flow-duration curve arrays using a fixed 366-day structure and the current modeled year count. |
| 14. Crosswalk weather stations and close the file | After the object block is loaded, it calls search for each object's weather-station code and then closes unit 107 on con_file. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ob` | `ob(i)%typ, ob(i)%nhyds, ob(i)%sp_ob_no, ob(i)%hd(nhyds), ob(i)%hd_aa(nhyds), ob(i)%trans, ob(i)%hin_tot, ob(i)%hout_tot, ob(i)%hd_aa(:)` |
| [sym:constituent_mass_module] | `cs_db, obcs` | `cs_db%num_tot, obcs(i)%hd(nhyds), obcs(i)%hin(1), obcs(i)%hin_sur(1), obcs(i)%hin_lat(1), obcs(i)%hin_til(1), obcs(i)%hin_aqu(1), cs_db%num_pests, obcs(i)%hin(1)%pest(npests), obcs(i)%hin_sur(1)%pest(npests), obcs(i)%hin_lat(1)%pest(npests), obcs(i)%hin_til(1)%pest(npests), cs_db%num_paths, obcs(i)%hin(1)%path(npaths), obcs(i)%hin_sur(1)%path(npaths), obcs(i)%hin_lat(1)%path(npaths), obcs(i)%hin_til(1)%path(npaths), cs_db%num_metals, obcs(i)%hin(1)%hmet(nmetals), obcs(i)%hin_sur(1)%hmet(nmetals), obcs(i)%hin_lat(1)%hmet(nmetals), obcs(i)%hin_til(1)%hmet(nmetals), cs_db%num_salts, obcs(i)%hin(1)%salt(nsalts), obcs(i)%hin_sur(1)%salt(nsalts), obcs(i)%hin_lat(1)%salt(nsalts), obcs(i)%hin_til(1)%salt(nsalts), obcs(i)%hin(1)%salt_min(nsalts), obcs(i)%hin(1)%saltc(nsalts), obcs(i)%hin_sur(1)%salt_min(nsalts), obcs(i)%hin_sur(1)%saltc(nsalts), obcs(i)%hin_lat(1)%salt_min(nsalts), obcs(i)%hin_lat(1)%saltc(nsalts), obcs(i)%hin_til(1)%salt_min(nsalts), obcs(i)%hin_til(1)%saltc(nsalts), obcs(i)%hin(1)%salt, obcs(i)%hin(1)%salt_min, obcs(i)%hin(1)%saltc, obcs(i)%hin_sur(1)%salt, obcs(i)%hin_sur(1)%salt_min, obcs(i)%hin_sur(1)%saltc, obcs(i)%hin_lat(1)%salt, obcs(i)%hin_lat(1)%salt_min, obcs(i)%hin_lat(1)%saltc, obcs(i)%hin_til(1)%salt, obcs(i)%hin_til(1)%salt_min, obcs(i)%hin_til(1)%saltc, cs_db%num_cs, obcs(i)%hin(1)%cs(ncs), obcs(i)%hin(1)%cs_sorb(ncs), obcs(i)%hin(1)%csc(ncs), obcs(i)%hin(1)%csc_sorb(ncs), obcs(i)%hin_sur(1)%cs(ncs), obcs(i)%hin_sur(1)%cs_sorb(ncs), obcs(i)%hin_sur(1)%csc(ncs), obcs(i)%hin_sur(1)%csc_sorb(ncs), obcs(i)%hin_lat(1)%cs(ncs), obcs(i)%hin_lat(1)%cs_sorb(ncs), obcs(i)%hin_lat(1)%csc(ncs), obcs(i)%hin_lat(1)%csc_sorb(ncs), obcs(i)%hin_til(1)%cs(ncs), obcs(i)%hin_til(1)%cs_sorb(ncs), obcs(i)%hin_til(1)%csc(ncs), obcs(i)%hin_til(1)%csc_sorb(ncs), obcs(i)%hin(1)%cs, obcs(i)%hin(1)%cs_sorb, obcs(i)%hin(1)%csc, obcs(i)%hin(1)%csc_sorb, obcs(i)%hin_sur(1)%cs, obcs(i)%hin_sur(1)%cs_sorb, obcs(i)%hin_sur(1)%csc` |
| [sym:time_module] | `time%step, time%nbyr` | `time%step, time%nbyr` |
| [sym:climate_module] | `sp_ob` | `sp_ob%gwflow` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wst` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(i)%typ` | When the object block is processed inside the nspu > 0 branch, before the object record is read back from con_file. | The object's type is set to the caller-supplied obtyp so later routing and object-class logic can treat every object in this block as the intended class. |
| `ob(i)%nhyds` | For each object in the selected block, after ob(i)%typ is assigned and before hydrograph arrays are allocated. | The object's hydrograph count is fixed to nhyds so downstream code knows how many hydrograph slots exist for that object. |
| `ob(i)%sp_ob_no` | For each object in the selected block, while numbering objects within the block. | sp_ob_no becomes a sequential index within the current spatial-object block, which later routines can use to identify the object's position among siblings of the same class. |
| `ob(i)%trans` | For every object in the block during initialization, before any file record is read. | trans is initialized to zero flow so the transfer hydrograph starts from a clean state. |
| `ob(i)%hin_tot` | For every object in the block during initialization, before any record-specific routing inputs are processed. | hin_tot is initialized to zero so the total inflow hydrograph starts empty. |
| `ob(i)%hout_tot` | For every object in the block during initialization, before any record-specific routing inputs are processed. | hout_tot is initialized to zero so the total outflow hydrograph starts empty. |
| `ob(i)%hd_aa(:)` | For every object in the block after hd_aa is allocated. | The average-annual hydrograph array is zeroed so later accumulation can begin from a blank state. |
| `obcs_alloc(i)` | When cs_db%num_tot > 0 for the current object. | obcs_alloc(i) is set to 1 to mark that constituent hydrograph storage has been allocated for this object. |
| `obcs(i)%hin(1)%salt` | When cs_db%num_salts > 0 for the current object. | The salt mass hydrograph for the object inflow container is allocated and set to zero so salt routing can be accumulated later. |
| `obcs(i)%hin(1)%salt_min` | When cs_db%num_salts > 0 for the current object. | The mineral salt hydrograph field is allocated and zeroed for later salt-balance tracking. |
| `obcs(i)%hin(1)%saltc` | When cs_db%num_salts > 0 for the current object. | The salt concentration field is allocated and zeroed for later concentration tracking. |
| `obcs(i)%hin_sur(1)%salt` | When cs_db%num_salts > 0 for the current object. | The surface-inflow salt mass field is allocated and zeroed so surface routing can receive salt loads. |
| `obcs(i)%hin_sur(1)%salt_min` | When cs_db%num_salts > 0 for the current object. | The surface-inflow mineral-salt field is allocated and zeroed for later salt-balance accounting. |
| `obcs(i)%hin_sur(1)%saltc` | When cs_db%num_salts > 0 for the current object. | The surface-inflow salt concentration field is allocated and zeroed for later transport calculations. |
| `obcs(i)%hin_lat(1)%salt` | When cs_db%num_salts > 0 for the current object. | The lateral-inflow salt mass field is allocated and zeroed so lateral routing can receive salt loads. |
| `obcs(i)%hin_lat(1)%salt_min` | When cs_db%num_salts > 0 for the current object. | The lateral-inflow mineral-salt field is allocated and zeroed for later salt-balance accounting. |
| `obcs(i)%hin_lat(1)%saltc` | When cs_db%num_salts > 0 for the current object. | The lateral-inflow salt concentration field is allocated and zeroed for later transport calculations. |
| `obcs(i)%hin_til(1)%salt` | When cs_db%num_salts > 0 for the current object. | The tile-inflow salt mass field is allocated and zeroed so tile routing can receive salt loads. |
| `obcs(i)%hin_til(1)%salt_min` | When cs_db%num_salts > 0 for the current object. | The tile-inflow mineral-salt field is allocated and zeroed for later salt-balance accounting. |
| `obcs(i)%hin_til(1)%saltc` | When cs_db%num_salts > 0 for the current object. | The tile-inflow salt concentration field is allocated and zeroed for later transport calculations. |
| `obcs(i)%hin(1)%cs` | When cs_db%num_cs > 0 for the current object. | The generic constituent mass field is allocated and zeroed so constituent routing can accumulate mass later. |
| `obcs(i)%hin(1)%cs_sorb` | When cs_db%num_cs > 0 for the current object. | The sorbed generic constituent mass field is allocated and zeroed for later sorption accounting. |
| `obcs(i)%hin(1)%csc` | When cs_db%num_cs > 0 for the current object. | The generic constituent concentration field is allocated and zeroed so later water-quality routines can compute concentrations. |
| `obcs(i)%hin(1)%csc_sorb` | When cs_db%num_cs > 0 for the current object. | The sorbed constituent concentration field is allocated and zeroed for later sorbed-phase tracking. |

## File I/O

<!-- facts:io -->


## Lineage

`hyd_read_connect.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `1567fba` (2026-03-31, "gwflow re-merge: input system - gwflow_read, output init extraction, NAM/USGS/st…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hyd_read_connect.f90` are listed.

- `1567fba` (2026-03-31) — gwflow re-merge: input system - gwflow_read, output init extraction, NAM/USGS/stats removal
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `32adbbb` (2025-07-08) — 07082026
- `889136d` (2025-02-03) — Fix typos
- `f1e61a3` (2024-10-08) — fixed tabs
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hyd_read_connect' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
