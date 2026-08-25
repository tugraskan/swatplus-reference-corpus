---
kind: procedure
symbol: hru_fr_change
title: hru_fr_change
status: filled
source_hash: 79f6793832834adb
version_label: SWAT+ 62.0.0
args:
  lsu_elem_upd: Provides the path to the updated landscape-cataloging-unit element file. If
    this file exists and is not the string `"null"`, the routine opens it and uses its records
    to refresh `lsu_elem` and downstream HRU-linked state.
  ru_elem_upd: Provides the path to the updated routing-unit element file. If this file exists
    and is not the string `"null"`, the routine opens it and uses its records to refresh `ru_elem`,
    including each element's delivery-ratio reference.
locals:
  titldum: Holds the first title line read from each update file so the routine can skip file
    header text before reading data records.
  header: Holds the second header line read from each update file so the routine can skip
    file header text before reading data records.
  eof: I/O status flag for `read` statements; negative values end the file scan and cause
    the open/read loop to stop for that input file.
  i_exist: Logical flag from `inquire` that records whether the configured update file is
    present on disk before the routine tries to read it.
  i: Record index read from each update file and then reused as the array index for updating
    `ru_elem(i)` or `lsu_elem(i)`.
  isp: Loop counter used to step through the maximum number of routing-unit or LSU elements
    while reading the corresponding update file.
  k: Discarded record number field read from the update files before the remaining fields
    are assigned into the element arrays.
  iob: Holds the object index for the HRU's connected object so the routine can mirror updated
    HRU area back to `ob(iob)%area_ha`.
  idr: Loop counter used to search delivery-ratio definitions in `dr_db` and find the matching
    delivery-ratio data for a routing element.
  ii: Loop counter used while walking the element indices listed in `ru_def(iru)%num` for
    each routing unit.
  ihru: Holds the HRU index derived from LSU or RU element object numbers so the routine can
    update HRU-specific area, wetlands, and roughness state.
  iprop: Points to the wetland/surface-storage property record associated with an HRU; if
    it is zero, no wetland reset is performed for that HRU.
  ihyd: Points from the wetland property record to the wetland hydrology definition that supplies
    spillway area and depth parameters.
  ielem: Holds the routing-unit element index taken from `ru_def(iru)%num(ii)` so the routine
    can inspect each routed element while computing `ru_n`.
uses:
  hydrograph_module: '`hydrograph_module` owns the routing and spatial connectivity arrays
    that this routine updates and later uses to map element records onto HRUs and routing
    units. The copied element fields identify object type, object number, and delivery-ratio
    data, while `ob`, `sp_ob`, and `ru_def` supply the object and routing counts needed for
    the update loops.'
  maximum_data_module: '`maximum_data_module` provides the maximum element counts that bound
    the two input-file scans. Those maxima determine how many routing-unit and LSU element
    records the routine attempts to read and therefore how much shared state can be refreshed.'
  dr_module: '`dr_module` holds the delivery-ratio lookup table. The routine matches each
    routing element''s `dr_name` against `dr_db(idr)%name` so it can assign the corresponding
    delivery-ratio data into `ru_elem(i)%dr`.'
  calibration_data_module: '`calibration_data_module` owns the LSU element array that receives
    the updated landscape records. Those records carry the basin and routing fractions that
    drive HRU area recalculation later in the routine.'
  hru_module: '`hru_module` contains the HRU state that is directly recomputed here: area
    in hectares, kilometer-equivalent area, object linkage, and the surface-storage pointer
    used for wetland resets.'
  reservoir_data_module: '`reservoir_data_module` supplies the wetland hydrology lookup data
    that converts an HRU''s surface-storage pointer into principal/emergency spillway depths
    and spillway fractions. Those parameters are needed to rebuild wetland geometry after
    HRU area changes.'
  reservoir_module: '`reservoir_module` owns the wetland output/state that gets rewritten
    from the new HRU area and wetland hydrology values. Those fields represent the updated
    wetland volume and surface-area geometry used by later reservoir calculations.'
  ru_module: '`ru_module` holds the routing-unit roughness accumulator `ru_n`, which this
    routine recomputes after element fractions and HRU areas change so routing behavior stays
    consistent with the updated landscape configuration.'
