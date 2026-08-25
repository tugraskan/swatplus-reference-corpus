---
kind: procedure
symbol: aqu_initial
title: aqu_initial
status: filled
source_hash: 08305bac76cb709c
version_label: SWAT+ 62.0.0
locals:
  iaq: Loop counter for aquifers. It is used to iterate over each aquifer object and its associated
    balance arrays.
  iob: Temporary object index into `ob`; it maps each aquifer number to the corresponding
    hydrograph object so the routine can read the owning object's properties and area.
  iaqdb: Database index for the current aquifer. It is derived from `ob(iob)%props` and used
    to copy the right record from `aqudb` into `aqu_dat(iaq)`.
  isalt: Loop counter for salt ions within each aquifer. It is used to zero per-salt balance
    fields in the monthly, yearly, and average-annual salt trackers.
  ics: Loop counter for generic constituents within each aquifer. It is used to zero per-constituent
    balance fields in the monthly, yearly, and average-annual constituent trackers.
uses:
  aquifer_module: The aquifer parameter module supplies the persistent aquifer parameter array
    that this routine fills. `aqu_initial` copies each aquifer's surface area from the hydrograph
    object into `aqu_prm(iaq)%area_ha` and computes `aqu_prm(iaq)%alpha_e` from the database
    alpha value, so the aquifer parameter type must already exist and be writable here.
  hydrograph_module: The hydrograph module ties each aquifer number to a spatial object and
    its source properties. `aqu_initial` uses `sp_ob%aqu` and `sp_ob1%aqu` to size and index
    the aquifer loops, and it reads `ob(iob)%props` and `ob(iob)%area_ha` to locate the aquifer
    database record and set the aquifer surface area.
  constituent_mass_module: The constituent-mass module provides the global counts that decide
    which aquifer substructures exist. `aqu_initial` checks `cs_db%num_pests`, `cs_db%num_salts`,
    `cs_db%num_paths`, `cs_db%num_metals`, and `cs_db%num_cs` before allocating the matching
    `cs_aqu` and balance arrays, so these counts control which arrays are created and initialized.
  aqu_pesticide_module: The pesticide output module holds the basin-wide and per-aquifer pesticide
    process arrays that must be allocated when pesticides are simulated. `aqu_initial` creates
    the per-aquifer `aqupst_*` arrays and the basin-wide `baqupst_*%pest` arrays so later
    pesticide initialization and reporting routines have storage to fill.
  salt_module: The salt module is imported as a dependency for the aquifer initialization
    path, but the extracted source and reference lists do not show any direct symbols from
    that module being used in this routine. The actual salt balance state that `aqu_initial`
    touches comes from `salt_aquifer`.
  salt_aquifer: The salt-aquifer module defines the per-aquifer salt balance objects that
    this routine allocates and zeros. `aqu_initial` creates the daily, monthly, yearly, and
    average-annual salt balance arrays and initializes the monthly/yearly/annual flux fields
    such as recharge, seepage, groundwater load, concentration, irrigation removal, and dissolved
    mass.
  cs_module: The cs module is imported for the aquifer constituent workflow, but the extracted
    evidence does not identify direct symbols from that module as used here. The constituent
    balance storage actually initialized in this routine is defined in `cs_aquifer` and sized
    by `constituent_mass_module` counts.
  cs_aquifer: The cs-aquifer module defines the per-aquifer constituent balance objects that
    this routine allocates and resets. `aqu_initial` creates the daily, monthly, yearly, and
    average-annual constituent balance arrays and initializes the monthly/yearly/annual flux
    and storage-tracking fields so later constituent routing can accumulate into them.
---

<!-- facts:header -->

Initializes aquifer-related storage and balance arrays for pesticides, salts, and other constituents. It also copies aquifer database parameters into working aquifer state and zeroes the aquifer flux trackers that later routines update.

## Bottom Line

aqu_initial sets up all aquifer-wide data structures before simulation proceeds. It allocates the per-aquifer working arrays, initializes aquifer parameters like area and exponential recession factor, and prepares daily, monthly, yearly, and annual balance containers for salts and other constituents when those processes are enabled.

