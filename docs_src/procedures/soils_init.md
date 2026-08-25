---
kind: procedure
symbol: soils_init
title: soils_init
status: filled
source_hash: 350c48eee53477e4
version_label: SWAT+ 62.0.0
locals:
  msoils: Maximum soil-record index to initialize; set from `db_mx%soil` and used to size
    and loop over the working soil database.
  isol: Loop index for the current soil record being copied, adjusted, and initialized.
  mlyr: Number of model layers to allocate for the current soil profile after any custom-depth
    adjustment.
  i: General loop counter used while building temporary millimeter-by-millimeter soil layers
    and while traversing layers during averaging.
  j: Layer loop counter used to copy source layer properties and to accumulate depth-weighted
    averages across soil layers.
  nly: Local copy of the HRU soil-layer count used when allocating HRU soil arrays and related
    state arrays.
  ly: HRU layer loop counter used when copying `sol(isol)` layer data into `soil(ihru)`.
  npl: Plant-count variable captured from `pcom(ihru)%npl`; it records how many plant entries
    the HRU has while allocating soil-state arrays.
  csld: Current custom soil-layer depth read from `soil_lyr_depths.sol`; it defines the requested
    layer boundary used to count and average layers.
  pcd: Previous custom depth boundary in millimeters; it marks the start of the current averaging
    window when aggregating temporary 1-mm soil data.
  prev_depth: Previous source-layer bottom depth in millimeters while expanding the source
    soil profile into a 1-mm temporary database.
  tot_soil_depth: Total depth of the source soil profile, in millimeters, used to limit custom
    layer processing and averaging.
  eof: I/O status flag returned by file reads from `soil_lyr_depths.sol`; used to detect end-of-file
    or read failure.
  n: Counter for how many 1-mm depth cells contribute to a layer average.
  dep_new1: Top depth of a new septic split layer, in millimeters, when a septic biozone boundary
    must be inserted.
  dep_new2: Bottom depth of a new septic split layer, in millimeters, when a septic biozone
    boundary must be inserted.
  sum_bd: Accumulator for bulk density values while averaging a layer from the temporary 1-mm
    soil profile.
  sum_awc: Accumulator for available water capacity values while averaging a layer from the
    temporary 1-mm soil profile.
  sum_cbn: Accumulator for organic carbon values while averaging a layer from the temporary
    1-mm soil profile.
  sum_k: Accumulator for saturated hydraulic conductivity values while averaging a layer from
    the temporary 1-mm soil profile.
  sum_clay: Accumulator for clay values while averaging a layer from the temporary 1-mm soil
    profile.
  sum_silt: Accumulator for silt values while averaging a layer from the temporary 1-mm soil
    profile.
  sum_sand: Accumulator for sand values while averaging a layer from the temporary 1-mm soil
    profile.
  sum_rock: Accumulator for rock-fragment values while averaging a layer from the temporary
    1-mm soil profile.
  sum_alb: Accumulator for soil albedo values while averaging a layer from the temporary 1-mm
    soil profile.
  sum_usle_k: Accumulator for USLE K values while averaging a layer from the temporary 1-mm
    soil profile.
  sum_ec: Accumulator for electrical conductivity values while averaging a layer from the
    temporary 1-mm soil profile.
  sum_cal: Accumulator for calcium carbonate values while averaging a layer from the temporary
    1-mm soil profile.
  sum_ph: Accumulator for pH values while averaging a layer from the temporary 1-mm soil profile.
  i_exist: Logical file-existence flag returned by `inquire` for `soil_lyr_depths.sol`.
  header: Second header line read from `soil_lyr_depths.sol` before the custom depths are
    processed.
  titldum: First title line read from `soil_lyr_depths.sol` before the custom depths are processed.
  units: Units label line read from `soil_lyr_depths.sol` before the custom depths are processed.
  first_layer_flag: Tracks whether the first output layer has been created so the routine
    can force a 10 mm surface layer and backspace the input stream once.
  sol_mm_db: Temporary in-memory 1-mm soil database used to hold copied source-layer values
    before they are depth-averaged into custom output layers.
