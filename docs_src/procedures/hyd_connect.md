---
kind: procedure
symbol: hyd_connect
title: hyd_connect
status: filled
source_hash: 101b9e03eefeb238
version_label: SWAT+ 62.0.0
locals:
  eof: End-of-file flag used while reading connection data; initialized to 0 and reset before
    processing.
  imax: Tracks the maximum count encountered while scanning input records or sizing arrays.
  iob_out: Holds the outgoing object type code from a source object's connection record during
    dispatch.
  iobtyp: Holds an object type code used while determining command order and special-case
    handling.
  nspu: Running sequential object index used to assign first object numbers and allocate per-object
    arrays.
  cmdno: Command counter for the object sequence being built.
  idone: Loop-completion flag for the command-order pass; set when all objects have been processed.
  cmd_prev: Previous command/object number in the command chain; used to link objects in sequence.
  ob1: Temporary object index used when accumulating drainage area from incoming objects.
  ob2: Temporary object index used in commented or alternate accumulation logic.
  iobj_tot: Counts how many objects have been finalized in the command-order pass.
  mexco_sp: Scratch real value used in connection processing; initialized but not central
    in the visible control flow.
  i: General loop counter over objects.
  ii: General loop counter over sources, receivers, or elements.
  ielem: Element index used when mapping routing-unit definitions to objects.
  k: Temporary object or element index used in routing-unit and receiver bookkeeping.
  iob: Temporary absolute object number used when indexing the global object array.
  kk: Secondary index used for sequential source/receiver slots and routing-unit membership
    slots.
  j: Temporary object index for a receiver object.
  ielem_db: Database element index used when expanding routing-unit definitions to object
    members.
  jj: Secondary loop counter used when writing diagnostics or assigning receiver slots.
  iord: Current pass number in the iterative command-order construction.
  isrc_tot: Number of source objects considered in the current command-order pass.
  iorder: Highest upstream command order found for the current object.
  ircv: Loop counter over incoming receivers for an object.
  ircv_ob: Object number of an incoming receiver used when looking up upstream order.
  max: Scratch variable for maximum values in the command-order logic.
  i_exist: Logical flag used when checking whether a file or record exists before reading.
uses:
  hydrograph_module: Provides the global object counts, object numbering offsets, hydrograph-slot
    counts, and connectivity arrays that `hyd_connect` fills and uses to build the watershed
    routing graph.
  input_file_module: Provides the connectivity filenames that `hyd_connect` opens for each
    object class.
  recall_module: No resolved outside references from this module were provided in the context
    packet.
  organic_mineral_mass_module: No resolved outside references from this module were provided
    in the context packet.
  constituent_mass_module: Provides constituent-count metadata and zeroed constituent hydrograph
    arrays that are allocated after connectivity is built.
  ru_module: No resolved outside references from this module were provided in the context
    packet.
  basin_module: Provides the maximum hydrograph lag length used when allocating per-receiver
    hydrograph storage.
---

<!-- facts:header -->

Builds the watershed connectivity network for hydrologic objects and initializes the routing and receiving arrays they need.

## Bottom Line

`hyd_connect` reads the various connectivity files for HRUs, routing units, aquifers, channels, reservoirs, recalls, export coefficients, delivery ratios, outlets, swat-deg channels, and gwflow. It assigns sequential object numbers, fills source/receiver links, and prepares hydrograph storage so later routing can run in a valid order.