The routine matters because later aquifer read/initialization code and subsequent water-quality and hydrologic calculations depend on these arrays already existing and starting from consistent zeroed state. In this checkout, aquifer pesticide and constituent state is initialized here only for the main storage arrays; the comment at the end notes that some pesticide/constituent initialization is completed in `aqu_read_init` and `aqu_read_init_cs` after this routine runs.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during aquifer setup in `proc_aqu`, after `aqu_read` has loaded the aquifer input data and before `aqu_read_init` and `aqu_read_init_cs` finish the remaining initialization. Its results matter to later aquifer water balance, pesticide, salt, and constituent calculations because those routines expect the aquifer parameter and flux arrays to already be allocated and zeroed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Allocate the top-level aquifer and constituent containers for every aquifer object. | The routine sizes the main aquifer arrays (`aqu_om_init`, `aqu_d`, `aqu_dat`, `aqu_prm`, `aqu_m`, `aqu_y`, `aqu_a`, `cs_aqu`, `aqupst_d`, `aqupst_m`, `aqupst_y`, `aqupst_a`) to the number of aquifers in `sp_ob%aqu`. |
| 2. Allocate basin-wide pesticide output arrays when pesticides are simulated. | If `cs_db%num_pests > 0`, it allocates the daily, monthly, yearly, and annual pesticide process arrays in `baqupst_*%pest` so basin-level pesticide results can be stored. |
| 3. Allocate basin-wide salt balance containers when salts are simulated. | If `cs_db%num_salts > 0`, it allocates `asaltb_d`, `asaltb_m`, `asaltb_y`, and `asaltb_a`, then allocates each aquifer's salt array and zeros the monthly, yearly, and average-annual salt flux fields plus the dissolved mass fields for salt ion 1. |
| 4. Allocate basin-wide generic constituent balance containers when constituents are simulated. | If `cs_db%num_cs > 0`, it allocates `acsb_d`, `acsb_m`, `acsb_y`, and `acsb_a`, then allocates each aquifer's constituent array and zeros the monthly, yearly, and average-annual flux and storage fields for every constituent. |
| 5. Loop through each aquifer to initialize aquifer-specific pesticide, salt, and constituent storage. | For each aquifer, if pesticides are enabled it allocates `cs_aqu(iaq)%pest`, the aquifer pesticide output arrays, and the pathogen/heavy-metal storage arrays used by the shared constituent-mass structure. |
| 6. Initialize per-aquifer salt storage arrays and zero the salt state vectors. | When salts are enabled, it allocates the aquifer's salt mass, mineral-fraction, and concentration arrays, then clears those arrays to zero so the aquifer starts without preloaded salt mass or concentration. |
| 7. Initialize per-aquifer generic constituent storage arrays and zero them. | When generic constituents are enabled, it allocates the aquifer's constituent mass, concentration, sorbed mass, and sorbed concentration arrays and sets them to zero. |
| 8. Map each aquifer to its source object, copy database parameters, and seed the hydrologic state. | The routine finds the owning hydrograph object, copies the aquifer database record into `aqu_dat(iaq)`, stores the aquifer area and exponential recession factor in `aqu_prm`, computes initial storage and initial nitrate storage, and resets recharge, seepage, evaporation, and nitrate flux variables in `aqu_d` to zero. |
| 9. Exit after noting that some pesticide and constituent initialization is handled elsewhere. | The routine documents that pesticide and constituent initialization continues in `aqu_read_init` and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:aquifer_module] | `aqu_prm` | `aqu_prm(iaq)%area_ha, aqu_prm(iaq)%alpha_e` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%aqu, sp_ob1%aqu, ob(iob)%props, ob(iob)%area_ha` |
| [sym:constituent_mass_module] | `cs_db, cs_aqu` | `cs_db%num_pests, cs_db%num_salts, cs_db%num_cs, cs_aqu(iaq)%pest, cs_aqu(iaq)%path, cs_db%num_paths, cs_aqu(iaq)%hmet, cs_db%num_metals, cs_aqu(iaq)%salt, cs_aqu(iaq)%salt_min(5), cs_aqu(iaq)%saltc, cs_aqu(iaq)%salt_min, cs_aqu(iaq)%cs, cs_aqu(iaq)%csc, cs_aqu(iaq)%cs_sorb, cs_aqu(iaq)%csc_sorb` |
| [sym:aqu_pesticide_module] | `baqupst_d, baqupst_m, baqupst_y, baqupst_a, aqupst_d, aqupst_m, aqupst_y, aqupst_a` | `baqupst_d%pest, baqupst_m%pest, baqupst_y%pest, baqupst_a%pest, aqupst_d(iaq)%pest, aqupst_m(iaq)%pest, aqupst_y(iaq)%pest, aqupst_a(iaq)%pest` |
| [sym:salt_module] | `salt_module appears in the use list, but no candidate outside references were resolved to it in the extracted evidence.` |  |
| [sym:salt_aquifer] | `asaltb_d, asaltb_m, asaltb_y, asaltb_a` | `asaltb_d(iaq)%salt, asaltb_m(iaq)%salt, asaltb_y(iaq)%salt, asaltb_a(iaq)%salt, asaltb_m(iaq)%salt(isalt)%rchrg, asaltb_m(iaq)%salt(isalt)%seep, asaltb_m(iaq)%salt(isalt)%saltgw, asaltb_m(iaq)%salt(isalt)%conc, asaltb_m(iaq)%salt(isalt)%irr, asaltb_y(iaq)%salt(isalt)%rchrg, asaltb_y(iaq)%salt(isalt)%seep, asaltb_y(iaq)%salt(isalt)%saltgw, asaltb_y(iaq)%salt(isalt)%conc, asaltb_y(iaq)%salt(isalt)%irr, asaltb_a(iaq)%salt(isalt)%rchrg, asaltb_a(iaq)%salt(isalt)%seep, asaltb_a(iaq)%salt(isalt)%saltgw, asaltb_a(iaq)%salt(isalt)%conc, asaltb_a(iaq)%salt(isalt)%irr, asaltb_m(iaq)%salt(1)%diss, asaltb_y(iaq)%salt(1)%diss, asaltb_a(iaq)%salt(1)%diss` |
| [sym:cs_module] | `cs_module appears in the use list, but no candidate outside references were resolved to it in the extracted evidence.` |  |
| [sym:cs_aquifer] | `acsb_d, acsb_m, acsb_y, acsb_a` | `acsb_d(iaq)%cs, acsb_m(iaq)%cs, acsb_y(iaq)%cs, acsb_a(iaq)%cs, acsb_m(iaq)%cs(ics)%csgw, acsb_m(iaq)%cs(ics)%rchrg, acsb_m(iaq)%cs(ics)%seep, acsb_m(iaq)%cs(ics)%irr, acsb_m(iaq)%cs(ics)%sorb, acsb_m(iaq)%cs(ics)%rctn, acsb_m(iaq)%cs(ics)%conc, acsb_m(iaq)%cs(ics)%srbd, acsb_y(iaq)%cs(ics)%csgw, acsb_y(iaq)%cs(ics)%rchrg, acsb_y(iaq)%cs(ics)%seep, acsb_y(iaq)%cs(ics)%irr, acsb_y(iaq)%cs(ics)%sorb, acsb_y(iaq)%cs(ics)%rctn, acsb_y(iaq)%cs(ics)%conc, acsb_y(iaq)%cs(ics)%srbd, acsb_a(iaq)%cs(ics)%csgw, acsb_a(iaq)%cs(ics)%rchrg, acsb_a(iaq)%cs(ics)%seep, acsb_a(iaq)%cs(ics)%irr, acsb_a(iaq)%cs(ics)%sorb, acsb_a(iaq)%cs(ics)%rctn, acsb_a(iaq)%cs(ics)%conc, acsb_a(iaq)%cs(ics)%srbd` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `asaltb_m(iaq)%salt(isalt)%rchrg` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the monthly loop. | `asaltb_m(iaq)%salt(isalt)%rchrg` is reset to zero so the monthly salt recharge accumulator starts clean for each salt ion and can later collect recharge mass during the simulation month. |
| `asaltb_m(iaq)%salt(isalt)%seep` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the monthly loop. | `asaltb_m(iaq)%salt(isalt)%seep` is reset to zero so the monthly salt seepage accumulator starts clean before any seepage mass is routed out of the aquifer. |
| `asaltb_m(iaq)%salt(isalt)%saltgw` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the monthly loop. | `asaltb_m(iaq)%salt(isalt)%saltgw` is reset to zero so the monthly salt loading-to-stream accumulator begins empty before groundwater loading is computed. |
| `asaltb_m(iaq)%salt(isalt)%conc` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the monthly loop. | `asaltb_m(iaq)%salt(isalt)%conc` is reset to zero so the monthly salt concentration field starts from no prior value. |
| `asaltb_m(iaq)%salt(isalt)%irr` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the monthly loop. | `asaltb_m(iaq)%salt(isalt)%irr` is reset to zero so the monthly irrigation-removal accumulator starts from no prior mass loss. |
| `asaltb_y(iaq)%salt(isalt)%rchrg` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the yearly loop. | `asaltb_y(iaq)%salt(isalt)%rchrg` is reset to zero so the yearly salt recharge accumulator starts clean for annual reporting. |
| `asaltb_y(iaq)%salt(isalt)%seep` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the yearly loop. | `asaltb_y(iaq)%salt(isalt)%seep` is reset to zero so the yearly salt seepage accumulator starts clean. |
| `asaltb_y(iaq)%salt(isalt)%saltgw` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the yearly loop. | `asaltb_y(iaq)%salt(isalt)%saltgw` is reset to zero so the yearly groundwater-load accumulator starts empty. |
| `asaltb_y(iaq)%salt(isalt)%conc` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the yearly loop. | `asaltb_y(iaq)%salt(isalt)%conc` is reset to zero so the yearly salt concentration field starts without carryover. |
| `asaltb_y(iaq)%salt(isalt)%irr` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the yearly loop. | `asaltb_y(iaq)%salt(isalt)%irr` is reset to zero so the yearly irrigation-removal accumulator starts empty. |
| `asaltb_a(iaq)%salt(isalt)%rchrg` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the average-annual loop. | `asaltb_a(iaq)%salt(isalt)%rchrg` is reset to zero so the average-annual salt recharge accumulator starts clean. |
| `asaltb_a(iaq)%salt(isalt)%seep` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the average-annual loop. | `asaltb_a(iaq)%salt(isalt)%seep` is reset to zero so the average-annual salt seepage accumulator starts clean. |
| `asaltb_a(iaq)%salt(isalt)%saltgw` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the average-annual loop. | `asaltb_a(iaq)%salt(isalt)%saltgw` is reset to zero so the average-annual groundwater-load accumulator starts empty. |
| `asaltb_a(iaq)%salt(isalt)%conc` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the average-annual loop. | `asaltb_a(iaq)%salt(isalt)%conc` is reset to zero so the average-annual salt concentration field starts without carryover. |
| `asaltb_a(iaq)%salt(isalt)%irr` | When `cs_db%num_salts > 0` and each aquifer is being initialized in the average-annual loop. | `asaltb_a(iaq)%salt(isalt)%irr` is reset to zero so the average-annual irrigation-removal accumulator starts empty. |
| `asaltb_m(iaq)%salt(1)%diss` | When `cs_db%num_salts > 0` and salt state is initialized for each aquifer after the per-salt loops. | `asaltb_m(iaq)%salt(1)%diss` is reset to zero so the monthly dissolved-salt transfer accumulator starts from no prior value. |
| `asaltb_y(iaq)%salt(1)%diss` | When `cs_db%num_salts > 0` and salt state is initialized for each aquifer after the per-salt loops. | `asaltb_y(iaq)%salt(1)%diss` is reset to zero so the yearly dissolved-salt transfer accumulator starts from no prior value. |
| `asaltb_a(iaq)%salt(1)%diss` | When `cs_db%num_salts > 0` and salt state is initialized for each aquifer after the per-salt loops. | `asaltb_a(iaq)%salt(1)%diss` is reset to zero so the average-annual dissolved-salt transfer accumulator starts from no prior value. |
| `acsb_m(iaq)%cs(ics)%csgw` | When `cs_db%num_cs > 0` and each aquifer is being initialized in the monthly loop. | `acsb_m(iaq)%cs(ics)%csgw` is reset to zero so monthly groundwater loading for the generic constituent starts clean. |
| `acsb_m(iaq)%cs(ics)%rchrg` | When `cs_db%num_cs > 0` and each aquifer is being initialized in the monthly loop. | `acsb_m(iaq)%cs(ics)%rchrg` is reset to zero so monthly recharge mass for the constituent starts clean. |
| `acsb_m(iaq)%cs(ics)%seep` | When `cs_db%num_cs > 0` and each aquifer is being initialized in the monthly loop. | `acsb_m(iaq)%cs(ics)%seep` is reset to zero so monthly seepage mass for the constituent starts clean. |
| `acsb_m(iaq)%cs(ics)%irr` | When `cs_db%num_cs > 0` and each aquifer is being initialized in the monthly loop. | `acsb_m(iaq)%cs(ics)%irr` is reset to zero so monthly irrigation removal for the constituent starts clean. |
| `acsb_m(iaq)%cs(ics)%sorb` | When `cs_db%num_cs > 0` and each aquifer is being initialized in the monthly loop. | `acsb_m(iaq)%cs(ics)%sorb` is reset to zero so monthly sorbed-mass transfer starts clean. |
| `acsb_m(iaq)%cs(ics)%rctn` | When `cs_db%num_cs > 0` and each aquifer is being initialized in the monthly loop. | `acsb_m(iaq)%cs(ics)%rctn` is reset to zero so monthly reaction mass starts clean. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:4.2.13 | Baseflow alpha from recession constant | $\alpha_{gw}=\frac{1}{N}*ln[\frac{Q_{gw,N}}{Q_{gw,0}}]$ | Verified against SWAT+ 62.0.0 (aqu_initial.f90:167). α_gw is an input; runtime use is `alpha_e = Exp(-alpha) |
| 2:4.2.14 | Alternative alpha relation with BFD | $\alpha_{gw}=\frac{1}{N}*ln[\frac{Q_{gw,N}}{Q_{gw,0}}]=\frac{1}{BFD}*ln[10]=\frac{2.3}{BFD}$ | The active routine reads alpha directly and stores exp(-alpha); the printed 2.3/BFD relationship is not recomputed in this checkout. |
| 3:1.9.7 | NO3 half-life to rate-constant relationship | $t_{1/2,NO3,sh}=\frac{0.693}{k_{NO3,sh}}$ | Verified against SWAT+ 62.0.0 (aqu_initial.f90:168). nloss = Exp(-.693/(hlife_n+.1))` — NO3 half-life→rate |

## Lineage

Resolved lineage evidence shows four behavior-changing commits in the source history plus one module-name fix. The routine began as a direct aquifer initializer, then 2405a68 changed the module imports to `salt_aquifer_module` and `cs_aquifer_module` for compilation, c7c8e22 added the initial aquifer allocation and parameter setup block from older upstream source, 6bbaf93 added explicit zeroing for several aquifer constituent arrays, f8bb6ec expanded initialization to allocate pesticide and constituent arrays with `source = 0.` in the aquifer loop, and 39fabde set the local loop counters to zero at declaration and made several constituent allocations and arrays explicitly zero-initialized.

- 2405a68 only changed the `use` statements to the module-form names `salt_aquifer_module` and `cs_aquifer_module` so the file would compile in that revision.
- c7c8e22 introduced the current aquifer initialization routine body, including the top-level allocations, salt and constituent balance loops, and aquifer parameter copy/seed logic.
- 6bbaf93 added zeroing for `cs_aqu(iaq)%pest`, `cs_aqu(iaq)%path`, and `cs_aqu(iaq)%hmet` after allocation, tightening the initialization of aquifer constituent storage.
- f8bb6ec changed several `cs_aqu(iaq)` and `aqupst_*` allocations to explicit source-initialized allocations, especially for pesticide and constituent storage.
- 39fabde initialized the loop counters at declaration and made more of the aquifer constituent allocations source-initialized, including `cs_aqu(iaq)%hmet`, `cs_aqu(iaq)%salt_min`, `cs_aqu(iaq)%saltc`, `cs_aqu(iaq)%csc`, `cs_aqu(iaq)%cs_sorb`, and `cs_aqu(iaq)%csc_sorb`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aqu_initial' has no extracted documentation comment.