uses:
  hru_module: The HRU module provides the HRU count and soil/septic indexing that `soils_init`
    needs to map each HRU to the correct soil record and septic configuration. Without `hru`,
    `wfsh`, `ihru`, `isep`, `iseptic`, and `i_sep`, the routine could not assign soils to
    HRUs or decide where to insert septic biozone layers.
  soil_module: The soil module holds the working soil profiles that `soils_init` builds and
    the layer objects it fills. The routine copies profile metadata and layer properties into
    `sol`, then later routines rely on those initialized `soil_module` records for hydrology,
    erosion, and constituent calculations.
  plant_module: The plant module matters because `soils_init` reads each HRU's plant count
    from `pcom(ihru)%npl` while sizing the soil-state setup for that HRU. That count is part
    of the per-HRU initialization context even though this routine does not modify plant data.
  maximum_data_module: The maximum-data module supplies `db_mx%soil`, which tells `soils_init`
    how many soil records to allocate and initialize. That value bounds the main soil loop
    and determines the size of the working `sol` array.
  soil_data_module: The soil-data module contains the source soil database that `soils_init`
    copies from. Its profile fields and layer records provide the baseline soil names, depths,
    and properties that are transferred into the working `sol` database before any custom-depth
    reshaping.
  organic_mineral_mass_module: The organic and mineral mass module matters because `soils_init`
    allocates the HRU-level carbon, sediment, residue, and nutrient state arrays stored there.
    Those arrays must match the soil-layer count created here so later carbon and nutrient
    routines can update per-layer mass pools.
  constituent_mass_module: The constituent mass module matters because `soils_init` prepares
    the per-layer storage arrays that later constituent transport and transformation routines
    use. The allocated arrays must exist before any constituent mass calculations can be attached
    to an HRU soil profile.
  hydrograph_module: The hydrograph module matters because `sp_ob%hru` controls the number
    of HRUs that `soils_init` iterates over when assigning soil profiles and allocating HRU
    soil state. It is the loop bound for the HRU-level initialization phase.
  time_module: The time module matters because soil initialization is part of the model start-up
    state that must be ready before time-stepping begins. Even though no time variable is
    directly assigned here in the extracted source, the module is part of the initialization
    context that drives when this routine runs.
  basin_module: The basin module matters because `soils_init` builds basin-wide shared soil
    state used across HRUs. The routine's outputs populate the basin-level soil structures
    that later basin hydrology, nutrient, and routing code reads.
  septic_data_module: The septic-data module matters because `soils_init` checks septic options
    and septic zone depth/thickness while deciding whether to split a soil layer for a biozone.
    Those septic parameters determine if the HRU soil profile must be modified before later
    routines run.
---

<!-- facts:header -->

Builds the working soil database for the run from `soildb`, optionally inserts custom depth layers, and initializes each HRU's soil and soil-state arrays. It also handles septic-zone layer splits and prepares soil physics for later hydrology and biogeochemistry routines.

## Bottom Line

`soils_init` is the main soil setup routine. It copies the configured soil database into the working `sol` array, optionally remaps soil layers from the `soil_lyr_depths.sol` custom-depth file, and then initializes derived soil physical properties for every soil record.