---

<!-- facts:header -->

Updates routing-unit and landscape-element fraction files, then propagates those fraction changes into HRU area, wetland geometry, and routing roughness state.

## Bottom Line

`hru_fr_change` reads the updated `rout_unit.ele`-style and `lsu_unit.ele`-style files named by its arguments, copies their element records into `ru_elem` and `lsu_elem`, and uses those updated fractions to reset HRU areas, linked object areas, wetland volumes/areas, and routing-unit Manning's n values.

It matters because later model behavior depends on these shared arrays and object properties being consistent after a fraction change. The routine is called from the `actions` workflow for the `hru_fr_update` action before the model writes the change record and continues simulation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`actions` calls this routine during the `hru_fr_update` action after the action table has supplied the two update-file names as `option` and `file_pointer`. The updated shared state then feeds the rest of the model through the recalculated HRU areas, wetland properties, and routing roughness values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check routing update-file availability | The routine tests whether the routing update file exists, or whether the caller supplied a non-`null` file name, before entering the routing-element read loop. |
| 2. Read routing-element records | The routine opens unit 107 on `ru_elem_upd`, skips the title and header lines, scans each record index, backspaces, and rereads the full record into `ru_elem(i)`; it then looks up the matching delivery-ratio name in `dr_db` and copies the referenced delivery-ratio data into `ru_elem(i)%dr`. |
| 3. Close routing update file | After the routing-element scan finishes, the routine exits the read loop and closes unit 107 for the routing update file. |
| 4. Check LSU update-file availability | The routine tests whether the LSU update file exists, or whether the caller supplied a non-`null` file name, before entering the LSU-element read loop. |
| 5. Read LSU element records | The routine opens unit 107 on `lsu_elem_upd`, skips the title and header lines, scans each record index, backspaces, and rereads the full record into `lsu_elem(i)`. |
| 6. Close LSU update file | After the LSU-element scan finishes, the routine exits the read loop and closes unit 107 for the LSU update file. |
| 7. Recompute HRU areas from LSU fractions | For each LSU element whose object type is `hru`, the routine takes the HRU index from `obtypno`, computes `hru(ihru)%area_ha` from `lsu_elem(i)%bsn_frac * bsn%area_ls_ha`, derives `hru(ihru)%km` as `area_ha / 100.`, and mirrors the new area back into the linked object record `ob(iob)%area_ha`. |
| 8. Reset wetland geometry for HRUs with surface storage | For each HRU, the routine checks `hru(ihru)%dbs%surf_stor`; if it points to a wetland property record, the routine uses `wet_dat(iprop)%hyd` and `wet_hyd(ihyd)` to recalculate wetland volume and surface-area fields from the new HRU area. |
| 9. Recompute routing-unit roughness | For each routing unit, the routine initializes `ru_n(iru)` to zero, walks the element list in `ru_def(iru)%num`, and accumulates `hru(ihru)%luse%ovn * hru(ihru)%km` for HRU elements; if an element is not an HRU, it falls back to `ru_n(iru) = 0.1`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ru_elem, ob, sp_ob, ru_def` | `ru_elem(i)%name, ru_elem(i)%obtyp, ru_elem(i)%obtypno, ru_elem(i)%frac, ru_elem(i)%dr_name, ru_elem(i)%dr, ob(iob)%area_ha, sp_ob%hru, sp_ob%ru, ru_def(iru)%num_tot, ru_def(iru)%num(ii), ru_elem(ielem)%obtyp, ru_elem(ielem)%obtypno` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ru_elem, db_mx%dr_om, db_mx%lsu_elem` |
| [sym:dr_module] | `dr_db` | `dr_db(idr)%name` |
| [sym:calibration_data_module] | `lsu_elem` | `lsu_elem(i)%name, lsu_elem(i)%obtyp, lsu_elem(i)%obtypno, lsu_elem(i)%bsn_frac, lsu_elem(i)%ru_frac` |
| [sym:hru_module] | `hru` | `hru(ihru)%area_ha, hru(ihru)%km, hru(ihru)%obj_no, hru(ihru)%dbs%surf_stor` |
| [sym:reservoir_data_module] | `wet_dat, wet_hyd` | `wet_dat(iprop)%hyd, wet_hyd(ihyd)%edep, wet_hyd(ihyd)%pdep, wet_hyd(ihyd)%psa, wet_hyd(ihyd)%esa` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(ihru)%evol, wet_ob(ihru)%pvol, wet_ob(ihru)%psa, wet_ob(ihru)%esa` |
| [sym:ru_module] | `ru_n, iru` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ru_elem(i)%dr` | When a routing-unit element record is read from `ru_elem_upd` and its `dr_name` matches `dr_db(idr)%name`. | The routine replaces the routing element's delivery-ratio output data with the matching `dr` entry so the element carries the updated delivery-ratio definition. |
| `hru(ihru)%area_ha` | When an LSU element has `obtyp == "hru"` during the LSU fraction update pass. | The routine recomputes the HRU's area from the LSU basin fraction and the basin area, so the HRU reflects the new fraction layout. |
| `hru(ihru)%km` | When an LSU element has `obtyp == "hru"` during the LSU fraction update pass. | The routine converts the new HRU area to kilometer units by dividing by 100, keeping the HRU's area-derived routing-size field consistent with the updated fraction. |
| `ob(iob)%area_ha` | When an LSU element has `obtyp == "hru"` and the linked HRU object number is retrieved. | The routine mirrors the recalculated HRU area back into the connected object record so the shared object connectivity state matches the updated HRU size. |
| `wet_ob(ihru)%evol` | When an HRU has a positive surface-storage pointer (`iprop > 0`). | The routine recomputes the wetland emergency-spillway volume from the updated HRU area and the wetland hydrology depth `edep`. |
| `wet_ob(ihru)%pvol` | When an HRU has a positive surface-storage pointer (`iprop > 0`). | The routine recomputes the wetland principal-spillway volume from the updated HRU area and the wetland hydrology depth `pdep`. |
| `wet_ob(ihru)%psa` | When an HRU has a positive surface-storage pointer (`iprop > 0`). | The routine recomputes the principal-spillway surface area from the updated HRU area and the wetland hydrology fraction `psa`. |
| `wet_ob(ihru)%esa` | When an HRU has a positive surface-storage pointer (`iprop > 0`). | The routine recomputes the emergency-spillway surface area from the updated HRU area and the wetland hydrology fraction `esa`. |
| `ru_n(iru)` | When a routing unit is processed in the final roughness loop. | The routine resets and then rebuilds the routing-unit roughness accumulator from the HRU elements listed in `ru_def(iru)%num`, using HRU overland roughness and HRU area-derived kilometer weighting; non-HRU elements force the accumulator to 0.1. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `hru_fr_change`. The original file was added in `df07e3f`, then `94b6dec` added the full routine body that opens the update files, reads routing and LSU element records, recomputes HRU area and wetland state, and rebuilds routing roughness. The later `39fabde` commit did not change logic; it initialized the local scalars `titldum`, `header`, `eof`, `i`, `isp`, `k`, `iob`, `idr`, `ii`, `ihru`, `iprop`, `ihyd`, and `ielem`.

- df07e3f introduced `hru_fr_change` as a new subroutine skeleton and preserved its input-file driven update workflow.
- 94b6dec implemented the actual fraction-change behavior: reading `ru_elem_upd` and `lsu_elem_upd`, xwalking delivery-ratio names, updating HRU areas, wetland parameters, and routing-unit roughness.
- 39fabde changed only initialization defaults for local variables and did not alter the procedure's control flow or calculations.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_fr_change' has no extracted documentation comment.