It also computes routing-unit membership and command ordering, checks for impossible loops, and writes a diagnostic summary of calculated versus input drainage areas. In short, this is the setup routine that turns the watershed configuration into the object graph used by downstream hydrology.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs during watershed connectivity setup, after the spatial object counts and connection filenames are available. It prepares the object graph and command order that later hydrology, routing, and transport routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counts and offsets | Resets counters, allocates the top-level receiver/defining arrays, and assigns the first sequential object number for each object class that exists in the watershed. |
| 2. Read class connectivity files | For each object class that exists, calls the appropriate reader to load its connectivity file and any class-specific supporting data such as routing-unit, aquifer, channel, delivery-ratio, or gwflow tables. |
| 3. Build routing-unit memberships | Allocates routing-unit membership arrays for objects that contain routing units, then maps routing-unit definitions to object numbers and counts defining-unit membership per routing-unit object. |
| 4. Map outgoing receivers | Walks every source object and its outgoing links, converts type/number pairs into absolute object numbers, increments receiver counts, and records hydrologic type codes for each outgoing connection. |
| 5. Allocate constituent arrays | Allocates and zeros the constituent hydrograph arrays for pesticides, pathogens, metals, salts, and other constituents using the database counts. |
| 6. Allocate receiver storage | Allocates incoming-object arrays, hydrograph lag storage, and constituent input arrays for every object that has at least one receiver. |
| 7. Populate incoming links | Loops over each source object again to fill incoming-object arrays, including the special modflow-to-all-channels case and the extra receiver bookkeeping for routing-unit elements. |
| 8. Order commands iteratively | Iteratively builds the command/object execution order by repeatedly firing objects whose incoming and defining dependencies are satisfied, while propagating receiver counts and upstream order. |
| 9. Write drainage diagnostics | Writes a diagnostic table of input and calculated drainage areas for non-HRU and non-RU objects after the connectivity graph has been built. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, hd_tot, ob, ru_def, ru_elem` | `sp_ob%objs, sp_ob%hru, sp_ob1%hru, sp_ob%hru_lte, sp_ob1%hru_lte, sp_ob%ru, sp_ob1%ru, sp_ob%gwflow, sp_ob1%gwflow, sp_ob%aqu, sp_ob1%aqu, sp_ob%chan, sp_ob1%chan, sp_ob%res, sp_ob1%res, sp_ob%recall, sp_ob1%recall, sp_ob%exco, sp_ob1%exco, sp_ob%dr, sp_ob1%dr, sp_ob%canal, sp_ob1%canal, sp_ob%pump, sp_ob1%pump, sp_ob%outlet, sp_ob1%outlet, sp_ob%chandeg, sp_ob1%chandeg, hd_tot%hru, hd_tot%hru_lte, hd_tot%ru, hd_tot%aqu, hd_tot%chan, hd_tot%res, hd_tot%recall, hd_tot%exco, hd_tot%dr, hd_tot%outlet, hd_tot%chandeg, hd_tot%gwflow, ob(i)%ru_tot, ob(i)%obj_subs(nspu), ru_def(iru)%num_tot, ru_def(iru)%num(ii), ru_elem(ielem)%obj, ob(k)%obj_subs(kk), ob(i)%src_tot, ob(i)%obtyp_out(ii), ob(i)%obj_out(ii), ob(i)%obtypno_out(ii), ob(j)%rcv_tot, ru_def(iru)%num(kk), ob(iob)%rcv_tot, ob(i)%typ, ob(i)%htyp_out(ii), ob(i)%ihtyp_out(ii)` |
| [sym:input_file_module] | `in_con` | `in_con%hru_con, in_con%hruez_con, in_con%ru_con, in_con%aqu_con, in_con%chan_con, in_con%res_con, in_con%rec_con, in_con%exco_con, in_con%delr_con, in_con%out_con, in_con%chandeg_con, in_con%gwflow_con` |
| [sym:recall_module] | `none resolved` |  |
| [sym:organic_mineral_mass_module] | `none resolved` |  |
| [sym:constituent_mass_module] | `hin_csz, cs_db` | `hin_csz%pest, cs_db%num_pests, hin_csz%path, cs_db%num_paths, hin_csz%hmet, cs_db%num_metals, hin_csz%salt, cs_db%num_salts, hin_csz%cs, cs_db%num_cs` |
| [sym:ru_module] | `none resolved` |  |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%day_lag_mx` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rcv_sum` | After initialization and class counting | Allocated to one slot per object and reset to zero so incoming links can be counted later. |
| `dfn_sum` | After initialization and class counting | Allocated to one slot per object and reset to zero so defining-unit membership can be counted later. |
| `ru_seq` | After initialization and class counting | Allocated to one slot per object and reset to zero so routing-unit membership slots can be assigned later. |
| `sp_ob1%hru` | When routing-unit memberships are built | Stores the first sequential object number for HRUs when HRUs exist. |
| `sp_ob1%hru_lte` | When routing-unit memberships are built | Stores the first sequential object number for HRU-LTE objects when they exist. |
| `sp_ob1%ru` | When routing-unit memberships are built | Stores the first sequential object number for routing units when they exist. |
| `sp_ob1%gwflow` | When routing-unit memberships are built | Stores the first sequential object number for gwflow objects when they exist. |
| `sp_ob1%aqu` | When routing-unit memberships are built | Stores the first sequential object number for aquifers when they exist. |
| `sp_ob1%chan` | When routing-unit memberships are built | Stores the first sequential object number for channels when they exist. |
| `sp_ob1%res` | When routing-unit memberships are built | Stores the first sequential object number for reservoirs when they exist. |
| `sp_ob1%recall` | When routing-unit memberships are built | Stores the first sequential object number for recalls when they exist. |
| `sp_ob1%exco` | When routing-unit memberships are built | Stores the first sequential object number for export-coefficient objects when they exist. |
| `sp_ob1%dr` | When routing-unit memberships are built | Stores the first sequential object number for delivery-ratio objects when they exist. |
| `sp_ob1%canal` | When routing-unit memberships are built | Stores the first sequential object number for canal objects when they exist. |
| `sp_ob1%pump` | When routing-unit memberships are built | Stores the first sequential object number for pump objects when they exist. |
| `sp_ob1%outlet` | When routing-unit memberships are built | Stores the first sequential object number for outlet objects when they exist. |
| `sp_ob1%chandeg` | When routing-unit memberships are built | Stores the first sequential object number for swat-deg channel objects when they exist. |
| `ru_seq(k)` | During routing-unit membership mapping | Incremented for each routing-unit element encountered so the element can be placed in the correct sequential slot. |
| `ob(k)%obj_subs(kk)` | During routing-unit membership mapping | Filled with the routing-unit object number that contains object k. |
| `dfn_sum(iob)` | During routing-unit membership mapping | Incremented for each routing-unit element assigned to the routing-unit object. |
| `ob(i)%obj_out(ii)` | During outgoing receiver mapping | Set to the absolute object number of each outgoing receiver. |
| `ob(j)%rcv_tot` | During outgoing receiver mapping | Incremented for each object that receives flow from a source object. |
| `iru` | During outgoing receiver mapping | Used to identify the routing unit whose elements must also receive counts when a routing-unit object is the receiver. |
| `ob(iob)%rcv_tot` | During outgoing receiver mapping | Incremented for routing-unit elements that are indirect receivers of a routing-unit outflow. |

## File I/O

<!-- facts:io -->


## Lineage

`hyd_connect.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 12 non-merge commit(s) since, most recently `1567fba` (2026-03-31, "gwflow re-merge: input system - gwflow_read, output init extraction, NAM/USGS/st…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hyd_connect.f90` are listed.

- `1567fba` (2026-03-31) — gwflow re-merge: input system - gwflow_read, output init extraction, NAM/USGS/stats removal
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `cf3201b` (2025-11-05) — in hyd_connect, code was added to allow multiple input object to routing units. in actions for irrigating from an aquifer, an if statement w…
- `889136d` (2025-02-03) — Fix typos
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No extracted documentation comment was present in the source; the purpose statement was taken from the Fortran header comment.
- `recall_module`, `organic_mineral_mass_module`, and `ru_module` had no resolved outside references in the context packet, so their module-state sections are intentionally minimal.
- The routine writes a looping diagnostic file and aborts if the command-order pass exceeds the safety threshold.
- algorithm_steps revised: merged the draft's fragmented case handling into broader source-faithful phases and added the later allocation/diagnostic phases to match the actual control flow.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