After the soil database is ready, it assigns each HRU its soil profile, creates septic biozone splits when needed, and allocates the layer arrays used by carbon, nutrient, sediment, and water-state routines. The routine runs during HRU processing before structure, plant, CN, and hydrograph initialization.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`soils_init` runs during HRU setup in `proc_hru`, immediately after septic parameters are assigned and before structure, plant, CN, and hydrograph initialization. Its results define the soil profiles and layer arrays that those later routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Size and seed the working soil database | Determine the number of soil records from `db_mx%soil`, allocate `sol(0:msoils)`, and copy the profile name, hydrologic group, maximum depth, anion exclusion, crack potential, and texture from `soildb` into the working soil records. |
| 2. Choose between default layering and custom-depth processing | Check whether `soil_lyr_depths.sol` exists. If it does not, set the working layer count from the source soil and allocate the working layer and physical-property arrays for a simple copy path. |
| 3. Copy or shift the source layers into the working profile | Create the first 10 mm surface layer from the source soil properties, then either shift the remaining source layers down by one slot when the first source layer is deeper than 19.5 mm or copy them directly when it is not. |
| 4. Expand source soil data into a 1-mm temporary profile | If custom depths are requested, build a temporary millimeter-by-millimeter soil database from the source layers so later depth averaging can be performed over arbitrary layer boundaries. |
| 5. Scan the custom-depth file and count output layers | Open `soil_lyr_depths.sol`, read its title/header/unit lines, then scan depth breakpoints to determine how many model layers will be needed and clamp the total depth to the last requested boundary. |
| 6. Allocate the custom-depth working arrays | Allocate the working `sol(isol)%ly` and `sol(isol)%phys` arrays using the counted layer total so the averaged custom profile can be written back. |
| 7. Rewind and reread the depth file for averaging | Rewind the custom-depth file and reread the header records so the subsequent layer-building loop starts from the beginning of the file. |
| 8. Average 1-mm values into each model layer | For each output layer, locate the corresponding depth range in the temporary 1-mm profile, sum the layer properties across that range, and write the mean values back into the working soil profile. |
| 9. Clean up the temporary file and database | Deallocate the temporary 1-mm soil database and close `soil_lyr_depths.sol` after the custom-depth profile has been built. |
| 10. Apply soil-test adjustments when present | If soil-test data are allocated, call `soils_test_adjust` so any matching profile corrections are applied to the current soil record before physics initialization. |
| 11. Initialize the physical soil parameters | Loop over all soil records and call `soil_phys_init` for each one to derive the working physical properties used by later model routines. |
| 12. Map working soils onto each HRU and derive wetness | For every HRU, look up the assigned soil record, compute `wfsh` from the top-layer porosity and texture terms, copy the soil profile into `soil(ihru)`, and allocate HRU layer arrays sized to that soil's layer count. |
| 13. Insert septic biozone splits when needed | If the HRU has an active septic system, compare septic depth and thickness with the soil-layer boundaries, choose split depths, and call `layersplit` for any nontrivial split boundaries. |
| 14. Allocate the HRU soil-state arrays | Use the final HRU layer count to allocate the carbon, sediment, residue, nutrient, and related soil-state arrays in `soil1` and `soil1_init` for every HRU. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, wfsh, ihru, isep, iseptic, i_sep` | `hru, wfsh, ihru, isep, iseptic, i_sep` |
| [sym:soil_module] | `sol` | `sol(isol)%s%snam, sol(isol)%s%hydgrp, sol(isol)%s%zmx, sol(isol)%s%anion_excl, sol(isol)%s%crk, sol(isol)%s%texture, sol(isol)%s%nly, sol(isol)%ly(mlyr), sol(isol)%phys(mlyr), sol(isol)%phys(1)%d, sol(isol)%phys(1)%bd, sol(isol)%phys(1)%awc, sol(isol)%phys(1)%k, sol(isol)%phys(1)%cbn, sol(isol)%phys(1)%clay, sol(isol)%phys(1)%silt, sol(isol)%phys(1)%sand, sol(isol)%phys(1)%rock, sol(isol)%ly(1)%alb, sol(isol)%ly(1)%usle_k, sol(isol)%ly(1)%ec, sol(isol)%ly(1)%cal, sol(isol)%ly(1)%ph, sol(isol)%phys(j)%d, sol(isol)%phys(j)%bd, sol(isol)%phys(j)%awc, sol(isol)%phys(j)%k, sol(isol)%phys(j)%cbn, sol(isol)%phys(j)%clay, sol(isol)%phys(j)%silt, sol(isol)%phys(j)%sand, sol(isol)%phys(j)%rock, sol(isol)%ly(j)%alb, sol(isol)%ly(j)%usle_k, sol(isol)%ly(j)%ec, sol(isol)%ly(j)%cal, sol(isol)%ly(j)%ph` |
| [sym:plant_module] | `pcom` | `pcom(ihru)%npl` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%soil` |
| [sym:soil_data_module] | `soildb` | `soildb(isol)%s%snam, soildb(isol)%s%hydgrp, soildb(isol)%s%zmx, soildb(isol)%s%anion_excl, soildb(isol)%s%crk, soildb(isol)%s%texture, soildb(isol)%ly(1)%z, soildb(isol)%s%nly, soildb(isol)%ly(1)%bd, soildb(isol)%ly(1)%awc, soildb(isol)%ly(1)%k, soildb(isol)%ly(1)%cbn, soildb(isol)%ly(1)%clay, soildb(isol)%ly(1)%silt, soildb(isol)%ly(1)%sand, soildb(isol)%ly(1)%rock, soildb(isol)%ly(1)%alb, soildb(isol)%ly(1)%usle_k, soildb(isol)%ly(1)%ec, soildb(isol)%ly(1)%cal, soildb(isol)%ly(1)%ph, soildb(isol)%ly(j-1)%z, soildb(isol)%ly(j-1)%bd, soildb(isol)%ly(j-1)%awc, soildb(isol)%ly(j-1)%k, soildb(isol)%ly(j-1)%cbn, soildb(isol)%ly(j-1)%clay, soildb(isol)%ly(j-1)%silt, soildb(isol)%ly(j-1)%sand, soildb(isol)%ly(j-1)%rock, soildb(isol)%ly(j-1)%alb, soildb(isol)%ly(j-1)%usle_k, soildb(isol)%ly(j-1)%ec, soildb(isol)%ly(j-1)%cal, soildb(isol)%ly(j-1)%ph, soildb(isol)%ly(j)%z, soildb(isol)%ly(j)%bd, soildb(isol)%ly(j)%awc, soildb(isol)%ly(j)%k, soildb(isol)%ly(j)%cbn, soildb(isol)%ly(j)%clay, soildb(isol)%ly(j)%silt` |
| [sym:organic_mineral_mass_module] | `soil1, soil1_init` | `soil1(ihru)%sw(nly), soil1(ihru)%cbn(nly), soil1(ihru)%sed(nly), soil1(ihru)%rsd_tot(nly), soil1(ihru)%emix(nly), soil1(ihru)%root_tot(nly), soil1(ihru)%mn(nly), soil1(ihru)%mp(nly), soil1(ihru)%tot(nly), soil1(ihru)%seq(nly), soil1(ihru)%org_con_lr(nly), soil1(ihru)%org_allo_lr(nly), soil1(ihru)%org_ratio_lr(nly), soil1(ihru)%org_tran_lr(nly), soil1(ihru)%org_flx_lr(nly), soil1(ihru)%org_flx_cum_lr(nly), soil1(ihru)%hact(nly), soil1(ihru)%hsta(nly), soil1(ihru)%str(nly), soil1(ihru)%lig(nly), soil1(ihru)%nonlig(nly), soil1(ihru)%meta(nly), soil1(ihru)%hs(nly), soil1(ihru)%hp(nly), soil1(ihru)%microb(nly), soil1(ihru)%man(nly), soil1(ihru)%water(nly), soil1_init(ihru)%sw(nly), soil1_init(ihru)%cbn(nly), soil1_init(ihru)%sed(nly), soil1_init(ihru)%mn(nly), soil1_init(ihru)%mp(nly), soil1_init(ihru)%tot(nly), soil1_init(ihru)%seq(nly), soil1_init(ihru)%hact(nly), soil1_init(ihru)%hsta(nly), soil1_init(ihru)%str(nly), soil1_init(ihru)%lig(nly), soil1_init(ihru)%nonlig(nly), soil1_init(ihru)%meta(nly), soil1_init(ihru)%hs(nly), soil1_init(ihru)%hp(nly), soil1_init(ihru)%microb(nly), soil1_init(ihru)%man(nly), soil1_init(ihru)%water(nly)` |
| [sym:constituent_mass_module] | `soil1, soil1_init` | `soil1(ihru)%sw(nly), soil1(ihru)%cbn(nly), soil1(ihru)%sed(nly), soil1(ihru)%rsd_tot(nly), soil1(ihru)%emix(nly), soil1(ihru)%root_tot(nly), soil1(ihru)%mn(nly), soil1(ihru)%mp(nly), soil1(ihru)%tot(nly), soil1(ihru)%seq(nly), soil1(ihru)%org_con_lr(nly), soil1(ihru)%org_allo_lr(nly), soil1(ihru)%org_ratio_lr(nly), soil1(ihru)%org_tran_lr(nly), soil1(ihru)%org_flx_lr(nly), soil1(ihru)%org_flx_cum_lr(nly), soil1(ihru)%hact(nly), soil1(ihru)%hsta(nly), soil1(ihru)%str(nly), soil1(ihru)%lig(nly), soil1(ihru)%nonlig(nly), soil1(ihru)%meta(nly), soil1(ihru)%hs(nly), soil1(ihru)%hp(nly), soil1(ihru)%microb(nly), soil1(ihru)%man(nly), soil1(ihru)%water(nly), soil1_init(ihru)%sw(nly), soil1_init(ihru)%cbn(nly), soil1_init(ihru)%sed(nly), soil1_init(ihru)%mn(nly), soil1_init(ihru)%mp(nly), soil1_init(ihru)%tot(nly), soil1_init(ihru)%seq(nly), soil1_init(ihru)%hact(nly), soil1_init(ihru)%hsta(nly), soil1_init(ihru)%str(nly), soil1_init(ihru)%lig(nly), soil1_init(ihru)%nonlig(nly), soil1_init(ihru)%meta(nly), soil1_init(ihru)%hs(nly), soil1_init(ihru)%hp(nly), soil1_init(ihru)%microb(nly), soil1_init(ihru)%man(nly), soil1_init(ihru)%water(nly)` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob` |
| [sym:time_module] | `time, yrc` | `time, yrc` |
| [sym:basin_module] | `basin, soildb, soil, soil1, soil1_init, sep, pcom` | `basin, soildb, soil, soil1, soil1_init, sep, pcom` |
| [sym:septic_data_module] | `sep` | `sep(isep)%opt, sep(isep)%z, sep(isep)%thk` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sol(isol)%s%snam` | During the soil-copy phase for every soil record, before any custom-depth remapping or soil-test adjustment. | `sol(isol)%s%snam` is set from the source soil database so the working soil record carries the soil series name used by later HRU assignment and diagnostics. |
| `sol(isol)%s%hydgrp` | During the soil-copy phase for every soil record, before any custom-depth remapping or soil-test adjustment. | `sol(isol)%s%hydgrp` is copied from the source database so later hydrology and wetness calculations can use the correct hydrologic soil group. |
| `sol(isol)%s%zmx` | During the soil-copy phase for every soil record, before any custom-depth remapping or soil-test adjustment. | `sol(isol)%s%zmx` is copied from the source database so the working profile retains the maximum rooting depth used later by soil and plant routines. |
| `sol(isol)%s%anion_excl` | During the soil-copy phase for every soil record, before any custom-depth remapping or soil-test adjustment. | `sol(isol)%s%anion_excl` is copied from the source database so the working soil profile preserves the anion exclusion fraction used in later transport behavior. |
| `sol(isol)%s%crk` | During the soil-copy phase for every soil record, before any custom-depth remapping or soil-test adjustment. | `sol(isol)%s%crk` is copied from the source database so the working soil profile retains the crack-volume potential used in later soil-water calculations. |
| `sol(isol)%s%texture` | During the soil-copy phase for every soil record, before any custom-depth remapping or soil-test adjustment. | `sol(isol)%s%texture` is copied from the source database so the working record keeps the texture label associated with the soil profile. |
| `sol(isol)%s%nly` | For each source soil record after the copy phase and after any custom-depth adjustment has determined the final number of layers. | `sol(isol)%s%nly` is set to the final layer count for the working soil profile, including any added surface layer or custom-depth remapping. |
| `sol(isol)%phys(1)%d` | When a soil profile is loaded, either on the simple copy path or after custom-depth averaging, for the first layer record. | `sol(isol)%phys(1)%d` stores the depth to the bottom of the first layer, set to 10 mm for the added surface layer. |
| `sol(isol)%phys(1)%bd` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%bd` is populated with the first-layer bulk density used by later soil physics. |
| `sol(isol)%phys(1)%awc` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%awc` is populated with the first-layer available water capacity used by later water-storage calculations. |
| `sol(isol)%phys(1)%k` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%k` is populated with the first-layer saturated hydraulic conductivity used by later flow calculations. |
| `sol(isol)%phys(1)%cbn` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%cbn` is populated with the first-layer organic-carbon content used by later biogeochemical routines. |
| `sol(isol)%phys(1)%clay` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%clay` is populated with the first-layer clay fraction used by later soil-physics and texture-based calculations. |
| `sol(isol)%phys(1)%silt` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%silt` is populated with the first-layer silt fraction used by later soil-physics and erosion calculations. |
| `sol(isol)%phys(1)%sand` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%sand` is populated with the first-layer sand fraction used by later soil-physics and erosion calculations. |
| `sol(isol)%phys(1)%rock` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%phys(1)%rock` is populated with the first-layer rock-fragment fraction used by later soil-physics calculations. |
| `sol(isol)%ly(1)%alb` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%ly(1)%alb` is populated with the surface-layer albedo used later in energy and moisture-related calculations. |
| `sol(isol)%ly(1)%usle_k` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%ly(1)%usle_k` is populated with the first-layer USLE erodibility factor used later by erosion routines. |
| `sol(isol)%ly(1)%ec` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%ly(1)%ec` is populated with the first-layer electrical conductivity used later by soil chemistry routines. |
| `sol(isol)%ly(1)%cal` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%ly(1)%cal` is populated with the first-layer calcium carbonate content used later by soil chemistry routines. |
| `sol(isol)%ly(1)%ph` | When the first layer of a soil profile is created from the source soil or custom-depth averages. | `sol(isol)%ly(1)%ph` is populated with the first-layer pH used later by soil chemistry routines. |
| `sol(isol)%phys(j)%d` | For each layer deeper than the surface layer, during either the simple copy path or the custom-depth averaging path. | `sol(isol)%phys(j)%d` stores the bottom depth of the j-th working soil layer so later routines can use the final layer boundaries. |
| `sol(isol)%phys(j)%bd` | For each layer deeper than the surface layer, during either the simple copy path or the custom-depth averaging path. | `sol(isol)%phys(j)%bd` stores the averaged or copied bulk density for layer j so later soil physics can use the final value. |
| `sol(isol)%phys(j)%awc` | For each layer deeper than the surface layer, during either the simple copy path or the custom-depth averaging path. | `sol(isol)%phys(j)%awc` stores the averaged or copied available water capacity for layer j so later soil-water routines can use the final value. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 4:1.1.2 | K_USLE Wischmeier-Smith formula | $K_{USLE}=\frac{0.00021*M^{1.14}*(12-OM)+3.25*(c_{soilstr}-2)+2.5*(c_{perm}-3)}{100}$ | usle_k is read from the soil database, not computed from soil texture at runtime. Lines 91/108/126 load the parameter value; the K formula from sand/silt/clay/OM is applied offline by the user. |
| 4:1.1.3 | Texture parameter M | $M=(m_{silt}+m_{vfs})*(100-m_c)$ | Derivation component of K_USLE (Wischmeier-Smith). Not computed in code; K_USLE is read as an input parameter. |
| 4:1.1.4 | Organic matter OM = 1.72*orgC | $OM=1.72*orgC$ | Derivation component of K_USLE. Not computed in code. |
| 4:1.1.5 | K_USLE EPIC alternative formula | $K_{USLE}=f_{csand}*f_{cl-si}*f_{orgc}*f_{hisand}$ | EPIC texture-based K_USLE alternative. Not computed in code; read as a user parameter. |
| 4:1.1.6 | f_csand factor | $f_{csand}=(0.2+0.3*exp[-0.256*m_s*(1-\frac{m_{silt}}{100})])$ | Component of EPIC K_USLE. Not computed in SWAT+ source; value provided via soil database. |
| 4:1.1.7 | f_cl-si factor | $f_{cl-si}=(\frac{m_{silt}}{m_c+m_{silt}})^{0.3}$ | Component of EPIC K_USLE. Not computed in SWAT+ source. |
| 4:1.1.8 | f_orgc factor | $f_{orgc}=(1-\frac{0.25*orgC}{orgC+exp[3.72-2.95*orgC]})$ | Component of EPIC K_USLE. Not computed in SWAT+ source. |
| 4:1.1.9 | f_hisand factor | $f_{hisand}=(1-\frac{0.7*(1-\frac{m_s}{100})}{(1-\frac{m_s}{100})+exp[-5.51+22.9*(1-\frac{m_s}{100})]})$ | Component of EPIC K_USLE. Not computed in SWAT+ source. |

## Lineage

`soils_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 41 non-merge commit(s) since, most recently `5323b15` (2026-05-13, "Initial changes to calculate non-lignin c and output to hru_cpool_stat"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `soils_init.f90` are listed.

- `5323b15` (2026-05-13) — Initial changes to calculate non-lignin c and output to hru_cpool_stat
- `0fee6d7` (2026-03-06) — Fixed issue with tillage events not happening in code when cswat=3 and added mixing efficiency to the output of hru_carbvars.txt and used ti…
- `febcf0c` (2026-01-27) — corrections to root distribution and tracking features to soil and plant modules
- `0d74307` (2026-01-07) — Fixed Warnings, removed unused variable declarations and update external function references
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'soils_init' has no extracted documentation comment.
- The extracted source shows `soils_init` uses `soil_lyr_depths.sol` as an optional custom layer-depth control file; the file layout is inferred from the header reads and numeric depth scans.
- The context packet did not resolve any lineage commits for this source span, so no behavior-changing commit history is available.
- plant_module candidate state is uncertain in the extracted source; `pcom(ihru)%npl` is visible in `soils_init.f90`, but the module ownership was not separately extracted.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
